# Developer Experience Skills Suite

Forty-two complementary Claude/Agent Skills covering the full developer lifecycle — discover, build, validate, ship, participate, improve — backed by one shared constitution of measurable DX standards.

## Find your skill

| You want to... | Use |
|---|---|
| Write or restructure documentation | `developer-docs` |
| Prove documentation is wrong or stale | `developer-docs-auditor` |
| Audit the entire developer journey | `developer-experience-auditor` |
| Design a ≤15-minute onboarding path | `developer-onboarding` |
| Design or audit the contribution system | `developer-community` / `developer-community-auditor` |
| Make a fresh clone productive fast | `local-development` |
| Review an API as a product | `api-design-reviewer` |
| Build idiomatic SDKs | `sdk-engineer` |
| Design or audit a CLI | `cli-designer` |
| Fix configuration UX | `configuration-dx` |
| Make errors actionable | `error-experience` |
| Speed up inner/outer feedback loops | `developer-workflow-auditor` |
| Give users a safe place to experiment | `sandbox-experience` |
| Help developers form a mental model | `architecture-experience` |
| Make things findable | `developer-discoverability` |
| Route post-self-service help | `developer-support` |
| Fix auth/RBAC ergonomics | `access-and-permissions-dx` |
| Make policy compliance self-service | `policy-experience` |
| Gate a release | `release-guardian` |
| Keep compatibility claims honest | `compatibility-engineer` |
| Build test strategy by system type | `quality-engineer` |
| Harden OSS supply chain | `security-supply-chain` |
| Make failures diagnosable at 2am | `observability-readiness` |
| Build consumer trust in operations | `operational-trust` |
| Announce changes developers will hit | `change-awareness` |
| Manage preview/staging environments | `environment-lifecycle` |
| Make pricing and quotas predictable | `developer-economics` |
| Design extension/plugin ecosystems | `extensibility-engineer` |
| Improve first-time OSS contribution | `contributor-experience` |
| Manage dependencies as policy | `dependency-health` |
| Prove integrations actually work | `integration-certifier` |
| Make a product excellent for coding agents | `agent-native-dx` |
| Turn feedback into DX improvements | `developer-feedback-analyst` |
| Run DX experiments safely | `experimentation-engineer` |
| Make developer surfaces accessible | `accessibility-dx` |
| Keep performance within budgets | `performance-engineer` |
| Author production-grade examples | `reference-application-engineer` |
| Generate project/connector templates | `golden-path-scaffolder` |
| Make IDEs excellent | `ide-experience` |
| Author fixtures and test data | `test-data-and-fixtures` |
| Remove dashboard/portal friction | `web-console-dx` |

## The core standards

