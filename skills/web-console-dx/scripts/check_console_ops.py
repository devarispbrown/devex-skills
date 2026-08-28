#!/usr/bin/env python3
"""Automation-parity checklist for console operations from a JSON manifest. Stdlib only."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_manifest(path: Path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        raise SystemExit(f"cannot read manifest {path}: {e}")
    if isinstance(data, dict):
        ops = data.get("operations")
        if ops is None:
            raise SystemExit(f"manifest {path}: object missing 'operations' list")
    else:
        ops = data
    if not isinstance(ops, list):
        raise SystemExit(f"manifest {path}: expected a list of operations or an object with an 'operations' list")
    return ops


def parse_ops(ops: list) -> list[tuple[str, bool, bool, str]]:
    rows = []
    for i, op in enumerate(ops):
        if not isinstance(op, dict):
            raise SystemExit(f"manifest entry {i}: expected an object, got {type(op).__name__}")
        name = op.get("name")
        if not name:
            raise SystemExit(f"manifest entry {i}: missing 'name'")
        api = bool(op.get("has_api_equivalent"))
        cli = bool(op.get("has_cli_equivalent"))
        docs = op.get("docs_link") or ""
        rows.append((str(name), api, cli, str(docs)))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print an automation-parity checklist for console operations. Informs; never fails."
    )
    parser.add_argument("manifest", help="path to JSON manifest of console operations")
    parser.add_argument("--json", action="store_true", help="emit a machine-readable summary")
    args = parser.parse_args()

    path = Path(args.manifest)
    rows = parse_ops(load_manifest(path))
    gaps = [r for r in rows if not r[1] and not r[2]]
    partial = [r for r in rows if r[1] != r[2]]
    covered = [r for r in rows if r[1] and r[2]]

    print(f"Manifest: {path} ({len(rows)} operations)\n")
    print("## Automation-parity checklist\n")
    for name, api, cli, docs in rows:
        status = "covered" if api and cli else ("partial" if api or cli else "GAP")
        print(f"{name:32} api={str(api).lower():5} cli={str(cli).lower():5} {status}")
        if docs and (not api or not cli):
            print(f"{'':34} docs: {docs}")

    print("\n## Automation-parity gaps")
    if gaps:
        for name, *_ in gaps:
            print(f"- {name}: no API equivalent, no CLI equivalent; provide the automation surface or remove the UI operation")
    else:
        print("- none")

    print("\n## Partial parity")
    if partial:
        for name, api, cli, _ in partial:
            missing = "CLI" if api else "API"
            print(f"- {name}: missing {missing} equivalent")
    else:
        print("- none")

    print(
        f"\nSummary: {len(covered)} covered, {len(partial)} partial, {len(gaps)} gaps "
        f"({len(rows) - len(gaps) - len(partial)} fully automatable)"
    )
    print("Inventory only: this report informs the audit and never fails. See SKILL.md for the gate procedure.")
    if args.json:
        print(json.dumps({"operations": len(rows), "covered": len(covered), "partial": len(partial), "gaps": len(gaps)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
