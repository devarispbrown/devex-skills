# Dependencies and Toolchain

## Version managers

Pin the runtime and toolchain in committed files, one per ecosystem:

- Node: `.nvmrc` (add `.node-version` when non-nvm users matter)
- Python: `.python-version`
- multi-runtime: `.tool-versions` (asdf), `.mise.toml` (mise)
- per-ecosystem: `rust-toolchain.toml`, the `go` directive in `go.mod`, `.ruby-version`, `.java-version`

Commit the pin file. Do not rely on a team chat message, a laptop's default version, or a step owner's memory.

## Lockfiles

Commit lockfiles for every package manager in use: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `uv.lock`, `poetry.lock`, `Pipfile.lock`, `go.sum`, `Cargo.lock`, `Gemfile.lock`, `composer.lock`.

- Install from the lockfile in the dev target and in CI (`npm ci`, `pnpm install --frozen-lockfile`, `uv sync --locked`).
- Do not commit a lockfile that was never validated by a clean install, and do not delete one to "fix" a resolution problem.

## Pinning vs floating: decision tree

- Is the artifact a library with a public API? **Float** within declared ranges; pin only tooling versions.
- Is the artifact an application or service? **Pin** runtime, toolchain, and dependencies.
- Do downstream consumers install your dependencies directly? **Float** ranges; publish a lockfile only if you consume it.
- Do developers on different machines resolve different versions today? **Pin** — the drift is the defect.
- Does CI resolve different versions than local installs? **Pin** — parity failure that breaks the clean clone is a `NON_REPRODUCIBLE_BUILD` signal.

When in doubt, pin. Floating saves maintenance; pinning buys reproducibility, and reproducibility is the gate.

## Runtime mismatch detection

Before the dev target runs, verify the active runtime against the pin:

- run `nvm use`, `mise install`, or the pinned interpreter as part of setup
- check `package.json` `engines`, `pyproject.toml` `requires-python`, and `rust-toolchain.toml` against the resolved runtime
- fail fast with the expected and actual versions; do not proceed on a mismatched runtime with a warning

## Monorepos and workspaces

- Use the package manager's native layout (`pnpm` workspaces, npm/yarn `workspaces`, `uv` workspaces, Cargo workspaces).
- Declare one canonical setup entry point at the workspace root; per-package setup lives in package metadata, not in per-developer notes.
- Install once at the root, not per directory. A setup that requires visiting N package directories by hand is N manual steps.
- CI and the dev target must use the same workspace install command; divergence is drift.
