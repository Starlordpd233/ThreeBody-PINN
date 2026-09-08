# Phase 57: Corrected Re-Run & the Preserved Evaluation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-07
**Phase:** 57-Corrected Re-Run & the Preserved Evaluation
**Mode:** `--all`, serviced autonomously per owner instruction 2026-09-07 (best-reasoned
option chosen for every mechanical/operational/sequencing gray area; STOP protocol
NOT waived — one cross-phase-scope call surfaced as GAP-57-01 and was subsequently
resolved by the owner on 2026-09-07).
**Areas discussed:** Amended-recipe implementation, Owner checkpoints ③/④, GATE-04
completeness precondition, Three-seed band & budget, Calibration smoke & no-commit-mid-band,
EVAL-02 evaluator assembly & pairing proof, EVAL-02 three preconditions, Conformance-only
iteration, Execution environment, Evidence contract.

---

## Post-discussion owner rulings — 2026-09-08

The owner subsequently resolved every decision that the discussion left in a
packet-only or inherited-open state. These later rulings supersede the earlier
"packet-only" rows below without rewriting the historical discussion:

- **GAP-56-01 / GATE-04:** require a `2:1` spread among non-anchor weights;
  apply the fixed uniform residual-bin scale
  `alpha = log(2) / (2 * P_15)`, which gives expected
  `w'_15 = 1/sqrt(2)`; require `front_idx = 15` and every perturbed weight
  `>= 0.70`.
- **Checkpoint ③ / GAP-54-06:** explicitly re-ratify `N = 500`; use one frozen
  training-only invariant-B monitor; freeze L-BFGS samples and detached causal
  weights for its entire segment.
- **Checkpoint ④:** pre-register seed 42, with fallback 41 then 43 only for
  structural ineligibility.

The authoritative exact record is `57-RULING.md`. It adds no `w_15 <= 0.45`,
`64*eps`, fixed-0.1 probe, monitor cadence, front margin, or persistence-count
criterion.

---

## Amended-recipe implementation (SPEC-01/SPEC-06 → `pinn/` code)

| Option | Description | Selected |
|--------|-------------|----------|
| A — Phase 57 bounded `pinn/` conformance patch to the causal-loss + collocation path, with separate verification before RUN-04 | Read RUN-04 as code-to-spec conformance (v2.2 Phases 46–49 precedent; SCOPE-37 "conformance" language); inventory follows the behavior through loss/sampler/controller/config wiring, not two filenames | ✓ owner 2026-09-07 |
| B — Insert a dedicated implementation phase before RUN-04 | New requirement/plan/verification; RUN/EVAL shift phase number | |
| C — Commission a new wholesale trainer rebuild in v2.3 | Corrected after surfacing: FUT-01 shipped in v2.0 (`PROJECT.md:344`), so another rebuild would require new justification | |
| D — Milestone blocks pending a new owner scope decision | | |
| **Surface as gap** | Proposal scoped implementation into Phase D; roadmap mapping dropped it; Phase 56 executed spec-only and left the amended-recipe implementation unassigned. No source then authorized the code change or named its owner. | ✓ initial discuss step |

**Choice:** Surfaced as **GAP-57-01** (HIGH, cross-phase reframing + semantic + scope),
then resolved by owner instruction on 2026-09-07 with **Option A**. Phase 57 owns an
explicit bounded implementation wave and a separate production-path verification wave
before RUN-04. The scope includes the causal loss, all-selected-slot collocation allocation,
sampler/controller/config wiring, exact §3.2 normalization and diagnostics, and focused
tests. It excludes retuning, redesign, data-policy changes, Stage-1+, PLAT-01..07, and a
wholesale rebuild; resource failure at 4096 rows fails closed. Remaining owner gates are
unchanged.
**Notes:** The proposal-vs-executed discrepancy (`2026-08-17-v2.3-roadmap-proposal.md:267`
"Phase D | SPEC-01 + SPEC-06 amendment **and implementation**" vs `ROADMAP.md:59` Phase 56
= "SPEC-01, SPEC-06, GATE-04") is itself part of what the owner needs to see. The change
touches loss math, the optimizer path, the data path, and the duration-gate calibration —
exactly the class v2.2 Phase 50's CONTEXT and `ROADMAP.md` "Gap discipline" require be
surfaced. The resolution expressly supersedes the Phase-56 implementation deferral for
this bounded path. `.planning/PROJECT.md:344` corrects the original option-C premise:
FUT-01 shipped in v2.0.

