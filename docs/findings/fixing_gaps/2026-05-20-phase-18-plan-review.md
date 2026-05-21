# Phase 18 Plan Review — Frame and Gauge Contracts
**Date:** 2026-05-20  
**Branch:** `milestone/v1.4`  
**Reviewer:** Independent audit  
**Scope:** All Phase 18 planning documents — `18-01-PLAN.md`, `18-02-PLAN.md`, `18-03-PLAN.md`, `18-CONTEXT.md`, `18-GAPS.md`, `18-RESEARCH.md`, `18-PATTERNS.md`, `18-VALIDATION.md` — against the resolution document (`ctl_pinn_resolution.md`) and the CRITICAL GOVERNANCE rule.

---

## Summary

| Severity | Count | Findings |
|---|---|---|
| BLOCKING | 2 | BLOCKING-1 (rotation-gauge algorithm omission + ε gap), BLOCKING-2 (OPEN gap enforcement violation) |
| MAJOR | 4 | MAJOR-3 (F9 user-supplied, confirmed), MAJOR-4 (D/T/V and normalization-scale orphaning), MAJOR-5 (AC-FRAME-01 circular pass-text), MAJOR-6 (9D Cartesian vs 9D position grep mismatch) |
| MODERATE | 1 | MODERATE-7 (Step 1 / Step 2.1 reconciliation) |
| MINOR | 3 | MINOR-8a (VERIFIED→VERIFIED no-op), MINOR-8b (Step 3 precondition imprecision), MINOR-8c (Step 1.5 ghost references) |

**Cross-cutting theme:** Every automated verify in these plans checks for heading strings and keyword markers, not for content completeness. An executor can satisfy all verify commands while leaving algorithm bodies, metadata lists, and definition blocks partially or incorrectly transcribed.

---

## MAJOR-3 (F9) — Stored-Metadata List Incomplete vs Resolution Doc §4.6

**Severity:** MAJOR  
**Location:** `18-01-PLAN.md:259`  
**Resolution doc:** `ctl_pinn_resolution.md:422-441`

### Evidence

Resolution doc §4.6 specifies the complete per-trajectory storage contract verbatim:

```text
traj_id
raw_file_paths
ordered_raw_masses: (3,)
permutation: (3,)
R0: (3,3)
R_COM0: (3,)
V_COM: (3,)
D, T, V
r0_prime_ordered_gauge: (3,3)
v0_prime_ordered_gauge: (3,3)
times_raw: (Nt,)
u: (Nt,)
tau: (Nt,)
r_true_prime_ordered_gauge: (Nt,3,3)
v_true_prime_ordered_gauge: (Nt,3,3)  # optional but recommended
IC13: (13,)
invariants: E, Q, s_min, L_vec, L_norm, I_norm_raw, I1, I2, I3, tau_L
brutus_tolerance, word_length, dt_out, trustworthy_horizon
```

The plan at `18-01-PLAN.md:259` instructs the executor to list: `ordered_raw_masses, permutation, R0, R_COM0, V_COM, D, T, V, r0_prime_ordered_gauge, v0_prime_ordered_gauge, times_raw, u, tau, r_true_prime_ordered_gauge, v_true_prime_ordered_gauge, IC13, and invariant metadata`.

### Missing from the plan

1. **`traj_id`** — trajectory identifier; required for audit trail and Phase 21 regime-stratified probes.
2. **`raw_file_paths`** — source pointer; required for data provenance and audit trail.
3. **Explicit `(optional but recommended)` marker on `v_true_prime_ordered_gauge`** — resolution doc marks this explicitly; omitting it leaves Phase 19/20 workers to infer optionality.
4. **`brutus_tolerance`, `word_length`, `dt_out`, `trustworthy_horizon`** — Brutus integration metadata; `trustworthy_horizon` is directly load-bearing for Phase 21 variance budgets and regime stratification.
5. **Full invariant slate:** `E, Q, s_min, L_vec, L_norm, I_norm_raw, I1, I2, I3, tau_L` — hand-waved as "invariant metadata"; leaves Phase 19/20 workers to invent the invariant set, which is itself a governance gap.

