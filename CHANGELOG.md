# Changelog

All notable changes are recorded here. The project follows Semantic Versioning after its first public tag.

## [Unreleased]

## [0.1.1] - 2026-10-05

### Changed

- `fetch` snapshots keep only `APPROVED` and `CHANGES_REQUESTED` reviews, the only states the analysis uses; comment-only and pending reviews are no longer stored.
- JSON methodology and the HTML reviewer table state that response hours run from pull-request creation and that per-reviewer figures are not a performance, responsiveness, or availability measure.
- Replace fixture and test logins that matched real GitHub accounts with clearly synthetic handles.
- Document the personal data in snapshots and reports, responsible-use limits, and CODEOWNERS consent in the privacy guide.
- Move the repository to `Akhilesh-Gogikar`, keep maintainer launch planning out of the repository, and list related tools only after they are public.

## [0.1.0] - 2026-08-17

### Added

- Offline public-GitHub-shaped input and optional bounded public metadata fetch.
- Deterministic path/reviewer metrics, response latency, UTC activity, concentration, unowned paths, and 80% review-authority bus factors.
- Static HTML, JSON, and correction-friendly CODEOWNERS suggestions.
- Synthetic fixture and standard-library tests.

[Unreleased]: https://github.com/Akhilesh-Gogikar/reviewbus/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/Akhilesh-Gogikar/reviewbus/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Akhilesh-Gogikar/reviewbus/releases/tag/v0.1.0
