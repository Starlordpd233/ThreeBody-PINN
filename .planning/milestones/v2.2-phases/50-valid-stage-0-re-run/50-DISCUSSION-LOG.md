# Phase 50: Valid Stage-0 Re-Run - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-08-11
**Phase:** 50-valid-stage-0-re-run
**Areas discussed:** Recipe & budget provenance, Seed band & Phase-51 pre-registration, First-contact ordering, Iteration policy under SCOPE-29, Validation-ε_H characterization, Evidence contract & execution environment

**Mode:** `/gsd-discuss-phase 50 --all` with an explicit owner instruction to
*"choose the best option following your best judgement and reasoning, no need to
ask the user for any input unless it is absolutely necessary."* All six gray
areas were auto-selected (`--all`) and every question was answered by the agent
from grounding rather than by prompt. The "Selected" column therefore records an
**agent selection under owner delegation**, not an owner choice. Two decisions
were deliberately *not* taken and are reserved to the owner (CONTEXT D-11, D-20).

---

## Recipe & budget provenance

**Question:** What budget do the three conformant runs execute at, and what does
"matching the v2.0 protocol" require?

| Option | Description | Selected |
|--------|-------------|----------|
| v2.0-matched (300 steps, `smoke: true`) | Copy the pilot config verbatim; maximal isolation of the conformance repair as the only changed variable | |
| Shipped Stage-0 config (1000 steps, non-smoke) | Use `configs/stage0-example.yaml`'s budget; comparability held at protocol level | ✓ |
| Both arms (300 + 1000) | Run a matched arm alongside the graded band to isolate the budget confound | |

