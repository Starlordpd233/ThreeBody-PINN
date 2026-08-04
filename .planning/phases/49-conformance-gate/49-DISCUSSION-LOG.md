# Phase 49: Conformance Gate - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-08-04
**Phase:** 49-conformance-gate
**Mode:** `/gsd-discuss-phase 49 --all` with owner-delegated autonomous selection
("choose the best option for each question by your own judgement, grounded in the
mathematics and physics; no manual approvals except for something truly of very
big scope that needs the owner's own verdict"). Every selection below was made by
the orchestrator against cited grounding, not by the owner — **except** the `N`
threshold, which was deliberately left to the owner (see the final section).
**Areas discussed:** PHYS-05 lock granularity and assertion surface; placeholder
census population and verdict semantics; runtime-invariant mechanism and
disposition; invariant B's operational form; the `N` owner checkpoint; the
divergence register's form, schema and initial contents; run-record surfacing and
the EVAL-01 projection; verification strategy and the no-run boundary; the
SCOPE-32 coordination decision.

---

## PHYS-05 lock granularity — which rows does preflight assert?

| Option | Description | Selected |
|--------|-------------|----------|
| Assert `λ_E^max` / `λ_L^max` rows only | The two quantities GAP-45-03's C-05 example concerns; leave `λ_phys^max` alone because §4.1 calls it a "default" | |
| Assert all three `λ^max` rows as locked; `λ_data` locked; `λ_IC` advisory | Reads GAP-45-03 consequences 1 and 4 together: overriding *any* per-stage value is a violation, and the "default" prose is the defect | ✓ |
| Assert every λ in §4.1 as locked, including `λ_IC` | Simplest and most uniform | |

**Choice:** middle option (CONTEXT D-01, D-03).
**Notes:** Option 3 was rejected because `λ_IC = 1` sits in §4.1's `where:` list
(line 644), outside the warmup-schedule block GAP-45-03 actually ruled on;
asserting it as locked would extend an owner ruling to a quantity the ruling
never named — a process-artifact-schema call the STOP protocol reserves. Option 1
was rejected because consequence 4 of the ruling explicitly records that the
"default" wording on `λ_phys^max` is *misleading relative to this ruling*, which
only makes sense if the value is locked. The two-tier `locked` / `advisory`
outcome is the honest middle, and it feeds VER-20 item (b) a second worked
instance of the locked-vs-default marking problem.

---

## The stage-boundary assertion under a single-stage build

| Option | Description | Selected |
|--------|-------------|----------|
| Assert only at run start | No stage boundaries exist in a Stage-0-only run, so a boundary hook is dead code | |
| Assert at run start and at every entered stage, and let stage 2 fail | GATE-01's text requires both; the stage-2 failure is correct behavior | ✓ |
| Assert at boundaries and add a `stage_factory` so stage 2 passes | Makes the table satisfiable at every stage | |

**Choice:** middle option (D-05, D-06).
**Notes:** Option 3 is PLAT-01 platform work, blocked by SCOPE-27 — and would
have converted a correct refusal into an invented capability. The arithmetic
matters: with no `stage_factory` the un-rebound scheduler still carries Stage-0's
caps, so stage 1 passes (its locked row is identical) and stage 2 correctly fails
(`λ_E^max(2) = 1e-2 ≠ 0`). Recording that as intended behavior prevents a future
agent from "fixing" it.

---

## Placeholder census — where does the population come from?

| Option | Description | Selected |
|--------|-------------|----------|
| Reuse `TrainingConfig._PROVISIONAL` | A registry with provenance already exists | |
| An explicit, spec-cited manifest; cross-check `_PROVISIONAL` and report disagreement | The manifest's completeness becomes a reviewable artifact | ✓ |
| Reflect over the loss call graph | No manual list to maintain | |

**Choice:** middle option (D-07, D-09).
**Notes:** Option 1 fails on a concrete case: `stage.energy_floor_factor` is
registered provisional, yet `ε_H = 1e-4·S_H` is locked by §3.4 — adopting the
registry's verdict would block a conformant run on a stale tag. Option 3 fails on
the exact class the gate exists to catch: the `S_H` gap was invisible *because*
nothing in the call graph referenced a quantity that did not exist. Only an
explicit enumeration of what must resolve can see an absence. The disagreement
between the two lists is itself reported as a finding.

---

## Does the census cover instrumentation preconditions?

| Option | Description | Selected |
|--------|-------------|----------|
| Loss-consumed quantities only | Matches GATE-02's literal text | |
| Loss-consumed quantities plus the spec-named instrumentation preconditions | Closes charter layer-1 bullet 3 (the C-06 class) at near-zero cost | ✓ |

**Choice:** include, recorded as a deliberate scope call (D-10).
**Notes:** C-06 (gradient statistics never logged) and the `S_H` gap are the same
failure — a spec-required thing that resolved to nothing — and Phase 48 already
built the fields, so the check is an existence assertion over `STEP_LOG_FIELDS`.
Recorded explicitly rather than absorbed silently, since it is not named in the
GATE-01..03 / INST-03 requirement text.

---

## Runtime invariants — where do they live and what do they do on trip?

| Option | Description | Selected |
|--------|-------------|----------|
| Two new HALT-family guards inside the existing `StepGuards` | Inherits ordering, failure bundles, journaling, and the live `guard_hook` | ✓ |
| A separate runtime-invariant subsystem beside `StepGuards` | Cleaner conceptual separation from numerical guards | |
| RECOVER-family, so the run rolls back and retries | Matches the existing NaN/Inf handling | |

**Choice:** first option, HALT family (D-15).
**Notes:** Option 3 is wrong on the physics of the situation, not just on style:
a conformance violation is structural, so rolling back to a checkpoint and
retrying cannot repair it and would convert a loud failure into a quiet loop
under `recover_retries`. Option 2 would be a second per-step guard mechanism —
the exact "do not build a competing mechanism" lesson Phase 48 D-11 recorded for
run-record persistence.

---

## Invariant B — what does "the causal front advances" mean operationally?

| Option | Description | Selected |
|--------|-------------|----------|
| `front_idx` must reach ≥ 1 within `N` steps of run start (one-shot) | Catches v2.0 exactly and is trivially cheap | |
| Instantaneous `front_idx` must strictly increase every `N` steps | The literal reading of "advances within N steps" | |
| High-water mark `F_t = max_{s≤t} front_idx(s)` must increase within `N` steps, with a saturation exemption at `N_colloc − 1` | Catches v2.0, survives saturation, tolerates stochastic bounce | ✓ |

**Choice:** third option (D-14).
**Notes:** Option 2 fires spuriously once the front saturates — at
`front_idx = N_colloc − 1` there is nowhere left to advance — and again on any
transient regression (3 → 2 → 3) that carries no information about a stall.
Option 1 stops protecting the run after the first advance, when a mid-run
collapse is exactly as invalidating. The high-water form is the only one of the
three that is correct at both ends of the run. Recorded arithmetic: with
`η_c = 1` and the code's 0.5 threshold, `front_idx ≥ 1 ⟺ R̄_0 < ln 2 ≈ 0.6931`.
`N_colloc` is read from the step's own weight vector rather than from a constant,
because `collocation_count = 16` is hard-coded at `train.py:920` and is not
config-resolved.

---

## `front_idx = -1`

| Option | Description | Selected |
|--------|-------------|----------|
| Tolerate as a documented sentinel | It exists to avoid raising on an empty sequence | |
| Treat as a hard invariant-A failure | It is arithmetically unreachable in a well-formed run | ✓ |

**Choice:** hard failure (D-13).
**Notes:** `w_0 = exp(0) = 1 > 0.5` always, because the exclusive prefix sum at
`n = 0` is empty. A `-1` therefore means the weight vector is empty or
non-finite. The `default=-1` accessor in `controllers.py` stays as written; the
gate is what gives the value meaning.

---

## `N` for invariant B — the owner checkpoint

| Option | Description | Selected |
|--------|-------------|----------|
| Select a defensible `N` now and mark it revisitable | Unblocks Phase 50 immediately | |
| Leave `N` to the owner; build the mechanism `N`-agnostic; define a fail-closed unset state | Preserves the reservation without stalling the phase | ✓ |
| Leave `N` to the owner and block the phase until it arrives | Strictest reading of "blocking owner checkpoint" | |

**Choice:** middle option (D-18, D-20, D-21). **This is the one item deliberately
NOT decided by the orchestrator.**
**Notes:** `N` is reserved to the owner twice — GAP-45-04's resolution ("N is
deliberately not set here … invariant B is *stated* but not yet *enforceable*")
and the roadmap's owner-checkpoint list — and the charter §6 classifies it with
X and M as a calibration decision "not inventable from first principles". The
delegated-autonomy instruction for this session explicitly carves out decisions
of that class. Option 1 would also be SCOPE-29-shaped: a front-advance window
fitted to what a run is observed to do is a threshold tuned against results.
Option 3 was rejected as unnecessary: D-20 defines the unset state
(`N` absent ⇒ invariant B record-only, an `INV-B-N-UNSET` open divergence, and
`eval01_precondition_i = false`), so a run may proceed but is structurally
ineligible to spend the single look — which is exactly the protection
EVAL-01 precondition (i) exists to give. The checkpoint therefore blocks the
*evaluation*, not the *phase*.

Evidence assembled for the checkpoint, to be presented at planning time (D-19):
the enforced definition of "advance"; the `R̄_0 < ln 2` threshold arithmetic; the
shipped Stage-0 anchors `N_Adam,0 = 1000` ⇒ `I_warm = 100`, `N_colloc = 16`; the
v2.0 observation `front_idx = 0` for 1500/1500 steps in 5/5 runs (non-conformant,
so an upper bound only); the statement that no conformant run has ever executed,
so `N` is a policy about tolerated silence rather than an estimate; and both
failure directions named — too small burns a healthy Phase-50 seed, too large and
the invariant never protects the look.

---

## The known-divergence register — form and location

| Option | Description | Selected |
|--------|-------------|----------|
| Markdown under `docs/work/` | Matches the charter's "pure documentation, no code" framing and the repo docs conventions | |
| Strict JSON at `pinn/conformance/divergence_register.json` with free-text prose fields | Machine-readable for preflight and the run record; one source | ✓ |
| YAML beside `configs/` | Human-friendliest to edit | |

**Choice:** JSON in a new `pinn/conformance/` subpackage (D-22).
**Notes:** the charter gives the register two teeth — "run preflight consults it"
and "any diagnosis phase must read it" — and the first makes it a runtime input,
not a document. A Markdown table would need a parser and would drift from what
preflight actually read. JSON over YAML for parity with every other machine-read
artifact in this codebase (`training_metadata.json` schema v2, `summary.json`
schema v1, the Phase-46 validation sidecars), all of which carry a
`schema_version`, atomic writes, and fail-closed re-validation. Human readability
is served by `rationale` / `what_it_would_take` prose fields plus rendering in
`summary.md` — one source, no second copy to drift.

---

## Register semantics — kinds, waivers, and self-defence

| Option | Description | Selected |
|--------|-------------|----------|
| One flat `divergence` kind with open/closed status | Simplest schema | |
| Three kinds (`divergence`, `qualification`, `deferred-scope`) with citation-only waivers and mandatory proof tests on closed entries | Distinguishes objects that are genuinely different, and cannot launder a regression | ✓ |

**Choice:** second option (D-23, D-24, D-25, D-26).
**Notes:** the CONF-01 qualification (RG-02 settled by owner ruling on measured
evidence, not by a clean verdict token) is not a divergence — the implementation
conforms — but REQUIREMENTS.md makes that caveat mandatory wherever CONF-01 is
cited under EVAL-01 precondition (ii), and a register is how it travels
automatically instead of depending on a human remembering. PLAT-01/PLAT-02 are
scope deferrals, not defects. Collapsing all three into "divergence" would be
dishonest in both directions. The `waiver` field is a **citation slot only**: it
names an already-granted authorization (a scope boundary, a gap ruling, an audit
finding) and never creates one — who may waive, and whether a waived run may
spend evaluation budget, are open charter §6 questions owned by the charter
workstream under SCOPE-32. Closed entries must cite the test that proves closure,
because a register asserting "C-03 closed" over regressed code would launder a
defect into a clean run record.

---

## Run-record surfacing and the EVAL-01 projection

| Option | Description | Selected |
|--------|-------------|----------|
| Extend `training_metadata.json` to schema v3 | One artifact, already re-validated on resume | |
| A separate `runs/<run>/preflight.json` plus a verbatim `conformance` passthrough block in `summary.json`, including `eval01_precondition_i` | Different lifecycle; mirrors the Phase-46 `_GATE_KEYS` / `eval01_precondition_iii` pattern | ✓ |

**Choice:** separate artifact (D-27, D-28).
**Notes:** `training_metadata.json` has resume-time recompute-and-compare
semantics tied to `S_H`; preflight results are per-assertion-event and include
stage-boundary re-assertions, a different lifecycle. A refusal writes the
artifact *before* exiting non-zero through the existing `finish_run("failed", 1)`
path — a blocked run must leave the evidence saying why. Naming: Phase 46 already
owns `gate_status` (instrumentation) and `gate_verdict` (metric) with a
deliberate distinction; Phase 49's "gate" is a different object, so every field
added here is prefixed `conformance_*` / `preflight_*` and no `gate_*` key is
reused or overloaded. Phase 51 remains the verifier of the three preconditions —
Phase 49 only makes the facts mechanically available.

---

## Verification strategy and the no-run boundary

| Option | Description | Selected |
|--------|-------------|----------|
| Dataset-free fixtures plus a synthetic-source end-to-end seam test | Follows the owner's 2026-07-30 Option-B ruling that governed Phase 47 | ✓ |
| Add a `--preflight-only` run mode and exercise it against the admitted corpus | Would de-risk the gate's first real-corpus contact | |

**Choice:** first option (D-29, D-30).
**Notes:** the owner ruled Option B for Phase 47 — "prove the semantics with
deterministic fixtures; no zero-step emitter added; first authoritative
real-corpus artifact deferred to Phase 50" — and a preflight-only runner is a
zero-step emitter under a different name. The cost is real (the gate is
unexercised against real data until Phase 50), so it is mitigated inside the
design instead: preflight reads only already-persisted, already-validated inputs
and computes nothing new about the data, and an end-to-end seam test drives the
real `main()` ordering with `data.source: synthetic` so the D-05 ordering
constraint is proven by execution rather than by inspection. Recorded as a
deferred idea so the trade-off is visible rather than lost.

---

## SCOPE-32 — consume charter deliverables, or implement the minimum subset?

| Option | Description | Selected |
|--------|-------------|----------|
| Consume charter deliverables | Avoids duplication if they have landed | |
| Implement the minimum subset, shaped so the charter can subsume it | Correct if nothing has landed | ✓ |

**Choice:** implement the minimum subset (D-31, D-32).
**Notes:** decided on evidence, re-derivable at planning time. A repository-wide
search finds the 2026-07-24 charter design document as the workstream's only
artifact — every other hit is a reference to it from `.planning/` or the v2.2
proposal. No divergence register, no normative-statement index, no preflight
code, and no charter branch or worktree exists (`git worktree list` shows
`master`, `fut05-comments`, `specwork`, `trainex`). The planner re-runs this
check and records the date; if a deliverable has landed in the interim it is
consumed rather than duplicated. Forward compatibility is bought explicitly: a
named module boundary, a versioned register schema, no waiver policy, no X/M
thresholds, and the normative-statement index not started.

---

## Claude's Discretion

Delegated to planner and executor, without re-opening any decision above: module
and symbol names inside `pinn/conformance/`; exact JSON field names and
schema-version numbering; how invariant-B resume state is threaded (checkpoint
payload preferred, re-arm-and-record permitted, silent re-arm prohibited); the
precise `StepGuards` integration signature; test-file organization within
`tests/phase49/`; and whether the two small D-24 interpretation entries are one
register row or two.

## Deferred Ideas

The general verification regime (normative-statement index, CI integration,
waiver policy, thresholds X and M) — charter workstream, SCOPE-32. A
preflight-only/zero-step run mode — owner ruling required. Multi-stage `λ^max`
reconfiguration (PLAT-01) and stochastic L-BFGS (PLAT-02) — SCOPE-27.
Config-resolving `collocation_count` — SCOPE-29. The four spec-text amendments
plus the new `λ_IC` locked-vs-default instance — VER-20, Phase 52. First
real-corpus `S_H`/`ε_H` and the gate's first real exercise — Phase 50. Verifying
and recording the EVAL-01 preconditions and spending the single evaluation —
Phase 51. Recipe tuning and trainex-r2 adjudication — v2.3.

Reviewed but not folded: `d-06-static-epsilon-sensitivity-check` (score 0.60,
lexical match only — a sensitivity study is tuning-shaped work prohibited by
SCOPE-29) and `trainex-r1-research-handoff` (research administration, unrelated).
