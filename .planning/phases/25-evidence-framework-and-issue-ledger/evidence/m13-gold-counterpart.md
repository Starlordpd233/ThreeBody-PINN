# Evidence Packet: M13 - 184 standard IDs without a gold counterpart (gold-counterpart contract + fallback policy)

## Header

| Field | Value |
|---|---|
| ID | `M13` |
| Title | `184 standard IDs without a gold counterpart (gold-counterpart contract + fallback policy)` |
| Severity | `MAJOR` (issue-doc classification; not re-adjudicated here) |
| Current Status | `VERIFIED` |
| Current Verdict | `accept-third-position` |
| Phase | `Phase 26` (Plan 26-04, resolved 2026-06-13) |
| Acceptance Check ID | `AC-PIPE-05` |
| Spec Sections Touched | `ctl_instruction.md` Step 5 ("Curriculum Stage Assignment") stage-assignment paragraph — mandatory data-side gold-counterpart contract (landed) + per-ID stage-label clarification + resolved gold-counterpart note (GAP-26-01 = Option B, framework-owner ruling 2026-06-13; OI-7a RESOLVED, OI-7b ACTIVATED) |
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

**`accept-third-position`.**

**User-decision provenance (not invented):** On 2026-06-13 the framework owner ruled the OI-7a label-semantics question (open STOP gap **GAP-26-01**) = **Option B: Stage-5 curriculum stage labels attach to IDs** (not to simulations) — every Stage-4-admitted ID owes a Stage-5 sample. The owner additionally directed the remediation: *"rerun the missing gold counterparts for the 184 standard IDs so that we will have a 1:1 match for base and gold."* This packet transcribes that grounded ruling; it does not infer or invent it. (Prior to the ruling this packet carried `defer-with-blocker`, pending the parent-recorded STOP gap; the deferral is now lifted by the user decision.)

Why `accept-third-position` (per `evidence/README.md`: "Reject both source positions in favor of an independently justified convention"):

1. The **per-ID premise is accepted** (issue-doc reading of the OI-7a hinge, `02-data-pipeline-and-validation.md:316`): every Stage-4-admitted ID owes a Stage-5 gold sample.
2. The resolution doc's **per-simulation no-fallback entailment is rejected** (`02-resolution-doc.md`): it was conditional on the simulations reading, which the ruling overturns.
3. The issue doc's **two offered fallback options are also rejected**: the directed remediation is neither "skip to Stage 6 if no gold data" nor "low-fidelity standard fallback with warning flag" (`02-data-pipeline-and-validation.md:316`). Instead the owner chose to **re-simulate the missing gold counterparts to restore a 1:1 base:gold correspondence** — a data-generation remediation that neither primary source proposes. This is the independently justified third position.

The **mandatory data-side contract** (set-difference gold-missing set; per-`physical_key` `gold_counterpart`; gold-folder-iterated Stage-5 stratum; no silent base→gold substitution) was adopted **unconditionally** (`02-resolution-doc.md:262`) and remains in force unchanged — it is verified by AC-PIPE-05 (184/184 set-difference match, re-confirmed 2026-06-13). Under Option B the gold-missing set is now interpreted as the **remediation backlog** (the 184 genuine Stage-5 gold holes), expected empty once the re-simulated gold trajectories land and validate (OI-7b, activated; not yet executed).

### OI-7a — RESOLVED (2026-06-13)

The OI-7a label-semantics hinge (Axis 2, obligation granularity) is **RESOLVED** by the framework-owner ruling: the Step-5 stage map ranges over the **abstract ID space, with every Stage-4 ID owing a Stage-5 sample** (the per-ID reading). The decisive convention is now grounded by a user decision, not invented.

### OI-7b — ACTIVATED (2026-06-13, forward reference)

The ruling activates **OI-7b**: a **data-generation remediation** to re-simulate the 184 missing gold counterparts to a 1:1 base:gold correspondence. This is NOT a loader fallback. It is a data-generation prerequisite for a complete gold Stage-5 stratum and is **not yet executed** (the owner stated intent to do this "shortly"). Recorded here as a forward reference; its completion is tracked downstream (data-generation work / FUT-01 hand-off), not in this packet.

### Why not `accept-resolution`

`accept-resolution` would adopt the resolution doc's per-simulation no-fallback entailment. The framework-owner ruling overturns its precondition (the simulations reading), so the no-fallback entailment does not hold. The landed B-11 annotation ("stage mapping keyed by `record_key`," `ctl_instruction.md:1228`) settled only the **key-type axis** (content key vs positional index); the **obligation-granularity axis** (OI-7a) was settled separately by the 2026-06-13 user ruling, not by side-effect.

## Root-Cause Framework Ambiguity

The framework never states the **domain** of the Step-5 stage map. Two orthogonal axes are conflated by the single phrase "each simulation ID":

- **Axis 1 — key TYPE** (content-derived key vs positional array index). **Settled** by B-11 (Plan 26-01): keyed by `record_key`, never by positional index (`ctl_instruction.md:1228`, item 7 at `:413-427`).
- **Axis 2 — obligation GRANULARITY / domain** (does the map range over *simulations that exist on disk* — the per-`record_key` reading — or over *the abstract ID space, with every Stage-4 ID owing a Stage-5 sample* — the per-ID reading?). **NOT settled** by anything in the corpus. This is OI-7a.

