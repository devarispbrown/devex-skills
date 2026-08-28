# Security Advisory Patterns

## Definition

An advisory is the notice for a vulnerability affecting a public surface: who is affected, what to do, by when, and what breaks if ignored — with the urgency of a security issue attached. It follows the same five-field contract as every other notice, plus security-specific fields.

## When an advisory is required

- a vulnerability affecting any public surface: API, SDK, CLI, config parsing, auth, webhooks, or dependency behavior
- a supply-chain issue in a published artifact
- a credential or secret exposure with public reach

## Advisory fields

| Field | Required | Notes |
|---|---|---|
| **Identifier** | always | CVE or project-internal ID; never publish a bare description without an identifier |
| **Severity** | always | the severity vocabulary from `references/standards.md`, assigned against impact, not effort |
| **Affected versions** | always | exact ranges, not "all recent versions" |
| **Patched versions** | always | exact versions that fix the issue |
| **Workaround** | when no patch yet | concrete, safe mitigation with its own deadline |
| **Action required** | always | upgrade, rotate, mitigate — with by-when |
| **What breaks if ignored** | always | exploit consequence in plain language |

## Disclosure timing

1. Disclose after the fix is available and released; the advisory names the patched version at the same time it names the vulnerable one.
2. Coordinated disclosure (embargo until patch) is the default for public surfaces; never disclose a live vulnerability with no mitigation.
3. If a workaround is the only mitigation, the advisory states it immediately and the patch deadline follows in a follow-up notice.

## Channels and reach

1. Advisories go to the channels affected developers actually read: security advisories feed, package-manager alerts, release notes, and the security page of the docs.
2. Reach is verified per `references/reach-verification.md`; a silent fix is not a disclosure.
3. The advisory links the patched release notes and the migration notice when the patch is breaking.

## Verification

- affected and patched version ranges are exact
- severity is assigned, not estimated
- a workaround exists whenever no patch exists
- the advisory reached the affected segments with labeled evidence
