---
phase: 32
phase_name: "evidence-framework-issue-ledger-conflict-adjudication"
project: "3-body-problem"
generated: "2026-07-02T10:47:23+00:00"
counts:
  decisions: 6
  lessons: 4
  patterns: 5
  surprises: 3
missing_artifacts: []
---

# Phase 32 Learnings: Evidence Framework, Issue Ledger & Conflict Adjudication

## Decisions

### D-conflict packet accepts raw-mass D ≈ 4.6416, rejects D = 6.694 / P4-1
**What was decided:** The `d-6-694-conflict.md` evidence packet recorded `accept-resolution` for the raw-mass `D ≈ 4.6416` convention and explicitly rejected the issue-doc's `D = 6.694` figure and its P4-1 rerun directive.
**Rationale:** Cross-checked against SCOPE-12, the current `ctl_instruction.md`, the v1.5 compute-globals precedent, and a first-principles dimensional-analysis check — all four agreed; GAP-17 (provenance of any artifact possibly produced under `6.694`) was kept provenance-only, not folded into this verdict.
**Source:** 32-02-SUMMARY.md "Decisions Made", 32-VERIFICATION.md Plan 32-02 Notes

### M14 packet accepts only the structural gradient-clipping merge
**What was decided:** `m14-gradient-clipping.md` recorded `accept-resolution` for the Adam-only structural merge (`clip_value = C_stage * median(recent global gradient norms)`, no L-BFGS clipping, CTL `7-10 / 5 / 3` preserved) but deliberately stopped short of the execution details (bootstrap floor, exact early-stage `C`, lower floor, history-reset mechanics) that the resolution doc leaves open.
**Rationale:** The resolution doc itself does not settle those execution details; inferring them here would have been an invented default rather than a transcription. They are routed to Phase 34 / FUT instead.
**Source:** 32-02-SUMMARY.md, 32-01-SUMMARY.md key-decisions ("Every non-headline row must get a packet ... before downstream spec edits")

