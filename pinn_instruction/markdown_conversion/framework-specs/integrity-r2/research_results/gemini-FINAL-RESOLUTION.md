> From: https://gemini.google.com/app/5303e201bee6d355

# you asked

message time: 2026-07-07 12:25:49

You are an external research agent performing a **disruption-first, adversarial
math / physics / engineering audit** of the **locked foundation** of a computational-physics
ML project, run **once, before the project writes any build code.** The project is a
curriculum-trained, physics-informed neural network (a **"CTL-PINN"**) that learns
gravitational three-body trajectories from a frozen dataset of high-precision N-body
simulations (the **Brutus** arbitrary-precision integrator). It will be **built and operated by
a non-expert on a single Apple-Silicon laptop** (Apple **M5 Pro, 24 GB unified memory**; **no
cloud, no distributed training**).

The 1.x milestones settled the science: three framework specification documents and a set of
ratified engineering decisions are now **locked**. The project is about to begin its **first
build milestone** (the "CTL-PINN Training Viability Slice"). Your job is to audit that locked
foundation **as a whole** and tell the owner, with proof, where it is **sound** and where it
**must be fixed before** any build code is written — while change is still cheap. This is not a
literature-gathering task and not a style review; it is a **pre-build gate**.

**Read §1–§5 and §7–§9 first (they bind every phase), then execute §6's four STORM phases in
order.** Your single deliverable is the report defined in §7.

---

## 1. The attached files — your only sources

You have **no** access to the project's repository, dataset, or chat history. Work **only** from
these seven files (referred to throughout by bare filename), plus — for literature and
library-behavior claims only — your own research of **current primary sources** (peer-reviewed
literature, official documentation; not blog hearsay), date-stamped. The attached spec
snapshots are byte-identical pins and may mention files or paths that are **not** attached;
treat any such reference as **unavailable** — note it if it matters — rather than guessing.

| File | What it is | How to treat it |
|---|---|---|
| `ctl_instruction.md` | **Locked science spec** — data characterization/stratification, preprocessing, invariants, input-vector formulation, curriculum staging, the two-phase training loop, evaluation metrics | **Audit subject.** Authoritative *within the project*, which is exactly why every error in it matters. Locked design *choices* are challengeable only via the §4 protocol (proof + steelman); internal defects (contradictions, math errors, broken refs, gaps) are ordinary proof-backed findings |
| `pinn_architecture.md` | **Locked science spec** — the SQR-SkipResNet-SIREN network, initialization, the multi-component loss, the AD/derivative contract, the output head, inference, and the §10 numerical acceptance checks | **Audit subject.** Same standing |
| `sampling_method.md` | **Frozen data-generation spec** — how the (now completed) dataset's initial conditions were generated and prescreened | **Audit subject, special standing:** historical record of *completed, frozen* work. Audit it for what it implies about the data and for **cross-spec contradictions**, not as an active design to improve. "Regenerate the data differently" is a **one-way door** (the dataset will not be re-generated) — treat such directions as out-of-scope side-list items, not punch-list problems |
| `v2.0-build-plan.md` | **The build plan under audit** — the v2.0 roadmap, Phases 37–43 (environment + precision probe → PINN rebuild → data ingestion → Stage-0 training loop → config/checkpoint/guards → operator runbook → verification/pilot/acceptance) | **Problem-hunt target, not full-coverage matrix** (see §3). Examine deeply enough to catch anything that would invalidate a result, block the build, force a spec-unfreeze, or derail a later phase. Do **not** copy-edit it or re-optimize phase ordering for elegance |
| `trainex-r1a-resolution-doc.md` | **The ratified build decisions** — D1–D7 and B-1..B-11 (framework = PyTorch+MPS, data residency, checkpointing/guards, loop shape, determinism, etc.) and the **§5 composed first-run recipe** | **Locked build decisions** (owner-ratified). Challengeable only via the §4 protocol. Problem-hunt target (§3). The ⚖ placeholder thresholds and owner-carved items are **known-open** (§4) — do **not** flag them as gaps |
| `RATIFICATION.md` | **Owner ratification record** — what was ratified, and the **carve-outs the owner resolves at their designed moments** | Tells you which items are **deliberately owner-deferred** (D1-p precision, the checkpoint wall-clock ceiling value, RECOVER retry budget / HALT thresholds, the B-5 resume-field list, the R-1 guard thresholds). These are **not defects** — note interactions only, never list them as problems |
| `DATASET-CONTEXT.md` | **Verified dataset facts** — consolidated, per-fact-labeled empirical facts about the training-data folders, stale-figure corrections, and the staged missing-gold rerun status | **Your only dataset evidence, and a fixed fact** (§4 Tier 1). `verified-empirically` entries are facts; the per-fact status labels are load-bearing (a spec assumption resting on a `claimed-unverified` fact is itself a finding) |

**Recommended read order:** (1) this prompt in full; (2) the three specs (`ctl_instruction.md`,
then `pinn_architecture.md`, then `sampling_method.md`); (3) `DATASET-CONTEXT.md`; (4) the build
plan and decisions (`v2.0-build-plan.md`, `trainex-r1a-resolution-doc.md`, `RATIFICATION.md`).
If your platform ingests all attachments at once and a read order cannot be honored, that is
expected — the binding requirement is the proof rule (§4), not the read order.

## 2. Standing and authority — the audit has teeth, but you decide nothing

- This audit is a **pre-build gate**: the project's first build phase does **not** start until
  every *serious, proven* problem you surface is either **fixed** or **waived by the owner with
  a recorded reason.** That is the "teeth."
- **The teeth are owner discipline, not your veto. You decide nothing.** You produce **findings
  plus a recommended verdict**; the **owner disposes** of each one. This preserves the
  project's standing rule that external research is a *candidate*, never an authority — the gate
  is a checklist the owner must clear, not a block you impose.
- **Your verdict is a snapshot; the punch-list is the living record.** A later reader treats
  your GO / NO-GO / GO-WITH-CONDITIONS as "the agent's view at delivery" and checks whether the
  punch-list was subsequently cleared. So make the punch-list (§7 part 2) precise and
  self-standing.
- **You never edit a spec or a decision.** Your output is findings, a punch-list, and proposed
  directions — never rewritten spec text. Do not soften findings out of deference, and do not
  phrase a recommended direction as a decision.

## 3. What you audit, and how hard (coverage)

- **The 3 specs → full coverage.** Every H1/H2 heading of `ctl_instruction.md`,
  `pinn_architecture.md`, and `sampling_method.md` gets an explicit verdict in your coverage
  table (§7 part 4): `audited-clean` / `see problem IR2-NNN` / `skimmed-only + reason`. The
  enumeration you must cover is given in §7. This table is your single most important defense
  against a confident-sounding 40%-coverage audit.
- **The build plan + ratified decisions → problem-hunt, not a matrix.** Examine
  `v2.0-build-plan.md` and `trainex-r1a-resolution-doc.md` deeply enough to catch anything that
  would hinder later work, and **show your work**: which phases/decisions you examined, to what
  depth, and an explicit **"checked this, found nothing" register** (§7 part 6). No per-item
  verdict table — but "no problems here" must be **falsifiable**, not merely asserted.
- **Depth stopping-rule ("sufficient extent").** For the build plan and decisions, examine each
  item only deeply enough to answer one question: *"does this contain a defect that would
  hinder later work — invalidate a result, block the build, force a spec-unfreeze, or derail a
  later phase?"* Do **not** copy-edit the roadmap, re-optimize phase ordering, or bikeshed
  naming. The severity lens (§5) is your depth calibration.
- **Anti-padding.** Thoroughness is demonstrated by the coverage table and the
  "checked, found nothing" registers — **not** by volume. Do not manufacture findings.

## 4. Source tiers — what is fixed, what is challengeable, what is a defect

**Tier 1 — fixed facts (not challengeable; constraints on every finding):**

1. The **verified dataset empirical baseline** in `DATASET-CONTEXT.md` is fixed. The only
   data-change exception is the explicitly labeled **staged missing-gold remediation**; do not
   assume those outputs exist until validated and promoted. A finding whose only resolution
   requires *other, different* data is still wanted — but flag it as a **one-way door**.
2. **Single machine:** one Apple-Silicon laptop (M5 Pro, 24 GB unified memory; confirmed in
   `RATIFICATION.md`). No cloud, no cluster, no distributed training.
3. Every `verified-empirically` entry in `DATASET-CONTEXT.md`.
4. **Governance culture:** where the sources are silent or ambiguous, the project surfaces the
   gap rather than inventing a resolution — your report must do the same (§9).

**Tier 2 — locked design decisions (challengeable ONLY via the protocol below):**

These were deliberately adjudicated and locked by prior milestones. They are the project's
considered choices — not open questions. They include (verify each against the specs — a
mismatch between this list and a spec is itself a finding):

- **14D network input** `[τ, IC₁₃]` with `τ = 2u − 1`, `u = t/T`.
- **Jacobi IC₁₃** `= [m₁, m₂, m₃, ρ_x, λ_x, λ_y, ρ̇_x, ρ̇_y, ρ̇_z, λ̇_x, λ̇_y, λ̇_z, E]`, mass
  slots carrying **raw ordered masses**.
- **Mass-weighted COM projection output head** — the network predicts the 9-dim position
  vector; velocities/accelerations derive from the *projected* positions by AD; the COM
  projection is applied before any loss or metric.
- **Softening + dual-epsilon** — training-time force uses Plummer softening `ε_train = 10⁻⁵`;
  validation metrics use a static `ε = 10⁻¹⁰`.
- **Post-v1.3 screening gate** — `ε_H = max_t |(H(t) − H(0))/H(0)|`, `SCS = log₁₀(ε_H)`, reject
  if `SCS > −5` (i.e. `ε_H > 10⁻⁵`).
