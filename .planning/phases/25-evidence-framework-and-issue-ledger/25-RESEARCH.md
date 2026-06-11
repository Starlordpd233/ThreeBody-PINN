---
status: active
purpose: other
created: 2026-06-11
milestone: v1.5
phase: evidence-framework-and-issue-ledger
retirement_trigger: Phase 25 PLAN.md files are created and the machinery + 3 EVID-10 records land
---

# Phase 25: Evidence Framework and Issue Ledger - Research

**Researched:** 2026-06-11
**Domain:** Adjudication-machinery construction (documentation/process engineering), not software. Markdown artifact authoring — evidence-packet template, protocol README, ledger re-issue, and three root-cause conflict adjudications — under the v1.5 STOP-protocol governance.
**Confidence:** HIGH (every source consumed directly; no external/training-knowledge dependency)

## Summary

Phase 25 is a **documentation/process phase with zero code and zero framework-spec edits** (CONTEXT D-02). It instantiates the v1.4 Phase 16 evidence machinery for v1.5/issue-02 and adjudicates the three known cross-source conflicts at root cause. There is no library research, no package install, no environment dependency — the "stack" is the existing GSD planning conventions, the v1.4 precedent files, and `scripts/agent-commit`. The work product is a set of Markdown artifacts under `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/` plus an in-place re-issue of one block in `24-ISSUE-LEDGER.md`.

The phase splits cleanly into two deliverable groups (CONTEXT D-01): (A) **the machinery** — adapt v1.4 `_TEMPLATE.md` and `evidence/README.md`, encode the downstream packet-before-edit / phase-exit / re-verification rules, and re-issue the ledger's stale Lifecycle Rules block; and (B) **the three EVID-10 records** — full root-cause adjudications for SCS thresholds, `compute_globals D=6.694`, and the M11/M12 severity reclassifications. Per-finding packets/verdicts for the other 16 findings are explicitly deferred to their owning phases 26–28. All three conflicts are already resolved in spec-edit-ready prose by the candidate verdict source (`02-resolution-doc.md` §5.1, §4.4, §3.3/§4.1), so the EVID-10 work is *transcription with independent grounding against the four sources*, not original physics derivation — but each conflict touches a v1.4-locked convention, so the STOP protocol governs: an outcome that would *overturn* a locked convention is a STOP gap, never an autonomous verdict (CONTEXT D-09).

**Primary recommendation:** Plan three waves — (W1) machinery: template + README + ledger Lifecycle re-issue; (W2) the three EVID-10 records, each grounded against issue-doc + resolution-doc + framework-spec + DATA-xx and checked against the locked convention; (W3) wire-up: ledger Evidence-Packet links, ID→filename map in README, carry the five READY-WITH-CAVEATS caveats into affected packets. Treat `24.5-RESOLUTION-MAP.md` as the navigation contract — never read the 820-line resolution doc cold. Honor STOP: the three conflicts all *uphold* locked conventions in the candidate source (no overturn), so the expected outcomes are `reject-issue-doc`-style verdicts; but if grounding diverges from the candidate source, surface a gap rather than invent.

## Architectural Responsibility Map

Phase 25 has no software tiers. The analogue is **artifact ownership** — which document owns which contract, and which phase consumes it. This map prevents the planner from misassigning content (e.g., putting a spec edit in Phase 25, or pre-assigning Phase 26-28 verdicts).

| Capability | Primary Owner (this phase) | Downstream Consumer | Rationale |
|------------|---------------------------|---------------------|-----------|
| Evidence-packet schema | `evidence/_TEMPLATE.md` (Phase 25) | Phases 26–28 copy it per finding | Schema is machinery; instances are owned by editing phases (D-01/D-04) |
| Packet/verdict protocol + enforcement | `evidence/README.md` (Phase 25) | Phases 26–28 inherit as plan-level constraints | D-03: packet-before-edit, phase-exit gate, ledger-edit-in-commit |
| Re-verification / lifecycle rules | `24-ISSUE-LEDGER.md` Lifecycle block re-issue (Phase 25) | Phases 26–29 operate under it | VER-10; D-11 re-issues stale v1.4 applicability text |
| SCS threshold conflict record | EVID-10 record (Phase 25) | Phase 28 VAL-01 edit "per the EVID-10 record" | D-08 conflict 1; spec edit is Phase 28, not 25 |
| `D=6.694` conflict record | EVID-10 record (Phase 25) | Phase 27 PIPE-09 edit "per the EVID-10 record" | D-08 conflict 2; spec edit is Phase 27, not 25 |
| M11/M12 severity record | EVID-10 record (Phase 25) | Phase 26 prioritization (M11), Phase 27 (M12) | D-08 conflict 3; informs prioritization, no edit |
| The 16 non-conflict packets+verdicts | NOT Phase 25 | Phases 26–28 author them using the machinery | D-01: "evidence before editing" loop runs in owning phase |
| Any framework-spec edit | NOT Phase 25 (D-02 zero edits) | Phases 27–28 (ctl/pinn only) | EVID-10 stops at "locked convention in spec-edit-ready prose" |

