#!/usr/bin/env python3
"""Inventory a repository tree for operational trust artifacts: status page
config, incident templates, SLO/SLA docs, webhook retry logic, and degraded-state
handling. Prints a checklist with gaps. Informs only; a successful scan exits 0
regardless of gaps. Stdlib only.
"""
import argparse, re
from pathlib import Path

SKIP_DIRS={'node_modules','vendor','.git','__pycache__','.venv','venv','dist','build','target','.tox'}
CONFIG_EXTS={'.json','.yaml','.yml','.toml'}
DOC_EXTS={'.md','.markdown','.txt','.hbs'}
CODE_EXTS={'.py','.js','.ts','.go','.rb','.java','.rs','.kt','.php','.cs'}

CATEGORIES=[
  dict(name='status-page', label='status page config', exts=CONFIG_EXTS,
       dir_re=re.compile(r'^(status|statuspage|status-page|uptime)$', re.I),
       name_re=re.compile(r'(^|[/_.-])status([/_.-]|$)', re.I),
       content_re=re.compile(r'"components"\s*:|"incidents"\s*:|status_page', re.I)),
  dict(name='incident-template', label='incident template', exts=DOC_EXTS|CONFIG_EXTS,
       name_re=re.compile(r'(incident|postmortem|post-mortem).*(template|tpl)|(template|tpl).*(incident|postmortem)', re.I),
       content_re=re.compile(r'incident\s*template|postmortem\s*template|\[STATUS\]\s*:|{{[- ]*(status|impact|timeline)', re.I)),
  dict(name='slo-docs', label='SLO/SLA docs', exts=DOC_EXTS|CONFIG_EXTS,
       name_re=re.compile(r'(^|[/_.-])(slo|sla|sli|error[_.-]?budget|reliability)([/._-]|$)', re.I),
       content_re=re.compile(r'error\s*budget|slo\s*:\s*\d|sla\s*:\s*\d|99\.\d+\s*%\s*(uptime|availability)', re.I)),
  dict(name='webhook-retries', label='webhook retry logic', exts=CODE_EXTS,
       name_re=re.compile(r'webhook|deliver[y]?', re.I),
       content_re=re.compile(r'webhook', re.I),
       require=re.compile(r'retry|backoff|max_attempts|max_retries|dead.?letter', re.I)),
  dict(name='degraded-state', label='degraded-state handling', exts=CODE_EXTS,
       name_re=re.compile(r'degraded|circuit.?breaker|fallback|graceful', re.I),
       content_re=re.compile(r'degraded|circuit[_.-]?breaker|circuit breaker|fallback|graceful', re.I)),
]

def matches(cat, rel, text):
    ext=rel.suffix.lower()
    if ext not in cat['exts']: return False
    if cat.get('dir_re') and any(cat['dir_re'].match(p) for p in rel.parts): return True
    if cat['name_re'].search(str(rel)): return True
    if not text: return False
    if not cat['content_re'].search(text): return False
    req=cat.get('require')
    return req is None or bool(req.search(text))

def main():
    ap=argparse.ArgumentParser(description='Inventory a tree for operational trust artifacts (informative only).')
    ap.add_argument('root', nargs='?', default='.', help='directory to scan (default: .)')
    ap.add_argument('--verbose', action='store_true', help='list every matching file')
    a=ap.parse_args()
    root=Path(a.root)
    if not root.is_dir(): raise SystemExit(f'Not a directory: {root}')
    found={c['name']: [] for c in CATEGORIES}
    for p in sorted(root.rglob('*')):
        if p.is_dir(): continue
        rel=p.relative_to(root)
        if any(part in SKIP_DIRS or part.startswith('.') for part in rel.parts): continue
        try: text=p.read_text(errors='ignore')
        except OSError: text=''
        for c in CATEGORIES:
            if matches(c, rel, text): found[c['name']].append(str(rel))
    gaps=[]
    print(f'Trust surface inventory: {root}')
    for c in CATEGORIES:
        hits=found[c['name']]
        if hits:
            shown=', '.join(hits) if a.verbose else hits[0] + (f' (+{len(hits)-1} more)' if len(hits)>1 else '')
            print(f'  [x] {c["label"]:<24} {shown}')
        else:
            gaps.append(c['name'])
            print(f'  [ ] {c["label"]:<24} MISSING')
    print('Gaps: ' + (', '.join(gaps) if gaps else 'none'))

if __name__=='__main__': main()
