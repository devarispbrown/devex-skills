# Build and CI Security

The build pipeline is an attack surface with privileged access: it holds secrets and writes release artifacts. Harden it as infrastructure, not as glue.

## Pin actions to full SHAs

**Procedure for every third-party action in every workflow:**

1. Replace `owner/repo@vX` refs with the full 40-character commit SHA of the tag you reviewed. `actions/checkout@v4` is a moving target; a SHA is not.
2. Record the tag next to the SHA in a comment so the pin stays readable: `uses: actions/upload-artifact@65a4ed1... # v4.3.0`.
3. Pin only after reading what the action does and who maintains it. An unknown action with access to your secrets is a P0 risk; prefer well-known, widely used actions.
4. Pin container actions by digest instead of a mutable tag.
5. Review action bumps like code changes: diff the SHA you use against the new tag before updating the pin.

Verify: `uses:` lines outside a `./` local path reference a full SHA or a digest. The scanner flags everything else.

## Keep untrusted input out of run blocks

1. Never interpolate pull request context into `run:` commands: titles, branch names, comments, and labels are attacker-controlled strings.
2. Do not pipe PR-authored scripts into the shell, even after "sanity checks". Write to a file and execute only after validation with a clean exit path.
3. If a run block must use an expression, expand it into `env:` and reference the variable, never `${{ ... }}` inline.
4. Never `git checkout` an untrusted ref and then execute its content in a workflow that holds write credentials.

Verify: `${{ secrets.` never appears inside a `run:` block. The scanner flags inline and block usage.

## Scope secrets to the job that needs them

1. Reference a secret only in the job that uses it, and only in `env:` mappings on the step that needs it.
2. Prefer environment-level secrets scoped to the branch or environment that is allowed to consume them. A production deploy token must not be readable by pull request runs.
3. Do not echo secrets, log them, or write them to files that are uploaded as artifacts.
4. Use `GITHUB_TOKEN` with the narrowest permission block; do not mint repository tokens for one-off jobs.

Verify: each secret has exactly one class of consumer, and that consumer is the only job with access.

## Protect PRs from forks

1. Treat `pull_request_target` as a vulnerability trigger unless mitigated: untrusted PR code runs with the base-branch token. If it cannot be avoided, check out only immutable refs, run only trusted steps, and use a dedicated minimal token.
2. Prefer `pull_request` semantics for untrusted contributions; run trusted steps on merge or on a dedicated branch.
3. Ensure fork PRs cannot read secrets or write to the repository. Confirm the "require approval for fork workflows" setting.

Verify: no workflow runs PR-authored code with base-branch credentials. The scanner flags every `pull_request_target` trigger for manual review.

## Wire SAST into CI

1. Add a SAST job on every push and pull request, including dependency and container scanning where the stack supports it.
2. Block merge on P0/P1 findings; report P2/P3 as annotations or comments, never silently.
3. Treat scanner silence as unverified, not clean: confirm the scanner actually ran and covered the changed paths.
4. Keep scanner configuration in the repository so findings are reproducible.

Verify: a fresh clone can reproduce every CI scan locally or in CI, and the failure policy matches the severity policy.
