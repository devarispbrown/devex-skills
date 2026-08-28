#!/usr/bin/env python3
"""Heuristic git-diff release classification scanner. Stdlib only."""
import argparse
import re
import subprocess

# (regex on path, likely class, affected consumers, suggested bump)
RULES = [
    (re.compile(r'(^|/)(openapi|swagger|asyncapi)[^/]*\.(ya?ml|json)$|\.proto$|\.graphqls?$|(^|/)schemas?(/|$)|\.schema\.json$', re.I),
     'breaking or behavioral', ['JSON/response parsers', 'generated SDKs', 'webhook handlers'], 'MAJOR if breaking else MINOR'),
    (re.compile(r'(^|/)migrations?(/|$)|(^|/)(alembic|flyway)(/|$)|\.sql$', re.I),
     'breaking', ['migrations / DB schemas', 'persisted data'], 'MAJOR'),
    (re.compile(r'(^|/)(config|settings|options)(/|$)|\.env(\.[a-z0-9]+)?$|(^|/)env(/|$)', re.I),
     'behavioral', ['config parsers', 'dashboards', 'deployment tooling'], 'MINOR or MAJOR'),
    (re.compile(r'(^|/)(types?|enums?|models?)(/|$)|\.d\.ts$', re.I),
     'behavioral', ['enum exhaustiveness', 'generated SDKs'], 'MINOR or MAJOR'),
    (re.compile(r'(^|/)(sdk|client|generated)(/|$)', re.I),
     'behavioral', ['generated SDKs', 'SDK parity'], 'MINOR or MAJOR'),
    (re.compile(r'(^|/)webhooks?(/|$)|(^|/)events?(/|$)|(^|/)hooks?(/|$)', re.I),
     'behavioral', ['webhook handlers', 'dashboards'], 'MINOR or MAJOR'),
    (re.compile(r'(^|/)(cmd|cli)(/|$)|(^|/)cli\.(py|go|ts|js)$|(^|/)main\.(py|go)$', re.I),
     'behavioral', ['shell scripts on CLI output', 'automation'], 'MINOR or MAJOR'),
    (re.compile(r'package\.json$|pyproject\.toml$|go\.mod$|Cargo\.toml$|pom\.xml$|build\.gradle$|requirements.*\.txt$|Gemfile$', re.I),
     'behavioral', ['runtime compatibility', 'install docs'], 'MINOR or MAJOR'),
    (re.compile(r'(^|/)(test|tests|spec|__tests__)(/|$)|\.(test|spec)\.(py|ts|js|go|rs)$|test_.*\.py$|.*_test\.go$', re.I),
     'internal', ['none'], 'PATCH or none'),
    (re.compile(r'(^|/)docs?(/|$)|\.(md|mdx|rst)$|(^|/)CHANGELOG|(^|/)README', re.I),
     'internal', ['docs consumers'], 'PATCH or none'),
]

BUMP_ORDER = {'PATCH or none': 1, 'MINOR': 2, 'MINOR or MAJOR': 2, 'MAJOR if breaking else MINOR': 3, 'MAJOR': 3}


def changed_files(base, head):
    proc = subprocess.run(['git', 'diff', '--name-only', f'{base}...{head}'],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f'git diff failed: {proc.stderr.strip() or proc.stdout.strip()}')
    return [x for x in proc.stdout.splitlines() if x.strip()]


def main():
    ap = argparse.ArgumentParser(description='Heuristic release-diff classifier (informational only).')
    ap.add_argument('--base', default='HEAD~1', help='base revision (default HEAD~1)')
    ap.add_argument('--head', default='HEAD', help='head revision (default HEAD)')
    args = ap.parse_args()
    try:
        files = changed_files(args.base, args.head)
    except SystemExit:
        raise
    print(f'Changed files: {len(files)}')
    if not files:
        print('No changed files. Nothing to classify.')
        return
    max_bump = 1
    for f in files:
        hits = [(cls, cons, bump) for rx, cls, cons, bump in RULES if rx.search(f)]
        if not hits:
            print(f'\n{f}\n  class: unclassified (semantic review required)')
            continue
        cls, cons, bump = hits[0]
        print(f'\n{f}')
        print(f'  class: {cls}')
        print(f'  consumers: {", ".join(cons)}')
        print(f'  suggested bump: {bump}')
        max_bump = max(max_bump, BUMP_ORDER[bump])
    summary = {1: 'PATCH or none', 2: 'MINOR', 3: 'MAJOR'}[max_bump]
    print(f'\nSummary: highest suggested bump: {summary}')
    print('HEURISTIC only: verify each classification against the diff before gating. Exits 0; never a verdict.')


if __name__ == '__main__':
    main()
