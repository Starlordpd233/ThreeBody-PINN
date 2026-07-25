# Phase 44: Physics-Gate Forensics - Pattern Map

**Mapped:** 2026-07-23
**Files analyzed:** 8 (3 analysis scripts + their JSON outputs, 1 pinning manifest, 1 evidence README, 1 diagnosis report, 1 phase-local gap register, 1 milestone gap-index first entry)
**Analogs found:** 7 / 8 (the standalone SHA-256+commit-hash pinning manifest has only a partial/structural analog — see "No Analog Found")

This phase produces **read-only forensic analysis artifacts**, not application code. All files live under
`.planning/phases/44-physics-gate-forensics/` (D-01); nothing is written to `pinn/`, `runs/`, or the framework
specs.

## File Classification

| New File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `evidence/diag01/eps_h_distribution.py` | utility / analysis script | batch (read JSON → compute stats → write JSON) | `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` (JSON-in/JSON-out idiom) + `pinn/verification/gate_metrics.py` (the exact ε_H/aggregate formula, read as factual record only) | role-match (script shape) + exact (formula to reproduce) |
| `evidence/diag02/loss_decomposition.py` | utility / analysis script | batch (read 4× JSONL → per-step decomposition → write JSON) | `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` (same idiom) + `pinn/training/step_log.py`/`pinn/training/scheduled_weights.py` (schema source, factual record) | role-match |
| `evidence/diag03/seed_band.py` | utility / analysis script | batch (read JSONL/status + cite external `.md` records → spread stats → write JSON) | `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` (idiom) + `43-CALIBRATION.md` (the exact spread-formula and table shape to reproduce) | role-match |
| `evidence/manifest.json` | config / pinning record | write-once (SHA-256 of every input file + `git rev-parse HEAD`) | `pinn/verify.py::git_head()` (bounded commit-hash subprocess) + Phase 43's embedded `sha256` dict in `evidence/pilot/README.md` | partial — see "No Analog Found" |
| `evidence/README.md` | doc / evidence wrapper | transform (prose + machine-readable block) | `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/evidence/pilot/README.md` and `evidence/smoke/README.md` | exact |
| `44-DIAGNOSIS.md` | report / governance doc | transform (synthesize DIAG-01..03 → ranked, cited hypotheses) | `43-VERDICT.md` (frontmatter + evidence-matrix + citation style) + `43-CALIBRATION.md` (raw-observation table + confidence section) | exact |
| `44-GAPS.md` | gap register (phase-local) | event-driven (append on STOP-protocol gap) | `43-GAPS.md` | exact |
| `.planning/milestones/v2.1-GAPS.md` (first entry) | milestone gap index | event-driven (append, created on first gap) | `.planning/milestones/v2.0-GAPS.md` | exact |

## Pattern Assignments

### `evidence/diag01/eps_h_distribution.py`, `evidence/diag02/loss_decomposition.py`, `evidence/diag03/seed_band.py`

**Analog 1 (script shape — imports, JSON-in/out, never-skip-on-error idiom):** `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`

**Imports pattern** (`calculate_metrics.py:1-13`):
```python
#!/usr/bin/env python3
"""
Brutus Metrics Calculator
- Processes all Brutus output files (no completeness checks)
- Calculates conservation metrics (energy, momentum, angular momentum)
- Creates JSON metric files for every file, even if partial or erroneous
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
import time
```
Phase 44's three scripts should mirror this shape (stdlib `json`/`hashlib`/`subprocess` + `numpy`, `pathlib.Path`
for all paths, no argparse needed since D-01 says paths are hardcoded to the pinned run — no CLI args).

