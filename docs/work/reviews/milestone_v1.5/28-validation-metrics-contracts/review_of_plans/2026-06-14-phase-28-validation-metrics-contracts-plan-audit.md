---
status: active
purpose: review-findings
created: 2026-06-14
milestone: v1.5
phase: 28-validation-metrics-contracts
retirement_trigger: every finding below reaches finding-by-finding closeout (addressed / superseded / not-applicable) after Phase 28 plan revision or executor sign-off
---

# Phase 28 Plan Audit — Validation-Metrics Contracts (28-01..04)

**Reviewer:** Claude (Opus 4.8), inline multi-persona document audit
**Date:** 2026-06-14
**Artifacts audited:** `28-01-PLAN.md` (SCS/VAL-01), `28-02-PLAN.md` (SASD/VAL-02), `28-03-PLAN.md` (IPR/VAL-03), `28-04-PLAN.md` (PSC/VAL-04), cross-read against `28-SPEC.md`, `28-CONTEXT.md`, `28-DISCUSSION-LOG.md`.
**Objective:** Stress-test the four execute-plans for flawless downstream execution by an autonomous agent, across **Logical Integrity**, **Execution Clarity**, and **Operational Resilience**.

## Method & scope note

This audit applied the `ce-doc-review` persona lenses (coherence, feasibility, scope-guardian, adversarial) **inline** rather than dispatching cold sub-reviewers. Rationale: the harness here discourages spawning sub-agents that were not requested, and this milestone's governance context (v1.5 STOP protocol, grounding hierarchy, evidence machinery) is already loaded in the reviewing context — cold reviewers would re-derive it and likely miss it. Findings were not taken on the plans' word: every load-bearing factual claim was verified against the live repository. The **Verification Ledger** at the end records each check so this review is re-derivable per repo norms.

---

## Verdict & posture

**The four plans are high quality and unusually faithful to the v1.5 STOP protocol.** Grounding is accurate where I could check it (see Verification Ledger): the existing SCS gate, the PIPE-09 contract, the dual-ε anchors, the resolution-doc fork language, and the DQA "PCHIP" misnomer are all real and correctly characterized. The packet-before-edit gate, the MUST-surface-despite-`autonomous:true` discipline, the understanding-gate, byte-exact append-only regression, two-phase SHA backfill, and AC negative controls are all present and well-designed.

**However**, the plans are **not yet ready for unattended autonomous execution.** There is **one environment blocker** (O1) that fails before any task runs, and **one genuine logical hole** (L1) that the plans' *own* designed STOP-park outcome can trigger. Both should be closed before execution. The remaining findings are clarity/coherence/bookkeeping refinements that an intuition-free agent could resolve the wrong way.

**Recommendation: revise for the items below (at minimum O1 + L1 + C1), then execute.**

---

## Prioritized findings

