# Community Tooling

Scope: tool selection guidance for the `developer-community` skill when designing or operating community systems. Complements `community-operations.md` (procedures) — this file answers "which tool stack".

## The matrix

| Need | Tool |
|---|---|
| Repo-level operating surface | **GitHub** — issues, issue forms, PR templates, Discussions, community profile, CODEOWNERS, labels, Projects, Actions |
| OSS-native metric definitions | **CHAOSS** — Time to First Response, Change Request Acceptance Ratio, New Contributors, Contributor Retention, Bus Factor, Elephant Factor; cite metric names verbatim, never paraphrase |
| Self-hosted analytics backend | **GrimoireLab** — the default OSS analytics implementation; ingests GitHub/GitLab/Discourse/Slack/mailing lists and computes core/regular/casual contributor models and attraction/retention |
| Managed OSS analytics | **Bitergia** — managed version of the same approach when operating your own stack is not worth it |
| Developer community + GTM | **Common Room** — community health and activity reporting combined with product usage and CRM signals |

## Rules

- Build skill guidance around CHAOSS definitions regardless of backend; the backend only supplies data.
- GitHub is the operating surface: automations and templates live in-repo, so contribution mechanics are versioned like code.
- Choose GrimoireLab when the project is OSS-first and self-hostable infrastructure is acceptable; choose Bitergia when not; choose Common Room only when GTM layering is the actual goal.
- Never invent metric names: a metric either exists in CHAOSS (cite it) or is defined in `dx-standards/community.md` (cite the constant).
