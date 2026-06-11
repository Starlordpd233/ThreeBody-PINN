# Issue-02 Resolution Document — Data Pipeline and Validation

**Date:** 2026-06-11
**Prepared by:** External research analyst (independent; repo-blind, package-only)
**Inputs received:** 6 of 7 manifest files — `RESEARCH-CONTEXT-MASTER.md`, `specs/02-data-pipeline-and-validation.md` (issue doc, non-authoritative), `specs/ctl_instruction.md`, `specs/pinn_architecture.md`, `specs/data_quality_assessment.md` (read-only research report), `specs/sampling_method.md` (FROZEN). **`DELIVERY-NOTE.md` was listed in the manifest but not delivered** (see §0.4 and Open Item OI-1). No Phase-24 `DATA-07` correction addendum accompanied the package; every CLM row retains its shipped status.

---

## 0. Scope and Decision Standard

### 0.1 What this document is

This document answers every question in the "Framed Research Questions" section of `RESEARCH-CONTEXT-MASTER.md` (master lines 97–497): Q-A1..Q-A6 (Cluster A, Ingestion & Selection), Q-B1..Q-B4 (Cluster B, Sampling, Precision & Global Scale), and Q-C1..Q-C4 (Cluster C, Validation Metrics). It is a candidate verdict source for the downstream Phase 25–28 adjudication; it decides nothing by itself. Each resolution is written so a skeptical reviewer can check it against the package snapshots, and so the spec author can transcribe the verdict without re-deriving it.

### 0.2 Decision standard

Verdicts are graded against the following authority order, applied strictly:

1. **Hard Constraints HC-1..HC-6** (master lines 148–219) are fixed inputs. No verdict re-opens them; several verdicts are *entailed* by them and are labeled as such.
2. **Framework specs** (`ctl_instruction.md`, `pinn_architecture.md`) are the source of truth and the only spec-edit targets. Where they are internally inconsistent, the inconsistency is reported (§6) and a repair is proposed (§7) rather than silently resolved.
3. **Verified CLM rows** (CLM-04..CLM-09 plus the erratum-corrected facts) are usable dataset facts. **Claimed-unverified rows** (CLM-01, CLM-02, CLM-03, CLM-10, CLM-11 prevalence, CLM-12, CLM-13) are never load-bearing: any verdict that touches one is written to be *robust to the figure being wrong*, and the dependency is named in the Confidence element.
4. **The issue doc** is the adjudication subject. Its findings and Recommended Resolutions (P1-1..P2-2) are evaluated, not transcribed. Where a recommendation is rejected, the rejection is shown from package evidence.
5. **`data_quality_assessment.md`** is non-authoritative *except* that it is the sole written home of the locked post-v1.3 SCS gate (HC-5, SI-DQA-003) and the only in-package definitions of SASD/IPR/PSC; it is cited accordingly, always with that annotation.
6. **`sampling_method.md`** is FROZEN history; it grounds generation-time facts (prescreen thresholds, mass normalization) and is never treated as a revision target.
7. Live `pinn/` code is excluded (SCOPE-10) and is cited nowhere as evidence.

### 0.3 Scope boundary compliance

The doc-03 exclusions are respected throughout: M16 (`dt_out` collocation-density scaling), G6 (causal-training Option A/B), and the training-loop usage of SCS/SASD/IPR/PSC are **not answered**. Where a question has a data-side facet adjacent to a deferred facet (Q-B1, Q-C2, Q-C3, Q-C4), the boundary is restated inside the resolution and the deferred facet is marked as a forward-reference only.

### 0.4 Input gap

`DELIVERY-NOTE.md` (handoff and gate context, D-16) was not among the uploaded files. Its absence does not block any Q-resolution — the master is self-contained for the questions — but the Phase 25–29 gate conditions and the DATA-07 addendum announcement are known here only through the master's summary of them. Recorded as Open Item OI-1 (Additional Input Needed).

### 0.5 Conventions used in this document

Each question receives five labeled elements: **Verdict**, **Reasoning**, **Evidence** (file + section/line citations into the package snapshots), **Confidence** (High/Medium/Low plus the single factor most likely to change the verdict), and **Verification suggestion**. Proposed spec text is consolidated in §7 (SPEC-1..SPEC-9), each block anchored to its target file and section; per-question resolutions point to their SPEC blocks. Line numbers refer to the uploaded snapshots (the byte-for-byte copies pinned at package commit `96f9150a…`). "Raw units" means the G=1 simulation units of the Brutus text files before the Step-2 (D, T) scaling; "scaled units" means after it. The two `ε_H` symbols are kept disjoint per the master's note (lines 205–219): in this document `ε_H` always means the validation raw-drift quantity of HC-5 unless explicitly stated otherwise.

---

## 1. Executive Decision Summary

The fourteen questions split into three groups by how much genuine uncertainty remains after adjudication.

**Group 1 — settled by the package (ten questions).** Q-A1, Q-A2, Q-A3, Q-A5, Q-A6, Q-B1, Q-B2, Q-B3, Q-B4, and Q-C1 are answerable with High confidence from the locked constraints, the framework specs, and the verified CLM rows. The headline results: a trajectory **admission gate** belongs at DataLoader initialization and its conditions are derivable from the package — but the issue doc's `snapshot_count >= 200` floor is arithmetically impossible for the standard-base population it would govern and must be rejected (Q-A1). The ID→path contract is scan-based, keyed `(variant folder, zero-padded numeric ID)`, with explicit misses; non-contiguity is *provable from verified rows alone* (the verified 184-ID list contains ID 3958 while the verified standard folder count is 2,749), so the contract does not depend on the unverified gap magnitudes (Q-A2). Blacklist consumption is a blocking-grade loader precondition with a precise load/validate/exclude/log/assert contract; whether current code violates it remains Phase-24's empirical question (Q-A3). The footer contract follows from the erratum-corrected facts: footers are all-or-nothing, folder defaults are verified (CLM-09), and the issue doc's "minimal footer"/"schema varies" premises are contradicted (Q-A5). HDF5 is the recommended primary store with `.npy` spec-compliant and JSON inspection-only; the one methodology consequence is mandatory float64 round-tripping (Q-A6). The 32-points-per-trajectory batch spec is **feasible**; M12's BLOCKING "infeasibility" claim is wrong, and the durable fix is a `min(cap, n_snapshots)` guard with without-replacement sampling (Q-B1). The mass-consistency check should cover **all** IC–Brutus pairs (dissolving the WR-01 sample-size conflict), use an explicit absolute float64 gate at 1e-15 consistent with the existing `ctl` §2.1 gate, and escalate to `decimal.Decimal` only on failure (Q-B2). float64 is sufficient for every data-side validation metric, with an error budget ≥8 orders below the gates (Q-B3). The pipeline must use the locked raw-mass `D ≈ 4.6416`; the issue doc's `D = 6.694` code is both constraint-violating and internally inconsistent, and the cost of the mass-fraction alternative is documented as a future-only rewrite (Q-B4). The SCS definition and reject gate are the locked HC-5 forms; the issue doc's ratio thresholds are a nomenclature collision plus an unsourced tightening and must not be transcribed (Q-C1).

**Group 2 — answerable with explicit provisional parameters (three questions).** Q-C2 (SASD), Q-C3 (IPR), and Q-C4 (PSC) receive complete, implementable data-side definitions, but the package under-determines specific choices (per-body vs system norms, collocation placement, units, grid geometry, thresholds). Those choices are made here, labeled as judgment, and every numeric threshold (SASD 0.5, IPR 1e-3 in raw units, PSC grid `[1e-3, 1e2]` × 25 bins/axis) is marked provisional pending Phase-24 distributions. The one constraint-entailed element is firm: the data-side IPR uses the validation softening `ε = 1e-10` (HC-4); the issue doc's `ε = 1e-5` belongs to the deferred doc-03 noise-floor role and the two are not numerically comparable.

**Group 3 — one structured STOP-gap candidate (one question).** Q-A4 (the 184 standard IDs without gold counterparts) is the only question where the honest answer is conditional. Under the locked stage definitions, *no fallback exists to choose*: Stage 5's data source is Set 2b (gold) only, a gold-less ID simply contributes no Stage-5 sample, and its base sample already persists into late-stage training via curriculum replay. Both issue-doc options presuppose a per-ID Stage-5 obligation the spec does not create. That reading is stated with its mechanics, and the genuinely open residue — whether the project *wants* Stage-5 coverage for those ICs, which is a gold re-simulation/resourcing decision — is flagged for the user gate, with the STOP-gap trigger condition spelled out (if downstream adjudication rules that stage labels attach to IDs rather than simulations, the no-fallback reading fails and Q-A4 becomes the Phase-26 STOP gap as annotated).

**Cross-cutting.** Adjudication surfaced seven findings beyond the posed questions (§6), the two most consequential being a transposed file-count pair in `ctl_instruction.md`'s `tab:brutus_compare` (contradicting verified CLM-05) and a three-way `E_scale` floor conflict inside the editable specs (`1e-10` vs `1e-8`). Nine proposed spec-text blocks (§7) repair these and give every accepted contract an authoritative home in the editable specs — including transcribing the locked SCS gate out of its single read-only home, which implements HC-5 rather than reopening it.

---

## 2. Decision Matrix

