# Test Pyramid and Test-Cost Reasoning

## The pyramid

- **Unit tests**: fastest, cheapest, most numerous. Test one unit with dependencies stubbed. Catch logic, validation, and state-transition errors.
- **Integration tests**: fewer. Test real boundaries — storage, brokers, filesystem, external services via test doubles where required. Catch contract and wiring errors.
- **E2E tests**: fewest. Drive the deployed system through real entry points. Catch orchestration errors the lower layers cannot.

## When to invert

The pyramid is a default, not a law. Invert or flatten when the system's failure modes live at a higher layer:

- **CLI and scripts**: mostly integration/E2E-shaped; unit test the pure logic, golden-test the output, and keep one E2E smoke per subcommand.
- **Infrastructure**: plan/apply validation dominates; unit tests on HCL logic are rarely worth it.
- **Thin integration glue**: an API that mostly forwards to a stateful backend warrants contract and integration tests over deep unit suites.
- **Heavy contracts**: when consumers are many or external, contract tests outrank deeper unit tests of the provider.

Do not invert for convenience. Invert only when the cheaper layer demonstrably misses the failure modes you mapped.

## E2E budgets

- Keep E2E suites small: a few paths per surface, chosen for the failures lower layers cannot catch.
- Time-box E2E runs in CI. A suite that drags the pipeline is a defect, not a virtue.
- Every E2E test must be stable; a flaky E2E test is worse than none because it teaches the team to ignore red.
- Never duplicate a unit or integration test as an E2E test.

## Test-cost reasoning

Cost of a test = authoring time + CI time per run + flake maintenance. Pick the lowest layer whose test would catch the mapped failure mode.

- If a unit test catches it, do not write an integration test for the same behavior.
- If an integration test catches it, do not write an E2E test for the same behavior.
- When the cheapest layer cannot catch the failure, the extra cost is justified — that is the entire reason the upper layers exist.

Use coverage as a sanity signal at each layer, never as the reason a layer is "done."
