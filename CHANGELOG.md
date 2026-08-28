# Changelog

## 2.3.1 - 2026-08-28

- Community gap closure: `UNACKNOWLEDGED_PRS` (max-days constant) and `NO_LICENSE` gates; LICENSE joins the community standards files as an eighth scored file.
- Maintainer Concentration Index reported as its own checker line; Q&A dimension gains `community_answer_share`.
- New procedural references: review-experience, qa-analysis, maintainer-sustainability (auditor); community-automation, community-tooling (designer).
- Cross-skill feedback loops added to the community pair's orchestration and operations sections; repeated-question-to-docs handoff procedure documented.
- Designer skill's standards subset now includes the community response SLO constants.

## 2.3.0 - 2026-08-28

- Added twenty new skills: `developer-community`, `developer-community-auditor`, `developer-workflow-auditor`, `sandbox-experience`, `architecture-experience`, `developer-discoverability`, `developer-support`, `access-and-permissions-dx`, `extensibility-engineer`, `developer-economics`, `environment-lifecycle`, `change-awareness`, `operational-trust`, `test-data-and-fixtures`, `ide-experience`, `policy-experience`, `web-console-dx`, `experimentation-engineer`, `accessibility-dx`, and `reference-application-engineer`. The suite now ships 42 skills.
- Added `dx-standards/community.md`: the 30-minute community onboarding path, response SLOs with trailing-30-day windows, ratio-based stage gates, ten named community gates with a hard-failure set, CHAOSS metric names, and the Community Health Score.
- Added `dx-standards/slo.md` (SLO-to-owner table, values by reference) and `dx-standards/domains.md` (six-domain canonical map of all 42 skills).
- Extended `dx-standards/metrics.md` with workflow feedback budgets, architecture comprehension, and the sandbox gate.
- Added `scripts/smoke_skills.py`: per-skill fixture smoke tests declared in `assets/smoke.json`, enforced as a fourth CI gate. Fixed a PII/secret redaction issue in the fixture hygiene scanner.
- Extended `scripts/validate_skills.py` with domains three-way mapping, CHANGELOG version check, plugin description skill count, README coverage and size cap.
- README reorganized around the six domains (Learn & Adopt, Build, Validate, Ship & Operate, Participate & Extend, Measure & Improve); the roadmap section is gone — the suite is complete.
- Merge workflow: PR template with commit-by-commit review checklist; releases merge only on green CI.

## 2.2.0 - 2026-08-28

- Added twelve new skills: `cli-designer`, `security-supply-chain`, `observability-readiness`, `configuration-dx`, `golden-path-scaffolder`, `performance-engineer`, `compatibility-engineer`, `contributor-experience`, `dependency-health`, `integration-certifier`, `agent-native-dx`, and `developer-feedback-analyst`.
- Each new skill ships a stdlib-only scanner or checker with fixtures, procedural references, and a generated `references/standards.md` subset.
- Plugin now registers 22 skills; the suite covers CLI ergonomics, supply-chain security, observability, configuration UX, scaffolding, performance budgets, compatibility matrices, contributor funnels, dependency policy, integration certification, agent readiness, and feedback analytics.
- Description disambiguation convention extended: `security-supply-chain` now routes permission-model ergonomics to `access-and-permissions-dx` and policy-as-code to `policy-experience`.

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
