# Community Automation

Scope: design playbook for automating community logistics in the `developer-community` skill. Complements `recognition-programs.md` (which covers what to recognize) — this file covers what to automate and where the line is. Audit-side automation signals live in the `developer-community-auditor` skill.

## Automate logistics, never appreciation

Rule: bots may move work, surface state, and reduce waiting. They must not substitute for human recognition. A bot can say "Tests failing: integration/postgres"; a maintainer should say "Thanks for working through this. The approach looks good."

## The playbook

1. **Welcome first-time contributors** — first-PR autoresponse pointing at review expectations and the ladder, from the project's own voice.
2. **Route issues to component owners** — CODEOWNERS-based routing so no issue waits on the wrong person.
3. **Detect missing reproduction** — label issues lacking repro steps and prompt the author.
4. **Suggest related issues** — duplicate detection before a maintainer re-explains a known problem.
5. **Surface unanswered discussions** — weekly digest of questions with no useful answer, so none expire silently.
6. **Identify stale PRs needing maintainer action** — nudge maintainers when a newcomer PR approaches the `COMMUNITY_UNACKNOWLEDGED_PR_MAX_DAYS` acknowledgment window.
7. **Prompt maintainers after SLO breaches** — when first-response SLOs trip, route to the owner rather than letting the breach age.
8. **Recognize merged first PRs** — mechanical acknowledgment of the milestone (template-driven, not fake warmth).
9. **Nominate reviewer eligibility** — when a contributor meets the ladder's reviewer criteria, flag for human decision.

## Design rules

- Every automation has a kill switch and a mute path for maintainers.
- Automation output is labeled as automated.
- No automation posts on behalf of a human without attribution.
- Each automation maps to a named gate or SLO constant it serves; unowned automation is noise.
