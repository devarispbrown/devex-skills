# Changelog

## 2.1.0 - 2026-08-28

- Added eight new skills: `developer-experience-auditor`, `developer-onboarding`, `api-design-reviewer`, `local-development`, `sdk-engineer`, `error-experience`, `quality-engineer`, and `release-guardian`.
- Added the shared `dx-standards/` layer as the single source of truth for principles, metrics, severity, release gates, compatibility, terminology, and the promoted shared methodology files.
- Added `scripts/sync-standards.py`, which distributes standards subsets into each skill's `references/standards.md` so every skill stays self-contained when installed alone. Generated files are committed; `--check` detects drift.
- Added the 14-stage developer journey model with per-stage timing, command counts, credential counts, and context-switch measurement, plus per-area DX scoring with an Overall DX score.
- Added named release gates: `BROKEN_QUICKSTART`, `NON_REPRODUCIBLE_BUILD`, `UNEXPLAINED_ERROR`, `UNDOCUMENTED_BREAKING_API`, `SDK_API_DRIFT`, `UNTESTED_SUPPORTED_VERSION`, and the inherited docs gates.
- Added the ≤10-minute clone-to-productive local-development standard and the 30-minute first-contribution target.
- Consolidated timing tools: `magic_path_runner.py` remains the execution engine, `journey_runner.py` orchestrates the 14-stage journey, and `estimate_magic_path.py` estimates designs without executing.
- `developer-docs-auditor` now defers observed magic-path timing to `developer-experience-auditor` when available.
- Added `scripts/validate_skills.py` for suite-wide structural checks and `.github/workflows/ci.yml` to enforce sync cleanliness on every push.
- Note: the plugin name remains `developer-docs-skills` for install continuity. Renaming to a suite name (e.g. `devex-skills`) is a 3.0.0 candidate.

## 2.0.0 - 2026-08-28

- Split the system into `developer-docs` for authoring/architecture and `developer-docs-auditor` for adversarial validation and release gating.
- Added the hard ≤15-minute end-to-end magic-path standard for new developers.
- Added observed, CI-observed, and estimated timing evidence levels.
- Added documentation impact/drift analysis and release gate semantics.
- Added independent Documentation Quality and Developer Experience scoring.
- Added deterministic helpers for magic-path timing, git-diff impact, local Markdown links, and terminology checks.
- Added Claude Code plugin packaging metadata.
