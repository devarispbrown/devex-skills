# Adversarial Documentation Audit Methodology

Audit as a skeptical external developer and release engineer. Do not reward prose quality when workflows are wrong, stale, ambiguous, or untestable.

## Evidence hierarchy

Prefer:

1. observed execution against a clean/representative environment
2. implementation/tests/specs
3. generated/current interface output such as `--help`
4. package/release metadata
5. examples
6. prose docs

When sources disagree, report the contradiction.

## Separate defect classes

Classify every finding primarily as:

- **Docs**: documentation can fix the issue.
- **Product/DX**: interface/workflow design is the root cause.
- **Infrastructure**: provisioning/build/runtime latency or reliability.
- **External dependency**: third-party approval, quota, API, network, etc.

Documentation must not absorb blame for product defects.

## Severity

- **P0 Blocker:** unsafe, impossible, materially incorrect, data/security/production risk.
- **P1 Critical:** blocks first success, breaks the ≤15-minute magic-path gate, or incorrectly documents a public contract.
- **P2 Major:** important missing workflow, stale example, API/SDK mismatch, poor error recovery, substantial drift.
- **P3 Minor:** clarity, navigation, terminology, maintainability.
- **P4 Polish:** presentation/style only.

## Audit order

1. establish repository/product truth
2. identify canonical onboarding and magic path
3. attempt/measure the path
4. compare docs to interfaces/specs
5. test examples and commands
6. inspect API/SDK parity
7. inspect errors/troubleshooting
8. inspect versioning/lifecycle
9. inspect terminology/navigation
10. inspect human + coding-agent usability
11. score and gate release

Prioritize defects that prevent developers from succeeding over cosmetic completeness.
