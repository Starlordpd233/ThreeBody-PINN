# Requirements: v2.3 Causal-Weight/SIREN-Scale Recipe Adjudication

**Defined:** 2026-08-18
**Core value:** A *grounded* recalibration of the two locked spec choices that collide at initialization — obtained through the governed decision channel rather than agent judgment, landed as a framework-spec contract amendment, proven train-free before a run is spent, and then tested by a Stage-0 re-run and the single preserved held-out evaluation.
**Total:** 15 requirements (2 ERW + 6 SPEC + 1 INST + 1 GATE + 2 RUN + 1 EVAL + 1 DIAG + 1 VER) + scope boundaries SCOPE-33..38.

**Source:** the owner-ratified v2.3 roadmap proposal (`docs/work/designs/cross_cutting/v2.3-milestone-proposal/2026-08-17-v2.3-roadmap-proposal.md`, drafted 2026-08-17, ratified 2026-08-18 at commit `16434f50`), consumed by `/gsd-new-milestone` on 2026-08-18. Requirement texts below are transcribed from that proposal.

## Why this milestone exists

v2.2 closed **incomplete** on 2026-08-17. It repaired all nine verified Stage-0
conformance divergences (C-01..C-09) and re-ran Stage-0 under the corrected
recipe — the first run that was actually the specified experiment. That run
HALTed at the invariant-B causal-front gate, step 501, `front_idx=0` for the
entire `N=500` window.

A bounded residual-frame conformance audit the same day established that this is
**not** a further conformance defect. It is a design-calibration gap between two
independently-locked framework-spec sections:

- `pinn_architecture.md` §2.2 locks a SIREN initialization (`first_omega_0 = 30`,
  12 layers) whose **second derivative** is `O(10⁵)` in the network's own units
  at initialization, giving `R̄ ≈ 10¹⁰`.
- `pinn_architecture.md` §3.2 locks a causal weighting
  `w_n = exp(−η_c · Σ_{m<n} stopgrad(R̄_m))` with `η_c = 1` on **unnormalized**
  `R̄` — a calibration that presumes a *converged* network's residual of `O(1)`.

Neither choice is wrong in isolation; they were simply never checked against each
other. Stacked, `exp(−η_c R̄)` underflows float32 at `R̄ > 87.3`, which the run
exceeds by 8.5 decades at step 0. The causal weighting saturates shut before
training begins and stays saturated: 15 of 16 collocation-point weights sit at
the numerical floor for the whole run, and the physics loss reduces to a single
point's residual.

The finding is established independent of any particular run's outcome — a
read-only characterization of the locked architecture alone (no data, no
optimizer, no training step) reproduces `R̄ ≈ 10¹⁰` and `front_idx = 0`
identically across six seed/IC combinations.

This is exactly the contingency v2.2's own goal statement named in advance:
*"If the conformant run still fails, that failure is the first real evidence
about the design, and recipe adjudication … is v2.3."*

## Grounding (authoritative inputs)

1. **The locked framework specs** (`ctl_instruction.md`, `pinn_architecture.md`)
   as completed by v1.4/v1.5/v1.6 — AND as amended by this milestone's own
   VER-20-item decisions under SCOPE-38's amendment discipline. This is the one
   milestone where editing them is the point.
2. **v2.2's closure record**: the residual-frame conformance audit
   (`docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md`,
   committed `ae14a99e`); the DIAG-05 root-cause re-derivation
   (`.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md`);
   the five-item routing list
   (`.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md`);
   and `.planning/milestones/v2.2-GAPS.md` "Milestone close".
3. **The trainex-r2 research report**
   (`pinn_instruction/markdown_conversion/framework-specs/trainex-r2/`) — **now
   legally a grounding source** (SCOPE-31's own text: "it enters at v2.3 as a
   premise-qualified candidate verdict source"), with a **mandatory premise
   qualification that must travel with every citation of it**: that round's
   output contract (`RESEARCH-CONTEXT-MASTER.md` §7, clause 3) reads *"Do not
   recommend a remedy."* It contains **no decision sheet, no options menu, no
   suggested defaults, and no one-way/two-way door classification**. Its Q3
   frames the diagnosis and independently derived the `ω₀=30` mechanism as a
   hypothesis (now confirmed); it does not contain the answer. v2.2 has since
   executed two of Q3's four discriminating tests (residual-on-stored-targets →
   CONF-01/08/09; per-term gradient statistics → INST-02) and repaired its
   reading-2 frame hypothesis as C-09.
