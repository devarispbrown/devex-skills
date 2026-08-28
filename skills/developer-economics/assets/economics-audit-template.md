# Developer Economics Report

Product: ___  Date: ___  Evidence label: Observed / CI-observed / Estimated

## 1. Surface inventory

| Surface | Kind | used | limit | reset | estimated cost |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 2. Checker results

`scripts/check_quota_surface.py <manifest>` — exit code ___, findings:

- ___

Not run because: ___

## 3. Findings

| # | Surface | Gap | Severity | Evidence | Required change |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 4. Design review

- Rate limits: PASS / FAIL / UNVERIFIED — ___
- Quota visibility: PASS / FAIL / UNVERIFIED — ___
- Cost estimation: PASS / FAIL / UNVERIFIED — ___
- Spend controls: PASS / FAIL / UNVERIFIED — ___
- Free tier: PASS / FAIL / UNVERIFIED — ___

## 5. Estimated deploy cost

- Workload: ___
- Per-unit prices: ___
- Total: ___ (bounds: ___)
- Hidden-cost surfaces: ___

## 6. Gates

- [ ] every metered surface has quota visibility
- [ ] every metered surface has cost estimation
- [ ] an estimate precedes any metered deploy
- [ ] spend caps are server-side enforced
- [ ] no finding is hidden by a score or an assumption

Verdict: PASS / PASS WITH DEBT / FAIL / UNVERIFIED
