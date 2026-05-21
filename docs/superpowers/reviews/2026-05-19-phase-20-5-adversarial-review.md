# Adversarial Review Report: Phase 20.5 Design Documents

**Date:** 2026-05-19
**Documents reviewed:**
- `docs/superpowers/specs/2026-05-19-sobol-allocation-ambiguity-design.md`
- `docs/superpowers/plans/2026-05-19-phase-20-5-sampling-coordinate-allocation.md`
**Reviewers dispatched:** 4 parallel adversarial reviewers (spec edits, convention/probe, governance, scope/sub-conflict)

---

## Executive Summary

| Area | Verdict | Blockers |
|------|---------|----------|
| Spec Edits 1–5 (Task 4 / Design §4) | Mostly sound | 1 BLOCK (design doc miscount), 1 FLAG (`rotate` omission) |
| Option A Convention & Probe (Design §3 / Task 5) | Correct physics, weak probe | 1 BLOCK (probe insufficient), 1 FLAG (`rotate` omission) |
| Governance Hooks (Tasks 2–3 / Design §5) | Plan correct, design doc wrong on gap count | 2 BLOCKs (design doc gap count), 1 FLAG (SCOPE-05 rationale breadth) |
| Sub-conflict #1 & Scope (Task 7 / Design §8) | Classification debateable | 1 BLOCK (sub-conflict #2 math claim), 3 FLAGs |

**Bottom line:** The **implementation plan** is internally consistent and ready to execute with minor amendments. The **design doc** has a clear error in §5.4 (gap count: 12 vs. correct 14). The most material technical gap is that the verification probe only tests dimension count, not allocation order — the very ambiguity Phase 20.5 exists to resolve.

---

## BLOCK Findings (Must Fix Before Implementation)

### BLOCK-1: Design doc gap count is wrong — says 12, actual is 14

**Severity:** BLOCK
**Location:** Design doc §5.4 (line 321)

The design doc says: "Bump frontmatter: `total_gaps: 12`, `resolved_gaps: 12`."

The actual `v1.4-GAPS.md` frontmatter has `total_gaps: 11`, `resolved_gaps: 11`. Adding 3 new gaps (GAP-20-5-01/02/03) yields **14**, not 12. The plan Task 3 correctly says 14; the design doc is off by 2.

**Impact:** If an agent implements from the design doc literally, it will search for `total_gaps: 12` in `v1.4-GAPS.md`, fail to find it, and either abort or apply the edit to the wrong location.

**Fix:** Correct design doc §5.4 to `total_gaps: 14`, `resolved_gaps: 14`.

---

### BLOCK-2: Verification probe tests dimension only, not allocation order

**Severity:** BLOCK
**Location:** Plan Task 5 (`verify_sobol_allocation.py`)

The probe instantiates `EnhancedThreeBodySampler` and asserts `s.sobol_dim == expected_d`. It never calls `_process_sobol_batch` or verifies that column 3 → scale and columns 4–6 → velocity.

**Impact:** If someone refactored `_process_sobol_batch` to swap scale and velocity columns, the probe would still pass. The entire purpose of Phase 20.5 is to resolve the `u_4` double-booking ambiguity — but the probe does not verify the allocation, only the dimension count.

**The plan acknowledges this:** The probe's own stdout says "Allocation ORDER ... verified by direct code reading." Human code reading is not a disposable probe.

**Fix:** Add a synthetic `sobol_batch` test to the probe:
1. Construct a batch where column `j` has a known value `j+1`.
2. Call `_process_sobol_batch`.
3. Assert that `scale` derives from column 3 and `v2_batch` derives from columns 4–6.

---

### BLOCK-3: Design doc claim "'6 additional' analysis remains valid" is false under the locked convention

**Severity:** BLOCK
**Location:** Design doc §8, lines 445–450