### Why it matters

This is a plain transcription task the plan partially executed. The Brutus integration metadata (`brutus_tolerance`, `trustworthy_horizon`) are the highest-risk omissions: Phase 21's VER-04 needs them for regime-stratified acceptance probes. "Invariant metadata" is an open invitation for Phase 19/20 to invent a list, which would be a MUST-surface semantic gap in those phases.

### Fix

Transcribe §4.6 verbatim into `18-01-PLAN.md` Task 2 sub-step 2.6 metadata list. No discretion required; the resolution doc is complete.

---

## BLOCKING-1 — Rotation-Gauge Algorithm Body Omitted From Plan 2.4 + ε Symbols Unbound

**Severity:** BLOCKING  
**Location (algorithm omission):** `18-01-PLAN.md:242`  
**Location (ε gap):** `ctl_pinn_resolution.md:336, 348, 354` — grep-confirmed only three occurrences, all symbolic  
**Resolution doc:** `ctl_pinn_resolution.md:324-403`

### Part A — Algorithm body omission

The plan's Task 2 sub-step 2.4 instructs:

> "In 2.4 include the Jacobi position definitions, `R_0`, and the gauge target `rho^g = (rho_x, 0, 0)`, `lambda^g = (lambda_x, lambda_y, 0)`, `lambda_y >= 0`."

This transcribes the *output* of the gauge (the fixed-up orientation) but omits the entire *construction algorithm* that §4.4 specifies:

- **`e_x = ρ/||ρ||`** (line 339) — guarded by `||ρ|| > ε_ρ`.
- **`λ_⊥ = λ − (λ·e_x)e_x`** (line 345) — the projection step.
- **`e_y = λ_⊥/||λ_⊥||`** (line 350) — guarded by `||λ_⊥|| > ε_λ`.
- **Complete collinear fallback** (lines 354–370):
  - Use the first nonzero projected vector from the ordered list `ρ̇, λ̇, v̄₁(0), v̄₂(0), v̄₃(0)`.
  - Where `ρ̇ = v̄₂(0) − v̄₁(0)` and `λ̇ = v̄₃(0) − (m₁v̄₁(0) + m₂v̄₂(0))/(m₁+m₂)`.
  - Project the chosen vector perpendicular to `e_x` and normalize.
  - If all candidates are degenerate, choose the fixed coordinate basis vector least aligned with `e_x` and project it perpendicular to `e_x`.
- **`e_z = e_x × e_y`**, R₀ construction (lines 372–387).
- **"Apply the same rotation to every snapshot"** (lines 389–394) — R₀ applied to all `r_i(t_n)` and `v_i(t_n)`, not just the initial state.

The Task 2 verify command (`18-01-PLAN.md:271`) greps only for the string `"canonical rotation gauge"` — confirming only a heading is present, not that the algorithm body was transcribed. An executor following these instructions will produce a spec that names the gauge but lacks the construction algorithm. A future implementer reading only the spec would be unable to implement the gauge correctly from Phase 18's output.

### Part B — ε_ρ and ε_λ unbound (un-surfaced governance gap)

Resolution doc §4.4 uses `ε_ρ` (line 336) and `ε_λ` (line 348) as guards on `||ρ||` and `||λ_⊥||`, and references `ε_λ` again in the collinear-fallback condition (line 354). None of the Phase 18 planning documents surface the fact that these thresholds are never numerically defined anywhere in the resolution document. The three occurrences at lines 336, 348, 354 are all symbolic uses — no binding assignment exists.

**Classification:** This is a **semantic governance gap** under the CRITICAL GOVERNANCE rule — "numerical tolerance choices" where the source punted. It was not logged in `18-GAPS.md`. It must be surfaced to the user before execution reaches sub-step 2.4.

### Consequence

