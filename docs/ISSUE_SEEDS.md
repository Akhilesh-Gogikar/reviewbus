# Issue seeds

These seeds are filed as issues #4–#8 in the `v0.2 — community evidence` milestone. They are scoped proposals, not promises; the live issue is authoritative for scope and labels. Keep the numbered headings stable because each issue links back to its seed. All tests and examples must use invented public-shaped data.

## 1. Show the analyzed pull-request bounds

**Issue:** [#4](https://github.com/Akhilesh-Gogikar/reviewbus/issues/4)

**Labels:** `good first issue`, `help wanted`, `reporting`, `difficulty: beginner`, `mentored`, `size: S`, `status: ready`

**Rationale:** `summary.pull_requests` gives a count but not the minimum/maximum PR number in the bundle. Reviewers need basic sample context before interpreting an unowned path or concentration value.

**Acceptance criteria:** add deterministic minimum/maximum PR numbers (or `null` for an empty bundle) to JSON and visible HTML methodology; do not imply chronological completeness; document the schema addition.

**Test plan:** cover empty, one-PR, unordered, and duplicate-number inputs; verify reversed input produces identical output; assert accessible HTML labels.

**Skills:** beginner Python, JSON, HTML. **Estimated scope:** 2–4 hours. **Likely files:** `reviewbus.py`, `tests/test_reviewbus.py`, `docs/API_STABILITY.md`, `README.md`.

## 2. Add median response time beside the mean

**Issue:** [#5](https://github.com/Akhilesh-Gogikar/reviewbus/issues/5)

**Labels:** `good first issue`, `help wanted`, `metrics`, `responsible-use`, `difficulty: beginner`, `mentored`, `size: M`, `status: ready`

**Rationale:** the arithmetic mean is sensitive to long tails. A median is useful only when the number of qualifying events remains visible and empty samples remain explicit.

**Acceptance criteria:** implement a small standard-library median helper; add path-level median fields without removing mean/count; do not add new per-reviewer timing statistics; use `null` for no events; define rounding and deterministic behavior in methodology.

**Test plan:** table-driven odd/even/empty/duplicate values, integration against the fixture, JSON determinism, and HTML text assertions.

**Skills:** beginner Python, descriptive statistics, testing. **Estimated scope:** 3–5 hours. **Likely files:** `reviewbus.py`, `tests/test_reviewbus.py`, `docs/ARCHITECTURE.md`, `docs/API_STABILITY.md`.

## 3. Design a separate corrections file

**Issue:** [#6](https://github.com/Akhilesh-Gogikar/reviewbus/issues/6)

**Labels:** `help wanted`, `design needed`, `responsible-use`, `difficulty: intermediate`, `size: M`, `status: ready`

**Rationale:** renamed accounts and maintainer corrections should improve suggestions without erasing what the public snapshot contained.

**Acceptance criteria:** agree on a minimal versioned JSON format; keep observed and corrected values separate; show every applied/stale correction; validate logins/paths; never auto-assign or mutate remote files; document privacy and compatibility.

**Test plan:** aliases, cycles, invalid logins, unknown paths, explicit unowned overrides, stale entries, deterministic ordering, and end-to-end CLI artifact checks.

**Skills:** data modeling, validation, privacy, CLI/API design. **Estimated scope:** 1–2 days after design approval. **Likely files:** `reviewbus.py`, `tests/test_reviewbus.py`, `docs/API_STABILITY.md`, `docs/PRIVACY.md`, `README.md`.

## 4. Paginate public fetches with explicit caps

**Issue:** [#7](https://github.com/Akhilesh-Gogikar/reviewbus/issues/7)

**Labels:** `help wanted`, `advanced`, `fetch`, `difficulty: advanced`, `size: L`, `status: ready`

**Rationale:** 0.1 reads one page per endpoint. Larger public repositories can produce silently incomplete file/review lists unless the snapshot records that ceiling.

**Acceptance criteria:** follow public pagination within user-configurable hard caps; retain stable sorting; record pages/items/truncation for each endpoint; respect rate-limit failures without partial overwrite; preserve public-only validation and token secrecy.

**Test plan:** mock multi-page, empty, repeated, truncated, rate-limited, malformed, and mid-fetch failure responses; assert atomic snapshot output and deterministic normalization.

**Skills:** HTTP pagination, failure handling, API boundaries, Python mocking. **Estimated scope:** 2–4 days. **Likely files:** `reviewbus.py`, `tests/test_reviewbus.py`, `docs/ARCHITECTURE.md`, `docs/PRIVACY.md`, `README.md`.

## 5. Carry path renames through the graph

**Issue:** [#8](https://github.com/Akhilesh-Gogikar/reviewbus/issues/8)

**Labels:** `advanced`, `metrics`, `compatibility`, `difficulty: advanced`, `size: L`, `status: ready`

**Rationale:** file history can split when a public change reports `previous_filename`. Continuity is useful, but a naive merge can combine unrelated files or make reports order-dependent.

**Acceptance criteria:** normalize optional rename metadata in snapshots; define deterministic continuity and conflict rules; retain original path evidence; expose whether a metric is direct or rename-linked; handle chains/cycles conservatively; document schema impact.

**Test plan:** simple rename, chain, divergent targets, cycle, missing metadata, mixed direct/renamed events, and reversed-input determinism; add responsible-use language for ambiguous history.

**Skills:** graph normalization, deterministic algorithms, schema migrations, defensive testing. **Estimated scope:** 3–5 days. **Likely files:** `reviewbus.py`, `tests/test_reviewbus.py`, `docs/ARCHITECTURE.md`, `docs/API_STABILITY.md`, `examples/public_repo.json`.
