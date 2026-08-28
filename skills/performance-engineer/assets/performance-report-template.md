# Performance Report

## Budgets

| Surface | Metric | Budget | Unit | Owner |
|---|---|---|---|---|
| <surface> | <metric> | <budget> | <unit> | <owner> |
| <surface> | <metric> | <budget> | <unit> | <owner> |

## Measured vs budget

Environment: <machine, OS, toolchain, revision, date>

| Surface | Metric | Measured | Budget | Unit | Status | Evidence |
|---|---|---|---|---|---|---|
| <surface> | <metric> | <value> | <budget> | <unit> | <PASS\|NEAR MISS\|BREACH\|UNVERIFIED> | <Observed\|CI-observed\|Estimated> |
| <surface> | <metric> | <value> | <budget> | <unit> | <PASS\|NEAR MISS\|BREACH\|UNVERIFIED> | <Observed\|CI-observed\|Estimated> |

## Findings

| Priority | Finding | Evidence | Fix recommendation |
|---|---|---|---|
| <P0–P4> | <what is slow and why it matters to users> | <profile/bisect evidence, artifact links> | <smallest evidence-backed change> |
| <P0–P4> | <what is slow and why it matters to users> | <profile/bisect evidence, artifact links> | <smallest evidence-backed change> |

## Gate recommendation

**Gate:** <PASS | PASS WITH DEBT | FAIL | UNVERIFIED>

- Reasoning: <tied to the measured values per budget, never to sentiment>
- Breach handling: <fail | warn | debt> per breached or near-miss budget; accepted debt carries <owner, ticket, deadline>

## Baselines and history

- Baseline recorded: <revision, date, location>
- Recent trend: <measured values over the last N runs, or "no history yet">

## Sign-off

- Budget owner: <name>
- Gate verdict: <verdict>
- Blocking items: <list or "none">