| Question | One-line verdict | Confidence |
|---|---|---|
| Q-A1 | Yes — admission gate at DataLoader init: `final_timestep >= 9.5` + structural parse floor (`>= 2` snapshots, finite, monotone) + locked SCS reject gate + blacklist + Step-2 gates + warn-level grid checks; **reject** the issue doc's `>= 200` Stage-4+ floor (arithmetically excludes the entire standard-base population) | High |
| Q-A2 | Identity is `(variant folder, zero-padded numeric ID)`; scan-built `id_to_path` per folder, collision-checked, explicit miss, never positional; non-contiguity is proven from verified rows alone (CLM-04 list contains 3958 > CLM-05 count 2,749), so the contract is unconditional and CLM-01/CLM-02 only size the blast radius | High |
| Q-A3 | Blacklist load at init is a blocking-grade contract: schema-validate `{hierarchical, standard}` → int lists, normalize int↔`%04d`, exclude `(variant, ID)` from base **and** gold, fail hard if file missing, log counts, assert at batch time, exclude **before** stage assignment and global statistics; current consumption status stays a Phase-24 (DATA-02) question | High (contract) |
| Q-A4 | No fallback exists under the locked stage definitions: a gold-less standard ID has no Stage-5 sample; its base sample persists via replay; both issue-doc options are rejected as posed; the open residue (commission gold re-simulation for any of the 184?) is a user-gate resourcing decision; STOP-gap trigger stated | Medium |
| Q-A5 | Footer present → parse full schema (provenance `direct`); absent → CLM-09 folder defaults (provenance `inferred`), `eta = null` (provenance `absent`); partial → anomaly flag + defaults; generalize `tol_confidence` to a per-parameter `param_provenance` dict with a `measured` channel for `dt_out`; footers never used for completeness or mapping | High |
| Q-A6 | HDF5 primary (groups `/{variant}/{id}`, float64 datasets, metadata/provenance attrs, `schema_version`); `.npy` spec-compliant but awkward; optional JSON export inspection-only, never a training input; methodology consequence: bitwise float64 round-trip + full transform metadata for auditability | High |
| Q-B1 | Feasible — M12's BLOCKING claim is wrong; contract `n_pts = min(n_pts_cap, n_snapshots)` sampled **without replacement** (cap default 32 = the spec's example value, flagged non-evidence-based); 50/50 split as weighted-then-uniform draws without replacement; loader exposes `n_snapshots`, `dt_out` (M16 consumption deferred) | High (form) |
| Q-B2 | Check **all** IC–Brutus pairs (WR-01 dissolves): gate `max_i |m_IC,i − m_Brutus,i(t=0)| < 1e-15` absolute float64, consistent with `ctl` §2.1; never rely on `np.allclose` defaults (`atol=1e-8` masks failures); escalate to `decimal.Decimal` re-compare only on gate failure; passing gate ⇒ IC masses canonical for IC₁₃ | High |
| Q-B3 | float64 sufficient for all data-side validation metrics: metric noise ~1e-15..1e-13, ≥8 orders below the 1e-5 gate and at/below the data's own tolerance (CLM-09); `|H(0)|→0` handled by the dqa undefined-SCS rule; `decimal.Decimal` required only as the Q-B2 escalation diagnostic; HC-4 governs softening, not arithmetic precision | High |
| Q-B4 | Pipeline must use locked raw-mass `D = (G·T²)^{1/3} ≈ 4.6416` (HC-6); issue-doc P1-7 code violates HC-6, mixes conventions internally (mass-fraction `D` with raw-mass energies), and uses the PHYS-03 additive-ε anti-pattern; mass-fraction adoption cost documented as future-only; side fix: canonicalize `E_scale` floor at `1e-8` | High (constraint-entailed) |
| Q-C1 | Definition + gate are the locked HC-5 forms (`ε_H` raw drift, `SCS = log₁₀ ε_H`, reject `SCS > −5`; boundary non-strict); issue doc's "SCS" is the raw ratio (nomenclature collision); its 1e-6 promotes the Acceptable/Marginal boundary to a reject gate, its 1e-8 is unsourced; do not transcribe; record SCS value + dqa band as metadata; stage-conditional tightening deferred to post-Phase-24 distributions; transcribe the gate into editable `ctl` (implements, does not reopen, HC-5) | High |
| Q-C2 | `SASD_i = Δt_i · max_{body,endpoint} (‖a‖ / max(‖v‖, 1e-12))` with **analytic** Plummer-`ε=1e-10` accelerations; trajectory score `max_i`; dimensionless and scale-invariant; **flag** (not reject) at `max SASD > 0.5` (provisional); flagged ∧ gold exists → satisfied by gold; flagged ∧ gold-missing → genuine resample queue (cross-ref Q-A4) | Medium |
| Q-C3 | `CubicHermiteSpline(t, q, dydx=v)` per component (the dqa's "PCHIP" is a misnomer); 10 deterministic interior points/interval; `IPR = (1/M)Σ‖q̈_spline − a_grav‖²` with **ε = 1e-10** (HC-4 validation side); issue doc's `ε = 1e-5` is the deferred doc-03 noise-floor role — not comparable; units pinned to raw G=1; gate `> 1e-3` provisional; store per-interval max residual | Medium |
| Q-C4 | Dataset-level Shannon entropy over admitted snapshots, per variant + pooled; 2-D grid on `(log₁₀ d_min, log₁₀ d_mid)` of sorted pair distances, range `[1e-3, 1e2]`, 25 bins/axis (K = 625), edge-clamped; plug-in estimator (Miller–Madow bias negligible at this N); report raw `H` and `Ĥ = H/ln K`; Stiffness Coverage Ratio `SCR = N(d_min < 0.5)/N` report-only; no reject gate | Medium |

The G1–G5 synthesis table (issue doc lines 96–105) requires no separate answers: G1 = Q-A1, G2 = Q-A2, G3 = Q-A3, G4 = Q-A4, G5's data-side facet = Q-B1 (its collocation-scaling facet, M16, is doc-03). G6 is doc-03 and is not answered.

---

## 3. Cluster A — Ingestion & Selection (Phase 26)

### 3.1 Q-A1 (B-06) — Stage 4 → Stage 5 validation gate

**Verdict.** Yes: a trajectory admission gate must run at DataLoader initialization, between Stage-4 metrics and any Stage-5 training use. It admits a trajectory record only if **all** of the following hold, evaluated per Brutus output file:

1. **Completeness:** `final_timestep >= 9.5`, computed as the maximum parsed block time (the README's primary check, using its stated header pattern `^(\d+\.?\d*)\s+3\s+\d+`). This is the CLM-11 *rule*, which is grounded; its prevalence is not assumed.
2. **Structural parse floor:** `snapshot_count >= 2`; all parsed values finite (no NaN/Inf); times strictly increasing. This is a parse-integrity condition (the spec already requires graceful handling of `< 2`-snapshot files), not a curriculum criterion.
3. **Locked SCS gate (HC-5):** reject if `ε_H > 1e-5` (equivalently `SCS > −5`), with `ε_H = max_t |(H(t) − H(0))/H(0)|`. The gate consumes the Stage-4 metrics output for the trajectory and recomputes `ε_H` per the HC-5 definition if the metrics record is absent or unparseable. `H(0)` numerically near zero → SCS undefined → quarantine for manual review (dqa rule), not silent pass or fail. (Full definition handling in Q-C1.)
4. **Blacklist exclusion** per the Q-A3 contract.
5. **Step-2 preprocessing gates as already specified:** mass-invariance (`ctl` §2.1), COM/momentum assertions (`ctl` §2.6) remain reject/quarantine conditions; the admission gate is their enforcement point for training use.
6. **Warn-level consistency checks (flag, do not reject, pending DATA-06):** grid regularity `max_i Δt_i <= 1.5 × dt_out(variant)`, and expected-count cross-check `snapshot_count >= 0.9 × (final_timestep / dt_out + 1)`. These catch interior truncation that `final_timestep` alone cannot see.

Every rejection/quarantine is logged with `(variant, id, reason)`, and per-variant admit/reject counts are logged at init. Admission runs **before** stage assignment and **before** dataset-wide normalization statistics (cross-ref Q-A3, Q-B4). The issue doc's `TrajectoryValidator` *placement* is endorsed; its proposed thresholds are adjudicated as follows: `final_timestep >= 9.5` **accepted** (README-grounded); `snapshot_count >= 2` **accepted** as a structural floor for all stages (its stage-restriction to "Stage 0–3" is dropped); `snapshot_count >= 200` for Stage 4+ **rejected**. Proposed spec home: SPEC-1 (new `ctl_instruction.md` "Step 1A: Trajectory Admission Gate").

**Reasoning.** Three independent package facts establish that the gate is needed and must live at DataLoader init. First, `calculate_metrics.py` provenance states explicitly that the script performs no completeness checks and processes every file, delegating validity to downstream consumers — so Stage 4 cannot be the gate. Second, the README designates `final_timestep >= 9.5` as the primary completeness check and explicitly forbids the two tempting proxies (footer presence, line counts) — so the gate's main condition is already grounded, it just has no enforcement point in the editable specs. Third, the locked SCS gate (HC-5) is a *data screening* gate ratified for exactly this position (the dqa Phase-1 ingestion protocol runs it on load), and the dqa's causal-firewall analysis (§4.1) explains why admitting one bad trajectory is disproportionately harmful under causal training: a high-residual segment collapses the causal weights for all later times.

The `>= 200` floor is rejected on verified arithmetic, not on the unverified CLM-10 counts. CLM-09 (verified) fixes `dt_out = 0.17` for standard base and the completeness rule fixes `final_timestep >= 9.5`; a complete standard-base run on its output grid therefore has at most about `ceil(10.03/0.17) + 1 ≈ 60` snapshots and *needs* only `ceil(9.5/0.17) + 1 = 57` to pass completeness. A `>= 200` floor for "Stage 4+" would therefore reject **every** complete standard-base trajectory — the very population the locked stratification assigns to Stages 3–4 (Set 1b) — while the issue doc's own dataset table (its line 13) says standard base has ~59 snapshots. The same arithmetic gives ~120 for hierarchical base (`dt_out = 0.08`) and ~951 for gold (`dt_out = 0.01`): the only population that could pass `>= 200` is gold. The floor appears to be a gold-resolution number misapplied across stages. More fundamentally, stage-dependent snapshot floors conflate two different things: per-trajectory *validity* (a property of the file) and curriculum *membership* (a property of the stratification, already fully specified by the locked stage definitions). The admission gate should test validity only. The `>= 2` floor, by contrast, is harmless and useful as a parse-integrity check — though note it is nearly vacuous for training admission because condition 1 dominates it (a 2-snapshot file cannot reach `t = 9.5` on any documented grid).

The warn-level checks in condition 6 are added because `final_timestep` is blind to interior gaps: a file truncated in the middle but containing a final block would pass conditions 1–2. They are warn-level rather than reject because the README warns against hard-coding grid expectations (CLM-10 note: `t_end` may be 10.01/10.03; gold reruns exist); DATA-06 will show whether escalation to reject is safe.

**Evidence.** Issue-doc position and proposal: issue doc lines 57 (B-06 row), 283 (P1-1), 320–331 (pipeline checklist, "GAP" row), 340 (DataLoader req. 2). Master framing: lines 251–270 (Q-A1 block), CLM-10/CLM-11 rows (lines 599–600) and row notes (626–633). README completeness rule and prohibitions: master lines 798–816 (Completeness Checks fragment, regex at 803–809). `calculate_metrics.py` no-completeness provenance: master lines 878–905. CLM-09 verified defaults: master lines 781–786. Locked SCS gate: HC-5 (master lines 186–196); `data_quality_assessment.md` lines 120 (definition), 124–130 (bands), 233–234 (Phase-1 gate), 325–328 (SI-DQA-003) — annotated: locked post-v1.3; sole written home is a read-only research report. Parse floor and graceful `< 2`-snapshot handling: `ctl_instruction.md` Step 1 item 3 (lines 352–360). Step-2 gates: `ctl` §2.1 (397–413), §2.6 assertions (617–626). Causal-firewall rationale: `data_quality_assessment.md` §4.1 (lines ~194–200). Frozen generation-time QC intent (energy/momentum/completion checks after Brutus): `sampling_method.md` §6 (lines 266–272).

**Confidence.** High. The single factor most likely to change the verdict: **DATA-06** revealing materially irregular snapshot grids (non-uniform `dt`, mid-file gaps) at scale — that would promote the warn-level condition-6 checks to reject conditions and could require a variant-aware expected-count floor in place of the simple structural floor.

**Verification suggestion.** DATA-06: distribution of `final_timestep`, `snapshot_count`, and `max Δt / dt_out` per variant; confirm the per-variant complete-run count clusters near 57/120/951 (+ grid-end slack). Unit tests: a file truncated at `t = 5` is rejected (reason `completeness`); a 1-snapshot file is rejected (reason `structure`); a synthetic trajectory with injected `ε_H = 2e-5` is rejected (reason `scs_gate`); a file with an interior gap of `3 × dt_out` admits with a `grid_irregular` warning.

### 3.2 Q-A2 (B-11) — Non-contiguous IDs (ID ≠ array index)

**Verdict.** The trajectory identity is the pair `(variant_folder, numeric_id)`, where the numeric ID is the zero-padded 4-digit token in the filename and the folder is the sole authority for variant and gold status (per erratum Correction 1, filenames carry no `_gold_` infix). The mapping contract:

1. At DataLoader init, build `id_to_path[variant][id]` by **scanning each of the four Brutus output folders** and parsing filenames with `^brutus_(hierarchical|standard)_(\d{4})\.txt$` (anchored; non-matching files logged and ignored).
2. IDs are normalized to `int` internally and formatted `%04d` for path operations; a duplicate ID within one folder is a hard error at init.
3. Lookup of an absent `(variant, id)` raises an explicit miss; there is **no** positional fallback, no `paths[id]` array indexing, and no assumption that IDs are dense, contiguous, or start at any particular value.
4. Iteration for any deterministic purpose (stage assignment, statistics, exports) goes over **sorted present IDs**, never over `range(n_files)`.
5. The Step-5 stage map is keyed by `(variant, id)` (it is already specified as a mapping "from each simulation ID to its assigned stage index"); `Result:` footer paths are never used for mapping (issue-doc INFO row concurs: OS-dependent, multi-folder).

The issue doc's `id_to_path` / `TrajectoryIndex` proposal (P1-2) is **accepted in substance**; this verdict pins down the parts P1-2 leaves open (key structure, regex, collision and miss semantics, iteration order). Proposed spec home: SPEC-2.

**Reasoning.** The decisive point is that the contract is provable **without** the unverified gap claims. CLM-04 (verified) is an explicit list of 184 standard IDs whose maximum member is `3958`; CLM-05 (verified) counts the standard base folder at 2,749 files. Since `3958 > 2749`, the standard ID space *cannot* be `{0..2748}` densely: gaps exist with certainty, and any `ID == index` assumption mis-addresses at least some trajectories regardless of what DATA-01 finds. CLM-01/CLM-02 (claimed-unverified: 1,250/4,000 and 143/5,000 gaps) therefore do not carry the verdict; if confirmed they quantify the blast radius — roughly one in three standard lookups wrong under dense indexing — and if corrected the contract is unchanged. This is also the master's own dataset-context position: "The numeric ID is NOT an index; gaps exist," and gaps are *intentional* (generation continuation, prescreen rejection, failed runs), so no future re-densification should be expected or designed for. Scanning the filesystem (rather than trusting nominal counts, footers, or documentation lists) makes the index correct by construction against whatever is actually on disk — which is also why the CLM-04 list itself is used only as a cross-check in Q-A4, never as the source of truth.

**Evidence.** Issue-doc position: lines 58 (B-11 row), 284 (P1-2), 314–318 (anomalies: gaps intentional, linear indexing wrong), 339 (DataLoader req. 1), 344 (req. 6: match by numeric ID; folder defines variant), 83 (INFO: footer paths not authoritative). Master: Q-A2 block (lines 272–285), CLM-01/02/04/05/12 rows (590–594, 601), file-naming fragment incl. Correction-1 integration (lines ~695–719: folder-only gold encoding; same filename in base and gold folders), CLM-04 ID list (lines 843–862; max entry 3958). Framework spec: `ctl` Step 5 (lines 1061–1068: mapping from simulation ID to stage index) — the spec already speaks in ID terms; it is silent only on the *mechanism*, which this contract supplies.

**Confidence.** High. The contract is unconditional; no plausible Phase-24 result weakens it. The single factor that would *modify* (not overturn) it: DATA-01 revealing IDs that violate the 4-digit zero-padded pattern (e.g., 5-digit IDs), which would widen the regex but change nothing else.

**Verification suggestion.** DATA-01 (actual vs nominal counts per folder; gap lists). Property test: `max(parsed IDs) >= file_count` holds in the standard base folder (it must, given CLM-04/05). Unit test: lookups for 10 randomly chosen IDs from the CLM-04 list against the **gold** folder raise explicit misses; the same IDs against the **base** folder resolve to existing files.

### 3.3 Q-A3 (M11) — Blacklist loading / consumption

**Verdict.** The required contract, stated as a blocking-grade precondition for any training run:

1. **Load** `problematic_ics_blacklist.json` at DataLoader init, before stage assignment and before any dataset-wide statistic is computed.
2. **Validate schema:** a top-level JSON object with exactly the keys `hierarchical` and `standard`, each mapping to a list of integers. Anything else is a hard configuration error.
3. **Normalize** entries to `int` internally; format `%04d` only at path boundaries (consistent with the Q-A2 identity).
4. **Exclusion semantics:** the blacklist is IC-level (`problematic_ics`). An entry `(variant, id)` excludes that ID from **both** the base and the gold folder of that variant — the gold ICs are a byte-identical subset of the base ICs (verified dataset-context fact), so a problematic IC is problematic at every fidelity.
5. **Missing or unparseable file = hard failure** at init. A loader that silently proceeds without the blacklist cannot guarantee the exclusion property; absence is a configuration error, not an empty blacklist.
6. **Logging:** per variant, `n_blacklist_entries`, `n_present_on_disk` (blacklisted IDs that actually exist in each folder), `n_excluded`. A blacklisted ID absent from disk is acceptable and logged, not an error.
7. **Defense in depth:** a cheap set-membership assertion at batch assembly time that no emitted sample is blacklisted; violation fails loudly (it indicates a bypass path, which is exactly the M11 failure mode).
8. **Ordering:** exclusion happens **before** stage assignment and **before** `compute_globals`-style statistics (cross-ref Q-B4: admitted-set statistics), so blacklisted trajectories cannot influence normalizers even indirectly.

The issue doc's P1-3 is **accepted and strengthened** (P1-3 already contains load-at-init, log count, fail-loudly-in-batch; this verdict adds schema validation, normalization, base+gold semantics, missing-file behavior, and ordering). Two scoping notes: (a) the *consumption status* of the blacklist in current code is not decidable from this package — live `pinn/` code is excluded (SCOPE-10) — and is exactly Phase-24's DATA-02 probe; (b) whether M11's MAJOR→BLOCKING reclassification stands is EVID-10's call; what this document asserts is that the **contract** is blocking-grade: a loader that can silently admit known-bad ICs corrupts training data at ingestion and the prevention is trivial. Proposed spec home: SPEC-1 (admission-gate clause).

**Reasoning.** The spec is silent on blacklist consumption (master, Q-A3 framework position), so the contract is constructed from the artifact's own structure and the pipeline's invariants. The dataset context fixes the JSON shape (`hierarchical`: 2 IDs `123, 253`; `standard`: 63 IDs beginning `21, 30, 52`), which yields the schema-validation clause and the int↔`%04d` normalization need (JSON integers vs zero-padded filenames). The base+gold semantics follow from the verified byte-identical-subset relationship between gold and base ICs: excluding only the base file would leave the same problematic dynamics in training via the gold copy. The fail-hard-on-missing rule follows from the exclusion property being a guarantee, not a best effort. The ordering rule follows from the dqa's sanitization rationale: statistics computed over a contaminated set bake the contamination into every normalized quantity downstream. On counts: CLM-03's `65 = 2 + 63` is claimed-unverified by design (Phase 23 ran no probes), so the contract is written count-free — it loads whatever the file contains and validates *shape*, not cardinality. Correspondingly, the issue doc's verification-checklist item "Blacklist load produces exactly 65 excluded IDs" must be re-keyed: assert against the parsed file content of the run, not a hard-coded 65.

**Evidence.** Issue-doc position: lines 59 (M11 row, reclassification note), 76 (reclassification ledger), 285 (P1-3), 297 (checklist hard-codes 65), 341 (DataLoader req. 3). Master: Q-A3 block (lines 287–302), CLM-03 row + note (lines 592, 606–611: count observable; consumption status is the M11 finding and is Phase-24-owned), blacklist summary fragment (lines 864–875: JSON shape, key composition), gold-IC byte-identical subset (lines ~830–835 in the CLM-04/05 source fragment). Statistics-ordering rationale: dqa Phase-1 protocol structure (lines 225–252: gate first, then analysis) and Q-B4's admitted-set recommendation in this document.

**Confidence.** High on the contract. The single factor most likely to change it: **DATA-02** finding the JSON's real schema differs from the documented two-key shape (extra keys, string IDs, nesting) — that would adjust clause 2's validation, nothing else. The empirical M11 claim (currently not loaded) is neither affirmed nor denied here; it is unverifiable from the package by construction.

**Verification suggestion.** DATA-02: verify count/composition against the JSON and probe consumption in the live loader (does a blacklisted ID appear in any emitted batch?). Unit tests: loader init fails when the file is absent; fails on a schema mutation (e.g., a third key); a blacklisted ID present on disk never appears across an exhaustive iteration of all stages; the batch-time assertion trips when the exclusion step is deliberately disabled.

### 3.4 Q-A4 (M13) — 184 standard IDs without a gold counterpart (fallback policy)

**Verdict.** Per the question's annotation, no fallback is asserted here. The finding is that **under the locked stage definitions there is no fallback to choose**: the spec's semantics already determine the behavior, and both issue-doc options presuppose an obligation the spec does not create.

- **What the locked text entails.** Stage 5's data source is Set 2b (gold standard) with criteria "Same as Stage 4"; stage labels are assigned per *simulation* ("a mapping from each simulation ID to its assigned stage index", with each Brutus output being a simulation); and each stage's training set includes all prior-stage data (curriculum replay). A standard ID with no gold counterpart has exactly one simulation — its Set-1b base run — which receives its Stage-3/4 (or 6) label from its own invariants and **persists into the Stage-5 and Stage-6 training sets via replay**. There is simply no Set-2b sample to label for that ID; "no Stage-5 sample" is the spec applied, not a policy gap.
- **Option 2 (flagged low-fidelity standard sample in Stage 5) is rejected as posed:** it contradicts Stage 5's data-source definition (Set 2b only) and double-counts — the base sample is already present in the Stage-5 training set through replay, so admitting it *again* as a Stage-5 member changes the stratum's composition for no informational gain.
- **Option 1 ("skip to Stage 6") is rejected as phrased but vacuous in substance:** nothing "skips" anywhere — the base simulation's own stage label is unchanged, and the ID's data reaches Stage-6 training through replay exactly as every other admitted sample does. Its operative content (no synthetic Stage-5 membership) is what the spec already entails.
- **Loader mechanics that implement the entailment:** (1) at init, compute the gold-missing set as the set difference of the scanned base and gold ID sets (Q-A2 index), and cross-check it against the verified CLM-04 184-ID list — log any discrepancy; never hard-code the list. (2) Attach per-trajectory metadata `gold_counterpart: present | absent`. (3) Build the Stage-5 stratum by iterating the **gold folder's actual files**, never by base-ID lookup into the gold folder (which would generate 184 spurious misses by construction).
- **The genuinely open residue — flagged for the user gate, not decided here:** whether the project *wants* Stage-5 (gold-resolution) coverage for any of those 184 ICs. That is a gold re-simulation and resourcing decision, outside loader policy. A principled selection criterion exists in this package's own terms: the intersection of the gold-missing set with the SASD resample queue (Q-C2) identifies exactly the gold-less trajectories whose base resolution is demonstrably insufficient.
- **STOP-gap trigger condition (Phase-26):** the entailment above rests on stage labels attaching to *simulations*. **If** downstream adjudication instead rules that labels attach to *IDs* and that every Stage-4 ID must yield a Stage-5 sample, the no-fallback reading fails, neither option is spec-derivable, and Q-A4 must be surfaced as the STOP gap exactly as the master annotates — rather than resolved by invention.

**Reasoning.** The question instructs "do not assert a fallback here," and the master flags Phase-26 STOP-gap status if sources are silent or conflicting. The sources are neither silent nor conflicting once read at the right granularity: the issue doc frames M13 as a hole ("Stage 5 training data is incomplete for these IDs") because it implicitly treats Stage 5 as an obligation per ID; the locked stratification defines Stage 5 extensionally by data source. Under the extensional reading, absence of a gold file is absence of a Stage-5 sample — the same way the 2 fewer hierarchical-gold parameter situations or any failed run shapes every other stratum. The double-counting argument against Option 2 is arithmetic: replay makes the Stage-5 *training set* = Stages 0–5 data; the base sample of a gold-less ID is in that set already. The mechanics clause 3 also closes a latent bug class flagged by Q-A2: any implementation that builds Stage 5 by iterating base IDs and looking them up in the gold index would turn a data fact into 184 runtime errors. One adjacent observation is recorded without being opened: Stage 5 applies the same τ_L criteria as Stage 4 to gold simulations, so some of the 2,565 gold files may themselves fail Stage-5 criteria and land elsewhere — stratum composition, not a Q-A4 matter. Confidence is Medium rather than High solely because the entailment has a stated defeater (the label-semantics conditional) that this package cannot itself close.

**Evidence.** Issue-doc position: lines 65 (M13 row, both options), 287 (P1-5), 299 (checklist: 184 missing), 316 (anomaly), 342 (DataLoader req. 4). Master: Q-A4 block with STOP-gap annotation (lines 304–321), CLM-04/CLM-05 rows (593–594), gold-gap source fragment incl. byte-identical-subset statement and the 184-ID list (lines ~826–862). Locked stage definitions: `ctl_instruction.md` Multi-Stage Data Stratification (section beginning line 105; Stage 4 at 204–227, Stage 5 at 229–235, Stage 6 at 237–245, replay at 247–249); Step 5 label semantics (lines 1061–1068). Hierarchical contrast (no gold gap: 4,857 = 4,857): master hierarchical-gold fragment (lines ~745–752).

**Confidence.** Medium. High that the no-fallback reading follows from the spec text as written; Medium overall because of the single named factor: a downstream **ruling that stage labels attach to IDs rather than simulations**, which would void the entailment and activate the STOP gap.

**Verification suggestion.** Obtain an explicit confirmation of Step-5 label semantics from the framework owner (one-line ruling closes the conditional). DATA-03: re-verify the 184-ID list against the gold folder by set difference. Unit test: Stage-5 stratum construction over a fixture containing a gold-less ID emits zero misses and the ID's base sample appears in the Stage-5 *training set* via replay exactly once.

### 3.5 Q-A5 (D7) — Footer / parameter heterogeneity

**Verdict.** The footer-handling contract, per Brutus output file:

1. **Footer present →** parse the full schema `(tol, Lw, dt_out, t_end, eta, energies)`; record each parameter with provenance `direct`. The corrected disk facts say presence implies the full schema, so a *partial* footer is not an expected state (clause 3).
2. **Footer absent** (the verified populations: 1,550 hierarchical-base, 701 standard-base, 219 standard-gold) **→** assign the verified CLM-09 folder defaults — standard base `tol=1e-13, dt_out=0.17, Lw=118`; hierarchical base `tol=1e-15, dt_out=0.08, Lw=130`; gold (both) `tol=1e-13, dt_out=0.01, Lw=130` — with provenance `inferred`. **`eta` has no folder default: store `null` with provenance `absent`.** Fabricating an `eta` is prohibited; nothing in the package supplies one for footerless files.
3. **Footer present but partial-schema →** treat as an **anomaly**: log `(variant, id, missing_fields)`, set `footer_anomalous = true`, fall back to defaults for the missing fields with provenance `inferred`, and surface the population to Phase 24 — under the corrected facts this state should be empty, so any member is new information.
4. **Provenance generalization:** replace the issue doc's single `tol_confidence` flag with a per-record `param_provenance` dict over `{tol, Lw, dt_out, eta}` with values `direct | inferred | absent | measured`. For `dt_out` specifically, additionally **measure** the median inter-snapshot spacing from the file's own timestamps, cross-check against the footer/default value, and warn on relative mismatch above 1% — the measured value is the one the trajectory actually exhibits and is more reliable than either documentation channel.
5. **Negative uses (unchanged from the README):** footers are never a completeness signal (Q-A1) and footer paths are never a mapping source (Q-A2).
6. **Destination:** these fields populate the per-record metadata that `ctl` §2.6 already *requires* (`brutus_tolerance, word_length, dt_out, trustworthy_horizon`) but for which no population mechanism is specified. (`trustworthy_horizon` itself is undefined anywhere in the package — Open Item OI-2; this contract does not invent a rule for it.)

The issue doc's P2-1 is **accepted in mechanism, corrected in premise, generalized in form**. Proposed spec home: SPEC-3 (amendment to `ctl` Step 1 item 3 plus a §2.6 provenance clause).

**Reasoning.** The verdict is mostly dictated by the erratum-corrected, verified facts, which overturn both factual premises of the issue doc's D7 framing: there are no "minimal footers" (the 219 standard-gold files have *no* footer and *no parameter fields anywhere*), and the footer schema does not "vary — some omit `eta`, `tol`, or both" (footers that exist carry the full schema, including `eta` and `tol`). What actually varies is *presence*, plus genuine within-folder heterogeneity among present footers (standard gold: 1,754 files at `tol=1e-13` vs CLM-08's verified 592 at `tol=1e-14`; hierarchical gold: five tuples across `tol ∈ {1e-13, 1e-14}` and `Lw ∈ {112..130}`). That heterogeneity is why clause 1 prefers per-file footer values over folder defaults whenever a footer exists, and why the provenance dict matters: a downstream consumer filtering on `tol=1e-14` must be able to distinguish "footer said so" from "default assumed." The `eta = null` rule follows from the corrected dataset context verbatim ("tol/Lw/dt are not parseable from these files; the folder-level defaults must be assumed" — defaults are enumerated for those three only) and from the erratum's removal of the unverifiable "different Brutus build omitted `eta`" story: with the provenance explanation withdrawn, there is no basis for any imputed `eta`. The `measured` channel for `dt_out` exists because `dt_out` is unique among the four fields in being independently observable from the data itself; the spec's own Step-1 item 4 already gestures at this ("dt_out: inferred from timestamps or defaults").

**Evidence.** Issue-doc position: lines 66 (D7 row), 68 (schema-variance claim), 196–207 (footer protocol notes), 291 (P2-1), 301 (checklist), 345 (DataLoader req. 7). Master: Q-A5 block (lines 323–342), CLM-07/08/09 rows + notes (596–598, 620–628), Correction 2 (lines 980–1007: corrected disk facts, full-schema-when-present, defaults-must-be-assumed, build-story removed), observed parameter-set tuples per folder (lines ~736–778: 3,307/1,550; 1,126+922/701; 1,754+592/219; hierarchical gold all-footer tuples), folder-default table (781–786). Framework spec: `ctl` Step 1 item 3 (352–360: optional `Result:` line, metadata extraction), item 4 (362–366: dt_out inferred from timestamps or defaults), §2.6 required metadata fields (lines 628–647, the four fields at 646).

**Confidence.** High. The single factor most likely to change it: **DATA-05's full footer scan finding genuine partial-schema footers** (a nonempty clause-3 population), which would reopen the schema-variance question and force a field-by-field fallback policy instead of the all-or-nothing model.

**Verification suggestion.** DATA-05: footer presence/schema scan over all 15,028 files; the presence counts must reproduce 3,307/1,550 (hier base), 2,048/701 (std base), 2,346/219 (std gold), 4,857/0 (hier gold), and the tuple histogram must match the dataset-context fragment. Unit tests: a footerless standard-base fixture yields `tol=1e-13 (inferred), Lw=118 (inferred), eta=null (absent), dt_out measured≈0.17`; a fixture with a footer missing `eta` only sets `footer_anomalous` and logs.

### 3.6 Q-A6 (D-03) — Processed training-data format

**Verdict.** The framework's requirement is an efficient binary store: `ctl` Step 1 item 6 names **HDF5 or `.npy`** — both are spec-compliant; `txt`/`json` as a primary store is outside the spec's recommendation. Within the compliant pair, this document recommends:

1. **HDF5 as the primary store.** Layout: one file (or one per variant), groups `/{variant}/{id}`; datasets `times`, `positions`, `velocities` (and the §2.6 derived arrays) stored as **float64**; per-group attributes carrying the full `ctl` §2.6 metadata record, the Q-A5 `param_provenance` dict, raw-file SHA-256 hashes, and a `schema_version` string; chunked + compressed (gzip or lzf); partial reads by group.
2. **`.npy` acceptable** (it satisfies the spec) but noted as awkward for this dataset: ragged per-trajectory arrays and rich metadata force either thousands of files or `.npz` plus a sidecar index, reinventing what HDF5 groups/attrs provide.
3. **Optional JSON export: inspection and debugging only, never a training input path.** The export is derived from the HDF5 store, clearly marked, and carries the same `schema_version`; no code path may train from it.
4. **Methodology consequences (this is not *purely* a storage decision):** (a) **float64 end-to-end** — the stored arrays are the inputs to every Q-B3 validation metric, so the store must round-trip the parsed float64 values bitwise; (b) **auditability** — store enough transform metadata (the §2.6 record: permutation, `R0`, `R_COM0`, `V_COM`, `D, T, V`, …) that the raw→processed map is re-derivable and checkable; (c) **determinism** — identical inputs produce byte-identical logical content (attribute ordering and compression aside).

This matches the issue doc's D-03 recommendation (HDF5 primary + optional JSON export), which is **endorsed** — with the addition of the precision/auditability clauses that make it spec-grade rather than a convenience choice. Proposed spec home: SPEC-4.

**Reasoning.** The framework-spec position is unusually direct here: Step 1 item 6 says to save parsed objects "into an efficient format like HDF5 or NumPy (.npy)" to avoid repeated text parsing — so the only adjudication needed is *within* the recommended pair plus the status of the JSON idea. HDF5 wins on fit, not fashion: the data model is literally `variant → id → ragged arrays + per-record metadata`, which is the HDF5 group/dataset/attribute model; the §2.6 metadata requirement and the Q-A5 provenance dict need attribute-like storage that `.npy` lacks; and stage-stratified access patterns benefit from partial reads. The issue doc's own pros/cons table reaches the same conclusion. The JSON guardrail (never a training input) exists because a second readable copy invites silent divergence; making it derived-and-marked keeps a single source of truth. The float64 clause is the bridge to Q-B3: every precision conclusion there assumes the metrics see the parsed values, not a down-cast copy — float32 storage would inject ~1e-7 relative noise, six orders worse than parse noise and within sight of the tightest data tolerances.

**Evidence.** Issue-doc position: lines 27–49 (D-03 decision block), 173–190 (format trade-offs), 262–277 (Open Decisions callout incl. recommendation). Master: Q-A6 block (lines 344–356). Framework spec: `ctl` Step 1 item 6 (lines 374–378); §2.6 required metadata record (628–647). Precision linkage: Q-B3 in this document; `ctl` numerical note "use double precision for all invariants" (lines 907–912).

**Confidence.** High. The single factor most likely to change it: an unstated **operational constraint** (e.g., a no-HDF5-dependency environment), which would flip the primary to `.npy + sidecar index` without touching clauses 3–4. No Phase-24 dataset result bears on this question.

**Verification suggestion.** Round-trip test: parse a sample of raw files → write store → read back → `np.array_equal` (bitwise) against the directly parsed float64 arrays, including times. Schema test: every group carries the full §2.6 attribute set + `param_provenance` + `schema_version`. Negative test: the training loader refuses a JSON path.

---

## 4. Cluster B — Sampling, Precision & Global Scale (Phase 27)

### 4.1 Q-B1 (M12) — Points-per-trajectory feasibility

**Verdict.** The feasible, durable contract for the per-trajectory data-loss sample count:

1. `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))`, with time points drawn from the trajectory's own snapshot set **without replacement**.
2. `n_pts_cap` defaults to **32** — explicitly the spec's *example* value (`ctl` writes "e.g., 32"; `pinn` uses `points_per_trajectory=32` as a code default), carried as a configuration knob and **flagged as non-evidence-based**, not as a lock.
3. The spec's 50/50 composition is implemented without replacement as: `k_w = floor(n_pts/2)` draws weighted by acceleration norm (weighted sampling without replacement, e.g. Gumbel-top-k), then `n_pts − k_w` uniform draws from the remaining snapshots; deterministic under a seed.
4. The loader exposes `n_snapshots` and `dt_out` per trajectory as metadata. (That is the data-side end of G5; how anything *scales with* `dt_out` — M16 — is doc-03 and is not answered.)

**Adjudication of M12:** the issue doc's BLOCKING claim — "standard trajectories (~59 snapshots) **cannot support** 32 points/trajectory (54% sampling ratio)" — is **wrong**. Drawing 32 distinct points from 59 without replacement is trivially possible; 54% is a *diversity* observation (batches over the same trajectory overlap heavily), not an infeasibility. Its proposed fix P1-4, `n_pts = min(32, int(0.5 · n_snapshots))`, is **rejected**: the 0.5 factor is unevidenced anywhere in the package, and the proposal is internally inconsistent with the issue doc's own verification checklist, which expects "gold with 1000 snapshots gets n_pts=128" — a value neither `min(32,·) = 32` nor `int(0.5·1000) = 500` produces, revealing an unstated third rule. The `min(cap, n)` guard is retained anyway because it is what makes the contract robust: the README warns against hard-coding snapshot counts (CLM-10 is claimed-unverified by design), and under the Q-A1 admission gate every admitted standard trajectory has ≥ 57 snapshots, so even a *fixed* 32 is feasible for the population in question — the guard simply makes the loader correct for any admitted file regardless of what DATA-06 finds. Proposed spec home: SPEC-5.

**Reasoning.** Two package facts anchor the analysis. First, the data-loss time points are drawn **from the discrete Brutus snapshots** — `pinn` §3.1 states it twice ("sampled from the BRUTUS trajectory snapshots", "sampled from the discrete BRUTUS trajectory snapshots") — so `n_snapshots` is the hard ceiling for distinct points and "without replacement" is the natural semantics (duplicated data points add no information to an MSE/Huber data term, only implicit re-weighting). Second, the count 32 is not locked: the `ctl` Mini-Batch section presents it parenthetically as an example, and the `pinn` listing carries it as a default parameter — and the spec's own SI-PINN-003 note flags the batch-construction text as inconsistent between the two documents, so treating 32 as immovable would over-read the weaker of two already-disagreeing passages. The feasibility arithmetic is then immediate: with verified `dt_out = 0.17` and the `>= 9.5` completeness gate, admitted standard trajectories carry 57–60 snapshots; `32 ≤ 57`. What *is* real in M12's vicinity is the diversity/concentration effect: with the weighted half drawn from a 59-point pool, the few highest-acceleration snapshots are selected near-deterministically every batch. That is a training-dynamics design question (arguably intended — the spec says the weighting "prioritizes close encounters"), and tuning it belongs with the training loop; the data-side contract here only guarantees the draw is well-defined, duplicate-free, and seeded. Robustness framing: the verdict's *form* does not depend on CLM-10 at all — `min(cap, n)` is correct whether the true counts are 59/125/1000 or anything else; CLM-10 only determines whether the cap ever binds in practice.

**Evidence.** Issue-doc position: lines 60 (M12 row), 77 (reclassification ledger), 286 (P1-4), 298 (checklist self-contradiction: 59→29 and 1000→128), 13 (its own ~59-snapshot figure). Master: Q-B1 block with the WR-03-corrected citation (lines 366–384), CLM-09/CLM-10 rows (598–599). Framework spec: `ctl` "Mini-Batch Construction with Lookahead Sampling" (lines 1197–1210: B=256, ~5% lookahead, "n_pts (e.g., 32)", 50% uniform / 50% acceleration-weighted, replay 240 / lookahead 16); `pinn` §3.1 batch construction (lines 323–351: `points_per_trajectory=32`, `N_data = 256·32 = 8192`, snapshots-sourced, author flag) and SI-PINN-003 (lines 1002–1006). Admission-gate floor: Q-A1 in this document (57-snapshot minimum for admitted standard trajectories from CLM-09 + the 9.5 rule).

**Confidence.** High on the contract form (clauses 1, 3, 4). Medium on retaining 32 as the default cap — it is the spec's example, not an evidenced optimum, and re-tuning it is a doc-03/training-loop matter. The single factor most likely to change the verdict: **DATA-06** revealing an admitted-population snapshot distribution materially below ~57 (e.g., widespread irregular grids), which would make the cap binding and put pressure on the default's value — not on the `min()` form.

**Verification suggestion.** DATA-06 snapshot-count distribution per variant over the **admitted** set. Unit tests: `n = 59 → 32` distinct indices, exactly `16 + 16` weighted/uniform; `n = 10 → 10` distinct indices (cap inactive, no error); fixed seed ⇒ identical draws; all drawn times exist in the trajectory's snapshot set.

### 4.2 Q-B2 — Footer / mass-drift protocol

**Verdict.** The required IC↔Brutus mass-consistency contract:

1. **Coverage: all pairs, not a sample.** At preprocessing, for every admitted `(variant, id)`, compare the three IC masses against the three Brutus `t = 0` masses. The cost is three scalars per pair across ~15,028 pairs — negligible — so the issue doc's sampling protocol is superseded by 100% coverage. This **dissolves WR-01** operationally: the 1,000-vs-100 internal conflict (issue doc line 202 vs P2-2 line 292) becomes moot because no sample size is needed; the conflict itself is still reported as an issue-doc defect (§6, F-3), and whether it receives a CLM row remains the open Phase-24 user-gate decision per the master — not settled here.
2. **Gate:** `max_i |m_IC,i − m_Brutus,i(t=0)| < 1e-15`, **absolute**, in float64 parse space — deliberately the same tolerance, space, and style as the existing `ctl` §2.1 intra-trajectory mass-invariance gate, and appropriate because the masses are O(1) by construction (both families normalize to `Σm = 3`), making absolute-1e-15 ≈ relative-1e-15..1e-14.
3. **Implementation warning:** do **not** use `np.allclose(rtol=1e-15)` with default arguments as P2-2 suggests — `np.allclose`'s default `atol = 1e-8` would pass absolute discrepancies up to eight orders larger than the gate. Either set `atol` explicitly (`rtol=0, atol=1e-15` for the absolute gate) or use a plain max-abs comparison.
4. **Escalation on failure (and only on failure):** re-compare the raw mass *strings* with `decimal.Decimal`. Decimal-equal ⇒ the float64 path has a parser bug (fix the parser; the data is fine). Decimal-unequal ⇒ a genuine textual/data discrepancy ⇒ quarantine the trajectory and log `(variant, id, body, |Δm|)`. Routine Decimal parsing is **not** adopted (cross-ref Q-B3).
5. **On pass:** the IC masses are canonical and feed the IC₁₃ raw-mass slots (HC-2); the Brutus echo is confirmatory metadata.

Expected outcome: a trivial pass — the spec's own sample Brutus output echoes the IC mass strings byte-identically in every block (e.g., `1.3490330328149076` at `t=0` and `t=0.08` alike). One framing correction is surfaced respectfully: the master's "spec is silent on a mass-drift verification protocol" is **incomplete** — `ctl` §2.1 already carries the folded-in B-11 "IC ↔ BRUTUS mass consistency" assertion; what is genuinely missing is only the explicit cross-file formula, tolerance arguments, and escalation path, which SPEC-6 supplies as a §2.1 amendment.

**Reasoning.** The numerical core is a one-ulp argument. IEEE-754 binary64 parsing of a decimal string is correctly rounded in CPython/NumPy: the *same* string always parses to the *identical* double, so textual equality ⇒ exact float equality ⇒ gate margin is infinite. If the strings differ but encode reals within one ulp of each other, the parsed doubles differ by at most ~2.2e-16 for O(1) values — an order below the 1e-15 gate — so the gate cannot be tripped by representation noise alone. Contrapositive: **a gate failure is evidence of a genuine discrepancy** (a rounded echo, a corrupted digit, a wrong file), which is exactly what the Decimal escalation then classifies into parser-bug vs data-defect. This is why the issue doc's framing ("text output may round" ⇒ pre-emptive Decimal) is inverted into fail-fast-then-escalate: Decimal buys nothing while the gate passes and is the right *diagnostic* when it does not. The all-pairs decision follows from cost (microseconds per pair) and from what the check protects: the IC₁₃ contract (HC-2) consumes these masses per trajectory, so a sampled audit certifies the wrong thing — the production gate must cover what production consumes. The absolute-tolerance choice mirrors §2.1 deliberately so the two mass gates (intra-trajectory drift; IC↔Brutus agreement) share one tolerance discipline; the O(1) mass scale (hierarchical sampling normalizes `m₁+m₂+m₃ = 3`; standard uses equal unit masses) is what licenses absolute form.

**Evidence.** Issue-doc position: lines 200–207 (protocol notes; the 1,000 figure at 204), 292 (P2-2: 100 pairs, `np.allclose(rtol=1e-15)`), 214 (Decimal-for-masses rationale), 343 (DataLoader req. 5). Master: Q-B2 block incl. the WR-01 surfacing (lines 386–403), WR-01 status (lines 1035–1040, 1047–1048: open, Phase-24-owned), CLM-09 row (598). Framework spec: `ctl` §2.1 (lines 397–413: float64 parse space, `max_{t,i}|m_i(t) − m_i(0)| < 1e-15`, reject/quarantine, folded-in B-11 IC↔Brutus mass-consistency assertion); sample Brutus output with byte-identical mass echoes (lines 309–322). Mass normalization Σ=3: `sampling_method.md` line 23 (hierarchical, FROZEN historical fact); standard equal masses: issue doc line 312 (dataset table).

**Confidence.** High. The single factor most likely to change the verdict: **Phase-24 (DATA-05)** discovering systematic IC-vs-Brutus textual divergence at scale — that would convert the escalation path into a standing Decimal-for-masses requirement (clause 4's else-branch becoming the rule), while leaving clauses 1–3 intact.

**Verification suggestion.** DATA-05: run the all-pairs comparison; report the max absolute discrepancy per variant (expected: exactly 0 for string-identical echoes). Unit tests: a fixture with one mass digit perturbed at the 16th significant figure passes the gate; perturbed at the 14th figure fails the gate, and the Decimal escalation classifies it as data-defect; an `np.allclose`-default implementation is caught by a test where `|Δm| = 1e-10` (must fail the gate; default-args `allclose` would pass it).

### 4.3 Q-B3 — Precision handling (float64 sufficiency; Decimal-for-masses)

**Verdict.** **float64 is sufficient for all data-side validation metrics (SCS, SASD, IPR, PSC)**, computed on CPU from float64-parsed arrays (stored per Q-A6). `decimal.Decimal` is required nowhere routinely; its sole mandated role is the Q-B2 escalation diagnostic on a mass-gate failure. Optional (recommended, not required) hygiene: pairwise or compensated (Kahan) summation in the Hamiltonian accumulation. The `|H(0)| → 0` edge case is handled by the dqa's undefined-SCS rule (quarantine for manual review), not by higher precision. The issue doc's *conclusion* (float64 acceptable; Decimal only for masses) is **endorsed**; two elements of its *reasoning* are corrected below, and one conflation is clarified: HC-4's dual-epsilon split (`ε = 1e-10` validation vs `ε_train = 1e-5`) governs **softening**, a physics-model parameter — it neither requires nor constrains arithmetic precision, so there is no tension between HC-4 and float64.

**Reasoning.** The error budget, end to end. (i) Parsing: correctly rounded decimal→binary64 conversion contributes ≤ ½ ulp ≈ 1.1e-16 relative per value — this holds whether the source string carries 17 digits (the `t=0` blocks, which echo the ICs) or ~41 digits (later blocks); digits beyond ~17 simply sharpen the rounding, they cannot worsen it. (ii) Metric arithmetic: evaluating `H = T + V` sums ~6 pair terms plus three kinetic terms; naive accumulation contributes a few × 1e-16 relative in `T` and `|V|` separately. (iii) Conditioning: the relative error of `H` is amplified by roughly `(2T + |V|)/|H|` under input perturbation — O(1–10) for ordinarily bound systems, diverging only as `|H| → 0`, which is precisely the population the dqa already routes to manual review. Net: the float64 noise floor on `ε_H` sits at ~1e-15..1e-13 even with amplification — **at or below the data's own integration tolerance** (CLM-09: 1e-13..1e-15) and **eight-plus orders below the 1e-5 reject gate**. The same budget covers SASD (ratios of O(1) norms), IPR (spline + force arithmetic; gate 1e-3), and PSC (binning is precision-insensitive). Corrections to the issue doc's reasoning: first, "float64 preserves approximately 1–3 guard digits beyond the Brutus tolerance" overstates the margin at the tight end — against `tol = 1e-15` the parse noise (~1.1e-16) leaves barely one decimal digit — and frames the wrong comparison anyway: what matters is metric noise vs the *gate scale* and vs the *data's intrinsic accuracy*, both of which clear decisively. Second, "Brutus output files contain 30–40 significant digits" is block-dependent: the `t=0` block carries 17-digit IC echoes; the ~41-digit mantissas appear from the first integrated block onward (both visible in the spec's sample output). Neither correction changes the conclusion; both matter for a reviewer re-deriving it. Finally, what higher precision *would* buy — exact reproduction of Brutus's internal multi-precision state — is consumed by nothing in this framework: metrics gate at 1e-5/1e-3, data tolerances stop at 1e-13..1e-15, and the network trains in float32/64.

**Evidence.** Issue-doc position: lines 208–216 (precision section: 30–40 digits, 1–3 guard digits, float64-CPU constraint, Decimal-for-masses, dual-epsilon restatement). Master: Q-B3 block (lines 405–417), CLM-09 row (598). Framework spec: `ctl` numerical defaults "use double precision for all invariants" (lines 907–912); sample output digit structure (lines 311–322: 17-digit `t=0` block vs ~41-digit `t=0.08` block). dqa: `H(0)` near zero ⇒ SCS undefined ⇒ manual review (line 120); gate scale (130, 233–234). HC-4 (master lines 177–184) for the softening/precision distinction.

**Confidence.** High. The single factor most likely to change the verdict: Phase-24 discovering a **non-trivial admitted population with `|H(0)|` within ~1e-10 of zero** — beyond what manual review absorbs — which would force a dedicated near-zero-energy metric variant (e.g., absolute-drift gating) rather than higher precision per se.

**Verification suggestion.** Synthetic perturbation probe: take real trajectories, inject ±1-ulp noise into all coordinates, and show `|Δε_H| ≲ 1e-13` — direct measurement of the metric noise floor. Cross-check one trajectory's `ε_H` computed naively vs with Kahan summation (difference should be ≪ gate). DATA-05/06 piggyback: log the `|H(0)|` distribution to size the manual-review population.

### 4.4 Q-B4 — Global-scale `compute_globals` / `D = 6.694` (KNOWN CONFLICT)

**Verdict (constraint-entailed; reconciliation presented, adjudication downstream at EVID-10/PIPE-09).** The data pipeline's global-scale computation **must use the locked raw-mass convention** `D = (G·T²)^{1/3} ≈ 4.6416` with `T = 10, G = 1` (HC-6 / PHYS-01). The issue doc's CLM-13 position (`D = cbrt(G·M_tot·t_max²) = 6.694`, P1-7 "recompute global scales") is, as a pipeline instruction today, (a) **a direct HC-6 violation** — `ctl` §2.5 derives the raw-mass form and explicitly rejects 6.694 "except under a mass-fraction convention rewrite" documented as future-only; and (b) **internally inconsistent as written**: its `compute_globals` listing scales coordinates by the mass-fraction `D = 6.694` while computing kinetic and potential energy with the *raw* masses parsed from the IC file — mixing the two conventions inside one function, so the resulting `E` values are dimensionless in *neither* system. Independently of the D question, the listing contains a second defect that must not be transcribed: it regularizes the potential with **additive** epsilon (`r_ik = ‖Δr‖ + eps`), the exact PHYS-03 anti-pattern; the invariant `V` must use the **Plummer** form `√(‖Δr‖² + ε_inv²)` with `ε_inv = 1e-10`, and ε enters `V` only. Per the question's ask, the adoption cost of the mass-fraction alternative is presented (below) without re-opening it. Side findings folded in: canonicalize the `E_scale` floor at **`1e-8`** and fix `ctl` §2.5's `1e-10` (three-source majority; details in §6 F-2 / SPEC-7); the listing's `r_char` (mean of the three pairwise distances) and `Q_scale = 0.5` **match** the spec; and `compute_globals` should run over the **admitted set** (post-gate, post-blacklist) — a minor judgment call flagged as such, since medians are robust either way, but admitted-set input is deterministic and immune to NaN poisoning from corrupt files.

**Reasoning.** The two conventions are both *internally* coherent; the lock is about which one this framework is built on. Derivation in two lines: substituting `r = D r'`, `t = T u` into Newton's equation and demanding the dimensionless residual `d²r'/du² = Σ m_j (r'_j − r'_i)/‖r'_j − r'_i‖³` **with raw masses** forces `D³ = G T²` ⇒ `D ≈ 4.6416`. Writing the same residual with mass *fractions* `m_i' = m_i/M_tot` instead forces `D³ = G M_tot T²` ⇒ `D ≈ 6.694` (with `M_tot = 3`, which both IC families satisfy by construction — hierarchical sampling normalizes `Σm = 3`, standard uses three unit masses — so the issue doc's *arithmetic* is right; its *convention* is the rejected one). The consequence of half-adopting it, as the listing does, is concrete: under a D change, kinetic energy scales as `D⁻²` and potential as `D⁻¹`, so scaled `E` values shift **non-uniformly** across trajectories — and scaled `E` is not merely fed to a robust normalizer, it is compared against locked stage thresholds (`E < −0.5`, `|E| < 0.01` in the stratification), all of which silently change meaning. Hence the full adoption cost the spec itself documents and this verdict itemizes: replace every mass with `m/M_tot` in every residual, Hamiltonian, angular-momentum, COM, and invariant formula; re-derive the stage thresholds; recompute `E_scale`/`s_min,scale` and all normalizer statistics; regenerate processed stores; retrain. That is a convention migration, not a bug fix — which is exactly why PHYS-01 was locked and why P1-7's checklist framing ("global scales … differ by amounts consistent with D=4.64→6.694 correction") presupposes the contested conclusion. The additive-ε defect is independent and unambiguous: `ctl`'s PHYS-03 anti-pattern text forbids mixing `(‖r‖+ε)` forms with Plummer forms and restricts `ε_inv` to `V`; an additive `1e-10` also (mildly) perturbs `r_char` semantics if ever copied there. On the E_scale floor: §2.5 says `+1e-10`, while the network-facing Step-4 table, `pinn` §5.2, and the issue-doc listing all say `+1e-8`; since the slot normalization `tanh(E/E_scale)` is the consumer, the network-facing value wins and §2.5 is the typo (full treatment in §6 F-2).

