# Code Comments and Symbol Documentation

## Principle

Code expresses mechanics. Comments should preserve intent, contract, invariants, and context that the code cannot express clearly.

## Public symbol docs

For exported/public APIs, document as appropriate:

- purpose
- parameters and accepted values
- return value
- errors/exceptions
- side effects
- concurrency/thread safety
- ownership/lifetime
- units/formats
- performance complexity when non-obvious and important
- examples for surprising usage
- deprecation/replacement

Follow the ecosystem's native doc convention: Go doc comments, JSDoc/TSDoc, Python docstrings, Rustdoc, JavaDoc, XML docs, etc.

## High-value inline comments

Explain:

- why a non-obvious approach is necessary
- invariant that later edits must preserve
- protocol/spec constraint
- concurrency ordering
- security boundary
- performance workaround
- compatibility requirement
- intentional deviation from a simpler implementation

## Low-value comments

Remove comments that:

- restate the next line
- describe syntax
- are stale TODOs without ownership/context
- narrate straightforward control flow
- contradict the implementation

## TODO/FIXME standard

Prefer an issue/reference and explain the blocking constraint. A durable TODO should tell the next maintainer why it exists and what condition allows removal.
