# Community Health Score Procedure

## Purpose

The Community Health Score (CHS) is a weighted sum of ten dimensions, each scored 0–100. It measures outcomes, not activity. It never overrides a gate.

## Dimensions and weights

Each dimension carries a weight constant. The numeric weights are defined in the checker's constants table and in the generated standards; they are never restated in hand-written files:

| Dimension | Weight constant | What it measures |
|---|---|---|
| funnel health | FUNNEL_HEALTH_WEIGHT | cohort conversion ratios through the funnel |
| responsiveness | RESPONSIVENESS_WEIGHT | response SLO compliance over the trailing 30 days |
| standards presence | STANDARDS_PRESENCE_WEIGHT | presence and quality of the eight standards files (including LICENSE) |
| contribution opportunities | CONTRIBUTION_OPPORTUNITIES_WEIGHT | usable newcomer issues and backlog health |
| governance and ladder | GOVERNANCE_LADDER_WEIGHT | governance honesty and ladder climbability |
| review experience | REVIEW_EXPERIENCE_WEIGHT | review speed and change acceptance |
| contributor retention | CONTRIBUTOR_RETENTION_WEIGHT | returning and new contributor share |
| maintainer sustainability | MAINTAINER_SUSTAINABILITY_WEIGHT | bus factor, maintainer depth, area coverage; the Maintainer Concentration Index is reported as its own line, never folded in |
| Q&A support | QA_SUPPORT_WEIGHT | useful-answer rate and speed; when `community_answer_share` is present, the blend is 0.5 rate + 0.3 speed + 0.2 share, else 0.6 rate + 0.4 speed. `community_answer_share` = useful answers from non-maintainers / total useful answers |
| recognition and automation | RECOGNITION_AUTOMATION_WEIGHT | recognition program and contribution automation |

The weights sum to 100; the CHS is the weighted mean of the dimension scores.

## Scoring

Score each dimension per its audit step; the checker `scripts/check_community_health.py` implements the arithmetic from the community-health JSON. The JSON input contract and the per-dimension formulas are defined by the checker's constants table and input schema; override any constant via the JSON `constants` key when the project's canonical values differ.

## Evidence labels

Every dimension score carries an evidence label: Observed, CI-observed, or Estimated. A score without a label is UNVERIFIED. An UNVERIFIED dimension contributes zero to the CHS and flags the CHS as UNVERIFIED. An estimate can never prove a gate PASS.

## Tiers

The tier is derived from the CHS against the tier constants: healthy at or above `CHS_HEALTHY_MIN`, developing at or above `CHS_DEVELOPING_MIN`, at risk below. Tiers describe health; they do not override gates.

## Gates override scores

A failing gate forces FAIL regardless of the CHS:

- hard-failure gates — `NO_CONTRIBUTING_WHILE_WELCOMING`, `NO_CODE_OF_CONDUCT`, `BROKEN_CONTRIBUTION_PATH`, `DEAD_END_COMMUNITY`
- remaining P1 gates — `UNRESPONSIVE_ISSUES`, `UNREVIEWED_FIRST_PR`, `OPAQUE_GOVERNANCE`, `STALE_GOOD_FIRST_ISSUES`, `UNACKNOWLEDGED_PRS`, `NO_LICENSE`
- P2 gates — `NO_GOOD_FIRST_ISSUES`, `NO_RECOGNITION_PATH`

A community at risk with no gate failure is reported with its tier; a healthy score with a failing gate is FAIL. Record the verdict as exactly one of PASS, PASS WITH DEBT, FAIL, UNVERIFIED.

## Checker

Assemble the community-health JSON per `assets/community-health.example.json` and run:

`python3 scripts/check_community_health.py <community-health.json>`

The checker prints the score card, tier, gate results, and verdict, and exits 1 when any named community gate fails. Use `assets/community-health.clean.json` as the all-gates-pass reference.
