#!/usr/bin/env python3
"""Score a pre-registered agent trial. Offline, deterministic, stdlib only.

A trial runs agents against real repositories and records how they fail. This
script reads the resulting log and answers one question: do the failures point
at something the existing skills already catch, or at a real gap?

See references/trial-protocol.md for the procedure. Start a new trial with
--new, understand the rule with --explain, share a result with --html.
"""
import argparse, html, json
from pathlib import Path

SCHEMA = 'agent-trial-log/v1'
MIN_DISTINCT_MODES = 15
COVERED_MAX = 0.20
GAP_MIN = 0.40
SECOND_RATER_MIN_FRACTION = 0.2
MIN_RUNS_PER_TASK = 5

REGISTRATION_FIELDS = {
    'registered_at': 'the date the trial was registered, before any run',
    'registration_url': 'the pull request where the registration was published',
    'repositories': 'the repositories the agent was run against',
    'task_prompts': 'the exact prompts given to the agent',
    'model': 'the model used',
    'checkpoint': 'the specific model checkpoint',
    'temperature': 'the sampling temperature',
    'harness': 'the agent harness used',
    'tool_set': 'the tools the agent was given',
    'codebook_version': 'the classification codebook version used to group failures',
    'coverage_corpus': 'the standards checked when deciding whether a failure is already covered',
}

# Fields the driver requires and the scorer accepts but does not demand. Adding one to
# REGISTRATION_FIELDS would reject logs written under an earlier release, which is a
# breaking change to the agent-trial-log/v1 contract rather than an addition to it.
OPTIONAL_REGISTRATION = ('harness_command',)

VERDICTS = {
    'ALREADY-COVERED': (
        'The existing skills already catch these failures.',
        'Ship tightening edits to existing skills. Do not add new surface area. '
        'Publish the negative result.'),
    'REAL-GAP': (
        'Most of these failures reach no existing standard.',
        'The uncovered list below is the specification for what to build. The conditional '
        'section of AGENT-DX-PROPOSAL.md unlocks.'),
    'INCONCLUSIVE': (
        'The result sits between the thresholds and decides nothing.',
        'Run once more at double the sample against the same registration. If it is still '
        'inconclusive, withdraw the proposal.'),
    'TOO-FEW-FAILURES': (
        'Too few distinct failure modes were observed to compute a stable share.',
        f'Widen or harden the task set until at least {MIN_DISTINCT_MODES} distinct modes '
        'appear, then re-run. Do not report a share from this trial.'),
}


# Values the scaffold writes. A registration still holding one names nothing real.
PLACEHOLDERS = {'yyyy-mm-dd', 'https://github.com/owner/repo/pull/n', 'owner/name'}


def is_placeholder(v):
    return isinstance(v, str) and v.strip().lower() in PLACEHOLDERS


def problem(code, what, why, where, fix):
    return {'code': code, 'what': what, 'why': why, 'where': where, 'fix': fix}


