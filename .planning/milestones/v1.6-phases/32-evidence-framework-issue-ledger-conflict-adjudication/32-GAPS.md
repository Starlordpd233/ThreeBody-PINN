# Phase 32 Gap Register

STOP-protocol gaps surfaced during Phase 32 (Evidence Framework, Issue Ledger &
Conflict Adjudication). Milestone index: `.planning/milestones/v1.6-GAPS.md`.

---

## GAP-32-01 - D-04 causal-training mode owner decision

- **Decision point:** Which causal-training mode should the framework own after
  Phase 32: per-time-step causal weighting, global sampling plus scalar-only ALM,
  or a fully specified time-windowed causal-ALM design?
- **Where in artifact:** `32-ISSUE-LEDGER.md` row `D-04`;
  `evidence/d-04-causal-training-mode.md` sections `Verdict` and
  `STOP / Gap Handling`.
- **Task context:** Phase 32 closeout remediation after the D-04 evidence packet
  recorded `defer-with-blocker` and the user instructed the closeout to preserve
  D-04 as a downstream deferred owner decision.
- **Classification:** **semantic** - the decision changes the training paradigm,
  loss weighting visibility over time, ALM scope, and potentially batch-window
  construction.
- **Source silence:** `pinn_instruction/issues/03-curriculum-and-training-loop.md:16-40`
  marks D-04 as awaiting human approval and lists the three options without
  selecting one; `pinn_instruction/issues/03-curriculum-and-training-loop.md:383-410`
  explicitly recommends keeping the decision open. The candidate resolution doc
  at `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:24-27`
  says the framework owner must still select the final mode, while
  `03-final-resolution.md:106-110` records CAU-04 as `surface_to_user` and CAU-05
  as deferred/source-silent. The Phase 31 map and readiness report route the caveat
  forward without resolving it (`31-RESOLUTION-MAP.md:46-47`, `31-READINESS-REPORT.md:207-211`).
- **Mathematical / engineering grounding:** Per-time-step causal weighting changes
  the loss contribution at each time by suppressing later residuals until earlier
  residuals improve; global sampling exposes late-time residuals immediately and
  accepts temporal-causality risk; a time-windowed hybrid changes the batch
  partition, ALM locality, convergence gates, and state propagation. These are not
  equivalent presentations of the same training loop, so Phase 32 cannot infer a
  final contract from source frequency or implementation convenience.
- **Agent was tempted to:** keep the current causal-weighting baseline because the
  current specs already contain it and the resolution doc rejects dense-residual
  pseudo-ALM. That would still silently choose an owner preference among modes the
  sources deliberately leave open.
- **What the user needs to decide:**
  - **A.** Retain per-time-step causal weighting as the baseline training mode.
  - **B.** Use global sampling with scalar-only ALM while preserving the rejection
    of dense-residual pseudo-ALM.
  - **C.** Commission a fully specified time-windowed causal-ALM design before
    final loss/batch transcription.
- **Confidence of impact:** **HIGH** - the selected mode determines Phase 35
  `LOSS-04` and may affect Phase 34 `LOOP-01` if batch-windowing changes.
