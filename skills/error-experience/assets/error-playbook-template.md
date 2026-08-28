# <ERROR_CODE> — <ONE_LINE_SUMMARY>

Severity: <P0 | P1 | P2 | P3 | P4>
Retry policy: <SAFE | SAFE_WITH_BACKOFF | NEVER>
Surface: <API | CLI | SDK | DIAGNOSTICS>

## What happened

<PLACEHOLDER: one plain sentence stating the failure the user observes.>

## Why

<PLACEHOLDER: the proximate cause in user terms. Distinguish user-caused from system-caused.>

## Where

- Operation: <PLACEHOLDER>
- Resource/field: <PLACEHOLDER: path or identifier syntax>
- Emitting code: <PLACEHOLDER: file and symbol>

## How to fix it

<PLACEHOLDER: numbered corrective steps. For CLIs use complete commands, e.g. "Run: <command>".>

## Retry safety

<PLACEHOLDER: is retry safe? With what backoff? What happens on duplicate submission? When must the user never retry?>

## Correlation

- Identifier location: <PLACEHOLDER: header, field, or log key>
- Log pattern: <PLACEHOLDER: grep-able query>
- Trace span: <PLACEHOLDER: span name or attribute>
- Example identifier: <PLACEHOLDER: realistic example value>

## Example

<PLACEHOLDER: the error exactly as the user or caller sees it, including the identifier.>

## Related

- Documentation: <PLACEHOLDER: URL or path>
- Support workflow: <PLACEHOLDER: ticket type or escalation path>
- Tests: <PLACEHOLDER: test names asserting this error>
