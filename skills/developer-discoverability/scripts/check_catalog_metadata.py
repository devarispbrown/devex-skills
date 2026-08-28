#!/usr/bin/env python3
"""Validate that every entry in a catalog JSON file has the required fields.

The catalog is a JSON list of entry objects. JSON only: the Python stdlib has
no YAML parser, so catalogs are committed as JSON. Stdlib only."""
import argparse, json, sys
from pathlib import Path

DEFAULT_REQUIRED = ('name', 'owner', 'lifecycle', 'docs_link', 'status')

def missing_fields(entry, required):
    return [f for f in required if f not in entry or entry[f] in (None, '')]

def main():
    ap = argparse.ArgumentParser(description='Check catalog entry metadata.')
    ap.add_argument('catalog', help='path to a catalog JSON file (a list of entries)')
    ap.add_argument('--required', nargs='+', default=list(DEFAULT_REQUIRED),
                    metavar='FIELD', help='fields every entry must have')
    a = ap.parse_args()
    try:
        catalog = json.loads(Path(a.catalog).read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(f'{a.catalog}: cannot read catalog: {e}', file=sys.stderr)
        raise SystemExit(2)
    if not isinstance(catalog, list):
        print(f'{a.catalog}: expected a JSON list of entries, got {type(catalog).__name__}',
              file=sys.stderr)
        raise SystemExit(2)
    findings = []
    for index, entry in enumerate(catalog):
        if not isinstance(entry, dict):
            findings.append((index, '<non-object>', 'entry is not an object'))
            continue
        for field in missing_fields(entry, a.required):
            findings.append((index, entry.get('name', '<unnamed>'),
                             f'missing required field {field!r}'))
    for index, name, message in findings:
        print(f'entry #{index} ({name}): {message}')
    if findings:
        print(f'{len(findings)} finding(s) in {a.catalog}: catalog invalid')
        raise SystemExit(1)
    print(f'{a.catalog}: OK - {len(catalog)} entries, all required fields present')

if __name__ == '__main__':
    main()
