# Spend Control Standard

## Caps are enforcement, not advice

A spend cap that only warns is not a cap. Enforcement is server-side: the metered surface stops consuming billable resources when the cap is reached, or requires explicit per-run authorization to continue.

## Components

Every spend control has:

- **cap** — the monetary or unit ceiling
- **alert** — notification before the cap
- **enforcement** — server-side stop or explicit override at the cap
- **overage policy** — what happens if consumption crosses the cap anyway

## Alert thresholds

- alerts fire before the cap, with margin for batched or lagging meters
- at least two thresholds (warning, near-limit) or one documented threshold with rationale
- alerts are actionable: what is consuming, what the cap is, what to do

## Enforcement semantics

- enforcement is server-side, never client-side only
- override flows require explicit authorization and are logged
- in-flight work behavior is documented: complete, abort, or partial
- the cap applies per key/account, never averaged across accounts

## Overage behavior

Define and document:

- whether overage is possible (racing traffic, async meters)
- how overage is billed and whether it is capped
- the notification path when overage occurs

Undefined overage behavior on an unbounded surface is a P1 defect.

## Cap changes

Cap and alert changes are behavior changes: announced, versioned where applicable, and reflected in the same surfaces as the cap itself.

## Review checklist

- [ ] cap exists for every unbounded metered surface
- [ ] alerts fire before the cap
- [ ] enforcement is server-side
- [ ] overage policy documented
- [ ] cap changes announced
