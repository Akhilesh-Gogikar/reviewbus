# Architecture

ReviewBus is one Python module with no runtime dependencies. It separates acquisition from analysis so public metadata snapshots remain inspectable and reproducible.

1. `fetch_public_repository()` optionally reads a bounded public repository/PR/files/reviews snapshot, keeps only `APPROVED` and `CHANGES_REQUESTED` reviews, and rejects repositories reported as private.
2. `analyze_bundle()` validates explicit public visibility, normalizes paths/users/timestamps, and converts the latest qualifying non-author review into path-review events.
3. Deterministic aggregators compute reviewer/path counts, latency, UTC activity, concentration, unowned paths, and the minimum reviewers responsible for 80% of events.
4. JSON, HTML, and CODEOWNERS renderers consume the same report object. Atomic writes prevent partial files.

The offline `analyze` path makes no network requests. The optional `fetch` path sends only public read requests and an optional token header. It does not write to the remote repository.

Metrics describe the analyzed sample, not formal authority, current availability, employment, expertise, or performance. Input and output compatibility are documented in [API stability](API_STABILITY.md).
