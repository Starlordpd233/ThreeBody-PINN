---
status: active
purpose: review-findings
created: 2026-06-14
milestone: v1.4
phase: 20-architecture-and-normalization-cleanup
retirement_trigger: Every finding below is adjudicated (addressed / superseded / not-applicable) by the user or a Phase 20 plan-remediation pass, with no open material finding remaining.
---

# Phase 20 Plan Audit — Execution-Readiness Stress Test

**Reviewer:** Claude Code (Opus 4.8), independent audit
**Date:** 2026-06-14
**Audit target:** `.planning/milestones/v1.4-phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md` … `20-05-PLAN.md` (ARCH-01…ARCH-05)
**Governing artifacts read for grounding:** `20-CONTEXT.md`, `20-GAPS.md`, evidence `_TEMPLATE.md`, `docs/git-guidelines.md`, `.githooks/`, and the post-execution `20-*-SUMMARY.md` / `20-LEARNINGS.md` / `20-VERIFICATION.md`.

---

## 1. Scope, Method, and Context

This is an **independent, forward-looking stress test** of the five Phase 20 plans, evaluating whether *another autonomous agent* — one that executes instructions literally and lacks human intuition — could run them to a flawless close. Findings are organized against the three requested dimensions:

- **Logical Integrity** — internal contradictions, procedural gaps, unverified assumptions.
- **Execution Clarity** — ambiguities and hidden consequences for a literal executor.
- **Operational Resilience** — missing/weak verification checkpoints, fragile steps, error handling.

**Two context facts the reader must hold:**

1. **Phase 20 already executed and closed cleanly.** `20-VERIFICATION.md` records all ARCH requirements PASS, and `20-LEARNINGS.md` notes "did not require any GAP entries or user escalations" with every evidence verdict landing on `accept-resolution`. **This does not exonerate the plans.** Execution succeeded *on the happy path*, run by an LLM that applied intuition to step over the defects below. The user's question — flawless execution by an intuition-free agent — targets exactly the off-happy-path and literal-execution fragilities that a clean run masks. **Most findings here are therefore latent, not historical failures.**
2. **Prior Phase 20 reviews exist but are archived** under `docs/archive/work/reviews/milestone_v1.4/20-plan-audit-legacy/` and `20-review-remediation/`. This report is a fresh independent pass, not a continuation of those, and is placed in the active `reviews/` tree per `docs/README.md`.

Every empirical claim in §3 is reproduced in the **Verification Appendix (§7)**.

---

## 2. Executive Summary

The Phase 20 plans are, on the whole, **unusually disciplined**: line-drift defense via section anchors and `rg` instead of line numbers, per-plan threat models, evidence-gating, an explicit wave/dependency DAG, and strong STOP-protocol guardrails (see §5). The defects are concentrated not in the *strategy* but in the **executable mechanics** — specifically the `rg` audit commands that constitute the verification checkpoints, and the verdict-gating control flow on the non-happy path.

| Severity | Count | Theme |
|---|---|---|
| **P0 — Critical** | 2 | Verification checkpoints that are *provably unsatisfiable or inert* as written |
| **P1 — High** | 2 | Self-contradictory verdict-gating control flow; commit blocks rejected by the active git hook |
| **P2 — Medium** | 4 | Verification weaker than it claims; concurrency hazard; noisy/ambiguous audits; unresolved placeholders |
| **P3 — Advisory** | 5 | Cognitive hazards, stale notes, vocabulary landmine, missing rollback branch |

**The two P0 findings are empirically proven** (§7) and would each cause a literal executor to either declare a false verification failure or attempt to "fix" already-correct output.

---

## 3. Prioritized Findings Index