def validate(log):
    """Return problems preventing scoring. Empty list means the log is scorable."""
    out = []
    if not isinstance(log, dict):
        return [problem('LOG_NOT_OBJECT', 'The trial log is not a JSON object.',
                        'The scorer expects a single object, not a list or a bare value.',
                        'the top level of the file',
                        'Regenerate the log with --new and fill it in.')]
    if log.get('schema') != SCHEMA:
        out.append(problem(
            'SCHEMA_MISMATCH', f'The log does not declare schema {SCHEMA!r}.',
            f'Found {log.get("schema")!r}. The scorer only reads {SCHEMA}.',
            'schema', f'Set "schema": "{SCHEMA}".'))

    reg = log.get('registration')
    if not isinstance(reg, dict):
        out.append(problem(
            'NOT_REGISTERED', 'The trial has no registration.',
            'A trial whose parameters were not fixed and published before it ran cannot '
            'distinguish a finding from a choice made after seeing the data.',
            'registration',
            'Register the trial first: run with --new, publish the registration in a pull '
            'request, run the agents, then score.'))
        return out

    for field, meaning in REGISTRATION_FIELDS.items():
        if field not in reg:
            out.append(problem(
                'REGISTRATION_INCOMPLETE', f'Registration is missing {field}.',
                f'The scorer needs {meaning} to make the result reproducible by someone else.',
                f'registration.{field}', f'Add "{field}" to the registration and re-publish it.'))
        elif is_placeholder(reg[field]) or (
                isinstance(reg[field], list)
                and any(is_placeholder(x) for x in reg[field])):
            out.append(problem(
                'REGISTRATION_PLACEHOLDER', f'Registration field {field} still holds the '
                'value the scaffold wrote.',
                'A scaffold placeholder is not a registration. It would make the trial '
                'look registered while naming nothing real.',
                f'registration.{field}', f'Replace the placeholder in "{field}" with {meaning}.'))
        elif reg[field] in ('', [], {}, None):
            out.append(problem(
                'REGISTRATION_INCOMPLETE', f'Registration field {field} is empty.',
                f'It must state {meaning}.',
                f'registration.{field}', f'Fill in "{field}" and re-publish the registration.'))

    prompts = reg.get('task_prompts')
    if isinstance(prompts, list):
        for i, task in enumerate(prompts):
            if not isinstance(task, dict):
                continue
            if not task.get('verify'):
                out.append(problem(
                    'TASK_NO_VERIFY',
                    f'Task {task.get("id", i)!r} has no verify command.',
                    'Every outcome in this trial was decided by a verify command. A task '
                    'without one has no stated basis for calling a session passed or failed.',
                    f'registration.task_prompts[{i}].verify',
                    'Record the argument list that decides the outcome, as the driver ran it.'))

    modes = log.get('failure_modes')
    if not isinstance(modes, list):
        out.append(problem(
            'MODES_NOT_LIST', 'failure_modes is not a list.',
            'The share is computed over a list of distinct failure modes.',
            'failure_modes', 'Provide failure_modes as a JSON array.'))
        return out

    seen = set()
    for i, m in enumerate(modes):
        at = f'failure_modes[{i}]'
        if not isinstance(m, dict):
            out.append(problem('MODE_NOT_OBJECT', f'{at} is not an object.',
                               'Each failure mode must be an object with an id.',
                               at, 'Replace it with an object carrying id, summary, covered_by.'))
            continue
        mid = m.get('id')
        if not mid:
            out.append(problem('MODE_NO_ID', f'{at} has no id.',
                               'Modes are counted by id, so every mode needs a stable one.',
                               f'{at}.id', 'Give the mode an id such as "fm-07".'))
            continue
        at = f'failure_modes[{mid}]'
        if mid in seen:
            out.append(problem(
                'MODE_DUPLICATE_ID', f'Two failure modes share the id {mid!r}.',
                'Duplicate ids silently change the denominator of the share.',
                f'{at}.id', 'Give each distinct mode a unique id, or merge them into one entry.'))
        seen.add(mid)
        if 'covered_by' not in m:
            out.append(problem(
                'MODE_NO_COVERAGE_CALL', f'{at} does not say whether anything covers it.',
                'Every mode must be an explicit call: either it names the standard that '
                'catches it, or it states that nothing does. Silence is not a call.',
                f'{at}.covered_by',
                'Name the gate or contract that catches it, or set covered_by to null.'))
        elif isinstance(m['covered_by'], str) and m['covered_by'].strip().lower() in (
                'null', 'none', 'n/a', 'na', 'nothing', '-'):
            out.append(problem(
                'MODE_COVERAGE_AMBIGUOUS',
                f'{at} sets covered_by to the text {m["covered_by"]!r}.',
                'That reads as a name, so the mode would count as covered and quietly pull '
                'the result toward "already covered".',
                f'{at}.covered_by', 'Use JSON null, not a word meaning null.'))
        elif m['covered_by'] is not None and not isinstance(m['covered_by'], str):
            out.append(problem(
                'MODE_COVERAGE_NOT_A_NAME',
                f'{at} sets covered_by to {m["covered_by"]!r}.',
                'Coverage must name the standard that catches the mode, as text, or be null.',
                f'{at}.covered_by', 'Name the gate or contract, or use null.'))
        occ = m.get('occurrences', 1)
        if not isinstance(occ, int) or isinstance(occ, bool) or occ < 1:
            out.append(problem(
                'MODE_OCCURRENCES_INVALID', f'{at} records occurrences = {occ!r}.',
                'A mode that was observed appeared at least once. Occurrences never move the '
                'share, but they are published in the report.',
                f'{at}.occurrences', 'Set occurrences to a whole number of 1 or more.'))

    rater = log.get('second_rater')
    if not isinstance(rater, dict):
        out.append(problem(
            'NO_SECOND_RATER', 'No second rater is recorded.',
            'One operator writing the prompts, setting the granularity, and judging coverage '
            'is the whole result. An independent sample is the only check on that.',
            'second_rater',
            f'Have a second person classify at least {SECOND_RATER_MIN_FRACTION:.0%} of the '
            'modes and record sampled and disagreements.'))
    else:
        frac = rater.get('sample_fraction')
        if not isinstance(frac, (int, float)) or frac < SECOND_RATER_MIN_FRACTION:
            out.append(problem(
                'SECOND_RATER_SAMPLE_TOO_SMALL',
                f'The second-rater sample is {frac!r}.',
                f'It must cover at least {SECOND_RATER_MIN_FRACTION:.0%} of the modes.',
                'second_rater.sample_fraction',
                f'Raise the sample to {SECOND_RATER_MIN_FRACTION} or more.'))
        for k in ('sampled', 'disagreements'):
            v = rater.get(k)
            if not isinstance(v, int) or isinstance(v, bool) or v < 0:
                out.append(problem(
                    'SECOND_RATER_COUNT_INVALID', f'second_rater.{k} is {v!r}.',
                    'It must be a whole number of modes, zero or more.',
                    f'second_rater.{k}', f'Set {k} to a non-negative integer.'))
        if isinstance(rater.get('sampled'), int) and isinstance(rater.get('disagreements'), int) \
                and not isinstance(rater.get('sampled'), bool) \
                and rater['disagreements'] > rater['sampled'] >= 0:
            out.append(problem(
                'SECOND_RATER_COUNT_INVALID',
                f'More disagreements ({rater["disagreements"]}) than modes sampled '
                f'({rater["sampled"]}).',
                'Disagreements are counted within the sample.',
                'second_rater.disagreements',
                'Correct the counts so disagreements never exceed sampled.'))

    runs = log.get('runs')
    if not isinstance(runs, list) or not runs:
        out.append(problem(
            'NO_RUNS', 'The log records no agent runs.',
            'Failure modes are claims about what agents did. Without the runs behind them '
            'there is no evidence, only assertion.',
            'runs', 'Record one entry per repository and task, with n and the outcomes.'))
        return out

    repos = reg.get('repositories') if isinstance(reg.get('repositories'), list) else []
    task_ids = {p.get('id') for p in reg.get('task_prompts', [])
                if isinstance(p, dict)} if isinstance(reg.get('task_prompts'), list) else set()
    failed = 0
    for i, r in enumerate(runs):
        at = f'runs[{i}]'
        if not isinstance(r, dict):
            out.append(problem('RUN_NOT_OBJECT', f'{at} is not an object.',
                               'Each run must record its repository, task, n, and outcomes.',
                               at, 'Replace it with a run object.'))
            continue
        n = r.get('n')
        if not isinstance(n, int) or isinstance(n, bool) or n < MIN_RUNS_PER_TASK:
            out.append(problem(
                'RUN_SAMPLE_TOO_SMALL', f'{at} has n = {n!r}.',
                f'Each repository and task needs at least {MIN_RUNS_PER_TASK} runs, or a single '
                'lucky or unlucky session decides the result.',
                f'{at}.n', f'Run the task at least {MIN_RUNS_PER_TASK} times and record n.'))
            continue
        outcomes = r.get('outcomes')
        if not isinstance(outcomes, list) or len(outcomes) != n:
            out.append(problem(
                'RUN_OUTCOMES_MISMATCH',
                f'{at} claims n = {n} but records '
                f'{len(outcomes) if isinstance(outcomes, list) else "no"} outcomes.',
                'The session count is what the trial cost and what its power rests on. It must '
                'be the number of outcomes actually recorded, not a separate claim.',
                f'{at}.outcomes', f'Record exactly {n} outcomes, one per session.'))
            continue
        failed += sum(1 for o in outcomes if o != 'pass')
        if repos and r.get('repository') not in repos:
            out.append(problem(
                'RUN_UNREGISTERED_REPO', f'{at} names repository {r.get("repository")!r}.',
                'It is not in the registered repository list, so this run was not part of the '
                'registered trial.',
                f'{at}.repository', 'Use a registered repository, or re-register the trial.'))
        if task_ids and r.get('task') not in task_ids:
            out.append(problem(
                'RUN_UNREGISTERED_TASK', f'{at} names task {r.get("task")!r}.',
                'It is not among the registered task prompts.',
                f'{at}.task', 'Use a registered task id, or re-register the trial.'))

    n_modes = len([m for m in modes if isinstance(m, dict)])
    if n_modes > failed:
        out.append(problem(
            'MORE_MODES_THAN_FAILURES',
            f'{n_modes} failure modes are claimed but only {failed} sessions failed.',
            'Every distinct mode has to have been seen in at least one failed session.',
            'failure_modes',
            'Remove modes with no failed session behind them, or record the runs they came from.'))
    return out


