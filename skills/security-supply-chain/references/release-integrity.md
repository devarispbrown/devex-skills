# Release Integrity

Consumers must be able to verify that a released artifact is what the project actually built. Release integrity is the material that makes that verification possible.

## Artifact signing

1. Sign release artifacts with a private key held outside the build runner: a hardware key, a managed KMS, or a dedicated signing environment.
2. Publish the public key and its fingerprint where consumers can find it without trusting the artifact itself.
3. Sign at the release step, after the build is verified, never inside the same untrusted step that produced the artifact.
4. Use a key that is revocable and separate from personal developer keys.

Verify: every released artifact has a signature that the published public key verifies, with an Observed or CI-observed evidence label.

## Provenance and SLSA

1. Generate a provenance attestation for every release build: what was built, from which source revision, on which runner, under which build definition.
2. Prefer a provenance format that the platform or ecosystem verifies natively (SLSA provenance, attestation bundles).
3. Attach the attestation to the release record so a consumer can check it without extracting it from a binary.
4. Record the provenance level the project claims; do not claim a level the build process cannot evidence.

Verify: the attestation's recorded source revision matches the tag, and the build environment is reproducible from the attestation alone.

## SBOM

1. Generate an SBOM from the resolved dependency tree of the released artifact, not from the manifest.
2. Emit it in a standard format (SPDX or CycloneDX) with the versions and integrity hashes of what shipped.
3. Attach the SBOM to the release record and regenerate it on every release; a stale SBOM is worse than none.

Verify: the SBOM lists the same dependencies and versions as the built artifact, not the manifest's ranges.

## Checksums

1. Publish a checksum manifest for every release artifact, generated on the release machine after build.
2. Include the algorithm in the manifest; prefer a strong, non-deprecated digest.
3. Keep the manifest with the release record, never only inside an archive the checksum is supposed to protect.

Verify: downloading the artifact and the manifest and verifying every checksum succeeds.

## Release process isolation

1. Run release builds from a protected state: a protected tag or a dedicated release environment, never ad hoc from a developer machine.
2. Give the release workflow the minimum permissions and its own environment secrets; it must not inherit contributor PR scope.
3. Make releases repeatable: a clean checkout of the tag produces the same artifact content with the same checksums.
4. Keep signing keys, registry tokens, and package-manager credentials in the release environment, not in the repository.

Verify: no release artifact can be produced outside the defined release process without a credential the project controls.

## Tag protection

1. Protect release tags from force-push and deletion in the hosting platform.
2. Only the release workflow or an explicitly authorized actor may create or move a release tag.
3. Treat a rewritten release tag as a P0 incident: the artifacts it pointed to are suspect, and consumers must be told.

Verify: the platform settings reject force-push to tags and the release tag creation is attributable to the release process.
