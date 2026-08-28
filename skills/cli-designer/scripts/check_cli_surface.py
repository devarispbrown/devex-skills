#!/usr/bin/env python3
"""Static CLI surface scanner: catalog commands and flags, flag suspicious patterns. Stdlib only."""
import argparse
import json
import os
import re
from pathlib import Path

DESTRUCTIVE_RE = re.compile(r"\b(delete|remove|rm|drop|destroy|purge|wipe|reset|clear)\b", re.I)
FLAG_RE = re.compile(r"(?<![\w-])--([a-z][a-z0-9-]*)\b")
SAFETY_FLAGS = {"force", "yes", "y", "confirm", "assume-yes", "no-input", "no-confirm"}
SOURCE_CMD_RES = [
    re.compile(r"""add_parser\(\s*["']([a-z][a-z0-9_-]*)["']"""),
    re.compile(r"""\.command\(\s*["']([a-z][a-z0-9_-]*)["']"""),
    re.compile(r"""Use:\s*["']([a-z][a-z0-9_-]*)["']"""),
]
EXIT_ANOMALY_RE = re.compile(r"(?:sys\.exit|exit|SystemExit)\(\s*-1\s*\)|os\._exit\(")
SOURCE_EXTS = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".rb", ".java", ".sh", ".bash", ".zsh", ".ps1"}
HELP_EXTS = {".txt", ".md", ".rst"}
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__", "venv", ".venv", "dist", "build", "target", ".tox"}
COMMAND_HEADER_RE = re.compile(r"^(?:sub?)?commands?:?\s*$", re.I)
HELP_COMMAND_RE = re.compile(r"^([a-z][a-z0-9_-]*)\s+\S")


def catalog_from_help(text):
    """Parse commands and long flags out of --help text. Returns (commands, flags)."""
    commands = set()
    flags = set()
    in_cmds = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if COMMAND_HEADER_RE.match(stripped):
            in_cmds = True
            continue
        if in_cmds:
            m = HELP_COMMAND_RE.match(stripped)
            if m:
                commands.add(m.group(1))
                continue
            if stripped and not stripped.startswith(("-", "(", ")")):
                in_cmds = False
        flags.update(FLAG_RE.findall(line))
    return commands, flags


def catalog_from_source(root):
    """Walk a tree and catalog commands, flags, and exit-code anomalies."""
    commands = set()
    flags = set()
    anomalies = []
    for path in _iter_files(root):
        if path.suffix in SOURCE_EXTS:
            _scan_source(path, commands, flags, anomalies)
        elif path.suffix in HELP_EXTS:
            try:
                c, f = catalog_from_help(path.read_text(errors="replace"))
            except OSError:
                continue
            commands |= c
            flags |= f
    return commands, flags, anomalies


def _scan_source(path, commands, flags, anomalies):
    try:
        lines = path.read_text(errors="replace").splitlines()
    except OSError:
        return
    for lineno, line in enumerate(lines, 1):
        for rx in SOURCE_CMD_RES:
            for m in rx.finditer(line):
                commands.add(m.group(1))
        flags.update(FLAG_RE.findall(line))
        for m in EXIT_ANOMALY_RE.finditer(line):
            anomalies.append((str(path), lineno, m.group(0).strip()))


def _iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            p = Path(dirpath) / name
            if p.suffix in SOURCE_EXTS or p.suffix in HELP_EXTS:
                yield p


def main():
    ap = argparse.ArgumentParser(
        description="Catalog a CLI's commands and flags and flag suspicious patterns. "
        "Informational only: always exits 0, never gates."
    )
    ap.add_argument("tree", nargs="?", help="directory tree to scan")
    ap.add_argument("--helpfile", metavar="FILE", help="captured --help text file to scan instead of a tree")
    ap.add_argument("--json", action="store_true", help="emit the catalog and findings as JSON")
    a = ap.parse_args()
    if a.helpfile is not None:
        source = a.helpfile
        text = Path(a.helpfile).read_text(errors="replace")
        commands, flags = catalog_from_help(text)
        anomalies = []
    else:
        if a.tree is None:
            raise SystemExit("a tree path or --helpfile is required")
        root = Path(a.tree)
        if not root.is_dir():
            raise SystemExit(f"not a directory: {a.tree}")
        source = str(root)
        commands, flags, anomalies = catalog_from_source(root)
        text = ""
    findings = []
    if "json" not in flags:
        note = ""
        if "--format" in flags and re.search(r"--format[^\n]*json", text):
            note = " (a --format flag accepts 'json'; a dedicated --json is still the contract)"
        findings.append(("MISSING_JSON", f"no --json flag; machine consumers cannot request stable JSON output{note}"))
    for cmd in sorted(commands):
        if DESTRUCTIVE_RE.search(cmd) and not (SAFETY_FLAGS & flags):
            findings.append(("DESTRUCTIVE_NO_FORCE", f"'{cmd}' is destructive but no --force/--yes/--confirm flag exists"))
    for path, lineno, snippet in anomalies:
        findings.append(("EXIT_CODE_ANOMALY", f"{path}:{lineno}: {snippet}"))
    if a.json:
        payload = {
            "source": source,
            "commands": sorted(commands),
            "flags": sorted(flags),
            "findings": [{"id": fid, "message": msg} for fid, msg in findings],
        }
        print(json.dumps(payload, indent=2))
    else:
        print("=== CLI surface catalog ===")
        print(f"Source: {source}")
        print(f"Commands ({len(commands)}): {', '.join(sorted(commands)) or '(none found)'}")
        print(f"Flags ({len(flags)}): {', '.join('--' + f for f in sorted(flags)) or '(none found)'}")
        print(f"Findings ({len(findings)}):")
        for fid, msg in findings:
            print(f"  [{fid}] {msg}")
        print("Informational scan only; exits 0 regardless of findings.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
