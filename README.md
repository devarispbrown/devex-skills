# Developer Docs Skills

Two complementary Claude/Agent Skills for building and enforcing world-class developer documentation:

- **`developer-docs`**: authoring, information architecture, onboarding, API/SDK/CLI/config documentation, READMEs, examples, code docs, and stakeholder documentation.
- **`developer-docs-auditor`**: adversarial testing, documentation drift detection, executable-doc validation, API/SDK parity, scoring, and release gating.

The system uses [Diátaxis](https://diataxis.fr/) as the information-architecture model, then adds product/DX review, docs-as-code, executable examples, lifecycle controls, and a hard onboarding standard inspired by the best developer platforms.

## The core standard: magic in 15 minutes

A brand-new developer with **zero product knowledge** should be able to open the canonical Quickstart and reach a **meaningful, verified, end-to-end product outcome in 15 minutes or less**.

This is a hard quality gate, not a writing guideline.

The timer includes product-specific installation, signup/authentication when required, configuration, execution, waiting, and verification. You cannot make the metric pass by moving product setup into a prerequisites section. If production setup requires manual approval or slow provisioning, the product should provide a sandbox, local mode, test environment, or seeded fixture.

| Time to verified end-to-end value | Rating |
|---|---|
| ≤5 min | Exceptional |
| >5 to ≤10 min | Strong |
| >10 to ≤15 min | Pass |
| >15 min | **P1 onboarding/DX failure** |
| No reproducible E2E quickstart | **P1 failure** |

A project cannot receive a **world-class** verdict if it fails this gate, regardless of how good the prose or reference coverage is.

## Why two skills?

Authoring and auditing have different incentives.

`developer-docs` asks: **What is the clearest, most maintainable documentation and developer journey we can build?**

`developer-docs-auditor` asks: **How can I prove this is wrong, stale, slow, contradictory, or non-executable before a developer discovers it?**

Keeping them separate reduces self-review bias and makes it natural to run the auditor as a PR or release gate.

## Repository layout

```text
developer-docs-skills/
├── README.md
├── LICENSE
└── skills/
    ├── developer-docs/
    │   ├── SKILL.md
    │   ├── references/
    │   ├── assets/
    │   └── scripts/
    └── developer-docs-auditor/
        ├── SKILL.md
        ├── references/
        ├── assets/
        └── scripts/
```

There is intentionally **no README inside either skill directory**. Agent Skills use `SKILL.md` as the skill entry point; the repository-level README is for humans browsing the OSS project.

## Install

### Claude Code

For a project-scoped install, copy the two folders into:

```text
<your-repo>/.claude/skills/developer-docs/
<your-repo>/.claude/skills/developer-docs-auditor/
```

For a personal install that is available across projects, copy them into:

```text
~/.claude/skills/developer-docs/
~/.claude/skills/developer-docs-auditor/
```

Claude can invoke them automatically from their descriptions, or you can explicitly use `/developer-docs` and `/developer-docs-auditor`.

This repository also includes `.claude-plugin/plugin.json`, so it can be distributed as a multi-skill Claude Code plugin or marketplace entry without changing the skill layout.

### Other Agent Skills-compatible clients

Copy each skill directory as-is into the client's Agent Skills directory. Each contains a required `SKILL.md` plus optional `references/`, `assets/`, and `scripts/` that are loaded progressively as needed.

## `developer-docs`

Use this skill while designing or writing documentation.

It covers:

- Diátaxis classification and documentation architecture
- the ≤15-minute canonical Quickstart
- repository README design
- API, CLI, configuration, event, and error documentation
- SDK documentation and cross-language semantic parity
- runnable examples and tutorials
- public code comments and symbol docs
- troubleshooting and production transition
- migration/deprecation/release documentation
- internal engineering and external stakeholder docs
- terminology, accessibility, and coding-agent/LLM usability
- product/DX review when an interface is difficult to document cleanly

Example prompts:

```text
Use developer-docs to redesign this project's documentation architecture around Diátaxis.
```

```text
Build a Quickstart where a new developer reaches the complete end-to-end magic path in under 15 minutes. Treat anything that prevents that as a product/DX problem, not just a writing problem.
```

```text
Update the README, API docs, Go SDK docs, examples, and migration guide for this feature. Establish truth from the implementation before writing.
```

```text
Create an external integration guide for a technical partner. Assume they know the domain but know nothing about our product or internal terminology.
```

## `developer-docs-auditor`

Use this after authoring, on pull requests, before releases, or periodically against a documentation system.

It covers:

- adversarial cold-start review
- observed/CI-observed/estimated magic-path timing
- hard ≤15-minute onboarding release gate
- git-diff documentation impact analysis
- documentation drift detection
- executable snippets/examples
- local Markdown link checks
- API/CLI/config contract correctness
- SDK/API parity
- error and troubleshooting quality
- terminology consistency
- lifecycle/migration/deprecation checks
- human and coding-agent retrieval quality
- independent Documentation Quality and Developer Experience scores
- PASS / PASS WITH DEBT / FAIL / UNVERIFIED release verdicts

Example prompts:

```text
Use developer-docs-auditor to audit this repo as if you had never seen the product. Actually test the canonical Quickstart where safe and prove whether the magic path is under 15 minutes.
```

```text
Review this PR for documentation impact and drift. Fail the review if public behavior changed without the required docs, examples, SDK, changelog, or migration updates.
```

```text
Audit our OpenAPI spec, TypeScript/Python/Go SDKs, examples, and API reference for semantic parity. Separate documentation bugs from API or SDK design bugs.
```

```text
Score the docs and underlying developer experience independently. Do not call them world-class if the 15-minute magic path is unverified or fails.
```

## Recommended workflow

### 1. Author

Use `developer-docs` while building a feature or designing a new documentation surface. Start from product truth, design the canonical magic path, then add how-to, reference, explanation, troubleshooting, and production material.

### 2. Audit

Use `developer-docs-auditor` from a clean developer perspective. Execute what can safely be executed. Check drift against source/specs, inspect SDK parity, and time the magic path.

### 3. Fix the right layer

The auditor classifies root causes as:

- **Docs**: documentation can fix it.
- **Product/DX**: the API, SDK, CLI, config, auth, errors, or workflow need redesign.
- **Infrastructure**: build/provision/runtime latency or reliability.
- **External dependency**: third-party approvals, services, quotas, etc.

Do not add three paragraphs of documentation to compensate for a bad API.

### 4. Gate releases

A release should fail when a P0/P1 documentation contract is broken, including a failed magic path, materially stale public reference, broken canonical install/auth, unsafe examples, or missing breaking-change migration guidance.

## Magic-path measurement

The auditor supports three evidence levels:

- **Observed**: a human/agent actually executes the path from a clean or representative environment.
- **CI-observed**: automation executes the product steps; useful for detecting drift, though it may undercount human reading/signup time.
- **Estimated**: the steps are analyzed but not executed. An estimate cannot prove a passing gate.

The included `magic_path_runner.py` can run a project-owned JSON manifest in sandbox/local/test environments:

```bash
python skills/developer-docs-auditor/scripts/magic_path_runner.py \
  .docs/magic-path.json --execute
```

Start from `skills/developer-docs-auditor/assets/magic-path-manifest.example.json`.

## Included deterministic tools

The auditor includes small dependency-free helpers intended to complement, not replace, repository-native CI:

```bash
# Candidate documentation impact from a git diff
python skills/developer-docs-auditor/scripts/docs_impact.py --base main --head HEAD

# Missing local Markdown link targets
python skills/developer-docs-auditor/scripts/check_markdown_links.py docs

# Forbidden terminology aliases using a project policy
python skills/developer-docs-auditor/scripts/check_terminology.py \
  .docs/terminology.json --root .

# Time an explicitly defined sandbox/local magic path
python skills/developer-docs-auditor/scripts/magic_path_runner.py \
  .docs/magic-path.json --execute
```

For snippets, schemas, SDKs, CLI help, and integration examples, prefer the target project's actual compiler, test runner, schema tooling, code generator, and sandbox infrastructure.

## Quality model

The auditor reports two scores because excellent prose can hide a poor interface:

### Documentation Quality

Correctness, onboarding, reference completeness, how-to coverage, SDK consistency, examples/testability, troubleshooting, information architecture, lifecycle, production guidance, maintainability, and agent usability.

### Developer Experience

Magic-path friction, API/CLI/config coherence, errors/recovery, auth/setup ergonomics, SDK quality, observability/debuggability, versioning, production transition, and self-service support.

A numerical score never overrides hard release gates.

## Diátaxis

These skills use [Diátaxis](https://diataxis.fr/) to keep documentation aligned with user intent:

| Mode | User need | Documentation job |
|---|---|---|
| Tutorial | Learn | Provide a successful guided learning experience |
| How-to | Work | Help an experienced user complete a task |
| Reference | Work | Provide accurate, complete technical facts |
| Explanation | Study | Build understanding, context, and mental models |

The 15-minute Quickstart is treated as a specially constrained tutorial: it must deliver a successful learning experience **and** demonstrate meaningful end-to-end product value under the onboarding budget.

## Design principles

1. **Truth before prose.** Source/spec/tests outrank stale narrative docs.
2. **Time to value is a documentation metric.** The getting-started experience has an explicit SLA.
3. **Docs expose product design.** Hard-to-document interfaces should trigger DX review.
4. **Examples should be executable.** Plausible-looking snippets are not proof.
5. **One canonical onboarding route.** Choices come after success.
6. **Reference should be generated where possible.** Hand-written material adds tasks, context, examples, and recovery.
7. **SDKs are products.** Each official language deserves parity and idiomatic UX.
8. **Failures are part of the product.** Error semantics and troubleshooting are first-class docs.
9. **Docs ship with code.** Public behavior changes imply documentation impact review.
10. **Humans and agents share the corpus.** Structure docs so both can retrieve current authoritative facts.

## Contributing

Contributions should improve a repeatable developer outcome rather than merely add more prose.

Useful contributions include:

- additional language-specific documentation tests
- better OpenAPI/AsyncAPI/protobuf/GraphQL parity checks
- SDK coverage tooling
- CLI/config drift checks
- quickstart measurement patterns
- new documentation templates
- real-world examples of Product/DX defects discovered through documentation work

When changing a skill, keep the main `SKILL.md` focused and move detailed specialist guidance into `references/` so agents can load it progressively.

## References and influences

- [Diátaxis](https://diataxis.fr/)
- [Agent Skills open specification](https://agentskills.io/)
- [Anthropic: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Stripe API documentation](https://docs.stripe.com/api)
- [Twilio documentation](https://www.twilio.com/docs)

Stripe and Twilio are used as quality references for developer-first onboarding, consistent API concepts, language-specific examples, errors, authentication, and self-service integration patterns. The skills are not affiliated with either company.

## License

MIT
