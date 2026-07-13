# Phase 39: Data Ingestion & Stage-0 Population Scan — Specification

**Created:** 2026-07-13
**Ambiguity score:** 0.149 (gate: ≤ 0.20)
**Requirements:** 6 locked

## Goal

The trainer serves fixed-shape Stage-0 mini-batches from an in-memory, admitted-set adapter, and the Thrust-A scan confirms Stage 0 is populated enough to train — with the on-disk format hidden behind a single adapter seam (DATA-01..06; `.planning/ROADMAP.md:102`).

## Background

**Current state (grounded scout, 2026-07-13):**

- The on-disk dataset lives at `<home>/Desktop/3_body_problem/simulation_data/Data/` in the **main repo** (gitignored and absent from this `.worktrees/trainex` worktree; `.gitignore:314-328`). It is plain-text `.txt`: IC files (3 lines × 7 floats) and Brutus files (repeating snapshot blocks + a `Result:` footer), one file per trajectory across four variant folders (`brutus_{hierarchical,standard_quasi_random}{,_gold_standard}/`; `simulation_data/Documentation/README.md:252-298`).
- `pinn/data-handling/` carries v1-era code: `core/parsing.py` (footer-robust `parse_brutus_file`), `core/scaling.py`, `processing/invariants.py`, `processing/stage_assignment.py`, `processing/input_vector.py`. Per `pinn/constants.py:9-11` (CTX-17) the Phase 38 rebuild does **not** import these. `stage_assignment.py:53` carries stale v1 thresholds (`s_min>2` for Stage 0) that conflict with the ratified interim floor `s₀=0.01`.
- Phase 38 shipped the rebuilt network (`pinn/network.py:210-228`): `forward(tau_ic13, masses)` takes 14-dim `[τ, IC₁₃]` plus raw `(3,)` masses, outputs 9-dim mass-weighted-COM. The 13-dim IC vector producer exists only in the v1 `input_vector.py:121` (`formulate_ic_vector`).
- **What does NOT exist yet:** no admitted-set container class, no replay/lookahead batch constructor, no DataLoader init running the Step-1A gate, no `n_snapshots(traj)`/`dt_out(traj)` accessor API, no `data_version_hash` mechanism.

**Grounding (two authoritative sources — no candidate verdict source):**
1. The ratified trainex-r1a decision set (`framework-specs/trainex-r1/decision-adjudication/{trainex-r1a-resolution-doc.md, RATIFICATION.md}`, owner-ratified 2026-07-05) — build engineering.
2. The locked framework specs (`ctl_instruction.md` Step 1A admission gate at `:539-651`, replay/lookahead batch contract at `:1813-1840`, `pinn_architecture.md`) — the science.

**Key locked values:** `D ≈ 4.6416` (`pinn/constants.py:24`); admission-gate Plummer softening `eps = 1e-10` in V (`ctl_instruction.md:566`, **distinct** from training `EPS_SOFT = 1e-5` at `pinn/constants.py:39`); conservation gate `SCS ≤ −5` reject (clause 5, `:568`); interim Stage-0/1 floor `s₀ = 0.01` (PB-1, `CLEARANCE.md`); blacklist 65 IDs / 2 hierarchical + 63 standard (`ctl_instruction.md:634`).

## Requirements

1. **Format-aware in-memory adapter (DATA-01)**: A single adapter module is the only component that imports/reads the on-disk dataset format; it preloads the admitted set fully in-memory as fp32 with `num_workers=0`, exposes `n_snapshots(traj)` and `dt_out(traj)` accessors, and emits a `mem:` log line against a configurable 0.7 memory watermark.
   - Current: No admitted-set container or adapter exists; v1 `parsing.py` reads the format but is not imported by the rebuild (CTX-17). On-disk data is absent from this worktree.
   - Target: One adapter module (env-var-located `GSD_DATA_ROOT` → main-repo default) holds the entire admitted set as fp32 tensors, exposes per-trajectory metadata accessors, logs `mem: <bytes> (<fraction>) watermark=0.7`, and is the sole importer of the `.txt` format.
   - Acceptance: A test constructs the adapter against the real dataset path; `n_snapshots(traj)` and `dt_out(traj)` return values matching a direct parse; grep confirms no other `pinn/` module imports the `.txt` parsing; the `mem:` line appears in logs with a fraction ≤ 0.7 on the 24 GB machine.

