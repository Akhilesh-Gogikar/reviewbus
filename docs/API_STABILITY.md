# API and output stability

ReviewBus 0.x is alpha software.

- CLI arguments, normalized snapshot fields, report fields, and metric definitions may change in a minor 0.x release.
- `schema_version` changes when report consumers must adapt. Additive fields may appear during 0.x without a bump.
- JSON entity ordering and formatting are deterministic, but consumers must parse JSON rather than compare whitespace.
- The offline input shape requires explicit public visibility plus nested `pull_requests`, `files`, and `reviews` arrays.
- HTML is a human report rather than a machine API. CODEOWNERS output is a suggestion requiring correction, never an assignment.

Metric-definition changes and migrations will be recorded in [CHANGELOG.md](../CHANGELOG.md). A 1.0 release will define a longer compatibility window after public-maintainer feedback.
