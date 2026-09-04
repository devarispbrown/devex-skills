# Adversarial selection review

The review that upstream guidance does not ship. The reviewer's job is to prove the model
will pick the wrong tool.

## Procedure

1. **List the surface.** Every tool, with the one-line intent its description claims.
2. **Form the pairs.** For each tool, name the sibling a caller could plausibly confuse it
   with. Judge by intent overlap, not string similarity, for the reason in
   `tool-definitions.md`.
3. **Write the deciding prompt.** For each pair, write the request a real caller would make
   that should select each side. Two prompts per pair.
4. **Test the descriptions alone.** Read only the two descriptions and the prompt. Can the
   choice be made? If it takes knowledge of the implementation, the description is the
   defect.
5. **Record the finding.** A pair that cannot be separated is a finding against the
   description, or a signal the two tools should be one.

## What counts as a finding

- Two descriptions that would both plausibly answer the same prompt.
- A description whose selection criteria are implicit in an example rather than stated.
- A pair separable only by knowing which is newer, faster, or internally preferred.
- A tool whose description names no boundary at all, so every adjacent prompt is a
  coin flip.

## What does not count

- Lexical similarity with no intent overlap.
- A pair a careful human reader separates instantly from the descriptions.
- A tool that is simply rarely used.

## Reporting

The result is a table of pairs with a separated or not-separated call, and for each
not-separated pair, the change proposed. The change is a description rewrite or a
consolidation. It is never a note added to the documentation, because the model reads the
description and not the documentation.

## Honest limits

This review is performed by a person who also authored or is reviewing the descriptions,
so it inherits the bias that reviewer bias always carries. It is a structured reading, not
a measurement. An empirical selection-accuracy result requires a labeled prompt set and the
trial machinery in `agent-native-dx`, and until that exists the review reports findings
rather than rates.
