#!/usr/bin/env python3
"""Static inventory of a repo's first-contribution funnel: guidance files, templates, CI, local checks, parity. Stdlib only."""
import argparse
import json
import re
from pathlib import Path

GIFI_RE = re.compile(r"good[ -]first[ -]issue", re.IGNORECASE)
PR_RE = re.compile(r"\bpull request\b|\bPR\b", re.IGNORECASE)
TEST_RE = re.compile(r"\btest", re.IGNORECASE)
REPRO_RE = re.compile(r"\breproduc", re.IGNORECASE)
CI_CMD_RE = re.compile(
    r"\b(make|npm run|npm|yarn|pnpm|pytest|tox|go test|cargo test|mix test|mvn test|gradle test|bundle exec rspec|flutter test|dotnet test)\b[^\n]*?\btest\b",
    re.IGNORECASE,
)
OWNER_RE = re.compile(r"^\s*\S+\s+@\S+", re.MULTILINE)
MAKE_TARGET_RE = re.compile(r"^test\s*:", re.MULTILINE)

CONTRIBUTING_NAMES = ("CONTRIBUTING.md", "CONTRIBUTING.rst", "CONTRIBUTING.txt", "CONTRIBUTING")
CODEOWNERS_NAMES = ("CODEOWNERS",)
ISSUE_TEMPLATE_DIRS = (".github/ISSUE_TEMPLATE", ".gitlab/issue_templates", "docs/ISSUE_TEMPLATE")
ISSUE_TEMPLATE_FILES = ("ISSUE_TEMPLATE.md", ".github/ISSUE_TEMPLATE.md")
PR_TEMPLATE_FILES = (
    ".github/pull_request_template.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "pull_request_template.md",
    "PULL_REQUEST_TEMPLATE.md",
    "docs/pull_request_template.md",
)
CI_FILE_GLOBS = (
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
    ".gitlab-ci.yml",
    ".circleci/config.yml",
    "Jenkinsfile",
    "azure-pipelines.yml",
    ".travis.yml",
    "appveyor.yml",
)


def find_first(root, names):
    for name in names:
        p = root / name
        if p.is_file():
            return p
    return None


def text_has(path, regex):
    try:
        return bool(regex.search(path.read_text(encoding="utf-8", errors="replace")))
    except OSError:
        return False


def makefile_test_command(makefile):
    try:
        content = makefile.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = MAKE_TARGET_RE.search(content)
    if not m:
        return None
    return "make test"


