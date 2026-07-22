# Phase 43 Stage-0 pilot evidence

This directory records the traceable reduction of three ordinary admitted-data pilot runs executed on 2026-07-22. The large runtime artifacts remain under `runs/` and are identified here by paths, config identity digests, and SHA-256 hashes.

## Reproduction boundary

Each temporary input was copied from `configs/smoke.yaml`; only `run.seed`, `run.name`, and the already owner-ratified `run.checkpoint.wall_clock_ceiling_s: 120` were set. The commands were:

```text
~/miniforge3/envs/pinn-train/bin/python -m pinn.train --config /tmp/phase43-pilot.sPqSt3/seed41.yaml
~/miniforge3/envs/pinn-train/bin/python -m pinn.train --config /tmp/phase43-pilot.sPqSt3/seed42.yaml
~/miniforge3/envs/pinn-train/bin/python -m pinn.train --config /tmp/phase43-pilot.sPqSt3/seed43.yaml
```

The frozen `config.yaml` in each run directory is the durable input record. All three processes exited 0 and reported `terminal_disposition=HALT`; their canonical `summary.json` disposition and `status.json` state are both `finished`. The controller's terminal `HALT` is the expected Stage-0 budget boundary, not a divergence.

## Machine-readable evidence manifest

Tests parse this block without launching the pilots.

