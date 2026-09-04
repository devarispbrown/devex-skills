# Tool names, descriptions and argument schemas

Procedural guidance for authoring and reviewing a tool definition. Normative naming rules
live upstream, see `upstream-specs.md`.

## The description is a prompt

A tool description is read by a model at selection time, alongside every sibling
description, with no opportunity to ask a clarifying question. It is doing prompt work.
Write it as such.

A description that states only what the tool does leaves selection to inference. State
three things:

- **What it does**, in one clause.
- **When to choose it**, in the caller's terms rather than the implementation's.
- **When not to**, naming the sibling that handles the adjacent case.

The third is the one most often missing and the one that most often decides selection.

## Naming

- A name is a verb on a namespaced object: `calendar_create_event`, not `newEvent`.
- One verb per concept across the whole surface. If `get`, `fetch` and `read` all appear,
  the surface is teaching the model that the distinction carries meaning when it does not.
- Two tools whose names differ only by a synonym are one tool with a parameter, or two
  tools with descriptions that say which is which.

## Namespaces are not verbs

A surface named `git_status`, `git_diff`, `git_commit` is namespaced on `git`. The verb is
the token after the namespace. Treating the shared prefix as the verb makes every tool a
synonym of every other, which is a mistake the checker made against the reference git
server until it was taught to strip a prefix shared by every tool.

## Confusability is a property of pairs

Lexical similarity does not predict confusion. `create_user` and `create_org` are almost
identical and never confused. `send` and `dispatch` are lexically distant and confused
constantly. Review pairs by intent overlap, not by string distance.

This is why the checker reports candidates rather than verdicts: it can see the string and
not the intent.

## Argument schemas

The schema is where a bad call is stopped before it costs a round trip.

- Every parameter carries a type and a description. A parameter named `mode` with no enum
  is a guess the model has to make.
- Enums are closed and listed. Prose describing valid values is not a schema.
- A required parameter the caller cannot construct is a design defect, not a caller error.
  If a tool needs an internal identifier, provide the tool that returns it or accept the
  natural key.
- The schema should reject what the endpoint rejects. A schema more permissive than the
  endpoint converts a validation error into a failed call.

## Consolidation

Many small tools that mirror endpoints push the composition work onto the model. Prefer
one tool per user intent. Ask what a caller is trying to accomplish, not what routes exist.
Parameter-count guidance in the upstream sources is a useful pressure test.
