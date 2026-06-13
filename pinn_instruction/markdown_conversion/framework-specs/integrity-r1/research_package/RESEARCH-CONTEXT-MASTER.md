---
title: Integrity R1 Research Context Master — Framework Integrity Audit
package_for: integrity-r1 (disruption-first audit of the three framework specs)
role: research-context entry point (orientation, source tiers, review dimensions RD-1..RD-8, output contract)
status: active
created: 2026-06-12
source_baseline: 14bd96e19d30dd8c25e5045ad1c40567f871644e
self_contained: true
---

# Integrity R1 Research Context Master — Framework Integrity Audit

This file is the entry point for **integrity-r1**, a disruption-first integrity audit of
the three framework specification documents of a computational-physics ML project: a
curriculum-trained physics-informed neural network (CTL-PINN) that learns gravitational
three-body trajectories from a frozen dataset of high-precision (Brutus
arbitrary-precision integrator) simulations, to be trained on a single MacBook by a
project owner who is not an expert at model training.

**Your task in one sentence:** before the project builds anything against these specs,
find everything in them — alone or in combination — that would force disruptive change
later: incoherence between specs, unbuildable or under-specified steps, mathematical or
physical errors, scientifically unsound choices, and fragile load-bearing assumptions.

**Disruption-first means:** your most valuable output is the finding that invalidates or
re-scopes downstream work, surfaced *now* while change is cheap. Rank accordingly. A
confirmed "this cannot work as specified" is worth more than fifty style notes; an
explicit, falsifiable "checked this thoroughly, found nothing" is itself a valued
deliverable — it retires risk.

## Standing of your report

Your report enters the project as a **findings register** — it is **NOT** a candidate
verdict source and **NOT** a grounding source for spec edits. No statement in it will be
transcribed into the specs on your authority; every finding feeds a human triage that
routes it into the project's adjudication machinery. Consequence for you: do not soften
findings out of deference, and do not phrase recommendations as decisions. Findings with
evidence, plus a consolidated decision list, are exactly what is wanted.

## You are working from attached files only

You have no access to the project's repository or dataset. Alongside this file you have
been given exactly five other documents, referred to throughout by bare filename. The
attached spec snapshots are byte-identical pins and may mention files or paths that are
not attached; treat any such reference as unavailable — note it in your §7 open-items
register if it matters — rather than guessing at its content.

| File | Role | How to treat it |
|---|---|---|
| `RESEARCH-CONTEXT-MASTER.md` | This file — orientation, source tiers, review dimensions, output contract | Read first; follow exactly |
| `ctl_instruction.md` | Framework spec — CTL methodology: data characterization/stratification, preprocessing, invariants, input-vector formulation, curriculum staging, training loop | **Audit subject.** Authoritative *within the project*, which is exactly why every error in it matters |
| `pinn_architecture.md` | Framework spec — network architecture, loss functions, AD contract, output head, inference, acceptance checks | **Audit subject.** Same standing |
| `sampling_method.md` | Framework spec — how the (now frozen, completed) dataset's initial conditions were generated and prescreened | **Audit subject, special standing:** historical record of completed generation work; frozen by default, not an active revision target. Audit it for what it implies about the data and for contradictions with the other two specs; treat "change the generation method" recommendations as one-way doors (the dataset will not be regenerated) |
| `DATASET-CONTEXT.md` | Consolidated, per-fact-labeled empirical facts about the training dataset, including stale-figure corrections and the staged missing-184 standard-gold rerun status | Your only dataset evidence. `verified-empirically` entries are Tier-1 facts; `active-staged-remediation` entries are current process state, not adopted dataset facts; the file's "Figures that moved" table corrects stale figures cited in the bundle |
| `KNOWN-ISSUES-AND-IN-FLIGHT-BUNDLE.md` | Three verbatim-embedded project documents (a data-quality research report; a candidate-verdicts resolution doc under adjudication; an unadjudicated curriculum/training-loop issue doc), each behind an authority banner, plus the project's in-flight work register | Read **last**. Evaluative material and novelty-classification anchor — never defaults to adopt. Respect each embedded doc's authority banner |

## Recommended read order — and an honest caveat

