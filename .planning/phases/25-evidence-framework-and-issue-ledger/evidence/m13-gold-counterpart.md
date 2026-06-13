# Evidence Packet: M13 - 184 standard IDs without a gold counterpart (gold-counterpart contract + fallback policy)

## Header

| Field | Value |
|---|---|
| ID | `M13` |
| Title | `184 standard IDs without a gold counterpart (gold-counterpart contract + fallback policy)` |
| Severity | `MAJOR` (issue-doc classification; not re-adjudicated here) |
| Current Status | `IN_PROGRESS` |
| Current Verdict | `defer-with-blocker` |
| Phase | `Phase 26` (Plan 26-04) |
| Acceptance Check ID | `AC-PIPE-05` |
| Spec Sections Touched | `ctl_instruction.md` Step 5 ("Curriculum Stage Assignment") stage-assignment paragraph — mandatory data-side gold-counterpart contract (landed) + neutral UNRESOLVED note (fallback policy pending OI-7a framework-owner ruling) |
| Code Paths Touched | `Not code-applicable` (data-side spec contract; DataLoader/stratum implementation is FUT-01) |

## Source Positions

Side-by-side line-range citations from both primary Issue 02 sources, recorded before the verdict.

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | `§3.4 Q-A4:255-293` (verdict `:257`; option rejections `:260-261`; mandatory data-side contract `:262`; STOP-gap trigger `:263`; open residue `:264`; reasoning `:266`; Medium confidence `:270`; verification `:272`; proposed conditional spec text `:274-290`; provenance/3-way split `:292`). Open Items `OI-7:768`; Additional Input Needed #1 (`Q-A4` ranked #1) `:777`. | "Per the master's annotation, no fallback is asserted." Under the locked stage definitions there is no fallback to choose: the spec's own semantics determine behavior, and both issue-doc options presuppose a per-ID Stage-5 obligation the spec does not create. Stage labels assigned per simulation (`record_key`); a gold-less standard ID has one base simulation that gets its own label and reaches Stage 5/6 training sets via cumulative replay — "no Stage-5 sample for that ID" is the spec applied. Option 2 (low-fidelity admit) rejected (contradicts Stage-5 data source; double-counts). Option 1 (skip to Stage 6) rejected as vacuous (nothing skips; base label unchanged; reaches Stage 6 via replay). **Mandatory data-side contract adopted unconditionally (`:262`).** **STOP-gap trigger preserved verbatim (`:263`):** the entailment rests on labels attaching to *simulations* (`record_key`); **if** Phase-26 rules labels attach to *IDs* (every Stage-4 ID must yield a Stage-5 sample), the no-fallback reading fails, neither option is spec-derivable, and Q-A4 must surface as the Phase-26 STOP gap, not be invented. Confidence **Medium** (`:270`). The proposed spec text (`:274-290`) is itself **explicitly conditional** on the label-semantics ruling. |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `:65` (M13 row); `:287` (P1-5 gold-counterpart check); `:299` (checklist); `:316` ("184 standard IDs ... cannot enter Stage 5 training"); `:342` (gold-counterpart check via `standard_quasi_random_ids_not_in_gold.md`). | M13 MAJOR: 184 standard IDs have no gold counterpart — "Stage 5 training data is incomplete for these IDs." Proposes: "Check gold counterpart existence before Stage 5 assignment. **Skip to Stage 6 if no gold data, or use low-fidelity standard fallback with warning flag.**" The issue doc **presupposes a per-ID Stage-5 obligation** (the "IDs" reading of the OI-7a hinge) and offers the two fallback options the resolution doc rejects as posed. |

Neither source is authoritative. The two primary sources **conflict** at exactly the OI-7a hinge: the issue doc assumes per-ID Stage-5 obligation (fallback required); the resolution doc derives a no-fallback entailment under the per-simulation reading but **declines to rule** the label-semantics question and routes it to the framework owner.

## Spec Evidence