**Evidence.** Issue-doc position: lines 218–258 (Global Scale Computation: the listing with `D = np.cbrt(G·M_tot_ref·t_max²)`, raw-mass `T`/`V_pot`, additive `+ eps`, `E_scale … + 1e-8`, `Q_scale: 0.5`), 231 and 258 (6.694 assertions), 289 (P1-7), 300 (checklist). Master: Q-B4 block (lines 419–436), CLM-13 row + note (602, 635–640), HC-6 (lines 198–203). Framework spec: `ctl` §2.5 (lines 576–608: scaling block `D = (G·T²)^{1/3}`, `D ~ 4.6416` at 587; Governing Mathematical Convention with the raw-mass derivation and the explicit rejection of 6.694 at ~593–604; `E_scale = |median(E)| + 10⁻¹⁰` at 608; `r_char` and `Q_scale = 0.5` at 609–611); PHYS-03 anti-pattern and `ε_inv = 1e-10` scope (lines 698–704; reaffirmed at 909–912 and 979–980); Step-4 energy-slot row `E_scale = |median(E)| + 10⁻⁸` (line 1049); `pinn` §5.2 `E_scale … + 10^-8` (line 761) and unit-system row `D = ∛(GT²)` (line 926). Mass normalization: `sampling_method.md` line 23 (Σ = 3, FROZEN). Stage thresholds consuming scaled `E`: `ctl` stratification (lines 105–245).

