# Phase 49: Conformance Gate - Research

**Researched:** 2026-08-04
**Domain:** Internal training-pipeline conformance gating (preflight assertion + per-step runtime guards + a first-class divergence register), no external libraries
**Confidence:** HIGH — every claim below is grounded in a file:line read this session; no web research was needed because the phase is a pure extension of existing, already-read internal modules

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-------------------|
| GATE-01 | Preflight asserts the **full** PHYS-05 per-stage `λ^max` table (not merely the `≤1` cap) at run start and at every stage boundary (per GAP-45-03). | `## Standard Stack`, `## Architecture Patterns` Pattern 1/Code Examples (D-05 site 1/2 exact insertion points), `## Common Pitfalls` #1 (`state_dict()` vs `current()`), `## Code Examples` |
| GATE-02 | Preflight placeholder census: every spec-required quantity the loss consumes resolves to a real pipeline value, or is explicitly owner-waived for that run. | `## Census Population Map` (full D-08 quantity → source → class table, zero unlocatable quantities), `## D-10 Verification` |
| GATE-03 | Runtime invariants: no causal weight exactly zero (invariant A); the causal front advances within N steps (invariant B — N is an owner checkpoint). Fail loud, fail early. | `## Architecture Patterns` Pattern 1 (`w_n_stats`/`N_colloc` already reachable in `guard_hook` with no threading), `## D-17 Verdict` (checkpoint-payload state survival), `## Common Pitfalls` #2 |
| INST-03 | Maintain the known-divergence register; the run record surfaces every open divergence so a run carries its own caveats. | `## Architecture Patterns` Pattern 2 (register pattern source: `run_metadata.py`), Pattern 3 (`summary.py` verbatim-passthrough extension point) |
</phase_requirements>

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

Twenty-eight decisions, D-01..D-28. Every decision below is grounded in a cited
owner ruling, a locked spec line, a verified audit finding, or a short
first-principles derivation stated inline. One item — the numeric value of `N`
for invariant B — is **deliberately left undecided** and preserved as a blocking
owner checkpoint (D-19..D-21).

*(Note: CONTEXT.md's own header text says "Twenty-eight decisions, D-01..D-28"
but the body enumerates D-01 through D-32 — the count is stale prose in the
source document, reproduced verbatim here per the copy-exactly instruction; do
not silently correct it.)*

#### GATE-01 — the PHYS-05 table assertion

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

#### GATE-02 — the placeholder census

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

#### GATE-03 — runtime invariants A and B

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

#### The owner checkpoint — `N` for invariant B

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

#### INST-03 — the known-divergence register

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

#### The run record and the EVAL-01 projection

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

#### Verification strategy and the no-run boundary

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

#### SCOPE-32 — the coordination decision (roadmap success criterion 5)

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

### Deferred Ideas (OUT OF SCOPE)

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

**Reviewed Todos (not folded):**
- **`d-06-static-epsilon-sensitivity-check`** (matched at score 0.60 on the
  lexical keywords "check / open / phase") — not folded. A sensitivity study over
  a static epsilon is tuning-shaped work prohibited by SCOPE-29 and is unrelated
  to building an enforcement gate. Same disposition as Phase 48, for the same
  reason.
- **`trainex-r1-research-handoff`** — not folded. Research-administration work
  unrelated to Phase 49.
</user_constraints>

## Summary

Phase 49 adds no new dependency and touches no framework spec. It is a **wiring
phase**: extend `StepGuards` with two new HALT-family guards (`guards.py`),
add a table-assertion + census function pair (a new `pinn/conformance/`
module) called from two already-identified call sites in `train.py` and
`controllers.py`, add a versioned `divergence_register.json` artifact
following the exact pattern `run_metadata.py` already established, and extend
`summary.py`'s existing verbatim-passthrough discipline with a `conformance`
block. Every "where does this hook in" question in the research brief has a
concrete, already-existing answer in the code — this phase has unusually low
architectural risk because Phases 40-48 already built every seam it needs
(`guard_hook`, `checkpoint_hook`, `_last_widened_details`, the
`run_metadata.py` atomic-write pattern, the `summary.py` `_GATE_KEYS`
passthrough pattern).

The single highest-value finding is on D-17 (checkpoint schema bump): the
codebase's own discipline of importing `CHECKPOINT_SCHEMA_VERSION` as a
symbol everywhere (never a hard-coded literal) means the "costly" migration
CONTEXT.md flagged is, on inspection, **cheap** — one constant, one additive
payload key, no fixture regeneration. See the D-17 Verdict section below.

The second highest-value finding is a genuine pitfall, not a gap: `ScheduledWeights`
exposes `warmup_length` and `n_adam_k` as public properties, but the three
`lambda_*_max` caps and `lambda_ic` are **private attributes with no public
accessor** — the gate must read them via `.state_dict()`, and must NOT call
`.current(epoch)` to infer the caps (that returns the *ramped* value, which is
`0` at epoch 0 regardless of the cap). See Common Pitfall 1.

No D-08 census quantity was unlocatable. Every quantity in the population
resolves to a real, cited code path (table in `## Census Population Map`
below). Two minor findings surfaced during the search, both non-blocking and
both already anticipated by D-09/D-11: `beta_v` is a `loss_catalog.py`
function-default parameter, not a `pinn/constants.py` entry (a house-style
deviation, not a placeholder); and `stage.energy_floor_factor` is registered
in `TrainingConfig.provisional_fields()` even though §3.4 locks it — this is
exactly the disagreement D-09 already told the census to record, not adopt.

**Primary recommendation:** build `pinn/conformance/` as three thin modules —
a table/census module, a register module, an invariants module extending
`StepGuards` — each following an already-proven pattern in this codebase
(`constants.py` for the table, `run_metadata.py` for the register,
`guards.py` itself for the invariants), and wire them into `train.py`/
`controllers.py` at the exact insertion points cited below.

## Architectural Responsibility Map

This phase has no browser/API/DB tiers — it is a single-process Python
training pipeline. The table below maps each requirement to the code layer
that owns it (adapted from the generic tier taxonomy).

| Capability | Primary Layer | Secondary Layer | Rationale |
|------------|---------------|------------------|-----------|
| GATE-01 PHYS-05 table assertion | Training composition root (`train.py:main()`) | Stage-transition controller (`CurriculumController.step()`) | The table check needs the *live* `ScheduledWeights` instance, which both layers hold; run-start owns the once-only stage-0 check, the controller owns re-assertion at every entered stage (D-05 two-site design) |
| GATE-02 placeholder census | Training composition root (`train.py:main()`, after S_H/metadata + ScheduledWeights) | Config/metadata layer (`TrainingConfig`, `training_metadata.json`) | Census reads only already-validated setup-time artifacts (D-30); no per-step evaluation |
| GATE-03 invariants A/B | Per-step guard layer (`pinn.training.guards.StepGuards`) | `RunController` (source of `w_n_stats`) | Guards already own the per-step HALT/RECOVER evaluation + disposition + failure-bundle machinery; invariants are two new guard families sharing it (D-15) |
| INST-03 divergence register | New persistence module (`pinn/conformance/`) | Run-record projection (`pinn.training.summary`) | The register is a standalone versioned JSON artifact (mirrors `training_metadata.json`); `summary.py` projects its open entries read-only, never recomputes |
| D-27 run-record `conformance` block | Run-record projection (`pinn.training.summary._compose`) | Preflight artifact (`preflight.json`) | `summary.py` is the established verbatim-passthrough layer (`_GATE_KEYS` precedent); `preflight.json` is the producer it reads from |

