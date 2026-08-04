# Phase 49: Conformance Gate - Context

**Gathered:** 2026-08-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 49 builds the **minimum enforcement subset** that makes an invalid Stage-0
run structurally unable to spend the single authorized held-out evaluation. It
owns exactly GATE-01, GATE-02, GATE-03, and INST-03:

- **GATE-01** — preflight asserts the **full** PHYS-05 per-stage `λ^max` table
  (not merely the `≤1` cap) at run start and at every stage boundary.
- **GATE-02** — a preflight **placeholder census**: every spec-required quantity
  the loss consumes resolves to a real pipeline value, or is explicitly
  owner-waived for that run. This is the check that would have caught the `S_H`
  gap.
- **GATE-03** — **runtime invariants** that fail loud and fail early: invariant A
  (no causal weight exactly zero) and invariant B (the causal front advances
  within the owner-ratified `N` steps).
- **INST-03** — the **known-divergence register**, maintained as a first-class
  artifact, with every open divergence surfaced in the run record so a run
  carries its own caveats.

Plus the roadmap's fifth success criterion: the **SCOPE-32 coordination
decision** is recorded (charter deliverables consumed if they landed, minimum
subset implemented otherwise — no duplicated regime).

**What this phase deliberately does NOT do.** No training run and no zero-step
emitter (Phase 50 owns the first real-corpus invocation — the same owner ruling
of 2026-07-30, Option B, that governed Phase 47). No held-out evaluation
(SCOPE-28; Phase 51). No framework-spec edit (SCOPE-30). No recipe tuning or
threshold fitting against observed results (SCOPE-29). No re-audit of the
component math (the conformance audit's verified-clean inventory is
load-bearing). No general verification regime — the normative-statement index,
full CI integration, waiver *policy*, and thresholds X/M belong to the concurrent
charter workstream (SCOPE-32). No re-opening of any Phase 46/47/48 decision.

</domain>

<decisions>
## Implementation Decisions

Twenty-eight decisions, D-01..D-28. Every decision below is grounded in a cited
owner ruling, a locked spec line, a verified audit finding, or a short
first-principles derivation stated inline. One item — the numeric value of `N`
for invariant B — is **deliberately left undecided** and preserved as a blocking
owner checkpoint (D-19..D-21).

### GATE-01 — the PHYS-05 table assertion

- **D-01 [GROUNDED — GAP-45-03 owner ruling option A, 2026-07-24]:** The locked
  object is the **per-stage `λ^max(k)` table itself**, not the schedule form plus
  the `≤1` cap. Preflight asserts, for the stage being entered:

  | quantity | k=0 | k=1 | k=2 | k=3 | k=4 | k=5 | k=6 | status |
  |---|---|---|---|---|---|---|---|---|
  | `λ_phys^max(k)` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **locked** |
  | `λ_E^max(k)` | 0 | 0 | 1e-2 | 1e-1 | 1 | 1 | 1 | **locked** |
  | `λ_L^max(k)` | 0 | 0 | 1e-2 | 1e-1 | 1 | 1 | 1 | **locked** |
  | `λ_data` | 1 (all k, not per-stage) | | | | | | | **locked** (§3.1 unweighted data term) |
  | `λ_IC` | 1 (all k, not per-stage) | | | | | | | **advisory** — see D-03 |
  | `I_warm(k)` | `min(2000, floor(0.1·N_Adam,k))` | | | | | | | **locked formula** |

  `λ_phys^max` is included in the locked tier on the ruling's own terms:
  consequence 1 says "overriding **any** per-stage value is a conformance
  violation", and consequence 4 records that the spec's adjacent "default"
  wording on that line "is now known to be misleading **relative to this
  ruling**" — i.e. the ruling locks the value and the prose is the defect.
  Correcting the prose remains VER-20 item (a), Phase 52.

- **D-02 [LOCKED TABLE HOME]:** The table lives in `pinn/constants.py` — the
  established single home for every spec-cited numeric, and the artifact the
  charter explicitly names as "the pattern to extend" (`§5 layer 3`). It carries
  the `pinn_architecture.md §4.1` line citation and the GAP-45-03 provenance.
  `ScheduledWeights`'s generic per-stage defaults are **not** changed — Phase 48
  D-14 forbids hard-coding stage values into the scheduler, and the gate reading
  a table is exactly how that separation is preserved.
  — **Reversibility:** reversible — a module-level constant with one consumer.

- **D-03 [BOUNDED — no invented lock]:** `λ_IC = 1` appears in §4.1's `where:`
  list (line 644) as a "default", **outside** the warmup-schedule block that
  GAP-45-03 ruled on. Asserting it as *locked* would extend an owner ruling to a
  quantity the ruling never named — a process-artifact-schema call the agent must
  not invent. It is therefore checked and **recorded** at tier `advisory`
  (non-blocking, always reported), and the ambiguity is routed to VER-20 as a
  second instance of the exact locked-vs-default marking problem item (b) already
  names. Two tiers only — `locked` (violation blocks) and `advisory` (violation
  recorded) — and no third tier is invented.

- **D-04 [EXACTNESS]:** The table is stored as explicit literals
  `(0.0, 0.0, 1e-2, 1e-1, 1.0, 1.0, 1.0)` and a companion test proves each
  `k ∈ {2,3,4}` entry equals `10.0 ** (k - 4)`, so the literal and the spec
  formula are provably the same object rather than two hopefully-equal ones.
  Comparison at the gate is exact equality against the canonical derivation —
  the discipline `run_metadata._validate_causal_clip_facts` already uses. No
  tolerance, no `isclose`: a `λ^max` that is *nearly* the locked value is a
  violation.

