# Task Runners

## Single source of truth

Makefile and package.json declare commands. tasks.json, run configurations, devcontainer post-create hooks, and CI reference those commands. Never duplicate long command strings: a task that strings together flags belongs in the Makefile or package.json script, and the IDE task becomes a one-line reference.

Rules:

- `make dev` or `npm run dev` is the canonical one-command dev loop
- task names mirror script names: dev, build, test, lint, format
- a tasks.json `command` must match a declared script or target, or the checker flags it stale
- when a task and a script drift, fix the task or delete it; never document the drift
- npm tasks use `"type": "npm"` with `"script"`; shell tasks use `"type": "shell"` with `"command"`
- full commands are comparable: `npm run build` matches a `build` script; `make build` matches a `build` target

## One-command task design

1. the canonical task starts the full dev loop (deps, build, serve, watch) with one command
2. `"group": {"kind": "build", "isDefault": true}` makes it the default build task for Cmd/Ctrl+Shift+B
3. `preLaunchTask` chains setup before a debug launch; the referenced task must exist in tasks.json
4. the task uses problem matchers so errors surface in the Problems panel, not only in terminal output
5. the same command appears in the README quickstart; the IDE and the docs agree

## Sync and staleness

Run `scripts/check_ide_config.py` to detect stale task commands. A task command that matches no package.json script and no Makefile target is stale; fix it or delete it. The checker also validates launch.json and tasks.json structure: JSON validity and required fields.

When a script is renamed or removed, update every referencing surface in the same change:

- tasks.json tasks
- JetBrains run configurations
- devcontainer `postCreateCommand`
- CI pipeline
- README quickstart

## Multi-tool parity

- devcontainer `postCreateCommand` uses the same canonical command the README documents
- JetBrains run configuration script name matches the package.json script
- CI runs the same test command the IDE task runs
- `make dev` / `npm run dev` is the one thing every surface references; when it breaks, every surface breaks loudly and the fix is one line
