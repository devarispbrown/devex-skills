# Time to Recovery

## Definition

Time to Recovery (TTR) is the canonical metric: the time from hitting an expected error to completing its corrective action.

- **Hitting** the error: the user or caller first encounters the failure and its output.
- **Completing the corrective action**: the fix is executed and verified successful.

The clock covers reading the error, locating guidance, executing the corrective action, and verifying the result. It excludes general troubleshooting that the error output did not direct.

The target is `TTR_TARGET_MIN`. Meeting it is a design requirement on the error surface, not a support metric.

## Measurement procedure

1. Identify the three most likely failures from telemetry volume, support volume, or surface frequency. If data is unavailable, pick the three failures any new user would hit first.
2. Reproduce each failure from a clean or representative state, exactly as a real user would.
3. Measure the segments: read the error, locate the corrective guidance, execute the corrective action, verify success.
4. Attribute blockers to a surface: API, CLI, SDK, diagnostics, or docs. A blocker is a defect in that surface, not in the user.
5. Record per failure: total TTR, segment breakdown, the evidence label, and the `UNEXPLAINED_ERROR` gate verdict.

## Evidence labels

- **Observed:** executed from a clean or representative environment and timed.
- **CI-observed:** executed in automation; may understate human reading time.
- **Estimated:** reasoned from the error output and docs without execution.

An estimate can indicate risk but never proves the target is met. An unlabeled measurement is UNVERIFIED.

## Auditing TTR

For each of the three most likely failures:

- Score the six-question coverage of the error output. Any missing answer is an `UNEXPLAINED_ERROR` gate failure; estimate the worst-case segment it adds.
- If the corrective action is not present in the error output itself, the "locate guidance" segment is a defect even when it is fast.
- If verification is not possible from the error output, the user cannot know the fix worked; record it as an open segment.
- Check the correlation path: can support reproduce the failing path from the identifier alone? If not, file the finding on the diagnostics surface.
- Attribute each over-target failure to its dominant segment and surface, and name the fix that would close it.

## Reporting

Report a table: failure, surface, six-question score, segment breakdown, TTR versus `TTR_TARGET_MIN`, evidence label, gate verdict. Never average a gate failure away: one `UNEXPLAINED_ERROR` forces the finding, regardless of other scores.
