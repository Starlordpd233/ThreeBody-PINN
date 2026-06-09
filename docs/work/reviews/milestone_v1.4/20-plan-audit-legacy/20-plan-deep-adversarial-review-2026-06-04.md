# Phase 20 Plan Deep Adversarial Review — 2026-06-04

**Review type:** Second-pass adversarial review (8-dimension framework)
**Prior reviews:** `20-plan-review-findings.md` (first-pass, 2026-06-03)
**Scope:** All 9 Phase 20 planning artifacts (5 plans + CONTEXT + RESEARCH + GAPS + DISCUSSION-LOG)
**Methodology:** 3-pass review — Pass A (scout/structural + source verification), Pass B (4 parallel adversarial subagents), Pass C (synthesis)

---

## Executive Summary

Phase 20's plans are well-structured and correctly identify the target surfaces in the framework specs. Evidence-gating is properly designed, STOP conditions are generally correct, and the plan architecture (evidence-first, verdict-gated edit, closure audit) is consistent across all executable plans.

**However, this review identified 3 CRITICAL findings, 8 HIGH findings, and 9 MEDIUM findings.** The most serious issues are: (1) a numeric mass range hardcoded in 20-04's spec edit prose that was computed under the v1.3 mass normalization formula (incompatible with v1.4's formula), (2) the I₃ adjudication plan (20-03) under-specifies what to do when the conditional lemma doesn't apply — which is the expected case given the issue doc's genuinely different I₃ definition, and (3) 20-04's `autonomous: true` flag is incorrect given the semantic judgment its STOP conditions require.

---

## Findings by Severity

### CRITICAL

#### C-001: Mass range `[-0.93, 0.585]` computed under v1.3 formula, ungrounded for v1.4 (D4/D5)

- **Plan:** 20-04-PLAN.md, Task 2 Step 2 (line ~185); 20-CONTEXT.md D-06 (line ~90)
- **What the plan says:** The spec edit prose hardcodes: "The hierarchical-mass `m_norm` range is asymmetric (approximately `[-0.93, 0.585]`, not centered on 0)"
- **Source verification — corrected finding:**
  - The numbers `[-0.93, 0.585]` DO appear in the issue doc at line 90 (M10 finding): "m_norm range asymmetric for hierarchical masses: [-0.93, 0.585]" — this is legitimate provenance. My initial Pass A scan incorrectly classified this as `[-n, n]` placeholder. **Correction:** The issue doc uses `[-n, n]` in normalization tables but provides specific numbers in the M10 finding.
  - **HOWEVER**, the D5 adversarial agent identified that these numbers were computed using the **v1.3 mass normalization formula** `2*(m_i/M_tot) - 1` (mass fraction with linear map to [-1, 1]). The v1.4 framework spec (Phase 17 input contract, `ctl_instruction.md:1027`) uses a **fundamentally different formula**: `tanh((m_i - mu_{m_i})/(sigma_{m_i} + 10^-8))` — dataset-statistics-based tanh squash on raw ordered masses.
  - These two formulas produce different numeric ranges for the same mass distribution. The `[-0.93, 0.585]` numbers are grounded in the issue doc but were derived for a normalization formula that v1.4 **replaced**.
  - Neither the issue doc, nor the dataset README, nor any other source re-derives this range for the v1.4 formula.
- **Why CRITICAL:** The plan instructs a subagent to insert numeric values from a v1.3-era formula into a v1.4 framework spec that uses a different formula. An executor creating the M10 evidence packet would find the issue doc's numbers but lack any source that confirms they apply to the v1.4 tanh-statistics formula. This forces either (a) committing numbers known to come from an incompatible formula, (b) recording a STOP gap, or (c) silently assuming the formulas produce similar ranges. All three are unacceptable. The plan's own governance (D-06: "Every numeric range must cite README.md" in the threat model) would additionally flag these numbers since README.md does not contain them.
- **Suggested fix:** Three options: (a) Replace with qualitative language matching the sources ("asymmetric, not centered on 0" without v1.3-derived numbers), (b) Add a Phase 16 evidence step to empirically recompute the range from the v1.4 tanh formula using actual dataset statistics and record in M10 before editing, or (c) Cite the issue doc numbers with an explicit formula-incompatibility caveat in the spec prose and M10 packet.

