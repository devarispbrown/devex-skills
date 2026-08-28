#!/usr/bin/env python3
"""Scan a tree for compatibility consumer signatures. Stdlib only."""
import argparse
import os
import re

SKIP_DIRS = {'.git', 'node_modules', 'vendor', '.venv', 'venv', 'dist', 'build',
             '__pycache__', '.tox', 'target', '.next', '.pytest_cache', '.mypy_cache'}
MAX_BYTES = 2_000_000

SIGNATURES = [
    ('JSON/response parsing', re.compile(r'json\.loads\s*\(|JSON\.parse\s*\(|\.json\s*\(\s*\)|body\.json\s*\(')),
    ('Enum exhaustiveness / switch', re.compile(r'switch\s*\(|match\s+[\w.]+?\s*\{|\bcase\s+[A-Z][A-Z0-9_]*\s*:|@exhaustive|ts-exhaustive')),
    ('Config parsing', re.compile(r'configparser|ConfigParser|load_dotenv|dotenv|os\.environ|process\.env')),
    ('Webhook handling', re.compile(r'webhook|X-Hub-Signature|x-hub-signature|verify\w*.*signature|event_type\b')),
    ('Dashboards / metrics', re.compile(r'\b(gauge|counter|histogram|summary)\s*\(|prometheus|datadog|statsd|grafana|new_relic')),
    ('CLI output parsing', re.compile(r'subprocess\.(check_output|run|Popen|check_call)|child_process\.(exec|spawn)|os\.system\s*\(|\.communicate\s*\(')),
    ('Serialization round-trip', re.compile(r'json\.dumps\s*\(|JSON\.stringify\s*\(|pickle\.(loads|load|dumps|dump)|yaml\.safe_load')),
]

DIR_MARKERS = [
    ('generated SDK/client dir', re.compile(r'^(generated|sdk|client|clients)$', re.I)),
    ('migrations dir', re.compile(r'^(migrations?|alembic|flyway)$', re.I)),
]


def scan(root):
    hits = []
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for label, rx in DIR_MARKERS:
            for d in dirnames:
                if rx.match(d):
                    hits.append((os.path.join(dirpath, d), None, f'directory marker: {label}'))
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            if size > MAX_BYTES:
                continue
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                    text = fh.read()
            except OSError:
                continue
            if '\x00' in text:
                continue
            file_count += 1
            for lineno, line in enumerate(text.splitlines(), 1):
                for label, rx in SIGNATURES:
                    if rx.search(line):
                        hits.append((path, lineno, label))
                        break
    return file_count, hits


def main():
    ap = argparse.ArgumentParser(description='Scan a tree for compatibility consumer signatures (read-only).')
    ap.add_argument('--root', default='.', help='directory to scan (default .)')
    args = ap.parse_args()
    file_count, hits = scan(args.root)
    by_kind = {}
    for path, lineno, label in hits:
        loc = f'{path}:{lineno}' if lineno else path
        print(f'{loc}: {label}')
        by_kind[label] = by_kind.get(label, 0) + 1
    print(f'\nFiles scanned: {file_count}')
    print(f'Candidate consumers: {len(hits)}')
    for label, count in sorted(by_kind.items()):
        print(f'  {count:3d}  {label}')
    print('Candidates are signals, not verdicts; confirm each semantically. Exits 0.')


if __name__ == '__main__':
    main()
