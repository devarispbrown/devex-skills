# Documentation and Developer Experience Scoring

Always report two independent scores when enough evidence exists.

## Documentation Quality Score (0-100)

| Dimension | Weight |
|---|---:|
| Correctness | 20 |
| Time to first success / onboarding | 15 |
| Reference completeness | 10 |
| Task/how-to coverage | 10 |
| SDK consistency | 10 |
| Examples/testability | 10 |
| Troubleshooting/error guidance | 8 |
| Information architecture/navigation | 5 |
| Lifecycle/versioning | 4 |
| Production/security guidance | 3 |
| Maintainability/CI | 3 |
| Agent/LLM usability | 2 |

## Underlying Developer Experience Score (0-100)

Assess the interface, not the prose:

| Dimension | Weight |
|---|---:|
| Magic-path friction | 25 |
| API/CLI/config coherence | 20 |
| Error quality/recovery | 15 |
| Auth/setup ergonomics | 10 |
| SDK idiomatic quality/parity | 10 |
| Observability/debuggability | 8 |
| Versioning/compatibility | 5 |
| Production transition | 5 |
| Support/self-service | 2 |

## Hard magic-path rule

The magic-path gate is not averaged away:

- ≤5 min: exceptional
- >5 to ≤10 min: strong
- >10 to ≤15 min: pass
- >15 min: P1 and release/world-class FAIL
- no reproducible E2E quickstart: P1 and FAIL
- manual approval/support required with no sandbox: P1 and FAIL

If timing is only estimated, label the magic-path result **UNVERIFIED** even if the estimate is <15 minutes.

## World-class threshold

Use "world-class" only when:

- all hard gates pass
- Documentation Quality ≥90
- Developer Experience ≥85
- no unresolved P0/P1 issues
- the magic path has observed or credible CI + periodic human evidence at ≤15 minutes
