---
status: active
milestone: v1.5
phase: 23-research-package-assembly
---

# Phase 23 Gap Register

## GAP-23-01 — R6 crosswalk column non-mechanical mappings

- **Status:** RESOLVED-WITH-INSTRUCTION.
- **Resolution note (2026-06-11):** user decisions applied to the crosswalk R6 column in `docs/work/plans/milestone_v1.5/23-research-package-assembly/2026-06-10-phase-23-issue-02-consolidation-agent-prompt.md`. Cells filled as:
  - Q-A1: `TrajectoryValidator at init; block causal firewalls (§3.1)`
  - Q-A2: `TrajectoryIndex mapping; resolve O(N) filter gaps (§3.2)`
  - Q-A3: `blacklist at training time; protect LayerNorm + SIREN (§3.3)`
  - Q-A4: `low-fidelity fallback with metadata flags (§3.5)`
  - Q-A5: `infer tol=1e-13 incomplete footers; tol_confidence flag (§3.6)`
  - Q-A6: `—` (D-03 not in R6 matrix)
  - Q-B1: `adaptive 0.5 * n_snapshot cap; prevent interpolation blindness (§3.4)`
  - Q-B2, Q-B3, Q-B4: `—` (Q-IDs not in R6 matrix)
  - Q-C1: `reject eps_H > 1e-5; SCS >= -5; 1e-6 diag-only (§3.8)` (gist extracted from §3.8)
  - Q-C2, Q-C3, Q-C4: `—` (no SASD/IPR/PSC sections in R6)
  - M16 §3.7: confirmed not in crosswalk (user override: confirm).
  - Shape-check passed: all 14 table rows have 9 columns; no `_` fill-markers remain.
