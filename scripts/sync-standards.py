#!/usr/bin/env python3
"""Distribute dx-standards/ sections into each skill's references/. Stdlib only.

Generated files are committed so skills stay self-contained. Selectors match
source headings by exact heading text; a selector matching nothing is an error.
"""
import argparse, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STANDARDS = ROOT / 'dx-standards'

MD_HEADER = ('<!-- GENERATED FILE - do not edit by hand. Source: dx-standards/. '
             'Regenerate with: python3 scripts/sync-standards.py -->\n\n')
PY_HEADER = ('# GENERATED FILE - do not edit by hand. Source: dx-standards/. '
             'Regenerate with: python3 scripts/sync-standards.py\n\n')


def split_sections(text):
    """Split markdown on '## ' headings; return {heading_text: section_text}."""
    sections = {}
    current_title, current_lines = None, []
    for line in text.splitlines(keepends=True):
        if line.startswith('## '):
            if current_title is not None:
                sections[current_title] = ''.join(current_lines)
            current_title = line[3:].strip()
            current_lines = [line]
        elif current_title is not None:
            current_lines.append(line)
        else:
            current_lines.append(line)
    if current_title is not None:
        sections[current_title] = ''.join(current_lines)
    else:
        sections[''] = ''.join(current_lines)
    return sections


def compose(files, map_entry):
    parts = []
    for item in files:
        src = STANDARDS / item['source']
        text = src.read_text()
        selectors = item['sections']
        if selectors == ['*']:
            parts.append(text)
            continue
        sections = split_sections(text)
        for sel in selectors:
            if sel not in sections:
                raise SystemExit(f'{map_entry}: selector {sel!r} matches nothing in {item["source"]}')
            parts.append(sections[sel])
    body = '\n\n'.join(p.rstrip('\n') + '\n' for p in parts).rstrip('\n') + '\n'
    if map_entry.get('header', True):
        header = MD_HEADER if map_entry['target'].endswith('.md') else PY_HEADER
        return header + body
    return body


def sync_one(skill, mapping, check=False):
    changed = []
    for target, entry in mapping.items():
        entry = dict(entry)
        entry['target'] = f'{skill}:{target}'
        dest = ROOT / 'skills' / skill / target
        content = compose(entry['files'], entry)
        if dest.exists() and dest.read_text() == content:
            continue
        changed.append(target)
        if not check:
            dest.parent.mkdir(parents=True, exist_ok=True)
            tmp = dest.with_name(dest.name + '.tmp')
            tmp.write_text(content)
            os.replace(tmp, dest)
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='exit 1 if any target differs from regeneration')
    ap.add_argument('--list', action='store_true', help='print the mapping')
    ap.add_argument('--skill', help='sync only this skill')
    a = ap.parse_args()
    sm = json.loads((STANDARDS / 'sync-map.json').read_text())
    if sm.get('version') != 2:
        raise SystemExit(f'sync-map.json version {sm.get("version")!r} unsupported; expected 2')
    skills = [a.skill] if a.skill else list(sm['skills'])
    if a.list:
        for sk in skills:
            for target in sm['skills'].get(sk, {}):
                print(f'{sk}: {target}')
        return 0
    drift = []
    for sk in skills:
        if sk not in sm['skills']:
            raise SystemExit(f'no sync-map entry for skill {sk!r}')
        mapping = sm['skills'][sk]['targets']
        changed = sync_one(sk, mapping, check=a.check)
        for t in changed:
            print(f'{"DRIFT" if a.check else "WROTE"} {sk}: {t}')
            if a.check:
                drift.append(t)
    return 1 if drift else 0


if __name__ == '__main__':
    raise SystemExit(main())
