---
phase: 33
phase_name: "curriculum-stage-contracts"
project: "3-body-problem"
generated: "2026-07-02T10:48:53+00:00"
counts:
  decisions: 6
  lessons: 4
  patterns: 5
  surprises: 3
missing_artifacts: []
---

# Phase 33 Learnings: Curriculum-Stage Contracts

## Decisions

### CURR-01 population safeguard owner-pending, ">10%" phrasing superseded
**What was decided:** The adaptive stage-assignment methodology (offline admitted-set EDA → robust transforms → PCA → clustering → quantile threshold, augmenting the static anchors) was transcribed into `ctl_instruction.md`, but the population-safeguard threshold value itself was explicitly marked owner-pending the FUT admitted-set EDA (SCOPE-15) rather than locked at any number.
**Rationale:** The prior roadmap/`CURR-01` `>10%` phrasing was superseded, not confirmed — transcribing it as a locked floor would have invented a number the sources never settled.
**Source:** 33-01-SUMMARY.md, 33-02-SUMMARY.md "Packet-First Constraint Compliance"

### CURR-02 L_max/tau_L: characteristic scale locked, estimator kept revisable
**What was decided:** `L_max` is transcribed as the characteristic angular-momentum scale (not a proven global maximum); the Rosenstein-style `tau_L` estimator is retained as a revisable baseline; the issue-doc's shadow-trajectory method and the unspecified PCA+Rosenstein shortcut are explicitly rejected as normative.
**Rationale:** The resolution doc grounds the characteristic-scale framing and the Rosenstein baseline but leaves the final estimator, time-unit convention, fit window, and thresholds open — transcribing those as settled would exceed what the source actually decided.
**Source:** 33-02-SUMMARY.md, evidence/l-max-tau-l.md (GAP-33-02)

### CURR-02/M7: tau_L excluded from IC13 by design
**What was decided:** A canonical sentence was added stating `tau_L` is staging/evaluation metadata, trajectory-derived and not an IC invariant, used only for stage assignment and predictability-horizon evaluation — never a network input, and therefore outside the 13-component IC vector.
**Rationale:** Directly grounded in resolution doc §1.7 (`accepted`); no adjudication was required.
**Source:** 33-02-SUMMARY.md, 33-UAT.md Test #3

### CURR-03 stage transitions reconciled into one ADVANCE/RECOVER/HALT-REVIEW machine
**What was decided:** The Stage Transition Criteria section's stale pre-decision musing was removed and its existing advance-only criteria list was folded into a single coherent three-state machine (ADVANCE on the four-criterion success gate; RECOVER on NaN/Inf with bounded retry; HALT/REVIEW on max-epoch/stagnation requiring explicit owner authorization for any degraded advancement). The issue-doc's "fallback advancement" framing (treating MAX_EPOCHS/stagnation/NaN as alternate advancement triggers) was explicitly rejected.
**Rationale:** A cross-AI review pass flagged the coexistence of the old advance-only list and the new state machine as a HIGH coherence problem; reconciling rather than merely appending was required to avoid a spec that contradicts itself.
**Source:** 33-03-SUMMARY.md ("Section reconciliation" pattern, xconverge-cycle-1 HIGH coherence finding)

### CURR-05 Stage-6 gate: unsoftened geometric s_min, dual-context epsilon
**What was decided:** The Stage-6 curriculum collision gate uses unsoftened geometric `s_min` from true pairwise separations (no Plummer/additive/epsilon softening); the issue-doc's `max(s_min, epsilon)` phrasing is rejected per the PHYS-03 anti-pattern. Loss-side matched-Plummer softening is routed to Phase 35. The dual-context epsilon split (`epsilon_inv = 1e-10` offline, `epsilon_train = 1e-5` training) from Phase 32's GAP-32-02/GAP-32-03 resolutions was transcribed directly.
**Rationale:** Directly consumes the already-resolved Phase 32 owner decisions (GAP-32-02 Option A, GAP-32-03 Option A) rather than re-adjudicating them; Phase 33 only transcribes the stage-gate consequence.
**Source:** 33-03-SUMMARY.md, 33-UAT.md Test #6

