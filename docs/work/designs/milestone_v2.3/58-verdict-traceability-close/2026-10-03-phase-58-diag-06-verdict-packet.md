---
status: active
purpose: design
created: 2026-10-03
milestone: v2.3
phase: 58-verdict-traceability-close
retirement_trigger: the owner's checkpoint-⑤ verdict is recorded in Phase 58 artifacts and the v2.3 milestone closes
---

# Phase 58 — DIAG-06 verdict packet (owner checkpoint ⑤)

**Audience:** the project owner, deciding the v2.3 verdict.
**This document is:** the evidence the verdict rests on, in plain language
first, plus one new read-only measurement.
**This document is not:** a remedy, a recipe change, a ranking of next steps,
or authorization for any run. Under SCOPE-37 nothing here may be tuned without
a new owner decision.

If anything here conflicts with a committed Phase-57 artifact, the committed
artifact wins.

---

## 1. What you are being asked to decide

ROADMAP Phase 58 asks for three things:

1. **The verdict: go, adjust, or rethink.** Stage-1+ and PLAT-01..07 reopen
   only on `go`. The roadmap's declared terminal state says that because the
   front failed to advance, the verdict is to be rendered **`rethink`-flavored**
   on this evidence (Phase 58 SC3). That pre-commitment was written before any
   run, so this outcome would be a clean close, not a drift.
2. **Requirement dispositions** for RUN-04, RUN-05, and EVAL-02. None is
   satisfied (section 2). In v2.2 the owner recorded the equivalent
   requirements as "closed incomplete" (RUN-01/02) and "not attempted"
   (RUN-03/EVAL-01).
3. **Where the next milestone routes** (Phase 58 SC2). Section 6 lists the open
   questions the evidence leaves, without ranking them.

## 2. What happened (facts)

- **Generations 1–6** never produced a usable band. In order:
  - a memory-guard block (generation 1);
  - an interrupted smoke (generation 2);
  - a sandbox block (generation 3);
  - an operator stop with no resumable checkpoint (generation 4);
  - a completed smoke (generation 5);
  - a graded seed 42 that died silently at step 513 (generation 6).

  Each continuation was owner-ruled (GAP-57-02..12). None was a scientific
  result.
- **Generation 7** (HEAD `629b1a6c`, every process launched detached):
  - the smoke finished;
  - the seed-42 setup check passed (identical splits, `s_h`, and `n_train`);
  - graded seed 42 tripped invariant B at step 951. The frozen monitor's
    high-water front had stood at 2 since step 450, giving 501 steps without
    an advance against N=500.
- Under the pre-registered rule, seeds 41 and 43 were not launched, and the
  single held-out evaluation remains **unspent**
  (`no-candidate.json`; verifier `final` → `FINAL-UNSPENT-OK`).

## 3. The new measurement: was it a near miss?

To tell "almost made it" apart from "nowhere close", the frozen monitor was
re-scored on every retained checkpoint. The replay used the same production
code the invariant-B guard reads, on the run's own MPS/float32 runtime, and
wrote nothing to the run directories (method in Appendix A). It reproduces the
guard's own state: front 2 at step 951.

**How to read it.** Bin `n` "counts" once the normalized residuals before it
sum to less than ln 2 ≈ 0.693. Its weight is `w_n = exp(−sum)`, and the front
is the last bin with `w_n > 0.5`. To move from front `k` to `k+1`, the sum over
bins `0..k` must fall below 0.693.

| Checkpoint | Monitor front | Sum that must fall below 0.693 | Weight on the next bin (needs > 0.5) |
|---|---|---|---|
| gen 7, step 0 (init) | 0 | bin 0 = 0.875 | 0.42 |
| gen 7, step 900 (`best.pt`) | **1** (back from 2) | bins 0–1 = 0.728 | 0.48 |
| gen 7, step 931 | 2 | bins 0–2 = 1.192 | 0.30 |
| gen 7, step 941 | 2 | bins 0–2 = 1.182 | 0.31 |
| gen 7, step 951 (trip) | 2 | bins 0–2 = **1.189** | **0.30** |
| gen 6, steps 490 / 500 / 510 | 1 (back from 2) | bins 0–1 = 0.954 / 0.805 / 0.789 | 0.39 / 0.45 / 0.45 |

**Reading (arithmetic, not inference about cause):**

- **Not a near miss.** At the trip, crossing into bin 3 needed the normalized
  residual over bins 0–2 to fall about 42% (1.19 → 0.69). That sum was flat
  over the last 20 steps (1.192 → 1.189).
