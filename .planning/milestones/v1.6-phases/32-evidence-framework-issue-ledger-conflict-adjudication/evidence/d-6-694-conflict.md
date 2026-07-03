# Evidence Packet: D = 6.694 - Raw-Mass D Conflict

## Header

| Field | Value |
|---|---|
| ID | `D = 6.694` |
| Title | Raw-mass D conflict |
| Severity | BLOCKING |
| Current Status | VERIFIED |
| Current Verdict | accept-resolution |
| Phase | Phase 32 |
| Owner Phase | Phase 32 |
| Consumer Phase | Phase 33 CURR-02; Phase 36 provenance/deferred-list checker |
| Acceptance Check ID | AC-EVID-15-D-CONFLICT |
| Spec Sections Touched | None in Phase 32; Phase 33 consumes current `ctl_instruction.md` global-scale convention for `tau_L` / `L_max` |
| Code Paths Touched | Not code-applicable |

## Source Positions

Neither source is authoritative. The resolution doc is a candidate verdict source, not authority; the issue doc is a non-authoritative conflict source.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:260-305`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:324-326`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:509-516` | Non-authoritative issue source | `compute_tau_L` assigns `D = np.cbrt(G * M_tot_ref * T_scale**2)  # = 6.694`, states `D = cbrt(G * M_tot_ref * T_scale^2) = 6.694`, and directs P4-1 to re-run stage assignment for all trajectories with corrected `D=6.694`. The reference section also labels live `pinn/` code as "Canonical"; that label is overridden by v1.6 governance and is not grounding. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:84-87` (section 1.16 / §1.16); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:169-172` (D-conflict claim_id rows `D-01` through `D-04`); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:206`; `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:235` | candidate verdict source, not authority | Section 1.16 accepts `D = (G T^2)^(1/3) ~= 4.6416`, rejects `D = 6.694` and P4-1, records that the issue-doc pseudocode's local `D` / `V` assignments are dead in that snippet, and defers only GAP-17 prior-artifact provenance. Claim rows distinguish `D-01` accepted convention, `D-02` rejected `6.694`, `D-03` pseudocode inspection, and D-conflict claim_id D-04 provenance deferral; this is distinct from the causal-decision finding `D-04`. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:61-63`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:96-98`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:155-157`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:171-176` | Navigation / line-map aid | The map anchors §1.16 to lines 84-87, maps `D = 6.694` to covered status, previews `accepted / rejected`, and states Phase 32 EVID-15 may revisit SCOPE-12 only with new first-principles evidence surfaced as a gap. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:897-913` defines global scaling with `T = 10`, `D = (G*T**2)^(1/3)`, and `D ~ 4.6416`.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:915-929` locks the governing raw-mass convention: substituting `r = D r'` and `t = T u` into Newton's equation with raw masses forces `D^3 = G T^2`; the mass-fraction alternative `D = (G M_tot T^2)^(1/3) ~= 6.694` is future-only and rejected as a pipeline instruction.

