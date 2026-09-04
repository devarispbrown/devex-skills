#!/usr/bin/env python3
"""Inventory a tool surface and report selection-risk candidates. Stdlib only.

Candidates only, never verdicts. Lexical similarity does not measure selection error:
create_user and create_org are near-identical and never confused, while send and dispatch
are distant and confused constantly. Only a human reading intent can decide a pair, so
this reports what to look at and refuses to rate the surface.

Reads a tool definition file: an MCP tools/list response, an array of tool objects, or an
object whose "tools" key holds them.
"""
import argparse, difflib, json, re, sys
from pathlib import Path

# Verbs that mean the same thing to a caller. A surface using more than one of a group
# teaches the model a distinction that does not exist.
SYNONYM_GROUPS = [
    {"get", "fetch", "read", "retrieve", "load", "show"},
    {"list", "search", "find", "query", "lookup"},
    {"create", "add", "new", "make", "insert"},
    {"update", "edit", "modify", "change", "set"},
    {"delete", "remove", "destroy", "drop", "purge"},
    {"send", "dispatch", "post", "publish", "emit"},
]
# A boundary is any phrasing that tells the caller when to pick something else. The
# trailing "... instead" form is common and was missed by a first pass keyed on
# "instead of", which produced a false candidate against a description that did state
# its boundary.
# A boundary names a sibling. "See the API docs" is a cross-reference, which is the fix
# selection-review.md explicitly forbids, and an earlier version accepted it as a boundary.
BOUNDARY_RE = re.compile(
    r"\b(?:instead|rather than|do not use|don't use|not for"
    r"|use .{0,60}? (?:when|for)|prefer .{0,60}? when|if you (?:need|want))\b",
    re.IGNORECASE)
TOOL_TOKEN_RE = re.compile(r"\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b")
# SEP-986 is cited as normative in references/upstream-specs.md. This is its one
# machine-checkable rule, and it was cited without being enforced.
NAME_RE = re.compile(r"^[A-Za-z0-9_-]{1,128}$")


def read_tools(path):
    p = Path(path)
    if p.is_dir():
        raise SystemExit(f'{path} is a directory, but a tool definition file is expected.\n'
                         'Pass the path to the file itself.')
    try:
        data = json.loads(p.read_text(encoding='utf-8', errors='replace'))
    except FileNotFoundError:
        raise SystemExit(f'No such file: {path}')
    except json.JSONDecodeError as e:
        raise SystemExit(f'{path} is not valid JSON: {e}')
    except OSError as e:
        raise SystemExit(f'Cannot read {path}: {e}')
    if isinstance(data, dict):
        data = data.get('tools', data.get('result', {}).get('tools') if
                        isinstance(data.get('result'), dict) else None)
    if not isinstance(data, list):
        raise SystemExit(f'{path}: expected a list of tools, or an object with a "tools" key.')
    return [t for t in data if isinstance(t, dict)]


def namespaces(names):
    """First tokens shared by two or more tools, which are namespaces rather than verbs.

    Requiring every tool to share one prefix made the check non-monotonic: adding a single
    unnamespaced tool to a namespaced surface turned every finding off. Multi-product
    servers, which is the shape this skill's own guidance recommends, were reported clean.
    """
    heads = {}
    for n in names:
        if not n:
            continue
        h = re.split(r'[_\-.]', str(n).strip().lower())[0]
        heads[h] = heads.get(h, 0) + 1
    return {h for h, c in heads.items() if c > 1}


def split_name(name, ns):
    """Return (verb, object) with any namespace prefix removed."""
    parts = [x for x in re.split(r'[_\-.]', str(name).strip().lower()) if x]
    if parts and parts[0] in ns:
        parts = parts[1:]
    if not parts:
        return '', ''
    return parts[0], '_'.join(parts[1:])


def verb(name, ns=frozenset()):
    return split_name(name, ns)[0]


def synonymous(v1, v2):
    if not v1 or not v2:
        return False
    if v1 == v2:
        return True
    return any(v1 in g and v2 in g for g in SYNONYM_GROUPS)


