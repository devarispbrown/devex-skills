#!/usr/bin/env python3
"""Scan a tree for configuration surface: mechanisms, duplicates, unsafe defaults. Stdlib only."""
import argparse
import json
import os
import re
from collections import Counter, defaultdict

SKIP_DIRS = {
    '.git', '.hg', '.svn', 'node_modules', 'vendor', '.venv', 'venv',
    'dist', 'build', '__pycache__', '.tox', '.mypy_cache', '.pytest_cache',
    '.next', 'target', 'coverage', '.eggs', '.gradle', 'site-packages',
}
MAX_BYTES = 2_000_000

SECRET_KEY_RE = re.compile(
    r'(password|passwd|secret|token|api[-_]?key|apikey|credential|'
    r'private[-_]?key|access[-_]?key|client[-_]?secret|auth)',
    re.I,
)

ENV_READ_PATTERNS = [
    re.compile(r'os\.environ\.get\(\s*["\']([A-Za-z_][A-Za-z0-9_]*)["\']', re.I),
    re.compile(r'os\.environ\[["\']([A-Za-z_][A-Za-z0-9_]*)["\']\]', re.I),
    re.compile(r'os\.getenv\(\s*["\']([A-Za-z_][A-Za-z0-9_]*)["\']', re.I),
    re.compile(r'process\.env\.([A-Za-z_][A-Za-z0-9_]*)', re.I),
    re.compile(r'process\.env\[["\']([A-Za-z_][A-Za-z0-9_]*)["\']\]', re.I),
    re.compile(r'System\.getenv\(\s*["\']([A-Za-z_][A-Za-z0-9_]*)["\']', re.I),
    re.compile(r'std::env::var\(\s*["\']([A-Za-z_][A-Za-z0-9_]*)["\']'),
]

ENV_FALLBACK_RE = re.compile(
    r'os\.(?:getenv|environ\.get)\(\s*["\']([A-Za-z_][A-Za-z0-9_]*)["\']\s*,\s*["\']([^"\']*)["\']',
    re.I,
)

LOADER_PATTERNS = [
    ('yaml', re.compile(r'yaml\.(?:safe_load|load)\s*\(')),
    ('json', re.compile(r'json\.load\s*\(')),
    ('toml', re.compile(r'(?:toml|tomllib)\.(?:load|loads)\s*\(')),
    ('ini', re.compile(r'configparser|ConfigParser')),
    ('dotenv', re.compile(r'load_dotenv|dotenv_values')),
]

FLAG_NAME_PATTERNS = [
    re.compile(r'add_argument\(\s*["\']--?([a-z][a-z0-9-]*)["\']'),
    re.compile(r'flag\.\w+\(\s*["\']([a-z][a-z0-9-]*)["\']'),
    re.compile(r'#[^\n]*\blong\s*=\s*["\']([a-z][a-z0-9-]*)["\']'),
    re.compile(r'#[^\n]*\bname\s*=\s*["\']([a-z][a-z0-9-]*)["\']'),
]
DEFAULT_LITERAL_RE = re.compile(r'default(?:_value)?\s*=\s*["\']?([^"\'\s,)]+)["\']?')
GO_FLAG_DEFAULT_RE = re.compile(
    r'flag\.\w+\(\s*["\'][a-z][a-z0-9-]*["\']\s*,\s*(?:["\']([^"\']*)["\']|(-?\d+(?:\.\d+)?))'
)

CONFIG_EXT = {'.yaml': 'yaml', '.yml': 'yaml', '.json': 'json', '.toml': 'toml'}
MECH_ENV, MECH_FILE, MECH_FLAGS = 'env', 'config-file', 'flags'

KEYVAL_RE = re.compile(r'^(\s*)([\w.-]+)\s*(?::|=)\s*(.*)$')


def norm(key):
    return re.sub(r'[-_.]', '', key).lower()


def _env_keys(line):
    keys = []
    for rx in ENV_READ_PATTERNS:
        for m in rx.finditer(line):
            keys.append(m.group(1))
    return list(dict.fromkeys(keys))


