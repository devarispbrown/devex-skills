# Inner Loop Audit

## Scope

The inner loop is the developer's edit-to-feedback cycle inside the repository: edit, format, compile, test, run, observe, debug. Audit each stage as a separate action-to-feedback segment.

## Stage map and budgets

| Stage | Budget constant | What feedback ends the segment |
|---|---|---|
| Format/lint | FEEDBACK_FORMATTER_MAX_S | formatter or linter result |
| Incremental compile | FEEDBACK_INCREMENTAL_COMPILE_MAX_S | typecheck or compile result |
| Unit tests | FEEDBACK_UNIT_TEST_MAX_S | unit test result |
| Focused integration | FEEDBACK_FOCUSED_INTEGRATION_MAX_S | focused integration result |
| Local reload | FEEDBACK_LOCAL_RELOAD_MAX_S | app reloaded and ready |

Run and observe are consumption stages: run exercises the app, observe verifies the behavior. They count as feedback segments when the developer must wait for them — a seed step or a deploy the developer cannot skip counts; background watching does not.

Debug is remediation, not a separate loop. Count it as part of the stage that failed.

## Per-stage measurement

For every stage, time from the moment the developer's action completes to the moment the feedback arrives. Record:

- the exact command or watch that produces the feedback
- measured_seconds for the representative run
- the evidence label
- whether the environment was clean or warm

Do not split a stage from the toolchain that invokes it unless the developer invokes them separately.

## Common root causes

- cold cache or missing incremental artifacts
- full rebuild where an incremental path exists
- test runner recompiling or reseeding before every run
- watch mode not started, silently restarting, or watching the wrong paths
- formatter or linter invoked over the whole tree instead of the change

## Verify

- each stage's measured time is compared against its own budget constant
- no stage is measured against the wrong constant
- the mapping of stage to constant is stated in the report
