# Structured Logging Procedure

Procedure for emitting, structuring, leveling, sampling, and redacting logs. Read before auditing or writing log statements.

## When to emit

- Emit at request entry and exit, dependency calls, state changes, and every handled error.
- Emit errors with the cause, the correlation ID, the affected scope (user, tenant, region), and the recovery taken or needed.
- Never log per loop iteration, per row, or per hot-path event without explicit sampling.
- Never log ordinary control flow as info noise; log what an operator needs, not what the code did.

## Structure

- One JSON (or key=value) record per event with a stable event name. The message is the event name; fields carry context.
- Put dynamic values in fields, never in the message. A message must be grep-stable across occurrences.
- Standard field names across services: event, level, timestamp, service, correlation_id, duration_ms, status, error.
- Use one logging library per service. Do not mix print, fmt, and logger calls.

## Levels

- **debug:** detailed internal state for investigation; off by default in production.
- **info:** lifecycle events an operator would want: started, stopped, request entry.
- **warn:** degraded or unexpected but handled conditions.
- **error:** a failure the operator must know about, with cause, scope, and correlation ID.
- Never log secrets, tokens, cookies, or full payloads at any level.

## Sampling

- Sample high-volume debug and info records by rate or by key (per user, per endpoint) when volume exceeds the sink's capacity.
- Never sample error records blindly. Tail-sample or always-keep errors and their surrounding context.
- State the sampling decision per surface in code and in the report. Undocumented sampling is unverifiable.

## PII redaction

- Redact at the source, never in the sink. The log pipeline is not a privacy boundary.
- Define an allowlist of fields that may be logged; drop everything else at the call site.
- Redact emails, phones, addresses, tokens, and keys before they reach a field. Never log raw request or response bodies.
- Add a redaction test or fixture per PII class. Scanning for PII in logs is part of the audit.

## Verification

- Grep for print/fmt/console logging calls that bypass the structured logger.
- Walk every error path: each catch/except block either logs with context or returns an error that does.
- Confirm sampling and redaction are testable and tested.
