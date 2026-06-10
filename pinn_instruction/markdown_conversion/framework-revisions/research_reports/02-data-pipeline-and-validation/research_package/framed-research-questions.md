---
id: framed-research-questions-02
status: DRAFT
phase: 23
topic: Issue-02 data pipeline & validation — neutral framed research questions
created: 2026-06-10
canonical: false
---

# Framed Research Questions — Issue 02: Data Pipeline and Validation

> **What this document is.** This is the task list for the external multi-AI
> research on issue 02 (data pipeline and validation). It poses every contested or
> unverified in-scope finding as an explicit, neutral question. It does **not**
> answer any of them — adjudication happens later, downstream of your research.
>
> **What this document is not.** It is not a set of decisions, not a verdict, and
> not an instruction to implement anything. Where a source proposes a fix, that
> proposal is reported as a *claim to be evaluated*, never as a settled answer.

## How To Read This Document

1. Read the **Source-Treatment Framing** first — it tells you which inputs are
   authoritative and which are not.
2. Treat the **Hard Constraints** as fixed. They are locked v1.4 conventions; your
   research must work *within* them, not re-open them.
3. Note the **Doc-03 Scope Boundary** — several tempting topics are explicitly out
   of scope for this research and must not be answered here.
4. Answer the questions in the three clusters that follow (Task 2 section).
5. Every dataset figure mentioned anywhere in this package carries a `CLM-` ID in
   the companion `claims-table.md`. Figures are *claims*, not established facts;
   reference them by their CLM ID and do not treat any unverified figure as true.

---

## Source-Treatment Framing (READ FIRST)

**Both the issue doc and its recommendations are NON-authoritative and may contain
errors.** The adjudication subject — `02-data-pipeline-and-validation.md` (the
intact snapshot under `specs/`) — and *especially* its "Recommended Resolutions"
(P1-1..P2-2) and "Open Decisions" sections are not authoritative. They are a
synthesis of an internal audit and several archived notes. The external research
must **adjudicate** these findings against the locked conventions and the dataset
facts — it must **not transcribe** the issue doc's proposed fixes as if they were
decisions.

**Worked example — why this matters (the seed conflict).** The issue doc states
ratio-based SCS thresholds: reject any trajectory with `SCS > 1e-6`, and tighten to
`SCS < 1e-8` for high-resolution data (issue doc lines 133–134). This **directly
conflicts** with the locked post-v1.3 SCS gate, where `SCS = log₁₀(ε_H)` and the
reject gate is `SCS > −5` (i.e. `ε_H > 10⁻⁵`). The issue doc's `1e-6` / `1e-8`
figures are *raw-ratio* numbers; the locked gate is a *log-drift* number — they are
not even the same quantity. This is one concrete demonstration that the issue doc
"may contain errors": do not assume any issue-doc number is correct without
checking it against the locked conventions and the dataset.

**The `pinn/` "Canonical" citation is OVERRIDDEN.** The issue doc's References list
cites `pinn/data-processing-pipeline-full.py` and `pinn/basic_architecture.py` as
"Canonical" (issue doc line 357). That citation is **overridden** (user directive
2026-05-19; SCOPE-10). The live `pinn/` code is **not** a grounding source for any
decision in this research. The **framework specs are the source of truth** — i.e.
the intact `ctl_instruction.md` and `pinn_architecture.md` snapshots in `specs/`.
Do not cite `pinn/` code as evidence.

---

## Hard Constraints — Locked v1.4 Conventions (verbatim)

These six conventions were locked during the v1.4 milestone (issue 01) and are
**fixed inputs** to this research. They are reproduced verbatim with their citation
into the intact spec snapshots in `specs/`. Do not re-open or contradict them; your
job is to adjudicate issue-02's data-pipeline findings *consistently with* them.

