#!/usr/bin/env python3
"""Validate an experiment manifest JSON for the experimentation-engineer skill.

Checks the required fields (name, hypothesis, variants, metrics, guardrails,
flag), exactly one control variant, metric definitions, guardrail thresholds,
and flag config. Exits 1 when the manifest is invalid. Stdlib only."""
import argparse, json, sys
from pathlib import Path

def check(m):
    bad = []
    if not isinstance(m, dict):
        return ['manifest must be a JSON object']
    for key in ('name', 'hypothesis'):
        if not isinstance(m.get(key), str) or not m[key].strip():
            bad.append(f'required string field {key!r} is missing or empty')
    variants = m.get('variants')
    if not isinstance(variants, list) or not variants:
        bad.append('variants must be a non-empty list')
    else:
        controls = []
        for i, v in enumerate(variants):
            if not isinstance(v, dict) or not isinstance(v.get('id'), str) or not v['id'].strip():
                bad.append(f'variant {i}: id is missing or empty')
            if isinstance(v, dict) and (v.get('control') is True or v.get('id') == 'control'):
                controls.append(i)
        if not controls:
            bad.append('no control variant: mark one variant with "control": true or id "control"')
        elif len(controls) > 1:
            bad.append('more than one control variant')
    metrics = m.get('metrics')
    if not isinstance(metrics, list) or not metrics:
        bad.append('metrics must be a non-empty list')
    else:
        for i, mt in enumerate(metrics):
            if not isinstance(mt, dict) or not isinstance(mt.get('name'), str) or not mt['name'].strip():
                bad.append(f'metric {i}: name is missing or empty')
            if not isinstance(mt, dict) or not isinstance(mt.get('definition'), str) or not mt['definition'].strip():
                bad.append(f'metric {i}: definition is missing or empty')
    guardrails = m.get('guardrails')
    if not isinstance(guardrails, list) or not guardrails:
        bad.append('guardrails must be a non-empty list')
    else:
        for i, g in enumerate(guardrails):
            if not isinstance(g, dict) or not isinstance(g.get('metric'), str) or not g['metric'].strip():
                bad.append(f'guardrail {i}: metric is missing or empty')
            t = g.get('threshold') if isinstance(g, dict) else None
            if not isinstance(t, (int, float)) or isinstance(t, bool):
                bad.append(f'guardrail {i}: threshold is missing or not a number')
    flag = m.get('flag')
    if not isinstance(flag, dict):
        bad.append('flag must be an object')
    elif not isinstance(flag.get('key'), str) or not flag['key'].strip():
        bad.append('flag.key is missing or empty')
    return bad

def main():
    ap = argparse.ArgumentParser(description='Validate an experiment manifest JSON')
    ap.add_argument('manifest', help='path to the experiment manifest JSON')
    a = ap.parse_args()
    try:
        m = json.loads(Path(a.manifest).read_text())
    except Exception as e:
        print(f'{a.manifest}: invalid JSON: {e}', file=sys.stderr)
        raise SystemExit(1)
    bad = check(m)
    for msg in bad:
        print(f'{a.manifest}: {msg}', file=sys.stderr)
    if bad:
        raise SystemExit(1)
    controls = sum(1 for v in m['variants'] if v.get('control') is True or v.get('id') == 'control')
    print(f'OK: {a.manifest} — {len(m["variants"])} variants ({controls} control), '
          f'{len(m["metrics"])} metrics, {len(m["guardrails"])} guardrails, flag key {m["flag"]["key"]!r}')
    raise SystemExit(0)

if __name__ == '__main__':
    main()
