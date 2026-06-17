# Phase 27: Sampling, Precision, and Global-Scale Contracts - Research

**Researched:** 2026-06-13
**Domain:** Spec-adjudication / transcription (v1.5 Issue-02 data-pipeline contracts). Internal-only; no external research applicable.
**Confidence:** HIGH (every verdict is upstream-locked; edit sites located by direct grep against current spec text)

## Summary

Phase 27 is a **transcription phase**, not a decision phase. All four contracts (PIPE-04/07/08/09) have LOCKED verdicts in Phase 25 evidence packets or Phase 24 remediation artifacts; the planner's job is to land the canonical phrasing into `ctl_instruction.md` (primary) and `pinn_architecture.md` (secondary, two narrow spots), move the touched Phase 24 ledger rows to `VERIFIED`, and run four spec-string acceptance checks (AC-PIPE-04/07/08/09 — seeded, no new IDs). The single most valuable input below is the **Exact Edit-Site Map**: three of the four contracts edit text that ALREADY EXISTS in the spec (Mini-Batch Construction line 1417-1423; §2.5 D derivation line 744-774; the §2.6 metadata schema + footer contract). Only PIPE-08's `sample_replay`/`sample_lookahead` stage-query interface and the PIPE-07 precision note are net-new spec text, and both have grounded spec-ready prose (resolution-doc §4.3 line 481-489 for precision; issue-03 curriculum doc lines 683-684 for the method semantics).

**Spec-ready prose already exists in the grounding sources** for PIPE-04 (m11-m12-severity.md:105-113; resolution-doc §4.1 lines 408-418), PIPE-07 (resolution-doc §4.3 lines 481-489), and PIPE-09 (compute-globals-D.md:104-108; resolution-doc §4.4 line 493+). The planner should transcribe these blocks, not paraphrase.

**Primary recommendation:** Plan four task-groups in CONTEXT D-13 order (M12/G5 → precision → stage-query → compute_globals). Transcribe the locked prose blocks verbatim, cite the named evidence packet + DATA-06/DATA-05 facts inline, and gate each ledger row's move to `VERIFIED` on a mechanical grep-based acceptance check. Surface ONE candidate process-schema STOP gap before planning closes (PIPE-07/PIPE-08/G5 packet-requirement ambiguity — see Candidate STOP Gaps).

## Project Constraints (from CLAUDE.md / AGENTS.md / SPEC / CONTEXT)

- **STOP protocol in full:** source-silent semantic / process-schema / cross-phase decisions MUST be surfaced, never invented. Subagents return candidate gaps; the orchestrator logs them.
- **Grounding hierarchy:** LOCKED = Phase 25 packets + Phase 24 verified-facts/remediation + 27-SPEC. Resolution doc = candidate (cite-only). Issue doc = non-authoritative (source-position/rejected-claim citations only). On-disk `simulation_data/` = empirical grounding. **Live `pinn/` code is NOT grounding** (forward FUT-01 hand-off references only).
- **No re-adjudication (D-03):** M12 third-position rule, PIPE-09 raw-mass D — do not reopen 0.5 factor, `D=6.694`, `M_tot_ref`, mass-fraction encoding, or `E_scale` rules.
- **Edit-target scope:** `ctl_instruction.md` (primary), `pinn_architecture.md` (secondary). `sampling_method.md` FROZEN (SCOPE-08, cite-only). `data_quality_assessment.md` READ-ONLY (SCOPE-09, cite-only).
- **No new AC IDs (D-06):** AC-PIPE-04/07/08/09 only.
- **Ledger lifecycle (D-07):** `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` (or explicit `DEFERRED`). Status + evidence link + spec edit + AC result travel in the SAME logical plan commit (same-commit discipline, evidence/README.md:101).
- **Git:** `scripts/agent-commit` with `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`; conventional-commit `<type>(27[-NN]): ...`; body required for spec/evidence/verify/plan commits; no raw `git commit`, no broad staging, no push from `milestone/*`.
- **Known stale text (do NOT flag):** ROADMAP.md line 228 success-criterion 1 still names the OLD candidate `min(32, int(0.5 * n_snapshots))`. Superseded by the Phase 25 M12 verdict. Note the supersession; it is not an open decision.

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| PIPE-04 | M12 points-per-trajectory: `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))`, without replacement, default cap 32, NO `0.5` factor; cite DATA-06 medians; expose `n_snapshots`/`dt_out` metadata; M16 deferred to doc-03. | Verdict locked in `m11-m12-severity.md` (`accept-third-position`); spec-ready prose at :105-113. Edit site: ctl Mini-Batch Construction (1417-1423) + line 498 cross-ref already present. DATA-06 medians: VERIFIED-FACTS CLM-10 (61/127/1003). |
| PIPE-07 | Precision: float64 sufficient for data-side metrics/invariants; `decimal.Decimal` ONLY as failure-classifier for a future IC→Brutus t=0 mass gate; current IC masses canonical; the 70 stale base-hier artifacts = staleness, NOT precision failure (rerun-remediated 70/70 at float64 mass equality). | Verdict: DATA-05 RESOLVED-WITH-INSTRUCTION (ledger mass-drift/footer rows); validation 70/70 PASS (`24-DATA05-RERUN-VALIDATION.md`). Spec-ready prose: resolution-doc §4.3 lines 481-489. Edit site: net-new note after ctl §2.1 (line 576). |
| PIPE-08 | DataLoader exposes per-traj `dt_out` + `n_snapshots` metadata; `sample_replay(n, max_stage)` + `sample_lookahead(n, stage)` (names LOCKED by SPEC); preserve PIPE-06 footer/default provenance; doc-03 forward-ref for M16; data-side only. | Metadata fields already in ctl §2.6 schema (line 811) + footer contract (358-392). Method semantics grounded: issue-03 curriculum doc lines 683-684; REQUIREMENTS PIPE-08. Edit site: net-new stage-query sub-section in ctl + arch §3.1 note. |
| PIPE-09 | `compute_globals`: raw-mass PHYS-01 `D=(G·T²)^(1/3)≈4.6416` canonical; reject `D=6.694`/`M_tot_ref` BY NAME; `E_scale` floor `+1e-8`; leave Phase 28 SCS alone. | Verdict locked in `compute-globals-D.md` (`accept-resolution`); spec-ready prose at :104-108. Edit site: ctl §2.5 (744-774) already carries the derivation + 6.694 rejection; consolidate into a normative contract + fix `E_scale` outlier. |

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Points-per-trajectory sampling (PIPE-04) | Data-side spec (`ctl` Mini-Batch) | Arch §3.1 (code-default note) | Sampling is a DataLoader/data-loss contract; arch only carries the `points_per_trajectory=32` code default. |
| Precision/mass policy (PIPE-07) | Data-side spec (`ctl` §2.1/§2.6) | — | Parsing/metric precision is a data-pipeline concern; no architecture surface. |
| `dt_out`/stage-query interface (PIPE-08) | Data-side spec (`ctl` §2.6 + new sub-section) | Arch (visibility note for FUT-01) | Metadata exposure + query signatures are data-side; arch note makes the interface visible to the consumer. |
| Global-scale `D`/`E_scale` (PIPE-09) | Data-side spec (`ctl` §2.5) | Arch §5.2 (`E_scale` consistency) | `compute_globals` is a preprocessing contract; arch §5.2 already mirrors the network-facing `E_scale=+1e-8`. |

