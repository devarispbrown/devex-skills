#!/usr/bin/env python3
"""Check sandbox manifest coverage for risky learning tasks. Stdlib only."""
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Gate: every risky task must have a sandbox route.')
    ap.add_argument('manifest', help='sandbox manifest JSON (see assets/sandbox-manifest.example.json)')
    a=ap.parse_args(); m=json.loads(Path(a.manifest).read_text())
    risky=[t for t in m.get('tasks',[]) if t.get('risky')]
    uncovered=[t for t in risky if not t.get('sandbox_route')]
    for t in uncovered:
        print(f"{t.get('id',t.get('task','?'))}: NO_SANDBOX_FOR_RISKY_PATH - {t.get('task','risky task')} ({t.get('risk_type','unclassified')}) has no sandbox route")
    total=len(risky); covered=total-len(uncovered)
    pct=100.0*covered/total if total else 100.0
    print(f'Manifest: {m.get("name","?")}')
    print(f'Sandbox coverage: {covered}/{total} risky tasks covered ({pct:.0f}%)')
    print('RESULT:', 'FAIL' if uncovered else 'PASS')
    raise SystemExit(1 if uncovered else 0)
if __name__=='__main__': main()
