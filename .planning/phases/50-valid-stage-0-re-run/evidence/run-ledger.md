# Phase 50 Run Ledger

**Scaffolded:** 2026-08-12 (plan 50-01)

## The D-22 rule this ledger enforces

Every launch that starts — refused before construction, HALTed by a guard or
an invariant, failed on an exception, interrupted, later superseded by a fresh
retry or a new band generation, or graded to completion — gets a record in
this ledger. The band Phase 51 sees must be the whole record, not the
surviving subset: a retry is a new attempt, never a silent overwrite, and any
unexpected resume history is preserved as terminal evidence rather than
discarded (`50-CONTEXT.md` D-22). This is the phase-local analog of the v2.0
`43-*/evidence/pilot/README.md` receipt discipline, extended with the
`band_generation`/`git_head`/attempt-ordinal machinery that phase needed only
after Phase 50 made mid-project commits possible again (`50-CONTEXT.md`
D-17).

## Reproduction boundary and write ownership

This scaffold is committed empty by plan 50-01 (this plan), before any
Phase-50 launch. Plan 50-02 **appends** `band_generations[]` and `records[]`
entries as **uncommitted working-tree edits** while the band is open — D-17
forbids a mid-band commit, and an uncommitted edit to this file does not
invalidate the timing calibration (only a *commit* does). Plan 50-02 closes
the generation (sets `status: "complete"` or `"terminal"` on the
`band_generations[]` entry, sets `final_band_generation`) and **commits** this
file, along with the volatile protocol evidence it references, in one
evidence commit at the end of the band. Plan 50-03 then **appends** the
extraction/candidate-selection receipt in a **separate** evidence commit; it
never edits an already-closed `band_generations[]` or `records[]` entry in
place.

## Machine-readable ledger (empty at scaffold time)

Tests and later plans parse this block without inferring shape from directory
contents.

