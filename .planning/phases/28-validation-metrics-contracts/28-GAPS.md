# 28-GAPS.md - Phase 28 STOP-Protocol Gap Register

**Phase:** 28 - Validation-Metrics Contracts
**Created:** 2026-06-16
**STOP-protocol authority:** `AGENTS.md` / `CLAUDE.md` "v1.5 applicability" + STOP-protocol field list.

## GAP-28-01 - SASD endpoint convention needs user sign-off before canonical spec edit

- **Decision point:** Should the canonical data-side SASD contract evaluate each interval using the DQA/issue-doc literal left endpoint `t_i`, or should it use the resolution doc's candidate both-endpoint maximum over `{t_i, t_{i+1}}`? This decides the endpoint convention for `ctl_instruction.md`'s future SASD clause.
- **Where in artifact:** Surfaced while authoring `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/sasd-sampling-density.md` for Phase 28 Plan 02 Task 1, before any SASD spec edit. The candidate spec edit is the future `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` `Data-side quality-metric contracts` subsection. No SASD clause has been landed.
- **Task context:** Phase 28 Plan 02 Task 1 ("Author the SASD EVID-06 packet + adjudicate the Q-C2 endpoint fork"). The plan explicitly routes outcome (b) to STOP when the evidence does not settle the fork or the resolution doc's sign-off request stands.
- **Classification:** **semantic** - this changes which trajectories may be flagged by a data-side validation metric and therefore affects resample-queue / clean-training designation semantics.
- **Source silence:**
  - `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md:138-158` defines SASD using the left endpoint `t_i`, explains `SASD > 0.5` as a resampling flag, and does not discuss right-endpoint or both-endpoint evaluation.
  - `pinn_instruction/issues/02-data-pipeline-and-validation.md:143-153` repeats a left-endpoint SASD formula and routes SASD to training-side collocation weighting, but it is non-authoritative and does not address the endpoint fork.
  - `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md:575-626` proposes both-endpoint evaluation and gives a rationale, but it also preserves CR-A's left-endpoint dissent and states the project should weigh the consolidation-generated endpoint argument directly; as a candidate verdict source it is not authority.
  - `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md:24-25` grounds the resolution context (`dt_out` and snapshot-count differences between base and gold), but those dataset facts do not decide the endpoint policy.
  - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:452-458` establishes data-side admission-gate placement but has no SASD contract and no endpoint convention.
- **Mathematical / engineering grounding:** SASD estimates whether an interval's output spacing is large relative to the local dynamical timescale, using `dt * ||a|| / ||v||`. Left-endpoint evaluation measures the interval only at `t_i`; both-endpoint max evaluates `t_i` and `t_{i+1}` and is monotone relative to left-only (`max(left,right) >= left`), so it cannot un-flag a trajectory already flagged by the DQA-literal form. It can, however, flag additional intervals, especially a spike at the final/right endpoint that left-only would never evaluate. That extra conservatism has downstream consequences: more trajectories may enter the resample queue, lose clean-training designation at base fidelity, or be marked satisfied-by-gold. The dataset's coarse base vs fine gold resolution makes the blind spot consequential, but it does not decide whether the framework should prefer literal source fidelity or conservative flag expansion.
- **Agent was tempted to:** choose both-endpoint evaluation because it is monotone, closes the final-snapshot blind spot, and matches the resolution doc's candidate text. Rejected: the resolution doc itself frames this as a genuine fork with preserved dissent and direct project sign-off, and adopting it would silently choose a semantic policy that changes flag populations.
- **What the user needs to decide:**
  - **A. Both endpoints.** Canonical SASD uses `max_{t in {t_i, t_{i+1}}}` per interval. Conservative; closes right/final-endpoint blind spot; may increase flags and resample/clean-training exclusions. This matches the resolution doc candidate.
  - **B. Left endpoint.** Canonical SASD uses the DQA/issue-doc literal `t_i` formula. Minimal deviation from the written DQA/issue sources; avoids expanding flags without explicit evidence; leaves final/right-endpoint blind spot documented.
  - **C. Defer SASD endpoint convention.** Keep VAL-02 deferred for now; Phase 28 does not land a canonical SASD clause until empirical SASD distributions or user-led research resolve the endpoint convention.
- **Confidence of impact:** **HIGH** - the endpoint convention directly changes which trajectories are flagged and therefore affects downstream resampling and clean-training designation. It blocks the SASD spec edit but does not invalidate independent IPR/PSC evidence work if those plans can proceed without relying on a canonical SASD clause.
- **Status:** **OPEN**
- **Resolution note:**

## GAP-28-02 - IPR raw-vs-scaled unit convention needs user sign-off before canonical spec edit

- **Decision point:** Should the canonical data-side IPR contract bind `IPR > 1e-3` to raw `G=1` units, or to scaled normalized units? The same numerical threshold differs by about 464x between conventions.
- **Where in artifact:** Surfaced while authoring `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/ipr-physics-residual.md` for Phase 28 Plan 03 Task 1, before any IPR spec edit. The candidate spec edit is the future `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` IPR clause in `Data-side quality-metric contracts` plus a possible `pinn_architecture.md` dual-epsilon visibility note. No IPR clause has been landed.
- **Task context:** Phase 28 Plan 03 Task 1 ("Author the IPR EVID-06 packet + adjudicate the Q-C3 units fork"). The plan explicitly routes outcome (b) to STOP when the evidence does not settle raw vs scaled units or the calibration-tripwire sign-off cannot be discharged.
- **Classification:** **semantic** - the unit convention changes the meaning of the `1e-3` flag and therefore changes which trajectories are flagged, resampled, or treated as clean training data.
- **Source silence:**
  - `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md:160-174` defines IPR and its residual construction, but does not state raw or scaled units.
  - `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md:220-252` places IPR in a Phase-1 "Load and Normalize" workflow and gives the `IPR > 10^-3` gate; the "Load and Normalize" wording prevents the agent from treating "on load" as an unambiguous raw-units proof.
  - `pinn_instruction/issues/02-data-pipeline-and-validation.md:155-165` gives an `eps = 1e-5` training/noise-floor role and does not settle data-side units.
  - `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md:627-673` proposes raw `G=1` units and derives the ~464x distinction, but it explicitly calls units a genuine consequential fork, preserves scaled-units dissent, and relies on placement inference plus calibration tripwire.
  - `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md:24-25` grounds snapshot/dt resolution context but does not determine the unit convention for the IPR threshold.
  - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:930-935` and `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:520-535` ground the validation/training epsilon separation, not the raw/scaled IPR unit pin.
