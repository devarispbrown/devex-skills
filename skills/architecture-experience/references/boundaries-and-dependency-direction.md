# Boundaries and Dependency Direction

## Hard objective

Verify that every claimed module/service boundary is real in the repository and that every dependency edge respects the system's stated direction rules, so the mental model does not inherit fictional structure.

## Boundary audit procedure

1. List candidate boundaries: modules, services, packages, deployables, namespaces.
2. For each candidate, verify it exists in code: directory, package, manifest, or runtime topology.
3. Check that the boundary is enforced: import rules, build boundaries, or team ownership.
4. Record boundary strength: enforced, convention-only, or fictional.

A boundary that exists only in prose or diagrams is a finding. A boundary that code cannot enforce is weaker than one enforced by tooling.

## Dependency direction rules

Verify per edge, never averaged:

- layers point in one direction, e.g. presentation → application → domain → infrastructure
- the dependency graph is acyclic; cycles are findings
- cross-boundary calls respect ownership; an upward call requires an explicit exception
- cross-boundary data structures do not leak internals; no domain objects in presentation, no DB rows in domain
- shared code lives in a shared module, never in a lower layer imported upward

## Violation classes

| Class | Example | Evidence to record |
|---|---|---|
| Cycle | A imports B, B imports A | both edges |
| Upward edge | domain imports infrastructure | the edge, the reason |
| Leak | service passes a DB row to the client | the type, the caller |
| Fictional boundary | a diagram shows a service that does not exist | absence in the repo |
| Unenforced boundary | convention-only layering | the violating edge |

## Evidence

Every finding carries the file, the dependency edge, the direction, and the rule violated. Label findings by how they were found: Observed (read the code), CI-observed (automated check), or Estimated (inferred).

## Output

A per-edge table of direction and violations feeds the architecture brief's dependency direction section. Do not remove a violation from the report because the codebase is legacy; legacy violations are the most valuable findings.
