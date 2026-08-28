# Journey Clustering

## Cluster definition

A cluster is a journey stage plus a failure mode plus a frequency. All three must be stateable in one sentence, for example: "install-stage blocked failures, 32% of install attempts."

A signal belongs to exactly one cluster. Do not invent a cluster for a single signal.

## Clustering procedure

1. Run `scripts/cluster_feedback.py` on the labeled JSONL to get a first-pass sketch by shared significant tokens.
2. Read the representative items of every sketch cluster. Confirm the items share a journey stage, a failure mode, and a plausible cause.
3. Merge sketch clusters that are the same journey problem approached from different angles.
4. Split clusters that share a symptom but not a cause.
5. Name each final cluster.
6. Count the frequency and state the unit: distinct developers or distinct events.

## Worked example

Labeled signals, install stage:

- "docker: connect: connection refused" — issue, install, blocked
- "unable to reach any registry endpoint" — issue, install, blocked
- "Error response from daemon: Get http://host.docker.internal:5000 ... connection refused" — chat, install, blocked
- "the quickstart says pull from the local registry but docker cannot connect to host.docker.internal" — chat, install, blocked
- "install attempt failed: registry pull connection refused at host.docker.internal" — telemetry, install, blocked

The script groups them on shared tokens: install, registry, docker, refused, host, internal. Reading the items confirms one cause: the quickstart's registry address points at a Docker-internal host that is unreachable outside the container network.

Cluster name: "install-blocked: quickstart registry unreachable (host.docker.internal)".

Frequency: 32% of install attempts this window failed at the registry step, from 19 distinct developers.

Do not name the cluster "docs problem" because the fix will probably be a docs change. The name describes the journey failure; the root-cause step decides the owner.

## Frequency x severity sizing

Size each cluster on the product of:

- frequency — how many developers or how many events
- severity — the P-level of the failure from the canonical vocabulary
- cost — time lost per hit, from impact sizing

A rare P1 beats a common P3. A common P3 that recurs on every developer session can beat a rare P2. Compute the rank in the impact step; clustering only needs the frequency.
