# Phase 20 Planning Artifacts — Comprehensive Review Report

**Date:** 2026-06-03
**Reviewers:** 5 parallel subagents (Coherence, Feasibility, Governance/STOP Protocol, Adversarial, Physics/Math)
**Artifacts Reviewed:** 9 files in `.planning/phases/20-architecture-and-normalization-cleanup/`
- `20-CONTEXT.md`, `20-GAPS.md`, `20-RESEARCH.md`, `20-DISCUSSION-LOG.md`
- `20-01-PLAN.md`, `20-02-PLAN.md`, `20-03-PLAN.md`, `20-04-PLAN.md`, `20-05-PLAN.md`
**Cross-References Validated Against:**
- `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, `.planning/STATE.md`
- `.planning/milestones/v1.4-GAPS.md`
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`
- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md`
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md`
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md`

---

## Executive Summary

Phase 20 planning artifacts demonstrate **strong governance awareness** — the STOP protocol, evidence-gating discipline, no-live-code directive, and GAP-20-01 blocking are all correctly implemented. The five-plan wave structure (20-01 ∥ 20-03 in wave 1; 20-02, 20-04 in wave 2) is logically sound for file-level dependencies.

However, this review identified **8 CRITICAL findings** that must be resolved before any plan is executed. The most severe are:

1. **Three plans pre-decide evidence verdicts** (20-01, 20-02, 20-03), creating governance violations that could cause spec drift.
2. **The I_3 geometry derivation in 20-03 is built on a false premise** — the issue doc and resolution doc use the **same formula** with different (both incorrect in different ways) range annotations, not different definitions.
3. **Wave 1 is not actually parallel-safe** — 20-01 and 20-03 both modify `16-ISSUE-LEDGER.md`, creating a race condition.
4. **20-04's conditional touch of `pinn_architecture.md` creates a hidden cross-dependency** with 20-02 that the wave model does not account for.
5. **A fatal identifier collision** — "D-02" means SIREN in 20-01-PLAN but raw-vs-bounded I_norm in 20-GAPS.

**Recommendation:** Do NOT execute Phase 20 plans until all CRITICAL findings are addressed. The fixes are mechanical (rewording verdict instructions, adding sequencing constraints, fixing identifiers) and should take less than one hour to apply.

---

## Critical Findings (Must Fix Before Execution)

### CRIT-01: D-02 Identifier Collision — Two Different Meanings Across Artifacts

**Severity:** CRITICAL  
**Category:** Terminology drift / Identifier collision  
**Files:** `20-CONTEXT.md`, `20-GAPS.md`, `20-01-PLAN.md`

**Finding:** The identifier "D-02" has two incompatible meanings:
- In `20-CONTEXT.md:18`, D-02 is "SIREN / omega0 Contract" (ARCH-01).
- In `20-GAPS.md:20` and `20-CONTEXT.md:71`, "D-02 / ARCH-04" refers to the raw-vs-bounded I_norm naming decision — which is actually `20-CONTEXT.md:69` **D-05**.

In `20-01-PLAN.md:19`, the `must_haves` truth says "D-02: Active SIREN contract is..." — this correctly references 20-CONTEXT D-02. But when an executor cross-references `20-GAPS.md` which also mentions "D-02 / ARCH-04", they will encounter a completely different meaning.

**Impact:** An autonomous agent could confuse SIREN decisions with I_norm decisions, leading to incorrect gap classification or spec edits.

**Fix:**
- Change `20-GAPS.md:22` and `20-CONTEXT.md:71` to reference "20-CONTEXT D-05" (not "D-02") for the raw-vs-bounded I_norm decision.
- Change `20-01-PLAN.md:19` to say "20-CONTEXT D-02 (SIREN)" for clarity.
- Audit all other Phase 20 files for bare "D-0N" references and qualify them with source document.

---

### CRIT-02: 20-01 Pre-decides "expected accept-resolution" Verdict for B-01/B-10

**Severity:** CRITICAL  
**Category:** Governance violation — Pre-decided verdict  
**Files:** `20-01-PLAN.md`

**Finding:** The plan embeds `accept-resolution` as the expected outcome:
- Task 1 Step 4: "If the resolution and issue doc agree the fixed contract is correct, record `accept-resolution` with reason."
- Task 1 Step 6: "Record the verdict (expected `accept-resolution` = remove in-run scheduler)."
- Task 2 PRECONDITION: "Apply the edits below ONLY IF both B-01 and B-10 verdicts are `accept-resolution`."

While a STOP condition exists, the repeated "expected" framing creates confirmation bias. The CRITICAL GOVERNANCE rule states: "The designated candidate verdict source is the candidate, not authority — agent transcribes what is explicit, never fills white space."

**Impact:** An executor may rationalize away contradictions to reach the "expected" verdict, causing spec drift.

**Fix:** Rewrite Task 1 Steps 4-6 to remove "expected" framing:
```
"Record the verdict based on neutral source review. Do not assume
`accept-resolution`. If the sources contradict the resolution doc position,
record the appropriate non-accept verdict or `defer-with-blocker`."
```

---

### CRIT-03: 20-02 Pre-decides "expected accept-resolution" Verdict for M8

**Severity:** CRITICAL  
**Category:** Governance violation — Pre-decided verdict  
**Files:** `20-02-PLAN.md`

**Finding:** Same pattern as CRIT-02. Task 1 Step 4: "If sources support 'project-specific stabilizer, skip-path only, default False', record `accept-resolution` with reason." The desired contract is baked into the verdict instruction itself.

**Impact:** If the issue doc disputes skip-path-only scope or `elementwise_affine=False`, the executor may miss or downplay the contradiction.

**Fix:** Same as CRIT-02 — remove confirmation-biased framing. Make the verdict instruction neutral.

---

### CRIT-04: 20-03 M5 Plan Embeds Geometry-Derived Answer as Presumed Correct Verdict

**Severity:** CRITICAL  
**Category:** Governance violation — Verdict by stealth  
**Files:** `20-03-PLAN.md`

**Finding:** The 20-03 plan (the most contested plan — M5 is explicitly flagged "Sources Disagree: YES — EVID-05 required") pre-writes:
1. The full geometry check with the resolution doc's answer baked in (raw I_3 ∈ [0, 1/3], map 6x-1).
2. All Task 2 spec edits for `accept-resolution`.
3. The Locked Convention section (Task 1 Step 7) is written for `accept-resolution` only.

The `defer-with-blocker` path exists nominally, but the plan's entire editorial structure assumes `accept-resolution`. The other three verdicts (`accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`) have no pre-written wording at all.

**Impact:** The executor is structurally pressured toward `accept-resolution`, potentially recording a verdict that doesn't genuinely engage the issue doc's position.

**Fix:**
- Rewrite Task 1 Step 4 to present the geometry check as **evidence to be recorded**, not as the answer.
- Rewrite Task 1 Step 6 to require neutral weighing of both sources against the geometry check.
- Rewrite Task 1 Step 7 (Locked Convention) with branches for each possible verdict, or state explicitly that only `accept-resolution` and `defer-with-blocker` are prepared, with other verdicts requiring user instruction.
- Rewrite Task 2 to be verdict-neutral: provide edit templates for `accept-resolution` and `accept-issue-doc` at minimum.

---

### CRIT-05: I_3 Issue Doc and Resolution Doc Use the SAME Formula — Not Different Definitions

**Severity:** CRITICAL  
**Category:** Physics / Source mischaracterization  
**Files:** `20-03-PLAN.md`, `20-RESEARCH.md`

**Finding:** The 20-03 plan and 20-RESEARCH repeatedly claim:
> "prior research identified the issue doc as assuming a different range/mapping"

**This is wrong.** Both sources use the **same formula**:
```
I_3 = (d_short + d_mid - d_long) / (d_short + d_mid + d_long)
```

The disagreement is about the **range of that same formula**:
- **Resolution doc:** Correctly states raw range is [0, 1/3], map is 6x-1.
- **Issue doc:** Incorrectly claims raw range is [0, 1], proposes map 2x-1.

The issue doc's M5 finding (`01-architecture-and-physics-foundations.md:87`) says:
> "I_3 claimed 'already in [-1,1]' but formula gives I_3 in [0,1]. Apply `I3_norm = 2*I3 - 1` to map [0,1] → [-1,1]."

The issue doc miscalculated the range of the formula (thought [0,1] instead of [0,1/3]) and proposed a linear map based on that miscalculation. The 20-03 plan's framing ("different range/mapping") implies the issue doc might use a different definition entirely — this misleads the EVID-05 Root-Cause analysis.

**Impact:** The M5 packet may contain an incorrect Root-Cause section, weakening the adjudication. The executor might waste effort looking for a non-existent definitional difference.

**Fix:**
- Rewrite 20-03 plan to explicitly state: "Both sources use the SAME I_3 formula. The disagreement is about the RANGE of that formula and the corresponding linear map, not about the formula itself."
- Rewrite 20-RESEARCH.md ARCH-03 "Source Anchors" to clarify this.
- The Root-Cause Framework Ambiguity section should identify: "The issue doc miscalculated the range of the agreed-upon formula as [0,1] instead of [0,1/3], then proposed a normalization map (2x-1) based on that miscalculation."

---

### CRIT-06: Wave 1 Race Condition — 20-01 and 20-03 Both Modify 16-ISSUE-LEDGER.md

**Severity:** CRITICAL  
**Category:** Execution / Parallelism  
**Files:** `20-01-PLAN.md`, `20-03-PLAN.md`

**Finding:** Both plans are `wave: 1`, `depends_on: []`, and both modify `16-ISSUE-LEDGER.md`:
- 20-01: changes B-01 and B-10 rows to IN_PROGRESS, then later to VERIFIED.
- 20-03: changes M5 row to IN_PROGRESS, then later to VERIFIED.

They edit different rows, but the ledger is a single file. Concurrent execution by separate agents will create git merge conflicts. The wave model claims wave 1 plans are parallel-safe.

**Impact:** Ledger corruption — one plan's status transitions could be overwritten by the other.

**Fix:** Choose ONE of:
- **(a)** Add `depends_on: ["20-01"]` to 20-03 (or vice versa), making ledger edits sequential.
- **(b)** Add explicit `git pull --rebase` instructions before each ledger modification step.
- **(c)** Create a separate ledger-update plan (20-00) that handles all ledger transitions atomically, with other plans producing evidence packets but not touching the ledger.

**Recommendation:** Option (a) is simplest — add `depends_on: ["20-01"]` to 20-03. M5 is `autonomous: false` anyway, so it won't run autonomously in parallel.

---

### CRIT-07: 20-04 Hidden Cross-Dependency with 20-02 on pinn_architecture.md

**Severity:** CRITICAL  
**Category:** Execution / Parallelism  
**Files:** `20-04-PLAN.md`, `20-02-PLAN.md`

**Finding:**
- 20-02 (wave 2, depends_on: 20-01) edits `pinn_architecture.md` for LayerNorm.
- 20-04 (wave 2, depends_on: 20-03) lists `pinn_architecture.md` in `files_modified` and conditionally edits it in Task 2 Step 3.

Both are wave 2 but depend on different wave 1 plans. The wave model says wave 2 plans are parallel-safe. But if 20-04's conditional trigger fires, both edit the same file simultaneously — a race condition.

**Impact:** Merge conflicts or spec regressions if 20-04's conditional touch fires during parallel execution.

**Fix:** Choose ONE of:
- **(a)** Remove `pinn_architecture.md` from 20-04's scope entirely. If the repeated input-normalization note needs updating, make that a 20-02 task (since 20-02 already owns pinn_architecture.md).
- **(b)** Add explicit cross-dependency: make 20-04 depend_on both 20-02 and 20-03, or make 20-02 and 20-04 sequential within wave 2.

**Recommendation:** Option (a) — 20-04 should focus on `ctl_instruction.md`. Any `pinn_architecture.md` normalization-note updates should be owned by the plan that already edits that file (20-02).

---

### CRIT-08: SIREN STOP Condition is Dangerously Misworded — Issue Doc Actually AGREES with Resolution

**Severity:** CRITICAL  
**Category:** Governance / Risk of false STOP or inverted formula  
**Files:** `20-01-PLAN.md`, `20-CONTEXT.md`

**Finding:** The 20-01 plan's STOP condition (Task 1 Step 4) says:
> "STOP CONDITION: if the sources are silent on, or **contradict, the divide-by-hidden_omega_0 direction**... do NOT invent a resolution"

But the sources **DO NOT contradict** the divide-by direction:
- **Resolution doc** (`ctl_pinn_resolution.md:680-681`): `W ~ U[-sqrt(6/n)/omega_0, +sqrt(6/n)/omega_0]` — divide-by-omega_0.
- **Issue doc** (`01-architecture-and-physics-foundations.md:71`): "The source architecture document's hidden-layer init table gives a wrong formula: it **scales with omega0 instead of dividing by omega0**" — the issue doc says the CURRENT SPEC is wrong (it multiplies), and the CORRECT behavior is divide-by-omega_0.

The issue doc's "Recommended Resolutions #2" (`:306`) says:
> "Keep the live code's **divide-by-omega0** implementation and update the source architecture document's table"

**Both sources agree on divide-by-omega_0.** The plan's STOP condition implies there might be a contradiction, but there isn't one.

**Impact:** A misreading executor might:
1. **Unnecessarily STOP** and create a false gap, thinking the issue doc contradicts divide-by.
2. **Invert the formula** to multiply-by-omega_0, thinking the issue doc advocates for scaling — which at omega0=30 across 12 layers would cause catastrophic variance explosion (exactly the bug the issue doc warns about).

**Fix:**
- Rewrite 20-01 Task 1 Step 4 to explicitly clarify: "The issue doc's 'scales with omega0' is a CRITICISM of the current (wrong) spec, not the issue doc's proposed alternative. Both sources agree: the correct behavior is divide-by-omega_0."
- Narrow the STOP condition to only trigger on genuine silence or new contradictions not covered by the known fixed contract.

---

## High-Priority Issues

### HIGH-01: I_3 Geometry Derivation Has a Gap in the Maximization Step

**Severity:** HIGH  
**Category:** Mathematical rigor  
**File:** `20-03-PLAN.md`, Task 1 Step 4

**Finding:** The derivation states:
> "N/P = d_short/(d_short + 2 d_mid) is maximized at d_short = d_mid = d_long (equilateral) ⇒ I_3 = 1/3"

But it skips showing that d_short/(d_short + 2 d_mid) is maximized when d_short = d_mid. The partial derivative argument is omitted.

**Impact:** A challenged EVID-05 adjudication could be undermined on the grounds that the geometry check is incomplete.

**Fix:** Add the explicit step:
```
For fixed d_mid, d_short/(d_short + 2 d_mid) increases monotonically
with d_short (derivative = 2 d_mid / (d_short + 2 d_mid)^2 > 0),
so the maximum occurs at the upper bound d_short = d_mid,
giving N/P = d_mid / (3 d_mid) = 1/3.
```

---

### HIGH-02: 20-01 Edit Targets Don't Exactly Match File Text

**Severity:** HIGH  
**Category:** Execution / Edit failure  
**File:** `20-01-PLAN.md`, Task 2 Step 2

**Finding:** The plan says: "Remove the bracketed author-note '[Need confirmation on this hidden layer's detail ...]'"

But the actual text at line 206 is:
```
**[Need confirmation on this hidden layer's detail. Need to make sure the
formula is correct according to the original SIREN paper?]**
```

The plan's quoted text uses plain square brackets without the bold markdown and omits the second sentence. A naive string replacement will fail.

**Fix:** Update the plan to quote the exact text from the file, including bold formatting and both sentences.

---

### HIGH-03: 20-01 Negative Audit Regex Matches Unrelated "warmup schedule" Text

**Severity:** HIGH  
**Category:** Execution / False positive  
**File:** `20-01-PLAN.md`, Task 3 Step 2

**Finding:** The negative audit command:
```bash
rg -ni "schedul|exponential decay|final_omega|decay_rate|update_omega0" pinn_architecture.md
```

Will match "warmup schedule" (lines 656, 669-670) — a loss-weight warmup scheduler unrelated to omega0. This creates false positives requiring manual disambiguation the plan doesn't account for.

**Fix:** Use a more specific regex:
```bash
rg -ni "omega0.*schedul|schedul.*omega0|exponential decay|final_omega|decay_rate|update_omega0" pinn_architecture.md
```

Or add a note: "Ignore matches for 'warmup schedule' — this is a loss-weight scheduler, not an omega0 scheduler."

---

### HIGH-04: Line Numbers Are "Orientation-Only" in Threat Model but Used as Primary Navigation in read_first

**Severity:** HIGH  
**Category:** Internal contradiction  
**Files:** `20-01-PLAN.md`, `20-02-PLAN.md`

**Finding:** The threat model says line numbers are "orientation only" and agents should "Locate every surface by section anchor / rg text pattern, never by the line numbers quoted here."

But the `read_first` blocks explicitly instruct:
> "start at the lines named in 20-RESEARCH.md (`:106`, `:126`, `:659-660`, `:685`, `:1227-1234`) and re-confirm by text search"

This is a direct contradiction — the plan simultaneously claims line numbers are unreliable and then uses them as primary navigation.

**Fix:** Remove all specific line numbers from `read_first` blocks. Replace with search terms:
```
Read the resolution doc and search for "first_omega_0", "hidden_omega_0",
"scheduler", and "omega_0" to locate all relevant passages.
```

---

### HIGH-05: 20-03 First-Principles Check Is Not "Short and Uncontroversial" in Context

**Severity:** HIGH  
**Category:** Governance  
**Files:** `20-03-PLAN.md`, `20-CONTEXT.md`

**Finding:** The governance rule allows first-principles physics "when the derivation is short and uncontroversial. Longer or contested derivations must be surfaced as a gap."

The I_3 derivation involves: sorting distances, triangle inequality, constrained optimization over a 2D domain, equilateral configuration analysis, and linear map construction. It is ~15 lines. More importantly, it is **contested in context** — a primary source (the issue doc) explicitly disagrees with the conclusion (claims [0,1] instead of [0,1/3]).

**Impact:** An adversarial reviewer could challenge whether this derivation is "uncontroversial" when a primary source contests it.

**Fix:** Add an explicit justification in 20-03:
```
The issue doc does not dispute the I_3 formula itself — it uses the same
formula. The disagreement is about the range calculation, which is a
pure mathematics question (triangle inequality + basic calculus), not a
physics controversy. Therefore the geometry check is uncontroversial.
```

---

### HIGH-06: 20-03 defer-with-blocker Is Treated as a Second-Class Option

**Severity:** HIGH  
**Category:** Governance  
**File:** `20-03-PLAN.md`

**Finding:** While `defer-with-blocker` is listed in the allowed enum, the plan's editorial investment is overwhelmingly in the `accept-resolution` path. The `accept-issue-doc`, `accept-third-position`, and `reject-both-as-unsupported` paths have no pre-written wording — the executor is told to "derive the wording from the M5 Locked Convention." But the Locked Convention section is itself written for `accept-resolution`.

**Fix:** Either (a) provide equal editorial preparation for all five verdict paths, or (b) explicitly state that only `accept-resolution` and `defer-with-blocker` are expected outcomes, with other verdicts requiring user instruction.

---

### HIGH-07: LayerNorm "Skip-Path Only" Scope Is Ambiguous in Resolution Doc

**Severity:** HIGH  
**Category:** Source ambiguity  
**File:** `20-02-PLAN.md`

**Finding:** The resolution doc says "skip path only on power branch" (`ctl_pinn_resolution.md:663-664`). This is ambiguous:
- Interpretation (a): LayerNorm is applied ONLY on the skip path.
- Interpretation (b): LayerNorm is applied on the skip path, but ONLY when that skip path is on the power branch.

The issue doc does NOT dispute skip-path scope — it only disputes attribution. The 20-02 plan's STOP condition ("if M8 cannot ground the branch scope... record a gap") is unnecessarily broad.

**Fix:** Narrow the STOP condition to only trigger if the affine default cannot be grounded. Add a note: "The skip-path scope is NOT contested between sources. Both agree LayerNorm is on the skip path. The dispute is attribution and affine default only."

---

### HIGH-08: Non-Accept-Verdict STOP Lacks Clear Next-Step Protocol

**Severity:** HIGH  
**Category:** Execution / Incomplete protocol  
**Files:** `20-01-PLAN.md`, `20-02-PLAN.md`, `20-04-PLAN.md`

**Finding:** When a STOP condition triggers, the plans say "record a gap and halt Task 2" but don't specify:
- What ledger state to set (`DEFERRED`? Keep `IN_PROGRESS`?)
- How to surface to the user
- Whether other independent plans can continue
- Commit message template for gap-only commits

**Fix:** Add a standard "STOP Protocol" subsection to each executable plan:
```
STOP Protocol:
1. Set ledger row state to DEFERRED (if verdict cannot be grounded) or
   IN_PROGRESS (if awaiting user instruction).