2. **Full Step-1A admission gate at load (DATA-02)**: The adapter applies all seven Step-1A clauses — (1) identity & fail-closed blacklist, (2) data-remediation quarantine (empty in the verified baseline), (3) structural integrity (≥2 snapshots, 3 body rows, finite, strictly monotone timestamps), (4) completeness (`final_timestep ≥ 9.5` from parsed times, never footer/line-count), (5) conservation reject gate (`SCS > −5` reject; `SCS = −5` Marginal; `|H(0)|≈0` quarantine; `eps_H = 0` Excellent), (6) physical-invariant gates (mass invariance `< 1e-15`, COM/momentum), (7) grid-consistency WARN — recomputing `eps_H` from raw parsed arrays in float64 with Plummer softening `eps = 1e-10`, and drops NaN/Inf samples with a logged count.
   - Current: No admission gate runs in the rebuild; the v1 pipeline does not enforce clause-5 recomputation.
   - Target: All seven clauses execute at adapter init; per-folder admitted/rejected/quarantined/dropped counts are logged; `eps_H` is computed as `max_t |(H(t)-H(0))/H(0)|` in float64 from snapshot arrays (NOT read from the metrics JSON or the footer `dE/E`).
   - Acceptance: A test with a known-good trajectory admits it; a synthesized trajectory with `SCS > −5` is rejected; a trajectory with `|H(0)|≈0` is quarantined (not floored); NaN/Inf samples are dropped and counted; the logged counts sum to the parsed total per folder.

3. **`data_version_hash` compare-and-refuse (DATA-03)**: The adapter reads `data_version_hash` and refuses to load on mismatch — a hard error, never a silent proceed. Because the hash **production** mechanism is open upstream (U-12, `trainex-r1a-resolution-doc.md:153`: "Open (v1.5 PIPE-XX); the adapter implements compare-and-refuse only"), when the hash field is absent the adapter emits a typed, logged skip/deferral (recorded as GAP-39-XX operational coordination) and proceeds — never a silent no-op.
   - Current: No `data_version_hash` mechanism exists anywhere in `pinn/`.
   - Target: The adapter calls a `verify_data_version(expected_hash)` method; mismatch raises a hard error; absent-field emits a typed `DataVersionHashDeferred` signal logged prominently and surfaced as a gap.
   - Acceptance: A test with matching hash loads successfully; a test with mismatching hash raises and aborts; a test with absent hash proceeds only after emitting the typed deferral log line (grep-verified).

4. **Deterministic stage-stratified split manifest (DATA-04)**: A deterministic train/val/test split (~80/10/10 default) is written to the run folder, partitioned by `physical_key = (variant, id)` first and expanded to all `record_key`s (base + gold), with a hard assertion that no `physical_key` spans splits; the train split shuffles per-epoch under a seeded RNG while val/test iterate in fixed order.
   - Current: No split logic exists; the v1 pipeline has no `physical_key` grouping.
   - Target: A split manifest (e.g., `splits.json`) is written at run init, keyed by `physical_key` → split assignment; an assertion verifies the grouped invariant (PB-4); the RNG seed is recorded for reproducibility.
   - Acceptance: A test constructs a split over a fixture where a base/gold pair share a `physical_key` and asserts both land in the same split; re-running with the same seed reproduces the manifest byte-for-byte; the manifest file exists in the run folder.

