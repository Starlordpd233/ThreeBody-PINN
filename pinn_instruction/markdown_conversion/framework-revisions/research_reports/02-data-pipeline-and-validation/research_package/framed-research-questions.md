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