- **D-05 [ASSERTION SITES]:** Two call sites, one function.
  1. **Run start** — in `pinn/train.py:main()`, after the S_H/`training_metadata`
     establishment block and after `ScheduledWeights` construction, and **before**
     `CurriculumController` construction. The census (D-08) needs the *validated*
     metadata; the table check needs the *actual* `ScheduledWeights` instance;
     both must precede step 1.
  2. **Stage boundary** — in `CurriculumController.step()`, for the **entered**
     stage: at the top of `step()` (covers the initial stage), and again in the
     ADVANCE branch after `self._stage = k + 1` and after any `stage_factory`
     rebinding, so the entered stage's rebound `ScheduledWeights` is asserted
     before a single step of that stage runs. This mirrors the existing
     `check_stage_preflight(k)` seam; that function is **not** modified (it means
     something else — the sL-BFGS PLAT-02 refusal).

- **D-06 [THE SINGLE-STAGE PATH IS A FEATURE, NOT A BUG]:** With no
  `stage_factory` (the shipped default, PLAT-01), stages ≥ 1 are not
  reconfigured. Stage 1's locked row equals Stage 0's, so it passes; **Stage 2
  would correctly FAIL** because `λ_E^max(2) = 1e-2` while the un-rebound
  scheduler still carries `0`. That refusal is the right behavior and must be
  preserved: a run that advances into stage 2 without reconfiguring its λ caps is
  non-conformant. It must **not** be "fixed" by adding a multi-stage factory —
  that is PLAT-01 platform work, blocked by SCOPE-27. A Stage-0-only v2.2 run
  never reaches it.

### GATE-02 — the placeholder census

- **D-07 [EXPLICIT MANIFEST, NOT INFERENCE]:** The census is driven by an
  **explicit, spec-cited manifest** enumerating every quantity in the population.
  It is not inferred from code reflection and it is not derived from
  `TrainingConfig._PROVISIONAL`. Each manifest entry declares: the quantity, its
  spec citation, its expected **resolution class**, and the runtime probe that
  reads its actual value. A quantity absent from the manifest is invisible to the
  gate, so the manifest's completeness is itself a reviewable artifact — which is
  precisely the property the `S_H` gap lacked.

- **D-08 [POPULATION]:** The manifest covers every spec-required quantity the
  loss assembly consumes, grouped by term:
  - `L_data` (§3.1): predicted positions, target positions (resident
    `pre.r_gauge`), `HUBER_DELTA_DATA`, `λ_data`.
  - `L_IC` (§3.3): `true_r0`, `true_v0`, `IC₁₃`, `β_v`, `λ_IC`.
  - `L_phys^causal` (§3.2/§4.1): `masses_ordered`, `EPS_SOFT`, `η_c`
    (`CAUSAL_ETA_C`), the causal-clip facts (the five Phase-48 fields),
    `D_CHARACTERISTIC_LENGTH`, `T_CHARACTERISTIC_TIME`, the `R̄` reduction, the
    collocation set.
  - `L_E` (§3.4): `S_H`, `ε_H = 1e-4·S_H`, `energy_floor_factor`, per-anchor
    `h0`, `HUBER_DELTA_ENERGY`.
  - `L_L` (§3.5): `l0`, `EPS_L`, `HUBER_DELTA_ANGMOM`.
  - Schedule (PHYS-05): `N_Adam,k`, `I_warm`, and the D-01 table.

- **D-09 [RESOLUTION CLASSES AND VERDICT]:** Four classes, and only the first two
  pass unconditionally:
  1. `pipeline` — computed from admitted data at run setup (`S_H`, `h0`, `l0`,
     `IC₁₃`, targets, masses).
  2. `spec-constant` — a `pinn/constants.py` entry with a spec citation
     (`EPS_SOFT`, `η_c`, the Huber deltas, `D`, `T`, `EPS_L`).
  3. `derived` — computed at runtime from 1 or 2 by a locked formula
     (`ε_H`, `I_warm`, the causal-clip facts).
  4. `placeholder` — a provisional stand-in, a hard-coded default with no spec
     citation, or an unbuilt upstream. **Any class-4 entry blocks the run**
     unless it carries an explicit waiver citation (D-16).

  The census additionally cross-checks its own classification against
  `TrainingConfig.provisional_fields()` and **reports disagreement as a finding**.
  It does not adopt that registry's verdict: `stage.energy_floor_factor` is
  registered provisional yet `1e-4` is locked by §3.4, and letting a stale
  in-code tag block a conformant run would be a false positive. The disagreement
  is recorded; correcting a demonstrably stale classification tag is permitted
  inside this phase but is not required for the gate to pass.

- **D-10 [INSTRUMENTATION PRECONDITIONS ARE IN THE CENSUS — recorded scope
  call]:** The census also asserts that the spec-named *instrumentation*
  preconditions resolve — concretely, that `STEP_LOG_FIELDS` carries the ten
  `grad_norm_raw_*` / `grad_norm_applied_*` fields plus `grad_stats_complete`
  that Phase 48 INST-02 landed, and the `w_min`/`w_mean`/`w_max`/`front_idx`
  fields invariants A/B consume. Rationale: the Phase-35 contract names logging
  as a precondition for any reweighting decision, and C-06 (never-logged gradient
  statistics) is the same silent-gap class as the `S_H` case — "a spec-required
  thing that resolved to nothing." This closes the charter's layer-1 third bullet
  at near-zero cost. Recorded explicitly as a deliberate scope call rather than
  silently absorbed, because it is not named in GATE-01..03/INST-03 text.

