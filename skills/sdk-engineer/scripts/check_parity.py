#!/usr/bin/env python3
"""Check SDK operation coverage against an OpenAPI JSON spec. Stdlib only.

Reads an OpenAPI document (JSON only; stdlib has no YAML parser — convert
YAML with your own tooling first, e.g. `npx @redocly/cli bundle --ext json`)
and greps an SDK source tree for each operation under per-language idiomatic
method names (Go `ListWidgets`, Python/Rust `list_widgets`, TS `listWidgets`).

Output: MISSING operations (confirmed absent — exit code 1) and UNCERTAIN
operations (spec name or path found but not the idiomatic name — candidates
for review, not failures). Test against the fixture spec and clients in
assets/sdk-example/.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HTTP_METHODS = ("get", "post", "put", "patch", "delete", "options", "head", "trace")

EXTENSIONS = {
    "go": {".go"},
    "python": {".py"},
    "ts": {".ts", ".tsx"},
    "rust": {".rs"},
}

IGNORED_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "__pycache__",
    ".venv", "venv", "env", "target", "dist", "build", ".tox", ".mypy_cache",
}


def to_snake(name):
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


def to_title(name):
    return "".join(p[:1].upper() + p[1:] for p in to_snake(name).split("_") if p)


def to_camel(name):
    parts = [p for p in to_snake(name).split("_") if p]
    if not parts:
        return name
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def expected_name(operation_id, lang):
    if lang == "go":
        return to_title(operation_id)
    if lang in ("python", "rust"):
        return to_snake(operation_id)
    return to_camel(operation_id)  # ts


def derive_operation_id(method, path):
    segs = [s for s in path.split("/") if s and not s.startswith("{")]
    base = to_camel(segs[-1]) if segs else "resource"
    return f"{method}_{base}"


def load_operations(spec_path):
    try:
        spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"spec not found: {spec_path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"invalid JSON in {spec_path}: {e}")
    paths = spec.get("paths")
    if not isinstance(paths, dict) or not paths:
        raise SystemExit(f"no 'paths' object in {spec_path}; is this an OpenAPI document?")
    ops = []
    for path, item in paths.items():
        if not isinstance(item, dict):
            continue
        for method in HTTP_METHODS:
            op = item.get(method)
            if not isinstance(op, dict):
                continue
            op_id = op.get("operationId")
            derived = not op_id
            if not op_id:
                op_id = derive_operation_id(method, path)
            ops.append({"path": path, "method": method.upper(),
                        "operation_id": op_id, "derived": derived})
    if not ops:
        raise SystemExit(f"no operations found in {spec_path}")
    return ops


def source_files(sdk_dir, lang):
    root = Path(sdk_dir)
    if not root.is_dir():
        raise SystemExit(f"SDK directory not found: {sdk_dir}")
    exts = EXTENSIONS[lang]
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in exts and not any(
                part in IGNORED_DIRS for part in p.parts):
            yield p


def contains(files, name):
    pat = re.compile(r"\b" + re.escape(name) + r"\b")
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if pat.search(text):
            return True
    return False


def main():
    ap = argparse.ArgumentParser(
        description="Check SDK operation coverage against an OpenAPI JSON spec.")
    ap.add_argument("spec", help="path to the OpenAPI document (JSON only)")
    ap.add_argument("sdk_dir", help="path to the SDK source tree to check")
    ap.add_argument("--lang", required=True, choices=sorted(EXTENSIONS),
                    help="target language naming convention")
    ap.add_argument("--verbose", action="store_true",
                    help="also list operations that are present")
    a = ap.parse_args()

    ops = load_operations(a.spec)
    files = list(source_files(a.sdk_dir, a.lang))
    if not files:
        raise SystemExit(f"no {a.lang} source files found under {a.sdk_dir}")

    missing, uncertain, present = [], [], []
    for op in ops:
        op_id = op["operation_id"]
        idiomatic = expected_name(op_id, a.lang)
        if op["derived"]:
            # Name is a guess, not a fact: always a review candidate.
            uncertain.append((op, "operationId missing from spec; name derived"))
        elif contains(files, idiomatic):
            present.append(op)
        elif op_id != idiomatic and contains(files, op_id):
            uncertain.append((op, f"raw operationId {op_id!r} found; "
                                  f"expected idiomatic name {idiomatic!r}"))
        else:
            missing.append(op)

    print(f"Parity check: spec={a.spec} sdk={a.sdk_dir} lang={a.lang}")
    for op in missing:
        print(f"MISSING   {op['operation_id']:24} expected "
              f"{expected_name(op['operation_id'], a.lang)!r:24} "
              f"{op['method']} {op['path']}")
    for op, why in uncertain:
        print(f"UNCERTAIN {op['operation_id']:24} expected "
              f"{expected_name(op['operation_id'], a.lang)!r:24} "
              f"{op['method']} {op['path']} — candidate for review: {why}")
    if a.verbose:
        for op in present:
            print(f"PRESENT   {op['operation_id']:24} "
                  f"{expected_name(op['operation_id'], a.lang)!r:24} "
                  f"{op['method']} {op['path']}")
    n = len(ops)
    print(f"Summary: {n} operations — {len(present)} present, "
          f"{len(uncertain)} uncertain, {len(missing)} missing")
    raise SystemExit(1 if missing else 0)


if __name__ == "__main__":
    main()
