# Community Health Report — <repo>

**Audit date:** <date>
**Verdict:** <PASS | PASS WITH DEBT | FAIL | UNVERIFIED>
**Evidence level:** <Observed | CI-observed | Estimated | UNVERIFIED>
**Community stage:** <founder-led | early | growing | scale | foundation>
**Window:** trailing 90 days (activity, funnel) / trailing 30 days (responsiveness)

## 1. Community Health Score

| Dimension | Weight | Score | Evidence |
|---|---|---|---|
| funnel health | <weight> | <score> | <label> |
| responsiveness | <weight> | <score> | <label> |
| standards presence | <weight> | <score> | <label> |
| contribution opportunities | <weight> | <score> | <label> |
| governance and ladder | <weight> | <score> | <label> |
| review experience | <weight> | <score> | <label> |
| contributor retention | <weight> | <score> | <label> |
| maintainer sustainability | <weight> | <score> | <label> |
| Q&A support | <weight> | <score> | <label> |
| recognition and automation | <weight> | <score> | <label> |

**Community Health Score:** <chs> — Tier: <healthy | developing | at risk>

## 2. Community Magic Path

**Status:** <PASS | FAIL | UNVERIFIED>
**Elapsed:** <minutes> minutes vs `COMMUNITY_ONBOARDING_PATH_MAX_MIN` (<Observed | CI-observed | Estimated>)
**Implementation time excluded:** <yes | no>
**Stages reached:** <discover | understand | ask | find | setup | first PR | ready-for-review>
**Friction attribution:** <docs / labels / setup / review / governance findings>
**Blocker:** <blocker or none>

## 3. Responsiveness SLOs

| Metric | P50 (h) | P90 (h) | SLO constant | Result |
|---|---|---|---|---|
| Issue first response | <p50> | <p90> | `COMMUNITY_ISSUE_RESPONSE_P50_H` / `COMMUNITY_ISSUE_RESPONSE_P90_H` | <PASS | FAIL> |
| First-PR review | <p50> | <p90> | `COMMUNITY_FIRST_PR_REVIEW_P50_H` / `COMMUNITY_FIRST_PR_REVIEW_P90_H` | <PASS | FAIL> |
| Useful answer | — | <p90> | `COMMUNITY_USEFUL_ANSWER_P90_H` | <PASS | FAIL> |

**Non-bot denominator:** <n> events

## 4. Contribution funnel

| Transition | Numerator | Denominator | Conversion | Leak |
|---|---|---|---|---|
| participants → first PR | <n> | <n> | <%> | <drop-off | bottleneck | dead end> |
| first PR → merged | <n> | <n> | <%> | <…> |
| merged → second contribution | <n> | <n> | <%> | <…> |
| regular → reviewer | <n> | <n> | <%> | <…> |
| reviewer → maintainer | <n> | <n> | <%> | <…> |

## 5. Gate results

| Gate | Severity | Result | Evidence |
|---|---|---|---|
| <gate constant> | P1 | <PASS | FAIL> | <evidence> |
| <gate constant> | P2 | <PASS | FAIL> | <evidence> |

## 6. Standards files

| File | Present | Quality | Findings |
|---|---|---|---|
| LICENSE | <yes | no> | <score> | <findings> |
| CONTRIBUTING.md | <yes | no> | <score> | <findings> |
| CODE_OF_CONDUCT.md | <yes | no> | <score> | <findings> |
| SECURITY.md | <yes | no> | <score> | <findings> |
| SUPPORT.md | <yes | no> | <score> | <findings> |
| GOVERNANCE.md | <yes | no> | <score> | <findings> |
| MAINTAINERS.md | <yes | no> | <score> | <findings> |
| Contributor ladder | <yes | no> | <score> | <findings> |

## 7. Governance and ladder

<findings: actual operation, decision authority, outsider path, ladder rungs, non-code paths, recognition>

## 8. Maintainer concentration

- Bus factor: <n> (<Observed | CI-observed | Estimated>)
- Elephant Factor: <n>
- Maintainer Concentration Index: <max single-maintainer share across review/merge/response, per references/maintainer-sustainability.md>
- Owners per critical area: <areas with multiple owners / critical areas>

## 9. Backlog of findings

| # | Severity | Finding | Gate | Fix owner |
|---|---|---|---|---|
| <n> | <P0 | P1 | P2 | P3> | <finding> | <gate constant> | <owner skill> |

## 10. Definition of done checklist

- [ ] community staged with observed evidence
- [ ] Community Magic Path run and timed (or report explains why not)
- [ ] eight standards files audited for presence and quality
- [ ] response SLOs measured over the trailing 30 days, bots excluded
- [ ] funnel and retention computed on cohorts with per-transition conversions
- [ ] governance, ladder, and recognition audited against the stage
- [ ] maintainer concentration, bus factor, and succession measured
- [ ] all ten dimensions scored and evidence-labeled
- [ ] every named gate applied; verdict is exactly one of PASS, PASS WITH DEBT, FAIL, UNVERIFIED
- [ ] checker run: `python3 scripts/check_community_health.py <community-health.json>`
