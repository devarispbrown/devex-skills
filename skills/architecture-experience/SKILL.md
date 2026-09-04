---
name: architecture-experience
description: Accelerate mental-model formation: module boundaries, dependency direction, ownership, data and control flow, extension points, ADRs, and the Architecture Magic Path of explaining where a feature belongs and tracing one request end-to-end within ARCHITECTURE_COMPREHENSION_MAX_MIN. For catalog-style discovery of services and owners use developer-discoverability.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and code navigation tooling.
metadata:
  version: "2.5.2"
---

# Architecture Experience

## Mission

Accelerate mental-model formation: module boundaries, dependency direction, ownership, data and control flow, extension points, and the decisions that shaped them. Deliver the two canonical answers — where a new feature belongs, and how one representative request flows end to end — fast enough to be useful inside a working session.

Describe the system as it is, not as it was designed. Ground every claim in the repository, tests, schemas, and runtime artifacts. When the code contradicts documented intent, surface the contradiction; never smooth it over.

Work in audit-first mode: form and verify the model before proposing changes. Redesign proposals are backlog entries, not audit results. This skill measures how quickly the system can be understood, not how good the system is.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

For catalog-style discovery — listing, searching, and indexing services and owners — use the `developer-discoverability` skill instead of re-deriving inventories here.

## Architecture Magic Path

A competent engineer explains where a new feature belongs AND traces one representative request end to end within `ARCHITECTURE_COMPREHENSION_MAX_MIN`.

Design for the timer. The timer covers orientation, boundary identification, the feature placement question, the request trace, and verification of the resulting claims. It stops when both answers are stated with evidence and rationale.

Benchmark persona: an engineer with repository access and code navigation tooling, general competence in the stack, and no prior mental model of this system.

The pass/fail bands and severity vocabulary are canonical in `references/standards.md`. Cite the constant by name; never restate its value here.

Evidence labels: **Observed**, **CI-observed**, or **Estimated**. An estimate cannot prove a pass; it can only indicate likely risk or feasibility.

Run `scripts/estimate_architecture_path.py` on a request trace or import graph for an Estimated comprehension time before committing to a budget.

Reading docs, chasing imports, and re-tracing wrong paths all count against the timer. The hop list is the estimate of record; it is not the full cost.

## Architecture experience workflow

### 1. Scope and orient

Determine:

- the system under study and its repository layout
- the representative request to trace, or the feature to place
- the benchmark start and stop conditions
- which claims can be Observed versus only Estimated

Do not begin a trace before the request's entry point and expected terminal effect are named. Record the repository layout and the system's entry points before choosing a representative request.

### 2. Form the mental model

Read `references/mental-model-formation.md`.

Answer the feature placement question: which module, service, and file the feature belongs in, and why. Then trace one representative request end to end, recording every hop.

Stop when the model is internally consistent, every hop is grounded in evidence, and the trace ends at a verified terminal effect.

Verify the placement answer survives the boundary and dependency checks before it is final.

### 3. Audit boundaries and dependency direction

Read `references/boundaries-and-dependency-direction.md`.

Verify that module and service boundaries are real in the repository, not only in prose. Check dependency direction per edge: layers point one way, the graph is acyclic, and no cross-boundary calls or data structures leak between layers.

Flag every violation as a finding with the file and dependency edge as evidence.

Verify every boundary claim against the repository; prose and diagrams are hypotheses.

### 4. Build the ownership map

Read `references/ownership-map.md`.

For each module or service, record the owner, code path, public surface, and escalation or on-call route. Derive ownership from CODEOWNERS, manifests, and git history. Unknown ownership is a finding, not a skip.

Verify the map against current manifests; a map that cannot be cross-checked is stale.

### 5. Trace data and control flow

Read `references/data-and-control-flow.md`.

Trace each relevant flow type — request/response, event/async, batch, config-driven — with the per-type procedure. Record each hop's layer, transformation, side effects, and failure modes.

