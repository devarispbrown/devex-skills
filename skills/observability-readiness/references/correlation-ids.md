# Correlation and Request ID Design

Procedure for designing and auditing request/correlation ID generation, propagation, logging placement, and tracing context. Read before auditing correlation.

## Generation

- Generate exactly one correlation ID per logical request, at the first boundary: the edge gateway, load balancer, or the first service that owns the request.
- Use an ID that is unique, opaque, and sortable: UUIDv4 or ULID. Never reuse timestamps, usernames, or IP addresses as IDs.
- Accept and propagate an incoming ID from a trusted caller when the system is a downstream hop. Do not re-generate; re-generating breaks the chain.
- For a retried request, keep the same correlation ID and start a new span. Retries are one logical request, not many.

## Propagation

- Carry the ID in the standard header (X-Request-ID or equivalent) across every hop: HTTP calls, queue messages, pub/sub events, and webhooks.
- Propagate W3C trace context (traceparent) alongside it; the correlation ID is the human-readable chain, the trace context is the machine-readable chain.
- Set the ID once in a middleware, filter, or interceptor at the boundary. Never scatter header reads across handlers.
- Propagate to outbound calls and consumers. An ID that stops at a service boundary is a gap.

## Logging placement

- Attach the correlation ID to every log line, metric, and span emitted while serving the request.
- Emit the ID as a structured field, never interpolated into the message text.
- Log the request at entry and exit with the same ID; the pair brackets the request lifecycle.
- For background jobs, generate an ID at job start and thread it through every step the job performs.

## Tracing context

- Create the root span at the same boundary that generates the correlation ID.
- Pass the correlation ID and the trace/span ID into child spans; never store one as an attribute of the other only.
- Move context explicitly (OpenTelemetry context propagation, explicit parameters). Never use globals.

## Verification

- Grep every entry point and confirm each generates or inherits an ID.
- Follow three example requests end to end — happy path, error, retry — and confirm every telemetry record carries the ID.
- Confirm the same ID value resolves in the log aggregation system and the trace explorer.

Do not emit a log line without a correlation ID. Do not leave the ID out of metrics. A request whose telemetry cannot be reassembled cannot be diagnosed.
