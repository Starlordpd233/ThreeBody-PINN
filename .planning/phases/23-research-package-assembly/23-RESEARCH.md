# Phase 23: Research Package Assembly - Research

**Researched:** 2026-06-10
**Domain:** Documentation assembly / external-research handoff packaging (no code, no external packages)
**Confidence:** HIGH

## Summary

Phase 23 is a documentation-assembly phase, not a code phase. It produces an external-research handoff package for issue 02 (data pipeline and validation): an annotated, self-contained document list (PKG-01), one framed-questions document grouped by downstream contract cluster (PKG-02), a dedicated claims table that marks every dataset figure `claimed-unverified` or `verified` (PKG-03), and a standalone read-only characterization of `data_quality_assessment.md` (PKG-04). On delivery, the external resolution-doc gate opens and the user's multi-AI research begins. There is no library research to do; the "stack" here is repository documents, governance rules, and the v1.4 precedent layout.

The research consisted of (a) a full read of the 364-line issue doc to enumerate every finding the questions-doc must pose; (b) a grounding audit of every dataset figure against `simulation_data/Documentation/` to pre-classify the CLM table (verified vs claimed) per the D-13 conservative rule; (c) locating the exact framework-spec section/line ranges that carry the six locked v1.4 conventions the PKG-02 preamble must cite; (d) characterizing the DQA file's structure and provenance for PKG-04; and (e) studying the v1.4 `ctl_pinn_resolution.md` + 4-model-report precedent and the EDL brief format the package mirrors.

**Primary recommendation:** Build the package per the locked CONTEXT.md decisions (D-01..D-17) in this task order: (1) DQA characterization first (D-15, informs inclusion) → (2) candidate finding/claims inventories → (3) surface the consolidation plan to the user as a hard gate (D-07) → (4) assemble snapshot copies + manifest + questions-doc + claims-table → (5) delivery note + STATE.md gate-open via gsd-tools handlers. Two findings carry known cross-source conflicts that must be posed neutrally, never settled: the ratio-based SCS thresholds and the `D = 6.694` global-scale claim. One structural surprise the planner must absorb: **the locked post-v1.3 SCS gate lives only in the read-only, non-authoritative `data_quality_assessment.md`, not in any editable framework spec.**

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Package location & delivery form**
- **D-01:** Package lives at `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/` — co-located with where the resolution doc is expected to land, mirroring the v1.4 layout.
- **D-02:** The package is **self-contained**: snapshot copies of every included document (external AI agents have no repo access). A manifest/README records, per file, its role annotation, canonical source path, and source commit hash, so the snapshot is traceable and the research state is pinned.
- **D-03:** Framework specs (`ctl_instruction.md`, `pinn_architecture.md`, and — if included — `sampling_method.md`) are copied byte-for-byte intact. NEVER consolidated, excerpted, or summarized (PKG-01 hard rule).

**Document list (candidate inventory + criteria; final list locked at execution)**
- **D-04:** Inclusion criterion: a document enters the list iff at least one issue-02 finding needs it for adjudication. Final list locked during execution AFTER the PKG-04 DQA characterization and AFTER the consolidation plan is surfaced to the user (D-07).
- **D-05:** Candidate inventory: issue doc (required); `ctl_instruction.md` + `pinn_architecture.md` (intact, spec-edit targets); `sampling_method.md` (intact, annotated FROZEN); `data_quality_assessment.md` (inclusion per PKG-04 outcome, annotated "research report, not authoritative spec"); one consolidated context file for scattered fragments (`simulation_data/Documentation/README.md` relevant content, `standard_quasi_random_ids_not_in_gold.md`, blacklist summary, relevant `simulation_data/Scripts/` provenance excerpts) — each fragment labeled with its source path.
- **D-06:** `pinn/` live code EXCLUDED. The package explicitly states, as a hard constraint, that issue-02's "Canonical" citation of `pinn/data-processing-pipeline-full.py` is overridden (directive 2026-05-19; SCOPE-10) and the framework specs are source of truth. Issue-01 NOT included (resolved by v1.4; outcomes travel as the locked-constraints block + intact specs). Issue-03 NOT included (doc-03 boundary; boundary statement covers it).
- **D-07:** Candidate list is ≥6 deliverable files, so the PKG-01 consolidation rule fires. **Hard execution checkpoint: the consolidation plan is surfaced to the user BEFORE assembly.** A requirement, not a courtesy. Plans MUST model this as a user gate.

**Research-question framing (PKG-02)**
- **D-08:** One questions document, structured as per-finding explicit questions grouped by downstream contract cluster: (a) ingestion & selection (B-06, B-11, M11, M13, D7, D-03 format, G1–G5 as applicable), (b) sampling / precision / global-scale (M12, precision handling, footer/mass-drift protocol, `compute_globals` D=6.694), (c) validation metrics (SCS, SASD, IPR, PSC definitions and thresholds). Grouping mirrors Phases 26–28.
- **D-09:** Neutral framing rule: each question presents the issue-doc position, the current framework-spec position, and the relevant dataset facts (via CLM IDs) — and NEVER presupposes the issue doc's "Recommended Resolutions". The package instructs that BOTH the issue doc and its recommendations are non-authoritative and may contain errors, citing the known seed conflict (ratio-based SCS thresholds vs the locked post-v1.3 gate).
- **D-10:** A shared hard-constraints preamble lists the locked v1.4 conventions verbatim: 14D input contract, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 softening outcome, post-v1.3 SCS gate (`ε_H > 10⁻⁵` / `SCS > −5`), PHYS-01 D convention — plus the doc-03 scope boundary (M16, G6, training-loop usage of SCS/SASD/IPR/PSC EXCLUDED, each noted as deferred with a forward-reference).

