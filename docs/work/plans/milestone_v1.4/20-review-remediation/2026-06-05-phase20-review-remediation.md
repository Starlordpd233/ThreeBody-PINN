---
status: consumed
purpose: other
created: 2026-06-05
milestone: v1.4
phase: 20-review-remediation
retirement_trigger: milestone complete; superseded by subsequent work
---

# Phase 20 Review Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Revise the Phase 20 planning documents so the review-report findings are addressed without inventing source-silent physics, schema, or adjudication decisions.

**Architecture:** This is a documentation and planning remediation pass. It updates canonical Phase 20 context, plan frontmatter, task instructions, verification gates, and blocked-work handling; it does not execute Phase 20 spec edits, create evidence packets, or resolve semantic gaps. Where review reports conflict, use the stricter safe rule: no numeric range unless grounded under the v1.4 formula, no hardcoded `I_3` accept-resolution closure, and no new ledger or evidence schema without a grounded source or user instruction.

**Tech Stack:** Markdown planning artifacts, YAML frontmatter, Phase 16 evidence workflow, shell verification with `rg`, `sed`, and `git diff --check`.

---

## Source Review Inputs

Read these review reports before editing:

- `docs/archive/work/reviews/milestone_v1.4/20-plan-audit-legacy/20-plan-review-comprehensive.md`
- `docs/archive/work/reviews/milestone_v1.4/20-plan-audit-legacy/phase20-deep-adversarial-review-v2-2026-06-04.md`
- `docs/archive/work/reviews/milestone_v1.4/20-plan-audit-legacy/2026-06-04-phase20-comprehensive-review.md`
- `docs/archive/work/reviews/milestone_v1.4/20-plan-audit-legacy/20-plan-review-findings.md`
- `docs/archive/work/reviews/milestone_v1.4/20-plan-audit-legacy/20-plan-deep-adversarial-review-2026-06-04.md`
- `docs/archive/work/reviews/milestone_v1.4/20-plan-audit-legacy/phase20-review.md`

The reports disagree on severity. Treat the following as mandatory remediation:

- `20-03-PLAN.md` must not hardcode accept-resolution values (`[0, 1/3]`, `6 I_3 - 1`) in Task 3 or closure proof; it must audit against the M5 Locked Convention.
- `20-04-PLAN.md` must not pre-insert `[-0.93, 0.585]` unless the future M10 packet grounds that range under the v1.4 mass-normalization formula; default to qualitative wording.
- `20-02-PLAN.md` and `20-03-PLAN.md` must serialize shared `16-ISSUE-LEDGER.md` writes.
- `20-CONTEXT.md` must carry canonical labels for D-09, D-10, and D-11 because `20-DISCUSSION-LOG.md` says execution decisions live in context.
- `ARCH-04` must remain blocked by `GAP-20-01`; no remediation task may invent its proof vehicle or attach it to M5.

## File Structure / Responsibility Map

**Modify:**

- `.planning/phases/20-architecture-and-normalization-cleanup/20-CONTEXT.md` — canonical decisions, execution coordination, and phase-exit guardrails.
- `.planning/phases/20-architecture-and-normalization-cleanup/20-DISCUSSION-LOG.md` — audit note for this review-remediation pass.
- `.planning/phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md` — SIREN plan executability hardening and severity-rationale text.
- `.planning/phases/20-architecture-and-normalization-cleanup/20-02-PLAN.md` — LayerNorm plan ledger coordination and M8 conditional branch-scope wording.
- `.planning/phases/20-architecture-and-normalization-cleanup/20-03-PLAN.md` — M5 adjudication neutrality, fallback completeness, and audit commands.
- `.planning/phases/20-architecture-and-normalization-cleanup/20-04-PLAN.md` — mass-range grounding, mechanical autonomy guard, wave label, audit gates, and AC-ARCH-05 partial-blocker wording.
- `.planning/phases/20-architecture-and-normalization-cleanup/20-05-PLAN.md` — ARCH-04 blocked exit and re-audit instructions.
- `.planning/phases/20-architecture-and-normalization-cleanup/20-GAPS.md` — only if a remediation step creates or resolves an actual gap per STOP protocol.
- `.planning/milestones/v1.4-GAPS.md` — only if `20-GAPS.md` changes.

