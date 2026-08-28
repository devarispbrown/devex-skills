# Expiry and Rotation UX Standard

## Objective

Expiry is a displayed, warned, and renewable property of every credential and grant. Rotation and revocation are documented procedures, not tribal knowledge.

## Expiry UX

- expiry is displayed in one consistent format on every token and grant listing
- warnings precede expiry with a concrete renewal path that does not require an admin
- what happens at expiry is stated: sessions end, calls fail, or access silently downgrades
- renewal is self-service and preserves least privilege

## Rotation

- every credential class has a documented rotation procedure: what to rotate, what breaks, and the rollback path
- rotation procedures are tested, not just written
- rotation revokes the old credential at the enforcement layer

## Revocation and leakage

- leaked or revoked credentials invalidate immediately and propagate to dependent sessions and consumers
- revocation notice reaches the grantee with the reason
- tokens derived from a revoked credential are invalid too

## Impersonation

- service accounts and impersonated sessions show who the credential acts as, not just who created it
- impersonation is time-bound and logged
- ownership of a credential is distinct from its use; the audit trail records both