5. **Replay/lookahead two-point-set batch constructor (DATA-05)**: The constructor selects `B_replay = 240` trajectories from `D_≤k` plus `B_lookahead = 16` from `D_{k+1}` under the `has_stage(k+1)` guard (256 total), emitting two independent point sets: data-fidelity points drawn from the selected trajectories' snapshots at `n_pts = min(32, n_snapshots)` (~8,192 points, provisional), and collocation points drawn continuously from `[0, T]` (~4,096 points, provisional; energy reuses the physics collocation set) — with the 50/50 uniform + acceleration-weighted time sampler applied to the data-fidelity set only (mixed continuous collocation deferred per LOOP-03).
   - Current: No replay/lookahead or batch constructor code exists in `pinn/`.
   - Target: A batch constructor emits fixed-shape mini-batches per `ctl_instruction.md:1813-1840`; `has_stage(k+1)` false → `B_lookahead = 0` (replay-only); `k+1` pool < 16 → sample-with-replacement padding holding `240+16` fixed (`:1827-1828`); the 14-dim `[τ, IC₁₃]` + raw `(3,)` masses travel per sampled point.
   - Acceptance: A test with a populated Stage 0 emits a 256-trajectory batch with the two point-set cardinalities; `has_stage(k+1)` false emits a replay-only batch; an under-sized `k+1` pool pads with replacement to 16; the data-fidelity points use the mixed sampler while collocation uses a uniform draw.

6. **Thrust-A Stage-0 population scan (DATA-06)**: A scan bins admitted trajectories by the difficulty invariants, counts per-stage populations (Stage 0 explicitly), reports the admitted-set `s_min` distribution for the owner's ratification of the Stage-0/1 threshold `s₀` (interim floor 0.01), and flags an under-populated Stage 0 as a fatal-class risk supplying per-stage byte counts before any training run.
   - Current: No scan exists; v1 `stage_assignment.py` has stale conflicting thresholds.
   - Target: The scan runs at init over the admitted set, bins by the Stage-0/1 criterion (`s_min > s₀` for Stage 1, else Stage 0; interim `s₀ = 0.01`), writes a per-stage population + byte-count + `s_min` distribution report, and raises a fatal-class signal if Stage 0 is under-populated (below the batch minimum of 240). It does NOT ratify `s₀`.
   - Acceptance: A test with a fixture admitted set produces the report with Stage-0 population ≥ 240 → proceeds; a fixture with Stage-0 population < 240 → fatal signal; the report file exists; the code path does not mutate `s₀`.

## Boundaries

**In scope:**
- The D3-C in-memory fp32 admitted-set adapter with `n_snapshots`/`dt_out` accessors and the `mem:` watermark log (DATA-01)
- The full Step-1A admission gate (clauses 1–7) running at load, with `eps_H` recomputed in float64 (DATA-02)
- The `data_version_hash` compare-and-refuse path with the typed absent-field deferral (DATA-03)
- The `physical_key`-grouped stage-stratified split manifest (DATA-04)
- The replay/lookahead two-point-set batch constructor emitting fixed-shape Stage-0 batches (DATA-05)
- The Thrust-A Stage-0 population scan with the `s_min` distribution report and fatal-class flag (DATA-06)

**Out of scope:**
- The adaptive collocation **sampler** interface (`(model, last_residuals)` hook) — Phase 40 owns TRAIN-04. Phase 39 emits a fixed uniform collocation point set in the batch; Phase 40 makes it adaptive.
- The full multi-stage curriculum-statistics EDA + Stage 1–6 threshold recalibration — FUT-02 (deferred; `.planning/REQUIREMENTS.md:110`). Phase 39 runs the Stage-0 scan only.
- `s₀` ratification — the owner ratifies `s₀` from the scan's `s_min` distribution; Phase 39 surfaces the evidence, it does not pick the value. The interim `0.01` is a seam (PB-1).
- The `data_version_hash` **production** mechanism — U-12 keeps this open upstream (v1.5 PIPE-XX); Phase 39 does compare-and-refuse only.
- Training-loop DataLoader plumbing (epoch iteration, loss wiring, optimizer feeding) — Phase 40. Phase 39 delivers the data substrate.
- Reimplementing the network or loss — Phase 38 (complete). Phase 39 consumes `network.forward`'s input contract as a read-only interface.

