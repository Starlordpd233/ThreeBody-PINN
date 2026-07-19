---
status: active
purpose: runbook
created: 2026-07-18
milestone: v2.0
phase: 42-operator-runbook-surface-monitoring
retirement_trigger: superseded by a later Stage-0 training operator runbook
---

# Stage-0 Training Operator Runbook

## Mental Model

A `runs/<name>/` directory is the reproducibility unit for one training run.
Its JSONL log is canonical; TensorBoard is a derived view. `status.json` is a
liveness signal, not a progress claim: a fresh heartbeat means the process is
alive even when an L-BFGS step is taking time.

During Adam, `bin_n` identifies an early/late relative rank. During L-BFGS, it
identifies a fixed collocation time (`tau`). Do not compare those two meanings
as though they were the same coordinate.

## The Five Entry Points

### Setup

From the repository root, create or validate the `pinn-train` environment:

```bash
./setup.sh
```

Activate the environment as printed by setup, then confirm TensorBoard is
available:

```bash
python -c "import tensorboard; print(tensorboard.__version__)"
```

### Configure

Copy the example before editing the run name and Stage-0 budget:

```bash
cp configs/stage0-example.yaml configs/stage0-local.yaml
```

### Launch

For an attended run, launch the config directly:

```bash
python -m pinn.train --config configs/stage0-local.yaml
```

For an unattended run on AC power, use the sleep-preventing wrapper:

```bash
scripts/train-unattended.sh --config configs/stage0-local.yaml
```

### Monitor

Follow the canonical human-readable log for a named run:

```bash
tail -f runs/<name>/logs/train.log
```

Use `tensorboard --logdir runs/<name>/tb` for derived charts and inspect
`runs/<name>/status.json` when checking the heartbeat or a process ID.

### Resume

Resume a stopped or interrupted run from its rolling checkpoint:

```bash
python -m pinn.train --config configs/stage0-local.yaml --resume latest
```

## Error Surface

| Symptom | Meaning | Action |
|---|---|---|
| Guard trip | A configured safety threshold stopped the run. | Read `runs/<name>/failure/` and the final `summary.md`; adjust only the documented operational setting before retrying. |
| NaN or divergence | A non-finite training value was detected. | Treat the run as failed, preserve its artifacts, and inspect the final log and failure bundle before changing the configuration. |
| Memory watermark | MPS driver allocation crossed the configured guard watermark. | Stop other GPU-heavy work; reduce the Stage-0 budget or batch pressure, then resume from the latest checkpoint. |
| Disk floor | Free disk space crossed the configured floor. | Free space outside the run directory, verify the floor is restored, then resume from the latest checkpoint. |
| Stalled heartbeat | `status.json` is older than its own `staleness_threshold_secs`. | Check the recorded PID and process state; if it is no longer alive, use checkpoint resume rather than assuming it will recover. |
| MPS unavailable | The configured `mps` device cannot initialize. | Re-run `./setup.sh`; confirm the environment checks report MPS available, or deliberately select the documented CPU fallback. |
| Config refused | The YAML is missing a required section or contains an unknown key. | Start from `configs/stage0-example.yaml` and correct the named key or required field. |
| Resume refused | The checkpoint and current configuration do not identify the same run. | Use the original frozen configuration or begin a new named run; do not force an incompatible checkpoint. |

## M5-Pro Notes

This workflow assumes one M5 Pro with 24 GB unified memory and one MPS device.
Thermal throttling can make a run slower without making it unhealthy, so read
the heartbeat and logs before intervening. For unattended work, keep the lid
open and the Mac on AC power; `caffeinate -is` prevents idle and AC sleep but
does not assert display wakefulness. Recovery is checkpoint-resume, not
“wake-and-hope.”
