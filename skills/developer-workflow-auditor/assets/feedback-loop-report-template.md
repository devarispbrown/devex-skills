# Feedback Loop Audit Report

- **Project:** {{project}}
- **Date:** {{date}}
- **Auditor:** {{auditor}}
- **Environment:** {{environment}}

## Loop map

| Stage | Loop | Action-to-feedback path |
|---|---|---|
| {{stage}} | {{inner/outer}} | {{action that starts the segment}} → {{feedback that ends it}} |

## Measurements

| Stage | Budget constant | Measured | Result | Evidence | Environment |
|---|---|---|---|---|---|
| {{stage}} | {{FEEDBACK_* constant name}} | {{seconds}}s | {{PASS/BREACH}} | {{Observed/CI-observed/Estimated}} | {{clean/warm}} |

Checker command and exit code: `python3 scripts/audit_feedback_loops.py {{manifest}}` — {{0 or 1}}

## Breach analysis

| Breach | Root cause | Severity | Fix | Verified |
|---|---|---|---|---|
| {{stage}} | {{cold cache / full rebuild / serial dependency / missing incremental path / CI queue / review latency}} | {{P1/P2}} | {{smallest fix}} | {{not yet / re-measured {{seconds}}s}} |

## Flow-state findings

{{forced waits >30 seconds between edit and feedback, context switches, interruptions observed, each with a P2 severity}}

## Verdict

{{PASS — no budget breaches; or FAIL — summary of P1/P2 findings}}

## Recommendations

{{smallest fix per breach, in priority order, with verification status}}
