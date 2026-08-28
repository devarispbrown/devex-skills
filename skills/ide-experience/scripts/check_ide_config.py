#!/usr/bin/env python3
"""Validate VS Code IDE configuration and flag stale task commands.

Parses .vscode/launch.json and .vscode/tasks.json, verifies each entry has
an identifier (name for launch, label for tasks) and a type or command,
and compares task commands against build/test commands declared in Makefile
targets and package.json scripts. A task whose command matches no declared
command is stale and is reported. Exits 1 when any finding is reported.

Files are parsed, never executed; no shell is invoked.

Stdlib only.
"""
import argparse, json, re
from pathlib import Path


def load_json(path, label, findings):
    try:
        return json.loads(path.read_text())
    except OSError as e:
        findings.append(f'[ERROR] {label}: cannot read ({e})')
    except json.JSONDecodeError as e:
        findings.append(f'[ERROR] {label}: invalid JSON ({e})')
    return None


def entry_list(data, key, label, findings):
    if not isinstance(data, dict) or not isinstance(data.get(key), list):
        findings.append(f'[ERROR] {label}: missing required "{key}" list')
        return []
    return data[key]


def check_entries(entries, label, findings, ident_key):
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            findings.append(f'[ERROR] {label}: entry #{i} is not an object')
            continue
        ident = entry.get(ident_key) or entry.get('name' if ident_key == 'label' else 'label')
        if not ident:
            findings.append(f'[ERROR] {label}: entry #{i} missing required field "{ident_key}"')
        if not entry.get('type') and not entry.get('command'):
            name = ident or f'#{i}'
            findings.append(f'[ERROR] {label}: entry "{name}" missing required field "type" or "command"')


def makefile_targets(path):
    targets = set()
    try:
        text = path.read_text()
    except OSError:
        return targets
    for line in text.splitlines():
        m = re.match(r'^([A-Za-z0-9_.-]+)\s*:', line)
        if m:
            name = m.group(1)
            if not name.startswith('.'):
                targets.add(name)
    return targets


def package_scripts(path):
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}
    scripts = data.get('scripts') if isinstance(data, dict) else None
    return scripts if isinstance(scripts, dict) else {}


def task_command(entry):
    if entry.get('type') == 'npm' and entry.get('script'):
        return f"npm run {entry['script']}"
    cmd = entry.get('command')
    if not cmd:
        return None
    args = entry.get('args') or []
    parts = [str(cmd)]
    if isinstance(args, list):
        parts.extend(str(a) for a in args)
    else:
        parts.append(str(args))
    return ' '.join(parts)


def is_stale(cmd, targets, scripts):
    tokens = cmd.split()
    if not tokens:
        return False
    prog = tokens[0]
    if prog == 'make':
        arg = next((t for t in tokens[1:] if not t.startswith('-')), None)
        return arg not in targets
    if prog in ('npm', 'yarn', 'pnpm') and len(tokens) >= 2:
        target = tokens[2] if tokens[1] == 'run' and len(tokens) >= 3 else tokens[1]
        return target not in scripts
    if prog in scripts or prog in targets:
        return False
    return True


def main():
    ap = argparse.ArgumentParser(description='Validate VS Code IDE configuration and flag stale task commands.')
    ap.add_argument('--root', default='.', help='project root; default paths resolve under it')
    ap.add_argument('--launch', help='path to launch.json (default: <root>/.vscode/launch.json)')
    ap.add_argument('--tasks', help='path to tasks.json (default: <root>/.vscode/tasks.json)')
    ap.add_argument('--makefile', help='path to Makefile (default: <root>/Makefile)')
    ap.add_argument('--package', help='path to package.json (default: <root>/package.json)')
    a = ap.parse_args()
    root = Path(a.root)
    launch = Path(a.launch) if a.launch else root / '.vscode' / 'launch.json'
    tasks = Path(a.tasks) if a.tasks else root / '.vscode' / 'tasks.json'
    makefile = Path(a.makefile) if a.makefile else root / 'Makefile'
    package = Path(a.package) if a.package else root / 'package.json'

    findings = []
    notes = []
    if launch.exists() or a.launch:
        data = load_json(launch, 'launch.json', findings)
        if data is not None:
            check_entries(entry_list(data, 'configurations', 'launch.json', findings), 'launch.json', findings, 'name')
    if tasks.exists() or a.tasks:
        data = load_json(tasks, 'tasks.json', findings)
        if data is not None:
            entries = entry_list(data, 'tasks', 'tasks.json', findings)
            check_entries(entries, 'tasks.json', findings, 'label')
            targets = makefile_targets(makefile) if makefile.exists() else set()
            scripts = package_scripts(package) if package.exists() else {}
            if entries and not targets and not scripts and not (makefile.exists() or package.exists()):
                notes.append('[NOTE] tasks.json: no Makefile or package.json found; skipping stale-command comparison')
            else:
                for entry in entries:
                    if not isinstance(entry, dict):
                        continue
                    cmd = task_command(entry)
                    if not cmd:
                        continue
                    ident = entry.get('label') or entry.get('name') or '?'
                    if is_stale(cmd, targets, scripts):
                        findings.append(f'[STALE] tasks.json: task "{ident}": command "{cmd}" matches no package.json script or Makefile target')

    for line in notes:
        print(line)
    for line in findings:
        print(line)
    print(f'FINDINGS: {len(findings)}')
    print('RESULT: PASS' if not findings else 'RESULT: FAIL')
    raise SystemExit(1 if findings else 0)


if __name__ == '__main__':
    main()
