# Canonical Terminology

One vocabulary for the suite. Existing skills keep legacy inline lists only as pointers to this file.

## Journey stages

The developer journey is 14 canonical stages. Audits may scope to a subset; unscoped audits walk all 14.

| Stage | Definition | Stop condition |
|---|---|---|
| find | locate the product and understand its claim | can state what the product does and whether it fits |
| understand | grasp concepts and architecture | can explain core concepts without guessing |
| install | get the software running | product installed or sandbox available |
| auth | authenticate or provision an account | authenticated, credential usable |
| configure | set up required configuration | configuration accepted, no unknowns |
| execute | run the core workflow | core workflow completed |
| verify | confirm the result | end-to-end outcome verified |
| modify | make a change to something owned | change applied |
| break | intentionally break something | failure reproduced on demand |
| diagnose | find the cause | root cause identified |
| recover | fix or work around the failure | state restored, workflow resumed |
| test | run the test suite meaningfully | tests green, coverage understood |
| deploy | ship to a target environment | deployment verified |
| upgrade | move to a newer version | upgrade completed, behavior intact |

**Legacy aliases** (superseded, not parallel): the 13-stage list in `developer-docs` (Discover → Prerequisites → Install → Account/Auth → Configure → First value → Verify → Customize → Debug → Production → Operate → Upgrade → Get help) and the 7-stage list in `docs-architecture.md` are subsets of these 14. All stages they name exist above.

## Problem classification

Nine classes, attributed by root cause, never by which team writes the fix:

| Class | Attribution rule |
|---|---|
| Product | core product behavior or workflow design is the root cause |
| API | HTTP/RPC surface design: resources, naming, semantics |
| CLI | command surface: hierarchy, flags, output, exit codes |
| SDK | language wrapper design or parity gaps |
| Configuration | config surface, defaults, precedence, secrets handling |
| Environment | toolchains, versions, ports, OS/arch issues |
| Documentation | docs alone can fix it |
| Infrastructure | provisioning/build/runtime latency or reliability |
| Third-party | external approval, quota, API, network, service |

**Legacy mapping**: the docs-auditor's four classes map directly — Docs → Documentation; Product/DX → Product, API, CLI, SDK, or Configuration (pick by root cause); Infrastructure → Infrastructure; External dependency → Third-party.

Documentation must not absorb blame for product defects.

## Canonical terms

- **magic path**: the canonical getting-started route delivering verified end-to-end value.
- **quickstart**: the artifact documenting the magic path.
- **zero-to-value**: the find→verify span of the journey.
- **Time to Recovery (TTR)**: time from hitting an expected error to completing its corrective action.
- **DX Report**: the structured output of a developer-experience audit (per-area scores, Overall DX, gates).
- **capability matrix**: per-SDK/language table of implemented capabilities.
- **drift**: divergence between documentation/generated artifacts and current behavior.
- **parity**: semantic equivalence of SDKs (or docs) with the canonical API.
