#!/usr/bin/env python3
"""Scan source trees for color-only signaling: ANSI red/green or chalk.red/green with no adjacent text marker. Stdlib only."""
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

# Color-only tokens: ANSI SGR escapes restricted to red (31/91) and green
# (32/92), written as a raw ESC byte or as a source literal (\x1b, \033, \e,
# or the u001b form), plus chalk.red/green calls.
ANSI_ESC_RE = re.compile(r"(?:\x1b|\\(?:x1b|033|e|u001[bB]))\[([0-9;]*)m")
CHALK_COLOR_RE = re.compile(r"chalk\.(?:bg)?(?:red|green)(?:Bright)?\b")

# Text markers that make color redundant rather than the only channel: severity
# words and terminal state words. Search runs after comment stripping.
MARKER_WORDS = [
    "error", "warn", "warning", "fail", "failed", "failure", "fatal",
    "success", "succeeded", "ok", "pass", "passed", "denied", "rejected",
    "invalid", "missing", "not found", "aborted", "cancelled", "canceled",
    "done", "complete", "completed", "created", "deleted", "removed",
    "installed", "started", "stopped", "updated",
]
MARKER_RE = re.compile(r"\b(?:" + "|".join(MARKER_WORDS) + r")\b", re.IGNORECASE)

# Comments are stripped before the marker search so wording in a comment can
# neither suppress nor create a finding.
HASH_COMMENT_RE = re.compile(r"(?:^|\s)#[^\n]*$")
SLASH_COMMENT_RE = re.compile(r"(?:^|\s)//[^\n]*$")
BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/")
HASH_EXTS = {".py", ".pyw", ".rb", ".rake", ".sh", ".bash", ".zsh"}
SLASH_EXTS = {".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".kt",
              ".kts", ".c", ".cc", ".cpp", ".h", ".hpp", ".swift"}
SOURCE_EXTS = HASH_EXTS | SLASH_EXTS


def _strip_comments(line, suffix):
    if suffix in HASH_EXTS:
        line = HASH_COMMENT_RE.sub("", line)
    if suffix in SLASH_EXTS:
        line = SLASH_COMMENT_RE.sub("", line)
        line = BLOCK_COMMENT_RE.sub("", line)
    return line


def _color_tokens(code):
    """Yield (kind, snippet) for each color-only-capable token in a line."""
    for m in CHALK_COLOR_RE.finditer(code):
        yield ("chalk", m.group(0))
    for m in ANSI_ESC_RE.finditer(code):
        codes = {int(c) for c in m.group(1).split(";") if c.strip()}
        if codes & {31, 91}:
            yield ("ansi-red", m.group(0).strip()[:MAX_LINE])
        elif codes & {32, 92}:
            yield ("ansi-green", m.group(0).strip()[:MAX_LINE])


def is_text_file(path):
    try:
        with path.open("rb") as fh:
            head = fh.read(8192)
    except OSError:
        return False
    return b"\x00" not in head


def iter_sources(root):
    """Yield source files under a directory root."""
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for name in sorted(files):
            p = Path(current) / name
            if p.suffix in SOURCE_EXTS:
                yield p


def scan(root):
    """Return (files_scanned, findings) where findings are (path, lineno, kind)."""
    findings = []
    scanned = 0
    for p in iter_sources(root):
        if not is_text_file(p) or p.stat().st_size > MAX_FILE_BYTES:
            continue
        scanned += 1
        try:
            lines = p.read_text(errors="ignore").splitlines()
        except OSError:
            continue
        for lineno, raw in enumerate(lines, 1):
            code = _strip_comments(raw, p.suffix)
            for kind, snippet in _color_tokens(code):
                if MARKER_RE.search(code):
                    continue
                if len(snippet) > MAX_LINE:
                    snippet = snippet[:MAX_LINE] + "..."
                findings.append((str(p), lineno, kind, snippet))
    return scanned, findings


def main():
    ap = argparse.ArgumentParser(
        description="Find color-only signaling: ANSI red/green or chalk.red/green "
        "with no adjacent text marker such as ERROR/WARN/success. Exits 1 on findings.")
    ap.add_argument("root", nargs="?", default=".",
                    help="directory tree to scan (default: current directory)")
    ap.add_argument("--max-per-file", type=int, default=30,
                    help="cap of findings printed per file (default: 30)")
    a = ap.parse_args()

    root = Path(a.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    scanned, findings = scan(root)

    print("=== Color-only signaling scan ===")
    print(f"Source: {root}")
    print(f"Files scanned: {scanned}")
    print(f"Findings ({len(findings)}):")
    per_file = {}
    for path, lineno, kind, snippet in findings:
        per_file.setdefault(path, []).append((lineno, kind, snippet))
    for path in sorted(per_file):
        for lineno, kind, snippet in per_file[path][:a.max_per_file]:
            label = "chalk color call" if kind == "chalk" else f"ANSI {kind} escape"
            print(f"  [COLOR_ONLY] {path}:{lineno}: {label} with no adjacent text marker ({snippet})")
        if len(per_file[path]) > a.max_per_file:
            print(f"  {path}: ... truncated at {a.max_per_file} findings")

    if findings:
        print(f"RESULT: FAIL — {len(findings)} color-only finding(s). Color must pair with a text marker.")
        raise SystemExit(1)
    print("RESULT: PASS — no color-only signaling found.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
