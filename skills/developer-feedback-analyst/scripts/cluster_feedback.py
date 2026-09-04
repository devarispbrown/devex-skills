#!/usr/bin/env python3
"""Cluster JSONL feedback signals by shared significant tokens. Stdlib only."""
import argparse
import json
import re
from collections import Counter
from pathlib import Path


def _read_input(path, what):
    """Read a required input file, or explain why it could not be read.

    The suite's own error-experience standard requires an expected error to say what
    happened, why, where, and how to fix it. A raw traceback answers none of those.
    """
    from pathlib import Path as _P
    p = _P(path)
    if p.is_dir():
        raise SystemExit(f'{path} is a directory, but {what} is expected to be a file.\n'
                         f'Pass the path to the file itself.')
    try:
        return p.read_text(encoding='utf-8', errors='replace')
    except FileNotFoundError:
        raise SystemExit(f'No such file: {path}\nExpected {what}.')
    except OSError as e:
        raise SystemExit(f'Cannot read {path}: {e}\nExpected {what}.')


def _read_json(path, what):
    import json as _j
    text = _read_input(path, what)
    try:
        return _j.loads(text)
    except _j.JSONDecodeError as e:
        raise SystemExit(f'{path} is not valid JSON: {e}\nExpected {what}.')

STOPWORDS = {
    "the", "and", "for", "with", "from", "this", "that", "these", "those",
    "your", "you", "are", "was", "were", "been", "not", "but", "can", "get",
    "got", "its", "all", "any", "out", "off", "one", "two", "new", "what",
    "when", "why", "how", "has", "have", "had", "will", "would", "could",
    "should", "into", "over", "about", "after", "before", "they", "them",
    "their", "there", "here", "then", "than", "etc", "also", "just", "like",
    "really", "very", "more", "most", "some", "such", "only", "other",
    "which", "while", "where", "who", "whom", "does", "did", "being",
}

CAMEL_RE = re.compile(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[0-9]+")


def stem(tok):
    if len(tok) > 6 and tok.endswith("ies"):
        return tok[:-3] + "y"
    if len(tok) > 5 and tok.endswith("ing"):
        return tok[:-3]
    if len(tok) > 4 and tok.endswith("ed"):
        return tok[:-2]
    if len(tok) > 4 and tok.endswith("es"):
        return tok[:-2]
    if len(tok) > 3 and tok.endswith("s"):
        return tok[:-1]
    return tok


def tokens(text):
    words = set()
    for part in re.split(r"[^A-Za-z0-9]+", text.lower()):
        for piece in CAMEL_RE.findall(part):
            piece = stem(piece.lower())
            if len(piece) >= 3 and piece not in STOPWORDS:
                words.add(piece)
    return words


def main():
    ap = argparse.ArgumentParser(
        description="Cluster JSONL feedback signals by shared significant tokens and print clusters ranked by size.",
        epilog="Informational only: the script proposes clusters; a human confirms names, causes, and impact.",
    )
    default_input = str(Path(__file__).resolve().parent.parent / "assets" / "feedback-sample.jsonl")
    ap.add_argument("input", nargs="?", default=default_input,
                    help="JSONL of feedback items (default: %(default)s)")
    ap.add_argument("--min-shared", type=int, default=2,
                    help="minimum shared significant tokens to join a cluster (default: 2)")
    ap.add_argument("--max-df", type=float, default=0.5,
                    help="drop tokens appearing in more than this fraction of items (default: 0.5)")
    ap.add_argument("--reps", type=int, default=3,
                    help="representative items printed per cluster (default: 3)")
    a = ap.parse_args()

    path = Path(a.input)
    if not path.exists():
        raise SystemExit(f"input not found: {path}")
    items = []
    for lineno, line in enumerate(_read_input(path, 'a feedback corpus').splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}")

    n = len(items)
    if n == 0:
        print("No signals found.")
        raise SystemExit(0)

    raw = [tokens(item.get("text", "")) for item in items]
    df = Counter(tok for doc in raw for tok in doc)
    common = {tok for tok, count in df.items() if count / n > a.max_df}
    sigs = [{tok for tok in doc if tok not in common} for doc in raw]

    clusters = []
    for idx, sig in enumerate(sigs):
        best, best_score = None, 0
        for ci, cl in enumerate(clusters):
            score = len(sig & cl["tokens"])
            if score > best_score:
                best, best_score = ci, score
        if best is not None and best_score >= a.min_shared:
            cl = clusters[best]
            cl["items"].append(idx)
            cl["tokens"] |= sig
        else:
            clusters.append({"items": [idx], "tokens": set(sig)})

    clusters.sort(key=lambda cl: len(cl["items"]), reverse=True)
    singletons = sum(1 for cl in clusters if len(cl["items"]) == 1)

    print(f"Feedback clusters: {n} signals, {len(clusters)} clusters ({singletons} singletons)")
    for rank, cl in enumerate(clusters, 1):
        idxs = cl["items"]
        size = len(idxs)
        tag = " (singleton)" if size == 1 else ""
        tally = Counter(tok for i in idxs for tok in sigs[i])
        stages = Counter(str(items[i].get("journey_stage", "?")) for i in idxs)
        modes = Counter(str(items[i].get("failure_mode", "?")) for i in idxs)
        print(f"\nCluster {rank} — {size} signal{'s' if size != 1 else ''}{tag}")
        print(f"  stages: {dict(stages)}  modes: {dict(modes)}")
        print(f"  shared tokens: {', '.join(t for t, _ in tally.most_common(8))}")
        print("  representative items:")
        for i in idxs[: a.reps]:
            item = items[i]
            src = str(item.get("source", "?"))
            surf = str(item.get("surface", "?"))
            text = str(item.get("text", ""))
            text = text if len(text) <= 110 else text[:107] + "..."
            print(f"    [{src:<11}] {surf:<8} {text}")
        if size > a.reps:
            print(f"    (+{size - a.reps} more)")
    print(f"\n{len(clusters)} clusters from {n} signals. Informational only: confirm names, causes, and impact.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
