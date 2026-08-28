# Signal Sources and Collection

## Source inventory

Collect from every agreed source. Each source contributes signals with different evidence strength:

| Source | Signals | Evidence strength |
|---|---|---|
| GitHub issues | failure reports, reproductions, feature requests | Observed |
| GitHub discussions | questions, workarounds, confusion | Observed |
| Support chat archives | live friction, escalations | Observed |
| Docs search logs | what developers look for and miss | CI-observed |
| CLI telemetry | command sequences, exit codes, durations | CI-observed |
| API error logs | status codes, error bodies, endpoints | CI-observed |
| Install/onboarding failure logs | failed setup steps, retries | CI-observed |
| SDK exception reports | stack traces, language, version | CI-observed |
| Product analytics | funnel drop-off, feature usage, sessions | CI-observed |

## Collection procedure

1. Agree the source list and the collection window before collecting. State both in the report.
2. Pull each source in bulk. Do not hand-pick signals you already know about.
3. For each signal record: source, timestamp, raw text or fingerprint, journey stage if known, surface, evidence label.
4. Label evidence strength per source: Observed from a human report, CI-observed from telemetry, Estimated from reasoning.
5. Record gaps: sources that could not be exported, windows that are incomplete, access that was denied.

## Privacy rules

Redact before analysis, never after:

- no personal emails, names, or handles in the working set
- no auth tokens, API keys, or secrets in any form
- no IP addresses or host identifiers
- no identifiers that single out one organization or one machine
- scrub snippets, not just headers: stack traces can embed file paths, URLs can embed user IDs

Aggregation rules:

- report counts and percentages only above the aggregation threshold
- below the threshold, merge the signals into a broader cluster or suppress them; never report a category whose count could identify an individual
- treat the redacted working set as temporary; do not persist it beyond the analysis

## Completeness

Do not report "no signal" as "no problem." Absence of issues in one source is evidence about that source only. When a source is missing, say so under gaps.
