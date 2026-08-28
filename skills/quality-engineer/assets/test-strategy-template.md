# Test Strategy for <PRODUCT_OR_SYSTEM>

Scope: <SCOPE_STATEMENT> · Owner: <OWNER> · Review date: <YYYY-MM-DD>

## System classification

| Surface | System type | Entry points | Dependencies | Consumers |
|---|---|---|---|---|
| <SURFACE_NAME> | <CRUD_API_OR_STREAMING_PIPELINE_OR_STATEFUL_SERVICE_OR_CLI_OR_LIBRARY_OR_INFRASTRUCTURE> | <ENTRY_POINTS> | <STORAGE_BROKERS_SERVICES> | <WHO_DEPENDS_ON_IT> |

## Technique map

| Production behavior | Failure mode | Technique | Test location | Evidence label |
|---|---|---|---|---|
| <BEHAVIOR> | <WRONG_RESULT_CRASH_DATA_LOSS_DUPLICATE_INCOMPATIBILITY_LEAK_UNAVAILABLE> | <UNIT_CONTRACT_PROPERTY_FUZZ_FAILURE_INJECTION_RACE_SNAPSHOT_COMPATIBILITY_MIGRATION> | <PATH_OR_CI_JOB> | <OBSERVED_CI_OBSERVED_ESTIMATED> |

## Gap list

| Gap | Unprotected behavior | Severity | Decision | Evidence |
|---|---|---|---|---|
| <GAP_ID> | <BEHAVIOR_WITH_NO_TEST> | <P0_P1_P2_P3> | <TEST_SCHEDULED_OR_ACCEPTED_RISK> | <EVIDENCE_LABEL_OR_REASON> |

## Gate wiring

| Gate | CI job/check | Command | Expected evidence | Verdict |
|---|---|---|---|---|
| <GATE_NAME> | <JOB_NAME> | <COMMAND> | <WHAT_MUST_PASS_OR_FAIL> | <PASS_PASS_WITH_DEBT_FAIL_UNVERIFIED> |

Supported-version claims: <LIST_EVERY_CLAIMED_VERSION_OR_PLATFORM_AND_ITS_CI_JOB>.

## Validation log

| Injected failure | Test that caught it | Environment | Evidence label | Date |
|---|---|---|---|---|
| <WHAT_WAS_BROKEN> | <TEST_NAME> | <CI_OR_LOCAL> | <OBSERVED_CI_OBSERVED_ESTIMATED> | <YYYY-MM-DD> |

Every P0/P1 gap must appear here with a caught injected failure, or be explicitly accepted.