| # | Dimension | Severity | One-line |
|---|-----------|----------|----------|
| **O1** | Operational | **HIGH** | All four plans' `<execution_context>` `@`-includes (`~/.claude-max-max/gsd-core/...`) resolve to a directory that does not exist on this machine. |
| **L1** | Logical | **HIGH** | If 28-02 (SASD) **parks**, the shared subsection it was to *create* never exists, but 28-03/28-04 assume it exists with no create-if-absent / cascade-park branch. |
| **C1** | Clarity | **MED-HIGH** | "`DEFERRED` is an allowed phase-exit state" vs "phase exit blocked while the gap is OPEN" — a premature-close ambiguity on an unresolved governance fork. |
| **C2** | Clarity | **MEDIUM** | Subsection heading is "Claude's discretion," yet 28-03/04 re-location greps **and** the AC checks hard-code the literal heading string. |
| **C3** | Clarity | **MEDIUM** | "Confirm the AC fails on the pre-edit spec" is required for 28-02/03/04 but the AC is authored *after* the edit, with no stated way to obtain the pre-edit spec. |
| **C4** | Clarity | **MEDIUM** | The evidence `ID→Filename` map does **not** contain SASD/IPR/PSC rows; plans condition the map-update on "if a different name is used," risking a permanently incomplete map. |
| **L2** | Logical | **MEDIUM** | The SCS ledger row's `Spec Section` cell still points only to the read-only DQA; no 28-01 task repoints it to `ctl_instruction.md` after VAL-01 lands. |
| **L3** | Logical | **MEDIUM** | SCS lands in Step-1A while SASD/IPR/PSC land in a new subsection titled "(SASD, IPR, PSC)" that excludes SCS; no cross-reference ties the four metrics into one family. |
| **O2** | Operational | **MED-LOW** | On a park, plans add a gap entry but never update the `v1.5-GAPS.md` frontmatter counters (`total_gaps`/`open_gaps`/`last_updated`); `28-GAPS.md` is created on-demand but no task names its creation. |
| **L4** | Logical | **LOW-MED** | The IPR dual-ε "training side = `1e-5`" anchor intersects an unresolved v1.4 Author Comment (arch:535, FUT-05) yet is framed as "settled/constraint-entailed." |
| **C5** | Clarity | **LOW** | "Fill EVERY required section" of `_TEMPLATE.md` collides with the template's conditional EVID-10-only sections; the packet-AC enumerates only 7 of 13 sections. |
| **L5** | Logical | **LOW** | 28-01 Task-2 `read_first` mislabels the arch dual-ε region as "§2.5" (that is ctl global-scaling; dual-ε lives in arch §3.2/§3.4). |
| **O3** | Operational | **LOW** | 28-01's PIPE-09 fixture boundary is a bold-text marker inside §2.5, not a heading — more fragile than the heading-bounded `awk` pattern it claims to mirror. |
| **O4** | Operational | **LOW** | "Surface to the user" assumes a channel an unattended autonomous run may not provide; parked work can idle silently. |
| **O5** | Operational | **LOW** | The candidate source (`02-resolution-doc.md:8`) carries leftover consolidation-agent narration ("Duplication detected…"); benign, but the plans don't point the executor at the clean `24.5-RESOLUTION-MAP` line-ranges. |

---

## Logical Integrity

### L1 — Wave-park substrate hole (HIGH)
**What.** Plan 28-02 Task 2 both *creates* the new `Data-side quality-metric contracts (SASD, IPR, PSC)` subsection in `ctl_instruction.md` **and** writes the SASD clause into it. But 28-02 is explicitly allowed — even designed — to **PARK** when its Q-C2 endpoint fork is unsettled (Task 1 outcome b), in which case Task 2 does **not** run and the subsection is never created. Plans 28-03 (Task 2: "APPEND the IPR clause to the `Data-side quality-metric contracts` subsection (created by 28-02)") and 28-04 (Task 2: append PSC) re-locate that subsection **by `grep`** and have **no branch** for "subsection absent because the prior wave parked."
**Why it bites an autonomous agent.** `depends_on: ["28-02"]` does not disambiguate *parked* from *landed*: a parked plan still commits (packet + `DEFERRED` row + SUMMARY), so a wave runner may proceed to 28-03. If 28-03's *own* fork happens to settle, its Task 2 greps for a heading that does not exist and has no instruction — it will either error, stall, or silently improvise an unspecified structure. The STOP protocol's own park outcome thereby breaks the two downstream waves.
**Fix.** Decide and state the dependency semantics under a park, in all three plans: either (a) **decouple substrate creation** — have whichever metric lands *first* create the (possibly single-clause) subsection, with 28-03/04 creating it if absent; or (b) **cascade-park** — if 28-02 parked, 28-03/04 also park (record the dependency in their gap entries) regardless of their own fork outcome. Option (a) is more robust and matches the append-only design.

### L2 — SCS ledger `Spec Section` not repointed (MEDIUM)
**What.** `24-ISSUE-LEDGER.md:34` records the SCS row's `Spec Section` as `data_quality_assessment.md (read-only; sole written home of locked gate)`. After VAL-01, the canonical SCS contract lives in `ctl_instruction.md` Step-1A clause 5. No 28-01 task updates this cell — it advances Status→`VERIFIED`, the evidence link, the transition log, and AC-VAL-01, but leaves the row asserting the wrong post-fix home.
**Fix.** Add to 28-01 Task 3: update the SCS row `Spec Section` to name `ctl_instruction.md` Step-1A conservation gate (keeping the DQA as the cited historical/read-only home), in the same commit.