def is_uncovered(mode):
    if not isinstance(mode, dict):
        return False
    c = mode.get('covered_by')
    return c is None or (isinstance(c, str) and not c.strip())


def score(log):
    # Defensive: validate() is the gate, but score() is importable on its own and
    # must never raise on a malformed log.
    modes = log.get('failure_modes') if isinstance(log, dict) else None
    modes = [m for m in modes if isinstance(m, dict)] if isinstance(modes, list) else []
    uncovered = [m for m in modes if is_uncovered(m)]
    total, n_unc = len(modes), len(uncovered)
    sessions = 0
    runs = log.get('runs') if isinstance(log, dict) else None
    for r in (runs if isinstance(runs, list) else []):
        if isinstance(r, dict):
            try:
                sessions += int(r.get('n', 0))
            except (TypeError, ValueError):
                pass

    failed = 0
    for r in (runs if isinstance(runs, list) else []):
        if isinstance(r, dict) and isinstance(r.get('outcomes'), list):
            failed += sum(1 for o in r['outcomes'] if o != 'pass')

    share = (n_unc / total) if total else 0.0
    note = ''
    if total == 0 and failed:
        # Sessions failed but nothing was classified. That is an unfinished trial, not a
        # clean run, and it must never resolve as a negative result.
        verdict = 'TOO-FEW-FAILURES'
        note = (f'{failed} sessions failed but no failure modes were recorded. Classify them '
                'before scoring.')
    elif total == 0:
        verdict = 'ALREADY-COVERED'
        note = ('No session failed. A trial that surfaces no failures is not evidence of a '
                'gap, so it resolves the same way as a low share.')
    elif total < MIN_DISTINCT_MODES:
        verdict = 'TOO-FEW-FAILURES'
    elif share <= COVERED_MAX:
        verdict = 'ALREADY-COVERED'
    elif share >= GAP_MIN:
        verdict = 'REAL-GAP'
    else:
        verdict = 'INCONCLUSIVE'
    # The share is withheld below the minimum sample. A ratio over a handful of modes is the
    # coarse artifact the minimum exists to suppress, and publishing it invites citation.
    reportable = verdict != 'TOO-FEW-FAILURES'
    return {'verdict': verdict, 'uncovered_share': (round(share, 4) if reportable else None),
            'total_modes': total, 'uncovered_modes': n_unc, 'covered_modes': total - n_unc,
            'agent_sessions': sessions, 'failed_sessions': failed, 'note': note}


