# SDK Errors

## Typed error hierarchies

- Every SDK exposes a single base error class for the surface, with a specific subclass per failure class.
- Specific classes are catchable: callers can branch on error type without parsing messages. If callers must string-match, the hierarchy has failed.
- Error classes are version-stable: adding a subclass is safe, changing a class's semantics or removing it is a breaking change.
- Every error instance carries the machine-readable code, the human message, and the request identifier when one exists, regardless of class.
- Do not leak the transport layer: an HTTP failure surfaces as the SDK's error class with the API code, not as a raw status exception.

## Wrapping versus chaining

- Preserve the cause chain through every boundary. Do not swallow the underlying cause.
- Use the language's native mechanism: Python `raise X from cause`, Go `%w` wrapping, Java `initCause` and suppressed exceptions, JavaScript `cause` option, Rust `source()`.
- Wrapping adds context at each layer ("upload failed: connection reset") while the root cause stays reachable and the original code stays present.
- Never discard the original code, message, or correlation identifier when wrapping.
- Never log-and-rethrow in a loop; log once at the boundary and once at the terminal decision.
- A chain that cannot reproduce the original failure is a defect.

## Retryable signals

- Retryable error classes carry an explicit signal: a `retryable` flag, a subclass marker, or a documented code list.
- Automatic retries only for classes marked retryable; honor `Retry-After` and backoff with jitter when the API provides them.
- Expose the retry policy to the caller: `max_retries`, backoff, and the retryable classes are configurable and documented.
- Distinguish transient from permanent at the type level, not only in the message.
- If the SDK retries automatically, it reports the retry decisions to the caller's logging or hooks; silent retries are a defect.

## Cross-language parity

- Official SDKs expose the same error classes, the same codes, and the same semantics in every language.
- Parity is semantic, not mechanical: each language uses its idiomatic error mechanism (exceptions, error values, results), but the same failure is catchable and identifiable everywhere.
- Maintain a parity table in the SDK docs: class name, code, retry policy per language.
- A new failure class ships in all official SDKs together, or is marked unsupported explicitly.
- A mechanically translated error model that ignores language idioms is a product defect.