def _flag_names(line):
    names = []
    for rx in FLAG_NAME_PATTERNS:
        for m in rx.finditer(line):
            names.append(m.group(1))
    return list(dict.fromkeys(names))


def _json_keys(node, prefix):
    out = []
    for k, v in node.items():
        key = f'{prefix}.{k}' if prefix else str(k)
        if isinstance(v, dict):
            out.extend(_json_keys(v, key))
        elif v is not None:
            out.append((key, str(v)))
    return out


def _config_file_keys(path, ext, text):
    """Extract (path, lineno_or_None, dotted_key, scalar_value) for config files."""
    if ext == '.json':
        try:
            data = json.loads(text)
        except ValueError:
            return []
        if not isinstance(data, dict):
            return []
        return [(path, None, dotted, value) for dotted, value in _json_keys(data, '')]
    out = []
    stack = []  # (indent, segment)
    section = ''
    for lineno, raw in enumerate(text.splitlines(), 1):
        stripped = raw.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if ext == '.toml' and stripped.startswith('[') and stripped.endswith(']'):
            section = stripped[1:-1].strip()
            continue
        m = KEYVAL_RE.match(raw)
        if not m:
            continue
        indent, name, value = m.group(1), m.group(2), m.group(3)
        value = re.split(r'\s+#', value, maxsplit=1)[0].strip().strip('"\'')
        while stack and len(indent) <= stack[-1][0]:
            stack.pop()
        segments = [seg for _, seg in stack]
        if section:
            segments.append(section)
        segments.append(name)
        stack.append((len(indent), name))
        out.append((path, lineno, '.'.join(segments), value))
    return out


def scan(root):
    env_reads = []
    file_keys = []
    flag_defs = []
    loaders = {}
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            ext = os.path.splitext(name)[1].lower()
            try:
                if os.path.getsize(path) > MAX_BYTES:
                    continue
            except OSError:
                continue
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                    text = fh.read()
            except OSError:
                continue
            if '\x00' in text:
                continue
            file_count += 1
            if ext in CONFIG_EXT:
                file_keys.extend(_config_file_keys(path, ext, text))
                continue
            seen_loaders = set()
            for lineno, line in enumerate(text.splitlines(), 1):
                fb_by_key = {}
                for m in ENV_FALLBACK_RE.finditer(line):
                    fb_by_key[m.group(1)] = m.group(2)
                for key in _env_keys(line):
                    env_reads.append((path, lineno, key, fb_by_key.get(key)))
                for kind, rx in LOADER_PATTERNS:
                    if rx.search(line):
                        seen_loaders.add(kind)
                for fname in _flag_names(line):
                    default = None
                    gm = GO_FLAG_DEFAULT_RE.search(line)
                    if gm:
                        default = gm.group(1) or gm.group(2)
                    else:
                        dm = DEFAULT_LITERAL_RE.search(line)
                        if dm:
                            default = dm.group(1)
                    flag_defs.append((path, lineno, fname, default))
            if len(seen_loaders) >= 2:
                loaders[path] = sorted(seen_loaders)
    return file_count, env_reads, file_keys, flag_defs, loaders


def _loc(path, lineno):
    return f'{path}:{lineno}' if lineno else str(path)


def _redact(norm_key, value):
    return value if not SECRET_KEY_RE.search(norm_key) else '<redacted>'