<!-- phase43-pilot-schema: phase43-pilot/v1 -->
```json
{
  "schema": "phase43-pilot/v1",
  "generated_utc": "2026-07-22T08:04:00+00:00",
  "confidence_rule": {
    "high_when_completed_seeds_at_least": 2,
    "otherwise": "LOW",
    "diverged_seeds_retained": true
  },
  "common": {
    "data_admission": "admitted",
    "device": "mps",
    "precision": "float32",
    "steps_requested": 300,
    "d4a_wall_clock_ceiling_s": 120.0,
    "loss_explosion_ceiling": 100000000000.0,
    "disk_floor_fraction": 0.05,
    "memory_watermark_fraction": 0.7,
    "recover_retries": 0,
    "machine_memory_bytes": 25769803776,
    "post_run_disk": {
      "filesystem_blocks": 971298980,
      "free_blocks": 680716528,
      "free_fraction": 0.7008310952823198
    }
  },
  "records": [
    {
      "seed": 41,
      "run_path": "runs/stage0-pilot-seed41",
      "config_identity_digest": "86e6045b72df87e2",
      "start_utc": "2026-07-22T07:53:44.495509+00:00",
      "end_utc": "2026-07-22T07:57:06.410460+00:00",
      "state": "finished",
      "disposition": "finished",
      "steps_completed": 300,
      "all_steps_finite": true,
      "final_losses": {
        "data": 0.1581554114818573,
        "ic": 9177.521484375,
        "phys": 566627968.0,
        "energy": 6635.607421875,
        "angmom": 68.7813720703125,
        "total": 566643776.0
      },
      "peak_total_loss": 6081173504.0,
      "peak_grad_norm": 95203855695872.0,
      "validation": {
        "step": 300,
        "final_val_loss": 463856672.0,
        "trend": "worsening"
      },
      "peak_memory": {
        "driver_bytes": 356581376,
        "current_bytes": 156940544
      },
      "wall_clock_secs": 201.914951,
      "final_s_per_step_ema": 0.09881577425706371,
      "checkpoints": ["best.pt", "ckpt-23752987098.pt", "latest.pt", "stage-0-init.pt", "step-000100.pt", "step-000200.pt", "step-000300.pt"],
      "failure_files": [],
      "sha256": {
        "config.yaml": "86e6045b72df87e2167b1ec6c501abd2cd6acb17900350802943c76b04794e7d",
        "summary.json": "dbbcde8b8ee545f7ba8e142456cdc3d3391e923db6b34f2073eaec38cad5fd28",
        "status.json": "6f661b42f8e6da9690ccbe8c9de11e92e2f350a7e0c915614954679e35c00c7d",
        "validation.jsonl": "c22bb39a70c60308bb688196101b1f6dede34ddb61047191dbcdd69748a5722a",
        "logs/train.log.jsonl": "d1be6a6613f59526840180bad9fd6a0cecaa7df7f45a510adf24c92b429c3998"
      }
    },
    {
      "seed": 42,
      "run_path": "runs/stage0-pilot-seed42",
      "config_identity_digest": "ac15f434681d2244",
      "start_utc": "2026-07-22T07:57:15.790562+00:00",
      "end_utc": "2026-07-22T08:00:33.474008+00:00",
      "state": "finished",
      "disposition": "finished",
      "steps_completed": 300,
      "all_steps_finite": true,
      "final_losses": {
        "data": 0.13550689816474915,
        "ic": 38527.19140625,
        "phys": 650400832.0,
        "energy": 4093.829345703125,
        "angmom": 587.6549682617188,
        "total": 650443456.0
      },
      "peak_total_loss": 3734660096.0,
      "peak_grad_norm": 70647606673408.0,
      "validation": {
        "step": 300,
        "final_val_loss": 78489008.0,
        "trend": "improving"
      },
      "peak_memory": {
        "driver_bytes": 356581376,
        "current_bytes": 156940544
      },
      "wall_clock_secs": 197.683446,
      "final_s_per_step_ema": 0.09758273411582492,
      "checkpoints": ["best.pt", "ckpt-23961380003.pt", "latest.pt", "stage-0-init.pt", "step-000100.pt", "step-000200.pt", "step-000300.pt"],
      "failure_files": [],
      "sha256": {
        "config.yaml": "ac15f434681d2244fda9a0bcdc8b33416ed1c8737b682f695782501862fb86ad",
        "summary.json": "e483e56b484fefac53f1d5b59f8ceb2ec87e6f91e8d1b764eee7f003f6d6422b",
        "status.json": "db570f152d26db6bd62591fc6464f0b27c395bf51d3988f67225749bb5f73cc2",
        "validation.jsonl": "efcc4fdc54ee92c51c08676574d477efb389b6401e5e47ea2bc9b9f3ef43e6b2",
        "logs/train.log.jsonl": "d7958a3397eafc7a41039c43dcf8a0d59fab46d53fa82952e0eb0bb769a7a3d2"
      }
    },
    {
      "seed": 43,
      "run_path": "runs/stage0-pilot-seed43",
      "config_identity_digest": "466bc4ffc8933a1d",
      "start_utc": "2026-07-22T08:00:39.669501+00:00",
      "end_utc": "2026-07-22T08:03:55.382859+00:00",
      "state": "finished",
      "disposition": "finished",
      "steps_completed": 300,
      "all_steps_finite": true,
      "final_losses": {
        "data": 0.13903017342090607,
        "ic": 43157.95703125,
        "phys": 150663264.0,
        "energy": 13685.5869140625,
        "angmom": 27.946874618530273,
        "total": 150720096.0
      },
      "peak_total_loss": 3832843264.0,
      "peak_grad_norm": 62418801655808.0,
      "validation": {
        "step": 300,
        "final_val_loss": 1851546240.0,
        "trend": "worsening"
      },
      "peak_memory": {
        "driver_bytes": 356581376,
        "current_bytes": 156940544
      },
      "wall_clock_secs": 195.713358,
      "final_s_per_step_ema": 0.09618073375458501,
      "checkpoints": ["best.pt", "ckpt-24163448064.pt", "latest.pt", "stage-0-init.pt", "step-000100.pt", "step-000200.pt", "step-000300.pt"],
      "failure_files": [],
      "sha256": {
        "config.yaml": "466bc4ffc8933a1d5cf2f94adbf35b3450eb2c5ff99777bb46740795fc9b8f96",
        "summary.json": "4f4620838d6e75ad2db7d1ca5de0fa8603c5b8df9fbd0d0ec3b6aa5d5d705f79",
        "status.json": "d8f3596b1e427c97b09a0c78346af591a6a85118275bb68ec57185ec5da9e1b4",
        "validation.jsonl": "b10de7758528be2a410165a61cf2747a279d111b761f11f83d0bad3d8ed8a012",
        "logs/train.log.jsonl": "0f1b5ba7a0c1de5cce4a2c51a307fe4706755fc271a07dc588b86c4bac109302"
      }
    }
  ],
  "rollup": {
    "completed_seed_count": 3,
    "diverged_seed_count": 0,
    "confidence": "HIGH",
    "spread_formula": "(max - min) / median",
    "max_observed_total_loss": 6081173504.0,
    "max_observed_driver_bytes": 356581376
  },
  "candidate_observation_refs": {
    "loss_explosion_ceiling": ["rollup.max_observed_total_loss", "records[*].peak_total_loss"],
    "disk_floor_fraction": ["common.post_run_disk", "records[*].failure_files"],
    "memory_watermark_fraction": ["rollup.max_observed_driver_bytes", "common.machine_memory_bytes"],
    "recover_retries": ["records[*].disposition", "records[*].failure_files", "common.recover_retries"]
  }
}
```

## Integrity notes

- Config identity digests are the first 16 hexadecimal characters of each frozen `config.yaml` SHA-256 and match each run summary.
- Runtime logs are ignored execution output, so this committed manifest carries hashes needed to re-derive every numerical claim while the local run directories exist.
- No failure or divergence record was discarded. The schema requires records to be retained independent of terminal disposition.
