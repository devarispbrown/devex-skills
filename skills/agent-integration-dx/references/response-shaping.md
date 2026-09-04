# Response shaping against a context budget

A tool response is a message to a reader with a finite context that is also holding the
conversation, the plan, and every other tool result. Completeness is not the goal.

## Shape for the reader, not the record

- Return what the caller needs to decide the next step, not the full record because it was
  available.
- Include the identifiers required for the next call. A response the agent cannot act on
  without a second lookup has moved the cost rather than removed it.
- Prefer a stable field set over a variable one. A response whose shape depends on the data
  forces the model to branch on structure.

## Pagination and truncation

- List responses paginate. A tool that returns an unbounded list will eventually return one
  that does not fit.
- Truncation is explicit. A silently truncated response is indistinguishable from a
  complete one, and the agent will reason from a partial set believing it is whole.
- State the total and the cursor. Without the total, the agent cannot tell whether another
  page is worth fetching.

## Errors

An error is the tool's most important response, because it is where an agent either
recovers or gives up. It must name the corrective action the agent can take without a
human: which argument was wrong, what shape was expected, whether the call can be retried.

A stable machine-readable code carries this across releases. Prose alone does not.

## Untrusted content

Any field carrying text the vendor did not author places third-party content into the
agent's context, where it may be read as instruction rather than data.

Declare which response fields are third-party-sourced and state the labeling contract for
them. That declaration is checkable against the schema. Whether the labeling defeats an
attack is not, so treat this as a disclosure requirement rather than a safety claim.
