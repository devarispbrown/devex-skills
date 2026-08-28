# Documentation Lifecycle, Releases, Migrations, and Deprecations

## Docs-as-code lifecycle

Documentation should change in the same engineering lifecycle as the product.

For each public change, answer:

- what docs change with this code?
- does API reference generation need regeneration?
- do SDKs need release or examples?
- does the quickstart still work?
- are old docs now misleading?
- is a migration guide required?
- is the changelog sufficient?

## Changelog

A developer changelog should be scannable by impact. Distinguish:

- breaking
- deprecated
- added
- changed
- fixed
- security/operationally significant

Link to migration material when action is required.

## Deprecation

A deprecation notice should state:

- what is deprecated
- replacement
- why when useful
- deprecation date
- behavioral impact
- migration steps
- sunset/end-of-support date if known
- version scope

Do not silently delete old docs before users have a migration route.

## Migration guides

Migration guides are how-to documentation. Include:

- affected users
- pre-migration checks
- breaking changes
- old/new side-by-side examples when useful
- sequence of changes
- compatibility window
- data migration if relevant
- validation
- rollback
- common failures

## Freshness

Use automation where possible to detect:

- docs referencing removed symbols
- outdated package versions
- obsolete flags/config keys
- dead links
- examples failing builds
- stale generated reference
- pages for unsupported releases
