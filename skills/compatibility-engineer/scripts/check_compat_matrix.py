#!/usr/bin/env python3
"""Verify each supported compatibility claim has CI or marker evidence. Stdlib only."""
import argparse
import json
from pathlib import Path

TIERS = {"supported", "best-effort", "deprecated"}
EVIDENCE_TYPES = {"ci", "marker", "link"}


def check_evidence(evidence, root):
    """Return (ok, detail) for one evidence block. Read-only; never mutates."""
    etype = evidence.get("type")
    if etype not in EVIDENCE_TYPES:
        return False, f"unknown evidence type {etype!r}"
    if etype == "link":
        url = evidence.get("url", "")
        if not (url.startswith("https://") or url.startswith("http://")):
            return False, f"invalid link url {url!r}"
        return True, url
    path = evidence.get("file", "")
    if not path:
        return False, "evidence file not specified"
    full = root / path
    if not full.is_file():
        return False, f"evidence file missing: {path}"
    if etype == "marker":
        return True, f"marker {path}"
    match = evidence.get("match", "")
    if not match:
        return False, f"ci evidence {path} has no match string"
    try:
        text = full.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return False, f"cannot read {path}: {exc}"
    if match not in text:
        return False, f"no match for {match!r} in {path}"
    return True, f"ci {path} (match {match!r})"


def main():
    ap = argparse.ArgumentParser(
        description="Check every supported compatibility claim has matching CI or evidence.")
    ap.add_argument("matrix", help="path to the compat matrix JSON")
    ap.add_argument("--root", default=".",
                    help="base directory for evidence paths (default: current directory)")
    args = ap.parse_args()

    matrix_path = Path(args.matrix)
    try:
        data = json.loads(matrix_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"cannot load matrix {matrix_path}: {exc}")

    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        raise SystemExit(f"{matrix_path}: matrix has no non-empty claims array")

    root = Path(args.root)
    print(f"Claim-vs-evidence matrix for {data.get('product', '?')} "
          f"(updated {data.get('updated', '?')})")
    print(f"{'surface':<14}{'version':<18}{'tier':<12}{'status':<12}evidence")
    print("-" * 80)

    findings = []
    for i, claim in enumerate(claims):
        surface = claim.get("surface", "?")
        version = claim.get("version", "?")
        tier = claim.get("tier", "supported")
        if tier not in TIERS:
            raise SystemExit(f"{matrix_path}: claim {i} has unknown tier {tier!r}")
        if tier != "supported":
            status, detail = "EXEMPT", "no evidence required for this tier"
        elif not claim.get("evidence"):
            status, detail = "UNTESTED", "no evidence recorded"
        else:
            ok, detail = check_evidence(claim["evidence"], root)
            status, detail = ("EVIDENCED", detail) if ok else ("MISSING", detail)
        if tier == "supported" and status != "EVIDENCED":
            findings.append((surface, version, tier, status, detail))
        print(f"{surface:<14}{version:<18}{tier:<12}{status:<12}{detail}")

    print()
    if findings:
        print("UNTESTED_SUPPORTED_VERSION findings:")
        for surface, version, tier, status, detail in findings:
            print(f"- {version} ({surface}, {tier}): {detail}")
        print(f"RESULT: {len(findings)} supported claim(s) lack evidence -> FAIL")
        raise SystemExit(1)
    print("RESULT: all supported claims carry evidence -> PASS")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
