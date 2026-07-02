# Evidence Packet: NS-13 - Energy Huber Delta

## Header

| Field | Value |
|---|---|
| ID | `NS-13` |
| Title | Energy Huber delta |
| Severity | `MAJOR` |
| Current Status | `IN_PROGRESS` |
| Current Verdict | `defer-with-blocker` |
| Phase | `Phase 35` |
| Owner Phase | `Phase 35` |
| Consumer Phase | `Phase 36` |
| Acceptance Check ID | `AC-LOSS-03` |
| Spec Sections Touched | `ctl_instruction.md` Loss Function Formulation; `pinn_architecture.md` §3.4 Soft Energy Conservation Regularizer |
| Code Paths Touched | `Not code-applicable` |

## Source Positions

Neither source is authoritative. The issue doc is a non-authoritative conflict source, and the final resolution doc is a candidate verdict source consumed under the Phase 32 evidence protocol.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:109`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:169-181`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:444` | Non-authoritative issue source | The issue doc says `delta=1.0` may be too large for normalized energy residuals, proposes tuning `delta_energy` from observed `|Delta H|` quantiles, and names `0.01-0.1` as a starting range. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `03-final-resolution.md:72-74` (§1.13 NS-13); `03-final-resolution.md:155-157` (NS13-01..03); `03-final-resolution.md:203` (DGR-14); `03-final-resolution.md:232` (GAP-14) | Candidate verdict source, not authority | §1.13 records a `defer` verdict: `delta_E = 1.0` remains the configurable current baseline, no normalized `|Delta H|` distribution supports immediate change to `0.1` or `0.01-0.1`, and quantiles, linear-branch occupancy, validation energy drift, and weighted gradients must be measured before changing the value or making it stage-dependent. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:58`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:93`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:152`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:211` | Navigation / line-map aid | Maps NS-13 to §1.13 lines 72-75, marks it covered with routing, records `defer`, and routes GAP-14 to Phase 35 LOSS-03. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:493-531` defines the soft energy conservation regularizer and sets the Huber transition to `delta = 1.0`.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:590-603` states that energy and physics use the same dimensionless unit system, the same `epsilon_train = 1e-5` softening, and the same collocation points.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1722-1751` defines the total-loss assembly by reference to the PHYS-05 loss-term catalog and states that Phase 35 owns the component definition, weight schedule, and Huber-delta calibration details.

No framework spec is edited by this packet.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:16` and `.planning/REQUIREMENTS.md:92-95` define SCOPE-12 through SCOPE-15: locked v1.4/v1.5 outcomes are hard constraints; v1.6 spec edits are limited to `ctl_instruction.md` and `pinn_architecture.md`; training-loop code and empirical EDA remain FUT.
- `.planning/phases/35-loss-energy-weight-contracts/35-SPEC.md:34-39` states the Phase 35 target for LOSS-03: keep `delta_E = 1.0` as baseline, defer per-stage `|Delta H|` quantile calibration pending measured evidence, and do not invent a per-stage table.
- `.planning/phases/35-loss-energy-weight-contracts/35-CONTEXT.md:119-126` records D-35-08 with the same baseline and measurement prerequisites.

No dataset evidence is available in this phase for the normalized `|Delta H|` distribution or branch occupancy; that absence is the reason for the deferral.

## FUT Hand-off Note

- FUT path / note: a later calibration/FUT task may measure normalized `|Delta H|` quantiles, linear-branch occupancy, validation energy drift, and weighted gradients before changing `delta_E`. Live `pinn/` code is NOT grounding evidence and is not cited here.
- Not FUT-applicable: This packet records only the evidence status and deferred calibration route.

## First-Principles or Engineering Check

1. **Huber branch behavior:** A Huber transition changes where the residual switches from quadratic to linear behavior. Choosing it requires the residual scale distribution, otherwise the branch occupancy is unknown.
2. **Validation coupling:** Reducing `delta_E` could increase robustness to outliers but also change gradient magnitudes and validation energy drift; the resolution doc therefore requires measured quantiles, occupancy, drift, and weighted-gradient evidence.
3. **Baseline preservation:** The current spec already has `delta_E = 1.0`; without the missing measurements, changing it or making it stage-dependent would be a fabricated numeric calibration.

## Verdict

Verdict: `defer-with-blocker` (resolution-doc NS-13 position: `defer`; retain `delta_E = 1.0` baseline)

Explicit user instruction: None beyond the Phase 35 SPEC/CONTEXT lock.

Reasoning:

- The candidate resolution doc §1.13 accepts the current baseline and explicitly defers any immediate change to `0.1` or `0.01-0.1`.
- NS13-02, NS13-03, DGR-14, and GAP-14 all identify missing empirical evidence or decision routing rather than a current replacement value.
- The current framework spec already defines `delta_E = 1.0`; Phase 35 later spec edits should tag that baseline and name the measurement prerequisites, not invent a per-stage table.

## Root-Cause Ambiguity

The issue doc treated an uncalibrated Huber transition as a prompt to choose a smaller numeric range. The current spec had a baseline value but no distributional evidence. The root ambiguity is calibration evidence, not the existence of the energy Huber term.

## Locked Convention or Owner Route

Deferred route for Phase 35 transcription:

```text
NS-13 / LOSS-03:
- Keep delta_E = 1.0 as the configurable current baseline.
- Treat 0.01-0.1 only as deferred calibration evidence, not as a locked table.
- Measure normalized |Delta H| quantiles, linear-branch occupancy,
  validation energy drift, and weighted gradients before changing delta_E
  or making it stage-dependent.
```

## Which Source Was Correct / Wrong

- Issue doc: correct that `delta_E = 1.0` may need calibration; not authoritative for an immediate smaller range or per-stage value.
- Resolution doc: correct in retaining the baseline and deferring calibration until the required measurements exist.
- Current specs: correct baseline value; later Phase 35 edits should annotate the deferred status and measurement prerequisites.

## Before / After or Intentional Non-Change Note

**Before:** `pinn_architecture.md:493-531` defines the energy Huber transition as `delta = 1.0`, but the section is not tagged as the Phase 35 NS-13 / LOSS-03 `defer` verdict and does not yet name the calibration evidence prerequisites.

**After:** Phase 35 spec-edit plans should add a LOSS-03 callout and deferred-calibration note while preserving `delta_E = 1.0`. The `0.01-0.1` range may appear only as deferred calibration evidence, never as a locked table.

## Named Acceptance Check

AC-LOSS-03

Planned pass criterion: the edited framework specs expose `LOSS-03`, `NS-13`, `defer`, and `delta_E = 1.0`; the `0.01-0.1` range appears only as deferred calibration evidence; the measurement prerequisites are named; no per-stage Huber-delta table is invented.

Owning phase: Phase 35, with Phase 36 final structural/acceptance verification.

## STOP / Gap Handling

No STOP gap opened. The missing empirical evidence is explicitly handled by the resolution doc's `defer` disposition and GAP-14 route (`03-final-resolution.md:72-74`, `03-final-resolution.md:203`, `03-final-resolution.md:232`), so this packet records the deferral rather than inventing a numeric value.

## Status Transition Log

```text
2026-06-29 pending-commit PENDING -> IN_PROGRESS (Phase 35 Plan 35-01 Task 1 by codex-gsd-executor-35-01; packet authored, NS-13 defer consumed)
```