The design doc says §2.1's hypothetical "6 additional Sobol dimensions" analysis "remains valid." Under the locked convention `d = 3 + δ_s + 3δ_v` with `δ_s = 1`, sampling velocities for two free particles would require `d = 3 + 1 + 6 = 10` dimensions, not 9. The "6 additional" framing implies a baseline of 3 position + 6 velocity = 9, omitting the scale dimension.

**Impact:** A reader comparing §2.1 to the locked convention will find an arithmetic mismatch. The design doc's "remains valid" claim is factually incorrect for the standard configuration.

**Fix:** In §8, qualify the claim: "§2.1's hypothetical analysis remains valid *for the no-scale case* (`δ_s = 0`). Under the standard configuration (`δ_s = 1`), the total dimension would be 10, not 9."

---

## FLAG Findings (Should Address)

### FLAG-1: `rotate=True` branch omitted from spec's dimension formula

**Severity:** FLAG
**Location:** Edit 2, Edit 3; `ic_generation_utils.py` lines 98–99

The code has a third conditional: `if self.rotate: self.sobol_dim += 3`. The spec's formula `d = 3 + δ_s + 3δ_v` omits this entirely. The spec presents the formula as complete, but it is not.

**Fix:** Either (a) add `δ_r` to the formula with a note that `δ_r = 0` in the standard config, or (b) explicitly scope the formula to `rotate=False`.

---

### FLAG-2: SCOPE-05 rationale text is broader than binding text

**Severity:** FLAG
**Location:** Plan Task 2 Step 3 / Design doc §5.3

The binding text names `simulation_data/Scripts/ic_generation/` as the permitted grounding source. The rationale says "`simulation_data/Scripts/` is a permitted grounding source" — broader. A future agent could overread the rationale to justify grounding on `simulation_data/Scripts/metrics_calculation/` or other subdirectories.

**Fix:** Tighten the rationale to match the binding text: "`simulation_data/Scripts/ic_generation/` is a permitted grounding source..."

---

### FLAG-3: Sub-conflict #1 is a contradiction in outcome distributions, not merely "under-specified"

**Severity:** FLAG
**Location:** Design doc §8; Plan Task 7

The design doc classifies the velocity-momentum discrepancy as "under-specified, not contradictory" because both approaches yield total momentum zero for equal masses. But the spec's "adjusting the velocity of the fixed particle" (singular) implies one particle is adjusted, while the code adjusts two particles symmetrically (`v1 = v3 = -v2/2`). The resulting `v1` and `v3` distributions are statistically different. A literal FUT-01 implementer would produce a different dataset.

**Fix:** Change the classification from "under-specified" to "contradictory in outcome distribution" in the finding file. Add explicit guidance that FUT-01 should follow the *code's* symmetric split, not the spec's singular wording, until the spec is corrected.

---

### FLAG-4: Success criterion claims "mutually consistent" while preserving an inconsistent sentence

**Severity:** FLAG
**Location:** Design doc §5.1 (Success Criterion 2)

Success Criterion 2 says the reader can verify "mutual consistency" across §1.1 dimension, "Sampling-Time Size Variability," and "Velocity Sampling." But the momentum-conservation sentence in "Velocity Sampling" is preserved verbatim and is inconsistent with the code. A reader trusting the "mutually consistent" claim may not realize the momentum-conservation procedure is still a live discrepancy.

**Fix:** Narrow Success Criterion 2 to: "Reader can verify the §1.1 dimension claim, 'Sampling-Time Size Variability', and the Sobol coordinate allocation within 'Velocity Sampling' are mutually consistent." Add a note that momentum-conservation procedure remains a separate, flagged discrepancy.

---

### FLAG-5: "Fixed particle" ambiguity in preserved momentum-conservation sentence

**Severity:** FLAG
**Location:** `sampling_method.md` line 119 (preserved verbatim in Edit 5)

