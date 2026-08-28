# Feedback Budgets

## Canonical constants

Apply the seven budgets by constant name. They are canonical; never redefine values or add local variants:

- `FEEDBACK_FORMATTER_MAX_S` — formatter/linter feedback
- `FEEDBACK_INCREMENTAL_COMPILE_MAX_S` — incremental compile
- `FEEDBACK_UNIT_TEST_MAX_S` — unit test result
- `FEEDBACK_FOCUSED_INTEGRATION_MAX_S` — focused integration result
- `FEEDBACK_LOCAL_RELOAD_MAX_S` — local reload
- `FEEDBACK_CI_FIRST_SIGNAL_MAX_MIN` — CI first useful signal
- `FEEDBACK_FULL_CI_MAX_MIN` — full CI

## Applying a budget

For each constant:

1. Confirm the stage maps to this constant and to no other.
2. Measure wall-clock from action completion to feedback arrival.
3. Compare the measured time to the constant.
4. Record PASS or BREACH with the evidence label.

Do not substitute a different unit for a constant's unit. The manifest expresses every budget in seconds, including the minute-based CI constants.

## Severity

- One exceeded budget: P2.
- Two or more exceeded budgets: P1.
- A forced wait >30 seconds between edit and feedback: P2 flow-state break, independent of stage budgets.

## Rules

- Never adjust a budget to fit a measurement.
- Never average a breach with a pass across stages.
- Never restate a constant's value in prose when the constant name suffices.
- An estimate can never prove a PASS.
