#!/usr/bin/env python3
"""Static inventory of a repository's agent-native readiness. Stdlib only."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

IGNORE_DIRS = {
    ".git", "node_modules", "vendor", ".venv", "venv", "dist", "build", "target",
    ".next", ".cache", "coverage", "__pycache__", ".terraform", "site-packages",
}

ENTRY_FILE_NAMES = {"agents.md", "claude.md", "agents.txt", "claude.txt"}

# An MCP server is how a product exposes itself to an agent at runtime. Nothing in the
# suite looked for one before, which left the surface the question is most often about
# entirely unmeasured.
MCP_FILE_NAMES = {
    "mcp.json", ".mcp.json", "mcp-server.json", "server.json",
    "claude_desktop_config.json", "mcp_config.json",
}
MCP_DEP_RE = re.compile(r"modelcontextprotocol|\bmcp[-_]?server\b|fastmcp", re.IGNORECASE)
MCP_DOC_RE = re.compile(r"\bMCP\b|model context protocol", re.IGNORECASE)
LLMS_TXT_NAMES = {"llms.txt", "llms-full.txt"}
SKILL_FILE_NAMES = {"skill.md"}

SCHEMA_FILE_NAMES = {
    "openapi.json", "openapi.yaml", "openapi.yml",
    "swagger.json", "swagger.yaml", "swagger.yml",
    "asyncapi.json", "asyncapi.yaml", "asyncapi.yml",
}

DOC_SUFFIXES = {".md", ".mdx", ".rst", ".txt", ".adoc"}

MANIFEST_NAMES = {
    "package.json", "pyproject.toml", "setup.py", "setup.cfg", "go.mod",
    "cargo.toml", "gemfile", "pom.xml", "build.gradle", "composer.json",
    "requirements.txt", "mix.exs",
}

README_NAMES = {"readme.md", "readme.rst", "readme.txt"}

JSON_FLAG_RE = re.compile(r"--json\b")
EXIT_CODE_RE = re.compile(
    r"\b(?:exit\s+(?:code|codes|status)|return\s+code|exitcode)\b", re.IGNORECASE
)


def walk(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        base = Path(current)
        for f in files:
            yield base / f


def is_schema(path: Path) -> bool:
    low = path.name.lower()
    if low in SCHEMA_FILE_NAMES:
        return True
    if low.startswith("openapi") or low.startswith("swagger") or low.startswith("asyncapi"):
        return True
    return low.endswith((".schema.json", ".schema.yaml", ".schema.yml"))


def is_doc(path: Path) -> bool:
    return path.suffix.lower() in DOC_SUFFIXES


def is_test(path: Path, root: Path) -> bool:
    parts = [p.lower() for p in path.relative_to(root).parts]
    if "test" in parts or "tests" in parts:
        return True
    name = path.name.lower()
    return (
        name.startswith("test_")
        or name.endswith(("_test.py", "_test.go"))
        or name.endswith((".test.js", ".spec.js"))
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory a repository's agent-native readiness surfaces."
    )
    parser.add_argument("root", nargs="?", default=".",
                        help="repository root (default: current directory)")
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 when gaps are found (default: exit 0, informational)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")

    entry_files, schemas, docs, tests, manifests, readmes = [], [], [], [], [], []
    mcp_files, mcp_deps, skills, llms = [], [], [], []
    for p in walk(root):
        low = p.name.lower()
        if low in ENTRY_FILE_NAMES:
            entry_files.append(p)
        if low in MCP_FILE_NAMES:
            mcp_files.append(p)
        if low in SKILL_FILE_NAMES:
            skills.append(p)
        if low in LLMS_TXT_NAMES:
            llms.append(p)
        if low in {"package.json", "pyproject.toml", "cargo.toml", "go.mod",
                   "requirements.txt"}:
            try:
                if MCP_DEP_RE.search(p.read_text(encoding="utf-8", errors="replace")):
                    mcp_deps.append(p)
            except OSError:
                pass
        if is_schema(p):
            schemas.append(p)
        if is_doc(p):
            docs.append(p)
        if low in README_NAMES:
            readmes.append(p)
        if low in MANIFEST_NAMES:
            manifests.append(p)
        if is_test(p, root):
            tests.append(p)

    json_flagged, exit_coded, mcp_docs = [], [], []
    for d in docs:
        try:
            text = d.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if JSON_FLAG_RE.search(text):
            json_flagged.append(d)
        if EXIT_CODE_RE.search(text):
            exit_coded.append(d)
        if MCP_DOC_RE.search(text):
            mcp_docs.append(d)

    def rel(p: Path) -> str:
        return str(p.relative_to(root))

    def names(paths, limit=3) -> str:
        if not paths:
            return "none found"
        shown = [rel(p) for p in sorted(paths)[:limit]]
        extra = len(paths) - len(shown)
        return ", ".join(shown) + (f" (+{extra} more)" if extra > 0 else "")

    checks = [
        ("agent entry file (AGENTS.md/CLAUDE.md)", bool(entry_files), names(entry_files)),
        ("machine-readable schema (OpenAPI/JSON Schema)", bool(schemas), names(schemas)),
        ("structured CLI output documented (--json)", bool(json_flagged), names(json_flagged)),
        ("exit codes documented", bool(exit_coded), names(exit_coded)),
        ("test discoverability markers", bool(tests), names(tests)),
        ("README present", bool(readmes), names(readmes)),
        ("build/config manifest present", bool(manifests), names(manifests)),
        ("MCP server exposed", bool(mcp_files or mcp_deps), names(mcp_files + mcp_deps)),
        ("MCP documented for users", bool(mcp_docs), names(mcp_docs)),
        ("agent skills shipped", bool(skills), names(skills)),
        ("llms.txt for doc retrieval", bool(llms), names(llms)),
    ]

    print(f"Agent-native readiness inventory: {root}")
    print()
    gaps = 0
    for label, ok, detail in checks:
        if not ok:
            gaps += 1
        print(f"[{'OK ' if ok else 'GAP'}] {label:34} {detail}")

    passed = len(checks) - gaps
    pct = round(100 * passed / len(checks))
    band = ("agent-ready" if pct >= 80 else
            "partly agent-ready" if pct >= 50 else "not agent-ready")
    print()
    print(f"Agent readiness: {passed}/{len(checks)} surfaces present ({pct}%) - {band}")
    if gaps:
        print("This is an inventory signal, not a verdict. Inspect each gap before acting.")
    print("Exits 0 by default (informational); pass --strict to exit 1 on gaps.")

    return 1 if (args.strict and gaps) else 0


if __name__ == "__main__":
    raise SystemExit(main())