### L3 — SCS placement coherence (MEDIUM)
**What.** SCS is reconciled *in place* in Step-1A (an admission gate with reject authority), while SASD/IPR/PSC are gathered into a brand-new subsection whose title literally enumerates `(SASD, IPR, PSC)` — structurally excluding SCS. The phase goal (`28-SPEC.md`) is "one canonical contract per metric," and AC-VAL-01 wants "one SCS definition." The split is defensible on semantics (SCS rejects; SASD/IPR flag; PSC is report-only), but **no task adds a cross-reference** binding the four into one validation-metric family.
**Fix.** Have 28-01 (or 28-02 when it creates the subsection) add a one-line cross-reference between the Step-1A SCS gate and the `Data-side quality-metric contracts` subsection so a reader / FUT-01 sees all four metrics as a coherent set.

### L4 — PHYS-03 `1e-5` anchor rests on an open author comment (LOW-MED)
**What.** 28-03 frames the dual-ε distinction (validation IPR `eps=1e-10` vs training `IPR_train eps=1e-5`) as "constraint-entailed / settled, independent of the units fork." But `pinn_architecture.md:535` carries an unresolved v1.4 Author Comment — *"(Author Comment: I am not sure why there is a duplicate 10^-5 here)"* — deferred to FUT-05. The "settled" training-side `1e-5` partly leans on a number flagged uncertain upstream.
**Fix.** Have 28-03 Task 1 explicitly confirm `1e-5` is the settled PHYS-03 softening outcome (cite the v1.4 PHYS-03 record), and note it is distinct from the arch:535 author-comment ambiguity — or, if it cannot, treat the dual-ε determination as a surface-worthy item rather than "settled."

### L5 — Section mislabel in 28-01 (LOW)
`28-01-PLAN.md` Task 2 `read_first` labels the dual-ε region "§2.5"; §2.5 in `ctl_instruction.md` is *Global scaling* (the PIPE-09 region). The dual-ε quantities (`eps_H = 1e-4*S_H`, `epsilon_train = 1e-5`) live in `pinn_architecture.md` §3.2/§3.4. The `grep` markers still find the right lines, but the label is wrong and could misdirect. **Fix:** relabel to "arch §3.2/§3.4."

---

## Execution Clarity

### C1 — `DEFERRED` vs OPEN-gap phase-exit ambiguity (MED-HIGH)
**What.** The evidence README Phase-Exit Rule states "Allowed phase-exit states are only `VERIFIED` and `DEFERRED`." The plans, on a park, set the row to `DEFERRED` (`defer-with-blocker`) **and** leave the STOP gap `OPEN`, while noting "phase exit is blocked while the gap is OPEN." The CLAUDE.md STOP protocol is emphatic that parked work "stays halted until the user provides instruction."
**Why it bites.** An intuition-free executor can read "the row is `DEFERRED`, and `DEFERRED` is an allowed exit state ⇒ I may close the phase" — bypassing the halt on a fork the user never adjudicated. The reconciliation (a row-status gate vs a governance/milestone-close gate are *different* gates; `DEFERRED`-with-OPEN-gap still blocks the *phase*) is correct but is scattered across 28-02/03/04 Task 3 and 28-04's "phase-exit note."
**Fix.** State once, prominently (ideally in CONTEXT and echoed in each plan): a `DEFERRED` row whose STOP gap is still `OPEN` satisfies the *row-status* gate but **does not** permit phase closure; phase-28 close requires every VAL gap `RESOLVED-WITH-INSTRUCTION`/`DEFERRED`-by-user. Make the two senses of "exit" explicit.

### C2 — Heading discretion vs hard-coded grep marker (MEDIUM)
**What.** CONTEXT grants "exact heading names … Claude's discretion," and 28-02 says the subsection may be titled `Data-side quality-metric contracts (SASD, IPR, PSC)` "or equivalent." But 28-03/04 re-locate the subsection with `grep -n 'Data-side quality-metric contracts'`, and the AC checks assert that literal string. Exercising the granted discretion silently breaks downstream re-location **and** the AC self-checks.
**Fix.** Either make the heading **normative** (remove the discretion for this one subsection) or instruct 28-02 to record the chosen heading in its SUMMARY and have 28-03/04 read that value instead of a hard-coded literal.

