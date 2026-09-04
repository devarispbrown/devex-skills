#!/usr/bin/env python3
"""Inventory environment-lifecycle surfaces in a repository tree.

Detects local development surfaces (devcontainer/compose/Dockerfile), CI
environment matrices, deploy automation, TTL markers, cleanup automation,
and seed automation, then prints a lifecycle checklist with gaps.

Inventory only: reports what exists and what is missing; never asserts
correctness. Always exits 0. Stdlib only.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

IGNORE_DIRS = {
    ".git", "node_modules", "vendor", ".venv", "venv", "dist", "build",
    "target", ".next", ".cache", "coverage", "__pycache__", ".terraform",
    ".serverless", ".pytest_cache",
}

CODE_SUFFIXES = {
    ".sh", ".bash", ".zsh", ".py", ".js", ".ts", ".yml", ".yaml", ".json",
    ".toml", ".tf", ".hcl", ".dockerfile",
}

TEXT_SUFFIXES = CODE_SUFFIXES | {".md", ".mdx", ".txt", ".ini", ".env", ".rst"}

LOCAL_FILE_NAMES = {
    "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml",
    "dockerfile", "vagrantfile", "devcontainer.json",
}

CI_DIR_HINTS = (".github/workflows", ".circleci", ".buildkite")
CI_NAME_HINTS = ("gitlab-ci", "circleci", "azure-pipelines", "jenkinsfile", "buildkite")

DEPLOY_NAME_HINTS = ("deploy", "promote")
DEPLOY_DIR_HINTS = ("terraform", "k8s", "kubernetes", "helm", "serverless", "cloudformation", "ansible")

TTL_RE = re.compile(
    r"\b(ttl|time-to-live|expires|expiration|expiry|lifetime|delete-after|delete_after)\b",
    re.IGNORECASE,
)
CLEANUP_RE = re.compile(
    r"\b(cleanup|clean-up|destroy|teardown|tear-down|prune|orphan)\b",
    re.IGNORECASE,
)
SEED_RE = re.compile(r"\bseed\b", re.IGNORECASE)

MATRIX_KW_RE = re.compile(r"\bmatrix\b", re.IGNORECASE)
MATRIX_ENV_LIST_RE = re.compile(r"environment\s*:\s*\[([^\]]+)\]", re.IGNORECASE)
MATRIX_ENV_ITEM_RE = re.compile(r"^\s*-\s+environment\s*:\s*([A-Za-z0-9_-]+)\s*$", re.IGNORECASE)


def walk(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        base = Path(current)
        for f in files:
            yield base / f


def read_safe(path: Path):
    try:
        return path.read_text(errors="ignore")
    except OSError:
        return None


def extract_matrix_envs(text: str) -> list[str]:
    found = []
    for m in MATRIX_ENV_LIST_RE.finditer(text):
        for name in re.split(r"[,\s]+", m.group(1)):
            name = name.strip()
            if name and "${" not in name and "{{" not in name:
                found.append(name)
    for m in MATRIX_ENV_ITEM_RE.finditer(text):
        name = m.group(1).strip()
        if name and "${" not in name and "{{" not in name:
            found.append(name)
    return sorted(set(found))


def classify(p: Path, root: Path, local, ci, deploy, ttl, cleanup, seed) -> None:
    rp = str(p.relative_to(root))
    rl = rp.lower()
    low_name = p.name.lower()
    parts = {x.lower() for x in p.parts}
    suffix = p.suffix.lower()

    if ".devcontainer" in parts or low_name == "devcontainer.json":
        local.append((rp, "devcontainer"))
    elif low_name in {"docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"}:
        local.append((rp, "compose"))
    elif low_name == "dockerfile" or low_name.startswith("dockerfile."):
        local.append((rp, "dockerfile"))

    is_ci = any(d in rl for d in CI_DIR_HINTS) or any(n in low_name for n in CI_NAME_HINTS)
    if is_ci:
        envs = None
        text = read_safe(p) if suffix in TEXT_SUFFIXES or suffix == "" else None
        if text is not None and MATRIX_KW_RE.search(text):
            envs = extract_matrix_envs(text)
        ci.append((rp, envs))

    is_deploy = any(d in parts for d in DEPLOY_DIR_HINTS) or any(n in low_name for n in DEPLOY_NAME_HINTS)
    if is_deploy:
        deploy.append(rp)

    if is_ci or is_deploy or suffix in CODE_SUFFIXES or suffix == "":
        text = read_safe(p) if suffix in TEXT_SUFFIXES or suffix == "" else None
        if text is None:
            return
        if TTL_RE.search(text):
            ttl.append(rp)
        if CLEANUP_RE.search(text):
            cleanup.append(rp)
        if "seed" in low_name or SEED_RE.search(text):
            seed.append(rp)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Inventory environment-lifecycle surfaces in a tree. "
                    "Inventory only: reports surfaces and gaps, never correctness; exits 0.",
    )
    ap.add_argument("root", nargs="?", default=".", help="directory tree to scan (default: .)")
    args = ap.parse_args()
    if not Path(args.root).is_dir():
        raise SystemExit(f'not a directory: {args.root}')
    root = Path(args.root).resolve()

    local = []
    ci = []
    deploy = []
    ttl = []
    cleanup = []
    seed = []

    for p in walk(root):
        classify(p, root, local, ci, deploy, ttl, cleanup, seed)

    print(f"Environment lifecycle inventory: {root}")
    print("Inventory only: surfaces and gaps are listed, never judged. Exit code is always 0.\n")

    print("## Surfaces")
    print(f"- local development surfaces ({len(local)}):")
    for rp, kind in sorted(local):
        print(f"    - {kind}: {rp}")
    if not local:
        print("    - none")
    print(f"- CI files ({len(ci)}):")
    for rp, envs in sorted(ci):
        if envs:
            print(f"    - {rp}: matrix environments {', '.join(envs)}")
        else:
            print(f"    - {rp}: no matrix environments detected")
    if not ci:
        print("    - none")
    print(f"- deploy configs ({len(deploy)}):")
    for rp in sorted(deploy):
        print(f"    - {rp}")
    if not deploy:
        print("    - none")
    print(f"- TTL markers ({len(ttl)}):")
    for rp in sorted(ttl):
        print(f"    - {rp}")
    if not ttl:
        print("    - none")
    print(f"- cleanup automation ({len(cleanup)}):")
    for rp in sorted(cleanup):
        print(f"    - {rp}")
    if not cleanup:
        print("    - none")
    print(f"- seed automation ({len(seed)}):")
    for rp in sorted(seed):
        print(f"    - {rp}")
    if not seed:
        print("    - none")

    devcontainer_found = any(kind == "devcontainer" for _, kind in local)
    ci_with_matrix = [rp for rp, envs in ci if envs is not None]
    matrix_envs = sorted({e for _, envs in ci for e in (envs or [])})

    items = []
    if local:
        items.append(("[ok]", f"local development surface exists ({len(local)} file(s))"))
    else:
        items.append(("[gap]", "no local development surface (devcontainer/compose/Dockerfile)"))
    if devcontainer_found:
        items.append(("[ok]", "devcontainer defined"))
    else:
        items.append(("[gap]", "no devcontainer - containerized local loop not reproducible"))
    if ci_with_matrix:
        items.append(("[ok]", f"CI matrix targets environments: {', '.join(matrix_envs) or 'dynamic'}"))
    elif ci:
        items.append(("[gap]", "CI exists but no environment matrix - stage coverage unverified"))
    else:
        items.append(("[gap]", "no CI environment matrix - stage coverage unverified"))
    if deploy:
        items.append(("[ok]", f"deploy automation exists ({len(deploy)} file(s))"))
    else:
        items.append(("[gap]", "no deploy automation - environments cannot be promoted"))
    if ttl:
        items.append(("[ok]", f"TTL markers found ({len(ttl)} file(s))"))
    else:
        items.append(("[gap]", "no TTL markers - ephemeral environments will live forever"))
    if cleanup:
        items.append(("[ok]", f"cleanup automation found ({len(cleanup)} file(s))"))
    else:
        items.append(("[gap]", "no cleanup automation - orphaned environments accumulate cost"))
    if seed:
        items.append(("[ok]", f"seed automation found ({len(seed)} file(s))"))
    else:
        items.append(("[gap]", "no seed automation - non-production stages lack deterministic data"))

    ok_n = sum(1 for tag, _ in items if tag == "[ok]")
    print(f"\n## Lifecycle checklist ({ok_n}/{len(items)} satisfied)")
    for tag, msg in items:
        print(f"{tag} {msg}")

    gaps = [msg for tag, msg in items if tag == "[gap]"]
    print("\n## Gaps")
    if gaps:
        for g in gaps:
            print(f"- {g}")
    else:
        print("- none")

    print("\nInfo: this report informs; it never asserts correctness and always exits 0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
