# Phase 59 evidence

## In plain language

This folder is the record of the read-only baseline. Each number is saved as a
file with a SHA-256 fingerprint. A separate checker,
`verify_phase59_evidence.py`, confirms that the scorecard was locked before any
result existed, that saved results have not changed, that no held-out file was
opened, and that nothing under `runs/` was rewritten. It does not train and it
does not re-run the checkpoint experiments.

Run every command from the repository root with the pinn-train interpreter.
The commands below use `python` for that interpreter. Do not paste a host path
into a committed evidence file.

## Areas

| Area | Producing plans | Files |
| --- | --- | --- |
| audit | 59-05 | `reader_acceptance.json`, `files_opened.json`, `provenance.json`, `MANIFEST.json` |
| census | 59-05 | `census.json`, `panels.json`, `census.csv`, `files_opened.json`, `provenance.json`, `MANIFEST.json` |
| survey | 59-06 | `survey.json`, `picks.json`, `{step}.done.json`, `files_opened.json`, `provenance.json`, `MANIFEST.json` |
| baselines | 59-08 | `two_kepler.json`, `nn_copy.json`, `baselines.json`, `files_opened.json`, `provenance.json`, `MANIFEST.json` |
| diag07 | 59-07 and 59-09 | `jx01.json` through `jx05.json`, `jx10.json`, `g1.json`, `{step}.done.json`, `files_opened.json`, `provenance.json`, `MANIFEST.json` |

## Frozen files

Four files are frozen together. The freeze commit is the commit that added
`evidence/scorecard-freeze.json`.

- `pinn/verification/artifacts/feasibility_scorecard_v1.json`
- `pinn/verification/feasibility_scorecard.py`
- `59-SCORECARD.md`
- `evidence/scorecard-freeze.json`

`decision_sources` pins `59-CONTEXT.md`, `59-GAPS.md`, `59-RESEARCH.md`, and
`59-VALIDATION.md`. Each pin stores `git_blob`, `sha256`, `last_commit`, and
`verify`. `verify` is `unchanged` for CONTEXT and RESEARCH (the current bytes
must still match). It is `ancestor_state` for GAPS and VALIDATION (checked
only as they stood at the freeze commit, because GAPS gains STOP entries and
plan 59-10 signs VALIDATION).

## Result files

A result is any `*.json` in an area except `MANIFEST.json`, `provenance*.json`,
`files_opened*.json`, and `*.done.json`. Every result carries:

- `schema` starting with `phase59-`
- non-empty `plain_language`
- `scorecard_sha256` equal to the frozen scorecard digest
- `producer_sha256`: repo-relative path to SHA-256 for every module or driver
  script that produced the file (`evidence_io.module_hashes`)

`census.csv` has an `id` column, one training system per row. `panels.json`
`rule` is the scorecard `panel_rule`. `singles`, `family`, and `validation`
are the three panels. `two_kepler.json` has an `ids` list covering every panel
id. `nn_copy.json` has 227 `rows`, each with `neighbour_id` in the census
training ids. `baselines.json` has a `feas09` entry. `picks.json` has
`stage4b` and `stage6`, each either `{record, value, rule, sensitivity}` or
`{no_pick: reason}`.

## Manifests

`MANIFEST.json` in an area:

```json
{
  "schema": "phase59-area-manifest/v1",
  "area": "census",
  "freeze_commit": "<commit that added scorecard-freeze.json>",
  "produced_at_head": "<HEAD when the manifest was written>",
  "scorecard_sha256": "<frozen digest>",
  "files": {"census.json": {"sha256": "<digest>", "size_bytes": 0}}
}
```

The file map skips `MANIFEST.json`, `logs/`, and `__pycache__`. `produced_at_head`
must be a descendant of `freeze_commit` (equality counts). The commit that last
changes `MANIFEST.json` must be a descendant of `produced_at_head`.

`evidence/manifest.json` uses schema `phase59-evidence-manifest/v1` and the
same fingerprint fields over every file under `evidence/` except itself,
`logs/`, and `__pycache__`. Paths are relative to `evidence/`.