Recommended order: (1) this file in full; (2) the three specs (`ctl_instruction.md`,
then `pinn_architecture.md`, then `sampling_method.md`); (3) `DATASET-CONTEXT.md`;
(4) `KNOWN-ISSUES-AND-IN-FLIGHT-BUNDLE.md` **last**, so your own reading of the specs is
formed before you see the project's existing critiques and candidate verdicts.

**Honesty caveat:** if you are a research platform that ingests all attachments
simultaneously, this read order is *advisory* and cannot be enforced — we know that. The
load-bearing anchoring mitigation is not the read order; it is the mandatory **novelty
classification** on every finding (`novel` / `confirms-known` / `contradicts-known` /
`against-in-flight-edit`), which forces you to state explicitly whether a finding is
your own or an echo of the bundle. Apply it honestly. A finding that merely restates a
bundle position without independent verification must be tagged `confirms-known` and
carry your own evidence for why you concur.

## Three-tier source treatment

**Tier 1 — fixed facts (not challengeable; constraints on every finding):**

1. The verified dataset baseline in `DATASET-CONTEXT.md` is fixed for this audit. The
   only current data-change exception is the explicitly labeled staged rerun of the 184
   missing standard-gold outputs; do not assume those outputs exist until validated and
   promoted. Findings whose only resolution requires other different data are still
   wanted — but must be flagged as one-way doors.
2. Training happens on a single MacBook (Apple-Silicon laptop, unified memory); no
   cloud, no cluster.
3. Every `verified-empirically` entry in `DATASET-CONTEXT.md`.
4. Project governance: where sources are silent or ambiguous, the project's culture is
   to surface gaps rather than invent resolutions — your report must do the same.

**Tier 2 — locked decisions-of-record (challengeable ONLY via the protocol below):**

These were adjudicated and locked by the project's previous milestone. They are stated
here as the project records them; verify their exact formulations against the specs (a
discrepancy between this list and a spec is itself a finding):

1. **14D network input contract** — input is exactly `[τ, IC₁₃]` with `τ = 2u − 1`,
   `u = t/T`.
2. **Jacobi IC₁₃ vector** —
   `IC₁₃ = [m₁, m₂, m₃, ρ_x, λ_x, λ_y, ρ̇_x, ρ̇_y, ρ̇_z, λ̇_x, λ̇_y, λ̇_z, E]`, mass
   slots carrying *raw masses*.
3. **Mass-weighted COM projection output head** — the network predicts only the 9-dim
   position vector; velocities/accelerations derive from the *projected* positions by
   automatic differentiation; the COM projection is applied before any loss or metric.
4. **Softening + dual-epsilon** — training-time force uses Plummer softening with
   `ε_train = 10⁻⁵`; validation metrics use a static `ε = 10⁻¹⁰`.
5. **Post-v1.3 screening gate** — `ε_H = max_t |(H(t) − H(0))/H(0)|`,
   `SCS = log₁₀(ε_H)`, reject gate `SCS > −5` (i.e. `ε_H > 10⁻⁵`). Its only written
   home is the embedded `data_quality_assessment.md` (a non-authoritative report) — that
   placement quirk is known to the project.
