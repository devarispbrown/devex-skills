#!/usr/bin/env python3
"""Static inventory of a repo's community surface: seven standards files, quality signals, stage checklist. Stdlib only."""
import argparse
import re
from pathlib import Path

CONTRIBUTING_NAMES = ("CONTRIBUTING.md", "CONTRIBUTING.rst", "CONTRIBUTING.txt", "CONTRIBUTING")
COC_NAMES = ("CODE_OF_CONDUCT.md", "CODE_OF_CONDUCT.rst")
SECURITY_NAMES = ("SECURITY.md", "SECURITY.rst")
SUPPORT_NAMES = ("SUPPORT.md", "SUPPORT.rst")
GOVERNANCE_NAMES = ("GOVERNANCE.md", "GOVERNANCE.rst")
MAINTAINERS_NAMES = ("MAINTAINERS.md", "MAINTAINERS.rst")
LADDER_NAMES = (
    "LADDER.md", "CONTRIBUTOR_LADDER.md", "CONTRIBUTOR_LADDER.rst",
    "MAINTAINER_LADDER.md", "MAINTAINER_LADDER.rst",
)
DEV_ENV_NAMES = ("DEVELOPMENT.md", "DEV_ENV.md", "docs/development.md", "docs/dev-env.md")
ISSUE_TEMPLATE_DIRS = (".github/ISSUE_TEMPLATE", ".gitlab/issue_templates")
ISSUE_TEMPLATE_FILES = (".github/ISSUE_TEMPLATE.md", "ISSUE_TEMPLATE.md", ".gitlab/issue_templates.md")
PR_TEMPLATE_FILES = (
    ".github/pull_request_template.md", ".github/PULL_REQUEST_TEMPLATE.md",
    "PULL_REQUEST_TEMPLATE.md", "pull_request_template.md",
)

TEST_CMD_RE = re.compile(
    r"\b(make test|npm test|yarn test|pnpm test|pytest|go test|cargo test|mix test|mvn test|gradle test|dotnet test|rake test|bundle exec rspec)\b",
    re.IGNORECASE,
)
SETUP_RE = re.compile(r"\bsetup\b|\binstall\b|\bbootstrap\b|\bclone\b", re.IGNORECASE)
PR_RE = re.compile(r"\bpull request\b|\bPR\b", re.IGNORECASE)
GIFI_RE = re.compile(r"good[ -]first[ -]issue", re.IGNORECASE)
REPORT_ROUTE_RE = re.compile(r"\breport\b|\bcontact\b|\bemail\b|\breach out\b|\bprivate\b", re.IGNORECASE)
ENFORCE_RE = re.compile(
    r"\benforcement\b|\benforce\b|\bconsequence\b|\baction\b|\binvestigat\w*\b|\btemporar\w*\b|\bpermanent\b",
    re.IGNORECASE,
)
DISCLOSE_RE = re.compile(r"\bdisclos\w*\b|\breport\b|security@|\bvulnerab\w*\b|\bprivate\b", re.IGNORECASE)
SUPPORT_ROUTE_RE = re.compile(
    r"\bdiscussion\w*\b|\bforum\w*\b|\bchat\b|\bslack\b|\bdiscord\b|\bmailing list\b|\bstack overflow\b|\bcommunity channel\b",
    re.IGNORECASE,
)
ADVANCEMENT_RE = re.compile(
    r"\badvanc\w*\b|\bpromot\w*\b|\bbecome\b|\bmore involved\b|\bresponsib\w*\b|\bnew maintainer\b|\bladder\b|\broad to\b",
    re.IGNORECASE,
)
HANDLE_RE = re.compile(r"@[A-Za-z0-9_-]+")
AREA_RE = re.compile(r"\barea\w*\b|\bowner\b", re.IGNORECASE)
LADDER_QUALITY_RE = re.compile(
    r"\brung\b|\bpromotion\b|\bremoval\b|\bprivilege\w*\b|\bresponsib\w*\b", re.IGNORECASE
)
RECOGNITION_RE = re.compile(r"\brecogni\w*\b|\backnowledg\w*\b|\bthank\w*\b|\bcredits?\b|\bhall of fame\b", re.IGNORECASE)
TRIAGE_RE = re.compile(r"\btriage\b", re.IGNORECASE)
MODERATION_RE = re.compile(r"\bmoderat\w*\b", re.IGNORECASE)
FOUNDATION_RE = re.compile(r"\bfoundation\b", re.IGNORECASE)
SUCCESSION_RE = re.compile(r"\bsuccession\b|\bsucceed\w*\b", re.IGNORECASE)
SECURITY_TEAM_RE = re.compile(r"\bteam\b|\bresponse\b|\bcoordinator\w*\b", re.IGNORECASE)

