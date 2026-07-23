# Phase 43: Verification, Stage-0 Pilot & Acceptance - Pattern Map

**Mapped:** 2026-07-20
**Files analyzed:** 8 (2 new modules, 2 modified modules, 4 reused-as-library groups, 1 test package, 1 verdict artifact)
**Analogs found:** 7 / 9 (2 items — the ε_H/SCS metric formula and the go/adjust/rethink verdict artifact — have only partial/structural analogs; see "No Analog Found")

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pinn/verify.py` (CREATE) | controller / CLI composition-root | request-response (orchestrates library calls, aggregates, gates) | `pinn/train.py` (CLI shape) + `pinn/training/slbfgs_preflight.py` (typed-refusal gate shape) | role-match (composition root) + exact (gate idiom) |
| `pinn/evaluate.py` (CREATE) | controller / CLI composition-root | batch (single no-grad forward pass → file I/O) | `pinn/train.py` (CLI/run-dir shape) + `pinn/verification/residual_probe.py` (single-pass evidence-dict + `main()` shape) | role-match |
| `pinn/train.py` (MODIFY — add >30-min preflight gate) | controller | request-response | `pinn/training/slbfgs_preflight.py` (`check_stage_preflight`/`StochasticLBFGSNotImplemented`) called from `pinn/train.py::main()` itself (self-analog, extend in place) | exact |
| `pinn/training/summary.py` (MODIFY — enrich in place) | service (pure render + atomic write) | transform (render-don't-recompute) | itself — `stub_summary` / `finalize_summary` / `_compose` / `_render_md` (self-analog, extend in place) | exact |
| `pinn/verification/{componentwise_ad,gradcheck_probe,residual_probe,overfit_probe}.py` (CALL, no modify) | service / probe library | batch (one measurement → structured dict) | n/a — these ARE the analog set for `verify.py`'s per-rung calls | exact |
| `pinn/training/controllers.py::RunController` / `pinn/training/stage_exit.py::StageExitMachine` (REUSE, no modify) | service | event-driven (EMA update per step) / transform (threshold evaluation) | n/a — direct reuse; consumed by `verify.py` (forecast) and referenced by the calibration note (R-1/R-2) | exact |
| `pinn/data-handling/processing/invariants.py` / `pinn/physics_residual.py` (REUSE, no modify) | service / physics kernel | transform | n/a — direct reuse for `evaluate.py`'s metric machinery; see "No Analog Found" for the ε_H/SCS formula gap | partial (machinery present, ε_H/SCS formula not yet coded anywhere) |
| `tests/phase43/*.py` (CREATE) | test | request-response (subprocess) / transform (pure-function) | `tests/phase42/` (`_fixtures.py`, `test_honesty_layer.py`) + `tests/phase41/test_prohibitions.py` (negative-test idiom) + `tests/phase41/test_train_entrypoint.py` (`_require` skip guard) | exact |
| `43-VERDICT.md` (CREATE, phase dir) | artifact / governance doc | transform (evidence → rendered verdict) | `.planning/phases/42-*/42-09-SUMMARY.md` (coverage-table idiom) + `.planning/milestones/v1.4-phases/21-*/21-CODE-DIVERGENCE.md` (shipped/implication/priority table idiom) | partial (no prior go/adjust/rethink artifact exists in this repo) |

## Pattern Assignments

### `pinn/verify.py` (CREATE — controller, request-response orchestrator)

**Analog 1 (CLI composition-root shape):** `pinn/train.py`

**Imports pattern** (`pinn/train.py:1-22`, `12-22` are the load-bearing lines):
```python
from __future__ import annotations

import argparse
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Sequence