<!-- phase50-run-ledger-schema: phase50-run-ledger/v2 -->
```json
{
  "schema": "phase50-run-ledger/v2",
  "final_band_generation": null,
  "band_generations": [
    {
      "band_generation": 1,
      "git_head": "584ffddd8e7e090200b722131aa15907732440cd",
      "pre_registration_commit": "abd5f8d9bc44c31abb58194e86806ea6aa39a649",
      "committed_config_sha256_by_path": {
        "configs/stage0-rerun-seed41.yaml": "90ccd7418211ca42ebe14e06ea0bf1f62249d87e19b71c9f670c9a9b8374f073",
        "configs/stage0-rerun-seed42.yaml": "72db4aa458a8ae4eb8b2645a27fe0c01392ecd08050fb689e2cf939a982fa097",
        "configs/stage0-rerun-seed43.yaml": "1c2336d8342198a417a129d3e70e7ce53609b1d28aff3fd021a92f8bd20360e6",
        "configs/stage0-rerun-smoke.yaml": "a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a"
      },
      "committed_config_set_sha256": "e6e1fd53f93ec0b3059ff2da8eb9d27b92546b3d74fd7bffdbd0a11373a4e078",
      "corpus_snapshot": {
        "path": ".planning/phases/50-valid-stage-0-re-run/evidence/corpus/generation-1.json",
        "file_sha256": "dd2de05731c359bfe41077de8ec29cdfceb63ee9787712f50cdf7f8c4aba952e",
        "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd"
      },
      "environment_snapshot": {
        "path": ".planning/phases/50-valid-stage-0-re-run/evidence/environment/generation-1.json",
        "file_sha256": "183b642dbe73588fe46bcb448ce8cd5561a1b825075157a3780aa9df46705b96",
        "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34"
      },
      "timing_fingerprint": {
        "device": "mps",
        "dtype": "torch.float32",
        "torch_version": "2.12.1",
        "python_version": "3.11.15",
        "git_head": "584ffddd8e7e090200b722131aa15907732440cd",
        "git_head_available": true
      },
      "summary_env_fingerprint": {
        "sw_vers": "ProductName:\t\tmacOS\nProductVersion:\t\t26.5.1\nBuildVersion:\t\t25F80",
        "python_version": "3.11.15",
        "torch_version": "2.12.1",
        "torch_build": "7269437d655783a26cba32aa88195b741ff496aa"
      },
      "opened_utc": "2026-08-13T05:11:10.926743+00:00",
      "closed_utc": "2026-08-13T05:18:59.477413+00:00",
      "cleanliness_receipts": [
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-13T05:11:10.865082+00:00",
          "external_end_utc": "2026-08-13T05:11:10.925775+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-1-open-runtime.json",
          "sha256": "f112d79e3ca5adbe2f928ac6c6b7de59ceeb447cd805dd37fe7c8807265ccc33"
        },
        {
          "boundary": "corpus",
          "command": "band_ops.py snapshot_corpus",
          "external_start_utc": "2026-08-13T05:11:40.279404+00:00",
          "external_end_utc": "2026-08-13T05:11:49.403271+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-1-open-corpus.json",
          "sha256": "c5cc15928b51d141ee9b8d3397cdf8ecb6afd960b16ed07c7d5296f48d52fdbc"
        },
        {
          "boundary": "environment",
          "command": "band_ops.py capture_environment",
          "external_start_utc": "2026-08-13T05:11:51.830745+00:00",
          "external_end_utc": "2026-08-13T05:11:52.765628+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-1-open-environment.json",
          "sha256": "d6d0f05f88adfac4581fec46c13655ee6588e62b3a12da3f9afec50da7a36f99"
        },
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-13T05:11:57.115394+00:00",
          "external_end_utc": "2026-08-13T05:11:57.145710+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-1-pre-smoke-runtime.json",
          "sha256": "e36bb9b0518ef2b5454830db5259f8c24569af9c3666928e3dc348ba7629cb12"
        },
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-13T05:18:48.521227+00:00",
          "external_end_utc": "2026-08-13T05:18:48.556309+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-1-post-smoke-interrupted-runtime.json",
          "sha256": "e89cd503aac7ac445bd7f64a125a193f1936e257a0f5f34cce542a6d1a7e8160"
        },
        {
          "boundary": "corpus",
          "command": "band_ops.py snapshot_corpus",
          "external_start_utc": "2026-08-13T05:18:48.557017+00:00",
          "external_end_utc": "2026-08-13T05:18:58.444201+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-1-post-smoke-interrupted-corpus.json",
          "sha256": "ce421c286d80b07e63a6c1b3a2b7a98c944ad0ba3d556c558e3215804f5da542"
        },
        {
          "boundary": "environment",
          "command": "band_ops.py capture_environment",
          "external_start_utc": "2026-08-13T05:18:58.444745+00:00",
          "external_end_utc": "2026-08-13T05:18:59.455198+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-1-post-smoke-interrupted-environment.json",
          "sha256": "1ae8645c15a518125c8b137203ce78f89d1b774509c80c6385494ff3b44bbf3a"
        }
      ],
      "verify_invocations": [],
      "status": "terminal"
    },
    {
      "band_generation": 2,
      "git_head": "7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4",
      "pre_registration_commit": "abd5f8d9bc44c31abb58194e86806ea6aa39a649",
      "committed_config_sha256_by_path": {
        "configs/stage0-rerun-seed41.yaml": "90ccd7418211ca42ebe14e06ea0bf1f62249d87e19b71c9f670c9a9b8374f073",
        "configs/stage0-rerun-seed42.yaml": "72db4aa458a8ae4eb8b2645a27fe0c01392ecd08050fb689e2cf939a982fa097",
        "configs/stage0-rerun-seed43.yaml": "1c2336d8342198a417a129d3e70e7ce53609b1d28aff3fd021a92f8bd20360e6",
        "configs/stage0-rerun-smoke.yaml": "a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a"
      },
      "committed_config_set_sha256": "e6e1fd53f93ec0b3059ff2da8eb9d27b92546b3d74fd7bffdbd0a11373a4e078",
      "corpus_snapshot": {
        "path": ".planning/phases/50-valid-stage-0-re-run/evidence/corpus/generation-2.json",
        "file_sha256": "9aa291eb2692ca04584177bf61e7eea321f9c0533ea1046c344d09e1ac2c4d70",
        "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd"
      },
      "environment_snapshot": {
        "path": ".planning/phases/50-valid-stage-0-re-run/evidence/environment/generation-2.json",
        "file_sha256": "9650cb9ab75ef59153647ed470e5cb18db998b43d1d17eeba9b3de4ecd341bc5",
        "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34"
      },
      "timing_fingerprint": {
        "device": "mps",
        "dtype": "torch.float32",
        "torch_version": "2.12.1",
        "python_version": "3.11.15",
        "git_head": "7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4",
        "git_head_available": true
      },
      "summary_env_fingerprint": {
        "sw_vers": "ProductName:\t\tmacOS\nProductVersion:\t\t26.5.1\nBuildVersion:\t\t25F80",
        "python_version": "3.11.15",
        "torch_version": "2.12.1",
        "torch_build": "7269437d655783a26cba32aa88195b741ff496aa"
      },
      "opened_utc": "2026-08-13T05:29:45.228602+00:00",
      "closed_utc": "2026-08-13T05:46:46.377778+00:00",
      "cleanliness_receipts": [
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-13T05:29:45.192748+00:00",
          "external_end_utc": "2026-08-13T05:29:45.227883+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-2-open-runtime.json",
          "sha256": "aedf6da1e4b94fcae8f0e8f7ad2380c1d52e3e67f2a1cb8e3c76fe619cb71ec5"
        },
        {
          "boundary": "corpus",
          "command": "band_ops.py snapshot_corpus",
          "external_start_utc": "2026-08-13T05:30:10.941829+00:00",
          "external_end_utc": "2026-08-13T05:30:20.187803+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-2-open-corpus.json",
          "sha256": "6e2cb594ce5c2d884075a78a2ad5d110ff41621443b244a2c849e2d848fcd760"
        },
        {
          "boundary": "environment",
          "command": "band_ops.py capture_environment",
          "external_start_utc": "2026-08-13T05:30:22.688365+00:00",
          "external_end_utc": "2026-08-13T05:30:23.614915+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-2-open-environment.json",
          "sha256": "2ee6b0f84b16cc3e0a27869c6d3100e5d6a5c0566e516755e042c83e08841093"
        },
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-13T05:30:25.800940+00:00",
          "external_end_utc": "2026-08-13T05:30:25.829013+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-2-pre-smoke-runtime.json",
          "sha256": "ba69457657c295050b7221463ca055911c21bbd0395ccd11d3c560b69f726c0b"
        },
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-13T05:38:08.311972+00:00",
          "external_end_utc": "2026-08-13T05:38:08.338720+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-2-post-smoke-runtime.json",
          "sha256": "745016fe8b954f631885957597384d065483824361c556489540d92f31ff7dd7"
        },
        {
          "boundary": "corpus",
          "command": "band_ops.py snapshot_corpus",
          "external_start_utc": "2026-08-13T05:38:10.509231+00:00",
          "external_end_utc": "2026-08-13T05:38:20.083263+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-2-post-smoke-corpus.json",
          "sha256": "9eaa2d7243e4440fe681ba81d89b813e615491751c266c8305758784e7ab8c82"
        },
        {
          "boundary": "environment",
          "command": "band_ops.py capture_environment",
          "external_start_utc": "2026-08-13T05:38:22.530997+00:00",
          "external_end_utc": "2026-08-13T05:38:23.470088+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-2-post-smoke-environment.json",
          "sha256": "50caf09e413223676d9706b0bac3642eba5bb73b627eef951b59fad5c91d39bc"
        },
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-13T05:39:58.626388+00:00",
          "external_end_utc": "2026-08-13T05:39:58.653706+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-2-pre-seed41-runtime.json",
          "sha256": "d2ffc38662521fc253320eba013dd6745acc9dea2270b0e4a5e66424c30ab760"
        },
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-13T05:45:37.403537+00:00",
          "external_end_utc": "2026-08-13T05:45:37.429963+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-2-post-seed41-failed-runtime.json",
          "sha256": "f04d5a07801a6dc5baa13a8d7bc6d324274957f4c3bde7447145777ba9e6810d"
        },
        {
          "boundary": "corpus",
          "command": "band_ops.py snapshot_corpus",
          "external_start_utc": "2026-08-13T05:45:39.613668+00:00",
          "external_end_utc": "2026-08-13T05:45:48.826566+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-2-post-seed41-failed-corpus.json",
          "sha256": "f0badc0548feabfb86614a770642a13da746d35af21f9a6a34c640203525add1"
        },
        {
          "boundary": "environment",
          "command": "band_ops.py capture_environment",
          "external_start_utc": "2026-08-13T05:45:51.191295+00:00",
          "external_end_utc": "2026-08-13T05:45:52.132257+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-2-post-seed41-failed-environment.json",
          "sha256": "5a0c8b4b1e8df9d72f611fbc67e37612645340207bc8178eac68b1f52b743750"
        }
      ],
      "verify_invocations": [
        {
          "invocation_ordinal": 1,
          "status": "closed",
          "command": "<home>/miniforge3/bin/conda run --no-capture-output -n pinn-train python -m pinn.verify",
          "external_start_utc": "2026-08-13T05:38:42.700958+00:00",
          "external_end_utc": "2026-08-13T05:38:55.747221+00:00",
          "exit_code": 0,
          "recovered_after_executor_loss": false,
          "transcript": ".planning/phases/50-valid-stage-0-re-run/evidence/launch-transcripts/generation-2-smoke-attempt-03-invocation-01-verify.txt",
          "transcript_sha256": "48028f7aa79a0ff9b08d05cd1e988ff3e98ba0c48c72dc7799ec78e60f4243a3",
          "result": "green",
          "runtime_fingerprint": {
            "device": "mps",
            "dtype": "torch.float32",
            "torch_version": "2.12.1",
            "python_version": "3.11.15",
            "git_head": "7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4",
            "git_head_available": true
          },
          "marker": {
            "path": ".planning/phases/50-valid-stage-0-re-run/evidence/verify/generation-2-smoke-attempt-03-invocation-01-marker.json",
            "sha256": "3906629ecf3ec9346594b18b5084fb1e002d2cc4d8c5e7818d72cabb97e9d4fc",
            "timestamp": "2026-08-13T05:38:55.167386+00:00"
          }
        }
      ],
      "status": "terminal"
    },
    {
      "band_generation": 3,
      "git_head": "c4a1550b7bd889121128e31d7078a478b0a6ca8a",
      "pre_registration_commit": "c4a1550b7bd889121128e31d7078a478b0a6ca8a",
      "source_identity_commit": "312f3080ab50e35be18ba87c9f0618866265b227",
      "committed_config_sha256_by_path": {
        "configs/stage0-rerun-seed41.yaml": "90ccd7418211ca42ebe14e06ea0bf1f62249d87e19b71c9f670c9a9b8374f073",
        "configs/stage0-rerun-seed42.yaml": "72db4aa458a8ae4eb8b2645a27fe0c01392ecd08050fb689e2cf939a982fa097",
        "configs/stage0-rerun-seed43.yaml": "1c2336d8342198a417a129d3e70e7ce53609b1d28aff3fd021a92f8bd20360e6",
        "configs/stage0-rerun-smoke.yaml": "a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a"
      },
      "committed_config_set_sha256": "e6e1fd53f93ec0b3059ff2da8eb9d27b92546b3d74fd7bffdbd0a11373a4e078",
      "corpus_snapshot": {
        "path": ".planning/phases/50-valid-stage-0-re-run/evidence/corpus/generation-3.json",
        "file_sha256": "0fd40be63ec41a217b20785a96496faa762a84ceb53cd9bcb3fe8d0059d3d21e",
        "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd"
      },
      "environment_snapshot": {
        "path": ".planning/phases/50-valid-stage-0-re-run/evidence/environment/generation-3.json",
        "file_sha256": "883afc6c1f63ec3e289bb3a35f3234773bec6350f90d673cf058675dbb7a0631",
        "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34"
      },
      "timing_fingerprint": {
        "device": "mps",
        "dtype": "torch.float32",
        "torch_version": "2.12.1",
        "python_version": "3.11.15",
        "git_head": "c4a1550b7bd889121128e31d7078a478b0a6ca8a",
        "git_head_available": true
      },
      "summary_env_fingerprint": {
        "sw_vers": "ProductName:\t\tmacOS\nProductVersion:\t\t26.5.1\nBuildVersion:\t\t25F80",
        "python_version": "3.11.15",
        "torch_version": "2.12.1",
        "torch_build": "7269437d655783a26cba32aa88195b741ff496aa"
      },
      "opened_utc": "2026-08-15T02:45:24.769319+00:00",
      "closed_utc": "2026-08-15T03:13:13.899889+00:00",
      "cleanliness_receipts": [
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-15T02:45:24.733481+00:00",
          "external_end_utc": "2026-08-15T02:45:24.768715+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-open-runtime.json",
          "sha256": "6f2858d126621c036fb4d3fbd82b0ddb5fb2ba933fe5f700223c175235d80488"
        },
        {
          "boundary": "corpus",
          "command": "band_ops.py snapshot_corpus",
          "external_start_utc": "2026-08-15T02:45:45.248219+00:00",
          "external_end_utc": "2026-08-15T02:45:54.880096+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-open-corpus.json",
          "sha256": "8520d28c90fc64b7491a4e95243773afcfc91fa54e246c60aa263eabc2ac497f"
        },
        {
          "boundary": "environment",
          "command": "band_ops.py capture_environment",
          "external_start_utc": "2026-08-15T02:45:57.614852+00:00",
          "external_end_utc": "2026-08-15T02:45:58.595248+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-open-environment.json",
          "sha256": "d1264608c7c66d08dff49c609c1d0b00f4fdf37adbfb6a80623ad416345d1476"
        },
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-15T02:46:29.327057+00:00",
          "external_end_utc": "2026-08-15T02:46:29.362356+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-pre-smoke-runtime.json",
          "sha256": "147d36899d6952d9c7d9ff58ba9553871970f51d7513d0859d4cd84043d31f8a"
        },
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-15T02:53:07.040835+00:00",
          "external_end_utc": "2026-08-15T02:53:07.070322+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-post-smoke-runtime.json",
          "sha256": "7c3ad84de108695023fab6558fb5cdf961261c7ac6f392a8482754208925c724"
        },
        {
          "boundary": "corpus",
          "command": "band_ops.py snapshot_corpus",
          "external_start_utc": "2026-08-15T02:53:09.436708+00:00",
          "external_end_utc": "2026-08-15T02:53:19.323957+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-post-smoke-corpus.json",
          "sha256": "88d08c63377f3dc6e554cfaaefa4caa301f0f0d7e17fbaf547f2d52add695228"
        },
        {
          "boundary": "environment",
          "command": "band_ops.py capture_environment",
          "external_start_utc": "2026-08-15T02:53:21.775841+00:00",
          "external_end_utc": "2026-08-15T02:53:22.752813+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-post-smoke-environment.json",
          "sha256": "7fd54a92d8075d90e4163e14814a29b9b873427b7e3068b3dc7ffb82bb6e417e"
        },
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-15T03:04:41.481041+00:00",
          "external_end_utc": "2026-08-15T03:04:41.513743+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-pre-seed41-runtime.json",
          "sha256": "344eae335ce9d975b684de85850e39e214dc9b4a8cc4778d8a3a7bfd95fe64ab"
        },
        {
          "boundary": "corpus",
          "command": "band_ops.py snapshot_corpus",
          "external_start_utc": "2026-08-15T03:04:44.144587+00:00",
          "external_end_utc": "2026-08-15T03:04:54.116748+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-pre-seed41-corpus.json",
          "sha256": "dc34a0f6500d598a1ecc8543af98943d0d60b1e17a00b3ac0461bd2026ff5cd3"
        },
        {
          "boundary": "environment",
          "command": "band_ops.py capture_environment",
          "external_start_utc": "2026-08-15T03:04:56.687018+00:00",
          "external_end_utc": "2026-08-15T03:04:57.694950+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-pre-seed41-environment.json",
          "sha256": "d2164a06d824c42770399b9188bbbb4e0f69302fc26036880fcd914a35231ceb"
        },
        {
          "boundary": "runtime",
          "command": "git status --porcelain --untracked-files=all -- pinn/ configs/ scripts/train-unattended.sh pyproject.toml",
          "external_start_utc": "2026-08-15T03:12:57.469844+00:00",
          "external_end_utc": "2026-08-15T03:12:57.500274+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-post-seed41-halted-runtime.json",
          "sha256": "8b8576fe65cd3c785b77949853aa9c01fb3661b628e7f012d64d66a6ef5b59fc"
        },
        {
          "boundary": "corpus",
          "command": "band_ops.py snapshot_corpus",
          "external_start_utc": "2026-08-15T03:12:59.830732+00:00",
          "external_end_utc": "2026-08-15T03:13:09.984681+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-post-seed41-halted-corpus.json",
          "sha256": "6e8d7304d1645b99358ed54c9148c992fa4ec123009821f5c06e620320df0dc3"
        },
        {
          "boundary": "environment",
          "command": "band_ops.py capture_environment",
          "external_start_utc": "2026-08-15T03:13:12.694351+00:00",
          "external_end_utc": "2026-08-15T03:13:13.681354+00:00",
          "exit_code": 0,
          "path": ".planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-3-post-seed41-halted-environment.json",
          "sha256": "77482bd14208654fe59b28abf535eccbd51848f42a4592868a41a60e9c578b0b"
        }
      ],
      "verify_invocations": [
        {
          "invocation_ordinal": 1,
          "status": "closed",
          "command": "<home>/miniforge3/bin/conda run --no-capture-output -n pinn-train python -m pinn.verify",
          "external_start_utc": "2026-08-15T02:52:24.784279+00:00",
          "external_end_utc": "2026-08-15T02:52:41Z",
          "exit_code": 0,
          "recovered_after_executor_loss": false,
          "transcript": ".planning/phases/50-valid-stage-0-re-run/evidence/launch-transcripts/generation-3-smoke-attempt-04-invocation-01-verify.txt",
          "transcript_sha256": "48028f7aa79a0ff9b08d05cd1e988ff3e98ba0c48c72dc7799ec78e60f4243a3",
          "result": "green",
          "runtime_fingerprint": {
            "device": "mps",
            "dtype": "torch.float32",
            "torch_version": "2.12.1",
            "python_version": "3.11.15",
            "git_head": "c4a1550b7bd889121128e31d7078a478b0a6ca8a",
            "git_head_available": true
          },
          "marker": {
            "path": ".planning/phases/50-valid-stage-0-re-run/evidence/verify/generation-3-smoke-attempt-04-invocation-01-marker.json",
            "sha256": "2ae78910532272427ddfcf357f383236fcd3796aab2ac24bf9faaff4d8e3ab30",
            "timestamp": "2026-08-15T02:52:40.248304+00:00"
          }
        }
      ],
      "calibration_path": ".planning/phases/50-valid-stage-0-re-run/evidence/calibration/generation-3.json",
      "status": "terminal",
      "expected_splits_sha256": {
        "41": "c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86",
        "42": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "43": "a8618b0c6d0f0f1487fe4e3f8c0409a3e3398c7e8cb8bee2b4d3d7962a576172"
      },
      "owner_checkpoint": {
        "choice": "proceed",
        "recorded_utc": "2026-08-15T03:02:42.070482+00:00"
      },
      "seed41_first_validation_proof": {
        "seed": "41",
        "recorded_utc": "2026-08-15T03:08:31.104084+00:00",
        "stage_zero_underpopulated_absent": true,
        "validation_events_observed": 1,
        "first_event_step": 100,
        "status_step": 145,
        "status_state": "running"
      }
    }
  ],
  "records": [
    {
      "band_generation": 1,
      "run_name": "stage0-rerun-smoke",
      "attempt_ordinal": 1,
      "artifact_dir": "runs/stage0-rerun-smoke-attempt-01-interrupted-20260813T052918Z",
      "config": "configs/stage0-rerun-smoke.yaml",
      "source_config_sha256": "a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a",
      "frozen_config_sha256": "3db88b697aac2f3c61075e402602fb7a447aaf9113109669dc5925934e2dd46d",
      "config_identity_digest": "3db88b697aac2f3c",
      "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd",
      "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34",
      "git_head": "584ffddd8e7e090200b722131aa15907732440cd",
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": "fresh",
          "status": "closed",
          "intended_artifact_dir": "runs/stage0-rerun-smoke",
          "launch_command": "<home>/miniforge3/bin/conda run -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-rerun-smoke.yaml --stage-0-only",
          "launch_transcript": ".planning/phases/50-valid-stage-0-re-run/evidence/launch-transcripts/stage0-rerun-smoke-attempt-01-invocation-01-train.txt",
          "transcript_sha256": "62fc24eefd4253894be87647e1999669c787404f9340b4ee05ae62869853df6b",
          "external_start_utc": "2026-08-13T05:12:10.914573+00:00",
          "external_end_utc": null,
          "exit_code": null,
          "recovered_after_executor_loss": true,
          "git_head": "584ffddd8e7e090200b722131aa15907732440cd",
          "source_config_sha256": "a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a",
          "frozen_config_sha256": "3db88b697aac2f3c61075e402602fb7a447aaf9113109669dc5925934e2dd46d",
          "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd",
          "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34",
          "timing_fingerprint": {
            "device": "mps",
            "dtype": "torch.float32",
            "torch_version": "2.12.1",
            "python_version": "3.11.15",
            "git_head": "584ffddd8e7e090200b722131aa15907732440cd",
            "git_head_available": true
          },
          "summary_env_fingerprint": {
            "sw_vers": "ProductName:\t\tmacOS\nProductVersion:\t\t26.5.1\nBuildVersion:\t\t25F80",
            "python_version": "3.11.15",
            "torch_version": "2.12.1",
            "torch_build": "7269437d655783a26cba32aa88195b741ff496aa"
          },
          "resume_checkpoint": null,
          "calibration_before": {
            "path": ".planning/phases/50-valid-stage-0-re-run/evidence/calibration/pre-smoke-20260813T051154Z-d931a3fbda20.json",
            "sha256": "d931a3fbda20ac6e8bf014268b81af05dfe2361d62396bbc7cee9de91fd2944b",
            "timestamp": "2026-07-22T08:03:55.336764+00:00",
            "source_path": "runs/.calibration/archive/pre-smoke-20260813T051154Z-d931a3fbda20.json"
          },
          "calibration_after": null,
          "observed_summary_disposition": "interrupted",
          "observed_guard_disposition": null,
          "artifact_sha256_at_exit": {
            "config.yaml": "3db88b697aac2f3c61075e402602fb7a447aaf9113109669dc5925934e2dd46d",
            "summary.json": "74e43b90f28abbba687b05ad129867d8aa0e5c85cd07e54817ce99ab6e0554a5",
            "summary.md": "216f366164fde68ec8a498f4daa20297a0b2ca628e31d28044f73506b108180d",
            "preflight.json": "359d2efdfb6d7e81878ee664cdd1f4a2f763b816f12a2d3bc7636d95bf947b0d",
            "training_metadata.json": "a7011e77a5f7c91720f924117de06b8892e316e35c19531ba8617c4c1236a095",
            "splits.json": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
            "curriculum.jsonl": "e1743dda8ef75b1577352f1f8e89b26659d876e2bc5fcef790968c3ffdaf396e",
            "status.json": "d837f467ce02402d19419289e10c03688ef98f209da62ebe4192981cce29a9d4",
            "logs/train.log.jsonl": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "run_start_rng.pt": "ebac994b484fca26b164bcf159648e1d0d35812a539b6e919673ffe2a83cc277",
            "checkpoints/latest.pt": "cb066be1dbde5ff1411e9f8ebc9897844b89a3e2b092851ace437a680651c9b4",
            "checkpoints/step-000000.pt": "6e0cda51706a9cdf62dc113d12d6291c439e032c1f78877b7d277fed283be9d4"
          },
          "invocation_snapshot": null
        }
      ],
      "final_process_disposition": "interrupted",
      "final_guard_disposition": null,
      "ledger_disposition": "interrupted",
      "protocol_labels": [],
      "in_final_band": false,
      "archive_move": {
        "from": "runs/stage0-rerun-smoke",
        "to": "runs/stage0-rerun-smoke-attempt-01-interrupted-20260813T052918Z",
        "verified_utc": "2026-08-13T05:29:18.692506+00:00",
        "hashes_equal": true
      },
      "terminal_artifact_sha256": {
        "config.yaml": "3db88b697aac2f3c61075e402602fb7a447aaf9113109669dc5925934e2dd46d",
        "summary.json": "74e43b90f28abbba687b05ad129867d8aa0e5c85cd07e54817ce99ab6e0554a5",
        "summary.md": "216f366164fde68ec8a498f4daa20297a0b2ca628e31d28044f73506b108180d",
        "preflight.json": "359d2efdfb6d7e81878ee664cdd1f4a2f763b816f12a2d3bc7636d95bf947b0d",
        "training_metadata.json": "a7011e77a5f7c91720f924117de06b8892e316e35c19531ba8617c4c1236a095",
        "splits.json": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "curriculum.jsonl": "e1743dda8ef75b1577352f1f8e89b26659d876e2bc5fcef790968c3ffdaf396e",
        "status.json": "d837f467ce02402d19419289e10c03688ef98f209da62ebe4192981cce29a9d4",
        "logs/train.log.jsonl": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "run_start_rng.pt": "ebac994b484fca26b164bcf159648e1d0d35812a539b6e919673ffe2a83cc277",
        "checkpoints/latest.pt": "cb066be1dbde5ff1411e9f8ebc9897844b89a3e2b092851ace437a680651c9b4",
        "checkpoints/step-000000.pt": "6e0cda51706a9cdf62dc113d12d6291c439e032c1f78877b7d277fed283be9d4"
      },
      "reason": "Executor-wrapper timeout killed the launch shell; the smoke process recorded disposition=interrupted before any Adam step (status.state=interrupted, curriculum HALT at step 0 with no failure bundle). preflight_status=passed; eval01_precondition_i=True; observed training_metadata s_h=22.321729071058996 eps_h=0.0022321729071058997 n_train=1812 (setup-time values from the interrupted attempt; D-14 not discharged because the smoke did not finish and wrote no calibration). Phase 50 forbids --resume; this interruption is terminal.",
      "retry_authorization": null
    },
    {
      "band_generation": 2,
      "run_name": "stage0-rerun-smoke",
      "attempt_ordinal": 2,
      "artifact_dir": null,
      "config": "configs/stage0-rerun-smoke.yaml",
      "source_config_sha256": "a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a",
      "frozen_config_sha256": null,
      "config_identity_digest": null,
      "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd",
      "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34",
      "git_head": "7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4",
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": "fresh",
          "status": "closed",
          "intended_artifact_dir": "runs/stage0-rerun-smoke",
          "launch_command": "<home>/miniforge3/bin/conda run --no-capture-output -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-rerun-smoke.yaml --stage-0-only",
          "launch_transcript": ".planning/phases/50-valid-stage-0-re-run/evidence/launch-transcripts/stage0-rerun-smoke-attempt-02-invocation-01-train.txt",
          "transcript_sha256": "35dc70527201ea020c33b584c4b46579eef278ff27ae5dc1b65c673d34b457e0",
          "external_start_utc": "2026-08-13T05:30:43.327347+00:00",
          "external_end_utc": "2026-08-13T05:31:19.379274+00:00",
          "exit_code": 127,
          "recovered_after_executor_loss": false,
          "git_head": "7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4",
          "source_config_sha256": "a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a",
          "frozen_config_sha256": null,
          "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd",
          "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34",
          "timing_fingerprint": {
            "device": "mps",
            "dtype": "torch.float32",
            "torch_version": "2.12.1",
            "python_version": "3.11.15",
            "git_head": "7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4",
            "git_head_available": true
          },
          "summary_env_fingerprint": {
            "sw_vers": "ProductName:\t\tmacOS\nProductVersion:\t\t26.5.1\nBuildVersion:\t\t25F80",
            "python_version": "3.11.15",
            "torch_version": "2.12.1",
            "torch_build": "7269437d655783a26cba32aa88195b741ff496aa"
          },
          "resume_checkpoint": null,
          "calibration_before": {
            "path": ".planning/phases/50-valid-stage-0-re-run/evidence/calibration/pre-smoke-20260813T051154Z-d931a3fbda20.json",
            "sha256": "d931a3fbda20ac6e8bf014268b81af05dfe2361d62396bbc7cee9de91fd2944b",
            "timestamp": "2026-07-22T08:03:55.336764+00:00",
            "source_path": "runs/.calibration/archive/pre-smoke-20260813T051154Z-d931a3fbda20.json"
          },
          "calibration_after": null,
          "observed_summary_disposition": null,
          "observed_guard_disposition": null,
          "artifact_sha256_at_exit": {},
          "invocation_snapshot": null
        }
      ],
      "final_process_disposition": null,
      "final_guard_disposition": null,
      "ledger_disposition": "failed",
      "protocol_labels": [],
      "in_final_band": false,
      "archive_move": null,
      "terminal_artifact_sha256": {},
      "reason": "Launcher wrapper used setsid, which is not present on this macOS host (transcript: command not found: setsid). No run directory was constructed; no training process started. Closed as a pre-construction setup failure. Fresh attempt 3 will launch with nohup only. Not a resume. Not a scientific/transient retry.",
      "retry_authorization": null
    },
    {
      "band_generation": 2,
      "run_name": "stage0-rerun-smoke",
      "attempt_ordinal": 3,
      "artifact_dir": "runs/stage0-rerun-smoke-attempt-03-finished-20260815T024505Z",
      "config": "configs/stage0-rerun-smoke.yaml",
      "source_config_sha256": "a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a",
      "frozen_config_sha256": "3db88b697aac2f3c61075e402602fb7a447aaf9113109669dc5925934e2dd46d",
      "config_identity_digest": "3db88b697aac2f3c",
      "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd",
      "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34",
      "git_head": "7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4",
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": "fresh",
          "status": "closed",
          "intended_artifact_dir": "runs/stage0-rerun-smoke",
          "launch_command": "<home>/miniforge3/bin/conda run --no-capture-output -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-rerun-smoke.yaml --stage-0-only",
          "launch_transcript": ".planning/phases/50-valid-stage-0-re-run/evidence/launch-transcripts/stage0-rerun-smoke-attempt-03-invocation-01-train.txt",
          "transcript_sha256": "a72361503a9d2eb7fccdbec6e12e73179020fea16eb4945057e26f14fdf32742",
          "external_start_utc": "2026-08-13T05:31:36.039580+00:00",
          "external_end_utc": "2026-08-13T05:35:25.000000+00:00",
          "exit_code": 0,
          "recovered_after_executor_loss": false,
          "git_head": "7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4",
          "source_config_sha256": "a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a",
          "frozen_config_sha256": "3db88b697aac2f3c61075e402602fb7a447aaf9113109669dc5925934e2dd46d",
          "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd",
          "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34",
          "timing_fingerprint": {
            "device": "mps",
            "dtype": "torch.float32",
            "torch_version": "2.12.1",
            "python_version": "3.11.15",
            "git_head": "7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4",
            "git_head_available": true
          },
          "summary_env_fingerprint": {
            "sw_vers": "ProductName:\t\tmacOS\nProductVersion:\t\t26.5.1\nBuildVersion:\t\t25F80",
            "python_version": "3.11.15",
            "torch_version": "2.12.1",
            "torch_build": "7269437d655783a26cba32aa88195b741ff496aa"
          },
          "resume_checkpoint": null,
          "calibration_before": {
            "path": ".planning/phases/50-valid-stage-0-re-run/evidence/calibration/pre-smoke-20260813T051154Z-d931a3fbda20.json",
            "sha256": "d931a3fbda20ac6e8bf014268b81af05dfe2361d62396bbc7cee9de91fd2944b",
            "timestamp": "2026-07-22T08:03:55.336764+00:00",
            "source_path": "runs/.calibration/archive/pre-smoke-20260813T051154Z-d931a3fbda20.json"
          },
          "calibration_after": {
            "path": ".planning/phases/50-valid-stage-0-re-run/evidence/calibration/generation-2-smoke-attempt-03-invocation-01.json",
            "sha256": "e111f020bcdfc7ccfb60352b0f4615aeaa1a4e15d46b98a2e75e7571dc215b43",
            "timestamp": "2026-08-13T05:35:24.167120+00:00",
            "source_path": "runs/.calibration/stage0-timing.json"
          },
          "observed_summary_disposition": "finished",
          "observed_guard_disposition": null,
          "artifact_sha256_at_exit": {
            "config.yaml": "3db88b697aac2f3c61075e402602fb7a447aaf9113109669dc5925934e2dd46d",
            "summary.json": "df545ed947965714a2af469235b84fe6d6f2ec54691567fdb69397847ef945f8",
            "summary.md": "edcdc0d0ab39b5fa222b6c645185382c57358c1cd74aa35ea68a5558b7467675",
            "preflight.json": "359d2efdfb6d7e81878ee664cdd1f4a2f763b816f12a2d3bc7636d95bf947b0d",
            "training_metadata.json": "a7011e77a5f7c91720f924117de06b8892e316e35c19531ba8617c4c1236a095",
            "splits.json": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
            "curriculum.jsonl": "7439572cb2940ce8a440b22796315c552c8dea725c70297c169ef9f065c4b68b",
            "validation.jsonl": "c918dbae7ec4331bacefa5a2ebb98a04b888657dc731f28c2c4301935aafe898",
            "status.json": "a38256e1269e201a3a8f50cc2d0378c4371c33939e8f6544d247ef23b28ed5ae",
            "logs/train.log.jsonl": "3028fcd3f5ce6bce59f706ae25bb38a40f40dba1712431f72ea8a7f8d763e7aa",
            "run_start_rng.pt": "d867dc5c9a924225fd888db1df0db5607115e12e9ecb4d6ff29b64f529224c34",
            "checkpoints/best.pt": "7b1e34cc531f20e3367b8fab928d1683cb6bff2a70c7139555a6ea768ffe6dd2",
            "checkpoints/latest.pt": "d6468a817820504b28e434f4991e2faf7ad2e370560543e65bf27c7b35d4f85e",
            "checkpoints/step-000300.pt": "cbaedf3090aaed06ff8ba9f5e461b6a963e83f181c8bb27a81d574b699725307"
          },
          "invocation_snapshot": null
        }
      ],
      "final_process_disposition": "finished",
      "final_guard_disposition": null,
      "ledger_disposition": "finished",
      "protocol_labels": [],
      "in_final_band": false,
      "archive_move": {
        "from": "runs/stage0-rerun-smoke",
        "to": "runs/stage0-rerun-smoke-attempt-03-finished-20260815T024505Z",
        "verified_utc": "2026-08-15T02:45:06.004650+00:00",
        "hashes_equal": true
      },
      "terminal_artifact_sha256": {
        "config.yaml": "3db88b697aac2f3c61075e402602fb7a447aaf9113109669dc5925934e2dd46d",
        "summary.json": "df545ed947965714a2af469235b84fe6d6f2ec54691567fdb69397847ef945f8",
        "summary.md": "edcdc0d0ab39b5fa222b6c645185382c57358c1cd74aa35ea68a5558b7467675",
        "preflight.json": "359d2efdfb6d7e81878ee664cdd1f4a2f763b816f12a2d3bc7636d95bf947b0d",
        "training_metadata.json": "a7011e77a5f7c91720f924117de06b8892e316e35c19531ba8617c4c1236a095",
        "splits.json": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "curriculum.jsonl": "7439572cb2940ce8a440b22796315c552c8dea725c70297c169ef9f065c4b68b",
        "validation.jsonl": "c918dbae7ec4331bacefa5a2ebb98a04b888657dc731f28c2c4301935aafe898",
        "status.json": "a38256e1269e201a3a8f50cc2d0378c4371c33939e8f6544d247ef23b28ed5ae",
        "logs/train.log.jsonl": "3028fcd3f5ce6bce59f706ae25bb38a40f40dba1712431f72ea8a7f8d763e7aa",
        "run_start_rng.pt": "d867dc5c9a924225fd888db1df0db5607115e12e9ecb4d6ff29b64f529224c34",
        "checkpoints/best.pt": "7b1e34cc531f20e3367b8fab928d1683cb6bff2a70c7139555a6ea768ffe6dd2",
        "checkpoints/latest.pt": "d6468a817820504b28e434f4991e2faf7ad2e370560543e65bf27c7b35d4f85e",
        "checkpoints/step-000300.pt": "cbaedf3090aaed06ff8ba9f5e461b6a963e83f181c8bb27a81d574b699725307"
      },
      "reason": "Calibration + first-real-corpus-contact smoke (in_final_band false; D-01/D-13/D-14). Observed training_metadata s_h=22.321729071058996 eps_h=0.0022321729071058997 n_train=1812. preflight_status=passed including affirmative invariant_b_window N=500. Calibration valid=true git_head=7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4 s_per_step=0.13972535059194488 gate_input_1000=139.7s (shipped gate input, not ETA). Curriculum journal disposition HALT at step 300 is stage-exit after Adam budget exhaustion under --stage-0-only, not a guard or invariant-B HALT (failure/ empty; final_guard_disposition null; no stage-1 artifacts). Validation-gate TypeError warnings at steps 100/200/300 left gate_status=failed:TypeError and eval01_precondition_iii=false; recorded, not used to change any rule (D-19). D-18 verify GREEN; gate_input<=1800s so graded launch is admissible.",
      "retry_authorization": null
    },
    {
      "band_generation": 2,
      "run_name": "stage0-rerun-seed41",
      "attempt_ordinal": 1,
      "artifact_dir": "runs/stage0-rerun-seed41-attempt-01-failed-20260815T024506Z",
      "config": "configs/stage0-rerun-seed41.yaml",
      "source_config_sha256": "90ccd7418211ca42ebe14e06ea0bf1f62249d87e19b71c9f670c9a9b8374f073",
      "frozen_config_sha256": "8a7e4c8b3904da24224702679bde8cfb98764eba65e1707dc609014de3b258da",
      "config_identity_digest": "8a7e4c8b3904da24",
      "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd",
      "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34",
      "git_head": "7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4",
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": "fresh",
          "status": "closed",
          "intended_artifact_dir": "runs/stage0-rerun-seed41",
          "launch_command": "<home>/miniforge3/bin/conda run --no-capture-output -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-rerun-seed41.yaml --stage-0-only",
          "launch_transcript": ".planning/phases/50-valid-stage-0-re-run/evidence/launch-transcripts/stage0-rerun-seed41-attempt-01-invocation-01-train.txt",
          "transcript_sha256": "d86417c213370eb5f15e19c66ec4e56292705639904f1bf8c84052f536f2721d",
          "external_start_utc": "2026-08-13T05:40:00.798493+00:00",
          "external_end_utc": "2026-08-13T05:43:18.000000+00:00",
          "exit_code": 1,
          "recovered_after_executor_loss": false,
          "git_head": "7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4",
          "source_config_sha256": "90ccd7418211ca42ebe14e06ea0bf1f62249d87e19b71c9f670c9a9b8374f073",
          "frozen_config_sha256": "8a7e4c8b3904da24224702679bde8cfb98764eba65e1707dc609014de3b258da",
          "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd",
          "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34",
          "timing_fingerprint": {
            "device": "mps",
            "dtype": "torch.float32",
            "torch_version": "2.12.1",
            "python_version": "3.11.15",
            "git_head": "7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4",
            "git_head_available": true
          },
          "summary_env_fingerprint": {
            "sw_vers": "ProductName:\t\tmacOS\nProductVersion:\t\t26.5.1\nBuildVersion:\t\t25F80",
            "python_version": "3.11.15",
            "torch_version": "2.12.1",
            "torch_build": "7269437d655783a26cba32aa88195b741ff496aa"
          },
          "resume_checkpoint": null,
          "calibration_before": {
            "path": ".planning/phases/50-valid-stage-0-re-run/evidence/calibration/generation-2-smoke-attempt-03-invocation-01.json",
            "sha256": "e111f020bcdfc7ccfb60352b0f4615aeaa1a4e15d46b98a2e75e7571dc215b43",
            "timestamp": "2026-08-13T05:35:24.167120+00:00",
            "source_path": "runs/.calibration/stage0-timing.json"
          },
          "calibration_after": {
            "path": ".planning/phases/50-valid-stage-0-re-run/evidence/calibration/generation-2-smoke-attempt-03-invocation-01.json",
            "sha256": "e111f020bcdfc7ccfb60352b0f4615aeaa1a4e15d46b98a2e75e7571dc215b43",
            "timestamp": "2026-08-13T05:35:24.167120+00:00",
            "source_path": "runs/.calibration/stage0-timing.json"
          },
          "observed_summary_disposition": "failed",
          "observed_guard_disposition": null,
          "artifact_sha256_at_exit": {
            "config.yaml": "8a7e4c8b3904da24224702679bde8cfb98764eba65e1707dc609014de3b258da",
            "summary.json": "91c729155dbd2be68d71c41a212e4882271f3409dbc2ec4e45bc366a80fa8884",
            "summary.md": "876891226a733d3fe9d4722f3466732b05b50d9a3470c016d92ee4350f0e85bb",
            "preflight.json": "808cda002d80de5e8fe7250dfdb60d664a1e0159563a071810e852e7b82cb915",
            "training_metadata.json": "7d23db77ccbb1c381f9601b2ba5bda1a9e8bef88cf20d1cdce628f3718876c11",
            "splits.json": "c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86",
            "status.json": "fe3df4945959d93e302be7308eb42286803601221e19a2fe7d5417b91a566155",
            "logs/train.log.jsonl": "a647736b5bb3d370e1330f7d9da6f06aa0e581c4869d6dddb2a5ae3ba53d87bf",
            "run_start_rng.pt": "7903d77f66db9dd0adb2f9b92d0429b420242ab31343d745492d0fb095d299ee",
            "checkpoints/latest.pt": "06ef5e828b9a33213183c21a45c70d08ebee767dd6a2e68f0d27416a01933d30"
          },
          "invocation_snapshot": null
        }
      ],
      "final_process_disposition": "failed",
      "final_guard_disposition": null,
      "ledger_disposition": "failed",
      "protocol_labels": [],
      "in_final_band": false,
      "archive_move": {
        "from": "runs/stage0-rerun-seed41",
        "to": "runs/stage0-rerun-seed41-attempt-01-failed-20260815T024506Z",
        "verified_utc": "2026-08-15T02:45:06.861246+00:00",
        "hashes_equal": true
      },
      "terminal_artifact_sha256": {
        "config.yaml": "8a7e4c8b3904da24224702679bde8cfb98764eba65e1707dc609014de3b258da",
        "summary.json": "91c729155dbd2be68d71c41a212e4882271f3409dbc2ec4e45bc366a80fa8884",
        "summary.md": "876891226a733d3fe9d4722f3466732b05b50d9a3470c016d92ee4350f0e85bb",
        "preflight.json": "808cda002d80de5e8fe7250dfdb60d664a1e0159563a071810e852e7b82cb915",
        "training_metadata.json": "7d23db77ccbb1c381f9601b2ba5bda1a9e8bef88cf20d1cdce628f3718876c11",
        "splits.json": "c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86",
        "status.json": "fe3df4945959d93e302be7308eb42286803601221e19a2fe7d5417b91a566155",
        "logs/train.log.jsonl": "a647736b5bb3d370e1330f7d9da6f06aa0e581c4869d6dddb2a5ae3ba53d87bf",
        "run_start_rng.pt": "7903d77f66db9dd0adb2f9b92d0429b420242ab31343d745492d0fb095d299ee",
        "checkpoints/latest.pt": "06ef5e828b9a33213183c21a45c70d08ebee767dd6a2e68f0d27416a01933d30"
      },
      "reason": "Seed-41 attempt 1 failed at first validation (step 100): StageZeroUnderpopulated Stage-0 population 227 < required 240 (DATA-06 select_stage_records on the validation split replay pool; replay_count resolved to the DATA-05 default 240 because the graded config omits the field). Preflight passed; 99 finite Adam steps; failure/ empty; not disk/memory/loss-explosion/non-finite/invariant-B. Not a transient; no retry authorized; seeds 42/43 not launched. eval01_precondition_i=True; D-12 splits recorded separately. D-19 forbids lowering replay_count to the observed 227.",
      "retry_authorization": null
    },
    {
      "band_generation": 3,
      "run_name": "stage0-rerun-smoke",
      "attempt_ordinal": 4,
      "artifact_dir": "runs/stage0-rerun-smoke",
      "config": "configs/stage0-rerun-smoke.yaml",
      "source_config_sha256": "a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a",
      "frozen_config_sha256": "3db88b697aac2f3c61075e402602fb7a447aaf9113109669dc5925934e2dd46d",
      "config_identity_digest": "3db88b697aac2f3c",
      "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd",
      "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34",
      "git_head": "c4a1550b7bd889121128e31d7078a478b0a6ca8a",
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": "fresh",
          "status": "closed",
          "intended_artifact_dir": "runs/stage0-rerun-smoke",
          "launch_command": "nohup <home>/miniforge3/bin/conda run --no-capture-output -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-rerun-smoke.yaml --stage-0-only",
          "launch_transcript": ".planning/phases/50-valid-stage-0-re-run/evidence/launch-transcripts/stage0-rerun-smoke-attempt-04-invocation-01-train.txt",
          "transcript_sha256": "4c05d5e4c956efb047c1d2cbad453f0695b3e157f50c2cf9ea9af4fbabec7440",
          "external_start_utc": "2026-08-15T02:47:06.238431+00:00",
          "external_end_utc": "2026-08-15T02:51:27Z",
          "exit_code": 0,
          "recovered_after_executor_loss": false,
          "git_head": "c4a1550b7bd889121128e31d7078a478b0a6ca8a",
          "source_config_sha256": "a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a",
          "frozen_config_sha256": "3db88b697aac2f3c61075e402602fb7a447aaf9113109669dc5925934e2dd46d",
          "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd",
          "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34",
          "timing_fingerprint": {
            "device": "mps",
            "dtype": "torch.float32",
            "torch_version": "2.12.1",
            "python_version": "3.11.15",
            "git_head": "c4a1550b7bd889121128e31d7078a478b0a6ca8a",
            "git_head_available": true
          },
          "summary_env_fingerprint": {
            "sw_vers": "ProductName:\t\tmacOS\nProductVersion:\t\t26.5.1\nBuildVersion:\t\t25F80",
            "python_version": "3.11.15",
            "torch_version": "2.12.1",
            "torch_build": "7269437d655783a26cba32aa88195b741ff496aa"
          },
          "resume_checkpoint": null,
          "calibration_before": {
            "path": ".planning/phases/50-valid-stage-0-re-run/evidence/calibration/pre-smoke-20260815T024631Z-e111f020bcdf.json",
            "sha256": "e111f020bcdfc7ccfb60352b0f4615aeaa1a4e15d46b98a2e75e7571dc215b43",
            "timestamp": "2026-08-13T05:35:24.167120+00:00",
            "source_path": "runs/.calibration/archive/pre-smoke-20260815T024631Z-e111f020bcdf.json"
          },
          "calibration_after": {
            "path": ".planning/phases/50-valid-stage-0-re-run/evidence/calibration/generation-3-smoke-attempt-04-invocation-01.json",
            "sha256": "ed30b06ae2f8303506d654d66f17bd89034b403e6671fc24cc2ce9e1454ed2a4",
            "timestamp": "2026-08-15T02:51:01.296265+00:00",
            "source_path": "runs/.calibration/stage0-timing.json"
          },
          "observed_summary_disposition": "finished",
          "observed_guard_disposition": null,
          "artifact_sha256_at_exit": {
            "config.yaml": "3db88b697aac2f3c61075e402602fb7a447aaf9113109669dc5925934e2dd46d",
            "summary.json": "46995777a52efe3be81984f51f6ad96749594dee019d011859ea4166a7665ac7",
            "summary.md": "55a80fb945f5fb9315bc47fcd5d9b1f49f28fe9f6fc84cf7b8d0cb44ff8be811",
            "preflight.json": "8c1e8e36703b1d78cb6ae948cf1bb4d4c19ed506a98293f5d4186942c70fd572",
            "training_metadata.json": "a7011e77a5f7c91720f924117de06b8892e316e35c19531ba8617c4c1236a095",
            "splits.json": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
            "curriculum.jsonl": "7439572cb2940ce8a440b22796315c552c8dea725c70297c169ef9f065c4b68b",
            "validation.jsonl": "cca8f0e0389a52df62229e3c3356ffc797dfe5f38abb33b90cd75fb74e31d4b0",
            "status.json": "951e4a396770ce4dd146fb4c17a1b9bd5c9e0c461e75009c9c583d9eace569a3",
            "logs/train.log.jsonl": "fe3b748517583feadebc37074f9f316abdb1dbbe347ba390df395d068c69613d",
            "run_start_rng.pt": "b61b74a1b77cb985bdf3d61a0170d2b5e4f7fb7d17c38cdcaeb85ccad4c8d3d2",
            "checkpoints/best.pt": "e14a9e3187a3218dbcda9e7c60010ba1b860e2415875e0988ab7a53c1ef3436e",
            "checkpoints/latest.pt": "69ddae7d1a29e7e53bff8d40d7390992a26591bf6bd69dc4edbd4eeee28bad5a",
            "checkpoints/step-000300.pt": "c25254ff12700e2339ef9fe7ed2a6a2b41a128984ff0be39b92abd0fc5bbf68c"
          },
          "invocation_snapshot": null
        }
      ],
      "final_process_disposition": "finished",
      "final_guard_disposition": null,
      "ledger_disposition": "finished",
      "protocol_labels": [],
      "in_final_band": false,
      "archive_move": null,
      "terminal_artifact_sha256": {
        "config.yaml": "3db88b697aac2f3c61075e402602fb7a447aaf9113109669dc5925934e2dd46d",
        "summary.json": "46995777a52efe3be81984f51f6ad96749594dee019d011859ea4166a7665ac7",
        "summary.md": "55a80fb945f5fb9315bc47fcd5d9b1f49f28fe9f6fc84cf7b8d0cb44ff8be811",
        "preflight.json": "8c1e8e36703b1d78cb6ae948cf1bb4d4c19ed506a98293f5d4186942c70fd572",
        "training_metadata.json": "a7011e77a5f7c91720f924117de06b8892e316e35c19531ba8617c4c1236a095",
        "splits.json": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
        "curriculum.jsonl": "7439572cb2940ce8a440b22796315c552c8dea725c70297c169ef9f065c4b68b",
        "validation.jsonl": "cca8f0e0389a52df62229e3c3356ffc797dfe5f38abb33b90cd75fb74e31d4b0",
        "status.json": "951e4a396770ce4dd146fb4c17a1b9bd5c9e0c461e75009c9c583d9eace569a3",
        "logs/train.log.jsonl": "fe3b748517583feadebc37074f9f316abdb1dbbe347ba390df395d068c69613d",
        "run_start_rng.pt": "b61b74a1b77cb985bdf3d61a0170d2b5e4f7fb7d17c38cdcaeb85ccad4c8d3d2",
        "checkpoints/best.pt": "e14a9e3187a3218dbcda9e7c60010ba1b860e2415875e0988ab7a53c1ef3436e",
        "checkpoints/latest.pt": "69ddae7d1a29e7e53bff8d40d7390992a26591bf6bd69dc4edbd4eeee28bad5a",
        "checkpoints/step-000300.pt": "c25254ff12700e2339ef9fe7ed2a6a2b41a128984ff0be39b92abd0fc5bbf68c"
      },
      "reason": "Calibration + first-real-corpus-contact smoke for generation 3 (in_final_band false; D-01/D-13/D-14). Observed training_metadata s_h=22.321729071058996 eps_h=0.0022321729071058997 n_train=1812. preflight_status=passed. Calibration valid=true fingerprint.git_head=c4a1550b7bd889121128e31d7078a478b0a6ca8a s_per_step=0.18288215688329543 gate_input_1000=182.9s (shipped D-18 gate input, not ETA). validation.jsonl events=3; every validation event completed without StageZeroUnderpopulated. Curriculum journal disposition HALT at step 300 is stage-exit after Adam budget exhaustion under --stage-0-only, not a guard or invariant-B HALT. Validation-gate TypeError warnings at steps 100/200/300 recorded, not used to change any rule (D-19). Launch used nohup without setsid.",
      "retry_authorization": null
    },
    {
      "band_generation": 3,
      "run_name": "stage0-rerun-seed41",
      "attempt_ordinal": 2,
      "artifact_dir": "runs/stage0-rerun-seed41",
      "config": "configs/stage0-rerun-seed41.yaml",
      "source_config_sha256": "90ccd7418211ca42ebe14e06ea0bf1f62249d87e19b71c9f670c9a9b8374f073",
      "frozen_config_sha256": "8a7e4c8b3904da24224702679bde8cfb98764eba65e1707dc609014de3b258da",
      "config_identity_digest": "8a7e4c8b3904da24",
      "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd",
      "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34",
      "git_head": "c4a1550b7bd889121128e31d7078a478b0a6ca8a",
      "invocations": [
        {
          "invocation_ordinal": 1,
          "launch_kind": "fresh",
          "status": "closed",
          "intended_artifact_dir": "runs/stage0-rerun-seed41",
          "launch_command": "nohup <home>/miniforge3/bin/conda run --no-capture-output -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-rerun-seed41.yaml --stage-0-only",
          "launch_transcript": ".planning/phases/50-valid-stage-0-re-run/evidence/launch-transcripts/stage0-rerun-seed41-attempt-02-invocation-01-train.txt",
          "transcript_sha256": "2902b39acbba270f875373623663f7528c15318e809348c54280d7d8fec67cb1",
          "external_start_utc": "2026-08-15T03:05:00.025989+00:00",
          "external_end_utc": "2026-08-15T03:09:51.167390+00:00",
          "exit_code": 1,
          "recovered_after_executor_loss": false,
          "git_head": "c4a1550b7bd889121128e31d7078a478b0a6ca8a",
          "source_config_sha256": "90ccd7418211ca42ebe14e06ea0bf1f62249d87e19b71c9f670c9a9b8374f073",
          "frozen_config_sha256": "8a7e4c8b3904da24224702679bde8cfb98764eba65e1707dc609014de3b258da",
          "corpus_snapshot_sha256": "9fdc39c478f5033a49e706a156b3fdcd517eb0dc66eab0613eded0e900dc9fdd",
          "environment_snapshot_sha256": "5df135235418f7d09ecf5c874530a489186695b66cf5cc3ec189c69ad95c2a34",
          "timing_fingerprint": {
            "device": "mps",
            "dtype": "torch.float32",
            "torch_version": "2.12.1",
            "python_version": "3.11.15",
            "git_head": "c4a1550b7bd889121128e31d7078a478b0a6ca8a",
            "git_head_available": true
          },
          "summary_env_fingerprint": {
            "sw_vers": "ProductName:\t\tmacOS\nProductVersion:\t\t26.5.1\nBuildVersion:\t\t25F80",
            "python_version": "3.11.15",
            "torch_version": "2.12.1",
            "torch_build": "7269437d655783a26cba32aa88195b741ff496aa"
          },
          "resume_checkpoint": null,
          "calibration_before": {
            "path": ".planning/phases/50-valid-stage-0-re-run/evidence/calibration/generation-3-smoke-attempt-04-invocation-01.json",
            "sha256": "ed30b06ae2f8303506d654d66f17bd89034b403e6671fc24cc2ce9e1454ed2a4",
            "timestamp": "2026-08-15T02:51:01.296265+00:00",
            "source_path": "runs/.calibration/stage0-timing.json"
          },
          "calibration_after": null,
          "observed_summary_disposition": "failed",
          "observed_guard_disposition": "HALT",
          "artifact_sha256_at_exit": {
            "config.yaml": "8a7e4c8b3904da24224702679bde8cfb98764eba65e1707dc609014de3b258da",
            "summary.json": "32dd49122ea500023b9f0fec962fd4cbd691905f5cc3ace0416fdb764e2810fb",
            "summary.md": "6b0e8d0ce762a6ab3f3e2d8b3ecc7ea2406b36a4d726898ce3d2e11b4873314f",
            "preflight.json": "f7729f2f160835746a644f9c5dddd29a50a93f1b11a46269132f46aca63442c1",
            "training_metadata.json": "7d23db77ccbb1c381f9601b2ba5bda1a9e8bef88cf20d1cdce628f3718876c11",
            "splits.json": "c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86",
            "curriculum.jsonl": "369793d9362e4ffdce19e7d780bfde0b81f8e90989ddfff12fd1d8eb627008b8",
            "validation.jsonl": "3c8d7158be141a443aa2cf8ecd1017ebe9ea5e4d0bcdbbc4969c2cafbb5f1835",
            "status.json": "3a297d0f423949e49196bb3711e29387580473d799f34fb9c6dd85595f24180d",
            "logs/train.log.jsonl": "25d54fb0cd9d73d5d91f0fd9621668b11231ea2b4b83f201a746073734ba22fd",
            "run_start_rng.pt": "0d468fa2e243fee724c64b18c592e50d4007846d9ece48af2aabcd15a95a07eb",
            "failure/README.txt": "daccc8ab99caa1e39612f4ae32fd1ba4e132493013c14b127f2420169cc85f68",
            "failure/trip.json": "0acc1a4f2040ab0804d009e944c61b92d4fb9bbaa4ea759830a571a209b48ade",
            "checkpoints/best.pt": "86d9f7b4dcbc6e6aef7a35844a3f32b09aa64b8ac033aaa5ebc4f4bf35024bb5",
            "checkpoints/latest.pt": "a9afa7805272723a6e682e9b26bad29c67a3e1238b772ffd1b353ee88ccef026",
            "checkpoints/step-000500.pt": "3a7324dc9df74d6d20d9c240b0a1d2c605627528a313d310d1c1f54c88b66d59",
            "checkpoints/failure-stage-0-step-501.pt": "edf7d165cabcc25cfff822e4c8ed0e4bc0a02a70928aecaf00da3f8c1c58509b"
          },
          "invocation_snapshot": null
        }
      ],
      "final_process_disposition": "failed",
      "final_guard_disposition": "HALT",
      "ledger_disposition": "halted",
      "protocol_labels": [],
      "in_final_band": false,
      "archive_move": null,
      "terminal_artifact_sha256": {
        "config.yaml": "8a7e4c8b3904da24224702679bde8cfb98764eba65e1707dc609014de3b258da",
        "summary.json": "32dd49122ea500023b9f0fec962fd4cbd691905f5cc3ace0416fdb764e2810fb",
        "summary.md": "6b0e8d0ce762a6ab3f3e2d8b3ecc7ea2406b36a4d726898ce3d2e11b4873314f",
        "preflight.json": "f7729f2f160835746a644f9c5dddd29a50a93f1b11a46269132f46aca63442c1",
        "training_metadata.json": "7d23db77ccbb1c381f9601b2ba5bda1a9e8bef88cf20d1cdce628f3718876c11",
        "splits.json": "c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86",
        "curriculum.jsonl": "369793d9362e4ffdce19e7d780bfde0b81f8e90989ddfff12fd1d8eb627008b8",
        "validation.jsonl": "3c8d7158be141a443aa2cf8ecd1017ebe9ea5e4d0bcdbbc4969c2cafbb5f1835",
        "status.json": "3a297d0f423949e49196bb3711e29387580473d799f34fb9c6dd85595f24180d",
        "logs/train.log.jsonl": "25d54fb0cd9d73d5d91f0fd9621668b11231ea2b4b83f201a746073734ba22fd",
        "run_start_rng.pt": "0d468fa2e243fee724c64b18c592e50d4007846d9ece48af2aabcd15a95a07eb",
        "failure/README.txt": "daccc8ab99caa1e39612f4ae32fd1ba4e132493013c14b127f2420169cc85f68",
        "failure/trip.json": "0acc1a4f2040ab0804d009e944c61b92d4fb9bbaa4ea759830a571a209b48ade",
        "checkpoints/best.pt": "86d9f7b4dcbc6e6aef7a35844a3f32b09aa64b8ac033aaa5ebc4f4bf35024bb5",
        "checkpoints/latest.pt": "a9afa7805272723a6e682e9b26bad29c67a3e1238b772ffd1b353ee88ccef026",
        "checkpoints/step-000500.pt": "3a7324dc9df74d6d20d9c240b0a1d2c605627528a313d310d1c1f54c88b66d59",
        "checkpoints/failure-stage-0-step-501.pt": "edf7d165cabcc25cfff822e4c8ed0e4bc0a02a70928aecaf00da3f8c1c58509b"
      },
      "reason": "Seed-41 attempt 2 HALTed at step 501 by invariant_B (D-20): causal front high-water mark did not advance within N=500 steps; front_idx=0 on all 502 logged steps; trip.json guard=invariant_b disposition=HALT threshold_provisional=false. First validation event at step 100 completed without StageZeroUnderpopulated (C-09 repair held; DATA-06 did not recur). validation_events=5 (steps 100/200/300/400/500). preflight_status=passed; eval01_precondition_i=True. D-12 splits MATCH sha256=c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86. s_h=21.978293176386664 n_train=1812 (seed-41 statistic; D-16 is seed-42 only and is undischarged). Not disk/memory/loss-explosion/non-finite/DATA-06. Not a transient; no retry authorized; seeds 42/43 not launched. N is not raised, softened, re-marked provisional, or bypassed. Launch used nohup without setsid. --stage-0-only; no --resume.",
      "retry_authorization": null,
      "first_validation_proof": {
        "seed": "41",
        "recorded_utc": "2026-08-15T03:08:31.104084+00:00",
        "stage_zero_underpopulated_absent": true,
        "validation_events_observed": 1,
        "first_event_step": 100,
        "status_step": 145,
        "status_state": "running"
      }
    }
  ],
  "integrity_notes": {
    "closeout_mode": "terminal",
    "terminal_reason": "stage0-validation-underpopulated-replay-count-240",
    "d23_evaluation_directory_absent": true,
    "d23_forbidden_artifacts": [],
    "d23_no_pinn_evaluate_in_ledger_commands": true,
    "d28_GSD_DATA_ROOT_unset": true,
    "d28_GSD_ALLOW_PARTIAL_DATA_ROOT_unset": true,
    "d22_attempt_count": 4,
    "d22_invocation_count": 4,
    "canonical_run_dirs_enumerated": [
      "runs/stage0-rerun-smoke",
      "runs/stage0-rerun-seed41",
      "runs/stage0-rerun-seed42",
      "runs/stage0-rerun-seed43"
    ],
    "live_process_at_closeout": false,
    "seed41_d12": "MATCH",
    "seed41_splits_sha256": "c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86",
    "leftover_canonical_archives": [
      {
        "run_name": "stage0-rerun-smoke",
        "attempt_ordinal": 1,
        "from": "runs/stage0-rerun-smoke",
        "to": "runs/stage0-rerun-smoke-attempt-01-interrupted-20260813T052918Z",
        "verified_utc": "2026-08-13T05:29:18.692506+00:00",
        "hashes_equal": true,
        "reason": "dead leftover occupying canonical path; moved so a later generation can reuse it"
      },
      {
        "run_name": "stage0-rerun-smoke",
        "attempt_ordinal": 3,
        "from": "runs/stage0-rerun-smoke",
        "to": "runs/stage0-rerun-smoke-attempt-03-finished-20260815T024505Z",
        "verified_utc": "2026-08-15T02:45:06.004650+00:00",
        "hashes_equal": true,
        "reason": "dead leftover occupying canonical path; moved so a later generation can reuse it"
      },
      {
        "run_name": "stage0-rerun-seed41",
        "attempt_ordinal": 1,
        "from": "runs/stage0-rerun-seed41",
        "to": "runs/stage0-rerun-seed41-attempt-01-failed-20260815T024506Z",
        "verified_utc": "2026-08-15T02:45:06.861246+00:00",
        "hashes_equal": true,
        "reason": "dead leftover occupying canonical path; moved so a later generation can reuse it"
      }
    ],
    "generation_3": {
      "closeout_mode": "terminal",
      "terminal_reason": "invariant-b-halt-front-idx-stalled-n-500",
      "d23_evaluation_directory_absent": true,
      "d23_forbidden_artifacts": [],
      "d23_no_pinn_evaluate_in_ledger_commands": true,
      "d28_GSD_DATA_ROOT_unset": true,
      "d28_GSD_ALLOW_PARTIAL_DATA_ROOT_unset": true,
      "d22_generation_3_attempt_count": 2,
      "d22_generation_3_invocation_count": 2,
      "canonical_run_dirs_enumerated": [
        "runs/stage0-rerun-smoke",
        "runs/stage0-rerun-seed41",
        "runs/stage0-rerun-seed42",
        "runs/stage0-rerun-seed43"
      ],
      "live_process_at_closeout": false,
      "seed41_d12": "MATCH",
      "seed41_splits_sha256": "c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86",
      "seed41_first_validation_stage_zero_underpopulated_absent": true,
      "seed41_validation_events": 5,
      "seeds_42_43_launched": false
    }
  }
}
```