1. **14D input contract** — the network input is exactly
   `x_net = [τ, IC₁₃]`, with `τ = 2u − 1` and `u = t/T`.
   Source: `specs/ctl_instruction.md` Step 4 "Network input contract" (≈ lines
   1000–1011; equation at 1005); restated in `specs/pinn_architecture.md` §5.2
   "Network Input Contract" (751–762). Locked Phase 17 (IO-01).

2. **Jacobi IC₁₃ vector** — the 13-component initial-condition vector is
   `IC₁₃ = [m₁, m₂, m₃, ρ_x, λ_x, λ_y, ρ̇_x, ρ̇_y, ρ̇_z, λ̇_x, λ̇_y, λ̇_z, E]`,
   where the mass entries are *raw masses before normalization*.
   Source: `specs/ctl_instruction.md` Step 4 (≈ lines 1011–1019); Jacobi vectors
   §2.4; validity note (PHYS-06) at line 961. Locked Phase 17 (IO-02) / Phase 18
   (FRAME-01).

3. **Mass-weighted COM projection head** — the network predicts only the 9-dim
   position vector `r_θ(t) = [r₁, r₂, r₃]`; velocities and accelerations are derived
   from the *projected position outputs* by componentwise AD. The mass-weighted
   centre-of-mass projection is applied to the position outputs before any loss or
   metric is evaluated.
   Source: `specs/pinn_architecture.md` §5.2 "Output Layer" (763–795, "projected
   position outputs"); enforced per the §10.2 "COM Invariance" acceptance check
   (line 972). Locked Phase 17 (IO, D-02).

4. **PHYS-03 softening outcome + dual-epsilon** — the training-time gravitational
   force uses Plummer softening with `ε_train = 10⁻⁵`. Validation and training use
   *different* epsilons: validation metrics run with a static `ε = 1e-10`; training
   runs with the dynamic `ε_train = 1e-5`.
   Source: `specs/pinn_architecture.md` §3.2 (372–399, `ε_train = 10⁻⁵`) and the
   matched-Plummer Hamiltonian §3.4 (491–534); dual-epsilon split noted in
   `specs/ctl_instruction.md` (≈ line 703). Locked Phase 19 (PHYS-03). The
   issue doc's own statement of this split (line 216) agrees with this constraint.

5. **Post-v1.3 SCS gate** — the raw Hamiltonian drift is
   `ε_H = max_t |(H(t) − H(0)) / H(0)|`, the Symplectic Conservation Score is
   `SCS = log₁₀(ε_H)`, and the reject gate is `SCS > −5` (equivalently
   `ε_H > 10⁻⁵`). This is the locked counter-position to the issue doc's ratio
   thresholds (the seed conflict above).
   Source / authority: ratified post-v1.3 (STATE.md decision; correction
   **SI-DQA-003**). Its **only written home is the read-only, non-authoritative
   research report** `specs/data_quality_assessment.md` — lines 120, 130, 234, and
   the SI-DQA-003 correction note (line 328). It does **not** live in any editable
   framework spec; cite it to `data_quality_assessment.md`, annotated "locked
   post-v1.3 (SI-DQA-003); sole written home is a read-only research report."

6. **PHYS-01 D convention** — the characteristic length scale is the raw-mass form
   `D = (G·T²)^(1/3) ≈ 4.6416` (with `G = 1`). The mass-fraction alternative
   `D = (G·M_tot·T²)^(1/3) ≈ 6.694` is **explicitly rejected** in the spec.
   Source: `specs/ctl_instruction.md` §2.5 "Global scaling" (581–600; explicit
   rejection of the 6.694 form at lines 597–598). Locked Phase 19 (PHYS-01). This
   is the locked counter-position to the issue doc's `D = 6.694` claim.

### A note on two distinct `ε_H` symbols (do not conflate)

The symbol `ε_H` is used for **two unrelated quantities** in the source material,
and they must be kept disjoint:

- **Validation raw-drift gate** `ε_H` — the maximum normalized Hamiltonian drift
  in constraint 5 above (`ε_H = max_t |(H(t) − H(0))/H(0)|`), thresholded at
  `ε_H > 10⁻⁵`. This is the validation-side quantity the SCS score logs.
- **Training energy-denominator floor** `ε_H = 1e-4·S_H` (with `ε_energy = 10⁻⁴`)
  — a training-loss denominator floor used in the energy regularizer (a training
  penalty, PHYS-04 / GAP-19-01), referenced in `ctl_instruction.md` (≈ line 1295)
  and `pinn_architecture.md` (≈ line 936). This is **not** the validation gate.

Same symbol, two roles. Questions in this document about the validation gate refer
only to the first meaning.

---

## Doc-03 Scope Boundary (out of scope for this research)

The following topics are **excluded** from this research. They belong to a future
`03-curriculum-and-training-loop.md` milestone (SCOPE-11) and appear here only as
**deferred forward-references**, never as questions to answer:

- **M16 — `dt_out` collocation-density scaling** (the proposal that supplemental
  collocation points scale with `dt_base / dt_out`). Deferred to doc-03. Do not
  pose or answer how collocation density is allocated across resolutions.
- **G6 — causal-training Option A vs Option B.** Deferred to doc-03.
- **Training-loop usage of the four metrics** — SASD-weighted collocation sampling,
  the IPR-as-ALM-noise-floor role, and PSC-governed curriculum replay. The
  *data-side definitions* of SCS/SASD/IPR/PSC are in scope (Cluster C); their
  *training-loop usage* is deferred to doc-03.

Where a finding has both a data-side facet (in scope) and a training-loop facet
(out of scope), only the data-side facet is posed below; the training-loop facet is
marked as a deferred forward-reference.

---

## Research Questions

The questions are grouped into three clusters that mirror the downstream
adjudication phases (Phase 26 / 27 / 28). Each question block reports, neutrally:
(i) the **issue-doc position** with its line citation (non-authoritative); (ii) the
**framework-spec position** (or "spec is silent"); and (iii) the relevant **dataset
facts**, referenced by `CLM-` ID from `claims-table.md` (claimed-unverified unless
the table says otherwise). No block presupposes a resolution.

### Cluster A — Ingestion & Selection (maps to Phase 26)

#### Q-A1 (B-06) — Stage 4 → Stage 5 validation gate

- **Issue-doc position (non-authoritative):** the issue doc claims there is no
  validation gate between Stage 4 (metrics) and Stage 5 (training); it states that
  `calculate_metrics.py` processes all Brutus files including partial/errored runs,
  and that the only validity signal (`final_timestep >= 9.5`) is checked at Stage 3
  and never re-validated at DataLoader init (issue doc line 57, 320–331). The issue
  doc *proposes* (non-authoritative) a `TrajectoryValidator` enforcing
  `snapshot_count >= 200` for Stage 4+, `>= 2` for Stage 0–3, and
  `final_timestep >= 9.5` (issue doc P1-1, line 283).
- **Framework-spec position:** the framework specs define the pipeline-stage
  contract but the spec is silent on a DataLoader-init completeness gate.
- **Dataset facts:** the `final_timestep >= 9.5` completeness rule is grounded, but
  its prevalence is CLM-11 (claimed-unverified); the per-trajectory snapshot counts
  the proposed `snapshot_count` bound would key on are CLM-10 (claimed-unverified).
- **Question:** Should a completeness/validity gate sit between metrics and
  training, and if so, what conditions should it enforce — `final_timestep >= 9.5`
  alone, a snapshot-count floor, both, or something else? Are the issue doc's
  proposed `>= 200` / `>= 2` snapshot bounds appropriate, given the actual snapshot
  distribution (CLM-10, CLM-11)?

#### Q-A2 (B-11) — Non-contiguous IDs (ID ≠ array index)

- **Issue-doc position (non-authoritative):** the issue doc claims IDs are
  non-contiguous and that the curriculum logic assumes `ID == array index` (issue
  doc line 58, 314–318); it *proposes* (non-authoritative) building an `id_to_path`
  dictionary / `TrajectoryIndex` from on-disk filenames (P1-2, line 284).
- **Framework-spec position:** spec is silent on the ID→path mapping mechanism.
- **Dataset facts:** the claimed gap magnitudes are CLM-01 (standard 1,250/4,000)
  and CLM-02 (hierarchical 143/5,000), both claimed-unverified; nominal IC counts
  are CLM-12. The gaps are described as intentional (generation continuation,
  prescreen rejection, failed runs).
- **Question:** What is the correct ID→trajectory mapping contract such that
  curriculum/stage assignment never assumes dense linear indexing? What do the
  actual gap magnitudes (CLM-01, CLM-02) imply for that contract?

#### Q-A3 (M11) — Blacklist loading / consumption

- **Issue-doc position (non-authoritative):** the issue doc claims the blacklist
  (`problematic_ics_blacklist.json`) is not loaded by current runners or the
  DataLoader, so blacklisted ICs can silently enter training; it reclassifies this
  audit-MAJOR finding to BLOCKING (issue doc line 59, 76, 341). It *proposes*
  (non-authoritative) loading the blacklist at DataLoader init and logging the
  exclusion count (P1-3, line 285).
- **Framework-spec position:** spec is silent on blacklist consumption.
- **Dataset facts:** the blacklist *size* is CLM-03 (65 IDs = 2 hierarchical + 63
  standard), claimed-unverified — note CLM-03's nuance: the count may be observable,
  but the *loading/consumption* status (the actual M11 finding) is a separate
  question Phase 24 owns.
- **Question:** What is the required contract for blacklist consumption at data-load
  time, and how should exclusions be surfaced? (The blacklist *count* is a claim,
  CLM-03; the *consumption* status is the open finding.)

#### Q-A4 (M13) — 184 standard IDs without a gold counterpart (fallback policy)

- **Issue-doc position (non-authoritative):** the issue doc claims 184 standard IDs
  have no gold counterpart, so Stage 5 training data is incomplete for them (issue
  doc line 65, 316, 342). It names **two candidate fallbacks**, without committing
  to either: (option 1) **skip to Stage 6** if no gold data exists; (option 2) use a
  **low-fidelity** standard fallback with a warning flag (issue doc line 65, P1-5
  line 287).
- **Framework-spec position:** spec is silent on the missing-gold fallback policy.
- **Dataset facts:** the 184 figure is CLM-04 (verified against
  `standard_quasi_random_ids_not_in_gold.md`); the related folder counts are CLM-05
  (2,749 base vs 2,565 gold).
- **Question (both options posed neutrally):** When a standard ID has no gold
  counterpart, which fallback is correct — (1) skip to Stage 6, or (2) admit a
  flagged low-fidelity standard sample — or a third option? **Annotation:** this is
  a **Phase-26 STOP-gap candidate** — if the resolution doc and the dataset are
  silent or conflicting on the fallback, the downstream adjudication must surface it
  as a STOP gap rather than invent a policy. Do not assert a fallback here.

#### Q-A5 (D7) — Footer / parameter heterogeneity

- **Issue-doc position (non-authoritative):** the issue doc claims 219 standard gold
  files have minimal footers (no `tol` parameter) while 592 files in the same folder
  carry `tol=1e-14`, and that footer schema varies (some omit `eta`, `tol`, or both)
  (issue doc line 66, 68, 196–207). It *proposes* (non-authoritative) using the
  folder-level default `tol=1e-13` with a `tol_confidence` flag ('direct' vs
  'inferred') and logging the inferred count (P2-1, line 291).
- **Framework-spec position:** spec is silent on footer-parsing fallbacks; footers
  are treated as metadata only.
- **Dataset facts:** CLM-07 (219 minimal-footer files, verified), CLM-08 (592
  `tol=1e-14` files, verified), CLM-09 (folder-default `tol`/`dt_out` per variant,
  verified).
- **Question:** What is the correct footer-handling contract when a footer is
  minimal or absent — which folder defaults apply per variant (CLM-09), and how
  should tolerance provenance (direct vs inferred) be represented?

#### Q-A6 (D-03) — Processed training-data format (HDF5 vs .npy vs txt/json)

- **Issue-doc position (non-authoritative):** the issue doc raises whether processed
  training data should stay HDF5 (`.h5`) or migrate to `.txt`/`.json` (issue doc
  lines 27–49, 173–190, 262–277). It notes `ctl_instruction.md` Step 1 item 6
  recommends HDF5 or `.npy`, and *recommends* (non-authoritative) keeping HDF5 as
  primary with an optional JSON export for inspection only.
- **Framework-spec position:** `specs/ctl_instruction.md` Step 1 item 6 recommends
  HDF5 or `.npy` for processed training data.
- **Dataset facts:** none (storage-format question; no dataset figure).
- **Question:** What processed-training-data format does the framework require —
  HDF5 primary, `.npy` acceptable, and/or an optional inspection-only export? Is
  there any methodology consequence, or is this purely a storage decision?

> **G1–G5 synthesis view (issue doc lines 88–105).** The issue doc presents G1–G5
> as a synthesis table mapping onto the findings above: G1 = B-06 (Q-A1), G2 = B-11
> (Q-A2), G3 = M11 (Q-A3), G4 = M13 (Q-A4), G5 = `dt_out` heterogeneity (data-side
> in Q-B1; the collocation-scaling facet, M16, is deferred to doc-03). No separate
> questions are posed for the G-table; it is a view over the constituent findings.

### Cluster B — Sampling, Precision & Global Scale (maps to Phase 27)

#### Q-B1 (M12) — Points-per-trajectory feasibility

- **Issue-doc position (non-authoritative):** the issue doc claims standard
  trajectories (`dt_out=0.17`, ~59 snapshots) cannot support the 32-points-per-
  trajectory batch spec (a 54% sampling ratio), and reclassifies this to BLOCKING
  (issue doc line 60, 77, 286). It *proposes* (non-authoritative) an adaptive cap
  `n_pts = min(32, int(0.5 * n_snapshots))` (P1-4, line 286).
- **Framework-spec position:** `specs/ctl_instruction.md` §5.3.2 carries the batch
  point-count assumption; spec is silent on an adaptive cap.
- **Dataset facts:** the per-trajectory snapshot counts (~59 / ~125 / ~1000) are
  CLM-10 (claimed-unverified; the dataset README warns against hard-coding snapshot
  counts); the per-variant `dt_out` values are CLM-09.
- **Question:** Given the actual snapshot distribution (CLM-10), what points-per-
  trajectory contract is feasible across variants — a fixed 32, an adaptive cap, or
  another rule? *(The `dt_out`-aware supplemental-collocation facet, M16, is out of
  scope — see the doc-03 boundary.)*

#### Q-B2 — Footer / mass-drift protocol

- **Issue-doc position (non-authoritative):** the issue doc claims Brutus
  arbitrary-precision output may round masses in text, and *proposes*
  (non-authoritative) parsing ~1000 IC–Brutus pairs and comparing `m_IC` vs
  `m_Brutus(t=0)` with `np.allclose(rtol=1e-15)`; if mismatched, parse masses with
  `decimal.Decimal`; if matched, treat IC masses as canonical (issue doc lines
  196–207, P2-2 line 292).
- **Framework-spec position:** spec is silent on a mass-drift verification protocol.
- **Dataset facts:** folder-default parameters are CLM-09; the empirical mass-drift
  comparison itself is a Phase-24 probe (DATA-05).
- **Question:** What mass-consistency check (tolerance, sample size, fallback to
  exact-precision parsing) should the data pipeline require between IC files and
  Brutus `t=0` masses?

#### Q-B3 — Precision handling (float64 sufficiency; Decimal-for-masses)

- **Issue-doc position (non-authoritative):** the issue doc claims Brutus outputs
  carry 30–40 significant digits, that validation in `float64` is acceptable
  (~1e-16 relative precision vs Brutus tolerance ~1e-13 to 1e-15), and that
  `decimal.Decimal` is needed only for mass consistency (issue doc lines 208–216).
- **Framework-spec position:** the dual-epsilon constraint (Hard Constraint 4) fixes
  validation `ε = 1e-10` vs training `ε = 1e-5`; spec is otherwise silent on parse
  precision.
- **Dataset facts:** folder-default tolerances per variant are CLM-09.
- **Question:** Is `float64` sufficient for the validation metrics given the Brutus
  convergence tolerances (CLM-09), and where (if anywhere) is exact-precision
  parsing required?

#### Q-B4 — Global-scale `compute_globals` / `D = 6.694` (KNOWN CONFLICT)

- **Issue-doc position (non-authoritative):** the issue doc claims `compute_globals`
  must use `D = cbrt(G · M_tot · t_max²) = 6.694` (with `M_tot = 3`), calling the
  older `D = cbrt(G · t_max²) ≈ 4.64` form an omission (issue doc lines 218–258,
  P1-7 line 289). This is CLM-13.
- **Framework-spec position (locked counter-position):** Hard Constraint 6 (PHYS-01)
  fixes the raw-mass `D = (G·T²)^(1/3) ≈ 4.6416`; `specs/ctl_instruction.md` §2.5
  line 598 **explicitly rejects** the `6.694` form except under a mass-fraction
  convention rewrite that would require touching every residual, Hamiltonian,
  angular-momentum, COM, and invariant formula.
- **Dataset facts:** CLM-13 (the `6.694` claim) is a contested convention claim, not
  a dataset count.
- **Question (both positions presented; do not settle):** Which `D` convention does
  the data pipeline's global-scale computation use — the locked raw-mass
  `≈ 4.6416`, or the issue doc's mass-fraction `6.694` — and what would adopting the
  latter require? Present the reconciliation; the adjudication (EVID-10 / PIPE-09)
  is downstream.

### Cluster C — Validation Metrics (maps to Phase 28)

> Scope note: only the **data-side definitions** of the four metrics are in scope.
> Their **training-loop usage** (SASD-weighted sampling, IPR-as-ALM-noise-floor,
> PSC-governed replay) is deferred to doc-03 — see the boundary above.

#### Q-C1 (SCS) — Symplectic Conservation Score (definition + thresholds, KNOWN CONFLICT)

- **Issue-doc position (non-authoritative):** the issue doc defines
  `SCS = max_t |H(t) − H(0)| / |H(0)|` computed with static `ε = 1e-10`, and states
  **ratio-based** reject thresholds `SCS > 1e-6` (Phase-1 screening) tightening to
  `SCS < 1e-8` for high-resolution data (issue doc lines 129–141).
- **Framework-spec position (locked counter-position):** Hard Constraint 5 fixes
  `ε_H = max_t |(H(t) − H(0))/H(0)|`, `SCS = log₁₀(ε_H)`, reject gate `SCS > −5`
  (`ε_H > 10⁻⁵`), per `data_quality_assessment.md` (SI-DQA-003). The issue doc's
  `1e-6`/`1e-8` are raw-ratio numbers; the locked gate is a log-drift number — they
  are not the same quantity (the seed conflict).
- **Dataset facts:** the prevalence of trajectories passing/failing the gate is not
  grounded; no CLM dataset count settles it.
- **Question (both positions presented; do not settle):** What is the correct SCS
  definition and reject threshold for data screening — the locked log-drift gate
  `SCS > −5`, or the issue doc's ratio thresholds — and how should the raw-ratio vs
  log-drift discrepancy be reconciled? The adjudication (VAL-01 / EVID-10) is
  downstream.

#### Q-C2 (SASD) — Stiffness-Aware Sampling Density (data-side)

- **Issue-doc position (non-authoritative):** the issue doc defines
  `SASD_i = Δt_i · ||a(t_i)|| / ||v(t_i)||` and claims that exceeding a critical
  threshold means the trajectory turns significantly between samples and should be
  flagged/resampled at higher resolution (issue doc lines 143–153).
- **Framework-spec position:** spec is silent on a data-side SASD definition.
- **Dataset facts:** per-variant `dt_out` resolution is CLM-09; snapshot counts are
  CLM-10.
- **Question:** What is the correct data-side SASD definition and the
  flag/resample criterion? *(The training-loop sampling-weight role is deferred to
  doc-03.)*

#### Q-C3 (IPR) — Interpolation Physics Residual (data-side, dual-epsilon)

- **Issue-doc position (non-authoritative):** the issue doc defines IPR as a
  cubic-Hermite-spline residual against the equations of motion, computed with the
  dynamic softening `ε = 1e-5` (issue doc lines 155–165).
- **Framework-spec position:** Hard Constraint 4 fixes the dual-epsilon split; the
  spec is otherwise silent on a data-side IPR definition.
- **Dataset facts:** none specific (definition question).
- **Question:** What is the correct data-side IPR definition, and which epsilon does
  it use given the locked dual-epsilon contract? *(The IPR-as-ALM-noise-floor role
  is deferred to doc-03.)*

#### Q-C4 (PSC) — Phase Space Coverage Entropy (data-side)

- **Issue-doc position (non-authoritative):** the issue doc defines PSC as the
  Shannon entropy of data points across a discretized phase-space grid, quantifying
  training-data diversity (issue doc lines 167–169).
- **Framework-spec position:** spec is silent on a data-side PSC definition.
- **Dataset facts:** none specific (definition question).
- **Question:** What is the correct data-side PSC definition (grid construction,
  entropy estimator)? *(The PSC-governed curriculum-replay role is deferred to
  doc-03.)*

---

## Inventory Coverage Table

Every item from the issue-02 finding inventory (`23-RESEARCH.md` §"Issue-02 Finding
Inventory") is accounted for below: posed as a question, carried as a deferred
forward-reference, or noted with its excluded/contextual rationale.

| Inventory item | Disposition | Question block / deferred reference / excluded rationale | CLM IDs | Downstream phase |
|----------------|-------------|----------------------------------------------------------|---------|------------------|
| D-03 processed training-data format | Question | Q-A6 | — | Phase 26 (PIPE-10) |
| B-06 Stage 4→5 validation gate | Question | Q-A1 | CLM-10, CLM-11 | Phase 26 (PIPE-01) |
| B-11 non-contiguous ID (ID ≠ index) | Question | Q-A2 | CLM-01, CLM-02, CLM-12 | Phase 26 (PIPE-02) |
| M11 blacklist not loaded | Question | Q-A3 | CLM-03 | Phase 26 (PIPE-03) |
| M12 points-per-trajectory infeasible | Question | Q-B1 | CLM-09, CLM-10 | Phase 27 (PIPE-04) |
| M13 184 standard IDs without gold | Question (both options; STOP-gap candidate) | Q-A4 | CLM-04, CLM-05 | Phase 26 (PIPE-05) |
| D7 footer/parameter heterogeneity | Question | Q-A5 | CLM-07, CLM-08, CLM-09 | Phase 26 (PIPE-06) |
| Severity reclassification (M11, M12 MAJOR→BLOCKING) | Contextual | Posed inside Q-A3 / Q-B1 as the issue doc's reclassification claim; the reclassification itself is adjudicated by EVID-10, not asserted here | — | Phase 25 (EVID-10) |
| G1–G5 pipeline validation gaps | Synthesis view | G1–G5 synthesis note (after Q-A6); maps to constituent findings, no separate questions | — | Phases 26–28 |
| Validation-threshold clarifications (overfit `<1e-6`; 14D; gold thresholds) | Partial | 14D is a locked Hard Constraint (not a question); gold-standard thresholds → Phase 28; the overfit-challenge `<1e-6` precision is training-loop-adjacent and not posed as a data-side question | — | Phase 28 / locked |
| SCS definition + ratio thresholds | Question (KNOWN CONFLICT) | Q-C1 | — | Phase 28 (VAL-01 / EVID-10) |
| SASD definition (data-side) | Question | Q-C2 | CLM-09, CLM-10 | Phase 28 (VAL-02) |
| IPR definition (data-side) | Question | Q-C3 | — | Phase 28 (VAL-03) |
| PSC definition (data-side) | Question | Q-C4 | — | Phase 28 (VAL-04) |
| Footer/mass-drift protocol (`np.allclose rtol=1e-15`, Decimal) | Question | Q-B2 | CLM-09 | Phase 26/27 (PIPE-06/07) |
| Precision handling (float64; Decimal-for-masses) | Question | Q-B3 | CLM-09 | Phase 27 (PIPE-07) |
| Global-scale `compute_globals` / `D = 6.694` | Question (KNOWN CONFLICT) | Q-B4 | CLM-13 | Phase 27 (PIPE-09 / EVID-10) |
| Recommended Resolutions P1-1..P2-2 | Non-authoritative | Each surfaces inside its mapped question as "the issue doc proposes X (non-authoritative)"; never presented as settled | — | — |
| Dataset Inventory (counts table) | Source of CLM figures | Enumerated in `claims-table.md`; every figure carries a CLM ID and status | CLM-01..CLM-12 | Phase 24 |
| DataLoader Requirements (10-item impl spec) | Data-side contracts posed; implementation deferred | The data-side contract each item implies is posed in Q-A1..Q-A5 / Q-B1..Q-B3 / Q-C1..Q-C4; the *implementation* is FUT-01 | CLM-03, CLM-04 | Phases 26–28 / FUT-01 |
| M16 `dt_out` collocation-scaling | Excluded (doc-03) | Deferred forward-reference (doc-03 boundary); not a question (SCOPE-11) | — | doc-03 |
| G6 causal-training Option A vs B | Excluded (doc-03) | Deferred forward-reference (doc-03 boundary); not a question (SCOPE-11) | — | doc-03 |
| Training-loop usage of SCS/SASD/IPR/PSC | Excluded (doc-03) | Data-side definitions posed in Q-C1..Q-C4; the training-loop usage is a deferred forward-reference (doc-03) | — | doc-03 |

---

## Return Format

This section states only what the external research is **expected to produce** — it
does **not** prescribe a schema. There is no required heading structure, no required
verdict labels, no required tables, and no required file layout. The resolution doc
is your product; v1.4's `ctl_pinn_resolution.md` is available as a *format
precedent* (a suggestion only), not a template you must follow.

Expectations:

- **Answer each question** in the three clusters above (Q-A1..Q-A6, Q-B1..Q-B4,
  Q-C1..Q-C4). It is acceptable to answer "insufficient evidence" where that is the
  honest finding.
- **Cite your sources** for each answer, including which of the package's snapshot
  documents (in `specs/` and the consolidated context file) you relied on.
- **Identify conflicts and uncertainty explicitly.** Where the issue doc conflicts
  with a Hard Constraint (e.g. the SCS thresholds in Q-C1, the `D` convention in
  Q-B4) or where the dataset facts (CLM IDs) do not settle a question, say so
  plainly rather than forcing a resolution.
- **Stay within the Hard Constraints and the doc-03 boundary.** Do not re-open a
  locked v1.4 convention, and do not answer the doc-03-excluded topics (M16, G6,
  training-loop metric usage).
- **Flag STOP-gap candidates.** Where a finding (e.g. the M13 fallback in Q-A4)
  appears genuinely undecidable from the available sources, mark it as such rather
  than inventing a policy.

*End of framed-research-questions.md*
