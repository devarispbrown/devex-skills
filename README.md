# Developer Experience Skills Suite

Twenty-two complementary Claude/Agent Skills covering the full developer lifecycle, backed by one shared constitution of measurable DX standards.

The suite splits naturally into authoring, auditing, and product-surface skills:

- **Author**: `developer-docs`, `developer-onboarding`, `sdk-engineer`
- **Audit**: `developer-docs-auditor`, `developer-experience-auditor`
- **Product surface**: `api-design-reviewer`, `local-development`, `error-experience`, `quality-engineer`, `release-guardian`, `cli-designer`, `configuration-dx`, `security-supply-chain`, `observability-readiness`, and more

The `developer-experience-auditor` is the orchestration layer: it runs the entire developer journey adversarially and delegates deep dives to the specialized skills when they are available.

## The core standards

Every skill references the same shared thresholds from `dx-standards/` (synced into each skill's `references/standards.md`):

| Standard | Value | Meaning |
|---|---|---|
| Magic path | **≤15 min** | a brand-new developer with zero product knowledge reaches a verified, meaningful, end-to-end product outcome |
| Local development | **≤10 min** | a clean clone reaches the productive state (tests run, dev loop exercised) |
| First contribution | **≤30 min** | fork to first PR-ready change (target, not a hard gate) |
| Time to Recovery | **≤5 min** | from hitting an expected error to completing its corrective action |

Hard gates carry names: `BROKEN_QUICKSTART`, `NON_REPRODUCIBLE_BUILD`, `UNEXPLAINED_ERROR`, `UNDOCUMENTED_BREAKING_API`, `SDK_API_DRIFT`, `UNTESTED_SUPPORTED_VERSION`.

Evidence is always labeled **Observed**, **CI-observed**, or **Estimated**. An estimate can never prove a PASS. Verdicts are exactly **PASS**, **PASS WITH DEBT**, **FAIL**, or **UNVERIFIED**, and a high score can never override a failing gate.

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

## Skill index

| Skill | What it does | Use instead |
|---|---|---|
| `developer-docs` | Author world-class docs: Diátaxis architecture, quickstarts, API/SDK/CLI/config docs, READMEs, examples, lifecycle | `developer-experience-auditor` for product/DX measurement |
| `developer-docs-auditor` | Adversarially audit and release-gate documentation: drift, executable examples, parity, scoring | `developer-experience-auditor` for whole-product DX |
| `developer-experience-auditor` | Run the full 14-stage developer journey, measure friction, score DX, produce the DX Report; orchestrates the other skills | `developer-docs-auditor` for documentation-only audits |
| `developer-onboarding` | Design zero-to-value onboarding: install modes, step elimination, sandbox-first magic paths | `developer-experience-auditor` to validate a path |
| `api-design-reviewer` | Review an API as a product: guessability, consistency, reliability semantics; API DX score separate from OpenAPI correctness | `developer-docs-auditor` for docs parity |
| `local-development` | Make clone→productive boring: toolchains, services, fixtures, dev targets, reproducibility | `developer-onboarding` for onboarding design |
| `sdk-engineer` | Design idiomatic Go/Python/TypeScript/Rust SDKs with semantic parity and capability matrices | `api-design-reviewer` for the API surface |
| `error-experience` | Six-question error standard, per-surface contracts, Time to Recovery | `api-design-reviewer` for error-model design |
| `quality-engineer` | Test strategy by system type: contracts, property/fuzz, failure injection | `release-guardian` for gate decisions |
| `release-guardian` | Gate releases: diff classification, behavioral compatibility, SemVer recommendation, migrations | `developer-docs-auditor` for docs release gating |
| `cli-designer` | Design CLIs as products: hierarchy, flags, output contract, exit codes, automation modes | `error-experience` for error text |
| `security-supply-chain` | Harden OSS posture: SECURITY.md, workflow permissions, signing, provenance, SBOM, SAST, fuzzing | `dependency-health` for upgrade hygiene |
| `observability-readiness` | Logs, metrics, traces, correlation IDs, health checks, SLOs: diagnose without new instrumentation | `error-experience` for error semantics |
| `configuration-dx` | Config as public API: precedence, defaults, validation, secrets handling | `release-guardian` for config compat |
| `golden-path-scaffolder` | Turn repeated workflows into generators: contracts, templates, output wiring | `developer-onboarding` for the path generated projects serve |
| `performance-engineer` | Performance budgets: benchmark, profile, bisect, gate regressions | `local-development` for loop speed |
| `compatibility-engineer` | Compatibility matrix with CI evidence: upgrades, wire compat, schema evolution | `release-guardian` for versioning decisions |
| `contributor-experience` | First contribution <30 min: funnel, guidance files, check parity, review health | `local-development` for the setup itself |
| `dependency-health` | Dependencies as policy: inventory, classification, upgrade cadence | `security-supply-chain` for vulnerabilities |
| `integration-certifier` | Verify claimed integrations: certification matrix with evidence and expiry | `compatibility-engineer` for version ranges |
| `agent-native-dx` | Make products excellent for coding agents: AGENTS.md, schemas, structured output | `developer-docs` for human-facing docs |
| `developer-feedback-analyst` | Cluster feedback signals into journeys, size impact, hand off fixes | relevant surface skill for the fix |

## Repository layout

```text
devex-skills/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .claude-plugin/plugin.json
├── dx-standards/                 # canonical standards: source of truth
│   ├── principles.md  metrics.md  severity.md  release-gates.md
│   ├── compatibility.md  terminology.md  magic-path.md
│   ├── api-dx.md  sdks.md  lifecycle.md  llm-ready-docs.md  style.md
│   ├── inventory_docs.py
│   ├── sync-map.json             # maps standards sections to skill files
│   └── README.md
├── scripts/
│   ├── sync-standards.py         # distribute standards into skills
│   └── validate_skills.py        # suite structural lint
├── .github/workflows/ci.yml      # drift + structure enforcement
└── skills/
    ├── developer-docs/
    ├── developer-docs-auditor/
    ├── developer-experience-auditor/
    ├── developer-onboarding/
    ├── api-design-reviewer/
    ├── local-development/
    ├── sdk-engineer/
    ├── error-experience/
    ├── quality-engineer/
    └── release-guardian/
```

There is intentionally **no README inside any skill directory**. Agent Skills use `SKILL.md` as the entry point; the repository-level README is for humans browsing the OSS project.

## Install

### Claude Code plugin

The repository is packaged as a Claude Code plugin (`developer-docs-skills`) that installs all ten skills at once:

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
4. **Gate releases** with `release-guardian` (product contract) and `developer-docs-auditor` (docs contract). A release fails when a hard gate fails, including a broken magic path, stale public reference, broken canonical install/auth, unsafe examples, or missing migration guidance.

### Onboarding → Local dev → DX audit

Design the zero-to-value path with `developer-onboarding`, make the clone experience boring with `local-development`, then measure both against their SLOs with `developer-experience-auditor`.

## Deterministic tools

The suite ships small dependency-free helpers intended to complement, not replace, repository-native CI:

| Tool | Skill | Purpose |
|---|---|---|
| `magic_path_runner.py` | docs-auditor | Execute and time a magic-path manifest (`--execute` opt-in, no shell) |
| `journey_runner.py` | experience-auditor | Orchestrate the 14-stage journey and produce timing/counts |
| `estimate_magic_path.py` | onboarding | Estimate a design against `MAGIC_PATH_MAX_MIN` without executing |
| `check_openapi_shape.py` / `guessability_check.py` | api-design-reviewer | Structural OpenAPI lint and convention candidates |
| `check_parity.py` | sdk-engineer | Find operations missing from an SDK source tree |
| `check_local_dev.py` | local-development | Inventory setup surfaces (never fails) |
| `error_inventory.py` | error-experience | Catalog error sources by surface |
| `assess_test_suite.py` | quality-engineer | Map test coverage to system-type gaps |
| `classify_diff.py` / `scan_compat_consumers.py` | release-guardian | Heuristic change classification and consumer scan |
| `sync-standards.py` | repo | Distribute `dx-standards/` into skill `references/`; `--check` detects drift |
| `validate_skills.py` | repo | Structural lint: plugin/directory/frontmatter agreement, versions, mentions |

For snippets, schemas, SDKs, CLI help, and integration examples, prefer the target project's actual compiler, test runner, schema tooling, code generator, and sandbox infrastructure.

## Shared standards and sync

`dx-standards/` is the single source of truth for the suite's vocabulary and thresholds. `scripts/sync-standards.py` writes each skill's subset into its `references/standards.md`; the generated files are committed, so every skill directory stays self-contained.

```bash
python3 scripts/sync-standards.py           # regenerate all targets
python3 scripts/sync-standards.py --check   # exit 1 on drift
```

Generated files carry a header — never hand-edit them. Change the source in `dx-standards/` and re-sync. Hand-written skill references are procedural only; normative numbers always flow through the standards layer. CI enforces both sync cleanliness and structural lint on every push.

## Roadmap

The strategy for this suite covers the whole developer lifecycle. Planned skills, in rough priority order:

```text
developer-community          developer-community-auditor
developer-workflow-auditor   sandbox-experience
architecture-experience      developer-discoverability
developer-support            access-and-permissions-dx
extensibility-engineer       developer-economics
environment-lifecycle        change-awareness
operational-trust            test-data-and-fixtures
ide-experience               policy-experience
web-console-dx               experimentation-engineer
accessibility-dx             reference-application-engineer
```

Contributions that advance any of these are welcome; see below.

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
- [Semantic Versioning](https://semver.org/)
- [Command Line Interface Guidelines](https://clig.dev/)
- [OpenSSF Scorecard](https://www.scorecard.dev/)
- [OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/)
- [Backstage Software Templates](https://backstage.io/docs/features/software-templates/)
- [GitHub dev containers](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers)
- [Stripe API documentation](https://docs.stripe.com/api)
- [Twilio documentation](https://www.twilio.com/docs)

Stripe and Twilio are used as quality references for developer-first onboarding, consistent API concepts, language-specific examples, errors, authentication, and self-service integration patterns. The skills are not affiliated with either company.

## License

MIT