- **The front oscillates; it does not creep.** In both runs the monitor front
  moved back and forth between 1 and 2. Invariant B counts only new high-water
  marks, so returning to 2 never counted as progress.
- **Total progress was modest.** From initialization to step 951 the
  per-bin normalized residuals in bins 0–5 fell 3.5×, 2.7×, 3.2×, 2.2×, 2.1×,
  and 1.5×. The median over all 16 bins fell 1.7× (1.11 → 0.66). The raw bin-0
  residual went from 1.7 × 10¹⁰ to 4.9 × 10⁹.
- **Distance to a full front.** Reaching bin 15 needs the sum over bins 0–14
  below 0.693. Bins 0–5 alone sum to 3.88 at step 951, so they would need at
  least a further 5.6× reduction before the other bins are counted.

## 4. What v2.3 established

| Finding | Basis | Strength |
|---|---|---|
| The R_ref normalization fixed the v2.2 failure mode. Weights are no longer pinned at zero, and the front left the floor (0→1 in the smoke at step 93; 0→2 in graded seed 42). | GATE-04 PASS; generation-7 telemetry; this replay | Established |
| The recipe does not keep the front advancing in the window: it stalls or oscillates at index 1–2. | Two independent runs (gens 6 and 7) stalled at the same index; trip at step 951 | Established for this recipe and seed |
| Per-bin progress slows: the front reached 1 at step ~93 and 2 at step ~450, then nothing by 951. | Ledger and guard state | Established (one run) |
| The 500-step window from 450 to 950 coincided with the cosine learning-rate schedule falling about 100× (5.8×10⁻⁴ → 6×10⁻⁶). | Training log | Fact. Whether it caused the stall is **unknown** |
| A front measured against R_ref tracks improvement relative to initialization, not physical accuracy. A full front means about a 20× residual reduction, with the raw residual still about 10⁹. | Arithmetic from the ratified formula | Arithmetic consequence, not a measured finding |

## 5. What is not known

- Why per-bin progress slows: whether through the optimization landscape, the
  learning-rate schedule, the SIREN starting frequency `ω₀ = 30`, or the step
  budget.
- Whether a longer run, or one without the learning-rate decay inside the
  window, would advance the front further. The one-run evidence cannot say.
- Whether an R_ref-relative front is the right success criterion for a model
  meant to satisfy the physics, or whether the criterion should be tied to an
  absolute accuracy.
- Seeds 41 and 43 were never run, so whether this behavior holds across seeds
  is unmeasured.

## 6. Open questions for the next milestone (unranked)

These are the questions the evidence leaves. They are not remedies, and none
is recommended over another.

- Is the coupling between the invariant-B window and a learning-rate schedule
  that decays inside it a design flaw, and how should the two relate?
- Should the causal-front criterion measure progress relative to initialization
  (R_ref) or absolute physical accuracy?
- Is the SIREN initialization scale `ω₀ = 30` (with the deferred power-skip
  ablation) the root of the slow pace?
- What Stage-0 step budget is realistic for the front to cross 16 bins?
- Does the front's oscillation between 1 and 2 point at a stability issue the
  frozen monitor exposes but the training batches hide?

The governed channel for questions like these is the External Research
Workflow (`docs/runbooks/external-research/2026-06-11-external-research-workflow.md`),
as `trainex-r3` was for v2.3. Choosing the channel is part of the routing
decision in section 1.

## 7. Evidence index

- `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-VERIFICATION.md`
  (SC3 unmet via the terminal branch)
- `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/terminal-state.json`,
  `no-candidate.json`, `run-ledger.md`, `generation-7-retention.json`
- `runs/stage0-v23g7-seed42/failure/trip.json` and checkpoints (Git-tracked)
- `57-05-SUMMARY.md`, `57-06-SUMMARY.md`; gap registers GAP-57-02..13

---

## Appendix A — frozen-monitor replay method and raw output

**Method.** For each checkpoint, a production `RunController` was built with:
- the real admitted corpus, via `pinn.train._build_admitted_sources`, given a
  temporary run directory that holds a copy of `splits.json`;
- the run's own runtime (`float32` / `mps`);
- the governed `R_ref` artifact.

The checkpoint was restored with `RunController.load_state_dict`, which
restores the frozen monitor. Then `RunController._evaluate_front_monitor()`
was called, the same evaluation the invariant-B guard reads.
`git status runs/` was empty afterwards. Script SHA-256:
`0e1297faf4aa1cfe495869eb316beac6bcbc883e7fb98f9fd7fb99c07e2b9bcd`. Run at HEAD
`aa2c6aea` on 2026-10-03, 359 s.