## Field contract: `band_generations[]`

Each `band_generations[]` entry describes one Phase-50 band-generation window
(a smoke + three graded seeds executed at one fixed `git_head` / config-set /
corpus / environment identity) and requires:

- `band_generation` — a monotone integer identifying the generation (1 for
  the first attempt at the band; a repair per D-17/D-19 opens a new,
  incremented generation).
- `git_head` — `git rev-parse HEAD` at generation-open (D-17's pin).
- `corpus_snapshot` — `{"path": ..., "file_sha256": ..., "corpus_snapshot_sha256": ...}`,
  the immutable evidence copy of the admitted-corpus identity fact the
  generation opened against.
- `committed_config_sha256_by_path` — the sorted `{repo-relative config path:
  sha256}` map for all four Phase-50 configs, reproduced from `git show
  <this-record's pre-registration commit>:<path>` and required to
  byte-match the pre-registration record's own `generation_binding` map
  before this generation may open.
- `committed_config_set_sha256` — the sha256 of that map's own compact sorted
  JSON (the single aggregate identity plan 50-02 checks against the
  pre-registration record before proceeding).
- `environment_snapshot` — `{"path": ..., "file_sha256": ..., "environment_snapshot_sha256": ...}`,
  the immutable evidence copy of the environment fingerprint fact.
- `timing_fingerprint` — the exact production six-field object:
  `device`, `dtype`, `torch_version`, `python_version`, `git_head`,
  `git_head_available=true` (the calibration fingerprint `pinn.verify`
  produces; D-13's duration-gate refusal is keyed to exact equality on this
  object).
- `summary_env_fingerprint` — the `header.env_fingerprint` object every run's
  `summary.json` carries (python/torch/sw_vers triple), captured once at
  generation level as the expected value every attempt's own
  `summary_env_fingerprint` must match.
- `pre_registration_commit` — the commit hash of `50-PRE-REGISTRATION.md`
  this generation is bound to.
- `opened_utc` / `closed_utc` — external wall-clock timestamps; `closed_utc`
  is null while the generation is open.
- `cleanliness_receipts` — the array documented below.
- `verify_invocations` — the array documented below.
- `status` — one of `active | superseded | terminal | complete`.

### `cleanliness_receipts[]`

Each generation structurally enumerates its runtime/corpus/environment
boundary receipts so plan 50-03 can prove exhaustive evidence coverage
without inferring files from directory contents. Each entry requires:
`boundary` (which cleanliness check this receipt proves — runtime, corpus, or
environment), `command` (the exact invocation), `external_start_utc` /
`external_end_utc`, `exit_code`, `path` (the immutable evidence copy holding
the receipt's exact stdout/stderr), and `sha256` (over that copy's bytes).

### `verify_invocations[]`

Every `pinn.verify` process this generation runs is enumerated, including a
**provisional** entry appended before spawn and **closed** after the process
exits, under the same nullable-loss rule invocations use (below). Each entry
requires: `invocation_ordinal`, `status` (`running | closed`), the exact
`command`, external timestamps, `exit_code`, `recovered_after_executor_loss`,
`transcript`, `transcript_sha256`, `result` (the verify ladder's own
pass/fail outcome), the runtime fingerprint the invocation ran under, and
`marker` — `{"path": ..., "sha256": ..., "timestamp": ...}` or `null` when no
fresh marker was produced.

## Field contract: `records[]` (one per attempted run)

Each `records[]` entry is one **attempt** at one canonical Phase-50 run name
(`stage0-rerun-smoke`, `stage0-rerun-seed41`, `stage0-rerun-seed42`,
`stage0-rerun-seed43`) — a refused launch, a HALTed/failed/interrupted run,
an archived attempt superseded by a retry, or an accepted finished run. The
`attempt_ordinal` + `artifact_dir` pair is what prevents an archived failed
run and its successful canonical retry from collapsing into one ambiguous
record; `terminal_artifact_sha256` (below) closes the run-completion ->
plan-50-03-extraction window. Required fields:

- `band_generation` — which generation this attempt belongs to.
- `run_name` — the canonical run name (never the archived directory name).
- `attempt_ordinal` — a positive integer, monotone per canonical `run_name`
  across generations (a second generation's first attempt does not restart
  the counter at 1 if an earlier generation already used higher ordinals for
  the same `run_name`).
- `artifact_dir` — the repo-relative canonical `runs/<run_name>/` directory,
  or the archived `runs/<run_name>-attempt-<NN>-<disposition>-<UTC>/`
  directory once an archive move has happened.
- `config` — the repo path of the committed config this attempt launched
  with.
- `source_config_sha256` — the full sha256 of that committed input YAML.
- `frozen_config_sha256` — the full sha256 of the resolved
  `runs/<artifact_dir>/config.yaml`; `null` when no run directory (and
  therefore no frozen config) was ever created — e.g. a pre-construction
  refusal.
- `config_identity_digest` — read from `summary.json`'s header once the run
  exists; `null` for a refusal that never built a run directory.
- `corpus_snapshot_sha256` / `environment_snapshot_sha256` — the generation's
  identity facts, repeated here so a single record is self-describing without
  a join back to `band_generations[]`.
- `git_head` — `git rev-parse HEAD` at this attempt's launch (D-17's pin,
  repeated at record level).