## Standard Stack

Not applicable — no external packages installed. Phase 27 edits Markdown framework-spec documents and `.planning/` ledger/evidence files. The only tooling is `scripts/agent-commit` + `.githooks` (already present) and `grep`/`python` for acceptance-check probes. **Package Legitimacy Audit: N/A (no package installs).**

## Exact Edit-Site Map (most decision-relevant section)

All line numbers are current as of 2026-06-13 against the two edit-target files.

### PIPE-04 / M12 — `ctl_instruction.md`

| Site | Lines | State | Current wording (quoted) | Action |
|------|-------|-------|--------------------------|--------|
| Mini-Batch Construction | **1417-1423** | EDIT-IN-PLACE | "Sample $n_{\text{pts}}$ (e.g., 32) time points per trajectory: 50% uniform from $[0, T]$, 50% weighted by acceleration norm (prioritizes close encounters)." | Replace/augment with the locked `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` contract: without-replacement, seeded `k_w = floor(n_pts/2)` weighted-then-uniform split, cap-32-as-example flagged non-evidence-based, explicit `0.5×` rejection, cite `m11-m12-severity.md` + DATA-06 medians. |
| Admission-gate cross-ref | **493-500** | ALREADY PRESENT (Phase 26 B-06) | "The per-trajectory *sampling* point count is governed by the locked M12 rule `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` (locked M12 rule, see Phase 27 PIPE-04; transcribed in `m11-m12-severity.md`), not by any admission floor." | Leave as-is OR tighten the forward-ref to point at the now-landed Mini-Batch text. **REGRESSION SURFACE** — this is Phase 26 B-06 admission text; if touched, re-run AC-PIPE-01 (D-14). |
| `n_snapshots`/`dt_out` metadata | §2.6 schema **811** (`brutus_tolerance, word_length, dt_out, trustworthy_horizon`) | ALREADY PRESENT | `dt_out` is in the stored-metadata schema; `n_snapshots` is implied by `times_raw: (Nt,)`. | Confirm both are stated as data-side metadata; M12 prose should reference them as the "forward interface for the deferred M16 collocation-density question (doc-03)." |

**Spec-ready prose to transcribe** (`m11-m12-severity.md:105-113`, and identical resolution-doc §4.1 block lines 408-418): the locked-convention paragraph beginning "Per-trajectory data-loss point count." Copy verbatim; do not re-derive.

### PIPE-04 / M12 — `pinn_architecture.md`

| Site | Lines | State | Current wording | Action |
|------|-------|-------|-----------------|--------|
| §3.1 Batch Construction | **329-344** | code-default only | `def get_batch(batch_size, points_per_trajectory=32):` + `N_data = batch_size * points_per_trajectory  # e.g., 256 * 32 = 8192` | Note `points_per_trajectory=32` is a **code default, not the spec contract** (m11-m12-severity.md:31,124 says so explicitly). Line 351 already carries an Author Comment "This above batch construction is not consistent with the CTL instruction plan." Optional: add a one-line pointer to the ctl Mini-Batch contract. Keep minimal (D-02: arch touched only where needed). |

### PIPE-07 / DATA-05 precision — `ctl_instruction.md`

| Site | Lines | State | Current wording | Action |
|------|-------|-------|-----------------|--------|
| §2.1 mass-invariance gate | **560-576** | ALREADY PRESENT (float64 gate) | "Step 1 parses ... in float64"; "`max_t,i \|m_i(t) - m_i(0)\| < 1e-15` in float64 parse space." + IC↔Brutus consistency clause. | Append the precision note AFTER §2.1 (resolution-doc §4.3 says "note appended after §2.1"). Net-new but short. |
| §2.6 / admission gate | **467, 484-486** | ALREADY PRESENT | line 467 "...PIPE-07 use until rerun validation from the current canonical ICs passes"; line 484-485 the float64 mass-invariance + "IC<->Brutus `t=0` mass gate (§2.1 as amended per Q-B2)". | Confirm the mass-gate + Decimal-classifier semantics are stated; the float64/Decimal split lands as the §2.1 note. |

