# Pilot results, 2026-09-03

Registration: pull request #17, published before any session ran.
Harness: claude-code headless 2.1.259, permissions granted, temperature 0.

## Scope actually run

Two repositories of the eight registered, as a pilot: `pallets/click` and `chalk/chalk`.
Three tasks, five runs each. 30 sessions.

| repository | task | outcomes |
|---|---|---|
| pallets/click | test | pass x5 |
| pallets/click | install | pass x5 |
| pallets/click | entry | pass x5 |
| chalk/chalk | test | pass x5 |
| chalk/chalk | install | pass x5 |
| chalk/chalk | entry | pass, fail, fail, fail, fail |

30 sessions, 4 failures, one distinct failure mode.

## Verdict

`TOO-FEW-FAILURES`. One distinct mode is far below the pre-registered minimum of 15, so
no uncovered share is reported. The rule was fixed before the data existed and it is
applied here unchanged.

## The one finding

Documenting `chalk/chalk` breaks `chalk/chalk`. Its `npm test` runs `xo`, which lints
markdown, including an `AGENTS.md` that did not exist a moment earlier. Every agent that
recorded the project's real test command failed on
`markdown/fenced-code-language`. The single pass recorded `npm install`, which tests
nothing.

This is a property of the product, not a mistake by the agent. A human contributor adding
any markdown file with an untagged code fence fails the same suite the same way. What is
agent-specific is the consequence: an agent asked to do one documented task does that task
and stops, where a human iterates until the linter is quiet.

Coverage: nothing in the registered corpus catches it. `BROKEN_CONTRIBUTION_PATH` is a
time threshold. The `contributor-experience` check-parity contract covers local versus CI
divergence, and here both fail identically. `UNEXPLAINED_ERROR` does not apply because
`xo` names the exact line and rule. No standard in this suite covers a verification
command coupled to repository contents.

## Two defects in the instrument, found by running it

**The harness wrote nothing and exited zero.** The headless CLI defaulted to blocking
writes. It ran 64 seconds, printed a correct `AGENTS.md` to stdout, and created no file.
At 120 sessions that produces a trial where every session fails and the uncovered share is
pure artifact, pointing at the answer the proposal wants. Fixed in pull request #16: the
driver now proves the harness can modify a tree before spending anything.

**The verify command rewards the wrong answer.** It accepts any recorded command that
exits 0, without checking the command actually runs tests. It bit once in 30 sessions,
and not randomly: it bites precisely in the cell where the honest answer fails, turning a
real failure into a pass. Unfixed, and it is why the remaining six repositories were not
run.

## Why the remaining 90 sessions were not spent

26 of 30 sessions passed. Two exceptionally well-maintained, heavily documented, popular
repositories, three basic tasks, on public code that is maximally likely to be in training
data. That is close to zero dynamic range, and at full scale this task set would return
`TOO-FEW-FAILURES` again while costing 90 more sessions.

Spending them would buy passes, not information.

## What a second attempt needs

- A verify that proves the recorded command is a test command, cheapest check being that
  it fails when a test is deliberately broken.
- Tasks with real dynamic range: make a change and keep the suite green, diagnose a seeded
  failure, upgrade across a breaking version.
- Repositories that are not the best documented projects in their ecosystems.

That is a different registration. This one stands as a published negative result for this
task set rather than being edited after the fact.

## Limits

Two repositories, one model, one harness, one date, one rater. The protocol requires a
second rater on 20 percent of modes and none was available, so that control is
unsatisfied and recorded as such in the log. The share is withheld by the decision rule,
not by choice.