4. **All prior locked decisions this milestone does not reopen**: the 14D
   `[τ, IC₁₃]` input, Jacobi IC₁₃, mass-weighted COM projection, PHYS-03
   softening `eps_soft = 1e-5`, the post-v1.3 SCS gate, the raw-mass
   `D ≈ 4.6416` convention (`D³ = G T²`), and the full v1.5/v1.6/v2.0/v2.1/v2.2
   DataLoader, validation, and conformance contracts (PIPE-01..10, VAL-01..04,
   CONF-01..09, INST-01..03, GATE-01..03, TEST-01..02).

## v2.3 Requirements

### External Research & Decision Grounding (ERW)

- [ ] **ERW-01**: Assemble a **strictly non-recommending** decision packet for the causal-weight/SIREN-scale recalibration and present it at a blocking owner gate. Contents: the confirmed mechanism; the coupled remedy surfaces (`η_c`, `R̄` normalization against a reference scale, the SIREN initialization scale `ω₀`, `N_t`/`n_col`, and the causal-exponent clip's declared semantics); what v2.2's evidence has already settled from trainex-r2 Q3; and an explicit statement of which questions the assembled evidence **cannot** answer. **Acceptance:** the packet marks no default, ranks no option, and recommends no remedy — and it names its own gaps. It doubles as the `trainex-r3` `RESEARCH-CONTEXT-MASTER.md` if the round is commissioned, so neither gate branch wastes work. [SCOPE-34; ERW runbook `docs/runbooks/external-research/2026-06-11-external-research-workflow.md`]
- [ ] **ERW-02**: Discharge the owner gate's branch and produce **one ratified recalibration decision**. Either (a) record the owner's direct ruling with its provenance, or (b) assemble and deliver `trainex-r3` per the canonical ERW runbook — Route B (open-book) against the post-repair tree, carrying the full **Rule-7 build-design output contract** that trainex-r2 deliberately lacked (2–4 option menus with mechanical-surface trade-offs, suggested defaults clearly marked, one-way vs two-way door classification on every default and deviation, a fill-in decision sheet, and a composed first-run recipe as a cross-menu coherence check) — plus the mandatory **Rule-19** per-claim in-repo verification pass, then land its consolidated decision sheet for owner ratification. [SCOPE-34; ERW Rules 7, 16, 19, 20]

### Framework-Spec Amendments (SPEC)

- [ ] **SPEC-01**: Implement the ratified causal-weight/SIREN-scale recalibration (VER-20 item **e**) as a `pinn_architecture.md` §2.2/§3.2 amendment. **Under SCOPE-38 this is a contract amendment, not a value edit**: `η_c = 1` carries an owner-ratified Phase-35 contract marker (**LOSS-04 / D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A / AC-LOSS-04**, `pinn_architecture.md:424`, grounded in the v1.6 resolution doc §1.1 and GAP-32-01). The edit must name the superseded ruling, record the new decision's provenance, and carry a **re-issued acceptance criterion**. If the ratified remedy touches `first_omega_0` (§2.2:167, *"fixed at 30 and is not scheduled during training"*) or the causal-exponent clip (spec'd in the same contract block as *"required only to avoid underflow"*), the same discipline applies to each. `N_t`/`n_col` is decided jointly — see SPEC-06. [VER-20 item (e); SCOPE-33, SCOPE-38]
- [ ] **SPEC-02**: Reword `pinn_architecture.md` §4.1's `λ_phys^max` line to state that the PHYS-05 per-stage table is **locked**, not defaulted. The line currently reads as though the value is a tunable default; GAP-45-03 ratified that the full table binds. [VER-20 item (a)]
- [ ] **SPEC-03**: Add a spec convention for marking **locked-vs-default values inside a table**. No existing convention distinguishes a locked constant from an illustrative default within the same table; SPEC-02 is one instance of a systemic wording problem. [VER-20 item (b)]
- [ ] **SPEC-04**: Make the `L_data` reduction explicit in spec prose — **mean over time, bodies, and spatial components**, as ratified by the owner on GAP-45-01 (2026-07-31, Phase 48 checkpoint, option A) — rather than leaving it inferable from code. [VER-20 item (c); CONF-07]
- [ ] **SPEC-05**: Codify the held-out physics gate's **aggregate statistic** in spec prose: worst-case max, not mean or median, owner-ruled 2026-07-23 on GAP-44-01 and never written into the spec. [VER-20 item (d)]
- [ ] **SPEC-06**: Dispose of the `n_col` spec/code divergence **as part of the recalibration**. `pinn/train.py:1033` hard-codes `collocation_count = 16`; `pinn_architecture.md` §3.2 specifies `n_col = 4096` with "recommended: 2048–4096" (`:433`, `:440`). Because `w_n` is an **exclusive prefix sum** over collocation points (`pinn/loss_catalog.py`), the exponent at point *n* grows with the number of preceding points, so `η_c`'s calibration is coupled to `N_t` — calibrating at 16 and later honoring 4096 moves the exponent by roughly 256×. SPEC-01 and SPEC-06 are **ratified together**, and the amended spec records the `N_t` the calibration binds to plus the re-check trigger if it ever changes. v2.2 deferred this as a recipe surface under SCOPE-29; that deferral expires here. [SCOPE-33; audit §6d]