## Standard Stack

Not applicable in the software sense. The "stack" is the set of existing conventions and precedent artifacts Phase 25 instantiates. No package install, no version verification, no registry — **the Package Legitimacy Audit and Environment Availability sections are SKIPPED** (no external dependencies; pure Markdown authoring + git).

### Tooling actually used

| Tool | Purpose | Why standard |
|------|---------|--------------|
| `scripts/agent-commit` | Mandatory commit path (`GIT_AGENT_ID` required) | Project governance; one atomic commit per plan (D-18) [VERIFIED: file exists, `scripts/agent-commit`] |
| gsd-tools handlers | STATE.md mutations only | Universal anti-pattern 15; never edit STATE.md by hand [CITED: CONTEXT code_context] |
| Native Write/Edit | Author Markdown artifacts | Standard for `.planning/` artifacts [ASSUMED — standard GSD practice] |

## Source Materials Map (the real research output)

This is the load-bearing section for the planner. Every Phase 25 artifact cites these by **path + section/line range** (EVID-06: never whole files).

### The four EVID-06 evidence sources (every packet cites all four)

| # | Source | Path | Role | Citation convention |
|---|--------|------|------|---------------------|
| 1 | Issue doc (NON-authoritative) | `pinn_instruction/issues/02-data-pipeline-and-validation.md` | §2 Source position (issue side) | line ranges, e.g. `:129-141` (SCS), `:235-275` (D listing), `:53-77` (BLOCKING table) [VERIFIED: read directly] |
| 2 | Resolution doc (candidate verdict source, NON-authoritative) | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | §2 Source position (resolution side) + §6 verdict candidate | §-number + Q-ID + line range, e.g. `§5.1 Q-C1:543-574`; line numbers anchored to committed 820-line revision [VERIFIED: read directly] |
| 3 | Framework specs (current; spec evidence) | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`, `pinn_architecture.md`; read-only `framework-revisions/data_quality_assessment.md` | §3 Spec evidence | line ranges; ctl `§2.5 line 598/608`, Step-4 table `line 1049`; DQA `§3.1` (sole written home of SCS gate) [CITED: resolution-doc §-cites; not independently line-verified this session] |
| 4 | Verified dataset facts (EVID-06 fourth source — NEW vs v1.4) | `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` | NEW §3b Dataset evidence | cite CLM rows, e.g. `CLM-03` (65 blacklist), `CLM-10` (medians 61/127/1003), `CLM-13` (PENDING — D=6.694 not probed) [VERIFIED: read directly] |

### Navigation + verdict-direction (consume FIRST, before the 820-line doc)

| Artifact | Path | What it gives Phase 25 |
|----------|------|------------------------|
| Resolution map | `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-RESOLUTION-MAP.md` | §1 section index, §2 finding→section table, §3 citation guide, §4 verdict-direction preview, §6 caveats. The navigation contract (D-16). [VERIFIED: read directly] |
| Readiness report | `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-READINESS-REPORT.md` | Verdict READY-WITH-CAVEATS; the 5 caveats to carry forward (D-15). [VERIFIED: read directly] |

### Machinery precedent (instantiate, don't redesign)

| Artifact | Path | Adaptation |
|----------|------|------------|
| v1.4 packet template (12-section) | `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | D-04 substitutions: §2 cite both issue-02 sources; §3 ctl/pinn/DQA lines; **NEW §3b dataset evidence (CLM rows)**; §4 FUT-01 note unchanged; §5-9 EVID-10 sections required when `Sources Disagree?=YES`; §6 verdict enum verbatim; §10 before/after doubles as EVID-08 false-positive record [VERIFIED: read directly] |
| v1.4 protocol README | `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` | D-03/D-05: adapt verdict enum, status lifecycle, EVID-10 trigger table, regression policy, phase-exit rule, AC-ID policy, packet-start procedure. Add ID→filename map (Claude's discretion). [VERIFIED: read directly] |

## The Three EVID-10 Conflicts (phase center of gravity)

Each must produce a complete EVID-10 record: first-principles check, named root-cause ambiguity, locked convention in spec-edit-ready prose, per-claim which-source-right/wrong. All three **uphold a locked convention** in the candidate source → expected verdict direction is "reject the issue-doc proposal." None *overturns* a locked convention → none is an automatic STOP gap, but the planner must keep D-09's guard.

### Conflict 1 — SCS thresholds (→ Phase 28 VAL-01)

| Field | Value |
|-------|-------|
| Issue-doc position | ratio thresholds `SCS > 1e-6` reject / `< 1e-8` tighten — `02-data-pipeline-and-validation.md:129-141` |
| Resolution-doc verdict | accept locked gate verbatim, reject issue-doc numbers — `02-resolution-doc.md §5.1 Q-C1:543-574` |
| Locked convention (HC-5) | `ε_H = max|(H(t)−H(0))/H(0)|`; `SCS = log₁₀(ε_H)`; reject `SCS > −5` (≡ `ε_H > 1e-5`) |
| Spec evidence | locked gate's **sole written home** is read-only `data_quality_assessment.md §3.1` (SI-DQA-003) — citable, never editable (SCOPE-09) |
| Dataset evidence | resolution doc notes addendum is silent by design (convention, not a count) — no CLM row |
| Root-cause ambiguity | `1e-6` = the dqa Acceptable/Marginal **band boundary mis-promoted to a reject gate**; `1e-8` has **no source anywhere in the package** |
| Which right/wrong | issue doc wrong on both numbers; locked gate right; resolution doc's diagnostic disposal correct (`1e-6` = real band edge mislabeled, `1e-8` = unsourced) |
| Expected verdict | `accept-resolution` (which itself upholds the locked gate / rejects issue doc) |

**STOP note:** the SCS row in `24-ISSUE-LEDGER.md` already carries `Sources Disagree? = YES — EVID-10 required`. Phase 28's VAL-01 edit must create a canonical SCS contract in editable specs (ctl) **without touching DQA** — that is precisely why the root-cause record matters before the edit (CONTEXT specifics).

### Conflict 2 — `compute_globals` D=6.694 (→ Phase 27 PIPE-09)

| Field | Value |
|-------|-------|
| Issue-doc position | `D = cbrt(G·M_tot·t_max²) = 6.694`, P1-7 — `02-data-pipeline-and-validation.md:235-275, 289, 306, 317` |
| Resolution-doc verdict | reject 6.694 / any `M_tot_ref` param; lock raw-mass `D ≈ 4.6416` — `02-resolution-doc.md §4.4 Q-B4:493-536` |
| Locked convention (HC-6 / PHYS-01) | `D = (G·T²)^(1/3) ≈ 4.6416` (G=1, T=10) |
| Spec evidence | `ctl_instruction.md §2.5 line 598` **explicitly rejects** the 6.694 form; `E_scale` 3-way conflict (`+1e-10` at line 608 outlier vs `+1e-8` at Step-4 table line 1049 + `pinn_architecture.md §5.2 line 761`) |
| Dataset evidence | `24-VERIFIED-FACTS.md` CLM-13 = **PENDING, not probed** (contested convention, not a dataset count); routed Phase 25 EVID-10 / Phase 27 PIPE-09 |
| Root-cause ambiguity | the issue-doc listing is **internally inconsistent** (mass-fraction D with raw-mass energies — dimensionless in neither convention); the arithmetic for 6.694 is *correct* but the convention is the rejected one |
| Which right/wrong | issue-doc arithmetic right, convention wrong; listing has 3 verified defects (mixed convention, additive-ε anti-pattern, E_scale outlier); locked raw-mass D right |
| Expected verdict | `accept-resolution` / reject-issue-doc; **formal ratification of CLM-13 is OI-11 — this is the EVID-10 step that ratifies it** |

**STOP note:** D-09 — an outcome that would adopt 6.694 would overturn PHYS-01/HC-6 = STOP gap. The candidate source does NOT recommend that (it rejects 6.694), so no overturn; proceed. The `E_scale = 1e-8` canonicalization is a 2-of-3 editable-spec choice flagged by the resolution doc for spec-author sign-off — that is a **Phase 27 edit decision**, not a Phase 25 verdict; record it in the EVID-10 prose, do not lock it as a Phase 25 spec change.

### Conflict 3 — M11 / M12 severity reclassifications (→ Phase 26 prioritization / Phase 27)

| Field | Value |
|-------|-------|
| Issue-doc position | M11 & M12 reclassified **audit MAJOR → BLOCKING**; dedicated "Severity Reclassification Ledger" — `02-data-pipeline-and-validation.md:59-60, 70-77` |
| Resolution-doc verdict | M12 BLOCKING claim is **wrong** on verified arithmetic (`§4.1 Q-B1:385-422`); M11 contract is blocking-grade but **"whether the MAJOR→BLOCKING reclassification stands is EVID-10's call"** (`§3.3 Q-A3:238`) |
| Spec evidence | M12: `ctl` Mini-Batch Construction lines 1197-1201; `pinn_architecture.md §3.1`. M11: dqa §5.1 gate-before-analysis ordering |
| Dataset evidence | M12: `24-VERIFIED-FACTS.md` CLM-10 medians **61/127/1003** (std min 59) → 32 distinct points from 59-61 is trivially feasible → BLOCKING-infeasibility claim falsified. M11: CLM-03 = 65 blacklist confirmed; consumption status `unverified — SCOPE-10` (OI-8) |
| Root-cause ambiguity | M12: issue doc conflated data-loss sample with collocation budget; its own checklist contradicts P1-4 (expects gold→128). M11: severity is a *process classification*, not a data fact — the resolution doc explicitly hands the reclassification decision to EVID-10 |
| Which right/wrong | M12: underlying observation real, BLOCKING reclassification + P1-4 `0.5×` factor wrong (unevidenced). M11: contract is blocking-grade (correct); the MAJOR→BLOCKING label is the EVID-10 ruling Phase 25 must make |
| Expected verdict | M12: `accept-third-position` / reject-issue-doc-as-posed. M11: Phase 25 makes the severity ruling explicitly (this is the one place the resolution doc defers TO Phase 25) |

**STOP note:** the M11 reclassification is the only one the candidate source explicitly routes to Phase 25 as "EVID-10's call." This is a **process-classification decision**, not a spec edit — Phase 25 owns it (CONTEXT specifics: M11/M12 record informs Phase 26 prioritization, D-02). Ground it in the data integrity argument (resolution §3.3 part 2), not architectural-harm narratives (resolution flags those as "not load-bearing").

**§6 F-3 cross-reference:** `02-resolution-doc.md §6 F-3 (line 740)` is the consolidated "issue-doc internal-defect catalog (for EVID-10)" — it itemizes 8 defects feeding the three conflicts. Cite it as supporting evidence in all three EVID-10 records.

## Architecture Patterns

### Artifact-flow diagram

```
                    24.5-RESOLUTION-MAP.md  (navigation contract — read FIRST)
                              │  finding→section, citation guide, verdict-direction
                              ▼
   ┌──────────────── EVID-06 four-source citation ────────────────┐
   │                                                              │
issue-02.md   02-resolution-doc.md   ctl/pinn/DQA specs   24-VERIFIED-FACTS.md
 (§2 issue)    (§2 resol. + §6 cand.)   (§3 spec)            (§3b dataset — NEW)
   │                  │                    │                     │
   └──────────────────┴──────────┬─────────┴─────────────────────┘
                                  ▼
              evidence/_TEMPLATE.md  ──copy──▶  evidence/{finding-id}.md
              (12-section, D-04)                (3 EVID-10 records this phase;
                                  │              16 others by Phases 26-28)
                                  ▼
              evidence/README.md (protocol: enum, lifecycle, EVID-10 trigger,
                                  regression, phase-exit, AC-ID, ID→filename map)
                                  │
                                  ▼
              24-ISSUE-LEDGER.md  (re-issue Lifecycle block for v1.5 phases 26-29;
                                   fill Evidence-Packet links; status transitions
                                   in same commit as underlying change)
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
        Phase 26 (PIPE)     Phase 27 (PIPE)     Phase 28 (VAL)
        consumes machinery + EVID-10 records; authors per-finding packets;
        lands the actual ctl/pinn spec edits
```

### Recommended artifact structure

```
.planning/phases/25-evidence-framework-and-issue-ledger/
├── 25-RESEARCH.md                 # this file
├── 25-CONTEXT.md                  # exists (decisions D-01..D-18)
├── 25-DISCUSSION-LOG.md           # exists
├── 25-GAPS.md                     # create ONLY on first STOP gap
├── 25-PLAN.md (+ 25-NN-PLAN.md)   # planner output
└── evidence/
    ├── _TEMPLATE.md               # adapted v1.4 12-section schema (D-04)
    ├── README.md                  # protocol doc (D-03/D-05) + ID→filename map
    ├── scs-thresholds.md          # EVID-10 conflict 1 (or SCS.md)
    ├── compute-globals-D.md       # EVID-10 conflict 2 (D-60: sanitized name)
    └── m11-m12-severity.md        # EVID-10 conflict 3 (or a packets+summary form, D-62)
```

### Pattern: EVID-10 record = transcribe-with-grounding, not derive

The resolution doc already supplies first-principles checks, root-cause names, and spec-edit-ready prose for all three conflicts. The pattern is: **cite the candidate source's reasoning, then independently confirm against spec lines + DATA-xx + a short first-principles check, then record the verdict.** The candidate source's agreement is NOT itself the verdict (RESOLUTION-MAP §3 authority reminder). Do not re-derive the physics from scratch; do confirm the arithmetic (e.g., 32 ≤ 59 for M12; `D³ = GT²` ⇒ 4.6416 for D=6.694).

### Anti-patterns to avoid

- **Pre-assigning the 16 non-conflict verdicts in Phase 25.** D-01 rejects the literal reading of criteria 1-3. ⚠ This is flagged in CONTEXT D-01 for user review — if the user prefers the literal reading, the phase must be replanned. The planner should treat D-01's split reading as the working assumption but surface the flag.
- **Editing any framework spec.** D-02: zero spec edits. EVID-10 stops at spec-edit-ready prose.
- **Editing DQA or sampling_method.md.** SCOPE-08/09. DQA is citable (SCS gate's written home), never editable.
- **Citing `pinn/` live code as evidence.** SCOPE-10. Only §4 FUT-01 hand-off notes may reference it, forward-pointing.
- **Rebuilding the ledger.** D-06/D-11: it is operated and re-issued in place, never rebuilt. Only the Lifecycle Rules block's stale applicability text changes ("Phases 17-22, including Phase 20.5" → v1.5 phases 26-28 + 29).
- **Inventing where the resolution doc is silent/hedged.** D-10: route to `defer-with-blocker` or a STOP gap. The doc's Open Items register (`§ lines 756-779`) and OI-7 (M13 STOP-gap defeater) are explicit silence markers.
- **Writing gap registers as a subagent.** Subagents return findings to the parent; only the parent writes `25-GAPS.md` / `v1.5-GAPS.md`.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Packet schema | New 12-section design | Copy/adapt v1.4 `_TEMPLATE.md` | D-04: "no structural redesign"; only the D-04 substitutions |
| Protocol doc | New protocol from scratch | Adapt v1.4 `evidence/README.md` | enum, lifecycle, regression, phase-exit all carry over verbatim |
| Verdict enum | New verdict vocabulary | EVID-07 fixed set exactly | `accept-resolution \| accept-issue-doc \| accept-third-position \| reject-both-as-unsupported \| defer-with-blocker` |
| Status state machine | New lifecycle | Ledger's existing `PENDING→IN_PROGRESS→FIX_APPLIED→VERIFIED` (+DEFERRED) | D-11: keep verbatim; only re-issue stale applicability text |
| Navigation into the 820-line doc | Re-read/re-index the doc | `24.5-RESOLUTION-MAP.md` §1-§4 | D-16: the map is the navigation contract |
| Dataset evidence | Re-derive counts | Cite `24-VERIFIED-FACTS.md` CLM rows | packets cite rows, never re-probe |
| AC-IDs | Mint new ones | Seeded AC-PIPE-01..10, AC-VAL-01..04 | D-13: Phase 25 mints no new AC-IDs |

**Key insight:** Phase 25's entire value is *fidelity to existing structure*. Every artifact is an adaptation of a committed v1.4 precedent or a consumption of a Phase 24/24.5 deliverable. The only genuinely new content is the three EVID-10 records and the §3b dataset-evidence section — and even those transcribe a candidate verdict source.

## Runtime State Inventory

> Phase 25 is not a rename/refactor of running systems, but it *operates* on a live planning artifact (the ledger) and creates a directory that downstream phases write into. This adapted inventory captures the stateful surfaces.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data (committed artifacts edited in place) | `24-ISSUE-LEDGER.md` (19 rows; Lifecycle Rules block carries stale v1.4 text "Phases 17-22, including Phase 20.5"; Evidence-Packet column all `—`) | D-11 re-issue Lifecycle block (state machine verbatim, applicability → 26-29); fill Evidence-Packet links as packets land; status transitions in same commit (D-06) |
| Live planning state | STATE.md (Phase 24.5 complete, Phase 25 queued/unblocked per memory 1065/1067) | Mutate ONLY via gsd-tools handlers (anti-pattern 15); never hand-edit |
| Cross-phase write surface | `evidence/` directory created by Phase 25, **written into by Phases 26-28** | README must document the ID→filename mapping so downstream phases write consistent filenames (Claude's discretion) |
| Caveats to propagate | READY-WITH-CAVEATS caveats OI-3, OI-6, OI-7, OI-8, OI-11 (D-15) | Carry each into the affected finding's packet before that finding is adjudicated; OI-11 (CLM-13) lands in the D=6.694 EVID-10 record |
| Git tag | `v1.5-pre-phase-25` (D-17) | Cut from `milestone/v1.5` HEAD at **execution start, after 24.5 passes** — NOT during planning |
| ID-namespace collision risk | issue-01 (v1.4) and issue-02 (v1.5) both use e.g. "B-06" | Every cross-document citation must be directory-qualified; no path collision (separate `evidence/` dirs) but cite-time confusion possible (CONTEXT specifics) |

**Nothing found:** No databases, no OS-registered state, no secrets/env vars beyond `GIT_AGENT_ID` (required by `scripts/agent-commit`, unchanged), no build artifacts. Verified by direct read of the ledger, CONTEXT, and config.

## Common Pitfalls

### Pitfall 1: Literal vs split reading of criteria 1-3
**What goes wrong:** Planner reads success criteria 1-3 as "Phase 25 authors all 19 packets + verdicts" and plans a full-adjudication phase.
**Why it happens:** Criteria 1-3 restate EVID-06..09 verbatim and admit a literal exit-condition reading (CONTEXT D-01 flag).
**How to avoid:** Use D-01's split reading (machinery + 3 EVID-10 records only). Surface the ⚠ flag so the user can confirm; do not silently pick. If user wants literal reading, replan.
**Warning signs:** A plan with 19 packet-creation tasks.

### Pitfall 2: Treating the candidate verdict source as authoritative
**What goes wrong:** Recording `accept-resolution` because the resolution doc says so, without grounding.
**Why it happens:** The doc is well-reasoned and READY-WITH-CAVEATS.
**How to avoid:** RESOLUTION-MAP §3 authority reminder — cite empirical grounding (CLM rows, spec lines) alongside the doc's recommendation; the doc's agreement is not the verdict (D-09).
**Warning signs:** An EVID-10 record whose only §3/§3b evidence is "resolution doc §X says".

### Pitfall 3: Inventing a verdict where the source is silent
**What goes wrong:** Forcing a verdict on an OI-routed or hedged facet (e.g., M13 fallback policy, calibration constants OI-3).
**Why it happens:** Pressure to "complete" every finding.
**How to avoid:** D-10 — silence/hedge → `defer-with-blocker` or STOP gap in `25-GAPS.md`. The doc's Open Items register and OI-7 STOP-gap defeater are explicit silence markers. (Note: M13 fallback is Phase 26's STOP-gap candidate, not Phase 25's — but if a Phase 25 EVID-10 facet hits silence, defer.)
**Warning signs:** A packet that resolves an OI-3/OI-6/OI-7 item autonomously.

### Pitfall 4: Letting a STOP-gap-worthy overturn slip through as a verdict
**What goes wrong:** An adjudication outcome that overturns PHYS-01/HC-5/HC-6.
**Why it happens:** Following the issue doc's reasoning too far.
**How to avoid:** D-09 — locked conventions are hard constraints; an overturn is a STOP gap for user decision, never an autonomous verdict. All three conflicts *uphold* the locked convention in the candidate source, so none should overturn; if your grounding diverges, that divergence IS the gap.
**Warning signs:** A draft verdict of `accept-issue-doc` on SCS or D=6.694.

### Pitfall 5: Ledger status edit detached from the underlying change
**What goes wrong:** Status transition committed separately from the packet/edit it reflects.
**Why it happens:** Forgetting the same-commit discipline.
**How to avoid:** D-06 / v1.4 D-04 — ledger status edits travel in the same commit as the underlying change, logged `date SHA status→status (actor/plan)`.
**Warning signs:** A commit touching only the ledger Status column.

### Pitfall 6: Re-issuing more of the Lifecycle block than the stale text
**What goes wrong:** "Improving" the state machine or batch definition while fixing the stale applicability.
**Why it happens:** Adjacent-code-improvement reflex.
**How to avoid:** D-11 — keep the state machine, batch definition, regression policy, and phase-exit gate **verbatim**; change only "Phases 17-22, including Phase 20.5" → v1.5 phases. Note the change in the ledger Notes section.
**Warning signs:** A ledger diff touching the state-machine prose.

## State of the Art

This is a project-internal process phase, not a moving technology domain. The relevant "state of the art" is the v1.4 → v1.5 evolution of the evidence machinery:

| v1.4 (Phase 16) | v1.5 (Phase 25) | Impact |
|-----------------|-----------------|--------|
| 3 evidence sources (issue, resolution, spec) | **4 sources** — adds §3b dataset evidence (DATA-xx / CLM rows) | EVID-06 fourth source; packets cite verified empirical facts |
| EVID-05 conflict trigger | EVID-10 (continues numbering) | Same machinery, new requirement IDs |
| ctl_pinn_resolution.md candidate source | 02-resolution-doc.md candidate source | Same standing, different doc |
| EVID-05 triggers: B-02/B-04/B-09/M5 (physics) | EVID-10 conflicts: SCS / D=6.694 / M11-M12 (data-pipeline) | Conflicts pre-flagged in ledger `Sources Disagree?=YES` |
| sampling_method.md editable | sampling_method.md FROZEN (SCOPE-08); DQA read-only (SCOPE-09) | narrower edit surface; DQA citable-not-editable |

**Deprecated/outdated in the seeded ledger:** the Lifecycle Rules block's "Phases 17-22, including Phase 20.5" applicability text (v1.4 carryover) — D-11 fixes it.

## Validation Architecture

> nyquist_validation is `true` in config. Phase 25 produces **no executable code and no acceptance-check execution** (that is Phase 29, VER-09). "Validation" here is artifact-completeness verification, not a test suite.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None — no code in this phase. Verification is doc-completeness review + git invariants. |
| Config file | n/a |
| Quick run command | `bash scripts/agent-commit` precondition check (`GIT_AGENT_ID` set); `git diff --check` |
| Full suite command | n/a — AC execution is Phase 29 |

### Phase Requirements → Verification Map
| Req ID | Behavior | Verification Type | How verified (Phase 25) | Artifact |
|--------|----------|-------------------|--------------------------|----------|
| EVID-06 | 4-source line-range citations per packet | doc review | each EVID-10 record cites issue+resolution+spec+DATA-xx with line ranges | the 3 records |
| EVID-07 | verdict from fixed enum | doc review | each record has exactly one enum value | the 3 records |
| EVID-08 | false positives documented | doc review | §10 before/after = false-positive record for any no-change | template §10 + records |
| EVID-09 | before/after note per accepted finding | doc review | §10 names changed spec section + contract + verification step | records |
| EVID-10 | root-cause adjudication for the 3 conflicts | doc review | each record has first-principles + root-cause + locked convention + right/wrong | 3 records |
| VER-10 | ledger lifecycle + re-verification rule | doc review | Lifecycle block re-issued; state machine + regression + phase-exit present | ledger |

### AC IDs (reserved, NOT executed here)
Phase 25 mints **no new AC-IDs** (D-13). EVID-10 records verify through the owning phase's seeded check: D=6.694 → AC-PIPE-09; SCS → AC-VAL-01; M11/M12 → AC-PIPE-03/04. Numeric pass criteria are VER-07 (owning phases); execution is Phase 29 (VER-09).

### Wave 0 Gaps
- [ ] `evidence/_TEMPLATE.md` — does not exist yet; create from v1.4 precedent (D-04)
- [ ] `evidence/README.md` — does not exist yet; create from v1.4 precedent (D-03/D-05)
- [ ] `25-GAPS.md` — create only on first STOP gap (do not pre-create)
- *(No test-framework install needed — non-code phase.)*

## Security Domain

> `security_enforcement` is not present in config; this is a documentation phase with no auth, network, input-parsing, or cryptography surface. No ASVS category applies. The only "security-adjacent" control is governance integrity (no spec drift, no invented verdicts), enforced by the STOP protocol and the same-commit ledger discipline — not by a security library. **Section otherwise N/A.**

## Project Constraints (from CLAUDE.md / AGENTS.md)

Binding directives the planner must honor (same authority as locked decisions):

- **STOP protocol in full** — source-silent semantic / process-schema / cross-phase decisions are surfaced as gaps, never invented. Phase 25 is a v1.5 adjudication phase under "CRITICAL GOVERNANCE" v1.5 applicability. Subagents return findings; only the parent writes `25-GAPS.md` + `.planning/milestones/v1.5-GAPS.md`.
- **Grounding test** — a decision is grounded only via: resolution doc, issue doc, prior user decision (LOCKED CONTEXT / RESOLVED-WITH-INSTRUCTION gap), planning artifact, a v1.4/v1.5-revised framework-spec section, or short first-principles. **`pinn/` live code is NOT grounding** (SCOPE-10).
- **Spec-edit targets** — `ctl_instruction.md` and `pinn_architecture.md` ONLY, and Phase 25 makes ZERO of them (D-02). `sampling_method.md` frozen (SCOPE-08); `data_quality_assessment.md` read-only (SCOPE-09).
- **Commit protocol** — use `scripts/agent-commit` (requires `GIT_AGENT_ID`); never raw `git commit`, never `--no-verify`. One atomic commit per plan (D-18). Scope `25` / `25-NN`. `docs`/`plan` types require a body. STATE.md only via gsd-tools handlers.
- **Branch awareness** — work on `milestone/v1.5`; surface git state before destructive ops (none expected in this phase).
- **docs/ placement** — Phase 25 writes under `.planning/`, not `docs/`. If any narrative doc were ever written to `docs/`, the frontmatter + purpose-folder rules apply — but this phase has no `docs/` output.

## Assumptions Log

> Claims tagged `[ASSUMED]` that the planner/discuss-phase should confirm. Most of this research is `[VERIFIED]` (read directly) or `[CITED]` (resolution-doc §-cites).

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Framework-spec line numbers (ctl §2.5 line 598/608, Step-4 1049, pinn §5.2 761) are taken from the resolution doc's self-cites, not independently line-verified this session | Source Materials Map / Conflict 2 | LOW — packets re-verify spec lines at authoring time; line numbers may have shifted if ctl/pinn changed since the doc was written |
| A2 | Native Write/Edit is the correct authoring tool for `.planning/` artifacts | Standard Stack | LOW — standard GSD practice; no contrary directive |
| A3 | The three EVID-10 records may be 3 separate packets OR packets-plus-summary (Claude's discretion per D-62) — research recommends 3 separate files for greppability | Recommended artifact structure | LOW — explicitly Claude's discretion in CONTEXT |

**Note:** No `[ASSUMED]` claim here touches a compliance/retention/security/performance target — all such surfaces are absent in this phase. The substantive verdicts (the 3 conflicts) are grounded in directly-read sources, not assumptions.

## Open Questions

1. **Literal vs split reading of criteria 1-3 (CONTEXT D-01 ⚠ flag)**
   - What we know: D-01 adopts the split reading (machinery + 3 records); the basis is roadmap structure + Phase 27/28 "per the EVID-10 record" wording + v1.4 precedent.
   - What's unclear: the user has not yet confirmed; criteria 1-3 admit a literal reading.
   - Recommendation: plan to D-01's split reading; surface the flag in the plan summary for user confirmation before execution. This is a planning-input question, not a STOP gap.

2. **EVID-10 record granularity (D-62, Claude's discretion)**
   - What we know: each conflict needs a complete EVID-10 record at a citable path; 3 separate packets or packets+summary both allowed.
   - Recommendation: 3 separate files (`scs-thresholds.md`, `compute-globals-D.md`, `m11-m12-severity.md`), greppable by finding ID, consistent with v1.4 one-file-per-finding. Record ID→filename in README.

3. **M11 severity ruling is the one verdict the resolution doc defers TO Phase 25**
   - What we know: `§3.3:238` says "whether M11's MAJOR→BLOCKING reclassification stands is EVID-10's call."
   - What's unclear: nothing source-silent — the data-integrity argument (resolution §3.3 part 2) grounds a BLOCKING-grade contract ruling.
   - Recommendation: make the ruling explicitly in the EVID-10 record, grounded on data integrity (not architectural-harm narratives, which the doc flags as non-load-bearing). Not a STOP gap.

## Sources

### Primary (HIGH confidence — read directly this session)
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` — §3.3 (M11), §4.1 (M12), §4.4 (D=6.694), §5.1 (SCS), §6 F-3 defect catalog, Open Items register
- `pinn_instruction/issues/02-data-pipeline-and-validation.md` — BLOCKING/MAJOR tables, Severity Reclassification Ledger (lines 53-77), SCS thresholds (129-141), compute_globals listing (235-275)
- `.planning/phases/25-evidence-framework-and-issue-ledger/25-CONTEXT.md` — decisions D-01..D-18, canonical refs
- `.planning/REQUIREMENTS.md` — EVID-06..10, VER-10, SCOPE-06..11, source-treatment policy
- `.planning/ROADMAP.md` — Phase 25 detail, verification protocol (25-29), source-treatment & STOP protocol
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` — 19 findings, Lifecycle Rules, per-finding notes
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` — CLM-01..13, DATA-05 row
- `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-RESOLUTION-MAP.md` — navigation + citation guide + verdict-direction
- `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-READINESS-REPORT.md` — READY-WITH-CAVEATS, OI caveats
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` and `evidence/README.md` — the machinery to instantiate
- `CLAUDE.md` / `.claude/rules/*` — governance, repo map, pinn reference

### Secondary (MEDIUM confidence)
- Resolution-doc self-cited framework-spec line numbers (A1) — re-verify at authoring time

### Tertiary (LOW confidence)
- None — no WebSearch or external sources used; this phase has no external dependency

## Metadata

**Confidence breakdown:**
- Machinery (template/README/ledger): HIGH — v1.4 precedents read directly; D-04/D-03/D-11 are explicit
- Three EVID-10 conflicts: HIGH — all four sources read directly; verdict directions confirmed by RESOLUTION-MAP §4 and resolution-doc sections
- Source materials map: HIGH for paths/sections (read directly); MEDIUM for exact spec line numbers (resolution-doc self-cites, A1)
- STOP-protocol handling: HIGH — governance read directly; the three conflicts all uphold (not overturn) locked conventions

**Research date:** 2026-06-11
**Valid until:** 2026-07-11 (30 days — stable internal artifacts; re-verify only if `02-resolution-doc.md` is re-delivered, per RESOLUTION-MAP §re-check)
