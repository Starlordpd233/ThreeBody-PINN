# Issue-02 Final Resolution Document — Data Pipeline and Validation (Consolidated)

**Role:** Single, final candidate verdict source for Phase 25–28 adjudication, produced by critical re-adjudication of two independent final resolution documents against the issue-02 research package and the Phase-24 DATA-07 correction addendum.
**Date:** 2026-06-11
**Prepared by:** Final consolidation analyst. Reports were weighed on argument only; no position was adopted on authority, length, or vote.

## External Research Agent's Note on This Document:
Duplication detected — §5 onward appears twice. Inspecting the boundary to determine the exact duplicate span before fixing.The consolidated final resolution document is complete: 155 KB, all 14 questions (Q-A1–A6, Q-B1–B4, Q-C1–C4) resolved with the seven required parts each, plus the input inventory, §0 decision standard, §1 executive summary, §2 decision matrix, §6 cross-cutting findings F-1–F-9, Open Items OI-1–OI-12 with an Additional Input Needed register, and References.

A note on this session: the resumed write produced a duplicated §5-through-References block (an earlier append from the interrupted session landed alongside this session's reconstruction). I kept the earlier, more detailed version and removed the duplicate, then re-verified structure — 14/14 question headers, 14× each of the seven parts, single instances of every F and OI item, and locked-value spot checks (HC-5 gate, D ≈ 4.6416 with all 14 `6.694` mentions in rejection context, dual-ε usage).

Substantively, the things worth your attention rather than your trust:

**Four genuine forks between CR-A and CR-B were decided here, not inherited.** Q-B2 (absolute vs relative mass-gate form — low stakes, near-equivalent for O(1) masses); Q-C2 (both-endpoints vs left-endpoint SASD — a deliberate departure from the dqa's literal formula, flagged in the spec text for sign-off); **Q-C3 units (the consequential one** — raw vs scaled IPR differs by ×≈464 against the same 1e-3 gate; I adopted raw on placement inference and built a calibration tripwire into the spec text in case that inference is wrong); and Q-C4 (the dedup+weighting composition exists in *neither* input — it's a flagged synthesis with a four-way verification run specified to ratify or refute it empirically).

**Two items are this pass's own findings:** OI-12 (an internal transcription slip in the addendum's CLM-08 summary row — in the authoritative correction channel, so it needs a one-line erratum even though nothing depends on it) and the explicit record that the R1–R8 bundle was never provided to this pass, so every "R1–R8" claim is secondhand. [High confidence] on the structural checks and constraint compliance; [Medium confidence] on the fork decisions themselves, for the reasons stated inline in each question's part 4.

## Header — inventory of inputs received

| Input | Contents | Received |
|---|---|---|
| `RESEARCH-CONTEXT-MASTER.md` | Package entry point: Per-File Manifest (PKG-01), Framed Research Questions (PKG-02), CLM Claims Register (PKG-03), Consolidated Dataset Context (D-05), Correction Provenance | Yes |
| `specs-bundle.md` | Five delimited byte-intact snapshots: `02-data-pipeline-and-validation.md` (issue doc; non-authoritative adjudication subject), `ctl_instruction.md` (spec-edit target), `pinn_architecture.md` (spec-edit target), `data_quality_assessment.md` (read-only; sole written home of the locked SCS gate and the SASD/IPR/PSC definitions), `sampling_method.md` (FROZEN) | Yes — all five read; every load-bearing spec claim in this document was re-verified directly against these snapshots |
| Report **CR-A** — `FINAL-ISSUE-02-RESOLUTION.md` (~65 KB) | Independent final resolution document; itself a consolidation of the eight first-generation reports R1–R8 plus the package and the addendum (per its own input inventory) | Yes — read in full |
| Report **CR-B** — `issue-02-final-resolution.md` (~154 KB) | Independent final resolution document; itself a consolidation of R1–R8 plus the package and the addendum (per its own input inventory) | Yes — read in full |
| `DATA-07-CORRECTION-ADDENDUM.md` | Phase-24 CLM-keyed correction addendum; authoritative correction channel; supersedes the master's interim correction record for any claim it covers | **Yes — received up front; no updated version was forwarded mid-task** |
| First-generation reports **R1–R8** (`research-results-bundle.md`) | The eight original independent research reports | **No — not provided to this consolidation pass.** Both CR-A and CR-B state they received and read all eight. R1–R8 positions reach this document only secondhand: through the two consolidations' provenance sections and the task prompt's crosswalk (which is explicitly non-authoritative). All R1–R8 attributions below are marked as secondhand. |
| `DELIVERY-NOTE.md` | Handoff / gate context (D-16) | **No** — named in the master's manifest; not provided here, nor (per their inventories) to CR-A, CR-B, or R1–R4. No framed question depends on it (Open Item OI-1). |

**Structural note on this consolidation's inputs.** The task identifies "the two independent research reports — the two independent, final resolution documents" as the report inputs, while its crosswalk describes the eight first-generation reports R1–R8. The two documents actually received are second-generation: each is an independent consolidation of R1–R8, produced from the same package and the same addendum, following the same output contract this document follows. This document is therefore a re-adjudication of two consolidations. Three consequences: (i) the primary evidence (package, specs, addendum) was re-checked directly, never taken on either consolidation's word — every spec citation that carries a verdict below was re-verified against the snapshots in `specs-bundle.md`; (ii) agreement classification (Method step 2) is performed first-hand across CR-A/CR-B, and only secondhand for R1–R8; (iii) where CR-A and CR-B genuinely conflict, the conflict is adjudicated on the merits and the losing position is preserved as a dissent — nothing is averaged.

**Input asymmetry inherited from the first generation.** Both CR-A and CR-B report that none of the eight first-generation reports had the DATA-07 addendum, and that R6 worked from a truncated master lacking the framed questions, the CLM register, and the dataset context. Both consolidations already re-evaluated every addendum-dependent R-position per ground rule 3; this document re-checked those re-evaluations against the addendum directly.

---

## §0 Scope and decision standard

### §0.1 Coverage

This document re-adjudicates and answers every question in the master's "Framed Research Questions" section: Cluster A (Q-A1–Q-A6, Phase 26), Cluster B (Q-B1–Q-B4, Phase 27), Cluster C (Q-C1–Q-C4, Phase 28). Question identifiers and CLM identifiers are used verbatim as anchors.

### §0.2 Exclusions (Doc-03 scope boundary)

Per the master's scope boundary (SCOPE-11), the following are not answered and appear only as deferred forward-references: **M16** (`dt_out` collocation-density scaling), **G6** (causal-training Option A vs B), and the **training-loop usage** of SCS/SASD/IPR/PSC (SASD-weighted collocation, IPR-as-ALM-noise-floor, PSC-governed curriculum replay). Neither CR-A nor CR-B resolved an excluded topic; both record that first-generation report R6 answered M16 in full and both excluded that content. That exclusion is maintained here (Open Item OI-10). No content in this document widens the scope.

### §0.3 Evidence standard

Authority order applied, strictly:

1. **Hard Constraints HC-1–HC-6** (master, "Hard Constraints — Locked v1.4 Conventions") are fixed inputs. Verdicts entailed by them are labeled as such. No verdict re-opens one; recommendations conflicting with one are rejected, never softened to fit.
2. **The DATA-07 addendum** is the authoritative correction channel. Where it verifies or corrects a figure, that value governs; verdicts that would otherwise turn on a still-unverified figure are stated conditionally.
3. **Framework specs** (`ctl_instruction.md`, `pinn_architecture.md`) are the source of truth and the only spec-edit targets. `data_quality_assessment.md` (hereafter "dqa") is non-authoritative except as the sole written home of the locked post-v1.3 SCS gate (SI-DQA-003) and the only in-package SASD/IPR/PSC definitions; it is cited with that annotation. `sampling_method.md` is FROZEN history.
4. **The issue doc** (`02-data-pipeline-and-validation.md`) is the adjudication subject; its findings and Recommended Resolutions P1-1..P2-2 are candidate positions only.
5. **CR-A and CR-B are argued candidate positions, nothing more**; R1–R8 positions are secondhand candidate positions one further step removed. Agreement is not correctness; no question is decided by count. Live `pinn/` code is excluded (SCOPE-10) and cited nowhere.

