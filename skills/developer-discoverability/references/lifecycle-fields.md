# Lifecycle Fields

## Purpose

Lifecycle is the contract between the catalog and its consumers: what may I rely on, how long, and what happens next. Every entry carries exactly one lifecycle value.

## Canonical lifecycle vocabulary

- **experimental** — under active design; may change or disappear; no compatibility promise
- **production** — the supported, default choice for new consumers
- **maintenance** — stable but no new features; fixes and security patches continue
- **deprecated** — replaced; consumers must plan migration; replacement and timeline are recorded
- **retired** — removed or replaced; only the historical entry remains, pointing at the replacement

Platforms may extend the vocabulary, but every extension is documented and every entry still maps to one canonical value.

## Field semantics

- `lifecycle` and `status` are separate. Lifecycle is the product's commitment; status is operational state (active, degraded, retired). A production service can be degraded; a deprecated package can still be operational.
- `docs_link` content must match the lifecycle: deprecated things link to migration docs, not to install docs.
- experimental entries state what may change; production entries state the support and security commitment.

## Transition rules

- **Experimental → production** requires a compatibility statement and changelog discipline (see the `release-guardian` skill's contracts).
- **Production → maintenance** is announced; consumers are told what will and will not change.
- **Deprecation** always records: the replacement entry link, the sunset date or window, and the migration path. A deprecation without a replacement link is a P1 defect.
- **Retirement** happens after the sunset window; the entry remains with `status: retired` and the replacement link so search still resolves.

## Staleness

A catalog entry is stale when it no longer matches the thing it describes: wrong version, moved docs, changed owner, dead links, or a lifecycle that contradicts reality.

- every entry records `last_verified`
- staleness beyond the platform threshold is a P2 defect; entries in production or published that mislead consumers beyond the threshold are P1
- staleness is detected by scheduled verification and by the feedback loop (search logs, 404s) in `discoverability-feedback-loops.md`
- a metric without an evidence label is UNVERIFIED per `references/standards.md`

## Severity mapping

- misclassified lifecycle (production thing marked experimental, or vice versa): P1
- undocumented deprecation of a published artifact: P1
- missing replacement link on a deprecated entry: P1
- stale version or docs link: P2
- missing `last_verified`: P3
