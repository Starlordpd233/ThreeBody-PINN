# Phase 50: Valid Stage-0 Re-Run - Pattern Map

**Mapped:** 2026-08-11
**Files analyzed:** 12 new/modified file classes (4 configs; 4 phase-level governance/evidence
records; 1 per-run evidence-copy bundle class, ×4 runs; 1 divergence-register append; 2
conditional gap-register files)
**Analogs found:** 12 / 12 — every artifact this phase produces has a same-shape precedent
already committed in this repository.

## Framing note (read first)

Phase 50 is not a typical feature-build phase, and this pattern map looks different from a
controller/service/component map as a result. Per `50-CONTEXT.md`'s own "Reusable Assets" section,
**the phase adds zero new `pinn/` production code** — `python -m pinn.train --config <yaml>` is
already the complete launch interface. Every new file is one of two kinds:

1. **Config YAML copies** (`configs/*.yaml`) — verbatim copies of two already-shipped templates,
   each with a 1-3 field delta (seed, run_name, log_every, one invariants line).
2. **Governance / evidence records** (Markdown + JSON under `.planning/phases/50-*/`) — this
   repo has a well-established, four-times-repeated convention for exactly this artifact type,
   set by Phases 43 (v2.0), 44 (v2.1), 46 and 47 (v2.2). Phase 50's run ledger, band record,
   pre-registration record, and sha256 evidence manifest are new instances of that convention,
   not a new pattern.

The strongest analogs are therefore **prior evidence-extraction phases**, not application code.
`.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/evidence/pilot/README.md`
is the single most load-bearing analog in this map: it is the committed evidence record from the
*same* v2.0 pilot runs (`runs/stage0-pilot-seed41/42/43/`) that this phase re-runs under the
repaired recipe — literally the direct ancestor of Phase 50's run ledger and band record.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `configs/<smoke-name>.yaml` (planner-named, distinct from `stage0-smoke`) | config | file-I/O | `configs/smoke.yaml` (full file) | exact — literal copy + 1-line amendment |
| `configs/<band-name>-seed41.yaml` (planner-named, distinct from `stage0-pilot-seed41`) | config | file-I/O | `configs/stage0-example.yaml` (full file) | exact — literal copy + seed/run_name/log_every |
| `configs/<band-name>-seed42.yaml` | config | file-I/O | `configs/stage0-example.yaml` | exact |
| `configs/<band-name>-seed43.yaml` | config | file-I/O | `configs/stage0-example.yaml` | exact |
| Pre-registration record (e.g. `50-PRE-REGISTRATION.md`) | governance-record | file-I/O | `44-DIAGNOSIS.md` §5 "pre-registered ... stated BEFORE" prose + `evaluation-receipt.json` identity-pinning | role-match |
| Config-delta record (e.g. `50-CONFIG-DELTA.md`) | governance-record | file-I/O | `pinn/conformance/divergence_register.json` qualification-entry mechanism (exact) + `44-DIAGNOSIS.md` §1 confound framing (prose precedent, partial) | partial — see "No Analog Found" |
| Run ledger (e.g. `50-RUN-LEDGER.md` or `evidence/run-ledger.md`) | governance-record / event-log | event-driven | `43-*/evidence/pilot/README.md` `records[]` array | exact |
| Band record (e.g. `50-BAND-RECORD.md` or `evidence/band-record.md`) | governance-record / aggregation | transform | `43-*/evidence/pilot/README.md` + `pinn/training/summary.py` `_GATE_KEYS` passthrough | exact |
| Per-run sha256 evidence manifest (×4 runs) | provenance-manifest / utility | batch | `44-*/evidence/build_manifest.py` + `44-*/evidence/manifest.json` | exact |
| Per-run evidence copies: `config.yaml`, `summary.json`, `summary.md`, `preflight.json`, `training_metadata.json`, `splits.json`, `curriculum.jsonl`, `validation.jsonl`, `validation_gate/step-*.json`, `status.json` (×4 runs) | evidence-copy (mirrored artifact) | file-I/O | `runs/stage0-pilot-seed4X/*` (v2.0 baseline, resident in this worktree) + producing modules | exact for copy mechanics; **no real-corpus prior instance** for 3 of 10 files (see below) |
| `pinn/conformance/divergence_register.json` (MODIFIED — one appended entry) | registry-entry (CRUD append) | CRUD | its own existing `CONF-01-QUALIFICATION` / `I_WARM-INTEGER-FLOOR` entries | exact |
| `50-GAPS.md` (CONDITIONAL — only if a gap opens) | governance-record | event-driven | `46-GAPS.md`, `47-GAPS.md` | exact |
| `.planning/milestones/v2.2-GAPS.md` (MODIFIED, CONDITIONAL — index append) | governance-index | event-driven | the file's own existing structure (already updated by Phases 46/47/49) | exact |

