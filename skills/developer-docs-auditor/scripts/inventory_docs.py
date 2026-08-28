#!/usr/bin/env python3
"""Inventory documentation-related surfaces in a repository.

This script intentionally does not judge correctness. It gives the agent a compact map
of likely documentation sources and public-interface artifacts before deeper review.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

IGNORE_DIRS = {
    ".git", "node_modules", "vendor", ".venv", "venv", "dist", "build", "target",
    ".next", ".cache", "coverage", "__pycache__", ".terraform"
}

DOC_NAMES = {
    "readme.md", "contributing.md", "security.md", "changelog.md", "changes.md",
    "migration.md", "migrations.md", "architecture.md", "design.md", "claude.md",
    "agents.md", "code_of_conduct.md", "license.md"
}

SPEC_SUFFIXES = {
    ".proto", ".graphql", ".gql", ".raml", ".apib"
}

SPEC_NAMES = {
    "openapi.json", "openapi.yaml", "openapi.yml", "swagger.json", "swagger.yaml",
    "swagger.yml", "asyncapi.json", "asyncapi.yaml", "asyncapi.yml"
}

PACKAGE_FILES = {
    "package.json", "pyproject.toml", "setup.py", "setup.cfg", "go.mod", "cargo.toml",
    "gemfile", "pom.xml", "build.gradle", "build.gradle.kts", "composer.json"
}

CI_HINTS = {".github", ".gitlab-ci.yml", "circle.yml", ".circleci"}


def walk(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        base = Path(current)
        for f in files:
            yield base / f


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    buckets: dict[str, list[str]] = {
        "docs": [], "specs": [], "examples": [], "packages": [], "tests": [], "ci": [],
    }

    for p in walk(root):
        rp = rel(p, root)
        low = p.name.lower()
        parts = {x.lower() for x in p.parts}

        if p.suffix.lower() in {".md", ".mdx", ".rst", ".adoc"} or low in DOC_NAMES:
            buckets["docs"].append(rp)
        if low in SPEC_NAMES or p.suffix.lower() in SPEC_SUFFIXES:
            buckets["specs"].append(rp)
        if "example" in parts or "examples" in parts or "sample" in parts or "samples" in parts:
            buckets["examples"].append(rp)
        if low in PACKAGE_FILES:
            buckets["packages"].append(rp)
        if "test" in parts or "tests" in parts or p.name.startswith("test_") or p.name.endswith("_test.go"):
            buckets["tests"].append(rp)
        if any(hint in rp.lower() for hint in CI_HINTS):
            buckets["ci"].append(rp)

    print(f"Repository: {root}")
    for name, items in buckets.items():
        print(f"\n## {name} ({len(items)})")
        for item in sorted(set(items))[:300]:
            print(item)
        if len(set(items)) > 300:
            print("... truncated ...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
