#!/usr/bin/env python3
"""Regression-test the trial decision rule. Stdlib only.

The fixtures prove the scorer runs. This proves it still decides correctly: every
band, both inclusive edges, the minimum-sample guard, and the two zero-mode cases.
Delete a band or loosen an edge and this fails.
"""
import importlib.util, sys
from pathlib import Path

SCORER = Path(__file__).resolve().parent / 'agent_trial_scorer.py'


def load():
    spec = importlib.util.spec_from_file_location('agent_trial_scorer', SCORER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def log(total, uncovered, failed=None, sessions=None):
    failed = total if failed is None else failed
    sessions = max(failed, 5) if sessions is None else sessions
    outcomes = ['fail'] * failed + ['pass'] * (sessions - failed)
    return {'failure_modes': [{'id': f'fm-{i}', 'covered_by': (None if i < uncovered else 'GATE')}
                              for i in range(total)],
            'runs': [{'repository': 'r', 'task': 't', 'n': sessions, 'outcomes': outcomes}]}


CASES = [
    # (modes, uncovered, expected verdict, what it pins down)
    (20,  0, 'ALREADY-COVERED',  'nothing uncovered'),
    (20,  4, 'ALREADY-COVERED',  'exactly at the covered edge, inclusive'),
    (20,  5, 'INCONCLUSIVE',     'one mode past the covered edge'),
    (20,  7, 'INCONCLUSIVE',     'mid band'),
    (20,  8, 'REAL-GAP',         'exactly at the gap edge, inclusive'),
    (20, 20, 'REAL-GAP',         'everything uncovered'),
    (15,  3, 'ALREADY-COVERED',  'covered edge at the minimum sample'),
    (15,  6, 'REAL-GAP',         'gap edge at the minimum sample'),
    (14,  6, 'TOO-FEW-FAILURES', 'one mode below the minimum sample'),
    (14,  0, 'TOO-FEW-FAILURES', 'below the minimum outranks a clean share'),
    (1,   1, 'TOO-FEW-FAILURES', 'a single mode never reports a share'),
]


def main():
    m = load()
    failures = 0

    for total, unc, want, why in CASES:
        got = m.score(log(total, unc))
        if got['verdict'] != want:
            print(f'FAIL {total} modes, {unc} uncovered: expected {want}, got {got["verdict"]}'
                  f'  ({why})')
            failures += 1
        if want == 'TOO-FEW-FAILURES' and got['uncovered_share'] is not None:
            print(f'FAIL {total} modes: share {got["uncovered_share"]} published below the '
                  f'minimum sample; it must be withheld')
            failures += 1

    # Zero modes with failed sessions is an unfinished trial, never a negative result.
    got = m.score(log(0, 0, failed=120, sessions=120))
    if got['verdict'] != 'TOO-FEW-FAILURES':
        print(f'FAIL 120 failed sessions with nothing classified: expected TOO-FEW-FAILURES, '
              f'got {got["verdict"]}')
        failures += 1

    # Zero modes because nothing failed is a genuine clean run.
    got = m.score(log(0, 0, failed=0, sessions=40))
    if got['verdict'] != 'ALREADY-COVERED':
        print(f'FAIL clean run with no failures: expected ALREADY-COVERED, got {got["verdict"]}')
        failures += 1

    # Occurrences must never move the share.
    a = m.score(log(20, 8))
    heavy = log(20, 8)
    for i, mode in enumerate(heavy['failure_modes']):
        mode['occurrences'] = 99 if i < 8 else 1
    if m.score(heavy)['uncovered_share'] != a['uncovered_share']:
        print('FAIL occurrences changed the share; they must not')
        failures += 1

    print(f'{len(CASES) + 4} decision-rule assertions, {failures} failure(s)')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
