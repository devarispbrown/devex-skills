#!/usr/bin/env python3
"""Structural lint for the skills suite. Stdlib only.

Checks: plugin.json <-> directory <-> frontmatter three-way match, version
matrix, frontmatter schema, reference-mention existence and orphans, no
path-based cross-skill references, description overlap warnings, stale-phrase
grep, py_compile of every script. Exit 1 on structural failure.
"""
import json, py_compile, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / '.claude-plugin' / 'plugin.json'

REQUIRED_FM = ('name', 'description', 'license', 'compatibility')
STOPWORDS = {'the', 'a', 'an', 'and', 'or', 'for', 'with', 'use', 'to', 'of',
             'in', 'on', 'as', 'is', 'are', 'be', 'by', 'not', 'that', 'this',
             'it', 'its', 'from', 'at', 'when', 'where', 'what', 'which'}
STALE_PHRASES = ('Two Agent Skills', 'Two complementary')


def frontmatter(text):
    # NOTE: relies on the flat line format `metadata:\n  version: "X.Y.Z"` —
    # the version check below flattens the nested key. If this parser is
    # refactored to real YAML, keep extracting version the same way or the
    # version-matrix enforcement silently disables.
    if not text.startswith('---'):
        return None
    end = text.find('\n---', 4)
    if end < 0:
        return None
    fm = {}
    for line in text[4:end].splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip()
    return fm


def number_word(n):
    ones = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
            'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
            'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy',
            'eighty', 'ninety']
    if n < 20:
        return ones[n]
    if n < 100:
        return tens[n // 10] + ('-' + ones[n % 10] if n % 10 else '')
    return str(n)


def words(text):
    return {w.lower().strip('.,;:()"\'/') for w in text.split()
            if w.lower().strip('.,;:()"\'/') not in STOPWORDS and len(w) > 3}


def main() -> int:
    failures, warnings = [], []

    # plugin.json
    plugin = json.loads(PLUGIN.read_text())
    plugin_version = plugin.get('version')
    plugin_skills = plugin.get('skills', [])
    if not plugin_version:
        failures.append('plugin.json: missing version')
    if not plugin_skills:
        failures.append('plugin.json: missing skills array')

    skill_names = []
    descriptions = []
    for entry in plugin_skills:
        d = (ROOT / entry).resolve()
        if not d.is_dir():
            failures.append(f'plugin.json: {entry} is not a directory')
            continue
        skill_file = d / 'SKILL.md'
        if not skill_file.exists():
            failures.append(f'{entry}: no SKILL.md')
            continue
        skill_names.append(d.name)
        text = skill_file.read_text()
        fm = frontmatter(text) or {}
        for field in REQUIRED_FM:
            if field not in fm:
                failures.append(f'{d.name}: frontmatter missing {field}')
        if fm.get('name') != d.name:
            failures.append(f'{d.name}: frontmatter name {fm.get("name")!r} != directory name')
        fm_version = fm.get('version', '').strip('"\'') or None
        if fm_version != plugin_version:
            failures.append(f'{d.name}: metadata.version {fm_version!r} != plugin version {plugin_version!r}')

        # reference mentions must exist; no cross-skill path references
        mentioned = set()
        for m in re.finditer(r'`((?:references|scripts|assets)/[^` ]+)`', text):
            p = d / m.group(1)
            mentioned.add(m.group(1))
            if not p.exists():
                failures.append(f'{d.name}: SKILL.md mentions missing {m.group(1)}')
        if re.search(r'`skills/[^`]+`', text):
            failures.append(f'{d.name}: SKILL.md uses a skills/ path; cross-skill references are by name only')

        # orphan reference files
        ref_dir = d / 'references'
        if ref_dir.is_dir():
            for ref in sorted(ref_dir.glob('*.md')):
                rel = f'references/{ref.name}'
                if rel not in mentioned:
                    warnings.append(f'{d.name}: {rel} never mentioned in SKILL.md')

        # description overlap between pairs
        descriptions.append((d.name, words(fm.get('description', ''))))

        # stale phrases

    # significant-word overlap between description pairs; skip pairs that
    # disambiguate each other by name (intended pointer sentences)
    for i in range(len(descriptions)):
        for j in range(i + 1, len(descriptions)):
            n1, w1 = descriptions[i]
            n2, w2 = descriptions[j]
            if n2 in ' '.join(w1) or n1 in ' '.join(w2):
                continue
            names = {d[0] for d in descriptions}
            shared = (w1 & w2) - names
            if len(shared) >= 8:
                warnings.append(f'descriptions {n1}/{n2} share {len(shared)} significant words: {sorted(shared)[:8]}')

    # stale phrases in user-facing files
    for p in (ROOT / 'README.md', PLUGIN):
        if p.exists():
            for phrase in STALE_PHRASES:
                if phrase in p.read_text():
                    failures.append(f'{p.name}: stale phrase {phrase!r}')

    # plugin description must carry the current skill count in words
    n = len(skill_names)
    if n and number_word(n) not in plugin.get('description', '').lower():
        failures.append(f'plugin.json: description missing skill count {number_word(n)!r}')

    # CHANGELOG must contain a heading matching the plugin version
    changelog = ROOT / 'CHANGELOG.md'
    if changelog.exists():
        if f'## {plugin_version} ' not in changelog.read_text() and f'## {plugin_version}\n' not in changelog.read_text():
            failures.append(f'CHANGELOG.md: no entry for version {plugin_version}')

    # README must mention every plugin-listed skill and stay under the size cap
    readme = (ROOT / 'README.md').read_text()
    for name in skill_names:
        if name not in readme:
            failures.append(f'README.md: does not mention skill {name}')
    if (ROOT / 'README.md').stat().st_size > 25600:
        failures.append('README.md: exceeds 25KB cap')

    # domains.md must list every plugin skill exactly once; extra rows allowed
    # (forward-looking for skills landing later in the release)
    domains = ROOT / 'dx-standards' / 'domains.md'
    if domains.exists():
        dtext = domains.read_text()
        for name in skill_names:
            pat = rf'(?<![a-z0-9-]){re.escape(name)}(?![a-z0-9-])'
            count = len([l for l in dtext.splitlines() if re.search(pat, l)])
            if count == 0:
                failures.append(f'domains.md: skill {name} not mapped to a domain')
            elif count > 1:
                failures.append(f'domains.md: skill {name} appears in {count} rows')

    # cross-check: every skills/ dir listed in plugin.json
    for d in sorted((ROOT / 'skills').glob('*')):
        if d.is_dir() and (d / 'SKILL.md').exists() and d.name not in skill_names:
            failures.append(f'skills/{d.name}: not listed in plugin.json')

    # py_compile every script
    for script in sorted(ROOT.glob('scripts/*.py')) + sorted(ROOT.glob('skills/*/scripts/*.py')):
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as e:
            failures.append(f'{script}: {e}')

    if failures:
        print('FAILURES:')
        for f in failures:
            print(f'  {f}')
    if warnings:
        print('WARNINGS:')
        for w in warnings:
            print(f'  {w}')
    print(f'{len(failures)} failure(s), {len(warnings)} warning(s)')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
