#!/usr/bin/env python3
"""Inventory extension surface signals in a tree and check them against the
stability-guarantee checklist. Stdlib only.

Scans for plugin manifests, hook registrations, and exported extension
interfaces (JS/TS, Python, Rust, Java patterns), then prints an inventory and
a per-item PASS/GAP checklist. Informational only: a completed scan always
exits 0 even when gaps are reported. Gaps require semantic confirmation.

Stdlib only.
"""
import argparse, json, os, re, sys

MANIFEST_NAMES={'plugin.json','plugin.yaml','plugin.yml','extension.json'}
VERSION_KEYS={'core_versions','requires_core','min_core_version','max_core_version',
              'api_version','version_contract','compatible_versions'}
YAML_KEY_RE=re.compile(r'^\s*(core_versions|requires_core|min_core_version|max_core_version|api_version|version_contract|compatible_versions)\s*:\s*\S')
TIER_TAGS=re.compile(r'@(stable|experimental|deprecated|public|since|compat)\b|supported_versions\b|api_version\b',re.I)
HOOK_RE=re.compile(r'(registerHook|hooks\.register|hookRegister|addHook|hook\s*:|"hook"\s*:|\x27hook\x27\s*:)')
HOOK_SCHEMA_RE=re.compile(r'(args_schema|params\s*:|schema\s*:|\x22args\x22\s*:)')
JS_EXPORT_RE=re.compile(r'^export\s+(default\s+)?(function|const|class|interface|type)\s+\w+')
RUST_PUB_RE=re.compile(r'^\s*pub\s+(?!\(crate\)|\(super\)|\(in\b)(fn|struct|trait|enum)\s+[A-Za-z_]\w*')
JAVA_IFACE_RE=re.compile(r'^\s*public\s+interface\s+[A-Za-z_]\w*')
PY_EXPORT_RE=re.compile(r'^\s*__all__\s*=')
PY_DECORATOR_RE=re.compile(r'^\s*@(public|stable|experimental|deprecated)\b')
POLICY_FILES={'compatibility.md','breaking-changes.md','breaking-change-policy.md','extension-policy.md'}
POLICY_HINT_RE=re.compile(r'breaking\s+change\s+policy|breaking-change',re.I)

def iter_files(root):
    for dirpath,_dirs,files in os.walk(root):
        for f in sorted(files):
            p=os.path.join(dirpath,f)
            if '__pycache__' in dirpath or f.startswith('.'): continue
            yield p

def read_lines(p):
    try:
        with open(p,encoding='utf-8',errors='replace') as fh: return fh.read().splitlines()
    except OSError as e:
        print(f'WARN: unreadable {p}: {e}',file=sys.stderr); return []

def is_manifest(p):
    b=os.path.basename(p)
    if b in MANIFEST_NAMES: return True
    if b=='manifest.json':
        try: data=json.loads(open(p,encoding='utf-8').read())
        except (OSError,ValueError): return False
        return isinstance(data,dict) and (data.get('type')=='plugin' or 'hooks' in data or 'capabilities' in data)
    return False

def scan_manifest(p):
    b=os.path.basename(p); ok_name=ok_version=False; versions=[]; caps=0; hooks=[]
    if b.endswith('.json'):
        try: data=json.loads(open(p,encoding='utf-8').read())
        except (OSError,ValueError) as e:
            raise SystemExit(f'ERROR: unparsable manifest {p}: {e}')
        ok_name=bool(data.get('name')); ok_version=bool(data.get('version'))
        caps=len(data.get('capabilities',[])) if isinstance(data.get('capabilities'),list) else 0
        hooks=[str(h.get('name')) for h in data.get('hooks',[]) if isinstance(h,dict) and h.get('name')]
        def walk(o):
            if isinstance(o,dict):
                for k,v in o.items():
                    if k in VERSION_KEYS and v: versions.append(k)
                    walk(v)
            elif isinstance(o,list):
                for v in o: walk(v)
        walk(data)
    else:
        for line in read_lines(p):
            m=re.match(r'^\s*(\w+)\s*:',line)
            if m:
                k=m.group(1)
                if k=='name' and line.split(':',1)[1].strip(): ok_name=True
                if k=='version' and line.split(':',1)[1].strip(): ok_version=True
                if k in VERSION_KEYS and line.split(':',1)[1].strip(): versions.append(k)
    return {'name_ok':ok_name,'version_ok':ok_version,'version_keys':versions,
            'capabilities':caps,'hooks':hooks}

def scan_hooks(p):
    found=[]
    for i,line in enumerate(read_lines(p),1):
        if HOOK_RE.search(line):
            schema=bool(HOOK_SCHEMA_RE.search(line)) or any(HOOK_SCHEMA_RE.search(l) for l in read_lines(p)[max(0,i-1):i+3])
            found.append((i,line.strip()[:60],schema))
    return found

def scan_interfaces(p):
    b=os.path.basename(p); found=[]
    lines=read_lines(p)
    for i,line in enumerate(lines,1):
        kind=None
        if JS_EXPORT_RE.match(line): kind='js/ts'
        elif RUST_PUB_RE.match(line): kind='rust'
        elif JAVA_IFACE_RE.match(line): kind='java'
        elif PY_EXPORT_RE.match(line): kind='python'
        elif PY_DECORATOR_RE.match(line) and i<len(lines) and re.match(r'^\s*(def|class)\b',lines[i]): kind='python'
        if kind:
            window=lines[max(0,i-6):i]
            tier=bool(any(TIER_TAGS.search(w) for w in window))
            found.append((i,kind,line.strip()[:60],tier))
    return found

