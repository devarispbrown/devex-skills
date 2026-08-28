# Recertification

## Purpose

Certification is a timestamp, not a property. Evidence expires, cells go stale, and claims must be re-verified on a schedule and when the world changes.

## Cadence

- Define a recertification interval per product area; quarterly is a common default, faster for fast-moving services.
- A cell whose last-tested date is older than the staleness threshold is stale; `scripts/check_certifications.py` flags it (default 90 days, override with `--stale-after-days`).
- Re-run the full matrix on schedule even when nothing changed. "Nothing changed" is exactly when claims silently rot.

## Drift triggers

Recertify immediately, not at the next scheduled run, when any of these change:

1. **Dependency bumps** — the client SDK, connector, or adapter library version changes.
2. **Service changes** — the integration target ships a new version, retires a version, or changes an API contract.
3. **Config changes** — auth model, protocol, feature flags, or defaults change on either side.
4. **Product changes** — our own release changes the integration surface.
5. **Evidence link rot** — a stored evidence link no longer resolves.
6. **User reports** — a reported failure contradicts a certified cell.

## Handling drift

For each trigger:

1. Identify the affected cells in the matrix.
2. Re-run those cells' tests.
3. Update evidence links and last-tested dates on success.
4. On failure, investigate; if the integration is genuinely broken, downgrade the cell to uncertified and remove or rewrite the claim; see `references/certification-publishing.md`.
5. Record the recertification run in the report.

## Evidence expiry rules

- A stale cell is not certified. Staleness is not a "pending" state.
- Never extend a last-tested date without a real test run.
- Never recertify by re-reading old evidence.

## Ownership

Assign an owner per integration. An integration with no owner is uncertified by default.
