# Phase 44: Physics-Gate Forensics - Research

**Researched:** 2026-07-23
**Domain:** Read-only forensic analysis of retained PINN training/evaluation artifacts (JSONL logs, JSON metrics, TensorBoard event files) — no new code system, no external libraries, no network research. All findings below were produced by direct inspection of the files and code in this worktree during this research session.
**Confidence:** HIGH — every claim in sections A-F is `[VERIFIED]` against a specific file, line, or computed value in this repository, except the single item that is explicitly and deliberately `[SILENT]` under the STOP protocol (D-07, see §C).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** Analysis scripts, their outputs, and an input-pinning manifest live in `.planning/phases/44-physics-gate-forensics/evidence/`. Nothing is written under `pinn/` — the shipped code is read as the *factual record of what executed* and is not modified (SCOPE-24 spirit).
- **D-02:** Every number quoted in `44-DIAGNOSIS.md` must be regenerable by running a retained script against pinned inputs. Pin inputs by **SHA-256 of each artifact file plus the repo commit hash**; record them in the evidence manifest.
- **D-03:** Scripts are plain Python 3 run against the repo as-is, no new dependencies. Determinism over cleverness: sorted inputs, explicit seeds where any sampling occurs (none expected).
- **D-04:** Report the **full distribution**, not just the headline number: min / percentiles (p25, p50, p75, p90, p99) / max, mean, and the fraction exceeding the `1e-5` reject threshold.
- **D-05:** Pre-register the uniform-vs-tail criterion before computing it: failure is **uniform** when the *minimum* per-trajectory ε_H already exceeds the reject threshold (100% fail); tail structure is then a separate magnitude-spread statement (max/median, p99/median).
- **D-06:** Break the distribution down by `variant` (hierarchical / standard) and `fidelity` (base / gold) — the only recorded attributes.
- **D-07 (MUST SURFACE, do not decide):** The reported `eps_h = 237.2086056078468` is exactly the maximum per-trajectory ε_H (mean = 5.6222). Whether max is the spec-intended gate statistic is checked against the locked spec and the Phase 43 evaluator record; if silent/ambiguous, record a STOP-protocol gap — do not decide.
- **D-08:** Report both raw per-term loss values and λ-weighted contributions for every step range.
- **D-09:** Attribute the warmup spike (~3.7e9) to specific term(s) by locating the spike step window and reporting `loss_*`, `grad_norm`, `lr`, `finite`/`nonfinite_keys` at those steps.
- **D-10:** `runs/stage0-smoke` is analysed as a fourth trace alongside the three pilot seeds, not folded into them.
- **D-11:** Characterize all three pilot seeds on validation-trend direction, final-loss/validation spreads, step-window trends; anchor to `43-CALIBRATION.md` ("2/3 seeds worsened") and state agreement/disagreement explicitly.
- **D-12:** Cite the Phase 38 single-trajectory overfit rung from its existing verification record — cited, never re-run (SCOPE-23).
- **D-13:** Rank ≥4 candidate causes with supporting AND contradicting evidence citations and the discriminating test that would settle each. Baseline candidates: insufficient training budget, loss-term imbalance, optimization/warmup pathology, normalization-or-data-scale issue.
- **D-14:** Discriminating tests are proposals only — never executed (SCOPE-23).
- **D-15:** The report states remedy-abstinence explicitly (SCOPE-26); any source-silent physics-adjudication call goes to the gap register, not into the report as a decision.
- **D-16:** `.planning/milestones/v2.1-GAPS.md` does not exist yet; created on the first gap (D-07 is the most likely first entry). Phase-local register: `.planning/phases/44-physics-gate-forensics/44-GAPS.md`.
- **D-17:** Commits go through `scripts/agent-commit` with `GIT_AGENT_ID`/`GIT_AGENT_OWNED_PATHS` set; explicit paths only.

### Claude's Discretion

All D-01..D-17 decisions above were `--auto`-selected recommended defaults (implementation-mechanics choices: evidence layout, pinning method, which statistics to report, ranking structure) and are safe for the planner to adjust on evidence. **Exception: D-07 is a governance obligation, not a preference** — the max-vs-mean gate-statistic question must be surfaced, never resolved by any agent.

### Deferred Ideas (OUT OF SCOPE)

- Remedy design of any kind (budget increases, loss re-weighting, warmup/LR schedule changes, curriculum re-pacing) — SCOPE-26, owner-routed via trainex-r2.
- Any decisive diagnostic training run — SCOPE-23. May be *proposed* in `44-DIAGNOSIS.md`, never executed.
- A new held-out evaluation — SCOPE-22.
- Spec edits implied by the diagnosis — SCOPE-24; become ERW research questions.
- `runs/probe-run/` and `runs/stage0-smoke-diag/` analysis — outside the named DIAG-02/03 artifact set (confirmed present on disk during this research; not analyzed further — see Open Questions).
- `trainex-r1-research-handoff` and `d-06-static-epsilon-sensitivity-check` — both deliberately reviewed-not-folded, deferred to Phase 45.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DIAG-01 | Per-trajectory ε_H distribution over 1,500 held-out test trajectories, from preserved `metrics.json` only, no evaluator invocation | §A.2 (exact schema verified: 1500-entry `per_trajectory`, keys `eps_h`/`fidelity`/`id`/`variant`, no per-trajectory SCS); computed distribution stats in §A.2; uniform-vs-tail pre-registered criterion mechanically satisfiable (min=0.9741 > 1e-5, so criterion resolves to uniform-fail before any tail statement is computed) |
| DIAG-02 | Five-term loss decomposition per-step across smoke + 3 pilot seeds, dominance, warmup-spike attribution, PHYS-05 interaction | §A.1 (exact `train.log.jsonl` schema, 26-key set, identical across all 4 runs); §B (four independently-verified per-run spike locations, dominant term, grad_norm/lr/finite context); PHYS-05 ramp schedule verified (0→1 over steps 1-31, `lambda_l` pinned at 0.0 for all 300 steps in all 4 runs — code-verified structural fact) |
| DIAG-03 | Three-seed band characterization (budget-limited vs recipe instability), Phase 38 overfit rung as control | §D.1 (43-CALIBRATION.md raw/spread tables quoted verbatim); §D.2 (38-VERIFICATION.md Rung 4 numbers + caveat about placeholder IC13); new finding: held-out **splits.json is seed-dependent** (§D.3), a load-bearing caveat for cross-seed magnitude comparison not present in 44-CONTEXT.md |
| DIAG-04 | Hypothesis-ranked diagnosis, ≥4 candidates, remedy-abstinent, gap-routes adjudication calls | §C (D-07 full evidentiary trail — supports a gap-register entry, not a decision); §B's `lambda_l_max` structural finding is directly usable as supporting evidence for a "loss-term imbalance" candidate; §D findings support "budget-limited descent" and "recipe instability" candidates |