**Confidence.** High — constraint-entailed. The single factor that could change it is **a user decision to reopen PHYS-01** (the documented future mass-fraction rewrite), which is out of scope for this research by construction; no dataset probe bears on a convention choice (CLM-13's own row note says as much).

**Verification suggestion.** Dimensional-consistency unit test: integrate an analytic two-body circular orbit, apply the locked `(D, T)` scaling, and confirm the dimensionless residual coefficient is 1 with raw masses (and is `M_tot` ≠ 1 if mass fractions are wrongly substituted). Static check: grep the pipeline for `6.694` / `M_tot` inside any `D` computation and for additive-ε potentials. Recompute `E_scale`/`s_min,scale` on the admitted set under the locked convention and archive them with the §2.6 metadata for Phase-24 comparison.

---

## 5. Cluster C — Validation Metrics (Phase 28)

> Scope note honored throughout: only the **data-side definitions** are resolved. SASD-weighted collocation sampling, the IPR-as-ALM-noise-floor role, and PSC-governed replay are doc-03 forward-references and are not answered.

### 5.1 Q-C1 (SCS) — Symplectic Conservation Score (definition + thresholds, KNOWN CONFLICT)

**Verdict (locked elements restated; reconciliation presented; adjudication downstream at VAL-01/EVID-10).** The correct data-screening definition and gate are the locked HC-5 forms, verbatim:

$$\varepsilon_H = \max_{t \in [0,T]} \left| \frac{H(t) - H(0)}{H(0)} \right|, \qquad SCS = \log_{10}(\varepsilon_H), \qquad \text{reject if } SCS > -5 \ (\varepsilon_H > 10^{-5}).$$

Operational completions, all from the dqa text (annotated: locked post-v1.3, SI-DQA-003; sole written home is a read-only research report):

1. **Band boundaries are non-strict** (dqa "Boundary Behavior"): `ε_H = 1e-5` exactly is **Marginal** (`−6 < SCS ≤ −5`), not Reject; the reject set is strictly `SCS > −5`.
2. **`H(0)` numerically near zero ⇒ SCS undefined ⇒ quarantine for manual review or re-simulation** — never forced through the logarithmic gate.
3. **`H` evaluation:** Plummer-softened potential with the HC-4 validation epsilon `ε = 1e-10` (the `ctl` `ε_inv` convention). At admitted separations (prescreen enforces min pair distance ≥ 0.01) the softening correction is ≤ `(ε/r)²/2 ≈ 5·10⁻¹⁷` relative — below machine epsilon — so this is numerically identical to the unsoftened Hamiltonian the dqa derivation writes; the issue doc's self-contradictory phrase "unsoftened static epsilon (ε = 1e-10)" denotes the same computation.
4. **Units:** compute in raw G=1 coordinates (the dqa loads raw Brutus output). This is also a free choice: under the locked scaling `H' = D·H` exactly (since `D³ = G T²` makes `V² = 1/D`, both `T` and `V_pot` scale by `1/D`), so the **relative** drift `ε_H` is invariant — raw and scaled evaluations agree to machine precision. State the invariance in the spec so implementations cannot diverge.
5. **Metadata:** record the trajectory's `ε_H`, `SCS`, and dqa band label (Excellent `≤ −10` / Acceptable `(−10, −6]` / Marginal `(−6, −5]` / Reject `> −5`) per record; the gate consumes Stage-4 metrics where present and recomputes otherwise (Q-A1 clause 3).

**Reconciliation of the seed conflict.** The issue doc's formula `SCS = max_t |H(t) − H(0)|/|H(0)|` (its line 140) is **exactly `ε_H`** — its "SCS" is the raw ratio, a nomenclature collision with the ratified log-score, which is precisely the category error SI-DQA-003 records being fixed at the source ("a logarithmic-vs-raw-drift category error in the Phase 1 SCS gate"). Read in raw-ratio terms, its `1e-6` reject threshold is the dqa **Acceptable/Marginal boundary** (`SCS = −6`) promoted to a reject gate — a stringency change with no ratification trail; its Stage-5 `1e-8` tightening has **no traceable source anywhere in the package**. Disposition: **do not transcribe the ratio thresholds.** The locked gate is the sole reject criterion; the graded structure the issue doc reaches for already exists as the dqa bands and is preserved as metadata (clause 5), so nothing protective is lost. **Stage-conditional tightening** (stricter screening for gold/Stage-5 data) is **deferred for insufficient evidence**: the discriminating test is the post-Phase-24 per-variant `ε_H` distribution — if the gold distribution carries no mass above `1e-8` (plausible: gold runs at `tol = 1e-13/1e-14` over ~1,000 outputs), the proposed tightening is non-binding and moot; if it does, the marginal band gives the review mechanism while a ratified tightening is considered. Finally, a **documentation-fragility fix** is proposed: transcribe the locked gate into the editable `ctl` spec (SPEC-1's admission-gate clause), with the SI-DQA-003 annotation — this *implements* HC-5 and removes its single-point-of-documentation status (the master itself flags that the gate "does not live in any editable framework spec"); it does not reopen the gate. The two `ε_H` symbols stay disjoint per the master's note: nothing here touches the training energy-denominator floor `ε_H = 1e-4·S_H`.