- **D-11 [SCOPE LINE — what the gate does NOT assert]:** GATE-01 is scoped to
  **PHYS-05** exactly as its requirement text reads. The LR schedule
  (`1e-3·0.7^k`), stage-exit thresholds (`β`, `patience`, `eps_*`), guard
  thresholds, and collocation budgets are **not** asserted as locked tables here:
  the spec itself marks the collocation budgets provisional/example
  (`ctl_instruction.md` LOOP-02/LOOP-06) and no owner ruling locks the others.
  They appear in the census with their true class and in the register where
  relevant, and general config-vs-locked-table coverage stays with the charter
  (SCOPE-32). Recording this line matters more than which side of it a given knob
  lands on — it is what prevents a silent scope drift in either direction.

### GATE-03 — runtime invariants A and B

- **D-12 [INVARIANT A — operational form]:** At every step where the physics term
  was evaluated, assert `w_min > 0.0` and `all(w_n)` finite, with `w_min` read
  from the already-computed `w_n_stats`. Phase 48's dtype-derived
  `clamp_min(exponent, log(finfo.tiny))` makes this true by construction on both
  precision arms, so invariant A is a **cheap standing proof that the construction
  still holds** — a regression detector, not a second implementation of the clip.
  It must not re-derive, re-clip, or re-scale anything.

- **D-13 [INVARIANT A — the degenerate sentinel]:** `front_idx = -1` is
  arithmetically impossible in a well-formed run: the exclusive prefix sum at
  `n = 0` is empty, so `w_0 = exp(0) = 1 > 0.5` always. A `-1` therefore means the
  weight vector is empty or non-finite, and is a **hard invariant-A failure**, not
  a tolerated sentinel. The `default=-1` in `controllers.py` stays as the
  non-raising accessor it was written to be; the gate is what gives `-1` meaning.

- **D-14 [INVARIANT B — operational form, derived]:** Let
  `F_t = max_{s ≤ t} front_idx(s)` be the **high-water mark** of the causal front,
  and let `N_colloc` be the length of the step's own `w_n` vector (read per step,
  never a constant — `collocation_count = 16` is hard-coded at
  `train.py:920` and is not config-resolved). Invariant B holds when, for every
  step `t` with `F_t < N_colloc − 1`, `t − last_advance_step ≤ N`, where
  `last_advance_step` is the most recent step at which `F` strictly increased
  (initialized to the first step of the run). Once `F_t = N_colloc − 1` the front
  is saturated and invariant B is **permanently satisfied** for that run.

  Three properties this form has and the naive readings do not: (i) it catches the
  v2.0 pathology exactly — `front_idx` pinned at 0 means physics supervision
  reached 1 of 16 collocation points for every step of every run; (ii) it does not
  fire spuriously at saturation, where the front *cannot* advance further; (iii)
  using the high-water mark rather than the instantaneous value means a transient
  regression (front 3 → 2 → 3) is not a violation, since the front's job is to
  sweep forward as the model learns, and stochastic bounce is not a stall.

  Supporting arithmetic, for the record: with `η_c = 1` and the 0.5 threshold the
  code uses, `front_idx ≥ 1 ⟺ Σ_{m<1} R̄_m = R̄_0 < ln 2 ≈ 0.6931`, and
  `front_idx = 15` requires the whole 15-bin prefix sum below `ln 2`. The front is
  a direct readout of residual magnitude, which is why it is the right thing to
  watch.

- **D-15 [DISPOSITION — HALT, never RECOVER]:** Both invariants trip as
  **HALT-family** guards. A conformance violation is not a numerical accident:
  rolling back to the last checkpoint and retrying cannot fix a structurally
  invalid run, and routing these through `recover_retries` would convert a loud
  failure into a quiet loop. They extend the existing `StepGuards` machinery in
  `pinn/training/guards.py` — `_GUARD_ORDER`, `_HALT_FAMILY`, `GuardOutcome`,
  `write_failure_bundle`, and the existing `guard_hook` in `train.py` — rather
  than introducing a second per-step guard mechanism.
  — **Reversibility:** costly — `_GUARD_ORDER` and the disposition families are
  consumed by the stage-exit journal and the failure-bundle writer; adding
  families is additive, but re-classifying one later touches those consumers.

- **D-16 [NO CHECK THAT CANNOT FAIL]:** `StepGuards.check()` gains the causal
  statistics it needs (the already-computed `w_n_stats` mapping) as an explicit
  input. When the invariants are enabled and a step evaluated the physics term,
  **absent statistics is itself a HALT** (`causal_stats_missing`), never a silent
  skip. Every guard added by this phase must have a test that drives it to
  actually trip; a guard whose trip branch is unreachable is not coverage. This is
  a direct application of the Phase-39 lesson (a check that structurally cannot
  fail passed three times before it was caught) and it applies equally to the
  preflight assertions of D-01 and D-09.

- **D-17 [RESUME MUST NOT SILENTLY RE-ARM]:** Invariant B carries cross-step
  state (`F`, `last_advance_step`). On resume that state must survive, or a long
  stall is masked by re-arming the window at the resume step. **Preferred:**
  serialize it into the checkpoint payload (the established resume contract),
  accepting a `CHECKPOINT_SCHEMA_VERSION` bump. **Permitted fallback**, if the
  planner's research shows the schema bump ripples too far: re-initialize at the
  resume step **and** record an open register entry saying the window was
  re-armed, so the run carries the caveat. **Prohibited:** silent re-arming.
  — **Reversibility:** costly — checkpoint schema migration touches
  `build_checkpoint_payload`, the resume validator, and existing fixtures.

