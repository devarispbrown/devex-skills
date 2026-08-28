#!/usr/bin/env python3
"""Inventory a test suite and map findings to system-type gaps. Stdlib only.

Read-only assessment: never creates, modifies, or deletes files. Detects
test files by framework patterns, fuzz/property/contract targets, and CI
test config, then maps findings to a system-type gap checklist. Always
exits 0 — this script informs, it never fails a build.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {'.git', '.hg', '.svn', 'node_modules', 'venv', '.venv',
             '__pycache__', 'build', 'dist', 'target', '.mypy_cache',
             '.pytest_cache', '.tox', '.idea', '.vscode'}
MAX_READ_BYTES = 1 << 20  # skip files larger than 1 MiB

TEST_FILE_RE = {
    'pytest': re.compile(r'^(test_[^/]*\.py|[^/]*_test\.py|conftest\.py)$'),
    'go test': re.compile(r'^[^/]*_test\.go$'),
    'jest/vitest': re.compile(r'^[^/]*\.(test|spec)\.(js|ts|jsx|tsx)$'),
    'junit report': re.compile(r'^(junit[^/]*\.xml|TEST-[^/]*\.xml)$'),
}
CARGO_TEST_RE = re.compile(r'#\[(tokio::)?test\]')
FUZZ_CONTENT_RE = re.compile(r'atheris|fuzz_target!|func Fuzz[A-Z]|go-fuzz', re.I)
PROPERTY_CONTENT_RE = re.compile(r'from hypothesis|@given\(|proptest!|quickcheck', re.I)
CONTRACT_CONTENT_RE = re.compile(r'pact|contract test|contract-testing', re.I)
SCHEMA_FILE_RE = re.compile(r'(^|/)(schema|openapi|asyncapi|swagger)[^/]*\.(json|ya?ml)$', re.I)
CONTRACT_DIR_RE = re.compile(r'(^|/)(contracts?|pact|schemas?)(/|$)', re.I)
FUZZ_DIR_RE = re.compile(r'(^|/)(fuzz|fuzzing|corpus)(/|$)', re.I)
INTEGRATION_DIR_RE = re.compile(r'(^|/)(integration|e2e|smoke)(/|$|-|_)', re.I)
TEST_CMD_RE = re.compile(
    r'pytest|go test|cargo test|npm (run )?test|yarn test|pnpm test|jest|vitest|'
    r'mvn test|gradle test|unittest|coverage|terraform (plan|validate)', re.I)
MARKER_RE = {
    'failure injection': re.compile(r'fault inject|chaos|kill.?switch|circuit.?break', re.I),
    'race tests': re.compile(r'\b-race\b|detect_races|tsan|thread-sanitizer', re.I),
    'snapshot tests': re.compile(r'snapshot|toMatchSnapshot|golden', re.I),
    'compatibility tests': re.compile(r'compatib|matrix', re.I),
    'migration tests': re.compile(r'migrat|upgrade path', re.I),
    'plan/apply validation': re.compile(r'terraform (plan|validate)|plan -out', re.I),
}
SUPPORT_CLAIM_FILES = {'pyproject.toml', 'setup.cfg', 'setup.py', 'package.json',
                       'go.mod', '.python-version', 'tox.ini'}
CI_FILES = [
    '.github/workflows/*.yml', '.github/workflows/*.yaml',
    '.gitlab-ci.yml', '.circleci/config.yml', 'azure-pipelines.yml',
    'Jenkinsfile', 'Jenkinsfile.*', 'tox.ini', 'Makefile', 'pytest.ini',
    '.coveragerc', 'pom.xml', 'build.gradle', 'build.gradle.kts',
]

SYSTEM_HINTS = {
    'CRUD API': re.compile(r'(^|/)(api|apis|handler|handlers|route|routes|controller|controllers|endpoint|endpoints|server|graphql)(/|$|-|\.)|\.app\.py$', re.I),
    'streaming pipeline': re.compile(r'stream|kafka|pipeline|consumer|producer|topic|events?|flink|spark|rabbitmq', re.I),
    'stateful service': re.compile(r'(^|/)(db|database|redis|postgres|mysql|mongo|sqlite|cache|store|state)(/|$|-|\.)|migration', re.I),
    'CLI': re.compile(r'(^|/)(cli|cmd|bin)(/|$)|click|argparse|typer|commander|subcommand', re.I),
    'library': re.compile(r'(^|/)(lib|src|packages|internal)(/|$)|(^|/)setup\.py$|(^|/)pyproject\.toml$', re.I),
    'infrastructure': re.compile(r'(^|/)(terraform|infra|helm|k8s|kubernetes|cloudformation|pulumi)(/|$)|\.tf$|Dockerfile', re.I),
}
# Technique families and the evidence keys that close the gap for each type.
TECHNIQUE_EVIDENCE = {
    'unit tests': ('pytest', 'go test', 'jest/vitest', 'cargo test'),
    'integration tests': ('integration',),  # special-cased below
    'contract tests': ('contract', 'schema'),
    'schema tests': ('schema',),
    'property tests': ('property',),
    'fuzz tests': ('fuzz',),
    'failure injection': ('failure injection',),
    'race tests': ('race tests',),
    'snapshot tests': ('snapshot tests',),
    'compatibility tests': ('compatibility tests',),
    'migration tests': ('migration tests',),
    'plan/apply validation': ('plan/apply validation',),
}
TYPE_TECHNIQUES = {
    'CRUD API': ('unit tests', 'contract tests', 'schema tests', 'property tests'),
    'streaming pipeline': ('integration tests', 'failure injection', 'compatibility tests'),
    'stateful service': ('race tests', 'migration tests', 'snapshot tests'),
    'CLI': ('snapshot tests', 'property tests', 'unit tests'),
    'library': ('property tests', 'fuzz tests', 'compatibility tests'),
    'infrastructure': ('plan/apply validation', 'failure injection'),
}


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            yield Path(dirpath) / name


def read_small(path):
    try:
        if path.stat().st_size > MAX_READ_BYTES:
            return ''
        return path.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return ''


def rel_str(root, path):
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def main():
    ap = argparse.ArgumentParser(
        description='Read-only test suite inventory mapped to system-type gaps. Never fails.')
    ap.add_argument('root', nargs='?', default='.',
                    help='repository root to scan (default: current directory)')
    ap.add_argument('--json', action='store_true',
                    help='emit machine-readable JSON instead of the checklist')
    a = ap.parse_args()

    root = Path(a.root).resolve()
    if not root.is_dir():
        raise SystemExit(f'not a directory: {root}')
    self_path = Path(__file__).resolve()

    found = {k: [] for k in TEST_FILE_RE}
    found['cargo test'] = []
    found['property'] = []
    found['fuzz'] = []
    found['contract'] = []
    found['schema'] = []
    found['integration'] = []
    for key in MARKER_RE:
        found[key] = []
    ci_configs = []
    ci_commands = set()
    support_claims = []
    hints = {t: [] for t in SYSTEM_HINTS}

    for path in walk(root):
        name = path.name
        r = rel_str(root, path)
        for fw, pat in TEST_FILE_RE.items():
            if pat.match(name):
                found[fw].append(r)
        if name.endswith('.rs') and CARGO_TEST_RE.search(read_small(path)):
            found['cargo test'].append(r)
        if INTEGRATION_DIR_RE.search(r):
            found['integration'].append(r)
        if SCHEMA_FILE_RE.search(r):
            found['schema'].append(r)
        if CONTRACT_DIR_RE.search(r):
            found['contract'].append(r)
        if FUZZ_DIR_RE.search(r):
            found['fuzz'].append(r)
        if any(Path(r).match(p) for p in CI_FILES):
            ci_configs.append(r)
        for t, pat in SYSTEM_HINTS.items():
            if pat.search(r):
                hints[t].append(r)

    # Content-based markers on source/test files and CI configs.
    for path in walk(root):
        r = rel_str(root, path)
        if path.resolve() == self_path:
            continue  # never let the scanner match its own pattern literals
        if path.name.endswith(('.py', '.rs', '.go', '.js', '.ts', '.json', '.xml')):
            content = read_small(path)
            if PROPERTY_CONTENT_RE.search(content):
                found['property'].append(r)
            if FUZZ_CONTENT_RE.search(content):
                found['fuzz'].append(r)
            if CONTRACT_CONTENT_RE.search(content):
                found['contract'].append(r)
            for key, pat in MARKER_RE.items():
                if pat.search(content):
                    found[key].append(r)
        if any(Path(r).match(p) for p in CI_FILES):
            content = read_small(path)
            for m in TEST_CMD_RE.finditer(content):
                ci_commands.add(m.group(0))
            if re.search(r'junit|test-results|coverage', content, re.I):
                ci_commands.add('reporting')

    # Supported-version claims vs CI matrix evidence (UNTESTED_SUPPORTED_VERSION).
    for path in walk(root):
        if path.name not in SUPPORT_CLAIM_FILES:
            continue
        content = read_small(path)
        claim = None
        m = re.search(r'(?:python_requires|requires-python)\s*=\s*["\']([^"\']+)', content)
        if m:
            claim = f'python_requires {m.group(1)}'
        m = re.search(r'"engines"\s*:\s*\{[^}]*"node"\s*:\s*"([^"]+)"', content)
        if m:
            claim = f'node engines {m.group(1)}'
        m = re.search(r'^go\s+([0-9.]+)', content, re.M)
        if m:
            claim = f'go {m.group(1)}'
        if claim:
            support_claims.append((rel_str(root, path), claim))
    ci_matrix = any(
        re.search(r'python-version|go-version|node-version|matrix|strategy', read_small(path))
        for path in walk(root) if any(Path(rel_str(root, path)).match(p) for p in CI_FILES))

    def has_evidence(technique):
        if technique == 'integration tests':
            return bool(found['integration']) or bool(ci_commands & {'e2e', 'integration'})
        return any(found[k] for k in TECHNIQUE_EVIDENCE[technique])

    if a.json:
        payload = {k: v for k, v in found.items()}
        payload['ci_configs'] = ci_configs
        payload['ci_test_commands'] = sorted(ci_commands)
        payload['ci_matrix_evidence'] = ci_matrix
        payload['support_claims'] = [f'{f}: {c}' for f, c in support_claims]
        payload['system_type_hints'] = {k: v for k, v in hints.items()}
        print(json.dumps(payload, indent=2))
        raise SystemExit(0)

    print(f'Test suite inventory for: {root}')
    print(f'{"framework":16} {"files":>4}')
    for fw in list(TEST_FILE_RE) + ['cargo test', 'integration', 'property', 'fuzz',
                                    'contract', 'schema']:
        print(f'{fw:16} {len(found[fw]):>4}')

    print('\nFuzz/property/contract targets')
    listed = 0
    for kind in ('property', 'fuzz', 'contract', 'schema'):
        for f in found[kind][:8]:
            print(f'  {kind:9} {f}')
            listed += 1
        if len(found[kind]) > 8:
            print(f'  ... {len(found[kind]) - 8} more')
    if not listed:
        print('  none detected')

    print('\nCI test config')
    if ci_configs:
        for c in sorted(set(ci_configs)):
            print(f'  {c}')
        if ci_commands:
            print('  commands: ' + ', '.join(sorted(ci_commands)))
    else:
        print('  NONE FOUND — no CI test jobs detected')

    print('\nSupported-version claims and CI evidence')
    if support_claims:
        for f, c in support_claims:
            verdict = 'CI matrix evidence found' if ci_matrix else 'NO CI matrix evidence'
            print(f'  {f}: {c} -> {verdict}')
        if not ci_matrix:
            print('  WARNING: support claims without CI matrix evidence risk the '
                  'UNTESTED_SUPPORTED_VERSION gate')
    else:
        print('  none detected')

    print('\nSystem-type hints and gap checklist (heuristic — confirm against '
          'production behavior)')
    any_tests = any(found[k] for k in ('pytest', 'go test', 'jest/vitest', 'cargo test'))
    for t, files in hints.items():
        if not files:
            continue
        print(f'\n  {t}: {len(files)} hint path(s)')
        for f in files[:6]:
            print(f'    {f}')
        if len(files) > 6:
            print(f'    ... {len(files) - 6} more')
        for m in TYPE_TECHNIQUES[t]:
            if has_evidence(m):
                print(f'    present: {m}')
            else:
                sev = 'P1 heuristic' if not any_tests else 'P2 heuristic'
                print(f'    GAP {sev}: {t} without {m} — no test protects this failure mode')

    total = sum(len(v) for v in found.values())
    types = len([t for t, v in hints.items() if v])
    print(f'\nChecklist: {total} test-related files across {types} system-type hint(s). '
          f'Verify gaps by mapping production behavior before acting.')
    print('No build failure: this script informs only (exit 0).')
    raise SystemExit(0)


if __name__ == '__main__':
    main()
