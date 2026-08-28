# Scaffolder Design: `<workflow name>`

Status: `<proposed | in progress | shipped | deprecated>`
Owner: `<team or individual>`
Date: `<YYYY-MM-DD>`

## 1. Candidate analysis

- Workflow name: `<workflow name>`
- Kind: `<kind>`
- Instances in the last 90 days: `<number>`
- Signal sources: `<PR archaeology | onboarding friction | support questions — list which and what they showed>`
- Error-prone steps: `<list the steps that go wrong, and how>`
- Decision: `<generator | document>`
- Rationale: `<frequency, defect rate, drift cost; cite thresholds by name>`

## 2. Generator contract

- Command: `<product> generate <kind> <name>`
- Inputs: `<name, options, environment variables — each with type and default>`
- Non-interactive behavior: `<defaults and flags for every prompt; behavior when input is missing>`
- Idempotency: `<re-run behavior on a fresh tree and on an edited tree>`
- Re-run safety: `<marker format; --force behavior>`
- Exit codes: `<0 success, 1 input error, 2 conflicting existing tree>`

## 3. Template list

| Template file | Output path | Placeholders | Fixture |
| --- | --- | --- | --- |
| `<templates/<kind>/config.py.tmpl>` | `<name>/config.py>` | `<host, port, env_prefix>` | `<fixture path>` |
| `<templates/<kind>/tests/test_config.py.tmpl>` | `<name>/tests/test_config.py>` | `<env_prefix, port>` | `<fixture path>` |

## 4. Output tree spec

```
<output root>/
  <name>/
    <file>   <- generated, marked
    <file>   <- generated, marked
    <file>   <- never touched
```

## 5. Output wiring

- CI: `<validation job; drift job>`
- Docs: `<docs index entry; quickstart link>`
- Metadata: `<registry entry; provenance marker>`
- Ownership: `<owner team for generated projects; owner for the generator>`

## 6. Maintenance

- Generator version: `<x.y.z>`
- Drift detection: `<job or procedure>`
- Deprecation plan: `<replacement kind; timeline>`
