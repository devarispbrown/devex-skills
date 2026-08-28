# Agent-Native Readiness Report: <product name>

- **Audit date:** <YYYY-MM-DD>
- **Repository:** <path or revision>
- **Audit method:** <inventory scan / simulated agent tasks / both>
- **Audit owner:** <person or team>

## Readiness checklist

Run `scripts/check_agent_readiness.py` on the repository root and paste the summary here.

| Surface | Status | Evidence |
|---|---|---|
| Agent entry file (AGENTS.md/CLAUDE.md) | <present / missing / stale> | <path, Observed/CI-observed/Estimated> |
| Machine-readable schema (OpenAPI/JSON Schema) | <present / missing / drifting> | <path and mismatch details> |
| Structured CLI output (`--json`) | <documented / missing> | <doc or help file> |
| Stable error codes / exit-code docs | <documented / missing> | <doc or help file> |
| Automation safety (deterministic, idempotent, non-interactive) | <verified / violation> | <commands checked> |
| Test discoverability | <runnable / missing> | <test command and result> |
| State inspectability (status/describe/--dry-run) | <present / missing> | <commands found> |

## Per-surface findings

### <surface> — <finding id, e.g. F1>

- **Severity:** <P0 / P1 / P2 / P3>
- **Finding:** <what is wrong>
- **Agent failure caused:** <how an agent fails or misbehaves today>
- **Surface:** <entry file / schema / CLI / error model / script / tests / structure>
- **Evidence:** <Observed / CI-observed / Estimated plus detail>

### <surface> — <finding id>

- **Severity:** <P0 / P1 / P2 / P3>
- **Finding:** <what is wrong>
- **Agent failure caused:** <how an agent fails or misbehaves today>
- **Surface:** <entry file / schema / CLI / error model / script / tests / structure>
- **Evidence:** <Observed / CI-observed / Estimated plus detail>

## Prioritized improvements

1. **<improvement>** — <surface>, <severity>
   - Change: <exact product change>
   - Effort: <small / medium / large>
   - Verify: <agent-visible verification step>
2. **<improvement>** — <surface>, <severity>
   - Change: <exact product change>
   - Effort: <small / medium / large>
   - Verify: <agent-visible verification step>

## Definition of done for this report

- every audited surface has a status and evidence
- every finding names the agent failure it causes
- every improvement is a product change with a verification step
- no finding hides behind a score or an estimate