### CURR-04 raw un-clipped L_norm locked, clipped stage-gate left owner-pending
**What was decided:** Raw un-clipped `L_norm` storage plus a mandatory nonfinite/near-degenerate `L_max` diagnostic-flag guard were locked into the spec; no global clamp was authorized. The `np.clip(L_norm, 0, 1)` stage-gate itself was explicitly marked NOT locked, owner-pending admitted-set evidence.
**Rationale:** GAP-33-03's resolution locked the diagnostic/storage behavior but left the actual clipping-gate decision open pending real admitted-set data — transcribing the clip as locked would have invented an unsupported default.
**Source:** 33-02-SUMMARY.md, evidence/m6-l-norm-metadata.md (GAP-33-03)

---

## Lessons

### Automated substring/negative-token checks are brittle to exact wording
**What was learned:** Multiple contract blockquotes passed their semantic intent but failed a literal-string verify check on a technicality — uppercase `**is NOT locked**` vs. the required lowercase `not locked`, and backtick-fenced `` `s_min` `` breaking a plain-substring match for `unsoftened geometric s_min`.
**Context:** Both were auto-fixed by adjusting wording without changing the underlying contract, but each required a dedicated fix-and-recommit cycle.
**Source:** 33-02-SUMMARY.md "Auto-fixed Issues" #1, 33-03-SUMMARY.md "Auto-fixed Issues" #2

### Line-number citations in plans/packets go stale within the same phase
**What was learned:** The plan and evidence packet for Plan 33-03 cited the Stage Transition Criteria section at `ctl_instruction.md:1666-1706`, but by execution time it had shifted to L1800-1840 because Plan 33-02's earlier insertions pushed later content down.
**Context:** The plan's automated checks were regex/substring-based (not line-number-based) so they remained valid; the executor located the section by heading and anchor text instead of trusting the stale line numbers.
**Source:** 33-03-SUMMARY.md "Auto-fixed Issues" #1

