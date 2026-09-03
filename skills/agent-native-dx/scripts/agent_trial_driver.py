#!/usr/bin/env python3
"""Run a pre-registered agent trial and write the trial log. Stdlib only.

An operator procedure, never CI. Dry run by default: pass --execute to run.

The driver holds no credentials and speaks to no model. It shells out to the agent
command declared in the registration, so the harness the operator already has
installed and authenticated is the harness under test. Commands run without a shell.

Outcome is decided by each task's committed verify command, not by reading the
transcript. A task whose verify command exits 0 passed. Nothing here classifies
failures: that is the operator's job, per references/trial-protocol.md.
"""
import argparse, hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path

SCHEMA = 'agent-trial-log/v1'
ID_OK = re.compile(r'^[A-Za-z0-9._-]+$')
REQUIRED_REG = ('repositories', 'task_prompts', 'model', 'checkpoint', 'temperature',
                'harness', 'harness_command', 'tool_set', 'codebook_version',
                'coverage_corpus', 'registered_at', 'registration_url')
MIN_RUNS_PER_TASK = 5
DEFAULT_TIMEOUT_S = 1800


def die(msg):
    raise SystemExit(f'{msg}')


def load_registration(path):
    try:
        log = json.loads(Path(path).read_text())
    except FileNotFoundError:
        die(f'No such file: {path}\nStart one with agent_trial_scorer.py --new {path}')
    except json.JSONDecodeError as e:
        die(f'{path} is not valid JSON: {e}')
    if not isinstance(log, dict):
        die(f'{path}: expected a JSON object')
    if log.get('schema') != SCHEMA:
        die(f'{path}: schema must be {SCHEMA!r}, got {log.get("schema")!r}. '
            'The scorer will not read a log without it.')
    reg = log.get('registration')
    if not isinstance(reg, dict):
        die(f'{path}: no registration. A trial must be registered before it is run.')

    missing = [f for f in REQUIRED_REG if f not in reg or reg[f] in ('', [], {}, None)]
    if missing:
        die(f'{path}: registration incomplete: {", ".join(missing)}\n'
            'Publish the full registration before running. Registering afterwards does '
            'not count, and the scorer refuses a log without it.')

    tasks = reg['task_prompts']
    if not isinstance(tasks, list) or not tasks:
        die(f'{path}: registration.task_prompts must be a non-empty list')
    for t in tasks:
        if not isinstance(t, dict) or not t.get('id') or not t.get('prompt'):
            die(f'{path}: every task needs an id and a prompt')
        if not t.get('verify'):
            die(f'{path}: task {t.get("id")!r} has no verify command.\n'
                'Outcome must be decided by a committed command, not by reading the '
                'transcript afterwards. Add "verify": ["cmd", "arg"].')
        if not ID_OK.match(str(t['id'])):
            die(f'{path}: task id {t["id"]!r} must match [A-Za-z0-9._-]+, because it '
                'becomes part of a transcript filename')
        if not isinstance(t['verify'], list):
            die(f'{path}: task {t["id"]!r} verify must be a list of arguments, so it can '
                'run without a shell')
    if not isinstance(reg['harness_command'], list) or not reg['harness_command']:
        die(f'{path}: registration.harness_command must be a non-empty argument list, '
            'for example ["claude", "-p", "{prompt}"]')
    if not any('{prompt}' in str(x) for x in reg['harness_command']):
        die(f'{path}: registration.harness_command must contain {{prompt}} somewhere, so '
            'the driver knows where to put the task prompt')
    return log, reg


def done_runs(log):
    """Runs already recorded, so a trial resumes instead of repeating paid sessions."""
    seen = {}
    for r in log.get('runs') or []:
        if isinstance(r, dict) and r.get('repository') and r.get('task'):
            seen[(r['repository'], r['task'])] = len(r.get('outcomes') or [])
    return seen


def plan(reg, n, seen):
    rows = []
    for repo in reg['repositories']:
        for task in reg['task_prompts']:
            have = seen.get((repo, task['id']), 0)
            rows.append({'repository': repo, 'task': task['id'], 'have': have,
                         'todo': max(0, n - have)})
    return rows