- `invocations` — a non-empty array; see below.
- `final_process_disposition` / `final_guard_disposition` / `ledger_disposition` /
  `protocol_labels` / `in_final_band` / `archive_move` /
  `terminal_artifact_sha256` / `reason` / `retry_authorization` — see the
  attempt-level disposition contract below.

### `invocations[]` (per-record)

Every process launch tied to an attempt — including a refused pre-directory
launch and, if it ever occurred, a resume — is its own invocation. Required
fields:

- `invocation_ordinal` — position of this invocation within the attempt.
- `launch_kind` — `fresh`. `resume` is schema-reserved (the field accepts the
  literal for forward compatibility) but is a **prohibited** value for every
  actual Phase-50 launch: `resume_allowed: false` in
  `50-PRE-REGISTRATION.md`'s `selection_policy`, and every Phase-50 launch
  passes `--stage-0-only` and never `--resume`.
- `status` — `running | closed`. A provisional entry is appended with
  `status: "running"` before the process spawns; it is closed to
  `status: "closed"` after the process exits.
- `intended_artifact_dir` — the `runs/<run_name>/` directory this invocation
  intended to create or use, recorded before launch so a pre-directory
  refusal is still traceable to an intended path.
- `launch_command` — the exact command line, including `--stage-0-only` (and
  never `--resume`, per the forbidden-flag rule).
