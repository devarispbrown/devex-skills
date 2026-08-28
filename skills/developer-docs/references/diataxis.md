# Diataxis Operating Guide

Use Diataxis to decide what a document is for before deciding how to write it.

## The four modes

| Mode | User need | Orientation | Primary question | Author responsibility |
|---|---|---|---|---|
| Tutorial | Acquire skill | Learning + action | "Teach me by helping me build something" | Guarantee a successful learning experience |
| How-to | Apply skill | Goal + action | "How do I accomplish X?" | Give a practical route to a result |
| Reference | Apply knowledge | Information | "What exactly is X?" | Be authoritative, precise, complete, neutral |
| Explanation | Acquire understanding | Understanding | "Why/how does this work?" | Build context, connections, rationale, mental models |

## Tutorial rules

A tutorial is a lesson, not a feature tour.

- Start from a controlled, explicit state.
- Choose a meaningful small outcome.
- Ensure every step works in order.
- Tell the learner exactly where to run commands and what to expect.
- Include checkpoints so the learner knows they are on track.
- Minimize optional branches.
- Minimize deep explanation. Link to explanation instead.
- Do not require knowledge the tutorial has not introduced.
- End with a real accomplishment and useful next steps.

Bad tutorial smell: "Here are all the options." That is reference.

## How-to rules

A how-to solves a real task for a user who already has basic competence.

- Title it around a goal: "Configure retries", "Rotate credentials", "Deploy behind a proxy".
- Begin from realistic prerequisites, not from first principles.
- Focus on actions and decisions needed for the task.
- Allow real-world branches where necessary.
- Do not teach the whole product.
- Do not duplicate full reference tables. Link to reference.
- Include verification and recovery when failure is likely.

Bad how-to smell: a 45-minute guided lesson that explains basic concepts. That is a tutorial.

## Reference rules

Reference is the authoritative description of the machinery.

- Structure it according to the product/interface itself.
- Use stable, consistent patterns.
- State exact types, values, defaults, constraints, and behavior.
- Keep prose neutral and concise.
- Prefer generated facts from authoritative schemas where possible.
- Include examples only to clarify use of the described interface.
- Do not hide normative behavior in tutorials or blog posts.

Bad reference smell: long rationale and opinion interrupting field definitions. Move that to explanation.

## Explanation rules

Explanation builds a mental model.

- Answer why, how, when, and what tradeoffs exist.
- Connect concepts to one another.
- Explain architecture, constraints, design choices, alternatives, and history when useful.
- Use diagrams when relationships are difficult to hold in prose.
- Discuss implications and edge cases.
- Do not turn explanation into a recipe.

Bad explanation smell: numbered imperative steps to accomplish a production task. That is how-to.

## Cross-linking pattern

A strong docs set lets users move between modes:

- Tutorial -> explanation for concepts, reference for details, how-to for next tasks
- How-to -> reference for exact options, explanation for tradeoffs
- Reference -> how-to for workflows, explanation for semantics/design
- Explanation -> tutorials for learning-by-doing, reference for exact details

## Classification test

Ask two questions:

1. Is the user **studying** or **working**?
2. Do they need **action** or **theory/information**?

- study + action = tutorial
- work + action = how-to
- work + information = reference
- study + theory = explanation

## Important nuance

Do not force the repository into four top-level folders merely to satisfy the framework. Improve page intent and user navigation first. The structure should emerge from clear content boundaries.