#### C-002: 20-03 executor is left without guidance when conditional lemma doesn't apply (D7/D4)

- **Plan:** 20-03-PLAN.md, Task 1 Steps 4-5 (lines ~122-124)
- **What the plan says:**
  > "If Step 4 revealed that one or both sources use a genuinely different `I_3` definition (e.g., sorted mutual distances), the conditional lemma does not apply to the dispute and you must either derive the appropriate first-principles check for the matched definition, or record `defer-with-blocker` if the definitions are too divergent to adjudicate."
- **Source verification confirms:** The issue doc (`01-architecture-and-physics-foundations.md:536`) defines I₁, I₂, I₃ as `sorted([r_01, r_12, r_20])` — literal mutual distances. The issue doc's normalization is `2*(I_i/I_max) - 1` where `I_max = I_3`, making I₃_norm ALWAYS equal to `2*1 - 1 = 1` (a degenerate constant). The resolution doc uses the ratio form `(d_short+d_mid-d_long)/(d_short+d_mid+d_long)` with range `[0, 1/3]`. These are **genuinely different definitions** — the conditional lemma will NOT apply.
- **Why CRITICAL:** The plan tells the executor to "derive the appropriate first-principles check for the matched definition" — but provides zero guidance on what that check would be. For the sorted-distance definition, the "appropriate first-principles check" would need to address: what is the raw range of sorted mutual distances? How does one normalize them? The issue doc's own normalization is degenerate (I₃/I_max = 1 always). This is a substantive physics/engineering task, not a mechanical evidence-filling exercise. The `autonomous: false` flag is correct, but the plan's fallback path ("derive...or record defer-with-blocker") puts the executor in an impossible position — the executor cannot derive a novel physics check and will inevitably record `defer-with-blocker`, making this plan effectively a blocker-discovery exercise rather than an executable adjudication.
- **Suggested fix:** Restructure 20-03 as an explicit two-phase plan: Phase A — source-definition comparison only (autonomous), with the expected outcome being a gap registration acknowledging the definition mismatch. Phase B — user-provided resolution path (not autonomous), triggered after the user chooses which definition framework to use. Or, pre-compute the sorted-distance first-principles analysis and include it as an alternative lemma in 20-RESEARCH.md parallel to the existing ratio-form lemma.

#### C-003: 20-04 `autonomous: true` flag is incorrect given semantic judgment requirement (D6)

- **Plan:** 20-04-PLAN.md, frontmatter `autonomous: true`
- **Discussion log D-11:** "Keep autonomous:true. Unlike M5, M9/M10 are not flagged Sources-Disagree/EVID-05, and the only judgment ('can this be grounded?') has a deterministic safe default (record a 20-GAPS entry, halt Task 2, surface to user)."
- **Why CRITICAL:** The reasoning in D-11 is flawed. "Can this be grounded?" is NOT a mechanical question. Determining whether source documents + dataset docs "ground" realized-support framing requires semantic judgment about what constitutes sufficient evidence. The plan's own STOP condition says: "If M9 cannot ground the support range (numeric or qualitative) without inventing it, record a gap." But the decision of whether something is "invented" vs "grounded" is itself a semantic judgment. An autonomous agent could (1) incorrectly judge weak evidence as sufficient grounding, or (2) incorrectly judge sufficient evidence as insufficient and record a spurious gap. The safe default ("record a gap") is only safe if the agent can reliably identify when grounding is insufficient — which requires exactly the kind of semantic judgment that `autonomous: false` is designed to protect against. This is compounded by C-001 — the plan already contains ungrounded numbers that an autonomous agent would need to judge.
- **Suggested fix:** Set `autonomous: false` for 20-04, or restructure to make the grounding test mechanical (e.g., "if README.md contains a numeric range for hierarchical mass support, cite it; otherwise use qualitative language and note the absence").

---

### HIGH

#### H-001: Wave labeling implies false parallelism (D2)

