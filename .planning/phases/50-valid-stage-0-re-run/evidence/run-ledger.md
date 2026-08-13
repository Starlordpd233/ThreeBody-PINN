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
    }
  ],
  "records": [
    {
      "band_generation": 1,
      "run_name": "stage0-rerun-smoke",
      "attempt_ordinal": 1,
      "artifact_dir": "runs/stage0-rerun-smoke",
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
      "archive_move": null,
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
    }
  ],
  "integrity_notes": {
    "closeout_mode": "terminal",
    "terminal_reason": "interrupted-executor-wrapper-timeout",
    "d23_evaluation_directory_absent": true,
    "d23_forbidden_artifacts": [],
    "d23_no_pinn_evaluate_in_ledger_commands": true,
    "d28_GSD_DATA_ROOT_unset": true,
    "d28_GSD_ALLOW_PARTIAL_DATA_ROOT_unset": true,
    "d22_attempt_count": 1,
    "d22_invocation_count": 1,
    "canonical_run_dirs_enumerated": [
      "runs/stage0-rerun-smoke",
      "runs/stage0-rerun-seed41",
      "runs/stage0-rerun-seed42",
      "runs/stage0-rerun-seed43"
    ],
    "live_process_at_closeout": false
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
