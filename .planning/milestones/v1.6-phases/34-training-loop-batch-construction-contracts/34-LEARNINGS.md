---
phase: 34
phase_name: "training-loop-batch-construction-contracts"
project: "3-body-problem"
generated: "2026-07-02T10:50:46+00:00"
counts:
  decisions: 6
  lessons: 4
  patterns: 5
  surprises: 3
missing_artifacts: []
---

# Phase 34 Learnings: Training-Loop & Batch-Construction Contracts

## Decisions

### LOOP-01/02/03 batch-construction contract transcribed as provisional, not locked
**What was decided:** The replay/lookahead batch contract (`B_replay = 240`, `B_lookahead = 16` gated by `has_stage(k+1)`, `n_pts_cap = 32`), the two-independent-point-set contract (data-fidelity vs. collocation, `8192/4096` example budgets), and the split-status note (data-fidelity 50/50 retained, collocation 50/50 deferred) were all transcribed tagged `provisional`, consuming B-07/B-08's `modified` verdicts rather than treating them as verified optimums.
**Rationale:** The resolution doc itself marks these as modified defaults, not final-tuned values; locking them as final would overstate the evidence.
**Source:** 34-01-SUMMARY.md, 34-03-SUMMARY.md

### GAP-34-01 resolved: Option A batch edge-case policy ratified
**What was decided:** The owner ratified Option A for the three source-silent batch edge cases: final-stage training uses the replay set only (`B_lookahead = 0`); an undersized lookahead pool (<16 eligible) is padded by sampling with replacement, holding batch size fixed at 240+16; the replay set is sampled without replacement across the epoch. Options B (reservoir sampler / shrink-batch) and C were declined.
**Rationale:** The batch edge-case policy affects the effective batch distribution, curriculum convergence, and whether the final stage trains correctly at all — genuinely source-silent and consequential, so it was surfaced as a formal STOP gap rather than filled with a plausible default.
**Source:** 34-GAPS.md GAP-34-01 (RESOLVED-WITH-INSTRUCTION 2026-06-25, via AskUserQuestion during `/gsd-verify-work 34`), 34-06-SUMMARY.md

### LOOP-04 gradient-clipping split into one canonical home per half, cross-referenced
**What was decided:** The clipping mechanism (`clip_value = C_stage · median(recent global gradient norms)`, Adam-only) lives solely in `pinn_architecture.md` §4.4; the per-stage C-schedule (`7-10 / 5 / 3`) lives solely in `ctl_instruction.md`; each file points to the other via a bidirectional `AC-LOOP-04` anchor, with zero duplicated normative text and `8.5` absent from both.
**Rationale:** M14's Phase 32 verdict locked only the structural merge, not a single-file placement; splitting by natural ownership (architecture file owns the mechanism, curriculum file owns the schedule) avoids two independently-editable copies of the same fact drifting apart.
**Source:** 34-02-SUMMARY.md

### LOOP-05 ALM contract: dense-residual rejected, OFF by default, clamp deferred
**What was decided:** Dense-residual ALM is rejected from the default training loss; ALM is OFF by default; the `mu_p` clamp `[1e-4, 100]` and RMSprop-style update are carried as deferred/conditional, usable only under an optional scalar-conservation ablation once GAP-19 closes.
**Rationale:** The resolution doc's §1.18 verdict is a `defer`, not an acceptance of any specific ALM mechanics as the default training behavior.
**Source:** 34-04-SUMMARY.md, evidence/alm-mu-p-clamp.md

### SI-PINN-003 reconciled by removing a stale comment, not adding a second copy
**What was decided:** The `pinn_architecture.md` §3.1 author comment asserting a batch-construction inconsistency (already false, since `ctl_instruction.md` had become canonical) was removed, and the existing PIPE-04 note was extended into a canonical pointer rather than duplicating the ctl batch contract into pinn as a second synchronized copy.
**Rationale:** Two independently-maintained copies of the same contract are a durable source of future drift; a single canonical home plus a pointer is cheaper to keep correct.
**Source:** 34-04-SUMMARY.md