---

## Owner checkpoint ③ — invariant-B window + fixed monitor + GAP-54-06

| Option | Description | Selected |
|--------|-------------|----------|
| Agent picks `N` / estimator / L-BFGS semantics | | |
| Agent assembles a strictly non-recommending packet; owner rules | Bundles the window `N`, the fixed pre-registered monitoring context, and the inherited GAP-54-06 into one blocking gate before any run | ✓ |

**Choice:** Packet-only (D-03). The three sub-decisions are owner-only (roadmap checkpoint ③;
`54-RULING.md` "Front-monitoring boundary" + "Optimizer-phase boundary"; GAP-54-06 DEFERRED
to checkpoint ③). The agent frames, names the gaps, picks nothing.
**Notes:** `N = 500` was `0.5 · N_Adam,0` against the old saturated dynamics — not carried
over by default. GAP-56-01 option D would add the GATE-04 condition-(ii) bound to this same
agenda.

---

## Owner checkpoint ④ — EVAL-02 spending seed

| Option | Description | Selected |
|--------|-------------|----------|
| Agent pre-registers a seed | | |
| Agent builds the pre-registration structure (grounded by v2.2 Phase 50 D-07..D-12); owner picks the seed | Committed-with-timestamp record before the first graded run: seed, `best.pt` checkpoint rule, ineligibility-only fallback, no-eligible-seed → owner | ✓ |

**Choice:** Structure dispositioned (D-04), seed pick is checkpoint ④. The packet may note
for continuity that v2.0 and v2.2 both used seed 42 as the candidate — as context, not a
recommendation.
**Notes:** The split is seed-dependent (`_partition_by_signature`), so pre-registration
before the band is visible is structurally mandatory.

---

## GATE-04 completeness precondition

| Option | Description | Selected |
|--------|-------------|----------|
| Accept the Phase-56 `PASS (INCOMPLETE, unratified: ii)` verdict | | |
| Require a complete GATE-04 PASS — GAP-56-01 resolved and GATE-04 re-run — before RUN-04 | GATE-04 condition (ii) is the SCOPE-35 single-look protection; an INCOMPLETE verdict is not a pass for that purpose | ✓ |

**Choice:** Complete PASS required (D-05). GAP-56-01 (Phase-56-local, OPEN) carried into
`57-GAPS.md` as an inherited blocker.
**Notes:** `56-OPEN-ITEMS.md` §2's two structural findings (`front_idx = 0` at init is
healthy; late-bin residual reductions cannot move the front) must be reflected in the
owner's condition-(ii) ruling.

---

## Three-seed band & budget (RUN-05)

| Option | Description | Selected |
|--------|-------------|----------|
| Copy the v2.0 config (300-step `run.smoke: true` budget) | | |
| Seeds 41/42/43, shipped `max_epochs = 1000` / `n_adam = 1000`, protocol-layer comparability, configs derived from `stage0-rerun-seed4X.yaml` | v2.2 Phase 50 D-01/D-02 grounding carried forward; a shorter budget makes invariant-B `N` unreachable | ✓ |

**Choice:** D-06, D-07, D-08. Run names distinct from the v2.2 `stage0-rerun-seed4X`
artifacts.
**Notes:** If checkpoint ③ re-ratifies `N` to imply a different `N_Adam,0`, the budget
follows the ③ ruling, not a fresh agent choice.

---

## Calibration smoke & no-commit-mid-band

| Option | Description | Selected |
|--------|-------------|----------|
| Assume the persisted v2.0-era calibration | | |
| Open with a fresh calibration smoke on the final code state; sequence code-commit → smoke → 3 graded runs → EVAL-02 with no intervening commit | `_check_duration_gate` pins `git_head`; the GAP-57-01 code commit + the 256× collocation change both invalidate the old calibration | ✓ |

