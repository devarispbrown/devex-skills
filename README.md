# Developer Experience Skills Suite

Forty-two Agent Skills that build, audit, and gate every surface of a developer tool. Onboarding, the API, the CLI, SDKs, docs, errors, your community, releases, operations: all of it, backed by one shared constitution of measurable DX standards.

## Why I built this

I've spent my career building developer tools and communities at Microsoft, Zendesk, Heroku, Twitter, and Meroxa, and I've watched the same story play out over and over.

A team ships a genuinely useful tool. The docs look fine. The API is well-tested. And adoption still flatlines. The getting-started path takes 45 minutes instead of 15. The error message says `Authentication failed` and nothing else. The quickstart quietly assumes you have a Postgres instance running. A first-time contributor's PR sits unreviewed for a month and they never come back.

None of that shows up in a feature backlog. All of it decides whether developers stay.

The frustrating part: these failures are predictable. I've seen the same handful of patterns separate tools people adopt from tools people abandon, across companies and across decades. This repo is those patterns, turned into skills an agent can actually run against your repo. Not essays. Checks.

- **The 15-minute magic path.** A brand-new developer with zero product knowledge reaches a verified, end-to-end outcome in fifteen minutes or less. If they can't, you have a problem, no matter how good the docs read.
- **Errors are product surface.** "Authentication failed" costs you a user. "Token expired 37 minutes ago. Run `conduit auth login`, or set CONDUIT_API_TOKEN. Request ID: req_01K98..." keeps one.
- **Authors and auditors are different people.** I've watched good teams ship stale quickstarts and contradictory SDKs because the person who wrote the docs also judged them. So every surface here gets a builder *and* an auditor, and the auditor's job is to try to prove the thing broken.
- **Evidence beats vibes.** Timings are Observed, CI-observed, or Estimated. An estimate never proves a PASS, and no pretty score overrides a failing gate.

## The methodology

All forty-two skills share one constitution, `dx-standards/`, synced into every skill's `references/standards.md`. Four rules hold it together:

- **Named SLOs, each with an owner.** Magic path ≤15 min, clone-to-productive ≤10 min, community onboarding ≤30 min, Time to Recovery ≤5 min, explicit feedback budgets. Every constant has one home and one owning skill; skills cite constants by name, never restate values.
- **Named gates.** `BROKEN_QUICKSTART`, `UNEXPLAINED_ERROR`, `UNDOCUMENTED_BREAKING_API`, `NO_CONTRIBUTING_WHILE_WELCOMING`, and the rest. A failing gate fails the release; a score never averages it away.
- **The loop.** Build with the surface's design skill, audit with its audit skill (or the end-to-end `developer-experience-auditor`), fix the right layer, gate the release. Findings get classified by root cause: Product, API, CLI, SDK, Configuration, Environment, Documentation, Infrastructure, Third-party. Because three paragraphs of docs never fixed a bad API.
- **One vocabulary.** Fourteen journey stages, nine problem classes, one severity scale (P0–P4), one verdict vocabulary (PASS / PASS WITH DEBT / FAIL / UNVERIFIED). CHAOSS metric names for community, Diátaxis for documentation architecture, SemVer for compatibility.

## The core standard: magic in 15 minutes

A brand-new developer with **zero product knowledge** should be able to open the canonical Quickstart and reach a **meaningful, verified, end-to-end product outcome in 15 minutes or less**.

I mean this literally. The timer includes installation, signup and authentication when required, configuration, execution, waiting, and verification. And no, you can't move the slow parts into a "prerequisites" section to make the metric pass. If production setup needs manual approval or slow provisioning, ship a sandbox, local mode, test environment, or seeded fixtures. Products that respect this get adopted; products that don't get blogged about.

| Time to verified end-to-end value | Rating |
|---|---|
| ≤5 min | Exceptional |
| >5 to ≤10 min | Strong |
| >10 to ≤15 min | Pass |
| >15 min | **P1 onboarding/DX failure** |
| No reproducible E2E quickstart | **P1 failure** |

No verdict can be **world-class** while this gate fails, regardless of how good the prose or reference coverage is.

## Install

The repository is packaged as a Claude Code plugin (`developer-docs-skills`) that installs all forty-two skills at once:

```bash
claude plugin marketplace add devarispbrown/devex-skills
claude plugin install developer-docs-skills@devex-skills
```

Or interactively from inside Claude Code:

```text
/plugin marketplace add devarispbrown/devex-skills
/plugin install developer-docs-skills@devex-skills
```

Claude invokes skills automatically from their descriptions, or explicitly with `/developer-docs`, `/developer-experience-auditor`, and so on.

