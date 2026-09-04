# Upstream specifications

Tool design is specified elsewhere by parties who revise on their own cadence. This skill
treats those documents as normative and does not restate them. A restatement becomes a
second copy that drifts, which is the defect `STALE_PUBLIC_REFERENCE` names, and the suite
applies that gate to other people's products.

The suite already works this way for SemVer, Diataxis, CHAOSS and OpenTelemetry. This file
is the same arrangement for tool definitions.

## Normative sources

| Source | Covers | Verified against |
|---|---|---|
| Model Context Protocol specification | server and tool contract, transport, capabilities | 2026-09-03 |
| MCP SEP-986, tool name format | naming rules for tools | 2026-09-03 |
| Anthropic, Writing effective tools for AI agents | namespacing, consolidation, response design, token efficiency, description engineering | 2026-09-03 |
| AWS Prescriptive Guidance, MCP tool strategy, and awslabs/mcp DESIGN_GUIDELINES.md | parameter count guidance, tool granularity | 2026-09-03 |

## Re-verification

Check these sources when auditing, and update the date column in the same change. A source
that has moved is a finding: the audit is being run against guidance that no longer says
what it said.

Two of these are not versioned artifacts. A vendor engineering post and a markdown file in
another repository can be edited or removed without notice, which is a weaker guarantee
than a dated specification. Treat a changed or missing source as a finding rather than
assuming continuity.

## What this skill adds

The sources above tell an author how to write a good tool. None of them ships the review
that tries to prove the tool surface wrong: a reviewer taking each confusable pair and
asking whether the descriptions alone decide the selection. That review, and the candidate
inventory that supports it, is this skill's contribution.
