# Guidance Files Audit Procedure

## CONTRIBUTING.md

Verify the file exists at the repository root, `.github/`, or `docs/`, and is current with the repository's actual workflow.

Check, in order:

1. environment setup and the commands to build and test
2. how to find an issue to work on, including the good-first-issue label
3. how to make, verify, and submit a change
4. what CI runs and what the PR must contain
5. review expectations: who reviews, how long, how disagreements are handled
6. DCO/CLA requirements and how to satisfy them

Test each command in the file from a clean clone. A command that fails, a version that does not exist, or a step that assumes a maintainer's machine is a P1 defect. An out-of-order, incomplete, or boilerplate-only CONTRIBUTING.md is a P1 defect: the file is the funnel's front door.

## CODEOWNERS

Check the root, `.github/`, and `docs/` for a CODEOWNERS file.

Verify:

- every meaningful change path has at least one owner
- owners are real, active accounts, not abandoned aliases
- a fallback `*` owner exists when paths are uncovered
- the file matches the current branching and review policy

An outdated CODEOWNERS routes reviews into a void: a P2 defect when reviews stall, P1 when it blocks merges with no one to approve.

## Issue templates

Check `.github/ISSUE_TEMPLATE/`, `.gitlab/issue_templates/`, `docs/`, and root `ISSUE_TEMPLATE.md`.

Verify:

- a bug template exists and requires reproduction steps, expected behavior, and environment
- a feature template exists and requires the problem statement, not a prescribed solution
- templates match the fields maintainers actually ask for in review

A bug template without reproduction steps is a P2 defect; it produces issues the contributor cannot pick up.

## PR template

Check `.github/pull_request_template.md`, root `PULL_REQUEST_TEMPLATE.md`, and `docs/`.

Verify the template elicits:

- a summary of the change and why
- test evidence: what was run and that it passed
- a checklist for tests, docs, and changelog

A missing PR template is a P2 defect. A template that demands internal context a first-time contributor cannot know is a P1 defect.

## Good-first-issue labeling

Verify the labeling procedure is documented in CONTRIBUTING.md or the README.

Check the labeled issues themselves:

- each is small: a bounded change, no architectural prerequisites
- each has a clear acceptance criterion and any relevant fixture
- none is stale (open without activity past the project's own freshness bar) or already claimed
- none requires internal knowledge to start

Scan for "good first issue" or "good-first-issue" mentions in CONTRIBUTING, README, templates, and CI workflows. A labeler workflow that auto-labels is a strong signal; a label with no usable issues is noise and a P2 defect.

## DCO/CLA evaluation

Determine which agreement the project uses, from CONTRIBUTING, LICENSE, or the PR bot:

- **DCO**: every commit must carry a `Signed-off-by` trailer. Verify the DCO bot is enabled on the branch and that CONTRIBUTING explains the one-line sign-off command.
- **CLA**: an individual/entity agreement exists. Verify the agreement is linked from CONTRIBUTING, the signing flow works without sales contact, and the CLA bot blocks or flags unsigned PRs.
- **None**: record it; the absence is a legal decision, not a defect, unless the project's license implies an agreement.

An unexplained bot block on an unsigned commit or PR is a P1 defect with an `UNEXPLAINED_ERROR` gate failure. The DCO/CLA requirement must be stated and enforceable by automation, never by memory.