No framework spec is edited in Phase 32.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:16-18` makes locked v1.4/v1.5 outcomes hard-constraint grounding and explicitly includes the raw-mass D convention with `D = 6.694` rejected.
- `.planning/REQUIREMENTS.md:90-99` states SCOPE-12 through SCOPE-15: v1.6 reconciles against the locked raw-mass convention, spec edits are limited to later `ctl_instruction.md` / `pinn_architecture.md` work, and live `pinn/` code is out of scope and not grounding.
- `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md:46-82` records the v1.5 first-principles dimensional check and `accept-resolution` verdict for raw-mass `D ~= 4.6416`.
- `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md:84-123` records the root-cause ambiguity, locked convention, source correctness, and before/after note that the D value itself does not change.

## FUT Hand-off Note

- FUT path / note: Not applicable to this Phase 32 packet.
- Not FUT-applicable: The issue-doc references to `pinn/data-processing-pipeline-full.py` and `pinn/basic_architecture.py` at `pinn_instruction/issues/03-curriculum-and-training-loop.md:515-516` are NOT grounding and are not used as evidence here. Any executable code divergence belongs to FUT-01/FUT-04 after framework specs are settled.

## First-Principles or Engineering Check

Start from Newton's equation with raw masses:

```text
d^2 r_i / dt^2 = G * sum_{j != i} m_j * (r_j - r_i) / ||r_j - r_i||^3
```

Substitute `r = D r'` and `t = T u`. The acceleration term contributes `(D / T^2) d^2 r_i' / du^2`; the force term contributes `G * sum m_j * D(r_j' - r_i') / D^3 ||r_j' - r_i'||^3`. Multiplying by `T^2 / D` yields:

```text
d^2 r_i' / du^2 = (G*T^2/D^3) * sum_{j != i} m_j * (r_j' - r_i') / ||r_j' - r_i'||^3
```

The current framework keeps raw masses `m_j` in the residual with unit coefficient, so `G*T^2/D^3 = 1` and `D = (G*T^2)^(1/3)`. For `G = 1`, `T = 10`, this gives `D = cbrt(100) = 4.6415888336`, recorded in this packet as `D ~= 4.6416`.

The issue-doc value `D = 6.694` is `cbrt(G*M_tot*T^2)` with `M_tot = 3`, i.e. `cbrt(300) = 6.6943295`. That value is arithmetically correct only under a mass-fraction convention where masses in the residual become `m_j / M_tot`. It is not a local correction to the raw-mass framework; it is a framework-wide convention migration.

The engineering consequence matches the v1.5 packet: half-adopting the mass-fraction D changes scaled positions, velocities, Hamiltonian components, stage thresholds, normalizers, and processed stores without changing every residual, Hamiltonian, angular-momentum, COM, and invariant formula. The issue-doc P4-1 rerun directive therefore cannot be accepted as a blanket local fix.

The `compute_tau_L` snippet itself assigns `D` and `V` but then constructs `y0` from already-scaled `r_prime` and `v_prime`; the shown body does not use `D` or `V` after assignment. That code-inspection point does not prove no external artifact used `6.694`; it only rejects a blanket claim that changing those assignments changes that displayed routine.

## Verdict

Verdict: accept-resolution

Explicit user instruction: None; the verdict is grounded by SCOPE-12, the current spec, v1.5 EVID-10, and the first-principles check above.

Reasoning:

- The raw-mass convention `D ~= 4.6416` is explicitly locked in current `ctl_instruction.md` and `.planning/REQUIREMENTS.md` SCOPE-12.
- The dimensional check independently reaches the same conclusion: raw masses with unit coefficient force `D^3 = G*T^2`, not `G*M_tot*T^2`.
- The issue-doc's `D = 6.694` is a mass-fraction convention value misframed as a local formula correction.
- The resolution doc's §1.16 is accepted only because it matches the current spec, SCOPE-12, v1.5 EVID-10, and first principles; it is not accepted by authority.

## Root-Cause Ambiguity

The root cause is a convention collision: raw-mass nondimensionalization versus mass-fraction nondimensionalization. The issue doc treats the mass-fraction length scale as a correction to the raw-mass framework. The current framework and v1.5 EVID-10 identify it as a different convention that would require a full migration, not a local D replacement.

The second ambiguity is provenance-only: GAP-17 records that the attached materials do not prove whether any processed store, threshold, or external artifact was produced under `6.694`. That gap does not reopen the D convention because it does not provide a first-principles contradiction of raw-mass scaling.

## Locked Convention or Owner Route

The convention remains locked:

```text
D = (G*T^2)^(1/3) ~= 4.6416 for G = 1, T = 10.
```

Raw masses are used throughout the framework. The mass-fraction form `D = (G*M_tot*T^2)^(1/3) ~= 6.694` remains rejected as a v1.6 pipeline/framework instruction and may only be considered as a future framework-wide rewrite with explicit user instruction.

GAP-17 is preserved as provenance-only: recompute only if provenance shows an affected artifact, not because the D convention itself is uncertain.

## Which Source Was Correct / Wrong

- Resolution doc: correct on the D convention and correct to reject the issue-doc P4-1 blanket rerun directive, after independent grounding.
- Issue doc: arithmetically correct that `cbrt(300) ~= 6.694` under `M_tot = 3`; wrong to present this as the corrected raw-mass convention or as a local rerun directive.
- Current spec / v1.5 EVID-10 / SCOPE-12: correct and governing for this packet.
- Neither source proves whether prior external artifacts were produced under `6.694`; this is why GAP-17 remains provenance-only.

## Before / After or Intentional Non-Change Note

**Before:** Current `ctl_instruction.md` already states the raw-mass D convention and rejects the mass-fraction alternative as a pipeline instruction.

**After:** Phase 32 makes no spec edit. The packet records the root-cause adjudication for downstream consumption: Phase 33 must use `D ~= 4.6416` when it transcribes `tau_L` / `L_max` contracts, and Phase 36 must check that any unresolved prior-artifact provenance is listed as provenance/deferred rather than silently assumed clean.

The issue-doc P4-1 blanket rerun directive is rejected. Recompute only if provenance shows an affected artifact.

## Named Acceptance Check

AC-EVID-15-D-CONFLICT

Planned pass criterion: this packet exists; cites issue-doc `compute_tau_L`, the `D = 6.694` statement, the P4-1 rerun directive, resolution-doc §1.16, D-conflict claim rows `D-01` through `D-04`, DGR-17, GAP-17, current `ctl_instruction.md` global-scaling lines, SCOPE-12, and v1.5 `compute-globals-D.md`; records `accept-resolution`; rejects `D = 6.694` and the blanket rerun directive; preserves GAP-17 as provenance-only; and updates `32-ISSUE-LEDGER.md` in the same plan.

Owning phase: Phase 32. Phase 36 may re-check ledger closure/provenance handling.

## STOP / Gap Handling

No STOP gap opened. The packet is grounded by locked SCOPE-12, current spec text, the v1.5 EVID-10 packet, and a short first-principles dimensional check. No genuine contradiction was found that could overturn `D ~= 4.6416`.

GAP-17 remains a provenance-only deferred caveat from the candidate resolution doc. It does not require creating `32-GAPS.md` because this packet does not invent a semantic answer about prior artifacts; it explicitly declines to declare no affected artifacts without provenance.

## Status Transition Log

```text
2026-06-21 pending-commit PENDING -> VERIFIED (Phase 32 P02 Task 1 by codex-gsd-executor-32-02)
```