Verify each hop in code or tests; inferred hops are labeled Estimated.

### 6. Audit ADRs

Read `references/adr-patterns.md`.

Verify each ADR states status, context, decision, consequences, and supersedes. Detect staleness: decisions contradicted by code, tests, or docs; statuses not updated; superseded decisions without a pointer to the successor.

Verify ADR status against the code; a decision the code contradicts is stale.

### 7. Identify extension points

Locate where new features, plugins, hooks, and protocols attach. Distinguish designed extension points from accidental seams. Note the hop cost each extension path adds to the mental model.

Verify an extension point by finding at least one consumer or call site.

### 8. Estimate the Architecture Magic Path

Assemble the trace as a JSON hop list and run `scripts/estimate_architecture_path.py`. Compare the Estimated comprehension time against `ARCHITECTURE_COMPREHENSION_MAX_MIN`; the script's default budget comes from its embedded constant table.

If the estimate is over budget, attribute the excess to individual hops and propose reductions: fewer hops, clearer boundaries, ownership clarity, or ADR remediation.

Example: `python3 scripts/estimate_architecture_path.py trace.json --max-const ARCHITECTURE_COMPREHENSION_MAX_MIN`. Verify the estimator against the bundled fixtures before trusting it on a real trace.

## Contracts

- Every claim carries an evidence label: Observed, CI-observed, or Estimated. An estimate cannot prove a PASS.
- Boundaries, dependencies, and ownership are derived from the repository, tests, and runtime artifacts, never from interviews or prose alone.
- Dependency direction is stated per edge; cycles and upward edges are findings, not noise.
- Ownership resolves to a team or role, or is recorded as Unknown. Unknown is a finding.
- ADR status is the current decision state; stale ADRs are findings.
- The Architecture Magic Path is compared against `ARCHITECTURE_COMPREHENSION_MAX_MIN` by name; values come from the canonical metrics and are never restated here.
- Hops are counted per layer crossing, and a trace is incomplete until it ends at a verified terminal effect.
- Heuristic tool output is never a verdict; semantic review is still required.

## Required output

Produce the architecture brief from `assets/architecture-brief-template.md`. The brief must contain:

1. Scope — system, representative request or feature, evidence labels
2. Mental model — feature placement answer with rationale; trace summary
3. Boundary audit — module/service boundaries verified, with evidence
4. Dependency direction — per-edge direction; cycles and violations
5. Ownership map — module/service to owner, or Unknown
6. Data and control flow — per flow type, with hops and transforms
7. ADR audit — quality and staleness findings
8. Extension points — designed versus accidental
9. Architecture Magic Path — hop count and Estimated minutes versus `ARCHITECTURE_COMPREHENSION_MAX_MIN`, with budget verdict
10. Prioritized backlog — findings with severity, evidence, and owner type

Sanity-check the estimator with `assets/trace-example.json` and `assets/trace-example.clean.json` before running it on real traces.

Label every number in the brief with its evidence: Observed, CI-observed, or Estimated. Unlabeled numbers are UNVERIFIED.

## Definition of done

Architecture experience work is done when:

- the feature placement question is answered with evidence and rationale
- one representative request is traced end to end with every hop recorded
- module/service boundaries are verified against the repository
- dependency direction is stated per edge, with violations flagged
- the ownership map is complete or explicitly Unknown
- data and control flow are traced for every relevant flow type
- ADRs are audited for quality and staleness
- extension points are identified and classified designed versus accidental
- the Architecture Magic Path is Estimated and compared against `ARCHITECTURE_COMPREHENSION_MAX_MIN`
- every claim is labeled Observed, CI-observed, or Estimated
- over-budget paths are attributed to hops with proposed reductions
- no fictional boundary or unverified hop is presented as fact
- the brief is rendered from `assets/architecture-brief-template.md`

Hand whole-product journey measurement to the `developer-experience-auditor` skill and documentation release gating to the `developer-docs-auditor` skill when available. This skill forms the mental model; it does not replace either.