**Spec-ready prose to transcribe** (resolution-doc §4.3 lines 481-489): the block "Validation metrics (SCS, SASD, IPR, PSC), invariants, and completeness checks are computed in CPU float64 ... decimal.Decimal is reserved for the §2.1 mass-gate escalation classifier ... no denominator floor is inserted into the locked SCS formula." Copy verbatim.

### PIPE-08 / stage-query — `ctl_instruction.md` + `pinn_architecture.md`

| Site | Lines | State | Current wording | Action |
|------|-------|-------|-----------------|--------|
| `ctl` §2.6 metadata schema | **791-824** | metadata PRESENT | `dt_out` (811) + `param_provenance` map (814-821) + `times_raw:(Nt,)` (804). | Confirm `dt_out` + `n_snapshots` are named per-trajectory metadata. Preserve the PIPE-06 `param_provenance` footer/default provenance (REGRESSION SURFACE — Phase 26 D7). |
| `ctl` stage-query interface | **NEW sub-section** (co-locate near Mini-Batch 1417 or §2.6) | NET-NEW | none — `sample_replay`/`sample_lookahead` do not yet appear in `ctl`/`arch`. | Add a data-side query-interface sub-section: `sample_replay(n, max_stage)` (sample n trajectories from cumulative D_≤k) + `sample_lookahead(n, stage)` (sample n from D_{k+1}); keep data-side, no training-loop policy; doc-03 forward-ref for M16. |
| `arch` visibility | §3.1 region (~325-351) | NET-NEW | none | Optional one-line note that the data-side loader exposes these signatures (D-02: only where FUT-01 needs visibility). |

**Method semantics grounding** (NOT live `pinn/` code — these are issue/curriculum spec docs): `pinn_instruction/issues/03-curriculum-and-training-loop.md:683-684` — "`sample_replay(n=240, max_stage=k)` — sample n trajectories from cumulative D_≤k; `sample_lookahead(n=16, stage=k+1)` — sample n trajectories from D_{k+1}." Also REQUIREMENTS PIPE-08 and issue-02 line 346 carry the names. The SPEC LOCKS the names; semantics are grounded in the curriculum spec doc.

> **NOTE — cross-doc provenance caveat:** issue-03 is a *non-authoritative* issue doc for milestone doc-03, not Issue-02. It is a legitimate source for the method *names/semantics* (which 27-SPEC independently locks), but the planner should cite REQUIREMENTS PIPE-08 + 27-SPEC as the authority and issue-03 only as the descriptive semantics reference. If the planner finds the semantics under-specified beyond "sample n trajectories from the cumulative/next-stage set," that is a candidate gap (see STOP gaps) — do not invent return types, ordering, or seeding policy.

### PIPE-09 / compute_globals — `ctl_instruction.md` + `pinn_architecture.md`

| Site | Lines | State | Current wording (quoted) | Action |
|------|-------|-------|--------------------------|--------|
| `ctl` §2.5 D derivation | **744-767** | ALREADY PRESENT | "`D = (G*T**2)^(1/3)`"; "With `G = 1`, `D ~ 4.6416`."; "The alternative $D = (G M_{\mathrm{tot}} T^2)^{1/3} \approx 6.694$ is correct only under a mass-fraction convention rewrite ... not adopted in v1.4." | Consolidate the existing derivation + rejection into a **normative `compute_globals` contract**: explicitly prohibit `M_tot_ref` as a config knob BY NAME, restate Plummer-vs-additive-ε rule, record admitted-set scope. The D VALUE does not change (compute-globals-D.md:123 "accept-resolution as no-change"). |
| `ctl` §2.5 `E_scale` floor | **771** | OUTLIER to fix | "$E_{\mathrm{scale}} = \lvert \mathrm{median}(\{E_j\}) \rvert + 10^{-10}$" | **Change `+10^{-10}` → `+10^{-8}`** (2-of-3 editable-spec majority; compute-globals-D.md:106). This is a Phase 27 EDIT DECISION pre-reasoned in the packet, NOT a re-adjudication. The `+1e-8` already appears at ctl Step-4 (~1049) and arch §5.2 (761). |
| `arch` §5.2 `E_scale` | **761** | ALREADY `+1e-8` | "`E_scale = \|median_traj(E)\| + 10^-8`" | No change (already matches the canonical value). Confirm consistency only. |

**Spec-ready prose to transcribe** (`compute-globals-D.md:104-108`): the "Global-scale D (HC-6 / PHYS-01)" locked-convention paragraph (D value, raw-mass justification, `M_tot_ref` prohibition, `E_scale=+1e-8`, Plummer/additive-ε rule, admitted-set scope). Copy verbatim.

## Locked-Verdict Extraction (canonical phrasing to transcribe)

