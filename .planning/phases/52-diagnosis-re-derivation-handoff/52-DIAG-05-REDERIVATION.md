# DIAG-05 — Phase 44 Diagnosis Re-Derivation

**Obligation discharged:** GAP-44-02 (`.planning/milestones/v2.1-GAPS.md`), which
required the next milestone to carry "an explicit, mapped requirement to
re-derive the diagnosis from a conformant run, with an acceptance check — not
a best-effort intention."

**Acceptance check (stated before re-deriving, per GAP-44-02's own condition):**
this re-derivation counts only if it is tied to evidence produced by, or a
direct architectural property of, a run whose known conformance divergences
(C-01..C-09) are repaired — not to inference, not to the non-conformant v2.0
pilot, and not to a forecast of a future run's outcome.

**Which branch of Phase 51's Success Criterion 1 applies:** neither cleanly.
Phase 51 never executed — RUN-03/EVAL-01 were deliberately not spent (Phase 50
`50-08-SUMMARY.md`, owner decision 2026-08-17). Phase 51's own criterion
anticipated "conformance divergence explains it" (pass) or "first
evidence-grounded diagnosis of the design" (fail). What actually happened sits
one level upstream of that fork: the conformant run never reached a state a
held-out evaluation could usefully grade, because a separate, deeper mechanism
halted it during training itself. That is closer to the "if it failed" branch
than the "if it passed" branch, and this document treats it that way — but the
finding is stronger than a failed held-out grade, because it is established
independent of any particular training run's outcome (§3).

---

## 1. Conformance status of the run this re-derivation is grounded in

Generation-3, seed 41 (`runs/stage0-rerun-seed41`, `evidence/attempts/stage0-rerun-seed41-attempt-02/`) is the run under evaluation. Its conformance state, as of Phase 50 close:

| Divergence | Repaired by | Verified |
|---|---|---|
| C-01/C-02 — causal collapse / no-zero-weight invariant | Phase 45 GAP-45-04 (invariant A); Phase 49 GATE-01..03 | `49-VERIFICATION.md` |
| C-03 — `R̄` factor `(1/9)` vs locked `(1/3)` | Phase 48 CONF-04 | `48-*-SUMMARY.md` |
| C-04 — `ε_H` stand-in vs `1e-4·S_H` | Phase 47 CONF-02/03 | `47-VERIFICATION.md` |
| C-05 — `λ_E^max` drift from locked `0` | Phase 45 GAP-45-02/45-03; Phase 48 | verified in Phase 48 suite |
| C-06 — missing per-term gradient statistics | Phase 48/49 INST-02/03 | `49-VERIFICATION.md` |
| C-07 — `L_data` reduction ambiguity | Phase 48 CONF-07 (owner ruling 2026-07-31, mean) | GAP-45-01 resolution |
| C-08 — mass↔position permutation / COM-boost gauge | Phase 46 CONF-08 | `46-VERIFICATION.md` |
| C-09 — training-path scale/rotation residency | Phase 47 CONF-09 | `47-VERIFICATION.md` |
| Residual non-dimensionalization frame (audited, not in the original C-01..C-08/C-09 inventory) | N/A — audited and found **not a defect** | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` |

All nine originally-verified divergences are repaired and independently
re-verified at Phase 49 close (176-test suite, `49-VERIFICATION.md`) and
Phase 50 (92-test suite at `50-08-SUMMARY.md`'s cited HEAD). The one additional
question raised during Phase 50 — whether the `u↔t` non-dimensionalization
introduces an undocumented ×100 floor — was independently audited on
2026-08-17 and refuted on four grounds (dimensional closure, spec-text match,
frame consistency, and the committed Phase-38 dual-gate probe). **This run is
conformant** in the sense GAP-44-02 requires: it is the first Stage-0 attempt
built from the locked specs with no known, repaired-or-audited divergence
outstanding.

## 2. What the conformant run actually showed

It did not reach a trainable state. Invariant B (front-advance-within-N,
`N=500`, Phase 49 GATE-03) HALTed at step 501: `front_idx=0` on all 502 logged
steps (`trip.json`, `50-05-SUMMARY.md`). This is the gate working as designed,
not a crash — but it means the run produced no candidate a held-out evaluation
would be meaningful against: `L_phys` never moved past effectively one
collocation point out of sixteen.

## 3. Root cause — re-derived, not merely qualified

`44-ERRATUM.md` (2026-07-24) left the DIAG-04 candidate-cause table
**under-determined**, explicitly because "nothing short of a conformant
Stage-0 run can discriminate the candidate causes, and no such run exists."
That run now exists (§1), plus a second, independent line of evidence the
2026-08-17 audit added: a **read-only characterization of the locked
architecture alone** — `ArchitectureSpec()` defaults, no data, no optimizer,
no training step — which reproduces `R̄≈10¹⁰` and `front_idx=0` identically
across six seed/IC combinations. This second line of evidence discriminates
the DIAG-04 causes independent of any particular training run's outcome,
which is why this re-derivation can resolve rows the original diagnosis and
the erratum could only rank or qualify.

| DIAG-04 row | 44-DIAGNOSIS rank | 44-ERRATUM qualification | **Re-derived verdict (this document)** |
|---|---|---|---|
| H-01/H-03 — population-scale generalization shortfall | Strong | Weakened — recipe divergences confound it | **REFUTED as the driving cause.** Generalization cannot be assessed for a term that received zero effective gradient signal on 15/16 collocation points across the entire run. The uniform 1500/1500 v2.0 failure remains true as an observation but is fully explained by §3's mechanism, which applies identically to every trajectory by construction (it is set at initialization, before any trajectory-specific data is seen). |
| H-04 — loss-term imbalance | Moderate | Qualified both ways — λ vector wasn't the locked one | **CONFIRMED, sharpened.** `L_data` and `L_phys` are imbalanced, but not primarily by a λ-weighting choice: the physics term's own internal causal weight vector collapses to a single active point regardless of λ_phys, so the imbalance is structural (§3), not a tunable-λ artifact. Retained log: `grad_norm_raw_phys`/`grad_norm_raw_data` median 6.3×10¹² (12.8 decades) — six decades past the float32 round-off floor once `λ_phys=1`. |
| H-05 — optimization/warmup pathology | Moderate | Sharpened — causal collapse, one of sixteen points | **CONFIRMED as the proximate cause, re-scoped from "warmup" to "structural."** It is not a warmup transient: the architecture-only characterization (no training) reproduces the same `R̄≈10¹⁰`, `front_idx=0` state at step 0, and the retained 502-step log shows `log₁₀R̄₁` moving −0.26 decades total — statistically flat. The causal-weighting mechanism (`exp(−η_c·R̄)`, `η_c=1`) is saturated at initialization and stays saturated; there is no "warmup" to complete. |
| H-06 — normalization/data-scale mismatch | Moderate | Gains the most — concrete loci found | **CONFIRMED as the root cause.** Fully localized: an `ω₀=30` SIREN's second derivative at initialization is `O(10⁵)` in the network's own units, against a causal-weight calibration (`η_c=1` on unnormalized `R̄`) that presumes a converged-network residual of `O(1)` (independently confirmed: Phase-38 Gate B shows 0.65% relative residual error on a *trained* network against ground truth). The two locked spec choices — SIREN init scale (`pinn_architecture.md` §2.2) and causal-weight calibration (§3.2) — are each internally consistent but were never calibrated against each other. |
| H-07 — insufficient budget | Weak | Confounded further — comparator not comparable | **REFUTED.** The failure is proven budget-independent: it is a property of the architecture at initialization (§3, zero training steps), and the retained 402-step run at full `λ_phys=1` shows no directional descent. No budget within the current calibration would cross 8.5–10.5 decades on this evidence. |
| H-02/H-08 — pre-registered rubric, tie handling | — | Unaffected | **Unaffected; not re-examined here** (process claims, not a training-dynamics cause). |

## 4. Statement required by DIAG-05

The v2.0 physics-gate failure is **not** explained by the conformance
divergences C-01..C-09 (option 1 of Phase 51's Success Criterion 1) — those
were real, independently verified, and fully repaired, and repairing them did
not produce a trainable run. It is explained by a prior, deeper design-level
mismatch between the locked SIREN initialization (`pinn_architecture.md`
§2.2) and the locked causal-weight calibration (`pinn_architecture.md` §3.2),
established as a property of the locked architecture at initialization,
independent of seed, IC, and training budget (option 2 — "the first
evidence-grounded diagnosis of the design"). This is the diagnosis GAP-44-02
required v2.2 to produce, and it resolves DIAG-04's under-determined rows
rather than leaving them qualified.

**What this does not establish:** no claim is made about what any future
run — under a different `η_c`, normalization, or SIREN scale — would do.
`later_generation_likelihood_claim: prohibited` stands. The remedy is a
framework-spec decision (SCOPE-30 forbids making it in v2.2) and is routed to
v2.3 (see `52-VER-20-ROUTING-HANDOFF.md`, item 5).

## Sources

- `.planning/milestones/v2.1-phases/44-physics-gate-forensics/44-DIAGNOSIS.md`, `44-ERRATUM.md`
- `.planning/milestones/v2.1-GAPS.md` GAP-44-02
- `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md`
- `.planning/phases/50-valid-stage-0-re-run/50-06-SUMMARY.md`, `50-08-SUMMARY.md`
- `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md` (C-01..C-08 inventory)
- `49-VERIFICATION.md`, `47-VERIFICATION.md`, `46-VERIFICATION.md`
