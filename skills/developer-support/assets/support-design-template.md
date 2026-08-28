# Support Routing Design

## Request classes and channels

| Request class | Primary channel | Secondary channel | Owner | Response commitment |
|---|---|---|---|---|
| Bug | | | | |
| Feature | | | | |
| How-to | | | | |
| Security | | | | |
| Billing | | | | |
| Outage | | | | |
| Data loss | | | | |

Tie-break rule for requests that fit two classes:

## Escalation ladder

| Rung | Entry condition | Promotion criteria | Evidence required |
|---|---|---|---|
| Error message | | | |
| Troubleshooting | | | |
| Search | | | |
| Community | | | |
| Ticket | | | |
| Engineering | | | |

Jump rules (classes that skip rungs):

## Diagnostic collection

| Field | Collection point | Required? | Sanitization |
|---|---|---|---|
| Version | | | |
| SDK version | | | |
| Request ID | | | |
| Trace ID | | | |
| Environment | | | |
| Config | | | |
| Sanitized logs | | | |

Ticket gate rule (what happens to an incomplete request):

## Response behavior

| Situation | Bot or human | Template / rule |
|---|---|---|
| Acknowledgment | | |
| Missing diagnostics | | |
| Template-resolvable request | | |
| Resolution | | |
| Escalation handoff | | |
| Security / billing / outage / data loss | | |

## Metrics

| Metric | Definition | Target | Evidence label |
|---|---|---|---|
| Routing efficiency | | | |
| Escalation rate | | | |
| Time to recovery | vs `TTR_TARGET_MIN` | | |
| Promotion bounce rate | | | |

## Scanner report

Attach the output of `scripts/scan_support_channels.py` against the repository.

## Gap ledger

| Gap | Fix | Owner | Due |
|---|---|---|---|
| | | | |
