# DX Report — <product name>

## Verdict

**Release gate:** PASS | PASS WITH DEBT | FAIL | UNVERIFIED
**Overall DX:** __/100 (evidence: Observed | CI-observed | Estimated | UNVERIFIED)

## Evidence

- Repository/revision:
- Environment (OS, versions, clean-clone date):
- Journey scope (stages in scope):
- Checks executed:
- Checks not executed:

## Magic path

**Status:** PASS | FAIL | UNVERIFIED
**Evidence:** Observed | CI-observed | Estimated
**Elapsed:** __ min __ sec (gate: `MAGIC_PATH_MAX_MIN`)
**Start / stop condition:**

| Metric | Count | Target | Status |
|---|---:|---:|---|
| Commands | | `MAGIC_PATH_MAX_COMMANDS` (P2) | |
| Credentials | | `MAGIC_PATH_MAX_CREDENTIALS` (P2) | |
| Context switches | | `MAGIC_PATH_MAX_CONTEXT_SWITCHES` (P2) | |

## Per-stage timing

| Stage | Objective met? | Time | Commands | Credentials | Context switches | Errors | Evidence |
|---|---|---|---|---|---|---|---|
| find | | | | | | | |
| understand | | | | | | | |
| install | | | | | | | |
| auth | | | | | | | |
| configure | | | | | | | |
| execute | | | | | | | |
| verify | | | | | | | |
| modify | | | | | | | |
| break | | | | | | | |
| diagnose | | | | | | | |
| recover | | | | | | | |
| test | | | | | | | |
| deploy | | | | | | | |
| upgrade | | | | | | | |

## Per-area scores

| Area | Weight | Score | Evidence | Notes |
|---|---:|---:|---|---|
| Time to first value | 20 | | | |
| API | 15 | | | |
| SDK | 10 | | | |
| CLI/config | 10 | | | |
| Errors/recovery | 12 | | | |
| Documentation | 10 | | | |
| Local dev | 8 | | | |
| Testing/quality | 8 | | | |
| Release/compatibility | 7 | | | |
| **Overall DX** | 100 | | | |

## Gate failures

| Gate | Severity | Stage | Finding | Evidence | Acceptance test |
|---|---|---|---|---|---|
| | | | | | |

## Problem-classification backlog

| Priority | Problem class | Stage | Finding | Owner skill | Acceptance test |
|---|---|---|---|---|---|
| | | | | | |

## Delegated evidence

| Finding | Delegated skill | Verdict | Re-verified? | Disagreements reported |
|---|---|---|---|---|
| | | | | |

## World-class checklist

- [ ] all hard gates pass
- [ ] Overall DX >= world-class threshold (procedure in `references/dx-scoring.md`)
- [ ] no unresolved P0/P1 findings
- [ ] magic path Observed or CI-observed at <= `MAGIC_PATH_MAX_MIN`
