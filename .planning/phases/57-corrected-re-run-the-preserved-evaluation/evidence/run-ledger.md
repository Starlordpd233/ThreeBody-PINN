# Phase 57 Run Ledger

The ledger is append-only during the smoke and graded run window.
Generations 1 and 2 are retained historical attempts; neither belongs to the
final band. The final generation is set only after a complete generation-3
band or the authorized scientific terminal branch is recorded.

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
    }
  ]
}
```
