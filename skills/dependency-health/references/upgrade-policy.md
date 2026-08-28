# Upgrade Policy

## Purpose

Define when dependency updates are accepted, batched, deferred, or migrated. The policy is the standing decision procedure for update PRs; without it, the queue drives the team.

## Cadence

- Run dependency review on a fixed cadence, not continuously.
- Between reviews, let the policy decide; do not let alert volume decide.
- Re-review abandoned or high-risk dependencies every cycle until resolved.

## Streaming vs batching

- **Stream** patch and minor updates for essential dependencies with passing checks; accept as-is.
- **Batch** groups of related low-risk updates: same ecosystem, same dependency family, or upgrades whose transitive graphs overlap. State the relationship when batching.
- **Never batch** unrelated majors or updates whose failure surfaces differ.

Batching is justified by dependency relationships, never by a calendar window.

## Pinning strategy

State per format how production dependencies are pinned:

- **npm:** exact versions or lockfile-pinned; caret/tilde ranges only where the policy says so. `*` and `latest` are findings.
- **Go:** versions in go.mod; go.sum pins hashes. Upgrades move the require line.
- **Rust:** exact versions in Cargo.toml or Cargo.lock-pinned; `*` and major-only specs are findings.
- **pip:** `==` pins; `>=`, `~=`, and bare names are findings unless the policy allows them.
- **pyproject:** exact `==` or lockfile-pinned; range specs only where the policy says so.

Never commit a new unpinned dependency. Never hand-edit a lockfile; regenerate it.

## Breaking-change triage

For every major or behavior-changing update:

1. Read the changelog and migration guide; list removed and changed surfaces.
2. Map each surface to the code that uses it.
3. Confirm behavioral parity with the current dependency where the change is observable.
4. Decide: adopt with code changes, defer, or replace the dependency.

A breaking update without a migration plan is deferred, not merged.

## Accept / defer / migrate

Record a decision per candidate in the report:

- **Accept:** within policy, checks pass.
- **Defer:** no maintenance signal, unresolved breaking surface, or pending removal decision. State the reason and the revisit date.
- **Migrate:** major or behavior-changing; requires the migration plan.

## Verify

- the policy matches the classification output
- every dependency class has an upgrade path
- batching decisions cite dependency relationships
- the pinning strategy is stated per format
- every candidate has an accept/defer/migrate decision
