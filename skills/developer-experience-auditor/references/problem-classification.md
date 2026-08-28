# Problem Classification

Every finding in the DX Report carries exactly one primary problem class. Classify by where the fix must land, not by where the symptom appeared.

## The nine problem classes

1. **Discovery and findability**
   - Fix lands in: navigation, indexing, naming, landing page, docs entry points.
   - Assign when: the developer cannot locate the product, the canonical path, or a documented capability.
   - Example: searching the docs index for "timeout" returns nothing although the feature exists.

2. **Onboarding and setup friction**
   - Fix lands in: install, auth, credentials, prerequisites, environment, sandbox provisioning.
   - Assign when: reaching an authenticated, configured state requires manual steps, hidden knowledge, or approvals.
   - Example: the sandbox requires an email verification only the sales team can approve.

3. **API and contract design**
   - Fix lands in: endpoints, resource model, request/response shape, status codes, pagination, rate limits.
   - Assign when: a documented call is awkward, inconsistent, or contradicts the rest of the API.
   - Example: list endpoints return an array but detail endpoints wrap results in an object.

4. **CLI and configuration**
   - Fix lands in: flags, exit codes, stdout/stderr, config schema, defaults, precedence, environment variables.
   - Assign when: command invocation or configuration is surprising, undocumented, or inconsistent.

5. **SDK quality**
   - Fix lands in: SDK implementation and its language idioms.
   - Assign when: an official SDK is missing operations, contradicts the canonical API, or feels non-idiomatic.

6. **Error and recovery quality**
   - Fix lands in: error messages, diagnostics, retry safety, correlation identifiers, troubleshooting docs.
   - Assign when: an expected error does not explain what happened, why, and how to fix it.

7. **Local development**
   - Fix lands in: build tooling, dev loop, committed automation, service setup.
   - Assign when: a clean clone cannot reach the productive state using only committed instructions.

8. **Testing and quality story**
   - Fix lands in: test commands, fixtures, CI configuration, sample data.
   - Assign when: the developer cannot run tests, or tests do not cover the journey.

9. **Release and compatibility**
   - Fix lands in: versioning, changelog, migration guidance, deprecation policy, upgrade path.
   - Assign when: upgrading or migrating is risky, undocumented, or breaks silently.

## Attribution rules

- Assign one primary class per finding. A secondary class may be noted when the fix spans two surfaces.
- When two classes could hold the fix, choose the root cause: the surface whose change removes the friction, not the surface that merely documents it.
- Do not classify an interface defect as **Discovery and findability** or **Onboarding and setup friction** merely because documentation could explain it. Interface defects belong to **API and contract design**, **CLI and configuration**, **SDK quality**, or **Error and recovery quality**.
- Infrastructure latency or reliability that blocks a stage belongs to the stage's class, with a note; it is not a separate class.
- External dependency blockers (third-party approval, quota, network) are attributed to the class where the developer experienced them, with the external dependency recorded.

## Legacy 4-class mapping

Reports written against the legacy defect vocabulary (Docs, Product/DX, Infrastructure, External dependency) map as follows:

| Problem class | Legacy class |
|---|---|
| Discovery and findability | Docs |
| Onboarding and setup friction | Product/DX |
| API and contract design | Product/DX |
| CLI and configuration | Product/DX |
| SDK quality | Product/DX |
| Error and recovery quality | Product/DX |
| Local development | Infrastructure |
| Testing and quality story | Infrastructure |
| Release and compatibility | Product/DX |

The legacy classes are retained only for cross-report compatibility. New findings use the nine classes.