| ID | P | Dimension | Finding (one line) | Locus |
|---|---|---|---|---|
| F1 | P0 | Resilience / Logic | Negative scheduler audit flags the plan's **own** required prose; "zero active matches" is unsatisfiable | 20-01 T2/T3; 20-02 T3 |
| F2 | P0 | Resilience | Verify regex uses `\|` (literal pipe in `rg`) → matches nothing → false failure | 20-04 T2 verify |
| F3 | P1 | Logic | Verdict-gate self-contradiction ("STOP for any non-accept" vs "fall back to Locked Convention") + Locked Convention is an EVID-05-only section the packet never creates | 20-01/20-02 T2; 20-04 T2 |
| F4 | P1 | Resilience | Raw single-line `git commit` blocks are rejected by the active commit-msg hook (body + agent trailer required; `agent-commit` mandated) | all plans, every commit step |
| F5 | P2 | Clarity | `<today>`/`<pending-commit>`/`<commit>` placeholders have no substitution rule; SHA is unknowable pre-commit | all plans, status-log steps |
| F6 | P2 | Resilience | Verification under-delivers vs. stated intent (no true before/after diff; `\in`-form blind spot; packet-completeness unchecked) | 20-01 T3; 20-03 T3; all T1 verifies |
| F7 | P2 | Resilience / Clarity | Wave-2 shared-ledger writes (20-02 & 20-03) serialized by prose only — unenforceable under parallel execution | 20-01/20-02/CONTEXT |
| F8 | P2 | Clarity | 20-04 defect-framing audit is a broad proximity regex that matches its own disclaimer prose; demands the semantic judgment the governance distrusts | 20-04 T3 Step 2 |
| F9 | P3 | Clarity | Plan-number ↔ requirement inversion (20-04→ARCH-05, 20-05→ARCH-04); pre-written prose anchors the verdict | 20-04/20-05 |
| F10 | P3 | Clarity | Stale threat-model rows warn of a `find-phase 20` hazard that CONTEXT marks RESOLVED / never-applicable | all plans |
| F11 | P3 | Clarity | "realized support" appears in `must_haves`/`objective` but is banned from spec prose (D-06/D-09) | 20-04 |
| F12 | P3 | Resilience | No explicit "audit failed → fix/revert" branch; spec is committed *before* the closure audit runs | all plans |
| F13 | P3 | Resilience | 20-04 formula-preservation pre-check is informational with no gate on a positive hit | 20-04 T2 Step 4 |

---

## 4. Detailed Findings

### P0 — Critical

#### F1 — The negative scheduler audit flags the plan's own corrected prose; its pass criterion is unsatisfiable
**Dimensions:** Operational Resilience, Logical Integrity.
**Where:** `20-01-PLAN.md` Task 2 verify (line ~180) and Task 3 Step 2 (line ~206); re-run in `20-02-PLAN.md` Task 3 Step 4 (line ~211).

The audit pattern includes `omega_0.*schedul | schedul.*omega_0 | omega0.*schedul`. The plan's own `20-01` Task 2 Step 1 instructs the executor to **write** the fixed-contract sentences:
> "`first_omega_0` is fixed at `30` and is **not scheduled** during training … There is **no epochwise or optimizer-step `omega0` scheduler**."

These sentences contain `omega_0 … scheduled` and `omega0 … scheduler`, so they **match the negative-audit pattern**. The current spec confirms it: the audit returns lines **167** and **170** (the new contract prose) in addition to the SI-PINN-002 line 998 (§7). But the pass criterion reads *"Expected: zero active/normative matches"*, whitelisting **only** the SI-PINN-002 match and stating *"Any other remaining hit must be removed or explicitly marked non-normative/historical."*

A literal executor is now trapped: lines 167/170 are required, active, normative prose that **cannot be removed** and are **not** historical. The instruction to drive the audit to "zero active matches (SI-PINN-002 excepted)" is therefore impossible to satisfy. Outcomes for an intuition-free agent: declare a false verification failure, or — worse — delete/mangle the very fixed-contract statement the phase exists to establish.

