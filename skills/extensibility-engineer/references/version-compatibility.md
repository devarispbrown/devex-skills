# Version Compatibility

## Purpose

Define the contract between extension and core versions, and how the two negotiate capabilities at load time. The goal: a mismatched extension fails loudly and safely, never silently misbehaves.

## Extension-to-core version contract

Every extension declares the core version range it supports, in the manifest or a dedicated contract file:

- `min_core_version`: the oldest core version the extension is tested against.
- `max_core_version`: the newest core version the extension is tested against, or an unbounded marker when forward-compatibility is guaranteed by policy.
- `api_version`: the extension API version the extension implements, when the API is versioned independently.

Version numbering follows the `SemVer contract` in `dx-standards/compatibility.md`. The extension API is a public surface: a breaking change to it is a MAJOR event for the host, applied to the whole extension consumer list.

## Enforcement at load

- The host validates the declared range against its own version before loading the extension.
- Out-of-range: refuse to load with an actionable message, or load in a documented degraded mode — never silently.
- Degraded mode must be opt-in per extension and must not alter data or state.

## Capability negotiation

- The extension queries the host for available capabilities; the host answers with its actual capability set.
- No silent fallback: a missing capability is a load-time decision, not a runtime surprise.
- The extension adapts only through documented negotiation APIs, never by probing host internals.

## Compatibility window

- The host states its compatibility window (how far back supported extensions go) following the `Cadence and policy` section of `dx-standards/compatibility.md`.
- A claimed-supported core version without CI evidence is an unsupported claim. Gate the claim the way `release-guardian` gates `UNTESTED_SUPPORTED_VERSION` — the release gate semantics live in that skill's scope.

## CI matrix

- Every extension with a published version contract runs contract tests across every core version in the declared range.
- Matrix results are the evidence for the range; the range is never widened on estimates.
- Core changes that would break the declared range are flagged before release, not discovered by users.

## Forward and backward compatibility

- Extensions pin the minimum core they need and declare it; they do not quietly rely on newer-only features.
- Core maintains the documented window; removing an API inside the window is a breaking change per the `SemVer contract` and `Behavioral compatibility` sections.
