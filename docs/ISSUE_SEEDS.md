# Issue seeds

These are ready-to-file proposals, not promises. Confirm the code still matches each seed before creating the issue. All tests and examples must use invented public-shaped data.

## 1. Show the analyzed pull-request bounds

**Proposed title:** `Add explicit pull-request sample bounds to every ReviewBus report`

**Labels:** `good first issue`, `help wanted`, `reporting`

**Rationale:** `summary.pull_requests` gives a count but not the minimum/maximum PR number in the bundle. Reviewers need basic sample context before interpreting an unowned path or concentration value.

**Acceptance criteria:** add deterministic minimum/maximum PR numbers (or `null` for an empty bundle) to JSON and visible HTML methodology; do not imply chronological completeness; document the schema addition.

**Test plan:** cover empty, one-PR, unordered, and duplicate-number inputs; verify reversed input produces identical output; assert accessible HTML labels.

**Skills:** beginner Python, JSON, HTML. **Estimated scope:** 2–4 hours. **Likely files:** `reviewbus.py`, `tests/test_reviewbus.py`, `docs/API_STABILITY.md`, `README.md`.

## 2. Add median response time beside the mean

**Proposed title:** `Report median review response hours without hiding sample counts`

**Labels:** `good first issue`, `help wanted`, `metrics`

**Rationale:** the arithmetic mean is sensitive to long tails. A median is useful only when the number of qualifying events remains visible and empty samples remain explicit.

**Acceptance criteria:** implement a small standard-library median helper; add path/reviewer median fields without removing mean/count; use `null` for no events; define rounding and deterministic behavior in methodology.

**Test plan:** table-driven odd/even/empty/duplicate values, integration against the fixture, JSON determinism, and HTML text assertions.

**Skills:** beginner Python, descriptive statistics, testing. **Estimated scope:** 3–5 hours. **Likely files:** `reviewbus.py`, `tests/test_reviewbus.py`, `docs/ARCHITECTURE.md`, `docs/API_STABILITY.md`.

## 3. Design a separate corrections file

**Proposed title:** `Add versioned reviewer-alias and path-owner corrections without rewriting observations`

**Labels:** `help wanted`, `design needed`, `responsible-use`

**Rationale:** renamed accounts and maintainer corrections should improve suggestions without erasing what the public snapshot contained.

**Acceptance criteria:** agree on a minimal versioned JSON format; keep observed and corrected values separate; show every applied/stale correction; validate logins/paths; never auto-assign or mutate remote files; document privacy and compatibility.

**Test plan:** aliases, cycles, invalid logins, unknown paths, explicit unowned overrides, stale entries, deterministic ordering, and end-to-end CLI artifact checks.

**Skills:** data modeling, validation, privacy, CLI/API design. **Estimated scope:** 1–2 days after design approval. **Likely files:** `reviewbus.py`, `tests/test_reviewbus.py`, `docs/API_STABILITY.md`, `docs/PRIVACY.md`, `README.md`.

## 4. Paginate public fetches with explicit caps

**Proposed title:** `Add deterministic public-fetch pagination and snapshot completeness metadata`

**Labels:** `help wanted`, `advanced`, `fetch`

**Rationale:** 0.1 reads one page per endpoint. Larger public repositories can produce silently incomplete file/review lists unless the snapshot records that ceiling.

**Acceptance criteria:** follow public pagination within user-configurable hard caps; retain stable sorting; record pages/items/truncation for each endpoint; respect rate-limit failures without partial overwrite; preserve public-only validation and token secrecy.

**Test plan:** mock multi-page, empty, repeated, truncated, rate-limited, malformed, and mid-fetch failure responses; assert atomic snapshot output and deterministic normalization.

**Skills:** HTTP pagination, failure handling, API boundaries, Python mocking. **Estimated scope:** 2–4 days. **Likely files:** `reviewbus.py`, `tests/test_reviewbus.py`, `docs/ARCHITECTURE.md`, `docs/PRIVACY.md`, `README.md`.

## 5. Carry path renames through the graph

**Proposed title:** `Model public file renames without silently merging unrelated paths`

**Labels:** `advanced`, `metrics`, `compatibility`

**Rationale:** file history can split when a public change reports `previous_filename`. Continuity is useful, but a naive merge can combine unrelated files or make reports order-dependent.

**Acceptance criteria:** normalize optional rename metadata in snapshots; define deterministic continuity and conflict rules; retain original path evidence; expose whether a metric is direct or rename-linked; handle chains/cycles conservatively; document schema impact.

**Test plan:** simple rename, chain, divergent targets, cycle, missing metadata, mixed direct/renamed events, and reversed-input determinism; add responsible-use language for ambiguous history.

**Skills:** graph normalization, deterministic algorithms, schema migrations, defensive testing. **Estimated scope:** 3–5 days. **Likely files:** `reviewbus.py`, `tests/test_reviewbus.py`, `docs/ARCHITECTURE.md`, `docs/API_STABILITY.md`, `examples/public_repo.json`.
