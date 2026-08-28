# Certification Matrix Design

## Purpose

Turn the claims list into a single table that states, per (integration, version, configuration) cell, what evidence exists and when it was last verified.

## Matrix shape

One table per integration, with configurations as rows and versions as columns. A cell is one claim. If an integration has a single dominant configuration, collapse rows to one and let versions be the columns.

## Cell fields

Every cell holds exactly four fields:

1. `evidence_link` — a link to a real test run (CI job, report artifact, recorded run). A link to source code is not evidence; a passing run is.
2. `last_tested` — the date the evidence was produced.
3. `certified` — whether the claim is currently certified.
4. `configuration` — the exact configuration exercised, stated once per cell.

## Tiers

- **Certified** — evidence exists, the last-tested date is within the staleness threshold, and the test exercised the real service.
- **Certified with caveats** — evidence exists and is fresh, but the test covers only part of the configuration, or the configuration is a close-but-not-exact match. State the caveat in the cell.
- **Stale** — previously certified; evidence older than the staleness threshold.
- **Uncertified** — no evidence, no last-tested date, or explicitly marked not certified.

Never certify a cell with an estimate. Estimated evidence is not evidence.

## Evidence requirements per cell

- the test must exercise the real service, not a mock
- the test run must be reproducible from the repo: committed test plus CI job or recorded command
- the evidence link must resolve at publish time
- the evidence label is recorded: Observed, CI-observed, or Estimated

## Machine-readable form

Keep the matrix in JSON so the checker can audit it. One `integrations` array; each integration carries `integration` (name) and a `cells` list with the four fields above. The example at `assets/cert-matrix.example.json` shows the shape; `scripts/check_certifications.py` validates it.

## Guardrails

- A version listed in the matrix is not certified until its cell carries evidence.
- Do not merge configurations that exercise different code paths into one cell: different auth modes, transports, or feature sets stay separate.
- Do not mark a cell certified when the evidence is for a different version.
- The matrix states what is verified, never what the product "should" support.
