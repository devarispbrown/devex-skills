# Sandbox Route Characteristics

## Purpose

Defines the five characteristics every sandbox route must satisfy. A route that fails any characteristic is not a sandbox route; it is production risk with a friendlier name.

## The five characteristics

1. **No credit card** — the route requires no payment instrument and no billable resource. No card, no spend cap, no usage metering that can bill, no trial that converts.
2. **No production account** — the route uses a sandbox/test account, tenant, or environment. It never authenticates as, or against, a production account, production data, or a live customer.
3. **Resettable** — the route returns to a known state on demand: tear down and recreate, reseed from a fixture, or restore from a snapshot. A route whose state cannot be restored is not resettable.
4. **Deterministic state** — identical inputs produce identical, inspectable state. Seeding is explicit and reproducible; no shared mutable leftovers between runs.
5. **Safe by construction** — the route structurally cannot reach production: separate credentials, separate endpoints, mock providers, or explicit isolation boundaries. Safety is a property of the mechanism, never of discipline.

## Verification checklist

Verify each route against all five characteristics. For each characteristic:

- the mechanism is named (test keys, mock provider, sandbox tenant, fixture seed, mock webhook receiver)
- the boundary is explicit (endpoint, account, namespace, tenant id)
- the state-restore path is demonstrated, not assumed
- evidence is labeled: **Observed** (executed in the sandbox), **CI-observed** (executed in automation), or **Estimated** (reasoned only)

An estimate can never prove a characteristic. A characteristic without an evidence label is UNVERIFIED.

## Not a sandbox route

The following lookalikes pass nothing; each fails at least one characteristic:

- a real account with a free trial or a promo credit — requires a card or bills on conversion
- a real endpoint called with test data — touches production
- a staging environment that shares production storage — not isolated
- a mock that still requires a real payment token — requires a card
- a route that needs manual approval or a support ticket to reset — not resettable

## When to escalate

When a product offers no mechanism that can satisfy all five characteristics for a documented task, the finding is a product gap, not a docs gap. Report it as a `NO_SANDBOX_FOR_RISKY_PATH` finding with the missing mechanism named.
