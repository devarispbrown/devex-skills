# Agent Entry Files (AGENTS.md / CLAUDE.md)

The entry file is the first read for any coding agent. Make it the complete, current, and unambiguous map of how to work in this repository.

## What belongs

1. **Build commands** — the exact commands that reach a working state from a clean checkout, in order, with expected output.
2. **Test commands** — how to run the full suite and a single test, with the exact command and expected result.
3. **Run commands** — how to run the product locally, including required env vars and services.
4. **Verify commands** — a command an agent can run to confirm a change worked.
5. **Invariants** — facts the agent cannot safely infer: constraints, ordering requirements, environment assumptions, supported versions.
6. **Gotchas** — known traps, with the symptom and the workaround.
7. **Architecture pointers** — one or two lines per area linking to deeper docs, never an essay.
8. **Code style and conventions** — what reviewers enforce, so the agent matches before submitting.

## What does not belong

- Marketing copy and value propositions. The agent is already working here.
- Content that duplicates docs. The entry file points to canonical sources; it does not restate them.
- Facts that can drift. Every line must be true today and after the next change, or the line names a check that enforces it.
- Internal jargon without a definition.

## Keeping it current

Treat the entry file as code:

1. Update it in the same change that changes the behavior the file describes.
2. Review it in every PR review pass, the same way a README is reviewed.
3. Verify periodically that every command in the file still works from a clean checkout. A broken entry-file command is a P1 finding.
4. When a fact lives in more than one place, keep the canonical copy in the entry file or point to it — never duplicate.

## Single source

The entry file is the single source for "how an agent works here". If the README or docs also instruct agents, the entry file wins on conflict, and the duplicate is replaced with a pointer.

## Write for execution

Each command must be complete and copy-pasteable:

- repository-root-relative paths, never machine-specific paths
- no interactive prompts; give the non-interactive form
- expected output shown after the command so the agent can verify
- failure recovery for the most likely failure after the command