# Stage requirements: ("label", kind, key). kind: file = file presence,
# check = keyword signal, info = metric/process, not statically verifiable.
STAGE_REQUIREMENTS = {
    0: [
        ("CONTRIBUTING.md", "file", "contributing"),
        ("CODE_OF_CONDUCT.md", "file", "coc"),
        ("Issue template", "file", "issue_template"),
        ("PR template", "file", "pr_template"),
        ("Documented dev environment", "check", "dev_env"),
    ],
    1: [
        ("Response SLO monitoring", "info", None),
        ("Good-first-issue labeling", "check", "gifi"),
        ("Triage process", "check", "triage"),
    ],
    2: [
        ("GOVERNANCE.md", "file", "governance"),
        ("Maintainer ladder", "file", "ladder"),
        ("Recognition program", "check", "recognition"),
    ],
    3: [
        ("Contributor analytics", "info", None),
        ("Delegation", "info", None),
        ("Moderation", "check", "moderation"),
        ("CoC enforcement", "check", "coc_enforce"),
    ],
    4: [
        ("Foundation governance", "check", "foundation"),
        ("Security response team", "check", "security_team"),
        ("Succession defined", "check", "succession"),
    ],
}
STAGE_NAMES = {0: "Founder-led", 1: "Early community", 2: "Growing", 3: "Scale", 4: "Foundation"}


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


def scan_texts(paths, regex):
    return any(text_has(p, regex) for p in paths if p is not None)