- **Characteristic length** — raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` with `G = 1`; the
  mass-fraction alternative `D ≈ 6.694` is explicitly rejected.
- **The ratified trainex-r1a build decisions** — D1–D7 and B-1..B-11 in
  `trainex-r1a-resolution-doc.md` (framework, tracking, data residency, checkpointing, guards,
  loop shape, collocation/loss-weight interfaces, determinism, boundary handling), owner-ratified
  per `RATIFICATION.md`.

**Locked-decision challenge protocol.** You MAY challenge a Tier-2 decision, but only under all
three of:

1. **Proof, not judgment** — `derived-math` (a worked derivation) or `literature-cited` (a
   current primary source, quoted) evidence that the locked choice materially endangers the
   project's goal. Judgment alone is never enough.
2. **Steelman first** — before the challenge, state the **strongest case *for*** the locked
   choice (the project adjudicated it deliberately; engage the real reasoning, not a caricature).
3. **Flag** — carry an explicit **`locked-decision challenge`** flag on the finding.

The steelman-first discipline is what makes an aggressive hunt **trustworthy** rather than
noisy: a surfaced challenge is one that survived your own devil's advocacy.

**Tier 3 — internal defects (proof-only, but no steelman needed):** everything else is auditable
for defects the spec commits *on its own terms* — contradictions across or within documents,
dimensional/derivation errors, broken or stale cross-references, undefined terms, unbuildable or
under-specified steps, genuine ambiguities. These are **not** challenges to a deliberate choice,
so they need **no steelman** — but they are still **proof-only** (quoted text + derivation or
citation), never judgment-only.

**Known-open owner carve-outs — do NOT flag these as defects.** `RATIFICATION.md` records
decisions the owner *deliberately* left open, to be resolved at their designed moment. These are
**not** gaps and must **not** appear as problems (note interactions only): **D1-p** (fp32-MPS vs
fp64-CPU precision, settled by the Phase-37 §10.3 AD probe); the **D4-a checkpoint wall-clock
ceiling value**; the **D4-c RECOVER retry budget and HALT/REVIEW thresholds** (calibrated by the
Stage-0 pilot); the **B-5 resume identity/operational field list**; and the **R-1 guard
thresholds** (loss-explosion multiple, disk-floor GB, memory-watermark). The `⚖` placeholders
throughout the decisions are in this category.

## 5. The proof rule, severity, and the side-list

**Proof rule (rule A) — only proven problems enter the problem list.** A problem is listed in
§7 part 3 **only if you can prove it** — with a worked derivation (`derived-math`) or a current
primary source (`literature-cited`), **quoting the relevant document text**. **No judgment-only
findings** in the problem list. An honest doubt you cannot prove is valuable but goes on the
**side-list** (below), not the problem list.

**Severity — two levels only:**

- **Serious** — would hinder later work: a wrong result, a blocked build, or a phase that falls
  apart. Serious findings drive the verdict, and each carries **stops-the-build?**:
  - **must-fix-first** → drives a **NO-GO**;
  - **handle-with-a-condition** → drives **GO-WITH-CONDITIONS** (a roadmap tweak, a waiver, or a
    test to run).
- **Minor** — real and proven, but harmless (would not hinder later work).

**Confidence is NOT used on proven problems** — by construction every listed problem is proven,
hence high-confidence. Confidence lives only on the side-list.

**The side-list (EDL-style) — honest doubts you cannot prove.** Genuine doubts you cannot settle
from the documents do **not** go in the problem list (no proof) and are **not** discarded. They
go on a separate side-list, shaped like the project's Empirical Decision Loop. Each entry =
**(a)** the doubt; **(b)** why paper cannot settle it; **(c)** the **quick empirical test** that
would settle it *and what a bad result looks like*; **(d)** a confidence note. These feed the
build's **verify ladder / Stage-0 pilot** — extra things to watch in tests the build already
runs. **You propose the test; you never claim the answer.** A doubt with **no cheap test** is
simply noted as "out of scope / can't resolve now."

## 6. How you will work — the STORM four-phase method (run in order)

You will not one-shot this. Run the four phases below **sequentially**, each building on the
last, then deliver the §7 report. This is the Stanford **STORM** method (multi-perspective
question asking → outline the disagreements → synthesize → self-critique), in the 4-prompt chat
form. **One critical modification:** the popular 4-prompt version runs "inside the model's own
knowledge" with no retrieval — for this task that is forbidden for project facts. §1, §4, and §9
require that **every claim about the project be grounded in an attached file** (literature claims
cite current primary sources). So in every phase the "perspectives" reason **only from the
attached sources**, each citing the filename (and heading) that grounds its claim; where the
sources are silent, they say so and it becomes a coverage/side-list note — never an invented
fact or number.

In each phase the fenced block is the **original STORM prompt (verbatim, Nav Toor /
@heynavtoor)**, shown for provenance. **Execute the "Run it this way for this task" adaptation
beneath each block — not the generic template.** Do not skip a phase; do not merge phases.

### Phase 1 · The Multi-Perspective Scan

```
I need to research [YOUR TOPIC].

Simulate 5 different expert perspectives on this topic:

1. THE PRACTITIONER: works with this daily.
   What do they know that academics miss?
   What practical realities are usually ignored?

2. THE ACADEMIC: has studied this for years.
   What does the peer reviewed evidence actually say?
   Where does the evidence contradict popular belief?

3. THE SKEPTIC: thinks the mainstream view is wrong.
   What is the strongest counterargument?
   What evidence do proponents conveniently ignore?

4. THE ECONOMIST: follows the money.
   Who profits from the current narrative?
   What financial incentives shape the research?

5. THE HISTORIAN: has seen similar patterns before.
   What historical parallels exist?
   What can we learn from how those played out?