Every skill references the same shared thresholds from `dx-standards/` (synced into each skill's `references/standards.md`):

| SLO | Value | Owned by |
|---|---|---|
| Magic path | **≤15 min** | `developer-onboarding` (design) / `developer-experience-auditor` (measure) |
| Local development | **≤10 min** | `local-development` |
| Community onboarding | **≤30 min** | `developer-community-auditor` |
| Architecture comprehension | **≤30 min** | `architecture-experience` |
| Time to Recovery | **≤5 min** | `error-experience` |
| Feedback budgets | 2s–10min per loop | `developer-workflow-auditor` |
| Community response SLOs | P50/P90 per channel | `developer-community-auditor` |

Hard gates carry names — `BROKEN_QUICKSTART`, `NON_REPRODUCIBLE_BUILD`, `UNEXPLAINED_ERROR`, `UNDOCUMENTED_BREAKING_API`, `SDK_API_DRIFT`, `UNTESTED_SUPPORTED_VERSION`, and the community gates (`NO_CONTRIBUTING_WHILE_WELCOMING`, `UNRESPONSIVE_ISSUES`, `STALE_GOOD_FIRST_ISSUES`, `UNACKNOWLEDGED_PRS`, `NO_LICENSE`, and more). The full SLO table with every constant and owner lives in `dx-standards/slo.md`.

Evidence is labeled **Observed**, **CI-observed**, or **Estimated**; an estimate can never prove a PASS. Verdicts are exactly **PASS**, **PASS WITH DEBT**, **FAIL**, or **UNVERIFIED**, and a high score never overrides a failing gate.

### The core standard: magic in 15 minutes

A brand-new developer with **zero product knowledge** should be able to open the canonical Quickstart and reach a **meaningful, verified, end-to-end product outcome in 15 minutes or less**.

This is a hard quality gate, not a writing guideline. The timer includes product-specific installation, signup/authentication when required, configuration, execution, waiting, and verification. Setup cannot be moved into a prerequisites section to game the metric. If production setup requires manual approval or slow provisioning, the product should provide a sandbox, local mode, test environment, or seeded fixture.

| Time to verified end-to-end value | Rating |
|---|---|
| ≤5 min | Exceptional |
| >5 to ≤10 min | Strong |
| >10 to ≤15 min | Pass |
| >15 min | **P1 onboarding/DX failure** |
| No reproducible E2E quickstart | **P1 failure** |

No verdict can be **world-class** while this gate fails, regardless of how good the prose or reference coverage is.

## The six domains

### Learn & Adopt

| Skill | One-liner |
|---|---|
| `developer-docs` | Author world-class docs: Diátaxis architecture, quickstarts, API/SDK/CLI/config docs, READMEs |
| `developer-onboarding` | Design zero-to-value onboarding: install modes, step elimination, sandbox-first magic paths |
| `golden-path-scaffolder` | Turn repeated workflows into generators: contracts, templates, output wiring |
| `architecture-experience` | Accelerate mental-model formation: the Architecture Magic Path |
| `developer-discoverability` | Make APIs, services, owners, and docs findable: catalogs with lifecycle metadata |
| `reference-application-engineer` | Production-grade reference apps demonstrating the nine mandatory concerns |
| `developer-economics` | Pricing, limits, and quotas as predictable API behavior |

Tools: `check_catalog_metadata.py`, `estimate_architecture_path.py`, `check_quota_surface.py`, `check_reference_app.py`

### Build

| Skill | One-liner |
|---|---|
| `api-design-reviewer` | Review an API as a product: guessability, consistency, API DX score |
| `sdk-engineer` | Idiomatic Go/Python/TypeScript/Rust SDKs with semantic parity |
| `cli-designer` | CLIs as products: hierarchy, output contract, exit codes, automation modes |
| `configuration-dx` | Config as public API: precedence, defaults, validation, secrets handling |
| `error-experience` | Six-question error standard, per-surface contracts, Time to Recovery |
| `local-development` | Clone→productive in ≤10 minutes: toolchains, services, fixtures, dev targets |
| `ide-experience` | IDE configuration: .vscode, launch/tasks, LSP, schema autocompletion |
| `test-data-and-fixtures` | Fixtures, seeds, mock servers, record-replay, golden files, sanitization |
| `developer-workflow-auditor` | Inner/outer feedback loops vs explicit feedback budgets |
| `accessibility-dx` | Accessible docs, portals, consoles, terminals: no red/green-only signaling |
| `agent-native-dx` | Make products excellent for coding agents: AGENTS.md, schemas, structured output |

Tools: `check_openapi_shape.py`, `guessability_check.py`, `check_parity.py`, `check_local_dev.py`, `check_ide_config.py`, `check_fixture_hygiene.py`, `audit_feedback_loops.py`, `check_cli_colors.py`

### Validate

| Skill | One-liner |
|---|---|
| `developer-docs-auditor` | Adversarially audit and release-gate documentation: drift, parity, scoring |
| `quality-engineer` | Test strategy by system type: contracts, property/fuzz, failure injection |
| `integration-certifier` | Verify claimed integrations: certification matrix with evidence and expiry |
| `dependency-health` | Dependencies as policy: inventory, classification, upgrade cadence |
| `security-supply-chain` | Harden OSS posture: SECURITY.md, workflow permissions, signing, SBOM, SAST |
| `sandbox-experience` | Safe experimentation: sandbox coverage gate for risky learning tasks |

Tools: `assess_test_suite.py`, `check_certifications.py`, `check_dependency_health.py`, `check_sandbox_coverage.py`

### Ship & Operate

| Skill | One-liner |
|---|---|
| `release-guardian` | Gate releases: diff classification, behavioral compatibility, SemVer, migrations |
| `compatibility-engineer` | Compatibility matrix with CI evidence: upgrades, wire compat, schema evolution |
| `observability-readiness` | Logs, metrics, traces, correlation IDs: diagnose without new instrumentation |
| `operational-trust` | Status pages, incident comms, SLO publication, webhook reliability |
| `change-awareness` | Changelogs, migration notices, deprecations: who, action, deadline, reach |
| `environment-lifecycle` | Local→production path: ephemeral/PR environments, TTL, seed, promotion |
| `developer-support` | Post-self-service routing, escalation ladder, automatic diagnostics |
| `access-and-permissions-dx` | Auth/RBAC as self-service: the 403-explanation standard |
| `policy-experience` | Policy-as-code, guardrails, self-service exceptions, actionable violations |
| `web-console-dx` | Console friction audit: automation parity for every UI operation |

Tools: `classify_diff.py`, `scan_compat_consumers.py`, `check_compat_matrix.py`, `check_trust_surface.py`, `check_change_notices.py`, `check_environment_lifecycle.py`, `scan_support_channels.py`, `check_403_explanations.py`, `check_policy_actionability.py`, `check_console_ops.py`

### Participate & Extend

| Skill | One-liner |
|---|---|
| `developer-community` | Contribution-system design: governance, onboarding, recognition, operations |
| `contributor-experience` | First contribution <30 min: funnel, guidance files, check parity |
| `extensibility-engineer` | Plugin/connector/hook author experience: stability, isolation, scaffolding |

Tools: `scan_community_surface.py`, `check_contributor_funnel.py`, `check_extension_surface.py`

### Measure & Improve

| Skill | One-liner |
|---|---|
| `developer-experience-auditor` | Orchestrator: 14-stage journey audits, DX Report, delegates to specialist skills |
| `developer-feedback-analyst` | Cluster feedback signals into journeys, size impact, hand off fixes |
| `developer-community-auditor` | Community Health Score, funnel analytics, responsiveness SLOs, gates |
| `experimentation-engineer` | DX experiments: quickstarts, CLI variants, onboarding flows |
| `performance-engineer` | Performance budgets: benchmark, profile, bisect, gate regressions |

Tools: `journey_runner.py`, `magic_path_runner.py`, `cluster_feedback.py`, `check_community_health.py`, `check_experiment_metrics.py`, `check_perf_budgets.py`

The canonical domain map lives in `dx-standards/domains.md`.

## Install

### Claude Code plugin

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

### Claude Code manual copy

Every skill directory is self-contained — including its generated `references/standards.md` — so any subset can be copied directly.

For a project-scoped install:

```text
<your-repo>/.claude/skills/<skill-name>/
```

For a personal install that is available across projects:

```text
~/.claude/skills/<skill-name>/
```

### Other Agent Skills-compatible clients

Copy each skill directory as-is into the client's Agent Skills directory. Each contains a required `SKILL.md` plus optional `references/`, `assets/`, and `scripts/` that are loaded progressively as needed. Cross-skill references are by name only ("if available"), so a skill installed alone still works.

## Recommended workflows

### Author → Audit → Gate

1. **Author** with `developer-docs` and `developer-onboarding`. Start from product truth, design the canonical magic path, then add how-to, reference, explanation, troubleshooting, and production material.
2. **Audit** with `developer-experience-auditor` (whole journey) and `developer-docs-auditor` (documentation correctness). Execute what can safely be executed and label all evidence.
3. **Fix the right layer.** Findings are classified into nine problem classes — Product, API, CLI, SDK, Configuration, Environment, Documentation, Infrastructure, Third-party. Do not add three paragraphs of documentation to compensate for a bad API.
4. **Gate releases** with `release-guardian` (product contract) and `developer-docs-auditor` (docs contract). A release fails when a hard gate fails.

### Community loop

Design the contribution system with `developer-community`, keep the funnel healthy with `contributor-experience`, and measure it continuously with `developer-community-auditor`. Repeated questions feed `developer-docs`; unexplained errors feed `error-experience`; confusing configuration feeds `configuration-dx`. The suite is a continuous improvement system, not a collection of prompts.

### Feedback loops

`developer-feedback-analyst` clusters behavior signals into journeys; `experimentation-engineer` tests candidate fixes safely; `developer-workflow-auditor` protects the inner loop while you work. Each skill hands findings to the surface skill that owns the fix, with evidence and an acceptance test.

## Repository layout

```text
devex-skills/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .claude-plugin/plugin.json
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
└── skills/                       # 42 self-contained skill directories
```

## Shared standards and sync

`dx-standards/` is the single source of truth for the suite's vocabulary and thresholds. `scripts/sync-standards.py` writes each skill's subset into its `references/standards.md`; the generated files are committed, so every skill directory stays self-contained.

```bash
python3 scripts/sync-standards.py           # regenerate all targets
python3 scripts/sync-standards.py --check   # exit 1 on drift
```

Generated files carry a header — never hand-edit them. Change the source in `dx-standards/` and re-sync. Hand-written skill references are procedural only; normative numbers always flow through the standards layer. CI enforces sync cleanliness, structural lint, compilation, and fixture smoke tests on every push. See `CHANGELOG.md` for release history.

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
