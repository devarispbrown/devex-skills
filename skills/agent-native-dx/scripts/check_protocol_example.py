#!/usr/bin/env python3
"""Prove the trial-log example in references/trial-protocol.md still matches the scorer.

The protocol document teaches the log format by showing one. Documentation that
teaches a stale format is worse than none, so this runs the document's own example
through the scorer's validator. Stdlib only.
"""
import importlib.util, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOC = HERE.parent / 'references' / 'trial-protocol.md'
SCORER = HERE / 'agent_trial_scorer.py'


def load_scorer():
    spec = importlib.util.spec_from_file_location('agent_trial_scorer', SCORER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    if not DOC.exists():
        print(f'missing: {DOC}')
        return 1
    blocks = re.findall(r'```json\n(.*?)```', DOC.read_text(), re.S)
    if not blocks:
        print(f'{DOC.name}: no fenced json example found; the format is taught nowhere')
        return 1

    scorer = load_scorer()
    failures = 0
    for i, block in enumerate(blocks):
        try:
            example = json.loads(block)
        except json.JSONDecodeError as ex:
            print(f'{DOC.name}: json block {i} does not parse: {ex}')
            failures += 1
            continue
        problems = scorer.validate(example)
        for p in problems:
            print(f'{DOC.name}: json block {i}: [{p["code"]}] {p["what"]} ({p["where"]})')
        failures += bool(problems)

        declared = set(example.get('registration', {}))
        required = set(scorer.REGISTRATION_FIELDS) | set(scorer.OPTIONAL_REGISTRATION)
        for extra in sorted(declared - required):
            print(f'{DOC.name}: json block {i}: registration.{extra} is documented but the '
                  'scorer does not know it')
            failures += 1

    # The fenced example is not the only place the format is taught. The prose
    # checklist is what an operator actually follows, and a JSON-only check cannot
    # see it going stale.
    prose = DOC.read_text()
    checklist = prose.split('## Pre-registration', 1)[-1].split('##', 1)[0]
    for field in sorted(set(scorer.REGISTRATION_FIELDS) | set(scorer.OPTIONAL_REGISTRATION)):
        bare = field.replace('_', ' ')
        if field not in checklist and bare not in checklist:
            print(f'{DOC.name}: pre-registration checklist does not mention {field!r}, '
                  'which the scorer reads')
            failures += 1

    print(f'{len(blocks)} example(s) and the pre-registration checklist checked against '
          f'{SCORER.name}, {failures} mismatch(es)')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
