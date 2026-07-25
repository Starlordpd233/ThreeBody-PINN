---
status: active
purpose: design
created: 2026-07-24
milestone: untracked
phase: cross-cutting
retirement_trigger: Retire when the three enforcement layers below are implemented and enforced (preflight gate blocking, runtime invariants live, spec-conformance tests in CI), and the known-divergence register is a maintained artifact that run preflight and any diagnosis phase are obligated to consult.
---

# Charter: Training Verification & Enforcement Regime

**Status of this document.** A problem statement and proposed design for a
separate, concurrent workstream. It proposes machinery; it implements nothing,
edits no framework spec, and selects no remedy for the v2.0 physics-gate
failure. Owner-owned decisions are listed as open questions and are not
pre-answered here.

**Commissioned by the owner 2026-07-24**, after the trainex-r2 research result
revealed that the Stage-0 pilot did not implement the locked spec in five
verified respects, and that three phases of downstream work were premised on the
assumption that it did.

## 1. What happened, in one paragraph

The v2.0 Stage-0 pilot failed its held-out physics-conservation gate by roughly
seven orders of magnitude, uniformly across all 1,500 held-out trajectories. That
failure was treated as a scientific result about the model, and two phases of
work followed from it: forensics on the retained artifacts (Phase 44, producing a
ranked hypothesis table whose top-ranked cause was a population-scale
generalization shortfall) and an external-research package asking how to re-tune
the training recipe (Phase 45). An external research agent, reading the codebase
under an owner override of the package's own "attached files only" design, found
that the executed code diverges from the locked specs. Five of its claims plus a
sixth were independently confirmed — see
`docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md`
for the file:line evidence. The cheap question — *does the code compute what the
spec says?* — was never asked, and answering it took about fifteen minutes of
read-only inspection once someone pointed at where to look.

## 2. The confirmed divergences, classified by what would have caught them

This classification is the design input. Each row names the layer that would
have caught it, which is why the proposed regime has three layers rather than
one.

| Divergence | Nature | Would have been caught by |
|---|---|---|
| Causal front never advanced off the first collocation point — 1500/1500 logged steps, 5/5 runs; weights underflowed to exactly 0.0 | Runtime pathology, fully visible in the run's own logs | **Runtime invariant** (layer 2) |
| Causal exponent unclipped, against a spec MUST | Code omits a normative requirement | **Conformance test** (layer 3) — but see §6, the bound is spec-deferred |
| R̄ computed as (1/9)Σ where spec locks (1/3)Σ | Formula transcription error, factor of exactly 3 | **Conformance test** (layer 3) |
| λ_E = 1.0 at Stage 0 where the locked schedule sets 0 | Configuration contradicts a locked table | **Preflight gate** (layer 1) |
| ε_H is a per-anchor stand-in because the `S_H` pipeline was never built | Spec prerequisite unsatisfied; code could not comply | **Readiness gate** (layer 1) |
| Per-term gradient statistics never logged, though the spec names them the precondition for any reweighting decision | Required instrumentation absent | **Readiness gate** (layer 1) |

Two observations that shape everything below:

**The single highest-value item is also the cheapest.** The causal front never
advancing was *in the logs the run itself wrote*. `front_idx` was recorded on
every step. The data existed; nobody asserted on it. An assertion of the form
"if the causal front has not advanced in N steps, halt and report" is on the
order of fifty lines and would have caught this in the first minutes of run #1,
before any of Phases 44 or 45 existed.

**None of these divergences was hidden.** Every one carries an inline provisional
marker with a governance tag — `WR-02`, `CTX-38`, and one reading
"⚖ PROVISIONAL — awaiting owner ratification **before run #1**." Run #1 happened.
The markers lived in code comments and were never consolidated anywhere a later
phase would consult. `pinn/STATUS.md`, the handoff document, enumerates deferred
*platform* features (Tier-3 remediation, auto-revert, PLAT-04) — not the
loss-math approximations. So Phase 44 built a diagnosis from run artifacts plus
the spec, with no inventory of the ways the build knowingly approximated that
spec, and no obligation to look for one.

## 3. Why the existing checks passed

Each phase ran its checks and each check passed. Understanding *why* is the
point — these were not skipped steps.

- **Phase 38 verification, Phase 43 calibration and verdict** validated that the
  machinery ran, produced finite losses, checkpointed, and recovered. They
  validated *operation*, not *fidelity to the locked equations*.
- **Phase 43's calibration ratification** covered guards, retries, and the
  checkpoint ceiling. It did not cover the λ schedule, the loss formulas, or the
  instrumentation field set — the latter of which was explicitly marked as
  awaiting ratification before run #1.
