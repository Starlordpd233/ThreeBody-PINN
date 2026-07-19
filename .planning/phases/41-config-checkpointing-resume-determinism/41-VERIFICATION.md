---
phase: 41-config-checkpointing-resume-determinism
verified: 2026-07-19T02:08:05Z
status: human_needed
score: 6/6 must-haves verified
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 5/6
  previous_verified: 2026-07-18T08:54:46Z
  gaps_closed:
    - "Full seed/RNG state is recorded in config + every checkpoint (CTRL-08 / ROADMAP SC #4 / SPEC AC) — closed by 9abc676c per GAP-41-01 RESOLVED-WITH-INSTRUCTION (representation B: sibling runs/<name>/run_start_rng.pt)"
  gaps_remaining: []
  regressions: []
gaps: []
deferred: []
human_verification:
  - test: "Owner-ratify B-5 IDENTITY/OPERATIONAL field lists in RESUME_FIELD_REGISTRY before production run #1"
    expected: "Lists marked owner-ratified (not only provisional/⚖); real-data deferred IDENTITY categories resolved or still explicitly deferred"
    why_human: "CTRL-05 requires owner ratification of the field list; code ships a surfaced ⚖ proposal only. NON-blocking for Phase-41 closure (pre-run-#1 obligation)"
  - test: "Owner-calibrate R-1 guard thresholds + D4-a wall-clock checkpoint ceiling at the Phase-43 Stage-0 pilot"
    expected: "loss_explosion_ceiling / disk_floor_fraction / memory_watermark_fraction and wall_clock_ceiling_s ratified from pilot variance"
    why_human: "Values are ⚖ provisional placeholders by design; mechanism is wired and tested, values are owner-carved at Phase 43. NON-blocking for Phase-41 closure"
---

# Phase 41: Config, Checkpointing, Resume & Determinism — Re-Verification Report

**Phase Goal:** Every run is driven by one frozen keyed config, survives interruption and corruption, resumes and rolls back correctly, and records enough seed/RNG state to reproduce to statistical equivalence — with guards that stop-and-preserve on trouble.

**Verified:** 2026-07-19T02:08:05Z
**Status:** `human_needed` (all 6 truths verified; two carried-forward human-owned ratification items remain — both NON-blocking for phase closure)
**Re-verification:** Yes — after GAP-41-01 closure (previous report 2026-07-18T08:54:46Z @ fe38b2d6, `gaps_found` 5/6)
**Branch / HEAD:** `milestone/v2.0` @ `66141380` (gap-fix commit `9abc676c` + gap-register docs `66141380`)

## Re-Verification Focus

The initial verification failed exactly one truth — #6 (CTRL-08 / ROADMAP SC #4): the four RNG streams were in every checkpoint but not on the frozen-config path; the `frozen_config_rng_recording_format` seam was UNDECIDED. That gap is now **GAP-41-01 RESOLVED-WITH-INSTRUCTION (2026-07-18)**, owner best-judgment delegation, ratified as **representation B**: `runs/<name>/config.yaml` stays a pure `TrainingConfig` (CTRL-01/CTX-51 re-parse equality untouched) and the four run-start streams land in the sibling artifact `runs/<name>/run_start_rng.pt`. **Ratified AC interpretation (recorded in GAP-41-01):** the SPEC acceptance "frozen config and a checkpoint both contain all four RNG stream states" is satisfied on the config side by the frozen-config-side sibling artifact — `config.yaml` purity is the ratified design, not a gap.

