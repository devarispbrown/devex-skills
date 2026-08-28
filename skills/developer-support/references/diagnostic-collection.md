# Diagnostic Collection Contract

## Fields

Every entry point collects the full diagnostic set. Nothing is optional at the ticket rung.

| Field | Meaning | Supplied by |
|---|---|---|
| Version | Product version | Automation |
| SDK version | SDK/client version | Automation |
| Request ID | Request identifier | Automation |
| Trace ID | Trace identifier | Automation |
| Environment | OS, runtime, region, deployment | Automation / form |
| Config | Non-secret configuration | Automation / form |
| Sanitized logs | Relevant log excerpt | Automation / form |

## Collection points

- **Error output:** errors and CLI diagnostics echo request ID and trace ID on the failure path, so the developer can copy them without opening the form.
- **Issue forms:** the seven fields are required fields; forms prefill what automation can supply.
- **Support intake:** pasted diagnostics are parsed and prefilled into the ticket.
- **Ticket gate:** a ticket missing request ID or trace ID is returned with instructions, never routed onward.

## Sanitization rules

- Secrets, tokens, credentials, and PII are redacted by policy, never by convention.
- Logs are truncated to the relevant time window and the relevant component.
- Config excludes values that are secrets; the form states this.
- Sanitization is verified on a sample before the design ships.

## Automation rule

The product supplies every field it can produce without asking. A form that asks the developer to retype the version, request ID, or trace ID that the error output already shows is a defect in the collection design.

## Evidence completeness gate

A request is routable only when its diagnostic set is complete. Incomplete requests return to the developer with a checklist naming the missing fields. This gate applies at every promotion: a promotion without evidence is a re-routing, not an escalation.

## Verification

Walk one failure end to end: error → request ID and trace ID in the error output → form prefilled or required → ticket complete → escalation carries the set. Any hop that drops a field fails the collection contract.