## Other records

- `phase59-files-opened/v1`: `test_split_opened`, `blocked_attempts`, and
  `refused_before_open` are all 0.
- `phase59-provenance/v1`: tool, redacted command, git head, dirty flag,
  python/numpy/torch versions, timing, `ru_maxrss_bytes`, `data_root_source`.
  Provenance is excluded from `--check` byte comparisons.
- `phase59-completion-marker/v1` (`{step}.done.json`): `status` is `complete`,
  plus command, timing, `ru_maxrss_bytes`, the `vm_stat` preflight, and
  `result_files` name to SHA-256. Survey and diag07 accept a result only when
  a marker covers it and the hashes still match.
- `phase59-launch-lock/v1` at `evidence/logs/launch.lock.log`: `area`, `step`,
  `run_id`, `pid`, redacted `command`, `utc_started`. `begin_long_step` creates
  it with an exclusive create. A second long step prints
  `LAUNCH-REFUSED: {area}/{step} run <run_id> pid <pid> alive <true|false> started <utc>`
  and exits 6. `end_long_step` releases it after the completion marker (build)
  or the final OK line (check). `record_long_step_failure` appends one
  `phase59-launch-failure/v1` line to `evidence/logs/launch-failures.log` and
  releases the lock. Without the matching run id it recovers only a dead pid.
  Never delete a lock by hand and never take over a live holder.
- Both lock files end in `.log`, so they are gitignored and outside every
  manifest. Detached-run logs go to `evidence/{area}/logs/{step}.log` and are
  also gitignored. They may contain absolute paths. Markers and results may not.
- Inline steps (the census in every mode, baselines in every mode) end with
  `runtime_gate`. The budget is 600 seconds. Exactly 600 passes. Over budget
  prints `{LABEL}-RUNTIME-OVER-BUDGET` and returns 5. The passing line is
  `WALL-SECONDS <seconds> budget 600` on stderr.

## Checker

```text
python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py scorecard-frozen
python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py manifest --area census
python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py audit --skip-rederive --require-committed
python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py census --skip-rederive --require-committed
python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py survey --skip-rederive --require-committed
python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py baselines --skip-rederive --require-committed
python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py diag07 --require all --require-committed
python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py guardrails
python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py final
```

OK tokens: `SCORECARD-FROZEN-OK`, `MANIFEST-<AREA>-OK` (`MANIFEST-CENSUS-OK`,
`MANIFEST-ALL-OK`), `AUDIT-OK`, `CENSUS-OK`, `SURVEY-OK`, `BASELINES-OK`,
`DIAG07-OK`, `GUARDRAILS-OK`, `PHASE59-EVIDENCE-OK`.

`scorecard-frozen --pre-commit` checks hashes and skips git ancestry.
`--require-committed` demands every area file, including `MANIFEST.json`, is
tracked, clean, and first committed strictly after the freeze.
`--skip-rederive` skips the producing tool. `final` does not skip it.
Every command except `manifest --write` is read-only. Running a check twice
gives the same result.

Re-derivation, from the repository root:

```text
python -B -m pinn.verification.stage0_census --acceptance --check
python -B -m pinn.verification.stage0_census --check
python -B -m pinn.verification.dataset_survey --check
python -B -m pinn.verification.baselines --check
```

Those print `AUDIT-CHECK-OK`, `CENSUS-CHECK-OK`, `SURVEY-CHECK-OK`, and
`BASELINES-CHECK-OK`. DIAG-07 results are hash-checked against
`generation-7-retention.json`. They are not re-run. Gate G1 is recomputed
with the frozen `g1_fires` rule from the recorded primary shares.

## Detached launch

Long steps (the survey pass and its check, every DIAG-07 driver) take the
launch lock, then the `vm_stat` preflight, then:

```text
nohup python -B -m pinn.verification.dataset_survey > evidence/survey/logs/survey.log 2>&1 &
```

Wait until `{step}.done.json` exists and `completion_marker_ok` is true.
A halt, a tolerance failure, a preflight refusal, or any exception calls
`record_long_step_failure` and releases the lock.