An executor writing sub-step 2.4 must choose numerical values for ε_ρ and ε_λ or leave them symbolic. Either choice is ungrounded and constitutes a MUST-surface decision per the governance block. The plan gives no instruction and no STOP marker.

### Fix

1. Add the full §4.4 construction algorithm to the plan's 2.4 action, verbatim from the resolution doc.
2. Open a new `GAP-18-04` entry in `18-GAPS.md` for ε_ρ/ε_λ numerical values (classification: semantic), update `v1.4-GAPS.md`, and surface to user.
3. Update the Task 2 verify command to check for algorithmic content, not just the heading string — e.g., grep for `e_x = rho/||rho||`, `lambda_perp`, `collinear`, `apply.*every snapshot` or equivalent.

---

## BLOCKING-2 — GAP-18-03 Is OPEN But Plans Execute Past It Without STOP

**Severity:** BLOCKING  
**Location:** `18-GAPS.md:97` (status: OPEN), `18-01-PLAN.md:178` (AC-FRAME-01 pass text), `18-01-PLAN.md` Task 3 (M3 VERIFIED), `18-03-PLAN.md:197-215` (B-05 VERIFIED)  
**Also:** `18-CONTEXT.md:9` (stale governance notice)

### Evidence

`18-GAPS.md` records GAP-18-03 as **OPEN** with **HIGH confidence of impact**. The gap asks whether Phase 18 may define structural `AC-FRAME-*` pass criteria and move B-05/M3 to `VERIFIED` before Phase 21. The STOP protocol is explicit: "Halted work stays halted until the user provides instruction."

Despite this:

- **`18-01-PLAN.md:178`** writes the `AC-FRAME-01 passes when...` structural criterion directly into the Named Acceptance Check template — the exact content GAP-18-03 flags as unapproved.
- **`18-01-PLAN.md` Task 3** moves M3 to `VERIFIED` "after AC-FRAME-01 scaling-order checks pass" — the exact lifecycle closure GAP-18-03 identifies as requiring user instruction.
- **`18-03-PLAN.md:197-215`** moves B-05 from `FIX_APPLIED` to `VERIFIED` after the full suite passes — the second exact closure point GAP-18-03 blocks.

None of these three locations include a `STOP`, a contingency branch, or any acknowledgment that GAP-18-03 is open and these actions require user resolution first.

### Secondary issue — `18-CONTEXT.md:9` stale governance notice

The governance notice at `18-CONTEXT.md:9` states: "Both are `RESOLVED-WITH-INSTRUCTION`... No `OPEN` gaps remain." GAP-18-03 was added to `18-GAPS.md` after `18-CONTEXT.md` was written and after the plans were generated. The notice is now factually false. Any worker reading `18-CONTEXT.md` as a summary of Phase 18 governance state will be misled.

### Fix

1. GAP-18-03 must be resolved with user instruction before any plan executes past a `VERIFIED` closure or writes `AC-FRAME-01 passes when...` text.
2. Until resolved: add a `STOP — GAP-18-03 OPEN` guard immediately above the Named Acceptance Check block in `18-01-PLAN.md` Task 1, above the M3 VERIFIED transition in Task 3, and above the B-05 VERIFIED closure in `18-03-PLAN.md` Task 2.
3. Update `18-CONTEXT.md:9` to reflect the current open-gap count.

---

## MAJOR-4 — D/T/V Definitions and Normalization Scales Orphaned by Step 2 Replacement

**Severity:** MAJOR  
**Location:** `18-01-PLAN.md:244-250` (action for step 2.5), `ctl_instruction.md:382-411` (content being replaced)  
**Resolution doc:** `ctl_pinn_resolution.md:1116-1118` (T, D, V definitions)

### Evidence

The plan instructs the executor to replace the old `Step 2` and `Step 2.5` with a new unified preprocessing pipeline. The action for sub-step 2.5 (scaling) says to include:

```markdown
r_i' = r_i^g / D
v_i' = v_i^g / V
V = D / T
```

