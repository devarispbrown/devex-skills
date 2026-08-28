#!/usr/bin/env python3
"""Check a certification matrix for uncertified and stale cells. Stdlib only."""
import argparse, json
from datetime import date, datetime
from pathlib import Path

def parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(str(s), "%Y-%m-%d").date()
    except ValueError:
        return None

def truncate(s, n):
    return s if len(s) <= n else s[:n - 1] + "…"

def main():
    ap = argparse.ArgumentParser(description="Audit a certification matrix JSON for uncertified or stale cells.")
    ap.add_argument("matrix", help="path to the certification matrix JSON")
    ap.add_argument("--stale-after-days", type=int, default=None,
                    help="staleness threshold in days (default: 90 or the matrix's staleness_days)")
    ap.add_argument("--today", default=None, help="reference date YYYY-MM-DD (default: today)")
    a = ap.parse_args()

    try:
        m = json.loads(Path(a.matrix).read_text())
    except Exception as e:
        raise SystemExit(f"cannot read matrix {a.matrix}: {e}")

    today = parse_date(a.today) or date.today()
    threshold = a.stale_after_days if a.stale_after_days is not None else m.get("staleness_days", 90)

    rows = []
    for integration in m.get("integrations", []):
        name = integration.get("integration") or integration.get("name") or "?"
        for cell in integration.get("cells", []):
            version = cell.get("version") or "?"
            config = cell.get("configuration") or ""
            evidence = (cell.get("evidence_link") or "").strip()
            tested = parse_date(cell.get("last_tested"))
            status, note = "CERTIFIED", ""
            if not evidence:
                status, note = "UNCERTIFIED", "no evidence link"
            elif tested is None:
                status, note = "UNCERTIFIED", "missing or invalid last-tested date"
            elif not cell.get("certified", True):
                status, note = "UNCERTIFIED", "explicitly marked not certified"
            elif (today - tested).days > threshold:
                status, note = "STALE", f"last tested {cell['last_tested']}, older than {threshold} days"
            rows.append((name, version, config, cell.get("last_tested") or "-", evidence or "-", status, note))

    hdr = ("Integration", "Version", "Configuration", "Last tested", "Evidence", "Status")
    widths = (24, 16, 34, 12, 48, 11)
    fmt = "  ".join("{%d:<%d}" % (i, w) for i, w in enumerate(widths))
    print(fmt.format(*hdr))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print(fmt.format(truncate(r[0], widths[0]), truncate(r[1], widths[1]), truncate(r[2], widths[2]),
                         truncate(r[3], widths[3]), truncate(r[4], widths[4]), r[5]))

    total = len(rows)
    stale = sum(1 for r in rows if r[5] == "STALE")
    uncertified = sum(1 for r in rows if r[5] == "UNCERTIFIED")
    print(f"\n{total} cells: {total - stale - uncertified} certified, {stale} stale, {uncertified} uncertified")

    if stale or uncertified:
        print("FLAGGED CELLS:")
        for r in rows:
            if r[5] != "CERTIFIED":
                print(f"  [{r[5]}] {r[0]} {r[1]} — {r[6]}")
        raise SystemExit(1)
    print("RESULT: PASS")

if __name__ == "__main__":
    main()