### GAP-32-01 (D-04 causal-training mode) resolved: Option A ratified
**What was decided:** After being held `defer-with-blocker` through Plan 32-03, the D-04 decision was surfaced as a formal STOP-protocol gap and the user ratified Option A — retain the current per-time-step causal weighting baseline (`w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, `w_1 = 1`, `eta_c = 1`), preserve the dense-residual pseudo-ALM rejection, keep scalar-conservation ALM as deferred P2, and defer the causal-exponent clip bound to FUT.
**Rationale:** The issue doc and resolution doc both deliberately left the causal-training mode open across three materially different training-loop designs; Phase 32 could not infer a final contract from source frequency or implementation convenience.
**Source:** 32-GAPS.md GAP-32-01 (RESOLVED-WITH-INSTRUCTION 2026-06-26)

### GAP-32-02 (D-05 s_min frame) resolved: unsoftened geometric gate + matched-Plummer loss
**What was decided:** The curriculum stage gate uses unsoftened geometric `s_min` (true pairwise separations); training residual and energy use matched-Plummer softening `r_safe = sqrt(||r||^2 + epsilon_train^2)` with `epsilon_train = 1e-5`. The issue-doc's `max(s_min, epsilon)` collision-criterion phrasing was explicitly NOT adopted.
**Rationale:** A `max`/additive floor would introduce a collision-loss term absent from the specs and would violate the PHYS-03 anti-pattern (`ctl_instruction.md:1062-1067`); ratifying the existing baseline as "owner approved" without this explicit check would have silently converted "a baseline exists" into "the owner chose it."
**Source:** 32-GAPS.md GAP-32-02 (RESOLVED-WITH-INSTRUCTION 2026-06-21, via AskUserQuestion)

### GAP-32-03 (D-06 epsilon strategy) resolved: dual-context, not collapsed
**What was decided:** Offline static/invariant and data-side validation contexts retain `epsilon_inv = 1e-10`; training residual/energy retain the locked `epsilon_train = 1e-5` (matched-Plummer). Option C (`1e-10` everywhere, reopening the loss-side contract) was rejected.
**Rationale:** This is the only choice consistent with both pre-existing locks (v1.5 GAP-28-02's `epsilon_inv = 1e-10` and the loss-side `epsilon_train = 1e-5`) without reopening either; the "indistinguishable from zero" argument in `review_of_framework.md` §2.2 applies to the float32 training loop, not float64 offline ground-truth invariants.
**Source:** 32-GAPS.md GAP-32-03 (RESOLVED-WITH-INSTRUCTION 2026-06-21, via AskUserQuestion)

### Evidence machinery reused the v1.5 Phase 25 protocol instead of inventing a new schema
**What was decided:** The issue-03 evidence packet template, verdict enum, and lifecycle-status tokens were adapted directly from the verified v1.5 Phase 25 evidence framework rather than designed from scratch.
**Rationale:** Avoids an invented process-artifact schema (a MUST-surface decision class under the STOP protocol) by grounding the new machinery in a prior user-accepted analog.
**Source:** 32-01-SUMMARY.md "Decisions Made"

---

## Lessons

### Structural citation checks can require literal label strings, not just correct content
**What was learned:** The M14 and D-conflict packets cited the correct resolution-doc line ranges and section headings, but the automated citation-freshness parser required the literal strings `section 1.8` / `section 1.16` to be present — correct-but-differently-worded citations failed the check.
**Context:** Caught by Plan 32-04's structural suite; fixed by adding the literal labels without changing any semantic verdict.
**Source:** 32-04-SUMMARY.md "Auto-fixed Issues" #1, 32-VERIFICATION.md "Repair During Task 1"

### Packet wording can accidentally imply a verdict that hasn't landed yet
**What was learned:** The D-05 packet's initial wording used "ratify," which read as though the geometric stage-gate choice had already been approved — before the actual owner decision (GAP-32-02) had been surfaced and resolved. It was tightened to neutral owner-approval language during task-local verification.
**Context:** A reminder that even a `defer-with-blocker` packet's prose can leak an implied default if not phrased carefully.
**Source:** 32-03-SUMMARY.md "Auto-Fixed Issues"

### Shell mechanics can break self-check scripts independently of the content being checked
**What was learned:** Two self-check attempts failed for reasons unrelated to the artifacts under test: a zsh `path` variable name collision, then a `pipefail`/SIGPIPE interaction from piping `git log` into `rg -q`. Both were shell-mechanics failures, not content failures.
**Context:** Resolved by renaming the variable and switching to `git rev-parse --verify`; no artifacts changed because of the failed attempts.
**Source:** 32-02-SUMMARY.md "Issues Encountered"

### An ambiguous ledger column definition needed closeout clarification
**What was learned:** The issue ledger's `Owner Phase` column was ambiguous between "the phase that authored/currently holds the verdict" and "the downstream phase that will finally resolve it" until closeout explicitly defined it as the former, with downstream resolution owners tracked separately in `Dependents` and blocker text.
**Context:** Flagged as a non-critical UAT finding and resolved during Phase 32 closeout, not during the original ledger-seeding plan.
**Source:** 32-UAT.md "Non-Critical Findings"

---

## Patterns

### Baseline-before-write sentinel with closeout diff-back guard
**Pattern:** Before writing any non-baseline artifact, capture a sentinel snapshot (dirty-doc patch hash, gap-file presence, untracked-`pinn/` hash, resolution-doc identity); at closeout, diff current state back against that sentinel to prove nothing outside the plan's intended scope drifted.
**When to use:** Any multi-plan phase where several plans touch a shared machinery directory and a later plan needs to prove the earlier baseline was preserved end-to-end.
**Source:** 32-01-SUMMARY.md, 32-VERIFICATION.md "Baseline" + closeout guard rows

### Packet-before-spec-edit ledger routing with non-terminal intermediate status
**Pattern:** Require every ledger row to get an evidence packet and ledger update before any downstream phase may edit a spec on its basis; treat `FIX_APPLIED` as a non-terminal status — only `VERIFIED` or `DEFERRED` actually closes a row.
**When to use:** Any adjudication phase producing verdicts that downstream phases will transcribe into specs, where a premature "looks fixed" status could let an unverified edit propagate.
**Source:** 32-01-SUMMARY.md key-decisions

### Fixed verdict/status token vocabulary for mechanical parsing
**Pattern:** Constrain packet verdicts and ledger statuses to a small fixed enum (`accept-resolution` / `accept-issue-doc` / `accept-third-position` / `reject-both-as-unsupported` / `defer-with-blocker`; `PENDING` / `IN_PROGRESS` / `FIX_APPLIED` / `VERIFIED` / `DEFERRED`) so structural checks can parse phase state with a script instead of a judgment read.
**When to use:** Any multi-finding adjudication ledger consumed by later automated verification.
**Source:** 32-VERIFICATION.md "Verdict enum and lifecycle token preservation" check

### Two-stage gap handling: defer-with-blocker during authoring, formal STOP-gap register at closeout
**Pattern:** When a source-silent owner decision surfaces mid-phase, record it as `defer-with-blocker` in the packet/ledger immediately (without derailing the current plan), then open the formal STOP-protocol gap register as a distinct closeout-remediation step that actually surfaces the question and captures the resolution.
**When to use:** Multi-plan phases where stopping every plan individually to open a gap file would fragment the STOP-protocol paperwork; batching the formal gap-register opening into closeout keeps authoring plans focused while still guaranteeing the decision gets surfaced before the phase is considered closed.
**Source:** 32-03-SUMMARY.md ("No STOP gap file was opened" during authoring) vs. 32-GAPS.md (register opened same phase, "Task context: Phase 32 closeout remediation")

### Dual-context resolution for a numeric convention locked in two different scopes
**Pattern:** When two already-locked conventions each properly govern a different context (e.g. offline float64 diagnostics vs. training-loop float32 residuals), the correct non-reopening resolution is to keep both, distinguished explicitly by context, rather than collapsing to a single value.
**When to use:** Any numeric-convention conflict where the apparent "inconsistency" actually reflects two valid, differently-scoped locked decisions.
**Source:** 32-GAPS.md GAP-32-03 resolution note

---

## Surprises

### "No STOP gap opened" in the authoring plans, three gaps opened and resolved at closeout
**What was surprising:** Plans 32-01 through 32-04 each state "no STOP-protocol gap was opened" / "no new STOP gap file was opened," yet the phase's own `32-GAPS.md` register (opened the same day) contains three real gaps (D-04/D-05/D-06), two resolved same-day via AskUserQuestion and one resolved five days later (2026-06-26).
**Impact:** Reading only the plan summaries would incorrectly suggest the phase never invoked the STOP protocol; the actual gap-surfacing happened in a distinct "closeout remediation" pass not visible from the four plan SUMMARY.md files alone.
**Source:** 32-03-SUMMARY.md / 32-04-SUMMARY.md ("no STOP gap") vs. 32-GAPS.md (three RESOLVED-WITH-INSTRUCTION entries)

### Option-letter labels didn't match across source documents
**What was surprising:** For D-06, the gap register's Option A was the same substantive choice as the issue doc's Option B — the letters didn't line up between the two documents even though the underlying option was identical.
**Impact:** Required resolving by matching on the option's description rather than trusting the letter alone, to avoid silently picking the wrong labeled option.
**Source:** 32-GAPS.md GAP-32-03 resolution note ("the option-letter mismatch is resolved by the description, not the letter")

### A routine epsilon-strategy question surfaced a real, quantified train/validate discrepancy
**What was surprising:** Resolving the seemingly administrative D-06 epsilon-context question surfaced that the training-loss softening (`epsilon_train`) and the offline validation softening (`epsilon_inv`) actually diverge by roughly 0.5–30% at the tightest encounters (`r ≤ ~1e-4`), bounded to the Stage-6 tail.
**Impact:** Logged as a non-blocking FUT/trainex validation follow-up (confirm the train-vs-validate mismatch is negligible on the admitted set) rather than reopening either locked convention.
**Source:** 32-GAPS.md GAP-32-03 resolution note "Known caveat (no blocker)"