- **Plan:** 20-04-PLAN.md frontmatter (`wave: 2`) and 20-03-PLAN.md frontmatter (`wave: 2`)
- **Issue:** 20-04 depends on BOTH 20-02 AND 20-03. Both dependencies are labeled `wave: 2`. But 20-04 cannot start until both complete — this makes 20-04 effectively wave 3. More importantly, 20-03 and 20-04 both edit `ctl_instruction.md` and are in the same wave. The only thing preventing a concurrent-edit conflict is 20-04's `depends_on: ["20-02", "20-03"]` — but if an orchestrator dispatches based on wave number rather than explicit dependencies, 20-03 and 20-04 could run concurrently and corrupt `ctl_instruction.md`.
- **Suggested fix:** Either label 20-04 as `wave: 3` or add an explicit warning that wave-2 plans editing `ctl_instruction.md` must be serialized.

#### H-002: 20-01 SIREN negative audit exemption is fragile to line shift (D1)

- **Plan:** 20-01-PLAN.md, Task 3 Step 2 (lines ~206-208)
- **Issue:** The negative audit exempts SI-PINN-002 at "~line 1000" as "conversion-provenance metadata, not active scheduler guidance." But after Task 2 edits remove ~30 lines from the file (the scheduler block + rationale), the SI-PINN-002 section will shift up to ~line 970. The audit uses `rg` pattern matching (not line numbers), so the exemption is specified by approximate position. A subagent checking line 1000 would find different content post-edit. The plan's `rg` patterns are correct and line-number-independent, but the exemption rationale references a line number that will be stale.
- **Suggested fix:** Identify SI-PINN-002 by section anchor (`rg -n "### SI-PINN-002"`) rather than approximate line number.

#### H-003: Cross-plan regression tests duplicate patterns without cross-validation (D1/D2)

