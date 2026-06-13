---
phase: 26-dataloader-ingestion-and-selection-contracts
plan: 04
subsystem: framework-specs / data-pipeline contracts
tags: [PIPE-05, M13, gold-counterpart, STOP-gap, label-semantics, OI-7a, ctl_instruction, adjudication]
requires: ["26-01 (Step-1A admission gate + B-11 id_to_path)", "26-02 (Step-1 item-7 record_key keying)"]
provides: ["PIPE-05 mandatory data-side gold-counterpart contract (ctl_instruction.md Step 5)", "AC-PIPE-05 definition + passing set-difference probe", "M13 defer-with-blocker verdict", "GAP-26-NN draft (parent-recorded)"]
affects: ["Phase 28 Q-C2 SASD resample queue (gold-rerun selection input, OI-7b)", "Phase 29 VER-09 acceptance suite", "FUT-01 DataLoader stratum builder"]
tech_stack:
  added: []
  patterns: ["packet-before-edit", "D-12 adopt-or-defer decision rule", "three-question understanding check (STOP step 2)", "OI caveat propagation (D-13)", "mandatory-contract-lands-regardless-of-path"]
key_files:
  created:
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/m13-gold-counterpart.md
  modified:
    - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md
    - .planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md
decisions:
  - "M13 verdict defer-with-blocker (path b): the fallback choice is source-conflicting (3-way upstream split, Medium confidence, resolution doc routes OI-7a to the framework owner); per ROADMAP success criterion 4 it is surfaced as a STOP gap, not invented"
  - "Mandatory data-side gold-counterpart contract landed UNCONDITIONALLY in ctl_instruction.md Step 5 per 02-resolution-doc.md:262 (set-difference gold-missing set, per-physical_key gold_counterpart, gold-folder-iterated Stage-5 stratum, no silent base->gold substitution)"
  - "The conditional fallback text (02-resolution-doc.md:274-290) was deliberately NOT landed: its precondition (a settled label-semantics ruling) is unmet"
  - "B-11's landed record_key annotation (ctl:1228) settles the key-TYPE axis, NOT the OI-7a obligation-granularity axis; reading it as disposing of the M13 defeater would be invention by side-effect (T-26-14)"
  - "M13 set IN_PROGRESS-with-note (not DEFERRED) by orchestrator directive: data-side contract FIX_APPLIED + AC-PIPE-05 verified, fallback policy pending parent-recorded STOP gap; G4 left unclosed"
metrics:
  duration: "~30 min"
  completed: 2026-06-13
  tasks: 3
  files: 4
---

# Phase 26 Plan 04: Gold-Counterpart Contract (PIPE-05 / M13) Summary

PIPE-05 adjudicated under the D-12 decision rule: the **mandatory data-side gold-counterpart contract** is locked into `ctl_instruction.md` Step 5 (set-difference gold-missing set cross-checked vs the CLM-04 184-ID list, per-`physical_key` `gold_counterpart`, gold-folder-iterated Stage-5 stratum, no silent base→gold substitution) and verified by a passing AC-PIPE-05 probe (184/184). The **fallback policy** is the pre-registered STOP gap: the OI-7a label-semantics ruling (do Stage-5 labels attach to *simulations*/`record_key` or to *IDs*?) is source-conflicting, so M13 is `defer-with-blocker` and the ruling is **NOT invented** — the full GAP-26-NN field set is returned to the orchestrator (parent) for recording.

## Which path: PATH (b) — defer-with-blocker

The fallback choice is **source-conflicting**, the pre-registered expectation:
- The resolution doc assigns **Medium** confidence (`02-resolution-doc.md:270`), names Q-A4 the **#1** question warranting the unavailable R1–R8 reports, and records a **genuine three-way upstream split** (entailment 3 / STOP-gap 4 / fallback 1) (`:292`, `:777`).
- The resolution doc **declines to rule** the OI-7a label-semantics question; it preserves the defeater verbatim (`:263`) and routes the ruling to the framework owner (`OI-7:768`).
- The two primary sources **conflict** at the hinge: the issue doc presupposes per-ID Stage-5 obligation (fallback required, `:316`); the resolution doc derives the per-simulation no-fallback reading but only conditionally.
- The spec's own words "each simulation ID" (`ctl_instruction.md:1227`) are genuinely ambiguous.

Per D-12(b) and ROADMAP Phase 26 success criterion 4 (`.planning/ROADMAP.md:196`), this is surfaced as a STOP gap for user decision. The label-semantics ruling is not invented.

## Three-question understanding check (STOP step 2) — documented in the packet

1. **Math/engineering at stake:** the disputed semantic is the **domain** of the Step-5 stage map — simulations-that-exist-on-disk (per-`record_key`) vs the abstract ID space (per-ID, every Stage-4 ID owes a Stage-5 sample). The two readings produce different Stage-5 stratum composition (2,565 vs 2,565+184) and decide whether base records are ever substituted into gold slots and whether Stage 6 becomes a missing-gold bucket.
2. **Why the readings differ downstream:** stratum membership, substitution behavior, and Stage-6 semantics all change — a semantic decision, not presentation.
3. **Sources consulted and why they did not answer:** `02-resolution-doc.md:259,263,266,270,768,777` (preserves the defeater, declines to rule, Medium confidence, routes to framework owner); `ctl_instruction.md:1227` (ambiguous hinge); the B-11 edit at `:1228` (settles key-TYPE, NOT obligation-granularity — distinct axis); `issues/02-data-pipeline-and-validation.md:65,287,316` (presupposes the per-ID reading without arguing it); `ROADMAP.md:196` (controls: conflicting ⇒ STOP gap).

