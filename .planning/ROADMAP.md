# Roadmap: 3-Body Problem Physics-Inspired LLM

## Milestones

- ✅ **v1.0 Codebase Cleanup** — Phases 1–4 (shipped 2026-03-20; [archive](milestones/v1.0-ROADMAP.md))
- ✅ **v1.1 LaTeX Modularization Verification** — Phases 5–8 (shipped 2026-03-22)
- ✅ **v1.2 PINN Implementation Readiness** — Phase 9 (shipped 2026-05-08)
- ✅ **v1.3 Markdown Conversion Verification & Correction** — Phases 10–15, 15.1 (shipped 2026-05-08; [archive](milestones/v1.3-ROADMAP.md))
- ✅ **v1.4 Resolving 01 Architecture and Physics Foundations** — Phases 16–22, including 20.5 (shipped 2026-06-09; [roadmap archive](milestones/v1.4-ROADMAP.md), [requirements archive](milestones/v1.4-REQUIREMENTS.md), [phase archive](milestones/v1.4-phases/))
- ✅ **v1.5 Resolving 02 Data Pipeline and Validation** — Phases 23–29, including 24.5 (shipped 2026-06-17; archived under [`milestones/v1.5-*`](milestones/))
- ✅ **v1.6 Resolving 03 Curriculum and Training Loop** — Phases 30–36 (shipped 2026-07-02; 32/32 requirements, 26/26 acceptance probes PASS, ledger 18/18 VERIFIED; FUT-01/FUT-04 routed to the trainex track; archived under [`milestones/v1.6-*`](milestones/))
- ✅ **v2.0 CTL-PINN Training Viability Slice** — Phases 37–43 (shipped 2026-07-23; the project's first **build** milestone / trainex track — Stage-0-first end-to-end training slice from the ratified trainex-r1a decisions; 42/42 requirements Complete; audit `tech_debt` with zero blockers; the sole held-out physics gate rendered an honest **FAIL** (`ε_H = 237.21` vs ≤ 1e-5) and the owner signed **`adjust`** — Stage-0 mechanical slice retained, PLAT-01..07 blocked, physics-gate investigation routed to the next milestone; archived under [`milestones/v2.0-*`](milestones/))
- ✅ **v2.1 Physics-Gate Investigation & trainex-r2 Research Package** — Phases 44–45 (shipped 2026-07-24; the separately governed investigation routed by the v2.0 `adjust` verdict — read-only forensics over the retained v2.0 artifacts + trainex-r2 ERW package delivery; 7/7 requirements, package audited PASS; a bounded conformance audit found the v2.0 pilot diverged from the locked specs in five verified respects, qualifying the Phase 44 diagnosis and seeding a conformance-first next milestone; archived under [roadmap](milestones/v2.1-ROADMAP.md), [requirements](milestones/v2.1-REQUIREMENTS.md), [gaps](milestones/v2.1-GAPS.md), [phase archive](milestones/v2.1-phases/))
- ⚠️ **v2.2 Stage-0 Conformance Repair & Valid Re-Run** — Phases 46–52 (started 2026-07-25; **closed incomplete 2026-08-17**; repaired all nine verified Stage-0 conformance divergences (Phases 46–49, CONF/INST/GATE/TEST-01..09 Complete) and re-ran Stage-0 under the corrected recipe (Phase 50), but the conformant run HALTed at the invariant-B causal-front gate, step 501 — a bounded 2026-08-17 conformance audit found this is a property of the locked architecture at initialization (SIREN second-derivative scale vs. causal-weight calibration), not a further conformance defect, with no remedy available inside v2.2 (SCOPE-30); owner selected `stop-incomplete` (RUN-01/RUN-02 unsatisfied), the sole held-out evaluation was preserved unspent (RUN-03/EVAL-01 not attempted), and DIAG-05/VER-19/VER-20 were discharged in adapted form (Phase 52); 20/24 requirements Complete, 2 closed incomplete, 2 not attempted; archived under [`milestones/v2.2-*`](milestones/); routes to v2.3)
- 🚧 **v2.3 Causal-Weight/SIREN-Scale Recipe Adjudication** — Phases 53–58 (started 2026-08-18; **in progress**; the milestone v2.2's `stop-incomplete` close routed to — get an owner-ratified recalibration for the causal-weight/SIREN-scale mismatch that halted the conformant Stage-0 re-run (§2.2's `ω₀=30` SIREN second derivative against §3.2's `η_c=1` on unnormalized `R̄`), land it as a framework-spec **contract amendment** under SCOPE-38's re-ratification discipline, prove it **train-free** before a run is spent (GATE-04), re-run Stage-0, and spend the single preserved held-out evaluation on a run that actually trains; 15 requirements (ERW-01/02, SPEC-01..06, INST-04, GATE-04, RUN-04/05, EVAL-02, DIAG-06, VER-21), scope boundaries SCOPE-33..38, five blocking owner checkpoints, and a **declared terminal state**; branch `milestone/v2.3`)
- 🔮 **Final Publication LaTeX Sync** — deferred until implementation, network/training design, training, and research-result interpretation are complete

## Deferred: Final Publication LaTeX Sync

**Goal:** Refresh LaTeX/PDF publication sources from the final authoritative markdown framework specs.

**Preconditions:**

- Implementation complete (FUT-01 or successor milestone)
- Network design stable
- Training and research results complete
- No active framework-spec iteration expected

**Non-goal:** Maintaining `.tex` parity during active development milestones.

**Source of truth:** Markdown framework specs (`pinn_instruction/markdown_conversion/framework-specs/*.md`) at final sync start.

**Historical note:** This supersedes the earlier draft `v1.6.5-latex-sync` timing from the May 24, 2026 design document.

## 🚧 v2.3 Causal-Weight/SIREN-Scale Recipe Adjudication (Executing)

**Milestone Goal:** Get a properly grounded recalibration decision for the causal-weight/SIREN-scale mismatch — assembled and framed by the agent, ruled on by the owner, and externally researched via the ERW build-design channel if the assembled packet does not support a ruling — implement it as a framework-spec **contract amendment** (finally legal here; SCOPE-30 does not carry forward), prove the fix train-free before spending a run, re-run Stage-0 under the corrected recipe, and spend the single preserved held-out evaluation on a run that actually trains. **What this milestone deliberately does not do:** re-litigate the nine v2.2 conformance repairs (settled, not reopened), re-run DIAG-05 (superseded by `52-DIAG-05-REDERIVATION.md`, not re-litigated), open Stage-1+/PLAT-01..07 (still blocked by the v2.0 `adjust` verdict until a `go` verdict is rendered here), or author a remedy the owner has not ratified (SCOPE-34).

**Granularity:** standard (6 phases, 15 requirements: ERW-01..02, SPEC-01..06, INST-04, GATE-04, RUN-04..05, EVAL-02, DIAG-06, VER-21)
**Coverage:** 15/15 v2.3 requirements mapped at roadmap creation (VER-21's binding check is at Phase 58 close, against the final requirement count, not this one)
**Branch:** work continues in `.worktrees/trainex` on `milestone/v2.3`, created 2026-08-18 from `milestone/v2.2` at `16434f50` — the commit that carries the owner-ratified v2.3 proposal, so the branch point and the ratification are the same fact. Per-plan atomic commits via `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set; no push to protected branches (`master`, `main`, `milestone/*`); `master` remains governance-only and integration is user-controlled.

### Adjudication discipline (applies to all phases)

- **Hard boundaries (SCOPE-33..38):** framework-spec edits **ARE** authorized, narrowly — only `52-VER-20-ROUTING-HANDOFF.md` items (a)–(e) plus the `n_col`/`N_t` disposition coupled to item (e); SCOPE-30 does **not** carry forward, and nothing here licenses open-ended spec rewriting (SCOPE-33). **The recalibration decision is owner-ratified, never agent-decided** — the agent assembles and frames the decision packet and, if commissioned, the `trainex-r3` round; it marks no default, ranks no option, and picks nothing, and the STOP protocol's semantic / MUST-surface class governs every sub-question (SCOPE-34). **Exactly ONE held-out evaluation** — the one preserved unspent from v2.2 — spent only on a run passing its preconditions, only after the recalibrated recipe actually trains (causal front advances), and only on a seed pre-registered before RUN-04/05 execute (SCOPE-35). **Stage-0 only** — no Stage-1+, no PLAT-01..07, unchanged from v2.2 and still blocked by the v2.0 `adjust` verdict pending a `go` at DIAG-06 (SCOPE-36). **Iteration after the spec edit lands is conformance-only again** — once the new `η_c` / normalization / SIREN-scale / `N_t` values are locked, no further tuning against observed re-run results without a new owner decision, which is what keeps a second failure informative (SCOPE-37). **Amending a locked contract requires explicit re-ratification** — `η_c` (LOSS-04 / D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A / AC-LOSS-04, `pinn_architecture.md:424`), `first_omega_0` (§2.2:167, *"fixed at 30 and is not scheduled during training"*), and the causal-exponent clip's *"required only to avoid underflow"* purpose each carry an owner-ratified contract marker; changing any is a **formal amendment** recorded with its provenance, naming the superseded ruling, and carrying a re-issued acceptance criterion. A changed number without a re-ratified contract is not a legal v2.3 edit (SCOPE-38).
- **No phase may plan an agent-chosen value.** SCOPE-34 binds planning, not only execution: no plan in this milestone may propose, default, rank, or "provisionally assume" an `η_c`, an `R̄` normalization, an `ω₀`, or an `N_t`. Plans carry the decision channel, the transcription of what was ratified, and the verification — never the pick. A plan that needs a number the owner has not ratified is blocked, and the need is routed as a gap.
- **Grounding (authoritative inputs):** the **locked framework specs** (`ctl_instruction.md`, `pinn_architecture.md` — v1.4/v1.5/v1.6) as amended by this milestone's own VER-20-item decisions under SCOPE-38's discipline; **v2.2's closure record** — the residual-frame conformance audit (`docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md`, committed `ae14a99e`), `52-DIAG-05-REDERIVATION.md` (the operative diagnosis, superseding `44-DIAGNOSIS.md`/`44-ERRATUM.md`'s under-determined rankings — treated as settled, not re-litigated), `52-VER-20-ROUTING-HANDOFF.md`, and `.planning/milestones/v2.2-GAPS.md` "Milestone close"; and the **trainex-r2 research report** (`pinn_instruction/markdown_conversion/framework-specs/trainex-r2/`), **now legally a grounding source** per SCOPE-31's own text, **with a mandatory premise qualification that travels with every citation of it**: that round's output contract (`RESEARCH-CONTEXT-MASTER.md` §7, clause 3) reads *"Do not recommend a remedy"*, so it contains no decision sheet, no options menu, no suggested defaults, and no one-way/two-way door classification. Its Q3 frames the diagnosis and independently derived the `ω₀=30` mechanism as a hypothesis (now confirmed); it does **not** contain the answer. **Not reopened:** the 14D `[τ, IC₁₃]` input, Jacobi IC₁₃, the mass-weighted COM projection head, PHYS-03 softening `eps_soft = 1e-5`, the post-v1.3 SCS gate, the raw-mass `D ≈ 4.6416` convention (`D³ = G T²`), and the full v1.5/v1.6/v2.0/v2.1/v2.2 DataLoader, validation, and conformance contracts (PIPE-01..10, VAL-01..04, CONF-01..09, INST-01..03, GATE-01..03, TEST-01..02).
- **Owner checkpoints (blocking, never auto-decided):** ① **the ERW gate** (Phase 54) — reading ERW-01's assembled packet, the owner rules directly or commissions `trainex-r3`; the agent does not select the branch. ② **the recalibration decision** (Phase 54) — the actual `η_c` / normalization / SIREN-scale / `N_t` pick, together with the SCOPE-38 re-ratification of each locked contract the pick amends; it binds SPEC-01 and SPEC-06 **jointly**, and Phase 56 may not open without it. ③ **invariant-B window re-ratification** (Phase 57, before any run executes) — `N = 500` was ratified 2026-08-05 for the *old, saturated* dynamics; the new recipe may need a different window and this must not be silently carried over. ④ **pre-registration of the EVAL-02 spending seed** (Phase 57, before RUN-04/05 execute) — choosing after seeing three seeds would be a selection-effect leak against a single-look budget. ⑤ **the DIAG-06 go / adjust / rethink verdict** (Phase 58), after RUN-04/05 and EVAL-02.
- **Declared terminal state:** if GATE-04 refuses the recalibration train-free, or RUN-04's causal front still fails to advance under the ratified recipe, **SCOPE-37 forbids further tuning without a new owner decision.** The milestone then closes on a `rethink`-flavored DIAG-06 verdict with the held-out evaluation **preserved unspent** — declared here up front, so that outcome is a clean close rather than a drift. Phases 57 and 58 both carry this branch explicitly. This is v2.2's lesson written into v2.3's roadmap: the terminal branch must be named before it is needed.
- **Gap discipline:** any source-silent physics/spec adjudication call is recorded in the phase-local `NN-GAPS.md` **and** the milestone index `.planning/milestones/v2.3-GAPS.md` (created on the first gap, standing trigger) and routed to the owner — never decided inline (the build-track analog of the STOP protocol). The class is wider here than in a normal build milestone: under SCOPE-34 every recalibration sub-question is MUST-surface by construction, and under SCOPE-38 any spec value the owner's ratification does not explicitly cover is a gap, not a default.

## Phases

**Phase Numbering:** integer phases 53–58 continue from v2.2's Phase 52 (numbering does not reset). Decimal phases reserved for urgent insertions.

- [ ] **Phase 53: Narrow Spec Codification** — The four VER-20 items with no research dependency, discharged first so the milestone ships them regardless of how the recalibration lands: §4.1's `λ_phys^max` line restated as **locked** rather than defaulted (GAP-45-03), a spec convention for marking locked-vs-default values *inside a table*, the `L_data` reduction — mean over time, bodies, and spatial components (GAP-45-01, owner option A, 2026-07-31) — written into prose rather than left inferable from code, and the held-out physics gate's aggregate statistic codified as **worst-case max** (GAP-44-01, owner-ruled 2026-07-23). Each is a transcription of an already-ratified owner ruling; none touches a contract-marked value, so SCOPE-38 does not fire. (SPEC-02, SPEC-03, SPEC-04, SPEC-05)
- [ ] **Phase 54: Recalibration Decision Grounding** — The governed decision channel, staged as ratified: ERW-01 assembles a **strictly non-recommending** decision packet (the confirmed mechanism; the coupled remedy surfaces `η_c`, `R̄` normalization against a reference scale, the SIREN init scale `ω₀`, `N_t`/`n_col`, and the clip's declared semantics; what v2.2's evidence already settled from trainex-r2 Q3; and an explicit statement of what the assembled evidence **cannot** answer), a **blocking owner gate** then rules directly or commissions `trainex-r3`, and ERW-02 discharges whichever branch fires — a recorded ruling with its provenance, or a Route-B (open-book) build-design round carrying the full ERW Rule-7 output contract trainex-r2 deliberately lacked plus the mandatory Rule-19 per-claim in-repo verification pass. The packet doubles as the `trainex-r3` `RESEARCH-CONTEXT-MASTER.md`, so neither branch wastes work. **Owner checkpoints ① and ②.** (ERW-01, ERW-02)
- [ ] **Phase 55: Architecture Characterization Probe** — v2.3's central premise currently rests on an ad-hoc measurement that exists nowhere in the repository, and `pinn/verification/` has no such probe. INST-04 lands it as committed, tested tooling: for a given `ArchitectureSpec` at initialization — **no data, no optimizer, no training step** — it reports `‖r′‖`, `‖v′‖`, `‖a′‖ = ‖d²r′/du²‖`, `‖F_grav‖`, minimum pairwise separation, median `R̄`, the full causal weight vector, and `front_idx` over a configurable seed/IC sweep, and reproduces the 2026-08-17 audit's six-row table. Independent of the ERW branch; runs in parallel with Phases 53 and 54. It is also the instrument Phase 56's GATE-04 fires, so it must exist before the gate can. (INST-04)
- [ ] **Phase 56: Contract Amendment & Train-Free Gate** — The ratified recalibration becomes spec law under SCOPE-38 amendment discipline — naming the superseded LOSS-04 / D-04 / AC-LOSS-04 ruling, recording the new decision's provenance, carrying a re-issued acceptance criterion, and applying the same discipline separately to `first_omega_0` and to the clip's underflow-only purpose if the remedy touches them — with the `n_col`/`N_t` disposition ratified **jointly**, since `w_n` is an exclusive prefix sum over collocation points and `η_c`'s calibration therefore moves by roughly 256× between the code's `collocation_count = 16` and §3.2's `n_col = 4096`. GATE-04 then makes INST-04's probe a **fail-closed** precondition on RUN-04: no causal weight pinned at the dtype clamp floor, a weight vector carrying differential information, and `front_idx` able to advance. Hard-gated on Phases 54 and 55. (SPEC-01, SPEC-06, GATE-04)
- [ ] **Phase 57: Corrected Re-Run & the Preserved Evaluation** — Stage-0 re-runs end-to-end under the SPEC-01/SPEC-06-corrected recipe with invariant B required to show the causal front **actually advancing** — not merely no-longer-saturated — inside the re-ratified window; the three-seed band is re-established on the v2.0/v2.2 protocol so the runs are comparable; and the **sole preserved held-out evaluation**, the one v2.2 never attempted, is spent **once** on the pre-registered seed after its three preconditions and the `r′` ↔ `u = t/T` pairing proof. Iteration is conformance-only (SCOPE-37). **Owner checkpoints ③ and ④, both discharged before any run executes.** Carries the declared terminal state: a GATE-04 refusal or a still-failing front means the evaluation is **not** spent. (RUN-04, RUN-05, EVAL-02)
- [ ] **Phase 58: Verdict & Traceability Close** — The owner renders the final **go / adjust / rethink** verdict on the recalibrated design — the second attempt at the verdict v2.2's Phase 51 never reached, and the gate that governs whether Stage-1+/PLAT-01..07 re-open — and VER-21's traceability is re-verified at close against the **final** requirement count rather than carried forward from this roadmap's check, reading it the way v2.2's CONF-09 lesson requires. **Owner checkpoint ⑤.** (DIAG-06, VER-21)

## Phase Details

### Phase 53: Narrow Spec Codification

**Goal**: The four VER-20 items that need no research are settled in the spec text, so a worst-case v2.3 still discharges four of the five routed amendments.
**Depends on**: Nothing — ungated first v2.3 phase (ratified sequencing track A). Runs in parallel with Phases 54 and 55.
**Requirements**: SPEC-02, SPEC-03, SPEC-04, SPEC-05
**Plans:** 1/1 plans executed

Plans:

- [x] 53-01-PLAN.md — convention preamble + PHYS-05 marking + adjudication re-key (tracer), L_data reduction correction, §10.6 aggregate-statistic subsection

**Success Criteria** (what must be TRUE):

  1. `pinn_architecture.md` §4.1's `λ_phys^max` line states that the PHYS-05 per-stage table is **locked**, no longer reads as a tunable default, and cites GAP-45-03's ratification that the full table binds (SPEC-02).
  2. The spec carries a stated convention that distinguishes a locked constant from an illustrative default **inside the same table**, and §4.1's PHYS-05 table is marked under it — so SPEC-02's instance is closed by the convention rather than by a one-off rewording of a systemic problem (SPEC-03).
  3. A reader can determine the `L_data` reduction — **mean over time, bodies, and spatial components** — from spec prose alone, without consulting `pinn/`, with the owner's GAP-45-01 option-A ruling (2026-07-31, Phase 48 checkpoint) cited as its authority (SPEC-04, CONF-07).
  4. The held-out physics gate's aggregate statistic is written in spec prose as **worst-case max** — explicitly not mean and not median — citing the owner's 2026-07-23 GAP-44-01 ruling that was never written into the spec (SPEC-05).
  5. Every edit in this phase is a transcription of an already-ratified ruling: none changes a value or formula carrying an owner-ratified contract marker, so no SCOPE-38 amendment is triggered, and any wording question the rulings do not answer is routed as a gap rather than decided inline (SCOPE-33, SCOPE-34).

### Phase 54: Recalibration Decision Grounding

**Goal**: Exactly one owner-ratified recalibration decision exists, reached through the governed channel — the agent framed the question, the owner answered it.
**Depends on**: Nothing — ungated (ratified sequencing track B). Runs in parallel with Phases 53 and 55; its ratified output hard-gates Phase 56.
**Requirements**: ERW-01, ERW-02
**Plans**: TBD

**Success Criteria** (what must be TRUE):

  1. A decision packet exists that states the confirmed mechanism, enumerates the coupled remedy surfaces (`η_c`, `R̄` normalization against a reference scale, the SIREN initialization scale `ω₀`, `N_t`/`n_col`, and the causal-exponent clip's declared semantics), records what v2.2's evidence has already settled from trainex-r2 Q3, and **names the questions the assembled evidence cannot answer** — and a reader can verify by inspection that it marks no default, ranks no option, and recommends no remedy (ERW-01, SCOPE-34).
  2. Every citation of trainex-r2 in the packet travels with its premise qualification — that round's output contract (`RESEARCH-CONTEXT-MASTER.md` §7, clause 3) forbade recommending a remedy, so it carries no decision sheet, no options menu, no suggested defaults, and no door-type classification, and its 2026-07-25 vintage predates the v2.2 conformance repairs.
  3. **Owner checkpoint ① is discharged:** reading the packet, the owner either rules directly or commissions `trainex-r3`, and the branch taken is recorded with its provenance. The agent does not select the branch, and no work proceeds past the gate on an assumed branch.
  4. If `trainex-r3` is commissioned, it is delivered per the canonical ERW runbook as a Route-B (open-book) build-design round against the post-repair tree, carrying the full **Rule-7** output contract — 2–4 option menus with mechanical-surface trade-offs, suggested defaults clearly marked, one-way vs two-way door classification on every default and deviation, a fill-in decision sheet, and a composed first-run recipe as a cross-menu coherence check — and passes the mandatory **Rule-19** per-claim in-repo verification pass before its consolidated decision sheet is presented for ratification (ERW-02).
  5. **Owner checkpoint ② is discharged:** exactly one ratified recalibration decision is recorded — the `η_c` / normalization / SIREN-scale / `N_t` pick together with the SCOPE-38 re-ratification of each locked contract the pick amends. A ratification that does not dispose of `N_t` leaves SPEC-06's joint-ratification requirement unmet and is routed back to the owner as a gap, never completed by an agent choice (SCOPE-34).

### Phase 55: Architecture Characterization Probe

**Goal**: The measurement v2.3's central premise rests on stops being ad-hoc and becomes committed, tested tooling that anyone can re-run against any candidate recipe.
**Depends on**: Nothing — ungated (ratified sequencing track C). Runs in parallel with Phases 53 and 54; it is the instrument GATE-04 fires in Phase 56.
**Requirements**: INST-04
**Plans**: TBD

**Success Criteria** (what must be TRUE):

  1. `pinn/verification/` contains committed, tested tooling that, given an `ArchitectureSpec` at initialization and **no data, no optimizer, and no training step**, reports `‖r′‖`, `‖v′‖`, `‖a′‖ = ‖d²r′/du²‖`, `‖F_grav‖`, minimum pairwise separation, median `R̄`, the full causal weight vector, and `front_idx` over a configurable seed/IC sweep (INST-04).
  2. Run under the pre-amendment recipe, the probe **reproduces the 2026-08-17 residual-frame conformance audit's six-row table** across the same six seed/IC combinations — `R̄ ≈ 10¹⁰` and `front_idx = 0` in every row — and the reproduction is recorded re-derivably (command, tree state, full output) per the GAP-44-02 discipline, so the milestone's premise no longer rests on an unrepeatable measurement.
  3. The probe derives `R̄` and the causal weights from the same implementation the trainer uses, so a probe result is evidence about the shipped recipe rather than about a parallel re-implementation of it.
  4. A test suite fails if any reported quantity, the sweep configuration, or the six-row reproduction regresses — the probe is protected the way the Phase 49 gate work is, not left as a script.

### Phase 56: Contract Amendment & Train-Free Gate

**Goal**: The ratified recalibration is law in the framework specs under SCOPE-38's amendment discipline, and a train-free gate refuses to let a Stage-0 run be spent on a recipe whose causal weighting is still saturated shut.
**Depends on**: Phase 54 (the ratified decision — SCOPE-34 forbids opening this phase without it, including its `N_t` disposition) **and** Phase 55 (the probe GATE-04 fires). Both are hard gates, not preferences.
**Requirements**: SPEC-01, SPEC-06, GATE-04
**Plans**: TBD

**Success Criteria** (what must be TRUE):

  1. `pinn_architecture.md` §2.2/§3.2 carries the ratified recalibration as a **formal contract amendment**, not a value edit: it names the superseded ruling (**LOSS-04 / D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A / AC-LOSS-04**, `pinn_architecture.md:424`, grounded in the v1.6 resolution doc §1.1 and GAP-32-01), records the new decision's provenance, and carries a **re-issued acceptance criterion** (SPEC-01, SCOPE-38).
  2. If the ratified remedy touches `first_omega_0` (§2.2:167, *"fixed at 30 and is not scheduled during training"*) or the causal-exponent clip's *"required only to avoid underflow"* purpose, each is amended under the same discipline **separately and by name** — a remedy that silently repurposes the clip as a floor-raiser is not a legal edit (SCOPE-38).
  3. The `n_col` spec/code divergence is disposed of in the same ratification: the amended spec records the `N_t` the calibration binds to, reconciles `pinn/train.py:1033`'s `collocation_count = 16` against §3.2's `n_col = 4096` ("recommended: 2048–4096", `:433`, `:440`), and states the re-check trigger that fires if `N_t` ever changes — because `w_n` is an exclusive prefix sum over collocation points, so calibrating at 16 and later honoring 4096 would move the exponent by roughly 256× (SPEC-06).
  4. GATE-04 is wired **fail-closed** ahead of RUN-04: under the SPEC-01/SPEC-06 recipe and across at least the audit's six seed/IC combinations, INST-04's probe must show (i) no causal weight pinned at the dtype clamp floor, (ii) a weight vector carrying **differential information** — not all-floor, not degenerate — and (iii) `front_idx` able to advance; a probe failure **blocks** the run rather than warning about it (GATE-04).
  5. The gate is demonstrated to refuse: fired against the pre-amendment recipe it produces a blocking failure, so a passing result on the amended recipe is evidence rather than a no-op. This is the check that would have spared v2.2's generation-3 run.

### Phase 57: Corrected Re-Run & the Preserved Evaluation

**Goal**: Stage-0 is re-run under the corrected recipe and — only if it actually trains — the single preserved held-out evaluation is spent, once, on a seed fixed before anyone saw a result.
**Depends on**: Phase 56 — GATE-04 must pass before a Stage-0 run may be spent (SCOPE-35's single-look protection).
**Requirements**: RUN-04, RUN-05, EVAL-02
**Plans**: TBD

**Success Criteria** (what must be TRUE):

  1. **Owner checkpoint ③ is discharged before any run executes:** the invariant-B front-advance window is re-ratified for the new dynamics, with the ratified `N` and its provenance recorded in the run configuration. `N = 500` was ratified 2026-08-05 against the old, saturated dynamics and is not carried over by default.
  2. **Owner checkpoint ④ is discharged before any run executes:** the EVAL-02 spending seed is pre-registered in writing before RUN-04/05 run, so it cannot be chosen after the three-seed band is visible (SCOPE-35).
  3. Stage-0 runs end-to-end under the SPEC-01/SPEC-06-corrected recipe and invariant B records the causal front **actually advancing** — `front_idx` increasing within the re-ratified window, not merely off the floor — and the three-seed band is re-established under the same recipe on the v2.0/v2.2 protocol so the runs are comparable (RUN-04, RUN-05).
  4. No `η_c`, `R̄` normalization, `ω₀`, or `N_t` value is adjusted against an observed run result in this phase; iteration is conformance-only and any pressure to tune is routed to the owner as a new decision (SCOPE-37).
  5. The sole preserved held-out evaluation is invoked **exactly once**, on the pre-registered seed, only after its three preconditions (the v2.2 EVAL-01 structure, adapted for the new recipe) are verified and recorded, and only after a dataset-free regression **and** a pre-invocation assertion prove the evaluator pairs canonical predicted `r′` with `u = t/T` (GAP-46-01's delegated ruling, 2026-07-26). **Terminal branch:** if GATE-04 refused the recalibration or RUN-04's front still fails to advance, the evaluation is **not** spent — it is preserved unspent, that fact is recorded, and the phase closes there rather than iterating (SCOPE-35, SCOPE-37).

### Phase 58: Verdict & Traceability Close

**Goal**: The owner grades the recalibrated design, and the milestone's traceability obligation closes against what the milestone actually became.
**Depends on**: Phase 57 (the corrected re-run and the evaluation — or the recorded terminal branch in which the evaluation was preserved unspent).
**Requirements**: DIAG-06, VER-21
**Plans**: TBD

**Success Criteria** (what must be TRUE):

  1. **Owner checkpoint ⑤ is discharged:** the owner renders a **go / adjust / rethink** verdict on the recalibrated design, recorded with the evidence it was rendered on (the v2.0 ACC-06 pattern) — the second attempt at the verdict v2.2's Phase 51 never reached (DIAG-06).
  2. The verdict's consequence is stated explicitly: Stage-1+ and PLAT-01..07 re-open **only** on `go`; on `adjust` or `rethink` SCOPE-36 continues to block them and the routing of the next milestone is named (DIAG-06, SCOPE-36).
  3. **The declared terminal state is honored:** if GATE-04 refused the recalibration or RUN-04's front failed to advance, the verdict is rendered `rethink`-flavored on that evidence, the held-out evaluation is recorded as **preserved unspent**, and the milestone closes there — SCOPE-37 bars a further tuning pass without a new owner decision, and this outcome is a clean close, not a drift.
  4. Every v2.3 requirement maps to exactly one phase, with no orphans and no duplicates, re-verified **at close** against the final requirement count rather than carried forward from this roadmap's 15/15 check — and read the way v2.2's CONF-09 lesson requires: a passing coverage count is evidence of no *orphans*, never of no *gaps* (VER-21).

## Progress

**Execution Order:** 53 ∥ 54 ∥ 55 → 56 → 57 → 58 — three independent openers, then strict dependency order. The ratified sequencing puts the four narrow VER-20 items (Phase 53) first precisely because they have no research dependency, so even a worst-case v2.3 discharges four of five routed amendments; Phase 54 (the ERW packet → owner gate → ruling or `trainex-r3`) and Phase 55 (the characterization probe) are independent of it and of each other. Phase 56 is hard-gated on **both** 54 (the ratified decision — SCOPE-34 admits no substitute) and 55 (the instrument GATE-04 fires), then 57 (corrected re-run + the single preserved evaluation) and 58 (verdict + traceability close) follow in order. The declared terminal state is the milestone's only branch: a GATE-04 refusal or a still-failing RUN-04 front routes straight to a `rethink`-flavored DIAG-06 with the evaluation preserved unspent, and Phases 57 and 58 both carry it. Unlike v2.2 this milestone *does* contain an external-research gate — but it is the governed ERW channel at checkpoint ①, not a generic web-research pass, which SCOPE-34 and the STOP protocol forbid.

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 53. Narrow Spec Codification | v2.3 | 1/1 | In Progress|  |
| 54. Recalibration Decision Grounding | v2.3 | 0/? | Not started | - |
| 55. Architecture Characterization Probe | v2.3 | 0/? | Not started | - |
| 56. Contract Amendment & Train-Free Gate | v2.3 | 0/? | Not started | - |
| 57. Corrected Re-Run & the Preserved Evaluation | v2.3 | 0/? | Not started | - |
| 58. Verdict & Traceability Close | v2.3 | 0/? | Not started | - |

---
*v2.3 created 2026-08-18 (`/gsd-new-milestone`, roadmap generated inline from the owner-ratified v2.3 roadmap proposal `docs/work/designs/cross_cutting/v2.3-milestone-proposal/2026-08-17-v2.3-roadmap-proposal.md`, ratified 2026-08-18 at `16434f50` — the v2.0/v2.1/v2.2 precedent; no GSD domain-research spawn, since external research for this milestone is routed through the governed ERW channel (ERW-01/02) and a generic web-research pass would produce exactly the unratified remedy analysis SCOPE-34 and the STOP protocol forbid). 6 phases (53–58) continuing numbering from v2.2's Phase 52; 15/15 requirements mapped (SPEC-02..05→53, ERW-01/02→54, INST-04→55, SPEC-01+SPEC-06+GATE-04→56, RUN-04/05+EVAL-02→57, DIAG-06+VER-21→58) — a one-to-one mapping onto the proposal's ratified A–F sequencing, with no merges, splits, or reordering. Grounded in the locked framework specs, v2.2's closure record, and the premise-qualified trainex-r2 report; scope boundaries SCOPE-33..38 are hard constraints and the five owner checkpoints are blocking. v2.2 archived under [`milestones/v2.2-*`](milestones/) (roadmap, requirements, gaps, phase dirs); its four inherited obligations are covered by SPEC-01 (obligation 1), EVAL-02 (2), SPEC-02..05 (3), and the "not reopened" grounding clause (4).*