| Contract | Source (path:line) | Verdict enum | Canonical phrasing anchor |
|----------|--------------------|--------------|----------------------------|
| PIPE-04 / M12 | `evidence/m11-m12-severity.md:87-89` | `accept-third-position` | "`n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` ... without replacement ... `n_pts_cap` defaults to 32 ... **No `0.5 × n_snapshots` factor is imposed**" (:105-113) |
| PIPE-07 / DATA-05 | `24-ISSUE-LEDGER.md:41,457-461` + `24-DATA05-RERUN-VALIDATION.md:1-6` | RESOLVED-WITH-INSTRUCTION (DATA-05); resolution-doc Q-B3 verdict | "float64 is sufficient for all data-side validation metrics ... `decimal.Decimal` ... sole required role is the Q-B2 escalation classifier" (resolution-doc §4.3:469); "70/70 ... satisfy `m_IC == m_Brutus(t=0)` at float64" (remediation:110-112) |
| PIPE-08 | `24-ISSUE-LEDGER.md:329-334` (G5) + REQUIREMENTS PIPE-08 | (data-side; closes with M12/G5) | "`sample_replay(n=240, max_stage=k)` — sample n trajectories from cumulative D_≤k; `sample_lookahead(n=16, stage=k+1)` — sample n from D_{k+1}" (issue-03:683-684, semantics only) |
| PIPE-09 | `evidence/compute-globals-D.md:76` | `accept-resolution` | "`D = (G·T²)^(1/3) ≈ 4.6416` ... The mass-fraction alternative `D = (G·M_tot·T²)^(1/3) = 6.694` ... is **rejected as a pipeline instruction** ... No configuration parameter may select the mass-fraction form ... **`E_scale` floor:** `E_scale = |median(E)| + 1e-8`" (:104-106) |

## Evidence-Packet Mapping per Finding (CRITICAL process check)

Per evidence/README.md EVID-10 trigger table (lines 73-78) + EVID-06 packet-before-edit rule (line 99) + D-05/D-06/D-08:

| Finding | Has packet? | Packet path | EVID-10 trigger? | Disposition |
|---------|-------------|-------------|------------------|-------------|
| PIPE-04 / M12 | ✅ YES | `evidence/m11-m12-severity.md` | YES (severity reclass) — adjudicated | Transcribe; cite packet by path. |
| PIPE-09 / D=6.694 | ✅ YES | `evidence/compute-globals-D.md` | YES (convention conflict) — adjudicated | Transcribe; cite packet by path. |
| PIPE-08 / G5 | ❌ NO (by design) | closes with M12 (D-08/D-12) | NO | "G5 closes with M12 ... no separate evidence packet" (ledger:192-193). |
| PIPE-07 / DATA-05 (mass-drift + footer rows) | ⚠️ AMBIGUOUS | points to `24-DATA05-RERUN-REMEDIATION.md` (Phase 24 artifact, NOT an `evidence/{id}.md` packet) | NOT in the EVID-10 table | **See Candidate STOP Gap G-27-01.** |

**The ambiguity:** EVID-06 (README:99) states "No spec edit in Phases 26-28 is permitted without a completed evidence packet + verdict for the finding being edited. Each owning spec-edit phase authors its non-conflict packets immediately before its edits." PIPE-07 is a non-conflict finding (not EVID-10) whose verdict already lives in Phase 24 remediation/validation artifacts. Whether that satisfies "a completed evidence packet" — or whether Phase 27 must author a NEW `evidence/{pipe-07}.md` (or `evidence/mass-drift.md`) under the `_TEMPLATE.md` schema — is not unambiguously answered. The ID→Filename map (README:119-129) does NOT list a PIPE-07 / mass-drift / footer packet name. This is a **process-schema** decision; do not invent a packet structure or unilaterally decide none is needed.

## Ledger-Row Map

Stable path: `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md`. Status enum: `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` (or `DEFERRED`).

| Row | Line | Current status | Verdict (current) | Phase 27 transition |
|-----|------|----------------|-------------------|----------------------|
| M12 | 26 | PENDING (adjudicated-but-unfixed) | `accept-third-position` | → IN_PROGRESS → FIX_APPLIED → **VERIFIED** (AC-PIPE-04 pass) |
| G5 | 33 | PENDING | — (closes with M12, D-08) | → **VERIFIED** synthesis-close with M12; record doc-03 M16 deferral. No separate packet. |
| footer | 40 | PENDING | — (GAP-24-01 RESOLVED; rerun done) | PIPE-07 facet → **VERIFIED** (AC-PIPE-07). NOTE: the PIPE-06 footer facet was already VERIFIED via D7 row (line 28) in Phase 26 — Phase 27 owns only the PIPE-07 precision facet of this row. |
| mass-drift | 41 | PENDING | — (DATA-05 RESOLVED; 70/70 validated) | → IN_PROGRESS → FIX_APPLIED → **VERIFIED** (AC-PIPE-07). |
| D=6.694 | 39 | PENDING (adjudicated-but-unfixed) | `accept-resolution` (CLM-13 convention-rejected) | → IN_PROGRESS → FIX_APPLIED → **VERIFIED** (AC-PIPE-09). |

**G5-closes-with-M12 synthesis rule (D-08):** G5 is a data-side facet over M12 + M16-deferred metadata; it gets NO separate packet and closes with M12, recording the doc-03 M16 deferral. (`m11-m12-severity.md:140` "G5->M12 close with parent"; ledger:192-193.)

**Same-commit discipline (README:101):** each row's status edit + evidence link + spec edit + AC result must land in ONE commit. Splitting across commits is a process defect.

## Regression Surface (Phase 26 sections that overlap Phase 27 edits)

Per CONTEXT D-14 + evidence/README.md Regression Policy (line 83). If a Phase 27 edit touches the listed text, re-run the named AC and confirm the Phase 26 row stays VERIFIED.

| Phase 26 contract | Shared spec text | Overlaps | Re-run if touched |
|-------------------|------------------|----------|-------------------|
| **B-06 admission gate** (AC-PIPE-01) | ctl Step-1A admission text, esp. lines 493-500 (the M12 forward-ref + `>=200` floor rejection + DATA-06 medians) | PIPE-04 sampling | AC-PIPE-01 (grep `## Step 1A — Trajectory Admission Gate`, `final_timestep >= 9.5`, `SCS > -5`, no `>= 200` floor). Precedent: m11-m12-severity.md:171 already did this for the M11 sub-section. |
| **D7 footer provenance** (AC-PIPE-06) | ctl Step-1 item 3 footer contract (358-392) + §2.6 `param_provenance` (814-821) | PIPE-07/PIPE-08 (precision note near §2.1; metadata exposure in §2.6) | AC-PIPE-06 (grep footer all-or-nothing contract + `param_provenance` `{direct, inferred, absent, measured}` + folder defaults). |
| **D-03 HDF5 format** (AC-PIPE-10) | ctl Step 1 item 6 (HDF5 canonical) | only if PIPE-08 metadata text is moved near Step-1 item 6 | AC-PIPE-10 (grep HDF5-canonical wording) — only if nearby text is relocated. |

