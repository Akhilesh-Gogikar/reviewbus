# ReviewBus

> **Private incubation repository. Do not publish or announce yet.**

Public reviewer-authority and maintainer bottleneck maps for OSS repositories.

## Problem

Contributor count hides the smaller set of people who can safely review and merge each subsystem.

## Planned v0

- Build a path-to-reviewer bipartite graph from public GitHub metadata.
- Measure review concentration, unowned paths, response latency, timezone handoffs, and review-authority bus factor.
- Render a correction-friendly static report and optional CODEOWNERS suggestions.

## Non-goals

- Employee performance scoring or maintainer shaming.
- Automatic issue closure, reviewer assignment, or governance decisions.
- Scanning private repositories in v0.

## Repository state

This repository contains only the clean-room project brief and planning scaffold. No implementation has started.

- Scope and exclusions: [SCOPE.md](SCOPE.md)
- Source/provenance log: [PROVENANCE.md](PROVENANCE.md)
- Initial execution plan: [docs/PLAN.md](docs/PLAN.md)

## Licensing

No public license is granted while this repository is private. Select an OSS license only after ownership and third-party provenance review.