Truth #6 was re-verified end-to-end against live code; truths 1-5 received regression checks (artifact existence, key-link sanity, full suite re-run).

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Single keyed YAML (`run/stage/opt/loss`) drives the run; fully-resolved copy frozen into `runs/<name>/config.yaml` (CTRL-01 / B-9) | ✓ VERIFIED | Carried forward + regression-confirmed: `config_yaml.load_config` + `freeze_resolved_config` intact; `FrozenCopyRoundTripTests.test_freeze_resolved_config_reparse_equal` asserts `reloaded == cfg`; independent spot-check CHECK2 re-confirmed frozen == original after a real launch |
| 2 | Dual-trigger + atomic checkpointing with rolling/best/latest/anchor retention (CTRL-02/03) | ✓ VERIFIED | Carried forward: `checkpoint.py` (607 lines) unchanged by gap fix; DualTrigger/Atomicity/Retention/FallbackScan + e2e tests all green in the 193-test suite re-run |
| 3 | Dual stage anchors + idempotent ordered promotion + `curriculum.jsonl` (CTRL-04) + complete Adam reset at boundary (CTRL-06) | ✓ VERIFIED | Carried forward: `controllers.py` ADVANCE path unchanged; `LedgerAndPromotionTests`, `AdamResetCompositionTests`, `OptimizerRestoreOrderingTests` green in re-run |
| 4 | `--resume` continues exactly; `--hold-stage` rolls back; field-classified resume-diff refuses identity/unclassified (CTRL-05) | ✓ VERIFIED | Carried forward: `resume.py` + train CLI unchanged; mid-stage exact-continuation + hold-stage e2e tests green in re-run; field list remains ⚖ provisional (human item, non-blocking) |
| 5 | Tier-1+2 guards + RECOVER/HALT + always-on `failure/` bundle (CTRL-07) | ✓ VERIFIED | Carried forward: `guards.py` + `guard_hook` wiring unchanged; guard unit + HALT-family + failure-bundle tests green in re-run |
| 6 | Full seed/RNG state recorded in **config + every checkpoint**; statistical-equivalence + exact continuation (not bitwise); strict-CPU switch (CTRL-08) | ✓ VERIFIED | **Checkpoint half (carried):** four streams in every CTX-53 payload; exact restore. **Config half (NEW, 9abc676c):** `determinism.record_run_start_rng` writes `runs/<name>/run_start_rng.pt` via the same `capture_rng_state` + `atomic_write_torch` + `torch.load(weights_only=True)` path; wired in `pinn/train.py:316-322` at fresh launch AFTER `_resolve_runtime_spec` (strict-CPU reseed reflected), on the same `run_rng` generator RunController consumes (`rng=run_rng`, train.py:478); `if not is_resume:` guard means resume never overwrites. Behavioral: `RngRecordedEverywhereTests` (real launch → all four streams in sibling + pure-config reparse) green; independent 3-part spot-check PASS (see below) |

**Score:** 6/6 truths verified (0 present-but-behavior-unverified)

### Gap Closure Verification (truth #6, three levels + data flow)

| Level | Check | Result |
|-------|-------|--------|
| Exists | `RUN_START_RNG_FILENAME` (determinism.py:39), `record_run_start_rng` (:118), `load_run_start_rng` (:138), `FROZEN_CONFIG_RNG_RECORDING_FORMAT = "sibling-artifact:run_start_rng.pt"` (config.py:134) | ✓ |
| Substantive | `record_run_start_rng` payload = `capture_rng_state(rng)` + `rng_stream_keys` + `reproducibility_scope`, written via `atomic_write_torch`; `load_run_start_rng` uses `weights_only=True` — same representation as every checkpoint | ✓ |
| Wired | `pinn/train.py:322` calls `determinism.record_run_start_rng(run_dir, run_rng)`; ordering: after `_resolve_runtime_spec` (which applies `apply_strict_cpu_determinism` when strict_cpu on), before RunController build; `run_rng` is the exact generator passed to RunController (`rng=run_rng`, :478); guarded by `if not is_resume:` | ✓ |
| Data flows | Independent spot-check: recorded torch state tensor numel=5056 (real), numpy state carries PCG64 bit_generator (real), python_random 3-tuple (real) — not empty/hardcoded | ✓ |
| Seam closed | `provisional_fields()` no longer registers `frozen_config_rng_recording_format` (docstring: DECIDED, GAP-41-01 rep B); `test_frozen_config_rng_recording_format_decided_option_b` asserts the constant | ✓ |

