# Guessability Probes

Guessability is the test of API design: **can a developer with the product's domain vocabulary predict the interface without reading the docs?**

## Question bank

Ask every question against the actual contract, never against the docs:

1. **Endpoint**: given the product's nouns, can the developer predict the path for listing, creating, and fetching a resource?
2. **Path parameters**: can they predict the parameter names (`{widgetId}` vs `{id}` vs `{widget_id}`) and their format?
3. **Collection shape**: will the list response be a bare array or a wrapped object? Is it the same for every list?
4. **Pagination**: can they predict the parameter names (page? offset? cursor?), the response fields, and the envelope without checking?
5. **Filtering and sorting**: does `?status=active` and `?sort=-created_at` behave the way the domain suggests?
6. **Errors**: can they predict the status code for a bad request, a missing resource, and a conflict? Do error bodies share one shape?
7. **Enums**: given a status like `pending`, can they predict `succeeded` vs `success` vs `complete`? Are enum values lowercase, kebab, or mixed across resources?
8. **Naming**: given one resource pair, can they predict the next resource's field names (camelCase vs snake_case vs kebab across fields and paths)?
9. **Methods**: does the HTTP method match the action (GET for reads, DELETE for removal, POST for creation, PATCH for partial update)?
10. **Reliability**: can they predict that a retry is safe, which errors are retryable, and whether a POST is idempotent?

## Scoring method

Score each probe 0, 1, or 0.5:

- **1** — predictable from the domain vocabulary alone
- **0.5** — predictable after one docs look-up
- **0** — requires docs, examples, or guessing

Compute the guessability score as the percentage of points earned:

- **90-100%** — highly guessable; document only the exceptions.
- **70-89%** — mostly guessable; the exceptions are P3/P2 findings.
- **40-69%** — inconsistent; naming and shape fixes are the highest-leverage API improvements. Report P2 findings.
- **below 40%** — the API is documentation-dependent; report as a P1 API design defect.

## Running the probes

Run `scripts/guessability_check.py` on the OpenAPI JSON first; its output is a list of **candidates** to probe, not verdicts. Verify each candidate against the question bank before reporting it as a finding.

Do not score guessability from the documentation. Cover the docs, guess from the domain, then uncover.

Record each probe result (question, score, evidence) in the report so the score is reproducible.