**Claims register (PKG-03 + Phase 24 handoff)**
- **D-11:** A dedicated claims table with stable IDs (`CLM-01`, …): every dataset figure stated anywhere in the package gets a row with value, source citation, and status `claimed-unverified` or `verified` (with grounding citation). All inline figure mentions reference their CLM ID.
- **D-12:** The claims table IS the "delivered package's claim list" Phase 24 consumes as its verification checklist; the DATA-07 correction addendum is keyed by CLM IDs. Must enumerate at minimum: 1,250/4,000 standard and 143/5,000 hierarchical ID gaps; 65 blacklist IDs; 184 standard IDs without gold; 2,565 vs 2,749 folder counts; 219 minimal standard-gold footers; ~59/~125/~1000 snapshot counts; `final_timestep >= 9.5` prevalence; folder-default tolerance/dt values.
- **D-13:** Conservative verified-status rule: only `simulation_data/Documentation/` files and prior-phase probe evidence (committed v1.4 artifacts) count as "prior grounded source". `.planning/codebase/*.md` maps do NOT count. When in doubt → `claimed-unverified` (over-marking is harmless; Phase 24 verifies everything).

**DQA characterization (PKG-04)**
- **D-14:** Deliverable is a standalone phase artifact `.planning/phases/23-research-package-assembly/23-DQA-CHARACTERIZATION.md` covering provenance (git origin/history), a section-by-section content map, its relation to the not-yet-performed dataset↔framework compatibility verification, and a package-inclusion recommendation. Zero edits to `data_quality_assessment.md`.
- **D-15:** Sequencing: characterization completes BEFORE the document list is finalized — DQA characterization is an early task, before package assembly.

**Gate-opening record & handoff**
- **D-16:** Delivery = package committed + a delivery note to the user stating: how to use the package for external multi-AI research; that the resolution doc must land under `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`; that v1.4's `ctl_pinn_resolution.md` is a format precedent (suggestion only — no required schema); that Phase 24 runs in parallel immediately and forwards a DATA-07 correction addendum for any package-stated claim verification contradicts.
- **D-17:** Gate-open state recorded in STATE.md via gsd-tools state handlers only (no direct Write/Edit to STATE.md).

### Claude's Discretion
- Exact file names inside the package (manifest/README name, questions-doc name, claims-table placement as standalone file vs section of the manifest) — presentation-only; keep names self-describing and kebab/snake-consistent with the repo.
- Which `simulation_data/Scripts/` excerpts enter the consolidated context file — judged per-finding during execution, within D-04, shown to the user at the D-07 checkpoint.
- Whether `sampling_method.md` ships in the package — recommended YES (the findings concern the dataset it generated) but final call rides the D-07 user checkpoint alongside the DQA inclusion decision.

### Deferred Ideas (OUT OF SCOPE)
- Prescribing a required schema for the user's resolution doc — rejected for Phase 23 (the doc is the user's product); only a format-precedent pointer ships (D-16). A Phase 25 concern if needed.
- Any empirical probe (counting files, parsing footers) — Phase 24 territory; Phase 23 states claims only.
- M16 collocation-scaling, G6 causal-training, training-loop metric usage — doc-03 milestone (SCOPE-11); appear in the package only as stated exclusions.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| PKG-01 | Complete annotated document list; consolidate scattered fragments into one context file (specs intact); surface consolidation to user before assembly | Candidate inventory (D-05) confirmed against the issue doc's References (issue-02 lines 352–358) and Documentation/ contents; consolidation rule fires (≥6 files, D-07). Document roles and grounding map in `## Document List & Roles` below. |
| PKG-02 | Frame each contested/unverified finding as an explicit question; list locked v1.4 conventions as hard constraints; state doc-03 boundary | Full finding inventory with line ranges + in-scope/excluded classification in `## Issue-02 Finding Inventory`. Exact spec citations for all six locked conventions in `## Locked v1.4 Convention Citations`. Doc-03 exclusions enumerated. |
| PKG-03 | Mark every dataset figure `claimed-unverified` unless a prior grounded source verified it; no unverified figure presented as fact | Pre-classified CLM candidate table with grounding citations in `## CLM Candidate Claims Inventory` — derived from a direct grounding audit of `simulation_data/Documentation/` per D-13. |
| PKG-04 | Characterize `data_quality_assessment.md` read-only (provenance, content map, relation to compatibility verification); inform doc-list decision | DQA section map, git provenance, and compatibility-verification relation in `## DQA Characterization Inputs`. |
</phase_requirements>

## Architectural Responsibility Map

This phase has no software tiers. The analogous map is artifact ownership: which deliverable owns each capability.

| Capability | Primary Artifact | Secondary Artifact | Rationale |
|------------|------------------|--------------------|-----------|
| Enumerate what the research must adjudicate | Framed-questions doc (PKG-02) | Manifest/README | Questions are the research's task list; grouped by Phase 26–28 clusters (D-08) |
| Pin the factual baseline & its trust level | Claims table (PKG-03, CLM IDs) | — | Single source for every figure + verified/claimed status; Phase 24 checklist (D-12) |
| Carry the immutable design contracts | Intact spec snapshots (`ctl_instruction.md`, `pinn_architecture.md`) | Hard-constraints preamble (D-10) | Specs are byte-for-byte truth; preamble names the six locked conventions (D-03/D-10) |
| Make the package self-navigable for repo-blind agents | Manifest/README (D-02) | Consolidated context file (D-05) | Role annotations + source paths + commit hashes; one file for scattered fragments |
| Report DQA standing without editing it | `23-DQA-CHARACTERIZATION.md` (PKG-04, phase-local) | Doc-list inclusion note | Read-only characterization; informs whether DQA ships (D-14/D-15) |
| Open the gate & record handoff state | Delivery note (D-16) + STATE.md via gsd-tools (D-17) | — | Delivery is the gate-open event; STATE mutated only through handlers |

## Issue-02 Finding Inventory

Every finding/decision the questions-doc (PKG-02) must pose, with issue-doc line ranges, v1.5 in-scope vs doc-03-excluded classification, downstream phase, and the documents an external researcher needs to adjudicate it. All line citations `[VERIFIED: pinn_instruction/issues/02-data-pipeline-and-validation.md]` (direct read).

