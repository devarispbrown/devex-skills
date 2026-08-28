# Community Q&A Analysis

Scope: audit procedure for community questions. Complements the quantitative Q&A dimension in `check_community_health.py` and the useful-answer measurement in `responsiveness-monitor.md`; this file covers what to measure beyond the score and what to do with repeated questions.

## Measure

- **Question volume** — questions per trailing 30 days, by channel.
- **Answer rate** — questions receiving at least one response.
- **Useful-answer rate** — questions receiving a useful answer (definition in the canonical standards).
- **Accepted-answer rate** — where the platform supports accepted answers.
- **Unanswered questions** — list them; each is a routing or documentation signal.
- **`community_answer_share`** — useful answers from non-maintainers divided by total useful answers. Rising share means a self-sustaining community; falling share means maintainers are the bottleneck.

## Repeated-question loop

Cluster repeated questions by topic. For each cluster with substance:

1. Record the question phrasing and count.
2. Determine the intended answer (from maintainers or resolved threads).
3. Hand off to `developer-docs` if available: this is a documentation gap — a how-to or troubleshooting page should exist at the searchable path the asker tried.
4. If the answer is complicated because the product surface is complicated, escalate the finding to the relevant surface skill by name (`api-design-reviewer`, `configuration-dx`, `error-experience`) — do not document around a product defect.

Verify: after the docs change, the same question should be answerable by search within the documented magic path's link neighborhood.
