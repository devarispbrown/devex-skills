# Contributing

## Find something to work on

Issues tagged `good first issue` are scoped for newcomers and carry context, acceptance criteria, and pointers to the relevant files. Larger work lives in open issues and discussions. If nothing fits, open an issue describing the outcome you want to improve.

## Set up the repository

```bash
git clone git@github.com:devarispbrown/devex-skills.git
cd devex-skills
```

No build step and no dependencies beyond Python 3 and git. Everything in the suite is stdlib-only.

## Run tests

```bash
python3 scripts/sync-standards.py --check   # standards drift gate
python3 scripts/validate_skills.py          # suite structural lint
python3 scripts/smoke_skills.py             # per-skill fixture smoke tests
python3 -m py_compile scripts/*.py skills/*/scripts/*.py
```

CI runs exactly these checks on every push.

## What an acceptable change looks like

- Skills: keep `SKILL.md` focused (150–230 lines), put specialist guidance in `references/`, ship stdlib-only scripts that are read-only or dry-run by default.
- Standards: normative numbers live only in `dx-standards/`; skills cite constants by name, never restate values. After editing standards, run `python3 scripts/sync-standards.py`.
- Every checker script ships a broken fixture (exits 1) and, where feasible, a clean fixture (exits 0), wired into `assets/smoke.json`.

## How review works

Open a pull request. CI runs the four gates; review walks the commits. Merge happens when checks are green and review passes. Review usually takes a few days; first-time contributor PRs get a first review within the response SLOs in `dx-standards/community.md`.

## Who can help

The maintainer is listed in `MAINTAINERS.md`. Tag them on issues or discussions when you're stuck.

## How decisions are made

See `GOVERNANCE.md`. In short: the maintainer decides, decisions are recorded in pull requests and release notes, and sustained contributors get invited to review and maintain.

## Becoming more involved

Review PRs, triage issues, answer questions, or improve docs. Sustained, high-quality work leads to reviewer and then maintainer status, per the ladder in `GOVERNANCE.md`.