**Reasoning.** Most of this verdict is restatement under HC-5; the analytic content is in clauses 3–4 and the threshold archaeology. Clause 3 closes the only definitional ambiguity (which ε enters `H`): HC-4 assigns `ε = 1e-10` to validation metrics, the `ctl` invariant convention names the identical `ε_inv = 1e-10` Plummer form, and the prescreen's hard `min distance ≥ 0.01` bounds the correction below representability — so the choice is constraint-consistent *and* provably inconsequential, which is the strongest position a spec line can be in. Clause 4's invariance proof matters operationally because the pipeline has both raw and scaled data in flight; a one-line homogeneity statement prevents a class of silent unit bugs. On the thresholds: tracing `1e-6` to the band boundary explains its origin without endorsing it (a band edge is a *labeling* line, not a *rejection* line, by the ratified semantics), and the absence of any source for `1e-8` is itself the finding — under this package's own evidence standard an unsourced number cannot be transcribed into a gate.

**Evidence.** Issue-doc position: lines 129–141 (SCS section: roles, `> 1e-6` and `< 1e-8` thresholds at 133–134, "unsoftened static epsilon (ε = 1e-10)" at 137, raw-ratio formula at 139–141). Master: seed-conflict worked example (lines 132–139), HC-5 (186–196), two-`ε_H` note (205–219), Q-C1 block (444–461). dqa: definition split `ε_H` vs `SCS` and the undefined-`H(0)` rule (line 120), bands (124–130), Boundary Behavior (132–134), Phase-1 gate (233–234), SI-DQA-003 (325–328: category error; reject tightened `−4 → −5` under the ratified gate-led policy). HC-4 and `ε_inv`: master lines 177–184; `ctl` lines 698–704, 909–912. Prescreen min distance: `sampling_method.md` lines 210, 230 (FROZEN). Stage-4 metrics provenance: master lines 878–905.

**Confidence.** High — the gate is locked; the completions are dqa-textual or proved inconsequential. The single factor bearing on the *open* sub-question (stage-conditional tightening): **Phase-24 per-variant `ε_H` distributions** — a heavy gold tail above `1e-8` would make the deferred tightening question live; nothing changes the gate itself.

**Verification suggestion.** Recompute `ε_H` independently for a stratified sample and reconcile against the Stage-4 metrics JSONs (catches definition drift in the existing metrics). Per-variant `ε_H` histograms (the tightening discriminator). Unit tests: `ε_H = 1e-5` exactly labels Marginal and is admitted; a synthetic `H(0) = 0` system quarantines; raw-vs-scaled `ε_H` agree to ≤ 1e-14 relative.

### 5.2 Q-C2 (SASD) — Stiffness-Aware Sampling Density (data-side)

**Verdict.** Data-side definition, completing the dqa formula where it is ambiguous (completions labeled as judgment):

