# Phase 18: Frame and Gauge Contracts - Pattern Map

**Mapped:** 2026-05-20
**Files analyzed:** 8 implementation targets
**Analogs found:** 8 / 8
**Scope:** Documentation/spec adjudication only. Do not edit `pinn/`; live `pinn/` references are FUT-01 hand-off coordinates only, not v1.4 grounding evidence.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md` | documentation evidence packet | file-I/O + adjudication | `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | exact |
| `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M3.md` | documentation evidence packet | file-I/O + adjudication | `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | exact |
| `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` | documentation ledger | event-driven + batch index | same file status table and per-finding notes | exact self-edit |
| `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` | framework spec | transform | same file Step 2/2.5/4 + `ctl_pinn_resolution.md` sections 4.1-4.6 and 10.2 | exact self-edit |
| `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | framework spec | cross-reference | same file Section 5.3 + Phase 17 output contract | exact self-edit |
| `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` | framework spec | transform | same file Stage 1 + `simulation_data/Scripts/ic_generation/` algorithms | exact self-edit |
| `.planning/phases/18-frame-and-gauge-contracts/18-CODE-DIVERGENCE.md` | hand-off register | batch + file-I/O | `.planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md` | role-match |
| `.planning/milestones/v1.4-GAPS.md` | milestone coordination index | cross-phase notice | existing Phase 18 heads-up row | already present |

Workflow artifacts such as `18-01-PLAN.md`, `18-02-PLAN.md`, `18-03-PLAN.md`, summaries, and verification reports are planner/executor outputs, not implementation targets for this map.

## Pattern Assignments

### Evidence Packets: `B-05.md`, `M3.md`

**Analog:** `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md`

Use the full 12-section template. Both findings are non-EVID-05 because the issue doc and resolution doc agree, so keep EVID-05-only headings and write `Not contested; sources agree after the Phase 18 FRAME-01 contract is applied.`

Header values:

| Packet | Title | Severity | Verdict | AC |
|---|---|---|---|---|
| `B-05.md` | `COM frame consistency` | `BLOCKING` | `accept-resolution` | `AC-FRAME-01` |
| `M3.md` | `Scaling order and COM transform order` | `MAJOR` | `accept-resolution` | `AC-FRAME-01` |

### `ctl_instruction.md`

**Analog:** same file Step 2, Step 2.5, Step 4.

Replace current Step 2/2.5 with one unified section. Move the canonical-ordering procedure out of Step 4 and into Step 2.3, using the resolution-doc tie-break order:

1. descending raw mass;
2. descending norm of COM-corrected initial position;
3. descending norm of COM-corrected initial velocity;
4. original file order.

Leave the Step 4 Mathematical Guarantees block untouched. In particular, do not edit the sentence containing `13 constraints for an 8-dimensional reduced phase space`.

### `pinn_architecture.md`

**Analog:** Section 5.3 Output Frame and File Format.

Use this as a cross-reference surface only. The hard COM projection is already Phase 17's output contract. Phase 18 may add a short FRAME-02 note that the projected output has mass-weighted COM zero by construction and AD-derived velocities/accelerations inherit the same zero-COM derivative property.

### `sampling_method.md`

**Analog:** Stage 1 hierarchical and quasi-random sections.

The executable worker must verify claims against `simulation_data/Scripts/ic_generation/generate_ics.py` and `simulation_data/Scripts/ic_generation/ic_generation_utils.py` before editing. Confine prose changes to:

- hierarchical Gaussian perturbation after COM/P enforcement;
- quasi-random equal-mass COM/P construction;
- a forward reference that FRAME-01 preprocessing is applied universally.

Do not rewrite the Sobol coordinate-allocation formula. Phase 20.5 owns that.

### `18-CODE-DIVERGENCE.md`

**Analog:** `.planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md`

Use the same five-column schema:

| Surface | Live code (file:line) | Spec target (Phase 18 decision) | FUT-01 item | FUT-01 priority |
|---|---|---|---|---|

Allowed live `pinn/` references are FUT-01 hand-off references only. The divergence file should cover expected gaps around COM-first preprocessing, ordering tie-breaks, rotation gauge, scaling order, and model-output metadata threading.