### C3 — Pre-edit AC discrimination has no stated mechanic (MEDIUM)
**What.** 28-02/03/04 Task 3 require "confirm the AC FAILS on the pre-edit spec" to prove the check discriminates — but the AC is **authored in Task 3, after Task 2 already edited the working tree**. Only 28-01 explains how to reach a pre-edit state (`git show HEAD:…ctl_instruction.md`); the sibling plans do not.
**Why it bites.** A literal executor runs the freshly-authored AC against the already-edited working tree, it passes, and the "fails pre-edit" evidence cannot be produced — or the executor fabricates the claim.
**Fix.** Either author+run the discriminating AC **before** Task 2's edit (as 28-01 does in its Task 1), or add the explicit `git show HEAD:ctl_instruction.md` re-derivation to the "confirm fails pre-edit" step in 28-02/03/04.

### C4 — `ID→Filename` map rows are absent, not just "different" (MEDIUM)
**What.** Verified: the evidence README map lists `SCS`, `D=6.694`, `M11/M12`, `B-06`, `B-11`, `D7`, `M13`, `D-03`, `mass-drift/DATA-05` — and **not** SASD, IPR, or PSC. The plans say "if the executor prefers a *different* sanitized name it MUST record the mapping row," which conditions the map update on deviation.
**Why it bites.** A literal executor, told the mapping is `SASD → sasd-sampling-density.md`, may assume the row already exists and skip the add (since it is not "different"), leaving the map permanently missing all three new packets — a process-schema integrity miss the README treats as a STOP-able ambiguity.
**Fix.** Change the instruction to: "**Add** the SASD/IPR/PSC rows to the `ID→Filename` map in the same commit (the map currently lacks them), using the sanitized name; record any deviation."

### C5 — "Every required section" vs the template's conditional sections (LOW)
`_TEMPLATE.md` has 13 sections; four (First-Principles Physics Check, Root-Cause Framework Ambiguity, Locked Convention, Which Source Was Correct/Wrong) are **EVID-10-conflict-only** and apply to SASD/IPR/PSC only under outcome (c). The action says "Fill EVERY required section" and names the FUT-01 Hand-off Note, while the packet-AC enumerates only 7 sections (omitting the Hand-off Note). **Fix:** state "every required non-conflict section (EVID-10 sections only on outcome (c))" and align the AC enumeration with the action.

---

## Operational Resilience

### O1 — Dangling execution-harness includes (HIGH)
**What.** Every plan opens with:
```
<execution_context>
@$HOME/.claude-max-max/gsd-core/workflows/execute-plan.md
@$HOME/.claude-max-max/gsd-core/templates/summary.md
</execution_context>
```
On this machine, `~/.claude-max-max/gsd-core` **does not exist** (verified — the whole directory is absent). `execute-plan.md` is the executor's operating protocol (deviation handling, checkpoints, commit discipline); `summary.md` is the template every plan's `<output>` requires ("Create `28-0N-SUMMARY.md`").
**Why it bites.** If the executing profile does not mount that path, the `@`-includes resolve to nothing and the executor runs without its harness and without the SUMMARY template — the first thing to fail, before any task.
**Caveat / fix.** This may be specific to a CCP "max-max" profile that mounts `gsd-core` at run time. **Confirm the actual `gsd-core` path for the exact profile that will execute these plans**; if the path is stale, correct the `@`-include in all four plans. Do not begin autonomous execution until these two includes resolve.

### O2 — Gap-index counter drift on park; `28-GAPS.md` creation unnamed (MED-LOW)
**What.** `v1.5-GAPS.md` carries frontmatter counters (`total_gaps: 6`, `open_gaps: 0`, `resolved_gaps: 6`, `last_updated`). On a park, the plans add a gap **entry** and cite CLAUDE.md STOP step 4 ("update the milestone-wide index") but never mention updating those **counters**. Separately, `28-GAPS.md` does not exist yet and no task explicitly names its creation (it is created on-demand at first park).
**Fix.** Add to the park branch: create `28-GAPS.md` (full STOP schema) and update `v1.5-GAPS.md` — add the `## Phase 28` section/row **and** increment `total_gaps`/`open_gaps` and set `last_updated`.

### O3 — Fragile PIPE-09 fixture boundary (LOW)
28-01 Task 3 extracts the regression fixture "from the `Normative compute_globals contract` marker to the next heading." Unlike 27-01's heading-bounded `awk` (`/^## Step 1A …/{…} /^## /{…}`), the `compute_globals` contract is a **bold paragraph inside §2.5** (`ctl:781`), not its own `##`/`###` heading; the start boundary is a bold-text marker and the end is the next `### 2.6`. Workable (the plan also records exact tokens as a backstop) but more brittle than the pattern it claims to mirror. **Fix:** specify the exact extraction range (`### 2.5` body from the bold marker to `### 2.6`) or hash the whole §2.5 block.

