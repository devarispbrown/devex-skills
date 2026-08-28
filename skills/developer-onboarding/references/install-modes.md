# Install Modes

Compare install modes before choosing the canonical one. The chosen mode's install, auth, configure, execute, and verify time all count inside the magic-path timer; the mode choice is a budget decision, not a taste decision.

## Evaluation matrix

| Mode | Platform coverage | Upgrade story | Timer fit | Wins when |
|---|---|---|---|---|
| brew formula | macOS; Linux via Linuxbrew | `brew upgrade`; formula published and versioned by you | fast when installed; formula install is seconds | the primary developer platform is macOS and the team owns the formula |
| npm package | any Node host | `npm update` or `npm install -g`; registry handles versions | fast, one command; Node runtime is the prerequisite | the ecosystem is JavaScript and the package is small and dependency-light |
| `go install` | any Go toolchain | none built in; developer re-runs `go install` at a pinned version | fast, one command; Go toolchain is the prerequisite | the product is a single-binary Go CLI and a Go toolchain is a realistic prerequisite |
| docker image | any Docker runtime | `docker pull` the new tag; tag drift is easy | pull time counts against the timer; large images can eat the install budget | dependencies are complex or multi-service and the developer already runs Docker |
| `npx` | any Node host | registry version pinned per invocation | zero permanent install; first run downloads the package | the product is a one-shot runner or scaffold and install is not the point |
| curl-script | anything with curl | weak; script must be pinned and checksummed | fast but adds a trust decision | nothing else fits; only with a versioned, checksum-pinned, audited script |

## Rules that apply to every mode

**One canonical mode before first success.** Present the chosen mode as the only install step. Other modes become alternates after success.

**Keep the prerequisite honest.** A language runtime or package manager listed as a platform prerequisite is allowed. Product-specific CLIs, agents, containers, and services are inside the timer no matter which mode delivers them.

**Prefer the smallest surface.** The mode with the fewest moving parts and the least post-install state usually wins. A mode that requires a daemon, a path edit, or a restart adds segments you did not budget.

**The upgrade story is part of the design.** Design how the developer and CI get the next version before choosing the mode. A mode with no upgrade story is a support burden that will surface as an onboarding failure later.

## Docker and npx special cases

Docker earns its cost when the product genuinely cannot run on the host: multi-service stacks, native dependencies, version-sensitive runtimes. It loses when the image is large, the pull is slow, or the developer must learn Docker to evaluate the product. Prefer a slim image and document the non-container path after success.

`npx` wins for ephemeral use: run a scaffold, seed a fixture, execute one command. It loses as a day-to-day install because every invocation re-resolves the package. When the developer will keep using the product, install it for real after first success.

## What belongs inside the timer

The mode chosen, the install command itself, any post-install setup it triggers, authentication, configuration, execution, waiting, and verification all count against `MAGIC_PATH_MAX_MIN`. If the chosen mode cannot fit its own install segment, switch modes — do not move install into prerequisites.
