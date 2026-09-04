# Changelog

## 2.9.2 - 2026-09-03

- `check_tool_surface.py` pairs tools by intent rather than string distance. A threshold on lexical similarity flagged `create_user` against `create_org`, which is the pair the script's own docstring names as never confused, while the real separator is whether two tools act on the same object with interchangeable verbs.
- The boundary check no longer accepts a documentation cross-reference as a boundary. A description reading "See the API docs" satisfied it, which is the fix `selection-review.md` explicitly forbids.
- Namespace detection buckets per prefix instead of requiring every tool to share one. Adding a single unnamespaced tool to a namespaced surface previously turned every finding off, so multi-product servers, the shape this skill's own guidance recommends, were reported clean.
- Added two checks traceable to a cited normative source and decidable from the file: tool names must match the naming rule from the cited MCP naming SEP, and a description naming a tool the surface does not expose is a dead end.
- Removed `--strict`, which was documented and never read.
- `read_tools` handles `OSError` rather than emitting a traceback, matching the fix already made across the suite.
- `SKILL.md` no longer claims a checker verifies untrusted-content declarations. No checker does, and no gate constant covers them; the section now says the boundary is unautomated.
- `agent-native-dx` names `agent-integration-dx` in its description. Routing was one-directional, so "review my MCP server" matched the audit skill.
- The clean fixture routed to a tool that does not exist on its own surface. The new dangling-reference check caught it, which is the first time a fixture in this suite was corrected by a check added alongside it.

## 2.9.1 - 2026-09-03

- `check_tool_surface.py` only reports a missing boundary when the tool has a near sibling, because confusability is a property of pairs, which the skill's own reference already said and the checker did not implement. Run against the reference MCP git server it had produced a candidate on 12 of 12 tools, which is noise.
- Sibling detection is namespace aware. A surface named `git_status`, `git_diff`, `git_commit` is namespaced on `git`, and treating that shared prefix as the verb made every tool a synonym of every other. The prefix is stripped when every tool shares it.
- Duplicate tool names are reported as duplicates rather than as a confusable pair with themselves.
- Against Anthropic's reference git server the output drops from 13 candidates to 6, and the surviving finding is real: `git_diff`, `git_diff_staged` and `git_diff_unstaged` all describe showing changes and none states when to choose another, so an agent asked to show what changed picks among three with no stated boundary.
- `agent-integration-dx` documents that most servers declare tools in source and return them from `tools/list` rather than shipping a file, so the captured response is what to pass.

## 2.9.0 - 2026-09-03

- Added the `UNVERIFIABLE_CI_PARITY` gate (P1): the documented local check command does not appear in CI configuration, so a green local run does not predict a green CI run. `contributor-experience` has always called a local-versus-CI divergence a P1 defect, but prose cannot fail a release. It is promoted to a constant because the failure mode is worse for an unattended caller than for a person: a developer sees the CI email and iterates, while an agent either ships work it believes is finished or spends cycles guessing.
- The gate is decidable from committed files, and thirteen of the fifteen audited public repositories trip it.
- `check_agent_readiness.py` now names the gate constant a gap trips, so a finding points at something that can fail a release rather than floating free. Missing setup and test commands name `NON_REPRODUCIBLE_BUILD`, which already covered them; no new constant was minted for those.

## 2.8.0 - 2026-09-03