### LOOP-06/07/08 and the total-loss ordering skeleton kept explicitly opaque
**What was decided:** `dt_out`-aware collocation scaling (LOOP-06) was recorded `realized-as-deferred` with no probe-able formula; LOOP-07/08 metric roles (IPR, PSC, SASD) were carried as provisional roles with no invented weighting formula; the per-step total-loss ordering skeleton (forward → `L_total` → backward → clip → `optimizer.step()` → optional scalar-ALM) names the step sequence and forward-references Phase 35 for loss-component content, without defining any loss term itself.
**Rationale:** These are all topics the resolution doc explicitly defers or leaves to a named future phase; recording the ordering/role without the content avoids scope creep into Phase 35's territory.
**Source:** 34-03-SUMMARY.md

---

## Lessons

### A resolved gap doesn't automatically upgrade its value's confidence tier
**What was learned:** Even after GAP-34-01 was formally resolved with explicit owner instruction, the transcribed edge-case policy was tagged `provisional` (inheriting LOOP-01's status, B-07 `modified`) rather than promoted to `locked`/`verified` — resolving *which* policy to use doesn't by itself prove the policy is optimally tuned.
**Context:** Keeps the provisional/locked distinction meaningful: it tracks calibration confidence, not just "has an owner decided."
**Source:** 34-06-SUMMARY.md "Decisions Made"

### Locked-convention regression guards need "unregressed" semantics, not "must be present"
**What was learned:** Some IDs the regression guard checks for (PIPE-01/02/05/10, VAL-01) were absent even at the pre-Phase-34 baseline. Treating their absence as a failure would have been a false positive; the check had to be reinterpreted as "nothing present at HEAD was removed," not "everything must be present."
**Context:** A regression guard's job is to detect *loss* of a prior guarantee, not to assert universal presence of every referenced ID regardless of whether that ID was ever actually there.
**Source:** 34-05-SUMMARY.md "Decisions Made" / "Issues Encountered"

### Automated verify regexes can force cosmetic edits or need content-equivalent substitutes
**What was learned:** A verify check's literal pattern `7\s*[\-–—]\s*10` didn't match the existing table's double-hyphen `7--10`, requiring the table itself to be normalized to a single dash just to satisfy the check. Separately, a negative-check look-behind `(?<!deferred[^.]{0,100})` was rejected outright by Python's `re` module (fixed-width look-behind only) and had to be replaced with a content-equivalent substring check.
**Context:** Both were resolved without changing the underlying spec's meaning, but both cost an extra fix-and-recommit cycle traceable purely to the verify tooling, not the content.
**Source:** 34-02-SUMMARY.md "Issues Encountered", 34-04-SUMMARY.md "Issues Encountered"

### Deferral bodies for owner-pending mechanics should be prose contracts, not pseudocode
**What was learned:** The LOOP-05 ALM clamp/update was deliberately written as a status-tagged deferral body (prose stating the clamp bounds and conditions) rather than as a transcribed pseudocode block for the update rule.
**Context:** Pseudocode reads as implementation-ready and could be mistaken for a locked mechanism; a prose deferral body is harder to misread as settled.
**Source:** 34-04-SUMMARY.md "Decisions Made" (D-34-09)

---

## Patterns

### Cross-file single-canonical-home split with bidirectional anchors
**Pattern:** When a contract naturally has two halves that belong in different spec files (a mechanism vs. a schedule, an architecture concern vs. a curriculum concern), give each half exactly one canonical home and link the two with a shared stable anchor ID (e.g. `AC-LOOP-04`) referenced from both sides, rather than duplicating either half.
**When to use:** Any contract whose content logically spans more than one framework-spec file.
**Source:** 34-02-SUMMARY.md tech-stack patterns

### Owner-instruction-grounded transcription with explicit non-chosen-option rejection
**Pattern:** When transcribing a resolved STOP gap's ratified option into the spec, name the chosen option's mechanics exactly as ratified and explicitly state that the non-chosen options were declined — rather than only stating the positive contract and leaving the rejected alternatives implicit.
**When to use:** Any spec edit following a `RESOLVED-WITH-INSTRUCTION` gap, to prevent future drift toward one of the declined options.
**Source:** 34-06-SUMMARY.md tech-stack patterns, "Decisions Made"

### Closure-gate clearance via a dated addendum, not a rewritten verification record
**Pattern:** When a phase's verification report already recorded `passed-with-closure-gate` pending an open gap, clear the gate once the gap resolves by updating the frontmatter status/gaps-remaining fields and appending a dated addendum section — preserving the original verification body rather than rewriting it.
**When to use:** Any phase whose verification runs before all of its gaps are resolved and needs a later, narrowly-scoped update once the remaining gap closes.
**Source:** 34-06-SUMMARY.md tech-stack patterns, "Files Created/Modified"

### Name a downstream phase's content location without defining it
**Pattern:** A structural skeleton (e.g. the total-loss step ordering) can name where its opaque parts will be filled in later ("Phase 35 defines the loss components here") without attempting to guess or stub those parts.
**When to use:** Any contract that has a settled *shape* but source-deferred *content*, especially when the content is explicitly another phase's scope.
**Source:** 34-03-SUMMARY.md "What Changed"

### Status-tagged deferral body instead of pseudocode for owner-pending mechanics
**Pattern:** Represent an owner-pending mechanism (bounds, conditions, applicability) as explicit prose with status tags (`deferred`, `optional`, `conditional`) rather than as a pseudocode block that reads as implementation-ready.
**When to use:** Any mechanism whose parameters are settled in principle (e.g. a clamp range) but whose adoption into the default pipeline is still gated on a future ablation or decision.
**Source:** 34-04-SUMMARY.md "Decisions Made"

---

## Surprises

### A plan hit a protected-branch commit blocker mid-execution and stopped rather than work around it
**What was surprising:** Plan 34-03 completed all of its edits and verification checks, then discovered mid-plan that agent commits are prohibited directly on the protected `milestone/v1.6` branch — and stopped before staging or committing, leaving four ready-to-commit files in the working tree for the user rather than finding a workaround.
**Impact:** The plan's own summary is explicit that "commits not created because of protected-branch blocker" — a case of governance correctly halting an otherwise-complete plan at the very last step.
**Source:** 34-03-SUMMARY.md "Commit Blocker"

### A spec's own internal "inconsistency" comment had outlived the inconsistency it described
**What was surprising:** `pinn_architecture.md` §3.1 still carried an author comment flagging a batch-construction inconsistency with `ctl_instruction.md`, even though `ctl_instruction.md` had already become the canonical source in substance — the comment was stale prose describing a problem that had already been effectively resolved elsewhere.
**Impact:** Required an explicit removal-and-reconciliation step (SI-PINN-003) rather than a simple addition, plus reconciling a related SI-PINN-002 item to agree.
**Source:** 34-04-SUMMARY.md "Accomplishments", "Decisions Made"

### A phase's verification isn't necessarily one-shot when a live gate is attached to an open gap
**What was surprising:** Phase 34's verification report was deliberately published in a `passed-with-closure-gate` state (not a plain `passed`) while GAP-34-01 remained open, then had to be revisited and selectively re-cleared once the gap resolved — a two-stage verification lifecycle rather than the usual single verify-and-done pass.
**Impact:** Established a reusable closure-gate mechanic (see Patterns) for any future phase that must verify before every one of its gaps is closed.
**Source:** 34-05-SUMMARY.md "Decisions Made" (GAP-34-01 closure gate), 34-06-SUMMARY.md