## Standard Stack

No new libraries. This phase extends five existing modules and adds a new
first-party package (`pinn/conformance/`, does not exist yet — verified via
`ls pinn/conformance` returning nothing) plus a new test package
(`tests/phase49/`, also does not exist yet).

### Core (existing modules this phase extends)

| Module | Role in Phase 49 | Why this module |
|--------|-------------------|------------------|
| `pinn/training/guards.py` | Add 2 HALT-family guards (invariant A, invariant B) + `causal_stats_missing` HALT | `StepGuards` already owns per-step HALT/RECOVER, `GuardOutcome`, failure-bundle writing (D-15) |
| `pinn/training/run_metadata.py` | Pattern source, not modified | Worked example for atomic-write / re-validate-on-load / exact-equality (D-04, D-22 reuse this) |
| `pinn/training/summary.py` | Add `conformance` block + `eval01_precondition_i` to `_compose`/`_render_md` | Existing `_GATE_KEYS` verbatim-passthrough discipline is exactly D-27's contract |
| `pinn/training/step_log.py` | No new fields required — `w_min`/`w_mean`/`w_max`/`front_idx` and the 10 gradient-norm fields already exist (verified, see D-10 Verification below) | `STEP_LOG_FIELDS` is the canonical registry (D-28: extend, never open a second log) |
| `pinn/training/config.py` | Add `InvariantsConfig` nested dataclass (`run.invariants.front_advance_window_n: Optional[int] = None`) | `RunConfig` already nests `GuardConfig`/`CheckpointCadence`/`MonitorConfig` this way |
| `pinn/training/config_yaml.py` | Register `InvariantsConfig` in `_resolve_nested_cls`'s `known` dict | **Required, not automatic** — see Common Pitfall 3 |
| `pinn/constants.py` | Add the D-01 locked table | House style: module-level literals with an inline spec citation |
| `pinn/train.py` | Two call sites (D-05 site 1) + `guard_hook` gains `w_n_stats`/`N_colloc` access (already free, see A.2 below) | Composition root |
| `pinn/training/controllers.py` | `CurriculumController.step()` two call sites (D-05 site 2), `build_checkpoint_payload` gains an additive key (D-17) | Owns the ADVANCE branch and the checkpoint envelope |

### New module (this phase creates)

| Path | Purpose |
|------|---------|
| `pinn/conformance/__init__.py` | Package marker (D-32: named module boundary) |
| `pinn/conformance/<table-module>.py` (name is discretion) | GATE-01 table assertion, reading `pinn.constants`'s new table + the live `ScheduledWeights.state_dict()` |
| `pinn/conformance/<census-module>.py` (name is discretion) | GATE-02 census against the D-07 manifest |
| `pinn/conformance/<register-module>.py` (name is discretion) | INST-03 `divergence_register.json` load/validate, mirroring `run_metadata.py` |
| `pinn/conformance/preflight.py` (name is discretion) | Writes `runs/<run>/preflight.json` (D-27), composes table + census + register into one artifact |

### Alternatives Considered

| Instead of | Could use | Tradeoff |
|------------|-----------|----------|
| A new `pinn/conformance/` module | Inline functions in `train.py`/`controllers.py` | Rejected by D-32 explicitly — "a named module boundary… rather than logic scattered through train.py" |
| `StepGuards.check()` new kwarg for `w_n_stats` | A parallel second guard mechanism | Rejected by D-15 explicitly — reuse `_GUARD_ORDER`/`_HALT_FAMILY`/`GuardOutcome` |

**Installation:** none — no `pip install` needed; every dependency (`torch`, `numpy`, `pytest`) is already present in the repo's `.venv` (verified: `.venv/bin/python -m pytest --version` → `pytest 9.1.1`).

## Package Legitimacy Audit

**Not applicable.** This phase installs no external packages — it is a pure
extension of existing first-party modules under `pinn/`. No `npm install` /
`pip install` / `cargo add` of any kind. The Package Legitimacy Gate protocol
is therefore skipped; nothing to audit.

## Architecture Patterns

### System Architecture Diagram

```
                         run start (train.py main())
                                    |
                 [config load, S_H/training_metadata.json
                  established+validated, ScheduledWeights built]
                                    |
                                    v
                +-------------------------------------------+
                |  GATE-01 table assert (D-05 site 1)        |
                |  + GATE-02 census (D-07..D-11)             |
                |  reads: config, scheduled_weights,         |
                |         training_metadata.json,            |
                |         divergence_register.json           |
                +-------------------------------------------+
                     |  pass                    |  fail
                     v                           v
        writes runs/<run>/preflight.json   writes preflight.json
        (assertions=[run_start])           (refusal), then
                     |                      finish_run("failed", 1)
                     v
         curriculum.run() -> CurriculumController.step()  <---+
                     |                                        |
        top-of-step(): re-assert D-01 table for self._stage   |
        (covers initial/resumed stage)                        |
                     |                                        |
        _get_disposition -> run_controller.run_stage(k)        |
        [runs ALL steps of stage k]                            |
             |                                                 |
             v                                                 |
   per Adam step: _compose_loss_terms -> _non_data_terms       |
   sets controller._last_widened_details["w_n_stats"]          |
   (w_min/w_mean/w_max/front_idx) + residuals_per_bin           |
             |                                                 |
             v                                                 |
   guard_hook(controller, loss_terms, grad_norm, step, k, "2a")|
             |                                                 |
   StepGuards.check(..., w_n_stats=controller._last_widened_   |
   details["w_n_stats"], N_colloc=len(residuals_per_bin))      |
             |                                                 |
   +----------------------------+                              |
   | invariant A: w_min<=0 or   |--HALT--> write_failure_bundle |
   | non-finite -> HALT         |          + preflight/register |
   | invariant B: front stalled |          projected into       |
   | > N steps -> HALT          |          summary.json         |
   | (record-only if N unset,   |                                |
   |  D-20)                     |                                |
   +----------------------------+                                |
             |  no trip                                          |
             v                                                   |
   disposition ADVANCE -> self._stage = k+1, stage_factory       |
   rebind (if any) -> D-05 site 2: re-assert D-01 table for      |
   the ENTERED stage's rebound ScheduledWeights ------------------+
             |
             v
        finish_run("finished"/"failed", ...) -> finalize_summary()
        summary.py projects preflight.json verbatim as
        "conformance" + eval01_precondition_i (D-27/D-28)
```

### Recommended Project Structure