### O4 — Surfacing channel assumption (LOW)
A MUST-surface park records a gap and halts, "awaiting user instruction." Under an unattended autonomous wave run, there may be no active channel; the work idles on a `DEFERRED`+OPEN row. Orchestration-level, not plan-internal — flag so the runner is watched when a fork is plausible.

### O5 — Candidate-source narration cruft (LOW, hygiene)
`02-resolution-doc.md:8` embeds leftover consolidation-agent narration: *"Duplication detected — §5 onward appears twice. Inspecting the boundary … before fixing."* **Verified benign:** the §5.1–5.4 headers each appear once (543/575/627/675) and `24.5-RESOLUTION-MAP.md` gives clean single ranges with a READY-WITH-CAVEATS verdict. **Fix:** have 28-01/28-04 (like 28-02/03 and CONTEXT) point the executor at the `24.5-RESOLUTION-MAP` line-ranges for EVID-06 citations, and note the line-8 text is an artifact, not a structural defect, so the executor is not misled into "fixing" the candidate source.

---

## What the plans get right (calibration)

These are genuine strengths and should be preserved through any revision:

- **STOP-protocol fidelity:** packet-before-edit gate; the three-outcome fork structure (settle / park / EVID-10); MUST-surface explicitly *not* auto-picked despite `autonomous: true`; the understanding-gate (no verdict *or* gap if the math cannot be articulated); `defer-with-blocker` + the non-destructive ledger-revert rule (D-14).
- **Faithful grounding (verified):** the existing SCS gate, the PIPE-09 `compute_globals` contract, the dual-ε anchors, and the resolution-doc fork phrasings are all real and accurately represented; the DQA "PCHIP" misnomer is correctly caught and converted into a `PchipInterpolator`-prohibited / `CubicHermiteSpline`-required contract.
- **Regression discipline:** byte-exact fixtures with append-only edits and re-verification of prior clauses (SASD intact after IPR; SASD+IPR intact after PSC); the D=6.694 row protected after the SCS edit.
- **Commit integrity:** same-commit atomicity (spec + ledger + evidence + AC result), the two-phase SHA backfill (correctly mirroring the *verified-to-exist* 27-01 pattern), and the owned-paths self-audit.
- **AC negative controls:** ratio thresholds appear only in rejection context (SCS); no training-loop/collocation policy text (SASD/IPR); no replay policy and no reject-gate (PSC).
- **Scope discipline:** DQA read-only (SCOPE-09), `sampling_method.md` frozen (SCOPE-08), no live `pinn/` grounding (SCOPE-10), every training-loop use a doc-03 forward-reference (SCOPE-11).

---

## Verification Ledger (re-derivable)

| Claim under test | Result | Evidence |
|---|---|---|
| 28-01's premise that a SCS gate already exists in ctl (reconcile, not duplicate) | **CONFIRMED** | `ctl_instruction.md:474-481` — Step-1A clause 5 carries `SCS = log10(eps_H)`, `REJECT SCS > -5`, band table |
| PIPE-09 `compute_globals` contract present, marker locatable | **CONFIRMED** | `ctl_instruction.md:781` — "Normative `compute_globals` contract (PIPE-09)"; D≈4.6416 canonical, 6.694 rejected, `eps_inv=1e-10`, admitted-set scope |
| Dual-ε anchors in pinn_architecture.md | **CONFIRMED** | arch §3.4 `eps_H = 1e-4*S_H` (`:526`), `epsilon_train = 1e-5` (`:535,567`), §3.2 residual (`:359`) |
| Phase-27 two-phase-SHA + byte-fixture patterns the plans "mirror" | **CONFIRMED** | `27-01-PLAN.md:225-239` (placeholder + `verify(27-01): backfill commit sha`), `:271-291` (awk-extract + shasum + diff) |
| `scs-thresholds.md` verdict + sections the plan depends on | **CONFIRMED** | verdict `accept-resolution` (`:63`); Locked Convention, Before/After, Status Transition Log, Which-Source present |
| Evidence README: AC-VAL-01..04 reserved, four-source, phase-exit, packet-before-edit | **CONFIRMED** | README `:113, :24-29, :89-91, :99` |
| `ID→Filename` map already contains SASD/IPR/PSC | **FALSE → finding C4** | README `:121-129` lists 9 rows; none is SASD/IPR/PSC |
| Resolution-doc fork language matches plan descriptions | **CONFIRMED** | `02-resolution-doc.md:14` — Q-C2 "flagged…for sign-off"; Q-C3 "the consequential one" ×≈464 + calibration tripwire + placement inference; Q-C4 "neither input" + four-way verification run |
| Resolution-doc §5 "appears twice" is a real structural duplication | **FALSE (benign) → O5** | §5.1-5.4 headers single (`:543/575/627/675`); `24.5-RESOLUTION-MAP.md:63-66` gives clean ranges; gate READY-WITH-CAVEATS |
| DQA metric sections + the "PCHIP" misnomer | **CONFIRMED** | DQA §3.1-3.4 (`:110/138/160/176`); "PCHIP … using {(q_i,v_i)}" (`:166`); SASD `>0.5` flag (`:158,242`) |
| Execution-context `@`-includes exist | **FALSE → finding O1** | `~/.claude-max-max/gsd-core` absent (dir does not exist) |
| `scripts/agent-commit` + `.githooks` exist | **CONFIRMED** | `scripts/agent-commit` (executable), `.githooks/` present |
| Phase 27 closed / Phase 28 correctly positioned | **CONFIRMED** | `STATE.md:6,8` — "Phase 27 complete; Phase 28 ready"; ledger D=6.694 & M12 `VERIFIED` |

