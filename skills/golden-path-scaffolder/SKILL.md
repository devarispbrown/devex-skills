---
name: golden-path-scaffolder
description: Turn repeated development workflows into generators: detect patterns worth templating, design scaffold commands, embed best practices into generated code, and wire generated output into CI, docs, and metadata. When to build a generator versus document a path. For the onboarding path the generated project serves use developer-onboarding.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and the project's build/template tooling.
metadata:
  version: "2.7.1"
---

# Golden Path Scaffolder

## Mission

Scaffolding turns developer experience into leverage. A repeated workflow is an unpaid tax: every hand-copy pays the same setup cost, makes the same mistakes, and drifts further from the current best practice. A generator turns that tax into a paved road — one command emits a correct, best-practice-embedded starting point, and every copy after the first is free.

The generator is the single source of truth. The output is generated, never hand-copied.

Do not scaffold everything. Some workflows are better served by documentation, and some by neither. The decision to build a generator is a product decision: it changes how a workflow is consumed, maintained, and improved. This skill supplies the evidence to decide, the contract to design against, and the workflow to ship and maintain the generator.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Read `references/candidate-detection.md` when searching the repository, history, and support channels for repeated workflows worth templating.

Read `references/generator-contract.md` when designing the scaffold command, its inputs, and its guarantees.

Read `references/template-design.md` when laying out templates and embedding best practices into generated code.

Read `references/output-wiring.md` when connecting generated output to CI, docs, and metadata registries.

Read `references/generator-lifecycle.md` when versioning, regenerating, and deprecating generators.

For the onboarding path the generated project serves, use the `developer-onboarding` skill if available. For measuring the friction that motivates a generator, use the `developer-experience-auditor` skill if available.

## When to scaffold

Build a generator when:

- the same structure or code is created repeatedly (frequency thresholds in `references/candidate-detection.md`)
- the manual steps are error-prone: credentials, wiring, metadata registration, or platform configuration are easy to get subtly wrong
- the team's best practices change faster than existing copies can follow
- the output must pass checks, appear in docs, and be registered in metadata — all things a generator can emit correctly the first time

Document the path instead when the workflow is infrequent, highly varied, or depends on judgment. A generator for a one-off pattern is a second maintenance burden, not leverage.

Never build a generator for a workflow you cannot name, run end-to-end, and verify. Never scaffold a workflow below the frequency thresholds in `references/candidate-detection.md` unless the manual path is actively producing defects.

## Scaffolder workflow

### 1. Detect candidate workflows

Run `scripts/scan_scaffold_candidates.py` against the repository as a first-pass signal. The scanner reports candidate families, repeated boilerplate, and docs with fill-in markers, ranked by repetition. Read `references/candidate-detection.md`.

Verify:

- the candidate is confirmed by at least two signal sources: PR history, onboarding friction, or support questions
- the workflow can be named and its steps enumerated end-to-end
- the repetition is structural, not coincidental — same file shapes, same wiring, same failure modes
- the frequency meets the thresholds in `references/candidate-detection.md`

The scan is a signal, never a verdict. Confirm every candidate before designing.

### 2. Design the generator contract

Read `references/generator-contract.md`.

Define the command shape, inputs, output tree, and guarantees before writing any template:

- one command per product: `<product> generate <kind> <name>`
- named kinds with a small, explicit option set
- non-interactive by default; every prompt has a default and a flag
- idempotent: re-running on an existing tree either reproduces it or fails loudly
- re-run safe: generated files are marked and never silently overwritten after hand edits

Verify:

- the contract is expressible in one `--help` screen
- the output tree is fully specified before templates are written
- the idempotency and re-run safety guarantees are stated in the contract

### 3. Define the template set

Read `references/template-design.md`.

Map each step of the workflow to a template file. Every template carries `<placeholder>` slots, never hardcoded values. Keep conditional blocks explicit and minimal.

Verify:

- every placeholder is documented with its type and default
- unresolved placeholders fail generation instead of producing broken output
- templates embed best practices: CI jobs, tests, docs stubs, and metadata
- nothing that must stay hand-owned is generated

### 4. Embed best practices

Best practices live in the templates, not in the generator's README. Generated code ships correct by default:

- CI configuration that lints, tests, and builds the generated project
- a smoke test that runs on the generated tree
- docs stubs that are complete except for the placeholders
- metadata and ownership registration emitted with the tree

Never embed secrets, credentials, personal configuration, or machine-specific values in templates or generated output.

### 5. Wire output into CI, docs, and metadata

Read `references/output-wiring.md`.

A generated project that is not wired in is a folder, not a paved road:

- CI validates generated projects and detects template drift
- docs link the generated kind to its quickstart and index
- metadata registries receive the generated entry with an owner
- ownership is explicit for every generated project and for the generator itself

Verify:

- generation is exercised in CI: generate, run checks, compare against fixture
- the generated kind is discoverable in docs and metadata
- every generated project and the generator have an explicit owner

### 6. Version and maintain the generator

Read `references/generator-lifecycle.md`.

Version the generator, track template drift, and deprecate deliberately:

- the generator has a SemVer version, a changelog, and an embedded version marker
- regeneration is a supported, diff-first workflow
- template changes ship with migration notes for existing generated projects
- deprecated templates announce, warn, and migrate on a timeline

Never let templates drift silently from what a fresh generation produces.

## Generator contract

Every generator is a single command: `<product> generate <kind> <name>`.

The contract guarantees:

1. **Shape** — the command takes a kind and a name; output lands in a deterministic tree.
2. **Inputs** — the name, the kind, and a small set of options that change generated output. Environment variables override defaults; secrets are never inputs to the template.
3. **Non-interactive** — generation succeeds with no prompts; defaults are complete. Interactive prompts may exist for humans, but every prompt has a flag or a default.
4. **Idempotency** — generating twice produces identical output. Re-running on an existing generated tree is either a no-op or a loud failure with a diff.
5. **Re-run safety** — generated files carry a marker; files modified since generation are never silently overwritten. Overwrites require `--force` and show the diff first.
6. **Upgrade path** — generated projects have a supported regeneration path that preserves intentional edits where possible.

Read `references/generator-contract.md` for the full contract and its verification checklist.

## Template-maintenance contract

- Templates are the single source of truth for the generated kind; generated output is derived data.
- Every template change ships with regeneration guidance and, when behavior changes, a migration note.
- Every template has a fixture that fresh generation must match; the fixture runs in CI.
- Generated output is marked (`GENERATED BY <product> generate <kind>`); hand edits outside marked regions are preserved on regeneration.
- Template sets are versioned with the generator and deprecated deliberately.

Read `references/template-design.md` and `references/generator-lifecycle.md` for the operating details.

## Required output

For every scaffolded workflow, produce the scaffolder design using `assets/scaffolder-design-template.md`.

The design must contain:

1. **Candidate analysis** — workflow name, repetition evidence with counts, error-prone steps, and the generator-versus-document decision with rationale.
2. **Generator contract** — command shape, kind, inputs, options, non-interactive behavior, idempotency and re-run safety guarantees.
3. **Template list** — every template file, its output path, its placeholders, and its fixture.
4. **Output tree spec** — the deterministic tree the command emits, including files the generator must never touch.

## Definition of done

Scaffolding is done when:

- the repeated workflow no longer needs hand-copying: a single command produces the correct starting point
- the generator runs non-interactively, idempotently, and safely on re-run
- generated output embeds the team's best practices and passes its own checks
- generated output is wired into CI, docs, and metadata with explicit ownership
- every template has a fixture and fresh generation matches it in CI
- the generator has a version, a changelog, and a documented deprecation path
- the scaffolder design is rendered from `assets/scaffolder-design-template.md` and the decision is evidence-based