</phase_requirements>

## Summary

Every artifact named in 44-CONTEXT.md and REQUIREMENTS.md was located, opened, and its schema verified directly in this session (Python one-liners against the actual files, and `grep`/`Read` against the actual spec and phase-record text) — nothing below is inherited from the CONTEXT.md scouting notes without independent re-verification. The four run directories (`stage0-smoke`, `stage0-pilot-seed{41,42,43}`) have byte-identical `train.log.jsonl` key sets (300 lines, single `event: "step"` type, 26 keys per record) and near-identical `config.yaml`/`status.json`/`summary.json` schemas, differing only in a small number of documented fields (`run.checkpoint.wall_clock_ceiling_s`, `run.recover_retries`, `run_name`, `seed`). `stage0-pilot-seed42/evaluation/metrics.json` is the **sole** evaluator output in the repository (1500-entry `per_trajectory` array, keys `eps_h`/`fidelity`/`id`/`variant` only — no per-trajectory SCS anywhere).

The most consequential finding is that **the locked framework specs do not define how to aggregate a per-trajectory ε_H/SCS quantity across a held-out model-evaluation population into one gate-rendering number** (§C). The `ctl_instruction.md` SI-DQA-003 clause defines the `max_t |...|` formula for admitting *individual raw trajectories into the training corpus* — a per-trajectory decision that needs no cross-trajectory aggregation. The one place in `ctl_instruction.md` that *does* aggregate an ε_H-family quantity across a trajectory population (the stage-ADVANCE "Energy-Conservation Check") uses **mean**, not max, a different time-selection (`t_final` vs `max_t`), and a different epsilon/threshold pair entirely. The "worst-trajectory (maximum)" convention that produced `eps_h = 237.2086` was written into the Phase-43 plan (`43-02-PLAN.md`) as a design decision, in direct response to a cross-AI review that explicitly flagged the aggregation rule as spec-absent (`43-REVIEWS.md`) — and that flag was never routed to `43-GAPS.md` or an owner sign-off record. This is a textbook STOP-protocol semantic gap; Phase 44 must record it, not resolve it.

A second, independently discovered, load-bearing fact not called out in 44-CONTEXT.md: **the held-out test/train/validation split is seed-dependent** (`pinn/data/splits.py::_partition_by_signature` seeds its RNG on `run.seed`). Seeds 41 and 43 each have their own `splits.json`, substantially different from seed 42's (verified via SHA-256 and a ~5,200-line diff each). This means DIAG-03's per-seed validation-loss comparisons are comparisons across **different held-out populations**, not the same population under three model fits — a caveat the planner should require DIAG-03 to state explicitly.

A third fact directly usable in DIAG-04: the angular-momentum loss weight (`lambda_l`) is **structurally pinned at 0.0 for all 300 steps in all four runs** — `pinn/training/config.py`'s `LossConfig` exposes only `lambda_e_max` as a settable field; `lambda_l_max` has no config surface at all and defaults to `0.0` in `ScheduledWeights.__init__`. The angular-momentum loss term never contributed gradient signal in any Stage-0 run examined here.

