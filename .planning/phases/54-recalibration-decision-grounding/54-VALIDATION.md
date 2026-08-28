---
phase: 54
slug: recalibration-decision-grounding
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-19
---

# Phase 54 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> This phase's validation is **textual**, not runtime — the phase authors
> Markdown and writes no code. It is one step lighter than Phase 53: it does not
> even edit a framework spec, it only *cites* one.
>
> **Scope note (CONTEXT.md D-11, updated 2026-08-28):** this contract covers the
> ERW-01 execution pass (packet + delivery note + gate presentation) and the
> 54-06/54-07 reconciliation and handoff-readiness plans. ERW-02 is **partially
> discharged** — the package is assembled and the handoff is certified. Delivery,
> the ERW Rule-19 per-claim in-repo verification, the ERW Rule-12 consolidation,
> and owner checkpoint ② remain outstanding. Phase 54 does not close here.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | none — `grep` / `diff` / file-existence shell assertions, per the Phase 45 (`45-AUDIT.md`) and Phase 53 (`53-VALIDATION.md`) precedent |
| **Config file** | none |
| **Quick run command** | the per-task `grep -c` / `test -f` / `git diff --stat` assertions scoped to the file that task wrote |
| **Full suite command** | the full `45-AUDIT.md`-style check battery, scoped to what ERW-01 actually creates (the pre-snapshot subset — see Manual-Only below) |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** that task's own textual assertions + the two standing negative-diff bars (read-only spec bar, read-only `pinn/` bar)
- **After every plan wave:** the full assertion set for everything the wave touched
- **Before checkpoint ① is presented to the owner:** every assertion below green, plus the D-04 self-audit section's recorded result read manually
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