- `launch_transcript` — the path to the immutable evidence copy of this
  invocation's combined stdout/stderr.
- `transcript_sha256` — sha256 of that transcript copy.
- `external_start_utc` / `external_end_utc` — wall-clock timestamps observed
  by the invoking process, not by anything inside the training run.
- `exit_code` — the process exit code.
- `recovered_after_executor_loss` — `true` only when the executor lost
  contact with a running process and had to recover the outcome after the
  fact; in that case `external_end_utc` and `exit_code` MAY be `null` (see
  below). Normally `false`.
- `git_head`, `source_config_sha256`, `frozen_config_sha256`,
  `corpus_snapshot_sha256`, `environment_snapshot_sha256`,
  `timing_fingerprint`, `summary_env_fingerprint` — this invocation's own
  observed identity facts, so a within-attempt identity drift (which must
  never happen inside one attempt) is independently checkable rather than
  assumed from the record level.
- `resume_checkpoint` — `{"path": ..., "sha256": ..., "global_step": ...}` or
  `null`. Recorded only as immutable identity metadata; Phase 50 never copies
  model-checkpoint bytes into committed evidence, and the original checkpoint
  is preserved under `runs/` through Phase 52.
- `calibration_before` / `calibration_after` — `{"path": ..., "sha256": ...,
  "timestamp": ..., "source_path": ...}` or `null`. `timestamp` is the timing
  JSON's own field; `path` is the immutable evidence copy, never the mutable
  canonical `runs/.calibration/stage0-timing.json` alias.
