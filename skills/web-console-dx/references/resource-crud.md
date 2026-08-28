# Resource CRUD UX in the Console

## Core principle

Every CRUD operation is one of the product's most repeated surfaces. List, create, read, update, and delete must each exist as a first-class operation with a matching API call and, where the product has a CLI, a copyable CLI equivalent.

A resource row that can be seen but not created, edited, or deleted is a support ticket waiting to happen.

## List

- show the fields developers actually filter and sort by, matching the API's filter/sort parameters
- pagination must not hide the total or make deep pages unreachable
- empty states explain how to create the first resource and link to the create flow
- each row offers the resource's actions directly; do not bury edit behind a detail page when update is a common action

## Create

- pre-fill defaults that match the API defaults; state what is defaulted
- every required field is marked and validated before submit
- on success, show the created resource's ID and link to its detail view
- on failure, show the API error, the failing field, and the next step

## Read and detail

- the detail view shows the resource's identity, status, timestamps, and the fields the API returns
- destructive or irreversible attributes are labeled
- the detail view links to the underlying API call and, when a CLI exists, offers a copyable command for the entity

## Update

- edits are explicit: show what changes, confirm before applying
- updates that trigger side effects (reprovision, redeploy, reindex) state the side effect and its duration
- partial updates show which fields were accepted and which were rejected

## Delete

- deletion requires confirmation and states irreversibility
- cascading effects (children, references, billing impact) are enumerated before confirmation
- soft-delete vs hard-delete semantics are stated and match the API
- after deletion, the UI confirms what was removed and what remains

## Bulk operations

Bulk operations exist when the API supports them. Never fake bulk behavior with repeated single calls that half-fail.

- bulk select, bulk action, and bulk confirm are explicit and auditable
- the UI reports per-item outcomes: succeeded, failed, skipped — never a bare aggregate
- partial failures surface the failed items with reasons and a retry path
- bulk operations are automatable: the API call behind them is documented and, with a CLI, scriptable

## Automation parity

- every CRUD action maps to a named API endpoint
- the CLI equivalent is copyable from the row or detail view
- filters and sort in the list view match the API query parameters
- IDs are copyable and match what the API and CLI use
