---
name: developer-workflow-auditor
description: Audit inner and outer feedback loops: edit, format, compile, test, run, observe, debug against explicit feedback budgets (formatter 2s, incremental compile 5s, unit tests 10s, focused integration 60s, local reload 3s, CI first signal 3min, full CI 10min) and protect flow state from waits and context switches. For whole-journey friction use developer-experience-auditor; for runtime speed of shipped artifacts use performance-engineer.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and build/test tooling.
metadata:
  version: "2.2.0"
---

# Developer Workflow Auditor

## Mission

Measure the inner and outer feedback loops against explicit time budgets and protect flow state. A workflow is healthy when every action produces its feedback within budget — format, incremental compile, unit tests, focused integration, local reload, CI first signal, full CI — without forced waits or context switches.

The budgets are canonical constants, not local opinions. Cite them by name; never redefine their values in prose.

Run this audit when feedback feels slow, when developers report waiting, or before a tooling investment. The audit produces measurements, not impressions: every finding is a number compared to a named constant, labeled with evidence.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Read `references/inner-loop.md` when auditing the inner loop.

Read `references/outer-loop.md` when auditing the outer loop.

Read `references/feedback-budgets.md` when applying the feedback budgets.

Read `references/flow-state.md` when assessing flow state, waits, and context switches.

Read `references/loop-measurement.md` when measuring a loop segment or labeling evidence.

## Flow state

Flow state is the developer's active working context: the current task, the feedback they expect next, and the next action. Every forced wait or context switch dissolves it, and rebuilding it costs more than the wait itself.

A forced wait >30 seconds between edit and feedback breaks flow state. Do not dismiss a 30-second wait because the stage budget still passes — the flow-state rule is independent of the stage budget.

Detect interruptions: manual status checks, queued jobs, missing watch mode, degraded incremental paths, feedback delivered in a different window than the action. Each interruption is a P2 finding on its own.

The cost of a context switch is the rebuild time: the developer must re-establish what they were doing, what they expected, and the next action. A workflow that forces frequent small switches costs more than one long wait.

Do not classify chosen activity as a forced wait. Reading, planning, or parallel work the developer opted into is not a wait the workflow caused.

Protection rules:

- Never design a workflow step that requires the developer to poll for its result.
- Never place the result of an action in a different tool than the action itself.
- Never require a manual step between edit and feedback that automation can perform.

Verify: between every action and its feedback, the developer is never required to idle longer than the flow-state rule.

## Feedback loop audit

Audit the loops in five steps. Every measurement is compared against exactly one FEEDBACK_* constant, and every measurement carries exactly one evidence label.

### 1. Map the loops

Enumerate the inner loop as it actually exists: edit, format, compile, test, run, observe, debug. Enumerate the outer loop: commit, CI first signal, full CI, PR, preview, review.

Name each stage by its observable feedback — formatter result, compile result, unit result, integration result, reload, CI signal, CI completion — not by its tool.

Verify:

- every stage the developer actually performs is on the map, with its action-to-feedback path named
- the map distinguishes inner-loop stages from outer-loop stages
- the map covers the developer's default path, not the intended one

Do not map the intended workflow. Map the commands and watches that really run.

### 2. Measure each stage

Read `references/loop-measurement.md`.

Time each stage from action completion to feedback arrival. Record per stage: name, command, budget_seconds, measured_seconds, and one evidence label.

Record the method with the number: the command timed, the environment (clean or warm), and the sample chosen. A measurement without its method is unverifiable.

Do not average stages. Do not time only the happy path. Do not report the fastest sample as the truth.

### 3. Run the checker

Write the measurements to a loop manifest JSON matching the assets fixtures, then run:

`python3 scripts/audit_feedback_loops.py <manifest.json>`

The script never executes commands; the manifest's command field is documentation. Use `assets/loop-manifest.example.json` as the shape reference for a valid manifest.

Verify: exit 0 means every stage is within budget; exit 1 lists the breaches. Record the exit code in the report.

### 4. Diagnose breaches

For each BREACH, attribute exactly one primary root cause: cold cache, full rebuild, serial dependency, missing incremental path, CI queue time, or review latency.

Apply severity: one exceeded budget is P2; two or more are P1. A forced wait >30 seconds between edit and feedback is P2 regardless of the stage budget.

Verify:

- every breach has exactly one primary root cause
- severity follows the contract above, never a judgment call
- the breach is reproduced before the fix, not assumed

Never explain away a breach with a warm cache unless the default state is warm. Never compare against a budget you redefined.

### 5. Recommend and verify fixes

Recommend the smallest change that restores compliance: caches, incremental builds, watch mode, parallel or sharded tests, split CI jobs, an earlier first signal.

Prioritize P1 breaches before P2. Do not gold-plate: one fix per breach, re-measured, verified, then the next.

Never mark a fix verified on Estimated evidence. Re-measure after each change with the same method and the same evidence rules.

Do not fold unrelated tooling improvements into the audit's recommendations.

## Feedback budget contract

- Every loop stage maps to exactly one FEEDBACK_* constant by name.
- Measured time at or under the budget constant is PASS; over it is BREACH.
- The manifest expresses every budget in seconds, including the minute-based CI constants.
- One exceeded budget is P2; two or more are P1.
- A forced wait >30 seconds between edit and feedback is a flow-state break (P2), independent of the stage budget.
- A stage measured with Estimated evidence can never prove PASS.
- Budget constants are canonical. Do not restate their values in prose, add local variants, or adjust a budget to fit a measurement.

## Evidence contract

- Every measurement carries exactly one label: Observed, CI-observed, or Estimated.
- Observed: a human or agent actually executed the step and timed it.
- CI-observed: automation executed the step; useful for drift but may undercount human time.
- Estimated: reasoned from steps without execution.
- Never present an estimate as proof of passing a budget. A metric without an evidence label is UNVERIFIED.

## Required output

Produce the feedback loop audit report using `assets/feedback-loop-report-template.md`.

The report must contain:

1. **Loop map** — inner and outer loop stages with their action-to-feedback paths
2. **Measurements** — per stage: budget constant, measured time, PASS/BREACH, evidence label, environment
3. **Breach analysis** — root cause and severity per breach
4. **Flow-state findings** — forced waits >30 seconds, context switches, interruptions observed
5. **Recommendations** — the smallest fix per breach, with verification status
6. **Verdict** — PASS when no breaches; otherwise FAIL with the P1/P2 summary

## Definition of done

The audit is done when:

- every inner-loop and outer-loop stage the developer performs is mapped and measured
- every measurement is compared to its FEEDBACK_* constant by the checker script
- no stage is mapped to the wrong FEEDBACK_* constant
- the manifest is machine-checkable and the checker exit code is recorded
- every breach has a root cause and a severity
- no estimate is presented as proof of passing a budget
- flow-state findings are reported as their own section, not buried in the breach table
- the report is rendered from the template and states the verdict

Hand off whole-journey friction to the `developer-experience-auditor` skill if available, and runtime performance of shipped artifacts to the `performance-engineer` skill if available. This skill audits the loops and the wait; it does not replace either.