### The owner checkpoint — `N` for invariant B

- **D-18 [BLOCKING OWNER CHECKPOINT — NOT AUTO-DECIDED]:** `N` is reserved to the
  owner twice over: GAP-45-04's resolution ("**N is deliberately not set here**
  … invariant B is therefore *stated* but not yet *enforceable*"), and the
  roadmap's owner-checkpoint list ("② N for invariant B (Phase 49 — the
  front-advance window)"). The charter §6 classifies it with X and M as a
  calibration decision with false-positive/false-negative trade-offs, "not
  inventable from first principles." **No agent selects `N`.** Everything in D-14
  through D-17 is deliberately `N`-agnostic so the whole mechanism can be built,
  tested, and shipped while the number is outstanding.

- **D-19 [EVIDENCE PACKET THE CHECKPOINT MUST CARRY]:** Following the GAP-45-01
  precedent (present the choice against computed numbers, never as an abstract
  preference), the checkpoint is surfaced with:
  1. the enforced definition of "advance" from D-14, stated explicitly;
  2. the threshold arithmetic `front_idx ≥ 1 ⟺ R̄_0 < ln 2 ≈ 0.6931`;
  3. the run-length anchors from the shipped Stage-0 config:
     `N_Adam,0 = 1000`, `max_epochs = 1000`, so
     `I_warm = min(2000, floor(0.1·1000)) = 100`; `N_colloc = 16`, so
     `front_idx ∈ [0, 15]`;
  4. the v2.0 observation: `front_idx = 0` across 1500/1500 logged steps in 5/5
     runs — which bounds `N` from above if the invariant is to have caught v2.0,
     but was measured on a **non-conformant** run and therefore says nothing about
     healthy advance speed;
  5. the honest statement that **no conformant run has ever executed**, so `N` is
     a policy choice about how long to tolerate silence, not an estimate — with
     both failure directions named: too small HALTs a healthy-but-slow run and
     burns a Phase-50 seed; too large and the invariant never protects the single
     look;
  6. candidate anchors to react to, not a recommendation to ratify:
     `N = I_warm = 100`, `N = 0.25·N_Adam,0 = 250`, `N = 0.5·N_Adam,0 = 500`, or
     explicit deferral to the D-20 record-only path.

  Obtaining a fresh real-corpus `R̄_0` under the corrected `(1/3)Σ` and completed
  frame would strengthen item 2 and is **permitted** via the established
  gitignored single-trajectory copy pattern, but is **not required** — the packet
  above is complete without it, and the 5.32e+09 figure carried in GAP-46-07 must
  not be re-cited without stating which `R̄` convention produced it.

- **D-20 [`N` UNSET IS A DEFINED, FAIL-CLOSED STATE — the phase does not
  deadlock]:** `N` is an explicit config field (`run.invariants.front_advance_
  window_n`) with **no default**. If it is absent or null:
  - invariant B runs in **record-only** mode (state tracked, statistics logged,
    no HALT);
  - preflight records the open divergence `INV-B-N-UNSET` in the register;
  - the run record reports at least one unwaived open divergence, which sets
    `eval01_precondition_i = false`.

  So a run may still proceed, but it is **structurally ineligible** to spend the
  single look — exactly the protection EVAL-01 precondition (i) exists to give.
  Phase 49 can therefore close on the owner's schedule rather than blocking on it.
  When `N` is set, invariant B enforces and `threshold_provisional` is `false` on
  the resulting `GuardOutcome`.

- **D-21 [NO PROXY FOR `N`]:** No agent may substitute a "temporary", "provisional",
  or "conservative" `N` and mark it revisitable. The Phase-48 causal clip was
  legitimately implementer-chosen because GAP-45-04 consequence 3 explicitly
  delegated it and the bound is dtype-derived rather than fitted; consequence 2
  withheld `N` in the same ruling. Choosing a number here would also be
  SCOPE-29-shaped: a front-advance window fitted to what a run is observed to do
  is a threshold tuned against results.

### INST-03 — the known-divergence register

- **D-22 [FORM AND LOCATION]:** One first-class, machine-readable file:
  `pinn/conformance/divergence_register.json`, with a strict schema, a
  `schema_version`, and fail-closed validation on load — mirroring
  `run_metadata.py`'s `training_metadata.json` (schema v2) and the Phase-46
  validation sidecars. JSON rather than Markdown because **preflight parses it**
  and the run record embeds it, and a prose table would need a parser and would
  drift; JSON rather than YAML for parity with every other machine-read artifact
  in this codebase. Human readability is served by free-text `rationale` and
  `what_it_would_take` fields per entry plus rendering in `summary.md` — one
  source, no second copy.
  — **Reversibility:** costly — the run record embeds the schema, so a later
  format change is a schema migration across preflight, summary, and any Phase-52
  consumer.

