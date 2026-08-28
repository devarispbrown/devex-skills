#!/usr/bin/env python3
"""Run and time a 14-stage developer-journey manifest. Stdlib only."""
import argparse, json, os, subprocess, sys, time
from pathlib import Path

STAGES = ['find','understand','install','auth','configure','execute','verify',
          'modify','break','diagnose','recover','test','deploy','upgrade']
ZERO_TO_VALUE = set(STAGES[:7])          # find..verify: the magic-path span
BUDGET_DEFAULT_SECONDS = 900             # MAGIC_PATH_MAX_MIN * 60 (dx-standards/metrics.md)
TARGET_COMMANDS = 8                      # MAGIC_PATH_MAX_COMMANDS (P2 target)
TARGET_CREDENTIALS = 2                   # MAGIC_PATH_MAX_CREDENTIALS (P2 target)
TARGET_CONTEXT_SWITCHES = 4              # MAGIC_PATH_MAX_CONTEXT_SWITCHES (P2 target)
SCORE_WEIGHTS = {                        # canonical weights: references/dx-scoring.md
    'time_to_first_value': 20, 'api': 15, 'sdk': 10, 'cli_config': 10,
    'errors_recovery': 12, 'documentation': 10, 'local_dev': 8,
    'testing_quality': 8, 'release_compatibility': 7,
}

def load_manifest(path):
    m = json.loads(Path(path).read_text())
    if not isinstance(m, dict) or not isinstance(m.get('steps'), list):
        raise SystemExit(f'{path}: manifest must be a JSON object with a "steps" list')
    for i, step in enumerate(m['steps']):
        if step.get('segment') not in STAGES:
            raise SystemExit(f'{path}: step {i} {step.get("name", "?")!r} has invalid segment '
                             f'{step.get("segment")!r}; expected one of: {", ".join(STAGES)}')
        cmd = step.get('command')
        if not (isinstance(cmd, list) and cmd and all(isinstance(t, str) for t in cmd)):
            raise SystemExit(f'{path}: step {i} {step.get("name", "?")!r} command must be an argv list of strings')
        step.setdefault('scope', 'core')
        if step['scope'] not in ('core', 'optional'):
            raise SystemExit(f'{path}: step {i} {step.get("name", "?")!r} scope must be "core" or "optional"')
    return m

def load_scores(path):
    s = json.loads(Path(path).read_text())
    if not isinstance(s, dict):
        raise SystemExit(f'{path}: scores must be a JSON object of area -> 0..100')
    missing = [k for k in SCORE_WEIGHTS if k not in s]
    if missing:
        raise SystemExit(f'{path}: missing area scores: {", ".join(sorted(missing))}')
    for k, v in s.items():
        if not isinstance(v, (int, float)) or not 0 <= v <= 100:
            raise SystemExit(f'{path}: {k} = {v!r} must be a number in 0..100')
    return s

def run_steps(m, scope, cwd):
    rows = []
    for step in m['steps']:
        if scope == 'core' and step['scope'] != 'core':
            continue
        name, seg = step['name'], step['segment']
        timeout = step.get('timeout_seconds', 300)
        env = os.environ.copy()
        env.update(step.get('env', {}))
        start = time.monotonic()
        try:
            cp = subprocess.run(step['command'], cwd=cwd, text=True, capture_output=True,
                                timeout=timeout, env=env)
            code = cp.returncode
            ok = code == step.get('expected_exit_code', 0)
            needle = step.get('stdout_contains')
            if needle is not None:
                ok = ok and needle in cp.stdout
            if not ok:
                if cp.stdout: print(cp.stdout, end='')
                if cp.stderr: print(cp.stderr, file=sys.stderr, end='')
        except subprocess.TimeoutExpired:
            code = 'timeout'
            ok = False
        rows.append((name, seg, start, time.monotonic(), ok, code, step))
    return rows