### Required Artifacts (regression check)

| Artifact | Status | Details |
|----------|--------|---------|
| `pinn/training/atomic_io.py` | ✓ VERIFIED | 92 lines, unchanged |
| `pinn/training/config.py` | ✓ VERIFIED | 540 lines; UNDECIDED seam removed, `FROZEN_CONFIG_RNG_RECORDING_FORMAT` constant added |
| `pinn/training/config_yaml.py` | ✓ VERIFIED | 282 lines; pure-TrainingConfig freeze preserved (rep B requirement); docstring documents the decided seam |
| `pinn/training/checkpoint.py` | ✓ VERIFIED | 607 lines, unchanged |
| `pinn/training/guards.py` | ✓ VERIFIED | 510 lines, unchanged |
| `pinn/training/determinism.py` | ✓ VERIFIED | 248 lines; +`record_run_start_rng`/`load_run_start_rng`/`RUN_START_RNG_FILENAME` (exported in `__all__`) |
| `pinn/training/controllers.py` | ✓ VERIFIED | 1374 lines, unchanged |
| `pinn/training/resume.py` | ✓ VERIFIED | 631 lines, unchanged |
| `pinn/train.py` | ✓ VERIFIED | 547 lines; run-start RNG recording wired at :316-322 |
| `tests/phase41/*` | ✓ VERIFIED | 193 tests (was 192): +RunStartRngRecordTests round-trip; RngRecordedEverywhereTests extended; config_yaml seam test flipped from UNDECIDED-assertion to decided-Option-B assertion |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `freeze_resolved_config` | `atomic_io.atomic_write_text` | `runs/<name>/config.yaml` | ✓ WIRED | Pure config (rep B design); re-parse equality carried |
| **Frozen-config path** | **four RNG streams** | **`determinism.record_run_start_rng` → sibling `run_start_rng.pt`** | ✓ WIRED | **Previously NOT_WIRED — now closed.** Fresh-launch-only, post-strict-CPU-resolve, same generator RunController consumes |
| `load_run_start_rng` | recorded payload | `torch.load(weights_only=True)` | ✓ WIRED | Same load discipline as checkpoints |
| `--resume` | run-start record | `if not is_resume:` guard (train.py:321) | ✓ WIRED | Spot-check CHECK3: sha256 unchanged across resume |
| All other links (config→dataclasses, store→atomic_io, hooks, ADVANCE, restore ordering, strict-CPU→build_network) | — | — | ✓ WIRED | Unchanged by gap fix; exercised by the green 193-test re-run |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|-------------------|--------|
| `run_start_rng.pt` | `payload["rng"]` | `capture_rng_state(run_rng)` at fresh launch | torch tensor numel=5056; numpy PCG64 state; python_random 3-tuple | ✓ FLOWING (was ✗ DISCONNECTED) |
| frozen config.yaml | TrainingConfig fields | resolved defaults + YAML overrides | Real resolved config; reparse EQUAL | ✓ FLOWING |
| Rolling checkpoints / best.pt / trip.json | (carried) | (carried) | (carried) | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Full phase41 suite | `conda run -n pinn-train python -m unittest discover -s tests/phase41 -t .` | **193 tests, OK** (36.6s) | ✓ PASS |
| Phase40 regression | `conda run -n pinn-train python -m unittest discover -s tests/phase40 -t .` | **163 tests, OK** (29.4s) | ✓ PASS |
| Fresh launch writes `run_start_rng.pt` with 4 real streams | Independent script (scratchpad, outside suite): real `pinn.train.main` launch | torch numel=5056, numpy PCG64, python_random tuple, scope string present | ✓ PASS |
| `config.yaml` re-parses EQUAL after real launch | Same script, CHECK2 | `load_config(frozen) == load_config(original)` | ✓ PASS |
| `--resume` never overwrites run-start record | Same script, CHECK3: resume from `latest.pt`, compare sha256 | sha256 `742fea5b7a68191a` unchanged | ✓ PASS |

