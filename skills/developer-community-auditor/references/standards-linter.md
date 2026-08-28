# Community Standards Files Linter

## Scope

Eight files define the community contract: LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, SUPPORT.md, GOVERNANCE.md, MAINTAINERS.md, and the contributor ladder. Each file is audited for presence AND quality.

Presence is real: a committed file with actual content, not a stub, a template left with default placeholders, or a redirect to a private document.

## Quality questions per file

- **CONTRIBUTING.md** — does it state how to find work, how to set up, how to run tests, what an acceptable PR is, how review works, how long review takes, who can help, how decisions are made, and how to become more involved?
- **CODE_OF_CONDUCT.md** — does it state a report route and an enforcement commitment?
- **SECURITY.md** — does it state a disclosure route?
- **SUPPORT.md** — does it route questions away from the issue tracker?
- **GOVERNANCE.md** — does it describe actual operation, decision authority, and how outsiders gain responsibility?
- **MAINTAINERS.md** — are named maintainers listed with their areas?
- **Contributor ladder** — does it state responsibilities, privileges, requirements, and promotion and removal per rung, including paths for non-code contributors?

## Procedure

1. List the repo root for the eight files. The ladder may live inside CONTRIBUTING.md or GOVERNANCE.md; record where it actually lives.
2. For each present file, read it and answer its quality questions. Score the file quality as the share of questions answered with substance.
3. A file that exists but answers none of its quality questions scores zero quality. Presence without quality is a finding.
4. Record presence, quality, and the gates the absence triggers.

## Gate mapping

- Welcoming claims with no CONTRIBUTING.md → `NO_CONTRIBUTING_WHILE_WELCOMING`.
- Stage ≥1 with no Code of Conduct → `NO_CODE_OF_CONDUCT`.
- Stage ≥2 with no GOVERNANCE.md and ladder, or governance that describes aspiration rather than operation → `OPAQUE_GOVERNANCE`.

## Output

Record one row per file: presence, quality score, quality-question summary, and findings. Feed presence and quality into the standards-presence dimension of the Community Health Score. Never award full credit for presence alone.
