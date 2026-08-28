# Developer Experience Scoring

Scores are per-area judgments of the developer experience, not of the documentation. They are computed from journey evidence and labeled per the evidence rules.

## Per-area scores (0-100)

| Area | Weight | What it measures |
|---|---:|---|
| Time to first value | 20 | end-to-end time from find to verify against `MAGIC_PATH_MAX_MIN` |
| API | 15 | coherence and usability of the public API surface |
| SDK | 10 | SDK parity and idiomatic quality |
| CLI/config | 10 | command ergonomics, config model, defaults, precedence |
| Errors/recovery | 12 | error quality and TTR against `TTR_TARGET_MIN` |
| Documentation | 10 | whether docs drive the journey or mislead it |
| Local dev | 8 | clean-clone-to-productive against `LOCAL_DEV_MAX_MIN` |
| Testing/quality | 8 | test command, fixtures, and CI coverage of the journey |
| Release/compatibility | 7 | versioning, migration, upgrade, deprecation experience |

Weights sum to 100.

## Overall DX

Overall DX = round(Σ (weight x area score) / 100).

All nine areas must be scored. A missing or UNVERIFIED area makes Overall DX UNVERIFIED; do not substitute an assumed value.

## Evidence requirements per score

- A score of 85 or above requires **Observed** evidence in that area, executed from a clean or representative environment.
- A score of 70-84 requires **CI-observed** evidence or a review of implementation, specs, and generated interface output.
- A score below 70 may rest on **Estimated** evidence, labeled as such.
- A score without an evidence label is UNVERIFIED.
- An estimate can never prove a gate PASS, and a labeled score can never override a failing gate.

## World-class threshold

Claim world-class only when the full procedure passes:

1. all hard gates pass (magic path, local dev, and named gate constants)
2. Overall DX >= `WORLD_CLASS_OVERALL_DX`
3. every per-area score >= `WORLD_CLASS_MIN_AREA`
4. no unresolved P0/P1 findings
5. magic-path timing is Observed or CI-observed at <= `MAGIC_PATH_MAX_MIN`

Constants: `WORLD_CLASS_OVERALL_DX` = 85, `WORLD_CLASS_MIN_AREA` = 75.

A high Overall DX alone never makes a product world-class; the procedure is conjunctive.
