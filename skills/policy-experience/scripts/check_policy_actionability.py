#!/usr/bin/env python3
"""Check policy violation samples for the four actionability fields.

Each sample must carry what_happened, why, how_to_fix, and request_exception
so the developer can act without opening the policy file. Missing or empty
fields make the violation opaque. Exits 1 when any sample is opaque.
Stdlib only.
"""
import argparse, json
from pathlib import Path

REQUIRED_FIELDS = ('what_happened', 'why', 'how_to_fix', 'request_exception')


def main():
    ap = argparse.ArgumentParser(description='Check policy violation samples for actionability')
    ap.add_argument('samples', help='path to a JSON array of policy violation samples')
    a = ap.parse_args()
    try:
        samples = json.loads(Path(a.samples).read_text())
    except Exception as e:
        raise SystemExit(f'cannot read {a.samples}: {e}')
    if not isinstance(samples, list):
        raise SystemExit(f'{a.samples}: expected a JSON array of violation samples')
    problems = []
    for i, sample in enumerate(samples):
        if not isinstance(sample, dict):
            problems.append((i, 'sample is not an object'))
            continue
        for field in REQUIRED_FIELDS:
            value = sample.get(field)
            if not isinstance(value, str) or not value.strip():
                problems.append((i, f'missing or empty field {field!r}'))
    for i, problem in problems:
        print(f'sample {i}: {problem}')
    if problems:
        raise SystemExit(1)
    print(f'{len(samples)} violation sample(s): all actionable')


if __name__ == '__main__':
    main()
