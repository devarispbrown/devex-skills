#!/usr/bin/env python3
"""Find forbidden terminology aliases using a JSON policy. Stdlib only."""
from pathlib import Path
import argparse, json, fnmatch, re

def matches(path, globs): return any(fnmatch.fnmatch(path, g) for g in globs)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('policy'); ap.add_argument('--root', default='.')
    a=ap.parse_args(); root=Path(a.root).resolve(); policy=json.loads(Path(a.policy).read_text())
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