def main():
    ap = argparse.ArgumentParser(
        description="Inventory the community surface of a repository. Read-only; exits 0."
    )
    ap.add_argument("path", nargs="?", default=".", help="repository root to scan (default: current directory)")
    ap.add_argument("--stage", type=int, choices=sorted(STAGE_REQUIREMENTS), default=0,
                    help="checklist target stage (default: 0); lower-stage requirements are cumulative")
    a = ap.parse_args()
    root = Path(a.path).resolve()
    if not root.is_dir():
        raise SystemExit(f"error: not a directory: {root}")

    def find(names):
        return find_first(root, names) or find_first(root / ".github", names) or find_first(root / "docs", names)

    contributing = find(CONTRIBUTING_NAMES)
    coc = find(COC_NAMES)
    security = find(SECURITY_NAMES)
    support = find(SUPPORT_NAMES)
    governance = find(GOVERNANCE_NAMES)
    maintainers = find(MAINTAINERS_NAMES)
    ladder = find(LADDER_NAMES)

    issue_templates = []
    for d in ISSUE_TEMPLATE_DIRS:
        dp = root / d
        if dp.is_dir():
            issue_templates.extend(sorted(p for p in dp.iterdir() if p.is_file()))
    for f in ISSUE_TEMPLATE_FILES:
        p = root / f
        if p.is_file():
            issue_templates.append(p)
    pr_template = next((root / f for f in PR_TEMPLATE_FILES if (root / f).is_file()), None)
    dev_env_doc = find_first(root, DEV_ENV_NAMES)

    readme = find_first(root, ("README.md", "README.rst", "README"))

    print(f"Community surface inventory: {root}")
    print("-" * 60)

    def report(label, path, notes, ok):
        rel = path.relative_to(root) if path else "missing"
        detail = f" ({'; '.join(notes)})" if notes else ""
        print(f"[{'OK' if ok else 'GAP'}]  {label}: {rel}{detail}")

    gaps = []

    # 1. CONTRIBUTING.md
    if contributing:
        notes = []
        if text_has(contributing, TEST_CMD_RE):
            notes.append("states a test command")
        if text_has(contributing, PR_RE):
            notes.append("mentions pull requests")
        if text_has(contributing, GIFI_RE):
            notes.append("mentions good-first-issue")
        if text_has(contributing, SETUP_RE):
            notes.append("describes setup")
        report("CONTRIBUTING.md", contributing, notes, True)
        if not any(r.search(contributing.read_text(encoding="utf-8", errors="replace")) for r in (TEST_CMD_RE, PR_RE)):
            gaps.append("CONTRIBUTING.md exists but mentions neither a test command nor pull requests")
    else:
        report("CONTRIBUTING.md", None, ["missing"], False)
        gaps.append("CONTRIBUTING.md missing")

    # 2. CODE_OF_CONDUCT.md
    if coc:
        notes = []
        if text_has(coc, REPORT_ROUTE_RE):
            notes.append("has a report route")
        if text_has(coc, ENFORCE_RE):
            notes.append("states enforcement")
        report("CODE_OF_CONDUCT.md", coc, notes, True)
        if not text_has(coc, REPORT_ROUTE_RE):
            gaps.append("CODE_OF_CONDUCT.md lacks a report route")
    else:
        report("CODE_OF_CONDUCT.md", None, ["missing"], False)
        gaps.append("CODE_OF_CONDUCT.md missing")

    # 3. SECURITY.md
    if security:
        notes = []
        if text_has(security, DISCLOSE_RE):
            notes.append("has a disclosure route")
        report("SECURITY.md", security, notes, True)
        if not text_has(security, DISCLOSE_RE):
            gaps.append("SECURITY.md lacks a disclosure route")
    else:
        report("SECURITY.md", None, ["missing"], False)
        gaps.append("SECURITY.md missing")

    # 4. SUPPORT.md
    if support:
        notes = []
        if text_has(support, SUPPORT_ROUTE_RE):
            notes.append("routes to community channels")
        report("SUPPORT.md", support, notes, True)
        if not text_has(support, SUPPORT_ROUTE_RE):
            gaps.append("SUPPORT.md does not route questions away from the issue tracker")
    else:
        report("SUPPORT.md", None, ["missing"], False)
        gaps.append("SUPPORT.md missing")

    # 5. GOVERNANCE.md
    if governance:
        notes = []
        if text_has(governance, ADVANCEMENT_RE):
            notes.append("mentions advancement")
        report("GOVERNANCE.md", governance, notes, True)
        if not text_has(governance, ADVANCEMENT_RE):
            gaps.append("GOVERNANCE.md does not mention how outsiders gain responsibility")
    else:
        report("GOVERNANCE.md", None, ["missing"], False)
        gaps.append("GOVERNANCE.md missing")

    # 6. MAINTAINERS.md
    if maintainers:
        content = maintainers.read_text(encoding="utf-8", errors="replace")
        notes = []
        if HANDLE_RE.search(content) or ("|" in content and AREA_RE.search(content)):
            notes.append("names maintainers with areas")
        report("MAINTAINERS.md", maintainers, notes, True)
        if not notes:
            gaps.append("MAINTAINERS.md exists but names no maintainers or areas")
    else:
        report("MAINTAINERS.md", None, ["missing"], False)
        gaps.append("MAINTAINERS.md missing")

    # 7. Contributor ladder
    if ladder:
        notes = []
        if text_has(ladder, LADDER_QUALITY_RE):
            notes.append("describes rungs, promotion, or removal")
        report("Ladder", ladder, notes, True)
        if not text_has(ladder, LADDER_QUALITY_RE):
            gaps.append("Ladder file exists but lacks rung/promotion/removal signals")
    else:
        report("Ladder", None, ["missing"], False)
        gaps.append("No contributor ladder file")

    # 8. Issue and PR templates
    if issue_templates:
        names = ", ".join(sorted(str(p.relative_to(root)) for p in issue_templates))
        print(f"[OK]   Issue templates: {names}")
    else:
        print("[GAP]  Issue templates: missing")
        gaps.append("Issue templates missing")
    if pr_template:
        print(f"[OK]   PR template: {pr_template.relative_to(root)}")
    else:
        print("[GAP]  PR template: missing")
        gaps.append("PR template missing")

    # 9. Dev environment
    dev_env_ok = dev_env_doc is not None or (contributing is not None and text_has(contributing, SETUP_RE))
    if dev_env_ok:
        src = dev_env_ok.relative_to(root) if isinstance(dev_env_ok, Path) else "CONTRIBUTING.md setup section"
        print(f"[OK]   Dev environment: documented ({src})")
    else:
        print("[GAP]  Dev environment: not documented")
        gaps.append("No documented dev environment (DEVELOPMENT.md or setup instructions)")

    # Stage checklist (cumulative through the selected stage)
    print("-" * 60)
    print(f"Stage {a.stage} checklist ({STAGE_NAMES[a.stage]}); requirements are cumulative from Stage 0")
    stage_gaps = []
    for stage in range(0, a.stage + 1):
        for label, kind, key in STAGE_REQUIREMENTS[stage]:
            if kind == "info":
                status = "INFO"
            elif kind == "file":
                present = {
                    "contributing": contributing, "coc": coc, "issue_template": issue_templates,
                    "pr_template": pr_template, "governance": governance, "ladder": ladder,
                }[key]
                status = "OK" if present else "GAP"
            else:
                check = {
                    "dev_env": dev_env_ok,
                    "gifi": bool(contributing and text_has(contributing, GIFI_RE)) or (readme is not None and text_has(readme, GIFI_RE)),
                    "triage": scan_texts([contributing, support, governance], TRIAGE_RE),
                    "recognition": scan_texts([contributing, readme, governance], RECOGNITION_RE),
                    "moderation": scan_texts([coc, support], MODERATION_RE),
                    "coc_enforce": bool(coc and text_has(coc, ENFORCE_RE)),
                    "foundation": bool(governance and text_has(governance, FOUNDATION_RE)),
                    "security_team": bool(security and text_has(security, SECURITY_TEAM_RE)),
                    "succession": bool(governance and text_has(governance, SUCCESSION_RE)),
                }[key]
                status = "OK" if check else "GAP"
            if status == "GAP":
                stage_gaps.append(f"Stage {stage}: {label}")
            print(f"  [{'OK' if status == 'OK' else 'INFO' if status == 'INFO' else 'GAP'}]  Stage {stage} {label}: {status}")

    print("-" * 60)
    print(f"{len(gaps)} inventory gap(s), {len(stage_gaps)} stage requirement gap(s).")
    for g in gaps:
        print(f"  - {g}")
    for g in stage_gaps:
        print(f"  - {g}")
    print("Informational inventory only; no files were modified.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
