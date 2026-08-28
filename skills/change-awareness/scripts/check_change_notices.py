#!/usr/bin/env python3
"""Check that deprecation, breaking, and removal markers in code are noted in the changelog/notices file. Stdlib only."""
import argparse
import os
import re

SKIP_DIRS = {'.git', 'node_modules', 'vendor', '.venv', 'venv', 'dist', 'build',
             '__pycache__', '.tox', 'target', '.next', '.pytest_cache', '.mypy_cache'}
MAX_BYTES = 2_000_000

MARKERS = [
    ('DEPRECATION', re.compile(
        r'@deprecated\b|@Deprecated\b|@available\([^)]*\bdeprecated\b'
        r'|\#\[deprecated\]|\bObsolete(?:\]|\()|DeprecationWarning\b')),
    ('BREAKING', re.compile(r'BREAKING CHANGE:|BREAKING:\s|@breaking\b')),
    ('REMOVAL', re.compile(r'\bTODO\b(?=[^\n]{0,80}\bremove\b)', re.I)),
]

DEF_RE = re.compile(
    r'^\s*(?:export\s+(?:default\s+)?|public\s+|pub\s+|async\s+)?'
    r'(?:function|def|class|fn|func|struct|interface|enum|trait|let|const|var|static)\s+'
    r'([A-Za-z_]\w*)')


def enclosing_symbol(lines, lineno, stem):
    marker_indent = len(lines[lineno - 1]) - len(lines[lineno - 1].lstrip())
    for i in range(lineno - 1, 0, -1):
        m = DEF_RE.match(lines[i - 1])
        if not m:
            continue
        indent = len(lines[i - 1]) - len(lines[i - 1].lstrip())
        if indent <= marker_indent:
            return m.group(1)
    return stem


def scan(root, changelog_abs, changelog_text):
    findings = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            path = os.path.join(dirpath, name)
            if os.path.abspath(path) == changelog_abs:
                continue
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            if size > MAX_BYTES:
                continue
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                    lines = fh.read().splitlines()
            except OSError:
                continue
            if '\x00' in (''.join(lines[:20])):
                continue
            stem = os.path.splitext(name)[0]
            for lineno, line in enumerate(lines, 1):
                for kind, rx in MARKERS:
                    if not rx.search(line):
                        continue
                    key = enclosing_symbol(lines, lineno, stem)
                    if key and key.lower() in changelog_text:
                        continue
                    findings.append((os.path.relpath(path, root), lineno, kind, key))
    return findings


def main():
    ap = argparse.ArgumentParser(description='Scan code for change markers not noted in the changelog (read-only).')
    ap.add_argument('--root', default='.', help='directory to scan (default .)')
    ap.add_argument('--changelog', '--notices', dest='changelog', default='CHANGELOG.md',
                    help='changelog/notices file to check entries against (default CHANGELOG.md)')
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        raise SystemExit(f'root directory not found: {root}')

    changelog_abs = os.path.abspath(args.changelog)
    if not os.path.isfile(changelog_abs):
        print(f'changelog/notices file not found: {args.changelog} — treating every marker as unnoted')
        changelog_text = ''
    else:
        changelog_text = open(changelog_abs, 'r', encoding='utf-8', errors='replace').read().lower()

    # Deduplicate per file/kind/symbol; one finding per unnoted surface, not per marker.
    seen = set()
    findings = []
    for rel, lineno, kind, key in scan(root, changelog_abs, changelog_text):
        if (rel, kind, key) in seen:
            continue
        seen.add((rel, kind, key))
        findings.append((rel, lineno, kind, key))

    for rel, lineno, kind, key in findings:
        print(f'{rel}:{lineno}: {kind}: {key} not noted in {args.changelog}')
    print(f'Markers found: {len(findings)} unnoted' if findings
          else f'Markers scanned: all noted in {args.changelog}')
    raise SystemExit(1 if findings else 0)


if __name__ == '__main__':
    main()