---

## Recommended pre-execution actions (ordered)

1. **O1** — Confirm the `gsd-core` path for the executing profile; fix the four `<execution_context>` `@`-includes if stale. *(blocker)*
2. **L1** — Specify the subsection-substrate behavior when a prior wave parks (create-if-absent **or** cascade-park) in 28-03 and 28-04. *(blocker)*
3. **C1** — State the `DEFERRED`-with-OPEN-gap vs phase-close distinction in one authoritative place.
4. **C2 / C3 / C4** — Fix the heading-marker coupling, the pre-edit AC mechanic, and the "add the ID→Filename rows" instruction.
5. **L2 / L3** — Repoint the SCS ledger `Spec Section`; add the SCS↔subsection cross-reference.
6. **O2** — Add `28-GAPS.md` creation + `v1.5-GAPS.md` counter updates to the park branch.
7. **L4 / L5 / C5 / O3 / O4 / O5** — Apply the low-severity clarifications as convenient.

*Finding-by-finding closeout is required before this review may be proposed for retirement (per `docs/README.md`).*

---

## Finding-by-finding closeout (2026-06-14, post-verification revision)

Each finding below was independently verified against the live repository before action (citations in the per-row notes). 14 findings are **addressed** in the Phase 28 planning artifacts; **O1 is addressed-by-push-back** (the factual claim is true but the recommended path-edit is declined on technical grounds — see its row). Status remains `active`; retirement awaits executor sign-off / the revised plans running.