## Constraints

- **Single M5 Pro, 24 GB unified memory** (R-3 closed): in-memory fp32 preload must hold under the 0.7 watermark. Corrected corpus ≈8,228,794 snapshots ≈ 0.72 GB fp32 (`CLEARANCE.md` PB-5 propagation note) ≈ 3% of RAM — comfortably in-memory.
- **`num_workers=0`** (D3-C): single-process preload; no `ProcessPoolExecutor` in the adapter (the v1 `scaling.py` uses one — not reused).
- **Precision split:** admission-gate `eps_H` is computed in **float64** with Plummer softening `eps = 1e-10` (`ctl_instruction.md:566`); the in-memory preload is **fp32** (D3-C); training-time `EPS_SOFT = 1e-5` is distinct (`pinn/constants.py:39`) and not used by the gate.
- **Raw-mass convention:** `D ≈ 4.6416` (`pinn/constants.py:24`); masses travel raw alongside the 13-dim IC vector (the model takes raw `(3,)` masses explicitly — `network.py:210-228`).
- **CTX-17:** the adapter does NOT import v1 `pinn/data-handling/`; needed parsing/invariants/IC-vector logic is ported + rewritten to spec in new Phase 39 modules.
- **Data location:** `GSD_DATA_ROOT` env var (or equivalent) defaults to the main-repo `simulation_data/Data/` path; configurable. The blacklist file (`problematic_ics_blacklist.json`) is fail-closed (missing/unreadable/schema-invalid = hard init failure — clause 1).

## Acceptance Criteria

- [ ] The adapter preloads the admitted set in fp32 with `num_workers=0` and logs a `mem:` line ≤ 0.7 of 24 GB (DATA-01)
- [ ] `n_snapshots(traj)` and `dt_out(traj)` return values matching a direct parse of the `.txt` file (DATA-01)
- [ ] No `pinn/` module other than the adapter imports/reads the on-disk `.txt` format (grep-verified) (DATA-01)
- [ ] The adapter applies all 7 Step-1A clauses at init and logs admitted/rejected/quarantined/dropped counts per folder (DATA-02)
- [ ] A trajectory with `SCS > −5` is rejected; `SCS = −5` is admitted-and-flagged Marginal; `eps_H = 0` is labeled Excellent (DATA-02)
- [ ] `eps_H` is recomputed in float64 from raw parsed arrays (NOT read from the metrics JSON, NOT read from the footer `dE/E`) (DATA-02)
- [ ] A trajectory with `|H(0)|` numerically near zero is quarantined — NO denominator floor is introduced (DATA-02)
- [ ] NaN/Inf samples are dropped with a logged count (DATA-02)
- [ ] A `data_version_hash` mismatch raises a hard error and aborts load (DATA-03)
- [ ] An absent `data_version_hash` field proceeds only after emitting a typed `DataVersionHashDeferred` log line (DATA-03)
- [ ] A deterministic split manifest is written to the run folder, grouped by `physical_key` with no key spanning splits (DATA-04)
- [ ] Re-running the split with the same seed reproduces the manifest byte-for-byte (DATA-04)
- [ ] The batch constructor emits a 256-trajectory batch (240 replay + 16 lookahead) with the data-fidelity (~8,192 pts) and collocation (~4,096 pts) point sets (DATA-05)
- [ ] `has_stage(k+1)` false → replay-only batch (`B_lookahead = 0`) (DATA-05)
- [ ] `k+1` pool < 16 → sample-with-replacement padding holding batch size fixed at 256 (DATA-05)
- [ ] The 50/50 uniform + acceleration-weighted sampler applies to the data-fidelity set only; collocation uses a uniform draw (DATA-05)
- [ ] An **empty admitted set** is a hard init failure, not an empty-batch proceed (edge-derived, R1-empty)
- [ ] The Thrust-A scan reports per-stage populations + byte counts + the `s_min` distribution to a report file (DATA-06)
- [ ] A Stage-0 population below 240 raises a fatal-class signal (DATA-06)
- [ ] A trajectory with `s_min = s₀` exactly lands in Stage 0 (Stage-1 criterion is strict `> s₀`) (edge-derived, R6-boundary)

