---
name: extensibility-engineer
description: Design plugin, provider, connector, middleware, and hook author experiences: extension API stability, isolation, version compatibility, capability discovery, testing harnesses, and scaffolding workflows such as project plugin create/test/publish. For the core API surface use api-design-reviewer; for version-range maintenance use compatibility-engineer.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and the extension architecture.
metadata:
  version: "2.3.0"
---

# Extensibility Engineer

## Mission

Design the author experience for plugin, provider, connector, middleware, and hook authors: the surface they code against, the guarantees they rely on, and the workflow from scaffold to shipped extension. The extension API is a product. If an author cannot build, test, and ship an extension without guessing, the extension API design is the defect — do not paper over it with templates or docs.

Extensions are untrusted code running inside the host. Isolation, failure containment, and version contracts are design requirements, not afterthoughts.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Read the reference for the active phase:

- `references/extension-api-stability.md` — stability tiers for extension APIs, breaking-change policy
- `references/isolation-and-sandboxing.md` — extension isolation, failure containment, security boundaries
- `references/version-compatibility.md` — extension-to-core version contracts, capability negotiation
- `references/capability-discovery.md` — plugin/connector discovery mechanisms, registries, metadata
- `references/testing-harness.md` — extension test harnesses, mock cores, contract tests
- `references/scaffolding-cli.md` — create/test/publish command design for extensions

Version and compatibility doctrine derives from the `SemVer contract`, `Behavioral compatibility`, and `Cadence and policy` sections of `dx-standards/compatibility.md`. Do not restate their values here.

## The extension contract

Every extension author experience passes through a fixed contract, in order:

1. **Surface** — enumerate the exported extension API: hooks, interfaces, config points, provider slots.
2. **Stability** — assign every exported surface a stability tier and apply the breaking-change policy.
3. **Isolation** — define what the extension may touch and how failures are contained.
4. **Version contract** — declare which core versions the extension targets; the host enforces fit at load.
5. **Discovery** — authors find the surface; the host finds extensions and their capabilities.
6. **Testing** — the author validates against a mock core and contract tests, not the real host.
7. **Scaffolding** — create/test/publish commands carry the author from empty directory to shipped extension.

Do not skip to the testing harness before stability and isolation are decided. Never ship an extension surface with an unsatisfied contract item.

## Extension author experience

### 1. Map the extension surface

Enumerate everything an extension author can implement, register, or configure: hooks, interfaces, middleware, providers, connectors, config schemas, and resource access.

Verify:

- every surface has an unambiguous name, signature or interface shape, and semantics
- naming is consistent with the host's existing vocabulary
- the surface list is grounded in the codebase, never invented from patterns seen elsewhere
- undocumented or implicit surfaces are either documented or removed

Run `scripts/check_extension_surface.py` against the tree as a first-pass signal when repository access is available. The script output is heuristic inventory, never a verdict.

### 2. Assign stability tiers and policy

Read `references/extension-api-stability.md`.

Verify:

- every exported surface carries exactly one stability tier: internal, experimental, stable, or deprecated
- experimental surfaces are opt-in, labeled, and have a defined promotion path
- stable surfaces are covered by behavioral compatibility; changes require deprecation and migration
- the breaking-change policy is written down and enforced, not implied
- a fix that changes observable behavior is never presented as compatible

### 3. Design isolation and failure containment

Read `references/isolation-and-sandboxing.md`.

Verify:

- the security boundary defines what the extension may read, write, execute, and reach over the network
- failure of one extension cannot take down the host: timeouts, limits, quarantine, disable
- secrets and ambient authority are never exposed to extensions
- the sandbox used in tests matches the sandbox used in production

### 4. Define the version contract

Read `references/version-compatibility.md`.

Verify:

- every extension declares the core version range it supports
- the host validates the contract at load and refuses or warns on mismatch
- capability negotiation is explicit: the extension queries, the host answers, no silent fallback
- supported core versions are verified with CI evidence, never claimed

### 5. Design capability discovery

Read `references/capability-discovery.md`.

Verify:

- the manifest is the single source of truth for discovery metadata
- registry metadata covers identity, compatibility, capabilities, and integrity
- install, update, and removal are idempotent and versioned

### 6. Build the testing harness

Read `references/testing-harness.md`.

Verify:

- a mock core exists that records calls, injects fixtures, and simulates failures
- contract tests assert the extension against its declared contract in both directions
- the scaffolded project ships tests that pass before the author writes any code

### 7. Design the scaffolding CLI

Read `references/scaffolding-cli.md`.

Verify:

- `create` yields a runnable extension skeleton with a clean surface inventory
- `test` runs the harness with a fast feedback loop
- `publish` refuses extensions with checklist gaps or a missing version contract
- commands share flag conventions, exit codes, and machine-readable output

### 8. Validate the whole experience

Walk the author journey end to end: scaffold, implement one hook, run contract tests, package, publish, install into a fresh host, upgrade the core, and confirm behavior.

Verify:

- a brand-new author completes the journey without host internals knowledge
- every promise in the documentation is exercised, not asserted
- gaps found are fixed at the design level, not documented around

## Extension surface contract

Every extension API must define, per exported surface:

- purpose and exact name and signature
- stability tier and change policy
- inputs, types, defaults, and error semantics
- side effects and resource access
- version range and capability requirements
- example usage and expected behavior

The extension surface inherits the behavioral compatibility doctrine of `dx-standards/compatibility.md`. The consumer list includes installed extensions, published extensions, scaffolded templates, and test harnesses.

## Scaffolding CLI contract

`create`, `test`, and `publish` are the public author workflow. Each command:

- has one default route and minimal choices
- validates before mutating
- reports machine-readable results on stdout and diagnostics on stderr
- is idempotent and safe to re-run

`publish` never succeeds with an unsatisfied checklist item.

## Handoffs

- Core API surface design: `api-design-reviewer`.
- Version-range and compatibility-window maintenance: `compatibility-engineer`.
- Release gating of breaking extension changes: `release-guardian`.
- Extension author documentation: `developer-docs`.

## Required output

For every extension author experience design, produce the extension brief from `assets/extension-brief-template.md`.

The brief must contain:

1. **Surface inventory** — every hook, interface, config point, and provider slot, with file, kind, tier, and evidence
2. **Stability map** — tier and breaking-change policy per surface, with deprecation windows
3. **Isolation boundaries** — permitted access, containment guarantees, failure behavior
4. **Version contract** — supported core versions, negotiation rules, enforcement point
5. **Discovery metadata** — manifest schema, registry identity, integrity model
6. **Testing plan** — mock core, contract tests, fixture list, CI matrix
7. **Scaffolding workflow** — create/test/publish behavior, flags, exit codes
8. **Gap list** — every open item with owner and acceptance test

## Definition of done

An extension author experience is done when:

- every exported surface is enumerated, tiered, and covered by the breaking-change policy
- isolation and failure containment are defined and enforced in production and tests
- every extension declares a version contract the host validates
- discovery metadata is complete and machine-readable
- contract tests and a mock core exist and run in CI
- create/test/publish carry an author from empty directory to installed extension
- the scaffolded skeleton passes the checklist in `scripts/check_extension_surface.py`
- a new author completes the journey end to end without internal knowledge
- no surface promise rests on documentation alone; each is exercised or removed
- handoffs to `api-design-reviewer`, `compatibility-engineer`, `release-guardian`, and `developer-docs` are named where their scope applies
