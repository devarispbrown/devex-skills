#!/usr/bin/env python3
"""Scan a tree for copy-paste pattern signals that indicate scaffoldable workflows. Stdlib only."""
import argparse
import difflib
import re
from collections import defaultdict
from pathlib import Path

EXCLUDE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv",
    ".tox", ".mypy_cache", ".pytest_cache", ".ruff_cache", "dist", "build",
}
DOC_EXTS = {".md", ".rst", ".txt", ".adoc", ".markdown"}
MAX_READ_BYTES = 1 << 20  # skip files larger than 1 MiB
MAX_UNIT_FILES = 200      # skip directories with more files than this

FILL_MARKERS = [
    re.compile(r"TODO\s*:\s*fill", re.I),
    re.compile(r"\bFILL IN\b", re.I),
    re.compile(r"\bCHANGE_ME\b", re.I),
    re.compile(r"\bREPLACE(?:\s+ME|_ME)?\b", re.I),
    re.compile(r"\bYOUR_[A-Z0-9_]+", re.I),
    re.compile(r"INSERT\s+[A-Z ]+\s+HERE", re.I),
]
WEAK_MARKER = re.compile(r"\b(?:TODO|FIXME|XXX)\b")


def split_tokens(name):
    return [t for t in re.split(r"[-_.]", name) if t]


def token_distance(a, b):
    """Return the indices where two token lists differ, or None if they differ
    in more than one position or not at all (names must be near-identical)."""
    if len(a) != len(b) or a == b:
        return None
    diffs = [i for i in range(len(a)) if a[i] != b[i]]
    return diffs if len(diffs) == 1 else None


def norm_lines(text):
    return [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines() if ln.strip()]


def read_text(path):
    try:
        if path.stat().st_size > MAX_READ_BYTES:
            return None
        return path.read_text(errors="replace")
    except OSError:
        return None


def similarity(a, b):
    la, lb = norm_lines(a), norm_lines(b)
    if not la and not lb:
        return 1.0
    return difflib.SequenceMatcher(None, la, lb).ratio()


def iter_files(root, exclude):
    for path in sorted(root.rglob("*")):
        if path.is_file() and not any(part in exclude for part in path.parts):
            yield path


def find_families(root, exclude, min_sim, min_members):
    """Cluster sibling directories whose names differ by one token and whose
    file sets are structurally and content-similar."""
    files_under = defaultdict(list)
    for f in iter_files(root, exclude):
        for d in [f.parent] + list(f.parents):
            files_under[d].append(f)
    units = {
        d: {str(f.relative_to(d)): f for f in fs}
        for d, fs in files_under.items()
        if len(fs) <= MAX_UNIT_FILES
    }
    units.pop(root, None)
    by_parent = defaultdict(list)
    for d in units:
        by_parent[d.parent].append(d)
    pairs = []
    for siblings in by_parent.values():
        for i in range(len(siblings)):
            for j in range(i + 1, len(siblings)):
                si, sj = units[siblings[i]], units[siblings[j]]
                if token_distance(split_tokens(siblings[i].name), split_tokens(siblings[j].name)) is None:
                    continue
                shared = []
                for rel in sorted(set(si) & set(sj)):
                    ti, tj = read_text(si[rel]), read_text(sj[rel])
                    if ti is None or tj is None:
                        continue
                    ratio = similarity(ti, tj)
                    if ratio >= min_sim:
                        shared.append((rel, ratio))
                union = len(set(si) | set(sj))
                if union and len(shared) >= 2 and len(set(si) & set(sj)) / union >= 0.5:
                    pairs.append((siblings[i], siblings[j], shared))
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for a, b, _ in pairs:
        union(a, b)
    families = defaultdict(list)
    for a, b, shared in pairs:
        families[find(a)].append((a, b, shared))
    result = []
    for members in families.values():
        dirs = sorted({d for pair in members for d in pair[:2]})
        per_file = {}
        for _, _, shared in members:
            for rel, ratio in shared:
                per_file.setdefault(rel, []).append(ratio)
        result.append({
            "dirs": dirs,
            "pairs": len(members),
            "shared_files": {rel: sum(rs) / len(rs) for rel, rs in per_file.items()},
        })
    return [r for r in result if len(r["dirs"]) >= min_members]


