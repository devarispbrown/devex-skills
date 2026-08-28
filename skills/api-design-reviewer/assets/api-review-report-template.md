# API Design Review Report

## Scores

**API DX Score:** __/100  
Evidence: Observed | CI-observed | Estimated

**OpenAPI Correctness Score:** __/100  
Evidence: Observed | CI-observed | Estimated

**Verdict:** PASS | PASS WITH DEBT | FAIL | UNVERIFIED

## Evidence

- Repository/revision:
- Contract reviewed (OpenAPI/Proto/observed behavior):
- Checks executed:
- Checks not executed:
- Guessability probes run: yes | no

## Findings

| Severity | Owner | Surface | Finding | Evidence | Acceptance test |
|---|---|---|---|---|---|
| P0 | API/Product/Docs | <path or surface> | <finding> | <observed/estimated> | <test> |
| P1 | | | | | |

Owner types: **API** (contract design), **Product** (scope and decisions), **Docs** (documentation and guidance).

## Guessability probe results

| # | Probe | Score (1/0.5/0) | Evidence / note |
|---|---|---|---|
| 1 | Endpoint | | |
| 2 | Path parameters | | |
| 3 | Collection shape | | |
| 4 | Pagination | | |
| 5 | Filtering and sorting | | |
| 6 | Errors | | |
| 7 | Enums | | |
| 8 | Naming | | |
| 9 | Methods | | |
| 10 | Reliability | | |

## OpenAPI structural pass

- Unique operationIds: PASS | FAIL
- Resolvable $refs: PASS | FAIL
- Examples decode: PASS | FAIL
- 4xx/5xx responses: PASS | FAIL

## Dimension scores (API DX)

| Dimension | Weight | Score | Note |
|---|---|---|---:|---|
| Consistency | 20 | | |
| Guessability | 20 | | |
| Resource model | 15 | | |
| Errors | 15 | | |
| Reliability | 10 | | |
| Async operations and events | 8 | | |
| Authentication and authorization | 7 | | |
| Versioning | 5 | | |

## Prioritized backlog

| Priority | Owner type | Change | Acceptance test |
|---|---|---|---|
| P1 | | | |
| P2 | | | |
| P3 | | | |
