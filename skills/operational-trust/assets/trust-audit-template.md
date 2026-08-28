# Trust Surface Audit Report

## Posture

**Trust posture:** <TRUSTED | PASS WITH DEBT | BROKEN>

## Evidence

- Repository/revision: <repo> @ <rev>
- Environment: <env>
- Checks executed: <list, including scanner run>
- Checks not executed: <list>
- Evidence labels: <Observed | CI-observed | Estimated> per claim

## Trust surface checklist

| Surface | Present | Evidence | Notes |
|---|---|---|---|
| Status page config | <yes\|no\|partial> | | |
| Incident templates | | | |
| SLO/SLA publication | | | |
| Webhook delivery guarantees | | | |
| Retry behavior | | | |
| Degraded-state signaling | | | |
| Maintenance windows | | | |
| Incident history | | | |

## Gap analysis

| Gap | Severity | User impact | Acceptance test |
|---|---|---|---|
| <gap> | <P0–P4> | | |

## Recovery assessment

| Expected error | Cause guidance | Corrective action | Retry-safe | TTR vs `TTR_TARGET_MIN` |
|---|---|---|---|---|
| <error> | | | | <meets\|exceeds\|unverified> |

## Fix backlog

| Priority | Finding | Owner type | Verification |
|---|---|---|---|
| <P0–P4> | | | |

## Sign-off

- Trust posture: <posture>
- Must-fix before next release: <list or "none">