**Recommendation:** Make the negation prose explicit in the audit. Either (a) exclude absence-statements, e.g. add a follow-up filter `| rg -v "not scheduled|no .*omega0 scheduler|is not a"`, or (b) restate the criterion as "the only matches permitted are the SI-PINN-002 provenance line **and** the fixed-contract negation sentences; any match asserting an *active* scheduler fails," enumerating the allowed lines by anchor text rather than "zero matches."

---

#### F2 — `20-04` Task 2 verify uses escaped pipes (`\|`), which `rg` treats as literals → the check can never pass
**Dimensions:** Operational Resilience.
**Where:** `20-04-PLAN.md` Task 2 verify (line ~201).

The command is `rg -n "unused\|asymmetry carries\|dataset-occupied\|data-generation\|not a.*correctness\|not.*invalid normalizer" …`. ripgrep uses Rust-regex syntax, where `\|` is an **escaped literal pipe**, not alternation. The pattern therefore searches for one long literal string that does not exist in the file. Empirically (§7) this returns **exit 1 / no output**, whereas the unescaped form matches every line. The same plan's Task 3 Step 1 (line ~220) uses the **correct** unescaped `|` — so the bug is an isolated, copy-divergent regression in the Task 2 checkpoint.

Consequence: the Task 2 verify ("shows the dataset-occupancy framing for both energy and mass") will report the framing **absent even when it is present**, signalling a false failure that an intuition-free agent may "remediate" by re-editing correct prose.

**Recommendation:** Replace `\|` with `|` in the Task 2 verify command to match Task 3 Step 1.

---

### P1 — High

#### F3 — Verdict-gating control flow is self-contradictory, and the fallback points to a section that does not exist in these packets
**Dimensions:** Logical Integrity.
**Where:** `20-01-PLAN.md` Task 1 verify (line ~138) and Task 2 PRECONDITION/FALLBACK (line ~155); identical structure in `20-02-PLAN.md` (lines ~129, ~146); related in `20-04-PLAN.md` Task 2 (line ~167).

Within a single block, `20-01`/`20-02` Task 2 says both:
- **PRECONDITION:** "Apply edits ONLY IF … `accept-resolution`. **For any other verdict, STOP** and follow the gap."
- **FALLBACK:** "If a verdict is not `accept-resolution`, **derive the replacement wording from the recorded Locked Convention** … Do not apply the pre-written prose."

For the identical case (verdict ≠ `accept-resolution`) the executor is told to STOP *and* to proceed via a fallback. Compounding this, the Task 1 verify treats **any** non-`accept-resolution` verdict as requiring a `20-GAPS.md` entry + STOP — but `accept-issue-doc` / `accept-third-position` are *grounded* verdicts, not source-silence gaps. The milestone's actual STOP trigger is `defer-with-blocker` / source silence, which `20-03` and `20-05` model correctly.

The fallback is also **dangling**: the evidence `_TEMPLATE.md` marks **"Locked Convention" as REQUIRED for EVID-05 only**, and the non-EVID-05 Task 1 procedures (B-01, B-10, M8, M9, M10) never create that section. So "derive wording from the recorded Locked Convention" references a section the packet does not contain. Only the genuinely-EVID-05 plan `20-03` (M5) and `20-05` (D-02-NORM, which explicitly writes a Locked Convention) have a real fallback target.

This stayed invisible because execution hit `accept-resolution` on every finding (§1). A literal agent that drew, say, `reject-both-as-unsupported` would face a contradiction with no deterministic resolution.

**Recommendation:** Adopt the `20-03` pattern uniformly: `defer-with-blocker` (or source silence/contradiction of the locked contract) → STOP + gap; any other grounded verdict → proceed using an explicitly-created Locked Convention. Either add a "Locked Convention" authoring step to the non-EVID-05 Task 1s, or delete the FALLBACK clause and state plainly that for these findings any non-`accept-resolution` verdict is a STOP.

---

#### F4 — Every commit block violates the now-active commit-msg hook and the `agent-commit` mandate
**Dimensions:** Operational Resilience.
**Where:** the `git commit` step in every task of all five plans.