def analyze(env_reads, file_keys, flag_defs, loaders):
    findings = []
    mech = defaultdict(list)  # norm key -> [(kind, path, lineno, display)]
    defaults = defaultdict(list)  # norm key -> [(value, path, lineno)]

    for path, lineno, key, fb in env_reads:
        mech[norm(key)].append((MECH_ENV, path, lineno, key))
        if fb:
            defaults[norm(key)].append((fb, path, lineno))
    for path, lineno, dotted, value in file_keys:
        mech[norm(dotted)].append((MECH_FILE, path, lineno, dotted))
        if value:
            defaults[norm(dotted)].append((value, path, lineno))
    for path, lineno, fname, default in flag_defs:
        mech[norm(fname)].append((MECH_FLAGS, path, lineno, fname))
        if default:
            defaults[norm(fname)].append((default, path, lineno))

    for nk in sorted(mech):
        kinds = sorted({k for k, _, _, _ in mech[nk]})
        if len(kinds) >= 2:
            locs = ', '.join(_loc(p, ln) for _, p, ln, _ in mech[nk][:6])
            findings.append(('DUPLICATE MECHANISM',
                f"key {nk!r} reachable through {len(kinds)} mechanisms "
                f"({', '.join(kinds)}): {locs}"))

    for path, lineno, key, fb in env_reads:
        if fb and SECRET_KEY_RE.search(key):
            findings.append(('UNSAFE DEFAULT',
                f"secret-pattern env var {key} has a committed default at {_loc(path, lineno)}"))
    for path, lineno, dotted, value in file_keys:
        if (SECRET_KEY_RE.search(dotted) and value
                and value.lower() not in {'null', 'none', 'true', 'false'}):
            findings.append(('UNSAFE DEFAULT',
                f"secret-pattern key {dotted} has a committed value at {_loc(path, lineno)}"))
    for path, lineno, fname, default in flag_defs:
        if default and SECRET_KEY_RE.search(fname):
            findings.append(('UNSAFE DEFAULT',
                f"secret-pattern flag --{fname} has a committed default at {_loc(path, lineno)}"))

    for nk in sorted(defaults):
        entries = defaults[nk]
        distinct = {v for v, _, _ in entries}
        if len(distinct) >= 2:
            first = entries[0]
            other = next(e for e in entries if e[0] != first[0])
            findings.append(('CONTRADICTORY DEFAULTS',
                f"key {nk!r} has conflicting defaults {_redact(nk, first[0])!r} at "
                f"{_loc(first[1], first[2])} vs {_redact(nk, other[0])!r} at "
                f"{_loc(other[1], other[2])}"))

    files_by_key = defaultdict(set)
    for path, _lineno, dotted, _value in file_keys:
        files_by_key[norm(dotted)].add(path)
    for nk in sorted(files_by_key):
        paths = sorted(files_by_key[nk])
        if len(paths) >= 2:
            findings.append(('UNCLEAR PRECEDENCE',
                f"key {nk!r} appears in multiple config files ({', '.join(paths)}); "
                "file precedence is undefined"))
    for path in sorted(loaders):
        findings.append(('UNCLEAR PRECEDENCE',
            f"multiple loaders in {path} ({', '.join(loaders[path])}); "
            "merge order is undefined"))

    return findings, mech


def main():
    ap = argparse.ArgumentParser(
        description='Scan a tree for config surface: mechanisms, duplicates, unsafe defaults. '
                    'Read-only; exits 0.')
    ap.add_argument('--root', default='.', help='directory to scan (default .)')
    args = ap.parse_args()

    file_count, env_reads, file_keys, flag_defs, loaders = scan(args.root)
    findings, _mech = analyze(env_reads, file_keys, flag_defs, loaders)

    print(f'Configuration surface scan of {os.path.abspath(args.root)}')
    print(f'Files scanned: {file_count}')
    print()
    print('Mechanism inventory')
    for path, lineno, key, fb in sorted(env_reads):
        note = ' (has fallback default)' if fb else ''
        print(f'  {_loc(path, lineno):54} env         {key}{note}')
    for path, lineno, dotted, _value in sorted(file_keys):
        print(f'  {_loc(path, lineno):54} config-file {dotted}')
    for path, lineno, fname, default in sorted(flag_defs):
        note = ' (has default)' if default else ''
        print(f'  {_loc(path, lineno):54} flags       --{fname}{note}')

    print()
    print('Findings')
    if findings:
        for kind, msg in findings:
            print(f'  [{kind}] {msg}')
    else:
        print('  none')
    counts = Counter(kind for kind, _ in findings)
    detail = ', '.join(f'{counts[k]} {k}' for k in sorted(counts)) or '0 findings'
    print()
    print(f'Summary: {len(env_reads)} env reads, {len(file_keys)} config-file keys, '
          f'{len(flag_defs)} flag definitions; {len(findings)} findings ({detail}).')
    print('Findings are heuristic signals, not verdicts; confirm each semantically. Exits 0.')
    raise SystemExit(0)


if __name__ == '__main__':
    main()
