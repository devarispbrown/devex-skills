# Cost Estimation Before Deploy Standard

## Cost is predictable before deploy

Deploying a metered workload without a cost estimate is a risk change. The estimate precedes the deploy, not the invoice.

## Estimate command

Every product with per-use pricing has an estimate command that prices a workload before it runs. Inputs are the workload description (requests, tokens, compute, storage, duration). Output is a total cost with:

- per-unit prices, explicit
- quantity assumptions, stated
- a confidence/error bound where material

The estimate command is idempotent, side-effect-free, and works in sandbox/test mode.

## Price transparency

Per-unit prices are:

- explicit in the estimate output
- machine-readable where the product ships schemas
- versioned with pricing changes
- never buried in prose or behind a login

## Coverage

An estimate covers the full run, not the first call:

- every metered dimension the workload touches
- burst and sustained phases
- retries and overage paths where material
- storage and egress where they apply

## Surprise-invoice prevention

Assess per surface:

- can the workload run unbounded? A spend cap is required.
- do estimates and bills use the same price list? Drift between them is a P1 defect.
- are hidden costs (egress, storage retention, retries) listed?

Any surface where estimated cost and actual billing can diverge materially without warning is a finding.

## Review checklist

- [ ] estimate command exists and prices the full run
- [ ] per-unit prices explicit and versioned
- [ ] bounds stated where material
- [ ] hidden-cost surfaces identified
- [ ] estimate precedes the deploy and is recorded as evidence