def rule_text():
    return [
        'What a trial measures',
        '',
        '  Agents are run against real repositories and every distinct way they fail is',
        '  recorded. Each failure mode is then checked against the standards this suite',
        '  already ships. The result is one number: the share of failure modes that no',
        '  existing standard catches.',
        '',
        'How the share decides',
        '',
        f'  at most {COVERED_MAX:.0%} uncovered   ALREADY-COVERED   tighten existing skills, build nothing',
        f'  {COVERED_MAX:.0%} to {GAP_MIN:.0%} uncovered    INCONCLUSIVE      re-run once at double sample, then withdraw',
        f'  at least {GAP_MIN:.0%} uncovered  REAL-GAP          the uncovered list is what to build',
        '',
        f'  Fewer than {MIN_DISTINCT_MODES} distinct modes gives TOO-FEW-FAILURES and no share.',
        '  Zero observed failures resolves as ALREADY-COVERED.',
        '',
        'Why the thresholds are what they are',
        '',
        '  They are conventions, not derivations. Their only virtue is being fixed before',
        '  the data existed, so neither outcome can be rationalised after the fact.',
        '',
        'What the scorer refuses',
        '',
        '  A trial whose parameters were not registered and published before it ran. Without',
        '  that, a finding cannot be told apart from a choice made after seeing the data.',
    ]


