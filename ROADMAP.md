# Roadmap

This roadmap communicates scope and sequencing, not delivery dates. Reproducibility, inspectability, privacy, and responsible interpretation outrank metric count.

## Shipped in 0.1

- Offline public-shaped bundles and optional bounded public fetching.
- Deterministic path/reviewer events, latency/UTC activity, concentration, unowned paths, and 80% review-authority bus factor.
- JSON, accessible static HTML, correction-friendly CODEOWNERS suggestions, and installable CLI packaging.

## Next: sample transparency and corrections for 0.2

- Include explicit PR/sample bounds in reports.
- Add path-level median response time while preserving raw count/context.
- Design a separate, versioned corrections file for reviewer aliases and suggested owners.
- Paginate public fetching with deterministic caps and complete snapshot metadata.

These map to [issue seeds 1–4](docs/ISSUE_SEEDS.md). Fixture, wording, accessibility, and small diagnostic improvements are welcome now.

## Explore after corrections are inspectable

- Rename-aware path continuity using public file metadata.
- Explicit path grouping rules that never silently merge subsystems.
- Versioned migrations for metric/input schema changes informed by public feedback.

See [issue seed 5](docs/ISSUE_SEEDS.md). Exploration does not promise inclusion.

## Before 1.0

- Stabilize input/report schemas and metric definitions.
- Validate responsible-use language and accessibility with independent reviewers.
- Publish a deprecation window and migrations for intentional breaks.

Private repository scanning, employee scoring, location inference, leaderboards or cross-repository indexes that name individual reviewers, automatic reviewer assignment, and governance actions remain out of scope.
