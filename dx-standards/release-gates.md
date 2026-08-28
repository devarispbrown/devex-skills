# Release Gates

Canonical named gates for the suite. Each gate names a release-blocking condition; a skill finding references the gate constant, not a paraphrase. Gates supersede and extend the prose gate list in `skills/developer-docs-auditor/references/release-gating.md`, which points here.

## Gate identifiers

| Gate constant | Severity | Fails when |
|---|---|---|
| `BROKEN_QUICKSTART` | P1 | magic path exceeds `MAGIC_PATH_MAX_MIN`, no reproducible end-to-end quickstart exists, or manual approval/support is required with no sandbox route |
| `NON_REPRODUCIBLE_BUILD` | P1 | a clean checkout cannot reach the productive state within `LOCAL_DEV_MAX_MIN` using only committed instructions/automation |
| `UNEXPLAINED_ERROR` | P1 | a public, expected error lacks what happened / why / where / how to fix / retry-safety, or a support-correlation identifier |
| `UNDOCUMENTED_BREAKING_API` | P0 | a breaking API/CLI/config change ships without changelog entry and migration guidance |
| `SDK_API_DRIFT` | P1 | a released official SDK is missing operations or contradicts the canonical API |
| `UNTESTED_SUPPORTED_VERSION` | P1 | a version/platform is claimed supported without CI or equivalent evidence |
| `STALE_PUBLIC_REFERENCE` | P1 | generated reference observably disagrees with current behavior |
| `UNSAFE_EXAMPLES` | P1 | security-sensitive examples encourage unsafe credential handling |
| `BROKEN_CANONICAL_INSTALL` | P1 | canonical install/auth path is broken |

## Community gates

Community gate constants (`NO_CONTRIBUTING_WHILE_WELCOMING`, `UNRESPONSIVE_ISSUES`, `BROKEN_CONTRIBUTION_PATH`, and the rest) live in `community.md` and use the same severity levels and verdict vocabulary as this file.

## Gate semantics

- Hard gates cannot be averaged away by any score. A failing gate forces FAIL regardless of the Overall DX number.
- Conditional gates (missing SDK update/parity, undocumented new errors/events/config, missing changelog entry, missing production guidance for preview-to-stable promotion, missing rollback/migration path) become blockers when material to the changed surface.
- Gate result: PASS / PASS WITH DEBT / FAIL / UNVERIFIED, per the verdict vocabulary in `severity.md`.
