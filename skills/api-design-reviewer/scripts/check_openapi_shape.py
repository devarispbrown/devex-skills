#!/usr/bin/env python3
"""Structural lint on an OpenAPI 3 JSON spec: unique operationIds, resolvable $refs, 4xx/5xx responses, and decodable examples. JSON input only - convert YAML with your own tooling first. Stdlib only."""
import argparse, json
from pathlib import Path

HTTP_METHODS = {'get', 'put', 'post', 'delete', 'patch', 'head', 'options', 'trace'}


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


def resolve_ptr(doc, pointer):
    cur = doc
    for part in pointer.lstrip('/').split('/'):
        if not part:
            continue
        part = part.replace('~1', '/').replace('~0', '~')
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list) and part.isdigit() and int(part) < len(cur):
            cur = cur[int(part)]
        else:
            return None
    return cur


def main():
    ap = argparse.ArgumentParser(description='Lint an OpenAPI 3 JSON spec for structural defects')
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

    findings = []

    # Unique operationIds and 4xx/5xx response coverage
    opid_sites = {}
    for path_key, path_item in (doc.get('paths') or {}).items():
        if not isinstance(path_item, dict):
            continue
        pptr = '/paths/' + esc(path_key)
        for method, op in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(op, dict):
                continue
            mptr = pptr + '/' + method
            opid = op.get('operationId')
            if isinstance(opid, str):
                opid_sites.setdefault(opid, []).append(mptr + '/operationId')
            rptr = mptr + '/responses'
            responses = op.get('responses')
            if not isinstance(responses, dict) or not responses:
                findings.append((rptr, 'operation declares no responses'))
            else:
                codes = sorted(str(c) for c in responses)
                if not any(c[0] in '45' for c in codes):
                    findings.append((rptr, 'operation has no 4xx/5xx responses (only: ' + ', '.join(codes) + ')'))
    for opid, sites in opid_sites.items():
        if len(sites) > 1:
            for site in sites:
                findings.append((site, f'duplicate operationId "{opid}" ({len(sites)} occurrences)'))

    # Resolvable $refs and decodable examples, anywhere in the document
    def check_ref(ref, ptr):
        if ref.startswith('#'):
            if resolve_ptr(doc, ref[1:]) is None:
                findings.append((ptr, f'unresolvable $ref {ref}'))
            return
        fname, _, frag = ref.partition('#')
        target = (spec_path.parent / fname).resolve() if fname else spec_path.resolve()
        if not target.exists():
            findings.append((ptr, f'$ref target file not found: {fname or ref}'))
            return
        try:
            target_doc = json.loads(target.read_text())
        except (OSError, ValueError):
            findings.append((ptr, f'$ref target is not valid JSON (convert YAML with your own tooling first): {fname}'))
            return
        if frag and resolve_ptr(target_doc, frag) is None:
            findings.append((ptr, f'unresolvable $ref {ref}'))

    def walk(node, ptr):
        if isinstance(node, dict):
            ref = node.get('$ref')
            if isinstance(ref, str):
                check_ref(ref, ptr + '/$ref')
            ex = node.get('example')
            if isinstance(ex, str) and ex[:1] in '{[':
                try:
                    json.loads(ex)
                except ValueError:
                    shown = ex if len(ex) <= 48 else ex[:45] + '...'
                    findings.append((ptr + '/example', f'example fails JSON decode: {shown!r}'))
            for k, v in node.items():
                walk(v, ptr + '/' + esc(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, ptr + '/' + str(i))

    walk(doc, '')

    for ptr, msg in sorted(findings, key=lambda f: lines.get(f[0], 0)):
        print(f'{a.spec}:{lines.get(ptr, 1)}: {msg}')
    raise SystemExit(1 if findings else 0)


if __name__ == '__main__':
    main()
