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