- **D-23 [ENTRY SCHEMA]:** Each entry carries `id`, `kind`, `status`, `title`,
  `spec_citation`, `authority`, `rationale`, `what_it_would_take`, and
  `proof_test` (D-25). Three `kind` values, because collapsing them would be
  dishonest:
  - `divergence` — the implementation knowingly departs from a locked spec value
    or formula (the charter's original definition);
  - `qualification` — the implementation conforms, but a recorded caveat must
    travel with a claim made about it;
  - `deferred-scope` — a locked capability that is deliberately unbuilt under an
    owner-ratified scope boundary.

  `status` is `open`, `closed`, or `waived`.

- **D-24 [INITIAL CONTENTS]:** The audit's C-01..C-08 are transcribed as the
  register's initial contents (charter §9 item 2), each with its **current**
  status re-derived from the v2.2 record rather than copied from the audit:
  C-01/C-02 closed by CONF-05, C-03 by CONF-04, C-04 by CONF-03, C-05 by CONF-06,
  C-06 by INST-02, C-07 by the GAP-45-01 option-A ruling, C-08 by TEST-01/02;
  plus the two later-discovered divergences CONF-08 (`kind: divergence`, closed)
  and CONF-09 (closed). At least four entries are expected **open** at Phase-49
  close and must be present:
  1. `CONF-01-QUALIFICATION` (`kind: qualification`) — RG-02 was settled by owner
     ruling on measured arm evidence, **not** by a clean
     `VERDICT_TARGETS_ARE_RAW`/`_SCALED` token. REQUIREMENTS.md makes this
     qualification mandatory wherever CONF-01 is cited under EVAL-01 precondition
     (ii); the register is what makes it travel automatically into the run record
     instead of depending on a human remembering.
  2. `PLAT-01-SINGLE-STAGE` (`kind: deferred-scope`, waived by SCOPE-27) — stages
     ≥ 1 are not reconfigured with no `stage_factory` (see D-06).
  3. `PLAT-02-SLBFGS` (`kind: deferred-scope`, waived by SCOPE-27/PLAT-02) —
     stages 3–6 refuse via `check_stage_preflight`.
  4. `INV-B-N-UNSET` (`kind: divergence`, open and unwaived) — present until the
     owner sets `N` (D-20).

  Two further low-severity entries the scout surfaced and that should not stay
  invisible: `I_warm` is integer-floored where §4.1 writes `min(2000, 0.1·N_Adam,k)`
  without a floor (an interpretation, not a departure — a step count must be an
  integer, and the two agree at `N_Adam,0 = 1000`), and `collocation_count = 16`
  is hard-coded at `train.py:920` rather than config-resolved (the spec marks
  collocation budgets provisional, so this is a wiring gap, not a value defect).

- **D-25 [THE REGISTER MUST DEFEND ITSELF]:** Every entry whose `status` is
  `closed` and whose closure is testable cites the named test that proves it in
  `proof_test`, and CI runs those tests. A register that asserts "C-03 closed"
  while the code regressed is worse than no register — it launders a defect into a
  clean run record. This is the same anti-pattern D-16 guards at the runtime layer.

- **D-26 [THE REGISTER CREATES NO AUTHORITY]:** Every `waived` entry cites an
  **already-granted** authorization by identifier — a scope boundary
  (SCOPE-27/28), a gap ruling (GAP-45-0x, GAP-46-0x), or an audit finding. The
  register never grants a waiver, and Phase 49 defines **no waiver policy**: who
  may waive, and whether a waived run remains eligible to spend evaluation budget,
  are open charter §6 questions owned by the charter workstream (SCOPE-32). The
  `waiver` field is a citation slot, not a decision surface. Consequently the
  register is a **derived record**, never a grounding source.

### The run record and the EVAL-01 projection

- **D-27 [ARTIFACT AND PROJECTION]:** Preflight writes
  `runs/<run>/preflight.json` — atomic write, strict schema, fail-closed
  re-validation on load, one `assertions` array appending one record per
  assertion event (`run_start`, and `stage_boundary` for each entered stage). A
  **refusal writes the artifact first, then exits non-zero** through the existing
  `finish_run("failed", 1)` path: a blocked run must leave the evidence that says
  why it was blocked. `summary.py` projects a `conformance` block as a
  **verbatim passthrough** of the persisted bytes — never recomputed, never
  null-collapsed — following the Phase-46 `_GATE_KEYS` D-19/D-20 discipline
  exactly, and adds `eval01_precondition_i` alongside the existing
  `eval01_precondition_iii`. Phase 51 remains the **verifier** of the three
  preconditions; Phase 49 only makes the facts mechanically available so Phase 51
  is not reverse-engineering them from logs.

- **D-28 [NAMING — do not collide with the Phase-46 gate vocabulary]:** Phase 46
  established `gate_status` (instrumentation health) and `gate_verdict`
  (ε_H/SCS metric) with a deliberate distinction between them. Phase 49's "gate"
  is a *different* object — the conformance gate. Every field this phase adds is
  prefixed `conformance_*` or `preflight_*`; **no `gate_*` key is reused,
  redefined, or overloaded.** New JSONL events extend `STEP_LOG_FIELDS` (the
  canonical registry with its non-finite policy) rather than opening a second log.

### Verification strategy and the no-run boundary

- **D-29 [DATASET-FREE, PER THE OWNER'S PHASE-47 PRECEDENT]:** Phase 49 proves
  the gate with deterministic fixtures and synthetic sources in `tests/phase49/`,
  following the owner's 2026-07-30 Option-B ruling that governed Phase 47 —
  "prove the semantics with deterministic fixtures; no zero-step emitter added;
  first authoritative real-corpus artifact deferred to Phase 50." **No
  preflight-only run mode, no zero-step emitter, and no admitted-corpus
  invocation is added by this phase.** The gate's first real-corpus contact is
  Phase 50's run start.

- **D-30 [DE-RISK THE FIRST CONTACT ANYWAY]:** Because D-29 means the gate is
  unexercised against real data until Phase 50, it must be built to make that
  first contact low-risk: preflight reads only already-persisted,
  already-validated inputs (`training_metadata.json`, the resolved
  `TrainingConfig`, the live `ScheduledWeights`, the register file) and computes
  nothing new about the data. An end-to-end seam test must drive the real
  `main()` ordering — `data.source: synthetic`, a handful of steps — through
  preflight to the first guard evaluation, so the ordering constraint in D-05 is
  proven by execution rather than by inspection. Test conventions follow Phase 48:
  `pytest` under the repo `.venv`, with the locked `conda run -n pinn-train`
  torch-2.12.1 MPS probe where backend behavior is the claim.

### SCOPE-32 — the coordination decision (roadmap success criterion 5)

- **D-31 [DECISION, with evidence, 2026-08-04]:** **The charter workstream has
  landed no consumable deliverable; v2.2 implements the minimum subset.**
  Evidence, re-derivable: a repository-wide search finds
  `docs/work/designs/cross_cutting/training-verification-regime/2026-07-24-verification-enforcement-charter.md`
  as the workstream's only artifact — every other hit is a *reference* to it from
  `.planning/` or the v2.2 proposal. No divergence register, no normative-statement
  index, no preflight code, and no charter branch or worktree exists
  (`git worktree list` shows only `master`, `fut05-comments`, `specwork`,
  `trainex`). The planner **re-runs this check at planning time** and records the
  date; if a charter deliverable has landed in the interim, it is consumed rather
  than duplicated.

- **D-32 [FORWARD COMPATIBILITY — build so the charter can subsume this]:** The
  minimum subset is shaped so the general regime absorbs it without a rewrite:
  a named module boundary (`pinn/conformance/`) rather than logic scattered
  through `train.py`; a versioned register schema; **no waiver policy** (D-26);
  **no X/M thresholds** invented (charter §6); and the normative-statement index
  explicitly not started. Where this phase must choose, it chooses the narrower
  option and records the boundary (D-11).

### Claude's Discretion

The planner and executor own, without re-opening anything above: module and
symbol names inside `pinn/conformance/`; the exact `preflight.json` and register
JSON field names and schema-version numbering; how the D-17 invariant-B state is
threaded (checkpoint payload preferred, re-arm-and-record permitted, silent
re-arm prohibited); the precise `StepGuards` integration signature; test-file
organization within `tests/phase49/`; and whether the small D-24 interpretation
entries are one register row or two. Those choices must preserve every decision
above, add no dependency, keep JSON as the durable machine-read format, and
introduce no threshold, cadence, waiver authority, or evaluator path outside this
phase.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and owner-ratified boundaries

- `.planning/ROADMAP.md` §"Phase 49: Conformance Gate" — goal, requirements, the
  `N` owner checkpoint, and the five success criteria (including the SCOPE-32
  coordination record).
- `.planning/ROADMAP.md` §"Conformance discipline (applies to all phases)" —
  hard boundaries, the binding evaluation policy, grounding inputs, and the
  owner-checkpoint list.
- `.planning/REQUIREMENTS.md` — GATE-01..03, INST-03, SCOPE-27..32, and the
  binding evaluation policy with its EVAL-01 preconditions.
- `.planning/PROJECT.md` — active v2.2 milestone and the owner-ratified
  evaluation policy.
- `.planning/STATE.md` — Phase 49 position and the inherited Phase 47/48
  decisions (notably the 2026-07-30 Option-B deferral of the first real-corpus
  `S_H`/`ε_H`/`N_train` to Phase 50).
- `CLAUDE.md` / `AGENTS.md` — STOP protocol, source precedence, and Git policy.

### The owner rulings this phase implements

- `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md`
  §"GAP-45-03" — the full PHYS-05 lock-boundary record and its five numbered
  consequences. **The primary grounding for GATE-01.**
- `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md`
  §"GAP-45-04" — invariant A locked and self-executing; invariant B stated with
  `N` withheld as owner-owned; the implementer-delegated clip. **The primary
  grounding for GATE-03 and for D-18/D-21.**
- `.planning/milestones/v2.1-GAPS.md` — the five v2.1 rulings and the six
  obligations inherited by this milestone (item 4 is GATE-01's).
- `.planning/milestones/v2.2-GAPS.md` — GAP-46-01..07 and GAP-47-01, and the
  record that GAP-45-01 is resolved.

### The charter and the audit

- `docs/work/designs/cross_cutting/training-verification-regime/2026-07-24-verification-enforcement-charter.md`
  §5 (three layers plus the register), §6 (the owner-owned open questions,
  including `N`), §7 (rationed evaluation needs a conformance precondition), §9
  (suggested first moves). **The authority on the general regime — SCOPE-32.**
- `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md`
  — C-01..C-08 (the register's initial contents) and the equally binding
  "verified clean" inventory.
- `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-28-conformance-divergence-verification-report.md`
  — independent confirmation plus the seventh (CONF-09) divergence and its
  measured consequences.
- `docs/work/designs/cross_cutting/v2.2-milestone-proposal/2026-07-25-v2.2-roadmap-proposal.md`
  — the owner-ratified proposal the milestone was generated from.

### Locked spec sections

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  §4.1 (lines 633–678) — the PHYS-05 warmup schedule, the per-stage `λ^max(k)`
  table at line 663, the `λ_phys^max` "default" wording at line 662, the causal
  clip mandate at lines 647–650, the Phase-35 LOSS-02 contract note, and the
  optimizer-phase / stage-boundary re-warm semantics.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  §§3.1–3.5 — the component contracts whose consumed quantities form the D-08
  census population.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
  §"Loss Function Formulation" (~line 1757 ff.) — total-loss assembly, the
  Phase-35 logging precondition, the data-vs-collocation point separation
  (LOOP-02) and the provisional collocation budgets (LOOP-06).

### Immediate predecessors

- `.planning/phases/48-loss-math-conformance/48-CONTEXT.md` — D-08..D-12 (the
  causal clip and its explicit Phase-49 boundary), D-13..D-15 (Stage-0
  `λ_E^max = 0` and the deliberate non-hard-coding of stage values in the
  scheduler), D-16..D-20 (the gradient statistics the census asserts).
- `.planning/phases/48-loss-math-conformance/48-VERIFICATION.md` and
  `48-04-SUMMARY.md` §"Phase-50 handoff" — what Phase 48 verified and what it
  explicitly left to Phase 49.
- `.planning/phases/47-frame-completion-s-h-pipeline/47-CONTEXT.md` — the frame
  and `S_H`/`ε_H` decisions the census asserts as real.
- `.planning/phases/46-frame-resolution-gate-aligned-validation/46-CONTEXT.md` —
  the `gate_*` vocabulary D-28 must not collide with, and the
  `eval01_precondition_iii` projection pattern D-27 mirrors.

### Code and test seams

- `pinn/training/scheduled_weights.py` — the PHYS-05 schedule state machine; its
  "provisional seams (CTX-38)" docstring is the prose GATE-01 supersedes.
- `pinn/constants.py` — the spec-cited-numeric home the locked table extends.
- `pinn/train.py:860-935` — the S_H metadata block, `ScheduledWeights`
  construction, and the `CollocationSampler(collocation_count=16)` hard-code;
  D-05's run-start assertion site sits here.
- `pinn/train.py` `guard_hook` and `finish_run` — the existing per-step guard
  callback and the fail-closed exit path D-27 reuses.
- `pinn/training/controllers.py` — `CurriculumController.step()` and its ADVANCE
  branch (D-05 site 2); `RunController._non_data_terms` and
  `_last_widened_details["w_n_stats"]` (the `w_min`/`front_idx` source);
  `build_checkpoint_payload` (D-17).
- `pinn/training/guards.py` — `_GUARD_ORDER`, `_HALT_FAMILY`, `GuardOutcome`,
  `StepGuards.check`, `write_failure_bundle`.
- `pinn/training/slbfgs_preflight.py` — `check_stage_preflight`, the existing
  stage-entry seam; **not modified**, it means the PLAT-02 refusal.
- `pinn/training/run_metadata.py` — `training_metadata.json` schema v2, the
  atomic-write / re-validate-on-load / exact-canonical-comparison pattern the
  register and `preflight.json` follow.
- `pinn/training/step_log.py` — `STEP_LOG_FIELDS` (37 fields), the non-finite
  policy, and `JsonlStepHandler`.
- `pinn/training/summary.py` — `_GATE_KEYS`, `_GATE_MD_ORDER`,
  `_eval01_precondition_iii`, `_compose`, `_render_md`.
- `pinn/loss_catalog.py` `causal_physics_loss` / `resolve_causal_clip_facts` —
  the Phase-48 clip whose standing proof is invariant A.
- `pinn/training/config.py` — `LossConfig`, `_PROVISIONAL`,
  `provisional_fields()`, `ConfigRequiredError` (the fail-closed
  required-field pattern for `N`).
- `configs/stage0-example.yaml`, `configs/smoke.yaml` — `n_adam: 1000` / `300`,
  `lambda_e_max: 0.0`, and the `run.guards:` block that `run.invariants:` sits
  beside.
- `tests/phase48/`, `tests/phase47/`, `tests/phase46/_fixtures.py`,
  `tests/phase40/_fixtures.py` — the dataset-free fixture and stub-controller
  conventions D-29/D-30 follow.
- `.planning/phases/48-loss-math-conformance/48-VALIDATION.md` — the exact
  pytest and `conda run -n pinn-train` MPS probe command forms.

### Explicitly excluded source

- `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/` — not a
  grounding source under SCOPE-31. Do not consult its tuning analysis; only
  independently verified `[FACT-W]` findings may be used, and none is needed
  here.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- **`StepGuards`** already provides everything invariant A/B need except the
  causal statistics: an ordered guard evaluation, RECOVER/HALT families with HALT
  winning a tie, a `GuardOutcome` carrying `guard`/`metric`/`value`/`threshold`/
  `threshold_provisional`, failure-bundle writing, and a live `guard_hook` call
  site in `train.py`. `threshold_provisional` maps exactly onto `N`'s
  owner-owned status.
- **`run_metadata.py`** is the worked example for a strict, versioned,
  atomically written, fail-closed-on-load JSON artifact — including
  `_validate_causal_clip_facts`'s exact-equality-against-canonical-derivation
  comparison, which D-04 reuses for the λ table.
- **`_GATE_KEYS` / `_eval01_precondition_iii` in `summary.py`** are the worked
  example for projecting persisted bytes into the run record without
  recomputation or null-collapse — the D-27 pattern.
- **`ScheduledWeights`** already exposes `warmup_length`, `n_adam_k`, and the
  three `λ^max` caps, and already defaults Stage 0 correctly. The gate reads it;
  it does not change it.
- **`TrainingConfig.provisional_fields()`** is an existing enumerate-with-
  provenance surface. It is a *config-threshold* seam, not the census population
  — D-09 cross-checks against it and reports disagreement rather than adopting
  its verdict.
- **`check_stage_preflight`** proves the stage-entry seam already exists and is
  already called at exactly the right moment in `CurriculumController.step()`.
- **`ConfigRequiredError`** is the established fail-closed pattern for a config
  field that must be explicitly supplied.

### Established Patterns

- Strict JSON schemas with `schema_version`, atomic writes, and re-validate-on-
  load — `training_metadata.json` (v2), `summary.json` (v1), the Phase-46
  validation sidecars. New artifacts follow it rather than inventing an informal
  sidecar.
- One canonical JSONL event stream fanning out to optional sinks; new fields
  extend `STEP_LOG_FIELDS`, they never open a second log.
- Phase-scoped tests are dataset-free and use synthetic sources and stub
  controllers; no training run is needed to prove a repair.
- Assembly-boundary interception is preferred over duplicating component
  formulas in tests — every verified divergence in this milestone lived in a
  seam, not in a component.
- Instrumentation state and metric state are kept distinct (`gate_status` vs
  `gate_verdict`), so an instrumentation failure can never render as a PASS.
  D-28 extends that discipline to the conformance vocabulary.

### Integration Points

- **Config → gate:** `TrainingConfig` (incl. the new `run.invariants` block) and
  the live `ScheduledWeights` feed the D-01 table assertion.
- **Metadata → census:** the validated `training_metadata.json` (`s_h`, `eps_h`,
  `energy_floor_factor`, the five causal-clip fields, the frame block) is how the
  census proves the `L_E` and clip quantities are real rather than stand-ins.
- **Register → preflight → run record:** `divergence_register.json` is loaded at
  run start, its open entries are copied into `preflight.json`, and `summary.py`
  projects them plus `eval01_precondition_i`.
- **Controller → invariants:** `_last_widened_details["w_n_stats"]`
  (`w_min`, `w_mean`, `w_max`, `front_idx`) is the per-step input; the length of
  the step's own `w_n` vector supplies `N_colloc` for the D-14 saturation test.
- **Invariants → guards → failure bundle:** two new HALT-family guards reuse the
  existing outcome, journaling, and bundle-writing path.
- **Checkpoint → resume:** invariant-B state must survive a resume (D-17).

</code_context>

<specifics>
## Specific Ideas

- **The gate's whole purpose is one sentence:** a run that is not the specified
  experiment must be unable to reach the evaluator. Every design choice above is
  answerable to that sentence — if a check cannot block, cannot fail, or cannot
  be seen in the run record, it is decoration.
- **Two silent-gap classes, one lesson.** `S_H` (a spec prerequisite that was
  never built) and the gradient statistics (a spec-named precondition that was
  never logged) both passed every code-vs-spec review, because the code was as
  compliant as it could be given something that did not exist. Only an explicit
  enumeration of what *must* resolve catches that class — hence D-07's manifest
  and D-10's inclusion of instrumentation.
- **The register is what makes a run honest about itself.** Phase 44 ranked a
  generalization hypothesis as Strong while five spec divergences sat unlisted in
  code comments. That ordering was reasonable given what the phase could see. The
  register changes what a phase can see.
- **A closed register entry with no proof test is a liability, not an asset**
  (D-25) — and so is a guard whose trip branch no test reaches (D-16). Both are
  the same failure: a check that cannot fail reads as a check that passed.
- **`N` is the one number nobody may guess.** The clip bound was legitimately
  implementer-chosen because it is dtype-derived and the ruling delegated it. `N`
  is a policy about tolerated silence on a run type that has never executed, and
  the same ruling withheld it. D-20 exists so that withholding costs the phase
  nothing.

</specifics>

<deferred>
## Deferred Ideas

- **The general verification-enforcement regime** — normative-statement index,
  full CI integration, waiver policy (who may waive; whether a waived run may
  spend evaluation budget), and thresholds X (dominance ratio) and M (persistence
  window) — charter workstream, SCOPE-32. Explicitly not started here.
- **A preflight-only / zero-step run mode** — would have de-risked the gate's
  first real-corpus contact, but the owner's 2026-07-30 Option-B ruling that
  governed Phase 47 (no zero-step emitter; first real-corpus artifact deferred to
  Phase 50) applies with equal force. Reconsider only on owner instruction.
- **Multi-stage `λ^max` reconfiguration (`stage_factory`)** — PLAT-01, blocked by
  SCOPE-27. Phase 49 makes its absence a loud stage-2 refusal (D-06) rather than
  fixing it.
- **Stochastic L-BFGS for stages 3–6** — PLAT-02, blocked by SCOPE-27.
- **Config-resolving `collocation_count`** — registered as a wiring gap (D-24);
  changing it is a recipe surface and is out of scope under SCOPE-29.
- **Spec-text amendments** — the `λ_phys^max` "default" wording, the
  locked-vs-default marking convention (now with the second `λ_IC` instance from
  D-03), the explicit `L_data` reduction, and the GAP-44-01 aggregate gate
  statistic — VER-20 routing list, Phase 52, for a later spec milestone
  (SCOPE-30).
- **First authoritative real-corpus `S_H` / `ε_H` / `N_train` and the first
  exercise of this gate against real data** — Phase 50.
- **Verifying and recording the three EVAL-01 preconditions, and the single
  authorized evaluation** — Phase 51. Phase 49 only projects
  `eval01_precondition_i` into the run record.
- **Recipe tuning and trainex-r2 remedy adjudication** — v2.3 (SCOPE-29/31).

### Reviewed Todos (not folded)

- **`d-06-static-epsilon-sensitivity-check`** (matched at score 0.60 on the
  lexical keywords "check / open / phase") — not folded. A sensitivity study over
  a static epsilon is tuning-shaped work prohibited by SCOPE-29 and is unrelated
  to building an enforcement gate. Same disposition as Phase 48, for the same
  reason.
- **`trainex-r1-research-handoff`** — not folded. Research-administration work
  unrelated to Phase 49.

</deferred>

---

*Phase: 49-conformance-gate*
*Context gathered: 2026-08-04*
