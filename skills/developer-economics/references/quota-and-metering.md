# Quota and Metering Visibility Standard

## Quotas are visible state

A quota is not a wall the developer hits; it is state the developer can read. Every metered resource exposes:

- **used** — consumption in the current window
- **limit** — the cap for the window
- **reset** — when the window resets
- **estimated_cost** — projected cost of current usage where per-use pricing applies

## Response contract

Quota fields appear:

- in the metered resource's response payload
- in a dedicated quota/usage endpoint
- in the usage command for CLI surfaces

Return all four fields or none. Partial visibility is a defect. Units and window are part of the field semantics, documented once and never duplicated across prose.

## Usage command

Every metered surface has a usage/quota command that returns used, limit, reset, and estimated cost with no side effects. The same command serves free tier and paid tier; hiding free tier usage is a defect.

## Meter semantics

Document per meter:

- unit (requests, tokens, compute seconds, storage bytes, seats)
- window (per-second, per-minute, per-day, per-month) and reset time
- counting rules (what counts once, what counts per unit)
- update latency (near-real-time vs batched)

Undocumented meter semantics make quotas unverifiable.

## Exhaustion behavior

Quota exhaustion produces a documented, actionable error: which quota, current used/limit, reset time, and the remediation path (upgrade, wait, request an increase). Silent degradation or a generic error is a P1 defect.

## Audit criteria

- [ ] used/limit/reset visible on every metered resource
- [ ] estimated_cost present where per-use pricing applies
- [ ] usage command exists and is side-effect-free
- [ ] meter semantics documented
- [ ] exhaustion error is actionable