**Direct re-verification performed for this pass** (so the skeptical reviewer need not trust either consolidation): the `ctl` §2.5 raw-mass derivation and explicit rejection of `D = 6.694`; the three `E_scale` floor statements (`ctl` §2.5 `+1e-10`; `ctl` Step-4 input table `+1e-8`; `pinn` §5.2 `+1e-8`); the `ctl` §2.1 absolute float64 `1e-15` mass-invariance gate and its folded-in IC↔Brutus consistency clause; the `ctl` §2.6 metadata schema including the undefined `trustworthy_horizon`; the `tab:brutus_compare` count transposition; Step-1 items 3/4/6 (optional footer; `dt_out` from timestamps or defaults; "HDF5 or NumPy (.npy)"); the Mini-Batch text "(e.g., 32) … 50% uniform … 50% weighted by acceleration norm"; the stage definitions (Stage 5 data source = Set 2b, criteria same as Stage 4; Stage 6 `s_min < 0.5` OR `|E| < 0.01`; cumulative replay; Step-5 "mapping from each simulation ID to its assigned stage index"); `pinn` §3.1 snapshot-sourced data points with `points_per_trajectory=32` as a code default; `pinn` §3.2/§3.4 `ε_train = 1e-5` and the training-side `ε_H = 1e-4·S_H`; the `ctl` Plummer `ε_inv = 1e-10` "only in V" rule and the additive-ε PHYS-03 anti-pattern text; the dqa §3.1–§3.4 metric texts, §5.1 Phase-1 gates, the band table with non-strict boundaries, the near-zero-`H(0)` rule, and SI-DQA-003; the issue doc's ratio thresholds, `compute_globals` listing (mass-fraction `D` with raw-mass energies and an additive `+eps`), P1-1..P2-2, the 1,000-vs-100 conflict (line-202-equivalent prose vs P2-2), and the checklist's `59→29` and `1000→128` rows; `sampling_method.md`'s prescreen `MIN_DISTANCE_THRESHOLD = 0.01`. Algebraic claims re-derived independently: `H' = D·H` under the locked scaling; SASD's exact raw/scaled invariance; the IPR raw-vs-scaled factor `(T²/D)² ≈ 464`; the `(1 − 70/15,028)^100 ≈ 63%` sample-miss probability; the cadence floors `57/120/951`; the DATA-05 quarantine count `(0005–0059) + (0061–0075) = 55 + 15 = 70`.

Confidence labels: **High** = entailed by a hard constraint, a framework spec, an addendum-verified fact, or first-principles arithmetic on such facts; **Medium** = contract well-supported but a parameter or empirical premise remains open; **Low** = the package under-determines the choice.

### §0.4 External literature

External citations are retained only where load-bearing and carried with their introduction chain (first-generation report → consolidation → here); this pass did not independently re-fetch them but confirms each is real and correctly characterized to the best of available knowledge. See References.

---

## §1 Executive decision summary

**Cluster A.** A trajectory **admission gate** runs at DataLoader initialization, between Stage-4 metrics and any training use. Its conditions: structural parse integrity (≥ 2 snapshots, exactly 3 body rows per snapshot, all values finite, strictly increasing timestamps); completeness `final_timestep >= 9.5` from parsed block times (never footer presence or line counts); the locked SCS gate; blacklist exclusion; the existing §2.1/§2.6 mass and COM/momentum gates; the DATA-05 quarantine of the 70 stale `brutus_hierarchical` outputs; and WARN-level grid-consistency checks. The issue doc's `snapshot_count >= 200` floor is rejected on verified arithmetic — the corrected medians (61 standard-base / 127 hierarchical-base / 1003 gold) mean it would reject both base populations in full (Q-A1). Trajectory identity is the scan-built pair (variant folder, zero-padded 4-digit ID) with a dual-key abstraction (`physical_key` for the IC, `record_key` for the on-disk realization); dense indexing is invalid, confirmed by DATA-01 (1,250 / 143 gaps) (Q-A2). Blacklist consumption is a blocking-grade, fail-closed loader precondition at IC level across base and gold, before stage assignment and global statistics; the count (65) is confirmed, consumption status remains Phase-25/FUT-01's question (Q-A3). For the 184 gold-less standard IDs, no fallback exists to choose under the locked stage definitions (Stage 5 is defined extensionally by the Set-2b gold data source; the base sample reaches late-stage training via cumulative replay); both issue-doc options are rejected as posed; the mandatory no-silent-substitution data contract is specified; the entailment's single defeater (whether stage labels attach to simulations or to IDs) and the Phase-26 STOP-gap trigger are preserved exactly, and the gold-rerun resourcing residue is routed to the user gate (Q-A4). Footers are all-or-nothing; absent footers take the verified folder defaults for `tol`, `Lw`, and `dt_out` under per-field provenance, with `eta = null/absent` and a `measured` cross-check channel for `dt_out` (Q-A5). HDF5 is the canonical processed store; `.npy/.npz` is a spec-compliant derived/secondary form; JSON/text is inspection-only; the methodology consequences are bitwise float64 round-tripping and transform-metadata auditability (Q-A6).

**Cluster B.** The per-trajectory data-loss point count is `n_pts = min(n_pts_cap, n_snapshots)` sampled without replacement, cap default 32 carried as the spec's example value and flagged non-evidence-based; the `0.5 × n_snapshots` factor is rejected as a normative rule (unevidenced; internally contradicted by the issue doc's own checklist; WR-03 confirms 32 was never a hard contract), and M12's BLOCKING infeasibility claim is wrong on verified arithmetic (Q-B1). The IC↔Brutus `t = 0` mass-consistency check is a full-population, every-trajectory admission condition — `max_i |Δm_i| < 1e-15`, float64 absolute, tolerances always explicit — with `decimal.Decimal` escalation only as a failure classifier; DATA-05 decides the coverage question empirically (the full scan found and enumerated 70 genuine base-hierarchical mismatches that are not a text-precision phenomenon; current ICs are canonical; the 70 outputs are quarantined pending rerun) (Q-B2). float64 is sufficient for every data-side validation metric; Decimal is mandated only as the Q-B2 classifier (Q-B3). The global scale is the locked raw-mass `D = (G·T²)^{1/3} ≈ 4.6416`; the `6.694` form, P1-7, and any `M_tot_ref` parameterization are rejected; the issue-doc `compute_globals` listing additionally carries a mixed-convention defect and the PHYS-03 additive-epsilon anti-pattern; the `E_scale` floor is canonicalized at `1e-8`; `compute_globals` runs over the admitted set (Q-B4).

**Cluster C.** SCS is the locked HC-5 contract verbatim — `ε_H = max_t |(H(t)−H(0))/H(0)|`, `SCS = log₁₀(ε_H)`, reject `SCS > −5` — with the Plummer validation softening `ε = 1e-10` in `V` (numerically inert at admitted separations), non-strict band boundaries, the `SCS = −5` tie ruled Marginal, `ε_H = 0 → SCS = −∞`, the near-zero-`H(0)` quarantine rule, raw/scaled invariance (`H' = D·H`), and the issue doc's ratio thresholds not transcribed (its `1e-6` is the Acceptable/Marginal band boundary mis-promoted to a gate; its `1e-8` is unsourced) (Q-C1). SASD is `SASD_i = Δt_i · max_{body, endpoint} ‖a‖ / max(‖v‖, 1e-12)` with analytic validation-ε accelerations evaluated at both interval endpoints, flag (not auto-reject) at `max_i > 0.5` provisional, a `v_floor_hit` flag, and a disposition rule routing flagged-and-gold-missing records to the resample queue feeding the Q-A4 user gate; the perpendicular form is an optional supplementary diagnostic only (blind to near-radial plunges) (Q-C2). IPR is built from per-component `CubicHermiteSpline(t, q, dydx=v)` — `PchipInterpolator` prohibited — at 10 deterministic mid-offset interior points per interval, residual against the analytic Plummer force at the **validation** `ε = 1e-10` (HC-4-entailed; the issue doc's `ε = 1e-5` is a different, doc-03 metric), aggregated as the mean squared stacked 9-component residual, units pinned to raw `G = 1` (scaled units read ×≈464 larger), flag `IPR > 1e-3` provisional (Q-C3). PSC is a dataset-level, report-only Shannon occupancy entropy over admitted snapshots on a fixed 2-D log grid of sorted **scaled** pair distances `(log₁₀ d_min, log₁₀ d_mid)` over `[1e-3, 1e2]`, 25 bins/axis, reported per (variant, fidelity) and on a deduplicated, equal-record-weighted pooled population (one record per `physical_key`, preferring gold; each record carries equal total weight) — the composition of the two consolidations' complementary confound fixes, flagged as a consolidator synthesis — with `H_norm = H/ln K`, the Miller–Madow term reported, the SCR companion (`d_min < 0.5`, matching the Stage-6 criterion in scaled units), and no reject gate (Q-C4).

**Cross-cutting.** Eight spec/package-hygiene findings are carried forward (§6), including the `tab:brutus_compare` count transposition (correction precondition now satisfied), the three-way `E_scale` conflict (resolved at `1e-8`), the issue-doc internal-defect catalog for EVID-10, the undefined `trustworthy_horizon` field (reserved), the CLM-10/CLM-11 probe-coverage gap over the 2,470 no-footer files (OI-6), and one new consolidator-original observation: the addendum's own CLM-08 summary-table row states "2,346 `tol=1e-13` standard-gold", which is internally inconsistent with the master's verified tuple histogram (1,754 at `1e-13` + 592 at `1e-14` = 2,346 *with-footer* files) and with the addendum's own "Not affected" clause; it is read as a transcription slip for "2,346 with-footer" (OI-12).

---

## §2 Decision matrix

Agreement classification (Method step 2) is performed first-hand across the two received reports, CR-A and CR-B. The "R1–R8 (secondhand)" note summarizes the first-generation picture as consistently reported by both consolidations; it is non-authoritative because R1–R8 were not provided to this pass.

| Question | Final verdict (one line) | Confidence | Agreement: CR-A vs CR-B | R1–R8 (secondhand) |
|---|---|---|---|---|
| Q-A1 (B-06) | Composite admission gate at DataLoader init: structural floor (≥2 snapshots, 3 body rows, finite, monotone) + `final_timestep >= 9.5` + locked SCS gate + blacklist + §2.1/§2.6 gates + DATA-05 quarantine + WARN-level grid checks; reject the `>= 200` floor (verified-fatal) | High | Unanimous in substance; CR-B's gate composition is a superset of CR-A's structural gate and is adopted | 7/8 reject `>= 200`; R6 adopted it (truncated input); R8's variant floors superseded by the addendum |
| Q-A2 (B-11) | Identity = (variant folder, zero-padded 4-digit ID); scan-built index, collision = hard error, explicit miss, sorted iteration; dual keys `physical_key`/`record_key`; never positional | High | Unanimous | Unanimous (8/8 in substance) |
| Q-A3 (M11) | Blacklist load at init: blocking-grade, fail-closed; IC-level exclusion across base and gold, before stage assignment and statistics; logged counts; batch-time assertion; count 65 confirmed, consumption status Phase-25/FUT-01 | High | Unanimous | Unanimous (8/8 in substance) |
| Q-A4 (M13) | No fallback exists under the locked stage definitions; both issue-doc options rejected as posed; mandatory no-silent-substitution contract; label-semantics defeater and Phase-26 STOP-gap trigger preserved; gold-rerun residue to the user gate | Medium | Unanimous on substance; CR-B's entailment-with-defeater framing adopted over CR-A's flat policy statement (closer to the master's "do not assert" annotation) | Fully split: entailment 3 (R1, R2, R4) / STOP-gap 4 (R3, R5, R7, R8) / Stage-5 low-fidelity fallback 1 (R6, rejected) |
| Q-A5 (D7) | Footers all-or-nothing; absent → verified folder defaults for `tol`, `Lw`, `dt_out` with per-field provenance ∈ {direct, inferred, absent, measured}; `eta = null/absent`; `measured` `dt_out` cross-check; footers never completeness or mapping signals | High | Unanimous; CR-B adds the `measured` channel and `trustworthy_horizon` reservation (adopted) | Unanimous on mechanism; split on provenance granularity (4 vs 4) and `Lw` (settled by addendum text) |
| Q-A6 (D-03) | HDF5 canonical store (`/{variant}/{fidelity}/{id}` groups, float64 datasets, provenance attrs, `schema_version`); `.npy/.npz` spec-compliant derived/secondary; JSON inspection-only; consequences: bitwise float64 round-trip + auditability | High | Unanimous; CR-B's layout/consequence clauses adopted | Unanimous among addressers (R6 unaddressed; R5 matrix-only) |
| Q-B1 (M12) | `n_pts = min(n_pts_cap, n_snapshots)` without replacement; cap default 32 (spec example, non-evidence-based, config knob); seeded weighted-then-uniform split; reject the `0.5 ×` factor and the BLOCKING infeasibility claim | High (form) / Medium (cap) | Unanimous | Split, minority adopted on merits by both consolidations: 0.5-factor 5 (R1, R3, R6, R7, R8) vs `min(cap, n)` 2 (R2, R4); R5 matrix-only |
| Q-B2 | Full-population IC↔Brutus `t=0` mass gate (~15,028 pairs): `max_i |Δm_i| < 1e-15` float64 **absolute**, tolerances explicit; Decimal only as failure classifier; ICs canonical; 70 base-hier outputs quarantined pending rerun (DATA-05) | High | Unanimous on coverage/escalation/quarantine; **genuine fork on gate form** — CR-B's absolute (`rtol=0, atol=1e-15`) adopted over CR-A's relative (`rtol=1e-15, atol=0`) for §2.1 consistency; near-equivalent in practice for these O(1) masses | Full scan 4 (R1–R4) vs sampled 2 (R7; R8 tier-1); R5 matrix-only; R6 unaddressed; addendum-decided |
| Q-B3 | float64 sufficient for all data-side metrics and invariants; Decimal only as the Q-B2 classifier; `H(0) ≈ 0` → undefined-SCS quarantine, never a denominator floor or higher precision | High | Unanimous | Unanimous among 7 addressers (R6 unaddressed) |
| Q-B4 | Locked raw-mass `D = (G·T²)^{1/3} ≈ 4.6416` (HC-6); reject `6.694`, P1-7, and `M_tot_ref` parameterization; fix the listing's mixed convention and additive-ε defect; `E_scale` floor = `1e-8`; admitted-set scope; CLM-13 ratification routed to EVID-10/PIPE-09 | High (constraint-entailed) | Unanimous on D; CR-B's verified spec-hygiene additions adopted (CR-A silent, not opposed) | Near-unanimous: 6 locked-D vs R8 parameterize-and-defer (rejected); R6 unaddressed |
| Q-C1 (SCS) | Locked HC-5 verbatim with operational completions: ε = 1e-10 Plummer in `H` (inert at admitted separations); non-strict bands; tie `SCS = −5` → Marginal; `ε_H = 0 → −∞`; near-zero-`H(0)` quarantine; `H' = D·H` invariance; ratio thresholds not transcribed; gate transcribed into editable `ctl` | High | Unanimous; CR-B's completions adopted (all dqa-textual or independently re-derived) | Unanimous among addressers; R6 outcome-consistent on stale citation |
| Q-C2 (SASD) | `SASD_i = Δt_i · max_{b, t∈{t_i, t_{i+1}}} ‖a_b‖/max(‖v_b‖, 1e-12)`, analytic ε = 1e-10 accelerations; flag (not reject) `max_i > 0.5` provisional; `v_floor_hit`; gold-aware disposition feeding Q-A4; perpendicular form supplementary only | Medium | Unanimous on family/threshold; **fork on endpoint evaluation** — CR-B's both-endpoints adopted over CR-A's literal left-endpoint (closes the final-snapshot blind spot; only raises `max SASD`) | Majority scalar + 0.5 flag; perpendicular-as-canonical 2 (R1, R2, demoted); system-norm aggregation (R8) rejected |
| Q-C3 (IPR) | `CubicHermiteSpline(t, q, dydx=v)` per component (PCHIP prohibited); 10 deterministic mid-offset interior points/interval; residual vs analytic Plummer force at ε = 1e-10 (HC-4-entailed); `IPR = (1/M_total) Σ ‖r_k‖²` stacked 9-vector; **raw G = 1 units** (scaled reads ×≈464 larger); flag `> 1e-3` provisional; `ε = 1e-5` variant re-housed as doc-03 `IPR_train` | High (ε, construction) / Medium (threshold, units, aggregation) | Unanimous on ε/construction/flag; **genuine fork on unit pinning** — CR-B's raw units adopted over CR-A's scaled/normalized-time units (a ×≈464 gate difference; raw matches the dqa Phase-1 on-load placement); evaluation-point spacing fork immaterial (mid-offset adopted) | ε = 1e-10: 6 of 7 addressers; R5's ε = 1e-5 rejected (HC-4 violation); construction split (Hermite-with-derivatives vs PCHIP-misnomer) |
| Q-C4 (PSC) | Dataset-level, report-only Shannon occupancy entropy on a fixed 2-D log grid of sorted **scaled** pair distances `(log₁₀ d_min, log₁₀ d_mid)`, `[1e-3, 1e2]`, 25 bins/axis (provisional); per-(variant, fidelity) unweighted + deduplicated equal-record-weighted pooled; `H_norm = H/ln K`; Miller–Madow reported; SCR companion (`d_min < 0.5`, scaled); no gate; invariant-space entropy optional secondary | Medium | Unanimous on family/grid/role; **fork on confound mechanism** — synthesis adopted: CR-B's dedup-prefer-gold composed with CR-A's equal-record weighting (complementary, not competing); `H_norm` denominator = full `ln K` (CR-B) over `K_eff` (CR-A); scaled-unit pinning made explicit (CR-A's, required by the SCR/Stage-6 anchor) | Fully split: five constructions across six addressers |

---

## §3 Cluster A — Ingestion & Selection (Phase 26)

> Provenance convention used in every part 7 below: **CR-A** = `FINAL-ISSUE-02-RESOLUTION.md`, **CR-B** = `issue-02-final-resolution.md` — the two independent consolidated reports received by this pass. Statements about R1–R8 are **secondhand** (reconstructed from the two consolidations' own provenance records, which broadly agree with each other and with the task prompt's crosswalk) and are non-authoritative: the original bundle was not provided to this pass (Open Items, "Additional Input Needed").

### §3.1 Q-A1 (B-06) — Stage 4 → Stage 5 validation gate

**1. Final verdict / recommendation.** Yes — a trajectory admission gate runs at DataLoader initialization, between Stage-4 metric generation and any training use (stage assignment, `compute_globals`, batch construction). A record `(variant, fidelity, id)` is admitted iff **all** of the following hold; every rejection/quarantine is logged `(variant, id, reason_code)`, and per-variant admitted/rejected/quarantined counts are logged at init:

1. **Identity & blacklist** — the ID resolves per the Q-A2 contract; blacklisted `(variant, id)` pairs are excluded from both base and gold per Q-A3, before stage assignment and before `compute_globals`. Missing blacklist file = hard init failure; a batch-time assertion re-checks emitted samples.
2. **DATA-05 quarantine** — the 70 `brutus_hierarchical` base outputs (IDs `0005`–`0059`, `0061`–`0075`) are excluded from training, metrics aggregation, and PIPE-07 use until rerun validation from the current canonical ICs passes (addendum, RESOLVED-WITH-INSTRUCTION 2026-06-11). The quarantine list is configuration, not code.
3. **Structural integrity** — the file parses into complete snapshot blocks; exactly 3 body rows per snapshot; all masses, positions, velocities, timestamps finite; timestamps strictly increasing; `n_snapshots >= 2` uniformly (the issue doc's "`>= 2` for Stage 0–3 only" stage-tiering is dropped; the completeness condition dominates it anyway).
4. **Completeness** — `final_timestep >= 9.5`, computed as the maximum parsed snapshot-block time via the README header pattern; never from footer text, footer presence, or line counts (the README's two explicit prohibitions).
5. **Conservation gate (locked HC-5; full definition Q-C1)** — reject if `ε_H > 1e-5` (equivalently `SCS > −5`); `|H(0)|` numerically near zero ⇒ SCS undefined ⇒ quarantine for manual review. Consumes the Stage-4 metrics record when present; recomputes per the HC-5 definition when absent/unparseable.
6. **Physical invariant gates** — the `ctl` §2.1 mass-invariance gate (`max_{t,i} |m_i(t) − m_i(0)| < 1e-15`, float64 absolute), the Q-B2 IC↔Brutus `t = 0` mass gate, and the §2.6 COM/momentum assertions apply as admission criteria with their existing reject/quarantine semantics.
7. **Grid-consistency checks (WARN, not reject)** — with `dt_out` the record's resolved output interval (Q-A5): warn if `max_i (t_{i+1} − t_i) > 1.5 × dt_out` or if `n_snapshots < 0.9 × (final_timestep / dt_out + 1)`. Escalation to reject is conditional on characterizing the no-footer populations' snapshot distributions (OI-6).

**The issue doc's `snapshot_count >= 200` floor (P1-1) is rejected.** No absolute snapshot-count floor above 2 is imposed.

**2. Reasoning.** Three package facts fix necessity and placement: `calculate_metrics.py` performs no completeness checks and processes every file (master, SCOPE-07 excerpt); the README designates `final_timestep >= 9.5` as the primary completeness check and forbids footer-presence/line-count proxies; and the locked SCS gate was ratified for exactly this screening position (dqa §5.1 runs it on load), with dqa §4.1's causal-firewall analysis explaining why one bad admitted trajectory is disproportionately harmful. The `>= 200` floor was rejectable from verified cadence arithmetic alone (`dt_out = 0.17` and the 9.5 rule imply complete standard-base runs of ~57–61 snapshots); the addendum makes the rejection empirical: corrected CLM-10 medians are 61 (standard base; min 59, max 61) and 127 (hierarchical base; 126–127), so the floor rejects one hundred percent of both base populations — the populations the locked stratification assigns to Stages 3–4. The floor conflates per-file *validity* with curriculum *membership*. CLM-11 prevalence is verified at 1.000 across the *probe-applicable* population — so the 9.5 gate is currently non-binding in practice, but stays mandatory as the catch for future partial runs, and "probe-applicable" is an uncharacterized qualifier (OI-6). The cadence floor `n_snapshots >= 1 + ceil(9.5/dt_nom)` (57/120/951) is arithmetically sound; it is retained at WARN level (clause 7's 0.9-slack form) rather than promoted to reject solely because the addendum's per-variant `n` values coincide exactly with the footer-bearing counts and therefore may not characterize the 2,470 no-footer files.

**3. Evidence.** Master: Q-A1 block; Completeness Checks fragment (regex; "Do NOT rely on" footer/line counts); `calculate_metrics.py` SCOPE-07 excerpt; CLM-09/10/11 rows. Addendum: Correction 3 (CLM-10 medians 61/127/1003 with min/max); Confirmed-Claims table (CLM-09; CLM-11 prevalence 1.000 "probe-applicable"); DATA-05 section (70-ID quarantine). Specs: `ctl_instruction.md` Step 1 item 3 (graceful `< 2`-snapshot handling), §2.1, §2.6; `data_quality_assessment.md` §5.1, §4.1, lines 119–130 — annotated: locked post-v1.3 (SI-DQA-003); sole written home is a read-only research report. Issue doc: lines 57, 74, 283 (P1-1), 337–348, 357. All spec line citations re-verified directly against the snapshots by this pass (§0.3).

**4. Confidence.** High. The single factor most likely to change the verdict: characterization of the no-footer populations' snapshot distributions (OI-6) — matching distributions would justify escalating clause 7 to a hard cadence floor; materially irregular ones would require a variant-aware expected-count design.

**5. Verification suggestion.** Extend the DATA-06 probe to the no-footer files explicitly; publish per-variant `final_timestep`, `n_snapshots`, `max Δt / dt_out` distributions split by footer presence. Unit tests: truncated-at-`t=5` file rejects (`completeness`); 1-snapshot file rejects (`structure`); injected `ε_H = 2e-5` rejects (`scs_gate`); interior gap of `3 × dt_out` admits with `grid_irregular`; `brutus_hierarchical` ID `0005` quarantines (`data05_stale`); a complete 59-snapshot standard-base file **admits**.

**6. Proposed specification text.** Target: `ctl_instruction.md`, new "Step 1A — Trajectory Admission Gate" inserted immediately after Step 1's item list, before Step 2:

```
Step 1A — Trajectory Admission Gate (data-side; runs at DataLoader init)

Every (variant, fidelity, id) trajectory must pass ALL conditions below before it
may enter stage assignment (Step 5), global-statistics computation
(compute_globals, §2.5), or any training batch. Failures are recorded
per-trajectory with a reason code; the loader logs admitted/rejected/quarantined
counts per folder at init.

1. Identity & blacklist. The id resolves via the Step-1 ID-resolution contract.
   (variant, id) pairs present in problematic_ics_blacklist.json are excluded
   from BOTH the base and gold folders of that variant, before stage assignment
   and before compute_globals. Missing blacklist file = hard init failure. A
   batch-time assertion re-checks emitted samples.
2. Data-remediation quarantine. The 70 brutus_hierarchical outputs flagged by
   DATA-05 (ids 0005-0059, 0061-0075) are quarantined from training, metrics,
   and PIPE-07 use until rerun validation from the current canonical ICs passes.
   The quarantine list is configuration, not code.
3. Structural integrity. >= 2 parsed snapshots; exactly 3 body rows per
   snapshot; all values finite; timestamps strictly monotone increasing.
4. Completeness. final_timestep >= 9.5, computed from parsed snapshot block
   times. Footer presence, line counts, and snapshot-count constants MUST NOT
   be used as completeness signals.
5. Conservation gate (locked post-v1.3; SI-DQA-003). With H evaluated in
   float64 using Plummer softening eps = 1e-10 in V:
       eps_H = max_t |(H(t) - H(0)) / H(0)|,   SCS = log10(eps_H)
   REJECT if SCS > -5 (equivalently eps_H > 1e-5). SCS = -5 exactly is
   Marginal: admitted, flagged for review. If |H(0)| is numerically near zero,
   SCS is undefined: QUARANTINE for manual review. Store per-trajectory eps_H,
   SCS, and band label (Excellent <= -10; Acceptable (-10,-6]; Marginal
   (-6,-5]; Reject > -5). [This clause TRANSCRIBES the locked gate into an
   editable spec; it implements, and does not re-open, Hard Constraint 5.]
6. Physical invariant gates. The Step-2/§2.1 gates apply as admission criteria:
   mass invariance max_{t,i}|m_i(t) - m_i(0)| < 1e-15 (float64, absolute); the
   IC<->Brutus t=0 mass gate (§2.1 as amended per Q-B2); the COM/momentum
   assertions with their existing reject/quarantine semantics.
7. Grid-consistency checks (WARN level, not reject). With dt_out the record's
   resolved output interval: warn if max_i (t_{i+1} - t_i) > 1.5 * dt_out, or
   if n_snapshots < 0.9 * (final_timestep / dt_out + 1). Escalation to reject
   is conditional on characterizing the no-footer populations' snapshot
   distributions.

No absolute snapshot-count floor is imposed beyond condition 3. (Verified
medians: 61 standard-base / 127 hierarchical-base / 1003 gold; floors such as
">= 200" are arithmetically incompatible with the base populations.)
```

**7. Consolidation provenance.** **CR-A:** structural gate only (parse success, finite, monotone, `N_t >= 2`, 9.5; footer irrelevant; `>= 200` rejected), with the SCS/blacklist/mass/DATA-05 screens deliberately housed under their own questions. **CR-B:** the same structural core *plus* the composite enforcement framing — SCS gate, blacklist, §2.1/§2.6 gates, DATA-05 quarantine, and WARN-level grid checks as explicit gate clauses with reason codes and ordering before statistics. **Decision: CR-B's composition adopted.** The two are not in conflict — CR-A's gate is a strict subset and its own §1 routes the remaining screens to Q-A3/Q-B2/Q-C1 — but the output contract demands a transcription-level gate a spec author can apply without cross-referencing four sections, and CR-B's single enforcement point also fixes *ordering* (before `compute_globals`), which CR-A leaves implicit. Both reject `>= 200` on the same addendum arithmetic; both keep the cadence check at WARN with escalation conditional on OI-6 — that WARN-vs-reject choice is the live judgment call here, and it is preserved as conditional rather than resolved. Secondhand R1–R8 picture (non-authoritative): 7/8 rejected `>= 200`; R6 adopted the floor on truncated input (rejected by both consolidations); R8's variant-specific `N_min` floors were superseded by the addendum's tight min/max spreads; R2 alone wanted the cadence floor as a hard reject (the dissent the conditional escalation preserves).

### §3.2 Q-A2 (B-11) — Non-contiguous IDs (ID ≠ array index)

**1. Final verdict / recommendation.** Trajectory identity is `(variant_folder, zero-padded 4-digit numeric ID)`; the folder is the sole authority for variant and gold status (Correction 1: zero `_gold_` filename matches in 4,857 + 2,565 probes). The mapping contract:

1. At DataLoader init, build `id_to_path[variant][fidelity][id]` by **scanning** the four Brutus output folders, accepting only filenames matching `^brutus_(hierarchical|standard)_(\d{4})\.txt$` (anchored; non-matching files logged and ignored).
2. IDs normalize to `int` internally, format `%04d` at path boundaries; a duplicate `(variant, fidelity, id)` within a folder is a hard init error.
3. Lookup of an absent key raises an explicit miss; no positional fallback, no `paths[id]` array indexing, no density/contiguity/zero-base assumption.
4. Deterministic iteration (stage assignment, statistics, exports) goes over **sorted present keys**, never `range(n_files)`.
5. Two key levels: `physical_key = (family, id)` for the physical IC (blacklist semantics, gold availability, IC-granularity labels) and `record_key = (family, fidelity, id)` for one on-disk realization (file lookup, per-record metadata). Base↔gold joins succeed only when both exact `record_key`s exist.
6. `Result:`-footer paths are never used for mapping.
7. Init logs per folder: files found, IDs parsed, duplicates (must be 0), min/max ID span vs file count (gap visibility).

The issue doc's P1-2 (`id_to_path` / `TrajectoryIndex`) is accepted in substance; this verdict pins what P1-2 leaves open.

**2. Reasoning.** The contract was provable before the addendum: the verified CLM-04 list contains ID `3958` while the verified standard-base count is 2,749, so the standard ID space cannot be dense — dense indexing mis-addresses some trajectories with certainty. The addendum confirms magnitudes: CLM-01 (1,250 gaps / 2,749 files) and CLM-02 (143 / 4,857) confirmed; CLM-12 nominal counts confirmed via max IDs 3,998/4,999 — roughly one in three standard lookups would be wrong under dense indexing. Gaps are intentional (generation continuation, prescreen rejection, failed runs), so no re-densification should be designed for. The dual-key abstraction is retained because three downstream contracts genuinely operate at IC granularity (blacklist, gold availability, the byte-identical gold⊂base IC subset) while file access operates at realization granularity; a single integer-keyed dictionary under-specifies both.

**3. Evidence.** Master: Q-A2 block; File Naming Conventions fragment ("The numeric ID is NOT an index; gaps exist"); CLM-01/02/04/05/12 rows; CLM-04 ID list (max 3958). Addendum: CLM-01/02/04/05a/05b/06/12 all confirmed; Correction 1 re-probed and confirmed. Specs: `ctl_instruction.md` Step 5 (stage map = "a mapping from each simulation ID to its assigned stage index" — ID-keyed already; verified at line 1068). Issue doc: lines 58, 284, 314–318, 356, 361.

**4. Confidence.** High; unconditional. The only modifying (not overturning) factor: IDs violating the 4-digit pattern in a future extension, which widens the regex and nothing else.

**5. Verification suggestion.** Property test on the standard base folder: `max(parsed IDs) >= file_count` (must hold given CLM-04/05). Unit tests: ten CLM-04 IDs raise explicit misses against the gold folder and resolve against base; a planted duplicate triggers the init error; `get(physical_key)` for a base-only ID reports gold absent rather than erroring.

**6. Proposed specification text.** Target: `ctl_instruction.md`, Step 1, appended item (cross-referenced from Step 5):

```
ID resolution (no dense-index assumption). Trajectory identity is
record_key = (variant, fidelity, id); the physical IC is
physical_key = (variant, id); id is the 4-digit zero-padded integer in the
filename. At init, build id_to_path by SCANNING each of the four Brutus output
folders; accept only filenames matching ^brutus_(hierarchical|standard)_(\d{4})\.txt$
(folder name alone encodes gold status — filenames carry no _gold_ infix). Two
files mapping to the same record_key = hard init error. Lookup of an absent key
raises an explicit error; NO code path may compute a path arithmetically from
an id or assume ids are contiguous, dense, or equal to an array index. All
deterministic iteration is over sorted record_keys. Stage labels (Step 5) are
keyed by record_key, never by positional index. Blacklist and gold-availability
semantics attach to physical_key and apply to every record_key beneath it.
Result: footer paths are never used for mapping. Init logs, per folder: files
found, ids parsed, duplicates (must be 0), and min/max id span vs file count.
```

**7. Consolidation provenance.** **CR-A:** scan-built `TrajectoryIndex`, `ic_key`/`traj_key` dual keys, folder-encoded fidelity, no positional identity. **CR-B:** identical contract with the operational details pinned — anchored regex, `%04d` normalization, collision/miss semantics, sorted iteration, init logging. **Decision: unanimous in substance; CR-B's mechanism-complete statement adopted, CR-A's key names normalized to `physical_key`/`record_key`** (the names CR-B uses and Q-A3/Q-A4 reference; pure terminology, no content difference). Secondhand R1–R8 picture (non-authoritative): both consolidations report 8/8 substantive unanimity, with R4 contributing the mechanism backbone and R1/R2/R3 the dual-key abstraction. No dissent recorded anywhere.

### §3.3 Q-A3 (M11) — Blacklist loading / consumption

**1. Final verdict / recommendation.** Blacklist consumption is a **blocking-grade, fail-closed precondition** for any training run:

1. **Load** `problematic_ics_blacklist.json` at DataLoader init, before stage assignment and before any dataset-wide statistic (`compute_globals` included).
2. **Validate schema:** top-level JSON object with exactly the keys `hierarchical` and `standard`, each a list of integer-like IDs; anything else is a hard configuration error. Normalize to `int` (the `%04d` boundary per Q-A2); deduplicate within family.
3. **Exclusion is IC-level:** a listed `(family, id)` excludes **every** realization — base and gold — of that `physical_key`. (Gold ICs are a byte-identical subset of base ICs; a problematic IC is problematic at every fidelity.)
4. **Missing, unreadable, or schema-invalid blacklist = hard init failure.** Absence is a configuration error, not an empty blacklist. Any override must be an explicit, logged, development-only flag.
5. **Logging:** per family — `n_blacklist_entries`, `n_present_on_disk` per fidelity, `n_excluded`. A listed ID absent from disk is logged, not fatal. The issue doc checklist's "exactly 65 excluded IDs" is re-keyed to assert against the parsed file content of the run, never a hard-coded 65.
6. **Defense in depth:** set-membership assertion at batch assembly; a blacklisted sample in an emitted batch raises a hard error (it indicates a bypass path — exactly the M11 failure mode).

The count (CLM-03: 65 = 2 hierarchical + 63 standard) is addendum-confirmed. The *consumption status of current code* is asserted nowhere in this document: the addendum marks it `unverified — outside grounding limits (SCOPE-10)`, routed to Phase 25 / FUT-01.

**2. Reasoning.** The spec is silent on consumption, so the contract is built from the artifact's structure and pipeline invariants. IC-level exclusion follows from the verified byte-identical-subset relationship — excluding one fidelity readmits the same problematic dynamics through the other. Before-statistics ordering prevents blacklisted records from contaminating normalizers (medians dampen but do not eliminate the effect; NaN-poisoned records would dominate). Fail-closed follows from the exclusion property being a *guarantee*: a loader that silently proceeds without the blacklist cannot certify the property M11 exists to enforce. Architectural-harm narratives (causal-firewall spikes; LayerNorm/SIREN saturation) are plausible motivation but not load-bearing; the contract stands on data integrity alone.

**3. Evidence.** Master: Q-A3 block; CLM-03 row + note (count observable; consumption Phase-24-owned); Blacklist Summary fragment (JSON shape); gold-IC byte-identical-subset fragment. Addendum: CLM-03 confirmed (65 = 2 + 63, `probes/data02_blacklist.py`); "PENDING — M11" (consumption unverified, SCOPE-10; Phase 25 / FUT-01). Specs: dqa §5.1 (gate-before-analysis ordering rationale). Issue doc: lines 59, 76, 285 (P1-3), 297, 341.

**4. Confidence.** High on the contract. The single factor most likely to change it: DATA-02-style schema findings (extra keys, string IDs, nesting), which adjust clause 2's validation and nothing else. Whether M11's MAJOR→BLOCKING reclassification stands is EVID-10's call; this document asserts only that the *contract* is blocking-grade.

**5. Verification suggestion.** Phase-25/FUT-01: probe the live loader (does a blacklisted ID appear in any emitted batch across an exhaustive stage iteration?). Unit tests: init fails on absent file; fails on a third top-level key; a listed ID present in both folders never appears in any manifest or batch; the batch-time assertion trips when exclusion is deliberately disabled; a listed-but-absent-on-disk ID logs and proceeds.

**6. Proposed specification text.** Carried inside the Step 1A gate (clause 1 of Q-A1's text) plus this loader-contract note in `ctl_instruction.md`:

```
Blacklist semantics attach to physical_key and exclude every record_key beneath
it. A missing or malformed problematic_ics_blacklist.json is a fatal
configuration error unless an explicit, logged development-only override is
set. Exclusion executes before stage assignment and before any dataset-wide
statistic. Exclusion counts are logged per family and fidelity; expected counts
are asserted against the parsed file content of the run, never hard-coded.
```

**7. Consolidation provenance.** **CR-A:** mandatory fail-closed load at init, `ic_key` granularity across fidelities, schema validation, normalization, exclusion-count persistence, batch assertion, explicit override only. **CR-B:** the same six-clause contract with two additions — the before-statistics ordering made explicit, and the checklist's hard-coded 65 re-keyed to file content. **Decision: unanimous; CR-B's two additions adopted** (the ordering clause is load-bearing for `compute_globals` correctness; the re-keying removes a brittleness both consolidations flag). Secondhand R1–R8 picture (non-authoritative): 8/8 substantive unanimity per both consolidations; R5's "silently exclude" wording was rejected by both as infelicitous (exclusions must be logged); R6's architectural rationale carried as motivation only. No dissent on substance.

### §3.4 Q-A4 (M13) — 184 standard IDs without a gold counterpart (fallback policy)

**1. Final verdict / recommendation.** Per the master's annotation, no fallback is asserted. The consolidated finding: **under the locked stage definitions there is no fallback to choose** — the spec's own semantics determine the behavior, and both issue-doc options presuppose a per-ID Stage-5 obligation the spec does not create.

- **What the locked text entails.** Stage 5's data source is Set 2b (gold standard) with criteria "same as Stage 4"; stage labels are assigned per simulation (`ctl` Step 5: "a mapping from each simulation ID to its assigned stage index"); each stage's training set includes all prior-stage data (cumulative replay). A standard ID with no gold counterpart has exactly one simulation — its base run — which receives its own stage label from its own invariants and **persists into Stage-5/6 training sets via replay**. "No Stage-5 sample for that ID" is the spec applied, not a policy gap.
- **Option 2 (flagged low-fidelity sample admitted into Stage 5) — rejected as posed:** contradicts Stage 5's data-source definition and double-counts (the base sample already reaches the Stage-5 training set through replay; re-admitting it as a Stage-5 *member* changes stratum composition for no informational gain).
- **Option 1 ("skip to Stage 6") — rejected as phrased, vacuous in substance:** nothing skips; the base simulation's label is unchanged, Stage 6 remains criteria-based (`s_min < 0.5` or `|E| < 0.01`), and the ID's data reaches Stage-6 training through replay like every admitted sample.
- **Mandatory data-side contract (adopted unconditionally):** (i) compute the gold-missing set at init as the set difference of scanned base and gold ID sets, cross-checked against the verified CLM-04 184-ID list with discrepancies logged — never hard-coded; (ii) per-`physical_key` metadata `gold_counterpart ∈ {present, absent}`; (iii) build the Stage-5 stratum by iterating the **gold folder's actual files**, never by base-ID lookup into the gold index (which manufactures 184 spurious misses by construction); (iv) never silently substitute a base-fidelity record into a gold-resolution slot.
- **STOP-gap trigger (preserved exactly):** the entailment rests on stage labels attaching to *simulations* (`record_key`). **If** Phase-26 adjudication rules that labels attach to *IDs* and every Stage-4 ID must yield a Stage-5 sample, the no-fallback reading fails, neither issue-doc option is spec-derivable, and Q-A4 must surface as the Phase-26 STOP gap — not be resolved by invention.
- **Genuinely open residue, routed to the user gate:** whether the project *wants* gold coverage for any of the 184 ICs — a re-simulation/resourcing decision outside loader policy. Principled selection input: the intersection of the gold-missing set with the SASD resample queue (Q-C2), which identifies exactly the gold-less trajectories whose base resolution is demonstrably insufficient.

**2. Reasoning.** The master instructs "do not assert a fallback here" and flags STOP-gap status *if the sources are silent or conflicting*. Read at the right granularity they are neither: the issue doc frames M13 as a hole only by implicitly treating Stage 5 as a per-ID obligation, while the locked stratification defines Stage 5 extensionally by data source. The verified figures (CLM-04 = 184; CLM-05b: base 2,749 / gold 2,565 / difference 184; hierarchical 4,857 = 4,857, no gap) size the issue without altering the logic. The defeater is genuinely live — `ctl` Step 5's phrase "each simulation ID" is the textual hinge, and "simulation" vs "ID" readings diverge exactly here — which is why this verdict states the entailment *with* its defeater and trigger rather than as settled doctrine, and why confidence is Medium.

**3. Evidence.** Master: Q-A4 block with the STOP-gap annotation; CLM-04/05 rows; standard-IDs-not-in-gold fragment (byte-identical subset; 184-ID list). Addendum: CLM-04 confirmed ("doc list matches set exactly"); CLM-05a/b confirmed. Specs: `ctl_instruction.md` Multi-Stage Data Stratification (Stage 5 = Set 2b, criteria same as Stage 4; Stage 6 `s_min < 0.5` or `|E| < 0.01`; cumulative replay verbatim — all re-verified by this pass), Step 5 line 1068. Issue doc: lines 65, 82, 287 (P1-5), 299, 316, 342.

**4. Confidence.** Medium. High that the no-fallback reading follows from the spec text as written; Medium overall because of the single named defeater — a downstream ruling that stage labels attach to IDs rather than simulations — which voids the entailment and activates the STOP gap. **This is the question on which the project should most expect to consult the original R1–R8 reports** (their three-way split was genuine; see part 7 and the Open Items register).

**5. Verification suggestion.** Obtain a one-line framework-owner ruling on Step-5 label semantics (simulations vs IDs) — it closes the conditional either way. Re-verify the gold-missing set by set difference (DATA-03 already did). Unit test: Stage-5 stratum construction over a fixture containing a gold-less ID emits zero misses, and that ID's base sample appears in the Stage-5 training set via replay exactly once.

**6. Proposed specification text.** Target: `ctl_instruction.md`, note under the Step-5 stage-assignment paragraph (conditional on the label-semantics ruling; if the ruling goes the other way, replace with a STOP-gap marker):

```
Stage labels attach to simulations (record_key). The Stage-5 stratum is built
by iterating the gold folders' actual files; base-fidelity records MUST NOT be
substituted into gold-resolution slots, and no base record is re-labeled or
re-mapped because its gold counterpart is absent. A standard physical_key with
no gold record keeps its base record in its originally assigned stage lineage,
is marked gold_counterpart = absent, and reaches later-stage training sets
through ordinary curriculum replay. Stage 6 remains criteria-based and is never
a missing-gold fallback bucket. The gold-missing set is computed at init by set
difference of the scanned base and gold ID sets and cross-checked against the
CLM-04 list (discrepancies logged; list never hard-coded). Whether to
commission gold re-simulation for any of these ICs is a user-gate resourcing
decision; the recommended selection input is the intersection of the
gold-missing set with the SASD resample queue.
```

**7. Consolidation provenance.** **CR-A:** flat policy statement — no synthetic fallback; base sample remains in its low-fidelity stage/replay lineage with `gold_available=false`; rerun commissioning surfaced as a separate open resourcing question. **CR-B:** the same operative behavior, derived as a *spec entailment* with the rejection of both options argued (double-counting; vacuity), the label-semantics defeater named, the STOP trigger preserved verbatim, the gold-folder-driven stratum-construction rule (the latent bug class), and the SASD-intersection selection input for the rerun residue. **Decision: CR-B's entailment-with-defeater framing adopted.** Reason: the master's annotation says "do not assert a fallback"; CR-A's framing *asserts a policy* (the right one, but as policy), while CR-B's shows the behavior is entailed by locked text, names the one premise under which it fails, and hands the trigger downstream — which is the closer fit to the annotation and the more honest epistemic posture. CR-A's `gold_available=false` flag is the same metadata as CR-B's `gold_counterpart`; merged. Secondhand R1–R8 picture (non-authoritative, and material here): genuinely fully split — entailment reading 3 (R1, R2, R4), STOP-gap declaration 4 (R3, R5, R7, R8), low-fidelity-fallback 1 (R6, rejected by both consolidations as contradicting the locked Stage-5 data source). R8's "Policy C" was ambiguous between the entailment and a replay-rule change; both consolidations record the ambiguity unresolved. Dissents preserved: R6 (pro-fallback), the four STOP-gap reports (honored through the explicit trigger).

### §3.5 Q-A5 (D7) — Footer / parameter heterogeneity

**1. Final verdict / recommendation.** The footer-handling contract, per Brutus output file:

1. **Footer present →** parse the full schema `(tol, Lw, dt_out, t_end, eta, energies)`; record each field with provenance `direct`. Under the corrected disk facts, presence implies the full schema.
2. **Footer absent** (verified populations: 1,550 hierarchical-base, 701 standard-base, 219 standard-gold) **→** assign the verified folder defaults — standard base `tol = 1e-13, Lw = 118, dt_out = 0.17`; hierarchical base `tol = 1e-15, Lw = 130, dt_out = 0.08`; gold (both) `tol = 1e-13, Lw = 130, dt_out = 0.01` — with provenance `inferred`. **`eta` has no folder default: store `null`, provenance `absent`**; fabricating an `eta` is prohibited.
3. **Footer present but partial-schema →** an **anomaly** under the corrected record: log `(variant, id, missing_fields)`, set `footer_anomalous = true`, fall back to defaults for missing fields (`inferred`), surface the population (it should be empty; any member is new information).
4. **Provenance is per-field:** a `param_provenance` dict over `{tol, Lw, dt_out, eta}` with values `direct | inferred | absent | measured`. For `dt_out`, additionally **measure** the median inter-snapshot spacing from the file's own timestamps, store under `measured`, warn on > 1% relative disagreement with the footer/default value.
5. **Negative uses:** footers are never a completeness signal (Q-A1) and never a mapping source (Q-A2); gate-relevant times come from parsed timestamps, not footer text.
6. **Destination:** these fields populate the `ctl` §2.6 per-record metadata; the §2.6 field `trustworthy_horizon` is undefined anywhere in the package and is marked **RESERVED** (Open Item) rather than invented.

P2-1 is accepted in mechanism, corrected in premise (no "minimal footers" exist; the footer schema does not "vary"), generalized in form (per-field provenance).

**2. Reasoning.** The corrected facts overturn both factual premises of D7: the 219 standard-gold files (and the 1,550/701 base populations) contain no footer and no parameter fields at all, and footers that exist carry the full schema including `eta` and `tol`. What actually varies is *presence*, plus genuine within-folder heterogeneity among present footers (standard gold: 1,754 at `tol = 1e-13` vs 592 at `1e-14`) — which is exactly why per-file footer values take precedence over folder defaults whenever present, and why per-field provenance matters (a consumer filtering on `tol = 1e-14` must distinguish "footer said so" from "default assumed"). On `Lw`: the addendum's Correction 2 states verbatim that for no-footer files the folder-level defaults "must be assumed", naming `Lw` among the default-assumable fields, with per-variant values 118/130/130 from the master's dataset context — settling a question two first-generation reports had answered the other way (null-unless-documented). `eta = null` follows from the same text (defaults enumerated for `tol`/`Lw`/`dt` only). The `measured` channel exists because `dt_out` is the one field independently observable from the data, and `ctl` Step-1 item 4 already gestures at timestamp-derived `dt_out`.

**3. Evidence.** Master: Q-A5 block; CLM-07/08/09 rows; Observed Parameter Sets fragment (per-folder tuples; assume-defaults lines with `Lw`); Correction 2. Addendum: Correction 2 re-probed (`data04_footers.py`, 15,028 files; 1,550/701/219 exact); CLM-07/08/09 confirmed. Specs: `ctl_instruction.md` Step 1 items 3–4 (optional footer; `dt_out` from timestamps or defaults — re-verified), §2.6 metadata fields incl. `trustworthy_horizon` (line 648, re-verified undefined). Issue doc: lines 66, 68, 83, 85, 291 (P2-1), 301, 345.

**4. Confidence.** High. The single factor most likely to change it: a footer scan finding a genuine partial-schema population (a nonempty clause-3 set), which would reopen the schema-variance question and force a field-by-field fallback policy in place of the all-or-nothing model.

**5. Verification suggestion.** Footer scan over all 15,028 files (already executed by `data04_footers.py`): presence counts must reproduce 3,307/1,550 — 2,048/701 — 2,346/219 — 4,857/0, and the tuple histogram must match the dataset context. Unit tests: a footerless standard-base fixture yields `tol = 1e-13 (inferred), Lw = 118 (inferred), eta = null (absent), dt_out measured ≈ 0.17`; a fixture with a footer missing only `eta` sets `footer_anomalous` and logs.

**6. Proposed specification text.** Target: `ctl_instruction.md`, Step 1 item 3 (replacement) plus a §2.6 amendment:

```
[Step 1 item 3 — replacement]
3. Footer handling. A Result: footer is OPTIONAL. If present, it carries the
   FULL parameter schema (tol, Lw, dt_out, t_end, eta, energies); parse all
   fields, mark each {param}_provenance = 'direct'. If absent (verified
   populations: 1,550 hierarchical-base / 701 standard-base / 219
   standard-gold; DATA-07 Correction 2), assign the folder-level defaults:
       standard base:      tol = 1e-13, Lw = 118, dt_out = 0.17
       hierarchical base:  tol = 1e-15, Lw = 130, dt_out = 0.08
       gold (both):        tol = 1e-13, Lw = 130, dt_out = 0.01
   and mark {param}_provenance = 'inferred'. eta has NO folder default: store
   null with provenance 'absent'. A footer that parses but lacks any
   full-schema field is an anomaly: flag footer_anomalous = true, fall back to
   defaults ('inferred'), surface in the init log. Independently of the footer,
   MEASURE dt_out as the median timestamp spacing; store it with provenance
   'measured' and WARN if it disagrees with the footer/default value by > 1%.
   Footers MUST NOT be used as completeness signals or for ID mapping.

[§2.6 — amendment]
Each processed record carries param_provenance: a map over
{brutus_tolerance, word_length, dt_out, eta} with values in
{'direct','inferred','absent','measured'} per the Step-1 item-3 contract.
The trustworthy_horizon field is RESERVED — definition pending (Open Item);
writers emit null and readers must not consume it until defined.
```

**7. Consolidation provenance.** **CR-A:** `footer_state ∈ {present_full, absent, anomaly_partial}` model, per-field provenance, folder defaults including `Lw`, `eta` null/absent. **CR-B:** the same contract plus the `measured` `dt_out` channel with its 1% cross-check and the `trustworthy_horizon` reservation. **Decision: unanimous on the contract; CR-B's two additions adopted** (the `measured` channel is the only independent check available against a default that 2,470 files will silently inherit; the reservation converts an undefined consumer-facing field from a latent bug into a tracked open item). The folder-default values are identical in both and re-verified against the master by this pass. Secondhand R1–R8 picture (non-authoritative): 8/8 on mechanism; the 4-vs-4 split on provenance granularity resolved toward per-field by both consolidations; the `Lw` null-vs-default split settled by the addendum's own text — recorded by both as the closest call in this question.

### §3.6 Q-A6 (D-03) — Processed training-data format

**1. Final verdict / recommendation.** The framework names **HDF5 or `.npy`** (`ctl` Step 1 item 6), so both are spec-compliant and `txt`/`json` as a primary store is outside the recommendation. Within the compliant pair:

1. **HDF5 is the canonical processed-training-data store.** Layout: groups `/{variant}/{fidelity}/{id}`; float64 datasets (`times`, `positions`, `velocities`, masses, §2.6 derived arrays); per-group attributes carrying the full §2.6 metadata record, the Q-A5 `param_provenance` dict, raw-file SHA-256 hashes, and a `schema_version`; chunked + compressed; partial reads by group.
2. **`.npy`/`.npz` is acceptable as a derived cache/export** preserving the identical schema — noted as awkward as a sole store (ragged arrays plus rich metadata force thousands of files or `.npz` + sidecar index, reinventing HDF5 groups/attributes).
3. **JSON/text export is inspection- and debugging-only, never a training input path**; derived from the HDF5 store, clearly marked, same `schema_version`.
4. **Methodology consequences (not purely storage):** (a) **float64 end-to-end** — stored arrays feed every Q-B3 metric, so the store must round-trip parsed float64 bitwise (float32 would inject ~1e-7 relative noise, within sight of the tightest data tolerances); (b) **auditability** — store the §2.6 transform metadata (permutation, gauge rotation, COM/boost, `D, T, V`, scales) so the raw→processed map is re-derivable; (c) **determinism** — identical inputs produce byte-identical logical content.

**2. Reasoning.** The spec position is direct, so the only adjudication is within the recommended pair plus the JSON idea's status. HDF5 wins on fit: the data model is literally `variant → fidelity → id → ragged arrays + per-record metadata`, which is the HDF5 group/dataset/attribute model; `.npy` is by design a single-array container lacking colocated metadata. The JSON guardrail exists because a second readable copy invites silent divergence. The issue doc's own D-03 recommendation (HDF5 primary + optional inspection JSON) is endorsed with the precision/auditability clauses that make it spec-grade; its "methodology impact: zero" is corrected to "zero *iff* clause 4 holds."

**3. Evidence.** Specs: `ctl_instruction.md` Step 1 item 6 ("HDF5 or NumPy (.npy)" — re-verified verbatim); §2.6 metadata record. Master: Q-A6 block (no dataset facts). Issue doc: D-03 decision block, format trade-off section. External (carried; References): h5py documentation; NumPy `.npy`/`.npz` format documentation.

**4. Confidence.** High. The single factor most likely to change it: an unstated operational constraint forbidding HDF5 dependencies, which flips the primary to `.npy + sidecar index` without touching clauses 3–4.

**5. Verification suggestion.** Round-trip test: parse raw files → write store → read back → bitwise `np.array_equal` against directly parsed float64 arrays, including times. Schema test: every group carries the full attribute set + `schema_version`. Negative test: the training loader refuses a JSON path.

**6. Proposed specification text.** Target: `ctl_instruction.md`, Step 1 item 6 (replacement):

```
6. Processed training data is stored in HDF5 (primary): groups
   /{variant}/{fidelity}/{id}, float64 datasets (t, q, v, m and §2.6 derived
   arrays), per-group attributes carrying the §2.6 metadata (including
   param_provenance), raw-file SHA-256 hashes, a top-level schema_version, and
   the build's transform metadata (D, T, V, E_scale and scale provenance), so
   raw values are exactly re-derivable. Chunked + compressed storage is
   recommended. .npy/.npz is an ACCEPTABLE derived/export alternative
   preserving the identical schema; the HDF5 file is the single source of
   truth. JSON/text exports are inspection-only and MUST NEVER be a training
   input path. Acceptance test: raw -> HDF5 -> arrays round-trips
   bit-identically in float64 against direct parsing for a sample of
   trajectories.
```

**7. Consolidation provenance.** **CR-A:** HDF5 canonical keyed by `traj_key`, float64 datasets, provenance/admission attributes, `.npy/.npz` traceable caches, JSON inspection-only. **CR-B:** identical verdict plus the explicit `/{variant}/{fidelity}/{id}` layout, SHA-256 hashes, `schema_version`, and the three named methodology consequences. **Decision: unanimous; CR-B's layout and consequence clauses adopted** — they are what makes the verdict transcribable, and the bitwise-round-trip clause is the only place the storage decision touches metric validity. Secondhand R1–R8 picture (non-authoritative): unanimous among addressers (R6 unaddressed; R5 matrix-only); the h5py/NumPy documentation argument originated with R1/R2 and is carried in References. No dissent.

---

## §4 Cluster B — Sampling, Precision & Global Scale (Phase 27)

### §4.1 Q-B1 (M12) — Points-per-trajectory feasibility

**1. Final verdict / recommendation.** The per-trajectory **data-loss** sample-count contract:

1. `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))`, with time points drawn from the trajectory's own snapshot set **without replacement**.
2. `n_pts_cap` defaults to **32**, carried explicitly as the spec's *example* value (`ctl` writes "(e.g., 32)"; the addendum's WR-03 note confirms it is an example, not a hard contract), exposed as a configuration knob and **flagged non-evidence-based**.
3. The spec's 50/50 composition is realized without replacement as `k_w = floor(n_pts/2)` acceleration-norm-weighted draws (weighted sampling without replacement, e.g. Gumbel-top-k), then `n_pts − k_w` uniform draws from the remaining snapshots; all draws from a seeded generator (reproducible batches).
4. The loader exposes `n_snapshots` and `dt_out` per trajectory as metadata — the data-side end of G5; how anything scales with `dt_out` (M16) is doc-03 and is not answered here.

**Adjudication of M12:** the BLOCKING claim ("standard trajectories cannot support 32 points/trajectory") is **wrong**: drawing 32 distinct points from 59–61 snapshots without replacement is trivially possible, and the verified median (61) makes a fixed 32 feasible for every admitted standard-base file. The proposed P1-4 `n_pts = min(32, int(0.5 · n_snapshots))` is **rejected as a normative data-side rule**: the 0.5 factor is unevidenced anywhere in the package, and P1-4 is internally inconsistent with the issue doc's own verification checklist, which expects gold trajectories to receive `n_pts = 128` — a value neither `min(32, ·) = 32` nor `int(0.5 × ~1000) = 500` produces.

**2. Reasoning.** Two package facts anchor the analysis: data-loss time points are drawn from the discrete Brutus snapshots (`pinn` §3.1 states it twice), so `n_snapshots` is the hard ceiling for distinct points and without-replacement is the natural semantics (duplicated points add no information, only implicit re-weighting); and 32 was never locked — parenthetical in `ctl`, a code default in `pinn`, and explicitly de-contractualized by WR-03, removing the premise that any "32-point contract" needed relaxing. The verified distribution (medians 61/127/1003; standard min 59) settles feasibility outright. What is real in M12's vicinity is a *diversity/concentration* observation — with the weighted half drawn from a ~60-point pool, the few highest-acceleration snapshots are selected near-deterministically every batch — but that is a training-dynamics tuning question (arguably intended: the spec says the weighting "prioritizes close encounters"), belonging with the training loop. The 0.5 factor's rationales conflate the data-loss sample with the deferred collocation budget (M16) or with the training set (batches re-draw, so every snapshot is consumed across batches regardless); its entire effect at the verified median is 32 → 30. A rule whose effect is cosmetic, whose constant has no package source, and whose proposing document contradicts it in its own checklist does not belong in spec text; `min(cap, n)` delivers the same robustness without the unmotivated constant.

**3. Evidence.** Master: Q-B1 block (WR-03-corrected citation, line 1197); CLM-09/10 rows. Addendum: WR-03 ("the '(e.g., 32)' … is an example, not a hard 32-point contract"); Correction 3 (medians 61/127/1003; standard min 59). Specs: `ctl_instruction.md` Mini-Batch Construction ("Sample n_pts (e.g., 32) time points per trajectory: 50% uniform …, 50% weighted by acceleration norm" — re-verified at lines 1197–1201); `pinn_architecture.md` §3.1 (snapshot-sourced; `points_per_trajectory = 32` default — re-verified). Issue doc: lines 60, 77, 286 (P1-4), 298 (checklist: 59→29 **and** 1000→128 — the internal contradiction).

**4. Confidence.** High on the contract form (clauses 1, 3, 4). Medium on retaining 32 as the default cap — the spec's example, not an evidenced optimum; re-tuning is a doc-03 matter. The single factor most likely to change the verdict: OI-6 revealing an admitted no-footer subpopulation materially below ~57 snapshots, which would make the cap bind and pressure the default's *value* — not the `min()` form.

**5. Verification suggestion.** Snapshot-count distribution per variant over the admitted set, split by footer presence (extends DATA-06). Unit tests: `n = 59 → 32` distinct indices, exactly 16 + 16 weighted/uniform; `n = 10 → 10` distinct indices (cap inactive, no error); fixed seed ⇒ identical draws; all drawn times exist in the trajectory's snapshot set.

**6. Proposed specification text.** Target: `ctl_instruction.md`, "Mini-Batch Construction with Lookahead Sampling" (amendment):

```
Per-trajectory data-loss point count:
    n_pts(traj) = min(n_pts_cap, n_snapshots(traj)),
sampled WITHOUT replacement from the trajectory's snapshot times.
n_pts_cap defaults to 32 (the spec's existing example value; not
evidence-based — revisit with admitted-set snapshot distributions). The 50/50
composition is realized as: k_w = floor(n_pts/2) snapshots drawn by
acceleration-norm-weighted sampling without replacement (Gumbel-top-k), then
n_pts - k_w drawn uniformly without replacement from the remainder; all draws
from a seeded generator. The loader exposes n_snapshots(traj) and dt_out(traj)
as metadata (forward interface for the deferred M16 collocation-density
question — doc-03; not used here). No 0.5 * n_snapshots factor is imposed
(unevidenced; see Q-B1 resolution).
```

**7. Consolidation provenance.** **CR-A:** `n_pts = min(n_pts_cap, N_valid)` without replacement, seeded weighted/uniform split, default cap 32 flagged as example; 0.5 factor and variant floors rejected. **CR-B:** the same verdict plus the explicit M12 adjudication (BLOCKING claim wrong; P1-4 internally inconsistent with the 128-point checklist row) and the diversity-observation triage. **Decision: unanimous between the consolidations; CR-B's adjudication detail adopted** because the question explicitly asks whether the bounds are "appropriate" and a candidate verdict source must say *why* the BLOCKING reclassification fails, not just decline the rule. Secondhand R1–R8 picture (non-authoritative, and material): the underlying reports split 5 (0.5-factor: R1, R3, R6, R7, R8) vs 2 (`min(cap, n)`: R2, R4) — **both consolidations independently adopted the two-report minority on the merits**, and this pass confirms that adjudication against the verified arithmetic and WR-03. The five-report majority position is preserved as the dissent; if the project prefers the 0.5 cap despite the evidentiary gap, it is a one-line semantic change to `n_pts_cap`, and the operational difference at the verified median is 30 vs 32 points.

### §4.2 Q-B2 — Footer / mass-drift protocol

**1. Final verdict / recommendation.** The IC↔Brutus mass-consistency contract:

1. **Coverage: all pairs, as a standing admission condition — not a one-off sample.** At preprocessing, for every `(variant, fidelity, id)`, compare the three IC masses against the three Brutus `t = 0` masses, in raw file order, before canonical reordering (~15,028 pairs × 3 scalars; negligible cost). This dissolves WR-01 operationally: with 100% coverage no sample size is needed; the 1,000-vs-100 conflict remains reported as a documentary defect and its CLM-row disposition stays the open Phase-24 user-gate decision per the addendum.
2. **Gate:** `max_i |m_IC,i − m_Brutus,i(t=0)| < 1e-15`, **absolute**, in float64 parse space — deliberately the same tolerance, space, and style as the existing `ctl` §2.1 intra-trajectory mass-invariance gate, and appropriate because the masses are O(1) by construction (both families normalize to `Σm = 3`), making absolute-1e-15 ≈ relative-1e-15.
3. **Implementation warning:** never call `np.allclose(rtol=1e-15)` with default arguments as P2-2 suggests — the default `atol = 1e-8` passes absolute discrepancies eight orders larger than the gate. Set tolerances explicitly (`rtol=0, atol=1e-15`) or use a plain max-abs comparison.
4. **Escalation on failure, and only on failure:** re-compare the raw mass **strings** with `decimal.Decimal`. Decimal-equal ⇒ a float64 parsing bug in the pipeline (fix the parser; the data is fine). Decimal-unequal ⇒ a genuine data discrepancy ⇒ **quarantine** with reason `mass_ic_mismatch`, log `(variant, id, body, |Δm|)`. Routine Decimal parsing is not adopted (Q-B3), and **a mismatch never silently changes the canonical mass source.**
5. **On pass:** the IC masses are canonical and feed the IC₁₃ raw-mass slots (HC-2); the Brutus echo is confirmatory metadata.
6. **Standing disposition from DATA-05:** the 70 `brutus_hierarchical` mismatches found by the full-population probe (IDs `0005`–`0059`, `0061`–`0075`; |Δm| ≈ 0.1–1.0) are governed by the 2026-06-11 user instruction — current IC files are canonical; the 70 base-hier outputs are stale artifacts quarantined from training, metrics, and PIPE-07 pending targeted rerun from current ICs; they are **not** a `decimal.Decimal` precision problem and are not to be skipped permanently.

**2. Reasoning.** The addendum decides the coverage question empirically: the full-population DATA-05 probe is what found and *localized* the defect set — 70/4,857 mismatches confined to one variant, with the gold runs of the same 70 IDs matching the ICs perfectly (0/4,857), the observation that ruled out a generation-side IC error and produced the canonical-ICs ruling. A 100-pair audit drawn uniformly over all pairs would have missed the defect with probability ≈ (1 − 70/15,028)^100 ≈ 63%, and even a hit would not enumerate the affected set; a 1,000-pair audit detects but still does not enumerate. The probe also refutes the protocol's framing: failures at |Δm| ≈ 0.1–1.0 are six-plus orders beyond any text-rounding effect, so "if mismatch, parse with Decimal" and especially "use Brutus t=0 masses as canonical" (a first-generation fallback branch) would have been exactly the wrong responses. The escalation path is therefore re-cast from remedy to **classifier**: correctly rounded decimal→binary64 parsing means identical strings parse to identical doubles, so a gate failure is evidence of a real discrepancy, which Decimal then sorts into parser-bug vs data-defect. One framing correction to the master is carried forward (F-4): "spec is silent on a mass-drift verification protocol" is incomplete — `ctl` §2.1 already carries the float64 absolute-1e-15 mass-invariance gate and an IC↔Brutus consistency clause (re-verified by this pass); what was missing is only the explicit cross-file formula, tolerance arguments, and escalation path.

**On the gate-form fork (absolute vs relative), see part 7.** For these data the two forms are numerically near-equivalent: with `Σm = 3` and individual masses O(0.1–2), `|Δm| < 1e-15` and `|Δm|/|m| < 1e-15` differ by at most one order of magnitude in effective stringency, both at the float64 representation floor and both at least 14 orders below the only observed real failures.

**3. Evidence.** Addendum: DATA-05 section in full (70/4,857 base-hier; gold-hier 0/4,857; base-std 0/2,749; gold-std 0/2,565; example ID 5 abs_diff ≈ 0.351; "not a decimal.Decimal precision problem"; RESOLVED-WITH-INSTRUCTION); WR-01 appendix. Master: Q-B2 block; CLM-09 row. Specs: `ctl_instruction.md` §2.1 (float64 parse space; `max_{t,i}|m_i(t) − m_i(0)| < 1e-15`; IC↔Brutus consistency clause — re-verified). FROZEN: `sampling_method.md` (`Σm = 3` normalization). Issue doc: lines 219–221, 292 (P2-2: 100 pairs, `np.allclose(rtol=1e-15)`), 231, 360. External (carried; References): NumPy `allclose` documentation (default `atol = 1e-8`); Goldberg (1991).

**4. Confidence.** High. The single factor most likely to change the verdict: post-rerun DATA-05 evidence of *systematic textual* IC↔Brutus divergence (rounding-scale, widespread), which would convert the escalation branch into a standing Decimal-for-masses requirement while leaving clauses 1–3 and 6 intact. Current evidence points the opposite way: every mismatch found was a stale-artifact defect.

**5. Verification suggestion.** Substantially executed by `probes/data05_mass_drift.py` (15,028 pairs). Remaining: re-run the gate after the 70-ID rerun lands and assert 0 failures; unit tests — a fixture perturbed at the 16th significant figure passes, at the 14th fails and Decimal classifies it data-defect; an `allclose`-defaults implementation is caught by a test where `|Δm| = 1e-10` (must fail the gate; default-args `allclose` would pass it).

**6. Proposed specification text.** Target: `ctl_instruction.md`, §2.1 (amendment):

```
IC<->Brutus t=0 mass gate (ALL pairs, at preprocessing — not a sample):
    max_i | m_IC,i - m_Brutus,i(t=0) | < 1e-15   (float64, ABSOLUTE; masses
    are O(1) with sum 3, so this sits at the representation floor)
Implementations MUST set tolerances explicitly (e.g. np.allclose(..., rtol=0,
atol=1e-15)); library defaults (atol = 1e-8) silently mask failures and are
forbidden here. Comparison runs in raw file order, before canonical
reordering. Escalation on failure: re-parse BOTH mass strings with
decimal.Decimal. If the decimal values are EQUAL, the discrepancy is a float64
parsing bug — fix the parser (do not quarantine the data). If they DIFFER, the
pair is genuinely inconsistent — QUARANTINE the trajectory with reason code
mass_ic_mismatch; a mismatch never silently changes the canonical mass source.
On pass, the IC-file masses are canonical for the IC13 vector. Standing
disposition (DATA-05, 2026-06-11): current IC files are canonical; the 70
brutus_hierarchical outputs at ids 0005-0059, 0061-0075 are quarantined from
training, metrics, and PIPE-07 pending targeted rerun from current ICs. The
mass-invariance-over-time gate of this section is unchanged.
```

**7. Consolidation provenance.** **CR-A:** full-population gate in **relative** form — `max_i |Δm_i|/|m_IC,i| ≤ 1e-15`, implemented `np.allclose(rtol=1e-15, atol=0.0)`; Decimal as failure classifier; quarantine semantics; DATA-05 disposition identical. **CR-B:** full-population gate in **absolute** form — `max_i |Δm_i| < 1e-15`, implemented `rtol=0, atol=1e-15`; same classifier, quarantine, and disposition; plus the explicit `allclose`-defaults prohibition, the raw-file-order clause, and the F-4 spec-not-silent correction. **Decision: genuine fork on gate form; CR-B's absolute form adopted.** Grounds: (a) the existing §2.1 mass-invariance gate is absolute (`max_{t,i}|m_i(t) − m_i(0)| < 1e-15`, re-verified), and the cross-file gate should match the in-file gate's space and style rather than introduce a second convention for the same quantity; (b) for these O(1), Σ=3 masses the forms are near-equivalent (one order of magnitude at the extremes of the mass range), so the choice costs nothing in discrimination while buying spec uniformity; (c) the absolute form has no zero-denominator edge case. This is a low-stakes fork — both forms pass and fail the same real data — and is recorded as such; a project preference for relative form would not change any other clause. CR-A's relative form is the preserved dissent. Both consolidations independently report the first-generation split as full-scan 4 (R1–R4) vs sampled 2 (R7, R8 tier-1), with R7's Brutus-masses-canonical fallback branch rejected by both as contradicted by the DATA-05 ruling; that secondhand picture is consistent and non-authoritative.

### §4.3 Q-B3 — Precision handling (float64 sufficiency; Decimal-for-masses)

**1. Final verdict / recommendation.** **float64 is sufficient for all data-side validation metrics** (SCS, SASD, IPR, PSC), invariant calculations, and completeness checks, computed on CPU from float64-parsed arrays (stored per Q-A6). `decimal.Decimal` is mandated nowhere routinely; its sole required role is the Q-B2 escalation classifier. Optional hygiene (recommended, not required): pairwise or compensated (Kahan) summation in Hamiltonian accumulation; extended-precision recomputation within small audit bands of a threshold is legitimate optional practice, not contract. The `|H(0)| → 0` edge case is handled by the dqa's undefined-SCS quarantine rule — never by a denominator floor inserted into the locked formula, and not by higher precision. HC-4's dual-epsilon split governs **softening** (a physics-model parameter), not arithmetic precision; there is no tension between HC-4 and float64.

**2. Reasoning.** The end-to-end error budget: correctly rounded decimal→binary64 parsing contributes ≤ ½ ulp ≈ 1.1e-16 relative per value (whether the source string carries 17 digits, as the `t = 0` IC echoes do, or ~41, as later blocks do — extra digits sharpen rounding, they cannot worsen it); metric arithmetic over a three-body system adds a few × 1e-16; conditioning amplifies `H`'s relative error by roughly `(2T + |V|)/|H|` — O(1–10) for ordinarily bound systems, diverging only as `|H| → 0`, the population the dqa already routes to manual review. Net float64 noise on `ε_H`: ~1e-15..1e-13 — at or below the data's own integration tolerance (CLM-09: 1e-13..1e-15, confirmed) and **eight-plus orders below the 1e-5 reject gate**. The same budget covers SASD (O(1) norm ratios vs a 0.5 flag), IPR (spline + force arithmetic vs a 1e-3 flag), and PSC (binning is precision-insensitive). The addendum closes the loop empirically: the one real mass anomaly the dataset contained (DATA-05) was a 0.1–1.0-scale artifact defect, explicitly "not a decimal.Decimal precision problem" — precisely the regime where higher precision buys nothing.

**3. Evidence.** Master: Q-B3 block; CLM-09 row; HC-4 (softening/precision distinction). Addendum: CLM-09 confirmed; DATA-05 ("not a decimal.Decimal precision problem"). Specs: `ctl` §2.1 (float64 parse space); numerical notes ("use double precision for all invariants"); dqa near-zero-`H(0)` manual-review rule (re-verified). Issue doc: lines 225–233. External (carried; References): NumPy `finfo` (float64 ε ≈ 2.22e-16); Python `decimal` documentation; Goldberg (1991).

**4. Confidence.** High. The single factor most likely to change the verdict: discovery of a non-trivial admitted population with `|H(0)|` within ~1e-10 of zero — beyond what manual review absorbs — which would force a dedicated near-zero-energy metric variant (e.g., absolute-drift gating), not higher precision per se.

**5. Verification suggestion.** Synthetic perturbation probe: inject ±1-ulp noise into all coordinates of real trajectories and show `|Δε_H| ≲ 1e-13` (direct measurement of the metric noise floor). Cross-check one trajectory's `ε_H` naive vs Kahan summation (difference ≪ gate). Log the `|H(0)|` distribution to size the manual-review population.

**6. Proposed specification text.** Target: `ctl_instruction.md`, note appended after §2.1:

```
Validation metrics (SCS, SASD, IPR, PSC), invariants, and completeness checks
are computed in CPU float64 over the float64-parsed arrays. Exact/Decimal
arithmetic is not used routinely; decimal.Decimal is reserved for the §2.1
mass-gate escalation classifier. Metric values within documented audit bands
of admission thresholds MAY be recomputed in extended precision as optional
hygiene. If |H(0)| is numerically near zero, the SCS-undefined quarantine rule
applies; no denominator floor is inserted into the locked SCS formula.
```

**7. Consolidation provenance.** **CR-A:** float64 for parsing and all data-side metrics; Decimal as raw-text diagnosis only; never to "repair" a true mismatch; near-zero-`H(0)` → metric-definition change, not precision. **CR-B:** the same verdict with the quantitative error budget (parse ulp, conditioning factor, net noise floor) and the explicit no-denominator-floor and HC-4-clarification clauses. **Decision: unanimous; CR-B's budget retained** because it is what makes the sufficiency claim *checkable* (verification item 1 measures it directly) rather than asserted. Secondhand R1–R8 picture (non-authoritative): unanimous among the seven addressers per both consolidations (R6 unaddressed); differences were rigor, not direction. No dissent.

### §4.4 Q-B4 — Global-scale `compute_globals` / `D = 6.694` (KNOWN CONFLICT)

**1. Final verdict / recommendation (constraint-entailed; reconciliation presented; formal ratification downstream at EVID-10/PIPE-09).** The data pipeline's global-scale computation **must use the locked raw-mass convention** `D = (G·T²)^{1/3} ≈ 4.6416` with `T = 10, G = 1` (HC-6 / PHYS-01). The issue doc's `D = cbrt(G·M_tot·t_max²) = 6.694` and its P1-7 are **rejected** as pipeline instructions: `ctl` §2.5 derives the raw-mass form and explicitly rejects the 6.694 alternative except under a mass-fraction rewrite documented as future-only (rejection re-verified at §2.5 by this pass). Any parameterization exposing the mass-fraction form as a runtime alternative (e.g., an `M_tot_ref` knob) is also rejected: a configuration path whose non-default branch produces a constraint-violating convention is a standing footgun, and the spec's explicit rejection leaves nothing legitimate for the parameter to select. Three accompanying repairs, none re-opening HC-6:

1. The issue doc's `compute_globals` listing is internally inconsistent and must not be transcribed: it scales coordinates by the mass-fraction `D = 6.694` while computing kinetic and potential energies with **raw** masses — a hybrid dimensionless in neither convention.
2. The listing regularizes the potential with an **additive** epsilon (`r_ik = ‖Δr‖ + eps`), the exact PHYS-03 anti-pattern; the invariant `V` must use the **Plummer** form `√(‖Δr‖² + ε_inv²)` with `ε_inv = 1e-10`, and ε enters `V` only (re-verified against the `ctl` anti-pattern text).
3. The `E_scale` floor is canonicalized at **`1e-8`** — a genuine three-way conflict verified directly by this pass: `ctl` §2.5 line 608 reads `+1e-10`; `ctl` Step-4 table (line 1049) and `pinn_architecture.md` §5.2 (line 761, the network-facing input contract) both read `+1e-8`; the issue-doc listing reads `+1e-8`. The network-facing statement governs on a 2-of-3 editable-spec basis; §2.5's `1e-10` is the outlier, plausibly propagated from the adjacent `ε_inv`.
4. `compute_globals` runs over the **admitted set** (post-Step-1A, post-blacklist, post-DATA-05-quarantine) — a documented minor judgment flagged for spec-author sign-off: medians make it nearly equivalent to all-files computation, but the admitted-set choice is deterministic and immune to NaN poisoning from corrupt or stale records.

**Reconciliation and adoption cost (presented, not endorsed):** both conventions are internally coherent. Substituting `r = D r'`, `t = T u` into Newton's equation and demanding a unit-coefficient dimensionless residual with **raw masses** forces `D³ = G T²` (≈ 4.6416); writing the same residual with mass fractions `m_i' = m_i/M_tot` forces `D³ = G M_tot T²` (≈ 6.694 at `M_tot = 3`, which both families satisfy by construction — the issue doc's *arithmetic* is right; its *convention* is the rejected one). Half-adoption is concretely harmful: under a D change, scaled kinetic energy goes as `D⁻²` and potential as `D⁻¹`, so scaled `E` shifts non-uniformly across trajectories, and scaled `E` feeds locked stage thresholds (`E < −0.5`, `|E| < 0.01`) whose meanings would silently change. Full adoption is a convention migration: every mass replaced by `m/M_tot` in every residual, Hamiltonian, angular-momentum, COM, and invariant formula; stage thresholds re-derived; normalizers recomputed; processed stores regenerated; the network retrained.

**2. Reasoning.** Inside this research the question is constrained, not open: HC-6 is a fixed input, the spec's rejection is explicit, and the addendum routes CLM-13 as PENDING — not probed — to exactly this consolidation→EVID-10/PIPE-09 path ("not a dataset count"). This document therefore supplies the constraint-entailed pipeline verdict plus the reconciliation the question asks for, leaving ratification to EVID-10 as designed. The mixed-convention finding is the strongest single argument that the 6.694 instruction, as written, is not even a coherent alternative — it is a bug. The additive-ε and `E_scale` findings are independent spec-hygiene defects verified directly against the snapshots by this pass.

**3. Evidence.** Master: Q-B4 block; CLM-13 row + note; HC-6. Addendum: CLM-13 PENDING; routed EVID-10/PIPE-09. Specs (all re-verified): `ctl_instruction.md` §2.5 (derivation; explicit 6.694 rejection; `E_scale … + 1e-10` at line 608 — the outlier; Step-4 table `+1e-8` at line 1049); `pinn_architecture.md` §3.2 (raw-mass nondimensionalization absorbs G), §5.2 (`E_scale … + 1e-8`, line 761); `ctl` additive-vs-Plummer prohibition with `ε_inv = 1e-10` scope (~line 698). FROZEN: `sampling_method.md` (`Σm = 3`). Issue doc: lines 235–275 (the listing), 289/306 (P1-7), 317.

**4. Confidence.** High — constraint-entailed. The single factor that could change it: a user decision to re-open PHYS-01 (the documented future mass-fraction rewrite), out of scope by construction.

**5. Verification suggestion.** Dimensional-consistency unit test: analytic two-body circular orbit under the locked `(D, T)` scaling — confirm the dimensionless residual coefficient is 1 with raw masses (and is `M_tot ≠ 1` if mass fractions are wrongly substituted). Static checks: grep the pipeline for `6.694`/`M_tot` inside any `D` computation and for additive-ε potentials. Recompute `E_scale` on the admitted set under the locked convention and archive with §2.6 metadata.

**6. Proposed specification text.** Target: `ctl_instruction.md`, §2.5 (one-token fix plus appended normative notes):

```
[E_scale line — replace]
    E_scale = |median(E)| + 1e-8
(canonicalizes the floor stated by the Step-4 table and pinn_architecture.md
§5.2 — the network-facing contract; the prior 1e-10 here was an outlier,
likely propagated from the adjacent eps_inv).

[appended normative notes]
- compute_globals evaluates per-IC energies with RAW masses and regularizes V
  with the PLUMMER form r_safe = sqrt(r^2 + eps_inv^2), eps_inv = 1e-10 —
  never an additive +eps on the distance norm (PHYS-03 anti-pattern).
  D = (G*T^2)^(1/3) (≈ 4.6416 for G=1, T=10) per PHYS-01; the mass-fraction
  6.694 form remains rejected, and no configuration parameter may select it.
- Scope: global statistics (E_scale, r_char, hence the fixed Q_scale = 0.5)
  are computed over the ADMITTED set (post Step-1A, post blacklist, post
  DATA-05 quarantine). Medians make this nearly equivalent to all-files
  computation, but the admitted-set choice is deterministic, documented, and
  excludes corrupt or stale records (documented minor judgment — flagged for
  spec-author sign-off).
```

**7. Consolidation provenance.** **CR-A:** locked raw-mass D; 6.694 valid only under a complete future rewrite; no runtime alternative; negative test that the 6.694 path is unavailable. **CR-B:** identical core verdict plus the three verified repairs (mixed-convention listing defect, additive-ε defect, `E_scale` three-way resolution) and the admitted-set scope rule. **Decision: unanimous on the constraint-entailed core; CR-B's repairs adopted.** CR-A acknowledges the listing's convention mixing in its provenance but does not carry the `E_scale` or additive-ε fixes into its verdict; since all three defects were independently re-verified against the snapshots by this pass (§0.3), omitting them would leave known, confirmed spec conflicts unresolved in the candidate verdict source. The `E_scale = 1e-8` choice is the one judgment in this question that is *not* constraint-entailed (it is a 2-of-3 editable-spec canonicalization) and is flagged as such. Secondhand R1–R8 picture (non-authoritative): near-unanimous locked-D (6 reports) vs R8's parameterize-and-defer (rejected by both consolidations as a constraint hazard; its deference honored via the explicit EVID-10/PIPE-09 routing); R6 unaddressed. Dissent preserved: R8's stance.

---

## §5 Cluster C — Validation Metrics, Data-Side Definitions (Phase 28)

> Scope reminder: only the data-side definitions are resolved here. Training-loop usage of all four metrics (SASD-weighted collocation, IPR-as-ALM-noise-floor, PSC-governed replay) is doc-03 scope and untouched (§0.2).

### §5.1 Q-C1 (SCS) — Symplectic Conservation Score: definition + thresholds (KNOWN CONFLICT)

**1. Final verdict / recommendation.** The data-side SCS contract is the **locked post-v1.3 gate, transcribed verbatim and operationally completed** — nothing from the issue doc's ratio-threshold scheme is transcribed into spec text.

1. **Definition (HC-5, locked; sole written home dqa §3.1 / SI-DQA-003):** `ε_H = max_{t∈[0,T]} |(H(t) − H(0)) / H(0)|`, `SCS = log₁₀(ε_H)`, **reject if `SCS > −5`** (equivalently `ε_H > 1e-5`).
2. **Hamiltonian evaluation:** `H(t)` in float64 with the **Plummer validation softening `ε = 1e-10`** in the potential (HC-4: validation metrics use the static ε). At admitted separations (`r ≥ 0.01` by the generation-time prescreen, re-verified in `sampling_method.md`) the softening correction is ≈ `(ε/r)²/2 ≤ 5e-17` relative — below float64 resolution; the ε is specified for definitional uniformity with the other validation metrics, not because it changes any admitted value.
3. **Band structure (non-strict boundaries, dqa §3.1, re-verified):** Excellent `SCS ≤ −10`; Acceptable `−10 < SCS ≤ −6`; Marginal `−6 < SCS ≤ −5` (admitted, flagged for review); Reject `SCS > −5`. The tie `SCS = −5` exactly is **Marginal** — admitted and flagged, not rejected (the gate is strict `>`).
4. **Edge cases:** `|H(0)|` numerically near zero ⇒ SCS **undefined** ⇒ quarantine for manual review (the dqa's own rule; never patched with a denominator floor). `ε_H = 0` exactly ⇒ `SCS = −∞` ⇒ Excellent (handled explicitly, not as an error).
5. **Units invariance, stated once:** under the locked scaling `H' = D·H` uniformly (kinetic and potential both scale as `1/D` when `G = 1, D³ = GT²`; re-derived by this pass), so `ε_H` — hence SCS and every band decision — is identical in raw and scaled units. Compute on raw parsed arrays by convention (matches dqa Phase-1 placement).
6. **Storage:** persist per-trajectory `eps_H`, `SCS`, and the band label in the Q-A6 store; the Q-A1 gate consumes them.
7. **Disposition of the issue doc's numbers (reconciliation, not transcription):** its `> 1e-6` "Phase-1 screening" threshold is the **Acceptable/Marginal band boundary (`SCS = −6`) mis-promoted to a reject gate** — adopting it would purge the entire Marginal band the locked scheme deliberately retains for review; its `< 1e-8` "tightening for high-resolution data" has **no source anywhere in the package** (not a dqa band edge, not a constraint, not a dataset fact) and is treated as an unsourced proposal. Whether any stage-conditional SCS tightening is wanted is deferred until per-variant SCS distributions exist and is in part a doc-03 question.
8. **Symbol hygiene:** the validation-gate `ε_H` (this metric) and the training-loss energy-denominator floor `ε_H = 1e-4 · S_H` (`pinn` §3.4) are **distinct quantities sharing a glyph**; nothing here touches the training-side symbol.

**2. Reasoning.** This is the package's seed conflict, and the authority order fixes it: HC-5 locks the log-drift definition and the `−5` gate; the dqa is read-only but is the gate's sole written home, so the operative spec change is **transcription into the editable `ctl`** (implementing, not re-opening, the constraint). The substantive adjudication concerns the issue doc's two numbers, and the right disposal is diagnostic rather than dismissive: `1e-6` is recognizably the dqa's Acceptable/Marginal boundary wearing a gate's clothes — which also explains *why* the issue doc landed on that number — while `1e-8` fails every sourcing test the package provides. The "ratio thresholds are the same physics in different units, just stricter" reconciliation is accurate arithmetic but incomplete adjudication: translated or not, adopting them overrides a locked gate, and the Marginal band's deliberate retention is design content a stricter gate would destroy. The operational completions (non-strict bounds; the tie; `ε_H = 0`; near-zero `H(0)`; invariance; storage) come from the dqa's own text plus one re-derived algebra fact, and exist because a spec author transcribing only the formula would still face each case.

**3. Evidence.** Master: Q-C1 block; HC-5; the two-`ε_H` disambiguation note. Addendum: silent on SCS by design (no CLM row; convention, not a count). Specs (re-verified): `data_quality_assessment.md` §3.1 (definition, non-strict bands, near-zero-`H(0)` rule), §5.1 (gate-on-load placement), SI-DQA-003 note; `pinn_architecture.md` §3.4 (the other `ε_H`); `ctl_instruction.md` (transcription target; dual-ε note ~line 703). Issue doc: lines 129–141 (ratio thresholds — re-verified at those lines by this pass).

**4. Confidence.** High — constraint-entailed in definition and gate; completions are dqa-textual plus one verified identity. The single factor that could change anything: a user decision re-opening HC-5 (out of scope), or per-variant SCS distributions motivating a documented *additional* review band layered on top of — never replacing — the locked gate.

**5. Verification suggestion.** Compute `ε_H`/SCS/band for ~100 trajectories per (variant, fidelity) in raw and scaled units and assert bitwise-equal band decisions (invariance test). Unit tests: `ε_H = 1e-5` exactly ⇒ Marginal-flagged, admitted; `1.0001e-5` ⇒ rejected; `H(0) = 1e-14` fixture ⇒ quarantined; constant-`H` fixture ⇒ `SCS = −∞`, Excellent. Publish per-variant SCS histograms.

**6. Proposed specification text.** Already carried as **clause 5 of the Step-1A gate** (§3.1, part 6), which is the locked gate's transcription into `ctl_instruction.md` including the band table, tie rule, near-zero-`H(0)` quarantine, ε = 1e-10 evaluation, and storage. One commentary addition to that clause:

```
Raw/scaled invariance: H' = D*H under the locked scaling, so eps_H and all
band decisions are unit-independent; compute on parsed raw arrays by
convention. The training-loss symbol eps_H = 1e-4 * S_H (pinn §3.4) is a
distinct quantity and is unaffected by this gate.
```

**7. Consolidation provenance.** **CR-A:** locked gate verbatim; store raw + log under distinct names; `ε_H = 0 → SCS = −∞` and pass; near-zero-`H(0)` quarantine; bands as optional; ratio thresholds demoted to "diagnostic bands only". **CR-B:** the same core with the remaining completions — the `SCS = −5` tie ruled Marginal, the softening-inertness quantification, the `H' = D·H` invariance, the symbol-hygiene clause, and the *diagnostic* disposal of the issue doc's numbers (1e-6 = mis-promoted band boundary; 1e-8 unsourced). **Decision: unanimous on everything load-bearing; CR-B's completions adopted** — each is dqa-textual or independently re-derived by this pass, and each closes a case a transcribing spec author would otherwise have to invent. One small CR-A/CR-B divergence resolved: CR-A labels the ratio numbers "diagnostic bands only", which over-credits `1e-8` (it is not any band edge); CR-B's unsourced-proposal classification is adopted for it, while `1e-6` does coincide with a real band boundary and is described as such. Secondhand R1–R8 picture (non-authoritative): unanimous among addressers per both consolidations; R6 outcome-consistent on a stale citation. No dissent.

### §5.2 Q-C2 (SASD) — Stiffness-Aware Sampling Density (data-side)

**1. Final verdict / recommendation.** The data-side SASD contract:

1. **Definition (canonical, completing the dqa's packaged scalar):** per interior interval `i` between consecutive snapshots,

   `SASD_i = Δt_i · max_{b ∈ bodies, t ∈ {t_i, t_{i+1}}} ( ‖a_b(t)‖ / max(‖v_b(t)‖, v_floor) )`, `v_floor = 1e-12`

   — the interval length times the **per-body** maximum of `‖a‖/‖v‖`, evaluated at **both endpoints** of the interval, with a divide guard. `Δt_i` comes from the file's parsed timestamps, never from nominal `dt_out`.
2. **Accelerations are analytic, never finite-differenced:** `a_b` is computed from the snapshot positions via the Newtonian force law with the **validation Plummer softening `ε = 1e-10`** (HC-4). Finite-differencing at the data's own spacing would estimate the very quantity SASD interrogates, circularly.
3. **Scale invariance, stated once:** `Δt·‖a‖/‖v‖` is dimensionless and invariant under the locked `(D, T)` scaling (re-derived by this pass: `Δu·‖a'‖/‖v'‖ = Δt·‖a‖/‖v‖` identically), so raw and scaled computation agree to machine precision; raw G = 1 units recommended for uniformity with Q-C1/Q-C3.
4. **Flag rule (provisional constant):** `max_i SASD_i > 0.5` ⇒ **flag**, persisting per-trajectory `max SASD`, its `argmax` interval, and a `v_floor_hit` boolean. The 0.5 is the dqa's stated value, carried as provisional pending the empirical distribution.
5. **Disposition (flag ≠ auto-reject):** SASD is a resolution-adequacy diagnostic, not a validity gate; it does not join the Q-A1 reject set. Flagged dispositions: **(a)** gold counterpart exists ⇒ the resample the dqa asks for already exists; mark `sasd_flag = satisfied_by_gold`. **(b)** gold counterpart absent ⇒ enqueue on the **resample queue** — the selection input routed to the Q-A4 user gate. **(c)** Pending disposition, flagged records are excluded from *clean-training* designation at base fidelity (the dqa's "do not train on this trajectory yet", honored at stratum-composition level) but remain in the store and diagnostics.
6. **Supplementary variant (optional, not canonical):** the perpendicular form `SASD⊥_i = Δt_i·‖a⊥‖/max(‖v‖, v_floor)` (`a⊥ = ‖a − (a·v̂)v̂‖`) may be computed in addition as a turning-rate diagnostic; it must not replace the full-norm form and has no flag authority (see Reasoning).
7. **Known floor effect, documented:** an encounter completing entirely *between* two snapshots is invisible to any endpoint-evaluated metric; SASD bounds resolution adequacy from the data that exists and is complemented by IPR (Q-C3), which probes between snapshots via the interpolant. The pairing is the design.

**2. Reasoning.** The dqa's `SASD_i = Δt_i·‖a(t_i)‖/‖v(t_i)‖` is the only packaged definition (re-verified: the dqa text is left-endpoint literal), so the adjudication completes its unspecified slots. **Aggregation:** per-body max beats a stacked 9-component norm because stiffness is local — one body whipping through periapsis sets the timescale while the others drift, and a stacked norm dilutes exactly that signal (≈ √3 understatement when one body dominates, worse when the fast body's `v` is small while the slow bodies' `v` is large). **Endpoints (the fork):** both-endpoint max beats the dqa-literal left endpoint for one reason — the last interval before a flagged snapshot is the under-resolved one, and left-evaluation misses a spike that arrives at `t_{i+1}`; in particular the final snapshot of the trajectory is otherwise never evaluated at all. Both-endpoints can only *raise* `max SASD` relative to left-endpoint, so it cannot un-flag anything the literal form flags; it strictly closes a blind spot at the cost of one extra force evaluation per interval. **Full norm vs perpendicular:** the perpendicular form's motivation (fast-but-straight motion interpolates fine, so don't flag it) fails in the **near-radial close encounter** — precisely this dataset's hardest structure — where `a ∥ v` on approach, `a⊥ → 0`, and the perpendicular SASD reads *quiet* while `‖v‖` collapses toward the turning point and the true dynamical timescale shrinks; the full-norm form diverges there, correctly. A conservative screen should over-flag the benign case rather than under-flag the catastrophic one; hence full-norm canonical, perpendicular optional. This blindness argument originated as consolidator-original in CR-B (no report and no spec states it); this pass re-checked the geometry (on a radial approach `a` and `v` are collinear along the line of centers, so the rejection is sound) and **adopts it, flagged as a consolidation-generation argument the project should weigh directly since it decides the fork.** **Threshold semantics:** `SASD ≈ 0.5` means the local dynamical time is ~2 sampling intervals — a Nyquist-flavored warning level with no derivation in the package, hence provisional. **Disposition:** the dqa says "flag for resampling; do not train on this trajectory yet"; the gold-aware reading turns that into an executable rule (the gold file *is* the resample for the 2,565 covered standard IDs) and produces, as a by-product, the principled selection input Q-A4's residue needed.

**3. Evidence.** Master: Q-C2 block; HC-4. Addendum: no CLM row (definition question); CLM-09 confirmed (the 16×/2× resolution context behind the floor effect). Specs (re-verified): `data_quality_assessment.md` §3.2 (definition `Δt_i·‖a(t_i)‖/‖v(t_i)‖`; flag > 0.5; "do not train yet"; the curvature parenthetical licensing clause 6), §5.1 Phase-2 placement; `pinn_architecture.md` HC-4; `ctl_instruction.md` Step-1 item 4 (timestamps-not-nominal-dt precedent); `sampling_method.md` `MIN_DISTANCE_THRESHOLD = 0.01` (prescreen scale, re-verified). Issue doc: lines ~143–153 (training-loop weighting role → doc-03).

**4. Confidence.** Medium. The form is well-determined by the sources plus the adjudicated completions; the **0.5 constant and the flag's stratum-level consequence are provisional** pending the per-variant `max SASD` distribution — if a large fraction of admitted standard-base trajectories flag, the threshold or the clean-training consequence must be re-tuned at the user gate rather than silently starving Stages 3–4.

**5. Verification suggestion.** Compute the `max SASD` distribution per (variant, fidelity) over the admitted set; report flag rates and the overlap of {flagged ∩ gold-missing} with the CLM-04 184-set (the Q-A4 selection input). Unit tests: an analytic two-body eccentric orbit — flag trips iff `dt_out` is coarsened past the periapsis timescale; a near-radial plunge fixture — full-norm flags, perpendicular stays quiet (regression-protects the clause-6 demotion); a `v ≈ 0` snapshot sets `v_floor_hit` without NaN/Inf; a trajectory whose acceleration spike sits at the final snapshot — both-endpoint form flags it, a left-endpoint implementation does not (regression-protects the fork decision).

**6. Proposed specification text.** Target: `ctl_instruction.md`, new subsection "Data-side quality-metric contracts (SASD, IPR, PSC)" placed after the Step-1A gate (SASD clause; Q-C3/Q-C4 add theirs):

```
SASD (Stiffness-Aware Sampling Density) — data-side contract.
For each interior interval i between consecutive parsed snapshot times:
    SASD_i = dt_i * max over bodies b and endpoints t in {t_i, t_(i+1)} of
             ( ||a_b(t)|| / max(||v_b(t)||, 1e-12) )
where dt_i = t_(i+1) - t_i from the file's own timestamps, and a_b is the
ANALYTIC Newtonian acceleration from snapshot positions with Plummer softening
eps = 1e-10 (validation epsilon; HC-4). Accelerations are never
finite-differenced from the snapshot grid. The quantity is dimensionless and
identical in raw and scaled units; compute on raw parsed arrays by convention.
FLAG (do not auto-reject) any trajectory with max_i SASD_i > 0.5 [provisional
constant — revisit against the admitted-set distribution]. Persist per
trajectory: max SASD, argmax interval, v_floor_hit. Disposition of flagged
records: if a gold counterpart exists, mark satisfied_by_gold (the gold record
is the resample); if absent, enqueue on the resample queue surfaced to the
gold-rerun user gate (Q-A4 residue). Pending disposition, flagged records are
excluded from clean-training designation at base fidelity but retained in the
store and diagnostics. The perpendicular-acceleration variant
(dt * ||a_perp|| / max(||v||, 1e-12)) MAY be computed as a supplementary
turning-rate diagnostic; it has no flag authority and must not replace the
full-norm form (it is blind to near-radial encounters where a is parallel
to v). Training-loop uses of SASD (collocation weighting) are doc-03 scope.
```

**7. Consolidation provenance.** **CR-A:** scalar family `Δu·‖a'‖/max(‖v'‖, 1e-12)` in scaled/normalized-time units, **left-endpoint evaluation** (dqa-literal), per-body, flag 0.5, `speed_floor_used` metadata, perpendicular form demoted to `SASD_perp` diagnostic. **CR-B:** the same family with **both-endpoint evaluation**, the invariance statement plus raw-units recommendation, analytic-ε accelerations made explicit, the gold-aware three-way disposition, and the near-radial argument for the perpendicular demotion. **Decisions:** (i) *Endpoints — genuine fork; CR-B's both-endpoints adopted*: it strictly dominates the literal form (only raises the max; closes the final-snapshot blind spot; one extra evaluation per interval), and the dqa's left-endpoint text is read as the simplest statement of a sampled quantity rather than a deliberate exclusion of the right endpoint. CR-A's literal reading is the preserved dissent and the safer choice *if* the project insists on zero deviation from the dqa text. (ii) *Units — not a substantive fork*: SASD is scale-invariant (re-derived), so CR-A's scaled convention and CR-B's raw recommendation produce identical numbers; raw is adopted purely for uniformity with the other metrics. (iii) *Perpendicular demotion — unanimous between the consolidations*; the deciding blindness argument is consolidator-original (CR-B generation), re-verified and flagged here. Secondhand R1–R8 picture (non-authoritative): scalar family + 0.5 flag majority; perpendicular-as-canonical 2 (R1, R2 — the preserved upstream dissent); a system-norm aggregation (R8) rejected by both consolidations on the dilution argument; R3's adaptive `v_floor` rejected (dataset-dependent metric); R6 unaddressed.

### §5.3 Q-C3 (IPR) — Interpolation Physics Residual (data-side; dual-epsilon)

**1. Final verdict / recommendation.** The data-side IPR contract:

1. **Interpolant — pinned to the data the files actually carry:** per body and per coordinate, `CubicHermiteSpline(t, q, dydx = v)` over the parsed snapshot times — the cubic Hermite interpolant whose slopes are the file's own **velocities**. **`PchipInterpolator` is prohibited** for this metric: despite the dqa's "PCHIP" name, PCHIP *estimates* slopes from positional shape (Fritsch–Carlson construction) and **discards the velocity data**, changing the interpolant and therefore the metric. The dqa's name is treated as a misnomer for "piecewise cubic Hermite", which its own `(q_i, v_i)` input list confirms (re-verified).
2. **Evaluation points — deterministic:** `M = 10` interior points per interval at mid-offsets `τ_{i,j} = t_i + (j − ½)·Δt_i/10`, `j = 1..10` (never at the knots; never random, so the flag is reproducible). Per-trajectory `M_total = 10·(n_snapshots − 1)`.
3. **Residual — locked epsilon:** at each `τ`, `r(τ) = q̈_spline(τ) − F_grav^{ε=1e-10}(q_spline(τ))` with the **analytic Plummer-softened force at the validation ε = 1e-10** (HC-4-entailed: IPR is a pre-training data-quality metric, hence validation-side by function). Spline second derivatives are analytic (`.derivative(2)`), never finite-differenced.
4. **Aggregation — pinned (resolves a real ×3 ambiguity):** `IPR = (1/M_total) · Σ_k ‖r_k‖²` with `r_k` the **stacked 9-component** residual — the literal reading of the dqa's `‖d²q/dt² − F‖²` with `q` the full state. (A per-body `1/(3M_total)` normalization reads three times smaller against the same gate; one convention had to be pinned and the dqa-literal form wins.)
5. **Units — pinned:** computed in **raw G = 1 units** on parsed arrays. The quantity is dimensionful (acceleration², scaling as `D²/T⁴` — a factor ≈ 464 between scaled and raw under the locked constants, re-derived by this pass: raw IPR ≈ scaled IPR × 2.155e-3, equivalently scaled reads ×≈ 464 larger), so the threshold is meaningless without this statement.
6. **Flag rule (provisional constant):** `IPR > 1e-3` (raw units) ⇒ flag, with the same flag-not-auto-reject semantics and disposition routing as SASD (§5.2 clause 5, mutatis mutandis); persist `IPR`, the max per-interval contribution, and its interval index. The 1e-3 is the dqa's stated value, provisional pending the admitted-set distribution.
7. **The issue doc's `ε = 1e-5` is rejected for the data-side metric and re-housed, not erased:** an IPR-like quantity at the training softening is a *different metric* with a legitimate doc-03 role (the ALM noise-floor / achievability bound the issue doc is actually describing). If doc-03 adopts it, it must carry a distinct name (`IPR_train`); the two are not numerically comparable (the softened force differs from the validation force exactly in the close-encounter regime IPR probes, so an `ε = 1e-5` IPR systematically under-reports the aliasing signal).
8. **Interaction with SASD:** IPR probes *between* snapshots via the interpolant and closes SASD's floor effect (§5.2 clause 7); a trajectory can pass one and fail the other — both flags are independent metadata.

**2. Reasoning.** Two decisions carry the question. **Epsilon** is not a judgment call: HC-4 assigns ε by *function* (validation metrics: static 1e-10; training loss: 1e-5); IPR's function is pre-training data screening, so 1e-10 is entailed. The "measure what the network can achieve" impulse behind the 1e-5 choice is exactly the doc-03 noise-floor role, preserved via clause 7 without the constraint violation. **Construction** is where positions silently diverged while appearing to agree: "PCHIP" with `(q_i, v_i)` inputs is incoherent — SciPy's `PchipInterpolator(t, q)` accepts no derivative argument and synthesizes slopes from shape, so feeding it this data discards every velocity and yields a different spline whose second derivative differs most near encounters. The `CubicHermiteSpline(t, q, dydx=v)` formulation with an explicit prohibition is adopted because it is the only statement that makes the wrong call impossible to implement innocently. Remaining completions are forced choices: deterministic vs random points (a reproducible flag needs determinism), stacked vs per-body norm (a genuine ×3 gate ambiguity, pinned dqa-literal), and units (a ×≈464 ambiguity — the largest silent fork in the cluster, see part 7). A proposed sanity check "verify IPR(1e-10) ≥ IPR(1e-5) always" is **not adopted**: softening changes the force model, not monotonically the residual of a fixed interpolant against it; the inequality has no proof and a plausible counterexample regime. The adopted check (material divergence of the two ε-variants only when `min separation ≲ 1e-3`) tests the actual mechanism.

**3. Evidence.** Master: Q-C3 block (poses the dual-ε question); HC-4. Addendum: no CLM row. Specs (re-verified): `data_quality_assessment.md` §3.3 (the `(q_i, v_i)` input list; "PCHIP" naming; 10 points/interval; the `‖·‖²` residual form; gate "> 1e-3 — Reject or Resample"); `pinn_architecture.md` §3.2 (dual-ε; the training residual this metric must not be confused with); `ctl_instruction.md` dual-ε note. Issue doc: lines 155–165 (the `ε = 1e-5` claim, re-housed by clause 7). External (carried; References): SciPy `CubicHermiteSpline` and `PchipInterpolator` documentation; Fritsch & Carlson (1980).

**4. Confidence.** High on clauses 1–3 and 7 (constraint- and construction-entailed). Medium on the gate constant, units pinning, and aggregation pinning — each is the best-sourced choice available, but 1e-3 has no derivation. The single factor most likely to force revision: an admitted-set distribution showing `1e-3` (raw) flags a large fraction of *gold* trajectories — which would indicate the threshold was authored against a different unit convention and must be re-anchored. The dqa's own gate verb ("Reject or Resample") is stronger than the flag semantics adopted here; the demotion to flag-with-disposition follows the same conservatism as SASD (no auto-reject on a provisional, unit-ambiguous constant) and is recorded as a deliberate softening.

**5. Verification suggestion.** Analytic two-body fixture: IPR decreases ~`Δt⁴`-fashion under grid refinement (Hermite order check) and passes at gold spacing. Construction regression: the same trajectory through `CubicHermiteSpline(t, q, dydx=v)` vs `PchipInterpolator(t, q)` produces materially different IPR near a close encounter. Dual-ε probe: the 1e-10 and 1e-5 variants diverge materially only on trajectories with `min separation ≲ 1e-3`. Determinism: two runs, bitwise-identical `IPR`. Distribution: per-(variant, fidelity) admitted-set IPR histograms, flag rates, overlap with SASD flags.

**6. Proposed specification text.** Target: `ctl_instruction.md`, the "Data-side quality-metric contracts" subsection (IPR clause):

```
IPR (Interpolation Physics Residual) — data-side contract.
Interpolant: per body and per coordinate, CubicHermiteSpline(t, q, dydx = v)
over the parsed snapshot times — the file's velocities are the slopes.
PchipInterpolator is PROHIBITED for this metric (its shape-derived slopes
discard the velocity data; the dqa's "PCHIP" is a naming artifact for
"piecewise cubic Hermite", as its (q_i, v_i) inputs show).
Evaluation points: M = 10 deterministic interior points per interval,
tau_(i,j) = t_i + (j - 1/2) * dt_i / 10, j = 1..10; never at knots; never
random. Residual: r(tau) = d2q_spline/dt2(tau) - F_grav(q_spline(tau)) with
the ANALYTIC Plummer-softened force at the VALIDATION epsilon = 1e-10 (HC-4).
Spline second derivatives are analytic (.derivative(2)), not
finite-differenced. Aggregate: IPR = (1/M_total) * sum_k ||r_k||^2 over the
stacked 9-component residual, M_total = 10 * (n_snapshots - 1). UNITS: raw
G = 1 (the quantity scales x~464 between scaled and raw; the threshold is
unit-bound). FLAG (not auto-reject) if IPR > 1e-3 [provisional constant —
calibrate against the admitted-set distribution]; persist IPR, max interval
contribution, and its index; disposition follows the SASD flag-routing
clause. An epsilon = 1e-5 variant is NOT this metric: if adopted by doc-03 as
the training noise floor it must be named IPR_train and is not numerically
comparable to IPR.
```

**7. Consolidation provenance.** **CR-A:** cubic Hermite from positions+velocities over **normalized time in scaled coordinates**, 10 deterministic interior points at `u_j + ℓ·Δu_j/11`, `ε_inv = 1e-10`, `IPR = (1/M)Σ‖R‖²` over the concatenated 9-vector, flag > 1e-3, `ε = 1e-5` rejected, PCHIP terminology corrected. **CR-B:** the same construction, ε, aggregation, and flag, with three pins CR-A lacks: **raw G = 1 units** with the ×≈464 statement, the explicit `PchipInterpolator` prohibition (vs terminology correction), and mid-offset evaluation points `(j−½)Δt/10`. **Decisions:** (i) *Units — genuine fork, the consequential one*: the two reports' IPR values would differ by ×≈464 against the same `1e-3` gate. CR-B's raw units adopted: the dqa runs IPR in Phase 1 *on load*, before the scaling transform exists in the pipeline order, and raw matches the Q-C1/Q-C2 convention; CR-A's scaled-units choice is internally coherent but would demand the threshold be re-derived rather than carried. Preserved as the dissent; the verification item about gold flag rates is the empirical test that would expose a wrong pin. (ii) *Evaluation points — immaterial fork*: both are 10 deterministic interior points excluding knots; mid-offset adopted, `ℓ/11` recorded as an equivalent alternative. (iii) Everything else unanimous, including the ε adjudication and the `IPR_train` re-housing. Secondhand R1–R8 picture (non-authoritative): ε = 1e-10 carried by 6 of 7 addressers, with the single `ε = 1e-5` position rejected by both consolidations as an HC-4 violation; the Hermite-vs-PCHIP confusion was caught by a report minority; a per-body `1/(3M)` normalization existed upstream (the ×3 ambiguity clause 4 pins); a monotonicity check `IPR(1e-10) ≥ IPR(1e-5)` was rejected as unproven. Dissents preserved: scaled units (CR-A), per-body normalization, ε = 1e-5, monotonicity check.

### §5.4 Q-C4 (PSC) — Phase Space Coverage entropy (data-side)

**1. Final verdict / recommendation.** The data-side PSC contract — a **dataset-level, report-only** diversity diagnostic; no per-trajectory gate, no reject authority. *The population/weighting construction (clause 5) is a consolidator synthesis of the two received consolidations' complementary fixes and is flagged as such.*

1. **Population:** all snapshots of all **admitted** trajectories (post Step-1A; quarantined and rejected records excluded — coverage claims must describe data that can actually train).
2. **Coordinates per snapshot:** compute the three pairwise separations **in scaled units** (the locked `r' = r/D`), sort them, take `(d_min, d_mid)`, and bin `(log₁₀ d_min, log₁₀ d_mid)`. Sorting makes the coordinates permutation-invariant (body labels are gauge); the log makes decades of separation — the structure that matters for close-encounter coverage — visible to a uniform grid. Scaled units are required so the clause-6 SCR threshold is the *same number* as the locked Stage-6 criterion (`s_min < 0.5`, a scaled quantity).
3. **Grid (fixed, not data-adaptive; constants provisional):** uniform in log space over `[1e-3, 1e2]` per axis (floor = the generation-time prescreen scale 0.01, with one decade of margin; ceiling above any bound system's excursions), **25 bins per axis, K = 625**, out-of-range values clamped to edge bins and counted (a non-trivial clamp rate is itself a finding). Fixed edges are required so per-population entropies are comparable; quantile edges would make every population's grid different and the numbers incommensurable.
4. **Estimator:** occupancy probabilities `p̂_k`; plug-in Shannon entropy `H = −Σ p̂_k ln p̂_k` (nats; base documented), reported with `H_norm = H/ln K ∈ [0, 1]` (full-`K` denominator) and the occupied-bin count. For unweighted populations the **Miller–Madow term `(K_occupied − 1)/(2N)` is computed and reported, not silently added** — at this dataset's scale it is negligible, and reporting it proves that.
5. **Reporting axes (the synthesis):**
   - **Per (variant, fidelity):** four unweighted populations (within one population the verified snapshot spreads are tight — 59–61, 126–127, 1002–1003 — so per-trajectory weighting is immaterial there and the plain estimator plus MM term applies).
   - **Deduplicated, equal-record-weighted pooled:** one record per `physical_key`, **preferring the gold record** where both exist (removes the base/gold double-count of the same physical system); each surviving record's snapshots weighted `1/N_t(record)` so **every record contributes equal total mass** (removes the within-pool resolution skew — without it, the 184 base-only standard ICs would each contribute ~61 snapshots against ~1003 from every gold-backed IC, a ~16× under-representation of exactly the gold-gap population). `p̂_k` = weighted occupancy / total weight. For this weighted population the MM term's `N` is ill-defined; report the effective sample size `N_eff = (Σw)²/Σw²` and the MM term computed at `N_eff`, explicitly labeled approximate.
   - The naive all-snapshot pooled value is **not a deliverable** (resolution mix and duplication confound it).
6. **Companion scalar (the actionable one):** `SCR = N(d_min < 0.5)/N` per population (weighted where the population is) — the Stiffness Coverage Ratio, the occupancy of the close-encounter region the dqa's `r_min → 0` bin check gestures at, with 0.5 matching the locked Stage-6 criterion so the number is curriculum-meaningful. An empty or near-empty close-encounter region is the finding PSC exists to surface.
7. **Consequence model:** PSC/SCR inform dataset-curation and IC-generation decisions at the user gate; they never reject trajectories; PSC-governed replay is doc-03 scope.
8. **Optional secondary (recorded, not required):** a trajectory-level invariant-space entropy — one point per admitted `physical_key` in normalized `(E/E_scale, L_norm, log s_min)`-style coordinates — measures *IC-diversity*, a different, compatible diagnostic; if adopted later it carries its own name and is not PSC.

**2. Reasoning.** This is the cluster's only fully open design question: the dqa supplies a concept (occupancy entropy over a discretized grid), one worked example (the `(r₁₂, r₂₃)` plane), and one operational check (the `r_min → 0` bin) — re-verified — and leaves grid, estimator, weighting, and population unstated. The adopted construction stays closest to the packaged intent (snapshot-occupancy entropy in configuration space) and fixes the defects the candidate constructions collectively exposed: label dependence (unsorted `(r₁₂, r₂₃)` depends on body labels; sorting removes it at zero cost), scale blindness (linear bins over a range reaching 1e2 collapse every close encounter into an edge bin; log axes are forced by the physics), dimensionality (6-D grids are either unestimable at this sample size or, under a generic bin-count rule, resolve ~2 bins per axis — useless; the 2-D log configuration grid is the largest construction the data can support *and* compare), and the **two-layer pooling confound**: a gold trajectory contributes ~16× the snapshots of its base twin (verified: 1003 vs 61), and 2,565 physical systems appear twice. CR-B's dedup-prefer-gold removes the duplication but leaves a ~16× under-weighting of the 184 base-only ICs inside the pooled number; CR-A's equal-record weighting removes the resolution skew but, applied without dedup, still double-counts 2,565 systems (at twice the mass of a base-only IC). **Each consolidation fixed one layer; the composition fixes both, and neither fix interferes with the other** — this is a genuine synthesis of compatible elements, not a compromise, and it is the principal consolidator-original content of this question (flagged accordingly; the project should sanity-check the composed weighting on the first run). The `H_norm` denominator is pinned to full `ln K` rather than `ln K_eff`/`ln K_occupied`: an occupied-bin denominator makes `H_norm` partially self-referential (a dataset covering few bins uniformly would score `H_norm ≈ 1`, hiding exactly the coverage gap PSC exists to expose), while the full-K form keeps "fraction of the designed grid covered, evenness-weighted" semantics; the occupied count is still reported separately. Scaled-unit pinning follows from the SCR/Stage-6 anchor (clause 2): in raw units the 0.5 would be a different physical separation and the curriculum linkage would silently break.

**3. Evidence.** Master: Q-C4 block. Addendum: CLM-09/CLM-10 confirmed (the 16×/61-vs-1003 confound arithmetic); no PSC CLM row. Specs (re-verified): `data_quality_assessment.md` §3.4 (definition; `(r₁₂, r₂₃)` example; `r_min → 0` bin check), §5.3 (diversity-check placement); `ctl_instruction.md` Stage-6 criterion (`s_min < 0.5` — the SCR anchor; a scaled quantity) and §2.5 scales (clause-8 coordinates); `sampling_method.md` prescreen 0.01 (the grid floor's anchor). Issue doc: PSC recitation lines 167–169 (replay role → doc-03). External (carried; References): Shannon (1948); Miller (1955); Paninski (2003).

**4. Confidence.** Medium. The metric's *role* (report-only, per-population + dedup-weighted-pooled, SCR companion) is firmly determined by the packaged intent plus the verified confound arithmetic; the **grid constants (range, 25 bins, the 2-D choice) are provisional design**, and the composed weighting is consolidation-original. The single factor most likely to change the construction: a demonstrated need for velocity-coverage claims (e.g., doc-03 replay design wanting kinetic diversity), which would add a documented coarse 3rd/4th axis rather than reopen the 2-D core.

**5. Verification suggestion.** One pass over the admitted set: per-population and dedup-weighted-pooled `H`, `H_norm`, occupied-bin counts, MM terms (assert ≪ `H`; pooled at `N_eff`, labeled approximate), clamp rates, and SCR; a bin-resolution sweep (15/25/40 per axis) confirming `H_norm` *ranking* stability across populations; the 2-D occupancy heatmaps themselves (the human-readable deliverable). Unit tests: body-label permutation leaves all numbers bitwise identical; a synthetic two-cluster fixture yields the analytic entropy; clamp counting trips on an out-of-range fixture; a fixture pool of one gold-backed and one base-only IC contributes exactly equal total mass under the clause-5 weighting (regression-protects the synthesis).

**6. Proposed specification text.** Target: `ctl_instruction.md`, the "Data-side quality-metric contracts" subsection (PSC clause):

```
PSC (Phase Space Coverage entropy) — data-side contract (REPORT-ONLY; no
gate). Population: all snapshots of ADMITTED trajectories (post Step-1A).
Per snapshot: compute the three pairwise separations in SCALED units (r/D);
sort; take (d_min, d_mid); bin (log10 d_min, log10 d_mid) on a FIXED uniform
grid over [1e-3, 1e2] per axis, 25 bins/axis (K = 625) [provisional
constants], clamping out-of-range values to edge bins and counting clamps.
Estimator: plug-in Shannon entropy in nats over occupancy probabilities,
reported with H_norm = H / ln K (full-K denominator), the occupied-bin count,
and the Miller-Madow term (K_occ - 1)/(2N) REPORTED (not added).
Reporting axes:
  (a) per (variant, fidelity) population, unweighted;
  (b) a deduplicated, equal-record-weighted pooled population: one record per
      physical_key, preferring gold; each record's snapshots weighted
      1/N_t(record) so every record carries equal total mass; for this
      weighted population report N_eff = (sum w)^2 / (sum w^2) and the MM term
      at N_eff, labeled approximate.
The naive all-snapshot pooled value is NOT a deliverable (resolution mix and
base/gold duplication confound it). Companion scalar: SCR = N(d_min < 0.5)/N
per population (0.5 matches the Stage-6 s_min criterion in scaled units).
Consequences: PSC/SCR inform dataset-curation and IC-generation decisions at
the user gate; they never reject trajectories. PSC-governed curriculum replay
is doc-03 scope. A trajectory-level invariant-space entropy (one point per
physical_key in normalized (E, L_norm, log s_min) coordinates) is an OPTIONAL
secondary diagnostic under its own name; it is not PSC.
```

**7. Consolidation provenance.** **CR-A:** fixed 25×25 log grid on sorted **scaled** `(d_min, d_mid)` over `[1e-3, 1e2]`; **equal-trajectory weighting** (`1/N_t` per snapshot, all trajectories); `H_norm = H/log K_eff` (occupied-bin denominator); per family/fidelity + pooled; weighted `Pr(d_min < 0.5)` companion; no gate; consolidator-original grid flagged. **CR-B:** the same grid family with full-`K` `H_norm`, the **dedup-prefer-gold** pooled population, the MM term reported-not-added, the explicit not-a-deliverable rule for naive pooling, the SCR/Stage-6 anchoring, and the invariant-entropy demotion to optional secondary. **Decisions:** (i) *Confound mechanism — genuine fork, resolved by synthesis*: CR-A's weighting and CR-B's dedup each fix one layer of the two-layer pooled confound (resolution skew; base/gold duplication) and are mutually compatible; the composition is adopted and **flagged consolidator-original** — this is the one construction in the document that exists in neither input, argued above from the verified 61-vs-1003 arithmetic and the 184-ID structure. (ii) *`H_norm` denominator*: CR-B's full `ln K` adopted over CR-A's `K_eff` (self-referentiality argument in the Reasoning); occupied count still reported. (iii) *Units*: CR-A's explicit scaled pinning adopted and made load-bearing via the SCR/Stage-6 anchor (CR-B's text anchors SCR to Stage-6 but leaves units implicit — composing the two closes that gap). (iv) *MM handling*: CR-B's report-not-add adopted, extended with the `N_eff` rule this pass adds because the synthesis makes the pooled population weighted (a consequence neither input had to face). Both consolidations agree on: no gate, fixed edges, log axes, sorted distances, admitted-set population, invariant-entropy as optional secondary. Secondhand R1–R8 picture (non-authoritative, and worth consulting after Q-A4): fully split — five constructions across six addressers (6-D quantile, 6-D unsorted, literal linear `(r₁₂, r₂₃)`, trajectory-level invariant entropy ×2, 2-D sorted log) — with both consolidations independently rejecting the 6-D and linear forms on estimability/scale-blindness grounds and demoting the invariant-entropy constructions to the optional secondary. All upstream dissents preserved through that record.

---

## §6 Cross-cutting consolidated findings

Findings that fall outside any single Q-ID but inside issue-02 scope. F-1 through F-8 were surfaced by the first-generation reports and carried by one or both received consolidations; each was re-checked by this pass where the inputs permit (the spec-side facts were re-verified directly; the R6-specific claims in F-7 are necessarily secondhand). F-9/OI-12 is original to this pass.

**F-1 — `tab:brutus_compare` count transposition in `ctl_instruction.md` (precondition satisfied; correction can proceed).** The spec's comparison table swaps the Set 1b / Set 2a populations relative to the verified folder counts — **re-verified directly by this pass**: the snapshot's table row for Set 1b reads 4,857 where the verified standard-base count is 2,749, and Set 2a reads 2,749 where the verified hierarchical count is 4,857. The consistent set: hierarchical base 4,857 / standard base 2,749 / hierarchical gold 4,857 / standard gold 2,565 (total 15,028). The correction was originally proposed conditional on count verification; the addendum confirms all four (CLM-05a/05b/06; Correction 1), so the precondition is met. Disposition: spec-hygiene edit to `ctl_instruction.md` with the verified numbers; no methodology consequence.

**F-2 — `E_scale` floor three-way conflict.** Resolved inside Q-B4 (§4.4, verdict clause 3): canonicalized at `1e-8` (the value of `pinn` §5.2 line 761 and the `ctl` Step-4 table line 1049 — both re-verified); `ctl` §2.5 line 608's `1e-10` is the outlier. The 2-of-3, network-facing-governs rationale is a judgment, flagged as such in §4.4.

**F-3 — Issue-doc internal-defect catalog (for EVID-10).** Defects established across this consolidation, beyond the per-question verdicts: (1) the `>= 200` snapshot floor — verified-fatal (Q-A1); (2) the M12 BLOCKING claim and P1-4's contradiction with the doc's own checklist (`gold → 128`) (Q-B1); (3) the `compute_globals` listing's mixed convention — mass-fraction `D` with raw-mass energies (Q-B4); (4) the additive-ε potential in the same listing — the PHYS-03 anti-pattern (Q-B4); (5) the SCS ratio thresholds — a band boundary mis-promoted to a gate plus an unsourced `1e-8` (Q-C1); (6) the IPR `ε = 1e-5` assignment — an HC-4 violation when read as data-side (Q-C3); (7) the D7 premise errors — "minimal footers" and "schema varies", contradicted by the corrected disk facts (Q-A5); (8) the WR-01 sample-size self-contradiction (1,000 vs 100) (Q-B2). Items 1–5 and 7–8 were re-verified against the issue-doc snapshot by this pass; item 6 is constraint-arithmetic. None of these defeats the issue doc's *problem reports* — B-06, B-11, M11, M13, D7, and M12's underlying observation all identified real gaps; the defects concentrate in its *proposed resolutions and parameters*.

**F-4 — Master framing correction: "spec is silent on a mass-drift protocol" is incomplete.** Resolved inside Q-B2 (§4.2): `ctl` §2.1 already carries the float64 absolute-`1e-15` mass-invariance gate and an IC↔Brutus consistency clause (re-verified); what was missing is the cross-file formula, explicit tolerance arguments, and escalation path.

**F-5 — `trustworthy_horizon` undefined.** The `ctl` §2.6 metadata schema names a `trustworthy_horizon` field (re-verified at line 648) that no package document defines. Disposition: marked **RESERVED** in the Q-A5 spec text (writers emit null; readers must not consume) and registered as OI-4. Inventing a definition would be fabrication.

**F-6 — `DELIVERY-NOTE.md` not provided (input-integrity note).** Named in the master's manifest (D-16); not provided to this pass, and — per both consolidations — not provided to them nor to R1–R4. The master is self-contained for the framed questions, so no verdict depends on it; registered under Additional Input Needed (OI-1) so the project can confirm nothing gate-relevant lived only there.

**F-7 — R6 input-integrity findings (secondhand; consolidation-level).** Both consolidations report, consistently with each other, that R6's master snapshot was truncated before the framed-questions and CLM sections, with traceable consequences (issue-doc-keyed structure; adoption of the verified-fatal `>= 200` floor; a full M16 answer excluded as scope creep; stale SI-DQA-002 citation; an arithmetic error in its Q-A5 verification counts). This pass cannot re-verify any of this without the bundle (Additional Input Needed) and carries it as the consistent secondhand record. The process recommendation stands on its own merits: any re-run of external research rounds should use delivery verification (file hashes + section checksums acknowledged by the researcher).

**F-8 — CLM-10/CLM-11 probe-coverage gap (OI-6).** The addendum's corrected snapshot statistics carry sample sizes coinciding *exactly* with the footer-bearing populations of each folder (standard base n = 2,048; hierarchical base n = 3,307; standard gold n = 2,346; hierarchical gold n = 4,857) — **re-verified by this pass against both documents' counts**. Either the probe keyed on footer-bearing files, or the coincidence is fourfold. If the former: the 2,470 no-footer files' snapshot distributions are uncharacterized (bears on Q-A1's WARN-vs-reject escalation and Q-B1's residual cap pressure), and it is unknown whether the 70 DATA-05-quarantined IDs fall in the characterized set. CLM-11's prevalence qualifier "across probe-applicable files" is undefined and plausibly the same population. Registered as OI-6 with a one-pass probe extension specified in §3.1 part 5.

**F-9 — Addendum-internal transcription slip in the CLM-08 summary row (consolidator-original to this pass; OI-12).** The addendum's confirmed-claims summary row for CLM-08 describes the standard-gold population as "2,346 `tol=1e-13`". That figure is internally inconsistent with the verified record the addendum itself confirms elsewhere: the with-footer standard-gold population is 2,346 total, decomposed as **1,754 at `tol = 1e-13` plus 592 at `tol = 1e-14`** (the 592 being exactly the CLM-08 claim the row confirms), and the addendum's own "Not affected" clause re-derives the full tuple histogram. The row is read as a transcription slip for "2,346 **with-footer**" — the CLM-08 verification itself (592 at `1e-14`) is unaffected, and no verdict in this document depends on the slipped phrasing. Registered as OI-12 for the addendum maintainer to correct, because the candidate verdict source should not silently inherit a defect in its own authoritative correction channel.

---

## Open Items register

Consolidates the open items of both received consolidations (their registers map onto each other almost exactly; CR-A's nine entries are subsumed by CR-B's OI-1–OI-11 numbering, which is retained) plus this pass's additions (OI-12 and the Additional Input Needed entries).

| ID | Item | Type | Owner / route | What resolves it |
|---|---|---|---|---|
| OI-1 | `DELIVERY-NOTE.md` (D-16) not provided — to this pass, to either consolidation, or (per their records) to R1–R4 | Missing input | Package maintainer | Provide the file or confirm it contains no gate-relevant content beyond the master |
| OI-2 | Stage-conditional SCS tightening (the impulse behind the issue doc's `1e-8`): wanted or not | Insufficient evidence (partly doc-03) | User gate, after data | Per-(variant, fidelity) SCS distributions on the admitted set (Q-C1 verification); then an explicit decision layered on — never replacing — the locked gate |
| OI-3 | Provisional numeric constants adopted without package derivations: SASD flag 0.5 (and the canonical-vs-perpendicular calibration question); IPR flag 1e-3 in raw units (and the stacked-vs-per-body ×3 convention record); PSC grid `[1e-3, 1e2]` × 25 bins (K = 625) and the composed dedup+weighting; `n_pts_cap = 32` | Calibration pending | Phase 26/27/28 implementers → user gate | The admitted-set metric distributions specified in the Q-B1/Q-C2/Q-C3/Q-C4 verification items; re-tune at the user gate with data in hand |
| OI-4 | `trustworthy_horizon` (`ctl` §2.6, line 648) undefined anywhere in the package | Spec gap | Framework owner | Define the field or delete it; until then RESERVED (writers null, readers forbidden) |
| OI-5 | WR-01 documentary defect (issue doc's 1,000-vs-100 sample sizes); CLM-row disposition | Documentary / register hygiene | Phase-24 user gate (per addendum) | Decide whether WR-01 becomes a CLM row; operationally moot — Q-B2 adopts full coverage and DATA-05 already ran it |
| OI-6 | No-footer populations (2,470 files) uncharacterized by the CLM-10 snapshot probe (sample sizes match footer-bearing counts exactly); CLM-11's "probe-applicable" qualifier undefined; unknown whether the 70 quarantined IDs are footer-bearing | Insufficient evidence (F-8) | Phase-24 probe extension | One pass: per-variant `final_timestep` / `n_snapshots` / max-gap distributions split by footer presence, with the 70 quarantined IDs tagged. Unblocks the Q-A1 escalation decision and clears Q-B1's residual risk |
| OI-7 | Q-A4 residue: (a) Step-5 label-semantics ruling (labels attach to simulations vs IDs) — the entailment's defeater; (b) gold-rerun resourcing for any of the 184 gold-less ICs | Decision required | (a) Framework owner (one line); (b) User gate | (a) The ruling either ratifies the §3.4 spec text or activates the Phase-26 STOP gap exactly as the master annotates; (b) decide using the {SASD-flagged ∩ gold-missing} selection input (§5.2 clause 5b) |
| OI-8 | M11 consumption status (does the live loader enforce the blacklist?) | Empirical; outside grounding limits (SCOPE-10) | Phase 25 / FUT-01 | The live-pipeline probe the addendum defers; the Q-A3 contract stands regardless of the answer |
| OI-9 | DATA-05 remediation: targeted rerun of the 70 stale `brutus_hierarchical` outputs from current canonical ICs | Data remediation in flight | 24-DATA05-RERUN-REMEDIATION | Rerun lands → re-run the Q-B2 gate (assert 0 failures) → lift the quarantine clause in Step-1A item 2 |
| OI-10 | Deferred by scope: M16, G6, training-loop metric usage (SASD weighting, `IPR_train` noise floor, PSC replay) | Forward references | doc-03 | Out of scope by SCOPE-11. Note for doc-03 carried from the consolidations: one excluded first-generation report section reportedly contains a full M16 proposal; it was not adjudicated anywhere in this chain and is one unvetted candidate among others |
| OI-11 | CLM-13 formal disposition (`D = 6.694`): PENDING in the addendum, routed to EVID-10 (Phase 25) / PIPE-09 (Phase 27) | Adjudication routing | EVID-10 / PIPE-09 | Ratify the Q-B4 constraint-entailed rejection (this document is the candidate verdict source for that step) |
| OI-12 | Addendum CLM-08 summary-row phrasing "2,346 `tol=1e-13`" is internally inconsistent with the verified tuple decomposition (1,754 @ 1e-13 + 592 @ 1e-14 = 2,346 with-footer); read as a transcription slip for "2,346 with-footer" (F-9; consolidator-original to this pass) | Documentary defect in the authoritative correction channel | Addendum maintainer (Phase 24) | One-line erratum to the addendum row; no verdict here depends on the slipped phrasing |

### Additional Input Needed (this pass)

1. **`research-results-bundle.md` (reports R1–R8) — not provided to this consolidation pass.** Both received documents are themselves consolidations of R1–R8 and quote/characterize them extensively and *consistently with each other and with the task prompt's crosswalk*, but per ground rule 6 those characterizations are secondhand and were not weighable as primary argument here. Every "R1–R8" statement in this document's provenance sections is marked non-authoritative on that basis. The quality bar instructs the project to consult the underlying reports where provenance records ambiguity or a close call; on this document's record, the questions that warrant it are, in order: **Q-A4** (the genuine three-way upstream split and the label-semantics defeater), **Q-C4** (five distinct upstream constructions; the adopted weighting is a synthesis existing in neither input), **Q-C3** (the ×≈464 units fork — confirm no upstream report argued a scaled-units threshold derivation this pass has not seen), **Q-C2** (the endpoint fork and the perpendicular-canonical minority's full argument), and **Q-B2** (the absolute-vs-relative gate form, low stakes but a genuine fork). For the remaining nine questions the two consolidations agree in substance and the originals add provenance texture, not verdict risk.
2. **`DELIVERY-NOTE.md`** — see OI-1.

---

## References

### Package inputs (the evidentiary basis of every verdict)

1. `RESEARCH-CONTEXT-MASTER.md` — manifest, framed research questions (Q-IDs), hard constraints HC-1–HC-6, CLM claims register, consolidated dataset context, correction provenance. All Q-ID and CLM-ID anchors in this document resolve here.
2. `DATA-07-CORRECTION-ADDENDUM.md` (2026-06-11) — authoritative Phase-24 correction channel: Corrections 1–3; confirmed-claims table (CLM-01–CLM-09, CLM-11–CLM-12); CLM-10 corrected medians with min/max; DATA-05 findings and the RESOLVED-WITH-INSTRUCTION ruling; CLM-13 PENDING routing; WR-01/WR-03 notes. Supersedes the master's interim record wherever they overlap. (See OI-12 for one internal transcription slip identified by this pass.)
3. `specs-bundle.md`, containing the five delimited snapshots (split and read in full by this pass; all line citations in this document re-verified against these copies):
   - `specs/ctl_instruction.md` — framework spec; spec-edit target; PHYS-01 (§2.5, with the explicit 6.694 rejection), §2.1 mass gates, §2.6 metadata schema (incl. the undefined `trustworthy_horizon`, line 648), Step 1/Step 5 loader and stage contracts, the stage stratification and cumulative-replay text, Mini-Batch Construction (lines 1197–1201), the Step-4 table (`E_scale + 1e-8`, line 1049), the dual-ε note (~line 703), the Plummer anti-pattern text (~line 698), and `tab:brutus_compare` (the F-1 transposition).
   - `specs/pinn_architecture.md` — framework spec; spec-edit target; §3.1 batch sourcing, §3.2 `ε_train = 1e-5`, §3.4 training-side `ε_H` floor, §5.2 network input contract and `E_scale + 1e-8` (line 761), §10.2 acceptance checks.
   - `specs/data_quality_assessment.md` — read-only research report; **sole written home of the locked post-v1.3 SCS gate (SI-DQA-003)** and of the packaged SASD/IPR/PSC definitions (§3.1–§3.4, §5.1, §5.3). Non-authoritative except as that home; cited with that annotation throughout.
   - `specs/sampling_method.md` — FROZEN historical record (generation methodology; `Σm = 3` normalizations; `MIN_DISTANCE_THRESHOLD = 0.01` prescreen). Not a revision target.
   - `specs/02-data-pipeline-and-validation.md` — the issue doc; non-authoritative adjudication subject (B-06, B-11, M11, M12, M13, D7, D-03; P1-1..P2-2; the `compute_globals` listing; the SCS/SASD/IPR/PSC recitations).
4. `FINAL-ISSUE-02-RESOLUTION.md` (**CR-A**, 65 KB) and `issue-02-final-resolution.md` (**CR-B**, 154 KB) — the two independent consolidated resolution documents received and re-adjudicated by this pass. Candidate argued positions only, per ground rules; per-question dispositions in each resolution's part 7.
5. `research-results-bundle.md` (reports R1–R8) — **referenced by both CR-A and CR-B as their input; not provided to this pass** (Additional Input Needed, item 1). All R1–R8 attributions herein are secondhand reconstructions from the two consolidations' provenance records.

### External literature and documentation

Carried from the consolidations (which carried them from the first-generation reports); retained only where load-bearing. Each was verified *in kind* — the works exist and say what they are cited for at the level used here — but none was re-fetched during this pass; bibliographic details are as carried. Introducing chain in brackets.

6. h5py documentation — Groups and Datasets (dict-like groups; NumPy-like chunked/compressed datasets; attributes). [R1/R2 → CR-B] — Q-A6.
7. NumPy documentation — `numpy.lib.format` (`.npy` single-array; `.npz` multi-array wrapper); `numpy.finfo` (float64 ε ≈ 2.22e-16); `numpy.allclose` (default `atol = 1e-8`). [R1/R2/R4 → both CRs] — Q-A6, Q-B2, Q-B3.
8. Python Software Foundation — `decimal` module documentation. [R1/R2 → CR-B] — Q-B2, Q-B3.
9. SciPy documentation — `scipy.interpolate.CubicHermiteSpline` (caller-supplied derivatives) and `scipy.interpolate.PchipInterpolator` (shape-derived slopes; no derivative input). [R1/R2/R4 → both CRs] — decisive for Q-C3 clause 1.
10. Fritsch, F. N. & Carlson, R. E. (1980). "Monotone piecewise cubic interpolation." *SIAM J. Numer. Anal.* 17(2), 238–246. [R4 → CR-B] — Q-C3.
11. Goldberg, D. (1991). "What every computer scientist should know about floating-point arithmetic." *ACM Computing Surveys* 23(1), 5–48. [R4 → CR-B] — Q-B2/Q-B3 error budget.
12. Shannon, C. E. (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal* 27. [R1 → CR-B] — Q-C4.
13. Miller, G. (1955). "Note on the bias of information estimates." *Information Theory in Psychology*, 95–100. [R7 → CR-B] — Q-C4.
14. Paninski, L. (2003). "Estimation of entropy and mutual information." *Neural Computation* 15(6), 1191–1253. [R4/R7 → CR-B] — Q-C4 estimator regime.
15. Boekholt, T. & Portegies Zwart, S. (2015). "On the reliability of N-body simulations." *Computational Astrophysics and Cosmology* 2:2. [R4 → CR-B] — Brutus convergence background; CLM-09 context only.
16. Portegies Zwart, S. & Boekholt, T. (2014). "On the minimal accuracy required for simulating self-gravitating systems by means of direct N-body methods." *ApJL* 785:L3. [R4 → CR-B] — same context.
17. Wang, S., Sankaran, S. & Perdikaris, P. (2024). "Respecting causality for training physics-informed neural networks." *CMAME*. [R4 → CR-B] — causal-firewall motivation in Q-A1/Q-A3; motivational, not load-bearing.
18. Sitzmann, V. et al. (2020). "Implicit Neural Representations with Periodic Activation Functions." *NeurIPS*. [R7 → CR-B] — SIREN background; motivational only.
19. Rosenstein, M. T., Collins, J. J. & De Luca, C. J. (1993). "A practical method for calculating largest Lyapunov exponents from small data sets." *Physica D* 65(1–2), 117–134. [R7 → CR-B] — referenced by the spec's Lyapunov estimator; contextual only.

CR-A's References section deliberately carried no external literature ("final decisions rest on the supplied package"); CR-B carried the list above. This document follows CR-B's practice with the verification caveat stated, because several adopted verdict clauses (the PCHIP prohibition; the `allclose` warning; the MM term) lean on the documented behavior of named libraries, and citing them is more checkable than asserting the behavior bare.

---

*End of document. All fourteen framed questions (Q-A1–Q-A6, Q-B1–Q-B4, Q-C1–Q-C4) are resolved above, each with the seven required parts; cross-cutting findings F-1–F-9 and Open Items OI-1–OI-12 plus the Additional Input Needed register capture everything surfaced that no single question owns. Per the quality bar: the genuine forks between the two input consolidations were Q-B2 (gate form), Q-C2 (endpoint evaluation), Q-C3 (units — the consequential one), and Q-C4 (confound mechanism — resolved by a flagged synthesis); everywhere else the two agreed in substance and the adjudication selected the more transcription-complete statement. The questions on which consulting the original R1–R8 reports is most worthwhile are listed under Additional Input Needed.*