def slug(repo):
    """Short, collision-resistant, filesystem-safe stem for transcript names."""
    s = repo.rstrip('/').split('://')[-1]
    parts = [x for x in s.replace(':', '/').split('/') if x not in ('', '.', '..')][-2:]
    stem = '__'.join(parts)[:44] or 'repo'
    # Two forges can host the same owner/name, and truncation can collide. The digest
    # is over the full registered identifier, so distinct repositories never share a
    # transcript file.
    return f'{stem}-{hashlib.sha256(repo.encode()).hexdigest()[:8]}'


def clone(repo, workdir):
    """Clone into a fresh directory per session. Nothing is ever deleted.

    A named, reused directory was both a correctness bug (sessions after the first
    started in the state the previous one left, so N runs were serially correlated
    rather than independent) and a safety bug (a repository entry of ".." made the
    destination the parent of the scratch directory, which was then removed).
    """
    dest = Path(tempfile.mkdtemp(prefix='session-', dir=str(workdir))) / 'repo'
    url = repo if repo.startswith(('http', 'git@', 'file://')) else f'https://github.com/{repo}.git'
    cp = subprocess.run(['git', 'clone', '--depth', '1', url, str(dest)],
                        capture_output=True, text=True, timeout=600)
    if cp.returncode != 0:
        return None, (cp.stderr.strip().splitlines() or ['clone failed'])[-1]
    return dest, None


def run_verify(task, cwd, timeout=600):
    """Run a task's verify command. Returns (exit_code_or_None, output, error_or_None)."""
    try:
        v = subprocess.run(task['verify'], cwd=str(cwd), capture_output=True,
                           text=True, timeout=timeout)
        return v.returncode, (v.stdout or '') + (v.stderr or ''), None
    except subprocess.TimeoutExpired:
        return None, '', 'verify timed out'
    except FileNotFoundError:
        return None, '', f'verify command not found: {task["verify"][0]}'
    except OSError as e:
        return None, '', f'verify could not run: {e}'


def harness_sanity(reg, repo, workdir):
    """Prove the harness can change a working tree before spending a whole trial.

    Found by a pilot run: a headless agent CLI defaulted to blocking writes, exited 0,
    and changed nothing. Every session would have recorded a failure, and the trial
    would have reported a large uncovered share that was entirely harness artifact.
    Preflight checks that verify discriminates; that is not the same as checking that
    the harness can do anything at all.
    """
    checkout, err = clone(repo, workdir)
    if checkout is None:
        die(f'harness check: cannot clone {repo}: {err}')
    probe = 'agent-trial-harness-probe.txt'
    prompt = (f'Create a file named {probe} at the repository root containing the single '
              'word ok. Do nothing else.')
    cmd = [str(x).replace('{prompt}', prompt) for x in reg['harness_command']]
    try:
        cp = subprocess.run(cmd, cwd=str(checkout), capture_output=True, text=True,
                            timeout=600)
    except subprocess.TimeoutExpired:
        die('harness check: the harness did not finish a trivial task within 600s.')
    except FileNotFoundError:
        die(f'harness command not found: {cmd[0]}')
    if not (checkout / probe).exists():
        tail = ((cp.stdout or '') + (cp.stderr or '')).strip().splitlines()
        hint = tail[0] if tail else '(no output)'
        die('harness check: the harness ran and exited '
            f'{cp.returncode} but did not create a file when asked to.\n'
            f'First line of its output: {hint}\n'
            'Every session would record a failure that is the harness, not the product. '
            'Grant the harness permission to edit files, then re-run.')
    print(f'  harness can modify a working tree (exit {cp.returncode})')


def preflight(reg, tasks_todo, workdir):
    """Prove each verify command runs and fails before an agent has touched anything.

    Without this, a typo in a verify command records five paid sessions as agent
    failures, and a verify that passes on an untouched tree records five as passes.
    Both are infrastructure errors indistinguishable from evidence in the log.
    """
    print('Preflight: checking the harness and each verify command before spending.')
    first_repo = sorted(tasks_todo)[0][0] if tasks_todo else None
    if first_repo:
        harness_sanity(reg, first_repo, workdir)
    for repo, tid in sorted(tasks_todo):
        task = {t['id']: t for t in reg['task_prompts']}[tid]
        checkout, err = clone(repo, workdir)
        if checkout is None:
            die(f'preflight: cannot clone {repo}: {err}')
        rc, _, verr = run_verify(task, checkout)
        if verr:
            die(f'preflight: task {tid!r} on {repo}: {verr}\n'
                'Fix the verify command before spending any sessions.')
        if rc == 0:
            die(f'preflight: task {tid!r} verify passes on {repo} before the agent has '
                'run.\nIt does not test the task, so every session would record a pass '
                'regardless of what the agent did. Make it fail on an untouched clone.')
        print(f'  {repo} {tid}: verify exits {rc} on an untouched clone, as it must')
    print()


