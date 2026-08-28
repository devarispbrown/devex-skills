# LLM and Coding-Agent Ready Documentation

Developer documentation increasingly serves both humans and software agents.

## Goals

Agents should be able to retrieve authoritative current facts without reconstructing them from marketing pages, screenshots, or conflicting blog posts.

## Practices

- Provide clean text/Markdown representations when possible.
- Maintain stable descriptive headings.
- Expose canonical schemas and specs.
- Keep version context close to the content.
- Clearly label preview, beta, deprecated, and historical behavior.
- Prefer complete examples over fragments with hidden context.
- Keep secrets out of sample code.
- Include error semantics and remediation in structured form.
- Keep canonical documentation indexable.
- Consider `llms.txt` as a machine-oriented index when supported.
- Avoid essential information that is only accessible through client-side interactions.
- Avoid duplicating normative facts across many pages.

## Retrieval test

Given only the docs, an agent should be able to answer correctly:

- How do I install this?
- How do I authenticate?
- What is the smallest working example?
- What parameters does this operation accept?
- What does this error mean and what should I do?
- Is retry safe?
- What API/SDK version is this for?
- How do I migrate from the previous version?

If answers require inference from multiple contradictory sources, improve the docs architecture.
