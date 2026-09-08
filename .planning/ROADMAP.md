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

**Milestone Goal:** Get a properly grounded recalibration decision for the causal-weight/SIREN-scale mismatch — assembled and framed by the agent, then owner-authorized either by direct ruling or express delegation, and externally researched via the ERW build-design channel if the assembled packet does not support a ruling — implement it as a framework-spec **contract amendment** (finally legal here; SCOPE-30 does not carry forward), prove the fix train-free before spending a run, re-run Stage-0 under the corrected recipe, and spend the single preserved held-out evaluation on a run that actually trains. **What this milestone deliberately does not do:** re-litigate the nine v2.2 conformance repairs (settled, not reopened), re-run DIAG-05 (superseded by `52-DIAG-05-REDERIVATION.md`, not re-litigated), open Stage-1+/PLAT-01..07 (still blocked by the v2.0 `adjust` verdict until a `go` verdict is rendered here), or author a remedy without owner authority (SCOPE-34).

**Granularity:** standard (6 phases, 15 requirements: ERW-01..02, SPEC-01..06, INST-04, GATE-04, RUN-04..05, EVAL-02, DIAG-06, VER-21)
**Coverage:** 15/15 v2.3 requirements mapped at roadmap creation (VER-21's binding check is at Phase 58 close, against the final requirement count, not this one)
**Branch:** work continues in `.worktrees/trainex` on `milestone/v2.3`, created 2026-08-18 from `milestone/v2.2` at `16434f50` — the commit that carries the owner-ratified v2.3 proposal, so the branch point and the ratification are the same fact. Per-plan atomic commits via `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set; no push to protected branches (`master`, `main`, `milestone/*`); `master` remains governance-only and integration is user-controlled.

### Adjudication discipline (applies to all phases)

- **Hard boundaries (SCOPE-33..38):** framework-spec edits **ARE** authorized, narrowly — only `52-VER-20-ROUTING-HANDOFF.md` items (a)–(e) plus the `n_col`/`N_t` disposition coupled to item (e); SCOPE-30 does **not** carry forward, and nothing here licenses open-ended spec rewriting (SCOPE-33). **The recalibration decision is owner-ratified, never agent-decided absent express delegation** — the agent assembled and framed the packet and trainex-r3 round without picking; at checkpoint ② on 2026-09-04 the owner expressly delegated the final adjudication to the Codex primary agent using its best mathematical and scientific reasoning, recorded verbatim in `54-RULING.md`. That exception is checkpoint-specific and does not relax any later owner gate or SCOPE-37 (SCOPE-34). **Exactly ONE held-out evaluation** — the one preserved unspent from v2.2 — spent only on a run passing its preconditions, only after the recalibrated recipe actually trains (causal front advances), and only on a seed pre-registered before RUN-04/05 execute (SCOPE-35). **Stage-0 only** — no Stage-1+, no PLAT-01..07, unchanged from v2.2 and still blocked by the v2.0 `adjust` verdict pending a `go` at DIAG-06 (SCOPE-36). **Iteration after the spec edit lands is conformance-only again** — once the new `η_c` / normalization / SIREN-scale / `N_t` values are locked, no further tuning against observed re-run results without a new owner decision, which is what keeps a second failure informative (SCOPE-37). **Amending a locked contract requires explicit re-ratification** — `η_c` (LOSS-04 / D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A / AC-LOSS-04, `pinn_architecture.md:424`), `first_omega_0` (§2.2:167, *"fixed at 30 and is not scheduled during training"*), the causal-exponent clip's *"required only to avoid underflow"* purpose, and the GAP-39-12 collocation time-draw clause each carry a contract marker touched or reviewed by the ruling. The four SCOPE-38 blocks in `54-RULING.md` record provenance, the superseded ruling and the re-issued or unchanged criterion. A changed number or formula without that record is not a legal v2.3 edit (SCOPE-38).
- **No phase may plan an unratified agent-chosen value.** SCOPE-34 binds planning, not only execution. The checkpoint-② values in `54-RULING.md` are now ratified through the owner's express delegation and may be transcribed and verified downstream. Any further value, tuning choice or change remains blocked and is routed as a gap.
- **Grounding (authoritative inputs):** the **locked framework specs** (`ctl_instruction.md`, `pinn_architecture.md` — v1.4/v1.5/v1.6) as amended by this milestone's own VER-20-item decisions under SCOPE-38's discipline; **v2.2's closure record** — the residual-frame conformance audit (`docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md`, committed `ae14a99e`), `52-DIAG-05-REDERIVATION.md` (the operative diagnosis, superseding `44-DIAGNOSIS.md`/`44-ERRATUM.md`'s under-determined rankings — treated as settled, not re-litigated), `52-VER-20-ROUTING-HANDOFF.md`, and `.planning/milestones/v2.2-GAPS.md` "Milestone close"; and the **trainex-r2 research report** (`pinn_instruction/markdown_conversion/framework-specs/trainex-r2/`), **now legally a grounding source** per SCOPE-31's own text, **with a mandatory premise qualification that travels with every citation of it**: that round's output contract (`RESEARCH-CONTEXT-MASTER.md` §7, clause 3) reads *"Do not recommend a remedy"*, so it contains no decision sheet, no options menu, no suggested defaults, and no one-way/two-way door classification. Its Q3 frames the diagnosis and independently derived the `ω₀=30` mechanism as a hypothesis (now confirmed); it does **not** contain the answer. **Not reopened:** the 14D `[τ, IC₁₃]` input, Jacobi IC₁₃, the mass-weighted COM projection head, PHYS-03 softening `eps_soft = 1e-5`, the post-v1.3 SCS gate, the raw-mass `D ≈ 4.6416` convention (`D³ = G T²`), and the full v1.5/v1.6/v2.0/v2.1/v2.2 DataLoader, validation, and conformance contracts (PIPE-01..10, VAL-01..04, CONF-01..09, INST-01..03, GATE-01..03, TEST-01..02).
- **Owner checkpoints (blocking, never auto-decided absent explicit delegation):** ① **the ERW gate** — discharged 2026-08-21 by commissioning `trainex-r3`. ② **the recalibration decision** — discharged 2026-09-04 under the owner's express delegation; `54-RULING.md` is the authorizing record and binds SPEC-01/SPEC-06 jointly. ③ **invariant-B window and fixed-monitor re-ratification** — discharged by direct owner ruling 2026-09-08: `N = 500`, one frozen training-only monitor, and L-BFGS samples/causal weights frozen for the entire segment. ④ **pre-registration of the EVAL-02 spending seed** — discharged 2026-09-08: seed 42, fallback 41 then 43 only for structural ineligibility. `57-RULING.md` is the exact checkpoint-③/④ record. ⑤ **the DIAG-06 go / adjust / rethink verdict** (Phase 58), after RUN-04/05 and EVAL-02, remains owner-only.
- **Declared terminal state:** if GATE-04 refuses the recalibration train-free, or RUN-04's causal front still fails to advance under the ratified recipe, **SCOPE-37 forbids further tuning without a new owner decision.** The milestone then closes on a `rethink`-flavored DIAG-06 verdict with the held-out evaluation **preserved unspent** — declared here up front, so that outcome is a clean close rather than a drift. Phases 57 and 58 both carry this branch explicitly. This is v2.2's lesson written into v2.3's roadmap: the terminal branch must be named before it is needed.
- **Gap discipline:** any source-silent physics/spec adjudication call is recorded in the phase-local `NN-GAPS.md` **and** the milestone index `.planning/milestones/v2.3-GAPS.md` (created on the first gap, standing trigger) and routed to the owner — never decided inline (the build-track analog of the STOP protocol). The class is wider here than in a normal build milestone: under SCOPE-34 every recalibration sub-question is MUST-surface by construction, and under SCOPE-38 any spec value the owner's ratification does not explicitly cover is a gap, not a default.

## Phases

**Phase Numbering:** integer phases 53–58 continue from v2.2's Phase 52 (numbering does not reset). Decimal phases reserved for urgent insertions.

- [x] **Phase 53: Narrow Spec Codification** — The four VER-20 items with no research dependency, discharged first so the milestone ships them regardless of how the recalibration lands: §4.1's `λ_phys^max` line restated as **locked** rather than defaulted (GAP-45-03), a spec convention for marking locked-vs-default values *inside a table*, the `L_data` reduction — mean over time, bodies, and spatial components (GAP-45-01, owner option A, 2026-07-31) — written into prose rather than left inferable from code, and the held-out physics gate's aggregate statistic codified as **worst-case max** (GAP-44-01, owner-ruled 2026-07-23). Each is a transcription of an already-ratified owner ruling; none touches a contract-marked value, so SCOPE-38 does not fire. (SPEC-02, SPEC-03, SPEC-04, SPEC-05) (completed 2026-08-19)
- [x] **Phase 54: Recalibration Decision Grounding** — The governed decision channel, staged as ratified: ERW-01 assembles a **strictly non-recommending** decision packet (the confirmed mechanism; the coupled remedy surfaces `η_c`, `R̄` normalization against a reference scale, the SIREN init scale `ω₀`, `N_t`/`n_col`, and the clip's declared semantics; what v2.2's evidence already settled from trainex-r2 Q3; and an explicit statement of what the assembled evidence **cannot** answer), a **blocking owner gate** then rules directly or commissions `trainex-r3`, and ERW-02 discharges whichever branch fires — a recorded ruling with its provenance, or a Route-B (open-book) build-design round carrying the full ERW Rule-7 output contract trainex-r2 deliberately lacked plus the mandatory Rule-19 per-claim in-repo verification pass. The packet doubles as the `trainex-r3` `RESEARCH-CONTEXT-MASTER.md`, so neither branch wastes work. **Owner checkpoints ① and ②.** (ERW-01, ERW-02) (completed 2026-09-04)
- [x] **Phase 55: Architecture Characterization Probe** — v2.3's central premise currently rests on an ad-hoc measurement that exists nowhere in the repository, and `pinn/verification/` has no such probe. INST-04 lands it as committed, tested tooling: for a given `ArchitectureSpec` at initialization — **no data, no optimizer, no training step** — it reports `‖r′‖`, `‖v′‖`, `‖a′‖ = ‖d²r′/du²‖`, `‖F_grav‖`, minimum pairwise separation, median `R̄`, the full causal weight vector, and `front_idx` over a configurable seed/IC sweep, and reproduces the 2026-08-17 audit's six-row table. Independent of the ERW branch; runs in parallel with Phases 53 and 54. It is also the instrument Phase 56's GATE-04 fires, so it must exist before the gate can. (INST-04) (completed 2026-09-06)
- [x] **Phase 56: Contract Amendment & Train-Free Gate** — The ratified recalibration becomes spec law under SCOPE-38 amendment discipline — naming the superseded LOSS-04 / D-04 / AC-LOSS-04 ruling, recording the new decision's provenance, carrying a re-issued acceptance criterion, and applying the same discipline separately to `first_omega_0` and to the clip's underflow-only purpose if the remedy touches them — with the `n_col`/`N_t` disposition ratified **jointly**, since `w_n` is an exclusive prefix sum over collocation points and `η_c`'s calibration therefore moves by roughly 256× between the code's `collocation_count = 16` and §3.2's `n_col = 4096`. GATE-04 then makes INST-04's probe a **fail-closed** precondition on RUN-04: no causal weight pinned at the dtype clamp floor, a weight vector carrying differential information, and `front_idx` able to advance. Hard-gated on Phases 54 and 55. (SPEC-01, SPEC-06, GATE-04) (completed 2026-09-07)
- [ ] **Phase 57: Corrected Re-Run & the Preserved Evaluation** — Stage-0 re-runs end-to-end under the SPEC-01/SPEC-06-corrected recipe with invariant B required to show the causal front **actually advancing** — not merely no-longer-saturated — inside the re-ratified window; the three-seed band is re-established on the v2.0/v2.2 protocol so the runs are comparable; and the **sole preserved held-out evaluation**, the one v2.2 never attempted, is spent **once** on the pre-registered seed after its three preconditions and the `r′` ↔ `u = t/T` pairing proof. Iteration is conformance-only (SCOPE-37). **Owner checkpoints ③ and ④, both discharged before any run executes.** Carries the declared terminal state: a GATE-04 refusal or a still-failing front means the evaluation is **not** spent. (RUN-04, RUN-05, EVAL-02)
- [ ] **Phase 58: Verdict & Traceability Close** — The owner renders the final **go / adjust / rethink** verdict on the recalibrated design — the second attempt at the verdict v2.2's Phase 51 never reached, and the gate that governs whether Stage-1+/PLAT-01..07 re-open — and VER-21's traceability is re-verified at close against the **final** requirement count rather than carried forward from this roadmap's check, reading it the way v2.2's CONF-09 lesson requires. **Owner checkpoint ⑤.** (DIAG-06, VER-21)

## Phase Details

### Phase 53: Narrow Spec Codification

**Goal**: The four VER-20 items that need no research are settled in the spec text, so a worst-case v2.3 still discharges four of the five routed amendments.
**Depends on**: Nothing — ungated first v2.3 phase (ratified sequencing track A). Runs in parallel with Phases 54 and 55.
**Requirements**: SPEC-02, SPEC-03, SPEC-04, SPEC-05
**Plans:** 1/1 plans complete

Plans:

- [x] 53-01-PLAN.md — convention preamble + PHYS-05 marking + adjudication re-key (tracer), L_data reduction correction, §10.6 aggregate-statistic subsection

**Success Criteria** (what must be TRUE):

  1. `pinn_architecture.md` §4.1's `λ_phys^max` line states that the PHYS-05 per-stage table is **locked**, no longer reads as a tunable default, and cites GAP-45-03's ratification that the full table binds (SPEC-02).
  2. The spec carries a stated convention that distinguishes a locked constant from an illustrative default **inside the same table**, and §4.1's PHYS-05 table is marked under it — so SPEC-02's instance is closed by the convention rather than by a one-off rewording of a systemic problem (SPEC-03).
  3. A reader can determine the `L_data` reduction — **mean over time, bodies, and spatial components** — from spec prose alone, without consulting `pinn/`, with the owner's GAP-45-01 option-A ruling (2026-07-31, Phase 48 checkpoint) cited as its authority (SPEC-04, CONF-07).
  4. The held-out physics gate's aggregate statistic is written in spec prose as **worst-case max** — explicitly not mean and not median — citing the owner's 2026-07-23 GAP-44-01 ruling that was never written into the spec (SPEC-05).
  5. Every edit in this phase is a transcription of an already-ratified ruling: none changes a value or formula carrying an owner-ratified contract marker, so no SCOPE-38 amendment is triggered, and any wording question the rulings do not answer is routed as a gap rather than decided inline (SCOPE-33, SCOPE-34).

### Phase 54: Recalibration Decision Grounding

**Goal**: Exactly one owner-authorized recalibration decision exists, reached through the governed channel — the agent framed the question and the owner either ruled directly or expressly delegated the adjudication.
**Depends on**: Nothing — ungated (ratified sequencing track B). Runs in parallel with Phases 53 and 55; its ratified output hard-gates Phase 56.
**Requirements**: ERW-01, ERW-02
**Plans:** 13 plans (13/13 complete) — **ERW-01 and ERW-02 complete.** Checkpoint ① commissioned `trainex-r3` on 2026-08-21. Two reports delivered on 2026-08-30; intake recorded their access-mode divergence; Rule-19 verification assigned 148 verdicts to 138 claim rows; premise adjudication returned `REFRAME-PARTIAL` / `CONSOLIDATION-AUTHORIZED=YES`; Rule-12 consolidation retained 230/230 attributions and zero candidate-sheet picks. Checkpoint ② was presented neutrally on 2026-09-03 and discharged on 2026-09-04 under the owner's express delegation to the Codex primary agent. `54-RULING.md` ratifies `A1 + B2 (residual-wide) + C1 + D3 + E1`, corrects Phase 54's too-narrow source trace by restoring prior owner ruling GAP-39-12's 4096-total-per-batch unit, and carries four complete re-ratification blocks. GAP-54-06 was deferred there and later resolved at Phase-57 checkpoint ③ on 2026-09-08; all eleven Phase-54 gaps now have resolved dispositions. UAT 10/10; verification 10/10; Nyquist 5/5; security 55/55 with zero blocking threats.

Plans:

- [x] 54-01-PLAN.md — wave 1, **tracer**: create the `trainex-r3` round root, the master's full §0–§10 skeleton with `access_mode: open-book` and its `source_baseline` pin, the §0 trainex-r2 premise-qualification block, the §10 neutrality-self-audit definition, and `DELIVERY-NOTE.md` end to end; verify the four standing bars (D-01, D-02, D-03, D-04, D-06, D-09)
- [x] 54-02-PLAN.md — wave 2: the evidence core — §1 Orientation, §4 the confirmed mechanism transcribed inline with corrected `file:line` citations plus the five decision surfaces in no-menu form, §6 the claims register with the trainex-r2 hypothesis-to-fact transition (D-05, D-06, D-07)
- [x] 54-03-PLAN.md — wave 2: `54-GAPS.md` and the new `.planning/milestones/v2.3-GAPS.md` carrying the single `GAP-54-01` anchor, plus `54-RULING.md`, the checkpoint-① gate stub with zero candidate values and the `N_t` completeness rule pre-declared (D-08, D-09, D-10)
- [x] 54-04-PLAN.md — wave 3: §2 Manifest with the r2→r3 role map, §3 Route-B source tiering, §5 the framed questions, §7 what the assembled evidence cannot answer, §8 Provenance, §9 the ERW Rule-7 output contract (the D-04 Layer-2 carve-out)
- [x] 54-05-PLAN.md — wave 4, **blocking**: run the ERW-01-applicable audit battery and record every result into §10, then present **owner checkpoint ①** and halt (D-04, D-11)
- [x] 54-06-PLAN.md — wave 5: reconcile the 2026-08-21 out-of-band assembly pass; retire the two-path tree-completeness guard; re-derive every hand-run audit result; correct ROADMAP / STATE / VALIDATION accounting from disk
- [x] 54-07-PLAN.md — wave 6: certify the commissioned round-root set against the ERW handoff rules; write the deferred-replan routing note; present the blocking owner handoff
- [x] 54-08-PLAN.md — wave 1 (post-delivery): certify the two returned reports at intake (ERW Rules 7, 12, 14); record the ERW Rule-16 access-mode divergence and derive a verification burden per report; fix the claim-class independence taxonomy; stamp the ERW Rule-20 live-tree pin per engagement and prove the pinned tree identical to the verifying tree across every cited path (D-11, D-12, D-14, D-15, D-18)
- [x] 54-09-PLAN.md — wave 2 (post-delivery): create the mandatory ERW Rule-19 verification report under `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/` and discharge the open-book half — every repository-derived claim re-derived independently with its command, its output and a verdict from a closed vocabulary; claims not re-derivable here routed with what would settle each (D-12, D-13)
- [x] 54-10-PLAN.md — wave 3 (post-delivery): discharge the closed-book half in the same report — anchor-provenance triage into relayed / reconstructed / untraceable, content resolution against the pinned tree, the closed-book claim ledger, and the cross-report independence ledger that decides where agreement is corroboration and where it is attachment-fidelity evidence only (D-12, D-14)
- [x] 54-11-PLAN.md — wave 4 (post-delivery): adjudicate every premise challenge against the packet premise it challenges using the recorded verdicts; record the re-frame determination per round and per surface; route to the owner every surfaced decision point no source settles, with the STOP-protocol field schema complete; a halting determination is written as a gap and presented at a **conditional blocking owner gate**, which stops the pass before consolidation (D-09, D-10, D-15, D-16, D-17)
- [x] 54-12-PLAN.md — wave 5 (post-delivery): the ERW Rule-12 consolidation into `trainex-r3-resolution-doc.md`, running the delivery note's Rule-11 join points in their recorded order, with a decision-row cross-walk onto the packet's surfaces and a candidate sheet attributed throughout and left unfilled (D-14, D-18)
- [x] 54-13-PLAN.md — wave 6 (post-delivery), **blocking**: `54-RULING.md`'s checkpoint ② section prepared additively with pointers and no candidates (commit `cdcbef1a`, 2026-09-03); the blocking owner gate presented and execution halted. The owner-delegated ruling followed on 2026-09-04, closing Phase 54 and GAP-54-01 only after post-ruling UAT and verification passed (D-08, D-09, D-18)

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
**Plans**: 4 plans (4/4 complete) — verification 12/12 (`55-VERIFICATION.md`, status passed; re-verified at HEAD 2026-09-06 after closeout). Code review recorded 2 warnings / 2 info (`55-REVIEW.md`, advisory). Nyquist `/gsd-validate-phase 55` discharged (`55-VALIDATION.md`, `nyquist_compliant: true`, 14/14 rows COVERED, 0 gaps); security `/gsd-secure-phase 55` discharged (`55-SECURITY.md`, `status: verified`, `threats_open: 0`, 21 threats); UAT `/gsd-verify-work 55` complete (`55-UAT.md`, 20/20 coverage-auto-covered, 0 issues). `55-COVERAGE.md` records the no-external-API declaration (`api-coverage.verify-pre` false positive on the module's own "public API" phrasing). `gsd-tools phase uat-passed 55 --require-verification` → `passed: true`; `ready_to_transition: true`. Closed 2026-09-06 (`55-CLOSE-CHECK.sh` → `PHASE55-CLOSE-PASS`).

Plans:
**Wave 1**

- [x] 55-01-PLAN.md — wave 1: tracer slice measuring one seed end-to-end through the trainer's own AD / force / causal-weight chain to all seven INST-04 quantities, then the six audited default cases and the Tier-1 invariant-bound regression net, plus the SC3 mutation proof (D-01 tier 1, D-02 Python surface)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 55-02-PLAN.md — wave 2: the `argparse` CLI whose zero-argument invocation reproduces the six audited rows, the `--cases-config` surface, the re-derivable evidence writer with git tree-state provenance, and the one documented `_EXCLUDE_SUFFIXES` entry the defaulted precision flag requires in `tests/phase38/test_prohibitions.py` (D-02 CLI surface)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 55-03-PLAN.md — wave 3, **checkpoint-gated**: the ratified 4096-total / 256-per-bin / 16-bin stratification and bin-mean helpers, unit-tested against synthetic arrays only, with two mechanical containment tests proving they are unreachable from the default sweep (D-03)

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 55-04-PLAN.md — wave 4: the committed Tier-2 exact-value baseline with its regeneration provenance and byte-stability proof, and the one committed evidence run cross-checked row by row against the 2026-08-17 audit §6b table (D-01 tier 2, ROADMAP SC2)

**Success Criteria** (what must be TRUE):

  1. `pinn/verification/` contains committed, tested tooling that, given an `ArchitectureSpec` at initialization and **no data, no optimizer, and no training step**, reports `‖r′‖`, `‖v′‖`, `‖a′‖ = ‖d²r′/du²‖`, `‖F_grav‖`, minimum pairwise separation, median `R̄`, the full causal weight vector, and `front_idx` over a configurable seed/IC sweep (INST-04).
  2. Run under the pre-amendment recipe, the probe **reproduces the 2026-08-17 residual-frame conformance audit's six-row table** across the same six seed/IC combinations — `R̄ ≈ 10¹⁰` and `front_idx = 0` in every row — and the reproduction is recorded re-derivably (command, tree state, full output) per the GAP-44-02 discipline, so the milestone's premise no longer rests on an unrepeatable measurement.
  3. The probe derives `R̄` and the causal weights from the same implementation the trainer uses, so a probe result is evidence about the shipped recipe rather than about a parallel re-implementation of it.
  4. A test suite fails if any reported quantity, the sweep configuration, or the six-row reproduction regresses — the probe is protected the way the Phase 49 gate work is, not left as a script.

### Phase 56: Contract Amendment & Train-Free Gate

**Goal**: The ratified recalibration is law in the framework specs under SCOPE-38's amendment discipline, and a train-free gate refuses to let a Stage-0 run be spent on a recipe whose causal weighting is still saturated shut.
**Depends on**: Phase 54 (the ratified decision — SCOPE-34 forbids opening this phase without it, including its `N_t` disposition) **and** Phase 55 (the probe GATE-04 fires). Both are hard gates, not preferences.
**Requirements**: SPEC-01, SPEC-06, GATE-04
**Plans**: 6/6 plans executed and verified — planned 2026-09-06; all six executed 2026-09-06/07; `56-VERIFICATION.md` passed 6/6 must-haves with GAP-56-01 explicitly carried as an accepted owner-routed override. GAP-56-01 was subsequently resolved by direct owner ruling on 2026-09-08; its production implementation and a new complete GATE-04 PASS are Phase-57 pre-run work. GAP-56-02 (§2.4 Table 1 locked-vs-default convention scope) remains open and independent. The historical gate run over the six default cases remains `PASS INCOMPLETE (unratified: ii)` and is not RUN-04 authorization (`.planning/phases/56-contract-amendment-train-free-gate/evidence/gate04/20260907T033409Z/`).

Plans:
**Wave 1**

- [x] 56-01-PLAN.md — tracer slice: GATE-04's fail-closed condition (i) path end to end (probe helper → trainer loss function → verdict → persisted `R_ref` artifact → committed test), behind a `checkpoint:decision` freezing the Phase-57-facing public contract (GATE-04)
- [x] 56-04-PLAN.md — spec amendment §3.2: Block 1 (causal-exponent contract, AMENDED additively), the frozen `R_ref` definition and its verbatim invalidation-trigger list, and Block 4 (collocation allocation and time-draw contract, AMENDED) (SPEC-01, SPEC-06)

**Wave 2**

- [x] 56-02-PLAN.md — GATE-04 expansion: condition (iii) front-capability structure, condition (ii)'s never-satisfiable unratified slot, and the operator CLI with its provenance-complete evidence record (GATE-04)
- [x] 56-05-PLAN.md — spec amendment completion: both NOT AMENDED contracts recorded separately by name, the three secondary wordings (`collocation_count` reconciliation, recommended-range, `η_c` cross-reference), render-oracle re-adjudication, and the committed content-match guard (SPEC-01, SPEC-06)

**Wave 3**

- [x] 56-03-PLAN.md — SC5 demonstration: the pre-amendment recipe frozen as a committed fixture, and the same verdict function proven to return BLOCK on all six audited cases (GATE-04)

**Wave 4**

- [x] 56-06-PLAN.md — phase close-out: `56-OPEN-ITEMS.md` (GAP-56-01, GAP-56-02, the two `front_idx` structural findings, and the `tests/phase38` stale-guard scoping decision), plus the authoritative GATE-04 run and its evidence (GATE-04, SPEC-01)

**Success Criteria** (what must be TRUE):

  1. `pinn_architecture.md` §2.2/§3.2 carries the ratified recalibration as a **formal contract amendment**, not a value edit: it names the superseded ruling (**LOSS-04 / D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A / AC-LOSS-04**, `pinn_architecture.md:424`, grounded in the v1.6 resolution doc §1.1 and GAP-32-01), records the new decision's provenance, and carries a **re-issued acceptance criterion** (SPEC-01, SCOPE-38).
  2. If the ratified remedy touches `first_omega_0` (§2.2:167, *"fixed at 30 and is not scheduled during training"*) or the causal-exponent clip's *"required only to avoid underflow"* purpose, each is amended under the same discipline **separately and by name** — a remedy that silently repurposes the clip as a floor-raiser is not a legal edit (SCOPE-38).
  3. The `n_col` spec/code divergence is disposed of in the same ratification: the amended spec records the `N_t` the calibration binds to, reconciles `pinn/train.py:1033`'s `collocation_count = 16` against §3.2's `n_col = 4096` ("recommended: 2048–4096", `:433`, `:440`), and states the re-check trigger that fires if `N_t` ever changes — because `w_n` is an exclusive prefix sum over collocation points, so calibrating at 16 and later honoring 4096 would move the exponent by roughly 256× (SPEC-06).
  4. GATE-04 is wired **fail-closed** ahead of RUN-04: under the SPEC-01/SPEC-06 recipe and across at least the audit's six seed/IC combinations, INST-04's probe must show (i) no causal weight pinned at the dtype clamp floor, (ii) at least a `2:1` spread among non-anchor weights, and (iii) under the fixed all-residual reduction `alpha = log(2)/(2 * P_15)`, expected final weight `1/sqrt(2)`, `front_idx = 15`, and every perturbed weight `>= 0.70`; a probe failure **blocks** the run rather than warning about it (GATE-04, owner ruling 2026-09-08).
  5. The gate is demonstrated to refuse: fired against the pre-amendment recipe it produces a blocking failure, so a passing result on the amended recipe is evidence rather than a no-op. This is the check that would have spared v2.2's generation-3 run.

### Phase 57: Corrected Re-Run & the Preserved Evaluation

**Goal**: Stage-0 is re-run under the corrected recipe and — only if it actually trains — the single preserved held-out evaluation is spent, once, on a seed fixed before anyone saw a result.
**Depends on**: Phase 56 — GATE-04 must pass before a Stage-0 run may be spent (SCOPE-35's single-look protection).
**Requirements**: RUN-04, RUN-05, EVAL-02
**Plans**: 6 plans (1/6 complete) — planned 2026-09-08. Plans 57-01 through 57-04 are the bounded conformance, verification, and pre-run authorization work; 57-05 and 57-06 are non-autonomous and retain explicit operator checkpoints before expensive training and before the sole held-out evaluation.

Plans:

**Wave 1**

- [x] 57-01-PLAN.md — Wave-0 stdlib `unittest` contracts for the real production path, normalization and gradients, monitor/window and L-BFGS freeze semantics, exact GATE-04, immutable band evidence, and the one-look boundary (RUN-04, RUN-05, EVAL-02) — complete 2026-09-08, 46 tests committed, all RED for missing production conformance (see `57-01-SUMMARY.md`)

**Wave 2** *(blocked on Wave 1 completion)*

- [ ] 57-02-PLAN.md — exact 4096-row / 16-bin all-slot allocation, frozen-`R_ref` causal normalization, controller integration, live model gradients, energy-point reuse, and raw/normalized diagnostics (RUN-04)

**Wave 3** *(blocked on Wave 2 completion)*

- [ ] 57-03-PLAN.md — strict runtime configuration, one frozen training-only invariant-B monitor distinct from the 500-accepted-step deadline, segment-frozen L-BFGS samples/weights with exact resume, and derived smoke/band configs (RUN-04, RUN-05)

**Wave 4** *(blocked on Wave 3 completion)*

- [ ] 57-04-PLAN.md — fresh exact six-case GATE-04 and governed `R_ref`, separate final-artifact-bound production conformance, canonical evaluator pre-access assertion, and Phase-57 evidence tooling (RUN-04, RUN-05, EVAL-02)

**Wave 5** *(blocked on Wave 4 completion; operator checkpoint before compute)*

- [ ] 57-05-PLAN.md — immutable-HEAD seed-42 smoke and seeds 41/42/43 Stage-0 band, or the ratified scientific terminal-unspent state; resource and operational failures remain incomplete rather than being normalized into success (RUN-04, RUN-05)

**Wave 6** *(blocked on Wave 5 completion; operator checkpoint before the held-out look)*

- [ ] 57-06-PLAN.md — structural-only candidate selection in order 42, 41, 43; immediate three-precondition and canonical-frame proof; exactly one evaluation invocation or a durable authorized unspent record (EVAL-02)

Cross-cutting constraints:

- The production and verification paths require exactly 4096 physics rows in 16 equal-time bins, contributions from every selected slot, and the one frozen governed `R_ref`; resource failure blocks rather than reducing the sample count.
- The invariant-B monitor is one frozen training-only context and is independent of the re-ratified 500-accepted-step no-advance deadline; L-BFGS samples and detached causal weights remain frozen for the full segment and across resume.
- No Stage-0 run starts without both a fresh complete six-case GATE-04 PASS and separate production-path conformance bound to the same final `R_ref` provenance.
- The smoke and every attempted graded run share one immutable fingerprinted HEAD, and the held-out evaluation remains inaccessible until structural selection and all three preconditions pass immediately before its sole invocation.

**Success Criteria** (what must be TRUE):

  1. **Owner checkpoint ③ is discharged before any run executes:** `N = 500` is explicitly re-ratified for the amended recipe; invariant B uses one frozen training-only monitor; L-BFGS samples and detached causal weights remain frozen for the entire segment. The ruling and its provenance are recorded in `57-RULING.md` and must be wired into the run configuration and checkpoint path.
  2. **Owner checkpoint ④ is discharged before any run executes:** `57-RULING.md` pre-registers seed 42, with fallback 41 then 43 only for structural ineligibility, before any RUN-04/05 result exists (SCOPE-35).
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
| 53. Narrow Spec Codification | v2.3 | 1/1 | Complete    | 2026-08-19 |
| 54. Recalibration Decision Grounding | v2.3 | 13/13 | Complete | 2026-09-04 |
| 55. Architecture Characterization Probe | v2.3 | 4/4 | Complete | 2026-09-06 |
| 56. Contract Amendment & Train-Free Gate | v2.3 | 6/6 | Complete    | 2026-09-07 |
| 57. Corrected Re-Run & the Preserved Evaluation | v2.3 | 1/6 | In progress | - |
| 58. Verdict & Traceability Close | v2.3 | 0/? | Not started | - |

---
*v2.3 created 2026-08-18 (`/gsd-new-milestone`, roadmap generated inline from the owner-ratified v2.3 roadmap proposal `docs/work/designs/cross_cutting/v2.3-milestone-proposal/2026-08-17-v2.3-roadmap-proposal.md`, ratified 2026-08-18 at `16434f50` — the v2.0/v2.1/v2.2 precedent; no GSD domain-research spawn, since external research for this milestone is routed through the governed ERW channel (ERW-01/02) and a generic web-research pass would produce exactly the unratified remedy analysis SCOPE-34 and the STOP protocol forbid). 6 phases (53–58) continuing numbering from v2.2's Phase 52; 15/15 requirements mapped (SPEC-02..05→53, ERW-01/02→54, INST-04→55, SPEC-01+SPEC-06+GATE-04→56, RUN-04/05+EVAL-02→57, DIAG-06+VER-21→58) — a one-to-one mapping onto the proposal's ratified A–F sequencing, with no merges, splits, or reordering. Grounded in the locked framework specs, v2.2's closure record, and the premise-qualified trainex-r2 report; scope boundaries SCOPE-33..38 are hard constraints and the five owner checkpoints are blocking. v2.2 archived under [`milestones/v2.2-*`](milestones/) (roadmap, requirements, gaps, phase dirs); its four inherited obligations are covered by SPEC-01 (obligation 1), EVAL-02 (2), SPEC-02..05 (3), and the "not reopened" grounding clause (4).*
