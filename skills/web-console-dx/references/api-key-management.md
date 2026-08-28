# API Key Management UI

## Core principle

API keys are credentials, but key management is an operations flow. Developers must create, scope, rotate, and revoke keys without contacting support, and the same operations must be automatable through the API and CLI.

A key lifecycle that requires a support ticket is a P1 console defect: it blocks automation and slows every new integration.

## Create

- create requires: a name, a scope or permission set, and an expiry where the product supports it
- the create flow states what the key can and cannot do before generation
- the secret is displayed exactly once, on creation, with a copy button
- the success view states rotation and revocation policy, not just "key created"

## Display

- the list shows key name, prefix, scopes, created, last used, and expiry
- the secret is never shown again; a truncated prefix identifies each key
- last-used and last-created timestamps are visible so stale keys are obvious

## Scope

- scopes map to documented API permissions, using the same names as the API and CLI
- changing a key's scope is explicit and states when it takes effect
- the UI rejects scope sets the API cannot express

## Rotate and revoke

- rotation is one action: issue a new key and invalidate the old one, with the same scope
- revocation states the blast radius: which integrations, scripts, and environments used the key
- both operations confirm before applying and report the API call made
- rotation and revocation have CLI equivalents with copyable commands

## Expiry

- expiry is set at creation and shown in the list
- near-expiry keys are surfaced, and expired keys are visually distinct
- expiry semantics match the API: absolute time, and no silent renewal

## Audit

- the key list records who created, rotated, and revoked each key
- audit events for key operations are visible or documented as queryable
- every key event links to the API call that produced it

## Automation parity

- create, rotate, revoke, and scope changes each map to a named API endpoint
- the CLI equivalents are copyable from the key list and detail views
- a revoked or expired key is expressible in the same state in API, CLI, and UI