6. **Characteristic length convention** — raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` with
   `G = 1`; the mass-fraction alternative `D = (G·M_tot·T²)^(1/3) ≈ 6.694` is explicitly
   rejected in the spec.

**Tier 3 — ordinary design content (fully reviewable):** everything else in the three
specs — architecture details, loss formulations and weights, curriculum staging,
stratification, preprocessing, hyperparameters, evaluation protocol, prose. No
deference owed.

### Locked-decision challenge protocol (Tier 2)

You MAY challenge a Tier-2 locked decision, but only under all three of:

1. **High evidence bar** — `derived-math` or `literature-cited` evidence (not
   `judgment` alone) that the locked decision materially endangers the project's goal.
2. **Steelman first** — before the challenge, state the strongest case for the locked
   decision (the project adjudicated these deliberately; engage the reasoning, not a
   caricature).
3. **Flag** — the finding carries an explicit `locked-decision challenge` flag and is
   automatically at least severity S2.

## In-flight work — timing and the `against-in-flight-edit` tag

The project is mid-milestone: an adjudication of data-pipeline-and-validation issues is
in flight. Its first tranche (DataLoader ingestion and selection contracts) has **already
landed in the attached `ctl_instruction.md`** and is part of what you are auditing; the
next tranche (sampling/precision/global-scale) is in planning with no adopted spec edits
yet; the validation-metric data-side definitions remain pending. The bundle's in-flight
register enumerates every topic by phase and marks which have landed. This audit is
deliberately commissioned *anyway*: disruption surfaced now is more useful than
disruption serialized until after those edits. Your obligations are only:

- Tag any finding overlapping a still-pending in-flight topic (the register marks which
  are pending vs already-landed) as `novelty: against-in-flight-edit`. Findings on
  already-landed contracts are ordinary audit findings against the attached spec text.
  Such findings are still fully wanted — the tag routes pending-topic findings to the
  owning workstream.
- Audit the specs **as attached** (the pinned snapshots), not as you guess they might
  look after in-flight edits.
- Do not answer the training-execution round's questions (the bundle register lists
  them); note interactions in blast radius instead.

## Review dimensions

Work through all eight dimensions, in this order — they are ordered by disruption
priority: RD-1 can invalidate everything downstream; later dimensions catch
progressively narrower classes of issue. Budget your depth accordingly. Every dimension
must produce: (a) findings in the output schema, (b) a per-dimension coverage statement
(what you examined and how), and (c) a "checked, found nothing" register for the
sub-checks that came back clean.

### RD-1 — Fundamental viability red-team (deepest treatment)

Can the as-specified CTL-PINN plausibly achieve its goal on this frozen dataset? Engage
PINN failure modes on chaotic / long-horizon dynamics, the curriculum premise, and
loss-design convergence plausibility — with literature citations throughout. This is the
single most disruptive possible finding; treat it with corresponding rigor and steelman
the design before concluding against it.

Named sub-checks:

- **(i) Lyapunov-time-aware evaluation feasibility.** Is the trained-model acceptance
  criterion quantitative, chaos-aware, and achievable given the integrator's accuracy
  ceiling and the chaotic-divergence horizon? An acceptance criterion that can never
  pass is a build-time landmine; one that is not chaos-aware (pointwise trajectory error
  over horizons beyond the Lyapunov time) may be unfalsifiable or vacuous. State what
  the specs' evaluation metrics actually measure and over what horizon.
- **(ii) Sufficient-data plausibility.** Given the dataset inventory in
  `DATASET-CONTEXT.md` (including the post-remediation population), is there enough
  training signal for the curriculum to do what the stages claim — per stage, not just
  in aggregate?
- **(iii) Symmetry treatment.** Are permutation / rotation / translation / Galilean /
  scaling symmetries of the three-body problem exploited, ignored, or violated by the
  14D input and the output head — and is the choice consistent across curriculum stages?

**Literature anchors (engage these, and search beyond them):**

- Breen, Foley, Boekholt & Portegies Zwart (2019), *"Newton vs the machine: solving the
  chaotic three-body problem using deep neural networks"* — NNs trained on
  **Brutus-generated** three-body data; the same generator lineage as this project and
  the most directly comparable prior work. Engage what it achieved, on what problem
  restriction, and how this project's scope differs.
- Krishnapriyan, Gholami, Zhe, Kirby & Mahoney (2021), *"Characterizing possible
  failure modes in physics-informed neural networks"* — the canonical PINN failure-mode
  taxonomy.
- Wang, Sankaran, Wang & Perdikaris (2023/2024), *"An Expert's Guide to Training
  Physics-Informed Neural Networks"* — current best-practice synthesis.

### RD-2 — Cross-spec coherence

Find contradictions across (and within) the three specs. Named seams to check
explicitly: the input-vector definition (including the in-spec flag SI-CTL-001); the
normalization / global-scaling chain; the AD / derivative contract (normalized time);
batch construction (including the in-spec flag SI-PINN-003 if present); curriculum
stages vs. data stratification; the conservation-loss formulations; output frame and
file format.

New sub-checks:

- **(i) Within-and-across-doc seam hunt.** The specs were revised section-by-section
  during a previous milestone; revision seams are where stale text contradicts newer
  locked contracts. Flag any section that reads as pre-revision in voice or content but
  coexists with newer conventions (e.g., text that contradicts a Tier-2 contract without
  acknowledging it).
- **(ii) Single-source-of-truth analysis.** Flag any fact normatively defined in two or
  more places *even if currently consistent* — duplicated definition is drift risk, and
  the project wants the inventory.
- **(iii) Cross-reference validity.** Every "see section X" / "as defined in Y" in every
  spec must land on a target that exists and says what the referrer claims. Check them
  all; broken or stale cross-references are the most common silent-drift source.
- **(iv) Authority hierarchy clarity.** When two specs disagree, is a conflict-resolution
  rule stated anywhere ("X takes precedence over Y")? If not, say so — a build agent
  will otherwise resolve conflicts arbitrarily.

### RD-3 — Buildability gap audit

Apply the no-invention standard: walk the pipeline end-to-end **as an implementing agent
that is forbidden to invent** — parse → preprocess → invariants → input assembly →
network → losses → training loop → stage transitions → evaluation. At every step ask: is
each definition, shape, unit, edge case, and hyperparameter fully specified by the
attached documents alone? Deliver the gap list keyed to pipeline step + spec section.

New sub-checks:

- **(i) External-reference dependency.** Does any spec lean on a document not in this
  package to be buildable (a paper, an external library's behavior, a dataset card)?
  Each such reliance is a self-containment gap.
- **(ii) Normative-vs-informative readability.** Can a builder reliably distinguish
  requirement from commentary? Flag passages whose modality is ambiguous (history,
  alternatives, and requirements interleaved without markers).
- **(iii) Tensor-shape audit.** Every input, output, intermediate, loss-input, and
  per-stage tensor shape explicitly stated? Shape ambiguities are silent until the first
  training step.
- **(iv) Hyperparameter scope.** For every hyperparameter: value, range, source of truth
  (which spec defines it), per-stage override semantics, and where the override happens.
- **(v) Reproducibility closure.** Seeds for data sampling, model init, optimizer,
  dataloader, and any stochastic curriculum decision — all specified? Is the RNG chain
  documented end-to-end?
- **(vi) Failure-mode behavior.** For every step that *can* fail at training time
  (diverging loss, NaN gradient, plateau, stage gate never met): is the prescribed
  response (LR cut, rollback, abort) specified?
- **(vii) Determinism boundary.** What is deterministic vs stochastic at training time,
  and is that boundary the same at evaluation time?

### RD-4 — Mathematical and physics correctness

Verify the equations: derivations, dimensional consistency, conservation formulations,
gauge/frame correctness, SIREN initialization math.

New sub-checks:

- **(i) Re-derive every closed-form expression from first principles**; show your work
  wherever you disagree.
- **(ii) Dimension-check every numeric constant** — including every loss weight, stage
  threshold, and scheduler coefficient.
- **(iii) Conservation-form consistency.** The total-energy and angular-momentum forms
  used in losses must be derived in the same coordinate system, the same normalization,
  and the same softening treatment as the network's output head. Verify, don't assume.
- **(iv) Softening–conservation interaction.** Plummer softening removes the 1/r
  singularity but breaks exact conservation of the unsoftened Hamiltonian. Do the
  energy / angular-momentum loss terms account for softening-induced drift —
  analytically, by an empirical floor, or not at all? If the specs use a
  matched-softened Hamiltonian, check the matching is exact.
- **(v) Autodiff round-off.** Second-derivative autodiff (∂²/∂t² for the physics
  residual on positions) is noise-sensitive under chaotic dynamics. Assess float32 vs
  float64 implications for the AD contract as specified — as analysis, noting that the
  project's precision contract is an in-flight topic (tag accordingly).

### RD-5 — Ambiguity audit

Find statements with two or more defensible readings that yield different
implementations. For each: quote the statement, give the readings, state which the
surrounding context favors (if any), and what each reading does downstream.

New sub-checks:

- **(i) Modal-language audit.** "may", "should", "must", "typically", "often",
  "approximately" — flag instances where the modal does not map to a definite code
  branch.
- **(ii) Unit and coordinate ambiguity.** Every numeric literal should have a stated
  unit and reference frame; "the position" without "in which frame" is two specs in one.
- **(iii) Stage-boundary semantics.** Is the moment a curriculum stage advances
  well-defined? Is the model/optimizer state at the boundary (learning rate, momentum,
  dataloader RNG, loss-term state) well-defined?
- **(iv) Loss-weighting collision.** When a stage advances, what happens to the relative
  magnitudes of the per-component loss terms? A silently-too-small weight effectively
  drops a term; a silently-too-large one dominates. Check the specified schedules
  compose across stage boundaries.

### RD-6 — Scientific soundness and best practices

Judge design choices against current PINN/SciML literature and ML engineering practice.
**Steelman before criticizing** — the project has reasoned about these choices; engage
that reasoning. Numerical-precision and compute red flags at the spec level are in
scope, with two carve-outs: the project's precision contract is in-flight (analysis
welcome, tag `against-in-flight-edit`), and runtime feasibility estimation belongs to
the training-execution round (note interactions only).

New sub-checks:

- **(i) Curriculum-design precedent check.** Is the staged curriculum (weighting ramps,
  stage-advancement gates) consistent with successful curriculum-learning practice on
  comparable problems? Cite precedent either way.
- **(ii) Loss-design convergence plausibility.** Multi-component PINN losses with
  stage-conditional weights are notorious for one-term-dominates-all failures. Is there
  a convergence argument or literature precedent for this configuration?
- **(iii) Data-split soundness.** Train/val/test split, leakage check (e.g., trajectories
  from the same IC family or the same base/gold pair landing across splits), and
  stratified-sampling soundness — as specified, not as charitably imagined.
- **(iv) Steelman locked contracts.** Every time RD-6 flags a design choice, also
  articulate the strongest argument for why it was chosen.
- **(v) Compute red flags at the spec level.** E.g., per-step memory growth under the
  specified batch/accumulation scheme, validation cadence vs dataset size, model size vs
  training horizon — flag what the spec *implies*, parameterized where facts are
  missing; do not invent runtime numbers.

### RD-7 — Data–framework compatibility

Check every dataset property the specs assume against the verified facts in
`DATASET-CONTEXT.md`, respecting its per-fact status labels (that labeling is the
load-bearing mechanism here — a spec assumption resting on a `claimed-unverified` fact
is a finding in itself). Respect in-flight markers: several known data-pipeline
mismatches are mid-adjudication; tag overlapping findings `against-in-flight-edit`
rather than re-adjudicating them, and focus fresh effort on assumptions nobody has
checked.

### RD-8 — Load-bearing assumptions and risk register

Enumerate the assumptions the design rests on, the evidence status of each, and what
breaks if each is false. This dimension synthesizes; it may cite findings from RD-1..7.

New sub-checks:

- **(i) Two-way vs one-way door classification.** For each load-bearing assumption, is
  the dependent design decision reversible (a different schedule, a different stage
  count) or irreversible (anything requiring data regeneration — the dataset is
  frozen)?
- **(ii) Compound-failure analysis.** Flag combinations of individually-soft assumptions
  whose *joint* failure probability is unacceptable (e.g., "softening negligible" +
  "conservation well-posed" + "late stages have enough data").
- **(iii) Mitigation-cost ranking.** For each load-bearing assumption: what would
  mitigation take (a config flag? a spec edit? regeneration — impossible)? Rank the
  register by mitigation cost as well as impact.

## Output contract

Deliver a **single self-contained markdown document**. Every finding must carry ALL of
the following fields:

- **Stable ID** — `INT-NNN`, assigned in order of first appearance, starting at
  `INT-001`.
- **Severity** — exactly one of:
  - **S1 — invalidates or re-scopes the core approach.** Potentially one-way (locked
    contracts or the frozen dataset implicated). Examples: the 14D input is the wrong
    inductive bias for the problem class; a PINN cannot reach the specified accuracy on
    chaotic orbits regardless of training budget.
  - **S2 — a builder cannot proceed, or two specs give contradictory instructions.**
    Must be resolved before the project's next spec-edit phase. Examples: the
    input-vector definition disagrees between two specs; a stage-advancement gate is
    undefined.
  - **S3 — implementable but rework-likely, or violates cited best practice.** Should
    be addressed during current or near-term spec work. Examples: a loss-weighting ramp
    is non-monotonic across a stage boundary; the data split risks leakage; the eval
    protocol is not chaos-aware.
  - **S4 — hygiene, clarity, naming, ergonomics.** Compress ALL S4 findings into a
    single appendix; do not let them dilute S1–S3 visibility.
- **Blast radius** — affected spec sections (file + heading) AND downstream work
  invalidated (which in-flight phase topic, which training-execution topic — per the
  bundle's register).
- **Door type** — one-way / two-way, with a one-sentence justification.
- **Novelty** — `novel` / `confirms-known` (already covered by the bundle) /
  `contradicts-known` (disagrees with a bundle position) / `against-in-flight-edit`
  (overlaps an in-flight spec-edit topic).
- **Evidence class** — `quoted-textual` (quotes both sides verbatim with file +
  section) / `derived-math` (re-derivation shown) / `literature-cited` (full citation) /
  `judgment` (analyst call, no external anchor). List all classes that apply.
- **Candidate resolution direction** — specified to the level a spec author could
  transcribe without further interpretation: exact formula, exact threshold, exact
  section to modify. For `contradicts-known` findings, also state what your direction
  does to the existing position. (This is a *direction*, not a decision — see Standing.)
- **Verification suggestion** — one line: how the project could independently confirm
  the finding is real.
- **Confidence** — High / Medium / Low, plus the single most important factor that
  would change your answer.

**Anti-padding rule:** "checked, found nothing" is a required, valued output per
dimension — carried by the per-dimension coverage statement and negative-results
register, never by filler findings. Do not manufacture findings to look thorough; the
coverage matrix (below) is how thoroughness is demonstrated.

### Required output sections, in this order

1. **Header** — title, date, and a one-line inventory of the six package files you
   actually received (so input mismatches are detectable).
2. **§0 Scope and decision standard** — what was covered, what was excluded and why,
   the evidence standard applied.
3. **§1 Top Disruptions** — ranked list of the 5–10 most disruptive findings, ordered
   severity-first, then by blast-radius magnitude. This is the section the project
   reads first; it must stand alone.
4. **§2 Decision matrix** — one row per finding: ID | severity | novelty | door |
   one-line verdict.
5. **§3 Coverage matrix** — for **every H1 and H2 heading enumerated below**, exactly
   one verdict: `audited-clean` / `findings: INT-NNN, …` / `skimmed-only` (with a
   reason, e.g. "non-normative commentary"). This is the audit's single most important
   defense against confident-sounding 40%-coverage.
6. **§4 Constants and contracts concordance** — the seeded table below, completed and
   extended: shared element | value as stated in `ctl_instruction.md` | value as stated
   in `pinn_architecture.md` | value as stated in `sampling_method.md` | match verdict.
   Record "absent" / "implied (cite)" where a spec does not state an element — absence
   is data. Any mismatch or double-definition becomes a finding (RD-2).
7. **§5 Resolutions by dimension** — per-RD subsections, each containing the coverage
   statement, that dimension's findings (full schema), and its "checked, found nothing"
   register.
8. **§6 Consolidated minimum-decision-list** — the smallest set of project-owner
   decisions needed to make the spec suite build-ready. Each entry: a question, options
   A/B/C(+), trade-offs per option, your recommendation, and confidence. (This format
   drops directly into the project's adjudication machinery — keep it clean.)
9. **§7 Open items register** — every "insufficient evidence" and additional-input-needed
   item in one place, including unattached references that mattered.
10. **References** — full citations for all external sources used.

### Coverage-matrix enumeration (audit every one of these)

Your §3 must carry a verdict for each heading below — 26 in `ctl_instruction.md`, 25 in
`pinn_architecture.md`, 12 in `sampling_method.md` (H1/H2 only; line numbers refer to
the attached snapshots; code-comment lines inside fenced blocks are excluded).

**`ctl_instruction.md`:**

| Line | Level | Heading |
|---|---|---|
| 9 | H1 | Important Note |
| 17 | H1 | Characterizing and Organizing the Multi-Fidelity Simulation Data |
| 19 | H2 | Existing Training Dataset |
| 44 | H2 | Multi-Fidelity Dataset and Physical Invariants |
| 105 | H2 | Multi-Stage Data Stratification by Difficulty (Revised to handle the issue that virial ratio is not preserved for quasi-random IC sampling) |
| 262 | H1 | A Glimpse at the Data |
| 334 | H1 | Phase 1 - Data Preparation and Stratification |
| 340 | H2 | Step 1: Parse Raw Simulation Data |
| 383 | H2 | Step 2: Unified Preprocessing Pipeline |
| 655 | H2 | Step 3: Necessary Calculations of Invariants (for Stage Assignment and Input Vector Formulation) |
| 925 | H2 | Step 4: Formulating the Input Vector: Canonical Ordering, Normalization, and Assembly |
| 1061 | H2 | Step 5: Curriculum Stage Assignment |
| 1070 | H1 | Phase 2 - The Definitive CTL-PINN Training Loop |
| 1100 | H2 | Overview: The Two-Phase Optimization Strategy |
| 1145 | H2 | Loss Function Formulation |
| 1174 | H2 | Phase 2a: Adam-driven Exploration |
| 1231 | H2 | Phase 2b: High-Precision L-BFGS Refinement |
| 1256 | H2 | Stage Transition Criteria |
| 1298 | H2 | Consolidated Hyperparameter Schedule |
| 1308 | H2 | Implementation Notes |
| 1337 | H1 | Advanced Considerations and Best Practices |
| 1339 | H2 | Evaluation Metrics and Validation |
| 1413 | H1 | Reproducibility Note (Ignore Now and Come Back Later): |
| 1446 | H1 | Supplementary Figures |
| 1452 | H1 | Source Issues / Notes for Future Reconciliation |
| 1456 | H2 | SI-CTL-001: Input-vector dimensionality inconsistency |

**`pinn_architecture.md`:**

| Line | Level | Heading |
|---|---|---|
| 6 | H1 | A Definitive Implementation Blueprint for a Hybrid SQR-SkipResNet-SIREN PINN with Soft Conservation Regularization for $\mathrm{N}$-Body Dynamics |
| 8 | H1 | 1. Foundational Architectural Principles: A Co-Designed Approach for Chaotic Systems |
| 105 | H1 | 2. The SQR-SkipResNet-SIREN Backbone: A Deep Dive into the Core Architecture |
| 113 | H2 | 2.1 The Sinusoidal Activation (SIREN): The Key to Derivative Fidelity |
| 149 | H2 | 2.2 A Principled Initialization Scheme for SIREN Layers |
| 190 | H2 | 2.3 The Power-Enhanced SkipResNet (SQR-SkipResNet) Formulation |
| 248 | H2 | 2.4 Finalized Architectural Hyperparameters |
| 268 | H1 | 3. The Multi-Component, Physics-Constrained Loss Function |
| 292 | H2 | 3.1 Data Fidelity Term ($\mathcal{L}_{\text{data}}$): Anchoring to Ground Truth |
| 358 | H2 | 3.2 Physics Residual Term ($\mathcal{L}_{\text{physics}}$): Enforcing Newtonian Dynamics |
| 467 | H2 | 3.3 Initial Condition Anchor Loss ($L_{IC}$) |
| 491 | H2 | 3.4 Soft Energy Conservation Regularizer ($L_{E}$): Enforcing a Global Conservation Law |
| 601 | H2 | 3.5 Angular Momentum Conservation Loss ($L_{L}$) |
| 615 | H1 | 4. Advanced Training and Optimization Strategy |
| 621 | H2 | 4.1 Loss Balancing via Warmup Schedule (PHYS-05) |
| 668 | H2 | 4.2 Optional ALM Ablation (P2) |
| 680 | H2 | 4.3 Two-Phase Optimization |
| 697 | H2 | 4.4 Adaptive Gradient Clipping |
| 722 | H1 | 5. Inference and Trajectory Generation |
| 727 | H2 | 5.1 Generating a Trajectory |
| 749 | H2 | 5.2 Output Layer and Kinematic Consistency via Automatic Differentiation |
| 795 | H2 | 5.3 Output Frame and File Format |
| 940 | H2 | References |
| 960 | H1 | 10. Numerical Acceptance Checks |
| 989 | H2 | Source Issues / Notes for Future Reconciliation |

**`sampling_method.md`:**

| Line | Level | Heading |
|---|---|---|
| 1 | H1 | A Unified Pipeline for Generating High-Fidelity Three-Body Initial Conditions |
| 5 | H2 | Overview of the Data Generation Pipeline |
| 20 | H2 | Stage 1: Hierarchical Initial Conditions Generation |
| 83 | H2 | Stage 2: Enhanced Quasi-Random Sampling |
| 86 | H2 | 1. Core Sampling Methodology |
| 168 | H2 | 2. Enhancements to the Sampling Algorithm |
| 200 | H2 | Stage 3: Pre-Screening of Generated ICs for Short-Term Stability |
| 203 | H2 | 3. The Pre-Screening Rationale |
| 224 | H2 | 4. Pre-Screening Criteria |
| 246 | H2 | 5. A Coordinated Strategy for Minimum Distance |
| 264 | H2 | 6. Execution and Final Quality Control |
| 279 | H2 | Source Issues / Notes for Future Reconciliation |

### Constants and contracts concordance — seeded shell (§4)

Complete every seeded row and extend the table with any further shared element you find.
"Shared element" means anything that must be in perfect unison wherever it appears.

| # | Shared element | `ctl_instruction.md` | `pinn_architecture.md` | `sampling_method.md` | Match verdict |
|---|---|---|---|---|---|
| 1 | Network input dimensionality and composition (`[τ, IC₁₃]`) | | | | |
| 2 | τ definition and normalized-time AD contract (`τ = 2u − 1`, `u = t/T`) | | | | |
| 3 | IC₁₃ slot order and mass encoding (raw vs fraction) | | | | |
| 4 | Trajectory horizon T | | | | |
| 5 | Gravitational constant G convention | | | | |
| 6 | Characteristic length scale D (formula and numeric value) | | | | |
| 7 | Input normalization formula and statistics source | | | | |
| 8 | Output head dimensionality and COM projection | | | | |
| 9 | Softening ε (training) and validation ε (dual-epsilon) | | | | |
| 10 | Energy-drift screening gate (form and threshold) | | | | |
| 11 | Hidden architecture (depth × width; SIREN ω₀ first/hidden; skip power; LayerNorm setting) | | | | |
| 12 | Loss-component inventory and weights/schedules | | | | |
| 13 | Energy-regularizer denominator floor | | | | |
| 14 | Batch construction (points per trajectory; replay/lookahead; point-set separation) | | | | |
| 15 | Curriculum stage count and stage-transition thresholds | | | | |
| 16 | Two-phase optimization boundary (Adam → L-BFGS) and its hyperparameters | | | | |
| 17 | Per-variant `dt_out` / tolerance values as stated in specs (cross-check against `DATASET-CONTEXT.md`) | | | | |
| 18 | Output frame and file format | | | | |

### Minimum-decision-list format (§6)

Each §6 entry:

```
MDL-N. <one-sentence question the project owner must answer>
  Option A: <position> — <trade-off>
  Option B: <position> — <trade-off>
  (Option C: ...)
  Source findings: INT-NNN, ...
  Recommendation: <A/B/C> — <one-sentence rationale>
  Confidence: High/Medium/Low
```

Keep it *minimum*: only decisions a builder cannot proceed without, or that gate an S1/S2
finding. Everything else stays in §5 as findings.

## Claims discipline

- Verify against current primary sources where you cite literature or library behavior;
  date-stamp such findings.
- Where the attached materials are silent or ambiguous, record the gap in §7 — never
  invent a resolution. Where you must assume to proceed, state the assumption explicitly
  in the finding.
- Quote verbatim (with file + heading) whenever a finding turns on what a document
  actually says — paraphrase is how audits drift.
- Write for a technically strong reader who is *not* an ML-training expert: plain
  language, defined symbols, no unexplained jargon.