**Primary recommendation:** Plan DIAG-01/02/03 as three independent, deterministic Python scripts (using the `pinn-train` conda env's `python3`, which has `numpy` 2.4.6 but not `pandas`/`matplotlib`) that read the exact files enumerated in §A, write their outputs + a SHA-256/commit-hash pinning manifest under `evidence/`, and self-check their own re-derivability (assert `n==1500`, assert `recomputed_max == metrics.json.eps_h`, etc.) before DIAG-04 synthesizes them. Route D-07 to `.planning/milestones/v2.1-GAPS.md` as the first gap under D-16, using the exact evidentiary trail in §C — do not have any plan task "resolve" it.

## Architectural Responsibility Map

This phase has no browser/API/DB tiers — it is a linear artifact→analysis→report pipeline. The map below substitutes the phase-appropriate tiers for the standard web-app tiers, so the planner can sanity-check which layer owns which responsibility.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Reading `runs/*/logs/train.log.jsonl`, `validation.jsonl`, `status.json`, `summary.json`, `curriculum.jsonl`, `splits.json`, `config.yaml`, `evaluation/metrics.json` | Retained Artifacts (read-only source of truth) | — | These files are the ONLY inputs; nothing in `pinn/` is executed (SCOPE-22/23) |
| Percentile/mean/median computation, spike location, spread arithmetic | Analysis Scripts (deterministic derivation) | Retained Artifacts | Pure functions of the artifact bytes; must be re-runnable and produce byte-identical output on the same pinned inputs (D-02) |
| SHA-256 + commit-hash pinning, script+output retention | Evidence Directory (`.planning/phases/44-physics-gate-forensics/evidence/`) | Analysis Scripts | D-01/D-02; mirrors the Phase 43 `evidence/<topic>/README.md` convention (§F) |
| Reading `pinn/verification/gate_metrics.py`, `pinn/training/scheduled_weights.py`, `pinn/training/config.py` as factual-record-of-execution | Retained Artifacts | — | Explicitly NOT a grounding source for spec intent (CLAUDE.md, 44-CONTEXT.md); used only to state what code executed |
| Reading `ctl_instruction.md` / `pinn_architecture.md` for the D-07 gate-definition question | Locked Specs (read-only) | — | SCOPE-24 forbids editing; this phase only checks these files for silence/ambiguity |
| Hypothesis ranking, remedy-abstinence statement | Diagnosis Report (`44-DIAGNOSIS.md`) | Analysis Scripts, Retained Artifacts | Synthesizes DIAG-01..03 outputs; must cite, never invent (SCOPE-26) |
| D-07 (and any other source-silent adjudication call) | Gap Register (`44-GAPS.md` → `v2.1-GAPS.md`) | Diagnosis Report | STOP protocol; the report references the gap, the register owns the decision-routing |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `numpy` | 2.4.6 (already installed in `~/miniforge3/envs/pinn-train`) `[VERIFIED: python3 -c "import numpy"` in that env, this session`]` | Percentiles (p25/p50/p75/p90/p99 per D-04), mean/median, distribution arithmetic | Already a direct pip dependency of the `pinn-train` env (`environment.yml`/`requirements-lock.txt`); using it is NOT a new dependency under D-03 |
| `json` (stdlib) | 3.11 (interpreter) | Parsing all `.jsonl`/`.json` artifacts | Stdlib, zero-dependency |
| `hashlib` (stdlib) | 3.11 | SHA-256 pinning (D-02) | Stdlib |
| `subprocess` (stdlib) | 3.11 | `git rev-parse HEAD` for commit-hash pinning (D-02) | Stdlib; matches the existing codebase pattern in `pinn/verify.py`'s marker writer (bounded timeout, graceful degrade) |

### Supporting (available, not required)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `tensorboard` | 2.21.0 `[VERIFIED: python3 -c "import tensorboard"` in `pinn-train` env`]` | Parsing `tb/` event files via `tensorboard.backend.event_processing.event_accumulator.EventAccumulator` | Only if the planner wants the `residuals/bin_00..15` per-step histogram series (§A.4) — NOT required by DIAG-02's stated scope (all five loss terms + PHYS-05 weights are already in `train.log.jsonl`) |
| `PyYAML` | present (`environment.yml`) | Parsing `config.yaml` if a script needs the full config rather than the two already-diffed fields | Optional convenience; the differences across runs are small enough to diff by hand (§A.3) |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `numpy.percentile` | stdlib `statistics.quantiles` (Python ≥3.8) | Zero dependency at all, but a **different interpolation method** than numpy's default — p25/p50/p75/p90/p99 values can differ in the last few digits depending on method. Since numpy is already an existing dependency (not new under D-03), prefer `numpy.percentile` and document the interpolation method (`numpy` default is linear) explicitly in the evidence README so D-02 re-derivability is unambiguous. |
| `tensorboard.event_accumulator` | `tbparse` | `tbparse` is **NOT installed** in `pinn-train` `[VERIFIED: ModuleNotFoundError this session]` — would be a genuinely new dependency, forbidden by D-03. `tensorboard`'s own `event_accumulator` module is already installed and sufficient for scalar extraction. |

**No installation commands** — D-03 forbids new dependencies; every library above is already present in the `pinn-train` conda environment.

**Version verification:** confirmed this session via `~/miniforge3/envs/pinn-train/bin/python3 -c "import numpy; print(numpy.__version__)"` → `2.4.6`, and the analogous check for `tensorboard` → `2.21.0`. `pandas` and `matplotlib` are **absent** (`ModuleNotFoundError`) in that environment — do not plan any task that assumes them.

## Package Legitimacy Audit

**Not applicable.** Phase 44 installs zero external packages (D-03: "no new dependencies"). All libraries used (`numpy`, `tensorboard`, stdlib `json`/`hashlib`/`subprocess`) are already present in the `pinn-train` conda environment, verified by direct import in this session. No `npm view`/`pip index versions`/`package-legitimacy check` gate applies because nothing is being newly installed.

## Architecture Patterns

### System Architecture Diagram

```
runs/stage0-{smoke,pilot-seed41,pilot-seed42,pilot-seed43}/
    logs/train.log.jsonl ─┐
    validation.jsonl      ├──► [Analysis Script: loss_decomposition.py] ──► evidence/diag02/*.json ──┐
    status.json/          │        (per-run: dominant term per step-range,                          │
    summary.json/         │         PHYS-05 ramp schedule, spike location)                           │
    curriculum.jsonl      │                                                                          │
    config.yaml ──────────┘                                                                          │
                                                                                                        │
runs/stage0-pilot-seed42/evaluation/metrics.json ──► [Analysis Script: eps_h_distribution.py] ──► evidence/diag01/*.json ──┐
    (1500-entry per_trajectory array; sole gate rendering)                                                                 │
                                                                                                                             │
43-CALIBRATION.md, 38-VERIFICATION.md (cited, not re-run) ──► [Analysis Script: seed_band.py] ──► evidence/diag03/*.json ──┤
                                                                                                                             │
ctl_instruction.md, pinn_architecture.md, 43-REVIEWS.md, gate_metrics.py (read-only, D-07 check) ─────────────────────────►│
                                                                                                                             ▼
                                                                                                          [Synthesis: 44-DIAGNOSIS.md]
                                                                                                          ranks ≥4 hypotheses,
                                                                                                          cites DIAG-01..03,
                                                                                                          abstains from remedy
                                                                                                                             │
                                                                                                                             ▼
                                                                                          any source-silent call ──► 44-GAPS.md ──► v2.1-GAPS.md
```

Every arrow above is a read; nothing writes back into `runs/`, `pinn/`, or the framework specs.

### Recommended Evidence Directory Structure

```
.planning/phases/44-physics-gate-forensics/evidence/
├── manifest.json          # D-02: SHA-256 of every input file read + `git rev-parse HEAD`
├── diag01/
│   ├── eps_h_distribution.py       # script (idempotent, no args needed — paths are hardcoded to the pinned run)
│   └── eps_h_distribution.json     # output: distribution stats, uniform-vs-tail verdict, variant/fidelity breakdown
├── diag02/
│   ├── loss_decomposition.py
│   └── loss_decomposition.json     # per-run: dominant term per step-range, spike step/term/grad_norm, PHYS-05 schedule
├── diag03/
│   ├── seed_band.py
│   └── seed_band.json              # per-seed trend/spread + splits.json seed-dependence caveat + Phase-38 rung citation
└── README.md               # Phase-43-style prose wrapper: reproduction boundary, exact commands, links to the JSON outputs
```

### Pattern 1: Pinned, self-checking analysis script

**What:** Each script hardcodes its input file paths (no CLI args needed — the inputs are fixed, already-retained artifacts), computes its statistics, asserts a small set of self-check invariants before writing output, and records the SHA-256 of every file it read plus `git rev-parse HEAD` in its own output JSON.
**When to use:** All three DIAG-01/02/03 scripts.
**Example:**
```python
# Source: this session's direct verification against runs/stage0-pilot-seed42/evaluation/metrics.json
import hashlib, json, subprocess

def sha256_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def commit_hash():
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=10
        ).stdout.strip()
    except Exception:
        return None  # degrade gracefully — matches pinn/verify.py's marker-writer pattern

path = "runs/stage0-pilot-seed42/evaluation/metrics.json"
data = json.load(open(path))
per_traj = data["per_trajectory"]
assert len(per_traj) == 1500, f"expected 1500 trajectories, got {len(per_traj)}"
assert all(set(e.keys()) == {"eps_h", "fidelity", "id", "variant"} for e in per_traj)

eps_h_values = [e["eps_h"] for e in per_traj]
recomputed_max = max(eps_h_values)
assert recomputed_max == data["eps_h"], (
    f"recomputed max {recomputed_max} != artifact top-level eps_h {data['eps_h']}"
)
```

### Anti-Patterns to Avoid

- **Assuming `python3` on PATH has numpy:** the system `python3` (`/opt/homebrew/bin/python3`, 3.14.6) has **no** numpy `[VERIFIED this session]`. All scripts must be invoked as `~/miniforge3/envs/pinn-train/bin/python3 <script>.py` (the project's own established convention — see `evidence/pilot/README.md` from Phase 43, which invokes `~/miniforge3/envs/pinn-train/bin/python -m pinn.train ...` directly by absolute path, not `conda activate`).
- **Treating `pinn/verification/gate_metrics.py`'s "worst-trajectory (maximum)" comment as spec authority:** it documents what executed, not what the spec requires (§C). Citing it as "the code says max is correct" would be exactly the kind of grounding-source violation the CLAUDE.md STOP protocol forbids.
- **Pooling `stage0-smoke` into the seed-41/42/43 population for spread statistics:** D-10 requires it stay a separate trace; it also happens to share `splits.json` with `pilot-seed42` (both configured with `run.seed: 42`) but differs in `wall_clock_ceiling_s` and has 2 curriculum-disposition events (a mid-run HALT at step 158 from a documented SIGTERM interrupt + `--resume latest`, per `STATE.md`'s Phase-43 note) vs. the pilots' single terminal HALT.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Percentile computation | A custom interpolation/percentile function | `numpy.percentile` (already installed) | Numpy's percentile implementation is well-tested and its interpolation method is document-able in one line; a hand-rolled version risks an off-by-one or interpolation mismatch that silently changes p90/p99 by a meaningful amount on only 1,500 samples |
| TensorBoard event parsing (if ever needed) | A raw protobuf reader for `events.out.tfevents.*` | `tensorboard.backend.event_processing.event_accumulator.EventAccumulator` (already installed) | The tfevents format is a length-prefixed, CRC-checked protobuf stream; hand-parsing it is exactly the kind of "deceptively complex" problem this heuristic exists to flag, and the correct reader is already a dependency |
| SHA-256/commit pinning | A bespoke manifest format | Plain `hashlib.sha256(...).hexdigest()` + `git rev-parse HEAD`, mirroring the Phase 43 precedent (`43-VERDICT.md`'s "Preserved artifact identities" table; `pinn/verify.py`'s marker writer) | Reinventing this would diverge from the project's own established re-derivability convention for no benefit |

**Key insight:** everything this phase needs is either stdlib or already an installed, load-bearing dependency of the training pipeline itself (`numpy`, `tensorboard`). There is no library gap here — the risk is entirely in schema/interpretation mistakes (wrong interpreter, wrong step-indexing convention, wrong assumption about split identity across seeds), not missing tooling.

## Common Pitfalls

### Pitfall 1: Wrong Python interpreter silently breaks numpy-dependent scripts
**What goes wrong:** A script written and tested with `python3` on PATH (system Python 3.14.6, Homebrew) raises `ModuleNotFoundError: No module named 'numpy'`.
**Why it happens:** The project's actual training/analysis environment is the separate conda env `~/miniforge3/envs/pinn-train` (Python 3.11.15); it is not the same interpreter as bare `python3`.
**How to avoid:** Every acceptance criterion and every script invocation must use the absolute path `~/miniforge3/envs/pinn-train/bin/python3`, matching the Phase 43 evidence precedent.
**Warning signs:** `ModuleNotFoundError` for numpy/torch/tensorboard/h5py/yaml at script run time.

### Pitfall 2: Off-by-one between `status.json`'s `step` and `train.log.jsonl`'s `step`
**What goes wrong:** Cross-referencing "the last logged step" between artifact types produces an inconsistent number.
**Why it happens:** `train.log.jsonl` steps are 1-indexed (`1..300` `[VERIFIED]`); `status.json.step` for a finished run is `299` (0-indexed) while `status.json.epoch` is `300` `[VERIFIED, all 4 runs]`.
**How to avoid:** Always use `train.log.jsonl`'s own `step` field as the canonical step index for DIAG-02; treat `status.json.step`/`epoch` only as corroborating metadata, and note the indexing difference explicitly if both are quoted in the same table.
**Warning signs:** An analysis that reports "step 299" as the final step when `train.log.jsonl` plainly ends at step 300.

### Pitfall 3: Treating "~3.7e9" as one shared cross-run spike location
**What goes wrong:** Searching all four logs for a single step where `total ≈ 3.7e9` finds it only in `stage0-pilot-seed42` (step 100, `total = 3,734,660,096`); the other three runs peak at different steps and magnitudes (`smoke` step 194 → 4.61e9; `seed41` step 123 → 6.08e9; `seed43` step 169 → 3.83e9), all `[VERIFIED]` this session.
**Why it happens:** REQUIREMENTS.md/ROADMAP.md's "~3.7e9" figure appears to describe the phenomenon generically (an order-of-magnitude description of an early-training loss transient), not a single located event common to all runs.
**How to avoid:** DIAG-02 should report all four per-run peaks independently (consistent with D-10's "smoke is a separate trace" requirement), not search for one canonical "the spike."
**Warning signs:** A script that raises/reports "no spike found near 3.7e9" for seed41, seed43, or smoke because it searched too narrow a tolerance band.

### Pitfall 4: Assuming the held-out split is identical across seeds
**What goes wrong:** Comparing `final_val_loss` magnitudes across seed41/42/43 as if they were all evaluated on the same held-out validation subset.
**Why it happens:** `pinn/data/splits.py::_partition_by_signature` seeds its RNG on `run.seed` (`np.random.default_rng(np.random.SeedSequence([seed, signature_index]))`); each run's `splits.json` is a genuinely different train/validation/test partition. `[VERIFIED]`: `runs/stage0-pilot-seed41/splits.json` and `.../seed43/splits.json` each differ from `.../seed42/splits.json` by ~5,200 diff-lines (out of the whole file); `stage0-smoke` and `stage0-pilot-seed42` share a byte-identical `splits.json` (SHA-256 `5846ae5b...` for both) because both configs set `run.seed: 42`.
**How to avoid:** DIAG-03 should state this caveat explicitly: per-seed validation *trend direction* (improving/worsening within that seed's own run) is a valid same-seed longitudinal signal; cross-seed validation-loss *magnitude* comparisons implicitly compare different held-out populations, not just different model fits on one fixed population.
**Warning signs:** A DIAG-03 claim like "seed43's validation loss is 4x worse than seed41's" stated without the population caveat.

### Pitfall 5: Conflating the SI-DQA-003 data-admission gate with the Phase-43 held-out model-evaluation gate
**What goes wrong:** Citing `ctl_instruction.md` lines 565-589 as if it defines how `metrics.json`'s single `eps_h`/`scs` number should be aggregated across the 1,500 held-out trajectories.
**Why it happens:** Both use the identical-looking formula shape (`eps_H = max_t |(H(t)-H(0))/H(0)|`, `SCS = log10(eps_H)`, reject if `SCS > -5`) — but the SI-DQA-003 clause is a **per-trajectory admission decision** for raw Brutus output entering the training corpus (each trajectory gets its own independent accept/reject; no cross-trajectory aggregation is needed or defined there). The Phase-43 gate applies the same per-trajectory formula to **model-predicted** trajectories and then aggregates 1,500 of them into ONE number — a step the SI-DQA-003 clause never addresses.
**How to avoid:** Cite `ctl_instruction.md:565-589` only for the per-trajectory formula and threshold values (which the Phase-43 evaluator code does correctly reuse); do not cite it as authority for the "max across the test set" aggregation choice — that choice is source-silent (§C).
**Warning signs:** A DIAG-04 or `44-DIAGNOSIS.md` sentence that reads "the spec requires worst-case aggregation" without qualification.

### Pitfall 6: Assuming `tb/` adds required DIAG-02 signal
**What goes wrong:** Spending a plan task parsing TensorBoard event files under the assumption they're needed to satisfy DIAG-02.
**Why it happens:** `tb/` does exist and does carry more scalar tags than `train.log.jsonl` (`residuals/bin_00`..`bin_15`, a 16-bin residual-distribution histogram-as-scalars, `[VERIFIED]` via `tensorboard.backend.event_processing.event_accumulator` this session) — but every tag DIAG-02 actually requires (`loss_data`/`loss_ic`/`loss_phys`/`loss_energy`/`loss_angmom`, `lambda_data`/`lambda_ic`/`lambda_phys`/`lambda_e`/`lambda_l`, `grad_norm`, `lr`) is already present, byte-for-byte reconcilable, in `train.log.jsonl`.
**How to avoid:** Treat `tb/` parsing as optional, zero-new-dependency bonus material (via the already-installed `tensorboard` package) only if the planner independently decides the residual-bin histogram adds discriminating value to DIAG-04 — not as a required DIAG-02 input.
**Warning signs:** A plan task titled "parse TensorBoard events for DIAG-02" when the required fields are already in the JSONL.

### Pitfall 7: Over-generalizing the Phase-38 overfit rung
**What goes wrong:** Citing the `L0/Lf = 1097.6×` overfit-ratio PASS as if it were run under the same conditions as the Stage-0 pilots.
**Why it happens:** The overfit rung (`38-VERIFICATION.md` Rung 4) used a **fixed placeholder** `tau_ic13(u_n) = [2u_n−1, zeros(13)]` — not real per-trajectory IC13 metadata — and a different optimizer configuration (Adam `lr=1e-4`, single trajectory, early-broke at 176 of a 5000-step cap) `[VERIFIED, 38-VERIFICATION.md:77-88]`.
**How to avoid:** Cite it strictly as machinery-integrity evidence ("the network architecture and training loop CAN drive data loss down by three orders of magnitude on one trajectory") per D-12/DIAG-03's own framing — not as evidence that the Stage-0 pilot's full-input-vector, 32-identity, 300-Adam-step configuration should behave similarly.
**Warning signs:** A DIAG-03/04 sentence implying the overfit rung "proves" the pilot's failure is purely budget-limited.

## Runtime State Inventory

Not applicable — Phase 44 is not a rename/refactor/migration phase. No stored data, live service config, OS-registered state, secrets, or build artifacts are being renamed or migrated. (Omitted per the template's own trigger condition.)

## Code Examples

### Loading a run's step log and locating the peak-loss step (DIAG-02)
```python
# Source: this session's direct verification against runs/stage0-pilot-seed42/logs/train.log.jsonl
import json

def load_steps(run_name):
    path = f"runs/{run_name}/logs/train.log.jsonl"
    return [json.loads(line) for line in open(path)]

def peak_step(records):
    return max(records, key=lambda r: r["total"])

recs = load_steps("stage0-pilot-seed42")
peak = peak_step(recs)
# peak["step"] == 100, peak["total"] == 3734660096.0, peak["loss_phys"] == 3734595072.0
# peak["grad_norm"] == 70647606673408.0, peak["finite"] is True, peak["nonfinite_keys"] == []
```

### Computing the ε_H distribution (DIAG-01)
```python
# Source: this session's direct verification against runs/stage0-pilot-seed42/evaluation/metrics.json
import json
import numpy as np

data = json.load(open("runs/stage0-pilot-seed42/evaluation/metrics.json"))
eps_h = np.array([e["eps_h"] for e in data["per_trajectory"]])
stats = {
    "min": float(eps_h.min()),
    "p25": float(np.percentile(eps_h, 25)),
    "p50": float(np.percentile(eps_h, 50)),
    "p75": float(np.percentile(eps_h, 75)),
    "p90": float(np.percentile(eps_h, 90)),
    "p99": float(np.percentile(eps_h, 99)),
    "max": float(eps_h.max()),
    "mean": float(eps_h.mean()),
    "frac_exceeding_1e5": float((eps_h > 1e-5).mean()),
}
# Verified this session: min=0.9741251227996501, p50=2.232675867436938 (~2.234),
# max=237.2086056078468 (exactly equals data["eps_h"]), mean=5.622187097745829,
# frac_exceeding_1e5 == 1.0 (1500/1500) -> D-05's uniform-failure criterion is satisfied
# by construction (min already exceeds the reject threshold by ~5 orders of magnitude).
```

### PHYS-05 scheduled-weight ramp check (DIAG-02)
```python
# Source: this session's direct verification, all four runs
import json
recs = [json.loads(l) for l in open("runs/stage0-pilot-seed42/logs/train.log.jsonl")]
first_full_ramp_step = next(r["step"] for r in recs if r["lambda_phys"] == 1.0)
# == 31 for all four runs (smoke, seed41, seed42, seed43)
lambda_l_values = sorted(set(r["lambda_l"] for r in recs))
# == [0.0] for all four runs -- angular-momentum weight never leaves zero
```

## State of the Art

Not applicable in the conventional sense (this is not a library/framework research question). One relevant "convention changed" note: the Phase-43 evaluator's "worst-trajectory (maximum)" aggregation is a **Phase-43-local convention**, introduced to close a cross-AI-review-flagged spec gap, not a pre-existing locked convention from `ctl_instruction.md`/`pinn_architecture.md` — see §C for the full trail. If the eventual owner/ERW resolution changes this convention, `pinn/verification/gate_metrics.py::aggregate_test_eps_h` (currently hardcoded to `max()`) is the single point of change (informational only — Phase 44 does not touch it, SCOPE-24/26).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | REQUIREMENTS.md/ROADMAP.md's "~3.7e9" warmup-spike figure is a representative/approximate description of a recurring per-run phenomenon (four distinct peaks: 3.73e9 / 4.61e9 / 6.08e9 / 3.83e9), rather than a literal reference to one specific step shared by all four runs | §B, Pitfall 3 | Low — if the planner intended DIAG-02 to report exactly one canonical spike, they will find four instead; the underlying data is unambiguous (all four are directly verified), only the *interpretation* of the requirement's wording is an inference. Recommend DIAG-02 report all four explicitly regardless. |

**All other claims in this research are `[VERIFIED]`** — confirmed by direct file read, direct code read, or a computed value produced in this session against the actual artifacts. The single item that is deliberately `[SILENT]` (not `[ASSUMED]` — an assumption fills a gap; this finding documents that the gap exists) is D-07 (§C): the specs and the Phase-43 record do not state which statistic the held-out gate is defined over. That is not a risk to hedge — it is the exact governance-gap Phase 44 must record.

## Open Questions

1. **Does DIAG-02 want one canonical "the spike" narrative, or four independent per-run peak-attribution entries?**
   - What we know: four distinct peaks exist, at different steps and magnitudes, all fully attributable to `loss_phys` with a simultaneous `grad_norm` spike to ~1e13-1e14, always `finite: true`.
   - What's unclear: whether the planner should frame this as "the same phenomenon recurring four times" or "four independent single-run events."
   - Recommendation: report all four independently (matches D-10's "smoke stays separate" spirit); a DIAG-04 hypothesis can still note the *pattern* (loss_phys-dominated, post-ramp, always finite) as a cross-run commonality without claiming it's one event.

2. **Does the `ctl_instruction.md:572` instruction to "Store per-trajectory eps_H, SCS, and band label" (for the SI-DQA-003 data-admission gate) have any bearing on why Phase 43's held-out `metrics.json` lacks per-trajectory SCS?**
   - What we know: the SI-DQA-003 clause is about admitting raw Brutus trajectories into the corpus, not about the held-out model-evaluation gate; the two are formally distinct per `ctl_instruction.md:578-580`'s own "same glyph, different quantity" callout.
   - What's unclear: whether the *absence* of per-trajectory SCS in the Phase-43 evaluator output reflects a deliberate scope decision (evaluation only ever needed the aggregate) or an oversight relative to the general "store per-trajectory X/SCS/band" pattern established elsewhere in the pipeline.
   - Recommendation: DIAG-01 should state plainly that only `eps_h` is available per-trajectory (§A.2, §C.1) and not speculate on why; this is adjacent to, but not the same governance question as, D-07.

3. **`runs/probe-run/` and `runs/stage0-smoke-diag/`** — both exist on disk with apparently complete artifact sets (confirmed present this session) but are explicitly out of the named DIAG-02/03 scope per 44-CONTEXT.md. Not analyzed further in this research; raise with the owner if the planner believes either is needed (44-CONTEXT.md already flags this as a deferred item, not newly discovered here).

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `~/miniforge3/envs/pinn-train/bin/python3` | All DIAG-01/02/03 scripts | ✓ | 3.11.15 | — |
| `numpy` (in `pinn-train` env) | Percentile/mean/median computation (D-04) | ✓ | 2.4.6 | `statistics.quantiles` (stdlib) if the planner prefers zero external deps — note the differing interpolation method |
| `tensorboard` (in `pinn-train` env) | Optional `tb/` scalar parsing | ✓ | 2.21.0 | Not needed — all DIAG-02-required fields are in `train.log.jsonl` |
| System `python3` (`/opt/homebrew/bin/python3`) | — | ✓ but **wrong interpreter** | 3.14.6, no numpy/pandas/matplotlib | Do not use; always invoke the `pinn-train` env's `python3` by absolute path |
| `pandas` | Not required by any DIAG task | ✗ (absent in `pinn-train`) | — | Use `numpy`/stdlib instead; do not plan any task requiring pandas |
| `matplotlib` | Not required (no plots requested by DIAG-01..04) | ✗ (absent in `pinn-train`) | — | If the planner wants a visual, this would be a genuinely new dependency — flag as a discretionary scope addition, not assumed |
| `tbparse` | Not required (tensorboard's own `event_accumulator` suffices) | ✗ (absent) | — | Do not install; use `tensorboard.backend.event_processing.event_accumulator` instead |
| `git` (`git rev-parse HEAD`) | D-02 commit-hash pinning | ✓ | — (system git) | Already used elsewhere in the codebase (`pinn/verify.py`) with a 10s-timeout graceful-degrade pattern; reuse it |

**Missing dependencies with no fallback:** none — every required capability is already satisfied by the `pinn-train` environment.

**Missing dependencies with fallback:** `pandas`/`matplotlib`/`tbparse` are absent but not needed; `numpy` has a stdlib fallback (`statistics.quantiles`) if the planner wants to eliminate even the existing-dependency usage, though this is not required by D-03 (numpy is already installed, not new).

## Validation Architecture

Phase 44 produces **analysis artifacts** (Python scripts + their JSON/markdown outputs + a pinning manifest), not application code with a conventional test suite. Validation here means: (1) every number in `44-DIAGNOSIS.md` can be mechanically regenerated from the pinned inputs, and (2) the scripts self-check their own output shape before anything is written.

### Re-derivability check (D-02)

A re-derivability claim is checked by:
1. Recording, in `evidence/manifest.json`, the SHA-256 of every input file the script reads (`runs/stage0-*/logs/train.log.jsonl`, `.../validation.jsonl`, `.../status.json`, `.../summary.json`, `.../curriculum.jsonl`, `.../splits.json`, `.../config.yaml`, `runs/stage0-pilot-seed42/evaluation/metrics.json`) plus `git rev-parse HEAD` at the time of the run.
2. Re-running the exact script (`~/miniforge3/envs/pinn-train/bin/python3 evidence/diagNN/<script>.py`) against a checkout at the pinned commit hash and confirming the SHA-256 of every input file is unchanged (a changed hash means the "same" analysis is no longer re-derivable against the original evidence — it must be re-run and re-pinned, not silently trusted).
3. Confirming the script's own JSON output is byte-identical (or, for floating-point values, identical to full `repr()` precision) across the two runs.

### Mechanical verification that "every number is regenerable" (D-02)

Each script embeds a small set of **self-check assertions** that must pass before it writes output — these are the automated proxy for "this number is real, not transcribed by hand":

```python
assert len(per_trajectory) == 1500
assert max(e["eps_h"] for e in per_trajectory) == metrics_json["eps_h"]   # D-07's own premise, re-verified on every run
assert set().union(*(e.keys() for e in per_trajectory)) == {"eps_h", "fidelity", "id", "variant"}
assert len(train_log_records) == 300
assert {r["step"] for r in train_log_records} == set(range(1, 301))
```

A script that fails any of these assertions must halt (fail-closed) rather than write a plausible-looking but unverified number into `evidence/`. The evidence README should show the exact assertion list alongside a note that it passed on the pinned commit.

### What CANNOT be validated in-phase (must be asserted by review instead)

- **Whether `max` is the spec-intended gate statistic (D-07).** This is not a re-derivability question — it's a semantics question the sources do not answer. No script can validate it; it can only be routed to the gap register. Review (human or ERW) must confirm the gap entry accurately represents the evidentiary trail in §C before it's considered "surfaced correctly."
- **Whether the ranked DIAG-04 hypotheses are causally correct.** DIAG-04 explicitly proposes discriminating tests (D-14) rather than running them (SCOPE-23); there is no in-phase mechanism to confirm which hypothesis is right — only that each hypothesis has honestly-cited supporting AND contradicting evidence, and that a decisive-but-unexecuted test is named for each.
- **Whether the `residuals/bin_*` TensorBoard series would have changed the DIAG-02 conclusions.** Not computed in this phase (Pitfall 6); if the planner scopes it in, it becomes a new, separately-validatable analysis, not a retroactive check on the DIAG-02 conclusions already drawn from `train.log.jsonl`.
- **Whether the seed-dependent split (Pitfall 4) materially changes the DIAG-03 seed-band interpretation.** This phase can only surface the caveat, not quantify its effect (quantifying it would require re-partitioning or re-evaluating, which is out of scope / budget-exhausted for evaluation, and simply re-describing the same three seeds' own validation trends for training-set partitioning does not require new evaluation runs — but a rigorous "how much does the split difference matter" analysis is a discretionary scope question for the planner, not assumed here).

### Sampling rate

- **Per script:** run its own self-check assertions (above) every time it executes — this is the "quick run."
- **Per DIAG deliverable (01/02/03):** re-run against the pinned manifest once before `44-DIAGNOSIS.md` cites its numbers, confirming SHA-256 match.
- **Phase gate:** before `/gsd-verify-work`, re-run all three scripts end-to-end against the evidence manifest and confirm every number quoted in `44-DIAGNOSIS.md` traces to a script output (not a hand-transcribed value).

### Wave 0 gaps

- No test framework exists for this phase (analysis scripts, not application code) — none is needed; the self-check assertions embedded in each script ARE the test surface.
- `evidence/manifest.json` does not exist yet — created by the first analysis script's pinning step.

## Security Domain

Phase 44 has no network-facing surface, no authentication, no user input, and no persistence beyond writing files into a git-tracked evidence directory that the phase itself owns. Most ASVS categories do not apply to a local, read-only, single-operator analysis phase.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No auth surface |
| V3 Session Management | No | No sessions |
| V4 Access Control | No | Single local operator; file permissions inherited from the repo |
| V5 Input Validation | Yes (narrow) | Scripts must assert artifact schema (key sets, `n==1500`, `step` range) before trusting values, per the self-check pattern above — this protects re-derivability claims from silent schema drift, not from adversarial input |
| V6 Cryptography | Yes (narrow) | SHA-256 (`hashlib.sha256`, stdlib) for artifact pinning per D-02 — a re-derivability/integrity control, not a confidentiality control; no encryption need exists here |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Silent schema drift (an artifact's key set changes between when this research ran and when a plan task executes) | Tampering (of trust assumptions, not malicious) | The self-check assertions above (Validation Architecture) fail closed on any unexpected key set or count, rather than silently computing over malformed data |
| A future re-run of an analysis script against a since-modified `runs/` tree silently produces different numbers than what's cited in `44-DIAGNOSIS.md` | Repudiation (of the original evidentiary claim) | SHA-256 pinning (D-02) makes any drift immediately detectable — a hash mismatch is the tamper-evidence signal |

## Sources

### Primary (HIGH confidence — direct file/code inspection, this session)
- `runs/stage0-{smoke,pilot-seed41,pilot-seed42,pilot-seed43}/logs/train.log.jsonl` — line counts, event types, exact key set, step range (all `[VERIFIED]`)
- `runs/stage0-{smoke,pilot-seed41,pilot-seed42,pilot-seed43}/validation.jsonl`, `status.json`, `summary.json`, `curriculum.jsonl`, `splits.json`, `config.yaml` — schema, per-run diffs
- `runs/stage0-pilot-seed42/evaluation/metrics.json`, `evaluation-receipt.json`, `metrics.md` — exact schema, computed distribution stats, the D-07 load-bearing quote (metrics.md:15)
- `pinn/verification/gate_metrics.py` (lines 180-288), `pinn/training/scheduled_weights.py` (lines 91-230), `pinn/training/config.py` (LossConfig, ~line 505) — read as factual record of execution only, per CLAUDE.md's explicit non-grounding rule
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` (lines 545-604, 1900-1999) — SI-DQA-003 admission-gate clause and stage-ADVANCE energy-conservation criterion, both searched exhaustively for "held-out"/"aggregate"/"test set" language
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (lines 520-620, 990) — training-loss ε_H denominator-floor definition, confirmed distinct from the validation-gate ε_H
- `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md` — full raw/spread tables quoted
- `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md` — owner-signed verdict text, evidence matrix
- `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-02-PLAN.md`, `43-02-SUMMARY.md`, `43-REVIEWS.md`, `43-GAPS.md` — the D-07 evidentiary trail (design-intent-as-plan-text, cross-AI review flag, absence from the gap register)
- `.planning/milestones/v2.0-phases/38-pinn-model-rebuild-from-specs-fut-01/38-VERIFICATION.md` (lines 55-113) — Rung 4 overfit numbers and placeholder-IC13 caveat
- `.planning/milestones/v2.0-MILESTONE-AUDIT.md` — W-1/W-2/W-3 warning text
- Direct environment probes this session: `python3 --version`/`numpy`/`pandas`/`matplotlib`/`tensorboard`/`tbparse` import checks against both the system Python and `~/miniforge3/envs/pinn-train/bin/python3`
- `pinn/data/splits.py` (lines 356-654) — confirms `run.seed`-dependent split partitioning, independently discovered and verified this session

### Secondary (MEDIUM confidence)
- None — no web/external research was performed for this phase; every claim above was verified directly against repository files or computed values.

### Tertiary (LOW confidence)
- None.

## Metadata

**Confidence breakdown:**
- Artifact schema (§A): HIGH — every key set, line count, and computed statistic was produced directly against the actual files in this session.
- Warmup-spike attribution (§B): HIGH — all four peaks located and their full context (loss terms, grad_norm, lr, finite flags, PHYS-05 weight state) read directly from the JSONL.
- D-07 gate-statistic question (§C): HIGH confidence that the sources are silent/ambiguous (thoroughly searched and cross-checked); the underlying semantic question itself remains, by design, unresolved — that is the correct outcome, not a confidence gap.
- DIAG-03 anchors (§D): HIGH — all quoted numbers read directly from `43-CALIBRATION.md`/`38-VERIFICATION.md`; the seed-dependent-split finding is an independently verified, code-grounded addition.
- Environment/tooling (§E): HIGH — every package-presence claim was tested by direct import in the actual `pinn-train` environment this session.

**Research date:** 2026-07-23
**Valid until:** Effectively indefinite for the artifact-schema claims (the retained `runs/` artifacts and `.planning/milestones/v2.0-*` records are frozen historical evidence, SCOPE-22/23 forbid regenerating them). Re-verify the environment-availability claims (§E) if the `pinn-train` conda environment is rebuilt or `requirements-lock.txt` is regenerated before Phase 44 executes.
