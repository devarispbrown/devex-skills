# Repository Security

Repository security is the governance surface: how the project receives reports, who owns what, and what the hosting platform enforces before anything reaches main.

## SECURITY.md procedure

**Audit the file** at the repository root, not just its presence:

1. Confirm a reporting channel exists and is reachable: a security email, a private form, or a private vulnerability advisory. Do not accept a placeholder with no channel.
2. Confirm the file states what to include in a report (version, package, impact, reproduction).
3. Confirm it states a response and disclosure timeline, and which supported versions receive fixes.
4. Confirm it names how patches are released and announced.
5. Confirm the channel is monitored: check that the mail alias or advisory notification is wired to an actual inbox. A dead channel is a P1 finding.

Verify: every public-facing project has a SECURITY.md whose channel a reporter could actually use.

## CODEOWNERS procedure

1. Check for `CODEOWNERS` in `.github/`, `docs/`, or the root. Absence is a finding: there is no owner map for required reviews.
2. Confirm coverage includes release and CI paths, not just `src/`. Unreviewed release automation is a P1 finding.
3. Confirm each glob maps to a team or user that exists and has write access. Dead owners are a P2 finding.
4. Pair CODEOWNERS with branch protection that requires reviews from owners; the file alone enforces nothing.

## Branch protection procedure

Branch protection lives in hosting settings, not in the tree. Verify in the platform UI or API:

- the default branch requires pull request reviews
- review requires status checks to pass before merge
- signed commits are required or enforced by policy
- direct pushes to the default branch and protected tags are blocked
- force-push is disabled on the default branch

Verify: record each item as pass, fail, or unverified with an Observed or CI-observed evidence label. Never report branch protection as present without checking the platform.

## Workflow permissions procedure

1. Set workflow-level `permissions:` to the minimum set the job needs. A job that only builds and tests needs `contents: read`, not write.
2. Use `permissions: read-all` or an explicit block per job; never rely on the default token scope.
3. Scope secrets to the job or step that uses them. Do not give a lint job the deploy token.
4. Pin third-party actions to full commit SHAs (see build-and-ci-security). An unpinned action is a P1 finding.

## Review requirements

- Require at least one review on every pull request, from a CODEOWNER on owned paths.
- Never let a contributor approve their own change.
- Treat the merge of the release tag and the publication of artifacts as reviewed, signed-off steps, not casual actions.

Verify: the review policy is enforced by the platform, not by convention.
