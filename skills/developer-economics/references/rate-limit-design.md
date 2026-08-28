# Rate Limit Design Standard

## Rate limits are API behavior

A rate limit is a contract between the service and the client. The client must be able to read the contract from the response, not from documentation prose.

## Standard headers

Every rate-limited endpoint returns, on every response:

- `RateLimit-Limit` — the quota per window, as an integer
- `RateLimit-Remaining` — quota remaining in the current window
- `RateLimit-Reset` — Unix time (seconds) when the window resets

Support the legacy `X-RateLimit-*` names when ecosystem compatibility requires it, but always emit the standard names.

## 429 semantics

- Every 429 response carries `Retry-After`, either seconds or an HTTP-date.
- The value is concrete — a number or a date, never a suggestion.
- `RateLimit-Reset` on the 429 matches `Retry-After`.
- The error body states which limit was exceeded and the key it applies to (API key, account, IP, org).

Never return 429 without `Retry-After`. Never rate limit with a 400 or a silent 200.

## Burst vs sustained

When the product has both:

- expose both limits with distinct header names
- document the relationship: burst over N seconds, sustained per minute/hour
- design the burst buffer explicitly; do not let one mechanism silently consume the other's budget

A burst cap that eats the sustained budget is a product defect, not a tuning detail.

## Limit identity

Document per limit:

- the key it applies to (API key, account, IP, org)
- the window and units
- the counting rules (requests, tokens, concurrent calls)
- what happens at the boundary (queued, rejected, throttled)

## Limit changes

A limit change is a behavior change:

- versioned or announced before it takes effect
- reflected in headers and documentation in the same release
- never applied retroactively to the current window without notice

## Design review checklist

- [ ] standard headers on every response
- [ ] Retry-After on every 429
- [ ] burst vs sustained both visible when both apply
- [ ] per-key, per-window semantics documented
- [ ] boundary behavior documented
- [ ] limit changes announced as behavior changes
