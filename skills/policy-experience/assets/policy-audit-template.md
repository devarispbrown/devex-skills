# Policy Audit Report

## Verdict

**Policy gate:** <PASS | PASS WITH DEBT | FAIL | UNVERIFIED>

## Evidence

- Repository/revision: <repo> @ <revision>
- Environment: <env>
- Checks executed: <list>
- Checks not executed: <list>
- Evidence labels: <Observed | CI-observed | Estimated> per claim

## Policy inventory

| Policy id | Source requirement | Rule location | Severity | Guardrail checkpoint |
|---|---|---|---|---|
| <id> | <framework/standard requirement> | <path> | <P0-P4> | <checkpoint> |

A requirement with no rule and a rule with no requirement are findings.

## Guardrail results

| Guardrail id | Policy id | Checkpoint | Result | Evidence |
|---|---|---|---|---|
| <id> | <id> | <pre-commit\|PR\|CI\|merge queue\|deploy\|runtime> | <PASS\|PASS WITH DEBT\|FAIL\|UNVERIFIED> | <evidence> |

No guardrail run goes unrecorded. A run that could not execute is UNVERIFIED, never PASS.

## Violation actionability

| Violation id | Policy id | what_happened | why | how_to_fix | request_exception | Result |
|---|---|---|---|---|---|---|
| <id> | <id> | <present\|missing> | <present\|missing> | <present\|missing> | <present\|missing> | <actionable\|opaque> |

Opaque violations are P1 findings and trigger `UNEXPLAINED_ERROR` at release gates.

## Exceptions

| Request id | Policy id | Scope | Duration | Approver chain | Status | Expiry | Evidence |
|---|---|---|---|---|---|---|---|
| <id> | <id> | <resources> | <dates> | <roles> | <approved\|denied\|expired\|revoked> | <date> | <evidence> |

## Audit trail summary

| Timestamp | Actor | Action | Policy id | Evidence hash |
|---|---|---|---|---|
| <ts> | <actor> | <requested\|approved\|denied\|expired\|renewed\|revoked> | <id> | <hash> |

Reconciliation: <active exceptions vs approved requests; expired exceptions removed>.

## Gate results

| Gate constant | Result | Evidence |
|---|---|---|
| UNEXPLAINED_ERROR | <PASS\|FAIL\|UNVERIFIED> | <opaque violation check> |
| NON_REPRODUCIBLE_BUILD | <PASS\|FAIL\|UNVERIFIED> | <guardrail run evidence> |
| <others as applicable> | | |

## Backlog (debt, when PASS WITH DEBT)

| Priority | Finding | Owner type | Acceptance test |
|---|---|---|---|
| <P0-P4> | | | |

## Sign-off

- Verdict: <verdict>
- Blocking items: <list or "none">
- Next review: <date or cadence>