### A combined baseline hash can go stale for a legitimate, designed reason
**What was learned:** The Phase 33 dirty-doc baseline guard failed its literal combined-hash check not because of a real protected-path violation, but because sequential Wave 1-3 executors legitimately committed tracking writes to `STATE.md` (an expected, designed delegated write documented in the plan's own governance directive).
**Context:** Resolving this required per-document hash decomposition to prove the genuinely user-owned protected file was untouched, rather than trusting or distrusting the combined hash as a single signal.
**Source:** 33-04-SUMMARY.md "Documented divergences" #1

### Cross-AI review found the phase's own verification tooling had gaps, separate from contract correctness
**What was learned:** Cross-AI review flagged two automation-brittleness concerns (a fragile hardcoded dirty-doc guard; protected-path checks that miss untracked files) and one process concern (STOP-gap completeness is not itself enforced by any final automated check) — all about the phase's verification machinery, not about whether the transcribed contracts were correct.
**Context:** Recorded as informational UAT notes rather than contract gaps, with a recommendation to address them in Phase 36 acceptance or the next milestone's tooling.
**Source:** 33-UAT.md "Notes (informational, not UAT failures)"

---

## Patterns

### Packet-first transcription with explicit owner-pending clauses
**Pattern:** Every framework-spec contract blockquote is grounded in a prior evidence packet and states, in-place, exactly which parts are locked and which parts remain explicitly owner-pending — rather than silently omitting the undecided parts or inventing a default for them.
**When to use:** Any spec-transcription phase consuming upstream evidence-packet verdicts, especially where the upstream verdict only partially settles the topic.
**Source:** 33-01-SUMMARY.md, 33-02-SUMMARY.md "Packet-First Constraint Compliance"

### Negative-token verification alongside positive-token verification
**Pattern:** Pair "required phrase present" checks with "forbidden superseded phrase present only inside a rejection marker" checks (e.g. `D = 6.694` may appear only in a "rejected provenance" context) so a stale or contradictory phrasing can't silently coexist with the new contract.
**When to use:** Any spec edit that supersedes prior wording without deleting every occurrence of the old term (e.g. because the old term is still referenced for provenance).
**Source:** 33-02-SUMMARY.md, 33-UAT.md Test #7 "Anti-pattern scan"

### Section reconciliation over pure insertion when a stale conflicting passage exists
**Pattern:** When the spec already contains prose that would contradict a newly grounded contract (e.g. an old advance-only list vs. a new three-state machine), remove/fold the stale passage into the new contract in the same edit, rather than inserting the new contract alongside it and leaving both to coexist.
**When to use:** Any framework-spec edit phase where `read_first` review turns up a pre-existing passage that partially overlaps the new contract's subject matter.
**Source:** 33-03-SUMMARY.md tech-stack patterns, "Deviations from Plan" (xconverge-cycle-1 HIGH coherence finding)

### Name a downstream phase's ownership without defining its content
**Pattern:** When a contract's boundary touches a topic a later phase owns (e.g. Phase 34's replay/ALM, Phase 35's loss-side softening), record the handoff by name only — which phase owns it — without attempting to pre-define what that phase will decide.
**When to use:** Any phase whose spec-edit scope is deliberately narrower than the full topic area, to avoid scope creep into a later phase's adjudication.
**Source:** 33-03-SUMMARY.md tech-stack patterns "Cross-phase handoff discipline"

### Per-document hash decomposition for multi-file baseline guards
**Pattern:** When a single combined hash covers several files' diffs, decompose it per-file at verification time so a legitimate, expected change to one file (e.g. a tracking-write to STATE.md) doesn't mask real drift in — or falsely implicate — the others.
**When to use:** Any baseline/dirty-doc guard spanning more than one file where some of those files are expected to change for reasons outside the current phase's scope.
**Source:** 33-04-SUMMARY.md tech-stack patterns, "Documented divergences" #1

---

## Surprises

### A literal "should we just test it and see" musing had survived in the framework spec
**What was surprising:** The Stage Transition Criteria section still contained a pre-decision conversational aside ending in the phrase "test train stage 0 and see how it goes," sitting alongside a formal advance-only criteria list, until Phase 33 finally reconciled it into the grounded three-state machine.
**Impact:** Required an explicit removal step (not just an addition) and was specifically caught by cross-AI review as a HIGH coherence risk rather than by the plan's own original scope.
**Source:** 33-03-SUMMARY.md "What Was Built" (Stage Transition Criteria section edits)

### A "protected path" hash failure was actually a designed feature, not a violation
**What was surprising:** The combined dirty-doc baseline hash guard flagged a mismatch that looked like it could be a protected-path violation, but was in fact the expected result of the phase's own sequential Wave 1-3 executors performing designed tracking writes to `STATE.md`.
**Impact:** Required documenting the divergence honestly rather than either silently re-baselining or treating a benign, designed behavior as a failure — and per-document decomposition to prove the actually-protected file was untouched.
**Source:** 33-04-SUMMARY.md "Documented divergences" #1

### STOP-gap completeness isn't itself a verified invariant
**What was surprising:** Even in a phase built around careful gap-surfacing discipline, cross-AI review found that nothing in the phase's own final automated checks actually verifies that every STOP condition that *should* have fired *did* fire and got recorded — that remains a judgment call, not a mechanically checked property.
**Impact:** Flagged as a process concern for Phase 36 acceptance checks or the next milestone's verification tooling, rather than blocking Phase 33's own closure.
**Source:** 33-UAT.md "Notes (informational, not UAT failures)"
