#!/usr/bin/env python3
"""Check a JSON surface manifest for quota visibility and cost estimation gaps. Stdlib only.

Reads a manifest whose "surfaces" array lists endpoints/commands (and
optionally meters and billing events) with fields: usage_visible,
limit_visible, reset_visible, cost_estimation. Flags every surface missing
quota visibility or cost estimation and exits 1 when findings exist.
"""
import argparse, json
from pathlib import Path

QUOTA_FIELDS = ('usage_visible', 'limit_visible', 'reset_visible')


def load(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError) as e:
        raise SystemExit(f'cannot read manifest {path}: {e}')


def surface_findings(surface):
    name = surface.get('name') or '<unnamed surface>'
    missing = [f for f in QUOTA_FIELDS if surface.get(f) is not True]
    findings = []
    if missing:
        findings.append(f'{name}: missing quota visibility ({", ".join(missing)})')
    if surface.get('cost_estimation') is not True:
        findings.append(f'{name}: missing cost estimation')
    return findings


def main():
    ap = argparse.ArgumentParser(
        description='Flag surfaces missing quota visibility or cost estimation.')
    ap.add_argument('manifest', help='path to JSON surface manifest')
    a = ap.parse_args()

    manifest = load(a.manifest)
    surfaces = manifest.get('surfaces') if isinstance(manifest, dict) else None
    if not isinstance(surfaces, list):
        raise SystemExit('manifest must be a JSON object with a "surfaces" array')

    findings = []
    for surface in surfaces:
        if not isinstance(surface, dict):
            findings.append('<non-object entry>: invalid manifest entry')
            continue
        findings.extend(surface_findings(surface))

    for f in findings:
        print(f'FINDING: {f}')
    print(f'{len(findings)} finding(s) in {len(surfaces)} surface(s)')
    raise SystemExit(1 if findings else 0)


if __name__ == '__main__':
    main()
