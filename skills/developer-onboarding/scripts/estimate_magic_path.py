#!/usr/bin/env python3
"""Estimate a design-phase magic path plan from JSON without executing anything. Stdlib only."""

import argparse
import json
import sys
from pathlib import Path

# Canonical thresholds mirror dx-standards/metrics.md; values live in the generated standards.
MAGIC_PATH_MAX_MIN = 15
BUDGET_SECONDS = MAGIC_PATH_MAX_MIN * 60
MAGIC_PATH_MAX_COMMANDS = 8
MAGIC_PATH_MAX_CREDENTIALS = 2
MAGIC_PATH_MAX_CONTEXT_SWITCHES = 4

VALID_SEGMENTS = {"orientation", "install", "account_auth", "configure", "execute", "wait", "verify", "recovery"}

# Per-segment guidance budgets in seconds (guidance, not gates); buffer is spare time at the end.
SEGMENT_GUIDANCE_SECONDS = {
    "orientation": 60, "install": 120, "account_auth": 180, "configure": 180,
    "execute": 180, "wait": 180, "verify": 60, "recovery": 0,
}
BUFFER_GUIDANCE_SECONDS = 120


def band(total_seconds: int) -> str:
    minutes = total_seconds / 60.0
    if minutes <= 5:
        return "exceptional (<=5 min)"
    if minutes <= 10:
        return "strong (>5 to <=10 min)"
    if minutes <= MAGIC_PATH_MAX_MIN:
        return "pass (>10 to <=15 min)"
    return "FAIL (>15 min)"


def main() -> int:
    ap = argparse.ArgumentParser(description="Estimate a magic path plan; never executes anything.")
    ap.add_argument("plan", help="path to the plan JSON (see assets/magic-path-plan.example.json)")
    a = ap.parse_args()

    try:
        plan = json.loads(Path(a.plan).read_text())
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"cannot read plan {a.plan!r}: {e}")

    steps = plan.get("steps", [])
    if not steps:
        raise SystemExit(f"plan {a.plan!r} has no steps")

    rows = []
    for i, s in enumerate(steps):
        name = s.get("name", f"step {i + 1}")
        seg = s.get("segment", "execute")
        if seg not in VALID_SEGMENTS:
            raise SystemExit(f"step {name!r}: invalid segment {seg!r}")
        rows.append({
            "name": name,
            "segment": seg,
            "seconds": int(s.get("estimated_seconds", 0)),
            "commands": int(s.get("commands", 0)),
            "credentials": int(s.get("credentials", 0)),
            "context_switches": int(s.get("context_switches", 0)),
        })

    total = sum(r["seconds"] for r in rows)
    commands = sum(r["commands"] for r in rows)
    credentials = sum(r["credentials"] for r in rows)
    switches = sum(r["context_switches"] for r in rows)
    buffer = BUDGET_SECONDS - total
    over_budget = total > BUDGET_SECONDS

    print(f"Plan: {plan.get('name', '<unnamed>')}  (evidence label: Estimated)")
    print(f"{'Step':30} {'Segment':14} {'Est s':>6} {'Cmd':>4} {'Cred':>5} {'Ctx':>4}")
    for r in rows:
        print(f"{r['name'][:30]:30} {r['segment']:14} {r['seconds']:6} {r['commands']:4} {r['credentials']:5} {r['context_switches']:4}")

    print(f"\nEstimated total: {total}s ({total / 60:.1f} min) vs budget {BUDGET_SECONDS}s ({MAGIC_PATH_MAX_MIN} min) -> {band(total)}")
    print(f"Spare buffer: {buffer}s (guidance wants >= {BUFFER_GUIDANCE_SECONDS}s)")

    print("\nPer-segment totals vs guidance:")
    for seg in VALID_SEGMENTS:
        secs = sum(r["seconds"] for r in rows if r["segment"] == seg)
        if secs == 0:
            continue
        guidance = SEGMENT_GUIDANCE_SECONDS[seg]
        if guidance and secs > guidance:
            flag = "OVER GUIDANCE"
        elif seg == "recovery" and buffer < BUFFER_GUIDANCE_SECONDS:
            flag = "LOW BUFFER"
        else:
            flag = "ok"
        print(f"  {seg:14} {secs:5}s / {guidance or '-':>4}s  {flag}")

    print("\nCounts vs targets:")
    flags = 0
    for label, value, target in (
        ("interactive commands", commands, MAGIC_PATH_MAX_COMMANDS),
        ("credentials", credentials, MAGIC_PATH_MAX_CREDENTIALS),
        ("context switches", switches, MAGIC_PATH_MAX_CONTEXT_SWITCHES),
    ):
        if value > target:
            print(f"  {label:20} {value:3} / {target:3}  OVER TARGET (P2)")
            flags += 1
        else:
            print(f"  {label:20} {value:3} / {target:3}  ok")

    if buffer < 0 and over_budget:
        print(f"\nRESULT: FAIL - estimated total exceeds {MAGIC_PATH_MAX_MIN}-minute budget (BROKEN_QUICKSTART risk)")
        print("Cut steps or file product changes; an estimate cannot prove the gate passes.")
        raise SystemExit(1)
    print(f"\nRESULT: PASS (estimated) - within budget, {flags} count target(s) over")
    print("Estimated timing cannot prove the gate. Have developer-docs-auditor time the path if available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