### Reproducibility & Train-Free Acceptance (INST / GATE)

- [ ] **INST-04**: Land the architecture-only characterization as **committed, tested verification tooling** under `pinn/verification/`. For a given `ArchitectureSpec` at initialization — no data, no optimizer, no training step — it reports `‖r′‖`, `‖v′‖`, `‖a′‖ = ‖d²r′/du²‖`, `‖F_grav‖`, minimum pairwise separation, median `R̄`, the full causal weight vector, and `front_idx`, over a configurable seed/IC sweep. **Acceptance:** it reproduces the 2026-08-17 audit's six-row table. This closes a real hole — v2.3's central premise currently rests on an ad-hoc measurement that exists nowhere in the repository, and `pinn/verification/` has no such probe. [audit §6b; GAP-44-02 re-derivability discipline]
- [ ] **GATE-04**: **Train-free acceptance gate on the recalibration.** Before RUN-04 may spend a Stage-0 run, INST-04's probe must show, under the SPEC-01/SPEC-06 recipe and across at least the six seed/IC combinations the audit used: (i) no causal weight pinned at the dtype clamp floor; (ii) a weight vector carrying **differential information** (not all-floor, not degenerate); (iii) `front_idx` able to advance. **Fail closed** — a probe failure blocks the run rather than warning about it. This is the check that would have spared v2.2's generation-3 run. [invariant A/B lineage from GATE-03; SCOPE-35 single-look protection]

### Re-Run & the Preserved Evaluation (RUN / EVAL)

- [ ] **RUN-04**: Re-run Stage-0 under the SPEC-01/SPEC-06-corrected recipe. Invariant B must show the causal front **actually advancing** — not merely no-longer-saturated — within the owner-re-ratified window. Gated on GATE-04. Iteration is conformance-only (SCOPE-37). [SCOPE-36 authorizes Stage-0 training]
- [ ] **RUN-05**: Re-establish the **three-seed band** under the corrected recipe, matching the v2.0/v2.2 protocol so the runs are comparable. [v2.0 pilot protocol; v2.2 RUN-02 lineage]

- [ ] **EVAL-02**: Spend the **sole preserved held-out evaluation** — the one v2.2 never attempted (RUN-03/EVAL-01 not attempted, preserved unspent by the 2026-08-17 owner decision). Gated on the same three-precondition structure as v2.2's EVAL-01, adapted for the new recipe, and on the **pre-registered spending seed** fixed before RUN-04/05 execute. Before any held-out access, prove with a dataset-free regression and a pre-invocation assertion that the evaluator pairs canonical predicted `r′` with `u = t/T`. [SCOPE-35; GAP-46-01 delegated ruling 2026-07-26]