## Acceptance-Check Design (AC-PIPE-04/07/08/09 — seeded, no new IDs)

Each AC is a **spec-string + evidence-link** assertion the executor runs mechanically. The "signal" is the locked verdict's correct presence in the edited spec + its packet/fact citation + the ledger transition. Frame as grep assertions over the edited files plus a dataset-fact cross-check.

### AC-PIPE-04
- **Asserts:** ctl Mini-Batch text states `min(n_pts_cap, n_snapshots)`, "without replacement", default cap 32 flagged as example/non-evidence-based, NO `0.5 * n_snapshots`, DATA-06 medians (61/127/1003) cited as facts (not hard per-file guarantees), `n_snapshots`/`dt_out` exposed as metadata, M16→doc-03 deferral, and cites `m11-m12-severity.md`.
- **Mechanical check:** `grep -E 'min\(n_pts_cap, n_snapshots' ctl_instruction.md` returns the Mini-Batch site; `grep -i '0\.5 \* n_snapshots\|0\.5×' ` returns ONLY rejection context (no normative use); `grep '61\|127\|1003' ` confirms DATA-06 cite; `grep 'm11-m12-severity'` confirms packet link. Cross-check CLM-10 medians via `data06_snapshots.py` probe (re-derivable).
- **Negative-control (no false pass):** assert the `0.5` factor appears ONLY adjacent to "reject"/"unevidenced", never as the operative rule.

### AC-PIPE-07
- **Asserts:** specs name float64 sufficiency for data-side metrics/invariants; Decimal-only-as-classifier for a future mass-gate; current IC masses canonical; the 70 base-hier artifacts rejected as STALE not precision; a fail condition for a future mass-gate mismatch; DATA-05 rerun remediation consumed.
- **Mechanical check:** `grep -i 'float64'` near §2.1 returns the precision note; `grep -i 'decimal.Decimal\|classifier'` confirms classifier-only framing; `grep -i 'stale\|canonical'` confirms staleness interpretation; cite `24-DATA05-RERUN-VALIDATION.md` (70/70 PASS). Cross-check: `data05_mass_drift.py` on remediated state (0 mismatches expected).
- **Negative-control:** assert Decimal is NOT named as the routine parse/metric path (only the escalation classifier).

### AC-PIPE-08
- **Asserts:** ctl exposes per-traj `dt_out` + `n_snapshots`; both stage-query signatures `sample_replay(n, max_stage)` + `sample_lookahead(n, stage)` present with data-side semantics; PIPE-06 footer/default provenance preserved; doc-03 forward-ref for M16; no training-loop policy.
- **Mechanical check:** `grep 'sample_replay(n, max_stage)\|sample_lookahead(n, stage)'` (exact signatures); `grep 'dt_out\|n_snapshots'` in §2.6; `grep 'param_provenance'` confirms PIPE-06 preservation; `grep -i 'doc-03\|M16'` confirms deferral.
- **Negative-control:** assert no replay-fraction / collocation-density POLICY text (that is doc-03); only the data-side interface.

### AC-PIPE-09
- **Asserts:** ctl §2.5 matches the compute-globals-D.md verdict: raw-mass `D=(G·T²)^(1/3)≈4.6416` canonical; `D=6.694` and `M_tot_ref` rejected BY NAME; `E_scale = |median(E)| + 1e-8`; additive-ε prohibited; admitted-set scope; Phase 28 SCS untouched.
- **Mechanical check:** `grep '6.694'` returns ONLY rejection context; `grep 'M_tot_ref'` returns ONLY prohibition context; `grep '1e-10' §2.5` returns NOTHING for `E_scale` (outlier fixed); `grep '4.6416\|(G.T'` confirms canonical D; `grep -i 'additive'` confirms PHYS-03 prohibition. Optional: dimensional-consistency unit check on a two-body circular orbit (length-scale sanity).
- **Negative-control:** assert `6.694`/`M_tot_ref` never appear as a selectable/canonical convention.

**First-principles dimensional sanity (permitted grounding):** `[G] = L³M⁻¹T⁻²`, so `[G·T²] = L³M⁻¹`. With raw masses absorbed into a unit-coefficient residual (`D³ = G·T²` at `G=1`), `D = (G·T²)^(1/3)` carries dimension `L` — a length scale. CONFIRMED (mirrors compute-globals-D.md:46-66 and v1.4 B-02). Short and uncontroversial; not a gap.

## Planning-Order / Batching Guidance

CONTEXT D-13 recommended order is sound and I confirm it: **M12/G5 → precision (PIPE-07) → stage-query (PIPE-08) → compute_globals (PIPE-09).**

