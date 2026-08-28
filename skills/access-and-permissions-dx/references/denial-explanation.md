# The 403 Explanation Standard

## Objective

Every expected denial answers four questions in the surface where it occurs:

1. **Required permission** — the exact permission the action needs, by canonical name.
2. **Your role** — the requester's current role, stated as-is.
3. **Roles containing it** — which roles grant that permission, so the requester can see the distance to access.
4. **Request route** — who grants it and how to ask, with expected turnaround.

A denial that omits any part is incomplete, regardless of how well the rest is written. A bare "forbidden", "access denied", or "insufficient permissions" on an expected path is a P1 or P2 finding per the canonical severity vocabulary.

## Good and bad

Bad:

> Access denied. Contact support.

Good:

> The `reports:read` operation requires the `reports:read` permission. Your current role is viewer; roles containing it are analyst and admin. Ask your admin to grant access; approval takes one business day.

## Rules

- state the required permission by its exact canonical name, never a paraphrase
- state the requester's current role, even when it seems obvious from context
- list the roles that contain the permission, not just the highest one
- give one concrete request route with expected turnaround; "contact support" with no path is not a route
- keep the four parts together; do not split them across pages or surfaces
- denial text is derived from the permission model and stays consistent with it

## Checking

`scripts/check_403_explanations.py` flags denials that omit the required permission, the grant route, or role context. Its output is heuristic: it proves the presence of a mention, never the correctness of the claim. Semantic review of the denial text is always required.