- **The per-step logs recorded the pathology faithfully.** `front_idx`,
  `w_min/w_mean/w_max`, and the five per-term losses were all logged. The
  observability was adequate; the *alerting* was absent. Nothing consumed those
  fields and asserted on them.

## 4. Why GSD verification structurally cannot catch this class

The owner's instinct here is correct, and the reason is structural rather than a
matter of the skill being run poorly.

`gsd-verifier` performs **goal-backward analysis against the phase's own plan** —
"does the codebase deliver what the phase promised." If a plan says "implement
the causal physics loss per spec" and the code contains a causal physics loss
that runs, goal-backward analysis returns PASS. It does not independently
re-derive `R̄ = (1/3)Σ‖f_i‖²` from the spec text and diff it against
`(residual ** 2).mean(dim=(-2,-1))`. It has no reason to.

Three compounding properties:

1. **Plan-conformance, not spec-conformance.** The plan is the reference, and the
   plan is one abstraction level above the equations. A plan can be fully
   satisfied by code that computes the wrong formula.
2. **No independent ground truth in the loop.** The same agent lineage authors
   the plan, writes the code, and verifies it, reading the same phase artifacts.
   A shared misreading of the spec is invisible — there is no oracle.
3. **Prose MUSTs are not enumerable by it.** "The exponent must be clipped" is
   one sentence in a 126KB spec. Nothing maps the spec's normative statements to
   named tests, so an unimplemented MUST leaves no trace of its absence.

**Conclusion for the workstream:** GSD verification should be retained for what
it is good at — did the phase deliver its promised scope — and must not be
credited as spec-conformance assurance. Conformance needs a separate, mechanical,
spec-anchored mechanism whose reference is the spec text, not the plan. This is
an addition to the GSD workflow, not a replacement for it.

## 5. Proposed design — three layers plus a register

### Layer 1 — Preflight gate (blocks a run from starting)

Runs before any training step, and re-asserts at every curriculum stage
boundary, since the locked schedules change per stage.

- **Config vs locked tables.** Every scheduled quantity in the run config is
  checked against the locked spec table for the stage being entered
  (λ_phys/λ_E/λ_L per PHYS-05, LR schedule, stage parameters). A mismatch blocks
  the run and names the spec line. This alone stops the λ_E case.
- **Placeholder census.** Every spec-required quantity the loss consumes must
  resolve to a real, pipeline-computed value. Anything resolving to a provisional
  stand-in, a hardcoded default, or an unbuilt upstream is enumerated and must be
  explicitly waived by the owner for that run. This is the check that catches the
  `S_H` case, which no code-vs-spec diff can catch — the code was as compliant as
  it could be given a prerequisite that didn't exist.