| Finding | Issue-doc lines | Cluster (D-08) | In scope? | Downstream | Adjudication documents needed |
|---------|-----------------|----------------|-----------|------------|-------------------------------|
| **D-03** processed training-data format (HDF5 vs .npy vs txt/json) | 27–49, 173–190, 262–277 | (a) ingestion | IN (PIPE-10) | Phase 26 | `ctl_instruction.md` Step 1 item 6; dataset README §File Schemas |
| **B-06** Stage 4→5 validation gate missing | 57, 196–207, 320–331 | (a) ingestion | IN (PIPE-01) | Phase 26 | README §Completeness Checks (final-timestep ≥9.5); `calculate_metrics.py` |
| **B-11** non-contiguous ID handling (ID ≠ index) | 58, 314–318 | (a) ingestion | IN (PIPE-02) | Phase 26 | README §File Naming/Mapping; `standard_quasi_random_ids_not_in_gold.md` |
| **M11** blacklist not loaded at training time | 59, 76, 341 | (a) ingestion | IN (PIPE-03) | Phase 26 | `problematic_ics_blacklist.json` |
| **M12** points-per-trajectory infeasible (32 pts on ~59 snapshots) | 60, 77, 286 | (b) sampling | IN (PIPE-04) | Phase 27 | README dt_out/snapshot info; `ctl_instruction.md` Sec 5.3.2 |
| **M13** 184 standard IDs without gold counterpart | 65, 316, 342 | (a) ingestion | IN (PIPE-05) | Phase 26 | `standard_quasi_random_ids_not_in_gold.md` |
| **D7** footer/parameter heterogeneity (minimal footers, tol fallback) | 66, 68, 196–207 | (a) ingestion / (b) precision | IN (PIPE-06) | Phase 26 | README §Brutus Parameters by Variant |
| **Severity reclassification** M11, M12 MAJOR→BLOCKING | 70–77 | adjudication framing | IN (EVID-10) | Phase 25 | Audit context; pose whether reclassification stands — do not assert |
| **G1–G5** pipeline validation gaps (= B-06/B-11/M11/M12-M16/M13) | 88–105 | (a)/(b) | IN (same findings) | Phases 26–28 | Same as constituent findings; G-table is a synthesis view |
| **Validation-threshold clarifications** (overfit `<1e-6`; 14D dimensionality; gold-standard thresholds) | 109–119 | mixed | PARTIAL | Phase 28 / locked | 14D is a *locked constraint*, not a question; gold-thresholds → Phase 28; overfit-challenge precision is training-loop-adjacent |
| **SCS** definition + ratio thresholds `>1e-6` / `<1e-8` | 129–141 | (c) metrics | IN — **KNOWN CONFLICT** (VAL-01/EVID-10) | Phase 28 | DQA §3.1; **locked gate in DQA lines 120/130/234** (see pitfall) |
| **SASD** definition (data-side) | 143–153 | (c) metrics | IN data-side (VAL-02); training-side weighting EXCLUDED | Phase 28 | DQA §3.2 |
| **IPR** definition (data-side) | 155–165 | (c) metrics | IN (VAL-03); ALM noise-floor role EXCLUDED | Phase 28 | DQA §3.3; PHYS-03 dual-epsilon |
| **PSC** definition (data-side) | 167–169 | (c) metrics | IN data-side (VAL-04); replay-governance EXCLUDED | Phase 28 | DQA §3.4 |
| **Footer/mass-drift protocol** (`np.allclose rtol=1e-15`, Decimal) | 196–207 | (b) precision | IN (PIPE-06/07) | Phase 26/27 | README §Brutus Parameters; mass-drift is a Phase-24 probe (DATA-05) |
| **Precision handling** (float64 sufficiency; Decimal-for-masses) | 208–216 | (b) precision | IN (PIPE-07) | Phase 27 | DQA; PHYS-03 dual-epsilon |
| **Global-scale `compute_globals` / `D = 6.694`** | 218–258 | (b) global-scale | IN — **KNOWN CONFLICT** (PIPE-09/EVID-10) | Phase 27 | `ctl_instruction.md` §2.5 (PHYS-01 D convention; **explicitly rejects 6.694**) |
| **Recommended Resolutions** P1-1..P2-2 | 281–301 | — | Present as **non-authoritative**, never settled (D-09) | — | These map to the findings above; cite as "issue-doc proposal" only |
| **Dataset Inventory** (counts table) | 305–318 | — | Source of CLM figures (PKG-03) | Phase 24 | `standard_quasi_random_ids_not_in_gold.md`; README |
| **DataLoader Requirements** (10-item impl spec) | 335–348 | (a)/(b)/(c) | Data-side contracts IN; *implementation* is FUT-01 | 26–28 | Pose the data-side contract each item implies; implementation deferred |
| **M16** dt_out collocation-scaling | 11–19, 67, 102, 290 | — | **EXCLUDED (doc-03, SCOPE-11)** | doc-03 | Forward-reference only; stated as deferred |
| **G6** causal-training Option A vs B | 103 | — | **EXCLUDED (doc-03, SCOPE-11)** | doc-03 | Forward-reference only; stated as deferred |
| **Training-loop usage** of SCS/SASD/IPR/PSC (weighting, ALM floor, replay) | 153, 159, 165, 169 | — | **EXCLUDED (doc-03)** | doc-03 | Data-side definitions IN; training-loop usage deferred with forward-reference |

## CLM Candidate Claims Inventory (PKG-03)

Pre-classification from a direct grounding audit of `simulation_data/Documentation/` per the D-13 conservative rule. "Grounded?" = whether a `Documentation/` file already verifies the figure (→ may ship `verified` with citation) or not (→ `claimed-unverified`). **This is a recommendation for the planner; the executor confirms at assembly. Phase 24 re-verifies every row regardless (D-12).**

