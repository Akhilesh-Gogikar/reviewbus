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
| 2026-08-16 | Project brief derived from public-landscape research | Initial scope only | Owner's personal planning notes (not included) | No implementation or copied source |
| 2026-08-16 | GitHub REST API documentation, version 2022-11-28, https://docs.github.com/en/rest | Public repository, pull request, files, and reviews response shapes | GitHub documentation terms | Implementation performs bounded read-only public requests |
| 2026-08-16 | Python 3 standard-library documentation, https://docs.python.org/3/ | CLI, HTTP, JSON, timestamp, and static HTML implementation references | PSF License Version 2 | Implementation is original and uses only the standard library |
| 2026-08-16 | Original synthetic public-GitHub-shaped fixture | Deterministic tests and demonstration | Original synthetic data | Names and events are invented; no private, partner, or customer inputs |
| 2026-08-16 | GitHub Docs, About code owners, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners | CODEOWNERS suggestion syntax | GitHub documentation terms | Output format only; no text copied |
| 2026-08-16 | Herfindahl–Hirschman index (public concentration measure) | `concentration_hhi` definition | Public mathematical definition | Original implementation |
| 2026-08-17 | setuptools >=77, https://setuptools.pypa.io/ | Build backend only | MIT | Not a runtime dependency |
| 2026-08-17 | actions/checkout and actions/setup-python, pinned by commit SHA | CI and release workflows only | MIT | Not distributed with the package |
| 2026-08-17 | MIT License, https://opensource.org/license/mit | Repository license text and packaging metadata | MIT | Exact standard text with owner-requested copyright line |
| 2026-08-17 | Original project governance, community, workflow, packaging, and documentation text | DevRel launch-readiness baseline | Original work under repository license | Tailored to ReviewBus scope; no private or partner material |
| 2026-08-17 | Locally authored deterministic social-preview SVG | Repository preview and README identity | Original work under this repository’s MIT License | No external logos, fonts, screenshots, adoption claims, or partner assets; adjacent PNG is rendered from the SVG |
| 2026-10-05 | Synthetic fixture handles `fixture-author-*`, `fixture-reviewer-*`, and `reviewbus-fixtures/synthetic-repo` | Replace short fixture logins that matched real GitHub accounts | Original synthetic data | Each handle returned HTTP 404 from the public GitHub users API on 2026-10-05; the mocked fetch test also uses GitHub's public `octocat/Hello-World` demo identifiers |
| 2026-10-05 | Owner launch review | Public-release gate in SCOPE.md | Not applicable | Owner confirmed personal ownership with no employer, company, or partner IP claim; MIT license confirmed; full-history secret, provenance, privacy, and boundary audit found no blockers; trademark check was a directional web search only |
