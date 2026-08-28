# Internal Catalog Design

## Purpose

The internal catalog answers the questions developers ask when they inherit, operate, or depend on internal systems:

- who owns this service, and who is on call?
- where is the runbook, and what is the escalation order?
- which datastore does this service use, and who may access it?
- which team owns this code path or this domain?

It is the Backstage-style backbone of an internal developer platform: entities, ownership, and lifecycle metadata exposed for search and for other tooling. The catalog is the platform's single source of truth for "who and what", consumed by humans and automation alike.

## Entry types

Every entry has exactly one `kind`:

- **service** — a deployable system with an id, an owning team, and an operational contract
- **team** — a first-class entity with a charter, scope, and contact paths
- **owner** — the accountable entity (a team, or a person only when no team exists) for a service or asset
- **datastore** — a database, message bus, or storage system with an owning service
- **runbook** — operational instructions bound to a service or system

## Required fields

Every entry carries the skill's required fields:

| Field | Contract |
|---|---|
| `name` | canonical id; matches the service id or team slug used in platform tooling |
| `owner` | exactly one accountable team, per `ownership-metadata.md` |
| `lifecycle` | exactly one value from the vocabulary in `lifecycle-fields.md` |
| `docs_link` | resolved URL to the canonical docs or handbook page |
| `status` | operational state: active, degraded, retired, or platform-defined |

## Recommended fields per type

- **service**: `service_id`, `owning_team`, `repo`, `deployment_envs`, `api_spec`, `runbooks`, `datastores`, `oncall`, SLI/SLO links
- **team**: `charter`, `scope`, `slack`, `handbook`, `codeowners`, `oncall_rotation`, `management_chain`
- **owner**: `team` or `person`, `contact_paths`, `escalation_order`, `coverage` (what this owner is accountable for)
- **datastore**: `owning_service`, `engine`, `sensitivity`, `access_path`, `retention`, backup/restore links
- **runbook**: `applies_to` (service id), `escalation_order`, `severity_thresholds`, `verification_steps`, `last_reviewed`

## Relationship rules

- Every `service` points to one owning `team`; every `runbook` and `datastore` points to the service or team it serves.
- An `owner` entry exists for every team, and the owner field on other entries references it.
- A service without a runbook is a P1 operational gap when it has on-call coverage expectations.
- A service that uses a datastore must link it; orphaned datastores are a P2 discovery defect.

## Confidentiality

- Entries never contain secrets, credentials, tokens, or unauthorized access instructions.
- Sensitive fields carry an access label (public / internal / restricted), and the access path is a link, never a credential.
- Catalog exports respect the access labels; the catalog itself is not an exfiltration surface.

## Validation

Run `scripts/check_catalog_metadata.py` on every catalog file before commit. Machine checks are the floor; ownership reachability and access-path accuracy require the review steps in the skill's catalog design workflow.
