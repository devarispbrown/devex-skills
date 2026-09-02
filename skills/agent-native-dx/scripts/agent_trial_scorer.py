#!/usr/bin/env python3
"""Score a pre-registered agent trial log. Offline, deterministic, stdlib only.

Consumes a trial log produced out of band by an operator (see
references/trial-protocol.md) and applies the decision rule: u is the share of
distinct failure modes the registered coverage corpus does not catch.

This script never executes an agent and never touches the network. Execution is
an operator activity; scoring is reproducible and belongs in CI.
"""
import argparse, json
from pathlib import Path

SCHEMA = 'agent-trial-log/v1'
REQUIRED_REGISTRATION = ('registered_at', 'registration_url', 'repositories',
                         'task_prompts', 'model', 'checkpoint', 'temperature',
                         'harness', 'tool_set', 'codebook_version', 'coverage_corpus')
MIN_DISTINCT_MODES = 15
PROCEED_NO_MAX = 0.20
PROCEED_YES_MIN = 0.40
SECOND_RATER_MIN_FRACTION = 0.2


def validate(log):
    """Return a list of reasons the log cannot be scored. Empty means scorable."""
    problems = []
    if log.get('schema') != SCHEMA:
        problems.append(f'schema must be {SCHEMA!r}, got {log.get("schema")!r}')
    reg = log.get('registration')
    if not isinstance(reg, dict):
        problems.append('registration missing: an unregistered trial is not evidence')
        return problems
    for field in REQUIRED_REGISTRATION:
        if field not in reg:
            problems.append(f'registration.{field} missing: pre-registration incomplete')
        elif reg[field] in ('', [], None):
            problems.append(f'registration.{field} empty: pre-registration incomplete')
    modes = log.get('failure_modes')
    if not isinstance(modes, list):
        problems.append('failure_modes must be a list')
    else:
        seen = set()
        for i, m in enumerate(modes):
            if not isinstance(m, dict) or 'id' not in m:
                problems.append(f'failure_modes[{i}] missing id')
                continue
            if m['id'] in seen:
                problems.append(f'failure_modes: duplicate id {m["id"]!r}')
            seen.add(m['id'])
            if 'covered_by' not in m:
                problems.append(f'failure_modes[{m["id"]}] missing covered_by '
                                '(use null when nothing in the corpus catches it)')
    rater = log.get('second_rater')
    if not isinstance(rater, dict):
        problems.append('second_rater missing: independent classification of a sample is required')
    elif rater.get('sample_fraction', 0) < SECOND_RATER_MIN_FRACTION:
        problems.append(f'second_rater.sample_fraction below {SECOND_RATER_MIN_FRACTION}')
    return problems


def score(log):
    modes = log['failure_modes']
    total = len(modes)
    uncovered = [m for m in modes if m.get('covered_by') in (None, '')]
    runs = log.get('runs', [])
    sessions = sum(int(r.get('n', 0)) for r in runs)

    if total == 0:
        # Zero observed failures counts as proceed-no. A trial that surfaces no
        # failures is evidence of nothing that warrants new surface area.
        return {'verdict': 'PROCEED-NO', 'u': 0.0, 'total': 0, 'uncovered': 0,
                'sessions': sessions, 'reason': 'zero failure modes observed'}
    u = len(uncovered) / total
    if total < MIN_DISTINCT_MODES:
        return {'verdict': 'RE-SCOPE', 'u': u, 'total': total, 'uncovered': len(uncovered),
                'sessions': sessions,
                'reason': f'{total} distinct failure modes observed, minimum is {MIN_DISTINCT_MODES}'}
    if u <= PROCEED_NO_MAX:
        verdict, reason = 'PROCEED-NO', 'existing standards already catch these failures'
    elif u >= PROCEED_YES_MIN:
        verdict, reason = 'PROCEED-YES', 'the uncovered modes are the list of what is missing'
    else:
        verdict, reason = 'INCONCLUSIVE', 'one re-run at 2N against the same registration, then withdraw'
    return {'verdict': verdict, 'u': u, 'total': total, 'uncovered': len(uncovered),
            'sessions': sessions, 'reason': reason}


def main():
    ap = argparse.ArgumentParser(
        description='Score a pre-registered agent trial log (see references/trial-protocol.md).')
    ap.add_argument('log', help='trial log JSON')
    ap.add_argument('--json', action='store_true', help='emit the result as JSON')
    a = ap.parse_args()
    log = json.loads(Path(a.log).read_text())

    problems = validate(log)
    if problems:
        for p in problems:
            print(f'UNSCORABLE: {p}')
        print(f'\nRESULT: UNSCORABLE ({len(problems)} problem(s))')
        raise SystemExit(1)

    r = score(log)
    reg = log['registration']
    modes = log['failure_modes']

    if a.json:
        print(json.dumps(r, indent=2, sort_keys=True))
        raise SystemExit(0)

    print(f'Trial: {len(reg["repositories"])} repositories, {len(reg["task_prompts"])} task prompts, '
          f'{r["sessions"]} agent sessions')
    print(f'Configuration: {reg["model"]} @ {reg["checkpoint"]}, temperature {reg["temperature"]}, '
          f'harness {reg["harness"]}')
    print(f'Registered: {reg["registered_at"]} ({reg["registration_url"]})')
    print(f'Codebook: {reg["codebook_version"]}')

    rater = log['second_rater']
    sampled = rater.get('sampled', 0)
    dis = rater.get('disagreements', 0)
    rate = (dis / sampled) if sampled else 0.0
    print(f'Second rater: {dis}/{sampled} disagreements ({rate:.0%} of a '
          f'{rater["sample_fraction"]:.0%} sample)')

    print('\nUncovered failure modes')
    for m in modes:
        if m.get('covered_by') in (None, ''):
            print(f'  {m["id"]}: {m.get("summary", "?")} [{m.get("problem_class", "unclassified")}] '
                  f'x{m.get("occurrences", 1)}')
    if r['uncovered'] == 0:
        print('  none')

    # Problem-class attribution is reporting only. It never decides coverage:
    # the nine classes are exhaustive by construction, so treating a successful
    # classification as coverage would drive u to zero mechanically.
    classes = {}
    for m in modes:
        classes[m.get('problem_class', 'unclassified')] = \
            classes.get(m.get('problem_class', 'unclassified'), 0) + 1
    print('\nProblem-class attribution (reporting only, never decides coverage)')
    for k in sorted(classes):
        print(f'  {k:16} {classes[k]}')

    print(f'\nDistinct failure modes: {r["total"]}  uncovered: {r["uncovered"]}')
    print(f'u = {r["u"]:.2f}  (proceed-no <= {PROCEED_NO_MAX}, proceed-yes >= {PROCEED_YES_MIN})')
    print(f'RESULT: {r["verdict"]} - {r["reason"]}')
    raise SystemExit(0)


if __name__ == '__main__':
    main()
