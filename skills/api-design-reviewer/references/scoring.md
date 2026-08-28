# API DX and OpenAPI Correctness Scoring

Report two independent scores. Never merge them, and never let one hide the other.

## API DX Score /100

Score each dimension from evidence (probes, contract inspection, observed behavior), then weight it:

| Dimension | Weight |
|---|---:|
| Consistency | 20 |
| Guessability | 20 |
| Resource model | 15 |
| Errors | 15 |
| Reliability | 10 |
| Async operations and events | 8 |
| Authentication and authorization | 7 |
| Versioning | 5 |

Sum the weighted dimension scores. Label the result with its evidence: Observed, CI-observed, or Estimated.

Score the API, not the docs. A confusing contract is an API defect even when documentation explains it.

## OpenAPI structural pass (correctness score)

The correctness score is separate and mechanical. Check the contract as a document:

- every `$ref` resolves, local and external
- every operationId is unique
- every example value decodes as its declared format
- every operation declares at least one 4xx or 5xx response

Run `scripts/check_openapi_shape.py` on the OpenAPI JSON; its findings are defects in the contract, not in the product. Correctness findings lower the correctness score only.

## Weighing evidence

- Structural findings always count against the OpenAPI Correctness Score.
- Reliability, error, and versioning findings count against the API DX Score when the contract is authoritative; count them against both scores when the server behavior was observed.
- Guessability findings come from probes. Only probe-verified findings count against the guessability dimension.
- Consistency findings are cross-surface: naming, shapes, and semantics that repeat identically everywhere score full; every divergence lowers the dimension.

## Reporting

- Report both scores with evidence labels; an unlabeled score is UNVERIFIED.
- A high OpenAPI score cannot hide a low API DX score, and vice versa.
- Verdicts follow the canonical vocabulary: PASS, PASS WITH DEBT, FAIL, UNVERIFIED. A hard-gate failure cannot be overridden by a high aggregate score.
