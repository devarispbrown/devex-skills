# Contributor Experience Report

**Repository:** <repo> @ <commit-or-date>
**Audit scope:** <fork-to-merge | fork-to-PR-ready | stage subset>
**Auditor:** <name-or-agent>
**Evidence labels:** Observed / CI-observed / Estimated — every number carries one.

## Journey timing

| Stage | Time | Evidence | Blockers / friction hit |
|---|---|---|---|
| Fork | <time> | <label> | <friction> |
| Clone | <time> | <label> | <friction> |
| Build | <time> | <label> | <friction> |
| Test | <time> | <label> | <friction> |
| Find issue | <time> | <label> | <friction> |
| Change | <time> | <label> | <friction> |
| Checks | <time> | <label> | <friction> |
| PR | <time> | <label> | <friction> |
| Review | <time> | <label> | <friction> |
| Merge | <time> | <label> | <friction> |

Fork-to-PR-ready total: <total> against `FIRST_CONTRIBUTION_TARGET_MIN` (cite the constant by name; do not restate its value).

## Funnel findings

| # | Stage | Severity (P0–P4) | Finding | Evidence |
|---|---|---|---|---|
| <1> | <stage> | <severity> | <finding> | <evidence> |
| <2> | <stage> | <severity> | <finding> | <evidence> |

Include at minimum: guidance file gaps, issue discoverability gaps, check-parity drift, review responsiveness, DCO/CLA status.

## Check parity

- Local canonical check: <command> (<source file>)
- CI test commands: <commands>
- Parity: <in parity | drift — describe>
- Versions compared: <local vs CI>

## Fix list

| Priority | Fix | Stage fixed | Acceptance test | Owner type |
|---|---|---|---|---|
| <1> | <fix> | <stage> | <fresh walk of the stage passes> | <owner> |
| <2> | <fix> | <stage> | <fresh walk of the stage passes> | <owner> |

## Definition of done checklist

- [ ] every stage carries a labeled measurement
- [ ] every finding carries a severity and evidence
- [ ] parity verified against actual commands, not claims
- [ ] review responsiveness measured on real PR history
- [ ] no numeric threshold restated; canonical constants cited by name
