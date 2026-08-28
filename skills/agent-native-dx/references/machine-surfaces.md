# Machine-Readable Surfaces

Machine-readable surfaces are the agent's senses. Each is an affordance with a job and a pay-off condition.

## OpenAPI

The canonical contract for HTTP APIs: endpoints, parameters, request/response shapes, errors, auth.

- **Agent affordance:** agents read it to build correct calls without trial and error; tooling generates clients and tests from it.
- **Pay-off:** any public HTTP API that agents or other tools call.
- **Verify:** every public endpoint is present, request/response shapes match implementation, and error responses are described.

## JSON Schema

The canonical contract for configuration and structured inputs/outputs.

- **Agent affordance:** agents validate generated config before using it and learn required fields without probing.
- **Pay-off:** config files, CLI input formats, event payloads — anything validated or consumed programmatically.
- **Verify:** a schema exists for every validated surface, validation uses the schema, and the schema matches accepted input.

## Structured CLI output

A `--json` (or equivalent) output mode for operations agents automate.

- **Agent affordance:** agents read state and results without fragile text parsing.
- **Pay-off:** any CLI command whose output an agent parses, diffs, or asserts on.
- **Verify:** the flag is documented in `--help`, output is valid JSON on success and on error, and the output shape is stable across releases.

## Stable error codes

Machine-distinguishable identifiers for errors, stable across releases.

- **Agent affordance:** agents branch on the code and route to remediation without parsing prose.
- **Pay-off:** any surface whose failures an agent must branch on: APIs, CLIs, config validation.
- **Verify:** codes are documented with meaning and remediation, codes never change meaning, and human-readable messages remain alongside.

## MCP servers

Agent-native interfaces exposing tools, resources, and prompts.

- **Agent affordance:** agents call typed tools instead of scraping CLIs or web UIs.
- **Pay-off:** when agents should operate on live state or capabilities, not just read the repo — a product control plane, a build service, a data store.
- **Verify:** tool names and descriptions are accurate, arguments match the underlying operation, and failure modes return structured errors.

## Agent Skills

Packaged, loadable instructions for recurring agent work.

- **Agent affordance:** agents load the skill and follow the procedure instead of improvising.
- **Pay-off:** when the product has a repeatable procedure agents should follow exactly — release process, migration steps, incident runbook.
- **Verify:** the skill states when to load it, and its steps stay true against the product they document.

## When each pays off

Do not add a surface because it is fashionable. Add one when an agent-visible workflow needs it:

- agents call the API → OpenAPI
- agents produce config or input → JSON Schema
- agents parse CLI output → structured output plus stable error codes
- agents operate live product state → MCP
- agents must follow a fixed procedure → Agent Skills

A machine surface that no agent workflow consumes is dead weight; a workflow that lacks its surface is a gap. Classify accordingly and recommend the surface, not the prose.