def checklist(manifests,hooks,ifaces,root):
    items=[]
    # 1 MANIFEST
    valid=[m for m in manifests if m['name_ok'] and m['version_ok']]
    items.append(('MANIFEST','plugin manifest present with name and version',
                  bool(valid), f'{len(valid)}/{len(manifests)} manifests valid'))
    # 2 VERSION_CONTRACT
    covered=0
    for m in manifests:
        if m['version_keys']: covered+=1
    contract_files=[p for p in iter_files(root) if 'version-contract' in os.path.basename(p).lower() or 'compat' in os.path.basename(p).lower()]
    for p in contract_files:
        if os.path.basename(p).endswith('.json'):
            try: data=json.loads(open(p,encoding='utf-8').read())
            except (OSError,ValueError): data={}
            keys=[k for k in VERSION_KEYS if data.get(k)]
            if any(k in ('min_core_version','core_versions','requires_core','api_version') for k in keys): covered+=1
    ok=bool(manifests) and covered==len(manifests)
    items.append(('VERSION_CONTRACT','every manifest or contract file declares a core version range',
                  ok, f'{covered}/{len(manifests)} manifests covered'))
    # 3 HOOK_CONTRACT
    regs=[h for h in hooks if h[2]]
    items.append(('HOOK_CONTRACT','every hook registration declares hook name and argument schema',
                  bool(regs) and len(regs)==len(hooks), f'{len(regs)}/{len(hooks)} registrations with schema'))
    # 4 INTERFACE_TIER
    tiered=[i for i in ifaces if i[3]]
    items.append(('INTERFACE_TIER','every exported interface carries a stability tier annotation',
                  bool(ifaces) and len(tiered)==len(ifaces), f'{len(tiered)}/{len(ifaces)} interfaces tiered'))
    # 5 BREAKING_POLICY
    found=None
    for p in iter_files(root):
        b=os.path.basename(p).lower()
        if b in POLICY_FILES or (b.endswith('.md') and 'breaking' in b): found=p; break
    if not found:
        for p in iter_files(root):
            if any(POLICY_HINT_RE.search(l) for l in read_lines(p)): found=p; break
    items.append(('BREAKING_POLICY','tree documents a breaking-change policy (policy file, compatibility doc, or changelog)',
                  bool(found), found or 'no policy signal'))
    # 6 PACKAGING
    packaged=[m for m in manifests if m['name_ok'] and m['version_ok'] and m['capabilities']>=0]
    has_desc=0
    for p in [p for p in iter_files(root) if is_manifest(p)]:
        b=os.path.basename(p)
        if b.endswith('.json'):
            try: data=json.loads(open(p,encoding='utf-8').read())
            except (OSError,ValueError): data={}
            if data.get('description') and (data.get('author') or data.get('publisher')): has_desc+=1
    items.append(('PACKAGING','manifest carries publish metadata (name, version, description, author/publisher)',
                  bool(packaged) and has_desc==len(packaged), f'{has_desc}/{len(packaged)} manifests packaged'))
    return items

def main():
    ap=argparse.ArgumentParser(description='Inventory extension surface signals vs the stability-guarantee checklist')
    ap.add_argument('tree',nargs='?',default='.',help='root directory to scan (default: .)')
    ap.add_argument('--json',action='store_true',help='emit machine-readable summary')
    a=ap.parse_args()
    if not os.path.isdir(a.tree): raise SystemExit(f'ERROR: not a directory: {a.tree}')
    root=a.tree
    manifests=[]; hooks=[]; ifaces=[]
    for p in iter_files(root):
        if is_manifest(p): manifests.append((p,scan_manifest(p)))
        h=scan_hooks(p)
        if h: hooks.append((p,h))
        i=scan_interfaces(p)
        if i: ifaces.append((p,i))
    print(f'Extension surface inventory: {root}')
    print('='*60)
    print('MANIFESTS')
    for p,m in manifests:
        print(f'  {os.path.relpath(p,root):42} name={m["name_ok"]} version={m["version_ok"]} versions={m["version_keys"] or "MISSING"} hooks={m["hooks"] or "-"} caps={m["capabilities"]}')
    if not manifests: print('  (none)')
    print('HOOK REGISTRATIONS')
    for p,rows in hooks:
        for ln,text,schema in rows:
            print(f'  {os.path.relpath(p,root)}:{ln}  {"schema" if schema else "NO-SCHEMA":10} {text}')
    if not hooks: print('  (none)')
    print('EXPORTED INTERFACES')
    for p,rows in ifaces:
        for ln,kind,text,tier in rows:
            print(f'  {os.path.relpath(p,root)}:{ln}  {kind:8} {"tiered" if tier else "NO-TIER":8} {text}')
    if not ifaces: print('  (none)')
    print()
    print('Stability-guarantee checklist')
    print('='*60)
    items=checklist([m for _p,m in manifests],[h for _p,h in hooks for h in h], [i for _p,i in ifaces for i in i], root)
    passes=0
    for code,desc,ok,detail in items:
        print(f'  [{"PASS" if ok else "GAP "}] {code:16} {desc}')
        print(f'        {detail}')
        passes+=int(ok)
    print()
    print(f'SUMMARY: {len(manifests)} manifests, {sum(len(h) for _p,h in hooks)} hook registrations, {sum(len(i) for _p,i in ifaces)} exported interfaces; {passes}/{len(items)} checklist items pass')
    print('Inventory complete. Informational only — gaps require semantic confirmation; exit 0.')
    if a.json:
        print(json.dumps({'manifests':len(manifests),'hooks':sum(len(h) for _p,h in hooks),
                          'interfaces':sum(len(i) for _p,i in ifaces),'checks':[{'id':c,'ok':o} for c,_d,o,_x in items]}))
    raise SystemExit(0)
if __name__=='__main__': main()
