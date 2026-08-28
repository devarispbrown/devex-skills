# Command Hierarchy and Naming

Procedure for designing or auditing command structure, naming, and aliases.

## Hierarchy design

1. Start with `tool <verb> <noun>`: actions are verbs, targets are nouns. `sync dataset`, `delete dataset`.
2. Keep the tree at most two levels deep; a third level is a finding.
3. Group related nouns under the verb they share. Do not invent a noun group ("resource", "object") that adds no meaning.
4. Prefer flat verbs over nested modes: `tool config set`, never `tool config --set` or `tool set-config`.
5. Every command has a help entry. A hidden command that users reach is a finding.

## Naming rules

1. Lowercase, one word; hyphens join, underscores never.
2. One verb per concept: pick `delete`, `remove`, or `drop` and use it everywhere in the tool.
3. Verbs for actions, nouns for targets. Do not mix `delete dataset` and `dataset remove` in one tool.
4. Never name a command after an implementation detail.
5. Common verbs keep common meanings: `list` enumerates, `get` fetches one, `sync` makes targets match, `run` executes a job, `set` writes config.

## No-argument defaults

1. A command run with no arguments shows help or runs a safe read-only default.
2. Never default to a destructive action when arguments are missing.

## Alias policy

1. Add aliases only for established muscle memory from a previous CLI.
2. Every alias is documented in help, pointing at the canonical name.
3. Never accept an alias as the only spelling; the canonical name always works.

## Decision tree

- New behavior is read-only? Use `list` or `get` with a noun target.
- New behavior changes state? Use a change verb: `set`, `add`, `update`, `sync`, `run`.
- New behavior destroys state? Use `delete`/`drop`/`purge`; apply destructive-operations.
- A verb already covers it? Reuse the verb; do not add a synonym.
- The name is taken? Rename the new command; never overload the old one with a second meaning.
- A flag would invert the meaning? Add the new flag and deprecate the old one; never silently invert.

## Verify

- every command appears once, with one meaning and one spelling
- no two commands are near-synonyms
- the full surface reads top-down as a coherent sentence
- no-arg behavior is safe and deliberate
