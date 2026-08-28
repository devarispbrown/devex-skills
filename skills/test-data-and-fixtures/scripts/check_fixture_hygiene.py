#!/usr/bin/env python3
"""Scan a fixture tree for test-data hygiene problems.

Flags email addresses that look real, API-key-like strings, credit-card
patterns, and unsanitized production markers. Prints findings to stdout and
exits 1 when any are found. Stdlib only.
"""
import argparse, re, sys
from pathlib import Path

PLACEHOLDER_DOMAINS={'example.com','example.org','example.net','example.edu',
    'example.test','test.com','localhost','local','invalid','test'}
PLACEHOLDER_VALUES={'changeme','change-me','change_me','xxxx','xxxxx','xxxxxx','test',
    'test-key','test_key','secret','password','passwd','your-api-key','your_api_key',
    'your-key','redacted','[redacted]','<redacted>','none','null','local','localhost',
    'example','dummy','placeholder','todo','xxx','your-token'}
EMAIL_RE=re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
DIGIT_RUN_RE=re.compile(r'(?<!\d)\d[\d\s-]{12,18}(?!\d)')
KEY_PATTERNS=(
    (re.compile(r'\b(?:AKIA|ASIA)[0-9A-Z]{16}\b'),'AWS access key'),
    (re.compile(r'\b(?:sk|pk|rk)_live_[A-Za-z0-9]{16,}\b'),'live API key'),
    (re.compile(r'\bghp_[A-Za-z0-9]{36}\b'),'GitHub personal access token'),
    (re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{10,}\b'),'Slack token'),
    (re.compile(r'\bAIza[0-9A-Za-z_-]{35}\b'),'Google API key'),
    (re.compile(r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b'),'JWT-like token'),
)
ASSIGN_RE=re.compile(r'\b(?:api[_-]?key|secret|token|password|passwd|access[_-]?key)\s*[=:]\s*["\']?([A-Za-z0-9._/+=-]{16,})["\']?',re.I)
PROD_RE=re.compile(r'(?i)\b(?:production|prod)(?:[\w -]{0,24}?(?:backup|dump|export|snapshot|database|db|cluster|instance|server))\b')
PROD_RE2=re.compile(r'(?i)\b(?:backup|dump|export|snapshot)[\w -]{0,24}?(?:production|prod)\b')
IP_RE=re.compile(r'\b(?<!\d)(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})(?!\d)\b')

def placeholder_domain(dom):
    return dom in PLACEHOLDER_DOMAINS or any(dom.endswith('.'+p) for p in PLACEHOLDER_DOMAINS)

def luhn_ok(digits):
    total=0
    for i,ch in enumerate(reversed(digits)):
        n=int(ch)
        if i%2==1:
            n*=2
            if n>9: n-=9
        total+=n
    return total%10==0

def private_or_doc_ip(o):
    a,b,c,d=(int(x) for x in o)
    if a in (10,127,0,255): return True
    if a==172 and 16<=b<=31: return True
    if a==192 and b==168: return True
    if a==169 and b==254: return True
    if (a,b,c) in ((192,0,2),(198,51,100),(203,0,113)): return True
    if a==198 and b==18: return True
    return False

def redact(value):
    value = str(value).strip('"\'')
    if len(value) <= 4:
        return '*' * len(value)
    return value[:4] + '...'

def check_email(line):
    for m in EMAIL_RE.findall(line):
        if not placeholder_domain(m.rsplit('@',1)[1].lower()):
            # never print the full address; findings land in logs and CI output
            return ('email','email address that looks real (%s)' % redact(m))
    return None

def check_key(line):
    for pat,label in KEY_PATTERNS:
        if pat.search(line): return ('key','key-like string (%s)' % label)
    m=ASSIGN_RE.search(line)
    if m and m.group(1).lower() not in PLACEHOLDER_VALUES:
        # never print the matched secret value
        return ('key','key-like string (secret value in %s)' % redact(m.group(1)))
    return None

def check_card(line):
    for m in DIGIT_RUN_RE.findall(line):
        digits=re.sub(r'\D','',m)
        if 13<=len(digits)<=16 and digits[0] in '3456' and luhn_ok(digits):
            return ('card','Luhn-valid credit-card pattern')
    return None

def check_prod(line):
    if PROD_RE.search(line) or PROD_RE2.search(line):
        return ('prod','unsanitized production marker')
    m=IP_RE.search(line)
    if m and not private_or_doc_ip(m.groups()):
        return ('prod','public IP address (looks like real infrastructure)')
    return None

CHECKS=(('email',check_email),('key',check_key),('card',check_card),('prod',check_prod))

def scan_file(path):
    findings=[]
    try:
        text=path.read_text(errors='replace')
    except OSError:
        return findings
    if '\x00' in text:
        return findings
    for i,line in enumerate(text.splitlines(),1):
        for kind,fn in CHECKS:
            r=fn(line)
            if r: findings.append('%s:%d: %s: %s' % (path,i,r[0],r[1]))
    return findings

def main():
    ap=argparse.ArgumentParser(description='Scan a fixture tree for test-data hygiene problems')
    ap.add_argument('path',nargs='?',default='.',help='fixture tree to scan (default: current directory)')
    a=ap.parse_args()
    root=Path(a.path)
    if not root.exists(): raise SystemExit('path does not exist: %s' % a.path)
    total=0; files_with_findings=set()
    for p in root.rglob('*'):
        if not p.is_file(): continue
        if any(part.startswith('.') for part in p.relative_to(root).parts): continue
        findings=scan_file(p)
        if findings:
            files_with_findings.add(str(p)); total+=len(findings)
            print('\n'.join(findings))
    print('%d hygiene finding(s) in %d file(s)' % (total,len(files_with_findings)))
    if total: raise SystemExit(1)
    print('Clean: no hygiene findings')
    raise SystemExit(0)
if __name__=='__main__': main()
