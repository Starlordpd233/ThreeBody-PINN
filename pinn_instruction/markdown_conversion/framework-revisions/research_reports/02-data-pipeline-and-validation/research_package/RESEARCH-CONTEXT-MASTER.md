---
title: Issue-02 Research Context Master
package_for: issue-02
role: research-context entry point (PKG-01 manifest, PKG-02 framed questions, PKG-03 claims register, D-05 consolidated context, correction provenance)
status: active
created: 2026-06-10
consolidated: 2026-06-11
consolidated_from: README.md, framed-research-questions.md, claims-table.md, consolidated-context.md, ERRATUM-2026-06-10.md (all five retired 2026-06-11)
consolidation_source_baseline: 27b05432ae76dd43227c4e4f2333e25b5469ca18 (pre-remediation repo state; per-file SHA-256 hashes recorded in `.planning/phases/23-research-package-assembly/23-VERIFICATION.md`, "Master Consolidation Baseline" section)
original_package_pin: 96f9150a02919d492a86ef9f63e10e5942d2d8e3
self_contained: true
---

# Issue-02 Research Context Master

This file is the single research-context entry point for the issue-02 ("Data Pipeline and
Validation") external-research package. It was consolidated on 2026-06-11, as a Phase 23
post-delivery remediation, from five retired package files: the manifest (`README.md`), the
framed research questions (`framed-research-questions.md`), the claims register
(`claims-table.md`), the consolidated dataset context (`consolidated-context.md`), and the
interim erratum (`ERRATUM-2026-06-10.md`). The two grounded corrections from that erratum are
integrated directly into the current text below; the full correction history is preserved in
[Correction Provenance And Verification Boundaries](#correction-provenance-and-verification-boundaries).

**Reading order for the package:** read this master file first (orientation → questions →
claims → dataset context → correction provenance, in that order), then the delivery note
(`DELIVERY-NOTE.md`) for handoff and gate context, then the `specs/` snapshots as the questions
direct you to them.

---

## Package Orientation And Manifest

This section records, for every file in this package, its role annotation, its canonical source
path inside the project repository, the source commit hash it was snapshotted from, and how it
should be treated.

The package is **self-contained**: every file referenced here is a sibling file inside this
package directory. Source paths in the manifest are provenance labels (where the file came from
in the project repository), not navigation links — the external researcher is assumed to have
no repository access and works only from the snapshot copies shipped here.

### Source-Treatment Preamble

Read these conventions before using any file in this package:

- **The issue doc is non-authoritative.** `specs/02-data-pipeline-and-validation.md` is the
  adjudication subject, not a source of truth. Both its findings **and** its "Recommended
  Resolutions" may contain errors and must NOT be treated as settled. The worked example of
  this is the known seed conflict: the issue doc's ratio-based SCS thresholds (`> 1e-6` /
  `< 1e-8`) conflict with the locked post-v1.3 gate (`epsilon_H > 1e-5` / `SCS > -5`). The
  external research adjudicates such conflicts; it does not assume the issue doc is correct.
- **The framework specs are the source of truth.** `specs/ctl_instruction.md` and
  `specs/pinn_architecture.md` carry the locked v1.4 conventions (14D input contract, Jacobi
  IC13, mass-weighted COM projection head, PHYS-03 softening, PHYS-01 D convention, post-v1.3
  SCS gate). They are the only spec-edit targets for downstream adjudication.
- **The `pinn/` "Canonical" citation is OVERRIDDEN.** The issue doc cites
  `pinn/data-processing-pipeline-full.py` as "Canonical". That citation is **overridden** by
  the 2026-05-19 directive (SCOPE-10): live `pinn/` code is NOT a grounding source and is
  excluded from this package entirely. The framework specs are authoritative instead.
- **Figures are claims until verified.** Every dataset figure in this package is tracked in the
  [CLM Claims Register](#clm-claims-register) by a stable CLM ID with status
  `claimed-unverified` or `verified`. No figure is presented as fact unless its CLM row is
  marked `verified`. Phase 24 verifies every row regardless of status.
- **Annotations live here, not in the snapshots.** The `specs/*.md` files are byte-for-byte
  intact copies. All role / FROZEN / non-authoritative annotations live in this manifest's
  Role annotation column, never inside the copied files (D-03).

### Per-File Manifest

| Package file | Role annotation | Canonical source path | Source commit hash | Treatment |
|--------------|-----------------|-----------------------|--------------------|-----------|
| `RESEARCH-CONTEXT-MASTER.md` | This file: research-context entry point — manifest/index (PKG-01), framed research questions (PKG-02), CLM claims register (PKG-03), consolidated dataset context (D-05), correction provenance | generated in Phase 23; consolidated 2026-06-11 from five retired package files | package commit | Generated package artifact |
| `DELIVERY-NOTE.md` | Handoff / gate-open delivery note (D-16) | generated in Phase 23 | package commit | Generated package artifact |
| `specs/02-data-pipeline-and-validation.md` | NON-authoritative; adjudication subject | `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `d43afcd69af027e0689f42ac61e130f8497939f8` | Byte-for-byte intact snapshot |
| `specs/ctl_instruction.md` | Spec-edit target; D-03 byte-for-byte; carries 14D input contract, Jacobi IC13, PHYS-01 D convention | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` | `192c7c3c55ca0730c34ce708abf24c613234dd2e` | Byte-for-byte intact snapshot |
| `specs/pinn_architecture.md` | Spec-edit target; D-03 byte-for-byte; carries COM projection head, PHYS-03 softening, loss contracts | `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | `192c7c3c55ca0730c34ce708abf24c613234dd2e` | Byte-for-byte intact snapshot |
| `specs/sampling_method.md` | FROZEN (SCOPE-08); historical record of dataset generation; not a revision target | `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` | `916d3f84ad7282c1f8ace45901441f7d3ac054ca` | Byte-for-byte intact snapshot |
| `specs/data_quality_assessment.md` | Research report, NOT an authoritative spec (SCOPE-09); non-authoritative; sole written home of the post-v1.3 SCS gate + metric definitions | `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` | `d3fcff99268b4493629eb2f0fe580f43c51ec019` | Byte-for-byte intact snapshot |

**Package-wide pin:** all snapshots were taken against project state
`96f9150a02919d492a86ef9f63e10e5942d2d8e3`; per-file hashes above record each source file's own
last-touched commit. The 2026-06-11 consolidation changed no `specs/` snapshot — their hashes
remain valid.

### Self-Contained Guarantee

Every file named in this manifest is a sibling inside this package directory
(`research_package/` and its `specs/` subdirectory). No entry above is a navigable link out of
the package, and no in-package file points a repo-blind agent at a project path that would
dangle without repository access. The canonical source paths in the manifest are recorded
solely for provenance and re-derivation by an agent that *does* have the repository; the
external researcher does not need them to use the package.

---

## Framed Research Questions

> **What this section is.** This is the task list for the external multi-AI research on issue
> 02 (data pipeline and validation). It poses every contested or unverified in-scope finding as
> an explicit, neutral question. It does **not** answer any of them — adjudication happens
> later, downstream of your research.
>
> **What this section is not.** It is not a set of decisions, not a verdict, and not an
> instruction to implement anything. Where a source proposes a fix, that proposal is reported
> as a *claim to be evaluated*, never as a settled answer.

### How To Read These Questions

1. Read the **Source-Treatment Framing** below first — it tells you which inputs are
   authoritative and which are not (it restates the manifest's preamble in research-task
   terms).
2. Treat the **Hard Constraints** as fixed. They are locked v1.4 conventions; your research
   must work *within* them, not re-open them.
3. Note the **Doc-03 Scope Boundary** — several tempting topics are explicitly out of scope
   for this research and must not be answered here.
4. Answer the questions in the three clusters that follow.
5. Every dataset figure mentioned anywhere in this package carries a `CLM-` ID in the
   [CLM Claims Register](#clm-claims-register). Figures are *claims*, not established facts;
   reference them by their CLM ID and do not treat any unverified figure as true.

### Source-Treatment Framing (READ FIRST)

**Both the issue doc and its recommendations are NON-authoritative and may contain errors.**
The adjudication subject — `02-data-pipeline-and-validation.md` (the intact snapshot under
`specs/`) — and *especially* its "Recommended Resolutions" (P1-1..P2-2) and "Open Decisions"
sections are not authoritative. They are a synthesis of an internal audit and several archived
notes. The external research must **adjudicate** these findings against the locked conventions
and the dataset facts — it must **not transcribe** the issue doc's proposed fixes as if they
were decisions.

**Worked example — why this matters (the seed conflict).** The issue doc states ratio-based SCS
thresholds: reject any trajectory with `SCS > 1e-6`, and tighten to `SCS < 1e-8` for
high-resolution data (issue doc lines 133–134). This **directly conflicts** with the locked
post-v1.3 SCS gate, where `SCS = log₁₀(ε_H)` and the reject gate is `SCS > −5` (i.e.
`ε_H > 10⁻⁵`). The issue doc's `1e-6` / `1e-8` figures are *raw-ratio* numbers; the locked gate
is a *log-drift* number — they are not even the same quantity. This is one concrete
demonstration that the issue doc "may contain errors": do not assume any issue-doc number is
correct without checking it against the locked conventions and the dataset.

**The `pinn/` "Canonical" citation is OVERRIDDEN.** The issue doc's References list cites
`pinn/data-processing-pipeline-full.py` and `pinn/basic_architecture.py` as "Canonical" (issue
doc line 357). That citation is **overridden** (user directive 2026-05-19; SCOPE-10). The live
`pinn/` code is **not** a grounding source for any decision in this research. The **framework
specs are the source of truth** — i.e. the intact `ctl_instruction.md` and
`pinn_architecture.md` snapshots in `specs/`. Do not cite `pinn/` code as evidence.

### Hard Constraints — Locked v1.4 Conventions (verbatim)

These six conventions were locked during the v1.4 milestone (issue 01) and are **fixed inputs**
to this research. They are reproduced verbatim with their citation into the intact spec
snapshots in `specs/`. Do not re-open or contradict them; your job is to adjudicate issue-02's
data-pipeline findings *consistently with* them.

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
   (line 967). Locked Phase 17 (IO, D-02).

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

#### A note on two distinct `ε_H` symbols (do not conflate)

The symbol `ε_H` is used for **two unrelated quantities** in the source material, and they must
be kept disjoint:

- **Validation raw-drift gate** `ε_H` — the maximum normalized Hamiltonian drift
  in constraint 5 above (`ε_H = max_t |(H(t) − H(0))/H(0)|`), thresholded at
  `ε_H > 10⁻⁵`. This is the validation-side quantity the SCS score logs.
- **Training energy-denominator floor** `ε_H = 1e-4·S_H` (with `ε_energy = 10⁻⁴`)
  — a training-loss denominator floor used in the energy regularizer (a training
  penalty, PHYS-04 / GAP-19-01), referenced in `ctl_instruction.md` (≈ line 1295)
  and `pinn_architecture.md` (≈ line 936). This is **not** the validation gate.

Same symbol, two roles. Questions in this document about the validation gate refer only to the
first meaning.

### Doc-03 Scope Boundary (out of scope for this research)

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

Where a finding has both a data-side facet (in scope) and a training-loop facet (out of scope),
only the data-side facet is posed below; the training-loop facet is marked as a deferred
forward-reference.

### Research Questions

The questions are grouped into three clusters that mirror the downstream adjudication phases
(Phase 26 / 27 / 28). Each question block reports, neutrally: (i) the **issue-doc position**
with its line citation (non-authoritative); (ii) the **framework-spec position** (or "spec is
silent"); and (iii) the relevant **dataset facts**, referenced by `CLM-` ID from the
[CLM Claims Register](#clm-claims-register) (claimed-unverified unless the register says
otherwise). No block presupposes a resolution.

#### Cluster A — Ingestion & Selection (maps to Phase 26)

##### Q-A1 (B-06) — Stage 4 → Stage 5 validation gate

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

##### Q-A2 (B-11) — Non-contiguous IDs (ID ≠ array index)

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

##### Q-A3 (M11) — Blacklist loading / consumption

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

##### Q-A4 (M13) — 184 standard IDs without a gold counterpart (fallback policy)

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

##### Q-A5 (D7) — Footer / parameter heterogeneity

- **Issue-doc position (non-authoritative):** the issue doc claims 219 standard gold
  files have minimal footers (no `tol` parameter) while 592 files in the same folder
  carry `tol=1e-14`, and that footer schema varies (some omit `eta`, `tol`, or both)
  (issue doc line 66, 68, 196–207). It *proposes* (non-authoritative) using the
  folder-level default `tol=1e-13` with a `tol_confidence` flag ('direct' vs
  'inferred') and logging the inferred count (P2-1, line 291).
- **Framework-spec position:** spec is silent on footer-parsing fallbacks; footers
  are treated as metadata only.
- **Dataset facts:** CLM-07 (219 standard-gold files with **no `Result:` footer at
  all**, verified — the issue doc's "minimal footer" characterization is corrected;
  see [Correction Provenance](#correction-provenance-and-verification-boundaries)
  Correction 2), CLM-08 (592 `tol=1e-14` files, verified), CLM-09 (folder-default
  `tol`/`dt_out` per variant, verified). Footers that are present carry the full
  schema; 1,550 hierarchical-base and 701 standard-base files likewise have no
  footer.
- **Question:** What is the correct footer-handling contract when a footer is
  absent — which folder defaults apply per variant (CLM-09), and how should
  tolerance provenance (direct vs inferred) be represented?

##### Q-A6 (D-03) — Processed training-data format (HDF5 vs .npy vs txt/json)

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

#### Cluster B — Sampling, Precision & Global Scale (maps to Phase 27)

##### Q-B1 (M12) — Points-per-trajectory feasibility

- **Issue-doc position (non-authoritative):** the issue doc claims standard
  trajectories (`dt_out=0.17`, ~59 snapshots) cannot support the 32-points-per-
  trajectory batch spec (a 54% sampling ratio), and reclassifies this to BLOCKING
  (issue doc line 60, 77, 286). It *proposes* (non-authoritative) an adaptive cap
  `n_pts = min(32, int(0.5 * n_snapshots))` (P1-4, line 286).
- **Framework-spec position:** `specs/ctl_instruction.md` "Mini-Batch Construction
  with Lookahead Sampling" (line 1197) carries the batch point-count assumption;
  spec is silent on an adaptive cap. *(Citation corrected at consolidation: the
  issue doc's "§5.3.2" numbering does not exist in the spec snapshot — see
  [Correction Provenance](#correction-provenance-and-verification-boundaries).)*
- **Dataset facts:** the per-trajectory snapshot counts (~59 / ~125 / ~1000) are
  CLM-10 (claimed-unverified; the dataset README warns against hard-coding snapshot
  counts); the per-variant `dt_out` values are CLM-09.
- **Question:** Given the actual snapshot distribution (CLM-10), what points-per-
  trajectory contract is feasible across variants — a fixed 32, an adaptive cap, or
  another rule? *(The `dt_out`-aware supplemental-collocation facet, M16, is out of
  scope — see the doc-03 boundary.)*

##### Q-B2 — Footer / mass-drift protocol

- **Issue-doc position (non-authoritative):** the issue doc claims Brutus
  arbitrary-precision output may round masses in text, and *proposes*
  (non-authoritative) parsing IC–Brutus pairs and comparing `m_IC` vs
  `m_Brutus(t=0)` with `np.allclose(rtol=1e-15)`; if mismatched, parse masses with
  `decimal.Decimal`; if matched, treat IC masses as canonical. **The issue doc
  states two conflicting sample sizes for this protocol:** its footer/mass-drift
  protocol prose says "parse **1000** IC-Brutus pairs" (issue doc line 202), while
  its Recommended Resolution P2-2 says "Batch-verify **100** IC-Brutus mass pairs"
  (issue doc line 292). This internal issue-doc conflict (WR-01) is reported here,
  not resolved; whether it receives its own CLM row is an open Phase 24 decision.
- **Framework-spec position:** spec is silent on a mass-drift verification protocol.
- **Dataset facts:** folder-default parameters are CLM-09; the empirical mass-drift
  comparison itself is a Phase-24 probe (DATA-05).
- **Question:** What mass-consistency check (tolerance, sample size, fallback to
  exact-precision parsing) should the data pipeline require between IC files and
  Brutus `t=0` masses?

##### Q-B3 — Precision handling (float64 sufficiency; Decimal-for-masses)

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

##### Q-B4 — Global-scale `compute_globals` / `D = 6.694` (KNOWN CONFLICT)

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

#### Cluster C — Validation Metrics (maps to Phase 28)

> Scope note: only the **data-side definitions** of the four metrics are in scope.
> Their **training-loop usage** (SASD-weighted sampling, IPR-as-ALM-noise-floor,
> PSC-governed replay) is deferred to doc-03 — see the boundary above.

##### Q-C1 (SCS) — Symplectic Conservation Score (definition + thresholds, KNOWN CONFLICT)

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

##### Q-C2 (SASD) — Stiffness-Aware Sampling Density (data-side)

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

##### Q-C3 (IPR) — Interpolation Physics Residual (data-side, dual-epsilon)

- **Issue-doc position (non-authoritative):** the issue doc defines IPR as a
  cubic-Hermite-spline residual against the equations of motion, computed with the
  dynamic softening `ε = 1e-5` (issue doc lines 155–165).
- **Framework-spec position:** Hard Constraint 4 fixes the dual-epsilon split; the
  spec is otherwise silent on a data-side IPR definition.
- **Dataset facts:** none specific (definition question).
- **Question:** What is the correct data-side IPR definition, and which epsilon does
  it use given the locked dual-epsilon contract? *(The IPR-as-ALM-noise-floor role
  is deferred to doc-03.)*

##### Q-C4 (PSC) — Phase Space Coverage Entropy (data-side)

- **Issue-doc position (non-authoritative):** the issue doc defines PSC as the
  Shannon entropy of data points across a discretized phase-space grid, quantifying
  training-data diversity (issue doc lines 167–169).
- **Framework-spec position:** spec is silent on a data-side PSC definition.
- **Dataset facts:** none specific (definition question).
- **Question:** What is the correct data-side PSC definition (grid construction,
  entropy estimator)? *(The PSC-governed curriculum-replay role is deferred to
  doc-03.)*

### Inventory Coverage Table

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
| Dataset Inventory (counts table) | Source of CLM figures | Enumerated in the [CLM Claims Register](#clm-claims-register); every figure carries a CLM ID and status | CLM-01..CLM-12 | Phase 24 |
| DataLoader Requirements (10-item impl spec) | Data-side contracts posed; implementation deferred | The data-side contract each item implies is posed in Q-A1..Q-A5 / Q-B1..Q-B3 / Q-C1..Q-C4; the *implementation* is FUT-01 | CLM-03, CLM-04 | Phases 26–28 / FUT-01 |
| M16 `dt_out` collocation-scaling | Excluded (doc-03) | Deferred forward-reference (doc-03 boundary); not a question (SCOPE-11) | — | doc-03 |
| G6 causal-training Option A vs B | Excluded (doc-03) | Deferred forward-reference (doc-03 boundary); not a question (SCOPE-11) | — | doc-03 |
| Training-loop usage of SCS/SASD/IPR/PSC | Excluded (doc-03) | Data-side definitions posed in Q-C1..Q-C4; the training-loop usage is a deferred forward-reference (doc-03) | — | doc-03 |

### Return Format

This subsection states only what the external research is **expected to produce** — it does
**not** prescribe a schema. There is no required heading structure, no required verdict labels,
no required tables, and no required file layout. The resolution doc is your product; v1.4's
`ctl_pinn_resolution.md` is available as a *format precedent* (a suggestion only), not a
template you must follow.

Expectations:

- **Answer each question** in the three clusters above (Q-A1..Q-A6, Q-B1..Q-B4,
  Q-C1..Q-C4). It is acceptable to answer "insufficient evidence" where that is the
  honest finding.
- **Cite your sources** for each answer, including which of the package's snapshot
  documents (in `specs/`) and which parts of the
  [Consolidated Dataset Context](#consolidated-dataset-context) you relied on.
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

---

## CLM Claims Register

**Purpose:** This register enumerates every dataset figure stated in the package with a stable
CLM ID, classified as `claimed-unverified` or `verified` (PKG-03).

**CLM-ID scheme:** Each row carries a unique stable identifier (`CLM-01`, `CLM-02`, ...). All
inline figure mentions in package prose reference their CLM ID rather than restating the figure
as fact.

**Status definitions:**

- **`claimed-unverified`**: The figure is stated in the issue doc or another non-authoritative
  source but has not yet been empirically verified against the on-disk dataset. Phase 24 will
  verify every row regardless of status.
- **`verified`**: The figure is grounded in a committed `simulation_data/Documentation/` file
  (provenance citation provided). Even verified rows are re-verified by Phase 24.

**Source citations** are provenance references (file path and line number where the figure
appears), not navigation links. The external researcher has access only to the snapshot copies
in this package. Dataset-README line numbers cite the corrected README (post-2026-06-10
correction commits — see
[Correction Provenance](#correction-provenance-and-verification-boundaries)).

**Phase-24 check column** describes the verification action each row requires. The DATA-07
correction addendum (produced by Phase 24) is keyed by CLM IDs.

### Claims Table

| CLM ID | Figure | Value (claimed) | Source citation | Status | Phase-24 check |
|--------|--------|------------------|-----------------|--------|----------------|
| CLM-01 | Standard ID gaps | 1,250 gaps out of 4,000 nominal (31.2%) | Issue doc lines 58, 312 | `claimed-unverified` | DATA-01: count standard Brutus output files; compute `nominal - actual` |
| CLM-02 | Hierarchical ID gaps | 143 gaps out of 5,000 nominal (2.9%) | Issue doc lines 58, 311 | `claimed-unverified` | DATA-01: count hierarchical Brutus output files; compute `nominal - actual` |
| CLM-03 | Blacklist size | 65 IDs (2 hierarchical + 63 standard) | Issue doc lines 59, 297; `simulation_data/Documentation/problematic_ics_blacklist.json` (provenance) | `claimed-unverified` | DATA-02: verify blacklist count/composition against json; verify loading/consumption status (M11 finding) |
| CLM-04 | Standard IDs without gold counterpart | 184 | `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` | `verified` | DATA-03: re-verify 184-ID list against gold Brutus outputs |
| CLM-05 | Standard folder counts | 2,749 base vs 2,565 gold | `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`; `simulation_data/Documentation/README.md` | `verified` | DATA-04: count base and gold folders independently |
| CLM-06 | Hierarchical Brutus output | ~4,857 files | `simulation_data/Documentation/README.md` Brutus Parameters by Variant (line 589) | `verified` | DATA-04: count hierarchical Brutus output files |
| CLM-07 | Standard-gold files with no `Result:` footer | 219 files (count unchanged; "minimal footer" characterization corrected — these files have no footer at all) | `simulation_data/Documentation/README.md` Brutus Parameters by Variant (lines 614–621) | `verified` | DATA-05: parse footer presence/schema across standard-gold files; count the no-footer subset |
| CLM-08 | tol=1e-14 standard-gold files | 592 files | `simulation_data/Documentation/README.md` Brutus Parameters by Variant (line 618) | `verified` | DATA-05: parse tolerance field across standard-gold files; count tol=1e-14 subset |
| CLM-09 | Folder-default tol / dt_out values | std: tol=1e-13, dt_out=0.17; hier base: tol=1e-15, dt_out=0.08; gold: tol=1e-13, dt_out=0.01 | `simulation_data/Documentation/README.md` Brutus Parameters by Variant (lines 578–629) | `verified` | DATA-05: parse footer parameters; verify default values per variant |
| CLM-10 | Snapshot counts per trajectory | ~59 (standard) / ~125 (hierarchical) / ~1000 (gold) | Issue doc lines 13, 60, 311-312 | `claimed-unverified` | DATA-06: count output rows per trajectory file; README warns against hard-coding snapshot counts (Snapshot Count Note, lines 623–629) |
| CLM-11 | `final_timestep >= 9.5` prevalence | Rule stated; prevalence figure not given | Issue doc lines 57, 202, 326; README Completeness Checks | `claimed-unverified` (prevalence) | DATA-06: compute `final_timestep` distribution; verify gate rule and quantify prevalence |
| CLM-12 | Nominal IC counts | ~4,000 standard / ~5,000 hierarchical | Issue doc lines 311-312 | `claimed-unverified` | DATA-01: verify actual vs nominal IC count |
| CLM-13 | `D = 6.694` global scale | `cbrt(G * M_tot * t_max^2) = 6.694` | Issue doc lines 231, 258, 289; conflicts with locked PHYS-01 `D = (GT^2)^(1/3) ~ 4.6416` (`ctl_instruction.md` section 2.5, line 598 explicitly rejects the 6.694 form) | `claimed-unverified` | PIPE-09 / EVID-10: pose as convention conflict to adjudicate; locked counter-position is PHYS-01 raw-mass D ~ 4.6416 |

### Row Notes

**CLM-03 (blacklist 65):** The count `65 = 2 hierarchical + 63 standard` is directly observable
in `problematic_ics_blacklist.json`, but DATA-02 (Phase 24) owns the verification verdict on
both count/composition and loading/consumption status. The count is marked `claimed-unverified`
to reflect that Phase 23 does not perform empirical probes — Phase 24 does. The M11 finding
(blacklist not loaded at training time) is about consumption status, not count; that nuance is
preserved for Phase 24.

**CLM-05 (standard folder counts) — WR-04 open schema question:** this row covers two distinct
observables whose values coincide today: the IC folder counts recorded in the gold-gap record
(2,749 / 2,565 ICs) and the Brutus output folder counts (2,749 / 2,565 files). Whether CLM-05
is split into separate IC-folder and Brutus-output rows, or amended in place, is an **open
Phase 24 user-gate decision (WR-04)** — this register does not settle it. Phase 24's DATA-04
counts both observables independently.

**CLM-07 (219 no-footer standard-gold files):** the original package characterized these 219
files as having "minimal footers"; the 2026-06-10 erratum corrected this — the files contain
**no `Result:` footer and no parameter fields at all**. The count of 219 stands and the row
remains `verified`; only the characterization changed. See
[Correction Provenance](#correction-provenance-and-verification-boundaries) Correction 2.

**CLM-10 (snapshot counts):** The README explicitly warns against hard-coding snapshot counts
(Snapshot Count Note, lines 623–629); the `~` prefix signals approximation. These figures are
`claimed-unverified` and will be empirically verified in Phase 24.

**CLM-11 (`final_timestep >= 9.5` prevalence):** The gate rule itself
(`final_timestep >= 9.5`) is grounded in README Completeness Checks, but the *prevalence* (what
fraction of trajectories satisfy it) is not stated in any `Documentation/` file. The rule is
grounded; the prevalence figure is `claimed-unverified`.

**CLM-13 (`D = 6.694`):** This is NOT a dataset count. It is a contested convention claim: the
issue doc derives `D = cbrt(G * M_tot * t_max^2) = 6.694` using total-mass scaling, while the
locked v1.4 PHYS-01 convention uses raw-mass `D = (G * T^2)^(1/3) ~ 4.6416` and
`ctl_instruction.md` section 2.5 line 598 explicitly rejects the 6.694 form. This is posed as a
conflict to adjudicate in Phase 27 (PIPE-09) / Phase 25 (EVID-10), not as a figure to verify
empirically.

*This register is the source of truth for the PKG-03 claims list. Phase 24 consumes it as its
verification checklist (D-12).*

---

## Consolidated Dataset Context

**Purpose:** This section consolidates scattered dataset facts from multiple repository sources
into one self-contained place for external researchers. Each fragment is labeled with its
canonical source path and line range. Source paths are provenance labels, not navigation links
— the researcher has access only to snapshot copies in this package. Dataset-README fragments
quote the corrected README (post-2026-06-10 correction commits; see
[Correction Provenance](#correction-provenance-and-verification-boundaries)), so the facts
below already incorporate both erratum corrections.

**Convention:** Every dataset figure in this section references its CLM ID from the
[CLM Claims Register](#clm-claims-register). Figures are not stated as fact; their verification
status (claimed or verified) is recorded in the register (PKG-03).

**Exclusions:** Framework specs (`ctl_instruction.md`, `pinn_architecture.md`,
`sampling_method.md`) are NEVER consolidated here — they ship as byte-for-byte intact snapshots
in `specs/`. Live code under `pinn/` is excluded from this package entirely (SCOPE-10: the
issue doc's "Canonical" citation of `pinn/data-processing-pipeline-full.py` is overridden by
directive 2026-05-19; framework specs are the source of truth).

### Source: `simulation_data/Documentation/README.md` — Dataset Sizes (lines 81-87)

| Category | Size |
|----------|------|
| Final-stage IC datasets | ~59 MB |
| Brutus output datasets | ~4.8 GB |
| **Total** | **~4.86 GB** |

### Source: `simulation_data/Documentation/README.md` — File Naming Conventions and Mapping (lines 193-225)

#### IC Files

Non-gold folders use:
```
ic_hierarchical_XXXX.txt
ic_standard_XXXX.txt
```

**Historical note (2026-06-10):** the gold-standard IC folders were documented as using a
`_gold_` infix (`ic_hierarchical_gold_XXXX.txt`, `ic_standard_gold_XXXX.txt`). Those folders
have since been removed, so this naming is no longer verifiable on disk; no current IC file
uses a `_gold_` infix.

Where `XXXX` is a 4-digit zero-padded integer (e.g., `0000`, `0427`, `3998`).

#### Brutus Output Files

All four folders use the **base filename prefixes**; gold-standard folders do **not** add a
`_gold_` infix (verified against the on-disk tree 2026-06-10):

```
simulation_data/Data/brutus_output/brutus_hierarchical/brutus_hierarchical_XXXX.txt
simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard/brutus_hierarchical_XXXX.txt
simulation_data/Data/brutus_output/brutus_standard_quasi_random/brutus_standard_XXXX.txt
simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/brutus_standard_XXXX.txt
```

Gold-standard status is encoded **only** in the folder name; filenames do not encode it. When
parsing, the folder is the authoritative (and only) variant identifier.

**Note:** The mapping between IC and Brutus files is always by numeric ID, within the
corresponding folder pair:
- `ic_hierarchical_0427.txt` → `brutus_hierarchical_0427.txt` (same filename in the base and
  gold-standard Brutus folders)
- `ic_standard_0427.txt` → `brutus_standard_0427.txt` (same filename in the base and
  gold-standard Brutus folders)

Non-contiguous IDs are intentional — caused by generation continuation, prescreen rejection,
and failed Brutus runs. The numeric ID is NOT an index; gaps exist (CLM-01, CLM-02).

*(The original package stated that gold-standard Brutus filenames carry a `_gold_` infix; that
claim was corrected by the 2026-06-10 erratum — see
[Correction Provenance](#correction-provenance-and-verification-boundaries) Correction 1.)*

### Source: `simulation_data/Documentation/README.md` — Brutus Parameters by Variant (lines 578-629)

Important distinction:
- `dt_out` in Brutus outputs is the **output sampling interval**, not the internal
  Bulirsch-Stoer step size (which is adaptive and not directly stored in these text files).

#### Observed Parameter Sets (from `Result:` footers)

Most Brutus output files end with a `Result:` footer; a subset has **no footer at all** (counts
below; verified 2026-06-10, matching the missing-footer counts in
`Validation/audit_reports/footer_audit_20251224_170141.md`). Footers that are present carry the
full schema, including `eta` and `tol`. Files without a footer cannot be assigned a parameter
set from the file alone; for those, assume the folder-level defaults.

Each entry below is `(tol, Lw, dt_out, t_end, eta) -> count`. Files with no footer are listed
separately.

##### `brutus_hierarchical/` (CLM-06: 4,857 files; 3,307 with footer, 1,550 without)

Footers (full schema, with `eta`):
- `(1e-15, 130, 0.08, 10, 0.263027) -> 3,307`

No `Result:` footer:
- `-> 1,550` (no parameters recorded in-file; assume folder defaults: tol=1e-15, Lw=130,
  dt_out=0.08)

##### `brutus_hierarchical_gold_standard/` (4,857 files; all full-schema)

- `(1e-13, 130, 0.01, 10.01, 0.277971) -> 4,146`
- `(1e-13, 124, 0.01, 10.01, 0.277971) -> 649`
- `(1e-14, 118, 0.01, 10.01, 0.270396) -> 34`
- `(1e-14, 112, 0.01, 10.01, 0.270396) -> 27`
- `(1e-14, 124, 0.01, 10.01, 0.270396) -> 1`

##### `brutus_standard_quasi_random/` (CLM-05: 2,749 files; 2,048 with footer, 701 without)

Footers (full schema, with `eta`):
- `(1e-13, 118, 0.17, 10.03, 0.277971) -> 1,126`
- `(1e-13, 130, 0.17, 10.03, 0.277971) -> 922`

No `Result:` footer:
- `-> 701` (no parameters recorded in-file; assume folder defaults: tol=1e-13, Lw=118,
  dt_out=0.17)

##### `brutus_standard_quasi_random_gold_standard/` (CLM-05: 2,565 files; 2,346 with footer, CLM-07: 219 without)

Footers (full schema, with `eta` and `tol`):
- `(1e-13, 130, 0.01, 10.01, 0.277971) -> 1,754`
- `(1e-14, 130, 0.01, 10.01, 0.270396) -> CLM-08: 592`

No `Result:` footer:
- `-> CLM-07: 219` (no parameters recorded in-file; assume folder defaults: tol=1e-13, Lw=130,
  dt_out=0.01)

*(The original package stated that all Brutus output files contain a `Result:` footer and
characterized the 1,550 / 701 populations as "partial footers" and the 219 standard-gold
population as "minimal footers"; the 2026-06-10 erratum corrected this — those files contain no
footer and no parameter fields at all. See
[Correction Provenance](#correction-provenance-and-verification-boundaries) Correction 2.)*

#### Folder-default parameters (CLM-09)

| Variant | Default tol | Default dt_out |
|---------|------------|----------------|
| Standard quasi-random | 1e-13 | 0.17 |
| Hierarchical base | 1e-15 | 0.08 |
| Gold standard (both) | 1e-13 | 0.01 |

#### Snapshot count warning (CLM-10)

Avoid hard-coding exact expected snapshot counts (README "Snapshot Count Note", lines 623-629):
- `t_end` can be slightly larger than 10 (e.g., 10.01 or 10.03) when `dt_out` does not evenly
  divide the nominal stop time.
- Some runs may have been re-executed with different parameters, especially in gold folders.

Approximate snapshot counts are stated in the issue doc (CLM-10: ~59 standard / ~125
hierarchical / ~1000 gold), but the README explicitly warns against hard-coding these values.

### Source: `simulation_data/Documentation/README.md` — Completeness Checks (lines 633-647)

**Primary Check:** Final timestep >= 9.5

```python
# Validation pattern used in run scripts
timestep_pattern = re.compile(r'^(\d+\.?\d*)\s+3\s+\d+')
final_timestep = max([float(t) for t in timesteps])
if final_timestep < 9.5:
    # Mark as incomplete
```

**Do NOT rely on:**
- `Result:` footer presence or schema for completeness (a footer is absent in 1,550
  hierarchical-base, 701 standard-base, and 219 standard-gold files; where present it carries
  the full schema — see Observed Parameter Sets above)
- Line count thresholds (variable due to integration dynamics)

The `final_timestep >= 9.5` gate rule is grounded in README Completeness Checks (CLM-11). The
prevalence (what fraction of trajectories satisfy it) is `claimed-unverified` (CLM-11).

### Source: `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (full file)

Generated: 2026-03-18

#### Summary

- `ic_standard_quasi_random/` contains **CLM-05: 2,749** ICs.
- `ic_standard_quasi_random_for_gold_standard/` contains **CLM-05: 2,565** ICs.
- All 2,565 gold-standard ICs are a **byte-identical subset** of the standard ICs (differing
  only in filename prefix: `ic_standard_` vs `ic_standard_gold_`).
- **CLM-04: 184 ICs** exist in the standard folder but have no gold-standard counterpart.

These 184 ICs were simulated at standard Brutus resolution but were never selected for
gold-standard (higher temporal resolution, `dt_out=0.01`) re-simulation.

*(Provenance note: this is a full-file quote of a dated source record (2026-03-18). It
describes the IC folders as they existed then — including the `ic_standard_gold_` filename
prefix; the gold IC folders have since been removed (see the File Naming fragment above). The
184-ID list and the 2,749/2,565 counts are the substantive content (CLM-04, CLM-05).)*

#### The 184 IDs

```
0038  0042  0049  0138  0142  0149  0238  0242  0249  0338
0342  0349  0438  0442  0449  0504  0540  0555  0557  0579
0585  0586  0638  0642  0649  0704  0740  0755  0757  0779
0785  0786  0838  0842  0849  0904  0940  0955  0957  0979
0985  0986  1023  1043  1055  1061  1127  1130  1144  1148
1150  1154  1155  1191  1238  1242  1338  1342  1426  1440
1455  1457  1479  1485  1486  1538  1542  1549  1604  1640
1655  1657  1679  1685  1686  1702  1723  1743  1755  1761
1827  1830  1840  1844  1848  1850  1854  1855  1891  1909
1941  1956  1958  1975  2004  2039  2056  2060  2107  2110
2127  2136  2164  2172  2206  2219  2274  2277  2281  2351
2359  2382  2386  2402  2439  2455  2460  2495  2538  2542
2604  2640  2655  2657  2679  2685  2686  2723  2743  2755
2761  2827  2830  2844  2848  2850  2854  2855  2909  2941
2956  2958  3004  3039  3056  3060  3107  3110  3136  3172
3219  3277  3359  3362  3368  3382  3386  3402  3439  3455
3460  3538  3542  3604  3640  3655  3657  3679  3685  3686
3723  3743  3755  3761  3827  3830  3844  3848  3850  3854
3855  3891  3941  3958
```

Total: **184 IDs**

### Source: `simulation_data/Documentation/problematic_ics_blacklist.json` — Blacklist Summary (CLM-03)

The blacklist is a JSON object with two keys: `hierarchical` and `standard`.

- **`hierarchical`**: 2 IDs (123, 253)
- **`standard`**: 63 IDs (first entries: 21, 30, 52, ...)
- **Total: CLM-03: 65 IDs** (2 hierarchical + 63 standard)

This count is observable in the JSON file. The count itself is `claimed-unverified` (CLM-03)
because Phase 23 performs no empirical probes; Phase 24 (DATA-02) verifies both
count/composition and the loading/consumption status at training time (the M11 finding).

### Source: `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` — Provenance Excerpt (SCOPE-07)

This script processes all Brutus output files across the four variant directories, calculating
conservation metrics (energy, momentum, angular momentum) and producing JSON metric files for
every output file, even if partial or erroneous.

**Key structural details (provenance for metric-related findings):**

Input directories enumerated in the script:
- `brutus_hierarchical/`
- `brutus_hierarchical_gold_standard/`
- `brutus_standard_quasi_random/`
- `brutus_standard_quasi_random_gold_standard/`

Output goes to `simulation_data/Data/metrics/` with per-variant subdirectories.

Brutus parameter defaults recorded in the script (`BRUTUS_PARAMS` dict):
- Hierarchical: tolerance=1e-15, word_length=130, dt_out=0.08
- Standard: tolerance=1e-13, dt_out=0.17

The script does NOT perform completeness checks (no `final_timestep >= 9.5` gate); it processes
all files found. Completeness checking is the responsibility of downstream consumers.

**Relevance to findings:** This script is the provenance grounding for how metrics were
calculated (SCS/SASD/IPR/PSC definitions are in `data_quality_assessment.md` section 3, not in
this script). The script's output feeds the metric values that Phase 24 will re-verify against
the claims register.

### Per-Finding SCOPE-07 Inclusion Matrix

| Finding area | Scripts directory source | Included? | Rationale |
|---|---|---|---|
| Metrics calculation provenance | `calculate_metrics.py` | Yes (excerpt above) | Grounds how metrics were produced; feeds DATA-05/DATA-06 |
| Prescreening thresholds | `Validation/prescreening/` | No excerpt needed | Prescreening is upstream of Brutus; the findings concern Brutus outputs and downstream ingestion, not prescreen logic. README documents prescreen outcomes (ID gaps) sufficiently. |
| Brutus runner parameters | `Scripts/brutus_runners/` | No excerpt needed | README Brutus Parameters section documents the per-variant parameter sets exhaustively. Runner scripts invoke Brutus with those parameters; the README is the more direct source for adjudication. |

*End of consolidated dataset context. Every dataset figure above references its CLM ID from the
[CLM Claims Register](#clm-claims-register). No `pinn/` content is included (D-06/SCOPE-10). No
framework spec content is consolidated here (D-03).*

---

## Correction Provenance And Verification Boundaries

This section preserves the package's correction history and states what remains unverified. It
is the supersession target for the Phase 24 **DATA-07 correction addendum** (see
[Supersession](#supersession-and-the-authoritative-correction-channel) below).

### Consolidation Record (2026-06-11)

On user instruction dated 2026-06-11, the five top-level research-context files of this package
(`README.md`, `framed-research-questions.md`, `claims-table.md`, `consolidated-context.md`,
`ERRATUM-2026-06-10.md`) were consolidated into this single master file as a Phase 23
post-delivery remediation. `DELIVERY-NOTE.md` remains standalone; all five `specs/*.md`
snapshots are byte-identical to their pre-consolidation state. Pre-change SHA-256 hashes of all
eleven package files, source heading inventories, and the verification evidence for this
remediation are committed in
`.planning/phases/23-research-package-assembly/23-VERIFICATION.md` ("Master Consolidation
Baseline" and the associated remediation-verification sections). The consolidation source
baseline is repo state `27b05432ae76dd43227c4e4f2333e25b5469ca18`.

The consolidation integrated the erratum's two grounded corrections directly into the current
text (dataset-context fragments and CLM register above) instead of leaving them in a separate
sibling erratum. No CLM ID changed, no CLM status was upgraded or downgraded, and no
open governance decision was settled by the consolidation.

### Erratum 2026-06-10 (integrated)

**Scope:** interim correction to two dataset claims carried in this package, found by the
2026-06-10 documentation integrity audit after the package was finalized and delivered. It was
originally shipped as an added sibling file (`ERRATUM-2026-06-10.md`) that modified no
delivered package file; its content is integrated here as of the 2026-06-11 consolidation.

#### Correction 1 — Gold-standard filenames carry no `_gold_` infix

**Affected:** the file-naming narrative in the consolidated dataset context (File Naming
Conventions and Mapping fragment). No CLM row carries this claim.

**The package originally stated:**

> Gold-standard folders use a `_gold_` infix: `ic_hierarchical_gold_XXXX.txt`,
> `ic_standard_gold_XXXX.txt` […] Non-gold and gold-standard folders use **different filename
> prefixes**: […] `brutus_hierarchical_gold_XXXX.txt` […] `brutus_standard_gold_XXXX.txt` […]
> Gold-standard status is encoded in **both** the folder name and the filename.

together with ID-mapping examples of the form `ic_hierarchical_gold_0427.txt ->
brutus_hierarchical_gold_0427.txt`.

**Corrected disk fact:** no file in either gold-standard Brutus output folder carries a
`_gold_` infix — 0 of 4,857 files in the hierarchical gold folder and 0 of 2,565 in the
standard gold folder. All four Brutus output folders use the base filename prefixes
(`brutus_hierarchical_XXXX.txt`, `brutus_standard_XXXX.txt`); gold-standard status is encoded
**only** by the folder name. The numeric-ID mapping itself is unchanged (same filename in the
base and gold folders). The gold IC folders were removed, so the IC-side `_gold_` naming is
unverifiable rather than contradicted.

**Evidence:** direct disk verification 2026-06-10 (listing each gold folder and counting
`_gold_` matches returns 0); the dataset documentation README — the source of these package
claims — was corrected on user sign-off in commits `d18f676` ("correct gold filename claims in
dataset spec readme") and `31b2cff` ("correct remaining gold infix mapping in dataset
readme").

#### Correction 2 — "Partial"/"minimal" footer populations have no `Result:` footer at all

**Affected:**

- CLM register row **CLM-07** (originally "Minimal standard-gold footers — 219 files with
  minimal footers", status `verified`): the **count of 219 stands**; the characterization was
  wrong — those files contain no footer of any kind. The row above now carries the corrected
  characterization; its status is unchanged.
- The consolidated dataset context (Observed Parameter Sets fragment): the original statement
  "All Brutus output files contain a `Result:` footer", the partial-footer entries
  "`(1e-15, 130, 0.08, ~10) -> 1,550` (same parameters, different Brutus build omitted `eta`)"
  and "`(1e-13, 118, 0.17, ~10.03) -> 701`", and the minimal-footer attribution of the 219
  standard-gold files.

**Corrected disk fact:** exactly 1,550 (hierarchical base), 701 (standard base), and 219
(standard gold) files end with their final snapshot block and contain **no `Result:` line and
no parameter fields anywhere in the file** (`eta`, `tol`, `Lw`, and energy fields are all
absent). tol/Lw/dt are **not** parseable from these files; the folder-level defaults must be
assumed for them. Footers that are present carry the full schema, including `eta` and `tol`.
The "different Brutus build" provenance explanation is unverifiable from the artifacts and has
been removed from the corrected source.

**Evidence:** direct disk verification 2026-06-10 (footer scan of all 15,028 files across the
four Brutus output folders, plus full-file marker scans on samples); consistent with the
2025-12-24 footer audit record (`footer_audit_20251224_170141.md`), whose "Missing Footer"
column records the same 1,550 / 701 / 219 counts; the dataset documentation README was
corrected on user sign-off in commit `ae609f3` ("recharacterize missing footers in dataset
spec readme").

#### Not affected — do not over-discount the package

Re-verified correct by the same 2026-06-10 audit:

- **CLM-09** — the folder-default `tol` / `dt_out` values per variant.
- **The file counts** behind CLM-05 and CLM-06 (2,749 and 4,857), the CLM-07 count (219), and
  the CLM-08 count (592 files at tol=1e-14 in the standard gold folder).
- **All full-schema footer parameter tuples** listed in the consolidated dataset context,
  including both gold-folder distributions — re-derived exactly as stated.

No other package content is touched by these corrections.

### Citation Corrections Applied At Consolidation (2026-06-11)

The 2026-06-11 consolidation also routed the following grounded citation corrections (Phase 23
review items WR-02 and WR-03) through this master's current text. Per the user-directed
consolidation, these corrections live here rather than in an erratum extension:

- **WR-02 (applied):** Hard Constraint 3 originally cited the §10.2 "COM Invariance" acceptance
  check at `specs/pinn_architecture.md` line 972; the section heading is at **line 967**
  (verified against the snapshot). The Hard Constraints section above carries the corrected
  line.
- **WR-03 (applied):** Q-B1's framework-spec position originally cited
  `specs/ctl_instruction.md` "§5.3.2" — stale issue-doc numbering that does not exist in the
  spec snapshot. The actual section is **"Mini-Batch Construction with Lookahead Sampling"
  (line 1197)** (verified against the snapshot). Q-B1 above carries the corrected citation.
- **WR-01 (surfaced, not resolved):** Q-B2 originally reported the issue doc's mass-drift
  protocol as "~1000 IC–Brutus pairs", citing P2-2 — which actually says 100. The issue doc
  internally conflicts: its protocol prose says 1,000 pairs (line 202) while P2-2 says 100
  pairs (line 292). Q-B2 above now reports both figures as an explicit internal issue-doc
  conflict. Whether this conflict receives its own CLM row is an **open Phase 24 user-gate
  decision** — not settled here.
- **Dataset-README line citations updated:** CLM rows and dataset-context fragment labels now
  cite the corrected dataset README's current line numbers (the README was corrected
  2026-06-10 in commits `d18f676`, `31b2cff`, `ae609f3`, which shifted some sections).

### Open Verification Boundaries

- **WR-01** — whether the issue-doc 1,000-vs-100 sample-size conflict receives a new CLM row:
  **OPEN**, owned by the Phase 24 user gate. Reported in Q-B2; not settled here.
- **WR-04** — whether CLM-05 is split into separate IC-folder and Brutus-output rows or amended
  in place: **OPEN**, owned by the Phase 24 user gate. Reported in the CLM-05 row note; not
  settled here.
- **Phase 24 empirical verification (DATA-01..07) has not executed.** No CLM row's status was
  changed by this consolidation; every row retains its Phase 23 status. The remediation's
  2026-06-11 read-only dataset re-scan (recorded in `23-VERIFICATION.md`) is remediation
  evidence only — it is not a Phase 24 committed probe result and promotes nothing to
  `verified`.
- **The Phase 25–29 gate is unchanged:** adjudication phases gate on both the external
  resolution doc landing and Phase 24 completion (see `DELIVERY-NOTE.md`).

### Supersession And The Authoritative Correction Channel

The Phase 24 **DATA-07 correction addendum** (CLM-keyed; announced in `DELIVERY-NOTE.md`) is
the authoritative correction channel for this package. When produced, it will be a standalone
sibling file in this package and **supersedes this section's interim correction record** for
any claim it covers. This master file is not edited in place by that addendum.
