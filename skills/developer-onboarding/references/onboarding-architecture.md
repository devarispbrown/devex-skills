# Onboarding Architecture

The onboarding system view: how the quickstart, docs, samples, templates, and support fit together, who owns each piece, and how the system improves itself.

## System view

One canonical path flows through five connected surfaces:

```
quickstart → docs → samples → templates → support
```

- **quickstart**: the canonical magic path; one route, verified end-to-end value within `MAGIC_PATH_MAX_MIN`
- **docs**: the reference, how-to, and explanation surfaces the quickstart links to after first success
- **samples**: working example projects the developer can run and modify
- **templates**: scaffold commands that produce a working project
- **support**: the failure channel; a recoverable path, not a dead end

Each surface has one job and one owner. The quickstart routes to the next surface at the moment the developer needs it — after success, not before.

## Owner per step

Every step in the onboarding plan has a named owner, chosen from the four owner classes:

- **Docs**: prose, examples, commands, links — the docs team can fix
- **Product/DX**: product behavior, defaults, flags, error messages — the product team must change
- **Infrastructure**: provisioning, sandboxes, accounts, tokens — the platform team must build
- **External dependency**: a third-party service, registry, or approval — the product cannot remove alone

Owner types keep the plan honest: a step owned by Product/DX is a product change request, not a documentation task. Never assign a step to Docs because the product is inconvenient.

## Telemetry feeds redesign

The onboarding system is a feedback loop, not a static document:

1. Ship the magic path with the sandbox route and starter credentials instrumented.
2. Collect: steps attempted, steps dropped, time between steps, errors, and where developers stall.
3. Compare against the plan's segment estimates; a segment that runs hot is a candidate for elimination.
4. Feed the finding back into step elimination and the product backlog.
5. Re-time after each change; label the evidence Observed or CI-observed.

A quickstart that is never measured is a guess. The plan's `Estimated` timings become real data once the path ships and the auditor or telemetry measures them.

## The first-contribution path

Beyond zero-to-value, design the fork-to-merge contributor path: clone, build, run tests, make a PR-ready change. Target `FIRST_CONTRIBUTION_TARGET_MIN` from first fork to PR-ready change. It is a target, not a hard gate: reaching it in 30–60 minutes is a PASS WITH DEBT signal, and over an hour is a P2 defect.

The contributor path reuses the onboarding surfaces: the magic path proves the product works, the local dev contract gets a clean clone to a productive state, and the contributor template removes scaffold decisions. A product with a great zero-to-value path and a broken contributor path converts users but loses contributors — design both.
