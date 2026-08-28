# Compatibility Matrix Design

## Purpose

Define which combinations of runtime, database, platform, and architecture the product claims to support, and discipline every claim into a verifiable row. The matrix JSON is the single source of truth for support claims; prose in docs and release notes must agree with it.

## Procedure

1. Enumerate the dimensions the product actually exercises: runtime versions, databases, platforms, architectures. Add a dimension only when behavior can differ across it; a pure-Python package's architecture matrix may be empty.
2. For each dimension, list candidate versions from the claim inventory: docs, package metadata, CI configs, changelogs, support pages.
3. Assign every cell exactly one tier (below). Unlisted versions are untested and must never be implied supported.
4. Write the matrix as JSON per the schema below, one claim per surface plus exact version string.
5. Run `scripts/check_compat_matrix.py`; fix or downgrade every failing row before the matrix ships.

## Tier labels

- **supported** — tested and verified; the only tier that may appear in docs as a support claim. Requires evidence.
- **best-effort** — expected to work, no promise; cannot be claimed as supported; may break at any time without notice.
- **deprecated** — still shipped; end-of-support date recorded; no new evidence required; no new users directed to it.

## Claim discipline

- One row per surface plus exact version string. "Python 3.x" is not a claim; "python 3.11" is.
- Evidence must name the exact claimed version; a neighboring version in CI does not count.
- Tier changes and removals are release events; record removals as deprecated, never delete silently.
- Never add a supported row to make docs look current. Claim what CI runs; otherwise downgrade the tier.

## Matrix JSON schema

```json
{
  "product": "<name>",
  "updated": "YYYY-MM-DD",
  "claims": [
    {
      "surface": "runtime | database | platform | architecture | dependency | wire-schema",
      "version": "<exact version string>",
      "tier": "supported | best-effort | deprecated",
      "evidence": {
        "type": "ci | marker | link",
        "file": "<repo-root-relative path>",
        "match": "<string the CI workflow must contain>",
        "url": "<recorded CI run link>"
      }
    }
  ]
}
```

`evidence` is required only for supported rows. `ci` requires `file` and `match`; `marker` requires `file`; `link` requires `url`. Evidence paths resolve against the checker's `--root`.
