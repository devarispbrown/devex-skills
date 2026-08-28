#!/usr/bin/env python3
"""Check measured performance values against a JSON budget file; exit 1 on any breach or unverified budget. Stdlib only."""
import argparse, json
from pathlib import Path

NEAR_MISS_RATIO=0.9  # measured/budget above this (for '<=') or below the inverse (for '>=') is a near miss
OPS={'<=': lambda v,b: v<=b, '>=': lambda v,b: v>=b}

def load(path, key):
    try: rows=json.loads(Path(path).read_text())[key]
    except KeyError: raise SystemExit(f'{path}: missing "{key}" list')
    except Exception as e: raise SystemExit(f'{path}: invalid JSON: {e}')
    if not isinstance(rows, list): raise SystemExit(f'{path}: "{key}" must be a list')
    return rows

def main():
    ap=argparse.ArgumentParser(description='Compare measurements against performance budgets. '
        'Read-only; prints one status line per budget (PASS/NEAR MISS/BREACH/UNVERIFIED) and exits 1 on any breach or unverified budget.')
    ap.add_argument('budgets', help='JSON budget file, schema of assets/perf-budgets.example.json')
    ap.add_argument('measurements', help='JSON measurements file, schema of assets/perf-measurements.example.json')
    a=ap.parse_args()
    budgets=load(a.budgets, 'budgets'); measured=load(a.measurements, 'measured')
    by_key={(m.get('surface'), m.get('metric')): m for m in measured}
    lines=[]; breaches=[]; unverified=[]; near=[]
    for b in budgets:
        key=(b.get('surface'), b.get('metric')); budget=b.get('budget')
        if not isinstance(budget, (int, float)) or budget<=0:
            raise SystemExit(f'{key[0]}:{key[1]}: budget must be a positive number')
        m=by_key.get(key)
        if m is None:
            unverified.append((key, 'no measurement')); lines.append(f'{key[0]}:{key[1]}  no measurement  UNVERIFIED'); continue
        if m.get('unit')!=b.get('unit'):
            unverified.append((key, f'unit mismatch ({m.get("unit")} != {b.get("unit")})'))
            lines.append(f'{key[0]}:{key[1]}  unit mismatch  UNVERIFIED'); continue
        value=m.get('value')
        if not isinstance(value, (int, float)):
            unverified.append((key, 'non-numeric value')); lines.append(f'{key[0]}:{key[1]}  non-numeric value  UNVERIFIED'); continue
        op=b.get('operator', '<='); ok=OPS.get(op, OPS['<='])(value, budget)
        is_near=(value>budget*NEAR_MISS_RATIO) if op=='<=' else (value<budget/NEAR_MISS_RATIO)
        label='BREACH' if not ok else 'NEAR MISS' if is_near else 'PASS'
        lines.append(f'{key[0]}:{key[1]}  {value}{m.get("unit")} vs {budget}{b.get("unit")} budget  {label}')
        if label=='BREACH': breaches.append((key, m, b))
        if label=='NEAR MISS': near.append((key, m, b))
    for (surface, metric), m in by_key.items():
        if not any(b.get('surface')==surface and b.get('metric')==metric for b in budgets):
            lines.append(f'{surface}:{metric}  {m.get("value")}{m.get("unit")} measured, no budget  UNMETERED')
    print('\n'.join(lines))
    for (s, mt), m, b in breaches:
        print(f'BREACH {s}:{mt} measured {m.get("value")}{m.get("unit")} over budget {b.get("budget")}{b.get("unit")}')
    for (s, mt), reason in unverified:
        print(f'UNVERIFIED {s}:{mt} — {reason}; cannot prove PASS')
    print(f'RESULT: {len(breaches)} breach(es), {len(unverified)} unverified, {len(near)} near miss(es)')
    raise SystemExit(1 if breaches or unverified else 0)
if __name__=='__main__': main()
