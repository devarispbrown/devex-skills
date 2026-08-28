#!/usr/bin/env python3
"""Check a loop manifest against feedback budgets. JSON + stdlib only.

Reads a JSON manifest of loop stages. Each step carries a measured time and
the budget it is compared against; the command field is informational and
never executed. Prints PASS or BREACH per step against its budget and exits
1 when any step exceeds its budget. Evidence labels follow the canonical
vocabulary: Observed, CI-observed, Estimated. An estimate can never prove
a PASS, so Estimated steps are flagged as unproven.
Stdlib only.
"""
import argparse
import json
from pathlib import Path

VALID_EVIDENCE = {'Observed', 'CI-observed', 'Estimated'}
REQUIRED_KEYS = ('name', 'command', 'budget_seconds', 'measured_seconds', 'evidence')


def main():
    ap = argparse.ArgumentParser(
        description='Check loop manifest steps against feedback budgets.')
    ap.add_argument('manifest', help='path to the loop manifest JSON')
    a = ap.parse_args()

    try:
        data = json.loads(Path(a.manifest).read_text())
    except (OSError, ValueError) as exc:
        raise SystemExit(f'cannot read manifest {a.manifest!r}: {exc}')

    steps = data.get('steps')
    if not isinstance(steps, list) or not steps:
        raise SystemExit('manifest must contain a non-empty "steps" list')

    breaches = 0
    estimated = 0
    print(f"Loop feedback audit: {data.get('name', 'unnamed manifest')}")
    print(f"{'step':28} {'budget':>8} {'measured':>10}  {'result':7} evidence")
    print('-' * 72)
    for step in steps:
        name = step.get('name')
        missing = [k for k in REQUIRED_KEYS if k not in step]
        if missing:
            raise SystemExit(f"step {name!r} missing keys: {', '.join(missing)}")
        try:
            budget = float(step['budget_seconds'])
            measured = float(step['measured_seconds'])
        except (TypeError, ValueError):
            raise SystemExit(f"step {name!r}: budget_seconds and measured_seconds must be numeric")
        evidence = step['evidence']
        if evidence not in VALID_EVIDENCE:
            raise SystemExit(
                f"step {name!r}: invalid evidence {evidence!r} "
                "(expected Observed, CI-observed, or Estimated)")
        ok = measured <= budget
        if not ok:
            breaches += 1
        if evidence == 'Estimated':
            estimated += 1
        print(f"{name:28} {budget:8.1f} {measured:10.1f}  "
              f"{'PASS' if ok else 'BREACH':7} {evidence}")

    if estimated:
        print('NOTE: Estimated evidence cannot prove a PASS; '
              'confirm Estimated steps with Observed or CI-observed measurements.')
    print(f'RESULT: {breaches} breach(es)' if breaches else 'RESULT: PASS')
    raise SystemExit(1 if breaches else 0)


if __name__ == '__main__':
    main()