**Manual copy**: every skill directory is self-contained (including its generated `references/standards.md`), so any subset can be copied into `<your-repo>/.claude/skills/<skill-name>/` or `~/.claude/skills/<skill-name>/`, or into any Agent Skills-compatible client. Cross-skill references are by name only ("if available"), so a skill installed alone still works.

## The 10-minute quickstart

Don't read the rest of this page yet. Three steps:

1. Install the plugin (commands above).
2. Ask Claude: "run `developer-experience-auditor` on this repo."
3. Read the DX Report.

That's the lay of the land. You do not need to learn forty-two skills. You need one. The report gives you a verdict, magic-path timing, per-area scores, and a prioritized backlog of gate failures, and every P1 names the skill that fixes it. That's how you discover the rest of the suite: by the problem in front of you, not by the catalog.

Then it's a loop:

- **Fix** the P1s with the named skills.
- **Re-run** the auditor and watch the score move.
- **Gate every release** with `release-guardian` and `developer-docs-auditor`; a release fails when a hard gate fails.

Running an open-source project? Same pattern: start with `developer-community-auditor` instead. The Community Health Report works exactly the same way: gates, owners, backlog.

**Want to know whether AI agents can use what you built?** Same three steps, different skill:

1. Install the plugin (commands above).
2. Ask Claude: "run `agent-native-dx` on this repo."
3. Read the readiness report.

It scores nineteen agent-facing surfaces, grouped by the three questions that decide whether an agent can work in your repository at all: can it find its way around, can it operate the product, can it do the work. You get a percentage, a band, and a per-surface list of what is missing.

Measured across fifteen public repositories in six ecosystems, scores ran from 79 percent down to 21 percent, so a low score means something. The most common substantive gap was CI parity: thirteen of fifteen gave no way to tell that a green local run predicts a green CI run. A human notices the CI email. An unattended agent does not, so it either ships broken work or burns cycles guessing.

## Skills by surface

Pick the surface you're building today.

### Getting started

| Skill | Role | One-liner |
|---|---|---|
| `developer-onboarding` | Build | Design zero-to-value onboarding: install modes, step elimination, sandbox-first magic paths |
| `developer-docs` | Build | Author quickstarts, READMEs, tutorials with Diátaxis architecture, truth before prose |
| `developer-docs-auditor` | Audit | Prove docs wrong, stale, or non-executable; gate documentation releases |
| `golden-path-scaffolder` | Build | Turn repeated workflows into generators |
| `reference-application-engineer` | Build | Production-grade example apps demonstrating auth, config, retries, shutdown |
| `sandbox-experience` | Audit | Verify every risky learning task has a safe, resettable sandbox route |

Tools: `estimate_magic_path.py`, `magic_path_runner.py`, `check_sandbox_coverage.py`, `check_reference_app.py`

### API

| Skill | Role | One-liner |
|---|---|---|
| `api-design-reviewer` | Audit | API-as-product review: guessability, consistency, reliability semantics; API DX score separate from OpenAPI correctness |
| `sdk-engineer` | Build | Idiomatic Go/Python/TypeScript/Rust SDKs with semantic parity |
| `developer-economics` | Audit | Rate limits, quotas, and pricing as predictable API behavior |
| `error-experience` | Build | Six-question error standard: what, why, where, fix, retry-safe, correlation |

Tools: `check_openapi_shape.py`, `guessability_check.py`, `check_parity.py`, `check_quota_surface.py`

### CLI

| Skill | Role | One-liner |
|---|---|---|
| `cli-designer` | Build | Command hierarchy, output contract, exit codes, automation modes: great for humans, stable for scripts |
| `configuration-dx` | Build | Config as public API: deterministic precedence, validation, secrets handling |
| `accessibility-dx` | Audit | No red/green-only errors; terminal output consumable by screen readers |

Tools: `check_cli_surface.py`, `check_config_surface.py`, `check_cli_colors.py`

### Errors and support

| Skill | Role | One-liner |
|---|---|---|
| `error-experience` | Build | Six-question error standard across API, CLI, SDK, diagnostics |
| `developer-support` | Build | Route bug/how-to/security/billing to the right channel; escalation ladder; automatic diagnostics |
| `developer-feedback-analyst` | Audit | Cluster issue/chat/telemetry signals into journeys, size impact, hand off fixes |

Tools: `error_inventory.py`, `scan_support_channels.py`, `cluster_feedback.py`

### Local development

