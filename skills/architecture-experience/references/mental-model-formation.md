# Mental Model Formation

## Hard objective

An engineer with repository access can state where a new feature belongs and can trace one representative request end to end, both with evidence, within `ARCHITECTURE_COMPREHENSION_MAX_MIN`.

## Benchmark persona

Assume the engineer has repository access, code navigation tooling, and general competence in the stack. Assume they do not have a prior mental model of this system, internal terminology, or tribal knowledge.

## Two canonical answers

The mental model is complete when both answers can be stated:

1. **Feature placement question** — given a new feature description, which module, service, and file it belongs in, and why.
2. **Request trace** — the path one representative request takes from entry point to verified terminal effect, hop by hop.

Answer the placement question first; it constrains the trace. If the placement question cannot be answered, the boundary audit is the blocker, not the trace.

## Feature placement procedure

1. Parse the feature description into what changes: behavior, data, surface, or integration.
2. Locate the existing code that owns the same behavior, data, or surface.
3. Check the ownership map and dependency direction for candidate modules.
4. Choose the lowest module that can own the change without violating dependency direction.
5. State the answer as module → service → file, with the alternatives considered and rejected.

## Request trace procedure

1. Name the entry point and the expected terminal effect before tracing.
2. Walk each hop: layer, component, transform, side effects, failure modes.
3. Record the data flow and the control flow separately; see `data-and-control-flow.md`.
4. Verify each hop in code or tests; do not infer hops from prose.
5. Stop at the verified terminal effect, not at a convenient stopping point.

## Stop conditions

Stop tracing when:

- every hop is grounded in a file, test, schema, or runtime artifact
- the model is internally consistent; no hop contradicts an earlier one
- the trace reaches a verified terminal effect
- the feature placement answer survives the boundaries and dependency checks

Do not stop at the first plausible answer. Do not stop because the model is large; stop because it is verified.

## Measurement

Label the result **Observed**, **CI-observed**, or **Estimated**. An estimate cannot prove a pass; it only indicates likely risk or feasibility. Run `scripts/estimate_architecture_path.py` on the hop list for an Estimated comprehension time.

## Diagnostic breakdown

When the path exceeds `ARCHITECTURE_COMPREHENSION_MAX_MIN`, attribute time to:

| Segment | Examples |
|---|---|
| Orientation | finding the entry point, naming the request |
| Boundary identification | discovering modules and services |
| Placement | deciding where the feature belongs |
| Trace | walking hops |
| Verification | confirming claims in code and tests |
| Recovery | dead ends, wrong layers, missing owners |

Classify the root cause as Architecture, Documentation, Ownership, or Tooling. Do not blame the trace when the boundary audit is the blocker.