---

## Pattern Assignments

### `configs/<smoke-name>.yaml` (config, file-I/O)

**Analog:** `configs/smoke.yaml` (59 lines, full file — this IS the copy source per D-04/D-13)

Full content (copy this verbatim, then apply exactly the D-15 delta):

```yaml
run:
  seed: 42
  precision: float32
  device: mps
  smoke: true
  log_every: 50
  run_name: stage0-smoke
  checkpoint:
    every_n_steps: 100
    rolling_keep: 4
  # GATE-03 / D-20: the owner sets front_advance_window_n here when invariant
  # B should enforce a window. Absent or null means record-only and carries
  # the open INV-B-N-UNSET divergence, so eval01_precondition_i is false.
  invariants:
    # front_advance_window_n: <owner-provided positive integer>
  monitor:
    heartbeat_secs: 30
    staleness_factor: 3

stage:
  max_epochs: 300
  n_adam: 300
  stagnation_window: 10000
  percentile_10_relaxation: 0.1
  replay_count: 32

opt:
  validation_every: 100

loss:
  lambda_e_max: 0.0

data:
  source: admitted
  blacklist_path: ../Documentation/problematic_ics_blacklist.json
```
(`configs/smoke.yaml:14-59`; header comment lines 1-13 explain the ACC-02 smoke's purpose and
the CPU-adapter/MPS-model split — carry that comment forward or replace it with a Phase-50
provenance note, but do not delete the DATA-01 independence explanation.)

**Required delta (D-15):** uncomment/set `run.invariants.front_advance_window_n: 500` (currently
commented placeholder at `configs/smoke.yaml:35`) so the smoke exercises the SAME
`invariant_b_window` preflight path the graded runs take. Also rename `run.run_name` (line 20) to
the phase's distinct smoke name (must not collide with `stage0-smoke`, which is the resident
v2.0/v2.1 artifact this phase must not overwrite — `runs/stage0-smoke/` already exists in this
worktree, per the `runs/` listing).

---

### `configs/<band-name>-seed{41,42,43}.yaml` (config, file-I/O, ×3)

**Analog:** `configs/stage0-example.yaml` (64 lines, full file — the copy source per D-01/D-04/D-06)

Full content (copy this verbatim into three files, then apply exactly the D-04/D-05 deltas):

```yaml
run:
  seed: 42
  precision: float32
  device: mps
  log_every: 100
  run_name: stage0-example
  recover_retries: 0
  checkpoint:
    wall_clock_ceiling_s: 120
  guards:
    loss_explosion_ceiling: 100000000000.0
    disk_floor_fraction: 0.05
    memory_watermark_fraction: 0.7
  invariants:
    front_advance_window_n: 500
  monitor:
    heartbeat_secs: 30
    staleness_factor: 3

stage:
  max_epochs: 1000
  n_adam: 1000
  stagnation_window: 10000
  percentile_10_relaxation: 0.1

opt:
  validation_every: 100

loss:
  lambda_e_max: 0.0
```
(`configs/stage0-example.yaml:2-64`; the owner-ratification comments at lines 8-19, 26, 34-39
document WHY each value is what it is — carry them forward unedited, since D-06 requires these
values stay byte-identical to the shipped template.)

**Required deltas, applied identically to all three copies (D-04/D-05):**
- `run.seed`: `41`, `42`, `43` respectively (line 3)
- `run.run_name`: the phase's distinct per-seed name (line 7) — must not collide with
  `stage0-pilot-seed41/42/43` (resident v2.0 artifacts in `runs/`)
- `run.log_every`: `100` → `50` (line 6) — the ONLY non-seed/non-name delta from the shipped
  template, per D-05's instrumentation-density rationale
- `data:` block is **absent** from `stage0-example.yaml` — D-02 requires it be added
  (`data.source: admitted`, same `blacklist_path: ../Documentation/problematic_ics_blacklist.json`
  used by `configs/smoke.yaml:59`) since the shipped example predates that requirement being
  made explicit; verify this is not already implied by a code-level default before adding it.

