# Diagnostics: Logs, Traces, and Correlation

## Request and correlation identifiers

- A correlation identifier is generated at the ingress boundary for every request or operation and propagated through every internal call, span, and log line.
- The identifier is echoed in error responses and error messages so the caller can hand it to support.
- Support can join the user's report to backend logs, traces, and metrics using only the identifier. If the join needs more than the identifier, the correlation path is incomplete.
- Propagate through asynchronous work: queues, background jobs, and webhooks carry the identifier or a derived one; record the parent linkage.
- The identifier is never a secret, never reused across distinct operations, and always generated when missing.

## Structured logging

- Emit key-value or JSON log lines with stable field names, not prose-only messages.
- Required fields on an error line: `code`, `message`, `request_id`, `surface`, `operation`, and the affected resource or field.
- Levels follow the product's documented convention; an error is logged at an error level, a retry decision at a warning or info level.
- Timestamps are ISO 8601 UTC with millisecond precision. Never log secrets, tokens, or full payloads.
- A structured line's fields are parseable and stable across releases; renaming a field is a breaking change for downstream tooling.

## Traces

- Annotate the failing span: record the error code, message, and the exception or error event on the span where the failure is detected.
- Trace context carries the correlation identifier so the log line and the span are joinable.
- Record the retry decision and the terminal failure on their own spans or events; the trace shows the whole failing path, not only the first hop.
- Propagate trace context on outbound calls and into message queues so downstream services extend the same trace.

## Sampling

- Never drop or under-sample error traces. Errors are the highest-value signal; sampling applies to successful traffic.
- The correlation identifier survives sampling: a sampled-out trace still leaves the log line, and the log line still carries the identifier.
- When head sampling cannot keep error traces, use tail sampling or a dedicated error-rate sampler that keeps complete failing traces.
- Record sampling decisions so "this trace was sampled" is knowable, not silently missing.

## When to emit

- Emit a log line where the failure crosses a boundary: inbound request rejected, outbound call failed, retry decided, terminal failure returned to the caller.
- Emit once per boundary, not once per frame. Do not double-log the same failure at every layer.
- Emit the retry decision and the final outcome; the gap between them is the retry history.
- Never log an error before it is classified: an unclassified error line cannot be triaged. Log the code even when the code is provisional.
