#!/usr/bin/env python3
"""Estimate architecture comprehension time from a request trace or import graph.

Input is user-supplied JSON on disk, or '-' for stdin.

  Trace form (preferred):
    {"type": "trace", "hops": [{"layer": "service", "name": "checkout"}, ...]}
  A bare JSON array of layer names, or of objects with a 'layer' key, also works.

  Import graph form:
    {"type": "imports",
     "edges": [{"from": "orders", "to": "payments", "layer": "integration"}, ...]}

Each hop or edge contributes a comprehension cost in minutes from the embedded
per-hop cost table, keyed by layer name. Unknown layers use the default cost.

The output is always an estimate: it is labeled Estimated and never presented
as proof. This script informs; it never gates. It exits 0 on any successful
estimate, including OVER BUDGET results. Malformed input raises SystemExit.

Stdlib only.
"""
import argparse
import json
import sys
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

# Per-hop cost table, keyed by layer name. Values are comprehension minutes
# per hop for an engineer building a mental model, not execution time.
LAYER_COST_MIN = {
    "client": 1.5,
    "frontend": 2.0,
    "web": 2.0,
    "gateway": 2.0,
    "api": 2.0,
    "bff": 3.0,
    "auth": 3.0,
    "middleware": 2.5,
    "service": 4.0,
    "domain": 5.0,
    "core": 5.0,
    "model": 4.0,
    "repository": 3.5,
    "data": 3.0,
    "database": 3.5,
    "db": 3.5,
    "cache": 3.0,
    "queue": 3.0,
    "worker": 4.0,
    "event": 3.5,
    "integration": 4.5,
    "external": 4.0,
    "third_party": 4.0,
}
DEFAULT_HOP_COST_MIN = 3.0

# Fixed overhead to read the request, orient, and verify the terminal effect.
OVERHEAD_MIN = 2.0

# Comprehension budgets by constant name. Only this table hardcodes budget
# values; the max is never hardcoded elsewhere in this script.
MAX_MIN_BY_CONSTANT = {
    "ARCHITECTURE_COMPREHENSION_MAX_MIN": 30,
    "MAGIC_PATH_MAX_MIN": 15,
    "LOCAL_DEV_MAX_MIN": 10,
}
DEFAULT_MAX_CONSTANT = "ARCHITECTURE_COMPREHENSION_MAX_MIN"


def hop_cost(layer):
    return LAYER_COST_MIN.get(layer, DEFAULT_HOP_COST_MIN)


def load_hops(raw):
    """Return (hops, kind) where hops is a list of layer names."""
    if isinstance(raw, list):
        hops = []
        for item in raw:
            if isinstance(item, str):
                hops.append(item)
            elif isinstance(item, dict) and "layer" in item:
                hops.append(str(item["layer"]))
            else:
                raise SystemExit(
                    "trace hops must be layer names or objects with a 'layer' key")
        return hops, "trace"
    if not isinstance(raw, dict):
        raise SystemExit("input JSON must be an object or a list of hops")
    kind = raw.get("type", "trace")
    if kind == "trace":
        hops_raw = raw.get("hops") or raw.get("trace")
        if hops_raw is None:
            raise SystemExit("trace input requires a 'hops' list")
        hops = []
        for item in hops_raw:
            if isinstance(item, dict):
                if "layer" not in item:
                    raise SystemExit("each hop object requires a 'layer' key")
                hops.append(str(item["layer"]))
            else:
                hops.append(str(item))
        return hops, "trace"
    if kind == "imports":
        edges = raw.get("edges") or raw.get("graph")
        if edges is None:
            raise SystemExit("imports input requires an 'edges' list")
        hops = []
        for edge in edges:
            if isinstance(edge, dict):
                hops.append(str(edge.get("layer") or edge.get("to", "unknown")))
            else:
                hops.append(str(edge))
        return hops, "imports"
    raise SystemExit(f"unknown input type {kind!r}; expected 'trace' or 'imports'")


def main():
    ap = argparse.ArgumentParser(
        description="Estimate architecture comprehension time from a request "
                    "trace or import graph.")
    ap.add_argument("input",
                    help="path to JSON input, or '-' for stdin")
    ap.add_argument("--max-const", default=DEFAULT_MAX_CONSTANT,
                    help="constant name for the budget lookup (default "
                         "%(default)s)")
    ap.add_argument("--max-min", type=float, default=None,
                    help="override the budget in minutes (default: from the "
                         "constant table)")
    a = ap.parse_args()

    if a.max_const not in MAX_MIN_BY_CONSTANT:
        raise SystemExit(
            f"unknown constant {a.max_const!r}; known: "
            f"{', '.join(sorted(MAX_MIN_BY_CONSTANT))}")
    max_min = a.max_min if a.max_min is not None else MAX_MIN_BY_CONSTANT[a.max_const]
    if max_min <= 0:
        raise SystemExit("--max-min must be positive")

    text = sys.stdin.read() if a.input == "-" else _read_input(a.input, "an architecture manifest")
    try:
        raw = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {a.input}: {exc}")

    hops, kind = load_hops(raw)
    if not hops:
        raise SystemExit("input contains no hops or edges")

    costs = [hop_cost(h) for h in hops]
    estimate = OVERHEAD_MIN + sum(costs)
    verdict = "OVER BUDGET" if estimate > max_min else "UNDER BUDGET"

    print(f"Input: {kind} ({len(hops)} hops)")
    for i, (h, c) in enumerate(zip(hops, costs), 1):
        print(f"  {i:>3}. {h:14} Estimated {c:.1f} min")
    print(f"Estimated comprehension time: {estimate:.1f} min  (label: Estimated)")
    print(f"Budget: {a.max_const} = {max_min} min")
    print(f"RESULT: {verdict} (Estimated)")
    print("Note: an Estimated time cannot prove a pass; it only indicates "
          "likely risk or feasibility.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