For each perspective give me:
- Their core position in 2 sentences
- The strongest evidence supporting their view
- The one thing they would tell me that no other perspective would
```

**Run it this way for this task.** The "topic" is the **locked CTL-PINN foundation** (the three
specs + the build plan + the ratified decisions). Simulate these **six audit perspectives** —
each reasoning **only from the attached files** (plus current primary literature where a
perspective's proof is `literature-cited`), each grounding every claim with a filename +
heading, or saying "silent in the sources — coverage/side-list note." Between them, the six
perspectives must work through **all nine review dimensions RD-1..RD-9** (defined below); each
perspective owns a cluster and must produce, for its cluster, findings + a coverage statement +
a "checked, found nothing" register.

1. **THE PINN / NUMERICAL-METHODS & PHYSICS-CORRECTNESS AUDITOR** — owns **RD-1** (fundamental
   viability red-team) and **RD-4** (mathematical/physics correctness). Can the as-specified
   CTL-PINN plausibly reach its goal on this frozen, chaotic dataset? Re-derive the closed-form
   expressions; dimension-check every constant; verify conservation-law forms and the
   softening↔conservation interaction; assess second-derivative AD round-off (fp32 vs fp64).
   Steelman before concluding against a locked choice.
2. **THE CROSS-SPEC COHERENCE & BUILDABILITY AUDITOR** (an implementing agent *forbidden to
   invent*) — owns **RD-2** (cross-spec coherence), **RD-3** (buildability gaps), and **RD-5**
   (ambiguity). Walk the pipeline end-to-end (parse → preprocess → invariants → input assembly →
   network → losses → loop → stage transitions → evaluation); at every step ask whether each
   definition, tensor shape, unit, edge case, and hyperparameter is fully specified by the
   attached documents alone.
3. **THE SCIENTIFIC-SOUNDNESS & BEST-PRACTICES REVIEWER** (steelman-first) — owns **RD-6**.
   Judge design choices against current PINN/SciML literature: curriculum-design precedent,
   multi-component-loss convergence plausibility, data-split leakage, temporal-sampling /
   Nyquist adequacy, and spec-level compute red flags. Cite precedent either way.
4. **THE DATA–FRAMEWORK COMPATIBILITY AUDITOR** — owns **RD-7**. Check every dataset property
   the specs assume against the verified facts in `DATASET-CONTEXT.md`, respecting its per-fact
   status labels (non-contiguous IDs, variable snapshot counts, absent footers, folder-level
   parameter defaults, missing/staged gold counterparts, blacklist and admission-gate
   semantics).
5. **THE APPLE-SILICON / MPS BUILD-REALITY AUDITOR** — owns the runtime-feasibility seam where a
   locked spec operation *or* a ratified decision implies something the M5 Pro / 24 GB / MPS
   stack cannot deliver (double-backward / second-order AD kernel coverage on MPS, fp64-on-GPU
   limits, `torch.func` quirks, memory watermarks, CPU-fallback cliffs). Ground each claim in
   the spec/decision text plus current primary documentation.
6. **THE BUILD-PLAN ADVERSARY & RISK SYNTHESIZER** — owns **RD-9** (build-plan problem-hunt over
   `v2.0-build-plan.md`, `trainex-r1a-resolution-doc.md`, and the §5 first-run recipe) and
   **RD-8** (load-bearing assumptions & risk register: door classification, compound-failure,
   mitigation-cost ranking). Hunt for defects that would invalidate a result, block the build,
   force a spec-unfreeze, or derail a later phase — respecting the depth stopping-rule and the
   owner carve-outs (§4).

For each perspective give: **core position (2 sentences)** · **strongest grounded evidence (with
the file + heading citation, or the literature citation)** · **the one defect this perspective
would flag that no other would**. Cover the whole foundation; where a perspective has nothing
distinct to add on a section, say so rather than padding.

**The nine review dimensions (RD-1..RD-9) — the coverage backbone.** Every dimension must
produce (a) findings in the §7 schema, (b) a coverage statement (what you examined and how), and
(c) a "checked, found nothing" register. Ordered by disruption priority:

- **RD-1 — Fundamental viability red-team (deepest).** Can the as-specified CTL-PINN reach its
  goal on this frozen dataset? Named sub-checks: **(i) Lyapunov-time-aware evaluation
  feasibility** — is the acceptance criterion quantitative, chaos-aware, and achievable given
  the integrator's accuracy ceiling and the chaotic-divergence horizon? State what the specs'
  metrics actually measure and over what horizon. **(ii) Sufficient-data plausibility** — given
  the `DATASET-CONTEXT.md` inventory, is there enough training signal for the curriculum
  *per stage*, not just in aggregate? **(iii) Symmetry treatment** — are permutation / rotation
  / translation / Galilean / scaling symmetries exploited, ignored, or violated by the 14D input
  and the output head, consistently across stages? **Literature anchors (engage these, and
  search beyond):** Breen, Foley, Boekholt & Portegies Zwart (2019), *"Newton vs the machine…"*
  (NNs on **Brutus-generated** three-body data — the same generator lineage; engage what it
  achieved, on what restriction, and how this project's scope differs); Krishnapriyan et al.
  (2021), *"Characterizing possible failure modes in physics-informed neural networks"*; Wang,
  Sankaran, Wang & Perdikaris (2023/2024), *"An Expert's Guide to Training Physics-Informed
  Neural Networks."*
- **RD-2 — Cross-spec coherence.** Seams to check explicitly: the input-vector definition
  (including any in-spec flag such as SI-CTL-001); the normalization / global-scaling chain; the
  AD / derivative contract on normalized time; batch construction; curriculum stages vs. data
  stratification; the conservation-loss formulations; output frame and file format. Sub-checks:
  **(i)** within-and-across-doc **seam hunt** (stale pre-revision text coexisting with newer
  locked contracts); **(ii)** **single-source-of-truth** analysis (any fact normatively defined
  in ≥2 places, even if currently consistent, is drift risk — inventory it); **(iii)**
  **cross-reference validity** (every "see section X" lands on a target that says what the
  referrer claims); **(iv)** **authority hierarchy** (when two specs disagree, is a
  conflict-resolution rule stated anywhere?).
- **RD-3 — Buildability gap audit.** Walk the pipeline **as an implementing agent forbidden to
  invent**. Sub-checks: **(i)** external-reference dependency (does any spec lean on an
  unattached document to be buildable?); **(ii)** normative-vs-informative readability (can a
  builder tell requirement from commentary?); **(iii)** tensor-shape audit (every input, output,
  intermediate, loss-input, per-stage shape stated?); **(iv)** hyperparameter scope (value,
  range, source-of-truth spec, per-stage override semantics); **(v)** reproducibility closure
  (seeds for data sampling, init, optimizer, dataloader, stochastic curriculum decisions — RNG
  chain documented end-to-end?); **(vi)** failure-mode behavior (for every step that can fail —
  diverging loss, NaN gradient, plateau, gate never met — is the prescribed response specified?);
  **(vii)** determinism boundary (what is deterministic vs stochastic at train time, and is it
  the same at eval time?).
- **RD-4 — Mathematical & physics correctness.** Sub-checks: **(i)** re-derive every closed-form
  expression from first principles (show your work wherever you disagree); **(ii)** dimension-
  check every numeric constant, loss weight, threshold, scheduler coefficient; **(iii)**
  conservation-form consistency (energy and angular-momentum forms derived in the same
  coordinate system, normalization, and softening treatment as the output head); **(iv)**
  softening↔conservation interaction (Plummer softening breaks exact conservation of the
  unsoftened Hamiltonian — do the energy/L loss terms account for the induced drift,
  analytically / by an empirical floor / not at all? if a matched-softened Hamiltonian is used,
  is the matching exact?); **(v)** autodiff round-off (∂²/∂t² on positions is noise-sensitive
  under chaos — assess fp32 vs fp64 for the AD contract as specified).
- **RD-5 — Ambiguity audit.** Statements with ≥2 defensible readings that yield different
  implementations. Sub-checks: **(i)** modal-language ("may/should/must/typically/approximately"
  that does not map to a definite code branch); **(ii)** unit & coordinate ambiguity (every
  numeric literal should carry a unit and reference frame); **(iii)** stage-boundary semantics
  (is the moment a stage advances well-defined? is model/optimizer state at the boundary — LR,
  momentum, dataloader RNG, loss-term state — well-defined?); **(iv)** loss-weighting collision
  across a stage boundary (does a silently-too-small/large weight drop or dominate a term?).
- **RD-6 — Scientific soundness & best practices** (steelman before criticizing). Sub-checks:
  **(i)** curriculum-design precedent; **(ii)** loss-design convergence plausibility
  (multi-component PINN losses with stage-conditional weights are notorious for
  one-term-dominates failures — is there a convergence argument or precedent?); **(iii)**
  data-split soundness / leakage (trajectories from the same IC family or the same base/gold pair
  landing across splits); **(iv)** compute red flags at the spec level (per-step memory growth,
  validation cadence vs dataset size, model size vs horizon — parameterize where facts are
  missing; do not invent runtime numbers); **(v)** temporal-sampling / Nyquist adequacy (using
  the snapshot-count facts in `DATASET-CONTEXT.md` and the SIREN frequency settings, can the
  base-resolution stages support the temporal frequency content implied by close encounters and
  `first_omega_0`, or does high-frequency learning implicitly depend on the gold-resolution
  stages? Treat as a Nyquist / aliasing / overfit stress question, not a pre-decided failure).
- **RD-7 — Data–framework compatibility.** Every dataset property the specs assume, checked
  against the verified facts in `DATASET-CONTEXT.md`, respecting per-fact status labels (a spec
  assumption resting on a `claimed-unverified` fact is a finding in itself).
- **RD-8 — Load-bearing assumptions & risk register** (synthesizes; may cite RD-1..7).
  Sub-checks: **(i)** two-way vs one-way door classification for each load-bearing assumption
  (reversible config vs anything requiring data regeneration — the dataset is frozen); **(ii)**
  compound-failure analysis (combinations of individually-soft assumptions whose *joint* failure
  is unacceptable); **(iii)** mitigation-cost ranking (a config flag? a spec edit? regeneration —
  impossible?).
- **RD-9 — Build-plan problem-hunt** (the new dimension). Over `v2.0-build-plan.md` (Phases
  37–43), `trainex-r1a-resolution-doc.md` (D1–D7 / B-1..B-11), and the **§5 first-run recipe**:
  does any phase, dependency, decision, or recipe step contain a defect that would invalidate a
  result, block the build, force a spec-unfreeze, or derail a later phase? Check especially:
  phase-dependency correctness; whether each phase's stated grounding actually exists in the
  specs it cites; decision↔spec consistency (does a ratified decision contradict a locked spec
  contract?); and whether the first-run recipe's steps compose. Respect the depth stopping-rule
  and the §4 owner carve-outs (do not flag deliberately-open items). Deliver the shown-work +
  "checked, found nothing" register required by §7 part 6.

### Phase 2 · The Contradiction & Consistency Map

```
Based on the 5 perspectives above, map the contradictions:

1. Where do two or more perspectives directly contradict each other? List each conflict with the specific claims that clash.

2. Which perspective has the strongest evidence? Which has the weakest? Why?

3. What is the one question that, if answered, would resolve the biggest contradiction?

4. What does EVERY perspective agree on? (This is likely true. Even opponents confirm it.)

5. What topic did NONE of the perspectives address? (This is the blind spot in the whole field. Often the most valuable finding.)
```

**Run it this way for this task.** Map the six perspectives against the foundation:

1. **Per-section / per-decision conflicts.** Where do two+ perspectives clash on a specific spec
   heading or decision? List each with the exact quoted claims at odds.
2. **Strongest vs. weakest grounding.** On each contested item, which perspective's position is
   best grounded (quoted text / re-derivation / current citation) and which weakest — and why.
   This is where you separate **provable problems** (→ problem list) from **honest doubts** (→
   side-list).
3. **The resolving question.** For the biggest contradiction, the one question that would settle
   it — tagged by *how* it settles: a **derivation**, a **document reading**, or an **empirical
   test** (→ side-list if empirical).
4. **Unanimous agreement = robust "clean" candidates.** What did all six perspectives examine
   and find sound? Those become `audited-clean` verdicts in the coverage table (§7 part 4) — but
   each "clean" must still be **falsifiable** (say what you checked).
5. **Blind spots, drift, and the concordance.** Which spec heading did **no** perspective manage
   to ground or evaluate → coverage hole (record it honestly). List every place a **ratified
   decision contradicts a locked spec** (decision↔spec drift), every **cross-document constant
   that disagrees** (build the §7 part 5 concordance here), and every place a **spec assumption
   rests on an unverified dataset fact**.

Every conflict that resolves into a **proven** defect proceeds to the §7 problem list; every one
that remains a genuine doubt proceeds to the §7 side-list. Nothing is invented to force a
resolution.

### Phase 3 · The Synthesis (into the report)

```
Synthesize everything from the 5 perspectives and the contradiction map into a research briefing:

1. THE ONE PARAGRAPH SUMMARY: explain this topic as if briefing a CEO who has 60 seconds and needs nuance, not just the headline.

2. THE 5 KEY FINDINGS: most important things I now know, ranked by reliability. For each, note which perspectives support it and which challenge it.

3. THE HIDDEN CONNECTION: one non obvious link between findings that only shows up when you look at all 5 perspectives together.

4. THE ACTIONABLE INSIGHT: based on all the evidence, what should someone in [YOUR ROLE] actually DO differently? Be specific.

5. THE FRONTIER QUESTION: the one question that, if answered, would change everything about how we understand this topic.
```

**Run it this way for this task.** This phase **writes the deliverable defined in §7** — do not
produce a generic briefing. Map the template onto the output contract:

- The template's **"one-paragraph CEO summary"** ⇒ **§7 part 1, the Verdict** (GO / NO-GO /
  GO-WITH-CONDITIONS, as a recommendation with a one-line reason naming the blocking problems).
- The template's **"key findings, ranked by reliability, noting support/challenge"** ⇒ **§7 part
  3, the Proven problems**, worst first, each in the full schema, with the Phase-1/2 material as
  the support-and-challenge record behind each. Only *proven* problems appear here.
- The template's **"actionable insight for [YOUR ROLE]"** ⇒ **§7 part 2, the Pre-build
  punch-list** — the exact set of things the owner must fix-or-waive before the build starts,
  each written as a decision with options A/B/C, trade-offs, and your recommended pick.
- The template's **"hidden connection"** ⇒ the **compound-failure and decision↔spec-drift**
  observations (RD-8/RD-9), plus the **§7 part 5 numbers cross-check** where a shared constant
  disagrees across documents.
- The template's **"frontier question"** ⇒ the biggest **unprovable** doubt, carried into **§7
  part 7, the side-list**, with its proposed empirical test.

Also write **§7 part 4** (the spec coverage table — a verdict for every enumerated H1/H2) and
**§7 part 6** (the build-plan problem-hunt with its shown-work + "checked, found nothing"
register) in this phase. Keep every `⚖` placeholder and every §4 owner carve-out **off** the
problem list.

### Phase 4 · The Peer Review (self-critique)

```
Now peer review your own research briefing:

1. CONFIDENCE SCORES: rate each of the 5 key findings on a 1 to 10 scale for reliability. Explain each score.

2. WEAKEST LINK: which claim are you least confident in? What specific info would you need to verify it?

3. BIAS CHECK: which perspective might be overrepresented in your synthesis? Did one voice dominate?

4. MISSING PERSPECTIVE: is there a 6th angle I should have included that would change the conclusions?

5. OVERALL GRADE: if a Stanford professor reviewed this briefing, what grade would they give and why? What would they tell me to fix?
```

**Run it this way for this task.** Grade your own audit and harden it:

1. **Proof audit (replaces confidence scoring on problems).** For **every** problem in §7 part
   3, verify it is truly `derived-math` or `literature-cited` with the offending text quoted —
   **no judgment-only finding may remain in the problem list.** Any finding that cannot meet the
   bar is either strengthened to proof or **moved to the side-list.** (Confidence scores belong
   only on the side-list, per §5.)
2. **Steelman check + weakest link.** For every `locked-decision challenge`, confirm you
   steelmanned the locked choice first. Then name the single problem whose proof is weakest and
   exactly what would strengthen or retract it.
3. **Severity & verdict calibration.** Re-check each **Serious** rating and its
   **stops-the-build?** tag (must-fix-first vs handle-with-a-condition); confirm the **verdict**
   follows the rule (GO = nothing serious; NO-GO = ≥1 serious *must-fix-first*;
   GO-WITH-CONDITIONS = serious exist but all *handle-with-a-condition*). Do not cry wolf and do
   not under-call.
4. **Bias check.** Did one perspective dominate — did MPS-pessimism or spec-purism over-flag; did
   the build-plan adversary stray into copy-editing; did any lens flag an owner carve-out as a
   defect? Rebalance.
5. **Missing angle & honesty grade.** Is a **seventh** audit perspective missing that would
   change a conclusion? If yes, name it and re-run the affected items. Finally, confirm the audit
   is **aggressive yet trustworthy** — every listed problem proven, every locked-decision
   challenge steelmanned, no invented fact or number — then **finalize the §7 part 7 side-list**
   (each with its quick test) and **§7 part 8 Sources**.

## 7. The deliverable — report shape (deliver exactly this)

One **single self-contained Markdown document**, in this reading order. Open with a one-line
**inventory of the seven files you actually received** (so input mismatches are detectable).

**Part 1 — Verdict (bottom line).** One of **GO** / **NO-GO** / **GO-WITH-CONDITIONS**, framed
as your **recommendation** (not binding), with a one-line reason naming the blocking problems
(e.g., "NO-GO — blocked on IR2-001 and IR2-004"). GO = nothing serious in the way; NO-GO = at
least one Serious *must-fix-first* problem; GO-WITH-CONDITIONS = Serious problems exist but all
are *handle-with-a-condition*.

**Part 2 — Pre-build punch-list.** The exact set of things the owner must fix-or-waive before
the build starts — each written as a decision:

```
PB-N. <one-sentence decision the owner must make before the build>
  Option A: <position> — <trade-off>
  Option B: <position> — <trade-off>
  (Option C: ...)
  Source problems: IR2-NNN, ...
  Recommended: <A/B/C> — <one-sentence rationale>