The existing `ctl_instruction.md:382-411` (old Step 2 being replaced) contains:

**Lines 388-396 — characteristic scale definitions:**
- `T = t_max = 10` (T is not just a symbol; it equals 10)
- `D = ∛(GT²)` (with G=1, D ≈ 4.6416)
- `V = D / T`

**Lines 403-411 — invariant normalization scales:**
- `E_scale = |median({E_j})| + 10⁻¹⁰`
- `s_min_scale = median({r_char,j})` where `r_char,j = (1/3) Σ_{i<k} ||r'_{i,j} - r'_{k,j}||`
- `Q_scale = 0.5` (fixed)

The plan's 2.5 bullet re-states only the `V = D/T` relation. It does **not** instruct the executor to transcribe `T = t_max = 10` or `D = ∛(GT²)`. An executor who deletes old Step 2 per plan instructions will produce a spec that references `D` and `T` in sub-step 2.5 without ever defining their numerical values. The values are grounded at `ctl_pinn_resolution.md:1116-1118` and must appear in the new Step 2.

The `E_scale/s_min_scale/Q_scale` normalization block (lines 403-411) is more concerning: **the plan makes no mention of it at all**. This block feeds Step 3 and Step 5 invariant staging. It is not in the resolution doc's §10.2 unified preprocessing patch, but it is present in the current spec and feeds downstream steps. The plan's `read_first` list includes `ctl_instruction.md` for this task, so an attentive executor might notice and preserve it — or might not. The plan should explicitly instruct: either transcribe the block into the new Step 2, or confirm the resolution doc intends to remove it (requiring a gap entry if the source is silent).

### Fix

1. Add `T = t_max = 10` and `D = ∛(GT²)` (with G=1) as explicit definitions in the sub-step 2.5 action bullet, grounded at `ctl_pinn_resolution.md:1116-1118`.
2. Add an explicit instruction for the `E_scale/s_min_scale/Q_scale` block: either "preserve verbatim" or "the resolution doc does not include this block — open a gap before deciding."

---

## MAJOR-5 — AC-FRAME-01 Pass Text Is Circular and Monolithic

**Severity:** MAJOR  
**Location:** `18-01-PLAN.md:178`

### Evidence

The Named Acceptance Check text instructs the executor to write:

> "AC-FRAME-01 passes when the specs show exactly one preprocessing order: parse, mass-invariance check, COM recenter, zero-momentum boost, canonical ordering, canonical rotation gauge, then global scaling; B-05 and M3 evidence packets exist; and the issue ledger records the lifecycle transition through VERIFIED only after structural checks pass."

Two problems:

**Circularity.** The criterion for `AC-FRAME-01` to pass includes "the issue ledger records the lifecycle transition through VERIFIED only after structural checks pass." But `AC-FRAME-01` is the structural check that triggers the VERIFIED transition. The AC-FRAME-01 criterion is now self-referential: it passes when the ledger says the thing that only AC-FRAME-01 passing can authorize. An independent Phase 21 executor reading only the ledger and evidence packets cannot determine pass/fail from this text.

**Monolithic bundling.** M3 is about scaling order; B-05 is about COM frame consistency across data families. They are separate findings with separate lifecycle states. The plan's Task 3 closes M3 to VERIFIED via AC-FRAME-01 scaling-order checks only. If B-05 later needs a separate VERIFIED pathway (it does — it waits for FRAME-03 in plan 18-02), the shared AC name makes ledger annotations ambiguous. This is compounded by GAP-18-03 being unresolved.

Note: this finding is partially blocked by BLOCKING-2 — if GAP-18-03 is resolved as option (c) (defer all AC-FRAME criteria to Phase 21), both the circularity and the bundling become moot. But if GAP-18-03 is resolved as options (a) or (b), these structural problems in the draft text need fixing.

### Fix

