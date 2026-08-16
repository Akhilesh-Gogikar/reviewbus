# Scope

## Purpose

Contributor count hides the smaller set of people who can safely review and merge each subsystem.

## v0 boundary

- Build a path-to-reviewer bipartite graph from public GitHub metadata.
- Measure review concentration, unowned paths, response latency, timezone handoffs, and review-authority bus factor.
- Render a correction-friendly static report and optional CODEOWNERS suggestions.

## Explicit non-goals

- Employee performance scoring or maintainer shaming.
- Automatic issue closure, reviewer assignment, or governance decisions.
- Scanning private repositories in v0.

## Clean-room exclusions

- No source, fixtures, prompts, traces, schemas, requirements, or examples from private company, partner, customer, or unpublished research repositories.
- No customer or partner names, data, incidents, screenshots, or derived requirements.
- No public release until ownership, license, trademark, security, and contractual reviews are recorded.

## First proof gate

Maintainers of five public repositories can inspect, correct, and reproduce the computed reviewer graph.
