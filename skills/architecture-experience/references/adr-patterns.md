# ADR Patterns

## Hard objective

Audit Architecture Decision Records so the mental model's rationale matches the current system, and every decision is either current, superseded with a pointer, or flagged stale.

## Required ADR anatomy

An ADR must state:

- **Status** — proposed, accepted, superseded, deprecated
- **Context** — the forces and constraints at decision time
- **Decision** — the concrete choice, in terms that can be contradicted
- **Consequences** — what changed, what is traded away
- **Supersedes / superseded by** — links, when applicable

A decision that cannot be contradicted by evidence is not a decision; it is prose.

## Quality checks

For each ADR:

- does it name the decision in terms the code can disagree with?
- does it state consequences, including negative ones?
- does it name the successor when superseded?
- does it have an owner and a date?
- is it retrievable from the architecture docs index?

## Staleness detection

Mark an ADR stale when:

- code, tests, schemas, or docs contradict the decision
- the status says accepted but the decision was reversed
- a superseding ADR exists without the older one pointing to it
- the ADR describes a module or service that no longer exists

A stale ADR is a finding with severity from the canonical vocabulary; it predicts misplacement decisions by engineers who trust it.

## Evidence

For every staleness finding, record the contradicting artifact: file, test, schema, or release note. Label the check Observed (read the code), CI-observed (automated compare), or Estimated (inferred).

## Output

A per-ADR table: name, status, verdict (sound / stale / superseded / missing), contradicting evidence. The table feeds the ADR audit section of the brief.
