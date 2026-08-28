# Security Policy

## Reporting a vulnerability

Report vulnerabilities privately through GitHub Security Advisories:

https://github.com/devarispbrown/devex-skills/security/advisories/new

Do not open a public issue for a suspected vulnerability.

Include:

- affected script or skill and version
- steps to reproduce
- impact assessment

You will receive an acknowledgment within the community response SLOs, and a fix or a concrete timeline as soon as practical. Credit is given in the release notes unless you ask otherwise.

## Scope

The suite is a collection of documentation skills and stdlib-only Python scripts. Scripts execute commands only through argv lists, never through a shell, and side-effecting tools default to dry-run. Findings in any script that reads, writes, or executes beyond its documented contract are in scope. Content of the skills themselves (markdown guidance) is not a security boundary.