- **Mathematical / engineering grounding:** IPR is an acceleration-squared residual: `||q''_spline - F_gravity(q_spline)||^2`. Under the locked scale transform `r = D r'`, `t = T u`, acceleration scales as `D/T^2`, so squared acceleration residuals scale as `D^2/T^4`; the resolution doc's reported relationship is raw IPR roughly scaled IPR times `2.155e-3`, equivalently scaled readings about 464x larger. Therefore a unitless-looking `1e-3` flag is not portable across raw/scaled conventions. Raw units align with the resolution doc's candidate and Q-C1/Q-C2 raw-array convention; scaled units align with a normalized preprocessing interpretation and CR-A's preserved dissent. The dataset facts show that aliasing diagnostics matter, but do not prove which unit convention authored the original threshold.
- **Agent was tempted to:** choose raw `G=1` units because the resolution doc offers a detailed candidate, raw aligns with the SCS convention, and the dimension analysis is clear. Rejected: the DQA "Load and Normalize" wording keeps the placement inference ambiguous, the resolution doc itself preserved scaled-units dissent, and a ~464x threshold change is too consequential for agent inference.
- **What the user needs to decide:**
  - **A. Raw units.** Canonical data-side IPR is computed on parsed raw `G=1` arrays, and `IPR > 1e-3` is a raw-unit flag. This matches the resolution doc candidate and requires distribution calibration as a tripwire.
  - **B. Scaled units.** Canonical data-side IPR is computed after locked scaling/normalized time, and `IPR > 1e-3` is a scaled-unit flag. This preserves the scaled-units dissent and likely flags many more trajectories for the same number.
  - **C. Defer IPR unit convention.** Keep VAL-03 deferred until empirical IPR distributions or user-led research resolves which convention the `1e-3` threshold was intended to bind.
- **Confidence of impact:** **HIGH** - raw vs scaled units change the threshold interpretation by about 464x. A wrong pin can materially over-flag or under-flag trajectories and mislead Phase 29 acceptance thresholds.
- **Status:** **OPEN**
- **Resolution note:**

## Milestone-wide index

Mirrored at `.planning/milestones/v1.5-GAPS.md` (Phase 28 section).