| Candidate CLM | Value (issue-doc) | Issue-doc line | Grounded by Documentation/? | Recommended status |
|---------------|-------------------|----------------|------------------------------|--------------------|
| Standard ID gaps | 1,250 gaps / 4,000 (31.2%) | 58, 312 | NO — README gives folder counts, not gap counts | `claimed-unverified` |
| Hierarchical ID gaps | 143 / 5,000 (2.9%) | 58, 311 | NO | `claimed-unverified` |
| Blacklist size | 65 IDs | 59, 297 | YES — `problematic_ics_blacklist.json` (observed: 2 hierarchical + 63 standard = 65) | `verified` (count only; *consumption/loading* status stays Phase-24/DATA-02) |
| Standard IDs without gold | 184 | 65, 316 | YES — `standard_quasi_random_ids_not_in_gold.md` | `verified` w/ citation |
| Standard folder counts | 2,749 base vs 2,565 gold | 318, 312 | YES — `standard_quasi_random_ids_not_in_gold.md` + README | `verified` w/ citation |
| Hierarchical Brutus output | ~4,857 | 311 | YES — README §Brutus Parameters (4,857 files) | `verified` w/ citation |
| Minimal standard-gold footers | 219 | 66, 301 | YES — README line 627 ("219 minimal") | `verified` w/ citation |
| tol=1e-14 standard-gold files | 592 | 66 | YES — README §Brutus Parameters | `verified` w/ citation |
| Folder-default tol / dt_out values | std 0.17/1e-13; hier base 0.08/1e-15; gold 0.01/1e-13 | 66, 68, 311–312 | YES — README §Brutus Parameters by Variant | `verified` w/ citation |
| Snapshot counts per trajectory | ~59 / ~125 / ~1000 | 13, 60, 311–312 | NO — **README explicitly warns against hard-coding snapshot counts (lines 629–637)** | `claimed-unverified` |
| `final_timestep >= 9.5` prevalence | (gate rule; prevalence unstated) | 57, 202, 326 | Rule grounded (README §Completeness Checks); *prevalence* not | `claimed-unverified` (prevalence) |
| Nominal IC counts | ~4,000 standard / ~5,000 hierarchical | 311–312 | Approximate ("~"); README gives actual output counts | `claimed-unverified` |
| `D = 6.694` global scale | `cbrt(G·M_tot·t_max²)=6.694` | 231, 258, 289 | NO — **conflicts with locked PHYS-01** `D=(GT²)⅓≈4.6416` (ctl §2.5) | Pose as **conflict to adjudicate**, not a count; flag both positions |

**Net:** ~7 figures are groundable as `verified` from `Documentation/`; ~5 remain `claimed-unverified`; `D = 6.694` is a convention conflict (not a dataset count) and must be framed as a contested claim with the locked counter-position cited. The blacklist `65` count is groundable, but its *loading/consumption* status (the actual M11 finding) is not — keep that nuance.

## Locked v1.4 Convention Citations (PKG-02 hard-constraints preamble)

Exact source locations for the six locked conventions D-10 requires verbatim. All `[VERIFIED]` via direct read of the named spec.

| Convention | Canonical location | Key line(s) | Locked by | Note |
|------------|--------------------|-------------|-----------|------|
| **14D input contract** `x_net = [τ, IC₁₃]`, `τ = 2u−1`, `u = t/T` | `ctl_instruction.md` Step 4 §"Network input contract" | 1000–1011 (eq at 1005); also `pinn_architecture.md` §5.2 "Network Input Contract" (751–762) | Phase 17 (IO-01) | Two homes; cite ctl as primary |
| **Jacobi IC₁₃** `[m₁,m₂,m₃,ρ_x,λ_x,λ_y,ρ̇_x,ρ̇_y,ρ̇_z,λ̇_x,λ̇_y,λ̇_z,E]` | `ctl_instruction.md` Step 4 | 1011–1014; validity note at 961 (PHYS-06); Jacobi vectors §2.4 (461–571); COM/frame Step 2.2 (415–439) | Phase 17 (IO-02) / Phase 18 (FRAME-01) | Validity is gauge-fixed encoding, not constraint-counting (line 961) |
| **Mass-weighted COM projection head** | `pinn_architecture.md` §5.2 "Output Layer" | 763–795 ("projected position outputs"); acceptance check §10.2 "COM Invariance" (972) | Phase 17 (IO, D-02) | Executor should quote the exact projection formula from §5.2; §10.2 confirms it is enforced before loss/metric |
| **PHYS-03 softening outcome** `ε_train = 10⁻⁵` Plummer; dual-epsilon (validation static `1e-10`, training dynamic `1e-5`) | `pinn_architecture.md` §3.2 (372–399), matched-Plummer Hamiltonian §3.4 (491–534) | 377, 399, 491–534; dual-epsilon noted in `ctl_instruction.md` line 703 | Phase 19 (PHYS-03) | The validation `eps=1e-10` vs training `1e-5` split is exactly issue-02's claim (line 216) — confirm, don't contradict |
| **Post-v1.3 SCS gate** `ε_H > 10⁻⁵` / `SCS > −5`, with `SCS = log₁₀(ε_H)` | **`data_quality_assessment.md` (READ-ONLY) lines 120, 130, 234; correction SI-DQA-003 line 328** | — | Post-v1.3 ratified (STATE.md decision; SI-DQA-003) | **Lives only in the read-only, non-authoritative DQA file — NOT in any editable spec. See Pitfall 1.** |
| **PHYS-01 D convention** raw-mass `D = (GT²)^⅓ ≈ 4.6416`; mass-fraction `D = (G·M_tot·T²)^⅓ ≈ 6.694` **explicitly rejected** | `ctl_instruction.md` §2.5 "Global scaling" | 581–598 (rejection at 598) | Phase 19 (PHYS-01) | This is the exact locked counter-position to issue-02's `D = 6.694` |