def package_test_command(pkg):
    try:
        data = json.loads(pkg.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return None
    scripts = data.get("scripts") or {}
    return "npm test" if "test" in scripts else None


def ci_test_commands(ci_files):
    cmds = []
    for p in ci_files:
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        cmds.extend(m.group(0).strip().strip("'\"") for m in CI_CMD_RE.finditer(content))
    return sorted(set(cmds))


def main():
    ap = argparse.ArgumentParser(
        description="Inventory the first-contribution funnel of a repository. Read-only; exits 0."
    )
    ap.add_argument("path", nargs="?", default=".", help="repository root to scan (default: current directory)")
    a = ap.parse_args()
    root = Path(a.path).resolve()
    if not root.is_dir():
        raise SystemExit(f"error: not a directory: {root}")

    print(f"Contributor funnel inventory: {root}")
    print("-" * 60)
    gaps = []

    contributing = find_first(root, CONTRIBUTING_NAMES) or find_first(root / ".github", CONTRIBUTING_NAMES) or find_first(root / "docs", CONTRIBUTING_NAMES)
    if contributing:
        notes = []
        if text_has(contributing, PR_RE):
            notes.append("mentions pull request")
        if text_has(contributing, TEST_RE):
            notes.append("mentions test")
        print(f"[OK]   CONTRIBUTING.md: {contributing.relative_to(root)} ({'; '.join(notes) or 'no quality signals'})")
        if not notes:
            gaps.append("CONTRIBUTING.md exists but mentions neither pull requests nor tests")
    else:
        print("[GAP]  CONTRIBUTING.md: missing")
        gaps.append("CONTRIBUTING.md missing")

    codeowners = find_first(root, CODEOWNERS_NAMES) or find_first(root / ".github", CODEOWNERS_NAMES) or find_first(root / "docs", CODEOWNERS_NAMES)
    if codeowners and OWNER_RE.search(codeowners.read_text(encoding="utf-8", errors="replace")):
        print(f"[OK]   CODEOWNERS: {codeowners.relative_to(root)} (has owner lines)")
    elif codeowners:
        print(f"[GAP]  CODEOWNERS: {codeowners.relative_to(root)} exists but has no owner lines")
        gaps.append("CODEOWNERS has no owner lines")
    else:
        print("[GAP]  CODEOWNERS: missing")
        gaps.append("CODEOWNERS missing")

    issue_templates = []
    for d in ISSUE_TEMPLATE_DIRS:
        dp = root / d
        if dp.is_dir():
            issue_templates.extend(sorted(p for p in dp.iterdir() if p.is_file()))
    for f in ISSUE_TEMPLATE_FILES:
        p = root / f
        if p.is_file():
            issue_templates.append(p)
    if issue_templates:
        names = ", ".join(sorted(str(p.relative_to(root)) for p in issue_templates))
        has_repro = any(text_has(p, REPRO_RE) for p in issue_templates)
        print(f"[OK]   Issue templates: {names}" + (" (includes reproduction steps)" if has_repro else " (no reproduction-steps signal)"))
        if not has_repro:
            gaps.append("Issue templates lack a reproduction-steps signal")
    else:
        print("[GAP]  Issue templates: missing")
        gaps.append("Issue templates missing")

    pr_template = next((root / f for f in PR_TEMPLATE_FILES if (root / f).is_file()), None)
    if pr_template:
        notes = []
        if text_has(pr_template, TEST_RE):
            notes.append("asks for test evidence")
        if text_has(pr_template, r"\[[ xX]\]"):
            notes.append("has a checklist")
        print(f"[OK]   PR template: {pr_template.relative_to(root)} ({'; '.join(notes) or 'present'})")
    else:
        print("[GAP]  PR template: missing")
        gaps.append("PR template missing")

    gifi_sources = []
    if contributing:
        gifi_sources.append(contributing)
    for f in ("README.md", "README.rst", "README"):
        p = root / f
        if p.is_file():
            gifi_sources.append(p)
    gifi_sources.extend(issue_templates)
    ci_files = []
    for glob in CI_FILE_GLOBS:
        ci_files.extend(sorted(root.glob(glob)))
    gifi_sources.extend(ci_files)
    gifi_hits = [p for p in gifi_sources if text_has(p, GIFI_RE)]
    if gifi_hits:
        print(f"[OK]   Good-first-issue: mentioned in {', '.join(sorted(str(p.relative_to(root)) for p in gifi_hits[:3]))}")
    else:
        print("[GAP]  Good-first-issue: no label or labeling procedure mentioned anywhere")
        gaps.append("Good-first-issue labeling not documented")

    if ci_files:
        print(f"[OK]   CI workflow files: {', '.join(str(p.relative_to(root)) for p in ci_files)}")
    else:
        print("[GAP]  CI workflow files: none found")
        gaps.append("No CI workflow files found")

    makefile = root / "Makefile"
    if not makefile.is_file():
        makefile = root / "makefile"
    pkg = root / "package.json"
    local_cmd = None
    local_src = None
    if makefile.is_file() and makefile_test_command(makefile):
        local_cmd, local_src = "make test", "Makefile"
    elif pkg.is_file() and package_test_command(pkg):
        local_cmd, local_src = "npm test", "package.json"
    if local_cmd:
        print(f"[OK]   Local test target: {local_cmd} ({local_src})")
    else:
        print("[GAP]  Local test target: no Makefile test target and no package.json test script")
        gaps.append("No local test target (Makefile test target or package.json test script)")

    ci_cmds = ci_test_commands(ci_files)
    if local_cmd:
        ci_text = "\n".join(
            p.read_text(encoding="utf-8", errors="replace") for p in ci_files if p.is_file()
        )
        if not ci_files:
            print("[WARN] Check parity: no CI to compare against")
        elif local_cmd in ci_text:
            print(f"[OK]   Check parity: CI runs {local_cmd}")
        elif ci_cmds:
            print(f"[GAP]  Check parity: local runs {local_cmd}, CI runs {', '.join(ci_cmds)}")
            gaps.append(f"Check parity: local runs {local_cmd}, CI runs {', '.join(ci_cmds)}")
        else:
            print(f"[GAP]  Check parity: CI found but no test command detected")
            gaps.append("Check parity: CI found but no test command detected")
    elif ci_files:
        print("[WARN] Check parity: no local test target to compare against CI")

    print("-" * 60)
    print(f"{len(gaps)} gap(s) found" + ("." if gaps else ": none."))
    for g in gaps:
        print(f"  - {g}")
    print("Informational inventory only; no files were modified.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
