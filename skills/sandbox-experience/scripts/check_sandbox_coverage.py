#!/usr/bin/env python3
"""Check sandbox manifest coverage for risky learning tasks. Stdlib only."""
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Gate: every risky task must have a sandbox route.')
    ap.add_argument('manifest', help='sandbox manifest JSON (see assets/sandbox-manifest.example.json)')
    a=ap.parse_args()
    path=Path(a.manifest)
    if path.is_dir():
        raise SystemExit(f'{a.manifest} is a directory, but a sandbox manifest file is expected.')
    try:
        m=json.loads(path.read_text(encoding='utf-8', errors='replace'))
    except FileNotFoundError:
        raise SystemExit(f'No such file: {a.manifest}')
    except json.JSONDecodeError as e:
        raise SystemExit(f'{a.manifest} is not valid JSON: {e}')
    except OSError as e:
        raise SystemExit(f'Cannot read {a.manifest}: {e}')
    if not isinstance(m, dict):
        raise SystemExit(f'{a.manifest}: expected a JSON object with a "tasks" list.')
    # A missing or misspelled tasks key previously reported 0/0 covered, 100%, PASS. A
    # gate that passes because it found nothing to check is the worst failure available
    # to it: it is indistinguishable from a real pass.
    if not isinstance(m.get('tasks'), list):
        raise SystemExit(f'{a.manifest}: no "tasks" list. A manifest with no tasks cannot '
                         'be scored, and reporting full coverage for it would be false.')
    risky=[t for t in m.get('tasks',[]) if isinstance(t, dict) and t.get('risky')]
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
