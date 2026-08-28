# Ownership Metadata

## Owner field contract

Every catalog entry carries exactly one `owner`. The contract:

- **One accountable owner.** An entry with multiple owners has none. Pick one team; other stakeholders go in `collaborators` or `stakeholders`.
- **Machine-matchable.** The owner is a stable team name or group id (slug), not free-form prose. Tooling must be able to join the catalog to the team entity.
- **Team over person.** Prefer a team; use a personal handle only when no team exists, and record that fact.
- **Contact paths.** Record how to reach the owner: Slack channel, mailing list, handbook page, codeowners file, on-call rotation. At least one path must be current.
- **Scope.** State what the owner is accountable for (service, artifact, datastore) so a developer can judge whether they asked the right person.

## Team discovery

Teams are first-class catalog entries (`kind: team`) with:

- a charter and scope statement
- the systems and assets they own, derived from owner references
- current contact and on-call information
- a management chain for escalation

A team that cannot be found cannot be held accountable. Registering a team is a prerequisite for owning anything in the catalog.

## Escalation

Define escalation per owner, in order:

1. **First responder** — the team member or rotation who takes the first look.
2. **On-call** — the rotation that owns incidents; pager or on-call link.
3. **Owner lead** — the accountable person for direction and decisions.
4. **Management chain** — the path when ownership is disputed, unclaimed, or the team is unresponsive.

Rules:

- escalation order is recorded per entry (or inherited from the team), never implied
- an unclaimed or disputed thing is marked `status: unowned` and routed to a governance owner, never left silent
- escalation paths are tested, not assumed; a rotted rotation link is a P2 defect

## Staleness

Ownership metadata rots fastest of all catalog fields: teams rename, rotations change, people leave.

- record `last_verified` on every owner reference
- a team entry with no verified contact in the platform's staleness window is a P2 backlog item
- verify on-call and contact paths at the same cadence as lifecycle verification (see `lifecycle-fields.md`)

## Ownership severity

- entry with no owner: P1 when the thing is in production or published
- owner unreachable (no valid contact): P2, escalated to P1 for incident-bearing systems
- multiple conflicting owners: P1 — ambiguity blocks every operational decision
- stale owner metadata: P2
