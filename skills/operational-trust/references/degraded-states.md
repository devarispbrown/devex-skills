# Degraded-State Signaling

Graceful degradation that stays honest: explicit degraded states, error taxonomy, and fallbacks that never masquerade as success. Read this when auditing degraded behavior or error handling.

## Signal, do not hide

A degraded mode that looks like a success is a trust defect. Verify:

- partial results are marked partial, with the missing portion identified
- fallback data is labeled stale or approximate, with the source and freshness stated
- skipped work is reported, never silently dropped
- feature-flag and quota degradation produce a documented, readable outcome

## Error taxonomy

Users must be able to tell whether it is you or them. Verify:

- client errors (4xx) are distinguishable from provider errors (5xx) with stable codes
- 5xx is never used for invalid input, and 4xx never for server failure
- retryable conditions are marked retryable, with retry-after or backoff guidance
- every response carries a correlation ID users can quote to support
- a documented error taxonomy exists, is linked from the docs, and covers remediation

## Degradation mechanisms

Verify the following, where present, are documented and visible to users:

- circuit breakers: open, half-open, and closed states are readable in responses or headers
- timeouts and deadlines: what the user sees when a dependency is slow
- fallback content: clearly labeled, with source and freshness
- maintenance mode: planned degraded states are announced via the status page and maintenance windows

## Distinguish you from them

When a dependency fails, tell users whose fault it is when determinable:

- upstream outage: the error names the dependency without leaking internals
- own outage: the error is honest, with a link to the status page and the incident number
- ambiguous: say so, and provide the correlation ID

## Verification

Verify by fault injection or CI where possible:

- each documented degraded state is exercised by a test
- error paths return the documented codes and headers
- the status page and the API share the same degraded-state vocabulary