Current framework-spec citations defining the convention in dispute:

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1220-1230` — Step 5 "Curriculum Stage Assignment": "assign a curriculum stage label (an integer from 0 to 6) to **each simulation** ... a mapping from **each simulation ID** to its assigned stage index. The stage mapping is keyed by `record_key`, never by positional index, per the Step-1 ID-resolution contract (Step 1 item 7); only trajectories admitted by the Step 1A gate appear in this mapping." **This phrase "each simulation ID" is the genuinely ambiguous textual hinge** — "simulation" suggests the per-simulation reading, "ID" suggests the per-ID reading; the two readings collide in one phrase.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:229-249` — Multi-Stage Data Stratification: Stage 5 = Set 2b (gold standard), "Criteria: Same as Stage 4"; Stage 6 = all remaining data (HF+LF), criteria `s_min < 0.5` OR `|E| < 0.01`; "each subsequent stage's training set includes all data from previous stages (curriculum replay) ... by the time we reach Stage 5 or 6, the training data is the entire dataset." Stage 5 is defined **extensionally by data source (Set 2b)**, not as a per-ID obligation — this is the textual basis of the resolution doc's entailment, but it does not by itself force either reading of the OI-7a hinge.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:413-427` — Step 1 item 7 (B-11 ID-resolution contract, landed Plan 26-01): dual `physical_key = (variant, id)` / `record_key = (variant, fidelity, id)`; scan-built `id_to_path`; IDs never contiguous/dense/zero-based/equal to an array index; "Stage labels (Step 5) are keyed by `record_key`, never by positional index." **This settles the key-TYPE axis (content key vs positional index), NOT the OI-7a obligation-granularity axis** (does every Stage-4 ID owe a Stage-5 sample?). See Root-Cause Framework Ambiguity for why these are distinct axes.

### Dataset Evidence (§3b)

From `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md`:

- `CLM-04:18` — **184 standard IDs without gold counterpart**, confirmed: `base_ids − gold_ids` set size = 184; doc `standard_quasi_random_ids_not_in_gold.md` lists exactly 184 IDs; intersection = 184/184 (exact match). Probe: `data03_gold_gap.py`.
- `CLM-05b:20` — confirmed: Brutus base output 2,749; Brutus gold output 2,565; base − gold = 184.

These figures **size** the issue (184 gold-less standard IDs) but do **not** resolve the label-semantics question — they are equally consistent with both readings (under "simulations" the 184 simply have no gold `record_key`; under "IDs" the 184 are genuine Stage-5 holes needing a fallback).

## FUT-01 Hand-off Note (formerly "Code Evidence")

> Live code in `pinn/` is NOT a v1.5 evidence source (user directive 2026-05-19). Forward-pointing only.

- `pinn/data-processing-pipeline-full.py` — the FUT-01 DataLoader must implement, in the eventual stratum builder: (i) gold-missing set computed at init by set difference of scanned base/gold ID sets, cross-checked vs the CLM-04 184-ID list (never hard-coded); (ii) per-`physical_key` `gold_counterpart ∈ {present, absent}` metadata; (iii) Stage-5 stratum built by **iterating the gold folder's actual files**, never by base-ID lookup into the gold index (which manufactures 184 spurious misses); (iv) no silent substitution of a base-fidelity record into a gold-resolution slot. The fallback-policy branch (if any) cannot be implemented until the OI-7a framework-owner ruling lands. Indexed for `NN-CODE-DIVERGENCE.md` / `pinn/STATUS.md`. NOT v1.5 evidence.

## First-Principles Physics Check

