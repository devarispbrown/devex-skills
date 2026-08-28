# Compatibility Analysis

Behavioral compatibility means documented consumers keep behaving after the upgrade. Analyze per consumer, never in aggregate.

## The consumer list

Walk every consumer type for each classified surface:

1. **JSON/response parsers** — added or renamed fields, type changes, null vs omitted, ordering. Strict parsers and serialization round-trips break on additions.
2. **Enum exhaustiveness** — `switch` statements, exhaustive matches, generated code. A new enum value can break a compiled switch or a validation pass.
3. **Generated SDKs** — clients generated from the canonical schema. Missing or contradictory operations are `SDK_API_DRIFT`.
4. **Migrations and DB schemas** — persisted columns, indexes, constraints, data transforms. Migration files are consumers of the schema.
5. **Configuration parsers** — renamed or removed keys, changed defaults, changed precedence, stricter validation.
6. **Webhook handlers** — payload shape changes, new event types, signature changes, retry behavior.
7. **Log/metric/dashboard consumers** — renamed metrics, changed units, changed event names, removed fields.
8. **Shell scripts on CLI output** — exit codes, stdout/stderr formatting, column order. Text parsing breaks on cosmetic changes.
9. **Preview/beta users** — consumers relying on documented-but-unstable behavior; promotion to stable is a contract change.

## Procedure

1. For each classified change, list the consumers that observe it.
2. For each consumer, determine whether its documented behavior changes.
3. State the impact per consumer with evidence: signature, test, or observed run.
4. Label every claim Observed, CI-observed, or Estimated.
5. An unverified consumer is UNVERIFIED for that consumer, never assumed compatible.

Run `scripts/scan_compat_consumers.py` against the tree to find candidate consumers. Confirm candidates semantically; the scan is a signal, not a verdict.

## Rules

- Compatibility is per documented consumer, not per API surface.
- An addition is breaking until proven additive for every consumer that observes it.
- Do not call a release compatible because the public signature is unchanged.
- Do not smooth over a breaking consumer impact because the change is an improvement.
- Preview/beta semantics must be explicit: opt-in, stability promise, promotion path.
