---
phase: 21
slug: acceptance-checks-and-handoff
status: repaired
created: 2026-06-08
---

# Phase 21 Research - Acceptance Checks and Handoff

## Executive Summary

Phase 21 is validation infrastructure, not a new adjudication phase. Its job is to make the previously resolved v1.4 spec contracts executable and hand off the remaining cleanup state to Phase 22. The repair pass found that the Section 10 acceptance checks exist, but the prior evidence artifact was not sufficient because it did not preserve raw stdout and several probes were too weak. The repaired suite now has five executable probes, per-probe stdout evidence, and a grounded handoff.

## Route Map by Requirement

| Requirement | Grounding | Phase 21 artifact |
|---|---|---|
| `VER-01` | `.planning/REQUIREMENTS.md:60`; `pinn_architecture.md:984-1009` | Section 10 acceptance checks with `.venv/bin/python` commands |
| `VER-03` | `.planning/REQUIREMENTS.md:62`; ledger M6/M7 deferrals at `16-ISSUE-LEDGER.md:303-328` | `21-HANDOFF.md` |
| `VER-04` | `.planning/REQUIREMENTS.md:63` | `21-PROBE-RESULTS.md` plus `evidence/*.stdout.txt` |
| `VER-05` | `.planning/REQUIREMENTS.md:64`; ledger lifecycle rules at `16-ISSUE-LEDGER.md:45-55` | `16-ISSUE-LEDGER.md` Phase 21 addendum and `21-VERIFICATION.md` |
| `VER-06` | `.planning/REQUIREMENTS.md:65` | `16-ISSUE-LEDGER.md` addendum and `21-HANDOFF.md` |

## Probe Design Grounding

### 10.1 Scaling Consistency

Grounded by the raw-mass nondimensionalization convention: the scaled residual has no free gravitational coefficient because `D^3 = G*T^2`. The repaired probe uses non-unit `T` cases and verifies both the residual coefficient and acceleration rescaling.

### 10.2 COM Invariance

Grounded by the mass-weighted output projection in `pinn_architecture.md:814-838`. The probe uses ordered raw masses and deterministic raw positions, then checks the projected mass-weighted COM norm.

### 10.3 Componentwise AD

Grounded by the normalized-time derivative contract in `pinn_architecture.md:840-907`, especially the explicit loop over components and synthetic trajectory. The probe compares AD to the symbolic derivative for `r(u) = [sin(2*pi*u), cos(2*pi*u), u^2]`.

### 10.4 Force-Energy Consistency

Grounded by the matched Plummer residual at `pinn_architecture.md:374-389` and the matched-Plummer Hamiltonian at `pinn_architecture.md:496-536`. The repaired probe checks that the manual acceleration residual equals `-dV/dx / m_i` with `epsilon_train = 1e-5`, and that `H_epsilon` is finite.

### 10.5 Loss Stability

Grounded by the SQR-SkipResNet-SIREN, LayerNorm, output, AD, physics, IC, energy, and angular momentum contracts in `pinn_architecture.md`. The repaired probe instantiates a representative 14D-input, 9D-output SIREN/skip/LayerNorm model and computes finite data, IC, physics, energy, and angular-momentum losses.

## SI-Ledger Research

- `SI-CTL-001` exists in `ctl_instruction.md` and is retired with "Resolved by v1.4 finding B-03. See Phase 17 input contract."
- `SI-SSR-001` exists in `stage_strat_revision.md` and is retired with "Resolved by v1.4 finding M5. See Phase 20 architecture and normalization cleanup."
- `SI-PINN-001` is not present in the current framework-spec SI sections and was not present there at `v1.4-pre-phase-21`; it appears only in planning references.
- Unrelated SI entries preserved: `SI-PINN-002`, `SI-PINN-003`, `SI-DQA-002`, and `SI-DQA-003`.

## Closure Proof

Fresh probe execution on 2026-06-08 produced exit code 0 for all five probes. `21-PROBE-RESULTS.md` records the observed metrics and SHA-256 hashes for the raw stdout evidence.