**Do not modify during this plan:**

- `pinn_instruction/markdown_conversion/framework-specs/*.md`
- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/*.md`
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`
- `pinn/`
- `.planning/phases/20-5-sampling-coordinate-allocation/`

## Global STOP Rules

- Semantic gap: stop dependent work, record the gap in `20-GAPS.md`, update `v1.4-GAPS.md`, surface to the user.
- Process-schema gap: do not invent new evidence packets, ledger statuses, acceptance checks, partial statuses, or shared protocol documents.
- Operational coordination: keep changes minimal and factual. Record the decision in `20-DISCUSSION-LOG.md`; if it changes plan orchestration semantics beyond serializing shared-file writes, record a `20-GAPS.md` operational-coordination gap and wait for user instruction.
- Live code in `pinn/` is not grounding evidence.

### Task 1: Preflight and Review Ledger

**Files:**

- Read: `docs/archive/work/reviews/milestone_v1.4/20-plan-audit-legacy/*.md`
- Read: `.planning/phases/20-architecture-and-normalization-cleanup/*.md`

- [ ] **Step 1: Confirm git state before edits**

Run:

```bash
cd <home>/Desktop/3_body_problem
git status --short --branch
```

Expected: current branch is visible. If the branch name is red-flagged (`backup`, `recovery`, `wip`, `experiment`, `tmp`) or the worktree contains unrelated edits in the Phase 20 files, stop and ask the user before editing.

- [ ] **Step 2: Confirm review-report inventory**

Run:

```bash
cd <home>/Desktop/3_body_problem
rg --files docs/archive/work/reviews/milestone_v1.4/20-plan-audit-legacy | sort
```

Expected: the six review reports listed in `Source Review Inputs` are present.

- [ ] **Step 3: Create a local remediation ledger in the executor notes**

Use this exact grouping while editing; do not write it as a new repo artifact:

```markdown
P0 STOP-controlled:
- ARCH-04 blocked by GAP-20-01; preserve block and phase-exit warning.
- M5/I_3 must stay verdict-neutral; audit against M5 Locked Convention.
- M10 mass range must be qualitative unless v1.4 formula grounding exists.
- No new ledger status, AC, packet, or shared evidence protocol without user instruction.

High/medium remediation:
- Add D-09/D-10/D-11 to canonical 20-CONTEXT.
- Serialize 20-02/20-03 ledger writes and move 20-04 to wave 3.
- Harden 20-04 audit commands and mechanical autonomy guard.
- Add severity-rationale text to B-01/B-10, M8, M9/M10 instructions.
- Harden 20-01/20-02 exact edit boundaries and SI-PINN-002 exception language.

Cleanup:
- Update status and traceability notes only when they do not change semantics.
- Record out-of-scope source/spec observations as follow-ups, not Phase 20 scope.
```

### Task 2: Canonical Context and Coordination Rules

**Files:**

- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-CONTEXT.md`
- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-DISCUSSION-LOG.md`

- [ ] **Step 1: Add D-09 through D-11 to `20-CONTEXT.md`**

In `20-CONTEXT.md`, insert this block inside `<decisions>` after D-08:

```markdown
### D-09: "Realized Support" Is Planning Shorthand, Not Spec Vocabulary

Named restatement of the existing D-06 vocabulary clarification, recorded as a labeled decision for traceability (review reports referenced it by label). "Realized support" remains planning/acceptance shorthand only: it labels the ARCH-05 objective in Phase 20 context, the Phase 16 ledger, and the roadmap success criterion, but it is not a new technical term for the framework specs; spec prose uses issue-doc language or plain descriptive wording. Source of record: 20-CONTEXT D-06 "Vocabulary clarification (user decision 2026-06-03)"; see also `20-DISCUSSION-LOG.md` Deep Review Decision D-09.

### D-10: I_3 Derivation Lives in Research Until Source Definitions Match

The ratio-form `I_3` derivation belongs in `20-RESEARCH.md` as a conditional lemma. A Phase 20 executor may consult it only after comparing the source definitions, ranges, and mappings in M5. If the issue doc uses a genuinely different `I_3` object, the ratio-form lemma must not be treated as verdict evidence for that object. Source: `20-DISCUSSION-LOG.md` Deep Review Decision D-10.

### D-11: 20-04 Autonomy Requires a Mechanical Grounding Gate

Plan 20-04 may remain `autonomous: true` because M9/M10 are not EVID-05 contested and D-11 records a deterministic safe default for ungrounded numeric ranges: record a `20-GAPS.md` entry, halt the affected Task 2 work, and surface the decision to the user. D-06 is the source for spec-safe plain descriptive wording when numeric support ranges are not explicitly grounded; if even qualitative/plain-language framing cannot be grounded, use the D-11 STOP path before editing. Sources: `20-DISCUSSION-LOG.md` Deep Review Decision D-11 for autonomy/safe-default handling; `20-CONTEXT.md` D-06 for issue-doc/plain-language support wording.
```

- [ ] **Step 2: Add execution coordination rules to `20-CONTEXT.md`**

After `</decisions>` and before `<canonical_refs>`, insert:

```markdown
<execution_coordination>
## Execution Coordination Rules

- `20-02` and `20-03` both write `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`. If the plans are implemented with parallel workers, their ledger-write tasks must be serialized: one worker must complete and commit its ledger update before the other begins its ledger update.
- `20-04` depends on both `20-02` and `20-03`; treat it as wave 3 for execution ordering even if older review notes describe it as wave 2.
- Phase 20 may execute the non-ARCH-04 plans while `GAP-20-01` is open, but the milestone must not be marked fully complete while `ARCH-04` remains OPEN. Full closure requires `GAP-20-01` to be `RESOLVED-WITH-INSTRUCTION` or `DEFERRED` by user instruction. Phase 20 may report ARCH-01/02/03/05 closed with ARCH-04 blocked; a downstream phase that "Depends on Phase 20" may proceed on the four closed ACs but must treat ARCH-04 as an explicit open carry-forward, not silently satisfied.
</execution_coordination>
```

- [ ] **Step 3: Add a remediation note to `20-DISCUSSION-LOG.md`**

Append this section before `## the agent's Discretion`:

```markdown
---

## Review Remediation Decisions (2026-06-05)

The review reports in `docs/archive/work/reviews/milestone_v1.4/20-plan-audit-legacy/` disagree on several severities. The remediation rule is to prefer the stricter safe path where disagreement affects grounding:

- M5 / `I_3`: Task and closure wording must reference the M5 Locked Convention, not hardcoded accept-resolution values.
- M10 / mass support: no hardcoded numeric range enters plan prose unless the future M10 packet grounds that range under the v1.4 formula; otherwise use qualitative wording.
- 20-04 autonomy: keep the plan autonomous only with a mechanical grounding gate and a STOP fallback.
- Wave coordination: serialize shared `16-ISSUE-LEDGER.md` writes by execution rule rather than redefining evidence semantics.
```

- [ ] **Step 4: Verify context additions**

Run:

```bash
cd <home>/Desktop/3_body_problem
rg -n "D-09|D-10|D-11|execution_coordination|Review Remediation Decisions" .planning/phases/20-architecture-and-normalization-cleanup/20-CONTEXT.md .planning/phases/20-architecture-and-normalization-cleanup/20-DISCUSSION-LOG.md
```

Expected: D-09, D-10, D-11, `execution_coordination`, and `Review Remediation Decisions` are present.

### Task 3: Repair `20-03-PLAN.md` I_3 Neutrality

**Files:**

- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-03-PLAN.md`

- [ ] **Step 1: Strengthen Task 1 Step 4 source-definition comparison**

Find `**Step 4: Definition/range/mapping comparison before physics.**` and ensure it contains this sentence:

```markdown
If the issue doc and resolution/current spec define different mathematical objects, record `defer-with-blocker` unless the cited sources plus a short first-principles check explicitly ground one locked convention; do not convert a sorted-distance convention into the ratio-form convention by assumption.
```

- [ ] **Step 2: Strengthen Task 2 fallback**

In Task 2, under the verdict-gated precondition/fallback paragraph, add:

```markdown
For every non-`accept-resolution` verdict, the M5 Locked Convention must contain spec-ready replacement prose for each surface this task edits. If the Locked Convention does not contain spec-ready prose, STOP, record a `20-GAPS.md` entry, update `.planning/milestones/v1.4-GAPS.md`, and surface to the user instead of improvising.
```

- [ ] **Step 3: Replace Task 3 hardcoded positive audit wording**

Replace the current Task 3 Step 1 positive-audit sentence with:

```markdown
- [ ] **Step 1: Positive surface audit.** Confirm every active `I_3` range/mapping surface matches the recorded M5 Locked Convention: raw range, staging/input map, and metadata-only framing must all match the convention recorded in M5.md Task 1.
```

- [ ] **Step 4: Replace the negative audit command so it does not flag the correct mapped range**

Replace the current Task 3 Step 2 command block with a regex that matches the **raw assignment form** (`I_3 = … ∈ [-1, 1]`) but not the legitimate `I_3^{\mathrm{in}}` mapped range. (The prior `raw`/`formula` keyword regex matched nothing — the spec line carries neither word — so the audit was vacuous.)

```bash
rg -n "I_3 *=.*\[-1, ?1\]" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
```

Expected text below the command:

```markdown
Expected: no match. This pattern matches only a raw `I_3 = (…)` annotation `∈ [-1, 1]`; it does NOT match the staging map `I_3^{\mathrm{in}} = 6 I_3 - 1` (whose `[-1, 1]` is the correct mapped range, since `I_3` there is followed by `^{...}`, not `=`). A match means the Step 1 raw-range edit was missed. As a backstop, also eyeball the Step 1 positive-audit output.
```

- [ ] **Step 5: Replace Closure Proof hardcoding**

In `## Closure Proof for AC-ARCH-03`, replace the parenthetical `raw [0, 1/3], staging map 6 I_3 − 1, metadata-only` with:

```markdown
raw range, staging/input map, and metadata-only scope all matching the recorded M5 Locked Convention
```

- [ ] **Step 5b: Fix the stale wave reference in 20-03 Architecture**

Because Task 4 moves `20-04` to `wave: 3`, update the `20-03-PLAN.md` Architecture sentence that reads "plan 20-04 (energy/mass support) edits the same file in wave 2 and depends on this plan" to say **wave 3** instead of wave 2.

- [ ] **Step 6: Verify no hardcoded accept-resolution audit remains**

Run:

```bash
cd <home>/Desktop/3_body_problem
rg -n "raw \\[0, 1/3\\]|6 I_3|6·I_3|6 I₃|6·I₃" .planning/phases/20-architecture-and-normalization-cleanup/20-03-PLAN.md
```

Expected: the accept-resolution values may appear inside Task 1's `accept-resolution` example convention (Steps 8 and 10) **and** inside Task 2's accept-resolution pre-written prose (Steps 1–2, which the FALLBACK gates to the accept-resolution verdict only). They must NOT appear in Task 3's audit commands or in the Closure Proof — those reference the recorded M5 Locked Convention instead.

### Task 4: Repair `20-04-PLAN.md` Mass-Range, Autonomy, Wave, and Audit Gates

**Files:**

- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-04-PLAN.md`

- [ ] **Step 1: Change the wave label**

In frontmatter, change:

```yaml
wave: 2
```

to:

```yaml
wave: 3
```

Keep `depends_on: ["20-02", "20-03"]`.

- [ ] **Step 2: Make the autonomy guard explicit in frontmatter truths**

Add this truth under `must_haves.truths`:

```yaml
    - "20-04 remains autonomous only because the M9/M10 grounding gate is mechanical: unsupported numeric ranges are replaced with qualitative wording or STOP-gapped before any edit."
```

- [ ] **Step 2b: Reconcile the `realized` artifact check with D-09**

The `20-04` frontmatter artifact for `ctl_instruction.md` asserts `contains: "realized"`, which contradicts D-09 and the Task 2 PRECONDITION (do not introduce "realized" into the spec). A correctly-executed plan that keeps "realized" out of the spec would then fail its own artifact gate. Change that artifact line from `contains: "realized"` to `contains: "asymmetry carries"` (a plain-language token the new occupancy prose actually contains). Also reword the `must_haves.truths` D-06 entry that says ranges are "framed as realized support" to "framed as dataset-occupied support in plain descriptive wording (not the planning term 'realized')".

- [ ] **Step 3: Harden the M10 Before/After note in Task 1 Step 3**

In Task 1 Step 3 the `Before / After Spec Note` describes the asymmetric hierarchical `m_norm` range but states no numeric — the numeric `[-0.93, 0.585]` lives in Task 2 Step 2 and is removed by Step 4 below. Replace that asymmetry sentence with:

```markdown
Complete `Before / After Spec Note` (before: ordered-mass normalization with no documentation of asymmetric hierarchical range; after: hierarchical `m_norm` range is asymmetric, that asymmetry carries mass hierarchy information, and no numeric range is stated unless the M10 packet explicitly grounds it under the v1.4 `tanh((m_i - mu)/(sigma+1e-8))` formula with citations).
```

- [ ] **Step 4: Replace the pre-written mass prose in Task 2 Step 2**

Replace the current mass prose block with:

```markdown
The mass slots are normalized per slot with dataset-wide statistics. For
hierarchical ICs, the dataset-occupied `m_norm` range is asymmetric; this
asymmetry carries mass hierarchy information and is not a centering or
correctness failure. Do not state a numeric range here unless M10.md grounds
that range under the v1.4 `tanh((m_i - mu)/(sigma+1e-8))` formula with
source and dataset citations.
```

- [ ] **Step 5: Replace the no-op formula-change guard**

Replace the command:

```bash
git diff -- pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md | rg "tanh|E_scale" || true
```

with a guard that inspects only **removed/modified** formula lines (this plan only ADDS occupancy prose, which may legitimately mention `tanh`, so a `+`-line matcher would false-positive on the plan's own intended prose):

```bash
git diff -- pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md | rg -n "^-.*(tanh|E_scale|sigma)"
```

Expected text below the command:

```markdown
Expected: no output. Any `-` (removed/changed) line touching a normalization formula or `E_scale` means this plan altered a formula rather than only adding prose — investigate before committing. New `+` prose that mentions a formula is allowed and is intentionally not flagged.
```

- [ ] **Step 6: Remove `realized` from spec-audit search patterns and broaden the defect audit**

Where the plan audits spec prose with a pattern containing `realized|support|occupied|data-generation`, replace it with:

```bash
rg -n "unused|asymmetry carries|dataset-occupied|data-generation|not a.*correctness|not.*invalid normalizer" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
```

Expected: the audit searches for issue-doc/plain-language framing, not the planning shorthand term `realized`.

Also replace `20-04-PLAN.md` Task 3 Step 2's negative-audit command with a proximity audit that catches defect phrasing such as `incorrect`, `problem`, and `flawed` as well as the original bug/error/failure vocabulary:

```bash
rg -ni "(one-sided|asymmet|degenerate|support|normaliz|normalizer|E_norm|m_norm).{0,120}(bug|error|failure|invalid|incorrect|problem|flawed|defect|should be symmetric|must be positive)|(bug|error|failure|invalid|incorrect|problem|flawed|defect|should be symmetric|must be positive).{0,120}(one-sided|asymmet|degenerate|support|normaliz|normalizer|E_norm|m_norm)" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
```

Expected: zero matches that characterize M9/M10 support occupancy/asymmetry as a normalization defect. Negating/disclaiming matches such as `not an invalid normalizer` are allowed only if quoted in the packet audit notes with a sentence explaining why they are disclaimers rather than defect claims.

- [ ] **Step 7: Make partial-blocker handling schema-safe**

Replace Task 3 Step 3 partial-blocker wording with:

```markdown
- [ ] **Step 3: Partial-blocker handling.** If only one of M9/M10 reaches `VERIFIED`, record audit proof only for the completed packet, leave the other packet and ledger row in its existing Phase 16-supported blocked/deferred state, and do NOT close `AC-ARCH-05`. Do not invent a partial AC status or a new ledger status.
```

- [ ] **Step 8: Clarify out-of-scope `pinn_architecture.md` audit**

In the threat model or Task 2 Step 3, ensure this sentence exists:

```markdown
If the read-only `pinn_architecture.md` audit finds defect-framing text that 20-04 does not own, record a follow-up in the M9/M10 packet notes or a Phase 20 gap; do not edit `pinn_architecture.md` from 20-04.
```

- [ ] **Step 9: Verify 20-04 hardening**

Run:

```bash
cd <home>/Desktop/3_body_problem
sed -n '1,18p' .planning/phases/20-architecture-and-normalization-cleanup/20-04-PLAN.md
! rg -n "\\[-0\\.93, 0\\.585\\]|\\|\\| true|HALF[_ -]?VERIFIED|PARTIAL[_ -]?VERIFIED" .planning/phases/20-architecture-and-normalization-cleanup/20-04-PLAN.md
rg -n "unused|asymmetry carries|dataset-occupied|data-generation|not a.*correctness|not.*invalid normalizer" .planning/phases/20-architecture-and-normalization-cleanup/20-04-PLAN.md
```

Expected: `wave: 3` is present; the strict no-match command succeeds with no output; the prose-audit command finds plain-language dataset-occupancy framing. The literal word `realized` may remain in planning context, objective, or packet titles, but not as a required spec-prose search term.

### Task 5: Harden `20-01-PLAN.md` and `20-02-PLAN.md`

**Files:**

- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md`
- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-02-PLAN.md`

- [ ] **Step 1: Qualify the SIREN scheduler truth in `20-01-PLAN.md`**

In `20-01-PLAN.md`, replace any truth or audit expectation that says no scheduler guidance remains anywhere with:

```markdown
No active/normative epochwise or optimizer-step `omega0` scheduler guidance remains. Historical or SI-PINN-002 non-normative discussion may remain only if explicitly labeled as non-normative and excluded from the implementation contract.
```

- [ ] **Step 2: Strengthen B-01/B-10 severity rationale (do NOT add Step 1a/1b)**

In the real `20-01-PLAN.md`, B-01 is already Task 1 Steps 1–5 and B-10 is Task 1 Step 6 — they are separate steps, so do NOT introduce Step 1a/1b (that would collide with the existing Step 2–6 bodies and would not enable parallel dispatch). Instead, replace the generic `Add a brief Severity Rationale …` sentence in the existing **Step 1** (B-01) and **Step 6** (B-10) with explicit keep-or-escalate rationale:

- In Step 1 (B-01): `Severity Rationale: Issue-doc B-01 was originally BLOCKING because the framework spec could mislead implementers; Phase 20 records MINOR only if the evidence packet verifies this pass is documentation/spec cleanup of an already locked target contract, not a model-behavior change. If that rationale is not source-grounded, keep or escalate the issue-doc severity before continuing.`
- In Step 6 (B-10): `Severity Rationale: Issue-doc B-10 concerns dynamic scheduling ambiguity; Phase 20 records MINOR only if the evidence packet verifies the target is documentation/spec cleanup that removes non-locked scheduler guidance while preserving stage-boundary ablation language. If that rationale is not source-grounded, keep or escalate the issue-doc severity before continuing.`

Optional (not required for this remediation): if parallel dispatch of B-01 and B-10 is wanted, lift B-10 (Step 6) into its own Task 1b mirroring `20-04`'s two-packet structure — that is a structural change to `20-01`, so make it only on explicit request.

- [ ] **Step 3: Add ledger serialization to `20-02-PLAN.md`**

In `20-02-PLAN.md` threat model, add:

```markdown
| Concurrent ledger write with 20-03 | HIGH | `20-02` and `20-03` both update `16-ISSUE-LEDGER.md`; serialize ledger-write tasks and commits. One plan's ledger commit must land before the other starts its ledger update. |
```

- [ ] **Step 4: Make 20-02 Task 2 Step 1 conditional on M8 support**

In `20-02-PLAN.md` Task 2 Step 1, ensure the branch-scope replacement includes:

```markdown
Apply skip/power-branch scope wording only if M8's recorded verdict explicitly supports that scope. If M8 grounds `elementwise_affine=False` but not branch scope, record the branch-scope uncertainty in `20-GAPS.md` and avoid inserting unsupported branch-specific prose.
```

- [ ] **Step 5: Add M8 severity rationale**

In `20-02-PLAN.md` Task 1 Step 1, replace the short severity-rationale instruction with:

```markdown
Severity Rationale: `Issue-doc M8 is MAJOR because attribution/default ambiguity can mislead architecture implementation. Phase 20 records MINOR only if the M8 evidence packet verifies this pass is documentation/spec cleanup of a locked LayerNorm contract, not a new architecture decision. If that rationale is not source-grounded, keep or escalate the issue-doc severity before continuing.`
```

- [ ] **Step 5b: De-duplicate the 20-02 omega regression check (orthogonal cross-validation)**

In `20-02-PLAN.md` Task 3 Step 4 (the SIREN regression re-check), add orthogonal verification so a false-negative in `20-01`'s exact `omega0` pattern is not silently inherited by re-running the identical pattern:

```markdown
Also run `rg -ni "schedul" pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` and manually confirm every hit is either absent or explicitly non-normative (SI-PINN-002). Do not rely solely on re-running 20-01's exact omega-specific pattern.
```

- [ ] **Step 6: Verify 20-01 and 20-02 hardening**

Run:

```bash
cd <home>/Desktop/3_body_problem
rg -n "SI-PINN-002|non-normative|Severity Rationale" .planning/phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md
! rg -n "Step 1a|Step 1b" .planning/phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md
rg -n "Concurrent ledger write with 20-03|branch-scope uncertainty|Issue-doc M8 is MAJOR" .planning/phases/20-architecture-and-normalization-cleanup/20-02-PLAN.md
```

Expected: `SI-PINN-002`, `non-normative`, and `Severity Rationale` are present in `20-01-PLAN.md`; `Step 1a`/`Step 1b` are absent; the `20-02-PLAN.md` phrases are present.

### Task 6: Preserve ARCH-04 Block and Phase Exit Semantics

**Files:**

- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-05-PLAN.md`
- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-GAPS.md` only if status/counts change
- Modify: `.planning/milestones/v1.4-GAPS.md` only if `20-GAPS.md` changes

- [ ] **Step 1: Add a post-20-03/20-04 re-audit warning to `20-05-PLAN.md`**

Under `Current-spec surfaces to audit once unblocked`, add:

```markdown
- Re-run this surface audit after 20-03 and 20-04 complete because both plans edit `ctl_instruction.md`. Do not rely only on the 2026-06-03 surface list.
```

- [ ] **Step 2: Preserve exact ARCH-04 block language**

Ensure `20-05-PLAN.md` still contains:

```markdown
ARCH-04 is SEPARATE from M5/ARCH-03. M5 adjudicates the `I_3` range/mapping; ARCH-04 concerns raw-vs-bounded `I_norm` naming. Do not conflate.
```

- [ ] **Step 3: Do not change `GAP-20-01` status without user instruction**

Run:

```bash
cd <home>/Desktop/3_body_problem
rg -n "GAP-20-01|Status: OPEN|total_gaps|open_gaps|resolved_gaps" .planning/phases/20-architecture-and-normalization-cleanup/20-GAPS.md .planning/milestones/v1.4-GAPS.md
```

Expected: `GAP-20-01` remains OPEN unless the user has explicitly resolved or deferred it in this execution session.

- [ ] **Step 4: Verify 20-05 re-audit and block**

Run:

```bash
cd <home>/Desktop/3_body_problem
rg -n "Re-run this surface audit after 20-03 and 20-04|ARCH-04 is SEPARATE|Do not conflate" .planning/phases/20-architecture-and-normalization-cleanup/20-05-PLAN.md
```

Expected: all phrases are present.

### Task 7: Final Verification and Commit

**Files:**

- Review all modified files from Tasks 2 through 6.

- [ ] **Step 1: Run the combined verification suite**

Run:

```bash
cd <home>/Desktop/3_body_problem
rg -n "D-09|D-10|D-11|execution_coordination" .planning/phases/20-architecture-and-normalization-cleanup/20-CONTEXT.md
rg -n "raw \\[0, 1/3\\]|6 I_3|6·I_3|6 I₃|6·I₃" .planning/phases/20-architecture-and-normalization-cleanup/20-03-PLAN.md
! rg -n "\\[-0\\.93, 0\\.585\\]|\\|\\| true|HALF[_ -]?VERIFIED|PARTIAL[_ -]?VERIFIED" .planning/phases/20-architecture-and-normalization-cleanup/20-04-PLAN.md
rg -n "Concurrent ledger write with 20-03|SI-PINN-002|branch-scope uncertainty|Re-run this surface audit" .planning/phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md .planning/phases/20-architecture-and-normalization-cleanup/20-02-PLAN.md .planning/phases/20-architecture-and-normalization-cleanup/20-05-PLAN.md
git diff --check
```

Expected:

- Context labels and coordination rules are present.
- `20-03` accept-resolution values appear only in the explicit accept-resolution example convention, not in closure proof or Task 3 audit expectations.
- `20-04` contains no `[-0.93, 0.585]`, no `|| true` verification gate, and no invented partial AC status.
- `20-01`, `20-02`, and `20-05` contain the hardening phrases.
- `git diff --check` reports no whitespace errors.

- [ ] **Step 2: Manually review the diff for scope**

Run:

```bash
cd <home>/Desktop/3_body_problem
git diff -- .planning/phases/20-architecture-and-normalization-cleanup/20-CONTEXT.md \
           .planning/phases/20-architecture-and-normalization-cleanup/20-DISCUSSION-LOG.md \
           .planning/phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md \
           .planning/phases/20-architecture-and-normalization-cleanup/20-02-PLAN.md \
           .planning/phases/20-architecture-and-normalization-cleanup/20-03-PLAN.md \
           .planning/phases/20-architecture-and-normalization-cleanup/20-04-PLAN.md \
           .planning/phases/20-architecture-and-normalization-cleanup/20-05-PLAN.md
```

Expected: the diff contains only planning-document remediation. There are no framework-spec edits, evidence-packet edits, live-code edits, or Phase 20.5 edits.

- [ ] **Step 3: Commit the remediation**

Run:

```bash
cd <home>/Desktop/3_body_problem
git add .planning/phases/20-architecture-and-normalization-cleanup/20-CONTEXT.md \
        .planning/phases/20-architecture-and-normalization-cleanup/20-DISCUSSION-LOG.md \
        .planning/phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md \
        .planning/phases/20-architecture-and-normalization-cleanup/20-02-PLAN.md \
        .planning/phases/20-architecture-and-normalization-cleanup/20-03-PLAN.md \
        .planning/phases/20-architecture-and-normalization-cleanup/20-04-PLAN.md \
        .planning/phases/20-architecture-and-normalization-cleanup/20-05-PLAN.md
# If a Global STOP rule or Task 6 modified the gap registers, stage those tracked changes too (no-op if unchanged):
git add -u .planning/phases/20-architecture-and-normalization-cleanup/20-GAPS.md .planning/milestones/v1.4-GAPS.md
git commit -m "plan(20): remediate review findings before execution"
```

Expected: one atomic commit containing only the Phase 20 planning remediation.

## Self-Review Checklist

- [ ] Every high-risk review finding has a task: M5 neutrality, M10 mass range, ledger serialization, D-09/D-10/D-11 traceability, 20-04 audit gates (incl. the `realized` artifact-check reconciliation, broadened defect-phrase audit, and removal-only formula-diff guard), 20-01/20-02 hardening, the 20-02 orthogonal omega regression check, the 20-04 `wave: 3` relabel and its 20-03 cross-reference, and ARCH-04 block preservation.
- [ ] No task asks the executor to adjudicate source-silent semantics without STOP protocol.
- [ ] No task invents an evidence packet, acceptance check, partial status, or shared evidence protocol.
- [ ] No task edits framework specs, evidence packets, live code, or Phase 20.5 artifacts.
- [ ] All verification commands use explicit paths under `<home>/Desktop/3_body_problem`.
- [ ] Consciously-deferred minors are recorded as out-of-scope follow-ups (not silently dropped): D-02 identifier collision (already qualified in 20-CONTEXT D-05); SI-PINN-002 located by section anchor vs `~line 1000`; `20-GAPS.md` governance line `AGENTS.md`→`CLAUDE.md` and its stale `2026-06-03` timestamp; `E_scale` epsilon `1e-8` vs `1e-10`; the `20-RESEARCH` ratio-form lemma's `I_3 = 0` collinear edge case.