| Skill | Role | One-liner |
|---|---|---|
| `local-development` | Build | Clone→productive in ≤10 minutes: toolchains, services, fixtures, dev targets |
| `ide-experience` | Build | .vscode, launch/tasks, LSP, schema autocompletion |
| `test-data-and-fixtures` | Build | Fixtures, seeds, mock servers, record-replay, sanitization |
| `developer-workflow-auditor` | Audit | Inner/outer feedback loops vs explicit budgets: formatter 2s, compile 5s, unit 10s, CI signal 3min |
| `performance-engineer` | Audit | Performance budgets: benchmark, profile, bisect, gate regressions |

Tools: `check_local_dev.py`, `check_ide_config.py`, `check_fixture_hygiene.py`, `audit_feedback_loops.py`, `check_perf_budgets.py`

### Tests and quality

| Skill | Role | One-liner |
|---|---|---|
| `quality-engineer` | Build | Test strategy by system type: contracts, property/fuzz, failure injection |
| `integration-certifier` | Audit | Prove claimed integrations work, per version, with evidence and expiry |
| `dependency-health` | Audit | Dependencies as policy: inventory, classification, upgrade cadence |
| `security-supply-chain` | Audit | SECURITY.md, workflow permissions, signing, provenance, SBOM, SAST |

Tools: `assess_test_suite.py`, `check_certifications.py`, `check_dependency_health.py`, `check_security_posture.py`

### Releases and compatibility

| Skill | Role | One-liner |
|---|---|---|
| `release-guardian` | Audit | Gate releases: diff classification, behavioral compatibility, SemVer, migrations |
| `change-awareness` | Build | Changelogs, deprecations, migration notices: who, action, deadline, reach |
| `compatibility-engineer` | Audit | Compatibility matrix with CI evidence: upgrades, wire compat, schema evolution |
| `environment-lifecycle` | Build | Preview/staging environments, TTL, seed data, promotion |

Tools: `classify_diff.py`, `scan_compat_consumers.py`, `check_change_notices.py`, `check_compat_matrix.py`, `check_environment_lifecycle.py`

### Operations and trust

| Skill | Role | One-liner |
|---|---|---|
| `observability-readiness` | Build | Logs, metrics, traces, correlation IDs so you can diagnose at 2am without new instrumentation |
| `operational-trust` | Build | Status pages, incident comms, SLO publication, so users can tell "is it you or is it me" |
| `access-and-permissions-dx` | Build | Auth/RBAC as self-service: the 403-explanation standard |
| `policy-experience` | Build | Policy-as-code, guardrails, self-service exceptions instead of Jira ticket-ops |
| `web-console-dx` | Audit | Console friction: every UI operation maps to an API/CLI equivalent |

Tools: `check_observability.py`, `check_trust_surface.py`, `check_403_explanations.py`, `check_policy_actionability.py`, `check_console_ops.py`

### Community and ecosystem

| Skill | Role | One-liner |
|---|---|---|
| `developer-community` | Build | Contribution system: governance, ladder, recognition, automation |
| `developer-community-auditor` | Audit | Community Health Score, funnel analytics, responsiveness SLOs, gates |
| `contributor-experience` | Audit | First contribution <30 minutes: funnel, guidance files, check parity |
| `extensibility-engineer` | Build | Plugin/connector author experience: stability, isolation, scaffolding |

Tools: `scan_community_surface.py`, `check_community_health.py`, `check_contributor_funnel.py`, `check_extension_surface.py`

### Agents and measurement

| Skill | Role | One-liner |
|---|---|---|
| `developer-experience-auditor` | Audit | Orchestrator: 14-stage journey audits, DX Report, delegates to specialist skills |
| `agent-native-dx` | Build | Make your tool excellent for coding agents: AGENTS.md, schemas, structured output |
| `experimentation-engineer` | Audit | Run DX experiments on quickstarts, CLI variants, onboarding flows |
| `architecture-experience` | Audit | Architecture Magic Path: where does a feature belong, traced end-to-end |
| `developer-discoverability` | Build | Catalogs: make APIs, owners, versions findable |

Tools: `journey_runner.py`, `check_agent_readiness.py`, `check_experiment_metrics.py`, `estimate_architecture_path.py`, `check_catalog_metadata.py`

## The standards

The numbers below are why the skills can trust each other's verdicts. They live in `dx-standards/`, the suite's single source of truth, synced into each skill's `references/standards.md`:

| SLO | Value | Owned by |
|---|---|---|
| Magic path | **≤15 min** | `developer-onboarding` (design) / `developer-experience-auditor` (measure) |
| Local development | **≤10 min** | `local-development` |
| Community onboarding | **≤30 min** | `developer-community-auditor` |
| Architecture comprehension | **≤30 min** | `architecture-experience` |
| Time to Recovery | **≤5 min** | `error-experience` |
| Feedback budgets | 2s–10min per loop | `developer-workflow-auditor` |
| Community response SLOs | P50/P90 per channel | `developer-community-auditor` |