def find_boilerplate(root, exclude):
    """Full-file duplicates and repeated file-header blocks across directories."""
    by_sig, by_head = defaultdict(list), defaultdict(list)
    for f in iter_files(root, exclude):
        text = read_text(f)
        if text is None:
            continue
        lines = norm_lines(text)
        if len(lines) >= 5:
            by_sig["\n".join(lines)].append(f)
        if lines:
            by_head["\n".join(lines[:10])].append(f)
    full = [fs for fs in by_sig.values() if len(fs) >= 2]
    heads = [fs for fs in by_head.values() if len(fs) >= 2 and len({f.parent for f in fs}) >= 2]
    return full, heads


def find_doc_markers(root, exclude):
    """Count fill-in markers in docs, grouped by containing directory."""
    hits = defaultdict(list)
    for f in iter_files(root, exclude):
        if f.suffix.lower() not in DOC_EXTS:
            continue
        text = read_text(f)
        if text is None:
            continue
        strong = sum(len(m.findall(text)) for m in FILL_MARKERS)
        weak = len(WEAK_MARKER.findall(text))
        if strong:
            hits[f.parent].append((f, strong, weak))
    return hits


def format_paths(files, limit=4):
    names = ", ".join(str(f) for f in files[:limit])
    return names + ("..." if len(files) > limit else "")


def main():
    ap = argparse.ArgumentParser(
        description="Scan a tree for copy-paste pattern signals that indicate scaffoldable workflows."
    )
    ap.add_argument("root", nargs="?", default=".",
                    help="directory tree to scan (default: current directory)")
    ap.add_argument("--exclude", action="append", default=[],
                    help="additional directory names to skip (repeatable)")
    ap.add_argument("--min-similarity", type=float, default=0.75,
                    help="near-identical content threshold (default: 0.75)")
    ap.add_argument("--min-members", type=int, default=2,
                    help="minimum members for a candidate family (default: 2)")
    a = ap.parse_args()
    root = Path(a.root)
    if not root.is_dir():
        raise SystemExit(f"error: not a directory: {a.root}")
    exclude = EXCLUDE_DIRS | set(a.exclude)

    families = find_families(root, exclude, a.min_similarity, a.min_members)
    full_clusters, head_clusters = find_boilerplate(root, exclude)
    doc_hits = find_doc_markers(root, exclude)

    print(f"Scaffold candidate scan: {root}")
    print(f"Excluded directory names: {', '.join(sorted(exclude)) or '(none)'}\n")
    candidates = []

    if families:
        print("Near-identical directory structures:")
        for fam in sorted(families, key=lambda r: (-len(r["dirs"]), -len(r["shared_files"]))):
            names = ", ".join(sorted(d.name for d in fam["dirs"]))
            avg = sum(fam["shared_files"].values()) / len(fam["shared_files"])
            print(f"  {names}  ({len(fam['dirs'])} members, {len(fam['shared_files'])} shared files, avg similarity {avg:.2f})")
            for rel, ratio in sorted(fam["shared_files"].items()):
                print(f"      {rel}  ({ratio:.2f})")
            candidates.append((len(fam["dirs"]) * (len(fam["shared_files"]) + 1),
                               f"family {names}"))
        print()

    if full_clusters:
        print("Identical full-file boilerplate:")
        for fs in sorted(full_clusters, key=len, reverse=True):
            print(f"  {len(fs)} identical files: {format_paths(fs)}")
            candidates.append((len(fs), f"{len(fs)} identical boilerplate files"))
        print()

    if head_clusters:
        print("Identical file-header blocks (first 10 lines):")
        for fs in sorted(head_clusters, key=len, reverse=True):
            print(f"  {len(fs)} files share a header: {format_paths(fs)}")
            candidates.append((len(fs), f"{len(fs)} files sharing a header block"))
        print()

    if doc_hits:
        print("Docs with fill-in markers (strong / weak):")
        for parent in sorted(doc_hits, key=lambda p: -sum(s for _, s, _ in doc_hits[p])):
            files = doc_hits[parent]
            total_strong = sum(s for _, s, _ in files)
            total_weak = sum(w for _, _, w in files)
            print(f"  {parent}: {len(files)} files, {total_strong} strong / {total_weak} weak markers")
            for f, s, w in sorted(files, key=lambda t: -t[1]):
                print(f"      {f.name}  ({s} strong, {w} weak)")
            candidates.append((total_strong, f"fill-in markers under {parent}"))
        print()

    print("Ranked scaffold candidates:")
    if candidates:
        for rank, (score, label) in enumerate(sorted(candidates, key=lambda c: -c[0]), 1):
            print(f"  {rank}. [score {score}] {label}")
    else:
        print("  None detected in this tree.")
    print("\nThis scan informs only; confirm every candidate with PR history, onboarding friction, and support questions.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