**Tempted to:** read B-11's landed `record_key` annotation as settling OI-7a for the per-simulation reading. **Rejected** — B-11 adjudicated key TYPE (content key vs positional index), not obligation granularity; treating it as also disposing of the M13 defeater is invention by side-effect (threat T-26-14).

## What was done

1. **M13 evidence packet** (`evidence/m13-gold-counterpart.md`) — 12-section packet authored from a full read of resolution-doc §3.4 Q-A4 (`:255-293`) + OI-7 (`:768`). Both primary sources cited with line ranges; §3 cites `ctl_instruction.md:1227` (hinge) + `:229-249` (stratification) + `:413-427` (B-11 item 7); §3b cites CLM-04:18 + CLM-05b:20. OI-7a (label-semantics defeater) and OI-7b (gold-rerun resourcing, user gate) propagated (D-13). Verdict `defer-with-blocker`. README ID→filename map row added.

2. **`ctl_instruction.md` Step 5 edit (the contract, lands regardless of path):** the mandatory data-side gold-counterpart contract (4 clauses: set-difference gold-missing set cross-checked vs the 184-ID list and never hard-coded; per-`physical_key` `gold_counterpart ∈ {present, absent}`; Stage-5 stratum built by iterating the gold folder's actual files; no silent base→gold substitution) + a **neutral UNRESOLVED note** stating the fallback policy is pending the OI-7a framework-owner ruling and recorded as a STOP gap. The conditional fallback text (`:274-290`) was deliberately NOT landed (its precondition is unmet).

3. **AC-PIPE-05 probe (mandatory contract verification)** — reused `data03_gold_gap.py`. **PASS:** `base_minus_gold_count=184`, `doc_listed_id_count=184`, `intersection_matches_set_diff: true` (184/184 exact match vs `standard_quasi_random_ids_not_in_gold.md`), base 2,749 / gold 2,565. Captured re-derivably in the packet (D-15, run 2026-06-13T06:34:40Z).

4. **AC-PIPE-02 regression re-check (D-08)** — `grep -nE 'id_to_path|record_key|physical_key|array index'` confirms B-11 Step 1 item 7 (`:413-427`) intact: dual keys, anchored regex, array-index prohibition (`:423`), `range(n_files)` prohibition (`:424`), Step-5 `record_key` cross-ref (`:1228`). **B-11 stays VERIFIED; no regression.**

5. **Ledger transitions** — M13 PENDING → IN_PROGRESS with note (defer-with-blocker verdict, packet link, mandatory contract FIX_APPLIED + AC-PIPE-05 verified, fallback policy UNRESOLVED pending OI-7a STOP gap). G4 PENDING → IN_PROGRESS (close-with-parent M13, inherits the pending disposition). Neither set to DEFERRED.

## Governance posture (CRITICAL)

- **Gap registers NOT written by this executor.** Per project governance (subagents return findings; only the parent writes gap registers) and threat T-26-16, this executor did NOT create or edit `26-GAPS.md` or `.planning/milestones/v1.5-GAPS.md`. The full GAP-26-NN field set is returned to the orchestrator for recording.
- **Label-semantics ruling NOT invented** (T-26-14). No fallback policy asserted in the spec; only a neutral UNRESOLVED note.
- **M13 IN_PROGRESS, not DEFERRED**, per orchestrator directive: the mandatory data-side contract is verified, only the fallback policy is pending.

## Deviations from Plan

The orchestrator's CRITICAL_GOVERNANCE_OVERRIDE supersedes the plan's Task-3 wording in two ways (both followed): (1) gap registers are parent-written — this executor returns draft fields rather than creating `26-GAPS.md`/`v1.5-GAPS.md`; (2) on path (b), M13 is set `IN_PROGRESS`-with-note (not `DEFERRED`) and a neutral spec note (not a "see GAP-26-NN" marker) is landed, pending the parent-recorded STOP gap.

**Line-anchor deviation (Rule 3 - blocking):** the plan/research cite `ctl_instruction.md:1068` for the Step-5 hinge, but Waves 1-3 (Step-1A gate, B-11 item 7, D7 §2.6) shifted the content; the "each simulation ID" hinge is now at line **1227** and the B-11 `record_key` annotation at **1228**. Re-confirmed the actual anchors at edit time (plan A1 directive); the edit landed at the correct current location.

## Self-Check: PASSED

- `evidence/m13-gold-counterpart.md` — FOUND (created)
- `ctl_instruction.md` gold-counterpart contract — FOUND (`grep gold_counterpart` matches)
- M13 ledger row IN_PROGRESS + defer-with-blocker + packet link — FOUND
- AC-PIPE-05 PASS (184/184) + AC-PIPE-02 regression PASS — captured in packet
- No `26-GAPS.md` / `v1.5-GAPS.md` in this executor's changes — CONFIRMED (perimeter clean)