- **Status:** **RESOLVED-WITH-INSTRUCTION** (2026-06-26)
- **Resolution note:** Per the user's Phase 35 spec-gate instruction, Option A is
  ratified: retain the current per-time causal weighting baseline with
  `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, `w_1 = 1`, and
  `eta_c = 1`; preserve the dense-residual pseudo-ALM rejection; keep optional
  scalar-conservation ALM as deferred P2 only; and defer the numeric
  causal-exponent clip bound to FUT. Phase 35 `LOSS-04` owns transcription of
  this owner-ratified verdict and status.

---

## GAP-32-02 - D-05 s_min stage-gate frame owner decision

- **Decision point:** Should the curriculum stage gate use unsoftened geometric
  `s_min`, a softened `max(s_min, epsilon)` quantity, or an owner-defined hybrid
  frame?
- **Where in artifact:** `32-ISSUE-LEDGER.md` row `D-05`;
  `evidence/d-05-s-min-frame.md` sections `Verdict` and `STOP / Gap Handling`.
- **Task context:** Phase 32 closeout remediation after the D-05 evidence packet
  recorded `defer-with-blocker` and the user instructed the closeout to preserve
  D-05 as a downstream deferred owner decision.
- **Classification:** **semantic** - the choice changes curriculum labels and stage
  gate semantics, while loss-side matched-Plummer softening is a separate numerical
  regularization convention.
- **Source silence:** `pinn_instruction/issues/03-curriculum-and-training-loop.md:42-63`
  marks D-05 as awaiting human approval; `pinn_instruction/issues/03-curriculum-and-training-loop.md:412-418`
  recommends an unsoftened stage gate plus softened training-loss criterion but
  still says to resolve before implementation; `pinn_instruction/issues/03-curriculum-and-training-loop.md:520-528`
  records an alternative softening rationale. The candidate resolution doc at
  `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:28-31`
  says the owner must ratify the geometric gate or define a softened gate, and
  `03-final-resolution.md:111-113` / `03-final-resolution.md:191-193` preserve the
  owner decision instead of turning current baseline evidence into approval. Phase
  31 routes it forward (`31-RESOLUTION-MAP.md:47-48`, `31-READINESS-REPORT.md:207-211`).
- **Mathematical / engineering grounding:** A geometric `s_min` gate classifies
  trajectories by actual pairwise separation. A softened gate changes the stage
  boundary by replacing very close separations with an epsilon floor. Matched-Plummer
  residual and energy softening keeps training numerically stable, but that does
  not prove the curriculum label should use the same softened quantity. Changing
  the gate frame can move trajectories between stages and change downstream
  curriculum counts.
- **Agent was tempted to:** lock the unsoftened geometric gate because current
  specs and the resolution doc identify it as the baseline while preserving
  matched-Plummer loss-side behavior. That would convert "baseline exists" into
  "owner approved," which the sources do not say.
- **What the user needs to decide:**
  - **A.** Ratify unsoftened geometric `s_min` for curriculum stage gates while
    preserving matched-Plummer softening in training residual/energy terms.
  - **B.** Use a softened `max(s_min, epsilon)` gate, including an explicit epsilon.
  - **C.** Define another hybrid or alternative gate frame and record how it affects
    stage labels.
- **Confidence of impact:** **HIGH** - the gate frame directly affects Phase 33
  `CURR-05` and can alter stage assignment semantics.
- **Status:** **RESOLVED-WITH-INSTRUCTION** (2026-06-21)
- **Resolution note:** Owner (user) ratified **Option A** on 2026-06-21 via
  AskUserQuestion: the curriculum stage gate uses **unsoftened geometric `s_min`**
  (true pairwise separations), while the training residual and energy use
  **matched-Plummer** softening `r_safe = sqrt(||r||^2 + epsilon_train^2)` with
  `epsilon_train = 1e-5`, identically in force and Hamiltonian. The resolution is
  recorded in matched-Plummer terms per `03-final-resolution.md` section 1.2 / `DGR-03`;
  the issue-doc "`max(s_min, epsilon)` collision criterion" phrasing is explicitly NOT
  adopted, because a `max`/additive floor would (a) introduce a collision-loss term that
  does not exist in the specs and (b) violate the PHYS-03 anti-pattern
  (`ctl_instruction.md:1062-1067`). Phase 33 `CURR-05` transcribes the geometric gate;
  Phase 35 cites only the matched-Plummer loss-side distinction. No spec edit in Phase 32.

---

## GAP-32-03 - D-06 static epsilon strategy owner decision

- **Decision point:** Should offline static/invariant contexts retain
  `epsilon_inv = 1e-10`, collapse to `1e-5`, or reopen the already locked loss-side
  epsilon contract?
- **Where in artifact:** `32-ISSUE-LEDGER.md` row `D-06`;
  `evidence/d-06-epsilon-strategy.md` sections `Verdict` and `STOP / Gap Handling`.
- **Task context:** Phase 32 closeout remediation after the D-06 evidence packet
  recorded `defer-with-blocker` and the user instructed the closeout to preserve
  D-06 as a downstream deferred owner decision.
- **Classification:** **semantic** - the choice changes static invariant and
  validation measurements, while loss-side `epsilon_train = 1e-5` remains a locked
  matched-Plummer convention unless explicitly reopened.
- **Source silence:** `pinn_instruction/issues/03-curriculum-and-training-loop.md:65-86`
  marks D-06 as awaiting human approval and lists three strategies. The candidate
  resolution doc at `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:32-35`
  locks loss-side `epsilon_train = 1e-5` but says no sensitivity study resolves the
  static choice; `03-final-resolution.md:114-118` records EPS-03 as
  `surface_to_user` and EPS-05 as deferred; `03-final-resolution.md:193` surfaces
  the static choice. Phase 31 routes C-03 forward without resolving it
  (`31-RESOLUTION-MAP.md:48-49`, `31-READINESS-REPORT.md:207-211`).
- **Mathematical / engineering grounding:** Training residual and energy losses
  require one internally consistent Plummer form so the force and Hamiltonian use
  the same `epsilon_train = 1e-5`. Static invariant and validation measurements are
  offline diagnostics: retaining `epsilon_inv = 1e-10` preserves a near-unsoftened
  diagnostic, while collapsing to `1e-5` aligns the measurement with training
  softening but changes energy/IPR and possible stage-gate semantics. Setting
  `1e-10` everywhere would conflict with the locked loss-side contract unless the
  owner explicitly reopens it.
- **Agent was tempted to:** preserve the current dual-context baseline because it
  appears in the current specs and the resolution doc narrows the open decision to
  static/invariant context. That would still ratify a static policy without the
  owner instruction or sensitivity evidence the sources say is missing.
- **What the user needs to decide:**
  - **A.** Retain the dual-context baseline: `epsilon_inv = 1e-10` for offline
    static/invariant contexts and `epsilon_train = 1e-5` for training residual/energy.
  - **B.** Collapse offline static/invariant contexts to `1e-5` while preserving the
    locked loss-side value.
  - **C.** Reopen the loss-side contract and pursue `1e-10` everywhere or another
    replacement strategy.
- **Confidence of impact:** **HIGH** - the choice affects Phase 33 static
  invariants and Phase 35 loss-consistency cross-references.
- **Status:** **RESOLVED-WITH-INSTRUCTION** (2026-06-21)
- **Resolution note:** Owner (user) ratified the **dual-context** strategy on 2026-06-21
  via AskUserQuestion (GAP-register Option A; equals issue-doc Option B - the
  option-letter mismatch is resolved by the description, not the letter): offline
  static/invariant and data-side validation contexts retain `epsilon_inv = 1e-10`, while
  the training residual/energy retain the locked `epsilon_train = 1e-5`, matched-Plummer.
  This is the only choice consistent with both existing locks - the v1.5-locked data-side
  IPR convention `epsilon_inv = 1e-10` (GAP-28-02, 2026-06-16; `ctl_instruction.md:622-636`)
  and the locked loss-side `epsilon_train = 1e-5` - without reopening either. Option C
  (`1e-10` everywhere) stays rejected. Grounding: `review_of_framework.md` section 2.2's
  "indistinguishable from zero" argument applies to the float32 training loop (already
  honored by `epsilon_train = 1e-5`), not to float64 offline ground-truth invariants where
  near-unsoftened fidelity is the goal. **Known caveat (no blocker):** no sensitivity study
  exists (EPS-05 `defer`, GAP-04 `missing_empirical_evidence`); at the tightest encounters
  (`r <= ~1e-4`) the validation energy (`epsilon_inv`) and training energy
  (`epsilon_train`) differ by about 0.5-30%, bounded to the Stage-6 tail. Logged as a
  FUT/trainex validation item: confirm this train-vs-validate mismatch is negligible on the
  admitted set. Phase 33 transcribes static invariants with `epsilon_inv = 1e-10`; Phase 35
  preserves the loss-side lock. No spec edit in Phase 32.

---

*Phase: 32-evidence-framework-issue-ledger-conflict-adjudication*
*Register opened: 2026-06-21*
