# LSP and Debug Adapter Wiring

## Procedure

Wire language servers and debug adapters in this order; verify each step before moving on.

1. Identify the language server for each language in the repository. Prefer the community-standard server per language: Python → pyright/Pylance, TypeScript/JavaScript → the bundled TypeScript server, Rust → rust-analyzer, Go → gopls, Java → Eclipse JDT LS, C/C++ → clangd, Ruby → solargraph, PHP → intelephense, Kotlin → the Kotlin language server.
2. Install the server through the extension or a pinned package; record it in `extensions.json` or the setup docs.
3. Wire the server in settings: server arguments, extra paths, formatting preferences. Give the server the same project config the build uses; a server that cannot parse the project config is not wired.
4. Verify four capabilities on representative symbols: diagnostics on save, hover, go-to-definition, find-references, and rename. All four must work; hover alone is not wiring.
5. Identify the debug adapter for each launch.json `type`: node → js-debug (bundled), python → debugpy, go → delve (dlv), java → Java debug server, C/C++ → cppdbg/lldb.
6. Write or repair the launch.json configuration against `references/vs-code-setup.md`.
7. Verify the debug flow end to end: start the configuration, hit a breakpoint, inspect variables, walk the stack, step, resume.
8. Commit the configuration and document the one-time install steps.

## Launch vs attach

- **launch**: the IDE starts the process with the debugger attached. Use for the canonical app entrypoint.
- **attach**: the IDE connects to a process started by other tooling (compose, remote, test runner). Configure `port`, `address`, and restart behavior; verify the process actually listens before blaming the IDE.

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| No diagnostics | Server not started or not installed | Install/start the server; check the language server output channel |
| Hover works, navigation does not | Partial capability or wrong server | Confirm the standard server for the language, not a proxy |
| Breakpoints never hit | Mismatched source maps or wrong request flow | Set `outFiles`/`sourceMaps`; use `launch` for the entrypoint |
| Attach times out | Port wrong or process not listening | Confirm the port and `attach` vs `launch` semantics |
| Server ignores project config | Config path or args mismatch | Point the server at the same config the build reads |

Never accept "the extension is installed" as proof of wiring. Verify capabilities, then commit.