- `observed_summary_disposition` / `observed_guard_disposition` — the exact
  values this invocation actually observed (may differ transiently from the
  attempt-level final values if closure races the process; the attempt-level
  fields below are the ones Phase 51 reads).
- `artifact_sha256_at_exit` — a mapping, keyed **relative to `artifact_dir`**,
  of every artifact present at this invocation's exit to its sha256.
- `invocation_snapshot` — `null` until needed; see the recovery/adoption
  contract below.

For a normally closed invocation, `external_end_utc` and `exit_code` are
**required** (non-null). They may be `null` **only** when
`recovered_after_executor_loss` is `true` — i.e. only when the executor
genuinely could not observe the process's own exit and had to reconstruct the
outcome from other evidence.

### `invocation_snapshot` — recovery/adoption of unexpected prior resume history

This structure is reserved for recovering or adopting any **unexpected**
pre-existing resume history — it exists so an anomaly is preserved as
evidence, not so a resume becomes eligible for the final band. Its presence
on a record can never make that record's history eligible for
`in_final_band: true`. Before any resume could overwrite or append to the
same canonical directory (which Phase 50's own policy prohibits, but which
this schema must still be able to represent if it is ever discovered),
**every** present mutable-journal artifact (summary/status/failure/preflight/
training-metadata metadata, `curriculum.jsonl`, `validation.jsonl`,
`logs/train.log.jsonl`, and every referenced `validation_gate` sidecar) is
copied under `evidence/attempts/<attempt>/invocation-<II>/`, and that
directory is recorded as the **prior** invocation's `invocation_snapshot`:
`{"root": ..., "created_utc": ..., "files": {...}, "snapshot_sha256": ...}`,
where `files` is a mapping keyed **relative to `root`**. Every
journal/sidecar artifact present at the interruption must appear in
`artifact_sha256_at_exit` with the identical copied hash; a field the
interrupted state never produced stays explicitly absent/inapplicable — it is
never fabricated. `snapshot_sha256` is the sha256 of the compact sorted JSON
of the relative-path -> hash map.

