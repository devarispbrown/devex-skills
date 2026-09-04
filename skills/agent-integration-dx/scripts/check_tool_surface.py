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
BOUNDARY_RE = re.compile(
    r"\b(?:instead|rather than|do not use|don't use|use .{0,40}? when|not for"
    r"|prefer .{0,40}? when|if you need|for .{0,40}? use|that is |see )\b",
    re.IGNORECASE)


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
    if isinstance(data, dict):
        data = data.get('tools', data.get('result', {}).get('tools') if
                        isinstance(data.get('result'), dict) else None)
    if not isinstance(data, list):
        raise SystemExit(f'{path}: expected a list of tools, or an object with a "tools" key.')
    return [t for t in data if isinstance(t, dict)]


def common_prefix(names):
    """The namespace every tool shares, if there is one.

    A surface like git_status, git_diff, git_commit is namespaced on git. Treating that
    shared token as the verb makes every tool a synonym of every other, which is how a
    first version produced a boundary candidate on 12 of 12 tools in the reference git
    server. The namespace is not the verb.
    """
    heads = [re.split(r'[_\-.]', n.strip().lower())[0] for n in names if n]
    return heads[0] if heads and len(set(heads)) == 1 and len(heads) > 1 else None


def verb(name, namespace=None):
    parts = [x for x in re.split(r'[_\-.]', name.strip().lower()) if x]
    if namespace and parts and parts[0] == namespace:
        parts = parts[1:]
    return parts[0] if parts else ''


def main():
    ap = argparse.ArgumentParser(
        description='Inventory a tool surface and report selection-risk candidates.')
    ap.add_argument('tools', help='tool definition JSON')
    ap.add_argument('--strict', action='store_true',
                    help='exit 1 when candidates are emitted (default: also exit 1)')
    a = ap.parse_args()
    tools = read_tools(a.tools)
    if not tools:
        print('No tools found.')
        raise SystemExit(0)

    names = [str(t.get('name', '')) for t in tools]
    ns = common_prefix(names)
    descs = {n: str(t.get('description', '') or '') for n, t in zip(names, tools)}
    candidates = []
    for n in sorted({x for x in names if names.count(x) > 1}):
        candidates.append(f'candidate: {n} is defined more than once in this surface')

    # Confusability is a property of pairs, which this skill's own reference says. A tool
    # with no near-sibling needs no boundary statement, and flagging one produces a
    # candidate on every tool in a surface. Run against the reference git server it fired
    # on 12 of 12 tools, which is noise rather than signal.
    def near_siblings(n):
        return [m for m in names if m != n and (
            (verb(m, ns) and verb(m, ns) == verb(n, ns))
            or difflib.SequenceMatcher(None, n.lower(), m.lower()).ratio() >= 0.7)]

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
    for i, x in enumerate(names):
        for y in names[i + 1:]:
            if x == y:
                continue
            r = difflib.SequenceMatcher(None, x.lower(), y.lower()).ratio()
            if r >= 0.8:
                candidates.append(f'candidate: {x} and {y} are lexically close; '
                                  'review whether the descriptions separate them by intent')

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