**Reproduce:** save the script below and run it with
`<home>/miniforge3/envs/pinn-train/bin/python <script>` under host
Metal access.

```python
"""Read-only replay of the frozen invariant-B monitor on retained Phase-57 checkpoints.

For each checkpoint: restore it into a production RunController (real admitted corpus,
the run's own runtime, the governed R_ref) and call the same _evaluate_front_monitor the
trainer's invariant-B guard reads. Nothing under runs/ is written: the data adapter gets a
temporary run directory holding a copy of splits.json.
"""
import json, math, shutil, sys, tempfile
from pathlib import Path

REPO = Path("<home>/Desktop/3_body_problem/.worktrees/trainex")
sys.path.insert(0, str(REPO))

import numpy as np  # noqa: E402
import torch  # noqa: E402

from pinn.architecture_spec import ArchitectureSpec  # noqa: E402
from pinn.network import build_network  # noqa: E402
from pinn.runtime import resolve_runtime  # noqa: E402
from pinn.train import _build_admitted_sources  # noqa: E402
from pinn.training.checkpoint import TorchSaveCheckpointStore  # noqa: E402
from pinn.training.collocation_sampler import CollocationSampler  # noqa: E402
from pinn.training.config import load_frozen_r_ref_artifact  # noqa: E402
from pinn.training.config_yaml import load_config  # noqa: E402
from pinn.training.controllers import RunController  # noqa: E402
from pinn.training.grad_clip import GradClipper  # noqa: E402
from pinn.training.scheduled_weights import ScheduledWeights  # noqa: E402
from pinn.training.stage_exit import StageExitMachine  # noqa: E402

LN2 = math.log(2.0)


def build_controller(run_name: str, tmp: Path) -> RunController:
    run_dir = REPO / "runs" / run_name
    config = load_config(REPO / "configs" / f"{run_name}.yaml")
    shutil.copy2(run_dir / "splits.json", tmp / "splits.json")
    train_source, validation_source = _build_admitted_sources(config, tmp)
    runtime = resolve_runtime(config.run.precision, config.run.device)
    model = build_network(ArchitectureSpec(seed=int(config.run.seed)), dtype=runtime.dtype, device=runtime.torch_device)
    s_h = json.loads((run_dir / "training_metadata.json").read_text())["s_h"]
    return RunController(
        model, train_source, validation_source, config,
        ScheduledWeights(int(config.stage.n_adam)), GradClipper(),
        CollocationSampler(2, np.random.default_rng(int(config.run.seed) + 1000)),
        StageExitMachine(config), TorchSaveCheckpointStore(tmp / "store"), runtime,
        s_h=float(s_h), rng=np.random.default_rng(int(config.run.seed)),
        replay_count=int(config.stage.replay_count), r_ref=load_frozen_r_ref_artifact(REPO / config.loss.r_ref_artifact_path),
    )


def replay(run_name: str, checkpoint_names: list[str]) -> list[dict]:
    rows = []
    with tempfile.TemporaryDirectory() as tmp_name:
        controller = build_controller(run_name, Path(tmp_name))
        for name in checkpoint_names:
            path = REPO / "runs" / run_name / "checkpoints" / name
            payload = torch.load(path, map_location="cpu", weights_only=True)
            controller.load_state_dict(payload)
            stats = controller._evaluate_front_monitor()
            rtilde = stats["residuals_per_bin"]
            prefix = [sum(rtilde[:n]) for n in range(len(rtilde) + 1)]
            front = stats["w_n_stats"]["front_idx"]
            rows.append({
                "run": run_name, "checkpoint": name,
                "global_step": int(payload["counters"]["global_step"]),
                "stored_invariant_b": payload.get("invariant_b_state"),
                "front_idx": front,
                "rtilde_bins_0_5": [round(x, 4) for x in rtilde[:6]],
                "prefix_through_front": round(prefix[front + 1], 4) if front >= 0 else None,
                "prefix_to_cross_next": round(prefix[front + 2], 4) if front + 2 <= len(rtilde) else None,
                "ln2": round(LN2, 4),
                "raw_rbar_bin0": stats["raw_residuals_per_bin"][0],
                "rtilde_median_all_bins": round(float(np.median(rtilde)), 4),
            })
    return rows


if __name__ == "__main__":
    targets = {
        "stage0-v23g7-seed42": ["stage-0-init.pt", "best.pt", "step-000931.pt", "step-000941.pt", "step-000951.pt"],
        "stage0-v23g6-seed42": ["step-000490.pt", "step-000500.pt", "step-000510.pt"],
    }
    out = []
    for run, names in targets.items():
        out += replay(run, names)
    for row in out:
        print(json.dumps(row))
```