**JSON-write idiom** (`calculate_metrics.py:504-505`, inside `process_simulation_type`):
```python
with open(metrics_path, 'w') as f:
    json.dump(metrics, f, indent=2, default=str)
```
**Never-skip-on-error idiom** (`calculate_metrics.py:461,500-514`) — the house convention is that a metrics
function `calculate_metrics(...)` **always returns a dict**, even on partial/erroneous input (the dict carries
an `error` key rather than the script silently omitting output):
```python
# Calculate metrics (always returns a dict)
metrics = calculate_metrics(output_file, sim_type)
...
if metrics.get('error'):
    print(f"[{i+1:3d}/{len(output_files)}] ! {output_file.name} - Generated with error")
    with_errors += 1
```
This is the same spirit as D-02/D-03's determinism-over-cleverness and the self-check assertions below — a
script should fail closed on a genuine schema violation (per RESEARCH.md's assertion pattern) but never
silently drop or fabricate a number.

**Print-summary idiom** (`calculate_metrics.py:516-523`) — a plain stdout table at the end of the run, not a
logging framework:
```python
print("-" * 80)
print(f"Summary for {sim_type}:")
print(f"  Processed: {processed}")
...
print(f"  Time taken: {elapsed:.1f} seconds")
```

**Analog 2 (the exact formula DIAG-01 must reproduce — read as factual record of execution, NOT as spec
authority):** `pinn/verification/gate_metrics.py:180-239`
```python
def trajectory_eps_h(hamiltonian_series) -> float:
    """``eps_H = max_t |(H(t) - H(0)) / H(0)|`` for one trajectory. ..."""
    ...
    return float(torch.max(drift))

def aggregate_test_eps_h(per_trajectory_eps_h: Sequence[float]) -> float:
    """Worst-trajectory (maximum) aggregate over a test set's eps_H values.

    Any non-finite per-trajectory ``eps_H`` makes the aggregate non-finite
    (``nan``) — the aggregate is never silently computed from only the finite
    subset (SPEC prohibition: no fabricated / dropped nonfinite metric).
    """
    values = [float(v) for v in per_trajectory_eps_h]
    if not values:
        raise ValueError(...)
    if not all(math.isfinite(v) for v in values):
        return float("nan")
    return max(values)
```
`eps_h_distribution.py`'s self-check assertion (`recomputed_max == metrics_json["eps_h"]`) is directly
reproducing this function's behavior against `metrics.json`'s stored `per_trajectory` array. **Do not** cite
this file's "Worst-trajectory (maximum)" docstring comment as evidence that max is the spec-intended gate
statistic (Anti-Pattern, RESEARCH.md §C / Pitfall 5) — it documents what executed, which is exactly the D-07
gap this phase must route to `44-GAPS.md`, not resolve.

**Core computation pattern (DIAG-01 percentiles):**
```python
import json
import numpy as np

data = json.load(open("runs/stage0-pilot-seed42/evaluation/metrics.json"))
eps_h = np.array([e["eps_h"] for e in data["per_trajectory"]])
stats = {
    "min": float(eps_h.min()), "p25": float(np.percentile(eps_h, 25)),
    "p50": float(np.percentile(eps_h, 50)), "p75": float(np.percentile(eps_h, 75)),
    "p90": float(np.percentile(eps_h, 90)), "p99": float(np.percentile(eps_h, 99)),
    "max": float(eps_h.max()), "mean": float(eps_h.mean()),
    "frac_exceeding_1e5": float((eps_h > 1e-5).mean()),
}
```
(Source: RESEARCH.md's own directly-verified session output — reproduce the computation, do not copy the
printed numbers.)

**Self-check / fail-closed assertions (all three scripts):**
```python
assert len(per_trajectory) == 1500
assert max(e["eps_h"] for e in per_trajectory) == metrics_json["eps_h"]
assert set().union(*(e.keys() for e in per_trajectory)) == {"eps_h", "fidelity", "id", "variant"}
assert len(train_log_records) == 300
assert {r["step"] for r in train_log_records} == set(range(1, 301))
```
A failed assertion halts the script (raises) rather than writing a plausible-looking but unverified number —
matching `calculate_metrics.py`'s house convention of never silently omitting/fabricating output, and
`gate_metrics.py`'s "never silently computed from only the finite subset" phrasing.

**Interpreter constraint (all three scripts):** invoke as `~/miniforge3/envs/pinn-train/bin/python3
<script>.py`, matching the Phase 43 evidence precedent (`evidence/pilot/README.md:9-13` invokes
`~/miniforge3/envs/pinn-train/bin/python -m pinn.train ...` by absolute path, never bare `python3` or
`conda activate`). System `python3` (`/opt/homebrew/bin/python3`) has no numpy.

---

### `evidence/manifest.json`

**Analog 1 (commit-hash pinning — bounded, graceful-degrade subprocess call):** `pinn/verify.py` (`git_head()`,
~lines 355-383; docstring comment at line 116: *"Bound on the `git rev-parse HEAD` subprocess so a wedged git
can never hang"*):
```python
def git_head() -> tuple[Optional[str], bool]:
    """Return ``(head_sha, available)`` from a bounded ``git rev-parse HEAD``.

    A missing git binary, a non-repository directory, a non-zero exit, and a
    timeout are all reported as unavailable — verify still reports its ladder
    result; only the marker's authority is withdrawn.
    """
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(_repo_root()),
            capture_output=True, text=True,
            timeout=_GIT_TIMEOUT_S, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None, False
    if completed.returncode != 0:
        return None, False
    head = completed.stdout.strip()
    if not head:
        return None, False
    return head, True
```
Copy this exact bounded/graceful-degrade shape for the manifest's commit-hash field (RESEARCH.md's own
`commit_hash()` code example follows the same shape with a 10s timeout).

**Analog 2 (per-file SHA-256 dict shape):** Phase 43's `evidence/pilot/README.md:82-88` embeds, per run
record, a `sha256` object keyed by relative artifact path:
```json
"sha256": {
  "config.yaml": "86e6045b72df87e2167b1ec6c501abd2cd6acb17900350802943c76b04794e7d",
  "summary.json": "dbbcde8b8ee545f7ba8e142456cdc3d3391e923db6b34f2073eaec38cad5fd28",
  "status.json": "6f661b42f8e6da9690ccbe8c9de11e92e2f350a7e0c915614954679e35c00c7d",
  "validation.jsonl": "c22bb39a70c60308bb688196101b1f6dede34ddb61047191dbcdd69748a5722a",
  "logs/train.log.jsonl": "d1be6a6613f59526840180bad9fd6a0cecaa7df7f45a510adf24c92b429c3998"
}
```
`evidence/manifest.json` should use this exact `{relative_path: sha256_hex}` shape per input file, plus a
top-level `git_head`/`git_head_available` pair (matching `pinn/verify.py::current_fingerprint`'s
`git_head`/`git_head_available` field names, not the manifest's own invention).

**JSON write idiom:** `pinn/verify.py:464` — `atomic_write_text(destination, json.dumps(payload, indent=2) +
"\n")`. Use `indent=2` for `manifest.json` to match both this and `calculate_metrics.py`'s convention.

**Note:** see "No Analog Found" below — no existing file in this repo combines "standalone JSON file" +
"SHA-256 per input + commit hash" in one document; Phase 44 assembles it from the two precedents above.

---

### `evidence/README.md`

**Analog:** `43-verification-stage-0-pilot-acceptance/evidence/pilot/README.md` and `evidence/smoke/README.md`
(full files — this is a near-exact structural match).

**Section shape to copy** (`evidence/pilot/README.md:1-21`):
1. A one-paragraph "what this directory records" intro naming the exact date and run count.
2. `## Reproduction boundary` — the exact commands that were run, by absolute interpreter path, plus which
   config fields were varied vs frozen.
3. `## Machine-readable evidence manifest` — introduced with *"Tests parse this block without launching the
   pilots"* — a fenced JSON block preceded by a schema-tag HTML comment:
   ```
   <!-- phase43-pilot-schema: phase43-pilot/v1 -->
   ```json
   { "schema": "phase43-pilot/v1", "generated_utc": "...", ... }
   ```
   ```
   Phase 44's `evidence/README.md` should use an analogous `<!-- phase44-evidence-schema: phase44-evidence/v1 -->`
   tag if it embeds a summary block, or simply link to `manifest.json` and the three `diagNN/*.json` outputs
   (D-01's evidence directory keeps the JSON separate from the scripts, unlike Phase 43's inline approach —
   note this divergence explicitly in the README rather than silently copying Phase 43's inline-block shape).
4. `## Integrity notes` (`evidence/pilot/README.md:190-194`) — a short bulleted list closing the file, e.g.
   *"Config identity digests are the first 16 hexadecimal characters of each frozen `config.yaml` SHA-256..."*
   and *"No failure or divergence record was discarded."* Phase 44's closing section should state the
   equivalent: which script produced which hash, and that no trajectory/step was excluded from the computed
   distributions (D-04's "report the full distribution" spirit).

---

### `44-DIAGNOSIS.md`

**Analog 1 (frontmatter + evidence-matrix + citation discipline):** `43-VERDICT.md`

**Frontmatter pattern** (`43-VERDICT.md:1-13`):
```yaml
---
schema_version: phase43-verdict/v1
status: owner-signed
gate: FAIL
verdict: adjust
recommendation: adjust
owner_decision: adjust
owner_decision_date: 2026-07-22
receipt_citation: runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json
seed_citation: .planning/phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md
timing_citation: .planning/phases/43-verification-stage-0-pilot-acceptance/evidence/smoke/README.md
seams_citation: pinn/STATUS.md
---
```
`44-DIAGNOSIS.md` should carry an analogous frontmatter block (`schema_version: phase44-diagnosis/v1`, plus a
`*_citation:` field per DIAG-01/02/03 output and per external record cited) — this is the load-bearing
machine-checkable pointer set that lets Phase 45's ERW package snapshot the doc without losing provenance.

**Evidence-matrix table pattern** (`43-VERDICT.md:35-47`, header row `| Evidence | Observed result |
Grounding |`) — every claim gets its own row with an exact citation in the `Grounding` column (file path, or
file path + line/anchor):
```
| Evidence | Observed result | Grounding |
| --- | --- | --- |
| Sole held-out receipt | `FAIL`; `eps_H = 237.2086056078468`; `SCS = 2.3751304405952904`; ... | `runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json`; ... |
```
D-13's "≥4 candidates, each with supporting AND contradicting citations plus a discriminating test" should use
this exact table shape, with two additional columns (`Contradicting evidence`, `Discriminating test proposed`).

**"Decision boundary" section pattern** (`43-VERDICT.md:23-33`) — a short prose block stating what the record
does and does not claim, immediately after the title. `44-DIAGNOSIS.md`'s remedy-abstinence statement (D-15)
belongs in an analogous section, stated in the report's own words (not copied verbatim from CONTEXT.md).

**Analog 2 (raw-observation table + explicit-formula-before-table + confidence-with-caveats):**
`43-CALIBRATION.md`

**Explicit formula-before-table pattern** (`43-CALIBRATION.md:30-32`):
```
## Defined spread calculation

For every reported metric, the absolute span is `max(seed values) - min(seed values)`. The relative span is
`(max - min) / median(seed values)`. No values are rounded before the calculation.
```
DIAG-01's D-05 pre-registered uniform-vs-tail criterion should be stated in this exact "define the formula in
prose, then show the table" order — pre-registration only works if the criterion text precedes the computed
number in the document.

**Confidence-with-explicit-limits pattern** (`43-CALIBRATION.md:42-50`):
```
## Confidence

**Overall confidence: HIGH.** ... It is not a convergence claim: final validation relative span is
`3.8224247683129153`, and two final validation trends were worsening.

Field-level limits matter:
- Loss and retry evidence is direct: ...
- Disk evidence is weak: ...
```
DIAG-03's seed-dependent-split caveat (RESEARCH.md Pitfall 4) and the Phase-38-overfit-rung
over-generalization caveat (Pitfall 7) should be stated with this same "confidence label, then explicit
per-claim limits" structure, separating verified fact from agent hypothesis inline — this is the house
convention this project already uses for exactly this purpose.

---

### `44-GAPS.md`

**Analog:** `43-GAPS.md` (exact field structure — this is the CLAUDE.md STOP-protocol schema already
instantiated once in this repo).

**Exact field order to copy** (`43-GAPS.md:1-106`, `GAP-43-01`):
```markdown
## GAP-43-01 — <title>

- **Decision point:** ...
- **Where in artifact:** `file:line`, `file:line`, ...
- **Task context:** ...
- **Classification:** cross-phase reframing | semantic | operational coordination | process-artifact schema
- **Source silence:**
  - `file:line` — what it says and why it doesn't answer the question
  - ...
- **Mathematical / engineering grounding:** ...
- **Agent was tempted to:** ...
- **What the user needs to decide:**
  - **A. <option> (recommended):** ...
  - **B. <option>:** ...
- **Confidence of impact:** HIGH | MEDIUM | LOW — <reason>
- **Status:** OPEN
- **Resolution note:** (empty until resolved)
```
D-07's gap entry (the first, and likely only, expected entry per D-16) must use this exact field set and
naming (`GAP-44-01`), matching the CLAUDE.md-mandated schema verbatim — no field renamed, none omitted.

---

### `.planning/milestones/v2.1-GAPS.md` (first entry)

**Analog:** `.planning/milestones/v2.0-GAPS.md` (full file — this is the direct structural precedent for a
brand-new milestone gap index's first commit).

**Header + table pattern** (`v2.0-GAPS.md:1-8`):
```markdown
# v2.0 Milestone Gap Index

Milestone-wide index of owner-routed decisions and source-silent gaps across
v2.0 phases. Each entry cross-references the phase-local gap register that
holds the full record. Updated whenever a phase surfaces a new gap.

| Gap ID | Phase | Classification | Status | One-line summary |
|--------|-------|----------------|--------|------------------|
| GAP-37-01 | 37 | cross-phase reframing (owner-carved D1-p) | RESOLVED-WITH-INSTRUCTION (2026-07-12) | ... |
```
`v2.1-GAPS.md` should open with the analogous intro paragraph (swap "v2.0" → "v2.1", "37 phases" → "44
phases") and the same 5-column table, with `GAP-44-01` as its first row.

**Closing provenance line** (`v2.0-GAPS.md:190`):
```
*Created 2026-07-12 on the first v2.0 STOP/defer gap (GAP-37-01).*
```
`v2.1-GAPS.md` must close with the exact equivalent, satisfying D-16 ("created on the first gap under the
standing trigger").

**"Open gaps blocking downstream work" + per-phase resolved-gaps sections** (`v2.0-GAPS.md:33-49`) — also
present in the analog; if GAP-44-01 stays `OPEN` at phase close (expected, since D-07 is a governance
obligation the agent must not resolve), it belongs in the "Open gaps blocking downstream work" section, not
buried only in the table.

## Shared Patterns

### SHA-256 + commit-hash pinning
**Source:** `pinn/verify.py::git_head()` (bounded subprocess, graceful degrade) + Phase 43's
`evidence/pilot/README.md:82-88` (per-file `sha256` dict shape).
**Apply to:** `evidence/manifest.json`, and each `diagNN/*.json` output's own embedded provenance fields (per
RESEARCH.md's Pattern 1 — each script records the SHA-256/commit of what it read, not just the shared
manifest).

### JSON output idiom
**Source:** `calculate_metrics.py:504-505` (`json.dump(metrics, f, indent=2, default=str)`) and
`pinn/verify.py:464` (`json.dumps(payload, indent=2) + "\n"`).
**Apply to:** all `diagNN/*.json` outputs and `evidence/manifest.json` — always `indent=2`, always a trailing
newline if writing via `atomic_write_text`-style helpers (none exists for this phase's scripts; plain `open(...,
'w')` + `json.dump` matches the `calculate_metrics.py` precedent and is sufficient for D-03's "plain Python,
no new dependencies").

### Fail-closed self-check assertions
**Source:** `gate_metrics.py:225-239` ("never silently computed from only the finite subset") +
`calculate_metrics.py:496-514` ("always returns a dict... with an error key", never a silent omission) +
RESEARCH.md's own assertion list (`assert len(per_trajectory) == 1500`, etc.).
**Apply to:** all three DIAG-01/02/03 scripts, before any output is written (D-02's re-derivability
mechanism).

### Verified-fact vs. agent-hypothesis separation, with explicit citations
**Source:** `43-VERDICT.md`'s evidence-matrix table (`Evidence | Observed result | Grounding`) and
`43-CALIBRATION.md`'s "Confidence" section (label + explicit per-field limits).
**Apply to:** `44-DIAGNOSIS.md` in full — every DIAG-04 hypothesis row needs a `Grounding`-style citation
column, and every ranked cause needs its own confidence/limits language, not a single blanket confidence
label for the whole report.

### Gap-register field schema (STOP protocol)
**Source:** `43-GAPS.md` (`GAP-43-01`, full 11-field record) — this is the CLAUDE.md STOP-protocol schema
already instantiated.
**Apply to:** `44-GAPS.md`'s `GAP-44-01` entry and its mirrored row/prose in `v2.1-GAPS.md`.

## No Analog Found

Files/conventions with no close existing match — the executor is establishing a new convention here, not
following one:

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| `evidence/manifest.json` (as a **standalone** file combining SHA-256-per-input + commit-hash) | config / pinning record | write-once | The repo has two half-precedents that Phase 44 must combine for the first time: (a) Phase 43's `evidence/pilot/README.md` embeds a `sha256` dict **inline inside a markdown fenced block**, with no commit-hash field at all; (b) `.planning/milestones/v1.5-phases/24-.../24-DATA05-RERUN-MANIFEST.json` is a genuine **standalone** `.json` file at a phase root, but records command/timing/status per-ID, not SHA-256 hashes or a commit hash. No file in this repo is simultaneously standalone-JSON **and** SHA-256+commit-hash-shaped — assemble it from `pinn/verify.py::git_head()` (commit-hash mechanics) + Phase 43's `sha256` dict shape (per-file hash mechanics), as detailed in the Pattern Assignment above, rather than searching for a closer match. |

One additional note, not a file-pattern gap but relevant to how DIAG-01's script should be written: the D-07
question (whether `max` is the spec-intended gate statistic) has **no code or spec analog to resolve it** —
`gate_metrics.py::aggregate_test_eps_h`'s "worst-trajectory (maximum)" choice is Phase-43-local, not
spec-derived (RESEARCH.md §C). This is not a pattern the executor should copy as authoritative; it is the
exact fact pattern that routes to `44-GAPS.md` under D-07.

## Metadata

**Analog search scope:** `simulation_data/Scripts/metrics_calculation/`, `simulation_data/Validation/
prescreening/`, `pinn/verification/`, `pinn/verify.py`, `pinn/training/`, `.planning/milestones/v2.0-phases/
43-verification-stage-0-pilot-acceptance/` (full phase directory + `evidence/`), `.planning/milestones/
v2.0-GAPS.md`, `.planning/milestones/v1.5-phases/24-.../24-DATA05-RERUN-MANIFEST.json`, and a repo-wide
`find`/`grep` for `*GAPS.md` and `*manifest*`.
**Files scanned:** ~20 (directory listings) + 10 read in full or by targeted range.
**Pattern extraction date:** 2026-07-23