**Choice:** D-09, D-10, D-11. Smoke at seed 42; `S_H` / `n_train` exact-equality cross-check;
`--stage-0-only` reused and re-verified.

---

## EVAL-02 evaluator assembly & pairing proof (GAP-46-01)

| Option | Description | Selected |
|--------|-------------|----------|
| Trust `pinn/evaluate.py` as-is | | |
| Characterize `pinn/evaluate.py` (Phase-43 vintage, pre-CONF-09) against the canonical `(r′, u = t/T)` contract; add a dataset-free assembly regression + a pre-access assertion before the single invocation | GAP-46-01 delegated ruling 2026-07-26: EVAL-02 is for the corrected conformant model, canonical frame only | ✓ |

**Choice:** D-12, D-13. If `evaluate.py`'s frame is not canonical, its bounded repair is
governed by GAP-46-01 / D-12, independently of the resolved causal-path authorization.

---

## EVAL-02 three preconditions (adapted)

| Option | Description | Selected |
|--------|-------------|----------|
| Invent new preconditions | | |
| The v2.2 EVAL-01 structure (i)–(iii), adapted: (i) includes a complete GATE-04 PASS; (ii) is CONF-09's canonical `(r′, u = t/T)` with the GAP-46-01 proof as its evidence; (iii) unchanged | Roadmap SC5 "the same three-precondition structure … adapted for the new recipe" | ✓ |

**Choice:** D-14, D-15. The pairing proof is RUN-04-mapped, not a fourth precondition
(GAP-46-01: "without altering EVAL-01's three eligibility preconditions").

---

## Conformance-only iteration (SCOPE-37)

| Option | Description | Selected |
|--------|-------------|----------|
| Allow recipe adjustment if a run looks bad | | |
| A change is conformance-only iff its justification does NOT cite what a run produced; an honest invariant-B HALT is a deliverable | v2.2 Phase 50 iteration policy, adapted from SCOPE-29 to SCOPE-37 | ✓ |

**Choice:** D-16.

---

## Execution environment

| Option | Description | Selected |
|--------|-------------|----------|
| Worktree-isolated `gsd-executor` subagents | | |
| Inline on the data-bearing checkout; conda `pinn-train` off-PATH; no pytest in the env; resolve the admitted-corpus data root as a run precondition | Project memory: gitignored data + STOP-protocol phases favour inline | ✓ |

**Choice:** D-17, D-18, D-19.

---

## Evidence contract

| Option | Description | Selected |
|--------|-------------|----------|
| Minimal logging | | |
| Carry the v2.2 Phase 50 evidence contract forward (run ledger, band record, pre-registration record, config-delta record, checkpoint packets, GATE-04 complete-PASS evidence, GAP-46-01 pairing artifacts, sha256 manifests) | Format is Claude's discretion, following the established layout | ✓ |

**Choice:** D-20. Two "checks that cannot fail" (no-eval-dir check, config-diff check) must
be real.

---

## Claude's Discretion

Wave decomposition and how the no-commit-mid-band constraint is expressed; smoke and band
extraction as one plan or several; attended vs unattended launch; formats/layouts of the
run ledger, band record, pre-registration record, config-delta record, evidence manifests;
band distribution quantiles; the exact v2.3-distinct run names; the dataset-free regression
test's exact shape (no held-out access, `unittest`, committed); evidence directory placement
under `.planning/phases/57-*/evidence/`.

## Deferred Ideas

- Any new wholesale trainer rebuild (FUT-01 shipped in v2.0; GAP-57-01 authorizes
  only the bounded amended-recipe path).
- Stage-1+ / PLAT-01..07 (SCOPE-36).
- The DIAG-06 verdict + VER-21 close (Phase 58, checkpoint ⑤).
- Any second held-out evaluation (SCOPE-35).
- Re-tuning `η_c` / `R_ref` / `ω₀` / `N_t` against an observed result (SCOPE-37).
- Reviewed-not-folded todos: `d-06-static-epsilon-sensitivity-check`,
  `trainex-r1-research-handoff` (same disposition as Phases 55/56).