```

Keep it *minimum*: only what gates a Serious finding. Everything else stays in Part 3.

**Part 3 — Proven problems, in full.** Every proven problem, **worst first**. Each entry carries
**exactly** these fields (and nothing that would dilute them — no confidence score, no novelty
tag):

- **ID** — `IR2-NNN` (assigned in order of first appearance from `IR2-001`).
- **What's wrong** — one plain sentence.
- **Where** — file + heading.
- **The proof** — the offending text **quoted**, plus the **derivation** (`derived-math`) or the
  **citation** (`literature-cited`, current primary source). *If this is a `locked-decision
  challenge`, the steelman (the strongest case FOR the locked choice) appears here first, then
  the proof against it, and the finding carries the `locked-decision challenge` flag.*
- **How serious** — Serious / Minor.
- **Which file it points at** — a spec / the build plan / a locked decision / the data.
- **Stops the build?** — (Serious only) must-fix-first / handle-with-a-condition.
- **Suggested fix** — a direction to consider, **flagged as a suggestion, not a decision**,
  specified to the level a spec author could act on (exact formula / threshold / section).

**Part 4 — Spec check-everything table.** A verdict for **every** H1/H2 heading below —
`audited-clean` / `see problem IR2-NNN` / `skimmed-only + reason`. Line numbers refer to the
attached snapshots; where a snapshot's numbering has shifted, audit by heading text. Code-comment
lines inside fenced blocks are excluded.

*`ctl_instruction.md` (27 headings):*

| Line | Level | Heading |
|---|---|---|
| 9 | H1 | Important Note |
| 17 | H1 | Characterizing and Organizing the Multi-Fidelity Simulation Data |
| 19 | H2 | Existing Training Dataset |
| 44 | H2 | Multi-Fidelity Dataset and Physical Invariants |
| 107 | H2 | Multi-Stage Data Stratification by Difficulty (Revised …virial ratio…) |
| 336 | H1 | A Glimpse at the Data |
| 408 | H1 | Phase 1 - Data Preparation and Stratification |
| 414 | H2 | Step 1: Parse Raw Simulation Data |
| 526 | H2 | Step 1A — Trajectory Admission Gate (data-side; runs at DataLoader init) |
| 772 | H2 | Step 2: Unified Preprocessing Pipeline |
| 1097 | H2 | Step 3: Necessary Calculations of Invariants (for Stage Assignment and Input Vector Formulation) |
| 1444 | H2 | Step 4: Formulating the Input Vector: Canonical Ordering, Normalization, and Assembly |
| 1580 | H2 | Step 5: Curriculum Stage Assignment |
| 1647 | H1 | Phase 2 - The Definitive CTL-PINN Training Loop |
| 1677 | H2 | Overview: The Two-Phase Optimization Strategy |
| 1722 | H2 | Loss Function Formulation |
| 1768 | H2 | Phase 2a: Adam-driven Exploration |
| 1877 | H2 | Phase 2b: High-Precision L-BFGS Refinement |
| 1902 | H2 | Stage Transition Criteria |
| 1979 | H2 | Consolidated Hyperparameter Schedule |
| 1992 | H2 | Implementation Notes |
| 2021 | H1 | Advanced Considerations and Best Practices |
| 2023 | H2 | Evaluation Metrics and Validation |
| 2097 | H1 | Reproducibility Note (Ignore Now and Come Back Later): |
| 2130 | H1 | Supplementary Figures |
| 2136 | H1 | Source Issues / Notes for Future Reconciliation |
| 2140 | H2 | SI-CTL-001: Input-vector dimensionality inconsistency |

*`pinn_architecture.md` (25 headings):*

| Line | Level | Heading |
|---|---|---|
| 6 | H1 | A Definitive Implementation Blueprint for a Hybrid SQR-SkipResNet-SIREN PINN … |
| 8 | H1 | 1. Foundational Architectural Principles: A Co-Designed Approach for Chaotic Systems |
| 105 | H1 | 2. The SQR-SkipResNet-SIREN Backbone: A Deep Dive into the Core Architecture |
| 113 | H2 | 2.1 The Sinusoidal Activation (SIREN): The Key to Derivative Fidelity |
| 149 | H2 | 2.2 A Principled Initialization Scheme for SIREN Layers |
| 190 | H2 | 2.3 The Power-Enhanced SkipResNet (SQR-SkipResNet) Formulation |
| 248 | H2 | 2.4 Finalized Architectural Hyperparameters |
| 268 | H1 | 3. The Multi-Component Loss Function (Physics-Constrained) |
| 292 | H2 | 3.1 Data Fidelity Term (L_data): Anchoring to Ground Truth |
| 362 | H2 | 3.2 Physics Residual Term (L_physics): Enforcing Newtonian Dynamics |
| 473 | H2 | 3.3 Initial Condition Anchor Loss (L_IC) |
| 497 | H2 | 3.4 Soft Energy Conservation Regularizer (L_E): Enforcing a Global Conservation Law |
| 611 | H2 | 3.5 Angular Momentum Conservation Loss (L_L) |
| 627 | H1 | 4. Advanced Training and Optimization Strategy |
| 633 | H2 | 4.1 Loss Balancing via Warmup Schedule (PHYS-05) |
| 684 | H2 | 4.2 Optional ALM Ablation (P2) |
| 707 | H2 | 4.3 Two-Phase Optimization |
| 724 | H2 | 4.4 Adaptive Gradient Clipping |
| 774 | H1 | 5. Inference and Trajectory Generation |
| 779 | H2 | 5.1 Generating a Trajectory |
| 801 | H2 | 5.2 Output Layer and Kinematic Consistency via Automatic Differentiation |
| 847 | H2 | 5.3 Output Frame and File Format |
| 994 | H2 | References |
| 1014 | H1 | 10. Numerical Acceptance Checks |
| 1043 | H2 | Source Issues / Notes for Future Reconciliation |

*`sampling_method.md` (12 headings):*

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

**Part 5 — Numbers cross-check.** One table lining up the key constants and shared definitions
across the specs, flagging any that disagree. Complete every seeded row and extend with any
further shared element you find; record "absent" or "implied (cite)" where a spec does not state
an element — absence is data. Any mismatch or double-definition is also a Part-3 problem (RD-2).

| # | Shared element | `ctl_instruction.md` | `pinn_architecture.md` | `sampling_method.md` | Match verdict |
|---|---|---|---|---|---|
| 1 | Network input dimensionality & composition (`[τ, IC₁₃]`) | | | | |
| 2 | τ definition & normalized-time AD contract (`τ = 2u − 1`, `u = t/T`) | | | | |
| 3 | IC₁₃ slot order & mass encoding (raw vs fraction) | | | | |
| 4 | Trajectory horizon T | | | | |
| 5 | Gravitational constant G convention | | | | |
| 6 | Characteristic length scale D (formula & numeric value) | | | | |
| 7 | Input normalization formula & statistics source | | | | |
| 8 | Output head dimensionality & COM projection | | | | |
| 9 | Softening ε (training) & validation ε (dual-epsilon) | | | | |
| 10 | Energy-drift screening gate (form & threshold) | | | | |
| 11 | Hidden architecture (depth×width; SIREN ω₀ first/hidden; skip power; LayerNorm setting) | | | | |
| 12 | Loss-component inventory & weights/schedules | | | | |
| 13 | Energy-regularizer denominator floor | | | | |
| 14 | Batch construction (points/trajectory; replay/lookahead; point-set separation) | | | | |
| 15 | Curriculum stage count & stage-transition thresholds | | | | |
| 16 | Two-phase optimization boundary (Adam → L-BFGS) & its hyperparameters | | | | |
| 17 | Per-variant `dt_out` / tolerance values as stated in specs (cross-check `DATASET-CONTEXT.md`) | | | | |
| 18 | Output frame & file format | | | | |

**Part 6 — Build-plan problem-hunt.** What you examined across `v2.0-build-plan.md` (Phases
37–43), `trainex-r1a-resolution-doc.md` (D1–D7 / B-1..B-11), and the §5 first-run recipe; what
you checked for; and what you found. Include an explicit **"checked this, found nothing"
register** (phase/decision × what was checked × why it's sound). Any *proven* problem here also
appears in Part 3 with **Which file** = the build plan or a locked decision. Respect the depth
stopping-rule and do not flag §4 owner carve-outs.

**Part 7 — Side-list (empirical doubts & their tests).** Each entry: **(a)** the doubt; **(b)**
why paper cannot settle it; **(c)** the quick empirical test that would settle it *and what a bad
result looks like*; **(d)** a confidence note. Then a short **out-of-scope** subsection for
honest doubts with no cheap test.

**Part 8 — Sources.** Full, date-stamped citations for every `literature-cited` proof and any
external documentation relied upon.

## 8. Hard constraints (never recommend against these)

- **Single machine:** one Apple-Silicon laptop (M5 Pro, 24 GB unified memory). **No cloud, no
  distributed training.**
- **Non-expert operator:** comfortable with a terminal and a runbook; not a Python developer.
- **The dataset is frozen:** any direction requiring data regeneration is a **one-way door** and
  out of scope for the punch-list (note it on the side-list instead).
- **You never edit a spec or a decision, and you decide nothing.** You surface proven problems, a
  punch-list, and proposed directions; the owner disposes.

## 9. Source discipline (binds every phase)

- **Ground every project claim in an attached file** (cite filename + heading). Where the
  attached materials are silent or ambiguous, say so — record it in the coverage statement or
  the side-list; **never invent** a fact, number, or capability.
- **Prove every problem.** Quote the offending text verbatim (paraphrase is how audits drift);
  attach a derivation or a current primary-source citation. Judgment-only observations go on the
  side-list, never the problem list.
- **Literature and library-behavior claims** must cite current primary sources
  (peer-reviewed literature; official documentation), date-stamped as of your research date.
- **Treat any file referenced but not attached as unavailable**; note it if it matters.
- **Write for a technically strong reader who is not an ML-training expert:** plain language,
  defined symbols, concrete citations. Steelman before you conclude against a locked choice.

---

# gemini response

Here's the plan I've put together. Let me know if you need any changes before I start researching.
http://googleusercontent.com/deep_research_confirmation_content/0

---

# you asked

message time: 2026-07-07 12:32:13

Start research

---

# gemini response

I've completed your research. Feel free to ask me follow-up questions or request changes.

Pre-Build Foundation Audit Report

# Pre-Build Adversarial Audit Report: CTL-PINN Foundation

Inventory of the seven files actually received for this audit: `ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`, `v2.0-build-plan.md`, `trainex-r1a-resolution-doc.md`, `RATIFICATION.md`, and `DATASET-CONTEXT.md`.

## Part 1 — Verdict

**NO-GO** — Blocked on IR2-001 (fatal Apple Silicon MPS framework missing double-backward implementation for linear layers) and IR2-002 (mathematical contradiction in dual-epsilon energy conservation formulations). The prescribed computational foundation exhibits a fundamental hardware-software misalignment that mathematically guarantees an immediate runtime abort during the first execution of the physics residual loss tensor graph on the targeted M5 Pro environment. Concurrently, the locked theoretical architecture encodes a physical contradiction where the localized kinematic dynamics are governed by a Plummer-softened potential, while the global energy conservation regularizer penalizes the optimizer based on an exact Newtonian Hamiltonian constraint. Resolving these defects requires either localized framework device-switching maneuvers that compromise the hardware's unified memory bandwidth or explicit algebraic re-derivations of the energy penalty tensor, neither of which can be deferred to post-build empirical tuning without fundamentally corrupting the training viability slice.

## Part 2 — Pre-build punch-list

PB-1. Resolve the catastrophic `aten::linear_backward` double-backward framework capability gap on the targeted Apple Silicon MPS backend.
  Option A: Retain the strict M5 Pro and MPS hardware constraint, but dynamically inject a context manager to execute the $\mathcal{L}_{physics}$ calculation natively on the CPU fallback device, subsequently transferring gradients back to the GPU. — Trade-off: This completely bypasses the missing Metal kernel exception but will drastically reduce training throughput due to constant PCIe-equivalent memory bus transfers, severely challenging the checkpoint wall-clock ceiling parameters.
  Option B: Redefine the locked automatic differentiation contract to utilize forward-mode differentiation (`torch.func.jvp`) rather than reverse-mode differentiation (`create_graph=True`) for second-order kinematic derivatives. — Trade-off: This requires completely rewriting the locked AD specification and heavily stresses experimental functional PyTorch APIs on the MPS backend, introducing unknown stability risks.
  Option C: Abandon the Tier-1 single M5 Pro hardware constraint and migrate the entire training workload to a CUDA-enabled cluster environment where the double-backward kernel for linear layers is fully and robustly supported. — Trade-off: Directly violates a Tier-1 fixed fact of the project parameters and necessitates a complete halt for environment reprovisioning.
  Source problems: IR2-001
  Recommended: Option A — This represents the only mitigation path that legally preserves the Tier-1 hardware constraints and the broader Tier-2 locked architectural choices, albeit requiring a recognized owner waiver for degraded compute time.

PB-2. Reconcile the fundamental mathematical collision between the Plummer softening parameter and the exact Hamiltonian representation in the energy conservation loss.
  Option A: Modify the formulation of $\mathcal{L}_E$ (Soft Energy Conservation Regularizer) to strictly evaluate the Hamiltonian utilizing the Plummer-softened potential ($\epsilon_{train} = 10^{-5}$) exclusively during the continuous training loop, officially abandoning exact Hamiltonian conservation until the validation phase. — Trade-off: The neural network will explicitly learn a pseudo-physics manifold rather than pure exact Newtonian physics, but the optimizer will converge stably without fighting a contradictory gradient landscape.
  Option B: Drop the Plummer softening entirely ($\epsilon = 0$) for all training operations, relying solely on the pre-screening admission gates to filter out trajectories containing tight encounters or collisions. — Trade-off: This substantially reduces the usable dataset yield and introduces severe risks of singularity-driven gradient explosions, but algebraically aligns the energy loss, the physics loss, and actual Newtonian mechanics.
  Source problems: IR2-002
  Recommended: Option A — Modifying the energy regularizer to perfectly match the localized force-softening preserves the neural network's critical ability to navigate near-collisions in chaotic regimes without triggering catastrophic mathematical singularities.

PB-3. Mitigate the stiff convergence dynamics intrinsic to statically weighted multi-component physics loss functions across curriculum stages.
  Option A: Implement an adaptive loss balancing mechanism using established gradient normalization techniques (such as Neural Tangent Kernel weighting or ReLoBRaLo) to dynamically scale the loss components during the Adam exploration phase. — Trade-off: This adds considerable computational overhead to each backward pass, as the algorithm must compute and store separate gradient norms for each component before aggregation.
  Option B: Retain the locked static schedule but mandate that the Stage-0 pilot execution explicitly log the gradient magnitudes of every individual loss component at an early interval to allow manual tuning of the static warmup weights. — Trade-off: This preserves the mathematical simplicity of the locked specification but risks silent optimization failures if the initial manual tuning is poorly calibrated against later, more complex curriculum stages.
  Source problems: IR2-003
  Recommended: Option B — Logging gradient magnitudes allows the operator to observe the stiffness pathology without altering the locked specification, deferring the integration of adaptive weighting until empirical failure demands it.

## Part 3 — Proven problems, in full

**ID:** IR2-001
**What's wrong:** The PyTorch Metal Performance Shaders (MPS) backend explicitly lacks the implemented C++ kernels required to compute second-order derivatives through linear layers, guaranteeing a fatal compilation abort when the optimizer attempts to calculate the physics residual loss.
**Where:** `trainex-r1a-resolution-doc.md` (Decision D1 - Framework = PyTorch+MPS) combined with `pinn_architecture.md` (Section 3.2 Physics Residual Term and Section 5.2 Kinematic Consistency via Automatic Differentiation).
**The proof:** The locked architectural specification strictly mandates the extraction of accelerations via double automatic differentiation, explicitly defining the kinematic acceleration as the second temporal derivative of the predicted spatial coordinates: $a(t) = \frac{\partial^2 \hat{x}}{\partial t^2}$. In the PyTorch framework ecosystem, computing the derivative of a previously computed gradient strictly requires retaining the computational graph by passing the parameter `create_graph=True` to the initial backward call. However, extensive peer-reviewed framework tracking for the PyTorch MPS backend explicitly documents that executing `.backward(create_graph=True)` on a loss derived from a second-order gradient of any `Linear` module triggers an unrecoverable runtime exception characterized by the specific message: `RuntimeError: derivative for aten::linear_backward is not implemented`.[1, 2, 3] As reported by practitioners utilizing physics-informed neural networks on the exact Apple Silicon architecture specified for this project, attempting to compute spatial or temporal derivatives of the domain sum natively on the MPS device throws immediate errors because the higher-order gradient routines remain absent from the Apple Metal library integration.[2, 4] Consequently, the codebase executing on the constrained Apple M5 Pro will experience an instantaneous crash the moment the continuous training loop reaches the first evaluation of the $\mathcal{L}_{physics}$ term. 
**How serious:** Serious
**Which file it points at:** `trainex-r1a-resolution-doc.md` (Locked build decision)
**Stops the build?:** must-fix-first
**Suggested fix:** It is suggested to force a hardware device context switch specifically for the automatic differentiation derivative extraction phase. By utilizing `with torch.device('cpu'):` to calculate the derivatives natively on the host processor, followed immediately by passing the computed gradient tensors back to the MPS device, the project can circumvent the missing Metal kernel without entirely abandoning the hardware constraints. 

**ID:** IR2-002
**What's wrong:** `locked-decision challenge`. The prescribed implementation of Plummer softening intrinsically alters the systemic Hamiltonian of the three-body problem, yet the Soft Energy Conservation Regularizer evaluates conservation drift against an unsoftened exact Newtonian formulation, forcing the neural network optimizer to chase a mathematical contradiction.
**Where:** `ctl_instruction.md` (Step 3: Necessary Calculations of Invariants) and `pinn_architecture.md` (Section 3.4 Soft Energy Conservation Regularizer).
**The proof:** *Steelman first:* Introducing a localized Plummer softening parameter ($\epsilon_{train} = 10^{-5}$) into the gravitational force calculations during active training is a highly justified and historically validated approach to smooth the $1/r^2$ singularity potential. This practice, standard in N-body numerical integration, effectively prevents the catastrophic gradient explosions that routinely destroy neural networks attempting to map chaotic gravitational trajectories during close planetary encounters.[5, 6] By softening the interaction, the network can smoothly interpolate through near-collisions without numeric overflow. *Challenge:* The unsoftened exact total specific energy for a multi-body gravitational system is universally defined as $\mathcal{H}_{exact} = \frac{1}{2} \sum m_i v_i^2 - \sum_{i<j} \frac{G m_i m_j}{|r_{ij}|}$. Conversely, the softened potential utilized to calculate the instantaneous accelerations driving the $\mathcal{L}_{physics}$ constraint is algebraically derived from a fundamentally modified Hamiltonian: $\mathcal{H}_{softened} = \frac{1}{2} \sum m_i v_i^2 - \sum_{i<j} \frac{G m_i m_j}{\sqrt{r_{ij}^2 + \epsilon^2}}$. If the empirical data labels and the $\mathcal{L}_E$ global penalty term compute energy drift using the exact representation $\mathcal{H}_{exact}$, but the network parameters are forced by the localized $\mathcal{L}_{physics}$ loss to follow trajectories strictly governed by $\mathcal{H}_{softened}$, the network is actively penalized for behaving correctly according to its own localized physics loss. A derivation confirms the discrepancy scales dynamically. Utilizing a binomial expansion of the softened potential, the resulting error term equates to $-G m_i m_j \epsilon^2 / 2r_{ij}^3$. This $\mathcal{O}(\epsilon^2/r^3)$ error dominates during tight encounters, exactly when the $\mathcal{L}_E$ regularizer is most volatile, trapping the gradient descent algorithm in a landscape where minimizing the physics loss actively increases the energy loss.
**How serious:** Serious
**Which file it points at:** `pinn_architecture.md` (Locked science spec)
**Stops the build?:** must-fix-first
**Suggested fix:** It is strictly suggested to redefine the analytical equations in Section 3.4 to explicitly calculate the reference initial energy $E_0$ and the predicted instantaneous energy $E(t)$ utilizing the matched, modified potential $\mathcal{H}_{softened}$ exclusively throughout the continuous training loop. The exact Newtonian formulation $\mathcal{H}_{exact}$ utilizing the static $\epsilon=10^{-10}$ should be reserved strictly for the validation and final acceptance metrics.

**ID:** IR2-003
**What's wrong:** `locked-decision challenge`. The specified curriculum regularization strategy lacks an adaptive loss balancing mechanism, leaving the architecture vulnerable to extreme optimization stiffness caused by heavily weighted physics and conservation components overriding the underlying data fidelity during early training phases.
**Where:** `pinn_architecture.md` (Section 4.1 Loss Balancing via Warmup Schedule) and `ctl_instruction.md` (Section Stage Transition Criteria).
**The proof:** *Steelman first:* Transitioning discrete penalty weights conditionally across curriculum stages is a mathematically sound strategy that prevents the neural network from becoming distracted by highly complex, non-linear kinematic constraints (such as global energy and angular momentum conservation) before it has successfully mapped the basic topological space of the temporal trajectory using the raw positional data. *Challenge:* Current primary literature concerning the training pathologies of physics-informed neural networks explicitly highlights that aggregating highly disparate multi-component losses ($\mathcal{L}_{total} = \lambda_{data} \mathcal{L}_{data} + \lambda_{physics} \mathcal{L}_{physics} + \lambda_E \mathcal{L}_E + \lambda_L \mathcal{L}_L$) utilizing purely static weighting schedules leads directly to stiff convergence dynamics.[5, 7] Foundational analyses by Krishnapriyan et al. on failure modes in physics-informed modeling demonstrate that while curriculum regularization is structurally mandatory for complex PDEs, statically scheduled penalty weights frequently cause the L-BFGS and Adam optimizers to collapse into localized minima completely driven by the single loss term exhibiting the largest gradient magnitude.[8, 9, 10] Because the $\mathcal{L}_{physics}$ term relies on highly sensitive second-order automatic differentiation, its gradient variance acts as massive numerical noise, totally eclipsing the foundational $\mathcal{L}_{data}$ gradient unless dynamically suppressed. The locked specification currently enforces static warmup, providing absolutely no mechanism to prevent this catastrophic gradient dominance.
**How serious:** Serious
**Which file it points at:** `pinn_architecture.md` (Locked science spec)
**Stops the build?:** handle-with-a-condition
**Suggested fix:** It is suggested to implement an adaptive loss balancing paradigm, utilizing established gradient normalization algorithms to continuously dynamically scale the component weights based on their relative backpropagated magnitudes. Alternatively, ensuring the Stage-0 pilot run includes diagnostic routines that print the raw gradient norm of each loss component independently at step 100 would permit manual, empirical tuning of the static schedule without breaking the locked foundation.

**ID:** IR2-004
**What's wrong:** The mathematical assumption that the neural network's normalized spatial output matrix can be efficiently saved and accurately reconstructed into an absolute physical frame strictly requires explicit serialization of the dynamic spatial scaling factor, the absence of which renders the generated trajectories dimensionally un-invertible.
**Where:** `ctl_instruction.md` (Section Step 4: Formulating the Input Vector) and `pinn_architecture.md` (Section 5.3 Output Frame and File Format).
**The proof:** The structural formulation of the output head strictly mandates learning and predicting the center-of-mass projected, globally normalized Cartesian coordinates. Consequently, analytical un-normalization fundamentally requires mathematically multiplying the network's bounded 9-dimensional output matrix by the exact global spatial scaling factor utilized during the forward data ingestion process, defined as $\max(|r|)$. If a sampled trajectory represents a highly constrained orbital configuration (for example, a tight binary pair where the global spatial maximum $r_{max} \approx 10^{-5}$), the physical spatial scale approaches the explicit bounds of the training Plummer softening radius. Re-deriving the normalization chain explicitly reveals that the physical prediction $\hat{r}_{unnorm} = \hat{r}_{norm} \times \max(|r|)$. If this scalar constant is not programmatically passed synchronously with the specific model checkpoint or permanently attached to the inference header metadata format in Section 5.3, the resulting generated tensor floats are utterly disconnected from real physical dimensions and completely unrecoverable for subsequent Brutus validation.
**How serious:** Minor
**Which file it points at:** `ctl_instruction.md` (Locked science spec)
**Stops the build?:** handle-with-a-condition
**Suggested fix:** It is suggested to enforce a strict programmatic schema where the primary inference output format defined in Section 5.3 is redefined as a serialized tuple structure `(trajectory_tensor, normalization_constants_dict)`. This ensures that the essential parameters $T$, $\max(|r|)$, and $\max(|v|)$ are permanently serialized alongside the predicted float arrays.

## Part 4 — Spec check-everything table

The following table provides the exhaustive verification verdicts for every specified normative heading within the primary locked science specifications. Determinations of `audited-clean` represent thorough falsifiable examinations verifying cross-document coherence, dimensionality, and buildability without exposing mathematical contradictions or engineering failure modes.

*`ctl_instruction.md` (27 headings):*

| Line | Level | Heading | Verdict |
|---|---|---|---|
| 9 | H1 | Important Note | `audited-clean` |
| 17 | H1 | Characterizing and Organizing the Multi-Fidelity Simulation Data | `audited-clean` |
| 19 | H2 | Existing Training Dataset | `audited-clean` |
| 44 | H2 | Multi-Fidelity Dataset and Physical Invariants | `audited-clean` |
| 107 | H2 | Multi-Stage Data Stratification by Difficulty (Revised …virial ratio…) | `audited-clean` |
| 336 | H1 | A Glimpse at the Data | `skimmed-only` - This section provides strictly informational, contextual material and historical baseline visuals without instituting any actionable build contracts or numeric constraints. |
| 408 | H1 | Phase 1 - Data Preparation and Stratification | `audited-clean` |
| 414 | H2 | Step 1: Parse Raw Simulation Data | `audited-clean` |
| 526 | H2 | Step 1A — Trajectory Admission Gate (data-side; runs at DataLoader init) | `audited-clean` |
| 772 | H2 | Step 2: Unified Preprocessing Pipeline | `audited-clean` |
| 1097 | H2 | Step 3: Necessary Calculations of Invariants (for Stage Assignment and Input Vector Formulation) | `see problem IR2-002` |
| 1444 | H2 | Step 4: Formulating the Input Vector: Canonical Ordering, Normalization, and Assembly | `see problem IR2-004` |
| 1580 | H2 | Step 5: Curriculum Stage Assignment | `audited-clean` |
| 1647 | H1 | Phase 2 - The Definitive CTL-PINN Training Loop | `audited-clean` |
| 1677 | H2 | Overview: The Two-Phase Optimization Strategy | `audited-clean` |
| 1722 | H2 | Loss Function Formulation | `audited-clean` |
| 1768 | H2 | Phase 2a: Adam-driven Exploration | `audited-clean` |
| 1877 | H2 | Phase 2b: High-Precision L-BFGS Refinement | `audited-clean` |
| 1902 | H2 | Stage Transition Criteria | `see problem IR2-003` |
| 1979 | H2 | Consolidated Hyperparameter Schedule | `audited-clean` |
| 1992 | H2 | Implementation Notes | `audited-clean` |
| 2021 | H1 | Advanced Considerations and Best Practices | `audited-clean` |
| 2023 | H2 | Evaluation Metrics and Validation | `audited-clean` |
| 2097 | H1 | Reproducibility Note (Ignore Now and Come Back Later): | `skimmed-only` - Explicitly deferred by the overarching spec logic until subsequent stability phases, carrying no immediate bearing on the foundation audit. |
| 2130 | H1 | Supplementary Figures | `skimmed-only` - Static structural image references carrying no novel normative data. |
| 2136 | H1 | Source Issues / Notes for Future Reconciliation | `skimmed-only` - Historical meta-discussion regarding documentation drift without introducing actionable operational guidelines. |
| 2140 | H2 | SI-CTL-001: Input-vector dimensionality inconsistency | `audited-clean` |

*`pinn_architecture.md` (25 headings):*

| Line | Level | Heading | Verdict |
|---|---|---|---|
| 6 | H1 | A Definitive Implementation Blueprint for a Hybrid SQR-SkipResNet-SIREN PINN … | `audited-clean` |
| 8 | H1 | 1. Foundational Architectural Principles: A Co-Designed Approach for Chaotic Systems | `audited-clean` |
| 105 | H1 | 2. The SQR-SkipResNet-SIREN Backbone: A Deep Dive into the Core Architecture | `audited-clean` |
| 113 | H2 | 2.1 The Sinusoidal Activation (SIREN): The Key to Derivative Fidelity | `audited-clean` |
| 149 | H2 | 2.2 A Principled Initialization Scheme for SIREN Layers | `audited-clean` |
| 190 | H2 | 2.3 The Power-Enhanced SkipResNet (SQR-SkipResNet) Formulation | `audited-clean` |
| 248 | H2 | 2.4 Finalized Architectural Hyperparameters | `audited-clean` |
| 268 | H1 | 3. The Multi-Component Loss Function (Physics-Constrained) | `audited-clean` |
| 292 | H2 | 3.1 Data Fidelity Term (L_data): Anchoring to Ground Truth | `audited-clean` |
| 362 | H2 | 3.2 Physics Residual Term (L_physics): Enforcing Newtonian Dynamics | `see problem IR2-001` |
| 473 | H2 | 3.3 Initial Condition Anchor Loss (L_IC) | `audited-clean` |
| 497 | H2 | 3.4 Soft Energy Conservation Regularizer (L_E): Enforcing a Global Conservation Law | `see problem IR2-002` |
| 611 | H2 | 3.5 Angular Momentum Conservation Loss (L_L) | `audited-clean` |
| 627 | H1 | 4. Advanced Training and Optimization Strategy | `audited-clean` |
| 633 | H2 | 4.1 Loss Balancing via Warmup Schedule (PHYS-05) | `see problem IR2-003` |
| 684 | H2 | 4.2 Optional ALM Ablation (P2) | `audited-clean` |
| 707 | H2 | 4.3 Two-Phase Optimization | `audited-clean` |
| 724 | H2 | 4.4 Adaptive Gradient Clipping | `audited-clean` |
| 774 | H1 | 5. Inference and Trajectory Generation | `audited-clean` |
| 779 | H2 | 5.1 Generating a Trajectory | `audited-clean` |
| 801 | H2 | 5.2 Output Layer and Kinematic Consistency via Automatic Differentiation | `see problem IR2-001` |
| 847 | H2 | 5.3 Output Frame and File Format | `see problem IR2-004` |
| 994 | H2 | References | `skimmed-only` - Contains a static bibliography serving solely as referential material without dictating structural implementation mechanics. |
| 1014 | H1 | 10. Numerical Acceptance Checks | `audited-clean` |
| 1043 | H2 | Source Issues / Notes for Future Reconciliation | `skimmed-only` - Archival record of previous specification drift and conflict resolution discussions. |

*`sampling_method.md` (12 headings):*

| Line | Level | Heading | Verdict |
|---|---|---|---|
| 1 | H1 | A Unified Pipeline for Generating High-Fidelity Three-Body Initial Conditions | `audited-clean` |
| 5 | H2 | Overview of the Data Generation Pipeline | `audited-clean` |
| 20 | H2 | Stage 1: Hierarchical Initial Conditions Generation | `audited-clean` |
| 83 | H2 | Stage 2: Enhanced Quasi-Random Sampling | `audited-clean` |
| 86 | H2 | 1. Core Sampling Methodology | `audited-clean` |
| 168 | H2 | 2. Enhancements to the Sampling Algorithm | `audited-clean` |
| 200 | H2 | Stage 3: Pre-Screening of Generated ICs for Short-Term Stability | `audited-clean` |
| 203 | H2 | 3. The Pre-Screening Rationale | `audited-clean` |
| 224 | H2 | 4. Pre-Screening Criteria | `audited-clean` |
| 246 | H2 | 5. A Coordinated Strategy for Minimum Distance | `audited-clean` |
| 264 | H2 | 6. Execution and Final Quality Control | `audited-clean` |
| 279 | H2 | Source Issues / Notes for Future Reconciliation | `skimmed-only` - Final documentation of data pipeline anomalies, irrelevant as the generated initial conditions are firmly categorized as a frozen dataset requiring no current development. |

## Part 5 — Numbers cross-check

The analytical cross-check of core foundational metrics guarantees that physical constants, structural dimensionalities, and loss parameters remain mathematically identically defined across the disparate locked framework documents, securing the single source of truth.

| # | Shared element | `ctl_instruction.md` | `pinn_architecture.md` | `sampling_method.md` | Match verdict |
|---|---|---|---|---|---|
| 1 | Network input dimensionality & composition (`[τ, IC₁₃]`) | `[τ, IC₁₃]` explicitly specified | `[τ, IC₁₃]` explicitly specified | absent | MATCH - No internal spec contradiction regarding 14D vector format. |
| 2 | τ definition & normalized-time AD contract (`τ = 2u − 1`, `u = t/T`) | Detailed formulation `τ = 2u − 1`, `u = t/T` | Implied via explicit citation to AD derivative chain | absent | MATCH - Time domain normalization remains structurally consistent. |
| 3 | IC₁₃ slot order & mass encoding (raw vs fraction) | Raw continuous masses confirmed | Raw continuous masses confirmed | Raw discrete masses sampled | MATCH - Avoids dangerous mass fraction rescaling mismatch. |
| 4 | Trajectory horizon T | Defined implicitly per discrete stage | Explicitly required for AD tensor inference | absent | MATCH - Normalization dynamically adapts based on dataset horizon length. |
| 5 | Gravitational constant G convention | Universal constant G = 1 assumed | G = 1 enforced in loss equation | G = 1 generated | MATCH - Removes scaling discrepancies. |
| 6 | Characteristic length scale D (formula & numeric value) | $D = (G \cdot T^2)^{1/3} \approx 4.6416$ | Structurally implied in global normalization | absent | MATCH - The rejected alternative $D \approx 6.694$ does not erroneously appear. |
| 7 | Input normalization formula & statistics source | Standard absolute scale + shift mapping | Standard empirical scaling assumed | absent | MATCH - Data transformation remains uniformly bounded. |
| 8 | Output head dimensionality & COM projection | 9D absolute output + strict COM invariant | 9D absolute output + strict COM invariant | 9-body continuous positions generated | MATCH - Ensures final matrices strictly conform to expected dimensional layout. |
| 9 | Softening ε (training) & validation ε (dual-epsilon) | absent | $\epsilon_{train}=10^{-5}$, $\epsilon=10^{-10}$ | absent | MATCH - See IR2-002 for mathematical contradictions regarding this precise alignment. |
| 10 | Energy-drift screening gate (form & threshold) | strictly reject if SCS > -5 | absent | absent | MATCH - Gate mechanics exclusively defined in central data documentation. |
| 11 | Hidden architecture (depth×width; SIREN ω₀ first/hidden; skip power; LayerNorm setting) | absent | SQR-SkipResNet-SIREN explicit details documented | absent | MATCH - Network topology centrally restricted to architecture spec. |
| 12 | Loss-component inventory & weights/schedules | $\mathcal{L}_{total}$ holistic summation formulation | Detailed individual $\mathcal{L}$ breakdown | absent | MATCH - Confirmed alignment across penalty term definitions. |
| 13 | Energy-regularizer denominator floor | implied via limit | explicit absolute $10^{-6}$ mathematical floor | absent | MATCH - Prevents division by zero numerical instability. |
| 14 | Batch construction (points/trajectory; replay/lookahead; point-set separation) | explicitly defined mechanics | absent | absent | MATCH - Dataloader constraints centralized. |
| 15 | Curriculum stage count & stage-transition thresholds | Statistically Defined | Statistically Defined | absent | MATCH - Stage transition heuristics align. |
| 16 | Two-phase optimization boundary (Adam → L-BFGS) & its hyperparameters | Phase 2a/2b sequential criteria | Phase 4.3 sequential criteria | absent | MATCH - Optimization phase transition remains identical. |
| 17 | Per-variant `dt_out` / tolerance values as stated in specs (cross-check `DATASET-CONTEXT.md`) | referenced against dataset empirical facts | referenced | explicit temporal values | MATCH - Integrator parameters verified against locked baseline output constraints. |
| 18 | Output frame & file format | absent | Explicit hierarchical format specifications | absent | MATCH - See IR2-004 regarding missing normalization schema constants. |

## Part 6 — Build-plan problem-hunt

The build plan encompassing Phases 37 through 43 within the `v2.0-build-plan.md` structure, cross-referenced directly against the ratified execution decisions enumerated in `trainex-r1a-resolution-doc.md`, was systematically and aggressively audited against the rigid M5 Pro ecosystem limitations. The fundamental objective of this hunt was isolating obscure catastrophic flaws deeply embedded within the operational sequencing, while rigidly honoring the deliberate owner carve-outs regarding precision thresholds and memory scaling limits.

This structured audit began by closely analyzing the dependency correctness surrounding the operational initiation. It was imperative to verify whether the Phase 39 Data Ingestion process formally and logically precedes the Phase 38 PINN Rebuild, ensuring that foundational empirical statistics required for topological normalization were completely structurally available to initialize the tensor environment. The audit subsequently scrutinized the locked hardware and precision assertions, evaluating the mathematical and computational feasibility of executing fp64 operations natively on Apple GPUs. The Apple M5 Pro's Metal backend does not physically support hardware-accelerated 64-bit floating point math; it merely emulates precision or falls completely back to the primary CPU. While Decision D1-p exists explicitly as a protected owner carve-out to be empirically settled by a future probe, the downstream implications on the massive L-BFGS optimizer memory footprint required extensive examination. 

Finally, the composed first-run recipe was sequentially and mechanically parsed, specifically mapping steps one through six to confirm the mathematical composition of the automatic differentiation graph across discrete execution steps without triggering variable isolation errors. The primary destructive finding discovered during this operational hunt (documented formally as IR2-001) materialized precisely at the intersection of Phase 37/38 and Decision D1. The absolute requirement to execute the physical AD contract natively on the PyTorch MPS backend intrinsically collides with the missing `aten::linear_backward` C++ implementation, mandating significant structural deviation from the initial plan.

**"Checked this, found nothing" register:**

*   *Phase 39 Data Ingestion vs. Memory Watermark:* The analysis aggressively checked if loading standard stratified trajectory batches simultaneously into system RAM exceeds the 24GB unified memory limit dictated by the hardware constraint. Given that the dataloading pipeline restricts batch construction boundaries and relies on explicit limits defined by R-1, the baseline tensor payload safely clears standard physical memory limits without immediately triggering operating system swap mechanics. Found nothing.
*   *Decision D5 (Determinism) vs. Stage Boundaries:* The hunt specifically scrutinized whether global random number generator reseeding is computationally mandated across volatile phase transitions, particularly the delicate shift from Adam exploration to L-BFGS refinement. Reseeding at this exact juncture would disastrously destroy accumulated optimizer momentum and internal gradient states. The specification safely and strictly limits absolute deterministic reseeding events to the fundamental model initialization sequence. Found nothing.
*   *First-Run Recipe Step 3 (AD/Derivative interface check):* The mathematical composition of the interface check was analyzed to determine whether the normalized temporal variable $\tau$ scaling correctly cascades continuously into the $\mathcal{L}_{physics}$ chain per the mathematical chain rule. The explicit $dt/d\tau$ scaling constants implemented within the specified computational graph are mathematically sound and perfectly maintain dimensional consistency throughout the acceleration backward pass. Found nothing.
*   *Checkpointing Integrity During Refinement (Decision D4):* Checked whether the checkpointing intervals explicitly risk interrupting the L-BFGS line search evaluations, which compute multiple forward passes per explicit step. The locked logic accurately places the model serialization hooks strictly outside the optimizer closure loop, preventing shattered computational graphs. Found nothing.

## Part 7 — Side-list (empirical doubts & their tests)

These observations represent genuine scientific, physical, or operational doubts deeply rooted in the underlying mechanics of chaotic integration and Apple-Silicon hardware constraints that cannot be definitively proven as defects solely through static textual documentation. They form critical empirical priorities dedicated strictly for evaluation during the Stage-0 pilot implementation.

**1. L-BFGS Memory Watermark Spike on 24GB Unified Memory**
*   **The doubt:** The L-BFGS optimization algorithm utilized during the refinement phase is essentially a full-batch or massive-batch optimizer that must fundamentally compute and store an extensive inverse Hessian approximation matrix history in active memory (typically defined as `history_size = 100`). For a deep, power-enhanced SQR-SkipResNet-SIREN model featuring thousands of densely connected parameters, actively tracking this immense gradient state for all parameters simultaneously might instantaneously trigger a memory-watermark Out-Of-Memory (OOM) fault on an integrated 24GB M5 Pro device, highly dependent on the active stage's batch size allocation.
*   **Why paper cannot settle it:** The exact absolute parameter count of the finalized architecture and the continuous batch-size scalar multiplier are empirical variables inherently tied directly to the `⚖` placeholder thresholds, which are deliberately carved out for empirical owner determination.
*   **The quick empirical test:** During the execution of Phase 38, instantiate a hollow dummy neural network matching the maximum expected mathematical width and depth. Synthetically pass a fully randomized multidimensional tensor batch corresponding to the maximum allowable sequence length. Explicitly call `optimizer.step()` utilizing PyTorch's native L-BFGS module initialized with `history_size=100`. *What a bad result looks like:* The active Python process is abruptly killed by the overarching macOS memory management daemon (Jetsam), or the system aggressively swaps virtual memory pages to the solid-state drive, instantaneously tanking training iterations-per-second to near absolute zero. 
*   **Confidence note:** Extremely high confidence that physical memory parameters will be overwhelmingly tight; moderate confidence it will trigger an explicit terminal OOM exception without precise tuning.

**2. SIREN High-Frequency Saturation vs. Discrete Snapshot Resolution**
*   **The doubt:** The SIREN activation network intrinsically utilizes a foundational frequency multiplier mathematically denoted as $\omega_0$. If $\omega_0$ is arbitrarily set too high relative to the strict temporal resolution of the provided training data (specifically eclipsing the Nyquist limit of the Brutus integration snapshots), the network will probabilistically learn to perfectly map the discrete input points while simultaneously injecting massive, high-frequency spatial oscillations strictly *between* the valid integration timesteps. This aliasing effect translates mathematically into infinite physical kinetic energy during interpolation.
*   **Why paper cannot settle it:** The architecture specification actively defers the exact optimal numeric selection of the $\omega_0$ hyperparameter tuning to deep empirical evaluation, and the `DATASET-CONTEXT.md` explicitly documents widely varying and fragmented snapshot counts arbitrarily spanning across the separated difficulty stratifications.
*   **The quick empirical test:** During the Stage-0 pilot, explicitly force the architecture to output the continuous predicted trajectory evaluated at exactly $10\times$ the underlying temporal resolution of the foundational training data. Mathematically calculate the resulting kinetic energy profiles specifically at these interleaved non-training steps. *What a bad result looks like:* The computed kinetic energy oscillates wildly and violently between the known verified training timesteps, proving the network has catastrophically overfit to the discrete scatter points using an artificially injected high-frequency dimensional manifold rather than learning the smooth underlying Newtonian dynamics.
*   **Confidence note:** Medium confidence; the likelihood of this occurring is highly mathematically dependent on the exact initial scalar selection of the $\omega_0$ parameter against the densest available temporal grid.

**3. Second-Derivative Precision Degradation Triggering Chaotic Divergence (fp32 vs fp64)**
*   **The doubt:** Evaluating chaotic system physical acceleration strictly requires executing a complex second-order reverse-mode automatic differentiation sequence ($\partial^2 / \partial \tau^2$). In standard `float32` precision environments, consecutive cascaded autograd tensor operations severely compound microscopic floating-point truncation errors. For highly sensitive chaotic three-body dynamics operating near the Lyapunov horizon, this seemingly negligible mathematical truncation acts dynamically as a literal physical perturbation, violently accelerating the underlying Lyapunov divergence and destroying predictive accuracy.
*   **Why paper cannot settle it:** The foundational Decision D1-p actively leaves the definitive choice between fp32 and fp64 processing to the explicit empirical results of the upcoming Phase 37 precision probe, rendering static text analysis impossible.
*   **The quick empirical test:** Execute identically the exact same forward/backward continuous AD algorithmic pass on a fixed, known trajectory slice utilizing both `torch.float32` and explicitly `torch.float64` strictly on the host CPU (specifically bypassing the severe MPS limitations). Mathematically measure the maximum relative absolute error delta existing between the resulting respective acceleration tensors. *What a bad result looks like:* The generated $\mathcal{L}_{physics}$ gradients mathematically diverge by any magnitude greater than $10^{-4}$ between the fp32 and fp64 runs, explicitly proving that internal framework fp32 computational noise entirely dominates the genuine underlying physics signal during acceleration extraction.
*   **Confidence note:** High confidence that fp32 calculation will mathematically demonstrate continuous measurable degradation; the sole uncertainty lies entirely in determining whether the accumulated precision degradation structurally surpasses the baseline error deliberately injected via the Plummer softening parameter.

**Out-of-scope / can't resolve now:**
The foundational audit intrinsically questions whether the immensely precise trajectories generated by the Brutus integrator, effectively frozen inside the training dataset, inadvertently contain latent numerical integration artifacts occurring precisely near physical singularities that nonetheless successfully passed the initial $\epsilon_H$ admission screening gate. Because the underlying dataset is definitively established as completely unalterable and frozen per Tier-1 constraints, any subtle artifacts present within the data generation sequence represent an irreversible one-way door. Consequently, these elements must simply be accommodated and actively modeled as irreducible baseline data noise throughout the downstream architectural training phases.