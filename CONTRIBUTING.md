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

## How versions work

The suite is versioned with SemVer, and `.claude-plugin/plugin.json` carries the one
authoritative version.

- **Major**: a skill is removed or renamed, a gate constant or SLO name is removed or
  redefined, or a script's command-line contract breaks. Anything that makes an existing
  invocation or an existing citation wrong.
- **Minor**: new capability that does not break what exists. A new skill, a new script or
  reference inside an existing skill, a new gate, constant, or SLO in `dx-standards/`, or
  a new flag on an existing script.
- **Patch**: everything else. Wording, corrections, fixture and smoke-test changes,
  refactors with no behavior change, and fixes to content that was already there.

The rule that decides between minor and patch is whether a reader gains something they
could not do or cite before. Two new named gates are a minor even though the diff is
small, because a skill can now fail a release on a constant that did not exist. Rewriting
a reference file for clarity is a patch even when the diff is large.

Releases before 2.4.0 do not all follow this policy. It applies going forward rather than
retroactively, and 2.3.1 in particular would be a minor under it.

### The version matrix

`scripts/validate_skills.py` requires `plugin.json` and every `SKILL.md`
`metadata.version` to agree, so a bump touches all of them or CI fails. In the same
commit:

1. `.claude-plugin/plugin.json` version.
2. Every `skills/*/SKILL.md` `metadata.version`.
3. A `## <version> - <date>` heading in `CHANGELOG.md`.

A change to the number of skills additionally touches the spelled-out count in the
`plugin.json` description, the per-domain counts in `dx-standards/domains.md`, which must
re-sum to the plugin's skills array, and the README, which names every skill and is size
capped. `.claude-plugin/marketplace.json` carries its own schema version and does not
track the plugin version, but it repeats the description, so a skill-count change has to
update it too.

## How review works

Open a pull request. CI runs the four gates; review walks the commits. Merge happens when checks are green and review passes. Review usually takes a few days; first-time contributor PRs get a first review within the response SLOs in `dx-standards/community.md`.

## Who can help

The maintainer is listed in `MAINTAINERS.md`. Tag them on issues or discussions when you're stuck.

## How decisions are made

See `GOVERNANCE.md`. In short: the maintainer decides, decisions are recorded in pull requests and release notes, and sustained contributors get invited to review and maintain.

## Becoming more involved

Review PRs, triage issues, answer questions, or improve docs. Sustained, high-quality work leads to reviewer and then maintainer status, per the ladder in `GOVERNANCE.md`.