def report(rows, m, budget, scores_path):
    print('\nStep results')
    for name, seg, start, end, ok, code, step in rows:
        print(f'{name:24} {seg:14} {end - start:8.2f}s  {"PASS" if ok else "FAIL"} ({code})')
    by_stage = {}
    for name, seg, start, end, ok, code, step in rows:
        s = by_stage.setdefault(seg, {'steps': 0, 'time': 0.0, 'pass': 0})
        s['steps'] += 1
        s['time'] += end - start
        s['pass'] += 1 if ok else 0
    print('\nPer-stage timing')
    for seg in STAGES:
        if seg in by_stage:
            s = by_stage[seg]
            print(f'{seg:14} {s["steps"]} step(s) {s["time"]:8.2f}s  {s["pass"]}/{s["steps"]} PASS')
    span = [r for r in rows if r[1] in ZERO_TO_VALUE]
    if not span:
        print('\nMAGIC PATH: no executed steps in the zero-to-value span (find..verify)')
        print('RESULT: FAIL (no reproducible end-to-end journey; BROKEN_QUICKSTART)')
        return 1
    span_time = span[-1][3] - span[0][2]
    commands = len(span)
    credentials = sum(int(r[6].get('credentials', 0)) for r in span)
    switches = sum(int(r[6].get('context_switches', 0)) for r in span)
    failed = any(not r[4] for r in span)
    print('\nMAGIC PATH (zero-to-value span; gate: MAGIC_PATH_MAX_MIN)')
    print(f'span time:        {span_time:7.2f}s / budget {budget}s')
    print(f'commands:         {commands:4d} (target {TARGET_COMMANDS}, P2)')
    print(f'credentials:      {credentials:4d} (target {TARGET_CREDENTIALS}, P2)')
    print(f'context switches: {switches:4d} (target {TARGET_CONTEXT_SWITCHES}, P2)')
    verdict_ok = not failed and span_time <= budget
    print('RESULT:', 'PASS' if verdict_ok else 'FAIL')
    if scores_path:
        scores = load_scores(scores_path)
        total = round(sum(SCORE_WEIGHTS[k] * scores[k] for k in SCORE_WEIGHTS) / 100)
        print('\nPer-area scores')
        for k, w in SCORE_WEIGHTS.items():
            print(f'{k:24} {w:3d}  {scores[k]:3d}/100')
        print(f'OVERALL DX: {total}/100 (world-class determination per references/dx-scoring.md)')
    else:
        print('\nOverall DX: UNVERIFIED (supply per-area scores with --scores PATH; see references/dx-scoring.md)')
    return 0 if verdict_ok else 1

def main():
    ap = argparse.ArgumentParser(description='Run and time a 14-stage developer-journey manifest.')
    ap.add_argument('manifest', help='journey manifest JSON (see assets/journey-manifest.example.json)')
    ap.add_argument('--cwd', default='.', help='working directory for step execution')
    ap.add_argument('--execute', action='store_true', help='actually execute steps (default: dry run)')
    ap.add_argument('--scope', choices=['core', 'all'], default='core',
                    help='core = zero-to-value span only (default); all = core + optional stages')
    ap.add_argument('--scores', metavar='PATH', help='per-area scores JSON; without it Overall DX stays UNVERIFIED')
    ap.add_argument('--budget-seconds', type=int, default=None,
                    help='override the magic-path budget (default: manifest budget_seconds, else MAGIC_PATH_MAX_MIN)')
    a = ap.parse_args()
    m = load_manifest(a.manifest)
    budget = a.budget_seconds if a.budget_seconds is not None else m.get('budget_seconds', BUDGET_DEFAULT_SECONDS)
    print(json.dumps(m, indent=2))
    print('\nPlanned scope')
    for scope in ('core', 'optional'):
        names = [s['name'] for s in m['steps'] if s['scope'] == scope]
        print(f'{scope:8} {len(names)} step(s): {", ".join(names) if names else "-"}')
    if not a.execute:
        print('\nDry run only. Pass --execute to run commands.')
        raise SystemExit(0)
    rows = run_steps(m, a.scope, a.cwd)
    raise SystemExit(report(rows, m, budget, a.scores))

if __name__ == '__main__':
    main()
