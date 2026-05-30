---
phase: 19-physics-and-loss-contracts
reviewed: 2026-05-30T18:40:20Z
post_reviewed: 2026-05-30T18:47:09Z
depth: standard
status: resolved_after_fixes
initial_findings:
  critical: 3
  warning: 3
  info: 0
  total: 6
post_review_findings:
  critical: 0
  warning: 1
  info: 0
  total: 1
final_findings:
  critical: 0
  warning: 0
  info: 0
  total: 0
---

# Phase 19 Code Review And Resolution Log

## Summary

The initial review found three blocking spec inconsistencies and three warnings. The post-review fixes updated the active framework specs, a follow-up reviewer caught one grounded sampler-field typo, and the Phase 19 structural suite plus targeted review guards were rerun successfully.

## Findings

| ID | Severity | Status | Resolution |
|---|---|---|---|
| CR-01 | BLOCKER | RESOLVED | `pinn_architecture.md:407` now defines per-time residual energy, causal weights with `stopgrad`, and `L_{phys}^{causal}` as the default physics loss consumed by `L_total`; the unweighted mean is diagnostic only. |
| CR-02 | BLOCKER | RESOLVED | `pinn_architecture.md:432` samples normalized physics time `u in [0, 1]`, and `pinn_architecture.md:739` instructs inference through `u_eval=t_eval/T`, wrapper-computed `tau=2u-1`, and differentiation with respect to canonical leaf `u`. |
| CR-03 | BLOCKER | RESOLVED | `ctl_instruction.md:1266` uses the persisted PHYS-04/D-20 denominator floor `epsilon_H = 1e-4 * S_H` in the stage-transition energy gate. |
| WR-01 | WARNING | RESOLVED | `ctl_instruction.md:1408` now describes `loss.yaml` as default loss weights, PHYS-05 warmup, causal residual settings, conservation regularizer scales, and tolerances. |
| WR-02 | WARNING | LIFECYCLE | `.planning/REQUIREMENTS.md` remains a phase-completion lifecycle update handled by `phase.complete`, not a spec blocker. |
| WR-03 | WARNING | RESOLVED | `pinn_architecture.md:554` has `TrajectoryDataset.__init__` and `compute_initial_energy` indented under the class. |
| WR-04 | WARNING | RESOLVED | `pinn_architecture.md:460` now samples adaptive collocation points from canonical trajectory field `traj_data['u']`, matching `ctl_instruction.md:638` and `ctl_pinn_resolution.md:434`. |

## Post-Review Validation

- Reran the full Phase 19 structural verifier for `AC-PHYS-01` through `AC-PHYS-06`: PASS.
- Reran targeted review guards for causal physics loss, canonical `u`-domain collocation/inference, `epsilon_H` stage gate, `loss.yaml` wording, and stale-string negative checks: PASS.
- Ran `git diff --check`: PASS.
- Confirmed no staged or unstaged `pinn/` diff exists: PASS.
