# Token Scope Preview Standard

## Objective

Never create a credential whose scope the user cannot enumerate. Every token creation surface shows exactly what the token will permit before the token exists.

## Preview rules

- the preview is generated from the same policy the token will enforce, never a hard-coded copy
- show the exact permissions, scopes, and resources the token will carry
- render a human-readable summary and a machine-readable scope statement embedded in the token artifact itself
- scoped tokens are the default; broad or unscoped tokens require explicit opt-in and state what they cover

## Expiry display

- token creation shows the expiry before the token is issued
- every token and grant lists its expiry in one consistent format wherever it appears
- warnings precede expiry and include the renewal path

## Audit

- creating, listing, and revoking tokens are themselves permissioned actions with audit records
- token listings show scope and expiry alongside the name, not behind a detail page
- a token's audit trail records who created it, what it was scoped to, and when it was revoked

## Verification

For each token surface, obtain a token, decode or query its scope, and confirm the preview matched the issued scope. A preview that contradicts the issued token is a P1 finding.
