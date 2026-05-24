---
title: EDL Registry
status: draft
scope: project-wide EDL index
created: 2026-05-24
canonical: false
---

# EDL Registry

This registry tracks central Empirical Decision Loop research-support artifacts. It is not the canonical blocking record. Phase-local gap registers own blocking status and final resolution.

## Status Values

- `OPEN-RESEARCH-NEEDED`: research brief exists and waits on user research.
- `USER-RESEARCHING`: user has taken the research task externally.
- `RESOLVED-WITH-INSTRUCTION`: user supplied enough instruction to resolve the linked gap.
- `DEFERRED-TO-EDL`: user deferred empirical work while allowing scoped progress.
- `EDL-APPROVED`: user approved designing and running a probe now.
- `EDL-COMPLETE`: probe ran and decision record is available.
- `BLOCKED`: no safe independent work remains until the decision is resolved.

## Registry

| EDL ID | Linked gap | Topic | Status | Brief | Blocking summary |
|--------|------------|-------|--------|-------|------------------|
| EDL-19-01 | `GAP-19-01` | `epsilon_H` energy-drift denominator floor | OPEN-RESEARCH-NEEDED | `.planning/research/edl/EDL-19-01-epsilon-H.md` | Blocks numeric `epsilon_H` default and dependent `L_E` / loss-stability probe design; unrelated Phase 19 work may continue. |

## Notes

- Add new entries only after the source-silent decision is recorded in the relevant phase gap register.
- Keep this index concise. The detailed research context belongs in the linked brief.
- A registry status update does not resolve the linked gap by itself; update the phase gap register when the user gives instruction.