All commit steps are raw `git commit -m "<single line>"` with commit types `evidence(20)` / `spec(20)` / `verify(20)`. The repository now enforces (confirmed live, §7):
- `core.hooksPath=.githooks`; `commit-msg` → `scripts/git_policy/validate_commit_msg.py`.
- `git-guidelines.md:212` — **a body is required** for `spec`, `evidence`, `verify`, `plan`.
- `git-guidelines.md:231` — an `Agent-Assisted-By:` / `Co-Authored-By:` trailer is required.
- `git-guidelines.md:232` — agents **must** use `scripts/agent-commit`; raw agent `git commit` is disallowed.

The plans supply a single-line message with no body and no trailer, via raw `git commit`. A fresh autonomous run today would be **hook-rejected** at the first commit. (Root cause: the git-policy tooling is dated 2026-06-11, *after* Phase 20's ~06-05/06 execution — this is staleness, not original error.)

**Recommendation:** Convert each commit step to `scripts/agent-commit` with `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS` set to the plan's `files_modified`, and give each `evidence`/`spec`/`verify` message a body plus an agent trailer. This is a milestone-wide template fix, not Phase-20-specific.

---

### P2 — Medium

#### F5 — Status-log placeholders are never resolved, and the SHA is unknowable when the line is written
**Dimension:** Execution Clarity. **Where:** Task 1/3 status-log steps in all plans (e.g. `20-01` Steps 5/6, Task 3 Step 4).

Steps instruct writing `` `<today> <pending-commit> PENDING -> IN_PROGRESS …` ``. Nothing tells the executor to substitute the real date, and the short SHA is a **forward reference** — the packet is written, *then* committed in a later step, so the hash does not yet exist. A literal agent may write the placeholder text verbatim, or stall trying to resolve `<pending-commit>`. The `_TEMPLATE.md` example uses `<SHA>` but does not resolve the ordering paradox.

**Recommendation:** State the substitution explicitly ("use today's ISO date; record the SHA with a follow-up `git commit --amend`/trailer after the commit, or write `pending` and reconcile in the closure commit").

#### F6 — Verification checkpoints are weaker than their prose claims
**Dimension:** Operational Resilience. **Where:** `20-01` Task 3 Step 3; `20-03` Task 3 Step 2; Task 1 verifies across plans.

- `20-01` Task 3 Step 3 says compare snippets "before and after … not just by checking that broad strings still exist," but the provided `rg` only checks **existence** — it cannot detect a regression. The intent (diff) and the command (grep) diverge.
- `20-03` Task 3 Step 2 negative pattern `I_3 *=.*\[-1, ?1\]` catches only the `=`-annotated raw form; a LaTeX `I_3 \in [-1,1]` raw range would be **missed**.
- Task 1 verifies confirm only `rg "Verdict"` (not `-`). They never check that **Source Positions**, citations, or **Before/After** are actually populated — a packet with empty evidence sections still passes.

**Recommendation:** For regression, use a scoped `git diff` of the named anchors. Broaden the I_3 negative audit to cover `\in`. Add packet-completeness asserts (both source rows carry a `path:Lx-Ly`; required sections non-empty).

#### F7 — Wave-2 shared-ledger writes are serialized by prose only
**Dimension:** Operational Resilience / Execution Clarity. **Where:** `20-01` threat row "Ledger handoff"; `20-02` threat "Concurrent ledger write with 20-03"; `20-CONTEXT.md` coordination rules.

`20-02` and `20-03` are both wave 2 and both modify `16-ISSUE-LEDGER.md`; `20-03` also consumes `20-01`'s committed ledger state. The mitigation ("one plan's ledger commit must land before the other starts") is unenforceable from inside a plan if an orchestrator dispatches the wave in parallel. `scripts/agent-commit` serializes the *commit*, but not the read-modify-write of the shared ledger.

**Recommendation:** Either demote the ledger-writing tasks to a single serial sub-wave, or have each ledger edit re-read + append (never overwrite) and verify its own row post-commit.

#### F8 — The defect-framing negative audit is broad enough to match its own disclaimers
**Dimension:** Execution Clarity. **Where:** `20-04` Task 3 Step 2 (line ~226).

The proximity regex pairs common words (`support`, `normaliz`, `E_norm`, …) within 120 chars of `bug|error|failure|invalid|…`. The plan's own prescribed prose — "not a normalizer correctness **failure**" — matches (`normaliz … failure`). The plan acknowledges this and *requires the executor to hand-classify each hit as disclaimer vs defect* — precisely the semantic judgment the project's STOP governance instructs agents **not** to exercise unaided. Signal-to-noise is low and the outcome is judgment-dependent.

**Recommendation:** Tighten to defect-assertion phrasings, or post-filter the known disclaimer sentences, so a clean run is the expected (zero-judgment) result.

---

### P3 — Advisory

- **F9 — Number inversion & anchoring.** Plan 20-04 implements ARCH-05 and plan 20-05 implements ARCH-04; the inversion is documented but is a standing cognitive trap. Separately, embedding the exact target prose next to "use only if `accept-resolution`" creates anchoring pressure toward that verdict (mitigated by the threat models, but residual).
- **F10 — Stale threat rows.** Every plan carries a `find-phase 20 → 20.5` mis-resolution row, but `20-CONTEXT.md` (Tooling Hazard, RESOLVED 2026-06-09) states `find-phase` was never affected. Harmless redundancy, now inconsistent with context.
- **F11 — Vocabulary landmine.** `must_haves`/`objective` use "realized support" freely, while D-06/D-09 forbid it in spec prose. An executor copying acceptance language into the spec would violate the locked vocabulary; only the Task 2 caveat prevents it.
- **F12 — No failure branch + commit-before-audit.** Task 2 commits the spec edit *before* Task 3's closure audit runs; no plan defines "audit failed → fix/revert." A failed audit leaves a committed bad edit with no specified recovery.
- **F13 — Toothless safeguard.** `20-04` Task 2 Step 4 runs `git diff … | rg "^-.*(tanh|E_scale|sigma)"` to detect deleted formulas but never gates on a positive hit — the commit proceeds regardless.

---

## 5. Strengths (to preserve through any remediation)

These plans get the hard parts right; remediation should not regress them:

- **Line-drift immunity:** every surface is located by section anchor / `rg`, with quoted line numbers explicitly "orientation only." This is the single biggest reason execution survived two upstream plans shifting the same files.
- **STOP-protocol rigor:** verdict-gating, `autonomous: false` on the contested plans (20-03/20-05), and explicit gap-register routing.
- **Evidence-first structure:** every spec edit is gated behind a completed, source-cited packet and a ledger transition.
- **Explicit wave/dependency DAG and separation guardrails** (M5/`I_3` vs `I_norm`; "do not collapse M9/M10"; "do not invent an ARCH-04 vehicle").
- **`20-04` partial-blocker handling** (one of M9/M10 verified, the other deferred, AC not closed) is a model the other multi-finding plan (20-01, B-01/B-10) should copy.

---

## 6. Recommended Remediation Order

1. **F1, F2** (P0) — fix the two audit commands; they are proven-broken verification checkpoints. *Lowest effort, highest correctness payoff.*
2. **F3** (P1) — resolve the verdict-gate contradiction and the dangling Locked Convention reference by aligning 20-01/20-02/20-04 to the 20-03 pattern.
3. **F4** (P1) — re-template all commit steps onto `scripts/agent-commit` with bodies + agent trailers (milestone-wide).
4. **F5–F8** (P2) — placeholder substitution, verification hardening, ledger serialization, audit-noise reduction.
5. **F9–F13** (P3) — opportunistic cleanup; fold into the next plan-template revision.

> **Note on applicability:** Phase 20 is closed; these fixes are not required to "re-pass" it. They matter because (a) these plans are the de-facto template for evidence-gated spec cleanup in later milestones, and (b) F1/F2/F4 would block a literal re-run today. Treat this as template-hardening, not a Phase 20 re-open, unless the user directs otherwise.

---

## 7. Verification Appendix (commands run + results)

**Environment:** repo root `<home>/Desktop/3_body_problem`, 2026-06-14.

**(F2) ripgrep escaped-pipe vs alternation — PROVEN:**
```text
$ printf 'unused\nasymmetry carries\ndataset-occupied\n' > /tmp/rgtest.txt
$ rg -n 'unused\|asymmetry carries\|dataset-occupied' /tmp/rgtest.txt ; echo exit=$?
exit=1                         # escaped \| (as in 20-04 Task 2 verify) → NO MATCH
$ rg -n 'unused|asymmetry carries|dataset-occupied' /tmp/rgtest.txt ; echo exit=$?
1:unused
2:asymmetry carries
3:dataset-occupied
exit=0                         # unescaped | (as in 20-04 Task 3) → matches
```

**(F1) negative scheduler audit on the post-execution spec — PROVEN:**
```text
$ rg -ni 'update_omega0|...|omega_0.*schedul|schedul.*omega_0|dynamic[ -]schedul' pinn_architecture.md
167:    `first_omega_0` is fixed at `30` and is not scheduled during training.
170:    epochwise or optimizer-step `omega0` scheduler. If `first_omega_0` is
998:  1. "Need more detail on this dynamic scheduling for omega_0" (Section 2)
# 167 & 170 are the plan's OWN required fixed-contract prose; only 998 is the
# SI-PINN-002 line the plan whitelists. "Zero active matches" is unsatisfiable.
$ rg -n 'SI-PINN-002' pinn_architecture.md
994:### SI-PINN-002: Author comments preserved in converted body
```

**(F4) commit governance — CONFIRMED live:**
```text
$ git config --get core.hooksPath            → .githooks
$ ls .githooks/                              → commit-msg (… → scripts/git_policy/validate_commit_msg.py)
$ ls -la scripts/agent-commit                → -rwxr-xr-x … (present, dated Jun 11 22:54)
docs/git-guidelines.md:212  A body is required for `spec`, `evidence`, `verify`, and `plan` commits
docs/git-guidelines.md:231  Agent-Assisted-By: / Co-Authored-By: trailer required
docs/git-guidelines.md:232  Agents must use scripts/agent-commit; raw agent git commit disallowed
```

**(F3) Locked Convention is EVID-05-only — CONFIRMED in `_TEMPLATE.md`:**
```text
## Locked Convention
<!-- REQUIRED for EVID-05: B-02, B-04, B-09, M5, and any further source conflict. -->
This section is required before any downstream spec edit for an EVID-05 finding.
# Non-EVID-05 Task 1 procedures (B-01/B-10/M8/M9/M10) never create this section,
# yet 20-01/20-02/20-04 Task 2 FALLBACK tells the executor to read it.
```

**Execution-context cross-check** (`20-LEARNINGS.md`, `20-VERIFICATION.md`): all ARCH PASS; "did not require any GAP entries or user escalations"; M5 flagged EVID-05 but resolved to `accept-resolution`; the `autonomous: false` precaution "turned out to be unnecessary." → confirms the off-happy-path control flow (F3) and the broken audits (F1/F2) were never literally exercised.

---

## 8. Lifecycle / Governance Closeout

- **Placement:** `docs/work/reviews/milestone_v1.4/20-architecture-and-normalization-cleanup/` — finding-bearing review, integer-phase slug per `docs/README.md` §"Milestone And Phase Paths"; dated filename; full frontmatter.
- **Relationship to prior reviews:** independent of the archived `20-plan-audit-legacy/` set; no duplicate bucket created.
- **Retirement:** governed by the finding-by-finding closeout rule in `docs/README.md`; do not delete until every F-item is `addressed` / `superseded` / `not applicable` with cited evidence and no open material finding remains.