- **Dependency rationale:** M12/G5 establishes the `n_snapshots`/`dt_out` snapshot-metadata contract that PIPE-08's stage-query interface references; doing PIPE-04 first means the metadata fields are settled before the interface wording cites them. PIPE-09 (`compute_globals`) is the most isolated (§2.5, no shared coupling with the SCS gate per compute-globals-D.md:139) and is safely last.
- **Batching:** PIPE-04 + G5 are one logical unit (G5 closes with M12). PIPE-07 + PIPE-08 both touch §2.1/§2.6 region and footer provenance — batch only if AC-PIPE-07 and AC-PIPE-08 + their ledger transitions stay individually reviewable (D-07). PIPE-09 should be its own plan/wave (isolated §2.5 edit + `E_scale` canonicalization).
- **No hard ordering constraint forces a multi-wave structure**, but same-commit discipline (status+evidence+spec+AC per finding) argues for one finding (or one tightly-coupled pair) per commit. Recommend ≥3 commits: {M12+G5}, {PIPE-07, possibly +PIPE-08}, {PIPE-09}.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Verdict prose for the four contracts | New paraphrased contract text | Verbatim transcription from m11-m12-severity.md:105-113, resolution-doc §4.3:481-489, compute-globals-D.md:104-108 | The packets contain spec-edit-ready prose authored for exactly this transcription; paraphrasing risks drift from the locked convention. |
| Evidence/ledger machinery | New schema/templates | Phase 25 `evidence/README.md` + `_TEMPLATE.md` + `24-ISSUE-LEDGER.md` | D-05: reuse, don't redesign. New schema = process-schema STOP gap. |
| Acceptance-check IDs | New AC IDs | Seeded AC-PIPE-04/07/08/09 | D-06: minting new IDs is prohibited. |
| Dataset facts (snapshot medians, mass-equality) | New probes from scratch | Re-run existing `data06_snapshots.py` / `data05_mass_drift.py` probes | Already re-derivable in VERIFIED-FACTS; re-deriving is fine, re-inventing is waste. |

**Key insight:** This phase's risk is *invention*, not *complexity*. Every artifact the planner needs already exists; the failure mode is paraphrasing a locked verdict into something subtly different, or inventing a packet/AC schema where the protocol is silent.

## Common Pitfalls

### Pitfall 1: Paraphrasing instead of transcribing
**What goes wrong:** Planner writes its own version of the M12 rule or D convention, drifting from the locked phrasing. **Why:** spec-ready prose is buried in the packets, easy to miss. **How to avoid:** transcribe the named anchor blocks verbatim. **Warning sign:** the edited spec says something the packet does not.

### Pitfall 2: Re-opening the ROADMAP `0.5` candidate
**What goes wrong:** treating ROADMAP line 228's `min(32, int(0.5 * n_snapshots))` as live. **Why:** it is stale but still in the roadmap. **How to avoid:** governance rule 4 — the M12 verdict supersedes it; note supersession, do not flag. **Warning sign:** any edit that re-introduces the `0.5` factor as operative.

### Pitfall 3: Authoring a PIPE-07 packet (or skipping one) without resolving the ambiguity
**What goes wrong:** inventing an `evidence/mass-drift.md` packet structure, or unilaterally deciding none is needed. **Why:** EVID-06 vs the EVID-10 table are ambiguous for non-conflict findings. **How to avoid:** surface G-27-01 before planning closes. **Warning sign:** a new file under `evidence/` not in the ID→Filename map, created without user instruction.

### Pitfall 4: Regressing Phase 26 B-06 / D7 text
**What goes wrong:** moving/editing admission-gate or footer text and silently breaking AC-PIPE-01/06. **Why:** PIPE-04 sampling text and PIPE-07 precision text sit adjacent to Phase 26 contracts. **How to avoid:** D-14 targeted rechecks. **Warning sign:** AC-PIPE-01 or AC-PIPE-06 grep fails after a Phase 27 edit.

### Pitfall 5: Citing live `pinn/` code as grounding
**What goes wrong:** referencing `pinn/data-processing-pipeline-full.py` to justify a contract. **Why:** it superficially looks authoritative. **How to avoid:** SCOPE-10 / directive 2026-05-19 — live code is NOT grounding; forward FUT-01 hand-off references only. **Warning sign:** any `pinn/*.py` path in a justification position.

## Runtime State Inventory

> Not a rename/refactor/migration phase. The DATA-05 dataset migration (70 stale base-hier reruns) was already executed and validated in Phase 24 (70/70 PASS, `24-DATA05-RERUN-VALIDATION.md`). Phase 27 only *consumes* that resolved state as evidence; it performs no data migration, no OS-registered state changes, no secret/env changes, and produces no build artifacts. **Nothing to inventory — verified by scope (spec-text + ledger edits only).**

## Validation Architecture

> nyquist_validation treated as enabled (not explicitly false). Deliverables are spec text + ledger transitions + acceptance checks — NOT runtime code. The acceptance-check assertions ARE the sampling mechanism.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Spec-string assertions (`grep`/`grep -E`) over edited Markdown + re-derivable dataset probes (`.venv/bin/python .../probes/*.py`) |
| Config file | none — checks are inline commands or small disposable scripts under `.planning/phases/27-*/` (Codex discretion, CONTEXT) |
| Quick run command | per-AC grep block against `ctl_instruction.md` / `pinn_architecture.md` |
| Full suite command | AC-PIPE-04 + AC-PIPE-07 + AC-PIPE-08 + AC-PIPE-09 + regression AC-PIPE-01/06 |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | Exists? |
|--------|----------|-----------|-------------------|---------|
| PIPE-04 | M12 rule landed, 0.5 rejected, DATA-06 cited | spec-string + dataset-fact | `grep -E 'min\(n_pts_cap, n_snapshots' ctl...` + `data06_snapshots.py` | ❌ Wave 0 (AC pass-criteria authored by Phase 27) |
| PIPE-07 | float64 sufficiency + Decimal-classifier + staleness | spec-string + dataset-fact | `grep -i 'float64\|decimal.Decimal\|stale' ctl...` + `data05_mass_drift.py` | ❌ Wave 0 |
| PIPE-08 | stage-query signatures + metadata + doc-03 ref | spec-string | `grep 'sample_replay(n, max_stage)\|sample_lookahead(n, stage)' ctl...` | ❌ Wave 0 |
| PIPE-09 | raw-mass D canonical, 6.694/M_tot_ref rejected by name, E_scale 1e-8 | spec-string + dimensional check | `grep '6.694\|M_tot_ref\|1e-8' §2.5` | ❌ Wave 0 |