**Doc-03 boundary (must be stated in the preamble, D-10):** M16 collocation-scaling, G6 causal-training, and training-loop usage of SCS/SASD/IPR/PSC are EXCLUDED from the research scope; each appears only as a deferred forward-reference to the future doc-03 milestone (`03-curriculum-and-training-loop.md`).

## DQA Characterization Inputs (PKG-04)

`data_quality_assessment.md` — 328 lines, `framework-revisions/` (a research report, NOT an authoritative spec; SCOPE-09 read-only).

**Section map** `[VERIFIED: grep headings]`:
- §1 Introduction (Brutus/Bulirsch-Stoer landscape; CTL-PINN architecture) — lines 9–30
- §2 Assessment Strategy (Static vs Dynamic; the "Staged Gate" Protocol) — 31–105
- §3 Mathematically Grounded Metrics — **the canonical metric definitions**: §3.1 SCS (110–137, incl. the locked `SCS > −5` / `ε_H > 10⁻⁵` gate), §3.2 SASD (138–159), §3.3 IPR (160–175), §3.4 PSC (176–191)
- §4 Risks to Model Parameters (causal firewall, dead neurons, spectral bias) — 192–219
- §5 Implementation Protocol ("Staged Gate" workflow; Phase 1 static audit at 224 carries the gate at line 234) — 220–291
- §6 Synthesis & future-work recommendations — 292–307
- Source Issues: SI-DQA-001 (orphaned bibliography), **SI-DQA-002 (superseded — initial audit missed SCS gate inconsistency)**, **SI-DQA-003 (source-level SCS gate inconsistency corrected; raw-drift `ε_H` vs log `SCS`; threshold tightened `−4`→`−5`)** — 308–328

**Provenance** `[VERIFIED: git log --follow]`: created during v1.3 Phase 11 markdown conversion (`314d956`, `460cf4b` 11-02; `b5edcc2` 11-03 added Source Issues); moved into `framework-revisions/` by `6ab19ea`; **SCS/raw-drift gate correction `3732f1f` "fix(dqa): correct SCS/raw-drift gate inconsistency"**; stale-report retirement `d3fcff9`. No v1.4/v1.5 design edits — content is the v1.3-era research report plus the SCS-gate correction.