- **Plan:** 20-02-PLAN.md, Task 3 Step 4 (lines ~209-212) re-runs 20-01's omega scheduler negative audit.
- **Issue:** 20-02's regression check uses the SAME `rg` pattern as 20-01. If 20-01's pattern has a false negative (missing a scheduler variant), 20-02's check would also miss it. There's no cross-validation — the second plan doesn't independently verify the first plan's work, it just re-runs the same check.
- **Suggested fix:** Add an orthogonal verification (e.g., search for `schedul` broadly and manually inspect each hit, rather than relying on 20-01's specific regex).

#### H-004: M5 evidence packet Step 4 (definition comparison) under-specified (D3/D7)

- **Plan:** 20-03-PLAN.md, Task 1 Step 4 (line ~122)
- **Issue:** Step 4 says: "Add a short comparison table that separately classifies each source's (a) I₃ definition, (b) raw range claim, and (c) normalization/input mapping." But the plan doesn't tell the executor what a "genuinely different" definition means or how to resolve the discovery. The executor could correctly identify that the issue doc defines I₃ as sorted distances while the resolution doc uses the ratio form, but what then? Step 4 says "choose defer-with-blocker" if unresolvable, but it's unclear whether the executor should attempt to resolve before deferring.
- **Suggested fix:** Add explicit decision criteria: "If the definitions use different mathematical formulas applied to different quantities, they are genuinely different and the conditional lemma does not apply. Proceed to defer-with-blocker after documenting the mismatch."

#### H-005: No phase exit condition defined for partial ARCH-04 block (D8)

- **Plans:** 20-05-PLAN.md, 20-CONTEXT.md
- **Issue:** Phase 20 has 5 requirements (ARCH-01 through ARCH-05) but ARCH-04 is blocked by GAP-20-01. No artifact defines what "Phase 20 complete" means given one requirement is blocked. Can Phase 20 exit with ARCH-04 unresolved? Must Phase 21 wait for ARCH-04? The roadmap says Phase 21 "Depends on: Phase 20" — does a partial Phase 20 completion satisfy this dependency?
- **Suggested fix:** Add an explicit phase exit condition to 20-CONTEXT.md or ROADMAP.md: "Phase 20 exits when ARCH-01/02/03/05 are closed. ARCH-04 is tracked as a deferred requirement carried forward to Phase 21 or resolved via GAP-20-01 before Phase 20 exit."

#### H-006: 20-03 pre-written prose structurally biases toward accept-resolution (D3/D4)

- **Plan:** 20-03-PLAN.md, Task 2 Steps 1-2
- **Issue:** 20-03 is `autonomous: false` and is a STOP-protocol EVID-05 adjudication, yet Task 2 pre-writes spec-edit prose exclusively for the `accept-resolution` path. The FALLBACK says to use the Locked Convention for other verdicts, but the executor is given ready-to-copy prose for only one of five possible outcomes. In a task where the correct outcome is more likely `defer-with-blocker` (due to genuine I₃ definition mismatch), this structural bias works against the governance-intended neutrality.
- **Suggested fix:** Either remove ALL pre-written spec-edit prose from Task 2 and direct the executor to derive wording from Task 1's Locked Convention regardless of verdict, or add equivalent prose blocks for all 5 verdict outcomes.

#### H-007: 20-04 verification command `git diff | rg ... || true` is a no-op gate (D1)

- **Plan:** 20-04-PLAN.md, Task 2 Step 4 (line ~192-196)
- **Issue:** The pre-commit verification uses `git diff -- ctl_instruction.md | rg 'tanh|E_scale' || true`. The `|| true` makes the command ALWAYS succeed (exit 0). Both "no formula changes found" (rg exit 1, masked) and "formula changes found" (rg exit 0) produce exit 0. The verification is a no-op — it cannot detect formula corruption. Combined with the verify step only checking for framing language, there is no automated guard against accidental normalization formula changes.
- **Suggested fix:** Restructure as a positive assertion that DETECTS unwanted changes: `if git diff -- ctl_instruction.md | rg -q '^-.*tanh\|^-.*E_scale'; then echo 'ERROR: normalization formula changed'; exit 1; fi`.

#### H-008: 20-01 truth statement contradicts SI-PINN-002 exception (D1)

- **Plan:** 20-01-PLAN.md, `must_have.truths` (line 20) vs Task 3 Step 2 (line ~208)
- **Issue:** The `must_have.truths` states: "No active/normative SIREN scheduler guidance... remains ANYWHERE in pinn_architecture.md." This is absolute. But Task 3's negative audit explicitly exempts SI-PINN-002 at ~line 1000 as "allowed non-normative conversion-provenance metadata." A subagent reading the truth literally would attempt to purge SI-PINN-002; a subagent reading the verify step first would be confused about whether the truth allows the exception. This internal contradiction could cause unnecessary file edits or a spurious verification failure.
- **Suggested fix:** Qualify the truth: "...remains anywhere in pinn_architecture.md except in non-normative conversion-provenance metadata (SI-PINN-002)."

---

### MEDIUM

#### M-001: Ledger merge conflict risk from 4 independent editors (D2)

- **Issue:** Four plans independently modify `16-ISSUE-LEDGER.md`: 20-01 (B-01/B-10 rows), 20-02 (M8 row), 20-03 (M5 row), 20-04 (M9/M10 rows). If these edits are committed in separate git commits, git's merge is trivially clean (different lines). But if two plans run in the same wave and edit before committing, the second plan's ledger read could be stale. The wave structure (20-01 → 20-02/20-03 → 20-04) serializes the ledger writes, so this is low-risk, but no plan explicitly gates its ledger write on a fresh `git pull` or re-read of the ledger.
- **Suggested fix:** Add a pre-edit ledger re-read step to each plan's Task 1.

#### M-002: 20-04 Task 3 Step 2 negative audit pattern may miss defect-framing variants (D1)

- **Plan:** 20-04-PLAN.md, Task 3 Step 2 (line ~224)
- **Issue:** The negative audit pattern `rg -ni "normalization (bug|error|failure)|invalid normalizer|should be symmetric|must be positive"` searches for specific English phrases. Defect-framing could use different language ("incorrect", "problem", "unexpected", "issue with", "flawed") that this pattern would miss.
- **Suggested fix:** Broaden the pattern or add a manual review step for any normalization-adjacent prose.

#### M-003: 20-01 Task 2 Step 2 old_string match is narrative, not exact (D1)

- **Plan:** 20-01-PLAN.md, Task 2 Step 2 (line ~169)
- **Issue:** The plan says to replace "The crucial difference is the scaling of the initialization range by $\omega_0$." The actual file text at line 195-196 reads: "The hidden_omega_0 parameter is also set to 1. The crucial difference is the scaling of the initialization range by $\omega_0$." The plan's instruction only matches the second sentence — a subagent using a strict text-replace tool would need the exact string. This is minor because subagents typically use section-level editing, but it's an imprecision worth noting.
- **Suggested fix:** Specify the exact old_string including context.

#### M-004: 20-RESEARCH conditional lemma doesn't address I₃ = 0 edge case (D5)

- **Source:** 20-RESEARCH.md, "Conditional Lemma — Ratio-Form I₃ Range Derivation"
- **Issue:** The derivation shows I₃ ∈ [0, 1/3]. The minimum I₃ = 0 occurs for collinear configurations (d_long = d_short + d_mid). While mathematically correct, the derivation doesn't discuss whether:
  1. Perfectly collinear configurations are reachable in the Jacobi-state parameterization
  2. The tanh mapping I₃^in = 6·I₃ − 1 maps 0 → -1, which is at the tanh saturation boundary
  3. Whether collinear-adjacent configurations create gradient issues
  These are edge cases a subagent might need to handle when writing the M5 packet's physics check.
- **Suggested fix:** Add a brief edge-case note to the lemma.

#### M-005: 20-05 I_norm surface list predates 20-03/20-04 edits (D7)

- **Plan:** 20-05-PLAN.md, "Current-spec surfaces to audit" section
- **Issue:** The plan documents 4 I_norm surfaces with a note: "re-locate by rg, not line number, since 20-03/20-04 shift ctl_instruction.md." While the instruction is correct (use rg not line numbers), the specific list of surfaces was located on 2026-06-03 BEFORE 20-03 and 20-04 edit the file. 20-03's I₃ edits and 20-04's normalization prose additions will shift line numbers AND may add new I_norm-adjacent text. The surface list should note that post-20-03/20-04, an additional audit is needed for any new I_norm mentions added by those plans.
- **Suggested fix:** Add: "After 20-03 and 20-04 complete, re-run the I_norm surface audit to catch any new I_norm mentions introduced by those plans' edits."

#### M-006: Plans reference "20-CONTEXT D-02" (SIREN) but issue doc also has D-02 (I_norm) (D2)

- **Context:** 20-CONTEXT.md D-02 is "SIREN / omega0 Contract." The issue doc has a different D-02: "I_norm definition" (routine documentation cleanup). 20-RESEARCH.md notes this: "issue-doc D-02, distinct from 20-CONTEXT D-02 SIREN."
- **Issue:** 20-01-PLAN.md line 19 references "20-CONTEXT D-02" which is unambiguous in context, but 20-04-PLAN.md line 134 also references "D-06 vocabulary clarification" and the issue-doc D-02 surfaces in ARCH-04 context. The D-02 identifier collision was flagged in the prior review (observation 12) but no systematic disambiguation prefix has been applied. A subagent reading "D-02" in isolation could confuse the two.
- **Suggested fix:** Consistently prefix with context source: "20-CONTEXT-D-02 (SIREN)" vs "issue-doc-D-02 (I_norm)." This is already done in 20-RESEARCH but not uniformly in the plans.

---

## Positive Findings

The following aspects of Phase 20 plans are well-executed and worth noting:

1. **Evidence-gating architecture is consistent and correct.** Every executable plan follows the same proven pattern: create evidence packet → record verdict → verdict-gated spec edit → positive surface audit → negative audit → advance ledger to VERIFIED. This is precisely the pattern established by Phases 17-19.

2. **STOP conditions are appropriately placed.** Every plan identifies the specific conditions under which source silence or contradiction should halt work and record a gap.

3. **ARCH-04 blocker is properly documented.** GAP-20-01 is correctly registered in both the phase-local gap register (20-GAPS.md) and the milestone-wide index (v1.4-GAPS.md), with all required fields filled per the STOP protocol template.

4. **D-09 "realized support" vocabulary guardrail is correctly applied.** 20-04's spec edit prose uses issue-doc language and plain descriptive wording rather than introducing "realized support" as a new technical term, consistent with the user's 2026-06-03 decision.

5. **D-10 I₃ lemma isolation is properly executed.** The conditional lemma was correctly moved from 20-03-PLAN to 20-RESEARCH to prevent anchoring bias during source-definition comparison.

6. **Source anchors verified accurate.** All cited resolution doc lines (L106, L126-128, L608-627, L659-664, L685, L1227-1234, L1435-1443) contain the content the plans claim they contain. No miscitation found.

7. **rg verification patterns are syntactically correct.** All `rg` patterns in verification steps match the actual text in current framework specs. The SI-PINN-002 exemption is correctly identified.

8. **No-live-code directive is respected everywhere.** Every plan's `must_have.truths` includes the directive, and no evidence step cites `pinn/` code as evidence.

---

## Dimension Coverage Matrix

| Dimension | Agent | Key Findings |
|-----------|-------|-------------|
| D1 — Plan-internal correctness | ce-adversarial-reviewer | M-003 (old_string imprecision), H-002 (SI-PINN-002 line fragility), M-002 (negative audit pattern gaps) |
| D2 — Cross-plan coherence | ce-coherence-reviewer | H-001 (wave labeling), M-001 (ledger merge risk), M-006 (D-02 identifier collision), H-003 (duplicate patterns) |
| D3 — Evidence-gating compliance | ce-correctness-reviewer | H-004 (M5 Step 4 under-specified), evidence template alignment confirmed |
| D4 — Source grounding | ce-correctness-reviewer | C-001 (ungrounded mass range), C-002 (I₃ definition mismatch depth) |
| D5 — Math/physics correctness | ce-adversarial-reviewer | C-001 (mass range provenance), M-004 (I₃ edge cases), ratio-form derivation verified correct |
| D6 — Governance compliance | ce-coherence-reviewer | C-003 (20-04 autonomy flag), H-005 (phase exit undefined), STOP protocol compliance confirmed |
| D7 — Subagent executability | ce-adversarial-reviewer | C-002 (I₃ fallback gap), M-005 (stale surface list), GSD routing hazard acknowledged |
| D8 — Completeness | ce-adversarial-reviewer | H-005 (ARCH-04 exit condition), all ARCH reqs covered, all 6 ledger rows handled |

---

## Comparison with Prior Review (20-plan-review-findings.md, 2026-06-03)

The prior review found: D-02 identifier collision, D-04/D-05 misdirection, implicit file-edit dependencies, Wave 1 ledger coordination gaps, I₃ definition mismatch (3-way), and ARCH-04 blocker status. All were addressed in subsequent plan revisions.

This second-pass review went deeper into mathematical claims and source provenance, finding 3 new CRITICAL issues (ungrounded numeric range, I₃ adjudication depth gap, autonomy flag error) that the first pass didn't surface. The prior review correctly identified the I₃ definition mismatch but didn't assess whether the plans' handling of that mismatch was adequate for a subagent executor.

---

## Recommended Actions

1. **Immediate (before any execution):** Resolve C-001 (mass range provenance) — either ground the numbers or replace with qualitative language.
2. **Immediate (before 20-03 execution):** Resolve C-002 (I₃ fallback path) — pre-compute the sorted-distance analysis or restructure the plan.
3. **Before 20-04 execution:** Resolve C-003 (autonomy flag) — either set `autonomous: false` or make the grounding test mechanical.
4. **Before wave dispatch:** Fix H-001 (wave labeling) and H-005 (phase exit condition).
5. **During plan refinement:** Address MEDIUM findings M-001 through M-006.

---

**Review conducted:** 2026-06-04
**Reviewer:** Claude Opus 4.8 (adversarial review framework, 3-pass methodology with 4 parallel dimension agents)
**Files reviewed:** 20-01-PLAN.md, 20-02-PLAN.md, 20-03-PLAN.md, 20-04-PLAN.md, 20-05-PLAN.md, 20-CONTEXT.md, 20-RESEARCH.md, 20-GAPS.md, 20-DISCUSSION-LOG.md
**Source documents verified:** ctl_pinn_resolution.md, 01-architecture-and-physics-foundations.md, ctl_instruction.md, pinn_architecture.md, 16-ISSUE-LEDGER.md, _TEMPLATE.md, simulation_data/Documentation/README.md, REQUIREMENTS.md, ROADMAP.md, v1.4-GAPS.md
