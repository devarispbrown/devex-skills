# Cleanup and Cost Control

## TTL enforcement

- the TTL marker set at creation is the enforcement input; nothing else matters
- an enforcement job runs on a schedule: expired environments are marked, then destroyed
- grace periods are short and explicit; grace does not reset the TTL
- environments past TTL with no owner are destroyed without waiting
- enforcement is automated and observable: a run reports what it deleted and why

## Cleanup automation

Cleanup runs:

- on a schedule (tight enough that TTL means something)
- on merge of the PR that created the environment
- on demand, for any named environment

Cleanup covers:

- expired ephemeral environments
- orphans: past TTL, unowned, or unreachable from any PR
- stale snapshots and branches
- orphaned resources the environment leaves behind

## Cost controls

Per stage, define:

- **budget**: what the stage may spend per month
- **alert**: a threshold that notifies before the budget is exhausted
- **cap**: a hard stop; the stage refuses to create beyond it
- **sleep**: non-production stages idle outside working hours where possible

Rules:

- preview is the cheapest stage: smallest topology, shortest TTL, hardest cap
- cost follows the TTL: an environment that cannot be destroyed cannot be cost-controlled
- unused environments are deleted, not paused indefinitely
- cost claims carry an evidence label: Observed, CI-observed, or Estimated

## Ownership

- every environment records a cost owner at creation
- an environment without an owner is deleted by the next cleanup run
- owners are notified before destruction, not asked for permission after expiry

## Debt and gates

TTL or cleanup gaps are severity-labeled using the canonical vocabulary in `references/standards.md`. Creating ephemeral environments without TTL enforcement is a P1 production-cost risk. Gaps reported without evidence are UNVERIFIED.