2. Append status-log line: "<today> <pending> IN_PROGRESS -> DEFERRED (STOP: <reason>)".
3. Surface to user via active workflow channel with gap ID and context.
4. Independent plans (those not depending on this plan) may continue.
5. Commit gap-only changes with: git commit -m "gap(20): <gap-id> <brief reason>"
```

---

### HIGH-09: 20-04 Unconditionally Commits pinn_architecture.md Even When Not Edited

**Severity:** HIGH  
**Category:** Execution / Cross-plan contamination  
**File:** `20-04-PLAN.md`, Task 2 Step 4

**Finding:** 20-04's commit command unconditionally adds `pinn_architecture.md`:
```bash
git add .../ctl_instruction.md .../pinn_architecture.md
```

But Task 2 Step 3 says the pinn_architecture.md touch is conditional ("If the surrounding spec text... frames... as a problem/bug/correctness failure, rewrite it"). If no edits were made, the unconditional `git add` is harmless in isolation. But if 20-02 has modified pinn_architecture.md in parallel (wave 2), this will stage 20-02's changes into 20-04's commit.

**Fix:** Make the commit conditional:
```bash
git add .../ctl_instruction.md
# Only add pinn_architecture.md if it was actually modified:
git diff --quiet .../pinn_architecture.md || git add .../pinn_architecture.md
```

---

### HIGH-10: No Cross-Plan Regression Check Between 20-01 and 20-02

**Severity:** HIGH  
**Category:** Execution / Regression risk  
**File:** `20-02-PLAN.md`

**Finding:** 20-02 edits `pinn_architecture.md` after 20-01 has already edited it. There is no explicit cross-plan regression check. What if 20-02's `rg` pattern for LayerNorm accidentally matches text inside newly-added SIREN prose? What if 20-02's edit re-introduces scheduler language?

**Fix:** Add a cross-plan regression check to 20-02's Task 3 (or 20-01's Task 3):
```bash
# After 20-02 commits, re-run 20-01's negative scheduler audit:
rg -ni "omega0.*schedul|schedul.*omega0|exponential decay|final_omega|decay_rate|update_omega0" pinn_architecture.md
# Expected: zero matches (ignore "warmup schedule").
```

---

## Medium-Priority Issues

### MED-01: 20-03 EVID-05 Section Ordering Mismatches Template

**Severity:** MEDIUM  
**Category:** Process-artifact schema  
**File:** `20-03-PLAN.md`

**Finding:** The 20-03 plan orders EVID-05 sections as:
1. First-Principles Physics Check
2. Root-Cause Framework Ambiguity
3. Verdict + "Which Source Was Correct/Wrong"
4. Locked Convention

But `_TEMPLATE.md` orders them as:
1. First-Principles Physics Check
2. Verdict
3. Root-Cause Framework Ambiguity
4. Locked Convention
5. Which Source Was Correct / Wrong

**Fix:** Align the plan's step ordering with the template, or document the deviation as intentional.

---

### MED-02: 20-02 Verify Regex Matches Its Own Intentionally-Added Text

**Severity:** MEDIUM  
**Category:** Execution / Ambiguous verification  
**File:** `20-02-PLAN.md`

**Finding:** Task 2 Step 2 adds: "Enabling affine parameters (`elementwise_affine=True`)... are optional future ablations". Task 3 Step 1 verify: `rg -n "elementwise_affine=True"` must return "no matches except where explicitly labelled an optional future ablation." But the regex will match the parenthetical in the future-ablation sentence, creating an ambiguous pass/fail condition.

**Fix:** Change the verify command to exclude the future-ablation sentence:
```bash
rg -n "elementwise_affine=True" pinn_architecture.md | rg -v "optional future ablation"
```

---

### MED-03: Evidence Template FUT-01 Section May Be Skipped

**Severity:** MEDIUM  
**Category:** Forward-compatibility  
**Files:** All evidence-creation plans (20-01, 20-02, 20-03, 20-04)

**Finding:** The `_TEMPLATE.md` has a "FUT-01 Hand-off Note" section for documenting spec-code divergence. The plans set "Code Paths Touched: Not code-applicable" and may skip the FUT-01 section. But there IS divergence (e.g., B-10's scheduler removal means FUT-01 should verify the code also has no scheduler).

**Fix:** Add a note to each plan's packet-creation step: "Fill the FUT-01 Hand-off Note even for documentation-only findings. Note any spec-code divergence relevant to FUT-01 planning."

---

### MED-04: README.md Energy Evidence Is Weaker Than Claimed

**Severity:** MEDIUM  
**Category:** Evidence grounding  
**File:** `20-04-PLAN.md`

**Finding:** 20-04 cites `README.md:423-443` for energy "regimes," but those lines contain prescreening thresholds (`ENERGY_ERROR_THRESHOLD = 0.01`), not energy normalization support ranges. The README does not document realized energy distributions.

**Fix:** Use qualitative realized-support wording without specific numeric ranges, or record a gap if numeric ranges cannot be grounded.

---

### MED-05: pinn_architecture.md Line Numbers in 20-RESEARCH May Be Stale

**Severity:** MEDIUM  
**Category:** Stale references  
**File:** `20-RESEARCH.md`

**Finding:** 20-RESEARCH cites specific line numbers (`:172`, `:195`, `:269-270`, `:945-947`). The git status shows `pinn_architecture.md` is modified (staged changes from a prior session). These line numbers may already be wrong.

**Fix:** Add a pre-flight note to all plans: "Before starting, run `git diff --name-only` to check for uncommitted changes in target spec files. If changes exist, re-locate all surfaces by `rg` search rather than relying on cached line numbers."

---

### MED-06: 20-05 "User Decision" Claim Is Not in Discussion Log

**Severity:** MEDIUM  
**Category:** Traceability  
**File:** `20-05-PLAN.md`

**Finding:** 20-05 claims "Per the user decision on 2026-06-03 ('Plan 4, block ARCH-04')" but the 20-DISCUSSION-LOG.md contains no such quoted user decision. The log records a procedural note about recording gaps instead of inventing vehicles.

**Fix:** Rephrase to: "Per the planning decision recorded in 20-CONTEXT D-05 and 20-GAPS GAP-20-01."

---

### MED-07: Research Plan Structure Mismatch

**Severity:** MEDIUM  
**Category:** Coherence  
**File:** `20-RESEARCH.md`

**Finding:** 20-RESEARCH's "Planning Implications" recommends a sequential structure (evidence → SIREN/LayerNorm → M5 → support ranges → ARCH-04). But actual plans use parallel waves (20-01 ∥ 20-03 in wave 1; 20-02 ∥ 20-04 in wave 2).

**Fix:** Update the Planning Implications section to match the actual wave structure.

---

### MED-08: ctl_instruction.md Has Internal Inconsistency (Formula vs Range Annotation)

**Severity:** MEDIUM  
**Category:** Pre-existing spec bug  
**File:** `ctl_instruction.md` (not a plan bug, but relevant)

**Finding:** Line 768 reads:
```
I_3 = (d_short + d_mid - d_long) / (d_short + d_mid + d_long) ∈ [-1, 1]
```

The formula is correct (resolution doc's triangle invariant). The range annotation `∈ [-1, 1]` is wrong for the raw formula — correct raw range is [0, 1/3]. This is exactly the inconsistency 20-03 correctly identifies and would fix.

**Note:** This is a pre-existing spec bug, not a plan bug. The 20-03 plan correctly identifies it.

---

### MED-09: Broad `git add` of Evidence Directory Captures Changes from Other Plans

**Severity:** MEDIUM  
**Category:** Execution / Commit contamination  
**Files:** `20-01-PLAN.md`, `20-03-PLAN.md`

**Finding:** Task 3 commits use `git add .planning/phases/16-evidence-framework-and-issue-adjudication/` — the entire directory. If another plan has staged changes in the same directory, they get captured.

**Fix:** Use specific file paths:
```bash
git add evidence/B-01.md evidence/B-10.md 16-ISSUE-LEDGER.md
```

---

### MED-10: M5 Severity Is Invented

**Severity:** MEDIUM  
**Category:** Process-artifact schema  
**File:** `20-03-PLAN.md`

**Finding:** The ledger has no Severity column. 20-03 assigns M5 `Severity: MAJOR` in the packet header. This is not obviously wrong, but it is invented without a source.

**Fix:** Either cite a severity source or use the template default.

---

## Low-Priority Issues and Suggestions

### LOW-01: 20-05 Blocked Placeholder Lacks Mid-Phase Resolution Path

**File:** `20-05-PLAN.md`

If GAP-20-01 is resolved during Phase 20 execution, the placeholder doesn't specify who converts it to an executable plan.

**Fix:** Add: "If resolved during Phase 20, the executor should convert this placeholder following the 20-01/20-02 pattern, or request a new plan from the planning agent."

---

### LOW-02: 20-04 `git diff HEAD~1` Assumes Single-Commit Plan

**File:** `20-04-PLAN.md`, Task 2 verify

`git diff HEAD~1` assumes Task 2 is exactly one commit after Task 1. But the plan has three tasks with three commits.

**Fix:** Use `git diff HEAD~2` or compare against the commit SHA recorded in the plan.

---

### LOW-03: 20-03 `autonomous: false` Makes Wave 1 "Parallel" Misleading

**File:** `20-03-PLAN.md`

20-03 may STOP and surface to the user (defer-with-blocker). It cannot truly run autonomously in parallel with 20-01. The wave assignment is technically correct (no file dependencies), but practically misleading.

**Fix:** Add a note: "20-03 is wave 1 for dependency ordering but may halt for human-in-the-loop adjudication. 20-01 may complete before 20-03 resolves."

---

### LOW-04: GAP-17-05 Referenced but Not Explained

**File:** `20-03-PLAN.md`

The `must_haves` truth mentions "GAP-17-05 (RESOLVED)" but the plan body doesn't explain what it was.

**Fix:** Add a one-sentence explanation: "GAP-17-05 resolved that I_3 is a metadata diagnostic, not a network IC slot, under the Phase 17 input contract."

---

### LOW-05: Hyphenated Grep Variant May Miss "dynamic-scheduling"

**File:** `20-01-PLAN.md`

The negative audit regex searches for "dynamically schedule" but not "dynamic-scheduling" (hyphenated).

**Fix:** Add `dynamic.schedul` to the regex (`.` matches hyphen in some rg modes, or use `dynamic[ -]schedul`).

---

### LOW-06: 20-01 Commit Squashes B-01 and B-10 Together

**File:** `20-01-PLAN.md`

Task 1 commit adds both B-01 and B-10 packets in one commit. This is fine for atomicity but means they cannot be independently reverted.

**Note:** Acceptable as-is. Not a bug.

---

## Grey Areas for Discussion

### GREY-01: Should the I_3 Geometry Check Be in the Plan at All?

The governance rule allows "first-principles physics... when the derivation is short and uncontroversial." The I_3 derivation is mathematically correct but ~15 lines and involves optimization. In the context of M5 (explicitly contested), is this truly "uncontroversial"?

**Discussion point:** Should the geometry check be:
- (a) Pre-written in the plan as evidence to record (current approach)
- (b) Left as a prompt for the executor to derive independently
- (c) Surfaced as a gap itself: "Need user to confirm whether first-principles geometry check is sufficient for EVID-05"

**Reviewer consensus:** (a) is acceptable IF the plan explicitly justifies why it's uncontroversial (the issue doc doesn't dispute the formula, only the range calculation). But the plan should not treat the geometry check as the verdict.

---

### GREY-02: What Happens if M8 Verdict Is Not `accept-resolution`?

20-02 prepares edits only for `accept-resolution`. If M8 yields `accept-issue-doc` (e.g., the issue doc says LayerNorm IS original SQR-SkipResNet content and the resolution doc is wrong), the plan has no prepared edits.

**Discussion point:** Should 20-02 prepare edit templates for at least `accept-resolution` and `accept-issue-doc`? Or is it acceptable to STOP and surface, given that the resolution doc is the "candidate verdict source"?

**Reviewer consensus:** Given the v1.4 governance framework, STOP-and-surface for non-accept verdicts is acceptable. But the plan should explicitly state this expectation.

---

### GREY-03: Energy/Mass "Realized Support" Framing — Is It Meaningful Without Numeric Ranges?

The M9/M10 packets are supposed to ground the realized-support framing in dataset documentation. But README.md does not contain explicit energy or mass range data. The framing may end up purely qualitative.

**Discussion point:** Is qualitative realized-support framing ("the range actually occupied by this dataset") sufficient to meet ARCH-05? Or do we need empirical analysis to derive numeric ranges?

**Reviewer consensus:** Qualitative framing is sufficient for ARCH-05. The requirement is about **framing**, not about deriving new numeric ranges. But the plans should not claim README.md contains evidence it doesn't have.

---

### GREY-04: Should 20-03 Be `autonomous: false` or `autonomous: true` with Human Checkpoint?

20-03 is `autonomous: false` because M5 is contested. But the plan's Task 1 (EVID-05 packet creation) could run autonomously — it's only Task 2 (spec edits) that needs verdict-gating.

**Discussion point:** Should the plan be split into two sub-plans: 20-03a (autonomous: create M5 packet) and 20-03b (autonomous: false, edit spec after user confirms verdict)?

**Reviewer consensus:** Current structure is acceptable. `autonomous: false` for the whole plan is conservative and aligns with governance. But the wave 1 parallel claim is misleading (see LOW-03).

---

## Positive Findings (What's Working Well)

1. **GAP-20-01 is correctly blocked.** 20-05 is a proper blocked placeholder. No attempt to invent evidence vehicles or attach ARCH-04 to M5.
2. **No-live-code directive is consistently enforced.** All five plans explicitly warn against reading/citing pinn/ files.
3. **Evidence-gating structure is correct.** Every spec-edit plan has a PRECONDITION requiring a recorded verdict before edits.
4. **Wave model is mostly correct.** File-level dependencies are properly sequenced (pinn_architecture.md edited by 20-01 then 20-02; ctl_instruction.md edited by 20-03 then 20-04).
5. **20-03 correctly identifies the contested nature of M5.** EVID-05 required sections are all listed, and the STOP condition is present.
6. **Commit cadence is logical.** Each task has its own atomic commit.
7. **Cross-reference network is dense.** Plans correctly reference CONTEXT, RESEARCH, ledger, template, and source documents.

---

## Recommendations Summary

### Before Any Execution

| # | Fix | Files | Effort |
|---|-----|-------|--------|
| 1 | Fix D-02 identifier collision | 20-GAPS.md, 20-CONTEXT.md, 20-01-PLAN.md | 5 min |
| 2 | Remove "expected accept-resolution" from 20-01 | 20-01-PLAN.md Task 1 | 10 min |
| 3 | Remove "expected accept-resolution" from 20-20 | 20-02-PLAN.md Task 1 | 10 min |
| 4 | Rewrite 20-03 to not pre-write accept-resolution | 20-03-PLAN.md Task 1, Task 2 | 20 min |
| 5 | Clarify I_3 sources use SAME formula | 20-03-PLAN.md, 20-RESEARCH.md | 10 min |
| 6 | Add dependency 20-03 → 20-01 (or reverse) | 20-03-PLAN.md frontmatter | 2 min |
| 7 | Remove pinn_architecture.md from 20-04 scope | 20-04-PLAN.md files_modified, Task 2 | 5 min |
| 8 | Fix SIREN STOP condition wording | 20-01-PLAN.md Task 1 Step 4 | 5 min |

**Total estimated fix time: ~70 minutes.**

### Before Plan 20-01 Execution

| # | Fix | Files | Effort |
|---|-----|-------|--------|
| 9 | Fix exact text match for bracketed note | 20-01-PLAN.md Task 2 Step 2 | 5 min |
| 10 | Fix negative audit regex | 20-01-PLAN.md Task 3 Step 2 | 5 min |
| 11 | Remove line numbers from read_first | 20-01-PLAN.md, 20-02-PLAN.md | 10 min |

### Before Plan 20-03 Execution

| # | Fix | Files | Effort |
|---|-----|-------|--------|
| 12 | Add maximization step to geometry derivation | 20-03-PLAN.md Task 1 Step 4 | 5 min |
| 13 | Add first-principles justification | 20-03-PLAN.md Task 1 Step 4 | 5 min |
| 14 | Add equal preparation for all verdicts | 20-03-PLAN.md Task 1 Step 7, Task 2 | 15 min |

### Before Any Plan Execution

| # | Fix | Files | Effort |
|---|-----|-------|--------|
| 15 | Add STOP Protocol subsection to all executable plans | 20-01, 20-02, 20-04 | 15 min |
| 16 | Add cross-plan regression check | 20-02-PLAN.md Task 3 | 5 min |
| 17 | Fix 20-02 verify regex | 20-02-PLAN.md Task 3 Step 1 | 2 min |
| 18 | Fix 20-04 commit conditionality | 20-04-PLAN.md Task 2 Step 4 | 5 min |
| 19 | Add FUT-01 note to packet creation | All evidence plans | 10 min |
| 20 | Fix M9 evidence grounding | 20-04-PLAN.md Task 1 Step 1 | 5 min |

---

## Appendices

### Appendix A: File-by-File Quick Reference

| File | Status | Key Issues |
|------|--------|------------|
| 20-CONTEXT.md | Good | D-02 collision (CRIT-01), D-04/D-05 naming confusion |
| 20-GAPS.md | Good | D-02 collision (CRIT-01) |
| 20-RESEARCH.md | Good | I_3 source mischaracterization (CRIT-05), plan structure mismatch (MED-07) |
| 20-DISCUSSION-LOG.md | Good | Missing "user decision" quote (MED-06) |
| 20-01-PLAN.md | **Needs fixes** | Pre-decided verdict (CRIT-02), race condition (CRIT-06), STOP miswording (CRIT-08), edit mismatch (HIGH-02), regex false positive (HIGH-03), line number contradiction (HIGH-04) |
| 20-02-PLAN.md | **Needs fixes** | Pre-decided verdict (CRIT-03), verify regex ambiguity (MED-02), no regression check (HIGH-10) |
| 20-03-PLAN.md | **Needs fixes** | Verdict by stealth (CRIT-04), I_3 mischaracterization (CRIT-05), geometry gap (HIGH-01), defer second-class (HIGH-06), EVID-05 ordering (MED-01) |
| 20-04-PLAN.md | **Needs fixes** | Hidden dependency (CRIT-07), unconditional commit (HIGH-09), weak evidence (MED-04) |
| 20-05-PLAN.md | Acceptable | Blocked placeholder is correct; minor traceability issue (MED-06) |

### Appendix B: Cross-Reference Validation

| Reference | Target | Status |
|-----------|--------|--------|
| ROADMAP.md:209 | ARCH-01 SIREN | ✓ Valid |
| ROADMAP.md:210 | ARCH-02 LayerNorm | ✓ Valid |
| ROADMAP.md:211 | ARCH-03 I_3 | ✓ Valid |
| ROADMAP.md:212 | ARCH-04 I_norm | ✓ Valid |
| ROADMAP.md:213 | ARCH-05 energy/mass | ✓ Valid |
| REQUIREMENTS.md:47-51 | ARCH-01..ARCH-05 | ✓ Valid |
| 16-ISSUE-LEDGER.md B-01/B-10 | AC-ARCH-01 | ✓ Valid |
| 16-ISSUE-LEDGER.md M5 | AC-ARCH-03 | ✓ Valid |
| 16-ISSUE-LEDGER.md M8 | AC-ARCH-02 | ✓ Valid |
| 16-ISSUE-LEDGER.md M9/M10 | AC-ARCH-05 | ✓ Valid |
| v1.4-GAPS.md GAP-20-01 | ARCH-04 blocked | ✓ Valid |

### Appendix C: Review Team Composition

| Reviewer | Lens | Key Findings |
|----------|------|--------------|
| Coherence | Internal consistency, terminology, dependencies | CRIT-01 (D-02 collision), CRIT-06 (race), CRIT-07 (hidden dep), HIGH-04 (line numbers) |
| Feasibility | Can plans execute? | CRIT-06 (race), HIGH-02 (edit mismatch), HIGH-03 (regex), HIGH-09 (commit) |
| Governance | STOP protocol, evidence-gating, no-live-code | CRIT-02 (pre-decided), CRIT-03 (pre-decided), CRIT-04 (verdict stealth), HIGH-05 (first-principles), HIGH-06 (defer second-class) |
| Adversarial | Stress-test, hidden assumptions | CRIT-05 (I_3 mismatch), CRIT-08 (SIREN STOP), HIGH-01 (math gap), HIGH-07 (LayerNorm scope), HIGH-08 (STOP protocol), HIGH-10 (regression) |
| Physics/Math | Mathematical correctness | CRIT-05 (I_3 definition), HIGH-01 (math gap), MED-08 (spec inconsistency) |

---

*Report generated by 5 parallel reviewer subagents, synthesized and cross-validated. All findings cite specific files and line numbers where applicable.*