A reader can satisfy Axis 1 (use `record_key`) under *either* answer to Axis 2: one can key a map by `record_key` and still hold that every base ID must produce a gold `record_key` for Stage 5 (per-ID obligation, requiring a fallback to manufacture the missing 184), or hold that the map ranges only over existing `record_key`s (no obligation, no fallback). B-11 does not pick between these; the resolution doc routes the pick to the framework owner.

## Locked Convention

The **mandatory data-side gold-counterpart contract** is now locked in `ctl_instruction.md` Step 5 (adopted unconditionally, `02-resolution-doc.md:262`):

> The gold-missing set is computed at init by set difference of the scanned base and gold ID sets, cross-checked against the verified CLM-04 184-ID list (discrepancies logged; the list is never hard-coded). Each standard `physical_key` carries `gold_counterpart ∈ {present, absent}`. The Stage-5 stratum is built by iterating the gold folder's actual files, never by base-ID lookup into the gold index. A base-fidelity record is never silently substituted into a gold-resolution slot.

The **label semantics and remediation** are now **LOCKED** by the framework-owner ruling (GAP-26-01 = Option B, 2026-06-13): Stage-5 labels attach to IDs (every Stage-4-admitted ID owes a Stage-5 gold sample, OI-7a RESOLVED); the 184 gold-less standard IDs are genuine Stage-5 holes resolved by **re-simulating their gold counterparts to a 1:1 base:gold correspondence** (OI-7b, a data-generation remediation — not a loader fallback — activated, not yet executed). No base→gold substitution; pending re-simulation each affected ID carries `gold_counterpart = absent` and contributes no gold Stage-5 sample. The resolved note records this in the spec at the Step-5 paragraph, with a per-ID stage-label clarification on the Step-5 hinge.

## Which Source Was Correct / Wrong

Per-claim:
- **Mandatory data-side contract** (`02-resolution-doc.md:262`): **resolution doc correct**, adopted; the issue doc is silent on the set-difference / gold-folder-iteration discipline (its "use exclusion list `standard_quasi_random_ids_not_in_gold.md`," `:342`, is consistent but under-specified). AC-PIPE-05 confirms (184/184).
- **Fallback policy / label semantics** (the OI-7a hinge): **neither source resolved the decisive convention; the framework owner did.** The issue doc assumed the per-ID reading without arguing it; the resolution doc named the per-simulation reading as the entailment basis but declined to rule. The 2026-06-13 framework-owner ruling (GAP-26-01 = Option B) settled it in favor of the per-ID reading — but the chosen remediation (re-simulate to 1:1) is **neither** the resolution doc's no-fallback entailment **nor** the issue doc's skip/low-fidelity-substitute options. Both source positions on the remediation are rejected in favor of the owner's independently directed data-generation remediation: `accept-third-position`.

## Before / After Spec Note

**Affected section:** `ctl_instruction.md` Step 5 "Curriculum Stage Assignment" — the stage-assignment paragraph (pre-edit `:1227-1230`).

**Before:** Step 5 stated the map as "a mapping from each simulation ID to its assigned stage index," keyed by `record_key` (B-11 annotation, Plan 26-01). No gold-counterpart contract; no statement of how the Stage-5 stratum handles the 184 gold-less standard IDs; the "each simulation ID" phrase left the stage-map domain (per-simulation vs per-ID) ambiguous.

