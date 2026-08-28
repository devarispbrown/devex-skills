# Violation Actionability

A violation is actionable when it stands alone: the developer can fix it without opening the policy file or the guardrail source.

## Required fields

Machine-readable violations carry the four actionability fields (the keys used by `scripts/check_policy_actionability.py`):

| Field | Content |
|---|---|
| `what_happened` | policy id, rule, target, and observed value — plus file:line or resource where the problem lives |
| `why` | the rule and its rationale, quoted from the policy file |
| `how_to_fix` | exact remediation, preferably copy-paste commands the developer can run |
| `request_exception` | the self-service route when the rule cannot be satisfied |

## Standing-alone rule

A violation must be readable and actionable in isolation, with:

- its policy id, so it can be tracked and its exception route keyed
- its location, so the fix is findable
- retry-safety: if the fix can be re-run, say so

## Good and bad

Actionable:

```
POL-102: image tag "latest" used in deploy.yaml:34; policy POL-102 pins immutable tags
Why: mutable tags make rollback and provenance unverifiable.
Fix: run `pin-images deploy.yaml` or replace the tag from the build job output.
Request an exception: `polx request POL-102 --scope deploy.yaml --until 2026-10-01`
```

Opaque:

```
POLICY CHECK FAILED
```

## Opaque violations are defects

A violation missing any required field is opaque. Treat it as a defect in the policy system, not a developer failure: severity P1, fixed in the guardrail's message builder. An opaque violation is an expected error without what/why/how/retry-safety and triggers the `UNEXPLAINED_ERROR` release gate.

## Verification

Run `scripts/check_policy_actionability.py` against a JSON array of violation samples:

- every sample with all four fields present: exit 0
- any sample missing a field: exit 1 and name the field

Keep a sample set next to each guardrail and run the checker in CI. A guardrail whose violations cannot pass the checker does not ship.