After GAP-18-03 is resolved: if Phase 18 is permitted to write structural criteria, rewrite the `AC-FRAME-01 passes when...` text to describe an observable, non-self-referential condition on the spec content alone (e.g., "the heading `Step 2: Unified Preprocessing Pipeline` is present and the six pipeline substeps appear in the prescribed order"). Remove the ledger-lifecycle clause.

---

## MAJOR-6 — Verify Regex `9D position` Won't Match Plan-Mandated Text `9D Cartesian positions`

**Severity:** MAJOR  
**Location (action text):** `18-01-PLAN.md:243`  
**Location (broken grep):** `18-03-PLAN.md:234`, `18-VALIDATION.md:31`  
**Phase gate:** Phase-final full-suite verification, Strict Full Suite Command

### Evidence

Plan 18-01 Task 2 action at line 243 instructs the executor to write prose containing:

> "the model output remains **9D Cartesian positions** and is not planar or invariant-only"

Both the 18-03-PLAN.md Task 2 automated verify (line 234) and the 18-VALIDATION.md Strict Full Suite Command (line 31) include:

```bash
rg -n "3D Cartesian|velocities remain fully 3D|9D position|not planar|not invariant-only" ...
```

The literal string `"9D position"` is NOT a substring of `"9D Cartesian positions"`. The string `9D Cartesian positions` starts with `9D C`, not `9D p`, so the `9D position` alternative in the `rg` pattern will not match.

The overall `rg` command still has other OR alternatives (`not planar`, `not invariant-only`) that may match the written text and cause the command to exit 0 even though the `9D position` check specifically fails. This means:

- The `9D position` term provides **no verification coverage** for the "9D Cartesian" constraint.
- The phase-final gate silently passes on `not planar` and `not invariant-only` hits, giving false assurance that the 9D Cartesian guard was verified.

### Fix

Replace `9D position` in both the 18-03-PLAN.md Task 2 verify and the 18-VALIDATION.md Strict Full Suite Command with `9D Cartesian`:

```bash
rg -n "velocities remain fully 3D|9D Cartesian|not planar|not invariant-only" ...
```

Also remove `3D Cartesian` from the pattern — it is not present in the expected output text ("9D Cartesian") and adds confusion.

---

## MODERATE-7 — Step 2.1 Parser Sub-Step vs Existing Step 1 Reconciliation

**Severity:** MODERATE  
**Location:** `18-01-PLAN.md` Task 2 action (sub-step 2.1), `ctl_instruction.md:339`  
**Resolution doc:** `ctl_pinn_resolution.md:255-269`

### Evidence

The plan instructs the executor to create sub-step 2.1 "Parser contract and mass-invariance check" inside the new unified `Step 2: Unified Preprocessing Pipeline`. The resolution doc §4.1 (lines 255-269) specifies parsing as the first operation in the preprocessing chain.

The current `ctl_instruction.md:339` already contains `## Step 1: Parse Raw Simulation Data`. Both steps cover parsing Brutus output files. The plan does not instruct the executor to:

- Remove or rename the existing Step 1, or
- Define what "parser contract" means in 2.1 vs Step 1, or
- Explain how the mass-invariance check `max|m_i(t) − m_i(0)| < 1e-15` relates to Step 1 content.

An executor will be left deciding whether Step 1 survives unchanged and 2.1 is a logic layer on top of it, or whether 2.1 absorbs Step 1's content. This is an under-specified action, not a governance gap, but it creates ambiguity at execution time and risks double-specification of the parser contract.

### Fix

Add an explicit instruction to the Task 2 action: either "Step 1 remains untouched; 2.1 is a spec-level contract layer that supplements it" or "move Step 1 content into sub-step 2.1 and renumber subsequent steps." Grounded by resolution §10.2 line 1125: "Replace Step 2.5 with a unified frame/gauge step" — Step 1 is not mentioned in the replacement patch, implying Step 1 survives.

---

## MINOR-8a — VERIFIED→VERIFIED Transition Log Is a No-Op Schema Extension

