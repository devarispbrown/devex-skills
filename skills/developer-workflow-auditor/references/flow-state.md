# Flow State

## Definition

Flow state is the developer's active working context: the current task, the feedback they expect next, and the next action. It is the unit of cost in this audit. A lost context is a P2 finding even when every stage budget passes.

## The wait rule

A forced wait >30 seconds between edit and feedback breaks flow state. A forced wait is idle time the developer cannot avoid: no watch mode, a queued job, a manual step they must perform, a silent hang.

Do not classify as forced wait: reading, planning, or parallel work the developer chose, or a wait the developer can cancel and continue around.

## Context switches

Count context switches separately from waits: interruptions, manual status checks, opening another tool to find feedback, switching branches to stay busy. Each switch is a P2 finding.

Verify: during the audit window, note every moment the developer had to change activity to obtain or wait for feedback.

## Interruption detection

Look for:

- watch mode not running or watching the wrong paths
- commands that report "still running" with no intermediate output
- feedback delivered in a different window than the action that produced it
- long queue or scheduler waits before a job starts
- human-gated steps: approvals, manual deploy, manual review

## Reporting

Report flow findings as their own section, never folded into the breach table. A workflow with zero budget breaches can still fail on flow state.