The spec refers to "the fixed particle" but does not identify which particle. Particle 1 is position-fixed; particle 3 is COM-derived. The code adjusts both symmetrically. The ambiguity matters because different readings imply different physical procedures.

**Fix:** No fix in Phase 20.5 (it is out of scope), but the finding file should explicitly note the ambiguity in particle identification as a separate sub-issue.

---

### FLAG-6: `s_min` symbol note reintroduces the symbol it claims to avoid

**Severity:** FLAG
**Location:** Edit 4 TO block, "Symbol note"

The note explains the rename from `s_min/s_max` to `s_lo/s_hi` to avoid collision with the minimum pairwise separation invariant `s_min` — but then uses `$s_{\min}$` in the note itself to refer to that invariant. A reader searching for `s_min` will find it in the symbol note.

**Fix:** Use a different reference in the symbol note, e.g., "the minimum pairwise separation invariant (denoted `s_min` in the resolution doc)."

---

### FLAG-7: Dataset alignment claim lacks independent verification

**Severity:** FLAG
**Location:** Design doc §3.2, §5.6; Plan Task 6

The documents claim the existing dataset was generated by the current `ic_generation_utils.py`, but no commit hash, generation log, or dataset manifest is cited. The dataset could have been generated by an earlier version of the code with a different allocation.

**Fix:** Acknowledge this as an unverifiable assumption in `20-5-DATA-ALIGNMENT.md`. If a generation log or manifest exists, cite it. If not, note the assumption explicitly.

---

### FLAG-8: GAP-20-5-03 classification stretches CLAUDE.md text

**Severity:** FLAG
**Location:** Plan Task 3 / `20-5-GAPS.md`

CLAUDE.md lists "acceptance-check pass criteria, divergence-file structure, new AC names beyond Phase 16 reservations, gap-register format itself" as MUST-surface process-artifact schemas. GAP-20-5-03 (hand-off file rename from `CODE-DIVERGENCE` to `DATA-ALIGNMENT`) is adjacent to "divergence-file structure" but is not the same thing — it is a naming choice for a file that documents alignment, not divergence.

**Fix:** Reclassify GAP-20-5-03 as "operational coordination" rather than "process-artifact schema," or add a brief justification explaining why a hand-off file rename falls under the "divergence-file structure" umbrella.

---

### FLAG-9: Forward reference to "v1.4 Phase 20.5" in spec is temporally awkward

**Severity:** FLAG
**Location:** Edit 1 TO block

The spec will contain a self-referential forward reference to the phase that is currently executing. This is circular — the spec claims the convention is "locked in v1.4 Phase 20.5" but Phase 20.5 exists to make this edit.

**Fix:** Acceptable post-execution; awkward during execution. No code change needed, but note the temporal oddity.

---

### FLAG-10: Phase 20.5 cross-references to Phases 17–20 may stale

**Severity:** FLAG
**Location:** Design doc §5.1, §7.2; Plan Task 1

The plan claims "no content dependency on Phases 17–20," but Edit 3 and Edit 4 contain cross-references to Phase 18 (FRAME-04) and Phase 19 (PHYS-01). If those phases change their scaling convention naming, the cross-references in `sampling_method.md` become stale.

**Fix:** Add a re-verification note to the Phase 20.5 completion checklist: "Verify cross-references to Phase 18/19 scaling conventions are still accurate after those phases complete."

---

## PASS Findings (Confirmed Correct)

| # | Finding | Evidence |
|---|---------|----------|
| P1 | All 5 FROM blocks are verbatim from `sampling_method.md` | Agent 1 verified character-by-character |
| P2 | Mathematical consistency: coordinate table matches velocity formula | `u_{4+δ_s}` = `u_{3+δ_s+1}` etc. |
| P3 | Resolution doc §4.5 and §10.1 references are accurate | Both sections exist and cover the claimed topics |
| P4 | SCOPE-02 amendment is additive, no distortion | Original FRAME-03 scope preserved; SAMP-01/02 added |
| P5 | Requirement count 30→32 arithmetic is correct | 5+4+4+6+5+2+6 = 32 |
| P6 | `s³` virial-ratio scaling derivation is correct | `T→s²T`, `U→s⁻¹U`, so `Q→s³Q` |
| P7 | Hierarchical ICs use no Sobol — claim is true | `generate_stable_hierarchical_systems` uses `np.random.uniform` only |
| P8 | Option A matches `ic_generation_utils.py` allocation order | Code: idx 0→3 position, 3→4 scale, 4→7 velocity |

