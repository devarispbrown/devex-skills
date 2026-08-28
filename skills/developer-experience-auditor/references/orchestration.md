# Orchestration and Delegation

Deep dives happen where the friction lives. Delegate to the specialist skill if available; when it is not, execute the embedded fallback checklist yourself. This skill must remain complete standalone.

## Delegation table

| Skill | Delegate when | Fallback checklist |
|---|---|---|
| developer-docs-auditor | journey friction is driven by documentation: stale quickstart, broken examples, missing reference, drift between docs and behavior | Re-execute the documented steps yourself; compare docs to implementation and `--help` for the touched surfaces; record drift as Discovery or Onboarding findings |
| api-design-reviewer | friction in execute/verify/modify traces to API shape, naming, status codes, or the resource model | Inspect the used endpoints against implementation and schema; note naming, error, and pagination inconsistencies in the calls the journey makes |
| sdk-engineer | official SDK steps fail, feel unidiomatic, or lag the API | Run the SDK steps yourself; diff exported operations against the canonical API; record capability gaps and parity issues |
| error-experience | errors encountered are unexplained, or TTR is slow | Reproduce each unexplained error once; capture full error text; check troubleshooting docs; time corrective action against `TTR_TARGET_MIN` |
| quality-engineer | the test stage is missing, broken, or not representative | Run the test command; inspect fixtures and CI config; record what the journey's tests do not cover |
| release-guardian | friction in deploy/upgrade: version pinning, migration, deprecation, changelog | Check changelog and migration guidance for the versions touched; verify semver adherence; exercise the upgrade steps |
| developer-onboarding | onboarding redesign work is requested, or onboarding friction needs a redesign proposal | Produce the onboarding-friction list from journey data and propose canonical-path fixes with acceptance tests |
| local-development | the local dev loop needs repair: build, services, committed automation | Time a clean clone to first success against `LOCAL_DEV_MAX_MIN`; check committed instructions and automation for gaps |

## Rules

- Label every delegated finding with the skill name in the DX Report's delegated-evidence section.
- Re-verify anything material to a hard gate (magic path, local dev, or a named gate constant) locally, even after delegation.
- Never silently override another skill's verdict. When your evidence disagrees, report the disagreement and say what evidence would settle it.
- A delegated verdict is evidence, not truth. The DX Report's verdict is yours.
