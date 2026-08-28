# Error Taxonomy

## Expected versus unexpected

**Expected error:** a designed-for failure mode of a supported path. Examples: validation failure, missing resource, authentication rejection, rate limit, conflict, transient dependency failure.

**Unexpected error:** a programmer bug, infrastructure collapse, or precondition violation the product did not design for. Examples: null dereference, assertion failure, corrupted state.

Rules:

- Expected errors get the full six-question treatment: text, code, retry policy, correlation, playbook.
- Unexpected errors still get capture, correlation, severity, and a path to become expected: reproduce, classify, document, then treat as expected.
- Do not label a frequent, user-reachable failure "unexpected" to avoid documenting it. Frequency and reachability make it expected.
- Do not let a rare-but-public failure escape correlation. Every surfaced error needs a support-correlation identifier.

## User-caused versus system-caused

**User-caused:** the user supplied invalid input, configuration, or state. The corrective action is expressed in user terms: "Set `RETRY_DELAY` to a positive integer." Point at the exact offending value or field.

**System-caused:** the product or a dependency failed. The corrective action is status reporting, retry policy, escalation, or an operator action: "Check the database status and rerun."

Rules:

- Never tell the user to change their input when the product failed.
- Never present a product bug as user error.
- When in doubt, classify as system-caused; the retry policy and escalation path are safer defaults.

## Stable error codes

- Codes are machine-readable, unique across the product, and stable across releases.
- Codes are semantic and namespaced (for example `AUTH_TOKEN_EXPIRED`, `RATE_LIMITED`) when the surface permits; numeric-only codes are accepted only where the protocol requires them.
- The message text may change; the code must not. Code and message are separate fields, never concatenated.
- A code is never repurposed, and a retired code is never reused for a new meaning.
- Codes live in structured output, not only in prose. A code that cannot be parsed cannot be retried or triaged.

## Taxonomy design procedure

1. Enumerate surfaces and the operations each exposes.
2. For each operation, list the expected failure modes: invalid input, missing state, auth, conflict, rate limit, transient failure.
3. Group failure modes into classes; assign one stable code per class.
4. Assign each code a severity, a retry policy, and a correlation requirement.
5. Draft the six-question text for each code: what, why, where, fix, retry, correlate.
6. Maintain a code registry, generated from schema or source when possible, so codes cannot drift from implementation.
7. Test that each code is stable, documented, and reachable; add a test asserting the six questions per expected error.

Do not create a new code when an existing code fits. Do not document a code the product never emits.
