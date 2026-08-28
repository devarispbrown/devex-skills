# Dev Targets: make dev, devcontainer, and docker compose

## Anatomy of `make dev`

A `Makefile` exposing standard phony targets:

- `install` — toolchain plus dependencies from lockfiles
- `services` — bring up backing services
- `migrate` — apply schema changes
- `seed` — load fixtures
- `dev` — a dependency chain ending in a running dev process with hot reload
- `test`, `lint`, `fmt`, `clean`, `down` — the surrounding loop

`dev` must be a chain of the above, not a script that silently skips failed prerequisites. Declare `.PHONY`, and let the dev process's health signal the "up" state.

**When it wins:** every stack, especially non-containerized local development, plain scripts, and teams that live in the terminal.

## Anatomy of a devcontainer

`devcontainer.json` with:

- a pinned image, never `latest`
- declared `features` (runtime, package manager, docker-in-docker) instead of ad-hoc `postCreateCommand` installs
- a `postCreateCommand` that completes setup: install, migrate, seed — then hands control to the dev command
- `forwardPorts` matching the app's real default ports, with `portsAttributes` labels
- `containerEnv`/`remoteEnv` for container-only defaults

**When it wins:** heterogeneous host machines, Windows/WSL, teams needing a byte-identical toolchain, and contributors who should not install anything on their host.

## Anatomy of `docker compose up`

A compose file where:

- every service declares a `healthcheck`
- the app service mounts source (`.:/app`) for hot reload
- `depends_on` uses the healthy condition, not just start order
- the app service waits on healthy dependencies before starting
- profiles keep optional services out of the default `up`

**When it wins:** multi-service backends, production-parity local stacks, and teams already containerized. It is a service target — pair it with a dev process for hot reload rather than a rebuild per edit.

## Choosing: decision tree

- Do teams run varied host OSes or struggle with toolchains? **devcontainer**.
- Is the app a web service with two or more backing services? **compose** for services; keep the app process on the host, or in a compose app service with volume mounts.
- Is the stack simple, scriptable, and host-friendly? **make dev**.
- Mixing: a devcontainer that shells out to compose is a legitimate, common pattern; the reverse — compose doing full toolchain setup — is a smell.

## Standard target names

Keep the names developers already expect: `dev`, `install`, `setup`, `services`, `migrate`, `seed`, `test`, `lint`, `fmt`, `clean`, `down`, `doctor`. New names must be documented; aliases are optional, missing standard targets are not.

## Hot reload

- Node: `node --watch`, `tsx watch`, `nodemon`, framework watchers
- Python: `--reload` (uvicorn), watchfiles, framework auto-reload
- Go/Rust: `air`, `cargo-watch`, rebuild-on-change scripts
- Containers: bind-mount source so the watcher in the container sees host edits

Verify: edit a file, confirm the app reflects it, and confirm the reload is logged, not silent.

## Graceful degradation

- When a dependency is missing or a port is taken, print the cause and the recovery, then exit non-zero — never start half-way and hang.
- Provide `doctor`/`check` targets that verify prerequisites before `dev`.
- When hot reload is impossible, `dev` must still start cleanly, and the documented restart cycle becomes part of the setup time.