---

## Cross-Cutting Concerns

### The `rotate` dimension: a hidden load-bearing omission

Three of four reviewers independently flagged the `rotate=True` branch in `ic_generation_utils.py` (lines 98–99) as omitted from the spec. The code's actual dimension formula is `d = 3 + δ_s + 3δ_v + 3δ_r`; the spec presents `d = 3 + δ_s + 3δ_v` as complete. This is the most material technical gap after the BLOCK findings. It undermines the spec's claim to "match the code exactly" and creates a latent bug for any FUT-01 implementation that enables rotation.

### The probe's inadequacy vs. the plan's honesty

The plan is admirably honest about the probe's limitation: it tests dimension count only, and allocation order is "verified by direct code reading." But honesty does not make the probe sufficient. Phase 20.5's entire purpose is allocation-order correctness. A probe that does not test allocation order is a smoke test, not a verification. This is a process gap, not a spec gap — the spec text is correct, but the verification step is weak.

### Sub-conflict #1: classification matters for FUT-01

Whether the velocity-momentum discrepancy is "under-specified" or "contradictory" is not pedantic — it determines how FUT-01 handles it. If "under-specified," implementers may reasonably choose their own interpretation. If "contradictory in outcome distribution," they must follow the code (which produces the existing dataset). The finding file should be explicit: "FUT-01 MUST follow the code's symmetric split until the spec is corrected."

---

## Recommendations

### Before implementation

1. **Fix BLOCK-1:** Correct design doc §5.4 gap count from 12 to 14.
2. **Fix BLOCK-2:** Upgrade the verification probe to test actual allocation order via synthetic `sobol_batch`.
3. **Fix BLOCK-3:** Qualify the §2.1 "remains valid" claim to acknowledge the scale dimension.

### During implementation (plan amendments)

4. **Amend Edit 2 / Edit 3:** Add `δ_r` for rotation or explicitly scope the formula to `rotate=False` (FLAG-1).
5. **Amend SCOPE-05 rationale:** Tighten to `ic_generation/` only (FLAG-2).
6. **Amend Success Criterion 2:** Narrow "mutually consistent" to exclude the momentum-conservation sentence (FLAG-4).
7. **Amend finding file:** Reclassify sub-conflict #1 as "contradictory in outcome distribution" and add explicit FUT-01 guidance to follow the code (FLAG-3).

### Post-implementation

8. **Re-verify cross-references:** After Phases 18 and 19 complete, check that `sampling_method.md` cross-references to their scaling conventions are still accurate (FLAG-10).
9. **Address `rotate` in a future phase:** When rotation is prioritized, update the spec formula and allocation table to include `δ_r`.
10. **Seek dataset provenance:** If a generation log or manifest exists for the standard quasi-random dataset, cite it in `20-5-DATA-ALIGNMENT.md` (FLAG-7).

---

## Reviewer Notes

This review was conducted by 4 parallel adversarial reviewers, each with a focused mandate, plus synthesis by the orchestrator. All reviewers had access to both design documents and the relevant source files (`sampling_method.md`, `ic_generation_utils.py`, `v1.4-GAPS.md`, `REQUIREMENTS.md`, `ctl_pinn_resolution.md`). Findings were cross-validated across reviewers; overlapping findings (e.g., `rotate` omission, gap count error) were independently discovered by multiple reviewers, increasing confidence.
