# Phase 54 Gap Register — Recalibration Decision Grounding

Phase-local STOP-protocol gap register for Phase 54 (milestone v2.3). Each entry
is a source-silent decision that this phase **surfaced** rather than decided, per
the CLAUDE.md STOP protocol. The milestone-wide index is
`.planning/milestones/v2.3-GAPS.md` (created by this phase on its first gap,
under the standing first-gap trigger).

Per D-10, this register carries **one anchor entry** covering both owner
checkpoints ① and ②. The packet itself is the surfacing instrument: the full
enumeration of what the assembled evidence cannot answer lives in the packet's
`## 7. What the assembled evidence cannot answer` section
(`pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md`),
and this entry points at it rather than duplicating it. (The alternative — one
record per recalibration sub-question — is flagged to the owner as 54-CONTEXT.md
Open Item 2 and can be expanded into per-surface records without rework.)

## GAP-54-01 — The causal-weight / SIREN-scale recalibration: which of the five decision surfaces change and to what, and which branch of checkpoint ① is taken to decide it

- **Decision point:** The recalibration decision VER-20 item (e) routes into v2.3: which of the five decision surfaces — `η_c` (the causal-weight exponent coefficient), the `R̄` normalization and its reference scale, `ω₀` / `first_omega_0` (the SIREN initialization scale), `N_t` / `n_col` (the collocation-point count), and the causal-exponent clip's declared semantics — change, and to what, and which branch of checkpoint ① (rule directly, or commission `trainex-r3`) is taken to decide it. No candidate is offered for any surface.

- **Where in artifact:** The packet at `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md`, sections `## 4. The confirmed mechanism and the coupled decision surfaces` and `## 7. What the assembled evidence cannot answer` (the enumeration this entry points at by heading; §7's content lands with plan 54-04); plus `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md:28-51` item (e) as the routing authority.

- **Task context:** Phase 54, ERW-01 decision-packet assembly under SCOPE-34 (the recalibration decision is owner-ratified, never agent-decided).

- **Classification:** **semantic** — SCOPE-34's own text invokes the STOP protocol's semantic / MUST-surface class for every recalibration sub-question, and a different disposition changes what Phase 56 may write into the framework spec.

- **Source silence:**
  - `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:435`, `:445`, `:181`, `:454`, `:461`, `:668-671` — fix the current values and their contract markers (the `w_n` formula and the `eta_c = 1` Phase 35 contract block, the fixed-at-30 `first_omega_0` sentence, the `n_col=4096` signature and its stated range, the clip's underflow-only purpose), but do not state any recalibrated value, form, normalization, or bound.
  - `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md:28-51` — item (e) explicitly declares that the correct calibration is a research question rather than an engineering default, and routes the decision to the owner-governed channel.
  - The trainex-r2 round's output contract §7 clause 3 forbade that round from naming a remedy, so it carries no decision sheet, no options menu, and no marked default `[r2-QUAL]` (quoted verbatim in the packet's §0).
  - `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` — establishes the mechanism (the initialization-scale chain, the underflow bound, the floored weights) but ends at diagnosis; it names no recalibrated value.

- **Mathematical / engineering grounding:** `w_n` is an **exclusive** prefix sum over collocation points — `cumsum_excl[n] = Σ_{m<n} R̄_m.detach()`, implemented by right-shifting a `torch.cumsum` and prepending a zero (`pinn/loss_catalog.py:326-342`) — so the exponent at point *n* grows with the count of preceding points, and the spec's `n_col = 4096` (`pinn_architecture.md:454`) against the run's `collocation_count = 16` (`pinn/train.py:1033`) differs by the exact factor `4096 / 16 = 256`. The float32 exponential underflows once its argument exceeds the threshold transcribed in the audit (`2026-08-17-residual-frame-conformance-audit.md:127`), so an unnormalized `R̄` near 10¹⁰ saturates the weighting shut at step 0 rather than degrading it gradually — the observed 15-of-16 floored weights (`:121`). Consequence per surface: a changed `η_c` without an `N_t` disposition leaves the exponent magnitude undetermined (SPEC-06's joint-ratification requirement, roadmap SC-5); an `R̄` normalization without a stated reference scale leaves the formula's units undefined; a changed `first_omega_0` shifts the second-derivative magnitude the whole causal mechanism is calibrated against (`:181`); and the clip's numeric bound, if any, interacts with whichever of those changes (`:668-671`). Each surface therefore changes what Phase 56 may legally write into the framework spec, which is why none of them is agent-disposable.

- **Agent was tempted to:** No candidate was formed, and none is recorded: SCOPE-34 removes the choice from the agent's authority by construction, so the packet is written as the surfacing instrument and the enumeration of what remains undecided lives in the packet's §7 rather than in an agent-held preference.

- **What the user needs to decide:** Two checkpoints, in order. Checkpoint ①: the branch — rule directly, or commission `trainex-r3`. Checkpoint ②: the per-surface disposition, plus the SCOPE-38 re-ratification of each locked contract the pick amends. A ruling that does not dispose of `N_t` / `n_col` is incomplete under roadmap Success Criterion 5 and SPEC-06's joint-ratification requirement, and routes back to the owner. No candidate value is offered for any surface; the only options named are the two branches at ①.

- **Confidence of impact:** **HIGH** — Phase 56 (SPEC-01 + SPEC-06) may not open without checkpoint ② being discharged, and Phases 57 and 58 follow from it.

- **Status:** OPEN

- **Resolution note:** **Checkpoint ① discharged 2026-08-21** — the owner selected `commission trainex-r3`, recorded verbatim in `.planning/phases/54-recalibration-decision-grounding/54-RULING.md`. The gap stays `OPEN` because checkpoint ② — the per-surface disposition and its SCOPE-38 re-ratifications — is what closes it, and that awaits the round's delivery, its Rule-19 verification, and owner ratification. The ruling itself is recorded in `54-RULING.md`, not here — a ruling is not a gap (D-09).

  ERW-02 assembly (2026-08-21) widened what the round is asked to consider, without disposing of anything: item (e)'s **fourth remedy family** (redesign the curriculum mechanism so it does not require the two to agree at initialization) was transcribed verbatim into the packet's §4.3 after it was found absent from the five decision surfaces, and two further open items were added to the packet's §7 — the SQR-SkipResNet stack's contribution to the same second-derivative magnitude `first_omega_0` is credited with, and the absence of any statement of the source method's own calibration procedure. See the packet's §11 amendment record.
