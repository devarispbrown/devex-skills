# Generator Lifecycle

A generator is a product surface. It is versioned, its drift is detected, and its templates are deprecated deliberately — never deleted silently.

## Versioning

- The generator is versioned with SemVer; the version is embedded in generated output markers.
- Every change has a changelog entry. Template changes that alter output bump the version and ship migration notes.
- Breaking changes (renamed kinds, changed output trees, renamed placeholders) are a MAJOR bump.

## Template drift vs generated projects

- **Template drift**: fresh generation differs from the fixture or from shipped generated projects. Cause: a template change without regeneration, or a hand edit.
- Detect with the drift job: regenerate with fixed inputs and diff.
- Triage each diff: template change (adopt it), intended hand edit (preserve it), or corruption (repair it).

## Regeneration workflows

1. `generate --upgrade` regenerates in place: marked generated regions are replaced, preserved hand edits are kept and reported.
2. Migration notes accompany every breaking template change; regeneration fails loudly when the diff cannot be applied automatically.
3. After regeneration, run the generated project's checks and the drift job.

## Deprecating templates

1. **Announce** — mark the kind deprecated in `--help` and in generated output markers; state the replacement and the timeline.
2. **Warn** — keep generating during the deprecation period, emitting a deprecation notice in the output.
3. **Migrate** — the replacement generator offers a migration path for existing generated projects.
4. **Remove** — delete the template and its fixture only after migration is complete and the removal ships as a documented MAJOR version change.

Never delete a template silently. A generated project that cannot be regenerated is a stranded asset.

## Maintenance checklist

Verify:

- the generator version and changelog are current
- the drift job is green, or every diff is triaged
- deprecated kinds are announced with a timeline
- every fixture matches fresh generation