def one_run(reg, task, repo, workdir, timeout, transcript_path):
    """One session: a fresh clone, one agent invocation, one verify. Never reuses a tree."""
    checkout, err = clone(repo, workdir)
    if checkout is None:
        return None, f'clone failed: {err}'

    cmd = [str(x).replace('{prompt}', task['prompt']) for x in reg['harness_command']]
    try:
        agent = subprocess.run(cmd, cwd=str(checkout), capture_output=True, text=True,
                               timeout=timeout)
        agent_out, agent_rc, timed_out = (agent.stdout or '') + (agent.stderr or ''), \
            agent.returncode, False
    except subprocess.TimeoutExpired as e:
        # Keep what the agent produced before the timeout; it is the only record of
        # a session that was paid for.
        agent_out = (e.stdout or b'').decode('utf-8', 'replace') if isinstance(e.stdout, bytes) \
            else (e.stdout or '')
        agent_out += (e.stderr or b'').decode('utf-8', 'replace') if isinstance(e.stderr, bytes) \
            else (e.stderr or '')
        agent_rc, timed_out = None, True
    except FileNotFoundError:
        die(f'harness command not found: {cmd[0]}\n'
            'Install the agent CLI named in registration.harness_command, or correct it.')

    verify_rc, verify_out, verify_err = run_verify(task, checkout)
    if verify_err:
        # An infrastructure error is not an agent failure. Preflight should have caught
        # this, so treat a late one as fatal rather than recording it as evidence.
        return None, verify_err
    outcome = 'pass' if verify_rc == 0 else 'fail'

    transcript_path.write_text(
        f'# repository {repo}\n# task {task["id"]}\n'
        f'# harness {" ".join(cmd[:1])} rc {agent_rc}, timed out {timed_out}\n'
        f'# verify {" ".join(task["verify"])} rc {verify_rc}\n# outcome {outcome}\n'
        f'# clone {checkout}\n\n'
        f'--- agent ---\n{agent_out}\n\n--- verify ---\n{verify_out}\n')
    return outcome, None


