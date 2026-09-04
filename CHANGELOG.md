# Changelog

## 2.5.2 - 2026-09-03

- `agent_trial_driver.py` refuses a task whose `verify` command reads the trial scratch directory. A verify that executes a command the agent wrote hands the agent control of its own grading. Found by running the 2026-09-03 pilot: every agent that recorded the project's real test command failed, and the one that recorded a command testing nothing passed, so the defect converts a real failure into a pass in exactly the cell where the honest answer fails. The driver now refuses the registration that pilot ran under.
- `references/trial-protocol.md` states the rule: a verify command asserts an outcome the agent cannot trivially satisfy, and never executes agent-authored content.

## 2.5.1 - 2026-09-02

- `agent_trial_driver.py` preflight now proves the harness can modify a working tree before spending any sessions, by asking it to create one file and checking the file exists. Found by a pilot run against a real repository: a headless agent CLI defaulted to blocking writes, exited 0, and changed nothing. Every session would have recorded a failure that was the harness rather than the product, and the trial would have reported a large uncovered share made entirely of artifact. Preflight already proved each verify command discriminates; that is not the same as proving the harness can do anything at all.

## 2.5.0 - 2026-09-02

- Added `skills/agent-native-dx/scripts/agent_trial_driver.py`: the live driver that runs a pre-registered agent trial and writes its log. Dry run by default, executing nothing until `--execute`, matching the gate on `magic_path_runner.py`. It holds no credentials and speaks to no model: it invokes `registration.harness_command`, so the harness under test is whichever agent CLI the operator has installed and authenticated. Commands run without a shell.
- Outcome is now decided by a committed command rather than a reading. Each task carries a `verify` argument list that runs in the same working copy after the agent finishes; its exit status decides pass or fail. The driver refuses a task that has no verify command.
- Each session runs against a fresh shallow clone in a scratch directory, so the operator's own checkouts are untouched. The log is written after every session, so an interrupted trial keeps the sessions it paid for and re-running resumes rather than repeating them.
- `registration.harness_command` is read by the driver and accepted, but not required, by the scorer. Making it required would have rejected any log written under 2.4.0, which is a breaking change to the `agent-trial-log/v1` format rather than an addition to it. The versioning policy now says so explicitly, since it previously covered command-line contracts and not data formats.
- `agent_trial_scorer.py --new` now writes empty `runs` and `failure_modes`. It previously shipped invented outcomes, which the driver's resume logic read as sessions already paid for and the scorer read as evidence, so the documented flow produced a verdict from placeholder data.
- The scorer refuses a registration still holding a scaffold placeholder, and refuses a task with no `verify` command. Every outcome in a trial is decided by a verify command, so a task without one has no stated basis for calling a session passed or failed. The driver already enforced this; the scorer did not, and a hand-written log bypassed it.
- `check_protocol_example.py` now also checks the prose pre-registration checklist, not just the fenced JSON example. The checklist is what an operator follows, and a JSON-only guard could not see it going stale, which is exactly what had happened.
- `.gitignore` covers `trial-transcripts/` and scratch clone directories. Transcripts carry raw agent stdout and stderr, which is where credentials surface, and the driver writes them to a relative path by default.
- `references/trial-protocol.md` gains a Running the trial section. The version bump is a minor per the policy added in `CONTRIBUTING.md`: new capability, nothing existing breaks.

## 2.4.0 - 2026-09-02

- Added `skills/agent-native-dx/scripts/agent_trial_scorer.py`: an offline, deterministic scorer for pre-registered agent trials. It validates that a trial was registered before it was run, computes `u` (the share of distinct failure modes the registered coverage corpus does not catch), and applies the decision rule from `AGENT-DX-PROPOSAL.md`. It refuses to emit a verdict for an unregistered trial rather than scoring it anyway.
- Added `skills/agent-native-dx/references/trial-protocol.md`: the operator procedure for running a trial. Pre-registration fields, the enumerated coverage corpus, the classification codebook with worked examples, the second-rater sample, the `agent-trial-log/v1` schema, the decision rule, threats to validity, and cost.
- Added two synthetic trial-log fixtures and `assets/smoke.json`, so the scorer is exercised by `scripts/smoke_skills.py` on every push. Neither fixture names a real product.
- The live driver that executes agents is deliberately not a script. It cannot run in CI: every script here is stdlib-only and offline, and GitHub withholds secrets from fork `pull_request` runs, so a keyed driver could never gate a contributor pull request. Execution stays an operator activity, as magic-path timing already is.

## 2.3.2 - 2026-08-31

- Added `.claude-plugin/marketplace.json`. Without it, the documented `claude plugin marketplace add devarispbrown/devex-skills` failed with `Marketplace file not found`, so the plugin could not be installed by the README's own instructions. The manifest publishes `developer-docs-skills` from the repository root, making the install path work as written.
- Repository layout section of the README now lists the marketplace manifest alongside `plugin.json`.

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