**Severity:** MINOR  
**Location:** `18-03-PLAN.md:221`

The plan instructs the executor to append this M3 transition-log entry:

```text
2026-05-20 ${EDIT_SHA} VERIFIED -> VERIFIED (Phase 18 P03 Task 2; regression check after FRAME-03 sampling edit)
```

A `VERIFIED → VERIFIED` transition is a state no-op: M3 is already VERIFIED from plan 18-01 Task 3. The Phase 16 lifecycle schema (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`) does not include a "regression re-check" loop. This entry either (a) invents a new lifecycle sub-state not present in any governance document, which is a process-artifact schema decision that should be surfaced, or (b) is a cosmetic audit note disguised as a lifecycle transition.

If the intent is to record that M3 was re-checked after the FRAME-03 sampling edit, the appropriate form is a comment/note in the evidence packet, not a lifecycle log entry. The lifecycle log should record only actual state changes.

### Fix

Replace the `VERIFIED → VERIFIED` lifecycle log with a prose note in `M3.md` (e.g., under "Follow-up Notes") that records the FRAME-03 regression check result. Do not append a no-op lifecycle transition.

---

## MINOR-8b — Step 3 Precondition Retarget Is Imprecise

**Severity:** MINOR  
**Location:** `18-01-PLAN.md:260`

The plan instructs: "Retarget Step 3's precondition text from old Step 2.5 to new Step 2." The current `ctl_instruction.md:437` says "checked already in step 2.5" and must be updated to point to the new unified pipeline. However, the instruction says to retarget to "new Step 2" without specifying which sub-step. The new Step 2 has six sub-steps (2.1 through 2.6); the relevant precondition (COM/momentum assertions) lands at sub-step 2.6. "New Step 2" is underspecified and could be interpreted as pointing to "Step 2: Unified Preprocessing Pipeline" generically rather than the assertions sub-step.

### Fix

Change the instruction to: "Retarget Step 3's precondition text to Step 2.6 (COM/momentum assertions)."

---

## MINOR-8c — Step 1.5 Ghost References Not Covered by Negative Grep

**Severity:** MINOR  
**Location:** `ctl_instruction.md:688, 695, 427` (existing stale references), `18-01-PLAN.md:271` (verify command)

The current `ctl_instruction.md` contains multiple "Step 1.5:" references at lines 427, 688, and 695 that are stale artifacts from the pre-Phase-18 structure. The plan's verify command at line 271 includes:

```bash
! rg -n "Step 2\.5: Verify Center-of-Mass|Hierachical ICs are NOT in COM frame|for quasi-random ICs and Brutus, we will not perform a transformation" ctl_instruction.md
```

This negative check catches the specific Step 2.5 stale sentences but does not check for "Step 1.5" references. If the executor removes old Step 2.5 content but leaves "Step 1.5" references at lines 688 and 695 (inside the canonical ordering function), the verify passes while the ghost references remain.

### Fix

Add `! rg -n "Step 1\.5" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` to the Task 2 verify command.

---

## Cross-Cutting Theme — Verify Regexes Check Headings, Not Algorithm Completeness

Every automated verify in the Phase 18 plans uses `rg` to assert that certain keywords appear in spec files. This pattern provides assurance that correct headings and key terms exist, but provides **no assurance** that:

- Algorithm bodies are complete (BLOCKING-1: rotation-gauge construction algorithm);
- Metadata lists are fully transcribed (MAJOR-3: stored-metadata keys);
- Numerical definitions are present (MAJOR-4: T=t_max=10, D=∛(GT²));
- Grep patterns match the actual text the plan mandates (MAJOR-6: `9D position` vs `9D Cartesian positions`).

The correct mitigation is not to replace all grep-based verification — heading/keyword checks have real value for detecting missing sections. The mitigation is to **also** add content-level checks for the most consequential transcription items (metadata key counts, definition appearances, algorithm-step markers) and to manually verify algorithm-body completeness during execution review (as already noted in `18-VALIDATION.md` Manual-Only Verifications table for FRAME-04).

---

## Cleared False Gaps (Explicitly Not Raised)

The following items were evaluated during this review and found to be correct or grounded. They are documented here to prevent re-examination:

1. **Quasi-random COM zero-by-construction claim (18-02-PLAN.md Task 2).** The claim that `p3 = -(p1+p2)` zeros the position COM and `v1 = -v2/2, v3 = -v2/2` zeros total momentum "for equal masses" is correct. `sampling_method.md:74` explicitly states "planar, **equal-mass** three-body system" and line 84 confirms the COM condition holds "for the equal-mass case." The equal-mass qualifier is correctly present in the plan's FRAME-03 note.

2. **Brutus frame transform (18-02-PLAN.md).** Brutus integrates Newtonian gravity in an inertial frame. For an isolated three-body system, the COM moves at constant velocity (zero net external force). The COM transform `r̄_i = r_i − R_COM(0) − V_COM·t` is therefore universally applicable to Brutus output, regardless of IC family. No gap exists here.

3. **FRAME-04 guard placement in sub-step 2.4 (18-01-PLAN.md:243).** Placement is grounded by `18-CONTEXT.md` D-05: "FRAME-04 3D Cartesian guard belongs at the rotation-gauge sub-step... exact wording = Claude's discretion." Explicitly authorized; not a gap.

4. **FRAME-02 derivative consequence in `pinn_architecture.md` (18-01-PLAN.md Task 3).** Phase 17 already locked the hard COM projection head in `pinn_architecture.md`. Phase 18 adds a cross-reference only, not a re-locking. The plan's "optional FRAME-02 cross-reference only" characterization is correct.

---

## Action Items by Plan

### 18-01-PLAN.md

| # | Action | Severity | Blocks Execution? |
|---|---|---|---|
| A1 | Resolve GAP-18-03 before proceeding | BLOCKING | Yes — until resolved, no AC-FRAME-01 pass text or VERIFIED closures |
| A2 | Add full §4.4 rotation-gauge algorithm to 2.4 action | BLOCKING | Yes |
| A3 | Open GAP-18-04 for ε_ρ/ε_λ numerical values | BLOCKING | Yes |
| A4 | Transcribe §4.6 verbatim into sub-step 2.6 metadata list | MAJOR | Yes |
| A5 | Add T=t_max=10 and D=∛(GT²) definitions to sub-step 2.5 | MAJOR | Yes |
| A6 | Add explicit disposition instruction for E_scale/s_min_scale/Q_scale block | MAJOR | Yes |
| A7 | Rewrite AC-FRAME-01 pass text (non-circular, non-bundled) after GAP-18-03 resolved | MAJOR | After GAP-18-03 |
| A8 | Reconcile Step 2.1 vs existing Step 1 | MODERATE | No |
| A9 | Retarget Step 3 precondition to sub-step 2.6 | MINOR | No |
| A10 | Add `! rg "Step 1\.5"` to Task 2 verify | MINOR | No |
| A11 | Update Task 2 verify to check algorithm-body content, not heading only | MODERATE | No |

### 18-03-PLAN.md and 18-VALIDATION.md

| # | Action | Severity | Blocks Execution? |
|---|---|---|---|
| B1 | Add GAP-18-03 STOP guard above B-05 VERIFIED closure | BLOCKING | Yes |
| B2 | Fix `9D position` → `9D Cartesian` in Task 2 verify (18-03-PLAN.md:234) | MAJOR | Yes |
| B3 | Fix `9D position` → `9D Cartesian` in Strict Full Suite Command (18-VALIDATION.md:31) | MAJOR | Yes |
| B4 | Replace VERIFIED→VERIFIED no-op log with M3 prose note | MINOR | No |

### 18-CONTEXT.md

| # | Action | Severity |
|---|---|---|
| C1 | Update governance notice at line 9 to reflect GAP-18-03 OPEN state | MINOR |
