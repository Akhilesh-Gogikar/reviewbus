# Provenance log

This repository must remain independently developed from public sources and synthetic fixtures.

## Rules

- Record every specification, dataset, fixture, snippet, dependency, and generated asset before it enters the repository.
- Prefer public primary sources and link the exact version or commit.
- Do not copy from private, partner, customer, or unpublished research repositories.
- Public visibility is not a copyright license; record applicable terms.
- Stop and request ownership review when provenance is uncertain.

## Sources

| Date | Source/version | Purpose | License or terms | Notes |
|---|---|---|---|---|
| 2026-08-16 | Project brief derived from public-landscape research | Initial scope only | Internal planning | No implementation or copied source |
| 2026-08-16 | GitHub REST API documentation, version 2022-11-28, https://docs.github.com/en/rest | Public repository, pull request, files, and reviews response shapes | GitHub documentation terms | Implementation performs bounded read-only public requests |
| 2026-08-16 | Python 3 standard-library documentation, https://docs.python.org/3/ | CLI, HTTP, JSON, timestamp, and static HTML implementation references | PSF License Version 2 | Implementation is original and uses only the standard library |
| 2026-08-16 | Original synthetic public-GitHub-shaped fixture | Deterministic tests and demonstration | Original synthetic data | Names and events are invented; no private, partner, or customer inputs |