### Probe Execution

| Probe | Command | Result | Status |
|-------|---------|--------|--------|
| *(none declared)* | — | Phase is library + CLI, not probe-migration | SKIP |

### Requirements Coverage

| Requirement | Status | Evidence |
|-------------|--------|----------|
| CTRL-01 | ✓ SATISFIED | Carried + reconfirmed (reparse equality after gap fix) |
| CTRL-02/03/04 | ✓ SATISFIED | Carried; suite re-run green |
| CTRL-05 | ✓ SATISFIED | Carried; field list ⚖ pending owner ratification (human item, non-blocking) |
| CTRL-06/07 | ✓ SATISFIED | Carried; suite re-run green |
| CTRL-08 | ✓ SATISFIED (was ✗ BLOCKED partial) | Checkpoints + restore + strict-CPU + honesty (carried) **+ frozen-config-side four-stream carriage via ratified sibling artifact (9abc676c)** |

**Orphaned requirements:** none.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| — | — | No `TBD`/`FIXME`/`XXX` in gap-fix files (determinism, train, config, config_yaml, tests) | — | clean |
| — | — | No `.is_available()` call sites (docstring mentions only; fe38b2d6 compliance held) | — | clean |
| — | — | No `yaml.load(` (safe-load discipline held) | — | clean |

The prior report's single 🛑 blocker (RNG-in-config intentionally absent) is closed.

### Human Verification Required

Both items are carried forward from the initial verification, are human-owned by design, and are **NON-blocking** for Phase-41 closure (per owner instruction 2026-07-18). Item #1 of the prior report (owner pick A/B) is resolved and removed.

### 1. Owner-ratify B-5 resume field lists (before production run #1)

**Test:** Review `RESUME_FIELD_REGISTRY` IDENTITY/OPERATIONAL classification before production run #1.
**Expected:** Ratified list (or explicit deferrals) replaces provisional-only status.
**Why human:** CTRL-05 / B-5 owner ratification; code surfaces a ⚖ proposal only.

### 2. Owner-calibrate R-1 guard thresholds + D4-a wall-clock ceiling (Phase 43 pilot)

**Test:** After the Stage-0 pilot, ratify `loss_explosion_ceiling` / `disk_floor_fraction` / `memory_watermark_fraction` and `wall_clock_ceiling_s` from pilot variance.
**Expected:** Values no longer only ⚖ placeholders.
**Why human:** Mechanism complete and tested; values owner-carved by design (Phase-43 obligation, not a Phase-41 code gap).

### Gaps Summary

**No gaps remain.** The sole gap from the initial verification (CTRL-08 config-side RNG carriage, GAP-41-01) is closed by commit `9abc676c` under the owner-ratified representation B: `config.yaml` stays a pure `TrainingConfig` and the four run-start streams (torch, torch_mps, numpy, python_random) are recorded once at fresh launch in the sibling artifact `runs/<name>/run_start_rng.pt`, after the strict-CPU runtime resolve, on the same generator RunController consumes, never overwritten by `--resume`. Verified at all four levels (exists / substantive / wired / data-flowing), by the extended 193-test phase41 suite plus the 163-test phase40 regression suite (both green), and by an independent out-of-suite fresh-launch + resume spot-check. Per the ratified AC interpretation in GAP-41-01, `config.yaml` purity is the design, not a deficiency.

No regressions detected in truths 1-5. Remaining human items are the two carried-forward owner-ratification obligations (B-5 before run #1; R-1/D4-a at Phase 43) — non-blocking for phase closure.

---

_Verified: 2026-07-19T02:08:05Z_
_Verifier: Claude (gsd-verifier, re-verification after GAP-41-01 closure)_
