# Handoff and Ownership

## Owner classes

Attribute each finding to exactly one owner class:

- Product — journey design, flow, feature shape, defaults
- API — endpoints, models, semantics, status codes
- CLI — commands, flags, output, exit codes
- SDK — client libraries, language ergonomics
- Config — configuration model, defaults, precedence
- Environment — setup, tooling, prerequisites
- Docs — documentation, examples, guidance
- Infrastructure — platforms, networking, registry, CI
- Third-party — external services, OS, network

A cluster is rarely owned by the surface it surfaced on. A CLI error caused by a bad default is Config; a docs example that installs the wrong thing is Docs; a registry that is unreachable is Infrastructure. Attribute by root cause, not by where the developer complained.

## Attribution rules

1. Read the cluster's representative signals. Identify the step that produced the failure.
2. Confirm the cause is present in the evidence, not inferred from a recent change.
3. Split mixed-cause clusters so each finding has one owner class.
4. Third-party causes are findings too: report them with evidence and mark the owner class Third-party.
5. Do not downgrade a cluster to "user error" without evidence of developer error.

## Acceptance tests

Every finding carries an acceptance test: what a developer will do and see after the fix. Write it as an observable scenario, not a code change:

- a developer runs the documented install on a clean machine and reaches the registry pull without error
- a developer who misconfigures the token sees a message naming the missing variable and the fix
- a developer completes the onboarding path within the canonical time target

The acceptance test is what the receiving team verifies. Do not hand off a finding that cannot be verified.

## Receiving suite skills

Hand findings to the matching suite skill, referenced by name, if available:

- docs findings — `developer-docs` (author the fix), `developer-docs-auditor` (verify and gate)
- API and CLI surface findings — `api-design-reviewer`
- SDK findings — `sdk-engineer`
- error and diagnostics findings — `error-experience`
- onboarding flow findings — `developer-onboarding`
- local setup and environment findings — `local-development`
- whole-journey re-measurement — `developer-experience-auditor`
- release-time gating of the fix — `release-guardian`

Do not invent owners outside this list. Unowned findings are listed in the report as unowned.