1. For each inter-snapshot interval `i` (between `t_i` and `t_{i+1}`, `Δt_i` from the file's own timestamps):
   $$SASD_i = \Delta t_i \cdot \max_{b \in \{1,2,3\}} \ \max_{t \in \{t_i,\, t_{i+1}\}} \frac{\lVert \mathbf{a}_b(t) \rVert}{\max(\lVert \mathbf{v}_b(t) \rVert,\ 10^{-12})}$$
2. **Accelerations are analytic**, evaluated from the Newtonian pairwise force at the snapshot state with the HC-4 validation Plummer softening `ε = 1e-10` — **not** finite-differenced from neighboring snapshots, which would estimate `a` from exactly the undersampled data whose adequacy is being tested and corrupt the signal in the stiff regime.
3. **Per-body max** (judgment): the body whipping through a close encounter sets the local timescale; a system-norm ratio dilutes a one-body spike by the two quiescent bodies. **Endpoint evaluation** (judgment, forced): interior spikes between snapshots are invisible to any snapshot-resident statistic — an acknowledged blind spot the issue doc itself notes ("SASD floor effect") and that IPR complements (Q-C3), since the spline residual *does* probe interval interiors.
4. **Denominator guard `1e-12` with flag-if-binding:** a near-zero `‖v_b‖` at a turning point legitimately means a tiny characteristic timescale, so the guard exists only to keep arithmetic finite; any interval where it binds is flagged `v_floor_hit` for review rather than silently normalized. The dqa's curvature-based robust form (`ρ_curv = v²/a_⊥`) is noted as an optional refinement, not the contract.
5. **Trajectory score:** `SASD(traj) = max_i SASD_i`. **Criterion: flag — not reject — if `SASD(traj) > 0.5`** (the package's only stated value; dqa: "flag for Resampling. Do not train on this trajectory yet"), threshold **provisional** pending Phase-24 distributions. The metric is dimensionless and exactly invariant under the locked scaling (`Δt' = Δt/T`, `a' = a·T²/D`, `v' = v·T/D` ⇒ the product is unchanged), so raw-vs-scaled evaluation is immaterial; compute in raw units for consistency with the dqa Phase-1 pipeline.
6. **Flag consumption (data-side only):** flagged ∧ gold counterpart exists ⇒ the requirement is already satisfied — the gold file *is* the higher-resolution resample (`dt_out = 0.01`), used at its own stage; the base sample's flag is informational. Flagged ∧ among the gold-missing set ⇒ a **genuine resample-queue entry** — and the intersection of this queue with the 184 gold-less IDs is the principled selection criterion offered to the Q-A4 user gate. The training-loop use of the SASD *profile* (collocation weighting) is doc-03 and is not specified here.

Proposed spec home: SPEC-8 (data-side metric contracts).

**Reasoning.** The dqa fixes the scalar form (`SASD_i = Δt_i · ‖a‖/‖v‖`, the inverse local timescale comparison) and the 0.5 flag level but is silent on the body-aggregation, the evaluation points, the source of `a`, and the failure semantics — clauses 2–4 close those gaps with the least-surprising physics-faithful choices and label them. A sanity bracket supports the 0.5 level as at least order-correct for the populations it must separate: near the Stage-6 stiffness boundary (`r ≈ 0.5`, O(1) masses) the per-body `a/v` ratio is ~4, so a standard-base interval (`Δt = 0.17`) scores ~0.7 — flagged, as intended; a wide quiet triple (`r ≈ 2`) scores ~0.04 — passes. Gold resolution divides every score by 17, which is exactly the "resample at `dt = 0.01`" remedy the dqa names. The flag-not-reject semantics matter: SASD failures indicate the *sampling* is inadequate, not that the trajectory is unphysical, so discarding would throw away dynamics the curriculum explicitly wants (Stage 6 exists for them); the remedy is resolution, which the gold folders already supply for all but the 184. Clause 2's analytic-`a` rule is the one place a plausible implementation would silently go wrong: central differences over `Δt = 0.17` near an encounter underestimate `‖a‖` precisely when SASD should fire.

**Evidence.** Issue-doc position: lines 143–153 (SASD section incl. the training-loop weighting forward-reference, not answered here), 16 (SASD floor effect / interior blindness). Master: Q-C2 block (463–474), CLM-09/CLM-10 rows (598–599). dqa: derivation and definition (§3.2, lines ~140–152; formula at 152), interpretation bands (154–157), flag rule `> 0.5` (158), Phase-1 stiffness step (239–242). HC-4 validation ε: master 177–184. Stage-6 boundary `s_min < 0.5`: `ctl` lines 237–243. Gold `dt_out = 0.01`: CLM-09 (master 781–786).

**Confidence.** Medium. The definition's load-bearing completions (per-body max, endpoint evaluation, analytic `a`) are this document's judgment, clearly labeled; the 0.5 threshold is provisional. The single factor most likely to change the verdict: **Phase-24 per-variant SASD distributions** — if gold trajectories do not pass cleanly or standard-base encounters are not caught at 0.5, the threshold (and possibly the aggregation choice) gets recalibrated.

**Verification suggestion.** Distribution probe (DATA-06-adjacent): per-variant `SASD(traj)` histograms; expected ordering gold ≪ hierarchical-base < standard-base, with the flagged set concentrated in low-`s_min` trajectories. Unit test: analytic two-body circular orbit, where `‖a‖/‖v‖ = v/r` exactly, recovers `SASD = Δt·v/r` to machine precision; a synthetic near-radial encounter trips the `v_floor_hit` flag.

### 5.3 Q-C3 (IPR) — Interpolation Physics Residual (data-side, dual-epsilon)

**Verdict.** Data-side definition:

1. **Interpolant:** per-component `CubicHermiteSpline(t, q, dydx = v)` — the cubic Hermite interpolant that consumes the file's **own velocities as the derivative data**. The dqa names "PCHIP" but describes exactly this object ("Cubic Hermite Splines (which preserve positions and velocities)… using the data {(qᵢ, vᵢ)}"); scipy's `PchipInterpolator` is a different algorithm (Fritsch–Carlson monotonicity-preserving slope *estimation*) that would discard the data velocities. The name is a misnomer; the construction is unambiguous and is pinned here.
2. **Collocation points:** `M = 10` **deterministic** interior points per interval, `τ_{i,j} = t_i + (j − ½)·Δt_i/10`, `j = 1..10` (the dqa fixes 10 per interval; mid-offset placement avoids the data points themselves and makes the metric reproducible without a sampling seed).
3. **Residual:** with `r_k = q̈_{spline}(τ_k) − a_{grav}(q_{spline}(τ_k)) ∈ ℝ⁹` (stacked bodies), `IPR = (1/M_{tot}) Σ_k ‖r_k‖²`, where `a_{grav,i} = Σ_{j≠i} m_j (q_j − q_i)/r_{safe,ij}³` and `r_{safe,ij} = √(‖q_j − q_i‖² + ε²)`. Note `q̈_{spline}` of a cubic Hermite is piecewise-linear per component — cheap and exact to evaluate.
4. **Epsilon (constraint-entailed):** the **data-side IPR uses `ε = 1e-10`** — it is a validation metric, so HC-4's static validation epsilon governs, consistently with SCS and SASD. The issue doc's `ε = 1e-5` (its formula is explicitly labeled `F_gravity^{ε=1e-5}`) belongs to the **different, doc-03-deferred role**: IPR as the ALM physics-loss noise floor, which by construction must use the training softening `ε_train = 1e-5` to be comparable to `L_phys`. Both epsilons are right *for their roles*; only the data-side role is posed here. **Forward-reference flag:** the data-side IPR (`ε = 1e-10`) is **not numerically comparable** to `L_phys^{ε=1e-5}`; when doc-03 takes up the noise-floor role it must recompute the residual at `ε_train` rather than reuse this metric. The divergence is material exactly where it matters — at separations approaching `ε_train` (`r ~ 10⁻³`–`10⁻⁵` encounters) the two force laws differ at order unity — and negligible elsewhere.
5. **Units (must be stated):** raw G=1 units, matching the dqa Phase-1 pipeline (it loads raw Brutus output before any preprocessing). IPR carries dimensions of acceleration², so the scaled-unit value differs by `(T²/D)² ≈ 464×` — an unstated-units gate is a latent factor-of-500 bug. **Gate: `IPR > 10⁻³` ⇒ reject or resample** (dqa Phase-1), pinned to raw units and **provisional** pending Phase-24 distributions.
6. **Diagnostics:** store the per-interval maximum `‖r_k‖²` alongside the trajectory aggregate — it localizes the offending segment, which is what the causal-firewall analysis needs (one bad interval, not a bad trajectory, is the typical failure).

Proposed spec home: SPEC-8.

**Reasoning.** Clause 4 is the heart of the question and is decided by role, not preference: HC-4 splits the epsilons *by function* — validation metrics evaluate "true Newtonian fidelity, not the regularized physics the network actually trains on" (the issue doc's own precision section states this rationale verbatim) — and the data-side IPR is a data-screening validation metric, so it inherits `1e-10`; meanwhile the dqa's "Updated role" paragraph (noise floor for ALM, halts μ_p escalation) only functions if computed with the network's `ε_train`, which is why the issue doc's formula says `1e-5`. The apparent conflict dissolves into two metrics with one name — and the spec text must say so, or the first implementation will compare incommensurable numbers. Clause 1 prevents a quiet correctness bug with an off-the-shelf library call: `PchipInterpolator(t, q)` type-checks, runs, and computes the wrong interpolant (its slopes are shape-derived, so the residual would partly measure the slope estimator, not the data). Clause 5's factor-464 arithmetic is the locked scaling applied to acceleration² (`a' = a·T²/D`; `(T²/D)² = (100/4.6416)² ≈ 464`). Clause 2's determinism choice trades a vanishing amount of estimator variance for exact reproducibility across runs and machines — appropriate for a gate.

**Evidence.** Issue-doc position: lines 155–165 (IPR section: PCHIP wording, noise-floor role, `F^{ε=1e-5}` formula at 161–163, μ_p halt at 165), 216 (dual-epsilon rationale sentence). Master: Q-C3 block (476–486), doc-03 boundary naming the IPR-as-noise-floor deferral (227–238), HC-4 (177–184). dqa: §3.3 protocol (lines 160–170: Hermite-with-(q,v), synthetic points between data points, residual eq. (6) at 168–170), 10 points/interval and the `> 1e-3` gate in Phase 1 (lines 244–252), causal-firewall localization rationale (§4.1, ~194–200). Scaling factor: `ctl` §2.5 (`D ≈ 4.6416`, `T = 10`).

**Confidence.** Medium overall — the epsilon assignment is High (constraint-entailed) but the gate value and the units pinning are provisional/judgment. The single factor most likely to change the verdict: **Phase-24 per-variant IPR distributions in raw units** — if the `1e-3` line bisects a clean population or passes an aliased one, the threshold (not the definition) moves.

**Verification suggestion.** Convergence test: analytic two-body circular orbit sampled at `Δt`, halve `Δt`, confirm IPR falls at the Hermite rate (residual `‖q̈_{spline} − a‖` shrinks ~`Δt²`, IPR ~`Δt⁴`) — validates the construction end to end. Per-variant IPR distributions (gold should sit orders below base). Cross-check: recompute one trajectory's IPR at `ε = 1e-5` and `1e-10` and confirm material divergence only when `min separation ≲ 10⁻³`.

### 5.4 Q-C4 (PSC) — Phase Space Coverage Entropy (data-side)

**Verdict.** Data-side definition — a dataset-level diversity metric over the **admitted** snapshot population, reported per variant and pooled (all parameters provisional and labeled):

1. **Coordinates (judgment):** for each snapshot, compute the three instantaneous pairwise distances, sort them `d_min ≤ d_mid ≤ d_max`, and bin the point at `(log₁₀ d_min, log₁₀ d_mid)`. Sorted pair distances are permutation-invariant (body relabeling), rotation/translation-invariant, and put the close-encounter structure on a log axis where it is resolvable — realizing the dqa's "(r₁₂, r₂₃) distance plane" example while removing its label dependence. Velocity axes are *not* added in the minimal contract (the dqa says "phase space" but exemplifies configuration distances; dimensionality is kept at 2 for occupancy).
2. **Grid (provisional):** fixed, dataset-independent edges over `[10⁻³, 10²]` per axis — floor a decade below the prescreen minimum distance 0.01 (in-flight encounters go below the IC-time bound), ceiling at the ejection scale — with **25 bins/axis (0.2 dex)**, `K = 625`; out-of-range values **clamp to edge bins**, so the lowest `d_min` rows *are* the `r_min → 0` stiffness cells the dqa says to inspect. Fixed edges keep `H` comparable across runs and variants.
3. **Estimator:** plug-in `p̂_k = n_k/N`, `H = −Σ p̂_k ln p̂_k` (natural log); report raw `H` and normalized `Ĥ = H/ln K ∈ [0,1]`. The plug-in bias is ≈ `−(K_{occ} − 1)/(2N)` (Miller–Madow), i.e. ~3·10⁻⁴ nats at `N ~ 10⁶–10⁷` admitted snapshots — negligible; the Miller–Madow correction is optional, not required.
4. **Stiffness Coverage Ratio (companion scalar):** `SCR = N(d_min < 0.5)/N`, report-only — `0.5` is the locked Stage-6 `s_min` boundary, so SCR reads as "fraction of snapshot mass in the extreme-stiffness regime," generalizing the dqa's empty-bin check.
5. **No reject gate.** PSC is diagnostic at report level: no threshold for `H` or SCR exists anywhere in the package, and the dqa's own use of PSC is for *composition* decisions (importance resampling, replay weighting) — which are doc-03. The data side computes, stores (optionally the per-snapshot bin index as metadata, the natural interface the deferred replay role would consume), and reports.

Proposed spec home: SPEC-8.

**Reasoning.** This is the most under-specified of the four metrics — the dqa gives one sentence of definition, one example plane, and an inspection heuristic — so the verdict's job is to make one concrete, defensible instantiation and to fence what it does *not* decide. Coordinate choice is driven by invariance (a diversity measure that changes under body relabeling or frame rotation measures bookkeeping, not dynamics) and by the metric's stated purpose (coverage of stable *and* close-encounter regimes ⇒ the encounter axis must be log-resolved). Grid arithmetic: 0.2 dex resolution puts the Stage-6 line (`log₁₀ 0.5 ≈ −0.30`) inside its own bin so SCR is consistent with a bin boundary; five decades × 25 bins balances resolution against occupancy (mean ~10³–10⁴ points/occupied bin at this N, comfortably estimable). The estimator analysis is what licenses simplicity: entropy estimation is bias-prone at small `N/K`, but at `N/K ~ 10³⁺` the plug-in bias is three to four orders below any difference one would act on, so heavier machinery (jackknife, coverage-adjusted estimators) is not warranted — stated with the citation so a reviewer can check the regime. The no-gate decision follows the package's own evidence standard: inventing a diversity floor with no source would be exactly the unsourced-threshold pattern rejected in Q-C1.

**Evidence.** Issue-doc position: lines 167–169 (PSC section: Shannon entropy over a discretized grid; replay governance — the latter deferred). Master: Q-C4 block (488–497), doc-03 boundary (227–238). dqa: §3.4 (lines 176–188: definition eq. (7), `(r₁₂, r₂₃)` example, low/high-entropy reading, `r_min → 0` bin check and importance-sampling recommendation). Prescreen min distance 0.01: `sampling_method.md` lines 210, 230. Stage-6 boundary: `ctl` lines 237–243. Estimator bias regime: Paninski (2003) (see References).

**Confidence.** Medium. The definition's structure is well-supported; every numeric (range, bin width, hence `K`) is a labeled provisional. The single factor most likely to change the verdict: **Phase-24 occupancy histograms** — in particular, if more than a few percent of snapshot mass clamps at the grid edges, the range widens (and `K` with it); a strong velocity-structure finding could also motivate the optional third axis.

**Verification suggestion.** Occupancy probe over the admitted set: per-variant 2-D histograms, edge-clamp mass fraction, `H`, `Ĥ`, SCR. Invariance unit test: random body permutations and rigid rotations/translations of a fixture leave every bin index unchanged. Estimator sanity: uniform synthetic occupancy over `K` bins recovers `Ĥ = 1` to within the Miller–Madow bound.

---

## 6. Cross-Cutting Findings

These findings emerged from cross-checking the package files against each other and against the verified CLM rows. None re-opens a Hard Constraint; each is either a spec-hygiene defect with a proposed fix (routed to a SPEC block in §7) or a package-level observation routed to the Open Items register (§8).

### F-1 — `ctl_instruction.md` Brutus-comparison table: per-set counts transposed

The `tab:brutus_compare` table (`ctl_instruction.md` lines 23–29) lists Set 1a = 4,857 Hierarchical, Set 1b = 4,857 Standard, Set 2a = 2,749 Hierarchical, Set 2b = 2,565 Standard (total 15,028). The verified dataset rows say otherwise: the standard **base** folder holds **2,749** files (CLM-05, `verified`) and the hierarchical **gold** folder holds **4,857** (master dataset context, parameter-tuple sums; erratum Correction 1 uses 4,857 as the hierarchical-gold denominator). So the table's Set 1b (standard base) and Set 2a (hierarchical gold) values appear **swapped**: the internally consistent assignment is Set 1a = 4,857 (hier base), Set 1b = 2,749 (std base), Set 2a = 4,857 (hier gold), Set 2b = 2,565 (std gold) — which preserves the stated 15,028 total (4,857 + 2,749 + 4,857 + 2,565 = 15,028) and matches every verified count. The transposition is consequential: stage stratification (`ctl` lines 105–249) keys data sources to these set labels, so a reader sizing Stage 3/4 from the table would expect ~4,857 standard-base trajectories where ~2,749 exist. Proposed correction: SPEC-9, **conditional on Phase-24 DATA-04** (the independent folder counts), since the fix transcribes dataset facts into an editable spec and DATA-04 is the committed probe for exactly those counts.

### F-2 — `E_scale` floor: three-way spec conflict (resolved to `1e-8`)

The energy normalizer's additive floor is stated three times with two values: `ctl_instruction.md` §2.5 line 608 says `E_scale = |median(E)| + 1e-10`; `ctl_instruction.md` Step 4 (line 1049) says `+ 1e-8`; `pinn_architecture.md` §5.2 (line 761, the network-facing input contract) says `+ 1e-8`. The issue doc's `compute_globals` listing (lines 218–258) also uses `+ 1e-8`. The majority position, and decisively the **network-facing contract** (the pinn §5.2 statement is what the 14D input slot actually consumes), is `1e-8`; §2.5's `1e-10` is the outlier and is best read as a typo propagated from the adjacent `ε_inv = 1e-10` softening constant. This floor is not among the six Hard Constraints, so correcting it is legitimate spec hygiene, not a re-opening. Resolution: canonicalize `1e-8` and amend `ctl` §2.5 line 608 — SPEC-7 (cross-referenced from Q-B4, §4.4). Numerically the choice is almost always immaterial (`|median(E)|` is O(0.1–1) in either unit system), but a single written value prevents implementation drift.

### F-3 — Issue-doc internal-defect catalog

The issue doc is the adjudication subject, and the package's source-treatment framing predicts it "may contain errors" (master lines 124–139). This research confirms six concrete internal defects, catalogued here so the downstream adjudication can weigh the document's reliability claim-by-claim rather than wholesale:

1. **The seed conflict (known going in).** Ratio-based SCS reject thresholds `> 1e-6` / `< 1e-8` (issue doc lines 133–134) versus the locked log-drift gate `SCS = log₁₀(ε_H)`, reject `SCS > −5` (HC-5; dqa lines 124–130, SI-DQA-003 at 325–328). Not the same quantity; adjudicated in Q-C1 (§5.1) — the `1e-6` figure is the Acceptable/Marginal **band boundary** mis-promoted to a reject gate, and `1e-8` is unsourced.
2. **WR-01 sample-size conflict.** The footer/mass-drift protocol prose says "parse **1000** IC–Brutus pairs" (line 202); Recommended Resolution P2-2 says "Batch-verify **100**" (line 292). Q-B2's verdict (§4.2) dissolves the operational question (the gate covers **all** pairs), but the documentary conflict stands and its CLM-row disposition is the open WR-01 user-gate decision (OI-5).
3. **P1-4 versus its own checklist.** P1-4 (line 286) proposes `n_pts = min(32, int(0.5 · n_snapshots))`; the verification checklist (line 298) expects gold trajectories to receive `n_pts = 128` — unreachable under the formula (`min(32, ·) ≤ 32`) and not equal to `0.5 × ~1000` either. Adjudicated in Q-B1 (§4.1); neither the `0.5` factor nor the `128` carries evidence.
4. **`compute_globals` mixed convention + additive epsilon.** The listing (lines 218–258) computes `D = cbrt(G·M_tot·t_max²) = 6.694` (mass-fraction `D`) while computing kinetic and potential energies from **raw** masses (raw-mass convention), an internally inconsistent hybrid; and it regularizes `V` with an **additive** `+ 1e-10` on the distance norm rather than the Plummer form — the exact PHYS-03 anti-pattern the spec names (`ctl` lines 698–704, 909–912). Adjudicated in Q-B4 (§4.4); fix in SPEC-7.
5. **Footer-schema premises contradicted by the corrected record.** The issue doc's "219 files with minimal footers (no `tol`)" and "footer schema varies (some omit `eta`, `tol`, or both)" (lines 66, 68, 196–207) are contradicted by erratum Correction 2 (master lines 980–1007): the 219 (and the 1,550 / 701 base populations) have **no footer at all**, and footers that exist carry the **full** schema. Adjudicated in Q-A5 (§3.5).
6. **`≥ 200` snapshot floor versus the doc's own dataset table.** P1-1 (line 283) proposes `snapshot_count ≥ 200` for Stage 4+, while the doc's own dataset table (lines 309–318) gives standard-base trajectories ~59 snapshots — the floor would reject the entire population that Stage 3/4 is *defined* over. Adjudicated in Q-A1 (§3.1): the floor is replaced by the variant-aware grid-consistency check.

The pattern across 3, 4, and 6 is the same failure mode: numerically plausible constants asserted without derivation from the dataset's verified parameters. The corrective standard applied throughout this document is that every numeric admitted into spec text is either sourced, derived (with the derivation shown), or explicitly labeled provisional.

### F-4 — Master's Q-B2 framing is incomplete: the spec is not silent

The master states "spec is silent on a mass-drift verification protocol" (Q-B2 block, line 398). This is incomplete: `ctl_instruction.md` §2.1 (lines 397–413) carries a mass-conservation gate `max_{t,i} |m_i(t) − m_i(0)| < 1e-15` (float64, absolute) **and** folds in the B-11-adjacent IC↔Brutus mass-consistency requirement (lines 410–413). What the spec lacks is only the *escalation* path (Decimal on failure) and the explicit IC-side comparison formula — which is what SPEC-6 adds. This is surfaced as a respectful correction to the package's framing, not a criticism: the master's "silent" claim was written against the issue doc's framing, and the §2.1 text is easy to miss because it is phrased as a trajectory-internal invariant rather than a cross-file protocol. Downstream consequence: Q-B2's verdict is **anchored in existing spec text**, which raises its confidence and means SPEC-6 is an amendment, not a new contract.

### F-5 — `trustworthy_horizon` is an undefined metadata field

`ctl_instruction.md` §2.6 (lines 628–647) requires per-record metadata including `brutus_tolerance`, `word_length`, `dt_out`, and `trustworthy_horizon` (line 646). The first three are populated by the Q-A5 footer contract (SPEC-3). `trustworthy_horizon` is **defined nowhere** in the package — no formula, no units, no consumer. It plausibly gestures at the converged-digits horizon concept from the Brutus literature (the time up to which the solution is converged at the run's tolerance), but guessing a computation rule would be inventing spec. Registered as OI-2 with two candidate dispositions for the spec author: (a) define it (e.g., from a per-run convergence diagnostic, if one exists upstream), or (b) drop the field from §2.6 until a consumer exists. SPEC-3 marks the field `reserved — definition pending OI-2` so the metadata schema remains stable either way.

### F-6 — `DELIVERY-NOTE.md` was not delivered with the package

The master's manifest lists `DELIVERY-NOTE.md` (D-16, handoff/gate context; master lines 74, 1057–1058) and the reading order directs the researcher to it, but the file was **not** among the six uploaded files. The miss is material only to gate context (Phase 25–29 gating is described as depending on it) — no framed question depends on its content, and this document is complete without it. Registered as OI-1: the spec author should confirm whether the omission was intentional (and if not, whether the note contains anything that would alter a verdict here — on the evidence of the master's own summary of it, nothing in scope).

### F-7 — Package arithmetic independently verified

All load-bearing counts in the package were re-derived from the package's own primitives and are internally consistent: the four-folder total `4,857 + 2,749 + 4,857 + 2,565 = 15,028` matches the `ctl` table total and the erratum's "all 15,028 files" scan denominator; the gold-gap identity `2,749 − 2,565 = 184` matches CLM-04, and the 184-ID list's maximum (3958) exceeds the standard-base file count (2,749), independently re-proving non-contiguity (Q-A2); the per-folder footer-tuple sums reproduce the folder totals exactly (hierarchical base `3,307 + 1,550 = 4,857`; standard base `1,126 + 922 + 701 = 2,749`; standard gold `1,754 + 592 + 219 = 2,565`; hierarchical gold: all 4,857 footered across 5 tuples); and the no-footer populations (1,550 / 701 / 219) match both Correction 2 and the 2025-12-24 footer-audit record cited there. No package count failed re-derivation. (These checks validate internal consistency only; the on-disk truth claim remains Phase 24's, per the CLM register.)

---

## 7. Proposed Specification Text

Nine spec blocks, each anchored to an editable framework spec (per the source-treatment rules, `ctl_instruction.md` and `pinn_architecture.md` are the only edit targets; the dqa and `sampling_method.md` are read-only). Proposed text is given in fenced blocks and is written to be transcribable by the spec author with at most local renumbering. Every numeric inside a block is sourced, derived in the corresponding §3–§5 resolution, or labeled `(provisional — OI-3)`.

### SPEC-1 — Trajectory Admission Gate (new subsection "Step 1A")

**Target:** `ctl_instruction.md`, new subsection inserted immediately after Step 1's item list (after line ≈ 381), before Step 2. **Implements:** Q-A1 (§3.1), Q-A3 (§3.3), Q-C1 (§5.1). **Consumes:** SPEC-2 (ID resolution), SPEC-3 (footer/defaults).

```
Step 1A — Trajectory Admission Gate (data-side; runs at DataLoader init)

Every (variant, folder, id) trajectory must pass ALL conditions below before it
may enter stage assignment (Step 5), global-statistics computation (compute_globals,
§2.5), or any training batch. Failures are recorded per-trajectory with a reason
code; the loader logs admitted/rejected/quarantined counts per folder at init.

1. Identity & blacklist. The id resolves via the Step-1 ID-resolution contract
   (item 7). (variant, id) pairs present in problematic_ics_blacklist.json are
   excluded from BOTH the base and gold folders of that variant, before stage
   assignment and before compute_globals. Missing blacklist file = hard init
   failure. A batch-time assertion re-checks emitted samples (defense in depth).
2. Structural integrity. >= 2 parsed snapshots; all coordinates, velocities,
   masses, and timestamps finite (no NaN/Inf); timestamps strictly monotone
   increasing.
3. Completeness. final_timestep >= 9.5 (the dataset's primary completeness rule).
   Footer presence, line counts, and snapshot-count constants MUST NOT be used
   as completeness signals.
4. Physical invariant gates. The Step-2/§2.1 gates apply as admission criteria:
   mass invariance max_{t,i} |m_i(t) - m_i(0)| < 1e-15 (float64, absolute);
   the IC<->Brutus t=0 mass gate of §2.1 (as amended by SPEC-6); the
   gauge-degeneracy and COM/momentum assertions with their existing
   reject/quarantine semantics.
5. Conservation gate (locked post-v1.3; SI-DQA-003). With H evaluated in float64
   using Plummer softening eps = 1e-10 in V (numerically identical to unsoftened
   at the dataset's r >= 0.01 scales):
       eps_H = max_t |(H(t) - H(0)) / H(0)|,   SCS = log10(eps_H)
   REJECT if SCS > -5 (equivalently eps_H > 1e-5). Boundary is non-strict:
   SCS = -5 exactly is Marginal — admitted, flagged for review. If |H(0)| ~ 0
   (below float64 amplification safety), SCS is undefined: QUARANTINE for manual
   review (do not auto-admit or auto-reject). The gate consumes the Stage-4
   metrics record when present and recomputes from raw data when absent.
   Per-trajectory metadata stored: eps_H, SCS, band label (Excellent <= -10;
   Acceptable (-10, -6]; Marginal (-6, -5]; Reject > -5).
   [Annotation: this clause TRANSCRIBES the locked post-v1.3 gate into an
   editable spec; its prior sole written home was the read-only research report
   data_quality_assessment.md (SI-DQA-003). It implements, and does not re-open,
   Hard Constraint 5.]
6. Grid-consistency checks (WARN level, not reject). Let dt_out be the record's
   resolved output interval (SPEC-3). Warn if max_i (t_{i+1} - t_i) > 1.5 * dt_out,
   or if snapshot_count < 0.9 * (final_timestep / dt_out + 1). Escalation of
   these warnings to quarantine is a Phase-24 decision (after DATA-06).

No absolute snapshot-count floor is imposed beyond condition 2. (A complete
standard-base run has ~ceil(9.5/0.17)+1 = 57 snapshots; floors such as ">= 200"
are arithmetically incompatible with the verified per-variant dt_out values.)
```

### SPEC-2 — ID-resolution contract (Step 1 item 7; consumed by Step 5)

**Target:** `ctl_instruction.md`, Step 1, appended as item 7 (after line ≈ 378); cross-reference from Step 5 "mapping from each simulation ID to stage index" (lines 1061–1068). **Implements:** Q-A2 (§3.2).

```
7. ID resolution (no dense-index assumption). Trajectory identity is the pair
   (variant, id) plus the folder (base|gold); id is the 4-digit zero-padded
   integer in the filename. At init, build id_to_path by SCANNING each of the
   four Brutus output folders; accept only filenames matching
       ^brutus_(hierarchical|standard)_(\d{4})\.txt$
   (folder name alone encodes gold status — filenames carry no _gold_ infix).
   Two files mapping to the same (variant, folder, id) = hard init error.
   Lookup of an absent id raises an explicit error; NO code path may compute a
   path arithmetically from an id or assume ids are contiguous, dense, or equal
   to an array index. All iteration over trajectories is over sorted
   (variant, folder, id) keys (deterministic order). Stage labels (Step 5) are
   keyed by (variant, folder, id), never by positional index. Init logs, per
   folder: files found, ids parsed, duplicates (must be 0), and the min/max id
   span versus the file count (gap visibility).
```

### SPEC-3 — Footer-handling and parameter-provenance contract

**Target:** `ctl_instruction.md`, Step 1 item 3 (replace lines ≈ 352–360) and §2.6 metadata list (amend lines ≈ 628–647). **Implements:** Q-A5 (§3.5). **Feeds:** §2.6 record metadata; SPEC-1 condition 6 (`dt_out`).

```
[Step 1 item 3 — replacement]
3. Footer handling. A Result: footer is OPTIONAL. If present, it carries the
   FULL parameter schema (tol, Lw, dt_out, t_end, eta, energies); parse all
   fields and mark each {param}_provenance = 'direct'. If absent (a verified
   population: 1,550 hierarchical-base / 701 standard-base / 219 standard-gold
   files), assign the folder-level defaults (CLM-09):
       standard base:      tol = 1e-13, Lw = 118, dt_out = 0.17
       hierarchical base:  tol = 1e-15, Lw = 130, dt_out = 0.08
       gold (both):        tol = 1e-13, Lw = 130, dt_out = 0.01
   and mark {param}_provenance = 'inferred'. eta has NO folder default: store
   null with provenance 'absent'. A footer that parses but lacks any full-schema
   field is an anomaly under the corrected record: flag footer_anomalous = true,
   fall back to defaults ('inferred'), and surface in the init log.
   Independently of the footer, MEASURE dt_out as the median timestamp spacing;
   store it with provenance 'measured' and WARN if it disagrees with the
   footer/default value by > 1%. Footers MUST NOT be used as completeness
   signals or for ID mapping (footer paths are environment-dependent).

[§2.6 — amendment]
Each processed record carries param_provenance: a map over
{brutus_tolerance, word_length, dt_out, eta} with values in
{'direct','inferred','absent','measured'} per the Step-1 item-3 contract.
The trustworthy_horizon field is RESERVED — definition pending (OI-2); writers
must emit null and readers must not consume it until defined.
```

### SPEC-4 — Processed-data storage contract

**Target:** `ctl_instruction.md`, Step 1 item 6 (replace lines ≈ 374–378). **Implements:** Q-A6 (§3.6).

```
6. Processed training data is stored in HDF5 (primary): one file per dataset
   build, groups /{variant}/{base|gold}/{id}, float64 datasets (t, q, v, m),
   per-group attributes carrying the §2.6 metadata (including param_provenance)
   plus a top-level schema_version and the build's transform metadata
   (scaling constants D, T, E_scale, r_char, Q_scale and their provenance), so
   raw values are exactly re-derivable. Chunked + compressed (gzip) storage is
   recommended. .npy/.npz is an ACCEPTABLE alternative for flat exports but the
   HDF5 file is the single source of truth. JSON/text exports are
   inspection-only and MUST NEVER be a training input path. Acceptance test:
   raw -> HDF5 -> arrays round-trips bit-identically in float64 against direct
   parsing for a sample of trajectories.
```

### SPEC-5 — Points-per-trajectory cap (Mini-Batch Construction amendment)

**Target:** `ctl_instruction.md`, "Mini-Batch Construction with Lookahead Sampling" (amend lines ≈ 1197–1210). **Implements:** Q-B1 (§4.1).

```
Per-trajectory data-loss point count:
    n_pts(traj) = min(n_pts_cap, n_snapshots(traj)),
sampled WITHOUT replacement from the trajectory's snapshot times.
n_pts_cap defaults to 32 (the spec's existing example value; not
evidence-based — revisit with Phase-24 DATA-06 snapshot distributions).
The 50/50 composition is realized as: k_w = floor(n_pts/2) snapshots drawn by
acceleration-norm-weighted sampling without replacement (Gumbel-top-k), then
n_pts - k_w drawn uniformly without replacement from the remainder; all draws
from a seeded generator (reproducible batches). The loader exposes
n_snapshots(traj) and dt_out(traj) as metadata (forward interface for the
deferred M16 collocation-density question — doc-03; not used here).
No 0.5 * n_snapshots factor is imposed (unevidenced; see resolution Q-B1).
```

### SPEC-6 — IC↔Brutus mass-consistency gate (§2.1 amendment)

**Target:** `ctl_instruction.md`, §2.1 (amend lines ≈ 397–413, extending the folded-in B-11 clause at 410–413). **Implements:** Q-B2 (§4.2).

```
IC<->Brutus t=0 mass gate (ALL pairs, at preprocessing — not a sample):
    max_i | m_IC,i - m_Brutus,i(t=0) | < 1e-15   (float64, ABSOLUTE; masses are
    O(1) with sum 3, so this is at the representation floor)
Implementations MUST set tolerances explicitly (e.g. np.allclose(..., rtol=0,
atol=1e-15)); library defaults (atol = 1e-8) silently mask failures and are
forbidden here. Escalation on failure: re-parse BOTH mass strings with
decimal.Decimal. If the decimal values are EQUAL, the discrepancy is a float64
parsing bug in the pipeline — fix the parser (do not quarantine the data). If
they DIFFER, the pair is genuinely inconsistent — QUARANTINE the trajectory
with reason code mass_ic_mismatch. (Rationale: identical source strings parse
to identical doubles; reals differing by <= 1 ulp differ by <~ 2.2e-16 << 1e-15
only at the boundary — a gate failure is therefore evidence of a real mismatch,
not rounding noise.) On pass, the IC-file masses are canonical for the IC13
vector. The mass-invariance-over-time gate of this section is unchanged.
```

### SPEC-7 — §2.5 fixes: `E_scale` floor; `compute_globals` regularization and scope

**Target:** `ctl_instruction.md`, §2.5 (one-token fix at line 608; normative notes appended to lines ≈ 576–611). **Implements:** Q-B4 (§4.4), F-2. **Locked context:** `D = (G·T²)^{1/3} ≈ 4.6416` (HC-6 / PHYS-01) is unchanged and remains the only admissible `D`.

```
[line 608 — replace]
    E_scale = |median(E)| + 1e-8
(canonicalizes the floor stated by Step 4 line 1049 and
pinn_architecture.md §5.2 line 761 — the network-facing contract; the prior
1e-10 here was an outlier, likely propagated from the adjacent eps_inv).

[appended normative notes]
- compute_globals evaluates per-IC energies with RAW masses and regularizes V
  with the PLUMMER form r_safe = sqrt(r^2 + eps_inv^2), eps_inv = 1e-10 — never
  an additive +eps on the distance norm (PHYS-03 anti-pattern; see lines
  698-704). D = (G*T^2)^(1/3) (≈ 4.6416 for G=1, T=10) per PHYS-01; the
  mass-fraction 6.694 form remains rejected.
- Scope: global statistics (E_scale, r_char, hence Q_scale = 0.5 * r_char) are
  computed over the ADMITTED set (post Step-1A, post blacklist). Medians make
  this nearly equivalent to all-files computation, but the admitted-set choice
  is deterministic, documented, and excludes corrupt records (minor judgment —
  OI-9).
```

### SPEC-8 — Data-side metric contracts: SASD, IPR, PSC (new subsection)

**Target:** `ctl_instruction.md`, new subsection inserted immediately before Step 4 (before line ≈ 1000), titled "Data-side quality-metric contracts (SASD, IPR, PSC)". **Implements:** Q-C2 (§5.2), Q-C3 (§5.3), Q-C4 (§5.4). SCS already lives in SPEC-1 condition 5. All thresholds below are provisional (OI-3); all run in float64 with validation softening `eps = 1e-10` (HC-4); units are stated explicitly (OI-4).

```
SASD (per snapshot interval i; dimensionless, scale-invariant):
    SASD_i = dt_i * max_{bodies b, endpoints t in {t_i, t_{i+1}}}
             ( ||a_b(t)|| / max(||v_b(t)||, 1e-12) )
with a_b ANALYTIC Newtonian gravity, Plummer eps = 1e-10 (never finite-
differenced from positions). Set v_floor_hit = true when the 1e-12 guard binds
(report; do not silently clip semantics). Trajectory score = max_i SASD_i.
FLAG (do not reject) trajectories with score > 0.5 (provisional — OI-3).
Endpoint evaluation cannot see interior spikes between snapshots — a labeled
judgment; IPR complements it. Disposition of flagged trajectories: if a gold
counterpart exists, the flag is SATISFIED by the gold sample; if not, the id
enters the resample queue (input to the OI-10 gold-regeneration decision).

IPR (per trajectory; units: raw G=1 acceleration squared — scaled units differ
by (T^2/D)^2 ≈ 464; the threshold below is in RAW units):
    Build the cubic Hermite interpolant with scipy
    CubicHermiteSpline(t, q, dydx=v) — the snapshot VELOCITIES are the slopes.
    (PchipInterpolator is NOT acceptable: its shape-derived slopes discard the
    data velocities and the residual would partly measure the slope estimator.)
    Evaluation points: per interval i, the 10 deterministic mid-offsets
    tau_{i,j} = t_i + (j - 1/2) * dt_i / 10, j = 1..10.
    IPR = (1/M) * sum over all tau, bodies, components of
          || q''_spline(tau) - a_grav(q_spline(tau)) ||^2,
    with a_grav using r_safe = sqrt(||dq||^2 + eps^2), eps = 1e-10.
    FLAG trajectories with IPR > 1e-3 (provisional, raw units — OI-3). Store
    the per-interval max residual as diagnostic metadata. (The eps = 1e-5
    variant of this quantity is the deferred training-side noise-floor role —
    doc-03; it is a DIFFERENT metric sharing the name and MUST NOT be compared
    against this gate.)

PSC (dataset-level, over the ADMITTED snapshot population; per variant and
pooled; report-only — NO reject gate):
    Per snapshot: sort the three pairwise distances d_min <= d_mid <= d_max;
    bin at (log10 d_min, log10 d_mid) on a FIXED grid over [1e-3, 1e2] per
    axis, 25 bins/axis (0.2 dex), K = 625; out-of-range values clamp to edge
    bins (provisional grid — OI-3). Estimator: plug-in p_k = n_k/N,
    H = -sum p_k ln p_k (nats); report H and H_norm = H / ln K in [0,1]
    (plug-in bias ~ -(K_occ - 1)/(2N): negligible at this N; Miller-Madow
    correction optional). Companion scalar: SCR = N(d_min < 0.5)/N (0.5 = the
    locked Stage-6 s_min boundary), report-only. Optionally store the
    per-snapshot bin index as metadata (interface for the deferred PSC-replay
    role — doc-03).
```

### SPEC-9 — `tab:brutus_compare` count correction (conditional on DATA-04)

**Target:** `ctl_instruction.md`, lines 23–29. **Implements:** F-1. **Condition:** apply only after Phase-24 DATA-04 confirms the folder counts (it transcribes dataset facts into spec text; the package's own rule is that Phase 24 owns on-disk truth).

```
| Set 1a | 4857 | Hierarchical (base) |
| Set 1b | 2749 | Standard (base)     |
| Set 2a | 4857 | Hierarchical (gold) |
| Set 2b | 2565 | Standard (gold)     |
| Total  | 15028 |                    |
(Corrects the transposed Set 1b / Set 2a values; the total is unchanged and
all four values now match the verified CLM-05/CLM-06 counts and the
dataset-context parameter-tuple sums.)
```

---

## 8. Open Items Register

Items this document surfaces but deliberately does not settle, with the owner that does. Nothing in this register blocks transcription of §7's spec blocks except where a block states its own condition (SPEC-9) or carries a `provisional` label (OI-3).

| ID | Item | Owner / phase | Surfaced in |
|----|------|---------------|-------------|
| OI-1 | `DELIVERY-NOTE.md` listed in the manifest but absent from the delivered package; confirm intent and whether its content touches anything in scope (on the master's own summary: it does not) | Package maintainer | §0.4, F-6 |
| OI-2 | `trustworthy_horizon` (§2.6 metadata field) is undefined anywhere in the package; define it or drop it — SPEC-3 marks it reserved meanwhile | Spec author | F-5, SPEC-3 |
| OI-3 | Provisional numerics pending Phase-24 distributions: SASD flag 0.5; IPR flag 1e-3 (raw units); PSC grid `[1e-3, 1e2]` × 25 bins/axis; `n_pts_cap` 32 | Phase 24 (DATA-06 + metric distributions) → spec author | Q-B1, Q-C2–C4, SPEC-5/8 |
| OI-4 | Metric unit statements (SASD dimensionless; IPR raw G=1 acceleration², ×≈464 vs scaled; PSC log₁₀ distance axes) must survive transcription into spec text verbatim — SPEC-8 carries them | Spec author | §5.2–5.4, SPEC-8 |
| OI-5 | WR-01: whether the issue doc's 1,000-vs-100 sample-size conflict receives its own CLM row (the operational question is dissolved by Q-B2's all-pairs gate; the documentary conflict remains) | Phase 24 user gate | Q-B2, F-3 |
| OI-6 | WR-04: whether CLM-05 is split into separate IC-folder and Brutus-output rows or amended in place | Phase 24 user gate | Master CLM-05 row note |
| OI-7 | CLM-01, CLM-02, CLM-10, CLM-11, CLM-12 remain `claimed-unverified`; the verdicts here that touch them are written to be robust to their failure, but Phase 24 must still run DATA-01/DATA-06 | Phase 24 | Q-A1, Q-A2, Q-B1 |
| OI-8 | Stage-conditional SCS tightening (e.g. a stricter gate for gold-resolution stages) is deferred until per-variant ε_H distributions exist; do not transcribe any tightened threshold now | Phase 24 → Phase 28 adjudication | Q-C1 |
| OI-9 | `compute_globals` scope (admitted set vs all files) — resolved here to admitted-set as a documented minor judgment; flag for explicit sign-off since the spec's original "all trajectories" predates the admission gate | Spec author sign-off | Q-B4, SPEC-7 |
| OI-10 | Gold-regeneration decision for the 184 gold-missing standard IDs; recommended selection input: gold-missing ∩ SASD-flag resample queue (a data-generation/resourcing decision, not a loader policy) | User gate | Q-A4, Q-C2 |
| OI-11 | Stage-label semantics ruling: this document reads stage labels as attaching to simulations `(variant, folder, id)`, not to bare IDs — the reading under which Q-A4 needs no fallback. If adjudication rules that labels attach to IDs, Q-A4 reverts to a Phase-26 STOP gap as the master anticipated | Phase 26 adjudication | Q-A4 |

---

## 9. References

### 9.1 Package files (all under the delivered package; commit hashes per the master's manifest; package-wide pin `96f9150a02919d492a86ef9f63e10e5942d2d8e3`)

1. `RESEARCH-CONTEXT-MASTER.md` — research-context entry point (manifest, framed questions, CLM register, consolidated dataset context, correction provenance). Generated package artifact, consolidated 2026-06-11.
2. `specs/02-data-pipeline-and-validation.md` — issue doc; NON-authoritative adjudication subject. Commit `d43afcd69af027e0689f42ac61e130f8497939f8`.
3. `specs/ctl_instruction.md` — framework spec; source of truth; spec-edit target. Commit `192c7c3c55ca0730c34ce708abf24c613234dd2e`.
4. `specs/pinn_architecture.md` — framework spec; source of truth; spec-edit target. Commit `192c7c3c55ca0730c34ce708abf24c613234dd2e`.
5. `specs/sampling_method.md` — FROZEN historical record of dataset generation (SCOPE-08). Commit `916d3f84ad7282c1f8ace45901441f7d3ac054ca`.
6. `specs/data_quality_assessment.md` — read-only research report (SCOPE-09); sole prior written home of the locked post-v1.3 SCS gate and the SASD/IPR/PSC definitions (SI-DQA-003). Commit `d3fcff99268b4493629eb2f0fe580f43c51ec019`.
7. `DELIVERY-NOTE.md` — listed in the manifest; **not delivered** (OI-1).

### 9.2 External literature

1. Boekholt, T. & Portegies Zwart, S. (2015). On the reliability of N-body simulations. *Computational Astrophysics and Cosmology* 2:2. DOI 10.1186/s40668-014-0005-3. (Brutus arbitrary-precision integrator; converged-digits framing used in Q-B3 and the F-5 discussion of a possible `trustworthy_horizon` reading.)
2. Portegies Zwart, S. & Boekholt, T. (2014). On the minimal accuracy required for simulating self-gravitating systems by means of direct N-body methods. *The Astrophysical Journal Letters* 785:L3. DOI 10.1088/2041-8205/785/1/L3. (Tolerance versus global trajectory accuracy in chaotic N-body systems — Q-B3's error-budget reasoning.)
3. Wang, S., Sankaran, S., & Perdikaris, P. (2024). Respecting causality for training physics-informed neural networks. *Computer Methods in Applied Mechanics and Engineering* 421:116813. DOI 10.1016/j.cma.2024.116813 (arXiv:2203.07404). (Causal-training context behind the dqa's causal firewall; motivates strict data-side admission — Q-A1, Q-C3.)
4. Fritsch, F. N. & Carlson, R. E. (1980). Monotone piecewise cubic interpolation. *SIAM Journal on Numerical Analysis* 17(2):238–246. DOI 10.1137/0717021. (Cited to *distinguish* PCHIP's shape-derived slopes from the Hermite-with-data-velocities construction the IPR requires — Q-C3.)
5. Goldberg, D. (1991). What every computer scientist should know about floating-point arithmetic. *ACM Computing Surveys* 23(1):5–48. DOI 10.1145/103162.103163. (float64 representation and rounding bounds behind the Q-B2 ulp argument and the Q-B3 noise-floor analysis.)
6. Paninski, L. (2003). Estimation of entropy and mutual information. *Neural Computation* 15(6):1191–1253. DOI 10.1162/089976603321780272. (Plug-in entropy-estimator bias regime supporting Q-C4's estimator choice.)

---

*End of resolution document. Prepared 2026-06-11 against the issue-02 research package pinned at `96f9150a…`; all line citations refer to the delivered snapshots. Phase 24 owns on-disk truth; Phases 25–28 own adjudication; this document owns the analysis in between.*
