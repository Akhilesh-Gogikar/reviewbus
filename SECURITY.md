# Security policy

## Supported versions

Until 1.0, only the latest tagged 0.x release and `main` receive security fixes.

## Report privately

Do not open a public issue for token handling, URL construction, unsafe output, or a report containing sensitive repository/person data. Open a private GitHub security advisory:

<https://github.com/akigogikar/reviewbus/security/advisories/new>

Provide the affected version, operating system, a minimal synthetic reproduction, impact, and mitigation if known. Never attach private metadata or live credentials. Expect acknowledgement within seven days; remediation timing depends on severity and reproducibility.

Use a least-privilege token only for optional public fetching. ReviewBus never needs write access. Prefer offline snapshots when reproducibility or data minimization matters.
