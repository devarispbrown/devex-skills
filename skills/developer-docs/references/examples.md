# Examples, Quickstarts, and Sample Apps

Examples are executable documentation and should be treated as production-maintained code.

## Levels of example

### Minimal snippet
Shows one concept with minimal surrounding code. Appropriate in reference.

### Complete example
Copy-pasteable or directly runnable example for a real task. Appropriate in how-to docs.

### Quickstart
Controlled end-to-end learning path with a clear success state. Appropriate as a tutorial.

### Sample application
A maintained application showing realistic integration patterns and architecture.

Do not confuse these levels.

## Requirements

Examples should:

- declare prerequisites
- use currently supported APIs/SDKs
- avoid hard-coded secrets
- include imports and setup when expected to run standalone
- include error handling proportional to the example's purpose
- show expected output or verification
- clean up resources when needed
- use realistic names/data without leaking production information
- link to deeper reference

## Test strategy

Prefer, in order:

1. execute the exact snippet/source in CI
2. import snippets from tested source files into docs
3. compile/type-check extracted snippets
4. schema-validate request/response examples
5. snapshot stable expected output

Avoid manually duplicated snippets across many pages.

## Production transition

Quickstarts should clearly separate "enough to learn" from "ready for production." Link to production guidance covering security, retries, observability, scaling, limits, data handling, and failure modes.


## Magic-path quickstarts

The canonical quickstart is a special tutorial with a hard ≤15-minute end-to-end success criterion. Read `magic-path.md` before creating or revising it. Optimize for one recommended route, copy-pasteability, a meaningful verified result, and minimal branching.
