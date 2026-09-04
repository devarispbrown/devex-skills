#!/usr/bin/env python3
"""Find forbidden terminology aliases using a JSON policy. Stdlib only."""
from pathlib import Path
import argparse, json, fnmatch, re


def _read_input(path, what):
    """Read a required input file, or explain why it could not be read.

    The suite's own error-experience standard requires an expected error to say what
    happened, why, where, and how to fix it. A raw traceback answers none of those.
    """
    from pathlib import Path as _P
    p = _P(path)
    if p.is_dir():
        raise SystemExit(f'{path} is a directory, but {what} is expected to be a file.\n'
                         f'Pass the path to the file itself.')
    try:
        return p.read_text(encoding='utf-8', errors='replace')
    except FileNotFoundError:
        raise SystemExit(f'No such file: {path}\nExpected {what}.')
    except OSError as e:
        raise SystemExit(f'Cannot read {path}: {e}\nExpected {what}.')


def _read_json(path, what):
    import json as _j
    text = _read_input(path, what)
    try:
        return _j.loads(text)
    except _j.JSONDecodeError as e:
        raise SystemExit(f'{path} is not valid JSON: {e}\nExpected {what}.')

def matches(path, globs): return any(fnmatch.fnmatch(path, g) for g in globs)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('policy'); ap.add_argument('--root', default='.')
    a=ap.parse_args(); root=Path(a.root).resolve(); policy=_read_json(a.policy, 'a terminology policy')
    if not Path(a.root).is_dir():
        raise SystemExit(f'not a directory: {a.root}')
    include=policy.get('include_globs',['**/*.md']); exclude=policy.get('exclude_globs',[])
    findings=[]
    for p in root.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(root).as_posix()
        if not matches(rel,include) or matches(rel,exclude): continue
        try: lines=p.read_text(errors='ignore').splitlines()
        except Exception: continue
        for canonical,spec in policy.get('canonical',{}).items():
            for alias in spec.get('forbidden_aliases',[]):
                rx=re.compile(r'(?<!\w)'+re.escape(alias)+r'(?!\w)', re.I)
                for i,line in enumerate(lines,1):
                    if rx.search(line): findings.append((rel,i,alias,canonical))
    for rel,i,alias,canonical in findings:
        print(f'{rel}:{i}: use canonical "{canonical}" instead of "{alias}" (review context)')
    raise SystemExit(1 if findings else 0)
if __name__=='__main__': main()