def scaffold():
    return {
        'schema': SCHEMA,
        '_readme': ('Fill in registration and publish it in a pull request BEFORE running any '
                    'agent. Then run the agents, record failure_modes, and score this file.'),
        'registration': {
            'registered_at': 'YYYY-MM-DD',
            'registration_url': 'https://github.com/OWNER/REPO/pull/N',
            'repositories': ['owner/name'],
            'task_prompts': [{'id': 't1',
                              'prompt': 'Install this product and reach a verified outcome.',
                              'verify': ['make', 'smoke']}],
            'model': '', 'checkpoint': '', 'temperature': 0,
            'harness': '', 'harness_command': ['claude', '-p', '{prompt}'],
            'tool_set': ['read', 'shell'],
            'codebook_version': 'codebook/v1',
            'coverage_corpus': ['release-gates.md#gate-identifiers', 'community.md#gates',
                                'metrics.md#thresholds', 'skill-contracts'],
        },
        # Empty on purpose. Invented runs would be read by the driver as sessions
        # already paid for, and by the scorer as evidence.
        'runs': [],
        'failure_modes': [],
        'second_rater': {'sample_fraction': 0.2, 'sampled': 0, 'disagreements': 0},
    }


def render_text(log, r):
    reg = log['registration']
    modes = log['failure_modes']
    L = []
    L.append(f'Trial {reg["registered_at"]} - {len(reg["repositories"])} repositories, '
             f'{len(reg["task_prompts"])} tasks, {r["agent_sessions"]} agent sessions')
    L.append(f'Configuration {reg["model"]} @ {reg["checkpoint"]}, temperature '
             f'{reg["temperature"]}, harness {reg["harness"]}, codebook {reg["codebook_version"]}')
    L.append(f'Registered at {reg["registration_url"]}')
    corpus = reg.get('coverage_corpus') or []
    L.append(f'Coverage judged against {", ".join(str(c) for c in corpus)}')

    rater = log['second_rater']
    if rater.get('sampled'):
        rate = rater['disagreements'] / rater['sampled']
        L.append(f'Second rater disagreed on {rater["disagreements"]} of {rater["sampled"]} '
                 f'modes sampled ({rate:.0%})')
    else:
        L.append('Second rater recorded no sampled modes')

    L.append('')
    L.append(f'{r["failed_sessions"]} of {r["agent_sessions"]} sessions failed.')
    L.append(f'{r["total_modes"]} distinct failure modes observed.')
    L.append(f'  {r["covered_modes"]} are already caught by an existing standard.')
    L.append(f'  {r["uncovered_modes"]} reach no existing standard.')
    if r['uncovered_share'] is not None:
        L.append(f'  That is {r["uncovered_share"]:.2%} uncovered '
                 f'({r["uncovered_modes"]}/{r["total_modes"]}).')
    elif r['total_modes']:
        L.append(f'  No share is reported below {MIN_DISTINCT_MODES} distinct modes.')

    unc = [m for m in modes if is_uncovered(m)]
    if unc:
        L.append('')
        L.append('Reaching no existing standard')
        for m in unc:
            L.append(f'  {m["id"]}  {m.get("summary", "?")}')
            L.append(f'        seen {m.get("occurrences", 1)}x, attributed to '
                     f'{m.get("problem_class", "unclassified")}')

    classes = {}
    for m in modes:
        k = m.get('problem_class', 'unclassified')
        classes[k] = classes.get(k, 0) + 1
    if classes:
        L.append('')
        L.append('Attribution, for reporting only. It never decides coverage, because the nine')
        L.append('problem classes are exhaustive and every failure lands in one of them.')
        for k in sorted(classes):
            L.append(f'  {k:16} {classes[k]}')

    headline, action = VERDICTS[r['verdict']]
    L.append('')
    L.append(f'VERDICT: {r["verdict"]}')
    L.append(f'  {headline}')
    if r['note']:
        L.append(f'  {r["note"]}')
    L.append(f'  Next: {action}')
    return '\n'.join(L)


