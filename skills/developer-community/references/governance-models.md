# Governance Model Design

## The three models

- **Benevolent dictator** — one decision maker. Fast, cheap, correct for Stage 0–1. Risk is bus factor; answer the succession question early, while the founder is still present.
- **Maintainer council** — decisions by a body; review and merge authority distributed. Correct for Stage 2–3. Requires a documented decision process, quorum, and a tie-break rule.
- **Foundation** — external legal structure with a board, code-of-conduct enforcement, security response team, and trademark ownership. Correct for Stage 4. Use CNCF governance and charter templates as the structure.

## Stage-appropriate choice

- Stage 0–1: founder-led. Document that the founder decides and write down the exception path. Do not copy a council charter onto a two-person project.
- Stage 2: council plus a ladder. Governance documents actual operation: who decides what, how reviewers become maintainers.
- Stage 3: delegation by area. Multiple owners per critical area; decisions are pushed to the area owners.
- Stage 4: foundation governance. Succession is defined and rehearsed before the stage is claimed.

## Decision records

Record decisions as they are made, not after conflict:

- each record states date, context, the decision, alternatives considered, and consequences
- store in `docs/decisions/` with sequential numbering; make records discoverable from CONTRIBUTING.md or GOVERNANCE.md
- anyone may propose a decision record; the decision authority approves it

Never leave decisions in chat. An undocumented decision is a governance claim the next maintainer cannot verify.

## Outsider advancement

Governance must state how outsiders gain responsibility: contribution → reviewer → owner → maintainer, with the ladder as the interface.

Verify the path is observable:

- promotion criteria are objective and recorded, not tenure-based
- removal process exists, is documented, and is fair
- non-code contributors reach the same rungs through triage, docs, testing, design, and support work

Never gate advancement on social access to the founders. If advancement requires knowing a maintainer personally, the governance is a clique, not a ladder.

## CNCF template guidance

Use CNCF governance and charter templates as structure, then adapt to the project's actual stage. Take the decision-authority and escalation clauses; skip the committee count. A foundation charter with five committees on a Stage 1 project is ceremony, not governance.

Verify:

- the document describes how the project actually operates today
- escalation paths are named, not "the maintainers will figure it out"
- security response and code-of-conduct enforcement are assigned to people, not left implicit

Never describe an aspirational structure. Governance that documents a structure the project does not operate is an `OPAQUE_GOVERNANCE` failure.