### Verdict & Traceability (DIAG / VER)

- [ ] **DIAG-06**: The owner renders a final **go / adjust / rethink** verdict on the recalibrated design — the second attempt at the verdict v2.2's Phase 51 never reached, and the gate that governs whether Stage-1+/PLAT-01..07 re-open. [v2.0 ACC-06 pattern; SCOPE-36]
- [ ] **VER-21**: Requirement traceability — every requirement maps to exactly one phase; no orphans, no duplicates. Re-verified at milestone close against the final requirement count, not carried forward from the roadmap-creation check. [VER-19 lineage]

## Scope Boundaries (owner-ratified 2026-08-18 — hard constraints)

| ID | Boundary |
|----|----------|
| SCOPE-33 | **Framework-spec edits ARE authorized**, narrowly: only the items in `52-VER-20-ROUTING-HANDOFF.md` (a)–(e), plus the `n_col`/`N_t` disposition coupled to item (e) per SPEC-06. No open-ended spec rewriting. SCOPE-30 does not carry forward. |
| SCOPE-34 | **The recalibration decision is owner-ratified, never agent-decided.** The agent assembles and frames the decision packet (ERW-01) and, if commissioned, the `trainex-r3` round (ERW-02); it marks no default, ranks no option, and picks nothing. The STOP protocol's semantic / MUST-surface class governs every sub-question. |
| SCOPE-35 | **Exactly ONE held-out evaluation** — the one preserved unspent from v2.2. Spent only on a run passing its preconditions, only after the recalibrated recipe actually trains (causal front advances), and only on a seed pre-registered before RUN-04/05 execute. Any further evaluation requires a new owner decision. |
| SCOPE-36 | **Stage-0 only.** No Stage-1+, no PLAT-01..07 platform work. Unchanged from v2.2 — still blocked by the v2.0 `adjust` verdict pending a `go` verdict at DIAG-06. |
| SCOPE-37 | **Iteration after the spec edit lands is conformance-only again.** Once the new `η_c` / normalization / SIREN-scale / `N_t` values are locked, no further tuning against observed re-run results without a new owner decision. Prevents the milestone from becoming an open-ended hyperparameter search, and keeps a second failure informative. |
| SCOPE-38 | **Amending a locked contract requires explicit re-ratification.** Any v2.3 spec edit that changes a value or formula carrying an owner-ratified contract marker — `η_c` (LOSS-04 / D-04 / AC-LOSS-04), `first_omega_0` (§2.2 "fixed at 30"), the causal-exponent clip's underflow-only purpose — is a **formal amendment** of that contract: recorded with its provenance, naming the superseded ruling, and carrying a re-issued acceptance criterion. A changed number without a re-ratified contract is not a legal v2.3 edit. |

## Owner Checkpoints (blocking — never auto-decided)

1. **The ERW gate** — after ERW-01's packet is assembled: rule directly, or commission `trainex-r3`.
2. **The recalibration decision** — the actual `η_c` / normalization / SIREN-scale / `N_t` pick, together with the SCOPE-38 re-ratification of each locked contract the pick amends.
3. **Invariant-B window re-ratification** — `N = 500` was ratified 2026-08-05 for the old, saturated dynamics; the new recipe may need a different window, and this must not be silently carried over.
4. **Pre-registration of the EVAL-02 spending seed** — fixed before RUN-04/05 execute. Choosing after seeing three seeds would be a selection-effect leak against a single-look budget.
5. **The DIAG-06 go / adjust / rethink verdict** — after RUN-04/05 and EVAL-02.

## Declared Terminal State

If GATE-04 refuses the recalibration train-free, or RUN-04's causal front still
fails to advance under the ratified recipe, **SCOPE-37 forbids further tuning
without a new owner decision.** The milestone then closes on a `rethink`-flavored
DIAG-06 verdict with the held-out evaluation preserved unspent — declared here up
front, so that outcome is a clean close rather than a drift. This is v2.2's
lesson written into v2.3's requirements: the terminal branch must be named before
it is needed.

