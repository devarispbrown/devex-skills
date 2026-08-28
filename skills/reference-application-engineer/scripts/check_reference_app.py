#!/usr/bin/env python3
"""Check a reference application tree for the nine mandatory production concerns.

Evidence is path and content pattern matching over text files. A match
confirms that wiring exists; it does not certify quality. Semantic review of
every concern remains required, and a passed check is never a production
readiness verdict. Stdlib only.
"""
import argparse
import json
import re
from pathlib import Path

MAX_BYTES = 1 << 20  # skip reading files larger than 1 MiB
SKIP_DIRS = {'__pycache__', '.git', '.venv', 'venv', 'node_modules', '.tox',
             '.pytest_cache', '.mypy_cache', 'dist', 'build', '.next', 'target'}

CONCERNS = [
    {
        'name': 'auth',
        'desc': 'authentication/authorization code (login, token check, scopes)',
        'path': r'(^|/)(auth|login|token|session|middleware)(/|$)|auth[^/]*\.(py|go|ts|js|rb)$',
        'content': r'Authorization|Bearer |\bJWT\b|authenticate|require_token|verify_token|api[_-]?key',
        'hint': 'an auth module or middleware that gates a route or resource',
    },
    {
        'name': 'config',
        'desc': 'config loading (env-driven settings with defaults)',
        'path': r'(^|/)(config|settings)(/|$)|(config|settings)[^/]*\.(py|go|ts|js|rb)$|\.env\.(example|sample)$',
        'content': r'os\.environ|getenv|environ\[|load_dotenv|from_env',
        'hint': 'a settings module reading environment variables with safe defaults',
    },
    {
        'name': 'errors',
        'desc': 'error handling (typed errors, status mapping)',
        'path': r'(^|/)(errors?|exceptions?)(/|$)|(error|exception)s?[^/]*\.(py|go|ts|js|rb)$',
        'content': r'except |raise\s+\w*Error|error_handler|status_code|Error\(',
        'hint': 'a typed error surface with status codes and messages',
    },
    {
        'name': 'retries',
        'desc': 'retry logic (bounded attempts, backoff)',
        'path': r'\bretr|backoff',
        'content': r'\bretry|backoff|max_attempts|max_tries|attempts',
        'hint': 'a bounded retry helper with backoff; never an unbounded loop',
    },
    {
        'name': 'observability',
        'desc': 'observability exports (logs, metrics, traces)',
        'path': r'observab|metrics|tracing|telemetry|logging',
        'content': r'logging\.|getLogger|logger\.|metric|counter|histogram|tracer|exporter|prometheus|opentelemetry|sentry',
        'hint': 'logging setup plus a metrics or tracing export path that is called',
    },
    {
        'name': 'tests',
        'desc': 'tests covering behavior, including failure paths',
        'path': r'(^|/)(test|tests|spec|__tests__)(/|$)|\.(test|spec)\.|test_|_test\.',
        'content': r'pytest|unittest|assert',
        'hint': 'a runnable test suite in the tree',
    },
    {
        'name': 'deployment',
        'desc': 'deployment config (container, manifest, or workflow)',
        'path': r'Dockerfile|docker-compose|compose\.ya?ml|(^|/)k8s?(/|$)|manifest\.ya?ml|serverless\.ya?ml|template\.ya?ml|Procfile|\.github/workflows',
        'content': r'FROM |image:|kind:\s*Deployment|serverless|handler:|runtime:',
        'hint': 'a deployable artifact definition matching the variant',
    },
    {
        'name': 'shutdown',
        'desc': 'graceful shutdown hooks (signal handling, drain)',
        'path': r'shutdown|graceful',
        'content': r'SIGTERM|SIGINT|atexit|on_shutdown|shutdown|graceful|drain|add_signal_handler',
        'hint': 'a signal handler that stops intake, drains in-flight work, and closes clients',
    },
    {
        'name': 'security',
        'desc': 'security practices (secret handling, safe defaults)',
        'path': r'secur|(^|/)secret|\.gitignore$',
        'content': r'secret|SECRET|bcrypt|argon2|scrypt|hash|Content-Security|X-Frame|CORS|sanitize|csrf|TLS|https://',
        'hint': 'secrets read from the environment, never hardcoded; safe defaults on',
    },
]


def iter_text_files(root):
    for p in sorted(root.rglob('*')):
        if p.is_file() and not any(part in SKIP_DIRS for part in p.parts):
            try:
                if p.stat().st_size <= MAX_BYTES:
                    yield p
            except OSError:
                continue


def read_text(p):
    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except OSError:
        return ''
    return '' if '\x00' in text else text


def find_evidence(root, concern):
    path_re = re.compile(concern['path'], re.I)
    content_re = re.compile(concern['content'], re.I)
    path_hits = []
    content_hit = None
    for p in iter_text_files(root):
        rel = p.relative_to(root).as_posix()
        if path_re.search(rel):
            path_hits.append(rel)
        if content_hit is None and content_re.search(read_text(p)):
            content_hit = rel
    if path_hits:
        # Prefer a real source file over a dotfile or __init__ marker.
        for hit in path_hits:
            name = Path(hit).name
            if not name.startswith('.') and not name.startswith('__'):
                return hit, 'path'
        return path_hits[0], 'path'
    return content_hit, 'content' if content_hit else None


def main():
    ap = argparse.ArgumentParser(
        description='Scan a reference application tree for the nine mandatory '
                    'production concerns (evidence check, not quality check).')
    ap.add_argument('tree', help='reference application tree to scan')
    ap.add_argument('--json', action='store_true',
                    help='emit machine-readable JSON instead of the checklist')
    args = ap.parse_args()
    root = Path(args.tree)
    if not root.is_dir():
        raise SystemExit(f'no such directory: {root}')
    rows = []
    for concern in CONCERNS:
        evidence, kind = find_evidence(root, concern)
        rows.append({'name': concern['name'], 'desc': concern['desc'],
                     'evidence': evidence, 'kind': kind, 'hint': concern['hint']})
    missing = [r['name'] for r in rows if not r['evidence']]
    if args.json:
        print(json.dumps({'tree': str(root), 'concerns': rows, 'missing': missing},
                         indent=2))
    else:
        print(f'Coverage checklist for {root}')
        for r in rows:
            if r['evidence']:
                print(f"  [x] {r['name']:<14} {r['evidence']} ({r['kind']})")
            else:
                print(f"  [ ] {r['name']:<14} no evidence found")
                print(f"        hint: {r['hint']}")
        present = len(rows) - len(missing)
        print(f'Summary: {present}/{len(rows)} mandatory concerns present')
        if missing:
            print('MISSING mandatory concerns: ' + ', '.join(missing))
    raise SystemExit(1 if missing else 0)


if __name__ == '__main__':
    main()
