# Phase 50 Evidence Tree

**Scaffolded:** 2026-08-12 (plan 50-01)

`runs/` is gitignored wholesale, so every artifact Phase 51 and Phase 52 need
from a Phase-50 run must be copied into this committed tree
(`50-CONTEXT.md` D-29). This file is the layout index; `run-ledger.md` (also
in this directory) is the authoritative per-attempt record of what exists and
why.

## Reproduction boundary

Every Phase-50 launch executes **inline in this worktree**
(`.worktrees/trainex`, `milestone/v2.2`), under
`<home>/miniforge3/bin/conda run -n pinn-train`, with the corpus
resolved via `default_data_root()` from the main-repo checkout — never a
gsd-executor-style fresh worktree and never a data copy (`50-CONTEXT.md`
D-27). Because `runs/` is gitignored, every evidence copy in this tree is
pinned to its `runs/` source by exact repo-relative source path and sha256 in
`manifest.json` (plan 50-03), so the evidence is provably faithful even
though the large runtime artifacts it was copied from never enter git
history (D-29). Checkpoints and TensorBoard event files stay out of this tree
by size; their identities are hashed instead of copied (see "Checkpoints" below).

## Layout

| Path | Contents | Written by |
|---|---|---|
| `README.md` | This file. | 50-01 |
| `run-ledger.md` | The D-22 per-attempt/per-invocation ledger (schema `phase50-run-ledger/v2`). Scaffolded empty here; appended as uncommitted edits during the band; closed and committed at band-generation close. | scaffolded 50-01; appended + closed + committed 50-02 |
| `config-band-diff.txt` | The D-04 receipt: literal `diff` output proving the three graded configs vary only in `run.seed`/`run.run_name`. | 50-01 |
| `band-record.md` | The D-24 per-seed band record: `gate_*` keys verbatim, the full validation-`eps_H` trajectory, sidecar distribution stats, `s_h`/`eps_h`/`n_train`, the `front_idx` high-water trajectory, final per-term losses, INST-02 gradient stats, and preflight/eligibility facts. | 50-03 |
| `manifest.json` | The sha256 provenance manifest: `{repo-relative evidence path: sha256}` for every copied file, proving the extraction is byte-faithful to its `runs/` source. | 50-03 |
| `source-manifest.json` | The companion manifest of `runs/` SOURCE paths + hashes the copies in this tree were taken from (so a later `runs/` mutation is independently detectable). | 50-03 |
| `candidate-receipt.json` | The plan 50-03 execution receipt for the pre-registered candidate: `source_config_sha256`, `frozen_config_sha256`, reproduced `splits.json` hash, selected `best.pt` hash, and terminal artifact hashes — keyed to `50-PRE-REGISTRATION.md`'s own commit. | 50-03 |
| `build_phase50_evidence.py` / `verify_phase50_evidence.py` | The extraction builder and an independent re-derivation verifier (mirrors the Phase-44 `build_manifest.py` convention). | 50-03 |
| `corpus/generation-<N>.json` | Per-band-generation corpus identity snapshot (file listing + `corpus_snapshot_sha256`). | 50-02 |
| `environment/generation-<N>.json` | Per-band-generation environment fingerprint snapshot (`environment_snapshot_sha256`). | 50-02 |
| `calibration/` | Every `runs/.calibration/stage0-timing.json` generation this band produced (the mutable canonical file is never the evidence copy — each generation's calibration is copied to an immutable, timestamped path here). | 50-02 |
| `verify/` | Fresh `pinn.verify` marker receipts (`verify_invocations[]` transcripts + markers). | 50-02 |
| `cleanliness/` | Runtime/corpus/environment boundary receipts (`cleanliness_receipts[]`). | 50-02 |
| `attempts/<archived-attempt>/` | CONDITIONAL: forensic copies for an archived failed/HALTed attempt or a superseded smoke (a stale-calibration refresh, a positively-identified transient retry). Includes `invocation-<II>/` recovery/adoption snapshots when `invocation_snapshot` is non-null. | 50-02 |
| `launch-transcripts/` | Combined stdout+stderr for every invocation (fresh, refused, or superseded), matching `invocations[].launch_transcript` / `transcript_sha256`. | 50-02 |
| `stage0-rerun-smoke/` | The D-29 per-run evidence copy set for the smoke (see below). | 50-03 |
| `stage0-rerun-seed41/` | The D-29 per-run evidence copy set for seed 41. | 50-03 |
| `stage0-rerun-seed42/` | The D-29 per-run evidence copy set for seed 42 (the pre-registered candidate). | 50-03 |
| `stage0-rerun-seed43/` | The D-29 per-run evidence copy set for seed 43. | 50-03 |

## The D-29 per-run file set

Each `stage0-rerun-{smoke,seed41,seed42,seed43}/` directory above holds, at
minimum, the frozen resolved `config.yaml`, `summary.json`, `summary.md`,
`preflight.json`, `training_metadata.json`, `splits.json`,
`curriculum.jsonl`, `validation.jsonl`, every `validation_gate/step-*.json`
sidecar referenced by a `validation.jsonl` event, and `status.json`. **All**
referenced `validation_gate` sidecars are retained — not only the terminal
one — because the D-24 band record needs the full per-trajectory
distribution trajectory across every validation event, not just the last.
Any `failure/` bundle and the complete `logs/train.log.jsonl` from an
archived attempt are retained in full: `train.log.jsonl` is what Phase 44's
forensics actually read, and it is what any future re-derivation over
Phase-50 evidence will read too. The small `run_start_rng.pt` is retained as
CTRL-08 RNG provenance — it is a tiny seed-stream record, **not** a model
checkpoint, and its exclusion is not implied by the checkpoint exclusion
below.

**A note on `*.log`:** the repository's `.gitignore` excludes `*.log`
globally, so `logs/train.log` (the human-readable mirror) cannot be committed
without an explicit negation and is deliberately **not** retained here;
`train.log.jsonl` does not match that glob and **is** retained, and it is the
strictly more complete, machine-readable record. A `failure/tail.log`
artifact inside a retained failure bundle is copied to a tracked
`failure/tail.log.txt` destination (the `.txt` extension sidesteps the same
glob), with source/copy hash equality recorded in `manifest.json`.

## Checkpoints (excluded, but identity-hashed)

Model checkpoints and TensorBoard event files are excluded from this tree by
size. What IS retained, in the ledger and the band record rather than as
copied bytes: the identity hashes of `best.pt`, the `latest` checkpoint, and
every stage-boundary/terminal checkpoint the ledger's
`terminal_artifact_sha256` map names. The pre-registered candidate's selected
`best.pt` digest is additionally repeated in `candidate-receipt.json`'s
candidate block, so Phase 51 has it in one place without cross-referencing
the full ledger. A hash proves identity — it does not let anyone recover an
excluded checkpoint's bytes, and a fresh same-seed MPS rerun (not bitwise
reproducible; `50-CONTEXT.md` §"Recovery / attempt policy") may **never**
substitute for the actual selected model.

## Retention boundary

Every `runs/` canonical and archived directory this band produces must be
preserved on disk **through Phase 52** — this evidence tree is a faithful,
hash-proven copy, not a replacement, and Phase 51 requires the exact
candidate `best.pt` path and hash to exist and match, or it STOPs rather than
substituting a different checkpoint or a fresh rerun.