## Attempt-level disposition fields and their deterministic mapping

At the attempt (`records[]`) level, beyond the per-invocation fields above,
every attempt also carries:

- `final_process_disposition` — the exact final `summary.json` value
  (`finished | failed | interrupted`), or `null` when no `summary.json` was
  ever produced.
- `final_guard_disposition` — `HALT | RECOVER | null`.
- `ledger_disposition` — the DERIVED outcome this ledger assigns:
  `finished | refused | halted | failed | interrupted`. A provisional
  pre-spawn invocation leaves the owning attempt's `ledger_disposition`
  `null` until the invocation closes.
- `protocol_labels` — an array; contains the literal `"superseded"` once a
  later band-generation policy retires this attempt. `protocol_labels` is
  the ONLY place supersession is recorded — it never rewrites
  `final_process_disposition`, `final_guard_disposition`, or
  `ledger_disposition` after they are first observed.
- `in_final_band` — boolean; may be `true` only for a record whose
  `band_generation` equals the ledger's own `final_band_generation`.
- `archive_move` — `null`, or `{"from": ..., "to": ..., "verified_utc": ...,
  "hashes_equal": ...}` once this attempt's directory has been archived
  ahead of a retry.
- `terminal_artifact_sha256` — a mapping from paths **relative to
  `artifact_dir`** (never a canonical repo path, which goes stale after an
  archive move) to their terminal 64-hex sha256 digests.
