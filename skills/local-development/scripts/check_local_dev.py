#!/usr/bin/env python3
"""Inventory local-development setup surfaces in a repository. Stdlib only."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

IGNORE_DIRS = {
    ".git", "node_modules", "vendor", ".venv", "venv", "dist", "build", "target",
    ".next", ".cache", "coverage", "__pycache__", ".terraform", ".tox", ".nox",
}

TOOLCHAIN_PINS = {
    ".nvmrc", ".node-version", ".python-version", ".tool-versions", ".mise.toml",
    "rust-toolchain.toml", "rust-toolchain", ".ruby-version", ".java-version",
}

LOCKFILES = {
    "package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml",
    "uv.lock", "poetry.lock", "pipfile.lock", "go.sum", "cargo.lock",
    "gemfile.lock", "composer.lock",
}

COMPOSE_NAMES = {"docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"}

DEV_SCRIPT_HINTS = ("dev", "start", "serve", "watch", "run", "test", "build", "setup", "doctor")


def walk(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        base = Path(current)
        for f in files:
            yield base / f


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def package_scripts(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return []
    scripts = data.get("scripts")
    return sorted(scripts) if isinstance(scripts, dict) else []


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory local-dev setup surfaces. Read-only; informs, never fails."
    )
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    makefiles: list[str] = []
    package_json: list[Path] = []
    devcontainers: list[str] = []
    compose: list[str] = []
    env_examples: list[str] = []
    lockfiles: list[str] = []
    pins: list[str] = []
    script_names: set[str] = set()

    for p in walk(root):
        rp = rel(p, root)
        low = p.name.lower()
        parts = {x.lower() for x in p.parts}
        if low in {"makefile", "gnumakefile"}:
            makefiles.append(rp)
        if low == "package.json":
            package_json.append(p)
            script_names.update(package_scripts(p))
        if "devcontainer" in low or "devcontainer" in parts:
            devcontainers.append(rp)
        if low in COMPOSE_NAMES:
            compose.append(rp)
        if low.endswith(".env.example"):
            env_examples.append(rp)
        if low in LOCKFILES:
            lockfiles.append(rp)
        if low in TOOLCHAIN_PINS:
            pins.append(rp)

    def check(label: str, items: list[str]) -> None:
        if items:
            print(f"[present] {label}")
            for item in sorted(set(items)):
                print(f"          {item}")
        else:
            print(f"[absent ] {label}")

    print(f"Repository: {root}")
    print("\n## Local-dev setup checklist\n")

    check("Makefile", makefiles)
    check("package.json with scripts", [rel(p, root) for p in package_json])
    check("devcontainer.json", devcontainers)
    check("docker compose files", compose)
    check(".env.example", env_examples)
    check("lockfiles", lockfiles)
    check("toolchain pins", pins)

    matched = sorted(n for n in script_names if any(h in n.lower() for h in DEV_SCRIPT_HINTS))
    if matched:
        print(f"[present] dev-related package.json scripts: {', '.join(matched)}")
    else:
        print("[absent ] dev-related package.json scripts")

    print("\nInventory only: this script does not judge quality or fail a setup. See SKILL.md for the gate procedure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