def render_html(log, r):
    reg = log['registration']
    modes = log['failure_modes']
    e = html.escape
    headline, action = VERDICTS[r['verdict']]
    tone = {'REAL-GAP': 'gap', 'ALREADY-COVERED': 'covered',
            'INCONCLUSIVE': 'mid', 'TOO-FEW-FAILURES': 'mid'}[r['verdict']]
    pct = f'{r["uncovered_share"]:.1%}' if r['uncovered_share'] is not None else 'withheld'
    rows = []
    for m in sorted(modes, key=lambda x: (not is_uncovered(x), str(x.get('id')))):
        unc = is_uncovered(m)
        rows.append(
            f'<tr class="{"u" if unc else "c"}"><td class="id">{e(str(m.get("id", "?")))}</td>'
            f'<td>{e(str(m.get("summary", "")))}</td>'
            f'<td class="n">{e(str(m.get("occurrences", 1)))}</td>'
            f'<td>{e(str(m.get("problem_class", "unclassified")))}</td>'
            f'<td class="cov">{"reaches no existing standard" if unc else e(str(m.get("covered_by")))}</td></tr>')
    classes = {}
    for m in modes:
        k = m.get('problem_class', 'unclassified')
        classes[k] = classes.get(k, 0) + 1
    chips = ''.join(f'<span class="chip">{e(k)} <b>{v}</b></span>' for k, v in sorted(classes.items()))
    rater = log['second_rater']
    dis = (f'{rater["disagreements"]} of {rater["sampled"]} sampled'
           if rater.get('sampled') else 'no modes sampled')

    return f"""<!doctype html>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agent trial report</title>
<style>
:root{{--bg:#fbfbf9;--fg:#1a1a18;--mut:#6b6b64;--line:#e2e2dc;--card:#fff;
--gap:#b4472e;--cov:#3f6b4a;--mid:#8a6d1f}}
@media(prefers-color-scheme:dark){{:root{{--bg:#16161a;--fg:#ececea;--mut:#9a9a94;
--line:#2c2c32;--card:#1e1e23;--gap:#e08163;--cov:#7fb08d;--mid:#d4b45c}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.55 ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
.wrap{{max-width:940px;margin:0 auto;padding:40px 22px 72px}}
h1{{font-size:23px;margin:0 0 4px;letter-spacing:-.01em}}
.sub{{color:var(--mut);font-size:13px;margin-bottom:26px}}
.verdict{{border:1px solid var(--line);border-left:4px solid var(--{tone});
background:var(--card);border-radius:7px;padding:18px 20px;margin-bottom:26px}}
.vname{{font:600 12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;
letter-spacing:.09em;color:var(--{tone});margin-bottom:9px}}
.vhead{{font-size:17px;margin-bottom:7px}}
.vact{{color:var(--mut);font-size:14px}}
.nums{{display:flex;gap:11px;flex-wrap:wrap;margin-bottom:26px}}
.num{{flex:1;min-width:132px;border:1px solid var(--line);background:var(--card);
border-radius:7px;padding:13px 15px}}
.num b{{display:block;font-size:25px;font-weight:600;letter-spacing:-.02em}}
.num span{{color:var(--mut);font-size:12px}}
.bar{{height:9px;border-radius:5px;overflow:hidden;display:flex;
border:1px solid var(--line);margin-bottom:8px}}
.bar i{{display:block}}.bar .bu{{background:var(--gap)}}.bar .bc{{background:var(--cov)}}
.key{{color:var(--mut);font-size:12px;margin-bottom:26px}}
.key s{{display:inline-block;width:9px;height:9px;border-radius:2px;
margin:0 5px 0 14px;text-decoration:none}}.key s:first-child{{margin-left:0}}
h2{{font-size:13px;text-transform:uppercase;letter-spacing:.07em;color:var(--mut);
margin:0 0 11px;font-weight:600}}
table{{width:100%;border-collapse:collapse;font-size:13.5px;margin-bottom:9px}}
th{{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.05em;
color:var(--mut);border-bottom:1px solid var(--line);padding:0 9px 7px}}
td{{border-bottom:1px solid var(--line);padding:9px;vertical-align:top}}
tr.u .cov{{color:var(--gap)}}tr.c .cov{{color:var(--mut)}}
.id,.n{{font:12px ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mut);
white-space:nowrap}}
.scroll{{overflow-x:auto}}
.chip{{display:inline-block;border:1px solid var(--line);background:var(--card);
border-radius:20px;padding:3px 11px;font-size:12px;color:var(--mut);margin:0 6px 6px 0}}
.note{{color:var(--mut);font-size:12.5px;margin:8px 0 26px}}
.meta{{border-top:1px solid var(--line);padding-top:16px;margin-top:34px;
color:var(--mut);font-size:12px}}
.meta div{{margin-bottom:4px}}
</style>
<div class="wrap">
<h1>Agent trial report</h1>
<div class="sub">{e(str(len(reg['repositories'])))} repositories &middot;
{e(str(len(reg['task_prompts'])))} tasks &middot; {r['agent_sessions']} agent sessions &middot;
registered {e(str(reg['registered_at']))}</div>

<div class="verdict">
<div class="vname">{r['verdict']}</div>
<div class="vhead">{e(headline)}</div>
<div class="vact">{e(action)}</div>
</div>

<div class="nums">
<div class="num"><b>{r['total_modes']}</b><span>distinct failure modes</span></div>
<div class="num"><b>{r['covered_modes']}</b><span>already caught by a standard</span></div>
<div class="num"><b>{r['uncovered_modes']}</b><span>reach no standard</span></div>
<div class="num"><b>{pct}</b><span>uncovered share</span></div>
</div>

<div class="bar"><i class="bu" style="width:{(r['uncovered_share'] or 0)*100:.1f}%"></i><i class="bc"
 style="width:{100-(r['uncovered_share'] or 0)*100:.1f}%"></i></div>
<div class="key"><s style="background:var(--gap)"></s>reaches no existing standard
<s style="background:var(--cov)"></s>already caught</div>

<h2>Failure modes</h2>
<div class="scroll"><table>
<tr><th>id</th><th>what the agent could not do</th><th>seen</th><th>attributed to</th><th>coverage</th></tr>
{''.join(rows)}
</table></div>

<h2>Attribution</h2>
{chips}
<div class="note">Reporting only. Attribution never decides coverage: the nine problem
classes are exhaustive, so every failure lands in one and counting that as coverage would
drive the share to zero.</div>

<div class="meta">
<div>Model {e(str(reg['model']))} @ {e(str(reg['checkpoint']))}, temperature
{e(str(reg['temperature']))}, harness {e(str(reg['harness']))}</div>
<div>Codebook {e(str(reg['codebook_version']))} &middot; second rater disagreed on {e(dis)}</div>
<div>Registration {e(str(reg['registration_url']))}</div>
<div>Thresholds fixed before the data existed: at most {COVERED_MAX:.0%} uncovered is
ALREADY-COVERED, at least {GAP_MIN:.0%} is REAL-GAP, and fewer than {MIN_DISTINCT_MODES}
distinct modes reports no share.</div>
</div>
</div>
"""


