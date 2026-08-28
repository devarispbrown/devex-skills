#!/usr/bin/env python3
"""Run and time a project-defined magic path manifest. JSON + stdlib only.

Only runs commands explicitly supplied by the repository/user. Prefer sandbox/local/test environments.
"""
import argparse, json, subprocess, time, os, sys
from pathlib import Path

VALID_SEGMENTS={'orientation','install','account_auth','configure','execute','wait','verify','recovery'}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('manifest'); ap.add_argument('--cwd', default='.')
    ap.add_argument('--execute', action='store_true', help='actually execute manifest commands')
    a=ap.parse_args(); m=json.loads(Path(a.manifest).read_text()); budget=m.get('budget_seconds',900)
    if not a.execute:
        print(json.dumps(m,indent=2)); print('\nDry run only. Pass --execute to run commands.'); return
    total_start=time.monotonic(); rows=[]; failed=False
    for step in m.get('steps',[]):
        name=step['name']; seg=step.get('segment','execute')
        if seg not in VALID_SEGMENTS: raise SystemExit(f'Invalid segment {seg!r}')
        cmd=step['command']; timeout=step.get('timeout_seconds',300)
        env=os.environ.copy(); env.update(step.get('env',{}))
        start=time.monotonic()
        try:
            cp=subprocess.run(cmd, cwd=a.cwd, shell=True, text=True, capture_output=True, timeout=timeout, env=env)
            elapsed=time.monotonic()-start
            ok=cp.returncode==step.get('expected_exit_code',0)
            needle=step.get('stdout_contains')
            if needle is not None: ok = ok and needle in cp.stdout
            rows.append((name,seg,elapsed,ok,cp.returncode))
            if not ok:
                failed=True; print(cp.stdout); print(cp.stderr,file=sys.stderr); break
        except subprocess.TimeoutExpired:
            elapsed=time.monotonic()-start; rows.append((name,seg,elapsed,False,'timeout')); failed=True; break
    total=time.monotonic()-total_start
    print('\nMagic path timing')
    for name,seg,elapsed,ok,code in rows:
        print(f'{name:24} {seg:14} {elapsed:8.2f}s  {"PASS" if ok else "FAIL"} ({code})')
    print(f'TOTAL: {total:.2f}s / budget {budget}s')
    print('RESULT:', 'FAIL' if failed or total>budget else 'PASS')
    raise SystemExit(1 if failed or total>budget else 0)
if __name__=='__main__': main()
