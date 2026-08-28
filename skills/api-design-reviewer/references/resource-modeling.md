# Resource Modeling and Naming

## Nouns, not verbs

- Resources are nouns; HTTP methods express the action. GET lists or reads, POST creates, PUT replaces, PATCH mutates, DELETE removes.
- A path segment that names an action (`/widgets/send`, `/widgets/run`) or embeds one (`getWidget`) is a candidate defect. Actions belong in methods.
- Report the action as a method on the affected resource, or as a documented POST when the action has side effects and no resource identity.

## Collections are plural

- Collection paths use plural nouns: `/widgets`, `/widgets/{widgetId}`. A singular collection path (`/widget`) is a candidate defect.
- A path with a verb or action between resource segments (`/widgets/{id}/approve`) is a candidate defect; model the state transition instead.
- Singleton resources (`/me`, `/status`) are the documented exception. Keep the exception explicit and rare.

## Opaque identifiers

- IDs are opaque strings. Never require clients to parse ordering, format, or globality out of them.
- Do not leak implementation into IDs: autoincrement counters, host names, environment markers, or internal table keys.
- Path parameters are identifiers, not filters: `/widgets/{widgetId}` retrieves one resource; `/widgets?color=red` filters a collection.
- ID field names are consistent across resources: `id` on every resource, `{resource}Id` for references.

## Parent/child consistency

- A child resource has exactly one canonical path form. Do not expose both `/widgets/{id}/parts` and `/parts?widgetId=`.
- Deleting a parent either cascades to children or orphans them. Document which; do not leave it ambiguous.
- Nested depth beyond two levels is a candidate defect. Flatten through composition, links, or top-level resources.

## State transitions are explicit

- Every stateful resource documents its states, the transitions between them, and who may trigger each transition.
- Do not overload a resource with an implied workflow that silently advances state on unrelated calls.
- Prefer a named transition endpoint with a defined outcome over free-form body flags when the transition has side effects.
- Transition failures are explicit errors, never silent no-ops.

## Decision tree: where does the resource boundary go?

1. **Does the thing have identity and a lifetime?** Addressable and durable: it is a resource.
2. **Does it only ever exist inside one parent?** Make it a sub-resource under that parent's path.
3. **Does it exist standalone but is commonly listed under a parent?** Make it a top-level resource; let the parent list filter by a parent-id parameter.
4. **Is it a one-shot action with no state?** Expose it as a POST action on the closest resource, or as its own resource only if it gains a job/status lifecycle.
5. **Is it a relationship between two resources?** Model the relationship as a resource named for the relationship, or as a link field on one side.
6. **Is it a computed or derived view?** Keep it read-only: a query parameter or a read-only endpoint. Never make it writable.
7. **Is it a configuration knob?** A small set of knobs is a resource; an open-ended map of options is a candidate for structured settings with validation.

Apply the tree per concept, then verify the resulting names are guessable from the domain vocabulary.