def main():
    ap = argparse.ArgumentParser(
        description='Score a pre-registered agent trial. See references/trial-protocol.md.')
    ap.add_argument('log', nargs='?', help='trial log JSON')
    ap.add_argument('--new', metavar='PATH', help='write a blank pre-registration to start a trial')
    ap.add_argument('--explain', action='store_true', help='explain what is measured and how it decides')
    ap.add_argument('--html', metavar='PATH', help='write a shareable HTML report')
    ap.add_argument('--json', action='store_true', help='emit the result as JSON')
    ap.add_argument('--expect', metavar='VERDICT',
                    help='exit non-zero unless the verdict matches; for regression fixtures')
    a = ap.parse_args()

    if a.new:
        p = Path(a.new)
        if p.exists():
            print(f'{p} already exists. Choose another path rather than overwriting a trial.')
            raise SystemExit(1)
        p.write_text(json.dumps(scaffold(), indent=2) + '\n')
        print(f'Wrote {p}')
        print('\nNext: fill in registration, publish it in a pull request, and only then run')
        print('the agents. Registering after the fact does not count. Score with:')
        print(f'  python3 {Path(__file__).name} {p}')
        raise SystemExit(0)

    if a.explain and not a.log:
        print('\n'.join(rule_text()))
        raise SystemExit(0)
    if not a.log:
        ap.error('a trial log is required (or use --new to start one, --explain for the rule)')

    try:
        log = json.loads(Path(a.log).read_text())
    except FileNotFoundError:
        print(f'No such trial log: {a.log}')
        print('Start one with --new PATH.')
        raise SystemExit(1)
    except json.JSONDecodeError as ex:
        print(f'{a.log} is not valid JSON: {ex}')
        print('Fix the syntax, or start fresh with --new PATH.')
        raise SystemExit(1)

    problems = validate(log)
    if problems:
        if a.json:
            print(json.dumps({'verdict': 'UNSCORABLE', 'problems': problems},
                             indent=2, sort_keys=True))
            raise SystemExit(1)
        print(f'This trial cannot be scored. {len(problems)} problem(s) found.\n')
        for p in problems:
            print(f'  [{p["code"]}] {p["what"]}')
            print(f'    Why it matters: {p["why"]}')
            print(f'    Where: {p["where"]}')
            print(f'    Fix: {p["fix"]}\n')
        print('Scoring is refused rather than reported, because a number from an unscorable')
        print('trial would look like evidence. Nothing here is retried automatically.')
        raise SystemExit(1)

    r = score(log)
    if a.explain:
        print('\n'.join(rule_text()))
        print()
    if a.json:
        print(json.dumps(r, indent=2, sort_keys=True))
    else:
        print(render_text(log, r))
    if a.html:
        Path(a.html).write_text(render_html(log, r))
        print(f'\nWrote {a.html}')
    if a.expect and a.expect != r['verdict']:
        print(f'\nExpected verdict {a.expect}, got {r["verdict"]}')
        raise SystemExit(1)
    # House convention, as in guessability_check.py: a result that needs human action
    # exits non-zero. ALREADY-COVERED and REAL-GAP settle the question; the other two
    # ask for another run, so they are not exit 0.
    raise SystemExit(0 if r['verdict'] in ('ALREADY-COVERED', 'REAL-GAP') else 1)


if __name__ == '__main__':
    main()