```
pinn/
├── conformance/                # NEW — D-32 named module boundary
│   ├── __init__.py
│   ├── table.py                # GATE-01: D-01 table + assertion (name discretionary)
│   ├── census.py                # GATE-02: D-07..D-11 manifest + resolution
│   ├── register.py              # INST-03: divergence_register.json load/validate
│   └── preflight.py             # composes the three above into preflight.json (D-27)
├── constants.py                 # + the D-01 locked table (D-02)
├── train.py                     # + 2 call sites, guard_hook extended
├── training/
│   ├── guards.py                # + 2 HALT guards + causal_stats_missing
│   ├── controllers.py           # + 2 call sites in CurriculumController.step()
│   ├── config.py                # + InvariantsConfig
│   ├── config_yaml.py           # + InvariantsConfig registered
│   └── summary.py               # + conformance block + eval01_precondition_i
tests/
└── phase49/                     # NEW — D-29 dataset-free fixtures + synthetic e2e seam
```

### Pattern 1: `guard_hook` already has `w_n_stats` and `N_colloc` for free

**What:** `RunController._non_data_terms` sets `self._last_widened_details["w_n_stats"]`
(a dict with `w_min`/`w_mean`/`w_max`/`front_idx`) and `self._last_widened_details["residuals_per_bin"]`
(a list the same length as the causal weight vector `w_n`) every time it runs — and
`_compose_loss_terms` (which calls `_non_data_terms`) runs **before** `guard_hook`
is invoked, on every Adam step ("2a" phase, the only phase Stage-0 reaches).

**Verbatim evidence:**
- `pinn/training/controllers.py:684-692` (inside `_non_data_terms`):
  ```python
  self._last_widened_details = {
      "w_n_stats": {
          "w_min": float(w_n.min()),
          "w_mean": float(w_n.mean()),
          "w_max": float(w_n.max()),
          "front_idx": max(
              [n for n, w in enumerate(w_n_list) if w > 0.5], default=-1,
          ),
      },
      "residuals_per_bin": [float(r) for r in rbar_det.tolist()],
      ...
  }
  ```
- `pinn/training/controllers.py:711-725` (`_compose_loss_terms`, called from the guarded path at `controllers.py:1047` **before** `guard_hook` at `controllers.py:1074`):
  ```python
  def _compose_loss_terms(self, batch, anchor_ctx: _AnchorContext, weights) -> LossTerms:
      data_term = self._data_term(batch.data_points)
      others = self._non_data_terms(anchor_ctx)
      terms = {"data": data_term, **others}
      return compose_total(terms, weights)
  ```
- `pinn/training/controllers.py:1074-1076` (the guard_hook call — `self` IS the `RunController`):
  ```python
  guard_outcome = self._guard_hook(
      self, loss_terms, grad_norm, self._global_step, k, "2a",
  )
  ```
- `pinn/train.py:997-1004` (the `guard_hook` signature in `main()`, first param is literally the `RunController`):
  ```python
  def guard_hook(
      controller: RunController,
      loss_terms: Any,
      grad_norm: Any,
      global_step: int,
      stage: int,
      phase: str,
  ) -> Any:
  ```

**How to use it (no new threading needed):** inside `guard_hook`, read
`getattr(controller, "_last_widened_details", None)` — the exact same access
pattern the existing `checkpoint_hook` already uses for a different private
attribute: `pinn/train.py:961` `val = getattr(controller, "_last_val_total", None)`.
`N_colloc` (D-14: "the length of the step's own `w_n` vector, read per step, never
a constant") is `len(controller._last_widened_details["residuals_per_bin"])` —
`residuals_per_bin` is `rbar_det.tolist()` and `rbar`/`w_n` share length in
`causal_physics_loss`, so this list's length equals `len(w_n)` for that step,
with no new field required on `_last_widened_details`.

**When absent (D-16 `causal_stats_missing`):** `_last_widened_details` starts
as `None` (`controllers.py:473`, `self._last_widened_details: Optional[dict] = None`)
and is only populated after the first `_non_data_terms` call. On any step
where the physics term was evaluated (i.e. every Stage-0 "2a" step reaching
`guard_hook`), it will be populated by the time `guard_hook` runs (per the
ordering proof above) — so `None`/missing `w_n_stats` at that call site is
itself the D-16 HALT signal, not a normal transient state.

### Pattern 2: the D-04 exact-equality discipline (`run_metadata.py`)

**What:** `_validate_causal_clip_facts` in `pinn/training/run_metadata.py:136-216`
is the worked example D-04/D-22 must reuse: type-check → exact key-set check →
**exact equality** (`!=`, never `math.isclose`) against a canonically derived
value, with every failure raising `ValueError` naming what to do
("regenerate … via fresh setup").

**When to use:** the D-01 table assertion (each `k∈{2,3,4}` entry must equal
`10.0 ** (k - 4)` exactly) and the register's own self-defense (D-25: closed
entries must cite a real, currently-passing test).

**Example (paraphrased shape, not literal code to copy):**
```python
# pinn/training/run_metadata.py:207-213 — the pattern to mirror
for name in ("causal_clip_exponent_floor",):
    if float(facts[name]) != float(canonical[name]):
        raise ValueError(
            f"{context} {name} does not match the canonical runtime-derived "
            f"value; got {facts[name]!r}; regenerate run metadata via fresh setup"
        )
```

### Pattern 3: the D-27 verbatim-passthrough discipline (`summary.py`)

**What:** `_GATE_KEYS` (`pinn/training/summary.py:67-76`) + `_eval01_precondition_iii`
(`summary.py:254-313`) show exactly how to project persisted bytes into
`summary.json`/`summary.md` without recomputing or null-collapsing them — the
comment at `summary.py:65-66` states the rule directly: *"Persisted-bytes
passthrough: never recomputed, never null-collapsed (D-20)"* (that D-20 is
Phase 46's, a different D-20 than this phase's D-20 — do not conflate).

**Concrete extension point:** `_compose` (`summary.py:408-449`) builds the
payload dict; add a `"conformance": <verbatim preflight.json bytes or None>`
key and an `"eval01_precondition_i": bool` key here, following the exact
shape of the existing `"validation": _validation_summary(...)` line at
`summary.py:440`. `_render_md` (`summary.py:452-545`) needs a parallel new
section, following the `## Validation summary` block's shape
(`summary.py:485-498`) — read the file directly rather than recompute
(`preflight.json` either exists with the run's own conformance record, or is
absent because the run refused before D-05 site 1 ever wrote it — the latter
is a genuine `None`, not a fabricated value, consistent with the module's
CTX-67 null policy stated at `summary.py:10-14`).

### Anti-Patterns to Avoid

- **Reading `ScheduledWeights.current(epoch)` to get the caps:** returns the
  *ramped* value (`lambda_phys_max * ramp`), which is `0` at epoch 0
  regardless of the cap. See Common Pitfall 1.
- **A second per-step guard mechanism:** D-15 forbids this explicitly; extend
  `_GUARD_ORDER`/`_HALT_FAMILY` in `guards.py` instead.
- **Hard-coding the register schema inline in `preflight.py`:** follow
  `run_metadata.py`'s `schema_version` + frozenset-of-keys + re-validate-on-load
  shape instead of inventing a new validation idiom.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Atomic JSON artifact write | A raw `open().write()` | `pinn.training.atomic_io.atomic_write_text` (already imported by `run_metadata.py`, `guards.py`, `summary.py`) | Every existing artifact in this codebase uses it; a raw write risks a partial file on crash |