**Relation to dataset↔framework compatibility verification (the PKG-04 "relation" requirement):** The DQA file *defines* the four validation metrics (SCS/SASD/IPR/PSC) and the staged-gate protocol, but **no phase has yet verified those definitions against the on-disk dataset or the v1.4 specs** (CLAUDE.md: "no dedicated phase or milestone has yet verified dataset ↔ framework compatibility; `data_quality_assessment.md` may cover parts of that ground and is to be characterized, not edited, during v1.5"). It is the *only* written home of the locked SCS gate, yet it is non-authoritative. The characterization must report: what ground it covers (metric math, gate thresholds), what remains unverified (the metric definitions vs the actual snapshot distributions; the threshold vs the dataset's real drift profile — Phase 24/28 territory), and that v1.5 edits land in the *editable* specs, not here.

**Inclusion recommendation (informs D-04/D-15):** Recommend **INCLUDE** the DQA snapshot, annotated "research report, not authoritative spec (SCOPE-09); sole written home of the post-v1.3 SCS gate; metric definitions unverified against dataset." Rationale: §3 is the most complete existing statement of the contested metrics the research must adjudicate (SCS/SASD/IPR/PSC), and the SCS gate the seed conflict turns on. The final call rides the D-07 user checkpoint.

## Document List & Roles (PKG-01)

Candidate deliverables with role annotations (final list locked at execution after D-07). Snapshot copies + manifest record per-file source path and commit hash (D-02).

| Document | Role annotation | Treatment |
|----------|-----------------|-----------|
| `02-data-pipeline-and-validation.md` | Adjudication subject — NON-authoritative; may contain errors | Intact copy |
| `ctl_instruction.md` | Spec-edit target; carries 14D contract, IC₁₃, PHYS-01 D convention, dual-epsilon | Intact, byte-for-byte (D-03) |
| `pinn_architecture.md` | Spec-edit target; carries COM projection head, PHYS-03 softening, loss contracts | Intact, byte-for-byte (D-03) |
| `sampling_method.md` | FROZEN (SCOPE-08); historical record of dataset generation | Intact if included (discretion; recommend YES) |
| `data_quality_assessment.md` | Research report, NOT authoritative spec (SCOPE-09); sole home of SCS gate + metric defs | Intact copy; inclusion per PKG-04 (recommend YES) |
| Consolidated context file (one) | Scattered dataset facts, each fragment labeled with source path | Consolidation surfaced to user before assembly (D-07) |

Consolidated-context-file fragments (D-05): `simulation_data/Documentation/README.md` finding-relevant content (Dataset Sizes 81–90; File Naming/Mapping 193–231; Brutus Parameters by Variant 584–628; Completeness Checks 637–660); `standard_quasi_random_ids_not_in_gold.md` (full — 184/2,749/2,565 grounding); `problematic_ics_blacklist.json` summary (65 = 2 hier + 63 std); `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` provenance excerpt (SCOPE-07). **`pinn/` EXCLUDED (D-06/SCOPE-10).**

## Precedent: v1.4 Layout & EDL Brief Format

**v1.4 `research_reports/01-architecture-and-physics-foundations/`** `[VERIFIED: ls + grep]` — the layout D-01 mirrors:
- 4 individual model reports (`chatgpt_research_report.md`, `claude_research_report.md`, `claude_research_report_2.md`, `gemini_research_report.md`) — the multi-AI research *inputs*.
- `ctl_pinn_resolution.md` — the resolution-doc *output* (43 KB). Structure (format precedent only, D-16): §0 Scope/Decision Standard/Supersession Rule → §1 Executive Decision Summary → §2 Final Decision Matrix → §3 Governing Mathematical Convention → §4–9 contract sections → §10 Exact Source Patch Requirements. This is what the user's external research consumed and produced last time. The package directory co-locates inputs + output the same way.

**EDL brief format** (`EDL-19-01-epsilon-H.md`) `[VERIFIED: grep headings]` — prior art for packaging context for user-led external research (structural inspiration for the questions-doc, D-08): Short Answer Needed → Current Project State → Why This Is A Gap → Agent Understanding → Candidate Resolutions (Options A–E) → Dependency Map → Core Files To Audit → External Research Questions → Return Format. The "present positions, never presuppose an answer" shape matches D-09's neutral-framing rule.

## Common Pitfalls

### Pitfall 1: Treating the SCS gate's home as an editable spec — or conflating two different `ε_H`
**What goes wrong:** The locked post-v1.3 SCS gate (`ε_H > 10⁻⁵` / `SCS > −5`) is documented **only in the read-only, non-authoritative `data_quality_assessment.md`** (lines 120/130/234, SI-DQA-003), not in any editable framework spec. Separately, `ctl_instruction.md` line 1295–1296 and `pinn_architecture.md` line 936 use a *different* `ε_H` — the energy-loss denominator floor `ε_H = 1e-4 · S_H` with `ε_energy = 10⁻⁴` (a training penalty, PHYS-04/GAP-19-01), NOT the SCS validation gate.
**Why it happens:** Same symbol `ε_H`, two unrelated roles (validation raw-drift gate vs training energy-denominator floor).
**How to avoid:** In the PKG-02 preamble, cite the SCS gate to DQA explicitly and annotate it "locked post-v1.3 (SI-DQA-003); its only written home is a read-only research report." Never imply it lives in an editable spec. Keep the two `ε_H` meanings disjoint in package prose.
**Warning signs:** Any package sentence that places the `SCS > −5` gate in `ctl_instruction.md`/`pinn_architecture.md`, or that equates `ε_H (raw drift)` with `ε_H = 1e-4·S_H`.

### Pitfall 2: Presenting issue-doc "Recommended Resolutions" as settled
**What goes wrong:** Issue-02 §Recommended Resolutions (lines 281–301) and §Open Decisions reads as prescriptive (P1-1..P2-2, a verification checklist). Copying it as guidance violates D-09 and the milestone source-treatment policy.
**How to avoid:** Frame every recommendation as "the issue doc *proposes* X (non-authoritative)"; pose the neutral question alongside the locked-convention position. State once, prominently, that both the issue doc and its recommendations may contain errors — cite the SCS-threshold seed conflict as the worked example (D-09).
**Warning signs:** Imperative verbs ("Implement…", "Use…") carried into the questions-doc without a "the issue doc claims" qualifier.

### Pitfall 3: Stating a dataset figure as fact (PKG-03 violation)
**What goes wrong:** Inline prose repeats "1,250 gaps" or "~59 snapshots" as established. README *warns against* the snapshot counts (lines 629–637); the gap counts are ungrounded.
**How to avoid:** Every figure references its CLM ID; the CLM table carries the status. Default to `claimed-unverified` when `Documentation/` does not ground it (D-13). Over-marking is harmless.
**Warning signs:** A number in package prose with no CLM-ID reference; a `verified` status whose citation is not a `Documentation/` file or a committed prior-phase probe.

### Pitfall 4: Leaking doc-03 scope into the questions
**What goes wrong:** M16 collocation-scaling, G6 causal-training, and training-loop metric *usage* (SASD weighting, IPR ALM floor, PSC replay governance) get posed as research questions, expanding scope beyond v1.5 (SCOPE-11).
**How to avoid:** Define metrics data-side only; mark each training-loop usage as a deferred forward-reference to doc-03. State the boundary in the preamble (D-10).
**Warning signs:** A question asking how collocation density should scale, or how a metric weights training — those are doc-03.

### Pitfall 5: Citing `pinn/` as canonical or consolidating a spec
**What goes wrong:** The issue doc's References list `pinn/data-processing-pipeline-full.py` as "Canonical" (line 357). Carrying that into the package contradicts SCOPE-10. Separately, summarizing a framework spec to save space violates the D-03 intact rule.
**How to avoid:** State explicitly (D-06) that the `pinn/` citation is overridden and the specs are source of truth. Copy specs byte-for-byte; consolidate only non-spec fragments.
**Warning signs:** Any package text treating `pinn/` code as evidence; any spec content paraphrased rather than snapshot-copied.

### Pitfall 6: Inventing where the issue doc is silent (STOP-protocol)
**What goes wrong:** A finding is ambiguous (e.g., M13 fallback policy: skip-to-Stage-6 vs flagged low-fidelity) and the agent picks one to "frame" the question, smuggling a decision.
**How to avoid:** Pose both options neutrally. If framing forces a semantic/process-schema/cross-phase choice the sources do not answer, STOP and log to `23-GAPS.md` + create `.planning/milestones/v1.5-GAPS.md` (neither exists yet). Mechanical/presentation choices (file names, table layout) are fine and noted in-artifact.
**Warning signs:** A question whose wording presupposes one resolution; a fallback policy asserted rather than asked.

### Pitfall 7: Direct STATE.md edit / wrong branch / non-self-contained references
**What goes wrong:** Editing STATE.md by hand (violates D-17), committing to master (work is on `milestone/v1.5`), or leaving repo-relative paths that dangle for repo-blind agents (violates D-02).
**How to avoid:** Mutate STATE.md only via gsd-tools handlers; verify `git status --short --branch` shows `milestone/v1.5`; ensure the package self-references only its own snapshot copies. Commit via `scripts/agent-commit`, one atomic commit per plan.

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---------|-------------|-------------|-----|
| Capturing source commit hashes for the manifest (D-02) | A bespoke provenance tracker | `git rev-parse HEAD` / `git log -1 --format=%H -- <path>` | Standard, re-derivable, pins research state |
| Summarizing the blacklist for the context file | Re-deriving counts by eye | `python3 -c "import json; ..."` one-liner (already used here: 65 = 2 hier + 63 std) | Deterministic; but the *count claim* still rides the CLM table |
| STATE.md gate-open record | Hand-edited YAML/prose | gsd-tools state handlers (D-17) | Anti-pattern 15; keeps state schema valid |
| Commit | Raw `git commit` | `scripts/agent-commit` | Project Git Commit Protocol; hooks + trailers enforced |
| Resolution-doc schema | A prescribed template | Format-precedent pointer only (D-16) | The resolution doc is the user's product; prescribing it is a deferred idea |

## Validation Architecture

> `nyquist_validation` is enabled, but Phase 23 ships **documents, not code** — there is no test framework, no `pytest`/runtime suite. The analogous acceptance checks are structural completeness checks on the deliverables, executed by inspection (and, for the consolidation gate, by user sign-off). No Wave 0 test infrastructure applies.

### Deliverable acceptance checks (map to success criteria)

| Req | Check | Method |
|-----|-------|--------|
| PKG-01 | Every finding's adjudication document is present in the package; specs are byte-identical to source (hash match); consolidation plan was surfaced to the user before assembly | Manifest cross-check + `git hash-object` / `diff` on each intact spec; D-07 user-gate record |
| PKG-02 | Every contested/unverified finding in the inventory above has a corresponding neutral question; the six locked conventions appear verbatim in the preamble; doc-03 boundary stated | Checklist against `## Issue-02 Finding Inventory` and `## Locked v1.4 Convention Citations` |
| PKG-03 | No dataset figure appears in prose without a CLM-ID; every CLM row has a status; no `verified` row cites a non-`Documentation/`/non-probe source | Grep figures vs CLM IDs; audit each `verified` citation against D-13 |
| PKG-04 | `23-DQA-CHARACTERIZATION.md` exists with provenance + section map + compatibility relation + inclusion recommendation; `data_quality_assessment.md` unchanged | Presence check + `git diff --quiet` on the DQA file |
| (criterion 5) | STATE.md records the gate open via handlers; delivery note states the resolution-doc path, Phase 24 parallelism, and the Phase 25–29 gate | Inspect STATE.md handler output + delivery note |

### Wave 0 Gaps
None — no test infrastructure is required for a documentation-assembly phase. The "checks" above are inspection-based deliverable audits, not automated tests.

## Standard Stack

**Not applicable.** Phase 23 installs no libraries and writes no application code. Tooling is entirely pre-existing repo infrastructure: `git` (snapshots, hashes, commit via `scripts/agent-commit`), `python3` stdlib (`json` for the blacklist summary), and `gsd-tools` (STATE.md handlers, commit helper). No new dependency is introduced.

## Package Legitimacy Audit

**Not applicable** — no external packages are installed in this phase. No npm/PyPI/crates additions; nothing to audit for slopsquatting. (The only executables invoked are `git`, `python3` stdlib, and the repo's own `scripts/agent-commit` and `gsd-tools`.)

## Security Domain

> `security_enforcement` is absent (= enabled by default), but this phase has no authentication, session, cryptography, or untrusted-input surface — it assembles internal documentation from the repo. Standard ASVS categories do not map.

The only security-adjacent concerns are **governance/provenance integrity**, covered under Common Pitfalls: (1) pinning source commit hashes so snapshots are traceable (D-02); (2) not leaking out-of-scope or overridden sources (`pinn/`, doc-03 content) into the external package; (3) not presenting unverified figures as fact (PKG-03). These are correctness-of-handoff controls, not application security controls. No threat-model table applies.

## Environment Availability

| Dependency | Required by | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| git | Snapshots, commit hashes, `agent-commit`, branch check | ✓ | repo on `milestone/v1.5` | — |
| python3 (stdlib `json`) | Blacklist summary for context file | ✓ | system python3 | Manual count (discouraged) |
| gsd-tools | STATE.md handlers (D-17), commit helper | ✓ | repo `gsd-core` | — |

**Missing dependencies:** none. All source documents to be snapshotted exist on disk and were read during this research (issue doc, both specs, `sampling_method.md`, DQA, `Documentation/` files). The package output directory `research_reports/02-data-pipeline-and-validation/` does **not exist yet** — the plan must create it.

## State of the Art

| Old approach | Current approach | When changed | Impact |
|--------------|------------------|--------------|--------|
| v1.4 ran verification before/around research | v1.5 phase-order swap: **research package first (Phase 23)**, empirical verification second (Phase 24, in parallel with the gate) | 2026-06-10 | Package figures ship `claimed-unverified` (PKG-03); Phase 24 forwards a DATA-07 correction addendum |
| SCS gate as raw-drift threshold `|SCS|>1e-5` | Post-v1.3: `ε_H` = raw drift, `SCS = log₁₀(ε_H)`, gate `ε_H>10⁻⁵` / `SCS>−5` (tightened from `−4`) | Post-v1.3 (SI-DQA-003, commit `3732f1f`) | The issue-02 ratio thresholds (`>1e-6`/`<1e-8`) conflict with this; pose neutrally |

**Deprecated / overridden:**
- Issue-02's "Canonical: `pinn/data-processing-pipeline-full.py`" citation — overridden 2026-05-19 (SCOPE-10); specs are source of truth.
- Issue-02's `D = 6.694` global scale — contradicted by the locked PHYS-01 raw-mass `D ≈ 4.6416` (ctl §2.5, line 598 explicitly rejects the 6.694 form). Not deprecated *by* the package — posed as a conflict to adjudicate (Phase 27).

## Assumptions Log

| # | Claim | Section | Risk if wrong |
|---|-------|---------|---------------|
| A1 | The blacklist `65` count is groundable as `verified` from `Documentation/problematic_ics_blacklist.json` (observed 2+63=65) under D-13 | CLM inventory | LOW — Phase 24 (DATA-02) re-verifies; over/under-marking is harmless. The *consumption* status remains claimed regardless. |
| A2 | The mass-weighted COM projection-head formula is fully specified within `pinn_architecture.md` §5.2 (763–795) + §10.2 | Locked conventions | LOW — §10.2 "COM Invariance" acceptance check confirms enforcement; executor quotes the exact subsection. If the formula is partly in ctl Step 2.2, cite both. |
| A3 | Including the DQA snapshot is the right call (recommend YES) | PKG-04 | LOW — final inclusion rides the D-07 user checkpoint; recommendation is advisory only. |
| A4 | `sampling_method.md` should ship (recommend YES, per discretion) | Document list | LOW — explicitly Claude's discretion; rides D-07. |
| A5 | The README's per-variant parameter/footer counts (4,857; 219; 592; 2,749/2,565) are current as of the committed README and count as grounding | CLM inventory | LOW — README is in `Documentation/` (D-13 grounding); Phase 24 re-verifies. |

**Note:** No assumption here is a *semantic adjudication* of any finding — that is forbidden in Phase 23 (Deferred; Phase 25 territory). All assumptions are about packaging mechanics and grounding status, which Phase 24 independently re-verifies.

## Open Questions (RESOLVED)

> Plan-checker reconciliation 2026-06-10: all three questions below are resolved by the
> committed 23-0N plans — Q1 by Plan 04 Task 1 (cite STATE.md decision + SI-DQA-003 as
> authority, DQA lines as location), Q2 by Plan 04 Task 2 (both M13 options posed neutrally
> with the Phase-26 STOP-gap annotation), Q3 by Plan 02 (the D-07 user checkpoint locks the
> final document count at execution).

1. **RESOLVED (Plan 04 Task 1)** — **Does citing the SCS gate to a read-only, non-authoritative research report satisfy "locked convention as hard constraint" (PKG-02/D-10)?**
   - What we know: The gate is ratified post-v1.3 (STATE.md decision; SI-DQA-003) but its only written home is `data_quality_assessment.md` (read-only, SCOPE-09).
   - What's unclear: Whether the package should cite DQA directly, or cite the STATE.md decision / SI-DQA-003 as the authority and DQA as the location.
   - Recommendation: Cite both — STATE.md decision + SI-DQA-003 as the ratifying authority, DQA lines 120/130/234 as the location. This is a presentation choice (mechanical), not a semantic gap — proceed; note the choice in the manifest. If the executor judges it forces a semantic call, STOP and log to `23-GAPS.md`.

2. **RESOLVED (Plan 04 Task 2)** — **M13 fallback policy framing (skip-to-Stage-6 vs flagged low-fidelity) — is posing both options "neutral framing" or does it pre-shape the research?**
   - What we know: Issue-02 line 65/287 names two options; PIPE-05 (Phase 26) says "if sources are silent/conflicting on the fallback, surface as a STOP gap, not invent."
   - What's unclear: Whether Phase 23 should pose the question with both options or flag it as a known STOP candidate for Phase 26.
   - Recommendation: Pose neutrally with both options listed as the issue-doc's candidates; annotate that the choice is a Phase-26 STOP-gap candidate. Do not assert a fallback.

3. **RESOLVED (Plan 02, D-07 gate)** — **Final document count and consolidation boundary** — locked only at execution after the D-07 user checkpoint and the PKG-04 outcome. Not resolvable in research; Plan 02 models the D-07 gate as a hard user checkpoint (`autonomous: false`) before assembly.

## Sources

### Primary (HIGH confidence)
- `pinn_instruction/issues/02-data-pipeline-and-validation.md` (364 lines, full read) — finding inventory, dataset figures, recommended resolutions, references.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` (headings + targeted reads) — 14D contract (Step 4, 1000–1014), IC₁₃ (1011–1014), PHYS-01 D convention (§2.5, 581–598), dual-epsilon (703), stage energy check (1295–1296).
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (headings + targeted reads) — COM projection head (§5.2, 763–795; §10.2, 972), PHYS-03 softening (§3.2/§3.4, 372–534).
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` (headings + targeted reads) — metric definitions §3, SCS gate (120/130/234), SI-DQA-002/003 (308–328); git provenance via `git log --follow`.
- `simulation_data/Documentation/README.md` (targeted reads) — Dataset Sizes (81–90), Brutus Parameters by Variant (584–628), Completeness Checks + Snapshot Count Note (629–660).
- `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` — 184/2,749/2,565 grounding.
- `simulation_data/Documentation/problematic_ics_blacklist.json` — blacklist shape + count (2 hier + 63 std = 65).
- `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, `23-CONTEXT.md` — locked decisions, requirements, scope, governance.
- `pinn_instruction/.../research_reports/01-architecture-and-physics-foundations/` (ls + heading grep) — v1.4 layout + `ctl_pinn_resolution.md` structure.
- `.planning/research/edl/EDL-19-01-epsilon-H.md` (heading grep) — EDL brief format precedent.

### Secondary / Tertiary
- None. All findings are from direct reads of repository files (codebase grep/read). No web sources; no external libraries.

## Metadata

**Confidence breakdown:**
- Finding inventory & line ranges: HIGH — full direct read of the issue doc.
- Locked-convention citations: HIGH — direct reads located each; SCS-gate-only-in-DQA finding verified by repo-wide grep.
- CLM verified/claimed split: HIGH for grounded figures (Documentation/ reads), HIGH for "claimed" classification (README explicitly warns on snapshot counts); the blacklist-65 grounding is a D-13 recommendation (A1).
- DQA characterization inputs: HIGH — section map + git provenance verified.
- Pitfalls: HIGH — each is anchored to a specific governance rule + a located source line.

**Research date:** 2026-06-10
**Valid until:** Stable until the framework specs, the issue doc, or the `Documentation/` files change. Re-verify line ranges if any spec is edited (no v1.5 spec edits land before Phase 26). ~30 days nominal.
