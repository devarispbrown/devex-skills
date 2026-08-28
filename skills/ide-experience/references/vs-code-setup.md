# VS Code Workspace Setup

## settings.json design

Workspace settings are project truth; user settings are machine truth. Keep the split clean:

- workspace settings.json: formatter, linter, language defaults, file associations, task defaults
- user settings: theme, keybindings, telemetry, editor chrome

Rules:

- commit only settings that change project behavior
- never commit secrets, tokens, or machine-specific paths
- prefer explicit language scoping over global fallbacks, one default formatter per language:

```json
"[typescript]": { "editor.defaultFormatter": "biome" }
```

- set `editor.formatOnSave` only with the formatter conflict resolved; set `editor.codeActionsOnSave` for lint fixes and organize imports
- keep diff hygiene explicit: `files.eol`, `files.insertFinalNewline`, `files.trimTrailingWhitespace`, `editor.rulers`
- exclude generated output from search and watching: `files.exclude`, `search.exclude`, `files.watcherExclude` for dist, build, coverage
- set `terminal.integrated.defaultProfile` per platform only when the project needs a specific shell
- add performance settings (`typescript.tsserver.maxTsServerMemory`, `search.followSymlinks`) only when measured need exists

## extensions.json

Declare the extension surface in `.vscode/extensions.json`:

- `recommendations`: extensions the repo actually needs (language servers, debug adapters, formatters, linters, schema tooling)
- `unwantedRecommendations`: extensions that conflict (multiple formatters, competing language servers)

Rules:

- every recommended extension must have a job; nothing is recommended for goodwill
- pin versions with `identifier@1.2.3` when a language server's behavior gates the workflow
- prefer extensions that bundle or declare their own language server over heavyweight suites

## launch.json design

Debug configurations live in `.vscode/launch.json`. Design rules:

- one configuration per canonical run flow; the first entry is the default
- every configuration has `name`, `type`, and `request` (`launch` or `attach`)
- `launch`: the IDE starts the process with the debugger attached; use for the app entrypoint
- `attach`: the IDE connects to an already-running process; configure `port`, `address`, and restart behavior
- use `preLaunchTask` to run setup (build, dev server) before launch; the task must exist in tasks.json
- use `${workspaceFolder}` for paths; never commit absolute or machine-specific paths
- set `env` explicitly; never read secrets from the workspace
- for transpiled languages, set source maps (`outFiles`, `sourceMaps`) and verify breakpoints hit the source
- compound configurations (`"compounds"`) group multiple debug sessions for multi-process flows
- remove configurations that no longer run; stale configs are worse than none

## Verification

- open a clean checkout and confirm zero red squiggles after install
- confirm format-on-save produces no diff against committed formatting
- confirm each launch.json configuration actually launches and stops at a breakpoint
- confirm tasks in tasks.json match declared Makefile targets or package.json scripts; run `scripts/check_ide_config.py` to detect drift
