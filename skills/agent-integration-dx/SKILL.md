---
name: agent-integration-dx
description: Design and audit tool definitions and MCP servers as shipped product artifacts. Covers tool naming, description-as-prompt authoring, argument schema design, response shaping against a context budget, pagination and truncation, and error surfaces an agent can act on. Use when building an MCP server, exposing tools to an agent framework, or reviewing a tool surface for wrong-tool selection. For auditing a whole repository's agent readiness use agent-native-dx; for the underlying HTTP API design use api-design-reviewer.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access to the tool definitions or MCP server source.
metadata:
  version: "2.9.4"
---

# Agent Integration DX

## Mission

A tool definition is a shipped product artifact. Its name, description, argument schema
and response shape are authored by the vendor and consumed by a model that cannot ask a
follow-up question. The description is a prompt you shipped, and it is doing prompt work
whether or not it was written that way.

This is the surface where a product either becomes usable by agents at runtime or does
not. It is distinct from making a repository legible to a coding agent, which is
`agent-native-dx`, and from the HTTP contract underneath, which is `api-design-reviewer`.

Read `references/standards.md` for the canonical severity vocabulary and release gates.

## Scope

In scope: tool names, tool descriptions, argument schemas, response bodies as the agent
sees them, pagination and truncation, tool-level error surfaces, and how many tools a
single server exposes.

Out of scope, with owners: transport, retry, and context management belong to the agent
harness, not the vendor. Repository legibility is `agent-native-dx`. Resource design,
status codes and idempotency are `api-design-reviewer`. Rate limits and quota semantics
are `developer-economics`. Credential scope and delegation are `access-and-permissions-dx`.

## This skill cites, it does not restate

Tool design already has published specifications that revise on their own cadence. This
skill treats them as normative and adds the audit they do not ship.

Read `references/upstream-specs.md` for the pinned revisions and the re-verification
cadence. Restating a spec here would create a second copy that drifts, which is the defect
`STALE_PUBLIC_REFERENCE` names.

What this skill adds is the adversarial review: a tool surface examined by someone trying
to prove the agent will pick the wrong tool, and a check that reports candidates.

## Tool definition workflow

### 1. Inventory the tool surface

Run the inventory over the tool definitions:

```
python3 scripts/check_tool_surface.py path/to/tools.json
```

Most servers do not ship their tool definitions as a file. They declare them in source and
return them from `tools/list` at runtime, so capture that response and pass it. The
checker accepts a `tools/list` result, a bare array of tool objects, or an object with a
`tools` key.

It reports candidates only and never issues a verdict, following the same convention as
`guessability_check.py` in `api-design-reviewer`. It exits non-zero when it emits
candidates, which means there is something to look at, not that the surface has failed.

### 2. Audit names and descriptions

Read `references/tool-definitions.md` before writing or reviewing a tool definition.

Verify:

- names are verbs on a namespaced object, and no two tools are near-synonyms
- each description states what the tool does, when to choose it, and when not to
- descriptions name the sibling a caller might confuse this tool with
- nothing in a description depends on context the model was never given
- required arguments are genuinely required, and optional ones state their default

### 3. Audit argument schemas

Verify:

- every parameter has a type, a description, and an example where the shape is not obvious
- enums are closed and spelled out rather than described in prose
- no parameter requires the caller to construct an identifier it has no way to obtain
- the schema rejects what the endpoint rejects, so failures happen before the call

### 4. Audit response shape against a context budget

Read `references/response-shaping.md` before changing what a tool returns.

Verify:

- responses are shaped for a reader with a finite context, not for completeness
- list responses paginate, and truncation is explicit rather than silent
- identifiers the agent needs for the next call are present in the response
- third-party-sourced fields are labeled, so the agent can tell data from instruction

### 5. Adversarial selection review

Read `references/selection-review.md` when running the review.

Take each pair of tools a caller could plausibly confuse. Write the prompt that should
select each one. Ask whether the descriptions alone decide it. A pair that cannot be
separated by its descriptions is the finding, and the fix is the description or the
consolidation, never a note in the docs.

## Tool-definition contract

- one tool per user intent, not one tool per endpoint
- a description states selection criteria, not just behavior
- an argument schema is a validation surface, not documentation
- a response is a message to a reader with a budget
- an error names the corrective action the agent can take without a human

## Untrusted content

A tool that returns third-party text places content the vendor did not author into an
agent's context. Treat the boundary as product surface: declare which response fields
carry third-party data and state the labeling contract for them. A product that cannot
say which fields are attacker-influenced cannot claim the boundary is handled.

This is a disclosure requirement, not a safety proof, and it is currently unautomated.
No checker in this suite reads untrusted-content declarations, and no gate constant
covers them. Treat the absence of a declaration as a finding recorded by a human reviewer,
not as something the tooling will catch.

## Required output

Produce the tool surface report using `assets/tool-surface-template.md`, containing:

1. **Tool inventory** with name, stated intent, and the sibling it is most confusable with
2. **Per-finding severity and evidence**, using the canonical severity vocabulary
3. **Selection review results**, listing each confusable pair and whether descriptions separate it
4. **Prioritized changes**, each naming the product change and how to verify it

## Definition of done

- names, descriptions, argument schemas and response shapes are all audited
- every confusable pair has been reviewed and either separated or consolidated
- untrusted-content fields are declared, or their absence is recorded as a finding
- upstream specs were re-verified against the dates in `references/upstream-specs.md`
- every finding names a product change, never a documentation workaround

Hand repository-level agent readiness to `agent-native-dx` if available, HTTP contract
design to `api-design-reviewer`, and quota semantics to `developer-economics`.