- `reason` — free-text pointer to the specific evidence (a preflight event, a
  guard-trip record, an exception message) backing the disposition above.
- `retry_authorization` — see below.

**The deterministic disposition mapping** (fixed once observed; never
rewritten by later supersession):

| Cause | `final_process_disposition` | `final_guard_disposition` | `ledger_disposition` |
|---|---|---|---|
| Duration-gate or run-folder-collision refusal, **before** any run directory is created | `null` | `null` | `refused` |
| Preflight/conformance refusal, **after** run construction | `failed` | `null` | `refused` |
| Normal `summary.json` disposition `interrupted` | `interrupted` | `null` (unless a guard also fired) | `interrupted` |
| A Tier-1/2 guard HALT (loss-explosion / disk / memory / invariant-B) | `failed` | `HALT` | `halted` |
| Calibration/protocol failure (e.g. a stale calibration refused before launch) | `finished` | `null` | `failed` |
| Setup/unknown exception before or during construction | `failed` | `null` | `failed` |
| An accepted, gate-clean, `finished` run | `finished` | `null` | `finished` |

Note the guard-HALT row: even though the guard disposition is `HALT`, the
observed `summary.json` process disposition for that same run is `failed` —
the two fields are independently observed facts, not derived from each
other, which is exactly why both are recorded rather than only the derived
`ledger_disposition`. A provisional (`status: "running"`) invocation's owning
attempt carries `ledger_disposition: null` until the invocation closes and
one of the rows above applies. Once a `ledger_disposition` is first observed
it is **preserved permanently**; later generation retirement appends
`"superseded"` to `protocol_labels` and touches nothing else on the record.

### `retry_authorization`

`null` unless a fresh transient retry was actually authorized for this
attempt's *parent* attempt, in which case:

```text
{
  "parent_attempt": <attempt_ordinal of the archived attempt this retry follows>,
  "cause": "disk_pressure" | "external_memory_pressure",
  "evidence_paths_sha256": {...},
  "before_resource_facts": {...},
  "after_resource_facts": {...},
  "unchanged_identity": {
    "git_head": ..., "source_config_sha256": ..., "frozen_config_sha256": ...,
    "corpus_snapshot_sha256": ..., "environment_snapshot_sha256": ...,
    "timing_fingerprint": {...}, "summary_env_fingerprint": {...}
  },
  "authorized_utc": ...
}
```

`before_resource_facts` / `after_resource_facts` must show, independently of
a bare memory-watermark reading, that external (non-Phase-50) resource
pressure was present and has since been removed — a watermark reading alone
is insufficient positive identification (`50-PRE-REGISTRATION.md` section
(7)). `unchanged_identity` proves the retry changed no code, config, corpus,
threshold, or seed relative to the parent attempt it follows.

## Why this couples every launch to observable evidence

This structure — attempt ordinal + invocation array + artifact-dir-relative
terminal hashes + the nullable-loss carve-out — couples every process launch,
including a refusal, an interrupted run, an archived attempt, and (if it were
ever to occur) a resume, to independently checkable process and calibration
evidence, without collapsing several distinct launches into one ambiguous
attempt.