## Edge Coverage

**Coverage:** 19/19 applicable edges resolved · 0 unresolved

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| adjacency | R1 | ✅ covered | Adapter owns the format; no merge/collision semantics — one admitted set per init |
| empty | R1 | ✅ covered | Empty admitted set → hard init failure (new AC; an empty proceed would silently corrupt training) |
| ordering | R1 | ✅ covered | Deterministic seeded iteration is the split/batch contract (R4); no undefined order |
| boundary | R2 | ✅ covered | `SCS = −5` exactly is Marginal (admitted, flagged); `eps_H = 0` is Excellent; `|H(0)|≈0` quarantines — all clause 5 (`ctl_instruction.md:568-571`) |
| precision | R2 | ✅ covered | `eps_H` in float64 with `eps = 1e-10`; distinct from fp32 preload and from training `EPS_SOFT = 1e-5` (`ctl_instruction.md:565-566`, `pinn/constants.py:39`) |
| unclassified | R3 | ✅ covered | The absent-field typed skip is locked (Round 1 Q3 + U-12); not edge-free but resolved by the deferral seam |
| adjacency | R4 | ✅ covered | `physical_key` invariant (PB-4): base/gold twins never straddle splits — hard assertion |
| empty | R4 | ✅ covered | Empty admitted set → hard init fail (R1-empty); a split over an empty set never occurs |
| ordering | R4 | ✅ covered | Train shuffles per-epoch under a seeded RNG; val/test fixed order — deterministic, recorded seed |
| boundary | R5 | ✅ covered | `has_stage(k+1)` false → `B_lookahead = 0`; pool < 16 → replacement to 256 (`ctl_instruction.md:1827-1828`) |
| adjacency | R5 | ✅ covered | `D_≤k` (cumulative) vs `D_{k+1}` (single next stage) — disjoint by stage assignment (`:1818`) |
| empty | R5 | ✅ covered | Stage 0 < 240 → R6 fatal signal stops the run before a batch is assembled |
| ordering | R5 | ✅ covered | Mixed sampler is data-fidelity-only; collocation uniform — the ordering contract is per-point-set, locked LOOP-03 |
| precision | R5 | ✅ covered | `n_pts = min(32, n_snapshots)` is the locked M12 rule; provisional 8192/4096 budgets flagged |
| boundary | R6 | ✅ covered | `s_min = s₀` exactly → Stage 0 (Stage-1 criterion is strict `> s₀`); new AC for the boundary |
| adjacency | R6 | ✅ covered | Bins are disjoint by the `s_min > s₀` criterion; no overlap |
| empty | R6 | ✅ covered | Stage 0 = 0 → fatal-class signal (the under-populated flag's limit case) |
| ordering | R6 | ✅ covered | Deterministic binned iteration; `s_min` distribution reported as a sorted summary |
| precision | R6 | ✅ covered | `s_min` computed in float64 (admission-gate precision); distribution is read-only for ratification |

## Prohibitions (must-NOT)

**Coverage:** 4/4 applicable prohibitions resolved · 0 unresolved

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT use the Brutus footer `dE/E` as the Step-1A `eps_H` — the footer value is raw Brutus energy drift, not `max_t \|(H(t)-H(0))/H(0)\|` recomputed in float64 | R2 | resolved (test) | The footer's `dE/E` is a distinct quantity (`ctl_instruction.md:578-581`); using it would silently admit/reject wrongly. Negative test: a trajectory whose footer `dE/E` disagrees with the recomputed `eps_H` must be gated by the recomputed value. |
| MUST NOT introduce a denominator floor for the `\|H(0)\|≈0` case — the correct action is quarantine, not a numeric floor | R2 | resolved (test) | Clause 5 (`ctl_instruction.md:570`): "do NOT introduce a denominator floor." A floor would silently admit trajectories with undefined conservation. Negative test: a trajectory with `|H(0)|<epsilon` is quarantined, not admitted via a floor. |
| MUST NOT read `eps_H` from the `Data/metrics/sim_result_metric_*/` JSON files — the gate recomputes from raw parsed arrays | R2 | resolved (test) | Clause 5 (`ctl_instruction.md:577-578`): "by convention the admission check is computed from the raw parsed arrays." The metrics JSON is a different pipeline stage's output. Negative test: the gate passes/fails on the recomputed value even when the JSON disagrees. |
| MUST NOT auto-ratify `s₀` or auto-decide Stage-0 sufficiency — the scan surfaces evidence; the owner ratifies | R6 | resolved (judgment) | PB-1 + the owner-carved discipline: `s₀` is owner-ratified from the scan's distribution. The interim 0.01 is a seam, not a decision. Routes to judgment review (a code path that mutates `s₀` is the failure mode). |

## Ambiguity Report

| Dimension          | Score | Min  | Status | Notes                              |
|--------------------|-------|------|--------|------------------------------------|
| Goal Clarity       | 0.92  | 0.75 | ✓      | DATA-01..06 each concrete with current/target/acceptance |
| Boundary Clarity   | 0.82  | 0.70 | ✓      | Phase 40 / FUT-02 / s₀-ratification / hash-production / DataLoader-plumbing all explicitly out |
| Constraint Clarity | 0.80  | 0.65 | ✓      | Env-var path, CTX-17-clean port, precision split, 0.7 watermark, fail-closed blacklist |
| Acceptance Criteria| 0.82  | 0.70 | ✓      | 20 pass/fail criteria incl. 4 test-tier prohibitions + 2 edge-derived boundaries |
| **Ambiguity**      | 0.149 | ≤0.20| ✓      |                                    |

Status: ✓ = met minimum, ⚠ = below minimum (planner treats as assumption)

## Interview Log

| Round | Perspective     | Question summary                                  | Decision locked                                                                 |
|-------|-----------------|---------------------------------------------------|---------------------------------------------------------------------------------|
| 1     | Researcher      | Data location: worktree-absent dataset, where?    | `GSD_DATA_ROOT` env var → main-repo `simulation_data/Data/` default (Recommended) |
| 1     | Researcher      | v1 `data-handling/` reuse vs CTX-17?              | Port + rewrite to spec in new Phase 39 modules; no v1 import (Recommended)       |
| 1     | Simplifier      | `data_version_hash` seam (U-12 production open)?  | Build compare-and-refuse + typed absent-field skip → GAP-39-XX (Recommended)     |
| 2     | Boundary Keeper | Phase 40 vs 39 collocation boundary?              | Phase 40 owns the adaptive sampler (TRAIN-04); Phase 39 emits the fixed point set |
| 2     | Boundary Keeper | Full curriculum EDA in scope?                     | No — FUT-02 deferred; Phase 39 runs Stage-0 scan only                            |
| 2     | Boundary Keeper | Who ratifies `s₀`?                                | The owner, from the scan's `s_min` distribution; Phase 39 surfaces evidence only |
| 2     | Boundary Keeper | Training-loop DataLoader plumbing?                | Phase 40; Phase 39 delivers the data substrate                                  |
| 2     | Boundary Keeper | Proceed to write SPEC.md?                         | Yes — write it                                                                  |
| 5.5   | Edge probe      | 19 applicable edges across R1–R6                  | 19/19 covered from spec (clause 5, ctl:1827-28, PB-4) + 2 new edge-derived ACs  |
| 5.6   | Prohibition     | Must-NOT axis for a scientific data loader        | 4 kept (3 test-tier: footer-dE/E, denominator-floor, metrics-JSON; 1 judgment: s₀-auto-ratify) |

---

*Phase: 39-data-ingestion-stage-0-population-scan*
*Spec created: 2026-07-13*
*Next step: /gsd-discuss-phase 39 — implementation decisions (how to build what's specified above)*
