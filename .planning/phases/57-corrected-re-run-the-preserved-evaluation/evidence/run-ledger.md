# Phase 57 Run Ledger

The ledger is append-only during the smoke and graded run window.
Generations 1 through 5 are retained historical attempts; none belongs to the
final band. The final generation is set only after a complete generation-6
band or the authorized scientific terminal branch is recorded. The generation-1
`blocked-state.json`, generation-3 `blocked-state-g3.json`, and generation-4
`blocked-state-g4.json` paths and digests are historical evidence and remain
immutable. The generation-5 completed smoke is retained under
`generation-5-retention.json`. If generation 6 reaches an operational block,
its record is written to `blocked-state-g6.json` instead.

<!-- phase57-run-ledger-schema: phase57-run-ledger/v2 -->
```json
{
  "schema": "phase57-run-ledger/v2",
  "phase": 57,
  "milestone": "v2.3",
  "pre_registration": {
    "source": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/57-RULING.md",
    "seed": 42,
    "fallback_order": [
      42,
      41,
      43
    ],
    "fallback_basis": "structural_ineligibility_only",
    "front_advance_window_n": 500,
    "evaluation": "preserved-unspent-until-three-preconditions-pass"
  },
  "final_band_generation": null,
  "band_generations": [
    {
      "band_generation": 1,
      "status": "blocked",
      "git_head": "285bc64431eb26556826d0315123da81716204f9",
      "extraction_git_head": null,
      "launch_order": [
        "stage0-v23-smoke",
        "stage0-v23-seed41",
        "stage0-v23-seed42",
        "stage0-v23-seed43"
      ],
      "launched_runs": [
        "stage0-v23-smoke"
      ],
      "evaluation": "preserved-unspent",
      "blocked_state": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state.json"
    },
    {
      "band_generation": 2,
      "status": "historical-incomplete",
      "git_head": null,
      "extraction_git_head": null,
      "launch_order": [
        "stage0-v23g2-smoke",
        "stage0-v23g2-seed41",
        "stage0-v23g2-seed42",
        "stage0-v23g2-seed43"
      ],
      "launched_runs": [
        "stage0-v23g2-smoke"
      ],
      "evaluation": "preserved-unspent",
      "retention_manifest": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/generation-2-retention.json"
    },
    {
      "band_generation": 3,
      "status": "blocked",
      "git_head": "ad96e6f46b5c7fd5ac7faa8b23c438974373dc38",
      "extraction_git_head": null,
      "launch_order": [
        "stage0-v23g3-smoke",
        "stage0-v23g3-seed41",
        "stage0-v23g3-seed42",
        "stage0-v23g3-seed43"
      ],
      "launched_runs": [
        "stage0-v23g3-smoke"
      ],
      "evaluation": "preserved-unspent",
      "blocked_state": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state-g3.json"
    },
    {
      "band_generation": 4,
      "status": "blocked",
      "git_head": "f0855a20762367da012ff9a3c8476c37c1d04729",
      "extraction_git_head": null,
      "launch_order": [
        "stage0-v23g4-smoke",
        "stage0-v23g4-seed41",
        "stage0-v23g4-seed42",
        "stage0-v23g4-seed43"
      ],
      "launched_runs": [
        "stage0-v23g4-smoke"
      ],
      "evaluation": "preserved-unspent",
      "blocked_state": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state-g4.json"
    },
    {
      "band_generation": 5,
      "status": "historical-complete-smoke",
      "git_head": "b151e02d25bd954409ab0dec6a0fda6d9a5d3cb3",
      "extraction_git_head": null,
      "launch_order": [
        "stage0-v23g5-smoke",
        "stage0-v23g5-seed41",
        "stage0-v23g5-seed42",
        "stage0-v23g5-seed43"
      ],
      "launched_runs": [
        "stage0-v23g5-smoke"
      ],
      "evaluation": "preserved-unspent",
      "retention_manifest": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/generation-5-retention.json"
    },
    {
      "band_generation": 6,
      "status": "blocked",
      "git_head": "ef4764f92d9ad23fa90c936166137944dc5e4aea",
      "extraction_git_head": null,
      "launch_order": [
        "stage0-v23g6-smoke",
        "stage0-v23g6-seed42",
        "stage0-v23g6-seed41",
        "stage0-v23g6-seed43"
      ],
      "launched_runs": [
        "stage0-v23g6-smoke",
        "stage0-v23g6-seed42"
      ],
      "evaluation": "preserved-unspent",
      "blocked_state": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state-g6.json"
    }
  ],
  "records": [
    {
      "band_generation": 1,
      "launch_kind": "smoke",
      "run_name": "stage0-v23-smoke",
      "seed": 42,
      "git_head": "285bc64431eb26556826d0315123da81716204f9",
      "config_path": "configs/stage0-v23-smoke.yaml",
      "config_sha256": "668ea42f2f162fc4e06b53e02af0075c13ee12acbf281038fdcafa0ea74113f5",
      "resolved_config_path": "runs/stage0-v23-smoke/config.yaml",
      "resolved_config_sha256": "6b1069eb9912e8f4ed52cb7623c8e9fcf3bb039bb343a3a7a3f0b314aa90e93f",
      "artifact_dir": "runs/stage0-v23-smoke",
      "command": "<home>/miniforge3/bin/conda run -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-v23-smoke.yaml --stage-0-only",
      "stage_0_only": true,
      "collocation_count": 4096,
      "replay_count": 240,
      "front_advance_window_n": 500,
      "max_epochs": 300,
      "n_adam": 300,
      "monitor": "training-only frozen monitor; no optimizer update completed",
      "r_ref": 19749775821.24417,
      "r_ref_artifact_path": "pinn/verification/artifacts/r_ref_stage0.json",
      "r_ref_artifact_sha256": "c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff",
      "corpus": {
        "splits_sha256": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "s_h": 22.321729071058996,
        "eps_h": 0.0022321729071058997,
        "n_train": 1812
      },
      "environment": {
        "device": "mps",
        "precision": "float32",
        "python_version": "3.11.15",
        "torch_version": "2.12.1",
        "torch_build": "7269437d655783a26cba32aa88195b741ff496aa",
        "platform": "macOS 26.5.1"
      },
      "launch_started_utc": "2026-09-08T15:00:56.422668+00:00",
      "completion_utc": "2026-09-08T15:15:08.361196+00:00",
      "wall_clock_secs": 851.938528,
      "process_pid": 54461,
      "exit_code": 1,
      "final_process_disposition": "HALT",
      "ledger_disposition": "blocked",
      "final_guard_disposition": "HALT",
      "guard": "memory_watermark",
      "guard_step": 0,
      "guard_stage": 0,
      "guard_phase": "2a",
      "guard_metric": "memory_fraction",
      "guard_value": 0.968756357828776,
      "guard_threshold": 0.7,
      "guard_threshold_provisional": true,
      "evaluation": "preserved-unspent",
      "in_final_band": false,
      "terminal": false,
      "blocked_state_path": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state.json",
      "blocked_state_sha256": "2d0e43343f84bf18df571b8f1fd2e1e14b9cd7c8ee416ad6f50ae2bacea1260b",
      "artifact_hashes": {
        "checkpoints/ckpt-223666118608.pt": "203931bd41006b1faae60d7dad12c44ab3c37746f8e4ae2e901f863534e4d1ec",
        "checkpoints/failure-stage-0-step-0.pt": "3e82aa0ca5d4097c588036efc4e7866e0055be9687f60f580e7a9ddd6f1aa461",
        "checkpoints/latest.pt": "156201b0e0a65b6828eeff831071826b5670c940da8d680643dcb9466ff317b9",
        "checkpoints/stage-0-init.pt": "a7f7de2b8422107d626d3fbb8e20a552b4130aeff61994b54d6558daa2b62a21",
        "config.yaml": "6b1069eb9912e8f4ed52cb7623c8e9fcf3bb039bb343a3a7a3f0b314aa90e93f",
        "curriculum.jsonl": "e1743dda8ef75b1577352f1f8e89b26659d876e2bc5fcef790968c3ffdaf396e",
        "failure/README.txt": "b8c3f9be212c1723e6a8c49a207118fed22e4f540fa55ff70010cd7400d4f299",
        "failure/trip.json": "f4f34a47a8f66c6ea91128a5c59ba5540b2cac9cea6fb852bee71f27556f064a",
        "logs/train.log": "eeaaec2ca746b5573f67e4d79d23c1bb5d66393f368d46f8940587dec6927990",
        "logs/train.log.jsonl": "97a4839f914a8033fa9d51a2b478f5473cf6bdf3a718df6169743e22f01469f3",
        "preflight.json": "3dd845c5800d5848249e66282264558747edf352f6cd009933ddb6e752ddfc89",
        "run_start_rng.pt": "4ee92de64d5290fa72689cfee383fccea1642cc9e99c0f9dc88e05920e09b65d",
        "splits.json": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "status.json": "3643cee92d98281e5e86aeeb56dc94f67653c37e6bd494026b10b4bb93368637",
        "summary.json": "4c2ef451d07c1ed3f5538dd1219ae82a71d72804c6757f3c87dce2769aa813b8",
        "summary.md": "b2fe1bf5119fa56ee57e2eafbb6fa7de49d01702751464b65dafac99c6c15995",
        "tb/<host>.54461.0": "19b988b0ee4ce29d19612a0157e49a4fbed6d205af5ec120c757331acda5d757",
        "training_metadata.json": "a7011e77a5f7c91720f924117de06b8892e316e35c19531ba8617c4c1236a095"
      },
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": "fresh",
          "command": "<home>/miniforge3/bin/conda run -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-v23-smoke.yaml --stage-0-only",
          "process_pid": 54461,
          "start_utc": "2026-09-08T15:00:56.422668+00:00",
          "end_utc": "2026-09-08T15:15:08.361196+00:00",
          "wall_clock_secs": 851.938528,
          "exit_code": 1,
          "git_head": "285bc64431eb26556826d0315123da81716204f9",
          "config_sha256": "668ea42f2f162fc4e06b53e02af0075c13ee12acbf281038fdcafa0ea74113f5",
          "disposition": "HALT",
          "boundary_checkpoint": null,
          "resume_checkpoint": null
        }
      ]
    },
    {
      "band_generation": 2,
      "launch_kind": "smoke",
      "run_name": "stage0-v23g2-smoke",
      "seed": 42,
      "git_head": null,
      "config_path": "configs/stage0-v23g2-smoke.yaml",
      "config_sha256": null,
      "resolved_config_path": "runs/stage0-v23g2-smoke/config.yaml",
      "resolved_config_sha256": "fef189da3567e04c3d79e9696f1e474496784704c05abbedad832a7fa94ced33",
      "config_identity_digest": "fef189da3567e04c",
      "artifact_dir": "runs/stage0-v23g2-smoke",
      "command": null,
      "stage_0_only": null,
      "collocation_count": 4096,
      "replay_count": 240,
      "front_advance_window_n": 500,
      "max_epochs": 300,
      "n_adam": 300,
      "corpus": {
        "splits_sha256": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "s_h": 22.321729071058996,
        "eps_h": 0.0022321729071058997,
        "n_train": 1812
      },
      "environment": {
        "python_version": "3.11.15",
        "sw_vers": "ProductName:\t\tmacOS\nProductVersion:\t\t26.5.1\nBuildVersion:\t\t25F80",
        "torch_build": "7269437d655783a26cba32aa88195b741ff496aa",
        "torch_version": "2.12.1",
        "device": "mps",
        "precision": "float32"
      },
      "launch_started_utc": "2026-09-13T13:01:06.557949+00:00",
      "completion_utc": "2026-09-13T13:16:48.569661+00:00",
      "wall_clock_secs": 942.011712,
      "process_pid": 91780,
      "exit_code": null,
      "final_process_disposition": "interrupted",
      "ledger_disposition": "historical-incomplete",
      "evaluation": "preserved-unspent",
      "in_final_band": false,
      "terminal": false,
      "provenance_note": "The owner recalled a deliberate stop on 2026-09-27; retained status and summary establish interrupted, but do not establish the signal, exit code, exact launch command, or run git_head. The Stage-0-only CLI flag is not independently retained. The exact fresh/resume launch kind is not independently retained.",
      "retention_manifest": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/generation-2-retention.json",
      "artifact_hashes": {
        "checkpoints/ckpt-61163069181.pt": "a4ca637ed0ececf609e4a90e6a0830b27b57587f7f219f51cad9a8800509d968",
        "checkpoints/latest.pt": "dcf369b053e91b3fa371c66255d359551aac8a27f84cb6adf7ba03fc92ea3031",
        "checkpoints/stage-0-init.pt": "b9f9ba949f92a77bada5e138b897b98f6e5ee7281c2db22a46b31c972ee2e6a7",
        "checkpoints/step-000031.pt": "084f89b27acda814f10b0e2e2a58c2a562126e025f371c7b5c9c1706dfd0d28b",
        "config.yaml": "fef189da3567e04c3d79e9696f1e474496784704c05abbedad832a7fa94ced33",
        "curriculum.jsonl": "2642a9cc6aa167ba059b92f761f2d7ce1c8bbdb66a779cba7d65bc431b2a8c43",
        "logs/train.log": "505322958f3cce766ff0e63e28b99ae574fb5b465884476533d2daf70fa16547",
        "logs/train.log.jsonl": "bab871cfd597c50f2fc789184e7e7dc17e9b959b683de86bcf3e277915825717",
        "preflight.json": "3dd845c5800d5848249e66282264558747edf352f6cd009933ddb6e752ddfc89",
        "run_start_rng.pt": "de1bb06f90f746ebd169dedc861f6f6639f3c022efb0bfb4652ddfd6dd3551fe",
        "splits.json": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "status.json": "00ed5e98f3710ca73ec03dfc73e7b74d404736293290c8157628989d7fba8def",
        "summary.json": "c9e9f0d64143f75a93862e4c2cbbfc27ab0982f8d65fc3513121379287cb2376",
        "summary.md": "172a164697c0fc91195183c6591e0293283cb1a2e619056a40aa68f4bddff1d8",
        "tb/events.out.tfevents.1789304466.<host>.91780.0": "bd399da083f1805e62cc148974e01f351f42423ccbd16229112f737294a8771e",
        "training_metadata.json": "a7011e77a5f7c91720f924117de06b8892e316e35c19531ba8617c4c1236a095"
      },
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": null,
          "command": null,
          "process_pid": 91780,
          "start_utc": "2026-09-13T13:01:06.557949+00:00",
          "end_utc": "2026-09-13T13:16:48.569661+00:00",
          "wall_clock_secs": 942.011712,
          "exit_code": null,
          "git_head": null,
          "config_sha256": null,
          "disposition": "interrupted",
          "boundary_checkpoint": {
            "path": "runs/stage0-v23g2-smoke/checkpoints/step-000031.pt",
            "sha256": "084f89b27acda814f10b0e2e2a58c2a562126e025f371c7b5c9c1706dfd0d28b"
          },
          "resume_checkpoint": null
        }
      ]
    },
    {
      "band_generation": 3,
      "launch_kind": "smoke",
      "run_name": "stage0-v23g3-smoke",
      "seed": 42,
      "git_head": "ad96e6f46b5c7fd5ac7faa8b23c438974373dc38",
      "config_path": "configs/stage0-v23g3-smoke.yaml",
      "config_sha256": "e06d2f0c7f6a3d89b464e3463eabdf5308e0c10d351c479a7ba7aa3363cd7471",
      "resolved_config_path": "runs/stage0-v23g3-smoke/config.yaml",
      "resolved_config_sha256": "782016b67d321682a50a8b51d2ffe764f5714299977453fd3ca35c43c57659a0",
      "config_identity_digest": "782016b67d321682",
      "artifact_dir": "runs/stage0-v23g3-smoke",
      "command": "<home>/miniforge3/bin/conda run -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-v23g3-smoke.yaml --stage-0-only",
      "stage_0_only": true,
      "collocation_count": 4096,
      "replay_count": 240,
      "front_advance_window_n": 500,
      "max_epochs": 300,
      "n_adam": 300,
      "monitor": "training-only frozen monitor; no optimizer update completed",
      "r_ref": 19749775821.24417,
      "r_ref_artifact_path": "pinn/verification/artifacts/r_ref_stage0.json",
      "r_ref_artifact_sha256": "c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff",
      "corpus": {
        "splits_sha256": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "s_h": 22.321729071058996,
        "eps_h": 0.0022321729071058997,
        "n_train": 1812
      },
      "environment": {
        "device": "mps",
        "precision": "float32",
        "python_version": "3.11.15",
        "torch_version": "2.12.1",
        "torch_build": "7269437d655783a26cba32aa88195b741ff496aa",
        "platform": "macOS 26.5.1"
      },
      "launch_started_utc": "2026-09-27T21:29:01.520895+00:00",
      "completion_utc": "2026-09-27T21:29:01.631936+00:00",
      "wall_clock_secs": 0.111041,
      "process_pid": 94402,
      "exit_code": 1,
      "final_process_disposition": "blocked",
      "ledger_disposition": "blocked",
      "final_guard_disposition": null,
      "guard": null,
      "evaluation": "preserved-unspent",
      "in_final_band": false,
      "terminal": false,
      "blocked_state_path": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state-g3.json",
      "blocked_state_sha256": "4398d1923fa90cd73148b19d8ceed28f28ae797cd5a67fc48eda53efa492059e",
      "artifact_hashes": {
        "config.yaml": "782016b67d321682a50a8b51d2ffe764f5714299977453fd3ca35c43c57659a0",
        "logs/train.log": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "logs/train.log.jsonl": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "status.json": "4fc5746c18311559c1016e8f62ebbe15d436d2a8f1d6ad2f8b77b31a21ab58ae",
        "summary.json": "c365fc26f30bd0a8972d6b92a41c19689e73018dede63e5f786d53a2da26c65e",
        "summary.md": "ca825cd18c1ff5e1d3816e6a1ddfae666f4f7d3502991f3b672fa11f04ea70cc",
        "tb/<host>.94402.0": "4902a1327fc2783a398fc81d64444c4959d54c4c12e0b94ae8c275ecbd0f6239"
      },
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": "fresh",
          "command": "<home>/miniforge3/bin/conda run -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-v23g3-smoke.yaml --stage-0-only",
          "process_pid": 94402,
          "start_utc": "2026-09-27T21:29:01.520895+00:00",
          "end_utc": "2026-09-27T21:29:01.631936+00:00",
          "wall_clock_secs": 0.111041,
          "exit_code": 1,
          "git_head": "ad96e6f46b5c7fd5ac7faa8b23c438974373dc38",
          "config_sha256": "e06d2f0c7f6a3d89b464e3463eabdf5308e0c10d351c479a7ba7aa3363cd7471",
          "disposition": "blocked",
          "boundary_checkpoint": null,
          "resume_checkpoint": null
        }
      ]
    },
    {
      "band_generation": 4,
      "launch_kind": "smoke",
      "run_name": "stage0-v23g4-smoke",
      "seed": 42,
      "git_head": "f0855a20762367da012ff9a3c8476c37c1d04729",
      "config_path": "configs/stage0-v23g4-smoke.yaml",
      "config_sha256": "e324817a69a28c1bffa18f49ae9c60f549f373ecd3e43880ba76ea228e6df1b0",
      "resolved_config_path": "runs/stage0-v23g4-smoke/config.yaml",
      "resolved_config_sha256": "19ebe5dd3ea144ebc88264af89d53a86935e5a355e1d097ed6eadb9bc0623d3c",
      "config_identity_digest": "782016b67d321682",
      "artifact_dir": "runs/stage0-v23g4-smoke",
      "command": "<home>/miniforge3/bin/conda run -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-v23g4-smoke.yaml --stage-0-only",
      "stage_0_only": true,
      "collocation_count": 4096,
      "replay_count": 240,
      "front_advance_window_n": 500,
      "max_epochs": 300,
      "n_adam": 300,
      "monitor": "training-only frozen monitor; no optimizer update boundary was written for resume",
      "r_ref": 19749775821.24417,
      "r_ref_artifact_path": "pinn/verification/artifacts/r_ref_stage0.json",
      "r_ref_artifact_sha256": "c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff",
      "corpus": {
        "splits_sha256": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "s_h": 22.321729071058996,
        "eps_h": 0.0022321729071058997,
        "n_train": 1812
      },
      "environment": {
        "python_version": "3.11.15",
        "torch_version": "2.12.1",
        "torch_build": "7269437d655783a26cba32aa88195b741ff496aa",
        "platform": "macOS 26.5.1",
        "device": "mps",
        "precision": "float32",
        "mps_available_at_launch": true,
        "mps_device_count_at_launch": 1
      },
      "launch_started_utc": "2026-09-28T04:25:33.509000+00:00",
      "completion_utc": "2026-09-28T04:37:00Z",
      "wall_clock_secs": 1886.5,
      "process_pid": 13784,
      "exit_code": 1,
      "final_process_disposition": "interrupted",
      "ledger_disposition": "blocked",
      "final_guard_disposition": null,
      "guard": null,
      "evaluation": "preserved-unspent",
      "in_final_band": false,
      "terminal": false,
      "blocked_state_path": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state-g4.json",
      "blocked_state_sha256": "b04723243240b51c502573bbd2b6198646cc8d84f46caf636be35ac1baec25fd",
      "artifact_hashes": {
        "checkpoints/ckpt-492755433024.pt": "7cf028729559315413d4685d7b516b4494e8bb8ed7fc762e80e819c25b6ebc7b",
        "checkpoints/latest.pt": "329fd439c556d3767d524faf99c67b7e746d4fb8e7273eeb461a565bd3f72899",
        "checkpoints/stage-0-init.pt": "c3fdae172a25006edfd1d55847e813f62c1029e9997fc71968f36a750ef56845",
        "config.yaml": "19ebe5dd3ea144ebc88264af89d53a86935e5a355e1d097ed6eadb9bc0623d3c",
        "logs/train.log": "a988c0fcdfc6ccf48d2bdd3c5388a849a8eb276fa045c8ac6cb04f9e7d526a1b",
        "logs/train.log.jsonl": "279b83eb94f139077848e12729f5aa51ab620f064a9e868429d91102b5c65c79",
        "preflight.json": "3dd845c5800d5848249e66282264558747edf352f6cd009933ddb6e752ddfc89",
        "run_start_rng.pt": "7ab0e3192b262790a3e7e07c23555930420af7abe24081a38c98acce7fac7c5e",
        "splits.json": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "status.json": "229bb849513e97773674889e4f6ce768a133207fd7f3c4432d8881e6daa1dc8b",
        "summary.json": "54f4d039ad731038943475ad9962f91686608bdf24fcc42c302eae08f7489388",
        "summary.md": "e1a786fb03271d128cc798f29335ad4934bce9b7ceee9327100f4f8d161760c4",
        "tb/<host>.13784.0": "7ea00210c4c16b239bad5ee779ecae1fcf34b646b4b283dcf7accc09c328d9eb",
        "training_metadata.json": "a7011e77a5f7c91720f924117de06b8892e316e35c19531ba8617c4c1236a095"
      },
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": "fresh",
          "command": "<home>/miniforge3/bin/conda run -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-v23g4-smoke.yaml --stage-0-only",
          "process_pid": 13784,
          "start_utc": "2026-09-28T04:25:33.509000+00:00",
          "end_utc": "2026-09-28T04:37:00Z",
          "wall_clock_secs": 1886.5,
          "exit_code": 1,
          "git_head": "f0855a20762367da012ff9a3c8476c37c1d04729",
          "config_sha256": "e324817a69a28c1bffa18f49ae9c60f549f373ecd3e43880ba76ea228e6df1b0",
          "disposition": "interrupted",
          "boundary_checkpoint": null,
          "resume_checkpoint": null
        }
      ]
    },
    {
      "band_generation": 5,
      "launch_kind": "smoke",
      "run_name": "stage0-v23g5-smoke",
      "seed": 42,
      "git_head": "b151e02d25bd954409ab0dec6a0fda6d9a5d3cb3",
      "config_path": "configs/stage0-v23g5-smoke.yaml",
      "config_sha256": "625b9f5f9356deeec1f1aaa9ee0f3bfe46c15f2fca06744cc24c53d1685dd05d",
      "resolved_config_path": "runs/stage0-v23g5-smoke/config.yaml",
      "resolved_config_sha256": "12c2fe4fcab05c878f4e0414115a35b64fe48451dfcfe6b4bc9079b8c1c5d0cd",
      "config_identity_digest": "12c2fe4fcab05c87",
      "artifact_dir": "runs/stage0-v23g5-smoke",
      "command": "/usr/bin/caffeinate -is <home>/miniforge3/envs/pinn-train/bin/python -m pinn.train --config configs/stage0-v23g5-smoke.yaml --stage-0-only",
      "stage_0_only": true,
      "collocation_count": 4096,
      "replay_count": 240,
      "front_advance_window_n": 500,
      "max_epochs": 300,
      "n_adam": 300,
      "monitor": "one frozen training-only monitor, front_high_water=1 at final checkpoint",
      "r_ref": 19749775821.24417,
      "r_ref_artifact_path": "pinn/verification/artifacts/r_ref_stage0.json",
      "r_ref_artifact_sha256": "c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff",
      "corpus": {
        "splits_sha256": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "s_h": 22.321729071058996,
        "eps_h": 0.0022321729071058997,
        "n_train": 1812
      },
      "environment": {
        "device": "mps",
        "precision": "float32",
        "python_version": "3.11.15",
        "torch_version": "2.12.1",
        "torch_build": "7269437d655783a26cba32aa88195b741ff496aa",
        "platform": "macOS 26.5.1"
      },
      "launch_started_utc": "2026-09-28T20:45:40.360426+00:00",
      "completion_utc": "2026-09-28T21:51:22.094684+00:00",
      "wall_clock_secs": 3941.734258,
      "process_pid": 56068,
      "exit_code": 0,
      "final_process_disposition": "finished",
      "ledger_disposition": "historical-complete-smoke",
      "final_guard_disposition": null,
      "guard": null,
      "evaluation": "preserved-unspent",
      "in_final_band": false,
      "terminal": false,
      "validation": {
        "gate_status": "ok",
        "gate_verdict": "FAIL",
        "gate_sidecar": "validation_gate/step-00000300.json",
        "gate_sidecar_sha256": "546b2edb38b34812a1b17f2f79a209291d10ad78358396fc116358b59936d85b"
      },
      "retention_manifest": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/generation-5-retention.json",
      "artifact_hashes": {
        "checkpoints/best.pt": "e77da792b4443bf59d4564d4e118b44c1712d364e9472e3f9715e38c25ee1efb",
        "checkpoints/ckpt-18887573397.pt": "5c5d0ae8d9c8f268965dd3025fff2f61e8a03863c7922a153c4e73574bae5344",
        "checkpoints/latest.pt": "ef4f58e24ed58120616f746f00300a8a593d49c382fdbf75d7fb97680e5831f7",
        "checkpoints/stage-0-init.pt": "72e26128e0190d8723815a12e459b9892cf0607d71855cb6ca636dc6a16b008d",
        "checkpoints/step-000100.pt": "d4f5c3f9efb7b4a832cb71105997109ac397204aa3712ff7c2dfce08ca9907f8",
        "checkpoints/step-000200.pt": "dd76c79a3a67d8fcbda92f8d0e61c0bfb93b5918684fc343d468ab97de8b2693",
        "checkpoints/step-000300.pt": "c4b487c2ff0a770beb2ff8238d538d81688a047aa9d3c915515654faead9c721",
        "config.yaml": "12c2fe4fcab05c878f4e0414115a35b64fe48451dfcfe6b4bc9079b8c1c5d0cd",
        "curriculum.jsonl": "7439572cb2940ce8a440b22796315c552c8dea725c70297c169ef9f065c4b68b",
        "logs/train.log": "c196484f60042415313e53fe4b78c36deb65b57cc380b185e8cee5aa13538473",
        "logs/train.log.jsonl": "aba2c3a934b9d059123c18d84719649e543941e5b1652b8ca4069aea4009250d",
        "preflight.json": "3dd845c5800d5848249e66282264558747edf352f6cd009933ddb6e752ddfc89",
        "run_start_rng.pt": "da6983b3f34492cb9547afda77fe349e3844da2bd76fc4bbd4a17960531765eb",
        "splits.json": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "status.json": "81155c8b5bd94ee85f87af5fbe4bedceaada09b3ca8f76a3ab05d0cfa243e3af",
        "summary.json": "ac181c526636b8a05902fc52ba671673bf89c578484664c198dad9ecc11029a9",
        "summary.md": "777422ad845b22b3c859074a9df9e112f944ae6ab3667f595290e4d430f4c7ec",
        "tb/<host>.56068.0": "d1e8ae48a7cacf3f9255fca7ce6eb2f363ead3204a3dab5c41caa777a116d1c3",
        "training_metadata.json": "a7011e77a5f7c91720f924117de06b8892e316e35c19531ba8617c4c1236a095",
        "validation.jsonl": "eac23d62246746090e9c81870e5c6dfb28a65913b99fc19df7ae803b91a360d1",
        "validation_gate/step-00000100.json": "f1fc4261af050f6db61fd42ec5f4b08090f4fdf8d7027b7814732ec1f29d562b",
        "validation_gate/step-00000200.json": "889938db42703f21effb29cff9eb5f7cf0f59199ffd6a87314510263cca0413f",
        "validation_gate/step-00000300.json": "546b2edb38b34812a1b17f2f79a209291d10ad78358396fc116358b59936d85b"
      },
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": "fresh",
          "command": "/usr/bin/caffeinate -is <home>/miniforge3/envs/pinn-train/bin/python -m pinn.train --config configs/stage0-v23g5-smoke.yaml --stage-0-only",
          "process_pid": 56068,
          "start_utc": "2026-09-28T20:45:40.360426+00:00",
          "end_utc": "2026-09-28T21:51:22.094684+00:00",
          "wall_clock_secs": 3941.734258,
          "exit_code": 0,
          "git_head": "b151e02d25bd954409ab0dec6a0fda6d9a5d3cb3",
          "config_sha256": "625b9f5f9356deeec1f1aaa9ee0f3bfe46c15f2fca06744cc24c53d1685dd05d",
          "disposition": "finished",
          "boundary_checkpoint": null,
          "resume_checkpoint": null
        }
      ]
    },
    {
      "band_generation": 6,
      "launch_kind": "smoke",
      "run_name": "stage0-v23g6-smoke",
      "seed": 42,
      "git_head": "ef4764f92d9ad23fa90c936166137944dc5e4aea",
      "config_path": "configs/stage0-v23g6-smoke.yaml",
      "config_sha256": "f6f6835ee18efee5bd8c08865e4d7d3a63ee1dfcd890675d4cfebea45fa15781",
      "resolved_config_path": "runs/stage0-v23g6-smoke/config.yaml",
      "resolved_config_sha256": "26771ae8ef9205622d0a04cdb55f4b9db0590f89fa2531e01612ace761e39860",
      "config_identity_digest": "26771ae8ef920562",
      "artifact_dir": "runs/stage0-v23g6-smoke",
      "command": "/usr/bin/caffeinate -is <home>/miniforge3/envs/pinn-train/bin/python -m pinn.train --config configs/stage0-v23g6-smoke.yaml --stage-0-only",
      "stage_0_only": true,
      "collocation_count": 4096,
      "replay_count": 240,
      "front_advance_window_n": 500,
      "max_epochs": 300,
      "n_adam": 300,
      "monitor": {
        "schema_version": "phase57-front-monitor/v1",
        "split": "train",
        "n_bins": 16,
        "n_collocation_rows": 4096,
        "invariant_b_state": {
          "front_high_water": 1,
          "last_advance_step": 93
        }
      },
      "r_ref": 19749775821.24417,
      "r_ref_artifact_path": "pinn/verification/artifacts/r_ref_stage0.json",
      "r_ref_artifact_sha256": "c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff",
      "corpus": {
        "splits_sha256": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "s_h": 22.321729071058996,
        "eps_h": 0.0022321729071058997,
        "n_train": 1812
      },
      "environment": {
        "device": "mps",
        "precision": "float32",
        "python_version": "3.11.15",
        "torch_version": "2.12.1",
        "torch_build": "7269437d655783a26cba32aa88195b741ff496aa",
        "sw_vers": "ProductName:\t\tmacOS\nProductVersion:\t\t26.5.1\nBuildVersion:\t\t25F80"
      },
      "launch_started_utc": "2026-09-29T02:38:47.359565+00:00",
      "completion_utc": "2026-09-29T03:44:26.327917+00:00",
      "wall_clock_secs": 3938.968352,
      "process_pid": 87113,
      "exit_code": 0,
      "final_process_disposition": "finished",
      "ledger_disposition": "finished",
      "final_guard_disposition": "finished",
      "guard": null,
      "evaluation": "preserved-unspent",
      "in_final_band": false,
      "terminal": false,
      "artifact_hashes": {
        "checkpoints/best.pt": "59ff27eb54b45967a44e1aa26dfe802751da0599ee41843e4d21a5679ed634f9",
        "checkpoints/ckpt-33998509856.pt": "3420ababf36da4b32562577c7aa552a7792b35ba8afb8c0403afac8051fad17c",
        "checkpoints/latest.pt": "ebb27c6fa08b9dd1ad040ebec4188c2d9a7851424df80e5f8d637a3e3aecbf80",
        "checkpoints/stage-0-init.pt": "a362dd7489fe5e93ca2e70f66c78f7205cd9f0b1b4fddb8296a09ddb97bd5052",
        "checkpoints/step-000100.pt": "f96d164a7b2a037afb8f90ba3e1a7a5b754cd13360aa78f75f42fc466abe4bed",
        "checkpoints/step-000200.pt": "81d9a7c6918d2d4ab7d485ecc3948beda79d623abe9779a628fecee936c7b320",
        "checkpoints/step-000300.pt": "4b44cc8780ef7a6774913b36ac41b8dc91fb9152b6b49d27754ddafc29b8d29b",
        "config.yaml": "26771ae8ef9205622d0a04cdb55f4b9db0590f89fa2531e01612ace761e39860",
        "curriculum.jsonl": "7439572cb2940ce8a440b22796315c552c8dea725c70297c169ef9f065c4b68b",
        "logs/train.log": "2d37ff4e0225b8af4437da65a89c8fac2ae316df429f38b0e1a31798a3a3fe1b",
        "logs/train.log.jsonl": "a1e33362cd86b66cc427a635b6bf4ea34a53f11f59231ff18c114b312266182a",
        "preflight.json": "3dd845c5800d5848249e66282264558747edf352f6cd009933ddb6e752ddfc89",
        "run_start_rng.pt": "b408644f117176e535ac6db01f44877bcd90557af709bc6090805ad006917a73",
        "splits.json": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "status.json": "5b17dc3042ed250d6e8b158c771742533c19784b0c7a45aef30b9cd0f375687b",
        "summary.json": "d5c0ab25df0e4b5aef64695f57792141b754118e55bf5e969708b26a0ece075a",
        "summary.md": "dcdf0583275079542ac11648f0f642e39d867145cbf1c3d9534317b143dcc8fb",
        "tb/<host>.87113.0": "7e7dfbaaad0ac403c81edf1749d079f8d4666690756559c5ab4fff78e596cb51",
        "training_metadata.json": "a7011e77a5f7c91720f924117de06b8892e316e35c19531ba8617c4c1236a095",
        "validation.jsonl": "eac23d62246746090e9c81870e5c6dfb28a65913b99fc19df7ae803b91a360d1",
        "validation_gate/step-00000100.json": "4ae798bfe52984d975d6f6033d9f6e836adb709f95e2387731cb669ac0ec282a",
        "validation_gate/step-00000200.json": "79ba8356dfac2a1447027fbe66eba1c04e47b774e1d1b366086878d876b50547",
        "validation_gate/step-00000300.json": "6ea12bc111137d764cb2de534aa057514424013f1d34d9000091e84ab7cadace"
      },
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": "fresh",
          "command": "/usr/bin/caffeinate -is <home>/miniforge3/envs/pinn-train/bin/python -m pinn.train --config configs/stage0-v23g6-smoke.yaml --stage-0-only",
          "process_pid": 87113,
          "start_utc": "2026-09-29T02:38:47.359565+00:00",
          "end_utc": "2026-09-29T03:44:26.327917+00:00",
          "wall_clock_secs": 3938.968352,
          "exit_code": 0,
          "git_head": "ef4764f92d9ad23fa90c936166137944dc5e4aea",
          "config_sha256": "f6f6835ee18efee5bd8c08865e4d7d3a63ee1dfcd890675d4cfebea45fa15781",
          "disposition": "finished",
          "boundary_checkpoint": null,
          "resume_checkpoint": null
        }
      ]
    },
    {
      "band_generation": 6,
      "launch_kind": "graded",
      "run_name": "stage0-v23g6-seed42",
      "seed": 42,
      "git_head": "ef4764f92d9ad23fa90c936166137944dc5e4aea",
      "config_path": "configs/stage0-v23g6-seed42.yaml",
      "config_sha256": "d1efdcf7ee709b18622d8a2f8d37b8df13ba126fc930696cb7caf4817cfa4dda",
      "artifact_dir": "runs/stage0-v23g6-seed42",
      "command": "/usr/bin/caffeinate -is <home>/miniforge3/envs/pinn-train/bin/python -m pinn.train --config configs/stage0-v23g6-seed42.yaml --stage-0-only",
      "stage_0_only": true,
      "collocation_count": 4096,
      "replay_count": 240,
      "front_advance_window_n": 500,
      "max_epochs": 1000,
      "n_adam": 1000,
      "environment": {
        "python_version": "3.11.15",
        "sw_vers": "ProductName:\t\tmacOS\nProductVersion:\t\t26.5.1\nBuildVersion:\t\t25F80",
        "torch_build": "7269437d655783a26cba32aa88195b741ff496aa",
        "torch_version": "2.12.1"
      },
      "corpus": {
        "splits_sha256": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "s_h": 22.321729071058996,
        "eps_h": 0.0022321729071058997,
        "n_train": 1812
      },
      "monitor": null,
      "r_ref": 19749775821.24417,
      "r_ref_artifact_path": "pinn/verification/artifacts/r_ref_stage0.json",
      "r_ref_artifact_sha256": "c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff",
      "launch_started_utc": "2026-09-29T03:46:14.276381+00:00",
      "completion_utc": null,
      "wall_clock_secs": null,
      "process_pid": 25061,
      "exit_code": null,
      "final_process_disposition": "process-lost",
      "ledger_disposition": "blocked",
      "final_guard_disposition": null,
      "guard": null,
      "evaluation": "preserved-unspent",
      "in_final_band": true,
      "terminal": false,
      "artifact_hashes": {
        "checkpoints/best.pt": "f33aa849a80dd21834a9feded038cea02916107611fbcf55e4501c3735de7508",
        "checkpoints/ckpt-38043381130.pt": "80920c36767df41b112268ed6fb15dd98ad7e22e4c2fc552778274fac3358466",
        "checkpoints/latest.pt": "27c537a18568ca499eee768f2013402635ed797154bf6b842df84b0e20917de0",
        "checkpoints/stage-0-init.pt": "3f096b6a96fe8927cbb474eda4f83c84251cbb1f081da2adad0ffb63298cf899",
        "checkpoints/step-000490.pt": "24739182a1d7f343eb3ead1f9661b7098937a906eb9e8efc5c273ebff9c4eac2",
        "checkpoints/step-000500.pt": "4d8e07bdb410926e2745dd730fd0c2947ec8effbf698575637dcb69be7c59ea0",
        "checkpoints/step-000510.pt": "649acdc9416426deebe96bcb93ac1119aa4a8cc5bfc7caf84fcbe25e4c26db5c",
        "config.yaml": "97c959a5c4042826bc112bc7b679840b81c80dfaf5d44f9d190533e1aa8fb796",
        "logs/train.log": "e272d446e6a5f9a8a65ea61b374261b436edc9198fe54d17340283b4e95464af",
        "logs/train.log.jsonl": "e4f8b0bd929895658e2e50b684225db7652dea6ddb224e8cb62ee5d13cee25b3",
        "preflight.json": "a167ea15855219e524011b3de8f32406fbf39f5663d9fa351b0f64d762871794",
        "run_start_rng.pt": "7f147d4565f9640366f4f1c933a7cf2482a69bec15bcd267878565adf5fe1d1c",
        "splits.json": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "status.json": "710f0e61d02533c54171fe7525100e84d60030c55d331ef58eea0de7df6a47be",
        "summary.json": "e373c48c4d997766340a260078c90b15cf31d89818754d7fa9ad04aa48004e5e",
        "summary.md": "575778ca70c6ada3d05377985f1275cc2a2b67b7a4a888e270307c692d5d2317",
        "tb/<host>.25061.0": "bc2048ad6623dc18cb107fe080459d0087bae54912628c2cacc269a2b69ed1a0",
        "training_metadata.json": "a7011e77a5f7c91720f924117de06b8892e316e35c19531ba8617c4c1236a095",
        "validation.jsonl": "60f608c779db55c656bd4ecb69bc82c22e70cb368f109c52e5c2220bcafabc49",
        "validation_gate/step-00000100.json": "5b2fb4bcc770a1879a0a4da67cada3ab9d57977a5bd62938531246536fbc7bf4",
        "validation_gate/step-00000200.json": "b2487dd9c90cf62ed29257d8cbf67062f3dd3f64c653c17eb225623b16c4800f",
        "validation_gate/step-00000300.json": "285702873de30445fd6142fe7af6dd024eb39e14b7a4c3c10bb071b2f3eb9bec",
        "validation_gate/step-00000400.json": "5693aeef04fd270e43404a51675268b11306cb4e6016bd4bbe10b6d85b921391",
        "validation_gate/step-00000500.json": "38b58f05d25c9f41b2798732c9b9d4df14bca93ddf77ce91dd0cc9861b5b0742"
      },
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": "fresh",
          "command": "/usr/bin/caffeinate -is <home>/miniforge3/envs/pinn-train/bin/python -m pinn.train --config configs/stage0-v23g6-seed42.yaml --stage-0-only",
          "process_pid": 25061,
          "start_utc": "2026-09-29T03:46:14.276381+00:00",
          "end_utc": null,
          "wall_clock_secs": null,
          "exit_code": null,
          "git_head": "ef4764f92d9ad23fa90c936166137944dc5e4aea",
          "config_sha256": "d1efdcf7ee709b18622d8a2f8d37b8df13ba126fc930696cb7caf4817cfa4dda",
          "disposition": "process-lost",
          "boundary_checkpoint": null,
          "resume_checkpoint": null
        }
      ],
      "blocked_state_path": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state-g6.json",
      "blocked_state_sha256": "8982868e87f9dead400257d17e51dc9d1d2ff8b211adfd61d63344891498faec",
      "last_logged_step": 513,
      "last_heartbeat_utc": "2026-09-29T05:33:21.581195+00:00",
      "process_loss_detected_utc": "2026-09-29T12:59:31.821563+00:00",
      "latest_checkpoint": {
        "path": "runs/stage0-v23g6-seed42/checkpoints/latest.pt",
        "sha256": "27c537a18568ca499eee768f2013402635ed797154bf6b842df84b0e20917de0",
        "global_step": 510,
        "curriculum": {
          "stage": 0,
          "phase": "2a",
          "epoch": 510,
          "step": 510,
          "disposition_log_pointer": null
        },
        "invariant_b_state": {
          "front_high_water": 2,
          "last_advance_step": 353
        },
        "kind": "rolling-not-governed-stop-boundary"
      }
    }
  ]
}
```