Not a physics adjudication — this is a **spec-semantics** adjudication (what the stage-mapping domain is). The decisive engineering content is set-theoretic, and it is captured in the AC-PIPE-05 probe: the gold-missing set is the well-defined set difference `base_ids − gold_ids = 184`, exactly matching the documentation list (184/184). The mandatory data-side contract rests entirely on this verified set-difference fact and on the locked B-11 `record_key`/`physical_key` keying — both grounded, neither in dispute. The **disputed** element is not a fact but a spec-semantic choice (the map's domain), which no first-principles argument can settle and which the resolution doc routes to the framework owner.

## Verdict

**`defer-with-blocker`.**

Reason: Per D-12 and ROADMAP Phase 26 success criterion 4 (`.planning/ROADMAP.md:196`: "if the sources are silent or conflicting on the fallback choice, it is surfaced as a STOP gap for user decision, not invented"), the fallback choice is **source-conflicting**:

1. The resolution doc itself assigns **Medium** confidence (`02-resolution-doc.md:270`), names Q-A4 the **#1 question** warranting the unavailable R1–R8 reports, and records a **genuine three-way upstream split** — entailment reading 3 (R1/R2/R4), STOP-gap declaration 4 (R3/R5/R7/R8), low-fidelity-fallback 1 (R6) (`:292`, `:777`).
2. The resolution doc does **not rule** the OI-7a label-semantics question; it preserves the defeater verbatim and routes the ruling to the framework owner (`:263`, `OI-7:768`: "(a) Framework owner (one line) ... ratifies the §3.4 spec text or activates the Phase-26 STOP gap exactly as the master annotates").
3. The two primary sources **conflict** at the hinge: the issue doc presupposes the per-ID reading (fallback required, `:316`); the resolution doc derives the per-simulation reading (no fallback) but only conditionally.
4. The spec's own words "each simulation ID" (`ctl_instruction.md:1227`) are genuinely ambiguous.

The **mandatory data-side contract** (set-difference gold-missing set; per-`physical_key` `gold_counterpart`; gold-folder-iterated Stage-5 stratum; no silent base→gold substitution) is adopted **unconditionally** (`02-resolution-doc.md:262`) and **lands in the spec regardless of the fallback verdict** — it is verified by AC-PIPE-05 (184/184 set-difference match). The **fallback policy** is the deferred element: it remains UNRESOLVED pending the OI-7a framework-owner ruling, surfaced as a parent-recorded STOP gap (GAP-26-NN). The label-semantics ruling is **not invented**.

### Why not `accept-resolution` (path a)

`accept-resolution` would require the no-fallback position to be fully grounded AND the label-semantics question genuinely settled by a grounding source. It is not settled: the resolution doc explicitly preserves the live defeater and routes it to the framework owner at Medium confidence with a 3-way upstream split. It is tempting to read the landed B-11 annotation ("stage mapping keyed by `record_key`," `ctl_instruction.md:1228`) as settling OI-7a for the per-simulation reading — but B-11 adjudicated the **key-type axis** (content key vs positional index), not the **obligation-granularity axis** (does every Stage-4 ID owe a Stage-5 sample). Treating the B-11 annotation as also disposing of the M13 defeater would be inventing the ruling by side-effect — exactly what governance T-26-14 prohibits.

## Root-Cause Framework Ambiguity

The framework never states the **domain** of the Step-5 stage map. Two orthogonal axes are conflated by the single phrase "each simulation ID":

- **Axis 1 — key TYPE** (content-derived key vs positional array index). **Settled** by B-11 (Plan 26-01): keyed by `record_key`, never by positional index (`ctl_instruction.md:1228`, item 7 at `:413-427`).
- **Axis 2 — obligation GRANULARITY / domain** (does the map range over *simulations that exist on disk* — the per-`record_key` reading — or over *the abstract ID space, with every Stage-4 ID owing a Stage-5 sample* — the per-ID reading?). **NOT settled** by anything in the corpus. This is OI-7a.

A reader can satisfy Axis 1 (use `record_key`) under *either* answer to Axis 2: one can key a map by `record_key` and still hold that every base ID must produce a gold `record_key` for Stage 5 (per-ID obligation, requiring a fallback to manufacture the missing 184), or hold that the map ranges only over existing `record_key`s (no obligation, no fallback). B-11 does not pick between these; the resolution doc routes the pick to the framework owner.

## Locked Convention

The **mandatory data-side gold-counterpart contract** is now locked in `ctl_instruction.md` Step 5 (adopted unconditionally, `02-resolution-doc.md:262`):

> The gold-missing set is computed at init by set difference of the scanned base and gold ID sets, cross-checked against the verified CLM-04 184-ID list (discrepancies logged; the list is never hard-coded). Each standard `physical_key` carries `gold_counterpart ∈ {present, absent}`. The Stage-5 stratum is built by iterating the gold folder's actual files, never by base-ID lookup into the gold index. A base-fidelity record is never silently substituted into a gold-resolution slot.

The **fallback policy** (what, if anything, happens to the 184 gold-less standard IDs at Stage 5) is **NOT locked** — it is deferred to the OI-7a framework-owner ruling and surfaced as GAP-26-NN. A neutral UNRESOLVED note records this in the spec at the Step-5 paragraph.

## Which Source Was Correct / Wrong

Per-claim:
- **Mandatory data-side contract** (`02-resolution-doc.md:262`): **resolution doc correct**, adopted; the issue doc is silent on the set-difference / gold-folder-iteration discipline (its "use exclusion list `standard_quasi_random_ids_not_in_gold.md`," `:342`, is consistent but under-specified). AC-PIPE-05 confirms (184/184).
- **Fallback policy / label semantics** (the OI-7a hinge): **neither source resolves the decisive convention.** The issue doc assumes the per-ID reading without arguing it; the resolution doc names the per-simulation reading as the entailment basis but declines to rule and routes it to the framework owner at Medium confidence. The decisive convention (the stage-map domain) is addressed by neither — it is surfaced as a STOP gap.

## Before / After Spec Note

**Affected section:** `ctl_instruction.md` Step 5 "Curriculum Stage Assignment" — the stage-assignment paragraph (pre-edit `:1227-1230`).

**Before:** Step 5 stated the map as "a mapping from each simulation ID to its assigned stage index," keyed by `record_key` (B-11 annotation, Plan 26-01). No gold-counterpart contract; no statement of how the Stage-5 stratum handles the 184 gold-less standard IDs; the "each simulation ID" phrase left the stage-map domain (per-simulation vs per-ID) ambiguous.

**After:** the **mandatory data-side gold-counterpart contract** is added (set-difference gold-missing set cross-checked vs the CLM-04 184-ID list, never hard-coded; per-`physical_key` `gold_counterpart ∈ {present, absent}`; Stage-5 stratum built by iterating the gold folder's actual files; no silent base→gold substitution). A **neutral UNRESOLVED note** is added stating that the fallback policy for the gold-missing set is unresolved pending a framework-owner label-semantics ruling (OI-7a), referencing this packet and the phase STOP-gap process. **No fallback policy is asserted, and the label-semantics ruling is not invented** — the conditional fallback text from `02-resolution-doc.md:274-290` is deliberately NOT landed, because its precondition (a settled label-semantics ruling) is not met (path b, not path a).

## Named Acceptance Check

**AC-PIPE-05** (reserved; no new AC-ID minted).

- **Pass criterion:** the gold-missing set equals the set difference `base_ids − gold_ids` and matches the documentation list `standard_quasi_random_ids_not_in_gold.md` exactly (count 184; intersection 184/184), confirming the mandatory data-side contract clause (i) — gold-missing set as a computed set difference, never hard-coded. (This AC verifies the **mandatory data-side contract**, which is locked regardless of the fallback verdict. The fallback policy itself is gated on the OI-7a framework-owner ruling, a governance input, not a probe.)
- **Data it runs on:** `simulation_data/Data/brutus_output/brutus_standard_quasi_random` (base) and `brutus_standard_quasi_random_gold_standard` (gold); `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (doc list).
- **Command:** `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data03_gold_gap.py` (reused; DATA-03 / CLM-04 probe).
- **Captured output (run 2026-06-13T06:34:40Z, D-15 re-derivable):**
  ```
  "clm_05_split_counts": { "brutus_base_output_count": 2749, "brutus_gold_output_count": 2565, "ic_folder_count": 2749 }
  "doc_cross_check": { "doc_listed_id_count": 184, "intersection_matches_set_diff": true, "intersection_with_set_diff": 184 }
  "set_diff": { "base_minus_gold_count": 184 }
  ```
  **Result: PASS** — `base_minus_gold_count = 184`, `doc_listed_id_count = 184`, `intersection_matches_set_diff: true`. The mandatory data-side contract (set difference matching the doc list, never hard-coded) is verified.
- **Regression re-check (D-08):** the M13 Step-5 contract references the B-11 ID-resolution contract (`record_key`). AC-PIPE-02 re-run (`grep -nE 'id_to_path|record_key|physical_key|array index' ctl_instruction.md`) confirms Step 1 item 7 (`:413-427`) is intact — dual keys, anchored regex, array-index prohibition (`:423`), `range(n_files)` prohibition (`:424`), Step-5 `record_key` cross-reference (`:1228`). **B-11 stays VERIFIED; no regression.**

## Status Transition Log

```text
2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)
2026-06-13 <THIS_SHA> PENDING -> IN_PROGRESS (Phase 26 P04; M13 packet authored; defer-with-blocker verdict; mandatory data-side gold-counterpart contract FIX_APPLIED in ctl_instruction.md Step 5; AC-PIPE-05 set-difference probe PASS 184/184; AC-PIPE-02 regression re-check PASS, B-11 stays VERIFIED; fallback policy UNRESOLVED pending OI-7a framework-owner label-semantics ruling, surfaced as parent-recorded GAP-26-NN STOP gap; label-semantics ruling NOT invented)
```

**Note:** M13 remains `IN_PROGRESS` (not `DEFERRED`) by orchestrator directive: the mandatory data-side contract is FIX_APPLIED and AC-PIPE-05 verified, but the fallback policy is pending the parent-recorded STOP gap. G4 (synthesis over M13) is left unclosed pending the same ruling. Final disposition (VERIFIED-with-conditional-note via path a, or DEFERRED via formal gap resolution) is set when the OI-7a ruling lands.
