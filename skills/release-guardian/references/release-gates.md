# Release Gates

Procedural checklist for verifying a product release before the tag. Gate vocabulary is canonical: reference constants by name and read `references/standards.md` for their definitions. Do not redefine constants here.

## Checklist

### 1. Changelog

Verify:

- every classified change has a changelog entry
- breaking changes are marked and linked to the migration guide
- a breaking change missing either is `UNDOCUMENTED_BREAKING_API`

### 2. Compatibility statement

Verify:

- the compatibility analysis is complete for the full consumer list
- behavioral compatibility claims carry evidence and an evidence label
- the SemVer bump is stated with rationale tied to the classification

### 3. SDK sync

Verify:

- released official SDKs cover the new surface
- SDKs contradicting the canonical API trigger `SDK_API_DRIFT`
- generated clients were regenerated, or divergence is intentional and documented

### 4. Docs sync

Verify:

- public reference matches current behavior; disagreement triggers `STALE_PUBLIC_REFERENCE`
- quickstart and examples still execute; a broken canonical path triggers `BROKEN_QUICKSTART` or `BROKEN_CANONICAL_INSTALL`
- examples avoid unsafe credential handling; violations trigger `UNSAFE_EXAMPLES`

For documentation-release gating, hand off to the `developer-docs-auditor` skill if available.

### 5. Quickstart verified

Verify:

- the canonical quickstart is reproducible end-to-end
- the timing band is recorded with an Observed or CI-observed label
- an estimated timing cannot prove a PASS

### 6. Time to Recovery (TTR)

Verify:

- expected errors in the changed surface have corrective guidance
- an expected error without cause, fix, and retry-safety triggers `UNEXPLAINED_ERROR`
- TTR follows the `TTR_TARGET_MIN` target

### 7. Gate vocabulary application

- Return exactly one verdict: PASS / PASS WITH DEBT / FAIL / UNVERIFIED.
- A gate failure forces FAIL. A score never overrides a gate.
- Missing evidence is UNVERIFIED for that gate; never convert it to PASS on assumptions.
- Supported-version claims without CI evidence trigger `UNTESTED_SUPPORTED_VERSION`; unreproducible local setup triggers `NON_REPRODUCIBLE_BUILD`.

## Result

- **PASS:** no P0/P1 gate failures; required hard gates pass.
- **PASS WITH DEBT:** no hard gate failure, but P2/P3 backlog remains.
- **FAIL:** one or more P0/P1 gates fail.
- **UNVERIFIED:** evidence is insufficient to prove critical gates.

Read `references/standards.md` for the canonical severity levels and verdict vocabulary.
