---
name: agent-native-dx
description: Make a product excellent for coding agents: AGENTS.md/CLAUDE.md quality, machine-readable schemas, structured CLI output, stable error codes, OpenAPI, MCP, Agent Skills, deterministic scripts, repository structure, and test discoverability. Human DX and agent DX are both first-class. For the human-facing documentation use developer-docs.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and agent tooling context.
metadata:
  version: "2.5.2"
---

# Agent-Native DX

## Mission

Developers increasingly work through coding agents, not only terminals. Agent UX is product UX: an agent that cannot build, run, verify, or debug your product is a product defect, not a documentation footnote.

Treat every agent-visible surface — entry files, schemas, structured output, error codes, scripts, tests, repository structure — as part of product design. Audit it as a product, and recommend product changes rather than documenting around friction.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Two audiences, one corpus

Humans and agents read the same repository. The corpus has two first-class audiences:

- **Humans** read prose, examples, and explainers.
- **Agents** read the same prose plus machine-readable complements: AGENTS.md/CLAUDE.md entry files, OpenAPI and JSON Schema, structured CLI output, stable error codes, MCP servers, Agent Skills, deterministic scripts, and discoverable tests.

Do not fork the corpus. Write one set of facts, and add machine-readable surfaces that state the same facts in agent-usable form. When prose and machine surface disagree, both lose to implementation truth — and the contradiction is a P1 finding.

For the human-facing documentation use the `developer-docs` skill if available. This skill audits and improves the agent-facing surfaces.

## Agent-native DX workflow

### 1. Audit agent entry points

Run `scripts/check_agent_readiness.py` on the repository root as a first-pass inventory signal. The output is heuristic and never a verdict.

Read `references/agent-entry-files.md` when auditing or writing AGENTS.md/CLAUDE.md entry files.

Read `references/agent-audit.md` when planning the audit, defining simulated agent tasks, and recording tool-use traces.

Verify:

- an entry file exists at the repository root
- it names the commands to build, test, run, and verify
- invariants and gotchas an agent cannot infer are stated
- commands are complete, copy-pasteable, and current
- the entry file is the single source for agent guidance, not a duplicate of the docs

### 2. Audit machine-readable surfaces

Read `references/machine-surfaces.md` when auditing OpenAPI, JSON Schema, structured CLI output, stable error codes, MCP servers, or Agent Skills.

Verify:

- canonical machine schemas exist for public interfaces and match implementation
- CLIs emit structured output (`--json` or equivalent) for the operations agents automate
- error codes are stable, documented, and machine-distinguishable from prose messages
- MCP and Agent Skills surfaces exist where they pay off, per the reference

### 3. Audit automation safety

Read `references/automation-safety.md` when auditing determinism, idempotency, non-interactive modes, destructive-operation guardrails, or secrets handling.

Verify:

- scripts and commands are deterministic and idempotent
- every interactive prompt has a non-interactive equivalent
- destructive operations require explicit opt-in; nothing destructive is the default
- secrets never appear in output, logs, or example commands

### 4. Audit test discoverability

Read `references/discoverability.md` when auditing repository structure, test discoverability, command discovery, or state inspectability.

Verify:

- the repository layout is conventional enough for an agent to map
- tests are discoverable by name and location, and runnable with one documented command
- commands are discoverable through complete `--help` output
- state is inspectable without mutation (status/describe/dry-run commands)

### 5. Recommend agent-native improvements

For each gap, produce a prioritized improvement:

1. Name the surface and the finding.
2. Assign severity using the canonical severity vocabulary.
3. State the exact product change, never a documentation workaround.
4. State how to verify the change with an agent-visible signal.

Do not recommend prose that merely describes the gap. Recommend the product change that removes it.

## Agent trials

Auditing the surfaces is not the same as observing an agent fail. A trial runs an
agent against a target repository and records what actually happened, so findings rest
on observation rather than inspection.

Read `references/trial-protocol.md` before running or scoring a trial. It defines
pre-registration, the coverage corpus, the classification codebook, the second-rater
sample, the trial log format, and the decision rule.

The work splits in two, and the split is not optional:

- The **live driver** is `scripts/agent_trial_driver.py`. It runs the agent sessions,
  N >= 5 per repository and task, and writes the trial log. It is dry run by default and
  executes nothing until `--execute` is passed, matching the gate on `magic_path_runner.py`
  in `developer-docs-auditor`. It holds no credentials and speaks to no model: it invokes
  the command in `registration.harness_command`, so the harness under test is whichever
  agent CLI the operator has installed. It never runs in CI, because GitHub withholds
  secrets from fork `pull_request` runs and a keyed driver would pass for maintainers and
  error for everyone else.
- The **scorer** is `scripts/agent_trial_scorer.py`. It consumes a trial log offline
  and deterministically, validates that the trial was pre-registered, and applies the
  decision rule. A trial scored without a complete registration is not evidence, and
  the scorer refuses it rather than reporting a verdict.

Run it against the worked example:

```
python3 scripts/agent_trial_driver.py assets/trial-log.example.json   # plan, runs nothing
python3 scripts/agent_trial_scorer.py assets/trial-log.example.json   # verdict and inventory
```

Outcome is decided by each task's committed `verify` command, not by reading a
transcript, and every session runs against a fresh shallow clone in a scratch directory.
The driver refuses a task with no verify command and refuses an incomplete registration.

`assets/trial-log.unregistered.json` is the counterpart fixture: a trial that cannot be
scored because it was never registered. Both fixtures are synthetic and name no real
product.

`scripts/check_decision_rule.py` pins the bands, both inclusive edges, and the
minimum-sample guard, so a change to the rule cannot pass silently.
`scripts/check_protocol_example.py` runs the example inside
`references/trial-protocol.md` through the same validator, so the documented format
cannot drift from the code.

The verdicts ALREADY-COVERED and REAL-GAP answer one question specific to this suite:
whether it should add a skill for agent-facing surfaces. A team auditing their own
product should read the uncovered inventory, which names real defects in their
product, and ignore the verdict, which is about this repository's roadmap.

The scorer reports the share of distinct failure modes the registered coverage corpus
does not catch. Attribution to the nine problem classes is reported alongside it
and never decides coverage: those classes are exhaustive by construction, so treating a
successful classification as coverage would drive `u` to zero mechanically.

## Agent-entry contract

An AGENTS.md/CLAUDE.md entry file is the agent's first read. It must contain:

- build, test, run, and verify commands that are complete and copy-pasteable
- invariants, gotchas, and constraints the agent cannot safely infer
- architecture pointers, not architecture essays
- current facts only; never duplicate content that lives in the docs

Entry files age like code. They belong in the same change as the behavior they describe. A stale entry file is a P1 finding — it misleads every agent that reads it.

## Machine-surface contract

Machine-readable surfaces are products with their own UX:

- OpenAPI is the canonical contract for HTTP APIs; JSON Schema for config and inputs
- structured CLI output is the contract for automation; humans keep the human output
- error codes are identifiers, stable across releases, documented with meaning and remediation
- MCP servers and Agent Skills are agent-native surfaces held to the same quality bar as the API

A machine surface that drifts from implementation truth misleads agents more reliably than missing prose, because agents trust it. Drift is a P1 finding.

## Automation-safety contract

Agents automate what humans would type. Every command an agent runs must be safe to run twice and safe to run unattended:

- deterministic: same input, same output, same order
- idempotent: rerunning converges, never doubles or corrupts
- non-interactive: every prompt has a flag, env var, or default
- destructive operations opt in explicitly and state their scope
- secrets stay out of output, logs, and examples

Never recommend a script pattern that relies on interactive confirmation as its only guardrail.

## Required output

For every audit, produce the agent-native readiness report using `assets/agent-readiness-template.md`.

The report must contain:

1. **Readiness checklist** — every audited surface with status and evidence
2. **Per-surface findings** — each finding with severity, evidence, and the agent failure it causes
3. **Prioritized improvements** — ordered by severity and effort, each with a verification step
4. **Evidence labels** — Observed / CI-observed / Estimated per finding

Report findings, never opinions. Ground every finding in observed or CI-observed evidence where possible.

## Definition of done

An agent-native audit is done when:

- entry points, machine surfaces, automation safety, and test discoverability are all audited
- the readiness checklist reflects the actual repository state
- every finding carries a severity and an evidence label
- every improvement is a product change with a verification step, not a documentation workaround
- the report is rendered from `assets/agent-readiness-template.md`
- machine-surface drift and stale entry files are reported, never silently worked around

Hand off human-facing documentation work to the `developer-docs` skill if available, and whole-product developer-experience measurement to the `developer-experience-auditor` skill if available.