**Verification that this delta discipline was followed (D-04's required diff evidence):** run
`diff` across the three seed configs and capture the output as phase evidence — the diff must
show ONLY `run.seed` and `run.run_name` lines changing. See the "Configure step" convention below
for the shell-command-plus-verbatim-output style this repo uses for that kind of proof.

---

### Configure-step copy convention

**Analog:** `docs/runbooks/training/2026-07-18-stage0-training-operator-runbook.md:40-46`

````markdown
### Configure

Copy the example before editing the run name and Stage-0 budget:

```bash
cp configs/stage0-example.yaml configs/stage0-local.yaml
```
````

Phase 50's four `cp` invocations (one per config) are the same operation this runbook already
documents as canonical — just with phase-specific destination names instead of `stage0-local.yaml`,
and (for the smoke) `configs/smoke.yaml` as the source instead of `stage0-example.yaml`. The
Launch section immediately below it (`runbook.md:48-60`) is the exact `python -m pinn.train
--config <yaml>` / `scripts/train-unattended.sh --config <yaml>` invocation pair Claude's
Discretion leaves open (attended vs. unattended) — both are pre-documented, either is compliant.

---

### Pre-registration record (governance-record, file-I/O)

**No single prior "pre-registration" FILE exists**, but this repo has twice used the identical
*discipline* — state the criterion/rubric in writing before any number that could bias it exists
— and that discipline, not a file layout, is what must be copied.

**Analog 1 — the "stated BEFORE" prose pattern:** `44-DIAGNOSIS.md:77-79` and `:127-140`

```markdown
[FACT] Pre-registered verdict (D-05, stated in the script before any number is read as a verdict):
failure is **uniform** iff `min > 1e-5` (strict). `min = 0.9741 > 1e-5` → **uniform failure**;
...

## 5. Pre-registered ranking rubric (stated BEFORE the table)

[HYP] The rubric below is fixed in this report before any candidate is ranked, so the ordering is
not post-hoc (same discipline as DIAG-01's D-05 criterion).
```

Phase 50's pre-registration record should open the same way: state the candidate seed (42), the
checkpoint rule (`best.pt`), and the fallback order (42→41→43) as **fixed, dated, committed text**
— structurally the same move as DIAG-01's criterion-before-verdict and DIAG-03's
rubric-before-ranking. The record's own commit timestamp (D-29: "must be committed before the
first graded run, so its timestamp proves it preceded the numbers") plays the role the pre-registered
script constant plays in `44-DIAGNOSIS.md`.

**Analog 2 — identity-pinning three hashes:** `runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json`
(full file, 621 bytes):

```json
{
  "checkpoint_path": "runs/stage0-pilot-seed42/checkpoints/best.pt",
  "checkpoint_sha256": "6c6f4ae0ebbf6dd56a792503fb32428038bb8dc0f9dc235507a11eff7f9edeaa",
  "config_sha256": "ac15f434681d2244fda9a0bcdc8b33416ed1c8737b682f695782501862fb86ad",
  "eps_h": 237.2086056078468,
  "run_dir": "/Users/.../runs/stage0-pilot-seed42",
  "schema_version": "phase43-evaluation-receipt/v1",
  "scs": 2.3751304405952904,
  "splits_sha256": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
  "timestamp": "2026-07-22T12:23:13.553360+00:00",
  "verdict": "FAIL"
}
```

This is `pinn/evaluate.py`'s own pattern for proving "I evaluated exactly this checkpoint against
exactly this config against exactly this split" — checkpoint/config/splits each pinned by sha256.
The pre-registration record should pin the same three identities (or at minimum name the exact
`checkpoints/best.pt` retention rule) BEFORE any of them exist, so Phase 51 can later prove it
evaluated the pre-registered run rather than a different one. D-12's own table already uses this
exact convention (pinning `splits.json` sha256 per seed before the run reproduces it).

---

### Config-delta record + divergence-register qualification entry (D-03)

**No standalone "config-delta document" precedent exists** — prior phases narrated deltas inline
inside a broader evidence README (43-06, below) rather than as a dedicated file. What DOES have an
exact precedent is the mechanism D-03 requires for making the caveat durable: a `kind:
"qualification"` entry in `pinn/conformance/divergence_register.json`.

**Analog — existing qualification-kind entries:** `pinn/conformance/divergence_register.json:122-135`
(`CONF-01-QUALIFICATION`) and `:170-182` (`I_WARM-INTEGER-FLOOR`):

```json
{
  "authority": "Owner ruling GAP-46-06 option B",
  "id": "CONF-01-QUALIFICATION",
  "kind": "qualification",
  "proof_test": null,
  "rationale": "CONF-01 is settled by owner instruction on measured arm evidence, not by a clean VERDICT_TARGETS_ARE_RAW or VERDICT_TARGETS_ARE_SCALED token. This qualification is mandatory wherever CONF-01 is cited under EVAL-01 precondition (ii): RG-02 was settled by measured evidence, not a clean verdict token.",
  "spec_citation": ".planning/REQUIREMENTS.md CONF-01; EVAL-01 precondition (ii); GAP-46-06",
  "status": "open",
  "title": "CONF-01 carries an owner-ruling qualification",
  "waiver": null,
  "what_it_would_take": "Phase 51 must carry this qualification whenever it projects CONF-01 into EVAL-01 precondition (ii)."
}
```

A new entry for the 1000-vs-300-step budget delta follows this exact shape: `kind:
"qualification"`, `proof_test: null` (a documentation caveat, not something a test asserts),
`status: "open"` (it must travel forward into Phase 52's DIAG-05 re-derivation), `authority` citing
`50-CONTEXT.md D-03`, and `what_it_would_take` stating that the caveat is discharged only once a
budget-matched arm exists (the deferred idea) or the owner rules otherwise.

**Write path — do not hand-edit the JSON.** `pinn/conformance/register.py:222-247`:

```python
def load_divergence_register(path: str | Path | None = None) -> dict[str, Any]:
    """Load and fail-closed validate the committed divergence register."""
    ...

def write_divergence_register(
    path: str | Path | None = None, payload: Mapping[str, Any] | None = None
) -> Path:
    """Validate and atomically write a deterministic register artifact."""
    target = _path_for(path)
    if payload is None:
        payload = load_divergence_register()
    checked = _validate_payload(dict(payload))
    text = json.dumps(checked, sort_keys=True, indent=2) + "\n"
    return atomic_write_text(target, text)
```

Load, append the new dict to `payload["entries"]`, call `write_divergence_register(payload=...)` —
this goes through the same `_validate_payload` fail-closed check (`_KINDS = frozenset({"divergence",
"qualification", "deferred-scope"})`, `register.py:42`) that already guards the other 16 entries, so
a malformed entry is refused rather than silently written.

The standalone markdown config-delta record (if the planner still wants one for human readability)
should then simply narrate the same fact prose-style, in the manner of `44-DIAGNOSIS.md`'s
confound framing:

> "1000 vs 300 steps means any v2.2-vs-v2.0 outcome difference is confounded between the
> conformance repair and a 3.33× larger budget." (`50-CONTEXT.md` D-03, verbatim)

---

### Run ledger + Band record (governance-record, event-driven / transform)

**Analog:** `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/evidence/pilot/README.md`
(194 lines, full file) — this is the single strongest analog in the whole map: it is the committed
evidence record from re-running exactly `runs/stage0-pilot-seed41/42/43/`, the same three runs
Phase 50 re-executes under the repaired recipe.

**Structure to copy** (narrative header → reproduction boundary → machine-readable JSON block →
integrity notes):

````markdown
# Phase 43 Stage-0 pilot evidence

This directory records the traceable reduction of three ordinary admitted-data pilot runs
executed on 2026-07-22. The large runtime artifacts remain under `runs/` and are identified
here by paths, config identity digests, and SHA-256 hashes.

## Reproduction boundary

Each temporary input was copied from `configs/smoke.yaml`; only `run.seed`, `run.name`, and
the already owner-ratified ... were set. The commands were:
```text
~/miniforge3/envs/pinn-train/bin/python -m pinn.train --config /tmp/.../seed41.yaml
...
```

## Machine-readable evidence manifest

Tests parse this block without launching the pilots.

<!-- phase43-pilot-schema: phase43-pilot/v1 -->
```json
{ ... }
```

## Integrity notes
...
````
(`43-*/evidence/pilot/README.md:1-21` header/reproduction; `:22-188` JSON block; `:190-194`
integrity notes.)

**JSON schema — this IS the run ledger + band record shape, condensed to one example record**
(`43-*/evidence/pilot/README.md:22-89`):

```json
{
  "schema": "phase43-pilot/v1",
  "generated_utc": "2026-07-22T08:04:00+00:00",
  "confidence_rule": { "high_when_completed_seeds_at_least": 2, "otherwise": "LOW", "diverged_seeds_retained": true },
  "common": { "data_admission": "admitted", "device": "mps", "precision": "float32", "steps_requested": 300, ... },
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
      "final_losses": { "data": 0.158, "ic": 9177.5, "phys": 566627968.0, "energy": 6635.6, "angmom": 68.78, "total": 566643776.0 },
      "peak_total_loss": 6081173504.0,
      "peak_grad_norm": 95203855695872.0,
      "validation": { "step": 300, "final_val_loss": 463856672.0, "trend": "worsening" },
      "checkpoints": ["best.pt", "ckpt-....pt", "latest.pt", "stage-0-init.pt", "step-000100.pt", "step-000200.pt", "step-000300.pt"],
      "failure_files": [],
      "sha256": {
        "config.yaml": "86e6045b72df87e2167b1ec6c501abd2cd6acb17900350802943c76b04794e7d",
        "summary.json": "dbbcde8b8ee545f7ba8e142456cdc3d3391e923db6b34f2073eaec38cad5fd28",
        "status.json": "6f661b42f8e6da9690ccbe8c9de11e92e2f350a7e0c915614954679e35c00c7d",
        "validation.jsonl": "c22bb39a70c60308bb688196101b1f6dede34ddb61047191dbcdd69748a5722a",
        "logs/train.log.jsonl": "d1be6a6613f59526840180bad9fd6a0cecaa7df7f45a510adf24c92b429c3998"
      }
    }
  ],
  "rollup": { "completed_seed_count": 3, "diverged_seed_count": 0, "confidence": "HIGH", "spread_formula": "(max - min) / median", ... },
  "candidate_observation_refs": { "loss_explosion_ceiling": ["rollup.max_observed_total_loss", "records[*].peak_total_loss"], ... }
}
```

Map this shape onto Phase 50's two records directly:
- **Run ledger (D-22)** = the `records[]` array, but with EVERY launch (refused/HALTed/failed/
  superseded/graded), not just successes — add a `disposition` value the v2.0 schema didn't need
  (`refused`, `halted`) and a `git_head` field (D-17's pinning requirement; the 43 schema didn't
  need this because nothing could commit mid-band at that point in the project).
- **Band record (D-24)** = an extended `records[]` entry per seed, adding the `gate_*` block (copy
  the exact 8-key list from `pinn/training/summary.py:67-76`, shown below), the full
  `validation.jsonl` trajectory (not just the terminal event, unlike v2.0's schema which only
  recorded `validation: {step, final_val_loss, trend}` at line 69-73 above), the
  `validation_gate` sidecar distribution stats, `s_h`/`eps_h`/`n_train`, and `front_idx`.

**The verbatim-projection field list to copy from `summary.json` (D-24, never recompute):**
`pinn/training/summary.py:67-76`

```python
# Phase 46 gate keys projected verbatim from the last validation record (D-19).
# Persisted-bytes passthrough: never recomputed, never null-collapsed (D-20).
_GATE_KEYS = (
    "gate_schema_version",
    "gate_eps_h",
    "gate_scs",
    "gate_verdict",
    "gate_status",
    "gate_n_trajectories",
    "gate_n_nonfinite",
    "gate_sidecar",
)
```

Note the v2.0 pilot's own `validation.jsonl` (already on disk, `runs/stage0-pilot-seed42/validation.jsonl`)
predates these keys entirely — `{"final_val_loss": 838149312.0, "step": 100, "trend": "unavailable"}`
— confirming D-24's observation that `gate_*` is new in v2.2 and is exactly the signal the band
record adds.

---

### Per-run sha256 evidence manifest (provenance-manifest, batch)

**Analog:** `.planning/milestones/v2.1-phases/44-physics-gate-forensics/evidence/build_manifest.py`
(131 lines, full file) + `.../evidence/manifest.json` (34 lines, full file) — the most recent, most
rigorous sha256-manifest convention in the repo, one milestone before this one.

```python
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def git_head():
    """Bounded `git rev-parse HEAD` -> (head_sha | None, available). Mirrors pinn/verify.py."""
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO),
                            capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            sha = r.stdout.strip()
            if sha:
                return sha, True
    except Exception:
        pass
    return None, False
```
(`44-*/evidence/build_manifest.py:42-63`)

Resulting `manifest.json` shape (`44-*/evidence/manifest.json:1-34`):

```json
{
  "schema": "phase44-evidence-manifest/v1",
  "generated_by": "evidence/build_manifest.py",
  "git_head": "8631576dc5d8f76d1d0b301895ec5014161941cc",
  "git_head_available": true,
  "inputs": { "runs/stage0-pilot-seed42/splits.json": "5846ae5b...", "...": "..." },
  "cross_check": { "all_match": true, "mismatches": [], "provenance_entries_checked": 15 },
  "convention_note": "..."
}
```

Adapt directly: `DIAG_OUTPUTS` (44's list of files to cross-check) becomes Phase 50's list of the
ten per-run evidence files (D-29); `inputs` becomes `{repo-relative evidence path: sha256}` for
every copied file. The `cross_check` block is optional for Phase 50 (44 needed it because it
recomputed provenance already embedded in upstream diag scripts; Phase 50 is copying, not
re-deriving, so a simpler `{path: sha256}` dict — Phase 43's convention, shown above — is also
fully precedented and lighter-weight). Either is a legitimate choice per Claude's Discretion; the
44 script form is preferred if the executor wants a re-runnable, tamper-evident manifest, and the
43 inline-dict form is preferred if a single narrative README is sufficient.

**Layout table + reproduction-commands convention:** `44-*/evidence/README.md:1-32` (full excerpt
already shown in file classification above) is the pattern for a top-level `evidence/README.md`
that indexes what lives where and how to reproduce it — apply the same table to Phase 50's
`evidence/<run>/` subdirectories.

---

### Per-run evidence copies (evidence-copy, file-I/O, ×4 runs)

The ten files D-29 lists are all EXISTING artifact types produced by shipped code; Phase 50 copies
them, it does not author new formats. Each has a byte-identical v2.0 real-corpus instance already
on disk in this worktree (`runs/stage0-pilot-seed42/`, confirmed resident) EXCEPT the three marked
below, which have a schema (writer code) but no prior real-corpus file to diff against.

| File | Producing code (schema source) | v2.0 real-corpus instance on disk? |
|---|---|---|
| `config.yaml` | frozen resolved copy of the launch config | yes — `runs/stage0-pilot-seed42/config.yaml` |
| `summary.json` / `summary.md` | `pinn/training/summary.py` `_compose`/`_render_md` | yes — full content below |
| `status.json` | `pinn/train.py` status writer | yes — full content below |
| `curriculum.jsonl` | stage-exit disposition log | yes — full content below |
| `validation.jsonl` | `opt.validation_every` event log | yes, but pre-`gate_*` schema (see Band Record section) |
| `splits.json` | `pinn/data/splits.py` `SplitManifest.to_dict` (`splits.py:397-406`) | yes, 4.16 MB, seed 42 byte-identical expected per D-12 |
| `training_metadata.json` | `pinn/training/run_metadata.py` `write_training_metadata` (`run_metadata.py:227-262`) | **no** — first real-corpus instance is this phase's own deliverable (D-14) |
| `preflight.json` | `pinn/conformance/preflight.py` `PreflightRecorder._write` (`preflight.py:295-316`) | **no** — same |
| `validation_gate/step-<8digit>.json` | `pinn/training/validation_gate.py` `publish_gate_sidecar`/`_observation_payload` (`validation_gate.py:338-413`) | **no** — same |

**`summary.json` real shape** (`runs/stage0-pilot-seed42/summary.json`, full file, 1250 bytes —
this is the exact object Phase 50's own `summary.json` files will superset):

```json
{
  "disposition": "finished",
  "final_losses": {"angmom": 587.65, "data": 0.1355, "energy": 4093.83, "ic": 38527.19, "phys": 650400832.0, "total": 650443456.0},
  "header": {
    "config_identity_digest": "ac15f434681d2244",
    "device": "mps",
    "end_utc": "2026-07-22T08:00:33.474008+00:00",
    "env_fingerprint": {"python_version": "3.11.15", "sw_vers": "...", "torch_build": "...", "torch_version": "2.12.1"},
    "precision": "float32", "run_name": "stage0-pilot-seed42", "seed": 42,
    "start_utc": "2026-07-22T07:57:15.790562+00:00", "wall_clock_secs": 197.683446
  },
  "run_name": "stage0-pilot-seed42",
  "schema_version": 1,
  "test_preview": {"eps_h": 237.2086056078468, "n_test_trajectories": 1500, "scs": 2.3751304405952904, "verdict": "FAIL"},
  "validation": {"final_val_loss": 78489008.0, "step": 300, "trend": "improving"}
}
```

Note this v2.0 instance predates Phase 46/49 — it carries no `conformance` block and no `gate_*`
keys inside `validation`. Phase 50's own `summary.json` (same producing code, now current) WILL
carry those fields (`_CONFORMANCE_KEYS` at `summary.py:95-99`, `eval01_precondition_i` at
`summary.py:513`) — the D-24 band record depends on that superset being present, which is exactly
the "first real-corpus contact" this phase provides for Phase 47/49's shipped-but-unexercised code.

**`training_metadata.json` schema (no real file exists yet — this IS the schema to expect):**
`pinn/training/run_metadata.py:251-260`

```python
payload = {
    "schema_version": TRAINING_METADATA_SCHEMA_VERSION,  # = 2
    "s_h": s_h,
    "eps_h": factor * s_h,
    "n_train": n_train,
    "eps_train": EPS_SOFT,
    "energy_floor_factor": factor,
    "frame": _live_frame_block(),
    **causal_clip_facts,
}
```

**`preflight.json` schema (no real file exists yet):** `pinn/conformance/preflight.py:295-304`

```python
payload = {
    "schema_version": PREFLIGHT_SCHEMA_VERSION,  # = 1
    "preflight_status": "failed" if any(e["status"] == "failed" for e in self._events) else "passed",
    "assertions": self._events,  # each: {event, stage, status, checks, census, open_divergences, findings}
}
```

**`validation_gate/step-<8digit>.json` sidecar schema (no real file exists yet):**
`pinn/training/validation_gate.py:338-349` (path) and `:360-390` (payload)

```python
def sidecar_relative_path(global_step) -> str:
    n = _strict_nonnegative_integral(global_step, what="global_step")
    return f"validation_gate/step-{n:08d}.json"

# payload: schema_version, run_dir, sidecar_path, global_step, stage, split, frame{...},
# n_trajectories, rows[{record_key, eps_h, scs}], n_nonfinite, eps_h_reject_threshold,
# scs_reject_threshold, aggregate_eps_h, aggregate_scs, verdict, gate_status
```

Copy the file at the **latest** `global_step` only (D-29: "the latest `validation_gate/step-*.json`
sidecar"), located by the highest 8-digit step number under `runs/<run>/validation_gate/`.

---

### `50-GAPS.md` (conditional — only if a gap is opened)

**Analog:** `.planning/phases/46-frame-resolution-gate-aligned-validation/46-GAPS.md:1-11` (header)
and `:12-60` (first gap entry, opening fields):

```markdown
# Phase 46 Gap Register — Frame Resolution & Gate-Aligned Validation

Phase-local STOP-protocol gap register for Phase 46 (milestone v2.2). Each entry
is a source-silent decision that this phase **surfaced** rather than decided, per
the CLAUDE.md / AGENTS.md STOP protocol and `46-CONTEXT.md` D-09 / D-13. The
milestone-wide index is `.planning/milestones/v2.2-GAPS.md` (created on the first
v2.2 gap, standing trigger).

This register is written by the Phase 46 orchestrator (parent session), not by a
subagent — per governance, the parent owns gap-register writes.

## GAP-46-01 — <one-line question as the heading>

- **Decision point:** ...
- **Where in artifact:** ...
- **Task context:** ...
- **Classification:** ...
- **Source silence:** ...
```

Header text for `50-GAPS.md` should follow the identical shape with `50-CONTEXT.md` D-19/D-30 as
the cited grounding (the D-numbers this phase's own governance section names), and the same
"parent-session-owns-gap-writes" note (D-30 in `50-CONTEXT.md` reiterates this — subagents return
findings, the orchestrator decides and logs). `47-GAPS.md` is an equally valid second reference for
the same convention. The milestone index update at `.planning/milestones/v2.2-GAPS.md` (18,041
bytes, already carries Phase 46/47/49 entries) follows the same per-gap-row format already
established there — append, do not restructure.

---

## Shared Patterns

### Strict JSON: `schema_version` + atomic write + fail-closed re-validate-on-load
**Source:** every machine-read artifact in `pinn/` — `preflight.py:36,177-180`,
`register.py:25,130-138`, `validation_gate.py:72,573-576`, `run_metadata.py:57,300-303`,
`splits.py:367,443-444`
**Apply to:** any of Phase 50's own records the planner chooses to author as JSON (run ledger,
band record, per-run sha256 manifest) rather than embedded-in-Markdown. Even the Markdown-embedded
convention (Phase 43) tags its JSON block with an explicit schema string
(`<!-- phase43-pilot-schema: phase43-pilot/v1 -->`, `43-*/evidence/pilot/README.md:21`) — carry a
`phaseNN-<artifact>/v1` schema tag regardless of which container format is chosen.

### Verbatim passthrough over recomputation
**Source:** `pinn/training/summary.py:65-66` — *"Phase 46 gate keys projected verbatim from the
last validation record (D-19). Persisted-bytes passthrough: never recomputed, never
null-collapsed (D-20)."*
**Apply to:** the band record's `gate_*`/`eps_h`/`s_h`/`n_train` fields — copy bytes from
`summary.json`/`training_metadata.json`, never re-derive them from raw logs.

### sha256 provenance pinning
**Source:** `43-*/evidence/pilot/README.md` (inline per-record `sha256` dict) and
`44-*/evidence/build_manifest.py` (standalone cross-checked manifest)
**Apply to:** the run ledger, the per-run evidence manifest, and the pre-registration record's
identity pins (checkpoint/config/splits).

### Evidence lives in the phase tree; runtime artifacts live in `runs/` (gitignored)
**Source:** `43-*/evidence/`, `44-*/evidence/`, `46-*/evidence/`, `47-*/evidence/` — four
consecutive phases follow this split.
**Apply to:** the whole `.planning/phases/50-valid-stage-0-re-run/evidence/` subtree; nothing
under `runs/` is ever the thing that gets committed.

### "Pre-registered ... stated BEFORE" prose discipline
**Source:** `44-DIAGNOSIS.md:77-79,127-130` (D-05's uniform-vs-tail criterion and the ranking
rubric, both stated in text before the number/table that could be biased by them)
**Apply to:** the pre-registration record — state seed/checkpoint/fallback-order as committed text
before any graded run exists, exactly the same rhetorical move.

### Gate-status vs. gate-verdict stay distinct
**Source:** `pinn/training/summary.py` `_GATE_KEYS` separates `gate_status` (instrumentation
health) from `gate_verdict` (the metric) — `summary.py:71-72`; the docstring at
`preflight.py`/`register.py` module level repeats the same "an instrumentation failure can never
render as a PASS" discipline the Phase-46 D-28 ruling established.
**Apply to:** every reported number in the band record (D-25 in `50-CONTEXT.md` requires this
explicitly).

---

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| Standalone config-delta **document** (as opposed to the register entry) | governance-record | file-I/O | No prior phase produced a dedicated "here is what changed and why" file; deltas were previously narrated inline inside a broader evidence README (`43-*/evidence/smoke/README.md`) or a diagnosis report (`44-DIAGNOSIS.md` §1). The mechanism that actually makes the caveat durable — the divergence-register qualification entry — IS exactly precedented (see Pattern Assignments above); a standalone Markdown file, if the planner adds one, is net-new prose composition, not a copied structure. |
| `training_metadata.json`, `preflight.json`, `validation_gate/step-*.json` — **as real-corpus files** | evidence-copy | file-I/O | The writer code and JSON schema are fully precedented (cited above with exact line ranges), but Phases 46/47/49 proved all three only against deterministic test fixtures (`50-CONTEXT.md` domain section: "all proven on deterministic fixtures"). No real-corpus instance has ever existed on disk before this phase, so there is no prior FILE to diff the new ones against — only the schema. This is expected and is precisely the "first real-corpus contact" the phase exists to produce (D-14). |

---

## Reference-only code seams (not authored, not copied — cited for planner context)

These exist already and are exercised, not modified, by Phase 50; they are not "analogs" in the
copy-from sense, but the planner needs their exact location:

- `pinn/train.py:576-627` `_check_duration_gate` / `DurationGateError` — the fingerprinted
  calibration refusal that makes the D-13 smoke-first sequencing mandatory, not optional.
- `pinn/training/timing.py`, `runs/.calibration/stage0-timing.json` (resident, stale `git_head`
  confirmed in `50-CONTEXT.md` D-13 — will be rewritten by the smoke's success path).
- `pinn/data/adapter.py` `default_data_root()` — resolves the corpus with no copy step (D-28).
- `scripts/train-unattended.sh` (227 bytes, exists) and `scripts/agent-commit` (2558 bytes,
  exists, executable) — the two operator entry points Claude's Discretion names.

---

## Metadata

**Analog search scope:** `configs/`; `.planning/phases/46-*`, `47-*`; `.planning/milestones/
v2.0-phases/43-*/evidence/`; `.planning/milestones/v2.1-phases/44-*/evidence/`; `runs/
stage0-pilot-seed{41,42,43}/` and `runs/stage0-smoke/` (resident v2.0/v2.1 baselines);
`pinn/training/{summary,run_metadata,validation_gate}.py`; `pinn/conformance/{preflight,
register}.py`; `pinn/data/splits.py`; `docs/runbooks/training/`.
**Files read in full or targeted range:** ~20 (2 config YAMLs full; 1 runbook full; 2 evidence
READMEs full — 43-pilot, 44; 1 evidence README long-form — 43-smoke; 1 build_manifest.py full;
1 manifest.json full; 5 pinn/ modules at targeted line ranges; 1 divergence_register.json full;
6 v2.0 pilot run artifacts full; 2 GAPS.md / DIAGNOSIS.md targeted excerpts).
**Pattern extraction date:** 2026-08-11