**After (Plan 26-04 initial, pre-ruling):** the **mandatory data-side gold-counterpart contract** was added (set-difference gold-missing set cross-checked vs the CLM-04 184-ID list, never hard-coded; per-`physical_key` `gold_counterpart ∈ {present, absent}`; Stage-5 stratum built by iterating the gold folder's actual files; no silent base→gold substitution), plus a neutral UNRESOLVED note deferring the fallback policy to the OI-7a framework-owner ruling.

**After (Plan 26-04 resolution, 2026-06-13, GAP-26-01 = Option B):** the mandatory data-side contract bullets are **unchanged**. The neutral UNRESOLVED note is **replaced** with a **resolved note** transcribing the ruling: Stage-5 labels attach to IDs (OI-7a RESOLVED); the 184 gold-less standard IDs are genuine Stage-5 holes resolved by **re-simulating their gold counterparts to a 1:1 base:gold correspondence** (OI-7b, data-generation remediation, activated, not yet executed); no base→gold substitution; pending re-simulation each affected ID carries `gold_counterpart = absent` and contributes no gold Stage-5 sample; the gold-missing set is the remediation backlog expected empty post-rerun. A one-line **per-ID stage-label clarification** is added on the Step-5 hinge ("Stage-label obligation is per-ID, not per-simulation"), now grounded by the ruling. Edit confined to `ctl_instruction.md` (D-04 perimeter; no `pinn_architecture.md` edit).

## Named Acceptance Check

**AC-PIPE-05** (reserved; no new AC-ID minted).

- **Pass criterion:** the gold-missing set equals the set difference `base_ids − gold_ids` and matches the documentation list `standard_quasi_random_ids_not_in_gold.md` exactly (count 184; intersection 184/184), confirming the mandatory data-side contract clause (i) — gold-missing set as a computed set difference, never hard-coded. (This AC verifies the **mandatory data-side contract**, which is locked regardless of the fallback verdict. The fallback policy itself is gated on the OI-7a framework-owner ruling, a governance input, not a probe.)
- **Data it runs on:** `simulation_data/Data/brutus_output/brutus_standard_quasi_random` (base) and `brutus_standard_quasi_random_gold_standard` (gold); `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (doc list).
- **Command:** `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data03_gold_gap.py` (reused; DATA-03 / CLM-04 probe).
- **Captured output (re-confirmed at resolution, run 2026-06-13T08:12:11Z, D-15 re-derivable; matches the earlier 2026-06-13T06:34:40Z run):**
  ```
  "clm_05_split_counts": { "brutus_base_output_count": 2749, "brutus_gold_output_count": 2565, "ic_folder_count": 2749 }
  "doc_cross_check": { "doc_listed_id_count": 184, "intersection_matches_set_diff": true, "intersection_with_set_diff": 184 }
  "set_diff": { "base_minus_gold_count": 184 }
  ```
  **Result: PASS (re-confirmed)** — `base_minus_gold_count = 184`, `doc_listed_id_count = 184`, `intersection_matches_set_diff: true`. The set difference is unchanged by the ruling; the mandatory data-side contract (set difference matching the doc list, never hard-coded) is verified. Under Option B this 184-ID set is the OI-7b re-simulation backlog.
- **Regression re-check (D-08):** the M13 Step-5 contract references the B-11 ID-resolution contract (`record_key`). AC-PIPE-02 re-run (`grep -nE 'id_to_path|record_key|physical_key|array index' ctl_instruction.md`) confirms Step 1 item 7 (`:413-427`) is intact — dual keys, anchored regex, array-index prohibition (`:423`), `range(n_files)` prohibition (`:424`), Step-5 `record_key` cross-reference (`:1228`). **B-11 stays VERIFIED; no regression.**

## Status Transition Log

```text
2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)
2026-06-13 1806366e PENDING -> IN_PROGRESS (Phase 26 P04; M13 packet authored; defer-with-blocker verdict; mandatory data-side gold-counterpart contract FIX_APPLIED in ctl_instruction.md Step 5; AC-PIPE-05 set-difference probe PASS 184/184; AC-PIPE-02 regression re-check PASS, B-11 stays VERIFIED; fallback policy UNRESOLVED pending OI-7a framework-owner label-semantics ruling, surfaced as parent-recorded GAP-26-NN STOP gap; label-semantics ruling NOT invented)
2026-06-13 683ef0fc IN_PROGRESS -> DEFERRED (Phase 26 P04 parent/orchestrator; GAP-26-01 recorded; fallback policy blocked on OI-7a label-semantics ruling pending user decision; mandatory data-side contract remains FIX_APPLIED + AC-PIPE-05-verified)
2026-06-13 ab5f7f06 DEFERRED -> FIX_APPLIED (Phase 26 P04 resolve; GAP-26-01 RESOLVED 2026-06-13 = Option B, Stage-5 labels attach to IDs, OI-7a; verdict accept-third-position; resolved gold-counterpart note + per-ID stage-label clarification landed in ctl_instruction.md Step 5 replacing the UNRESOLVED note; re-simulate 184 gold counterparts to 1:1, OI-7b ACTIVATED data-generation remediation not yet executed; no base->gold substitution; ruling transcribed NOT invented)
2026-06-13 ab5f7f06 FIX_APPLIED -> VERIFIED (Phase 26 P04 resolve; AC-PIPE-05 set-difference probe re-confirmed PASS 184/184; mandatory data-side contract unchanged and verified; deferral lifted by framework-owner ruling)
```

**Note:** M13 is `VERIFIED` as of 2026-06-13: the framework-owner ruling (GAP-26-01 = Option B) lifted the deferral, the resolved gold-counterpart note is landed in `ctl_instruction.md`, and AC-PIPE-05 is re-confirmed (184/184). The OI-7b re-simulation of the 184 missing gold counterparts is a forward data-generation prerequisite (activated, not yet executed) tracked downstream, not a blocker on this packet. G4 (synthesis over M13) closes with M13 = VERIFIED.

**OI-7b reconciliation (2026-06-16/17):** OI-7b executed **partial** — 117 validated (gold-config-homogeneous, staged) + 67 permanent-absent (MNAR close-encounter tail; gold integration non-terminating), 0 promoted. The 67 are permanent Stage-5 holes per the 2026-06-14 ruling (keep base; no base→gold substitution; no retry). Promotion of the 117 + the 184→67 cascade is **ruled to the FUT-01 dataset-finalization gate** (GAP-29-01; `29-CODE-DIVERGENCE.md` FO-1). M13/G4 stay `VERIFIED`; this is a factual-outcome record — the `accept-third-position` verdict is untouched (D-01a, GAP-29-01).
