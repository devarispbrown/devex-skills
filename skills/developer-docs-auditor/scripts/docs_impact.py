#!/usr/bin/env python3
"""Heuristic git-diff documentation impact scanner. Stdlib only."""
import argparse, subprocess, re

RULES = [
    (re.compile(r'(^|/)(openapi|swagger|asyncapi).*\.(ya?ml|json)$|\.proto$|schema', re.I), ['API reference','SDK parity','examples','changelog/migration']),
    (re.compile(r'(^|/)(cmd|cli)(/|$)|command|flags?', re.I), ['CLI reference','README/quickstart','examples']),
    (re.compile(r'config|\.env|settings|options', re.I), ['configuration reference','README/quickstart','deployment docs']),
    (re.compile(r'auth|oauth|token|credential|permission|rbac', re.I), ['authentication docs','quickstart','security docs','examples']),
    (re.compile(r'error|exception', re.I), ['error reference','troubleshooting','examples']),
    (re.compile(r'webhook|event', re.I), ['event/webhook reference','examples','how-to guides']),
    (re.compile(r'sdk|client|generated', re.I), ['SDK docs','examples','compatibility matrix']),
    (re.compile(r'package\.json|pyproject\.toml|go\.mod|Cargo\.toml|pom\.xml|build\.gradle', re.I), ['install docs','runtime compatibility','README','release notes']),
]

def changed_files(base, head):
    cmd=['git','diff','--name-only',f'{base}...{head}']
    return [x for x in subprocess.check_output(cmd, text=True).splitlines() if x.strip()]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--base', default='HEAD~1')
    ap.add_argument('--head', default='HEAD')
    args=ap.parse_args()
    try: files=changed_files(args.base,args.head)
    except Exception as e:
        raise SystemExit(f'git diff failed: {e}')
    impacts={}
    for f in files:
        for rx, surfaces in RULES:
            if rx.search(f):
                impacts.setdefault(f,set()).update(surfaces)
    print(f'Changed files: {len(files)}')
    if not impacts:
        print('No heuristic public-surface impacts detected. Semantic review is still required.')
        return
    for f in sorted(impacts):
        print(f'\n{f}')
        for s in sorted(impacts[f]): print(f'  - {s}')
    print('\nHeuristic only: verify whether behavior actually changed.')
if __name__=='__main__': main()
