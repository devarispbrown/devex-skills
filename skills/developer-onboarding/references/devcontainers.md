# Devcontainers in Onboarding

Use when a containerized development environment for the getting-started path is under consideration. A devcontainer is an accelerator for the working developer, never a requirement of the magic path.

## devcontainer.json anatomy

The file declares the container the editor/CLI builds and attaches to:

- `image` or `build.dockerfile`: the base image; prefer a published, versioned image over an unpinned tag
- `features`: reusable, versioned installs of toolchains and runtimes, applied on top of the image
- `postCreateCommand`: first-run setup such as dependency install, fixture seeding, or auth priming; runs once per container
- lifecycle hooks: `onCreateCommand`, `updateContentCommand`, `postCreateCommand`, `postStartCommand`, `postAttachCommand` — earlier hooks run on fresh containers, later hooks on every start
- `forwardPorts`: ports the dev server listens on, forwarded to the host
- `customizations`: editor and extension configuration
- `remoteUser`: the user the workspace runs as

Keep the file minimal: a base image, the needed features, one post-create command, and nothing the product does not use.

## Lifecycle and the magic path

The container build and the post-create command count inside the magic-path timer when the container is the canonical route. A cold build that pulls a large image and installs a toolchain can consume the whole budget before the developer runs the product. Design for the warm path: a prebuilt image, a small feature set, and a post-create command that finishes in seconds.

When the container is an alternate route offered after success, its build time does not count against the gate — but it still must work, so keep it exercised in CI.

## When devcontainers earn their cost

A devcontainer earns its cost when:

- the product's dependencies are heavy, native, or version-sensitive, and host setup is the main onboarding failure
- the team is large or heterogenous, and one blessed environment kills "works on my machine"
- contributors and CI must share a reproducible stack

It does not earn its cost when:

- the product is a simple CLI or library, and the container adds a build step the developer never needed
- the image is unmaintained, unpinned, or rebuilds from source every time
- it exists because the real product can't run on a supported OS — that is a product defect, not a container use case

## Keeping devcontainers non-mandatory

The magic path must succeed without a devcontainer. The canonical quickstart is the host-native path; the devcontainer is documented as an optional accelerator after first success.

Never gate the quickstart behind "open in container." When the container is offered, give it one link and one command — opening it must be as easy as the host path, or it is not an accelerator.

## Maintenance contract

A devcontainer is committed code: it has an owner, it is exercised in CI on every relevant change, and its dependencies are updated with the product. A container that silently rots will produce onboarding failures that look like developer errors.