**Selection:** Shipped Stage-0 config — `max_epochs = n_adam = 1000`, `smoke`
absent.
**Notes:** Decisive evidence, in order of weight. (1) The owner ratified
invariant-B `N = 500` on 2026-08-05 explicitly as `0.5 · N_Adam,0`, against the
Phase-49 D-19 packet whose stated anchors were the shipped config's
`N_Adam,0 = 1000` / `max_epochs = 1000`; at 300 steps the ratified window is
arithmetically unreachable and roadmap success criterion 2 ("invariants A/B hold
for a **full run**") becomes unfalsifiable. (2) The v2.0 pilot config carries
`run.smoke: true` — it is the ACC-02 ~5-minute mechanical smoke budget, and
"the pilot" is a misleading name for it. (3) `ctl_instruction.md` marks
`MAX_EPOCHS` "provisional pending FUT Stage-0 pilot calibration (SCOPE-14)" — the
spec delegates the value rather than being silent, and `configs/stage0-example.yaml`
is the calibrated artifact the owner has ratified into four times. Checked
against SCOPE-29: 1000 was committed before any conformant number existed, so it
is not selected against an observed result. The third option was rejected as
measurement beyond RUN-01/RUN-02 and recorded as a deferred idea. The resulting
3.33× budget confound is recorded (CONTEXT D-03) rather than argued away, because
Phase 44 ranked "undertrained budget" as a live hypothesis and DIAG-05 must see
it.

---

## Seed band & Phase-51 pre-registration

**Question:** Which run does Phase 51 evaluate, which checkpoint, and when is
that decided?

| Option | Description | Selected |
|--------|-------------|----------|
| Decide in Phase 51, after the band exists | Let Phase 51 pick the run and checkpoint once numbers are visible | |
| Pre-register seed 42 + `best.pt` before any graded run | Fix seed, checkpoint, and an ineligibility-only fallback order in a committed record | ✓ |
| Pre-register a metric rule (e.g. median-ε_H seed) | Fix a rule in advance, but one that reads the runs' own numbers | |

**Selection:** Pre-register seed 42, `checkpoints/best.pt`, fallback order
42 → 41 → 43 on *ineligibility only*, committed before the first graded run.
**Notes:** The forcing fact is that `splits.json` is partitioned with the **run
seed** (`_partition_by_signature(records, seed, ratios)`; seed 42 gives train
6,085 / validation 762 / test 759 physical keys of 7,606). Each seed has a
different held-out set, and one seed's test keys are another's training keys — so
a post-hoc choice both cherry-picks and scrambles train/test membership across
the band. Seed 42 is chosen because v2.0 spent its look there, making the new
`ε_H` directly comparable to `237.2086`; `best.pt` because that is what the v2.0
receipt records as evaluated, and it is selected by an automatic in-run retention
rule rather than by a human reading a chart. The third option was rejected: any
rule that reads the runs' numbers is selection against observed results, which is
the leakage the single-look budget exists to prevent. Also locked: if no seed is
eligible, the phase ends without a candidate and routes to the owner (CONTEXT
D-11) — no manufactured candidate, no relaxed precondition, no minted waiver.

---

## First-contact ordering

**Question:** Does Phase 50 begin with a cheap smoke run, or go straight to the
graded band?

| Option | Description | Selected |
|--------|-------------|----------|
| Straight to the graded band | Three runs, no preliminary; fastest path | |
| Calibration smoke first, then the band | One smoke on the current code state, then seeds 41 → 42 → 43 ascending | ✓ |

**Selection:** Smoke first — and this turned out not to be a preference.
**Notes:** `_check_duration_gate` (`pinn/train.py:576-627`) refuses any non-smoke
launch that has no persisted timing calibration matching the launch's **full**
fingerprint, `git_head` included. `runs/.calibration/stage0-timing.json` records
`git_head: ae250c77…` (v2.0, 2026-07-22); HEAD is `a7d355dc`. Every graded launch
would refuse. The smoke is therefore a discovered precondition of the shipped
code, and it simultaneously discharges two things earlier phases routed here at
smoke cost rather than on a graded run: the conformance gate's first real-corpus
execution (Phase-49 D-29/D-30) and the first authoritative real-corpus
`S_H`/`ε_H`/`N_train` (owner ruling 2026-07-30, Option B). Two refinements
followed: the smoke config carries `front_advance_window_n: 500` so first contact
walks the identical `REQUIRED_RUN_START_CHECKS` path the graded runs will
(`configs/smoke.yaml` leaves it unset, which would take a different branch), and
the smoke runs at seed 42 so its `s_h`/`n_train` must equal the graded seed-42
run's exactly — a free consistency assertion on the new statistic. A further
consequence surfaced and was locked as CONTEXT D-17: because the fingerprint pins
`git_head`, **no commit may land between the smoke and the graded runs**, which
constrains GSD's per-plan commit cadence and must shape the wave structure.

---

## Iteration policy under SCOPE-29

**Question:** What may change inside the phase when a run refuses, HALTs, or
fails — and what must be routed out?

| Option | Description | Selected |
|--------|-------------|----------|
| Case-by-case judgement | Handle each failure as it arises | |
| A written classification test + owner routing for the reserved cases | One test applied to every proposed change; invariant-B HALT and no-eligible-seed reserved to the owner | ✓ |

**Selection:** The written test — *does this change bring the implementation
closer to a locked spec value, an owner ruling, or a Phase-46..49 contract,
justified **without reference to what a run produced**?*
**Notes:** Yes ⇒ conformance repair, allowed, and the **full band** re-runs at
the new code state (seeds are never mixed across code states). No ⇒ tuning,
prohibited, whatever it is called. The reserved cases are explicit because they
are the ones under pressure: an invariant-B HALT at ~step 501 is a live
possibility (v2.0 logged `front_idx = 0` across 1,500/1,500 steps in 5/5 runs) and
is exactly the "too small HALTs a healthy-but-slow run" direction the owner was
shown before choosing 500 — so `N` is not raised, softened, re-marked
provisional, or bypassed by any agent (Phase-49 D-18/D-21 stand). A preflight
refusal gets the repair loop and a register entry, never a waiver minted here
(Phase-49 D-26: the register grants no authority and this milestone defines no
waiver policy). Guard trips are run outcomes, not interruptions: recorded failed
and re-launched fresh, `recover_retries` stays 0; `--resume` is reserved for
genuine interruptions. Every launch that starts — refused, HALTed, failed,
superseded, graded — is listed in a committed run ledger, because the protection
against a quiet retry loop is that retries are visible.

---

## Validation-ε_H characterization

**Question:** What does "validation ε_H recorded and characterized across three
seeds" concretely produce, and what may it be used for?

| Option | Description | Selected |
|--------|-------------|----------|
| Terminal `gate_eps_h` per seed | The three headline numbers and their spread | |
| Full band record: trajectories + per-trajectory distributions + run facts | All validation events, sidecar distributions, `S_H`, front high-water, per-term losses and gradient stats | ✓ |

**Selection:** The full band record, explicitly descriptive.
**Notes:** Scoped by what Phase 52's DIAG-05 will need, so the re-derivation finds
its evidence already captured rather than reconstructing it from logs — Phase 44
had to rebuild the per-trajectory ε_H distribution and the loss decomposition by
hand from retained artifacts. The distribution comes from each run's latest
`validation_gate/step-<8-digit>.json` sidecar (the INST-01 rows), and the headline
values are copied **verbatim** from `summary.json`'s `gate_*` keys rather than
recomputed, per the Phase-46 passthrough discipline. Three prohibitions recorded
alongside: validation ε_H is not the held-out gate and renders no verdict on the
design; it may not choose the submission seed or the checkpoint; and it may not
justify any parameter change. `gate_status` and `gate_verdict` stay distinct in
every reported number so an instrumentation failure can never render as a PASS.

---

## Evidence contract & execution environment

**Question:** Where do the runs execute, how do they reach the corpus, and what
gets committed?

| Option | Description | Selected |
|--------|-------------|----------|
| Isolated gsd-executor worktree | Standard GSD execution isolation | |
| Inline on `.worktrees/trainex` @ `milestone/v2.2`, conda `pinn-train` | Run where `runs/`, the calibration, and the v2.0 baselines already live | ✓ |

**Selection:** Inline, non-worktree, under
`<home>/miniforge3/bin/conda run -n pinn-train`.
**Notes:** `runs/` is worktree-local and gitignored, `runs/.calibration/` lives
there, and the v2.0 pilot artifacts this phase compares against are resident in
this checkout. Environment verified this session — python `3.11.15`, torch
`2.12.1`, MPS available — byte-matching every v2.0 pilot's `env_fingerprint`,
which is what preserves cross-milestone comparability. One assumption was checked
and turned out already solved: `default_data_root()` derives the **main-repo**
`simulation_data/Data` from the parent of `git rev-parse --git-common-dir`
(deliberately not `--show-toplevel`), so the 4.8 GB corpus at the master-root
checkout is reachable from this worktree with no copy, and the 776 KB
worktree-local `simulation_data/Data/` is refused by `DataSourceRootIncomplete`
rather than silently producing a green run over a tiny corpus. `GSD_DATA_ROOT`
and `GSD_ALLOW_PARTIAL_DATA_ROOT` stay unset — setting either bypasses the guard
that protects the whole result. The header comment in `configs/smoke.yaml`
("run from the main-root checkout") is stale relative to the code. Because
`.gitignore` excludes `runs/` wholesale, evidence extraction into
`.planning/phases/50-valid-stage-0-re-run/evidence/` is mandatory, with per-file
source path + sha256; `*.log` is globally ignored so `logs/train.log` is not
retained, while `train.log.jsonl` does not match the pattern and is.

---

## Claude's Discretion

Delegated to the planner/executor, bounded by every decision above: exact run and
config file names (locked properties only — distinct from the v2.0
`stage0-pilot-seed4X` names, committed, and the three graded configs differing
only in `run.seed`/`run.run_name`); the wave decomposition and how the
no-commit-mid-band constraint is expressed in it; the file format and layout of
the run ledger, band record, pre-registration record, and config-delta record;
which quantiles the distribution reports; whether the smoke and the band
extraction are one plan or several; attended vs unattended launch; and the sha256
manifest format for evidence extraction.

## Reserved to the owner (not decided here)

- **Whether an invariant-B HALT changes `N`** — routed as a gap if it fires
  (CONTEXT D-20). The shipped config comment already anticipates this: "retain
  this value verbatim unless the owner re-rules after a Phase-50 invariant-B
  HALT."
- **What happens if no seed is eligible** — the phase records the state and stops;
  Phase 51 does not open (CONTEXT D-11).

## Deferred Ideas

- A 300-step budget-matched arm to isolate the conformance repair from the
  budget change.
- Any recipe change suggested by the conformant numbers — v2.3 (SCOPE-29/31).
- Re-ruling `N` after an observed HALT — owner, not agent.
- Stage-1+ advance, PLAT-01 `stage_factory`, PLAT-02 sL-BFGS — SCOPE-27.
- Config-resolving `collocation_count`; the `I_warm` integer-floor
  interpretation — open register qualifications, SCOPE-29.
- Committing `logs/train.log` (needs a `*.log` negation) — not needed.
- The general verification-enforcement regime — charter workstream, SCOPE-32.
- The four VER-20 spec-amendment routing items — Phase 52, SCOPE-30.
- Verifying the EVAL-01 preconditions and spending the single evaluation —
  Phase 51.
- Re-deriving the Phase 44 diagnosis — Phase 52, DIAG-05.

### Reviewed Todos (not folded)

- **`d-06-static-epsilon-sensitivity-check`** (score 0.20, matched on the lexical
  keyword "phase") — not folded; below threshold and tuning-shaped work
  prohibited by SCOPE-29. Same disposition as Phases 48 and 49.
- **`trainex-r1-research-handoff`** — not folded; research-administration work
  for the r1b tuning round, unrelated to executing a conformant run.
