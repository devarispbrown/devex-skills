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


## Problem classification

Nine classes, attributed by root cause, never by which team writes the fix:

| Class | Attribution rule |
|---|---|
| Product | core product behavior or workflow design is the root cause |
| API | HTTP/RPC surface design: resources, naming, semantics |
| CLI | command surface: hierarchy, flags, output, exit codes |
| SDK | language wrapper design or parity gaps |
| Configuration | config surface, defaults, precedence, secrets handling |
| Environment | toolchains, versions, ports, OS/arch issues |
| Documentation | docs alone can fix it |
| Infrastructure | provisioning/build/runtime latency or reliability |
| Third-party | external approval, quota, API, network, service |

**Legacy mapping**: the docs-auditor's four classes map directly — Docs → Documentation; Product/DX → Product, API, CLI, SDK, or Configuration (pick by root cause); Infrastructure → Infrastructure; External dependency → Third-party.

Documentation must not absorb blame for product defects.


## Journey stages

The developer journey is 14 canonical stages. Audits may scope to a subset; unscoped audits walk all 14.

| Stage | Definition | Stop condition |
|---|---|---|
| find | locate the product and understand its claim | can state what the product does and whether it fits |
| understand | grasp concepts and architecture | can explain core concepts without guessing |
| install | get the software running | product installed or sandbox available |
| auth | authenticate or provision an account | authenticated, credential usable |
| configure | set up required configuration | configuration accepted, no unknowns |
| execute | run the core workflow | core workflow completed |
| verify | confirm the result | end-to-end outcome verified |
| modify | make a change to something owned | change applied |
| break | intentionally break something | failure reproduced on demand |
| diagnose | find the cause | root cause identified |
| recover | fix or work around the failure | state restored, workflow resumed |
| test | run the test suite meaningfully | tests green, coverage understood |
| deploy | ship to a target environment | deployment verified |
| upgrade | move to a newer version | upgrade completed, behavior intact |

**Legacy aliases** (superseded, not parallel): the 13-stage list in `developer-docs` (Discover → Prerequisites → Install → Account/Auth → Configure → First value → Verify → Customize → Debug → Production → Operate → Upgrade → Get help) and the 7-stage list in `docs-architecture.md` are subsets of these 14. All stages they name exist above.
