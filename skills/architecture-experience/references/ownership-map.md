# Ownership Map

## Hard objective

Produce a map artifact in which every module or service resolves to an owner — team or role — or is explicitly recorded as Unknown.

## Scope

Cover every module and service the mental model touches:

- module/service name
- owner team or role
- code path
- public surface (APIs, events, config)
- escalation or on-call route

## Sources

Derive ownership, in priority order:

- CODEOWNERS and similar ownership manifests
- package and deploy manifests with owner metadata
- git history: most frequent recent committers by path
- ADRs and design docs that name owners
- directory conventions

Interviews and folklore are secondary; record them as Estimated, never as Observed.

## Procedure

1. List the modules and services from the boundary audit.
2. Resolve each to an owner from the sources above.
3. For unresolvable entries, record **Unknown** — never a guessed name.
4. Cross-check that the owner can name the module's entry points; if not, the map is stale.

## Artifact

Render the map as a table in the architecture brief:

| Module/service | Owner | Code path | Public surface | Escalation | Evidence |
|---|---|---|---|---|---|

## Rules

- Unknown is a finding, not a skip. It predicts onboarding friction and delays on real work.
- Owner metadata that contradicts the map is a finding; the map does not win by default.
- A module with multiple effective owners is a finding: shared ownership without a designated primary is unowned.

## Output

The completed table becomes the ownership map section of the brief. Catalog-style search and listing of owners belongs to the `developer-discoverability` skill; this procedure builds the artifact, it does not index the catalog.
