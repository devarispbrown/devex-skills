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

# The surfaces above tell an agent the repository exists. The ones below decide whether
# it can do the work: set up from a clean clone, verify its own change, match the style
# the project enforces, and avoid destroying something unattended.
SETUP_RE = re.compile(
    r"(?:^|\n)\s*(?:\$\s*)?(?:make\s+(?:setup|install|bootstrap|dev)"
    r"|script/(?:setup|bootstrap)|uv\s+sync|poetry\s+install|pipenv\s+install"
    r"|npm\s+(?:ci|install)|pnpm\s+install|yarn\s+install|bundle\s+install"
    r"|cargo\s+build|go\s+mod\s+download|pip\s+install\s+-e)",
    re.IGNORECASE)
TEST_CMD_RE = re.compile(
    r"(?:^|\n)\s*(?:\$\s*)?(?:make\s+test|npm\s+(?:test|run\s+test)|pnpm\s+test"
    r"|yarn\s+test|pytest|tox|nox|cargo\s+test|go\s+test|bundle\s+exec\s+rspec"
    r"|rake\s+test|mvn\s+test|gradle\s+test|uv\s+run\s+pytest)",
    re.IGNORECASE)
LINT_CMD_RE = re.compile(
    r"\b(?:ruff|black|flake8|eslint|prettier|clippy|gofmt|golangci-lint|rubocop"
    r"|standardrb|ktlint|spotless|pre-commit)\b", re.IGNORECASE)
ARCH_FILE_RE = re.compile(r"^(architecture|design|internals|hacking|development)\.(md|rst|txt)$",
                          re.IGNORECASE)
TOOLCHAIN_NAMES = {
    ".tool-versions", ".nvmrc", ".python-version", ".ruby-version", "rust-toolchain",
    "rust-toolchain.toml", ".go-version", ".java-version", "runtime.txt", ".mise.toml",
}
DRYRUN_RE = re.compile(r"--dry-run|--dryrun|\bdry run\b|--no-act", re.IGNORECASE)
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
    toolchains, arch_files, ci_files = [], [], []
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
        if low in TOOLCHAIN_NAMES:
            toolchains.append(p)
        if ARCH_FILE_RE.match(p.name):
            arch_files.append(p)
        if ".github/workflows" in str(p).replace("\\", "/") and p.suffix in {".yml", ".yaml"}:
            ci_files.append(p)
        if low in {".gitlab-ci.yml", "azure-pipelines.yml", ".circleci/config.yml"}:
            ci_files.append(p)
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
    setup_docs, test_docs, lint_docs, dryrun_docs = [], [], [], []
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
        if SETUP_RE.search(text):
            setup_docs.append(d)
        if TEST_CMD_RE.search(text):
            test_docs.append(d)
        if LINT_CMD_RE.search(text):
            lint_docs.append(d)
        if DRYRUN_RE.search(text):
            dryrun_docs.append(d)

    ci_text = ""
    for f in ci_files:
        try:
            ci_text += f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
    # Parity is the property an agent depends on most: if a green local run does not
    # predict a green CI run, the agent cannot tell whether its change is finished.
    ci_parity = bool(ci_files and test_docs and TEST_CMD_RE.search(ci_text))

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
        ("setup command documented", bool(setup_docs), names(setup_docs)),
        ("test command documented", bool(test_docs), names(test_docs)),
        ("lint or format tool declared", bool(lint_docs), names(lint_docs)),
        ("CI config present", bool(ci_files), names(ci_files)),
        ("CI runs the documented test command", ci_parity,
         "documented test command appears in CI" if ci_parity else "no shared command found"),
        ("toolchain version pinned", bool(toolchains), names(toolchains)),
        ("architecture or internals doc", bool(arch_files), names(arch_files)),
        ("destructive-operation guardrail documented", bool(dryrun_docs), names(dryrun_docs)),
    ]

    print(f"Agent-native readiness inventory: {root}")
    gaps = 0
    for i, (label, ok, detail) in enumerate(checks):
        if i == 0:
            print("\nCan an agent find its way around\n")
        elif i == 7:
            print("\nCan an agent operate the product\n")
        elif i == 11:
            print("\nCan an agent do the work\n")
        if not ok:
            gaps += 1
        print(f"  [{'OK ' if ok else 'GAP'}] {label:42} {detail}")

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
