---
name: dependency-health
description: Manage dependencies as policy: why each exists, removability, maintenance status, upgrade risk, duplicate capabilities, transitive bloat, and vulnerability posture. Produce a dependency health report and intentional upgrade policy instead of endless Dependabot PRs. For vulnerability specifics use security-supply-chain.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and package manifest tooling.
metadata:
  version: "2.7.0"
---

# Dependency Health

## Mission

Every dependency is a maintenance contract, a supply-chain risk, and a slice of architectural debt. Most teams respond with whack-a-mole: endless update PRs, pin-everything zeal, or ignoring the graph until an incident forces attention. None of those measure health; they measure activity.

Manage dependencies as policy. For every dependency, know why it exists, whether it could leave, who maintains it, what an upgrade costs, and what it duplicates. Produce a dependency health report and an intentional upgrade policy, and let the policy drive the bot instead of the bot driving the team.

This skill assesses structure, maintenance, and upgrade posture. Vulnerability specifics, CVE triage, and exploitability belong to the `security-supply-chain` skill if available. Never issue a vulnerability verdict here; report the posture and defer the specifics.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Dependencies are policy

Treat these as policy statements, not engineering opinions:

- **Why it exists:** every direct dependency has a stated reason and a named use site.
- **Removability:** every dependency is evaluated for removal on a schedule, not at incident time.
- **Maintenance status:** a dependency with no maintenance signal is a risk, however popular it once was.
- **Upgrade risk:** upgrades are triaged by breaking-change surface, never by PR volume.
- **Duplication:** one capability, one dependency; duplicates are findings until consolidated.
- **Vulnerability posture:** posture is tracked per dependency; specifics belong to `security-supply-chain` if available.

The health report is the policy record. A dependency with no policy entry is ungoverned.

Do not approve, remove, or upgrade dependencies as one-off reactions. Apply the contracts below first.

## Dependency health workflow

### 1. Inventory the dependency graph

Read `references/dependency-inventory.md` when enumerating manifests and counting direct versus transitive dependencies.

Run `scripts/check_dependency_health.py` against the repository root for a first-pass map: manifest locations, direct dependency counts, cross-manifest duplicates, unpinned versions, and known-abandoned markers. The script is read-only and heuristic; its output is a starting map, never a verdict.

Verify:

- every manifest in the tree is listed
- direct dependencies are separated from transitive ones; transitive counts are labeled approximate
- lockfile presence is recorded per manifest; a missing lockfile is a finding
- workspace or monorepo membership is noted per manifest

Never assess, classify, or advise before the inventory is complete.

### 2. Classify each dependency

Read `references/dependency-classification.md` when reviewing why a dependency exists and whether it could leave.

For every direct dependency, answer: what capability does it provide, where is it used, could the standard library or first-party code replace it, is it essential or convenience, is it duplicated, is it vestigial?

Verify:

- classification is grounded in import and use sites, never the manifest alone
- each dependency maps to exactly one dominant class
- duplicate capabilities are named with the packages involved
- a removal recommendation exists for every non-essential dependency

### 3. Assess maintenance and risk

Read `references/maintenance-risk.md` when evaluating maintenance signals, bus factor, and upgrade risk.

For each dependency, assess activity, release cadence, security history, bus factor, and abandonment indicators. Assign every finding a severity from the canonical vocabulary in `references/standards.md`.

Verify:

- every recency claim carries an evidence label: Observed, CI-observed, or Estimated
- abandonment is never asserted from inactivity alone; at least two independent signals are required
- upgrade risk is expressed as breaking-change surface, not diff size
- vulnerability posture is reported as posture only; specifics are deferred to `security-supply-chain` if available

### 4. Detect duplication

Duplicate capabilities are the cheapest debt to remove. Compare classifications across manifests for packages serving the same role: two parsers, two HTTP clients, two date libraries, two validation sets.

Verify:

- duplicates are reported per capability, not per package name alone
- the consolidation names the survivor and the removal target
- cross-manifest duplicates flagged by `scripts/check_dependency_health.py` are confirmed at the use sites

Never consolidate blindly. Confirm behavioral parity and migration cost before recommending the survivor.

### 5. Define upgrade policy

Read `references/upgrade-policy.md` when setting cadence, batching, pinning, and breaking-change triage.

Produce an upgrade policy stating: cadence, streaming versus batching, pinning strategy, and breaking-change triage. The policy decides which update PRs are accepted as-is, which are batched, which are deferred, and which require a migration plan.

Verify:

- the policy is written down and matches the classification output
- every dependency class has an explicit upgrade path
- batching decisions cite dependency relationships, never arbitrary windows
- the pinning strategy is stated per manifest format

### 6. Produce the health report

Render the report from `assets/dependency-health-template.md`.

Verify:

- the report contains inventory counts, classifications, risk findings with severity, and the policy recommendation
- every finding carries an evidence label and a remediation
- the report names the next review date and the owner accountable for each backlog item
- nothing is marked resolved without the change being made

## Dependency-policy contract

The dependency graph obeys a standing contract:

- **Direct vs transitive:** direct dependencies are declared in manifests and governed individually; transitive dependencies are governed through the lockfile and the direct dependencies that pull them in. Never govern a transitive dependency in isolation.
- **Pinning:** production dependencies are pinned per the stated strategy; unpinned entries (`*`, `latest`, bare requirement lines) are findings until pinned. Never commit a new unpinned dependency.
- **Cadence:** dependency review runs on a fixed cadence; ad-hoc "while we are here" upgrades are discouraged unless they follow the policy.
- **Ownership:** every direct dependency has exactly one owner accountable for its maintenance assessment and upgrade decisions.
- **Documentation:** every direct dependency has a policy entry stating why it exists. Never add a dependency without a reason entry.

Read `references/dependency-governance.md` when approving new dependencies, assigning owners, centralizing monorepo dependencies, or sunsetting existing ones.

## Upgrade-policy contract

Update PRs are accepted or deferred by policy, never by mood:

- **Accept as-is:** patch and minor updates within the pinning strategy for essential dependencies with passing checks.
- **Batch:** related low-risk updates are applied together, with the relationship stated in the report.
- **Defer:** updates to dependencies with no maintenance signal, unresolved breaking-change surface, or a pending removal decision are deferred with a reason and a revisit date.
- **Migrate:** major updates and behavior-changing updates require a migration plan before merging.

Do not merge an upgrade that fails the contract for "keeping up to date" reasons. The report records an accept, defer, or migrate decision for every candidate.

## Required output

For every dependency health review, produce the dependency health report from `assets/dependency-health-template.md`.

The report must contain:

1. **Inventory** — manifests, formats, direct counts, transitive estimates, pinning state, lockfile presence
2. **Classifications** — per-dependency class with use sites and removal recommendation
3. **Risk findings** — maintenance and upgrade risk findings with severity and evidence labels
4. **Duplication** — duplicate capabilities with a named consolidation
5. **Policy recommendation** — cadence, batching, pinning, and an accept/defer/migrate decision per candidate
6. **Backlog** — prioritized findings with owners and a next review date

## Definition of done

A dependency health review is done when:

- the inventory lists every manifest with direct/transitive separation and lockfile state
- every direct dependency is classified with a use site and a removal recommendation
- maintenance and upgrade risk findings carry severity and evidence labels
- duplicate capabilities are identified with a named consolidation
- the upgrade policy states cadence, batching, pinning, and triage
- every update candidate has an accept, defer, or migrate decision with rationale
- the report is rendered from `assets/dependency-health-template.md`
- the next review date and per-item owners are recorded

Hand off vulnerability specifics and CVE triage to the `security-supply-chain` skill if available. Dependency health covers structure, maintenance, and policy; it does not replace vulnerability scanning.