**Field note.** In the raw output, `prefix_through_front` is the sum over bins
`0..front`, which is the quantity that must fall below 0.693 for the **next**
advance. `prefix_to_cross_next` is the sum one bin further.

**Raw output:**

```text
{"run": "stage0-v23g7-seed42", "checkpoint": "stage-0-init.pt", "global_step": 0, "stored_invariant_b": {"front_high_water": -1, "last_advance_step": null}, "front_idx": 0, "rtilde_bins_0_5": [0.8754, 0.8221, 2.0538, 2.7849, 1.4951, 1.0632], "prefix_through_front": 0.8754, "prefix_to_cross_next": 1.6975, "ln2": 0.6931, "raw_rbar_bin0": 17288675328.0, "rtilde_median_all_bins": 1.1058}
{"run": "stage0-v23g7-seed42", "checkpoint": "best.pt", "global_step": 900, "stored_invariant_b": {"front_high_water": 2, "last_advance_step": 450}, "front_idx": 1, "rtilde_bins_0_5": [0.3099, 0.4178, 0.6166, 1.0578, 0.8126, 0.6346], "prefix_through_front": 0.7277, "prefix_to_cross_next": 1.3443, "ln2": 0.6931, "raw_rbar_bin0": 6120390144.0, "rtilde_median_all_bins": 0.6363}
{"run": "stage0-v23g7-seed42", "checkpoint": "step-000931.pt", "global_step": 931, "stored_invariant_b": {"front_high_water": 2, "last_advance_step": 450}, "front_idx": 2, "rtilde_bins_0_5": [0.2447, 0.3085, 0.639, 1.2448, 0.7146, 0.7053], "prefix_through_front": 1.1922, "prefix_to_cross_next": 2.4369, "ln2": 0.6931, "raw_rbar_bin0": 4832969216.0, "rtilde_median_all_bins": 0.6473}
{"run": "stage0-v23g7-seed42", "checkpoint": "step-000941.pt", "global_step": 941, "stored_invariant_b": {"front_high_water": 2, "last_advance_step": 450}, "front_idx": 2, "rtilde_bins_0_5": [0.2444, 0.3042, 0.6329, 1.2457, 0.7103, 0.7145], "prefix_through_front": 1.1815, "prefix_to_cross_next": 2.4272, "ln2": 0.6931, "raw_rbar_bin0": 4827524608.0, "rtilde_median_all_bins": 0.6404}
{"run": "stage0-v23g7-seed42", "checkpoint": "step-000951.pt", "global_step": 951, "stored_invariant_b": {"front_high_water": 2, "last_advance_step": 450}, "front_idx": 2, "rtilde_bins_0_5": [0.2496, 0.3009, 0.6386, 1.263, 0.7274, 0.7032], "prefix_through_front": 1.1891, "prefix_to_cross_next": 2.452, "ln2": 0.6931, "raw_rbar_bin0": 4929262080.0, "rtilde_median_all_bins": 0.6578}
{"run": "stage0-v23g6-seed42", "checkpoint": "step-000490.pt", "global_step": 490, "stored_invariant_b": {"front_high_water": 2, "last_advance_step": 353}, "front_idx": 1, "rtilde_bins_0_5": [0.6178, 0.336, 0.2978, 0.7186, 0.4717, 0.5683], "prefix_through_front": 0.9538, "prefix_to_cross_next": 1.2516, "ln2": 0.6931, "raw_rbar_bin0": 12202052608.0, "rtilde_median_all_bins": 0.6682}
{"run": "stage0-v23g6-seed42", "checkpoint": "step-000500.pt", "global_step": 500, "stored_invariant_b": {"front_high_water": 2, "last_advance_step": 353}, "front_idx": 1, "rtilde_bins_0_5": [0.5686, 0.2366, 0.2834, 0.9864, 0.5081, 0.9038], "prefix_through_front": 0.8052, "prefix_to_cross_next": 1.0886, "ln2": 0.6931, "raw_rbar_bin0": 11230470144.0, "rtilde_median_all_bins": 0.7384}
{"run": "stage0-v23g6-seed42", "checkpoint": "step-000510.pt", "global_step": 510, "stored_invariant_b": {"front_high_water": 2, "last_advance_step": 353}, "front_idx": 1, "rtilde_bins_0_5": [0.4641, 0.3252, 0.2876, 0.3174, 0.76, 0.5498], "prefix_through_front": 0.7893, "prefix_to_cross_next": 1.0769, "ln2": 0.6931, "raw_rbar_bin0": 9165981696.0, "rtilde_median_all_bins": 0.5585}
```