def main():
    ap = argparse.ArgumentParser(
        description='Run a pre-registered agent trial. Dry run unless --execute. '
                    'See references/trial-protocol.md.')
    ap.add_argument('log', help='trial log carrying the published registration')
    ap.add_argument('--execute', action='store_true', help='actually run the agent sessions')
    ap.add_argument('-n', type=int, default=MIN_RUNS_PER_TASK,
                    help=f'runs per repository and task (minimum {MIN_RUNS_PER_TASK})')
    ap.add_argument('--transcripts', metavar='DIR', default='trial-transcripts',
                    help='where to write per-session transcripts for classification')
    ap.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT_S,
                    help='seconds per agent session')
    ap.add_argument('--workdir', metavar='DIR', help='scratch clones (default: a temp dir)')
    a = ap.parse_args()

    if a.n < MIN_RUNS_PER_TASK:
        die(f'-n must be at least {MIN_RUNS_PER_TASK}. Below that a single lucky or '
            'unlucky session decides the result.')

    log, reg = load_registration(a.log)
    seen = done_runs(log)
    rows = plan(reg, a.n, seen)
    todo = sum(r['todo'] for r in rows)

    print(f'Registration {reg["registered_at"]}  {reg["registration_url"]}')
    print(f'Harness      {reg["harness"]}, {reg["model"]} @ {reg["checkpoint"]}, '
          f'temperature {reg["temperature"]}')
    print(f'Command      {" ".join(str(x) for x in reg["harness_command"])}')
    for task in reg['task_prompts']:
        print(f'Verify {task["id"]:6} {" ".join(str(x) for x in task["verify"])}')
    print(f'Plan         {len(reg["repositories"])} repositories x '
          f'{len(reg["task_prompts"])} tasks x {a.n} runs')
    print()
    for r in rows:
        state = 'done' if not r['todo'] else (f'{r["todo"]} to run'
                                              + (f', {r["have"]} recorded' if r['have'] else ''))
        print(f'  {r["repository"]:32} {r["task"]:8} {state}')
    print(f'\n{todo} agent session(s) to run, {sum(r["have"] for r in rows)} already recorded.')

    if not a.execute:
        print('\nDry run. Nothing was executed and no credentials were used.')
        print('Each session runs the agent against a fresh shallow clone in a scratch')
        print('directory; your own checkouts are never touched. The agent runs with')
        print('whatever permissions your harness grants it.')
        print('The agent inherits your environment, and everything it prints is written')
        print('unredacted to the transcripts you will read. Run trials with credentials')
        print('that can absorb that.')
        print(f'\nPass --execute to run. Estimated cost is {todo} agent sessions on your '
              'own metered account.')
        return 0

    if not todo:
        print('\nNothing to run.')
        return 0

    try:
        Path(a.log).write_text(Path(a.log).read_text())
    except OSError as e:
        die(f'cannot write {a.log}: {e}\nThe log is rewritten after every session.')
    workdir = a.workdir or tempfile.mkdtemp(prefix='agent-trial-')
    Path(workdir).mkdir(parents=True, exist_ok=True)
    tdir = Path(a.transcripts)
    try:
        tdir.mkdir(parents=True, exist_ok=True)
        probe = tdir / '.write-probe'
        probe.write_text('')
        probe.unlink()
    except OSError as e:
        die(f'cannot write transcripts to {tdir}: {e}')
    tasks = {t['id']: t for t in reg['task_prompts']}
    log.setdefault('runs', [])
    runs = {(r['repository'], r['task']): r for r in log['runs']
            if isinstance(r, dict) and r.get('repository') and r.get('task')}

    todo_pairs = {(r['repository'], r['task']) for r in rows if r['todo']}
    preflight(reg, todo_pairs, workdir)

    print(f'Executing. Transcripts to {tdir}/, clones under {workdir}/\n')
    try:
        for row in rows:
            if not row['todo']:
                continue
            repo, tid = row['repository'], row['task']
            rec = runs.setdefault((repo, tid), {'repository': repo, 'task': tid,
                                                'n': 0, 'outcomes': []})
            for _ in range(row['todo']):
                idx = len(rec['outcomes']) + 1
                tp = tdir / f'{slug(repo)}.{tid}.{idx:02d}.txt'
                outcome, err = one_run(reg, tasks[tid], repo, workdir, a.timeout, tp)
                if outcome is None:
                    print(f'  {repo} {tid} run {idx}: skipped, {err}')
                    break
                rec['outcomes'].append(outcome)
                rec['n'] = len(rec['outcomes'])
                print(f'  {repo} {tid} run {idx}: {outcome}  ({tp.name})')
                # Persist after every session so a paid run is never lost to a crash.
                log['runs'] = sorted(runs.values(),
                                     key=lambda r: (r['repository'], r['task']))
                Path(a.log).write_text(json.dumps(log, indent=2) + '\n')
    except KeyboardInterrupt:
        done = sum(len(r.get('outcomes') or []) for r in log.get('runs') or [])
        print(f'\n\nInterrupted. {done} session(s) recorded and written to {a.log}. '
              'Re-run to resume; recorded sessions are not repeated.')
        return 1

    failed = sum(1 for r in log['runs'] for o in (r.get('outcomes') or []) if o != 'pass')
    total = sum(len(r.get('outcomes') or []) for r in log['runs'])
    print(f'\n{total} sessions recorded, {failed} failed. Written to {a.log}')
    print(f'\nNext: read the {failed} failed transcript(s) in {tdir}/, group them into')
    print('distinct failure modes per references/trial-protocol.md, and record each one')
    print(f'in failure_modes with its coverage call. Then score with:')
    print(f'  python3 agent_trial_scorer.py {a.log}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
