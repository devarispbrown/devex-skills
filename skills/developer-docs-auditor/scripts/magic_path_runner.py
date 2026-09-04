#!/usr/bin/env python3
"""Run and time a project-defined magic path manifest. JSON + stdlib only.

Commands are executed directly, never through a shell. Prefer sandbox/local/test environments.
If shell syntax is unavoidable, opt in explicitly with a list step like
["bash", "-lc", "cmd1 && cmd2"].
"""
import argparse, json, subprocess, time, os, sys, shlex
from pathlib import Path


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

VALID_SEGMENTS={'orientation','install','account_auth','configure','execute','wait','verify','recovery'}

def argv(cmd):
    if isinstance(cmd, list): return cmd
    if isinstance(cmd, str): return shlex.split(cmd)
    raise SystemExit('command must be a string or a list of argv tokens')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('manifest'); ap.add_argument('--cwd', default='.')
    ap.add_argument('--execute', action='store_true', help='actually execute manifest commands')
    a=ap.parse_args(); m=_read_json(a.manifest, 'a magic-path manifest'); budget=m.get('budget_seconds',900)
    if not a.execute:
        print(json.dumps(m,indent=2)); print('\nDry run only. Pass --execute to run commands.'); return
    total_start=time.monotonic(); rows=[]; failed=False
    for step in m.get('steps',[]):
        name=step['name']; seg=step.get('segment','execute')
        if seg not in VALID_SEGMENTS: raise SystemExit(f'Invalid segment {seg!r}')
        cmd=argv(step['command']); timeout=step.get('timeout_seconds',300)
        env=os.environ.copy(); env.update(step.get('env',{}))
        start=time.monotonic()
        try:
            cp=subprocess.run(cmd, cwd=a.cwd, text=True, capture_output=True, timeout=timeout, env=env)
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
