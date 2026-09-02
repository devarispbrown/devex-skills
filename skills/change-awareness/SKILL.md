---
name: change-awareness
description: Design the communication layer of change: changelogs, release notes, migration notices, deprecations, advisories, and API-version notices that state who is affected, what action is required, by when, and what breaks if ignored, with reach verification. For classifying breaking changes and version recommendations use release-guardian; for status and incident communication use operational-trust.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with git access and release communication channels.
metadata:
  version: "2.4.0"
---

# Change Awareness

## Mission

Design the communication layer of change: changelogs, release notes, migration notices, deprecation notices, security advisories, and API-version notices that tell every affected developer who is affected, what action is required, by when, and what breaks if ignored — and then verify the notice actually reached them.

A change to a public surface is a communication event. The notice is part of the change, not an afterthought: it ships before or with the change, never after it. A change that ships without a notice is a breaking change to developer trust even when the API surface itself is compatible.

Every notice answers five questions:

1. **Who is affected?** The concrete consumer segments, never a generic "users".
2. **What action is required?** The exact steps, copyable, never a version number alone.
3. **By when?** The deadline and the timeline that produced it.
4. **What breaks if ignored?** The consequence, in the severity vocabulary.
5. **Was anyone reached?** Evidence, not assumptions.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Change communication

Every change passes through the same sequence, in order. Do not write a notice before classifying the change; do not publish before reach is verified.

### 1. Classify the change surface

Enumerate the changed public surface: APIs, CLI flags and output, config schema and defaults, SDKs, webhook payloads, wire format, database schema, and observable behavior. For each changed surface, determine the change class — breaking, behavioral, deprecated, added, fixed, or internal — and the version impact. Hand classification and the SemVer recommendation to the `release-guardian` skill; do not guess a version from diff size.

Run `scripts/check_change_notices.py` against the tree and the changelog. Unnoted deprecation, breaking, and removal markers it finds are pre-existing communication debt; fold them into the notice plan rather than ignoring them.

### 2. Choose the notice types

Map every changed surface to at least one notice type. A single change can require several:

- changelog entry — every change, no exceptions
- release note — every user-visible change
- deprecation notice — every deprecated surface, at deprecation time
- migration notice — every breaking change
- security advisory — every vulnerability affecting a public surface
- API-version notice — every change to a versioned API contract

Read the reference for each type before writing it: `references/changelog-contracts.md`, `references/deprecation-notices.md`, `references/migration-notices.md`, `references/advisory-patterns.md`, `references/reach-verification.md`.

### 3. State who is affected

Never address "users" as a single audience. List the concrete segments the change touches, from the compatibility consumer list: language SDK consumers, JSON/response parsers, CLI script consumers, config file owners, webhook handlers, generated code, dashboards, and integrators of docs and examples. Name the segments even when the answer is "all of them". An affected segment that is not named is an affected segment that is not reached.

### 4. State the action required

Every notice names the exact action a developer takes. "Upgrade to 3.0" is not an action; "replace `legacy_transform` with `transform` at your call sites and move the `X-Token` header to `Authorization`" is. Prefer copyable before/after snippets over prose descriptions. If no action is required, state that explicitly; silence is not the same as a no-op.

### 5. State the deadline

Give the date or version by which the action must be complete, and the timeline that produced it. Deprecation follows the documented removal window from `references/deprecation-notices.md`; never remove before the window closes. Distinguish "action due" from "support ends" when they differ. An action without a deadline is a suggestion, not a notice.

### 6. State what breaks if ignored

State the consequence in the severity vocabulary from `references/standards.md`. Name the concrete failure: builds break, requests fail, data is lost, behavior silently changes, the package is no longer maintained. A breaking change that ships without a changelog entry and migration guidance fails the `UNDOCUMENTED_BREAKING_API` gate; write the notice so that gate passes with evidence, never because it was assumed.

### 7. Write the notice from the contract

Draft the notice from the contract in `references/changelog-contracts.md` using `assets/change-notice-template.md`. Keep the affected/action/deadline/consequence fields complete and free of hedging. For breaking changes, link the migration notice rather than inlining its steps. Changelog entries go in the Unreleased section; release notes go where consumers read them.

### 8. Publish before the change

The notice lands before or with the change, never after. Deprecation notices ship at deprecation time, not at removal time. Breaking changes ship with their migration notice in the same release. Keep changelog, release notes, and migration docs in sync through the documentation lifecycle; hand doc gating to the `developer-docs-auditor` skill when available. Publishing order matters: changelog first, release second, removal only after the window closes.

### 9. Verify reach

Verify the notice reached the affected segments using `references/reach-verification.md`: announcement channels, issue/PR mentions, dependency-graph alerts, in-product banners, and measured reads against the affected count. Label evidence Observed, CI-observed, or Estimated. An unreached notice is an uncommunicated change; convert unreachability to a follow-up, never to silence.

### 10. Close the loop

