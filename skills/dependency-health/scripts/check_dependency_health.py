#!/usr/bin/env python3
"""Scan manifests for dependency health signals: duplicates, unpinned versions, abandoned markers. Stdlib only."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

IGNORE_DIRS = {
    ".git", "node_modules", "vendor", ".venv", "venv", "dist", "build", "target",
    ".next", ".cache", "coverage", "__pycache__", ".terraform", ".idea",
}

MANIFESTS = {
    "package.json": "npm",
    "go.mod": "go",
    "Cargo.toml": "cargo",
    "requirements.txt": "pip",
    "pyproject.toml": "pyproject",
}

# Name-only heuristic. Confirm with maintenance signals before acting.
ABANDONED_MARKERS = {
    "request", "left-pad", "moment", "core-js", "bower", "node-sass", "pycrypto",
}

EXACT_SEMVER = re.compile(r"^\d+\.\d+\.\d+([-+][0-9A-Za-z.\-]+)?$")
GO_VERSION = re.compile(r"^v\d")
PIP_SPEC = re.compile(
    r"^(?P<name>[A-Za-z0-9_.\-\[\]]+)\s*(?P<op>==|!=|>=|<=|~=|===|>|<)?\s*(?P<spec>.*)$"
)


def parse_package_json(path: Path):
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError):
        return None
    deps = {}
    for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        block = data.get(section)
        if not isinstance(block, dict):
            continue
        for name, spec in block.items():
            spec = str(spec)
            deps[name] = (spec, EXACT_SEMVER.fullmatch(spec) is not None)
    return deps


def parse_go_mod(path: Path):
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    deps = {}
    in_block = False
    for raw in lines:
        line = raw.strip()
        if line.startswith("require ("):
            in_block = True
            continue
        if in_block:
            if line == ")":
                in_block = False
                continue
            parts = line.split()
            if len(parts) >= 2:
                deps[parts[0]] = (parts[1], GO_VERSION.match(parts[1]) is not None)
        elif line.startswith("require ") and "(" not in line:
            parts = line.split()
            if len(parts) >= 2:
                deps[parts[0]] = (parts[1], GO_VERSION.match(parts[1]) is not None)
    return deps


def parse_requirements(path: Path):
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    deps = {}
    for raw in lines:
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith(("-", "[")):
            continue
        m = PIP_SPEC.match(line)
        if not m:
            continue
        name, op, spec = m.group("name"), m.group("op") or "", m.group("spec")
        pinned = op == "==" and bool(spec) and not re.search(r"[,\s*]", spec)
        deps[name] = (op + spec, pinned)
    return deps


def _pip_entries(chunk: str, deps: dict):
    for m in re.finditer(r'"([^"]+)"', chunk):
        entry = m.group(1)
        dm = PIP_SPEC.match(entry)
        if not dm:
            continue
        op = dm.group("op") or ""
        spec = dm.group("spec")
        pinned = op == "==" and bool(spec) and not re.search(r"[,\s*]", spec)
        deps[dm.group("name")] = (op + spec, pinned)


def parse_pyproject(path: Path):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    deps = {}
    sections = re.split(r"(?m)^(\[[^\]]*\])", text)
    for i in range(1, len(sections), 2):
        name, body = sections[i], sections[i + 1] if i + 1 < len(sections) else ""
        if name in ("[project]", "[project.optional-dependencies]"):
            if name == "[project]":
                m = re.search(r"dependencies\s*=\s*\[(.*?)\]", body, re.S)
                if m:
                    _pip_entries(m.group(1), deps)
            else:
                for m in re.finditer(r"^\s*[A-Za-z0-9_.\-]+\s*=\s*\[(.*?)\]", body, re.S | re.M):
                    _pip_entries(m.group(1), deps)
        elif name == "[tool.poetry.dependencies]":
            for line in body.splitlines():
                m = re.match(r'^\s*([A-Za-z0-9_.\-]+)\s*=\s*"([^"]*)"', line)
                if m and m.group(1) != "python":
                    spec = m.group(2)
                    deps[m.group(1)] = (spec, EXACT_SEMVER.fullmatch(spec) is not None)
    return deps


def _cargo_pinned(spec: str) -> bool:
    if spec.startswith("="):
        spec = spec[1:].strip()
    return EXACT_SEMVER.fullmatch(spec) is not None


def parse_cargo(path: Path):
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    deps = {}
    section = None
    for raw in lines:
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("["):
            section = line
            continue
        if section in ("[dependencies]", "[dev-dependencies]", "[build-dependencies]"):
            m = re.match(r'^([A-Za-z0-9_\-]+)\s*=\s*\{\s*version\s*=\s*"([^"]+)"', line)
            if m:
                deps[m.group(1)] = (m.group(2), _cargo_pinned(m.group(2)))
                continue
            m = re.match(r'^([A-Za-z0-9_\-]+)\s*=\s*"([^"]+)"\s*$', line)
            if m:
                deps[m.group(1)] = (m.group(2), _cargo_pinned(m.group(2)))
                continue
            m = re.match(r"^([A-Za-z0-9_\-]+)\s*$", line)
            if m:
                deps.setdefault(m.group(1), ("", False))
        elif section and section.startswith("[dependencies."):
            m = re.match(r'^version\s*=\s*"([^"]+)"', line)
            if m:
                name = section[len("[dependencies."):].rstrip("]")
                deps[name] = (m.group(1), _cargo_pinned(m.group(1)))
    return deps


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Static dependency health scan: lists direct dependencies and flags duplicates "
        "across manifests, unpinned versions, and known-abandoned markers. Read-only; "
        "exit code is always 0 (informs, never blocks)."
    )
    ap.add_argument("root", nargs="?", default=".", help="tree to scan (default: current directory)")
    args = ap.parse_args()
    if not Path(args.root).is_dir():
        raise SystemExit(f'not a directory: {args.root}')
    root = Path(args.root).resolve()

    manifests = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            if f in MANIFESTS:
                manifests.append(Path(current) / f)

    parsers = {
        "npm": parse_package_json, "go": parse_go_mod, "cargo": parse_cargo,
        "pip": parse_requirements, "pyproject": parse_pyproject,
    }
    scanned, skipped = [], []
    for p in sorted(manifests):
        deps = parsers[MANIFESTS[p.name]](p)
        if deps is None:
            skipped.append(p)
            continue
        scanned.append((p, MANIFESTS[p.name], deps))

    name_locs = {}
    for p, _fmt, deps in scanned:
        for name in deps:
            name_locs.setdefault(name.lower(), []).append(str(p))
    dupes = {name: sorted(set(locs)) for name, locs in sorted(name_locs.items()) if len(set(locs)) > 1}

    print("# Dependency health scan")
    print(f"Root: {root}")
    print()
    print(f"## Manifests ({len(scanned)})")
    for p, fmt, deps in sorted(scanned, key=lambda t: str(t[0])):
        unpinned = sum(1 for _spec, pinned in deps.values() if not pinned)
        names = ", ".join(sorted(deps))
        print(f"- {p} ({fmt}): {len(deps)} direct deps ({names}), {unpinned} unpinned")
    for p in sorted(skipped):
        print(f"- {p}: skipped (unreadable or unparsable)")
    print()

    print("## Duplicates (same package in multiple manifests)")
    if dupes:
        for name, locs in dupes.items():
            print(f"- {name}: {', '.join(locs)}")
    else:
        print("- none")
    print()

    print("## Unpinned versions")
    unpinned_entries = 0
    for p, _fmt, deps in sorted(scanned, key=lambda t: str(t[0])):
        for name, (spec, pinned) in sorted(deps.items()):
            if not pinned:
                unpinned_entries += 1
                print(f"- {name} @ {p} [{spec or '(no version)'}]")
    if not unpinned_entries:
        print("- none")
    print()

    print("## Possibly abandoned or deprecated (verify before acting)")
    abandoned = 0
    for p, _fmt, deps in sorted(scanned, key=lambda t: str(t[0])):
        for name, (spec, _pinned) in sorted(deps.items()):
            if name.lower() in ABANDONED_MARKERS:
                abandoned += 1
                print(f"- {name} @ {p} [{spec}]")
    if not abandoned:
        print("- none")
    print()

    total_direct = sum(len(deps) for _p, _f, deps in scanned)
    print("## Summary")
    print(
        f"manifests={len(scanned)} direct_deps={total_direct} unique_packages={len(name_locs)} "
        f"duplicates={len(dupes)} unpinned_entries={unpinned_entries} abandoned_markers={abandoned}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
