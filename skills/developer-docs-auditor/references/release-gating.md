# Documentation Release Gating

Documentation is part of the release contract for developer-facing products.

## Hard gates

The canonical named gate vocabulary (`BROKEN_QUICKSTART`, `STALE_PUBLIC_REFERENCE`, `UNSAFE_EXAMPLES`, `BROKEN_CANONICAL_INSTALL`, and the rest) lives in the generated `references/standards.md`; it is authoritative. This file documents the docs-scoped procedure.

Block a world-class/release-ready verdict for:

- magic path >15 minutes or no reproducible end-to-end quickstart
- public API/SDK/CLI/config docs materially disagree with current behavior
- required migration/deprecation guidance missing for a breaking change
- canonical install/auth path is broken
- security-sensitive examples encourage unsafe credential handling
- primary examples do not build/run when the repository provides a feasible test path
- generated reference is observably stale

## Conditional gates

Treat as release blockers when material to the changed feature:

- missing SDK update/parity
- undocumented new errors/events/config
- missing changelog entry
- no production guidance for a feature being promoted from preview to stable
- no rollback/migration path for operationally risky changes

Magic-path timing evidence may be supplied by a `developer-experience-auditor` DX Report; label its provenance.

## Gate result

Return one of:

- **PASS:** no P0/P1 gate failures; magic path passes.
- **PASS WITH DEBT:** no hard gate failure, but P2/P3 backlog remains.
- **FAIL:** one or more P0/P1 gates fail.
- **UNVERIFIED:** evidence is insufficient to prove critical gates; do not convert this to PASS based on assumptions.

A high numerical score cannot override a hard-gate failure.