## Future Requirements (deferred beyond v2.3)

- **PLAT-01..07 platform expansion and Stage-1+ curriculum work** — blocked by the v2.0 `adjust` verdict and SCOPE-36; re-opens only on a `go` verdict at DIAG-06.
- **The general verification-enforcement regime** — normative-statement index, full CI integration, waiver policy, thresholds X/M — owned by the concurrent charter workstream (`docs/work/designs/cross_cutting/training-verification-regime/2026-07-24-verification-enforcement-charter.md`), inherited unchanged from v2.2 SCOPE-32.
- **Final Publication LaTeX Sync** — deferred until implementation, training, and research-result interpretation are complete.
- **Carried-forward todos** (remain in `.planning/todos/pending/`): `trainex-r1-research-handoff` (the r1b tuning round), `d-06-static-epsilon-sensitivity-check` (spec-side sensitivity question, answered as trainex-r2 Q6 but not yet dispositioned).

## Out of Scope

| Exclusion | Reason |
|-----------|--------|
| Re-litigating the nine v2.2 conformance repairs (C-01..C-09) | Settled and independently re-verified at Phase 49 close (176-test suite) and Phase 50. Not reopened. |
| Re-running or re-litigating DIAG-05 | `52-DIAG-05-REDERIVATION.md` is the operative diagnosis, superseding `44-DIAGNOSIS.md`/`44-ERRATUM.md`'s under-determined rankings. Treated as settled (v2.2-GAPS obligation 4). |
| Open-ended hyperparameter search / recipe tuning after the spec edit | SCOPE-37 — post-edit iteration is conformance-only, so a second failure is informative rather than another leak. |
| Stage-1+ work, PLAT-01..07 platform expansion | SCOPE-36 — Stage-0-only authorization pending a `go` verdict. |
| Any held-out evaluation beyond the one preserved | SCOPE-35 — requires a new owner decision. |
| Agent-authored recalibration options, defaults, or picks | SCOPE-34 — the decision is owner-ratified through the governed channel; agent judgment is not a grounding source. |
| A framework-spec value change without a re-ratified contract | SCOPE-38 — three of the candidate remedy surfaces carry owner-ratified contract markers. |
| Re-running the v2.0 seed-42 checkpoint's evaluation | The v2.0 record and its receipt-based refusal path are protected (v2.0 audit W-1). A corrected implementation is a new question, not a re-run. |
| The GSD 4-agent domain-research pass | External research for this milestone is routed through the governed ERW channel (ERW-01/02). A generic web-research pass would produce exactly the unratified remedy analysis SCOPE-34 and the STOP protocol forbid. |

## Traceability

*(Filled by the roadmapper at roadmap creation; VER-21's binding check is at milestone close, not at roadmap creation.)*

| Requirement | Phase | Status |
|-------------|-------|--------|
| ERW-01 | — | Pending |
| ERW-02 | — | Pending |
| SPEC-01 | — | Pending |
| SPEC-02 | — | Pending |
| SPEC-03 | — | Pending |
| SPEC-04 | — | Pending |
| SPEC-05 | — | Pending |
| SPEC-06 | — | Pending |
| INST-04 | — | Pending |
| GATE-04 | — | Pending |
| RUN-04 | — | Pending |
| RUN-05 | — | Pending |
| EVAL-02 | — | Pending |
| DIAG-06 | — | Pending |
| VER-21 | — | Pending |

**Namespace continuity.** `ERW` and `SPEC` are new categories beginning at 01 —
verified against every archived milestone requirements file, no collisions.
`INST` continues from v2.2's INST-03; `GATE` from GATE-03; `RUN` from RUN-03;
`EVAL` from EVAL-01; `DIAG` from v2.2's DIAG-05; `VER` from VER-20; `SCOPE`
from v2.2's SCOPE-32. SCOPE-33..38 are scope-boundary annotations, not numbered
requirements (v2.0 SCOPE-16..21 and v2.2 SCOPE-27..32 precedent).

---
*Requirements defined: 2026-08-18 via `/gsd-new-milestone`, transcribed from the owner-ratified v2.3 roadmap proposal (`16434f50`).*