def main():
    ap = argparse.ArgumentParser(
        description='Inventory a tool surface and report selection-risk candidates.')
    ap.add_argument('tools', help='tool definition JSON')
    a = ap.parse_args()
    tools = read_tools(a.tools)
    if not tools:
        print('No tools found.')
        raise SystemExit(0)

    names = [str(t.get('name', '')) for t in tools]
    ns = namespaces(names)
    descs = {n: str(t.get('description', '') or '') for n, t in zip(names, tools)}
    candidates = []
    for n in sorted({x for x in names if names.count(x) > 1}):
        candidates.append(f'candidate: {n} is defined more than once in this surface')

    # Confusability is a property of pairs, which this skill's own reference says. A tool
    # with no near-sibling needs no boundary statement, and flagging one produces a
    # candidate on every tool in a surface. Run against the reference git server it fired
    # on 12 of 12 tools, which is noise rather than signal.
    def near_siblings(n):
        """Pairs that share an object and a verb meaning.

        String distance does not separate these: create_user and create_org score .762 and
        are never confused, while get_user and fetch_user score .778 and are confused
        constantly. The separator is the object, not the spelling. An earlier threshold of
        .7 flagged create_user against create_org, which is the pair this file's own
        docstring names as never confused.
        """
        v1, o1 = split_name(n, ns)
        out = []
        for m in names:
            if m == n:
                continue
            v2, o2 = split_name(m, ns)
            if not synonymous(v1, v2):
                continue
            # Objects are the same thing when one is absent (git_diff against
            # git_diff_staged), when one contains the other (staged against unstaged), or
            # when they are near-identical strings. They are different things when they
            # are unrelated nouns, which is what keeps create_user off create_org.
            related = (
                # A verb-only tool pairs with a qualified one only under the identical
                # verb. git_diff against git_diff_staged is one act at two scopes;
                # git_add against git_create_branch is two acts whose verbs happen to be
                # synonyms, and pairing those was a false positive on the real git server.
                ((not o1 or not o2) and v1 == v2)
                or o1 == o2
                or (bool(o1) and bool(o2) and (o1 in o2 or o2 in o1))
                or (bool(o1) and bool(o2)
                    and difflib.SequenceMatcher(None, o1, o2).ratio() >= 0.8))
            if related:
                out.append(m)
        return out

    for n in names:
        d = descs[n]
        if not d.strip():
            candidates.append(f'candidate: {n} has no description; selection is left to the name alone')
            continue
        sibs = near_siblings(n)
        if sibs and not BOUNDARY_RE.search(d):
            shown = ', '.join(sorted(sibs)[:3])
            candidates.append(f'candidate: {n} states no boundary against {shown}; '
                              'nothing says when to choose the sibling instead')
        if len(d) > 1024:
            candidates.append(f'candidate: {n} description is {len(d)} chars; it is read on every selection')

    # verb drift across the surface
    used = {}
    for n in names:
        v = verb(n, ns)
        for i, g in enumerate(SYNONYM_GROUPS):
            if v in g:
                used.setdefault(i, set()).add(v)
    for i, vs in used.items():
        if len(vs) > 1:
            candidates.append('candidate: surface uses ' + ', '.join(sorted(vs)) +
                              ' for the same concept; one verb per concept')

    # near-duplicate names, reported as pairs to review by intent
    seen_pairs = set()
    for x in names:
        for y in near_siblings(x):
            key = tuple(sorted((x, y)))
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            candidates.append(f'candidate: {key[0]} and {key[1]} act on the same object with '
                              'interchangeable verbs; review whether the descriptions '
                              'separate them by intent')

    # argument schema gaps
    for t in tools:
        n = t.get('name', '?')
        schema = t.get('inputSchema') or t.get('input_schema') or {}
        props = schema.get('properties') if isinstance(schema, dict) else None
        if not isinstance(props, dict):
            candidates.append(f'candidate: {n} declares no argument schema properties')
            continue
        for pname, spec in props.items():
            if not isinstance(spec, dict):
                continue
            if not spec.get('description'):
                candidates.append(f'candidate: {n}.{pname} has no description')
            if spec.get('type') == 'string' and 'enum' not in spec and \
                    re.search(r'\b(mode|kind|type|status|format|level)\b', pname, re.I):
                candidates.append(f'candidate: {n}.{pname} looks like a closed set but declares no enum')

    for n in names:
        if not NAME_RE.match(str(n)):
            candidates.append(f'candidate: {n!r} is not a valid tool name under the cited '
                              'naming rule (letters, digits, underscore, hyphen, 1-128 chars)')
    # A description that routes the model to a tool the surface does not expose is a
    # dead end, and it is decidable from the file alone.
    known = {str(n) for n in names}
    for n in names:
        for tok in TOOL_TOKEN_RE.findall(descs.get(n, '')):
            if tok not in known and any(tok.startswith(p) for p in ns):
                candidates.append(f'candidate: {n} names {tok}, which is not a tool on this '
                                  'surface')

    print(f'Tool surface: {a.tools}')
    print(f'{len(tools)} tool(s): {", ".join(sorted(names))}\n')
    for c in sorted(set(candidates)):
        print(c)
    print(f'\n{len(set(candidates))} candidate(s). Candidates only, never verdicts: lexical '
          'similarity does not\nmeasure selection error. Run the review in '
          'references/selection-review.md to decide each pair.')
    raise SystemExit(1 if candidates else 0)


if __name__ == '__main__':
    main()