- Added `agent-integration-dx`, taking the suite to forty-three skills. It owns tool definitions and MCP servers as shipped product artifacts: tool naming, description-as-prompt authoring, argument schema design, response shaping against a context budget, pagination and truncation, and tool-level error surfaces. A tool description is read by a model at selection time with no chance to ask a clarifying question, so it is doing prompt work whether or not it was written that way.
- The skill cites rather than restates. The MCP specification, SEP-986, Anthropic's tool-writing guidance and the AWS design guidelines are treated as normative in `references/upstream-specs.md`, with a verification date per source and a rule that a moved source is a finding. Restating them would create a second copy that drifts, which is the defect `STALE_PUBLIC_REFERENCE` names and which the suite applies to other people's products.
- What it adds that the upstream sources do not is the adversarial selection review: take each plausibly confusable pair, write the prompt that should select each side, and ask whether the descriptions alone decide it.
- `scripts/check_tool_surface.py` inventories a tool definition file and reports selection-risk candidates: missing descriptions, descriptions that state no boundary, synonym verbs used for one concept, lexically close pairs, and argument schemas with undescribed or unclosed parameters. Candidates only, never verdicts, following `guessability_check.py`, because lexical similarity does not measure selection error.
- Why this skill and not another audit skill: fifteen public repositories were measured and none exposed an MCP server, `MCP` appeared in two of five hundred and seventy-eight files, and no checker in the suite looked for one. The audit side already had an owner in `agent-native-dx`; the build side had none.

## 2.7.1 - 2026-09-03

- `agent-native-dx` now describes itself by the question a developer actually asks, "is my repository ready for AI agents?", rather than by what it does for a product author. Skill routing matches on the description, so the old build-side framing meant a developer asking whether AI could use their repository would not find the skill that answers it. No new skill: this surface already had an owner, and a second one would have been a second front door onto the same question.
- The skill's workflow now leads with scoring the repository and reporting the gaps, which is what an invocation should produce first.
- README gains the agent-readiness path alongside the existing DX and community ones: install the plugin, ask Claude to run `agent-native-dx`, read the report.

## 2.7.0 - 2026-09-03

- `check_agent_readiness.py` adds eight surfaces that decide whether an agent can do the work rather than only find its way around: a setup command that works from a clean clone, a discoverable test command, a declared lint or format tool, CI configuration, whether CI runs the same test command the documentation gives, a pinned toolchain version, an architecture document, and a documented destructive-operation guardrail.
- The report is grouped by the three questions an agent faces: can it find its way around, can it operate the product, can it do the work.
- Measured across fifteen public repositories in six ecosystems, the score spread is 79% to 21%, so the inventory discriminates. The most common gap that is not simply an emerging practice is CI parity: thirteen of fifteen give no way to tell that a green local run predicts a green CI run, which is the property an agent depends on most, because it cannot otherwise know whether its change is finished.

## 2.6.0 - 2026-09-03

- `check_agent_readiness.py` now inventories the surfaces a repository exposes to agents at runtime, not just the ones a coding agent reads: an exposed MCP server (detected from `.mcp.json` and similar manifests, and from an MCP SDK dependency in the build manifest), whether MCP is documented for users, shipped agent skills, and `llms.txt`. Nothing in the suite looked for MCP before, which left the surface the question is most often about entirely unmeasured.
- Output is a readable report rather than a wall of paths: three examples per surface plus a count, and a closing readiness percentage with a band of agent-ready, partly agent-ready, or not agent-ready.
- Fixture `assets/mcp-sample` exercises the new surfaces, wired into smoke.

## 2.5.2 - 2026-09-03

- `agent_trial_driver.py` refuses a task whose `verify` command reads the trial scratch directory. A verify that executes a command the agent wrote hands the agent control of its own grading. Found by running the 2026-09-03 pilot: every agent that recorded the project's real test command failed, and the one that recorded a command testing nothing passed, so the defect converts a real failure into a pass in exactly the cell where the honest answer fails. The driver now refuses the registration that pilot ran under.
- `references/trial-protocol.md` states the rule: a verify command asserts an outcome the agent cannot trivially satisfy, and never executes agent-authored content.
- `check_contributor_funnel.py` no longer crashes on any repository that has a pull request template. One of six `text_has` call sites passed a raw string where a compiled pattern was expected, so the checker only completed on repositories missing a PR template. Found on first contact with `astral-sh/uv`.
- `check_contributor_funnel.py` detects local test targets beyond Make and npm: pyproject, tox, Cargo, go, Gemfile, Maven and Gradle. It previously reported a false gap on every repository in the first external audit, two Python projects and one Rust project, telling maintainers they had no local test target when they had pytest and cargo test respectively. A suite that tells a Python maintainer their test target does not exist is doing the thing it exists to prevent.

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
