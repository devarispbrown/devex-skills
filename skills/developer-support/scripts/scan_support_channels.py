#!/usr/bin/env python3
"""Inventory support-routing artifacts in a tree and report channel coverage.

Finds SUPPORT.md, issue forms and templates, CONTRIBUTING security sections,
and docs feedback links, then prints a request-class vs channel checklist
with gaps. Informs only; always exits 0.

Stdlib only.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

IGNORE_DIRS = {
    ".git", "node_modules", "vendor", ".venv", "venv", "dist", "build",
    "target", ".next", ".cache", "coverage", "__pycache__", ".terraform",
}

CLASS_ORDER = ("bug", "feature", "how-to", "security", "billing", "outage", "data-loss")

# Keywords used to classify an issue form: filename + frontmatter text.
CLASS_KEYWORDS = {
    "bug": ("bug", "defect", "broken", "regression"),
    "feature": ("feature", "enhancement", "idea", "proposal", "roadmap"),
    "how-to": ("how-to", "howto", "question", "help"),
    "security": ("security", "vulnerability", "vuln", "cve"),
    "billing": ("billing", "invoice", "payment", "charge", "quota"),
    "outage": ("outage", "incident", "status", "downtime", "degraded"),
    "data-loss": ("data-loss", "data loss", "restore", "corruption", "deleted"),
}

# A SUPPORT.md that mentions these topics covers the corresponding classes.
SUPPORT_TOPICS = {
    "billing": ("billing", "invoice", "payment", "charge", "quota"),
    "outage": ("status", "outage", "incident", "downtime"),
    "data-loss": ("data loss", "data-loss", "restore"),
    "how-to": ("community", "discord", "forum", "slack", "help"),
}

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
MARKDOWN_SUFFIXES = {".md", ".mdx"}
FORM_SUFFIXES = {".yml", ".yaml", ".md"}


def walk(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        base = Path(current)
        for name in files:
            yield base / name


def read_small(path: Path, limit: int = 200_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def find_issue_forms(root: Path) -> list[Path]:
    forms = []
    for p in walk(root):
        low = p.name.lower()
        parts = {x.lower() for x in p.parts}
        if low in ("config.yml", "config.yaml"):  # ISSUE_TEMPLATE config, not a form
            continue
        if ".github" in parts and "issue_template" in parts and p.suffix.lower() in FORM_SUFFIXES:
            forms.append(p)
        elif low == "issue_template.md":
            forms.append(p)
    return forms


def classify_form(path: Path, text: str) -> list[str]:
    haystack = f"{path.name} {text[:4000]}".lower()
    found = []
    for cls, kws in CLASS_KEYWORDS.items():
        if any(kw in haystack for kw in kws):
            found.append(cls)
    return found or ["unknown"]


def security_route(root: Path) -> str:
    for candidate in ("SECURITY.md", ".github/SECURITY.md"):
        if (root / candidate).is_file():
            return candidate
    for p in walk(root):
        if p.name.lower() == "contributing.md":
            text = read_small(p).lower()
            if "security" in text and ("vulnerability" in text or "report" in text):
                return "CONTRIBUTING.md security section"
    return ""


def readme_support_link(root: Path) -> tuple[bool, str]:
    for p in walk(root):
        if p.name.lower() == "readme.md":
            for label, href in LINK_RE.findall(read_small(p)):
                if "support" in f"{label} {href}".lower() or "help" in f"{label} {href}".lower():
                    return True, str(p.relative_to(root))
            return False, str(p.relative_to(root))
    return False, ""


def docs_feedback_links(root: Path) -> list[tuple[str, str]]:
    hits = []
    for p in walk(root):
        if p.suffix.lower() not in MARKDOWN_SUFFIXES:
            continue
        for label, href in LINK_RE.findall(read_small(p)):
            if "feedback" in f"{label} {href}".lower():
                hits.append((str(p.relative_to(root)), label or href))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", nargs="?", default=".", help="repository root to scan (default: .)")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    support = next((p for p in walk(root) if p.name.lower() == "support.md"), None)
    support_text = read_small(support) if support else ""

    forms = find_issue_forms(root)
    form_classes = {}
    for f in sorted(forms, key=lambda p: str(p)):
        form_classes[str(f.relative_to(root))] = classify_form(f, read_small(f))

    sec_route = security_route(root)
    readme_support, readme_path = readme_support_link(root)
    feedback = docs_feedback_links(root)

    covered = {}
    for cls in CLASS_ORDER:
        covered[cls] = []
    for rel, cls_list in form_classes.items():
        for cls in cls_list:
            if cls != "unknown":
                covered[cls].append(rel)
    if support_text:
        low = support_text.lower()
        for cls, kws in SUPPORT_TOPICS.items():
            if any(k in low for k in kws):
                covered[cls].append("SUPPORT.md")
    if sec_route:
        covered["security"].append(sec_route)

    print(f"Repository: {root}\n")
    print("## Inventory")
    print(f"SUPPORT.md         : {support.relative_to(root) if support else 'missing'}")
    print(f"Issue forms        : {len(forms)}")
    for rel, cls_list in form_classes.items():
        print(f"  {rel}  -> {', '.join(cls_list)}")
    print(f"Security route     : {sec_route or 'missing'}")
    if readme_path:
        print(f"README             : {readme_path}" + (" (support link found)" if readme_support else " (no support link)"))
    else:
        print("README             : missing")
    print(f"Docs feedback links: {len(feedback)}")
    for rel, label in feedback[:10]:
        print(f"  {rel}  -> {label}")

    print("\n## Channel vs request-class checklist")
    gaps = []
    for cls in CLASS_ORDER:
        if covered[cls]:
            print(f"  {cls:10} covered  ({', '.join(covered[cls])})")
        else:
            print(f"  {cls:10} GAP      (no route found)")
            gaps.append(cls)
    if not readme_path:
        print("  README     GAP      (no README with support link)")
        gaps.append("README support link")
    elif not readme_support:
        print("  README     GAP      (no support/help link in README)")
        gaps.append("README support link")

    print("\n## Gaps")
    if not gaps:
        print("None.")
    else:
        for g in gaps:
            if g == "feature":
                print("  feature: no feature request route (issue form or roadmap template)")
            elif g == "security":
                print("  security: no dedicated security reporting route (SECURITY.md, CONTRIBUTING section, or security issue form)")
            elif g == "how-to":
                print("  how-to: no help/community route (SUPPORT.md help section or docs feedback links)")
            elif g == "billing":
                print("  billing: no billing route (issue form or SUPPORT.md billing section)")
            elif g == "outage":
                print("  outage: no outage/status route (issue form or SUPPORT.md status section)")
            elif g == "data-loss":
                print("  data-loss: no data-loss route (issue form or SUPPORT.md data-loss section)")
            elif g == "README support link":
                print("  README: no support/help link (SUPPORT.md or support channel unreachable from README)")
            else:
                print(f"  {g}: no route found")

    print("\nInformational only; this scan never fails a build. Exit 0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
