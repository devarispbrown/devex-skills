#!/usr/bin/env python3
"""Check 403 denial explanations against the 403-explanation standard.

Reads a JSON array of error samples (each: location, text) and checks each
denial for the three required parts: the required permission, the grant
route, and role context. Prints findings per sample; exits 1 when any sample
is missing a field. Stdlib only.
"""
import argparse, json, re, sys
from pathlib import Path

PERMISSION_RE = re.compile(r"""(?ix)
    (?:requires?|needs?|lacks?|missing)\s+(?:the\s+)?[`"']?[\w./*:-]+[`"']?\s*(?:permission|access)
  | permission\s*[:`]\s*[`"']?[\w./*:-]+
""")
GRANT_RE = re.compile(r"""(?ix)
    https?://\S+
  | \b(?:ask|contact|request|file|open|submit|apply|message|email|ping)\b
    .{0,80}?\b(?:access|permission|grant|admin|owner|team|group|support|ticket|issue|iam|approv\w*)\b
""")
ROLE_RE = re.compile(r"""(?ix)
    \byour\s+(?:current\s+)?role\b
  | \b(?:you\s+are|you're|you\s+have)\b
  | \broles?\s*[:=]
  | \broles?\s+(?:that|which|with|containing|granting)\b
  | \b(?:assigned|membership|member\s+of)\b
""")
CHECKS = ((PERMISSION_RE, 'required permission'), (GRANT_RE, 'grant route'), (ROLE_RE, 'role context'))

def main():
    ap=argparse.ArgumentParser(description='Check 403 explanations against the 403-explanation standard')
    ap.add_argument('fixtures', help='JSON array of error samples (each: location, text)')
    a=ap.parse_args()
    try:
        samples=json.loads(Path(a.fixtures).read_text())
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f'cannot read {a.fixtures}: {e}')
    if not isinstance(samples, list):
        raise SystemExit(f'{a.fixtures}: expected a JSON array of error samples')
    findings=[]; checked=0
    for i, sample in enumerate(samples, 1):
        if not isinstance(sample, dict) or not isinstance(sample.get('location'), str) or not sample['location'].strip() \
                or not isinstance(sample.get('text'), str) or not sample['text'].strip():
            findings.append((f'entry #{i}', 'malformed sample: requires non-empty location and text'))
            continue
        checked+=1
        missing=[name for pat, name in CHECKS if not pat.search(sample['text'])]
        if missing:
            findings.append((sample['location'], 'missing '+', '.join(missing)))
    for loc, detail in findings:
        print(f'{loc}: {detail}')
    print(f'{len(findings)} finding(s) across {checked} denial(s)')
    raise SystemExit(1 if findings else 0)
if __name__=='__main__': main()