### Sampling Rate (adequacy — no false pass)
- **Per task commit:** the finding's own AC grep block (positive: verdict present; negative-control: rejected form appears ONLY in rejection context).
- **Per wave merge:** the finding's AC + any shared-section regression AC (AC-PIPE-01 for B-06 overlap; AC-PIPE-06 for D7 overlap).
- **Phase gate:** all four AC + regression AC green; all touched ledger rows at `VERIFIED`/`DEFERRED`; same-commit discipline confirmed; Phase 29 re-runs the full suite.
- **Adequacy argument:** the validation dimensions per contract are (1) verdict-present, (2) rejected-form-absent-as-operative (negative control), (3) evidence-packet/fact citation present, (4) ledger transition recorded. A spec edit that lands text but cites the wrong/missing verdict fails dimension (3); an edit that re-introduces a rejected form fails dimension (2). Sampling all four dimensions per contract prevents the false-pass where text is edited but the verdict is wrong or uncited.

### Wave 0 Gaps
- [ ] Author runnable pass-criteria (grep blocks / disposable scripts) for AC-PIPE-04/07/08/09 — the seeded IDs exist; the runnable criteria are Phase 27's to define (evidence/README.md:113).
- [ ] Confirm the Phase 24 probes (`data05_mass_drift.py`, `data06_snapshots.py`) still run against current dataset state.
- *(No test-framework install needed — grep + existing `.venv` python probes.)*

## Candidate STOP Gaps (for orchestrator review)

> Subagent does NOT write to gap registers. These are returned for the orchestrator to decide whether to log in `27-GAPS.md` + `.planning/milestones/v1.5-GAPS.md` and surface to the user.

### G-27-01 (process-schema) — PIPE-07 evidence-packet requirement is ambiguous
- **Decision point:** Does Phase 27 PIPE-07 (the mass-drift + footer-precision facet) require a NEW `evidence/{id}.md` packet authored under `_TEMPLATE.md`, or do the existing Phase 24 artifacts (`24-DATA05-RERUN-REMEDIATION.md` + `24-DATA05-RERUN-VALIDATION.md`) plus the ledger rows satisfy the packet-before-edit rule?
- **Where it surfaced:** `evidence/README.md:99` (EVID-06: "No spec edit ... without a completed evidence packet + verdict ... Each owning spec-edit phase authors its non-conflict packets immediately before its edits") vs the EVID-10 trigger table (README:73-78, which lists only SCS/D=6.694/M11-M12) vs the ID→Filename map (README:119-129, which has NO PIPE-07/mass-drift/footer entry) vs CONTEXT D-05 ("DATA-05 precision consumes the Phase 24 rerun remediation/validation artifacts and ledger notes").
- **Classification:** process-schema (packet existence/structure for a non-conflict finding).
- **Source silence:** D-05 says PIPE-07 "consumes the Phase 24 ... artifacts" — which reads as *no new packet* — but EVID-06's "authors its non-conflict packets immediately before its edits" reads as *yes, a new packet*. Neither the README nor CONTEXT states which governs when a non-conflict finding's verdict already lives in a Phase 24 artifact rather than an `evidence/` packet. The ID→Filename map's omission is consistent with "no packet" but is not stated as authoritative for this case.
- **Engineering grounding:** an evidence packet is the auditable unit that pins a verdict to its four EVID-06 sources before a spec edit; its purpose is to prevent ungrounded edits. PIPE-07's verdict IS already grounded and re-derivable (70/70 validation, the canonical-ICs ruling, float64 error budget in resolution-doc §4.3). The two candidate dispositions differ in audit-trail location, not in verdict: (A) author `evidence/mass-drift.md` (or similar) duplicating the Phase 24 grounding into the packet schema → uniform packet trail, some duplication; (B) cite the Phase 24 artifacts directly from the ledger row → less duplication, but breaks the "one packet per edited finding" uniformity and leaves the ID→Filename map incomplete. The choice sets a precedent for every future non-conflict spec-edit finding whose verdict predates the packet system.
- **Tempted to:** disposition (B) (cite Phase 24 artifacts, no new packet), because CONTEXT D-05/D-08 lean that way and the ID→Filename map omits PIPE-07. But this is a process-schema call the protocol does not unambiguously make, and D-06 explicitly says "If a required process artifact or packet mapping is missing or ambiguous, that is a process-schema STOP gap, not a license to invent a new schema."
- **What the user needs to decide:** For PIPE-07 (and by extension any non-EVID-10 finding whose verdict lives in a Phase 24 artifact): **(A)** author a new `evidence/{name}.md` packet under `_TEMPLATE.md` (specify the filename/ID→map entry), or **(B)** cite the Phase 24 remediation/validation artifacts directly from the ledger row with no new packet, or **(C)** some hybrid (e.g., a thin packet that points at the Phase 24 artifacts). Same question applies to whether the footer-row PIPE-07 facet needs anything beyond the already-VERIFIED D7 packet.
- **Confidence of impact:** MEDIUM — it does not change any verdict or spec text, but it determines the Phase 27 plan's task structure and the phase-exit audit trail, and sets a reusable precedent.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The `sample_replay`/`sample_lookahead` *semantics* (sample n trajectories from cumulative D_≤k / next-stage D_{k+1}) are adequately grounded by issue-03:683-684 + REQUIREMENTS PIPE-08 for the planner to transcribe the data-side interface without inventing return types/ordering/seeding. | Exact Edit-Site Map (PIPE-08) | If the planner needs return-type/ordering/seeding detail the sources don't give, that becomes a NEW candidate gap (do not invent). Flagged inline as the PIPE-08 provenance caveat. |

