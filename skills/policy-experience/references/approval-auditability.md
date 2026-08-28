# Approval Auditability

An approval that cannot be audited did not happen. The audit trail is the compliance evidence; if it cannot prove who approved what, why, and until when, the process does not exist.

## Trail design

- append-only: entries are never edited or deleted
- tamper-evident: entries hash the state they approved, and the chain of hashes lands in commit history or a signed log
- durable: survives the tool that wrote it; exportable as JSON or CSV

## Entry fields

Each entry records:

- timestamp
- actor — who acted
- action — requested, approved, denied, expired, renewed, revoked
- `policy_id` and scope
- evidence — hash of the state at approval
- justification — why the action was taken
- expiry — when an approval lapses

## Enforcement history

Audits need more than approvals: every guardrail run is recorded too — rule, checkpoint, result, evidence. A compliance review asks whether the guardrail fired, not only who approved the deviation.

## Reconciliation

- active exceptions reconcile with approved requests
- expired exceptions drop out of the active set automatically
- approvals whose evidence hash matches no known state are flagged

## Retention and export

- retention follows the governing compliance requirement; when unspecified, retain for the product's documented data-retention period
- export on demand in JSON or CSV; the audit trail must not require a proprietary viewer

## Gate vocabulary

Unverifiable approval evidence is UNVERIFIED, never PASS by assumption. An expected error path without cause, fix, and retry guidance triggers `UNEXPLAINED_ERROR`.
