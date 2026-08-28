<!-- GENERATED FILE - do not edit by hand. Source: dx-standards/. Regenerate with: python3 scripts/sync-standards.py -->

# Severity and Verdict Vocabulary

Canonical severity levels and verdict vocabulary for every skill in the suite.

## Severity levels

- **P0 Blocker:** unsafe, impossible, materially incorrect, data/security/production risk.
- **P1 Critical:** blocks first success, breaks a hard gate (magic path, local dev), or incorrectly documents a public contract.
- **P2 Major:** important missing workflow, stale example, API/SDK mismatch, poor error recovery, substantial drift.
- **P3 Minor:** clarity, navigation, terminology, maintainability.
- **P4 Polish:** presentation/style only.

Prioritize defects that prevent developers from succeeding over cosmetic completeness.

## Verdict vocabulary

Every release or audit verdict returns exactly one of:

- **PASS:** no P0/P1 gate failures; required hard gates pass.
- **PASS WITH DEBT:** no hard gate failure, but P2/P3 backlog remains.
- **FAIL:** one or more P0/P1 gates fail.
- **UNVERIFIED:** evidence is insufficient to prove critical gates; do not convert this to PASS based on assumptions.

A high numerical score cannot override a hard-gate failure.

## Report labeling

Every score and timing reported by any skill must carry its evidence label (Observed / CI-observed / Estimated). Unlabeled numbers are UNVERIFIED.

## Evidence hierarchy

Prefer, in order:

1. observed execution against a clean/representative environment
2. implementation/tests/specs
3. generated/current interface output such as `--help`
4. package/release metadata
5. examples
6. prose docs

When sources disagree, report the contradiction.


## Evidence labels

- **Observed**: a human or agent actually executed the path from a clean or representative environment.
- **CI-observed**: automation executed the product steps; may undercount human reading/signup time.
- **Estimated**: steps analyzed but not executed.
- An estimate can never prove a PASS. A metric without an evidence label is UNVERIFIED.


## Recovery thresholds

- `TTR_TARGET_MIN` = 5. Time to Recovery target for expected errors: from hitting the error to completing the corrective action. >10 min = P2.


## Canonical terms

- **magic path**: the canonical getting-started route delivering verified end-to-end value.
- **quickstart**: the artifact documenting the magic path.
- **zero-to-value**: the find→verify span of the journey.
- **Time to Recovery (TTR)**: time from hitting an expected error to completing its corrective action.
- **DX Report**: the structured output of a developer-experience audit (per-area scores, Overall DX, gates).
- **capability matrix**: per-SDK/language table of implemented capabilities.
- **drift**: divergence between documentation/generated artifacts and current behavior.
- **parity**: semantic equivalence of SDKs (or docs) with the canonical API.
