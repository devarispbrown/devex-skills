# Capability Discovery

## Purpose

Make extensions findable and their capabilities knowable, in both directions: authors must discover what the host offers, and the host and users must discover what installed and published extensions offer.

## Manifest as source of truth

The manifest is the single machine-readable record of identity and capability. Every extension publishes one. Required metadata:

- identity: name, namespaced and unique; version; description; author/publisher; license
- compatibility: the version contract (see `version-compatibility.md`)
- capabilities: the hooks, interfaces, config points, and provider slots the extension implements
- integrity: checksum and signature so installs are verifiable

The manifest is authoritative; discovery surfaces render it, never duplicate it by hand.

## Naming

- Namespaced names prevent collisions: `publisher/name`, not bare names.
- A canonical id survives renames; display names may change.
- Registration of a taken name is refused, not silently overwritten.

## Registries

- A central registry holds published extensions and their metadata; a local install holds what the host has loaded.
- Update channels: stable and preview. Preview channels never auto-promote; promotion is explicit.
- Registry entries are immutable per version; re-publishing the same version is an error.
- Integrity and provenance are verified before install; unknown sources are flagged, not trusted.

## Discovery surfaces

- CLI: `list`, `search`, `install`, `info` with machine-readable output for automation.
- Programmatic: a host API returning the installed capability set, so extensions can negotiate (see `version-compatibility.md`).
- Browse: a human surface over the same registry metadata.

## Lifecycle operations

Install, update, and remove are:

- idempotent: re-running the same operation is safe
- versioned: installs pin a version; updates are explicit
- reversible: uninstall and rollback restore the prior state
- transactional: a failed install leaves no half-installed extension

## Trust model

- Signed metadata and checksums at publish time; verification at install time.
- Provenance (who published, when, from where) is recorded and visible.
- Takedown and revocation propagate to installed copies, per the isolation reference's escalation path.