- **Required-instrumentation check.** Where the spec conditions a decision on
  measured evidence ("log weighted losses, scheduled weights, and gradient
  statistics before any control law"), the preflight asserts those fields are
  present in the logging registry. Catches the gradient-statistics case.

### Layer 2 — Runtime invariants (fail loud, fail early)

Cheap assertions over quantities the run already computes and logs. Highest
value per unit effort in the entire charter.

- Causal front advances: `front_idx` must move within N steps, else halt/alarm.
- Causal weights are not degenerate: not all-but-one underflowed to zero.
- No loss term dominates by more than X× for more than M consecutive steps.
- All terms finite; scheduled weights match the stage's expected values at every
  logged step, not merely at run start.

Thresholds (N, X, M) are owner-owned calibration decisions and are deliberately
left blank here — see §6.

### Layer 3 — Spec-conformance tests (CI, independent of any plan)

**Target the assembly layer, not the components.** The conformance audit
(`docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md`)
established that the pure component functions are spec-faithful and already
well-tested with hand-computed expected values — and that *every* confirmed
divergence lives in the seams where those components are assembled, fed, and
configured, which has no formula-level tests at all. Adding more component tests
would find nothing.

Worse, the existing suite **defends two of the divergences**:

- `tests/phase38/test_loss_catalog.py:193` asserts the energy term consumes a
  supplied `ε_H = 1e-4·S_H` (correct, per spec).
- `tests/phase40/test_optimizer_phase.py:745` asserts the *caller* must produce
  `ε_H == |h0|*1e-4 + 1e-12` (the divergent value).

Two passing tests, contradictory contracts for one quantity, nothing testing the
interface between them. Similarly, `test_scheduled_weights.py:81` asserts the
`λ_E^max ≤ 1` cap but no test asserts the locked Stage-0 value of 0 — the suite
encodes the weaker constraint and leaves the stronger unguarded. **Correcting the
code requires correcting these tests in the same change**, or the fix fails CI.

Design implications:

- Conformance tests assert **end-to-end quantities at the assembly boundary**:
  given known inputs, does the R̄ the loss actually receives equal the spec's
  (1/3)Σ‖f_i‖²; does the ε_H the energy term actually receives equal `1e-4·S_H`.
- **No test may hardcode a value that contradicts a locked spec value.** Worth a
  mechanical check of its own: any test asserting a numeric constant that also
  appears in a locked spec table must reference `pinn/constants.py`-style cited
  constants rather than a literal.
- `pinn/constants.py` is the pattern to extend — every value spec-cited with a
  section reference, single home, no scattered literals. It is why the constants
  are all correct while the formulas that consume them are not.
- **A normative-statement index.** Every MUST / locked value / prohibited
  anti-pattern in `ctl_instruction.md` and `pinn_architecture.md` that touches
  the training path is enumerated once, and each entry maps to either a named
  test or an explicit, dated waiver. An unmapped MUST is a CI failure. This makes
  "we forgot the clip" structurally impossible to miss rather than dependent on
  someone remembering.

### The known-divergence register

The artifact whose absence caused the Phase 44 misframing. One file, first-class,
listing every place the implementation knowingly departs from the locked spec:
what, why, the governance tag, whether the owner ratified it, and what it would
take to close.

Two obligations give it teeth:
- **Run preflight consults it** and surfaces every open divergence in the run
  record, so a run's output carries its own caveats.
- **Any diagnosis or forensics phase must read it before ranking hypotheses.**
  Phase 44 ranked "population-scale generalization shortfall" as its Strong
  candidate while five spec divergences sat unlisted in code comments. That
  ordering was reasonable given what the phase could see, and it was wrong. The
  register is what would have made it visible.

## 6. Open questions — owner-owned, deliberately unanswered

- **Runtime invariant thresholds** (front-advance window N, dominance ratio X,
  persistence M). Calibration decisions with false-positive/false-negative
  trade-offs; not inventable from first principles.
- **The causal-exponent clip bound.** The spec mandates clipping and defers the
  bound to future work. Fixing the code therefore requires either an owner
  decision on a value or a conservative choice that must be surfaced as a gap —
  it is *not* a pure code fix, and should not be treated as one.
- **Waiver policy.** Who may waive a preflight placeholder, and does a waived run
  remain eligible to spend rationed held-out evaluation budget? See below.
- **Retrofit scope.** Does the normative-statement index cover the whole training
  path at once, or only the Stage-0 slice first?

## 7. A structural insight worth carrying separately

**The rationed-evaluation policy needs a conformance precondition.** Held-out
evaluations were deliberately budgeted so that no one could tune against the
held-out set — sound discipline. But the single authorized look was spent on a
run that is now known not to have implemented the specified recipe. The budget
was protected against one failure mode (overfitting by repeated looks) and
completely exposed to another (spending a look on an invalid experiment).

Proposed principle: **a rationed evaluation may not be spent on a run that has
not passed preflight conformance with no unwaived divergences.** This costs
nothing when things are correct and preserves the scarcest resource in the
project when they are not.

## 8. Boundaries

This charter does not: edit any framework spec; select or recommend any remedy
for the v2.0 gate failure; authorize any training run or held-out evaluation;
implement any code. Implementing layers 1–3 touches `pinn/`, which is build work
for a milestone to schedule — not for this document to perform.

## 9. Suggested first moves for the concurrent session

Ordered by value per unit effort, on the evidence above:

1. **Runtime invariants (layer 2).** Smallest change, would have caught the
   worst defect within minutes of run #1. Needs the owner's thresholds first.
2. **The known-divergence register.** Pure documentation, no code, unblocks
   correct framing for every future diagnosis phase. Its initial contents are
   ready: transcribe findings C-01…C-08 from the completed conformance audit
   (§10).
3. **Preflight config-vs-locked-table check (layer 1, first bullet).**
   Mechanical, high certainty, catches the λ_E class outright.
4. **Placeholder census (layer 1, second bullet).** Catches the class no
   code-vs-spec diff can — spec prerequisites that were never built.
5. **Normative-statement index (layer 3).** Largest effort, deepest payoff;
   sequence it after the register exists so the two can cross-reference.

## 10. Relationship to concurrent work in the trainex worktree

The bounded conformance audit is **complete** (2026-07-24, `trainex` worktree,
branch `milestone/v2.1`):
`docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md`.

Read it before re-deriving anything. Its findings C-01…C-08 are the register's
initial contents, and its central conclusion reshapes layer 3 above: the
component math is faithful and well-tested; the divergences are all in the
assembly, wiring, and configuration seams; and the test suite currently defends
two of them. It also records a "verified clean" inventory so a future audit need
not re-check the component math, and lists two items that remain owner-owned
(authorization of λ_E = 1.0; the PHYS-05 lock boundary) plus one that needs data
absent from the worktree (the executed target frame).
