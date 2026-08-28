# Requests and Responses

## Required vs optional

- A field is required only when the API cannot act without it. Do not require fields that have safe defaults.
- Requiredness is declared once, in the schema's `required` list, and matches the documented contract.
- Do not change requiredness between related operations for the same resource without a versioned reason.
- Requiredness on read responses means the field is always present, including for edge-case records. If it can be absent, it is optional.

## Null vs omitted

- `null` means "explicitly set to nothing". Omitted means "not provided or not applicable".
- The null vs omitted distinction is only valid when the API documents and honors it. Otherwise treat them identically and say so.
- Never use an empty string or zero to mean null.
- Server responses that omit an optional field must not imply a default the API does not define.

## Defaults

- Every optional field with a default documents the default in the schema. Do not leave defaults implicit.
- Defaults never change between environments (test vs staging vs production) without explicit versioning.
- The server owns defaults. Clients may read them but must not be required to set them.

## Units and formats

- Timestamps use one canonical format (RFC 3339 UTC) named `created_at` / `updated_at`, identical across the API.
- Money is integer minor units plus an explicit currency field, or a decimal type. Never floats.
- Durations and sizes name their unit in the field name or in the documented format. Do not make the client guess milliseconds vs seconds.
- Byte sizes are decimal or binary consistently, documented once.

## Envelopes

- Pick one list envelope for the whole API: `{ "data": [...], "pagination": {...} }` or `{ "items": [...], "next": "..." }`. Do not mix.
- Do not wrap single resources in an envelope unless every resource is wrapped.
- Envelope fields are named consistently: the items key (`data` vs `items`) is the same everywhere.

## IDs and timestamps

- `id` is the primary identifier on every resource; `created_at` and `updated_at` use the canonical timestamp format.
- IDs and timestamps occupy the same position in every response object, so responses read the same way.
- Version or revision fields (`version`, `revision`, `etag`) are consistent in name and location where concurrency matters.

## Pagination

- One pagination vocabulary across the API: page/limit, offset/limit, or cursor-based. Never a mix.
- Cursor-based pagination returns opaque `next` / `previous` cursors (envelope or `Link` header); cursors may expire and that is documented.
- Pagination parameters are query parameters, ideally one shared parameter definition, with documented maximums.
- The pagination response fields (`next`, `total`, `has_more`) are the same names in every list response.

## Filtering and sorting

- Filters are query parameters named after the field: `?status=active`. One operator vocabulary (`eq`, `gt`, `lt`, `contains`) shared across the API.
- Sorting is `sort=field` or `sort=-field` for descending, with an explicit allowlist of sortable fields.
- Never accept arbitrary keys in a generic `filter` object without documenting and validating every key.
- Invalid filter or sort fields are explicit errors naming the rejected field, never silently ignored.

## Field selection

- Field selection (`?fields=`) is optional and additive; omitting it returns the full default representation.
- Do not silently drop fields the client did not request; document the default representation explicitly.
- Selected fields never change the semantics of the response, only its width.