Track removal deadlines. When the deadline passes, verify the code markers are gone — rerun `scripts/check_change_notices.py` — confirm the changelog entry and migration notice are in place, and record the removal in the change communication record. A deprecation that silently survives its deadline is a broken promise, not a kindness.

## Notice timing

Timing is part of the notice. A correct notice at the wrong time is a missed notice.

| Notice type | Ships when | Never later than |
|---|---|---|
| Changelog entry | with the change, in Unreleased | the release it describes |
| Release note | with the release | the release announcement |
| Deprecation notice | at deprecation time | the release that deprecates |
| Migration notice | with the breaking change | the release that breaks |
| Security advisory | when the fix is available | disclosure day |
| API-version notice | when the version contract changes | the version's release |

A deprecation announced only at removal time is not a deprecation; it is a surprise breaking change. A migration notice that ships after the breaking release forces readers to guess. When timing slips, the slip is itself announced, with the new deadline, before it matters.

## Coverage checker

`scripts/check_change_notices.py` scans a tree for deprecation annotations (`@deprecated`, `@Deprecated`, `@available(*, deprecated)`, `#[deprecated]`, `[Obsolete]`, `DeprecationWarning`), breaking-change comments, and TODO-remove markers, then checks a changelog or notices file for an entry matching each marked surface. Unnoted markers are printed as findings and the script exits 1, so it can run in CI and in the release checklist. Markers are signals, not verdicts: confirm each finding semantically before writing the notice. The fixture under `assets/notice-sample/` demonstrates the failure mode — a deprecated function with no changelog entry.

## Notice contracts

### Changelog contract

Every release gets a changelog entry for every change. Entries state the changed surface, who is affected, what action is required, by when, and what breaks if ignored, per `references/changelog-contracts.md`. Breaking changes link a migration notice. Never mark a breaking change `fixed` to avoid the notice.

### Release note contract

Release notes lead with user-visible value and the action the reader takes, then give the migration pointer. Same five fields as the changelog entry, written for the reading context. Internal changes do not belong in release notes.

### Deprecation notice contract

Deprecation is announced at deprecation time with the replacement and the removal timeline, per `references/deprecation-notices.md`. The code carries the marker (`@deprecated`, `DeprecationWarning`, `#[deprecated]`, `[Obsolete]`, `@available(*, deprecated)`) at the same time the notice ships, so the checker can verify coverage. Removal is a breaking change with its own changelog entry and migration notice.

### Migration notice contract

Every breaking change has a migration notice stating what changed, why, the exact upgrade steps, the rollback path, and the deadline, per `references/migration-notices.md`. A breaking change without migration guidance fails the `UNDOCUMENTED_BREAKING_API` gate.

### Advisory contract

Security issues affecting a public surface follow `references/advisory-patterns.md`: severity, affected versions, patched versions, workaround, and identifier, disclosed after the fix is available.

### API-version notice contract

Changes to a versioned API contract state the version affected, the version that resolves it, the support window, and the action required per version, in the same five-field shape. Never leave a version undocumented because the change "seems small".

When a versioned API is deprecated, the notice names the successor version and the overlap window during which both are served. When a version is retired, the notice names the retirement date, the migration path, and the consequence of staying on the retired version (unresolved issues, no security fixes, eventual failure). Version matrices in the docs must agree with the notice; a matrix that contradicts the notice is a second, worse notice.

### Cross-surface contract

When one change touches several surfaces, one record ties the notices together: same surface identifier, same deadline, per-surface entries linked from the changelog. Never let an API deprecation, its SDK stub, and its config key each get their own unlinked notice with different deadlines.

## Required output

For every change cycle, produce a change communication record containing:

1. **Notice inventory** — every changed surface mapped to its notice type, with the affected segments, action, deadline, and consequence for each
2. **Notice artifacts** — changelog entries, release notes, deprecation notices, migration notices, advisories, and API-version notices written from the contracts
3. **Publication evidence** — where each notice was published, when, relative to the change
4. **Reach evidence** — per notice, the channels used, the audience reached, and the evidence label (Observed, CI-observed, Estimated)
5. **Gate status** — per-gate result keyed by gate constant from `references/standards.md`, including `UNDOCUMENTED_BREAKING_API` and related release gates

## Definition of done

Change communication is done when:

- every public-surface change maps to at least one notice type
- every notice states who is affected, what action is required, by when, and what breaks if ignored
- every breaking change has a changelog entry and a migration notice
- deprecations state replacement and removal timeline at deprecation time, and the code carries the marker
- notices are published before or with the change, never after
- reach is verified with labeled evidence, never assumed
- removal deadlines are tracked and markers verified gone by rerunning the checker
- no notice ships with an unanswered affected/action/deadline/consequence field
- no `UNDOCUMENTED_BREAKING_API` failure is hidden by a score, a heuristic, or an assumption

Hand classification and version recommendations to the `release-guardian` skill, status and incident communication to the `operational-trust` skill, and documentation gating to the `developer-docs-auditor` skill when available. Change awareness designs the notices; it does not replace the release contract or the docs auditor.
