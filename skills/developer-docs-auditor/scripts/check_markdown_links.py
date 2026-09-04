#!/usr/bin/env python3
"""Check local Markdown links for missing targets. Stdlib only; does not fetch remote URLs."""
from pathlib import Path
import argparse, re, urllib.parse
LINK=re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root', nargs='?', default='.')
    args=ap.parse_args(); root=Path(args.root).resolve(); bad=[]
    if not Path(args.root).is_dir():
        raise SystemExit(f'not a directory: {args.root}')
    for p in root.rglob('*.md'):
        try: text=p.read_text(errors='ignore')
        except Exception: continue
        for m in LINK.finditer(text):
            raw=m.group(1).strip().split()[0].strip('<>')
            if not raw or raw.startswith(('#','http://','https://','mailto:')): continue
            target=urllib.parse.unquote(raw.split('#',1)[0])
            if not target: continue
            q=(p.parent/target).resolve()
            if not q.exists(): bad.append((p.relative_to(root),raw))
    for p,link in bad: print(f'{p}: missing {link}')
    raise SystemExit(1 if bad else 0)
if __name__=='__main__': main()