**Note:** A1 is the only standing assumption. All four verdicts, all edit sites, all ledger transitions, and the dataset facts are VERIFIED/CITED, not assumed.

## Open Questions

1. **PIPE-07 packet requirement** — captured as Candidate STOP Gap G-27-01. Recommendation: orchestrator surfaces to user before planning closes.
2. **PIPE-08 interface depth** — captured as Assumption A1. Recommendation: planner transcribes the data-side signatures + semantics at the grounded level; if it finds itself needing to specify return types / seeding / ordering not present in the sources, stop and raise a new gap rather than invent.

## Environment Availability

> Spec-text + ledger edits with re-derivable dataset probes. The only external dependency is the existing `.venv` python for the Phase 24 probes.

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| `.venv/bin/python` + Phase 24 probes | AC dataset cross-checks (`data05_mass_drift.py`, `data06_snapshots.py`) | assumed ✓ (used through Phase 26) | — | grep-only spec assertions still validate the spec text; dataset cross-check is corroborating, not blocking |
| `scripts/agent-commit` + `.githooks` | commit governance | ✓ (used Phases 24-26) | — | — |
| `grep` / `grep -E` | all four AC spec-string assertions | ✓ | — | — |

**Missing dependencies with no fallback:** none. **With fallback:** dataset probes (grep-only assertions suffice for spec-text correctness).

## State of the Art

| Old | Current | When changed | Impact |
|-----|---------|--------------|--------|
| M12 candidate `min(32, int(0.5 * n_snapshots))` | `min(n_pts_cap, n_snapshots)`, no 0.5 | Phase 25 (`e05b4b1a`) | ROADMAP:228 is stale; M12 verdict governs. |
| `D=6.694` / `M_tot_ref` proposal (issue doc) | raw-mass `D≈4.6416` (PHYS-01/HC-6) | Phase 20 lock; ratified Phase 25 | 6.694 rejected by name as a pipeline instruction. |
| §2.5 `E_scale = +1e-10` (outlier) | `+1e-8` (2-of-3 majority) | Phase 27 edit decision (pre-reasoned in compute-globals-D.md:106) | One-line value change; not a re-adjudication. |
| DATA-05 "Decimal-for-masses" framing (issue doc) | float64 canonical; 70 stale artifacts rerun; Decimal=classifier only | Phase 24 GAP-24-01 RESOLVED + 70/70 validated | precision is sufficient; staleness was the real issue. |

**Deprecated/outdated:** ROADMAP:228 0.5-factor candidate (superseded, do not flag); §2.5 `+1e-10` `E_scale` floor (to be canonicalized to `+1e-8`).

## Sources

### Primary (HIGH confidence — LOCKED)
- `evidence/m11-m12-severity.md` (M12 `accept-third-position`; spec-ready prose :105-113) — PIPE-04/G5
- `evidence/compute-globals-D.md` (PIPE-09 `accept-resolution`; spec-ready prose :104-108) — PIPE-09
- `24-ISSUE-LEDGER.md` (rows M12:26, G5:33, footer:40, mass-drift:41, D=6.694:39; lifecycle) — all
- `24-VERIFIED-FACTS.md` (CLM-10 medians 61/127/1003:25; DATA-05 row:35) — PIPE-04/PIPE-07
- `24-DATA05-RERUN-VALIDATION.md` (70/70 PASS:1-6) + `24-DATA05-RERUN-REMEDIATION.md` (:16-18,110-112) — PIPE-07
- `evidence/README.md` (EVID-10 table, lifecycle, packet protocol, ID→map, AC discipline) — process
- `ctl_instruction.md` (edit sites: 493-500, 560-576, 744-774, 791-824, 1417-1423) — primary target
- `pinn_architecture.md` (edit sites: 329-351 §3.1, 761 §5.2) — secondary target
- `27-SPEC.md` + `27-CONTEXT.md` (locked requirements, D-01..D-14) — phase contract

### Secondary (MEDIUM — candidate/descriptive, cite-only)
- `02-resolution-doc.md` §4.1 (408-418), §4.3 (467-489), §4.4 (493+) — candidate verdict source, spec-ready prose
- `pinn_instruction/issues/03-curriculum-and-training-loop.md:683-684` — `sample_replay`/`sample_lookahead` semantics (descriptive)
- `REQUIREMENTS.md` PIPE-04/07/08/09, SCOPE-06..10 — requirement text + freeze rules

### Tertiary (LOW — non-authoritative)
- `pinn_instruction/issues/02-data-pipeline-and-validation.md` — source-position/rejected-claim citations only

## Metadata

**Confidence breakdown:**
- Edit-site map: HIGH — located by direct grep against current spec text; three of four contracts edit existing text.
- Locked verdicts: HIGH — verbatim from Phase 25 packets / Phase 24 validated artifacts.
- Evidence-packet mapping: HIGH for M12/G5/PIPE-09; MEDIUM (ambiguous → G-27-01) for PIPE-07.
- AC design: HIGH — mechanical grep + dataset-fact assertions over edited spec.
- PIPE-08 interface depth: MEDIUM — names locked, semantics grounded, deeper detail flagged (A1).

**Research date:** 2026-06-13
**Valid until:** until the next edit to `ctl_instruction.md` / `pinn_architecture.md` / `24-ISSUE-LEDGER.md` (line numbers will shift). Re-grep edit sites if those files change before planning.
