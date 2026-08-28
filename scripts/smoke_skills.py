#!/usr/bin/env python3
"""Run per-skill fixture smoke tests declared in each skill's assets/smoke.json. Stdlib only.

Convention: a skill with a checker script ships assets/smoke.json:
  {"<script>.py": {"clean": [args...], "broken": [args...],
                   "clean_exit": 0, "broken_exit": 1}}
Each run executes `python3 skills/<skill>/scripts/<script>.py <args>` from the
repo root and asserts the exit code. Skills without smoke.json are skipped.
"""
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_one(skill, script, spec):
    results = []
    kinds = [k for k in ('clean', 'broken') if k in spec]
    skill_dir = ROOT / 'skills' / skill
    for kind in kinds:
        args = [sys.executable, str(skill_dir / 'scripts' / script)] + spec[kind]
        # fixtures and relative paths resolve inside the skill's assets directory
        cp = subprocess.run(args, capture_output=True, text=True, timeout=60, cwd=str(skill_dir / 'assets'))
        expected = spec.get(f'{kind}_exit', 0 if kind == 'clean' else 1)
        ok = cp.returncode == expected
        results.append(ok)
        status = 'OK' if ok else 'FAIL'
        print(f'{status} {skill}/{script} {kind}: exit {cp.returncode} (expected {expected})')
        if not ok:
            print('  stdout:', (cp.stdout or '').strip().splitlines()[-1] if cp.stdout else '')
    return all(results)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--skill', help='run only this skill')
    a = ap.parse_args()
    failures = 0
    for skill_dir in sorted((ROOT / 'skills').glob('*')):
        if not skill_dir.is_dir() or (a.skill and skill_dir.name != a.skill):
            continue
        smoke = skill_dir / 'assets' / 'smoke.json'
        if not smoke.exists():
            continue
        for script, spec in json.loads(smoke.read_text()).items():
            if not run_one(skill_dir.name, script, spec):
                failures += 1
    print(f'{failures} smoke failure(s)')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