Hard gates carry names: `BROKEN_QUICKSTART`, `NON_REPRODUCIBLE_BUILD`, `UNEXPLAINED_ERROR`, `UNDOCUMENTED_BREAKING_API`, `SDK_API_DRIFT`, `UNTESTED_SUPPORTED_VERSION`, and the community gates (`NO_CONTRIBUTING_WHILE_WELCOMING`, `UNRESPONSIVE_ISSUES`, `STALE_GOOD_FIRST_ISSUES`, `UNACKNOWLEDGED_PRS`, `NO_LICENSE`, and more). The full SLO table lives in `dx-standards/slo.md`.

Evidence is labeled **Observed**, **CI-observed**, or **Estimated**; an estimate can never prove a PASS. Verdicts are exactly **PASS**, **PASS WITH DEBT**, **FAIL**, or **UNVERIFIED**, and a high score never overrides a failing gate.

## Repository layout

```text
devex-skills/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .claude-plugin/
│   ├── marketplace.json          # marketplace manifest: makes the repo installable
│   └── plugin.json               # plugin manifest: the 42 skill entries
├── dx-standards/                 # canonical standards: source of truth
│   ├── principles.md  metrics.md  severity.md  release-gates.md
│   ├── compatibility.md  terminology.md  community.md  slo.md  domains.md
│   ├── magic-path.md  api-dx.md  sdks.md  lifecycle.md  llm-ready-docs.md  style.md
│   ├── inventory_docs.py
│   ├── sync-map.json             # maps standards sections to skill files
│   └── README.md
├── scripts/
│   ├── sync-standards.py         # distribute standards into skills
│   ├── validate_skills.py        # suite structural lint
│   └── smoke_skills.py           # per-skill fixture smoke tests
├── .github/workflows/ci.yml      # drift + structure + smoke enforcement
├── trials/                       # pre-registered agent trials and their logs
└── skills/                       # 42 self-contained skill directories
```

## Shared standards and sync

`dx-standards/` is the single source of truth for the suite's vocabulary and thresholds. `scripts/sync-standards.py` writes each skill's subset into its `references/standards.md`; the generated files are committed, so every skill directory stays self-contained.

```bash
python3 scripts/sync-standards.py           # regenerate all targets
python3 scripts/sync-standards.py --check   # exit 1 on drift
```

Generated files carry a header. Never hand-edit them. Change the source in `dx-standards/` and re-sync. Hand-written skill references are procedural only; normative numbers always flow through the standards layer. CI enforces sync cleanliness, structural lint, compilation, and fixture smoke tests on every push. See `CHANGELOG.md` for release history.

## Contributing

Contributions should improve a repeatable developer outcome rather than merely add more prose.

Useful contributions include:

- additional language-specific documentation and SDK tests
- better OpenAPI/AsyncAPI/protobuf/GraphQL parity checks
- SDK coverage tooling
- CLI/config drift checks
- quickstart measurement patterns
- new documentation templates
- real-world examples of Product/DX defects discovered through developer-experience work

When changing a skill, keep the main `SKILL.md` focused and move detailed specialist guidance into `references/` so agents can load it progressively. Keep normative numbers in `dx-standards/` and re-run `python3 scripts/sync-standards.py`.

## References and influences

- [Diátaxis](https://diataxis.fr/)
- [Agent Skills open specification](https://agentskills.io/)
- [Anthropic: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [DORA platform engineering capabilities](https://dora.dev/capabilities/platform-engineering/)
- [CHAOSS community health metrics](https://chaoss.community/kb-metrics-and-metrics-models/)
- [CNCF contributor and governance guidance](https://contribute.cncf.io/)
- [Semantic Versioning](https://semver.org/)
- [Command Line Interface Guidelines](https://clig.dev/)
- [OpenSSF Scorecard](https://www.scorecard.dev/)
- [OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/)
- [Backstage Software Catalog and Templates](https://backstage.io/)
- [OpenFeature](https://openfeature.dev/)
- [GitHub dev containers](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers)
- [Stripe documentation and sandboxes](https://docs.stripe.com/)
- [Twilio documentation](https://www.twilio.com/docs)

Stripe and Twilio are used as quality references for developer-first onboarding, consistent API concepts, language-specific examples, errors, authentication, and self-service integration patterns. The skills are not affiliated with either company.

## License

MIT
