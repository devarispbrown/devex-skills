# Free Tier Design Standard

## The free tier is a product surface

The free tier is not a marketing artifact. It is a metered surface with the same visibility requirements as paid tiers.

## What

State explicitly what the free tier includes:

- which surfaces, features, and limits are free
- what is free without limit and what is free only up to a limit
- what is excluded entirely

Ambiguity between "free" and "free tier" is a defect. A developer consuming billable usage while believing they are on a free tier is a surprise-invoice P1.

## Limits

Free limits follow the quota contract:

- used, limit, reset, and estimated cost are visible in the same surfaces as paid limits
- units and windows are the same units and windows as paid meters
- the free tier never hides its own limits

## Upgrade path

- the upgrade path is a documented, self-serve path reachable from the free tier surfaces
- upgrade is a product flow, not a sales funnel
- what changes on upgrade (limits, features, billing) is stated before the developer commits
- downgrade behavior is defined: what is lost, what happens to over-limit usage

## Abuse protection

- free tier abuse protection exists without degrading the legitimate experience
- enforcement follows the spend control contract: server-side, visible, actionable
- free tier rate limits are visible like any other rate limit

## Free tier changes

Changes to what is free, to limits, or to the upgrade path are behavior changes: announced with migration guidance for affected developers.

## Review checklist

- [ ] what is free stated explicitly
- [ ] limits visible via the quota contract
- [ ] upgrade path self-serve and documented
- [ ] downgrade behavior defined
- [ ] abuse protection visible and actionable
