#!/usr/bin/env python3
"""Static inventory of repository security posture. Stdlib only."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
USES_RE = re.compile(r"^uses:\s*(\S+)")
SECRET_RE = re.compile(r"\$\{\{\s*secrets\.([A-Z0-9_]+)")
COMMENT_RE = re.compile(r"\s+#.*$")
REPORT_HINTS = ("report", "contact", "email", "advisory", "vulnerab")


def analyze_workflow(path: Path) -> list[tuple[str, str]]:
    """Return (kind, message) findings for one workflow file. Heuristic; never fails."""
    findings: list[tuple[str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        findings.append(("risky", f"unreadable: {exc}"))
        return findings
    in_run_block = False  # inside a `run: |` multiline block
    in_env_map = False    # inside a step `env:` mapping
    run_indent = -1
    env_indent = -1
    for lineno, raw in enumerate(lines, 1):
        line = COMMENT_RE.sub("", raw)
        stripped = line.strip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip())
        # Strip a YAML list marker so `- uses:` and `uses:` parse alike.
        body = stripped[2:].lstrip() if stripped.startswith("- ") else stripped
        # Indentation transitions close open blocks.
        if in_run_block and indent <= run_indent:
            in_run_block = False
        if in_env_map and indent <= env_indent:
            in_env_map = False
        if body.startswith("pull_request_target"):
            findings.append((
                "risky",
                f"line {lineno}: pull_request_target trigger; untrusted PR code runs "
                "in the base-branch workflow scope",
            ))
        uses = USES_RE.match(body)
        if uses:
            ref = uses.group(1)
            if ref.startswith("./"):
                continue  # local action, not pin-able
            if ref.startswith("docker://"):
                findings.append((
                    "note",
                    f"line {lineno}: docker container action {ref!r} cannot be SHA-pinned; "
                    "pin the image digest instead",
                ))
                continue
            name, _, rev = ref.partition("@")
            if not rev:
                findings.append((
                    "risky",
                    f"line {lineno}: uses {name!r} without any ref; pin to a full commit SHA",
                ))
            elif not FULL_SHA.match(rev):
                findings.append((
                    "risky",
                    f"line {lineno}: unpinned action {ref!r}; use a full 40-char commit SHA",
                ))
            continue
        if body.startswith("run:"):
            in_run_block = body.endswith(("|", ">"))
            run_indent = indent
            if not in_run_block:
                for match in SECRET_RE.finditer(line):
                    findings.append((
                        "risky",
                        f"line {lineno}: secret {match.group(1)!r} referenced inline in a run "
                        "block; map it through env: instead",
                    ))
            continue
        if in_run_block:
            for match in SECRET_RE.finditer(line):
                findings.append((
                    "risky",
                    f"line {lineno}: secret {match.group(1)!r} referenced in a run block "
                    "without env indirection",
                ))
            continue
        if body.startswith("env:"):
            in_env_map = True
            env_indent = indent
            continue
        if in_env_map:
            for match in SECRET_RE.finditer(line):
                findings.append((
                    "note",
                    f"line {lineno}: secret {match.group(1)!r} mapped via env (safe indirection)",
                ))
            continue
        for match in SECRET_RE.finditer(line):
            findings.append((
                "note",
                f"line {lineno}: secret {match.group(1)!r} referenced outside a run block and "
                "outside env; verify placement",
            ))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Static security-posture inventory. Read-only; informs, never fails."
    )
    parser.add_argument(
        "path", nargs="?", default=".",
        help="repository root, or a single workflow file to scan",
    )
    args = parser.parse_args()
    target = Path(args.path)
    print(f"Target: {target}")

    if target.is_file():
        print("Single-file scan: repository-level checks skipped.\n")
        print("## Workflow findings\n")
        for kind, msg in analyze_workflow(target):
            label = "risky" if kind == "risky" else "note "
            print(f"[{label}] {target.name}: {msg}")
        print("\nInventory only: this script informs and never fails a repository. "
              "Verdicts belong to the audit in SKILL.md.")
        return 0

    root = target.resolve()
    security_md = root / "SECURITY.md"
    codeowners = root / "CODEOWNERS"
    if not codeowners.exists():
        codeowners = root / ".github" / "CODEOWNERS"
    workflows_dir = root / ".github" / "workflows"
    workflows = sorted(workflows_dir.glob("*.yml")) + sorted(workflows_dir.glob("*.yaml"))

    def rel(p: Path) -> str:
        try:
            return str(p.relative_to(root))
        except ValueError:
            return str(p)

    print("\n## Security posture checklist\n")
    if security_md.exists():
        print("[present] SECURITY.md")
        text = security_md.read_text(encoding="utf-8", errors="replace").lower()
        if not any(hint in text for hint in REPORT_HINTS):
            print("[note  ] SECURITY.md lacks a reporting keyword (report/contact/email/"
                  "advisory); add a reporting channel")
    else:
        print("[absent ] SECURITY.md (required by the SECURITY.md contract)")
    if codeowners.exists():
        print(f"[present] CODEOWNERS ({rel(codeowners)})")
    else:
        print("[absent ] CODEOWNERS (no owner map for required reviews)")
    if workflows:
        print(f"[present] workflow files ({len(workflows)})")
    elif workflows_dir.is_dir():
        print("[note  ] .github/workflows exists but contains no workflow files")
    else:
        print("[absent ] .github/workflows (no CI security surface committed)")
    print("[manual ] branch protection cannot be verified from the working tree; "
          "verify in hosting settings: require pull request reviews, require status checks, "
          "require signed commits, protect release tags")
    print("\n## Workflow findings\n")
    for wf in workflows:
        findings = analyze_workflow(wf)
        if not findings:
            print(f"[ok    ] {rel(wf)}: no risky patterns detected")
        for kind, msg in findings:
            label = "risky" if kind == "risky" else "note "
            print(f"[{label}] {rel(wf)}: {msg}")
    print("\nInventory only: this script informs and never fails a repository. It cannot see "
          "hosting settings. Severities and verdicts belong to the audit in SKILL.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
