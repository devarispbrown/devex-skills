#!/usr/bin/env python3
"""Emit heuristic convention candidates for an OpenAPI 3 JSON spec: plural nouns, kebab-case segments, verbs in paths, and pagination naming consistency. Candidates only, never verdicts. JSON input only - convert YAML with your own tooling first. Stdlib only."""
import argparse, json, re
from pathlib import Path

HTTP_METHODS = {'get', 'put', 'post', 'delete', 'patch', 'head', 'options', 'trace'}
VERBS = {
    'add', 'cancel', 'create', 'deactivate', 'delete', 'disable', 'download', 'enable',
    'execute', 'export', 'generate', 'get', 'import', 'list', 'post', 'put', 'refresh',
    'remove', 'renew', 'reset', 'restore', 'resume', 'retry', 'revert', 'revoke',
    'run', 'search', 'send', 'start', 'stop', 'subscribe', 'update', 'upload',
    'validate', 'verify',
}
SINGULAR_ALLOW = {
    'auth', 'callback', 'health', 'healthz', 'login', 'logout', 'me', 'metrics',
    'ping', 'ready', 'status', 'token', 'version', 'webhook', 'whoami',
}
PAGINATION_FAMILIES = {
    'page': {'page', 'page_number', 'page_num'},
    'offset': {'offset', 'skip'},
    'cursor': {'cursor', 'next_token', 'after', 'before'},
    'size': {'limit', 'page_size', 'per_page', 'size'},
}
PAGINATION_NAMES = {n for names in PAGINATION_FAMILIES.values() for n in names}
KEBAB_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')


def esc(seg):
    return seg.replace('~', '~0').replace('/', '~1')


def decode_with_lines(text):
    """Parse JSON and return (value, pointer->1-based-line) for every key in the document."""
    dec = json.JSONDecoder()
    lines = {}

    def rec(start, ptr):
        while start < len(text) and text[start] in ' \t\r\n':
            start += 1
        val, end = dec.raw_decode(text, start)
        lines[ptr] = text.count('\n', 0, start) + 1
        if isinstance(val, dict):
            cursor = start + 1
            for k in val:
                kidx = text.find(json.dumps(k), cursor, end)
                if kidx < 0:
                    kidx = text.find(json.dumps(k), cursor)
                kptr = ptr + '/' + esc(k)
                lines[kptr] = text.count('\n', 0, kidx) + 1
                vstart = kidx + len(json.dumps(k))
                while vstart < len(text) and text[vstart] in ' \t\r\n':
                    vstart += 1
                if vstart < len(text) and text[vstart] == ':':
                    vstart += 1
                _, v_end = rec(vstart, kptr)
                cursor = v_end + 1
        elif isinstance(val, list):
            cursor = start + 1
            for i in range(len(val)):
                _, v_end = rec(cursor, ptr + '/' + str(i))
                cursor = v_end + 1
        return val, end

    root, _ = rec(0, '')
    return root, lines


def main():
    ap = argparse.ArgumentParser(description='Emit heuristic convention candidates for an OpenAPI 3 JSON spec')
    ap.add_argument('spec', help='OpenAPI 3 spec as JSON (convert YAML with your own tooling first)')
    a = ap.parse_args()
    spec_path = Path(a.spec)
    try:
        text = spec_path.read_text()
    except OSError as exc:
        print(f'{a.spec}:1: cannot read file: {exc}')
        raise SystemExit(1)
    try:
        doc, lines = decode_with_lines(text)
    except ValueError as exc:
        print(f'{a.spec}:1: spec is not valid JSON: {exc}')
        raise SystemExit(1)

    candidates = []

    # Path segment conventions: plural nouns, kebab-case, no verbs
    for path_key, path_item in (doc.get('paths') or {}).items():
        if not isinstance(path_item, dict):
            continue
        pptr = '/paths/' + esc(path_key)
        for seg in path_key.split('/'):
            if not seg or (seg.startswith('{') and seg.endswith('}')):
                continue
            lowered = seg.lower()
            verb = None
            for v in VERBS:
                if lowered == v or (not seg.endswith('s') and lowered.startswith(v) and len(v) >= 3):
                    verb = v
                    break
            if verb:
                candidates.append((pptr, f'candidate: path segment "{seg}" looks like the verb "{verb}"; actions belong in HTTP methods, not paths'))
                if not KEBAB_RE.match(seg):
                    candidates.append((pptr, f'candidate: path segment "{seg}" is not kebab-case (lowercase words joined by hyphens)'))
            elif not KEBAB_RE.match(seg):
                candidates.append((pptr, f'candidate: path segment "{seg}" is not kebab-case (lowercase words joined by hyphens)'))
            elif seg not in SINGULAR_ALLOW and not seg.endswith('s'):
                candidates.append((pptr, f'candidate: path segment "{seg}" may be singular; collection paths use plural nouns'))

    # Pagination naming consistency across operations: the name set per operation
    # must match. One operation may legitimately mix families (page + limit), but
    # two operations that paginate with different field names are inconsistent.
    op_sets = {}
    for path_key, path_item in (doc.get('paths') or {}).items():
        if not isinstance(path_item, dict):
            continue
        pptr = '/paths/' + esc(path_key)
        for method, op in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(op, dict):
                continue
            mptr = pptr + '/' + method
            names = []
            for i, param in enumerate(op.get('parameters') or []):
                if not isinstance(param, dict) or param.get('in') != 'query':
                    continue
                name = param.get('name')
                if isinstance(name, str) and name in PAGINATION_NAMES:
                    names.append((name, f'{mptr}/parameters/{i}/name'))
            if names:
                op_sets[mptr] = names
    if op_sets:
        base_op = next(iter(op_sets))
        base_names = sorted({n for n, _ in op_sets[base_op]})
        for op_ptr, items in op_sets.items():
            these = sorted({n for n, _ in items})
            if these != base_names:
                ptr = next(p for n, p in items if n not in base_names)
                candidates.append((ptr, f'candidate: pagination field names differ across operations: {", ".join(these)} here vs {", ".join(base_names)} elsewhere'))

    for ptr, msg in sorted(candidates, key=lambda c: lines.get(c[0], 0)):
        print(f'{a.spec}:{lines.get(ptr, 1)}: {msg}')
    raise SystemExit(1 if candidates else 0)


if __name__ == '__main__':
    main()