> **Re-keyed at plan time (2026-08-20).** The planner emitted **five plans across
> four waves** (13 tasks), per the Phase-45 precedent and CONTEXT.md's Claude's
> Discretion on decomposition. The map below is keyed to the emitted plan/task
> IDs. The six standing shell assertions are named **Bar A / A2 / B / C / D / E /
> F** and are defined once, verbatim, in `54-01-PLAN.md`'s `<verification>` block
> (Bars A, A2, B, C, D) and `54-03-PLAN.md`'s (Bars E, F); every task below
> references them by name rather than restating them.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 54-01-01 | 01 | 1 | ERW-01 (D-01, D-02, D-03, D-04, D-06) | T-54-02 | Cited external content bounded as data, never imported wholesale | textual assertion | Master exists at the round root with `grep -c '^## '` = **11** (§0–§10, covering all seven r2 roles by content match plus D-03's three additions); frontmatter carries `access_mode: open-book` and a 40-char `source_baseline` equal to `git rev-parse HEAD`; both `NEUTRALITY-BAN` markers present and correctly bracketed; §0 carries the verbatim §7-clause-3 quote and the `2026-07-24` / `2026-07-25` vintage; Route-A phrases `you have no codebase access` / `attached files only` → **0** | ✅ (post-write) | ⬜ pending |
| 54-01-02 | 01 | 1 | ERW-01 (D-02, D-09, D-11) | T-54-08 | Gate routing carries no cost framing | textual assertion | `DELIVERY-NOTE.md` exists, opens with the never-upload warning, names all three withheld artifacts by path, points at `54-RULING.md` and `GAP-54-01`, repeats the master's `source_baseline`, and carries SCOPE-33..38. **Bar F** analog over the note (cost/effort/difficulty vocabulary) → **0** | ✅ (post-write) | ⬜ pending |
| 54-01-03 | 01 | 1 | ERW-01 (D-02), SCOPE-33/34 | T-54-01 | Read-only bars hold; branch neutrality is structural | tracer end-to-end assertion | **Bar A** → empty · **Bar B** → empty · **Bar C** → prints `NEUTRAL` · **Bar D** → empty · `find …/trainex-r3 -type f | wc -l` = **2** | ✅ | ⬜ pending |
| 54-02-01 | 02 | 2 | ERW-01 (D-03, D-06) | — | N/A | textual assertion | §1 has subsections 1.1/1.2/1.3, no placeholder remains, 1.3 transcribes SCOPE-34's bar and names §10 as the inspection criterion, `52-VER-20-ROUTING-HANDOFF.md` cited; **Bars A, B, D** green | ✅ (post-write) | ⬜ pending |
| 54-02-02 | 02 | 2 | ERW-01 (D-05, D-07) | T-54-03, T-54-06 | Mechanism transcribed, surfaces never enumerated | citation-fidelity + structural assertion | All five D-07 facts inline with `file:line`; **the step-501 halt must NOT cite the 2026-08-17 audit** — `grep -n '501' <master> | grep -c 'residual-frame-conformance-audit'` = **0**, correct sources `52-DIAG-05-REDERIVATION.md:58` / `50-03-SUMMARY.md:84` (RESEARCH.md Finding 5 / Pitfall 1). Both `87.34` and the rounded `87.3` present with distinct citations. Coupling: `4096`, `collocation_count = 16`, `256`, `SPEC-06` all present. Nine verified `pinn_architecture.md` anchors present; stale `:424`/`:167`/`:433`/`:440` → **0**. `sed -n '<N>p'` re-derives each cited line. **Manual:** per-surface no-menu verdict recorded | ✅ (spot-checkable) | ⬜ pending |
| 54-02-03 | 02 | 2 | ERW-01 (D-06) | T-54-02 | trainex-r2 citations bounded and tagged | textual assertion | §6 carries ≥ 8 `F-` rows (all with `file:line`) and ≥ 1 `H-` row (all labeled "not established fact"); the hypothesis→fact transition note present and `[r2-QUAL]`-tagged; no strength rubric (`strong|moderate|weak` → **0**); **Bar B** → empty | ✅ (post-write) | ⬜ pending |
| 54-03-01 | 03 | 2 | ERW-01 (D-10) | — | N/A | file-existence + textual | `test -f .planning/phases/54-recalibration-decision-grounding/54-GAPS.md` **and** `test -f .planning/milestones/v2.3-GAPS.md`; `grep -c '^## GAP-'` in the phase register = **1** (`GAP-54-01`); all eleven CLAUDE.md fields present; classification `semantic`; `Status: OPEN`; ≥ 4 resolving `file:line` source-silence citations; enumeration is a **pointer** to the packet's §7, not a duplication | ✅ (post-write) | ⬜ pending |
| 54-03-02 | 03 | 2 | ERW-01 (D-08, D-09) | T-54-03, T-54-04, T-54-07 | The gate artifact cannot pre-answer the gate | textual assertion | `54-RULING.md` has `status: PENDING`; checkpoint-② table has exactly five rows, every `Disposition` = `PENDING`; the `N_t` completeness rule pre-declared (content match on "does not dispose of" / incomplete-routes-back) ≥ 1 with `SPEC-06`; **zero** candidate values for `η_c`, the normalization reference scale, `ω₀`, `N_t`, or the clip; three SCOPE-38 blocks at `:445` / `:181` / `:668`; anchor-drift warning contains the four stale anchors and they appear nowhere else. **Bar F** → **0**; no-preference grep → **0** | ✅ (post-write) | ⬜ pending |
| 54-04-01 | 04 | 3 | ERW-01 (D-02, D-03) | T-54-01 | Withheld artifacts named, not created | textual assertion | §2 names all three withheld artifacts by path with the runbook's own reason and carries the seven-row r2→r3 role-mapping table; attachment-cap reasoning absent (RESEARCH.md Pitfall 4) → **0**; §3 carries the hard-constraint, challengeable, and Route-B repo-derived tiers, names `Rule 19`, and records that `pinn/` is not a grounding source; **Bars A–E** green | ✅ (post-write) | ⬜ pending |
| 54-04-02 | 04 | 3 | ERW-01 (SC-1 "names its own gaps") | T-54-03 | Questions frame without answering | structural assertion | §5 has ≥ 4 numbered questions, ≥ 1 explicitly about the couplings (`SPEC-06` cited), none embedding a value/range/form/direction. **§7 covers all five surfaces** — `η_c`, normalization, `ω₀`, `N_t`/`n_col`, clip each ≥ 1 within the §7 range; ≥ 5 `file:line` silences cited; points at `GAP-54-01`; `[r2-QUAL]` present. **Manual:** per-question verdict recorded | ✅ (post-write) | ⬜ pending |
| 54-04-03 | 04 | 3 | ERW-01 (D-03, D-04 Layer 2), SC-4 | T-54-09, T-54-10 | Rule-7 contract not gutted to pass a lexical sweep | inverse-polarity assertion | **Bar A2** — §9 Rule-7 vocabulary (`suggested default|one-way|two-way|decision sheet`) **≥ 4**; a lexically clean §9 FAILS. All six Rule-7 elements named; `never decide` present; `Rule 9` / `Rule 17` / `Rule 18` / `Rule 19` each ≥ 1; ≥ 3 read-only bars in the imperative. §8 records the baseline pin and defers the Rule-20 live-tree pin. `<!-- NEUTRALITY-BAN-END -->` line number **<** `## 9.` line number. **Bar A** still empty. Whole-file `grep -c 'Written by plan 54-'` = **0** | ✅ (post-write) | ⬜ pending |
| 54-05-01 | 05 | 4 | ERW-01 (D-04, SC-1) | T-54-11, T-54-06 | The self-audit's own claims are re-derivable | self-audit assertion | `sed -n '/^## 10\./,$p' <master> | grep -c 'PENDING'` = **0**; every Bar A/A2/B/C/D/E/F recorded by name with its producing command and outcome; the three excluded `45-AUDIT.md` checks (self-containment = Route-A-only; snapshot fidelity + snapshot pin half = presuppose the withheld `specs/`) named with reasons and marked **deferred, not waived**; per-surface structural verdicts × 5; citation-fidelity counts + every failure; `source_baseline` byte-identical across master frontmatter, §8, and the delivery note; `find …/trainex-r3 -type f` = 2 paths; SCOPE-33..38 boundary attestation; traceability table mapping ERW-01 and SC-1/SC-2/SC-3-gate, with SC-4/SC-5 marked not-yet-applicable | ✅ (post-write) | ⬜ pending |
| 54-05-02 | 05 | 4 | ERW-01 → checkpoint ① (D-08, D-11), SC-3 | T-54-03, T-54-12 | The agent does not select the branch | halt assertion | Blocking `checkpoint:decision` presented; `54-RULING.md`'s `Branch` still `PENDING` at presentation; **Bar C** passes and `find …/trainex-r3 -type f` = 2 (no ERW-02 artifact created pre-gate); no plan file numbered above `54-05`; `docs/work/reviews/milestone_v2.3/` does not exist; `GAP-54-01` still `OPEN` in both registers; **Bar F** → **0**; summary records Phase 54 **in progress**, not complete | ✅ | ⬜ pending |
| 54-06-01 | 06 | 5 | ERW-02 (reconciliation) | T-54-12, T-54-13, T-54-14 | Out-of-band commits recorded not authorized; Checks R1/R2 replace the two-path guard | textual assertion | `54-RECONCILIATION.md` exists; `grep -cF 'does not retroactively authorize'` ≥ 1; Check R1 prints `MANIFEST-OK`; Check R2 table matches introducing dates; four-path fail-demo prints `MANIFEST-FAIL` | ✅ (post-write) | ⬜ pending |
| 54-06-02 | 06 | 5 | ERW-02 (re-derivation) | T-54-11, T-54-15 | Every hand-run audit result re-derived with its command | textual assertion | Re-derivation table rows carry Command and Re-derived cells; empty-cell awk exits 0; A-1 through A-10 each present as first cell; new `A-` entries record at-source repairs; Bar D empty; `54-RULING.md` / gap registers byte-unchanged vs HEAD | ✅ (post-write) | ⬜ pending |
| 54-06-03 | 06 | 5 | ERW-02 (accounting + Bar G) | T-54-16, T-54-17 | ROADMAP/STATE/VALIDATION derived from disk; plan-file neutrality holds | textual assertion | Section 7 listings recorded; ROADMAP contains `partially discharged`; Bar G prints `BAR-G-CLEAN` or `BAR-G-CLEAN-NO-SURFACE-NAMED` with region cardinality; narrowed Bar E over REQUIREMENTS.md empty | ✅ (post-write) | ⬜ pending |
| 54-07-01 | 07 | 6 | ERW-02 (H1–H8) | T-54-12 | Round-root artifacts certified against ERW Rules 7, 15, 16, 17, 18, 20 and Rules 1–2 inversion | textual assertion | `54-HANDOFF-READINESS.md` has eight H1–H8 rows; Check R1 still `MANIFEST-OK` | ✅ (post-write) | ⬜ pending |
| 54-07-02 | 07 | 6 | ERW-02 (routing note) | T-54-08 | Deferred-replan routing names destinations and rules without cost framing | textual assertion | Routing note names `research_results/`, `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/`, `trainex-r3-resolution-doc.md`, Rule 19, Rule 12; Bar F analog 0 | ✅ (post-write) | ⬜ pending |
| 54-07-03 | 07 | 6 | ERW-02 → owner handoff | T-54-03 | Execution halts at the blocking-human gate; no candidate value | halt assertion | Blocking `gate="blocking-human"` presented; Phase 54 remains in progress; `GAP-54-01` OPEN; checkpoint ② unfilled; Phase 56 closed; `research_results/` absent; `docs/work/reviews/milestone_v2.3/` absent | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

### Scope note on this map (CONTEXT.md D-11)

Roadmap Success Criteria **4 and 5 have no row above** — they discharge at
delivery, the ERW Rule-19 per-claim in-repo verification, the ERW Rule-12
consolidation, and owner checkpoint ②, all still outstanding. ERW-02 is
**partially discharged** (package assembled; handoff certified). Tasks `54-06-*`
and `54-07-*` follow `54-05-02`; this execution pass continues through the 54-07
owner handoff and does not close the phase.

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements — no test framework, fixtures, config, or dependency is introduced. Every assertion runs with standard Unix utilities (`grep`, `diff`, `test`, `git`) already used throughout Phase 45 and Phase 53. This mirrors Phase 53's identical Wave-0 conclusion.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| The packet reads as non-recommending **structurally**, not merely lexically | ERW-01 / SC-1 (D-05) | The sharpest failure mode is a neutral-sounding sentence that enumerates comparable options — it has already ranked them. No `grep` asserts this; it needs a reader | Read the remedy-surfaces section end to end. For each surface, confirm it states *what the quantity is, where specified, what it couples to, what the evidence does and does not pin* — and never "the choices are…" |
| Which `45-AUDIT.md` checks apply pre-snapshot | ERW-01 (D-04) | Several r2 checks (e.g. self-containment) presuppose artifacts D-02 deliberately withholds this phase | Reviewer selects the applicable subset and records the exclusions with reasons in the self-audit section. RESEARCH.md Open Question 2 — flagged Claude's Discretion, not pre-resolved |
| Every `file:line` anchor still resolves | ERW-01 (D-07) | Line numbers drift when files are edited; Phase 53's commits already invalidated one set (CONTEXT.md Open Item 5) | Re-derive each `pinn_architecture.md` anchor by content match, not by trusting the number. RESEARCH.md Finding 7 verified the CONTEXT.md anchor set against the live tree |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending — not granted. Plan 54-06 does not close the phase. What is established: ERW-01 complete; checkpoint ① discharged; the round-root package assembled; Checks R1/R2 and Bar G defined. What is not established: delivery, Rule-19 verification, Rule-12 consolidation, checkpoint ②, Success Criteria 4 and 5, `nyquist_compliant`.