import numpy as np
```
`verify.py` should mirror the `argparse.ArgumentParser(prog="python -m pinn.verify")` shape (`pinn/train.py:73-87`, `_parser()`) — a single top-level parser, no subcommands, matching `python -m pinn.train`'s `prog=` convention.

**CLI entry / exit-code pattern** (`pinn/train.py:257-259, 676-677`):
```python
def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI entry — returns process exit code (0 success, non-zero refuse/error)."""
    args = _parser().parse_args(list(argv) if argv is not None else None)
    ...

if __name__ == "__main__":
    sys.exit(main())
```

**Analog 2 (typed-refusal gate — the exact pattern for "exits non-zero naming the first failing rung"):** `pinn/training/slbfgs_preflight.py` (full file, 50 lines)
```python
class StochasticLBFGSNotImplemented(Exception):
    """Typed refusal: ... Carries the refused ``stage`` so the caller can
    report which curriculum stage triggered the gate ..."""

    def __init__(self, stage: int) -> None:
        self.stage = stage
        super().__init__(
            f"stage {stage} requires stochastic L-BFGS (stages 3-6), which has "
            f"no implementation in this build (deferred PLAT-02); refusing "
            f"rather than silently deviating from the spec"
        )


def check_stage_preflight(stage: int) -> None:
    """... stages >= 3: raises ``StochasticLBFGSNotImplemented`` (typed stop,
    never a silent skip)."""
    if stage >= 3:
        raise StochasticLBFGSNotImplemented(stage)
```
Copy the shape, not the content: `verify.py`'s ladder should carry a small ordered list of `(rung_name, callable)` pairs, run each in order, catch exceptions as a FAIL record (never let an exception propagate past a rung — the residual/gradcheck probes already return `{"passed": bool, "reason": ..., "exception": ...}` dicts rather than raising on measured failure; a missing/broken probe import should be caught and converted to the same FAIL shape, matching CTX-70's "a missing/broken probe counts as that rung's FAIL, never a silent skip").

**Library-call pattern (each rung is a plain function call, not a subprocess):** the four probe modules already expose `run_*` functions returning JSON-serializable dicts with a `"passed"` key — call these directly, do not shell out. Signatures (verbatim):
```python
# pinn/verification/componentwise_ad.py:302
def run_probe_arm(precision, device, patterns=_PATTERN_IDS, protocol=None, u=0.3) -> dict: ...
# returns {"profile", "precision", ..., "patterns": {...}, "exception": None|dict}
# NOTE: no top-level "passed" key — verify.py must derive PASS from
# per-pattern correctness fields inside patterns[...] (or exception is None).

# pinn/verification/gradcheck_probe.py:91
def run_gradcheck(precision, device) -> dict: ...
# returns {"passed": bool, "reason": Optional[str], "runtime": RuntimeSpec, "exception": Optional[dict]}

# pinn/verification/residual_probe.py:179  (__all__ = ["main", "run_residual_on_ground_truth"])
def run_residual_on_ground_truth(precision, device, *, path=None, variant=None, id=None,
                                  residual_threshold=..., newtonian_residual_threshold=...,
                                  min_separation_guard=...) -> dict: ...
# returns {..., "gate_a": {...}, "gate_b": {...}, "passed": bool}

# pinn/verification/overfit_probe.py:288  (__all__ = ["main", "run_overfit"])
def run_overfit(precision, device, *, path=None, variant=None, id=None,
                 max_steps=..., lr=..., eps_h=None, com_offset_warn_threshold=...) -> dict: ...
# returns {..., "passed": bool, "fail_reason": Optional[str], ...}
```
`componentwise_ad.run_probe_arm` is the one outlier without a top-level `"passed"` — `verify.py` must define PASS for that rung from the per-pattern correctness records (or reuse `main()`'s own exit-code logic if it computes one; check `componentwise_ad.py:371-394` `main()` before assuming — `main()` there always returns 0, so `verify.py` cannot delegate to it for the pass/fail signal and must inspect the `patterns` dict directly).

**Device-sanity rung (rung 1) — NO existing analog; must be written fresh.** `pinn/runtime.py:1-16` explicitly documents that `resolve_runtime` "does NOT inspect availability, infer a device, catch/retry on CPU" — by design (CTX-12..14). The only existing `torch.backends.mps` reference in production code is informational (`componentwise_ad.py:352`, `mps_is_built()` inside an evidence dict, not a gate). `verify.py`'s device-sanity rung is genuinely new: call `torch.backends.mps.is_available()` directly and pair it with `pinn.runtime.resolve_runtime(precision, device)` for the D1-p-resolved dtype, per CTX-70. Do not add availability-inference to `resolve_runtime` itself — keep the new check local to `verify.py`.

**Error handling / exit-code pattern:** each probe's own `main()` (e.g. `gradcheck_probe.py:186`, `residual_probe.py:324`, `overfit_probe.py` similarly) returns `0 if passed else 1` — mirror this at the ladder level: print one `PASS`/`FAIL` line per rung (reuse the probes' own print-line phrasing style, e.g. `residual_probe.py:313-322`), then print an overall verdict line and `return 0` only if every rung passed, else `return 1` and name the first failing rung in the final message (CTX-70).

---

### `pinn/evaluate.py` (CREATE — controller, batch single-pass)

**Analog 1 (CLI + run-dir shape):** `pinn/train.py`
- Reuse the `runs/`-rooted, path-traversal-guarded directory resolution idiom at `pinn/train.py:97-113` (`_resolve_run_dir`) for the `--output <dir>` argument (adapted: `evaluate.py`'s output dir is caller-supplied, not derived from a config run-name, but the same `.resolve()` + `is_relative_to()` traversal guard applies if `--output` is expected to nest under `runs/<name>/`).
- Reuse the checkpoint-loading half of the resume path at `pinn/train.py:594-620` (load payload → `_restore_run_controller`/`load_state_dict`), simplified: `evaluate.py` only needs `build_network(...)` + `model.load_state_dict(payload["model"])`, not a full `RunController`.

**Analog 2 (checkpoint load, weights_only=True — mandatory project-wide invariant):** `pinn/training/checkpoint.py:444-480` (`TorchSaveCheckpointStore.load_checkpoint`)
```python
try:
    payload = torch.load(resolved, weights_only=True)
except Exception as exc:
    raise NoValidCheckpointError(path) from exc
```
`tests/phase41/test_prohibitions.py:59-91` locks this invariant repo-wide via an AST audit counting `torch.load` vs `weights_only=True` occurrences — any new `torch.load` call in `evaluate.py` MUST pass `weights_only=True` or that test's count assertion breaks (the audit currently scopes `pinn.training.checkpoint`, but the pattern is the one to copy regardless of whether the audit is later widened).

**Analog 3 (single-pass evidence-dict + `main()` shape, no-grad forward):** `pinn/verification/residual_probe.py:179-239` (`run_residual_on_ground_truth`) — same shape as `evaluate.py` needs: resolve runtime → load fixture(s) → compute → return one JSON-serializable dict with a `"passed"`/gate summary at the end. `overfit_probe.py:288-407` (`run_overfit`) shows the analogous pattern for a full test-set-shaped loop (though overfit trains; evaluate does not — model should be `.eval()` + `torch.no_grad()`, not `.train()` + optimizer step, mirroring `overfit_probe.py:338` `model.eval()` for its diagnostic-only passes, not its `.train()` optimization block).

**Output layout (`metrics.json` + `metrics.md`):** No existing dual-JSON+Markdown-with-atomic-write analog other than `pinn/training/summary.py` (see below) and the probes' own `_write_evidence` (`residual_probe.py:77-96`, `gradcheck_probe.py:75-88`, `overfit_probe.py` similarly) — all three probes share this idiom:
```python
def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + f".tmp.{_os.getpid()}")
    with open(temporary, "w", encoding="utf-8") as handle:
        handle.write(content)
        handle.flush()
        _os.fsync(handle.fileno())
    _os.replace(temporary, path)
```
Prefer `pinn.training.atomic_io.atomic_write_text` (already used by `summary.py:43`) over re-deriving `_atomic_write` — it is the canonical project-wide atomic writer; the probes' local `_atomic_write` predates it and is evidence-directory-scoped, not the one to copy for `evaluate.py`'s `runs/`-adjacent output.

**Gate render — CTX-75 direction is AUTHORITATIVE, the design doc is backwards:**
```
REJECT if ε_H > 1e-5   (smaller passes; boundary ε_H == 1e-5 → PASS)
PASS if SCS > -5        (boundary SCS == -5 → FAIL)
OVERALL FAIL iff ε_H > 1e-5 OR SCS <= -5
```
No code renders this yet anywhere in `pinn/` — build fresh, do not copy the design-doc §6.3 example (SPEC Prohibition #1, `ctl_instruction.md` authoritative per CTX-75).

**matplotlib-optional guard (CTX-77) — Phase 42 no-matplotlib rule.** Grep `tests/phase42/test_residual_panel.py:46-53` for the established try/except-ImportError + `unittest.skipUnless` idiom used when a component optionally depends on a plotting/visualization library; apply the same style to `evaluate.py`'s `plots/` best-effort output (wrap the plotting import in `try/except ImportError`, skip cleanly, never let a missing matplotlib break `metrics.json`/`metrics.md`).

---

### `pinn/train.py` (MODIFY — add the >30-min launch preflight gate, CTX-71)

**Where to add it:** between the existing run-folder resolution (`pinn/train.py:290-309`, after `run_dir.mkdir(...)`) and the freeze-config step (`pinn/train.py:387-395`) — i.e., before any expensive state is built, matching the existing fail-closed-before-construction discipline already used for `--resume`/`--hold-stage` validation at `pinn/train.py:261-282` ("Fail-closed CLI validation BEFORE construction").

**Pattern to copy (typed refusal, matches `check_stage_preflight`):**
```python
# pinn/train.py:271-282 (existing analog inside this same file)
if args.hold_stage:
    if args.resume is None:
        print(
            "error: --hold-stage requires --resume <stage-{{N}}-final.pt>",
            file=sys.stderr,
        )
        return 1
    try:
        validate_hold_stage_target(args.resume)
    except HoldStageTargetError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
```
The new >30-min gate follows the same `print(f"error: ...", file=sys.stderr); return 1` idiom, reading a fresh green `verify` marker written by `pinn/verify.py` (marker path/freshness window is a research/plan detail per CTX-71 — not pinned here).

**Forecast source (CTX-73):** `pinn/train.py` does not currently compute a forecast; `RunController._s_per_step_ema` (`pinn/training/controllers.py:356, 676-681`) is the EMA to read. The forecast math (`measured s/step × full-Stage-0 step estimate`) is new logic — no existing analog computes a duration forecast anywhere in `pinn/`.

---

### `pinn/training/summary.py` (MODIFY — enrich in place, CTX-78)

**Preserve exactly (do not alter):** the stub-then-finalize pair `stub_summary`/`finalize_summary` (`summary.py:232-289`), the render-don't-recompute discipline (`_render_curriculum`, `summary.py:120-146`, reads `curriculum.jsonl` line-by-line, never recomputes), and must-NOT #1 via `_null_if_nonfinite` (`summary.py:65-75`) + the failed/interrupted early-return template in `_render_md` (`summary.py:194-198`):
```python
lines: List[str] = ["# Run Summary", "", f"**Status:** {status_text}", ""]
if disposition != "finished":
    # Honest non-success template: state named, no fabricated metrics (must-NOT #1).
    lines.append("The run did not complete.")
    lines.append("")
```

**Section-writing structure to extend (`_render_md`, `summary.py:186-229`):** the file builds `lines: List[str]` and appends `## <Section>` blocks in sequence (`## Run header`, `## Final losses`, `## Curriculum progression`). Add the three new sections (`## Validation summary`, `## Test-set preview`, `## Comparison hint`) as additional blocks in this same `lines.append(...)` sequence, following the exact same style as the existing `## Final losses` block (`summary.py:209-214`):
```python
lines.append("## Final losses")
lines.append("")
for term in _LOSS_TERMS:
    value = losses.get(term)
    lines.append(f"- {term}: {value if value is not None else 'null'}")
lines.append("")
```
The `_compose()` function (`summary.py:154-183`) builds the `payload` dict that both `_render_md` and `summary.json` consume from one source of truth — new fields (validation summary, test-set preview, comparison hint) must be threaded through `_compose()`'s `payload` dict the same way `final_losses`/`curriculum` already are, so `summary.json` and `summary.md` stay in sync (never compute a field only for the Markdown render).

**Honesty-layer statements (CTX-78):** append the three §6.4 sentences as a final `## Honesty notes` (or similar) block using the same flat `lines.append(f"- ...")` bullet style as `## Final losses` — these are static strings, not derived from data, so no new computation is needed, only a fixed textual block.

**New inputs `finalize_summary` needs (signature extension):** currently `finalize_summary(run_dir, *, disposition, header, final_losses, curriculum_path)` (`summary.py:257-264`) — CTX-78's validation summary / test-set preview / comparison hint each need a new keyword-only parameter (e.g. `validation_records`, `evaluate_output_dir`, `compare_run_name`) following the existing `Optional[...] = None`-with-graceful-degradation style already used for `curriculum_path` (`_render_curriculum` returns `[]` on `None`/missing file, `summary.py:126-130`) — apply the same "missing input → empty/omitted section, never an error" discipline.

---

### `tests/phase43/*.py` (CREATE)

**Package analog:** `tests/phase42/` (directory listing: `__init__.py`, `_fixtures.py`, `test_honesty_layer.py`, `test_redaction.py`, `test_residual_panel.py`, `test_runbook_config.py`, `test_runs_contract.py`, `test_signals.py`, `test_status_heartbeat.py`, `test_step_log_jsonl.py`, `test_wrapper_exit.py`).

**Deferred-import skip guard (copy verbatim, adapt module name):** `tests/phase41/test_train_entrypoint.py:27-34` (identical helper repeated in `test_prohibitions.py:18-26`, `test_guards.py`, `test_resume.py`, `test_determinism.py`, `test_step_log_jsonl.py`):
```python
def _require(symbol, module=TRAIN_MODULE):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)
```
`_SKIP_PHRASE` is imported from the package `__init__.py` (`tests/phase41/__init__.py:12`, `tests/phase42/__init__.py:12`) — `tests/phase43/__init__.py` should carry the same constant/docstring convention.

**Subprocess harness to reuse/extend (not duplicate):** `tests/phase42/_fixtures.py` — re-exports phase40/41 fixtures rather than rebuilding them (`_fixtures.py:40-50`); `tests/phase43/_fixtures.py` should do the same (`from tests.phase42._fixtures import launch_train, write_train_config, wait_for_status, ...`), adding only Phase-43-specific helpers (e.g. a smoke-config writer with `checkpoint_every=100`/`~300 steps`, a pilot-seed launcher). Conda env python path convention (`_fixtures.py:66-70`):
```python
_CONDA_PYTHON = os.path.expanduser("~/miniforge3/envs/pinn-train/bin/python")
```

**Negative-test idiom for the 3 prohibitions (CTX-83):** `tests/phase41/test_prohibitions.py` (full file) is the exact template — one `unittest.TestCase` per prohibition, each test asserting the FORBIDDEN behavior does NOT occur (e.g. AST/string audits for the weights_only invariant, `40-98` structural asserts). Apply the same shape to:
1. gate-direction prohibition — boundary unit test with `ε_H`/`SCS` just above/below the threshold, asserting the CTX-75 direction (not the design-doc's inverted one).
2. metric-fabrication-on-failure prohibition — mirror `tests/phase42/test_honesty_layer.py` almost directly (it already asserts `final_losses.get(term)` is `None` for every term on a forced-failure run; the Phase 43 version does the equivalent for `evaluate.py`'s `metrics.json` / `summary.py`'s new sections on a failed/interrupted run).
3. >30-min gate prohibition — a launch-path test asserting a run with a forecast strictly above 30 min is refused (exit code 1, stderr names the gate) unless a fresh green `verify` marker exists; boundary case `== 30 min` allowed. Model the subprocess-driven shape on `test_honesty_layer.py`'s `_launch` / `wait_for_status` / `_wait_for_failure_artifact` barrier-polling idiom (`test_honesty_layer.py:111-167`).

---

### `43-VERDICT.md` (CREATE — phase-dir governance artifact)

**No prior go/adjust/rethink artifact exists anywhere under `.planning/`** (searched `.planning` and `.planning/milestones` for `*VERDICT*`, `*SUMMARY*` — only per-plan `NN-SUMMARY.md` execution summaries exist, e.g. `.planning/phases/42-operator-runbook-surface-monitoring/42-09-SUMMARY.md`). Two structurally-adjacent idioms to borrow FORM from (not content):

**Idiom 1 — coverage table with pass/fail + verification kind** (`42-09-SUMMARY.md:42-58`, `coverage:` YAML block):
```yaml
coverage:
  - id: E2-sigint-once
    description: SIGINT once → checkpoint written + exit 130 + state=interrupted.
    requirement: OPS-02
    verification:
      - kind: subprocess
        ref: test_sigint_once_checkpoints_and_exits_130
        status: pass
    human_judgment: false
```
`43-VERDICT.md` should cite evidence the same way: gate result / seed-band / measured s/step / open seams, each tied to a concrete test or artifact reference, not an unsupported assertion (SPEC AC 15, Prohibition "MUST NOT claim the model works... on validation loss alone").

**Idiom 2 — shipped/implication/priority table for the forward hand-off** (`.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/21-CODE-DIVERGENCE.md`, full file, 20 lines):
```markdown
| Spec target validated by probe | FUT-01 implication | FUT-01 priority |
|---|---|---|
| ... | ... | HIGH |
```
CTX-81's FUT-01/FUT-04 handoff update (shipped / placeholder-seam / deferred PLAT-01..07, reflecting GAP-38-01's disposition) maps onto this table shape almost directly: `column 1 = what` / `column 2 = shipped|placeholder-seam|deferred` / `column 3 = FUT-01/FUT-04 priority or PLAT-NN id`.

**Owner-ratification pause protocol has no code analog** — CTX-82's four pause points (B-5, D4-a, R-1/R-2, ACC-06 verdict) are a workflow discipline, not a mechanical pattern; `verification: judgment` in the coverage-table idiom above (Idiom 1) is the closest structural marker for "this line item requires a human, not a test."

---

## Shared Patterns

### CLI composition-root convention
**Source:** `pinn/train.py` (`_parser()` + `main(argv=None) -> int` + `if __name__ == "__main__": sys.exit(main())`)
**Apply to:** `pinn/verify.py`, `pinn/evaluate.py`
```python
def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m pinn.<cmd>")
    ...
    return parser

def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parser().parse_args(list(argv) if argv is not None else None)
    ...
    return 0  # or non-zero

if __name__ == "__main__":
    sys.exit(main())
```

### Typed-refusal / fail-closed gate
**Source:** `pinn/training/slbfgs_preflight.py` (whole file) + `pinn/train.py:261-282` (fail-closed-before-construction CLI validation)
**Apply to:** `pinn/verify.py` ladder rungs, `pinn/train.py`'s new >30-min gate
```python
try:
    <check>
except <TypedError> as exc:
    print(f"error: {exc}", file=sys.stderr)
    return 1
```

### Atomic write (canonical — use this, not the probes' local `_atomic_write`)
**Source:** `pinn/training/atomic_io.atomic_write_text` (imported by `summary.py:43`)
**Apply to:** `pinn/evaluate.py`'s `metrics.json`/`metrics.md`, any `pinn/verify.py` marker file
```python
from pinn.training.atomic_io import atomic_write_text
atomic_write_text(path, content)
```

### `weights_only=True` on every `torch.load`
**Source:** `pinn/training/checkpoint.py:474` + enforced by `tests/phase41/test_prohibitions.py:59-91` (AST audit)
**Apply to:** `pinn/evaluate.py`'s checkpoint load
```python
payload = torch.load(resolved, weights_only=True)
```

### Honesty / null-metric-on-non-success
**Source:** `pinn/training/summary.py:65-75` (`_null_if_nonfinite`) + `:194-198` (non-success early template) + `tests/phase42/test_honesty_layer.py` (the enforcing test)
**Apply to:** `pinn/training/summary.py` enrichment, `pinn/evaluate.py`'s NaN/Inf → honest FAIL (not crash) on `metrics.json`/`metrics.md`

### Deferred-import test skip guard
**Source:** `tests/phase41/test_train_entrypoint.py:27-34` (repeated across `tests/phase41/`, `tests/phase42/`)
**Apply to:** every new file in `tests/phase43/`
```python
def _require(symbol, module=MODULE):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)
```

### `runs/`-rooted path-traversal guard
**Source:** `pinn/train.py:97-113` (`_resolve_run_dir`)
**Apply to:** `pinn/evaluate.py --output <dir>` if the output dir is expected to nest under `runs/`

### Config field docstrings already point at Phase 43 as the calibration site
**Source:** `pinn/training/config.py:189-191` (`GuardConfig` — "⚖ PROVISIONAL R-1 guard threshold (owner-calibrate-at-Phase-43-pilot)") and `:243-246` (`CheckpointCadence.wall_clock_ceiling_s` — "⚖ PROVISIONAL D4-a wall-clock ceiling (owner-ratify-before-run-#1)")
**Apply to:** the calibration note / `43-VERDICT.md` — these are the exact config fields the pilot's derived R-1/R-2 and D4-a candidates should be written back into (post owner-ratification); `RunController` constructs `StageExitMachine` and guard checks directly from these `TrainingConfig` fields (`pinn/train.py:444, 455`), so no new plumbing is needed once the owner ratifies new values — only the YAML defaults change.

## No Analog Found

Files/items with no close code match in the codebase (planner should treat as research/first-principles work grounded in `ctl_instruction.md` / `data_quality_assessment.md` per CTX-76, not invented):

| Item | Role | Data Flow | Reason |
|---|---|---|---|
| ε_H / SCS metric computation from model predictions | transform (physics kernel) | No code anywhere in `pinn/` computes SCS (`grep -rn "SCS" pinn/` returns zero hits); `eps_h` exists only as a diagnostic *parameter* threaded through `overfit_probe.py::_evaluate_diagnostics` (`overfit_probe.py:195-260`, feeding `soft_energy_loss`), not as the ε_H *metric definition* itself. `pinn/data-handling/processing/invariants.py::compute_basic_invariants` computes `E` (raw energy) from IC arrays (numpy, not a model-prediction consumer) — a partial machinery analog, not a formula analog. CTX-76 explicitly reserves the precise formula as a research/plan pin, not something to invent in pattern-mapping. |
| `43-VERDICT.md` go/adjust/rethink content structure | artifact | No prior verdict artifact exists in `.planning/`; nearest structural relatives (`NN-SUMMARY.md` coverage tables, `NN-CODE-DIVERGENCE.md` shipped/implication tables) are cited above as FORM analogs only. |
| Device-sanity rung (`torch.backends.mps.is_available()` as a gate) | transform (boolean check) | `pinn/runtime.py` deliberately does NOT probe availability (CTX-12..14 contract); the only prior `mps.is_built()` reference is informational, inside an evidence dict, never a pass/fail gate. |

## Metadata

**Analog search scope:** `pinn/`, `pinn/training/`, `pinn/verification/`, `pinn/data-handling/processing/`, `tests/phase40/`, `tests/phase41/`, `tests/phase42/`, `.planning/phases/42-*/`, `.planning/milestones/v1.4-phases/21-*/`
**Files scanned:** `pinn/train.py` (677 lines, full read), `pinn/training/summary.py` (289 lines, full read), `pinn/training/stage_exit.py` (231 lines, full read), `pinn/training/slbfgs_preflight.py` (50 lines, full read), `pinn/verification/{componentwise_ad,gradcheck_probe,residual_probe,overfit_probe,fixture_loader}.py` (targeted reads of `run_*`/`main()` sections), `pinn/training/controllers.py` (targeted read of `_s_per_step_ema`/`_log_step`, lines 600-740), `pinn/training/checkpoint.py` (targeted read of `load_checkpoint`), `pinn/training/config.py` (targeted grep + read of `GuardConfig`/`CheckpointCadence`), `pinn/runtime.py` (targeted read), `pinn/data-handling/processing/invariants.py` (partial read), `tests/phase42/_fixtures.py` (full read), `tests/phase42/test_honesty_layer.py` (full read), `tests/phase41/test_prohibitions.py` (full read), `tests/phase41/test_train_entrypoint.py` (partial read), `.planning/phases/42-operator-runbook-surface-monitoring/42-09-SUMMARY.md` (partial read), `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/21-CODE-DIVERGENCE.md` (full read)
**Pattern extraction date:** 2026-07-20

---

*Phase: 43-verification-stage-0-pilot-acceptance*
*Patterns mapped: 2026-07-20*