| Per-step disposition/failure-bundle plumbing | A parallel guard loop | `pinn.training.guards.StepGuards` + `write_failure_bundle` | D-15 mandates reuse; `GuardOutcome`/`_GUARD_ORDER`/`_HALT_FAMILY` already exist |
| "Is this field provisional" bookkeeping | A second provisional registry | `TrainingConfig.provisional_fields()` (cross-check only, per D-09 — do not adopt its verdict) | Already exists, already wired into `_log_run_start` |
| Config schema validation | Hand-rolled dict key checks | `pinn.training.config_yaml._map_section`'s unknown-key-raises pattern, plus the new dataclass's own `__post_init__` | Existing recursive dotted-path `ConfigKeyError` already covers nested sections — but only if the new dataclass is registered (Common Pitfall 3) |

**Key insight:** every mechanism GATE-01/02/03/INST-03 needs already exists in
this codebase in a slightly different shape (guards, config, artifacts,
summary projection). The engineering risk in this phase is almost entirely in
wiring precision (exact insertion points, exact signatures), not in designing
new machinery.

## Census Population Map (GATE-02 / D-08 / D-09)

Every D-08 quantity resolves to a real code path. **No quantity was
unlocatable.**

| Term | Quantity | Current source | Resolution class |
|------|----------|-----------------|-------------------|
| `L_data` | predicted positions | model forward pass, `controllers.py:621` | derived |
| `L_data` | target positions (`pre.r_gauge`) | `pinn/data/adapter.py` (post-CONF-09 residency) | pipeline |
| `L_data` | `HUBER_DELTA_DATA` | `pinn/constants.py:55` (`= 1.0`) | spec-constant |
| `L_data` | `λ_data` | `ScheduledWeights.current()` fixed at `1.0`, `scheduled_weights.py:207` | spec-constant |
| `L_IC` | `true_r0`/`true_v0` | `controllers.py:581-582` (`_build_anchor_context`) | derived |
| `L_IC` | `IC₁₃` | `record.ic13`, `controllers.py:566-567` | pipeline |
| `L_IC` | `β_v` | `pinn/loss_catalog.py:265` — **function-default parameter `beta_v=1.0`, NOT a `pinn/constants.py` entry** | spec-constant (house-style deviation — flag, not block; see below) |
| `L_IC` | `λ_IC` | `ScheduledWeights._lambda_ic`, default `1.0`, `scheduled_weights.py:98/136` | spec-constant, tier **advisory** (D-03) |
| `L_phys^causal` | `masses_ordered` | `pre.masses_ordered`, `pinn/data/adapter.py:865` (per D-08's own citation) | pipeline |
| `L_phys^causal` | `EPS_SOFT` | `pinn/constants.py:39` (`= 1e-5`) | spec-constant |
| `L_phys^causal` | `η_c` (`CAUSAL_ETA_C`) | `pinn/constants.py:71` (`= 1.0`) | spec-constant |
| `L_phys^causal` | causal-clip facts (5 fields) | `resolve_causal_clip_facts`, `pinn/loss_catalog.py:77-115`; persisted `training_metadata.json` | derived |
| `L_phys^causal` | `D_CHARACTERISTIC_LENGTH` | `pinn/constants.py:24` | spec-constant |
| `L_phys^causal` | `T_CHARACTERISTIC_TIME` | `pinn/constants.py:31` (`= 10.0`) | spec-constant |
| `L_phys^causal` | `R̄` reduction | `controllers.py:653` (`(residual ** 2).sum(dim=(-2,-1)) / 3.0`) — CONF-04-conformant, TEST-02-covered | derived |
| `L_phys^causal` | collocation set | `CollocationSampler(collocation_count=16, ...)`, `train.py:919-922` — `16` is hard-coded, not config-resolved (already a named D-24 register entry, not a census blocker per D-11) | pipeline |
| `L_E` | `S_H` | `compute_s_h`, `run_metadata.py:73-99`; persisted `training_metadata.json` | pipeline |
| `L_E` | `ε_H = 1e-4·S_H` | `write_training_metadata`, `run_metadata.py:254` (`"eps_h": factor * s_h`) | derived |
| `L_E` | `energy_floor_factor` | `config.stage.energy_floor_factor`, default `1e-4`, `config.py:409` — **also registered in `provisional_fields()` at `config.py:161`: `("stage.energy_floor_factor", 1e-4, "ctl_instruction.md CURR-03 ε_H=1e-4·S_H (CTX-38)")`** | spec-constant/config — D-09 disagreement case, record don't adopt |
| `L_E` | per-anchor `h0` | `controllers.py:584-588` | derived |
| `L_E` | `HUBER_DELTA_ENERGY` | `pinn/constants.py:58` (`= 1.0`) | spec-constant |
| `L_L` | `l0` | `controllers.py:590-592` | derived |
| `L_L` | `EPS_L` | `pinn/constants.py:68` (`= 1e-8`) | spec-constant |
| `L_L` | `HUBER_DELTA_ANGMOM` | `pinn/constants.py:61` (`= 1.0`) | spec-constant |
| Schedule | `N_Adam,k` | `config.stage.n_adam`, CTX-39 required int, `config.py:382` | pipeline (config-required, enforced via `ConfigRequiredError`) |
| Schedule | `I_warm` | `ScheduledWeights.warmup_length` property, `scheduled_weights.py:172-175` | derived |
| Schedule | D-01 table | **new**, `pinn/constants.py` per D-02 | spec-constant (this phase creates it) |

**Two flagged findings (both non-blocking, both anticipated by D-09/D-11):**
1. `β_v` (`pinn/loss_catalog.py:265`) does not live in `pinn/constants.py`
   like every other spec-cited numeric — it is a bare Python default
   parameter. It still resolves to a real, spec-correct value (`1.0`); the
   census should record this as a house-style disagreement, not a
   placeholder, per D-09's "report disagreement, don't adopt the verdict"
   discipline.
2. `stage.energy_floor_factor` is simultaneously §3.4-locked (per D-08) and
   `provisional_fields()`-registered (`config.py:161`) — this is **exactly**
   the D-09 disagreement case CONTEXT.md already names by name
   ("`stage.energy_floor_factor` is registered provisional yet `1e-4` is
   locked by §3.4"). Confirmed verbatim in this session, not assumed.

### D-10 Verification — STEP_LOG_FIELDS field count and contents

**Verified this session** by parsing the AST of `pinn/training/step_log.py`'s
`STEP_LOG_FIELDS` dict (not a grep — the literal dict was walked and every
key printed):

```
count = 37
```

All ten `grad_norm_raw_*`/`grad_norm_applied_*` fields are present
(`grad_norm_raw_data`, `grad_norm_raw_ic`, `grad_norm_raw_phys`,
`grad_norm_raw_energy`, `grad_norm_raw_angmom`, `grad_norm_applied_data`,
`grad_norm_applied_ic`, `grad_norm_applied_phys`, `grad_norm_applied_energy`,
`grad_norm_applied_angmom`), plus `grad_stats_complete`
(`pinn/training/step_log.py:235-241`), plus `w_min`/`w_mean`/`w_max`/`front_idx`
(`step_log.py:242-269`). **D-10's claim ("37 fields") is confirmed exactly as
stated** — `[VERIFIED: pinn/training/step_log.py:33-306, AST-walked this
session]`. GATE-02's D-10 instrumentation-precondition check can therefore
assert against the already-existing registry; no new step-log field is
required for this sub-check (the census only needs to confirm these 15 names
are present in `STEP_LOG_FIELDS`, which they are).

## D-17 Verdict: the checkpoint-schema-bump route is CHEAP, not costly

**Verdict: use the D-17-preferred route (serialize invariant-B state into the
checkpoint payload, bump `CHECKPOINT_SCHEMA_VERSION`).** The fallback
(re-arm-and-record) is not needed — the evidence does not support "the schema
bump ripples too far."

**Evidence, exhaustive (grep across `pinn/` and `tests/` for every
`CHECKPOINT_SCHEMA_VERSION` reference):**

1. **The constant itself.** `pinn/training/checkpoint.py:32`:
   `CHECKPOINT_SCHEMA_VERSION: int = 1`. One line to bump to `2`.

2. **The resume validator.** `pinn/training/checkpoint.py:158-171`
   (`_is_structurally_valid`) does `if payload.get("schema_version") !=
   CHECKPOINT_SCHEMA_VERSION: return False` — this is a **dynamic** reference
   to the module-level symbol. **No code change required here**; it
   automatically tracks the bumped value.

3. **Every consumer that constructs a checkpoint payload dict references the
   symbol, never a literal.** Confirmed by grep across `pinn/train.py` (5
   call sites), `pinn/training/controllers.py` (`build_checkpoint_payload`,
   1 call site, plus 1 more inside `CurriculumController`), and every test
   file that builds a CTX-53 payload (`tests/phase41/test_train_entrypoint.py:510,543`,
   `tests/phase41/test_controllers_ext.py:28,203,211,221,229-231,415,451,475,539,617,766`,
   `tests/phase41/test_checkpoint.py:42`). **Zero of these need editing** —
   they import `CHECKPOINT_SCHEMA_VERSION` and re-use it symbolically.
   `tests/phase41/test_controllers_ext.py:229-231` even asserts controllers.py
   does NOT locally redefine the constant — this assertion is
   value-independent and stays green regardless of the bump.

4. **Two literal `"schema_version": 1` hits exist in the test suite — neither
   is affected:**
   - `tests/phase48/test_clip_metadata.py:101` — this is
     `TRAINING_METADATA_SCHEMA_VERSION` (a *different* schema, currently `2`,
     `run_metadata.py:57`), deliberately mutated to the old value `1` to test
     rejection of stale `training_metadata.json`. Unrelated to
     `CHECKPOINT_SCHEMA_VERSION`.
   - `tests/phase43/test_evaluate_gate.py:95` — writes a raw
     `torch.save({"model": ..., "schema_version": 1}, ...)` checkpoint
     fixture, but `pinn/evaluate.py:392-399` (`evaluate_run`'s checkpoint
     load) does `payload = torch.load(checkpoint_path, weights_only=True)`
     then `model.load_state_dict(payload["model"])` directly — **it never
     checks `schema_version` at all** (`_is_structurally_valid` is a
     `checkpoint.py`-internal function used only by the resume/rollback/
     fallback-scan paths, not by `evaluate.py`). This fixture is unaffected
     by a bump.

5. **No static/committed checkpoint fixture files exist.** `find tests
   -iname "*.pt"` returned nothing; no `runs/` directory is tracked in git.
   Every test-constructed payload is built at test-run time referencing the
   live symbol. There is nothing to regenerate.

**What the bump actually requires (additive, not migratory):**
- `build_checkpoint_payload` (`controllers.py:342-371`) gains one new dict
  key (e.g. `"invariant_b_state": {...}`) — additive, does not need to be in
  `_CTX53_REQUIRED_KEYS` (`checkpoint.py:35-43`) unless the plan wants it
  required; if optional, existing callers need no change at all.
- The invariant-B state (`F`, `last_advance_step`, per D-14) is natural to
  own on the `StepGuards` instance itself (`step_guards = StepGuards(config,
  disk_root=run_dir)`, `train.py:912` — constructed once, alive for the whole
  run including across stage boundaries, since it is a `main()`-local
  closure variable, not reconstructed per stage).
- A restore path mirroring `_restore_run_controller`
  (`pinn/train.py:641-648`) is needed for the resume branch
  (`train.py:1093-1119`), reading the new payload key back into
  `step_guards`.
- `CurriculumController` does not currently hold a reference to
  `step_guards` — threading it in (or the invariant-B state alone) needs one
  new keyword-only constructor parameter, following the exact pattern
  `stage_factory`/`forced_disposition` already use
  (`controllers.py:1587-1598`, all keyword-only with `None` defaults).

**Cost tally:** 1 constant change + 1 additive payload key + 1 new restore
function + 1 new optional constructor parameter. Zero fixture regenerations.
This directly contradicts the CONTEXT.md "costly" pre-assessment — the
research resolves the open question the CONTEXT explicitly delegated to it.

## Common Pitfalls

### Pitfall 1: `ScheduledWeights.current(epoch)` does not give you the caps

**What goes wrong:** Calling `scheduled_weights.current(0)` to "read" the
per-stage λ caps returns `LossWeights(lambda_phys=lambda_phys_max * ramp,
...)` where `ramp = min(1, epoch/I_warm)`. At `epoch=0`, `ramp=0`, so
`lambda_phys`/`lambda_e`/`lambda_l` are **all `0.0` regardless of the actual
cap** (`scheduled_weights.py:191-212`).

**Why it happens:** `ScheduledWeights` intentionally separates the ramped
per-step weight (`current()`) from the per-stage ceiling
(`_lambda_phys_max`/`_lambda_e_max`/`_lambda_l_max`/`_lambda_ic`) — but only
`warmup_length` and `n_adam_k` are exposed as `@property`
(`scheduled_weights.py:172-180`). The three caps and `lambda_ic` are
underscore-prefixed instance attributes with **no public accessor**.

**How to avoid:** read `scheduled_weights.state_dict()`
(`scheduled_weights.py:246-258`), which returns a plain dict including
`lambda_phys_max`, `lambda_e_max`, `lambda_l_max`, `lambda_ic`,
`warmup_length`, `n_adam_k` — this is the only public surface that exposes
the caps.

**Warning signs:** a table assertion that always fails (comparing `0.0`
against a locked non-zero value) or, worse, always passes because the
assertion was written against `k=0`'s all-zero row and never caught the
error.

### Pitfall 2: `guard_hook`'s "2b" (L-BFGS) call site is unreachable in v2.2 scope, but is code-present

**What goes wrong:** a plan or test author could assume `guard_hook`'s second
call site (`controllers.py:1306-1308`, `phase="2b"`) needs the same invariant
wiring effort as the "2a" site.

**Why it happens:** `guard_hook` genuinely has two call sites in
`controllers.py` (Adam "2a" at line 1074, L-BFGS "2b" at line 1306).

**How to avoid:** `check_stage_preflight` (`pinn/training/slbfgs_preflight.py:38-49`)
refuses any `stage >= 3` before it is ever entered, and stages 3-6 are the
only stages that reach the L-BFGS/"2b" path. Under SCOPE-27 (Stage-0-only
v2.2), "2b" is unreachable code this milestone. The plan should wire
invariants primarily through the "2a" path and may choose to thread
`w_n_stats` through "2b" too for completeness (cheap, since the same
`_last_widened_details` mechanism populates there as well via the closure
that calls `_compose_loss_terms` internally), but no test needs to actually
exercise "2b" to satisfy D-16 for this milestone.

### Pitfall 3: registering a new `RunConfig` nested section requires TWO edits, not one

**What goes wrong:** adding `invariants: InvariantsConfig =
field(default_factory=InvariantsConfig)` to `RunConfig` in `config.py` alone
is not enough — a YAML `run: invariants: {...}` block will not parse
correctly.

**Why it happens:** `pinn/training/config_yaml.py`'s `_resolve_nested_cls`
(`config_yaml.py:86-117`) resolves `from __future__ import annotations`
string type-annotations against a **fixed, hand-maintained** `known` dict
(`config_yaml.py:103-111`, currently `{"GuardConfig": GuardConfig,
"CheckpointCadence": CheckpointCadence, "MonitorConfig": MonitorConfig,
"RunConfig": RunConfig, "StageConfig": StageConfig, "OptConfig": OptConfig,
"LossConfig": LossConfig}`). A new nested dataclass not added to this dict is
invisible to the YAML mapper — `_map_section` would pass the raw parsed dict
straight through as the field value instead of constructing an
`InvariantsConfig` instance, and `RunConfig.__post_init__`'s isinstance check
(pattern at `config.py:360-373` for `guards`/`checkpoint`/`monitor`) would
then raise a confusing `TypeError` naming a `dict`, not the intended
`ConfigKeyError`.

**How to avoid:** two edits in lockstep — (1) `config.py`: define
`InvariantsConfig`, add the field to `RunConfig`, add an isinstance check in
`RunConfig.__post_init__` mirroring the three existing ones; (2)
`config_yaml.py`: import `InvariantsConfig` (line ~27-37) and add
`"InvariantsConfig": InvariantsConfig` to the `known` dict (line ~103-111).

**Warning signs:** a config that YAML-parses without a `ConfigKeyError` but
then explodes with an unrelated `TypeError` deep inside `RunConfig`
construction, or (worse) silently constructs a `RunConfig` whose
`.invariants` attribute is a plain dict that later code assumes has a
`.front_advance_window_n` attribute.

### Pitfall 4: D-20's "no default" must not be implemented via `ConfigRequiredError`

**What goes wrong:** the established CTX-39 pattern for "config-required, no
default" fields (`StageConfig.max_epochs` etc., `config.py:381-395,
411-428`) uses `_require_int`, which **raises `ConfigRequiredError` when the
value is `None`**. D-20 explicitly wants the opposite: `None`/absent is a
**defined, non-erroring, fail-open-to-record-only** state.

**Why it happens:** `_require_int`/`_require_float` are the only "optional
scalar" helpers currently in `config.py` with obvious names, and they are
error-on-None by design (that is their whole point for `max_epochs` etc.).

**How to avoid:** model `front_advance_window_n` on `RunConfig.run_name:
Optional[str] = None` (`config.py:329`) instead — a field that is genuinely
optional with no validation-on-None, validated only for type/positivity
**when present**. Do not route it through `_require_int`.

## Code Examples

### GATE-01 table assertion — reading the live ScheduledWeights correctly

```python
# CORRECT — reads the caps via state_dict() (scheduled_weights.py:246-258)
sd = scheduled_weights.state_dict()
live_caps = {
    "lambda_phys_max": sd["lambda_phys_max"],
    "lambda_e_max": sd["lambda_e_max"],
    "lambda_l_max": sd["lambda_l_max"],
    "lambda_ic": sd["lambda_ic"],
}

# WRONG — do not do this (see Common Pitfall 1)
# live_caps = scheduled_weights.current(0)  # gives ramped values, not caps
```

### D-05 site 1 — recommended insertion point in `pinn/train.py`

The literal constraint (D-05): "after the S_H/`training_metadata`
establishment block and after `ScheduledWeights` construction, and before
`CurriculumController` construction." Both conditions are first satisfied at
`train.py:917` (end of the `ScheduledWeights(...)` call) and the constraint's
upper bound is `train.py:1121` (`curriculum = CurriculumController(`).
Anywhere in `[918, 1121)` is D-05-compliant. **Recommended:** insert
immediately after line 917 / before line 918 (`grad_clipper = GradClipper()`)
— this is the earliest legal point, needs no resume-branch state, and keeps
the call adjacent to the objects it reads (`config`, `scheduled_weights`,
plus `s_h`/`causal_clip_facts`/`energy_floor_factor` already bound in local
scope from the block at `train.py:873-909`). A refusal here must write
`preflight.json` (with the failing assertion recorded) **before** returning
`finish_run("failed", 1)`, following the exact `except ValueError as exc:
print(...); return finish_run("failed", 1)` shape already used seven times
in `main()` (e.g. `train.py:902-907`).

### D-05 site 2 — exact two sub-sites in `CurriculumController.step()`

```python
# pinn/training/controllers.py:1770-1771 — TOP-OF-STEP site
check_stage_preflight(self._stage)
# <-- INSERT HERE: assert D-01 table for self._stage against
#     self._scheduled_weights.state_dict(); covers the initial/resumed stage
#     because CurriculumController.run() calls step() in a `while True` loop
#     (controllers.py:1897-1900) on every dispatch.
disposition = self._get_disposition(self._stage)
```

```python
# pinn/training/controllers.py:1779-1795 — ADVANCE branch, after rebinding
self._stage = k + 1
if self._stage_factory is not None:
    previous_model = self._run_controller.model
    new_controller = self._stage_factory(self._stage)
    if new_controller.model is not previous_model:
        raise StageFactoryModelMismatch()
    if self._run_controller is not None:
        self._run_controller._optimizer = None
    self._run_controller = new_controller
    self._scheduled_weights = new_controller.scheduled_weights
# <-- INSERT HERE (after line 1795, before line 1796): assert D-01 table for
#     the ENTERED stage (self._stage) against self._scheduled_weights — this
#     is the rebound instance if stage_factory fired, else the same instance
#     (PLAT-01 single-stage path, D-06: Stage 2 correctly fails here because
#     no factory means the un-rebound scheduler still carries Stage-0/1's
#     lambda_e_max=0 while the table demands 1e-2).
```

Both sites need access to a place to write the `stage_boundary` record into
`preflight.json` (D-27). `CurriculumController` currently holds no `run_dir`
or filesystem-writing capability — it only holds `config`, `checkpoint_store`,
`scheduled_weights`, `run_controller` (`controllers.py:1619-1627`).
**Recommended pattern:** add a new optional keyword-only constructor
parameter (e.g. `conformance_hook: Optional[Callable[[int], None]] = None`),
following the exact precedent of `stage_factory`/`forced_disposition`
(`controllers.py:1587-1598`, both keyword-only, both default `None`) — this
mirrors the `guard_hook`/`checkpoint_hook` injection pattern `train.py`
already uses for `RunController`, keeping `CurriculumController` decoupled
from filesystem paths (consistent with D-32's module-boundary goal).

### D-17 checkpoint payload — additive key, no signature break

```python
# pinn/training/controllers.py:342-371 — build_checkpoint_payload, additive change
def build_checkpoint_payload(
    controller: "RunController",
    curriculum_state: Any,
    config_identity: Any,
    schema_version: Any,
    invariant_b_state: Optional[Mapping[str, Any]] = None,  # NEW, optional
) -> dict[str, Any]:
    sd = controller.state_dict()
    return {
        "model": sd["model"],
        "optimizer": sd.get("optimizer"),
        "scheduled_weights": sd["scheduled_weights"],
        "grad_clip": sd["clipper"],
        "curriculum": curriculum_state,
        "rng": sd.get("rng"),
        "counters": sd.get("counters"),
        "config_identity": config_identity,
        "schema_version": schema_version,
        "invariant_b_state": invariant_b_state,  # NEW — additive key
    }
```

Existing 6 call sites (`train.py:957,993,1058,1158`; `controllers.py:1694`
via `_checkpoint_payload`) need no change if the new parameter defaults to
`None` — only the sites that need to persist live invariant-B state pass it
explicitly.

## Runtime State Inventory

Not applicable — Phase 49 is not a rename/refactor/migration phase. It is
additive (new module, new artifact, new guard families, new config section).
No existing runtime state (stored data, live service config, OS-registered
state, secrets, build artifacts) is renamed or relocated.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|----------------|
| A1 | Module/function names inside `pinn/conformance/` (`table.py`, `census.py`, `register.py`, `preflight.py`) are illustrative suggestions, not locked names — CONTEXT.md's "Claude's Discretion" explicitly grants "module and symbol names inside `pinn/conformance/`" | Standard Stack, Recommended Project Structure | None — explicitly discretionary per CONTEXT.md, not an assumption about an unverified fact |
| A2 | `invariant_b_state` and `conformance_hook` are illustrative names for the new checkpoint-payload key and `CurriculumController` constructor parameter — also explicit Claude's Discretion ("the exact `preflight.json` and register JSON field names… how the D-17 invariant-B state is threaded… the precise `StepGuards` integration signature") | D-17 Verdict, Code Examples | None — explicitly discretionary |

**No claim in this research required user confirmation.** Every quantity,
line citation, and code-shape claim above was verified by reading the actual
file this session (`Read` tool, not grep-only, not training-data recall). The
one place a genuine open decision exists — the numeric value of `N` for
invariant B — is explicitly out of scope for this research per the hard
constraints and is not treated as an assumption; it is D-18's owner
checkpoint, addressed in `## Open Questions For The Owner` only to confirm
this research does not attempt to resolve it.

## Open Questions For The Owner

**None generated by this research session.** Every research question in the
brief resolved to a concrete, file-grounded answer without hitting a
source-silent gap. `N` for invariant B remains the pre-existing D-18 owner
checkpoint (unchanged by this research — the mechanism this research
describes is fully N-agnostic per D-20, exactly as CONTEXT.md requires).

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.1.1 over the repository's existing unittest-/pytest-style modules `[VERIFIED: .venv/bin/python -m pytest --version, this session]` |
| Config file | none dedicated — run from repo root with explicit paths and `-q` (same as Phase 48) |
| Quick run command | `.venv/bin/python -m pytest -q tests/phase49` |
| Full suite command | `.venv/bin/python -m pytest -q tests/phase38 tests/phase40 tests/phase41 tests/phase42 tests/phase46 tests/phase47 tests/phase48 tests/phase49` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|--------------------|--------------|
| GATE-01 | Table assertion PASSES for a conformant Stage-0 `ScheduledWeights` | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate01_table.py -k pass` | ❌ Wave 0 |
| GATE-01 | Table assertion **TRIPS** (fails loud) for Stage-2 (no `stage_factory`, D-06's deliberate refusal) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate01_table.py -k stage2_fails` | ❌ Wave 0 |
| GATE-01 | Table assertion fires at both D-05 sites in a synthetic multi-step run | integration (e2e seam, D-30) | `.venv/bin/python -m pytest -q tests/phase49/test_e2e_seam.py -k table` | ❌ Wave 0 |
| GATE-02 | Census PASSES when every D-08 quantity resolves | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate02_census.py -k pass` | ❌ Wave 0 |
| GATE-02 | Census **BLOCKS** on an injected class-4 placeholder with no waiver | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate02_census.py -k placeholder_blocks` | ❌ Wave 0 |
| GATE-02 | Census records (not adopts) a `provisional_fields()` disagreement | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate02_census.py -k disagreement` | ❌ Wave 0 |
| GATE-03 | Invariant A **TRIPS HALT** on `w_min <= 0` / non-finite `w_n` | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k invariant_a_trips` | ❌ Wave 0 |
| GATE-03 | Invariant A's `front_idx == -1` sentinel is treated as a hard failure (D-13) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k front_idx_sentinel` | ❌ Wave 0 |
| GATE-03 | Invariant B **TRIPS HALT** when the front stalls beyond a configured `N` | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k invariant_b_trips` | ❌ Wave 0 |
| GATE-03 | Invariant B runs **record-only** (no HALT) when `N` is unset (D-20) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k n_unset_record_only` | ❌ Wave 0 |
| GATE-03 | `causal_stats_missing` **TRIPS HALT** when `w_n_stats` is absent on an evaluated-physics step (D-16) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k stats_missing_trips` | ❌ Wave 0 |
| GATE-03 | Invariant-B state survives a resume via the checkpoint payload (D-17) | integration | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_resume.py` | ❌ Wave 0 |
| INST-03 | Register loads/validates with fail-closed schema checking (D-22) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k schema` | ❌ Wave 0 |
| INST-03 | Every `status: closed` entry's cited `proof_test` actually currently passes (D-25) | integration/meta | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k proof_tests_pass` | ❌ Wave 0 |
| INST-03 | Open entries surface into `preflight.json` and `summary.json`'s `conformance` block (D-27) | integration | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k surfaces_in_run_record` | ❌ Wave 0 |
| INST-03 | No `gate_*` key collision — every new field is `conformance_*`/`preflight_*` (D-28) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k no_gate_collision` | ❌ Wave 0 |
| SCOPE-32 | Charter-landed-deliverable re-check documented with a date (D-31) | manual/operational | N/A — a planner-time check re-run, not a runtime test | — |

### Sampling Rate

- **Per task commit:** the directly named `tests/phase49/*.py` file plus the
  closest impacted existing module (e.g. `tests/phase41/test_guards.py` when
  `guards.py` changes, `tests/phase40/test_config.py` when `config.py`
  changes).
- **Per wave merge:** `.venv/bin/python -m pytest -q tests/phase38 tests/phase40
  tests/phase41 tests/phase42 tests/phase46 tests/phase47 tests/phase48
  tests/phase49` (same set Phase 48 used, plus `tests/phase49`).
- **Phase gate:** full suite green before `/gsd-verify-work`; per D-16, every
  new guard and every new preflight assertion must have a test that drives it
  to **actually trip** — a green suite with an untested failure branch does
  not satisfy this phase's own D-16 discipline (the Phase-39 lesson the
  CONTEXT itself cites).

### Wave 0 Gaps

- [ ] `tests/phase49/__init__.py` — phase package marker
- [ ] `tests/phase49/test_gate01_table.py` — table assertion pass + Stage-2 refusal
- [ ] `tests/phase49/test_gate02_census.py` — census pass + placeholder-blocks + disagreement-recorded
- [ ] `tests/phase49/test_gate03_invariants.py` — invariant A/B trip + record-only + `causal_stats_missing`
- [ ] `tests/phase49/test_gate03_resume.py` — invariant-B checkpoint round-trip
- [ ] `tests/phase49/test_inst03_register.py` — register schema, proof-test-currently-passes, run-record surfacing, no `gate_*` collision
- [ ] `tests/phase49/test_e2e_seam.py` — D-30 synthetic-source, real `main()` ordering, few steps, proving the D-05 ordering constraint by execution
- [ ] `tests/phase49/_fixtures.py` (optional) — dataset-free fixtures, following `tests/phase40/_fixtures.py`'s `_StubSource`/`make_stub_split_sources` shape if the e2e seam test needs a synthetic `data.source: synthetic` path

Framework install: none needed — pytest/torch/numpy already present (same
baseline Phase 48 validated).

## Security Domain

`security_enforcement` is not set in `.planning/config.json` (absent = enabled
per the default), but this phase has no network-facing, authentication, or
external-input surface — it is an internal training-pipeline gate operating
on already-validated local files and in-process state. ASVS categories are
evaluated for relevance, not applied wholesale.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|----------------|---------|-------------------|
| V2 Authentication | No | Single-operator local training run; no auth surface |
| V3 Session Management | No | Not a session-based system |
| V4 Access Control | No | No multi-user access boundary |
| V5 Input Validation | Yes (narrow) | Config/YAML fail-closed validation already exists (`ConfigKeyError`/`ConfigRequiredError`); this phase's `InvariantsConfig` must follow the same fail-closed discipline — type/positivity-checked when present, no silent coercion |
| V6 Cryptography | No | No cryptographic operation in this phase |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|----------------------|
| A conformance check that cannot fail reads as a check that passed (D-16's own named threat) | Repudiation (the run "denies" its own non-conformance) | Every guard/assertion gets a dedicated trip test (D-16); the register defends itself with `proof_test` (D-25) |
| A register entry asserting `closed` while the underlying code regressed | Tampering (of the record, not the code) | D-25: CI runs every cited `proof_test`; a stale `closed` claim is caught by re-running it |
| Path traversal via a malformed `preflight.json`/register path | Tampering | Follow `run_metadata.py`'s pattern: fixed filename under `run_dir`, never a user-supplied path; `atomic_write_text` + re-validate-on-load |

## Sources

### Primary (HIGH confidence — direct file reads this session)

- `pinn/training/guards.py` (full read) — `_GUARD_ORDER`, `_HALT_FAMILY`, `GuardOutcome`, `StepGuards.check` signature
- `pinn/train.py:1-70, 310-355, 635-650, 651-1182` — `main()`, `guard_hook`, `_admitted_data_preflight` precedent, `_restore_run_controller`
- `pinn/training/controllers.py:342-392, 626-730, 1240-1400, 1584-1830, 1873-1900` — `build_checkpoint_payload`, `_non_data_terms`, `_compose_loss_terms`, `CurriculumController.__init__`/`step`/`run`
- `pinn/training/scheduled_weights.py` (full read) — `warmup_length`/`n_adam_k` properties vs. private `_lambda_*_max`/`state_dict()`
- `pinn/training/run_metadata.py` (full read) — atomic-write/re-validate/exact-equality pattern
- `pinn/training/summary.py:1-110, 240-658` — `_GATE_KEYS`, `_eval01_precondition_iii`, `_compose`, `_render_md`
- `pinn/training/step_log.py:1-330` + AST field-count verification — `STEP_LOG_FIELDS` (37 fields confirmed)
- `pinn/training/config.py:1-90, 134-450, 559-700` — `ConfigRequiredError`, `GuardConfig`/`RunConfig`, `provisional_fields()`, `_PROVISIONAL` tuple
- `pinn/training/config_yaml.py:1-200` — `_resolve_nested_cls`, `_map_section`, the `known` dict
- `pinn/training/checkpoint.py:1-200` — `CHECKPOINT_SCHEMA_VERSION`, `_is_structurally_valid`
- `pinn/constants.py` (full read) — house style for spec-cited numerics
- `pinn/loss_catalog.py:1-130` — `CAUSAL_CLIP_FIELD_NAMES`, `beta_v` default, `resolve_causal_clip_facts`
- `pinn/training/slbfgs_preflight.py` (full read) — `check_stage_preflight`
- `pinn/training/stage_exit.py:25-40` — `StageDisposition` enum (three values only)
- `pinn/evaluate.py:380-400` — confirms `evaluate_run` never checks `schema_version`
- `pinn/data/adapter.py:855-870`, `pinn/data/preprocessing.py:180-200` — masses_ordered/residency pairing
- `configs/stage0-example.yaml` (full read) — `run.guards:` sibling shape, `n_adam: 1000`, `lambda_e_max: 0.0`
- `tests/phase40/_fixtures.py` (full read) — dataset-free stub-source fixture convention
- `tests/phase41/test_guards.py:1-100` — guard trip-test convention (`_guard_cfg`, `_make_guards`, `test_X_trips_Y` naming)
- `.planning/phases/48-loss-math-conformance/48-VALIDATION.md` (full read) — exact pytest/`conda run -n pinn-train` command forms
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:633-682` — §4.1 PHYS-05 spec text (context for GATE-01, not a re-adjudication)
- `.planning/phases/49-conformance-gate/49-CONTEXT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md` §Phase 49 / §Conformance discipline, `.planning/STATE.md` — locked decisions and phase position

### Secondary / Tertiary

None used — no web search, no external documentation lookup was needed; this
phase is entirely internal-codebase wiring.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no external library involved; every module read directly
- Architecture: HIGH — every insertion point cited to a specific line range, cross-checked against call-site behavior (e.g. traced `_compose_loss_terms` → `guard_hook` ordering to confirm `w_n_stats` availability)
- Pitfalls: HIGH — each pitfall reproduced from an actual code shape read this session, not inferred

**Research date:** 2026-08-04
**Valid until:** stable — this is internal-codebase research with no external dependency drift risk; re-verify only if Phases 40/41/47/48's files change before Phase 49 executes
