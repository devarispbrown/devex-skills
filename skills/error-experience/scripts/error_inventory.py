#!/usr/bin/env python3
"""Scan a tree for error/exception/exit sources and catalog them by surface for review. Stdlib only."""
import argparse
import os
import re
import sys
from pathlib import Path

IGNORE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", ".venv", "venv", "env",
    "dist", "build", "target", ".next", ".cache", "coverage", "__pycache__",
    ".terraform", ".idea", ".gradle", "Pods", "DerivedData",
}
MAX_FILE_BYTES = 1_000_000
MAX_LINE = 120

# Category -> regex per language family. Line matches only its language family's
# patterns, plus the shared HTTP-status literal check.
LANG_PATTERNS = {
    "python": [
        ("raise", re.compile(r"\braise\b")),
        ("SystemExit", re.compile(r"\bSystemExit\b")),
        ("exit", re.compile(r"\b(?:sys\.|os\._?)?exit\s*\(")),
        ("log.Error", re.compile(r"\blog(?:ger)?\.error\s*\(", re.IGNORECASE)),
    ],
    "go": [
        ("errors.New", re.compile(r"errors\.New\s*\(")),
        ("fmt.Errorf", re.compile(r"fmt\.Errorf\s*\(")),
        ("log.Error", re.compile(r"\blog\w*\.Error\s*\(")),
        ("exit", re.compile(r"\b(?:os\.)?Exit\s*\(")),
    ],
    "js": [
        ("throw", re.compile(r"\bthrow\b")),
        ("exit", re.compile(r"\b(?:process\.)?exit\s*\(")),
        ("log.Error", re.compile(r"\b(?:log|logger|console)\.error\s*\(", re.IGNORECASE)),
    ],
    "java": [
        ("throw", re.compile(r"\bthrow\b")),
        ("exit", re.compile(r"\bSystem\.exit\s*\(")),
        ("log.Error", re.compile(r"\b(?:log|logger)\.error\s*\(", re.IGNORECASE)),
    ],
    "ruby": [
        ("raise", re.compile(r"\braise\b")),
        ("exit", re.compile(r"\bexit\s*\(")),
        ("log.Error", re.compile(r"\b(?:log|logger)\.error\s*\(", re.IGNORECASE)),
    ],
    "rust": [
        ("exit", re.compile(r"\bexit\s*\(")),
        ("log.Error", re.compile(r"\b(?:log|tracing)::error\s*\(", re.IGNORECASE)),
    ],
    "shell": [
        ("exit", re.compile(r"\bexit\s+\d*")),
    ],
    "c": [
        ("exit", re.compile(r"\bexit\s*\(")),
    ],
}
LANG_BY_SUFFIX = {
    ".py": "python", ".pyw": "python",
    ".go": "go",
    ".js": "js", ".jsx": "js", ".mjs": "js", ".cjs": "js", ".ts": "js", ".tsx": "js",
    ".java": "java", ".kt": "java", ".kts": "java",
    ".rb": "ruby", ".rake": "ruby",
    ".rs": "rust",
    ".sh": "shell", ".bash": "shell", ".zsh": "shell",
    ".c": "c", ".cc": "c", ".cpp": "c", ".h": "c", ".hpp": "c",
}

# HTTP error status literals: a 4xx/5xx literal counts only when the line has
# status/HTTP context, to avoid noise from unrelated numbers.
HTTP_STATUS_RE = re.compile(r"\b(?:[45]\d\d)\b")
HTTP_CTX_RE = re.compile(
    r"\b(?:status|statuscode|status_code|http|httperror|http_error|response|"
    r"send_error|set_status|error_code|sc_)\w*\b",
    re.IGNORECASE,
)

# Surface guess from the relative path. First match wins.
SURFACE_RULES = [
    ("CLI", ("cli", "cmd", "console", "bin", "tool/", "scripts/")),
    ("SDK", ("sdk", "client", "clients")),
    ("API", ("api", "server", "http", "handler", "route", "endpoint", "controller", "rest")),
    ("Diagnostics", ("log", "trace", "telemetry", "observability", "metric", "diagnostic")),
]


def guess_surface(rel: str) -> str:
    low = rel.lower()
    for name, keywords in SURFACE_RULES:
        if any(k in low for k in keywords):
            return name
    return "Unclassified"


def is_text_file(path: Path) -> bool:
    try:
        with path.open("rb") as fh:
            head = fh.read(8192)
    except OSError:
        return False
    return b"\x00" not in head


def match_categories(line: str, lang: str):
    cats = []
    for name, rx in LANG_PATTERNS.get(lang, []):
        if rx.search(line):
            cats.append(name)
    if HTTP_STATUS_RE.search(line) and HTTP_CTX_RE.search(line):
        cats.append("http-status")
    return cats


def walk_files(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            p = Path(current) / f
            if p.stat().st_size <= MAX_FILE_BYTES:
                yield p


def main():
    ap = argparse.ArgumentParser(
        description="Catalog error/exception/exit sources by surface for manual review.")
    ap.add_argument("root", nargs="?", default=".",
                    help="directory tree to scan (default: current directory)")
    ap.add_argument("--max-per-file", type=int, default=30,
                    help="cap of catalog lines printed per file (default: 30)")
    ap.add_argument("--pattern", default=None,
                    help="only report categories containing this substring, e.g. 'raise'")
    a = ap.parse_args()

    root = Path(a.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    surfaces = {}
    scanned = 0
    total_matches = 0
    for p in walk_files(root):
        lang = LANG_BY_SUFFIX.get(p.suffix.lower())
        if lang is None:
            continue
        if not is_text_file(p):
            continue
        rel = p.relative_to(root).as_posix()
        surface = guess_surface(rel)
        entries = []
        try:
            lines = p.read_text(errors="ignore").splitlines()
        except OSError:
            continue
        scanned += 1
        for i, raw in enumerate(lines, 1):
            cats = match_categories(raw, lang)
            if a.pattern:
                cats = [c for c in cats if a.pattern in c]
            if not cats:
                continue
            snippet = raw.strip()
            if len(snippet) > MAX_LINE:
                snippet = snippet[:MAX_LINE] + "..."
            entries.append(f"{rel}:{i}: [{','.join(cats)}] {snippet}")
            if len(entries) >= a.max_per_file:
                entries.append(f"{rel}: ... truncated at {a.max_per_file} lines")
                break
        if entries:
            surfaces.setdefault(surface, []).extend(entries)
            total_matches += len(entries)

    print(f"Repository: {root}")
    print(f"Files scanned: {scanned}")
    for surface in sorted(surfaces):
        entries = surfaces[surface]
        print(f"\n## Surface: {surface} ({len(entries)} catalog lines)")
        for e in entries:
            print(e)
    print(f"\nCatalog: {total_matches} lines across {len(surfaces)} surfaces. Review only; exit 0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
