# Profiling Without Guessing

## Purpose

Profiling converts a slow benchmark into a named cost. The profile is evidence; the fix follows the widest frame, not the loudest hunch.

## Procedure per surface

### CLI and local processes

1. Reproduce the slow invocation under the benchmark harness.
2. Sample the process with a CPU profiler (perf, sample, or equivalent) for the duration of the measured path.
3. Convert samples to a flamegraph; read it top-down.

### API services

1. Trace the canonical request through the service; profile server-side where time is actually spent.
2. Include the client-server boundary: account for queueing and I/O when attributing latency.

### SDKs and libraries

1. Profile the import/initialization path in isolation from the host application.
2. Separate library time from application time; budget only the library's overhead.

### Builds and tests

1. Profile the build with build-system tracing or sampling, not wall-clock vibes.
2. Attribute time to phases — resolution, compile, link, packaging — before blaming a dependency.

## Flamegraphs

- Read width, not height: the widest frames hold the most time.
- Read the stack, not the tip: a wide leaf under a wide path is the cost; attribute it to the caller that matters.
- Confirm every candidate frame in code before proposing a fix. A wide standard-library frame may mean a hot call site in project code.
- Save the flamegraph artifact with the finding; before/after pairs prove the fix.

## Allocation tracing

- When CPU time points at allocation or GC, trace allocations and retainers instead of guessing at object counts.
- Count allocations and bytes by call site; the widest allocation site is the fix target.
- Beware allocations hidden in logging, string building, and per-request temporaries.

## Identifying hot paths without guessing

1. Rank frames by self time or inclusive time; start with the widest self-time frame.
2. Confirm the frame is reached from the measured path — profile the path, not the process at rest.
3. Reproduce before changing: one profiler run can lie; two agreeing runs rarely do.
4. Only then write the fix, and re-run the benchmark after it.

## Verify

- profile taken under the same conditions as the benchmark
- suspected hot path is the widest frame in the profile
- the frame's cost is attributable to project code
- profile artifacts saved with the finding
- the fix is benchmarked before it is claimed