| # | Disposition | Verification result | Where addressed in the revision |
|---|-------------|---------------------|---------------------------------|
| **O1** | **Addressed by push-back (do NOT edit the path)** | Dir absent here **confirmed**, but `.claude-max-max` is one of a CCP profile family (`.claude`,`.claude-max`,`.claude-max-max`,`.claude-free`,`.claude-alt` all carry `gsd-core`); phases 27 **and** 28 use it and **phase 27 executed successfully** under it. This session is `.claude-alt`. The include is the executing profile's convention, not a typo — editing it would risk breaking real execution. | CONTEXT **D-18(a)** records the inheritance + "confirm the profile, do not blind-edit"; surfaced to the user as the one item needing their confirmation. `<execution_context>` left unchanged. |
| **L1** | Addressed | Confirmed: only 28-02 Task 2 created the subsection; 28-03/04 re-located by grep with no create-if-absent / cascade branch, and their HARD PRECONDITION checked only their own fork. | CONTEXT **D-17** (idempotent locate-or-create + park-independence); 28-02/03/04 Task 2 locate-or-create; 28-03/04 Task 3 regression made conditional on each prior clause having landed; must_haves softened. |
| **C1** | Addressed | Confirmed: README Phase-Exit Rule allows `DEFERRED` at exit; CONTEXT D-13 blocks on OPEN gap — two genuinely different gates. | CONTEXT **D-13** (row-status vs phase-close, with the two senses of "exit" made explicit); echoed in 28-02/03/04 park branches and the 28-04 PHASE-EXIT NOTE. |
| **C2** | Addressed | Confirmed: CONTEXT granted heading "discretion" yet 28-03/04 + ACs hard-code the literal string. | CONTEXT **D-17** makes the `Data-side quality-metric contracts` heading normative; Claude's-Discretion bullet carves it out; 28-02/03/04 Task 2 state it. |
| **C3** | Addressed | Confirmed: 28-02/03/04 author the AC in Task 3 (after Task 2's edit); only 28-01 had a pre-edit mechanic. | `git show HEAD:…ctl_instruction.md` discrimination mechanic added to 28-02/03/04 Task 3. |
| **C4** | Addressed | Confirmed: README map lists 9 rows, none SASD/IPR/PSC. | 28-02/03/04 Task 1 changed to "**ADD** the row (map currently lacks it)"; verify + acceptance updated. |
| **C5** | Addressed | Confirmed: `_TEMPLATE.md` has 4 EVID-10-only sections; verify-enum listed only 7. | 28-02/03/04 reworded to "required **non-conflict** sections (EVID-10 only on outcome (c))"; verify enumeration aligned to the 9 non-conflict sections. |
| **L2** | Addressed | Confirmed: SCS row (ledger:34) Spec Section = DQA-only; every VERIFIED row instead names its ctl landing site (B-06→Step 1A, M12→Mini-Batch Construction). | 28-01 Task 3 repoints the SCS `Spec Section` to `ctl_instruction.md` Step-1A conservation gate (DQA kept as cited read-only home); must_haves + artifacts + acceptance updated. |
| **L3** | Addressed | Confirmed: SCS lands in Step-1A; subsection title enumerates `(SASD, IPR, PSC)`, excluding SCS; no cross-ref bound them. | 28-01 Task 2 (f) adds a forward cross-ref from the SCS gate to the subsection; CONTEXT D-17 has the creating plan add the reciprocal back-reference. |
| **L4** | Addressed (grounding exists — not downgraded to a gap) | arch:535 author comment **verbatim**, BUT it doubts a *duplicate 10^-5*, not the *value*; ctl:919 affirms `εtrain=1e-5` as the PHYS-03 softening. | 28-03 Task 1 cites the ctl:919 PHYS-03 grounding, distinguishes the arch:535 FUT-05 redundancy question, and falls back to surfacing **only if** the grounding cannot be confirmed; read_first + verify + acceptance updated. |
| **L5** | Addressed | Confirmed: ctl §2.5 = *Global scaling* (PIPE-09); dual-ε `eps_H=1e-4*S_H` lives in arch §3.4, not ctl §2.5. | 28-01 Task 2 read_first relabeled to arch §3.4 with a note that §2.5 is global scaling. |
| **O2** | Addressed | Confirmed: v1.5-GAPS.md carries `total_gaps/open_gaps/resolved_gaps/deferred_gaps/last_updated`; no `## Phase 28` section. | CONTEXT **D-13** park-bookkeeping (create 28-GAPS.md if absent; add `## Phase 28` + increment counters); echoed in 28-02/03/04 park branches + verify/acceptance. |
| **O3** | Addressed | Confirmed: `compute_globals` is a bold marker @ ctl:781 inside §2.5; §2.6 @792. | 28-01 Task 3 specifies the explicit extraction range (bold marker → `### 2.6`, with an example `awk`; optional whole-§2.5 hash). |
| **O4** | Addressed | Orchestration-level (accepted as written). | CONTEXT **D-18(b)** — watch the run when a Q-C2/C3/C4 park is plausible. |
| **O5** | Addressed | Confirmed benign: §5.1–5.4 headers single; 24.5-RESOLUTION-MAP gives clean ranges (READY-WITH-CAVEATS). | 28-01 + 28-04 Task 1 read_first point at the 24.5-RESOLUTION-MAP ranges and flag the line-8 narration as a benign artifact, not a defect to "fix". |

**Net spec-engineering effect:** no metric semantics, physics value, or source-silent decision was invented. L1/C2/O2 are operational-coordination plan-mechanics; C1/C3/C4/C5/L2/L3/L5/O3/O4/O5 are clarity/bookkeeping; L4 cites pre-existing v1.4 grounding (ctl:919) and otherwise routes to the STOP protocol. O1's path is left intact pending user confirmation of the executing profile.
