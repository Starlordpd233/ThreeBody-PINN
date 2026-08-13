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
  "band_generations": [],
  "records": []
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
