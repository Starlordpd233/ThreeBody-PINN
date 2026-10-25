# Phase 64: Feasibility Verdict - Pattern Map

**Mapped:** 2026-10-25
**Mapped against:** HEAD `377faebc` on `milestone/v2.4` (worktree `.worktrees/trainex`). Every line number below was read at this HEAD in this session; no range was read twice. Commit `00f7f1bc` (the Phase 60 close) is cited by hunk, not by line.
**Files analyzed:** 19 rows (13 new, 6 edited)
**Analogs found:** 17 / 19 at file level (10 exact, 6 role-match, 1 partial). Two rows have no repository analog (the SVG figure and the `PROJECT.md` rewrite); four further sub-parts have none (listed under "No Analog Found").

Tracked-source gate (#3645): every analog path named in this file was checked with `git ls-files -- <path>` and printed non-empty, so each is tracked source. No `.gsd/` capability mirror, no `runs/` path, no `.planning/tmp/` path and no untracked scratch file is named. All planned Phase 64 output paths were also checked with `git check-ignore`: none is ignored, and none has a `runs`, `tmp`, `scratch` or `outputs` segment (`scripts/git_policy/validate_staged_paths.py:11-27`).

Abbreviations used throughout (all repo-relative):

- `P59` = `.planning/phases/59-read-only-baseline-scorecard/evidence`
- `P60` = `.planning/phases/60-single-system-learnability/evidence`
- `E64` = `.planning/phases/64-feasibility-verdict/evidence` (the directory this phase creates)
- `PY` = the `pinn-train` interpreter named in `64-VALIDATION.md` (not repeated here, so no host path lands in this file)

## How to use this map

1. Read "Hazards and corrections for the planner" first. Items H1 to H4 change what a plan may touch or scan; H5 is a stale-copy trap in `64-RESEARCH.md`.
2. "File Classification" gives the closest analog per file and the suggested plan (RESEARCH "Suggested plan decomposition"; the planner may merge or split). "Pattern Assignments" says, per file, what to copy, what not to copy, and which test pattern proves it.
3. Row 1 (the verifier) and row 10 (its tests) carry the large excerpts. Other rows point back to them instead of repeating.
4. Code that has no repository analog (the time-constant derivation, the SVG writer, the Mac-only wording guard, the VER-22 counter) is in `64-RESEARCH.md` "Code Examples" 1 to 6. Those are not repeated here because they are not repository code. They have been smoke-run read-only by the researcher.
5. Tests are `unittest.TestCase` only (`pytest` is not installed in `pinn-train`).
6. Content decisions (the Stage-0 bar, the budget, the stop-rule margin, the `10^-5` bar) are owner decisions. This map gives the layout to copy, never the content. Where the sources are silent the page records "open".

## File Classification

| # | New/Modified File | Role | Data Flow | Closest Analog | Match | Suggested plan |
|---|-------------------|------|-----------|----------------|-------|----------------|
| 1 | `E64/verify_phase64_verdict.py` | verifier CLI (modes: inputs, numbers, derive, figure, rules, frozen, charter, ruling, traceability, final) | batch, read-only (git subprocess; torch only in `derive`/`figure`) | `P60/verify_phase60_evidence.py` + `P59/verify_phase59_evidence.py` | exact | 64-01 skeleton and committed-JSON modes; 64-02 `derive`, `figure`; 64-04 `charter`; 64-05 `ruling`; 64-06 `traceability`, `final` |
| 2 | `E64/build_phase64_evidence.py` | producer (writes `numbers.json`, the SVG, the provenance JSON) | transform + file-I/O (reads train-split records through the allowlist seam, writes canonical JSON) | `pinn/verification/baselines.py::_full_mode` + `pinn/verification/evidence_io.py` + `P60/verify_phase60_evidence.py::cmd_rescore` (load path) | role-match | 64-02 |
| 3 | `E64/numbers.json` | number manifest (id, value, source file and key, derivation) | file-I/O | `P59/baselines/baselines.json` (+ `P60/g2/stop-handoff.json` `basis` entries) | role-match | 64-02 |
| 4 | `E64/figure-1632.svg` | figure (system 1632 orbit beside the network's prediction) | transform | none in repo | none | 64-02 |
| 5 | `E64/figure-1632.provenance.json` | provenance record (input paths with SHA-256, figure SHA-256, versions) | file-I/O | `P59/baselines/provenance.json` + `evidence_io.provenance_record`; `P60/g2/stop-handoff.json` `basis` | role-match | 64-02 |
| 6 | `.planning/phases/64-feasibility-verdict/64-VERDICT.md` | owner-facing verdict document | docs | `.planning/phases/58-verdict-traceability-close/58-VERDICT.md` + `60-FINDINGS.md` + v2.0 `43-VERDICT.md` | exact (structure); the D-01 box and the cost section are new content | 64-03 |
| 7 | `.planning/phases/64-feasibility-verdict/64-CHARTER.md` | owner decision page (one page plus appendices) | docs | partial: the v2.3 verdict packet section 1 (framing), `59-GAPS.md` GAP-59-08 and `64-GAPS.md` GAP-64-01 (option layout) | partial | 64-04 |
| 8 | `.planning/phases/64-feasibility-verdict/64-CHECKPOINT-1-RULING.md` | owner ruling record (written only after the owner answers) | file-I/O | `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-RULING.md` + `60-17-PLAN.md` Task 3 + `pinn/verification/learnability_ruling.py` | role-match (format fixed by code and tests; no committed instance of an `owner-quote` ruling exists) | 64-05 |
| 9 | `tests/phase64/__init__.py` | test scaffold | none | `tests/phase60/__init__.py` | exact | 64-01 |
| 10 | `tests/phase64/test_verifier_phase64.py` | test (unit on synthetic git repos + real-worktree smoke + real-shape fixtures) | batch | `tests/phase60/test_verifier_phase60.py` + `tests/phase59/test_evidence_verifier.py` + `tests/phase60/test_ruling.py` | exact | 64-01 to 64-06 |
| 11 | frozen-path list for `frozen` mode (33 pinned + 8 sealed) | config (derived, or a small committed list) | file-I/O | `P60/run-protocol.json` `module_sha256` keys + `P59/scorecard-freeze.json` | role-match | 64-01 |
| 12 | `64-01-PLAN.md` to `64-06-PLAN.md` | GSD execution plans | docs | `60-17-PLAN.md` (checkpoint), `60-22-PLAN.md` (closeout), `60-13-PLAN.md` (verifier tracer) | exact | planner |
| 13 | `64-VALIDATION.md` (EDIT: bind rows to task ids) | validation contract | docs | `59-VALIDATION.md` | exact | planner |
| 14 | `.planning/REQUIREMENTS.md` (EDIT) | registry | docs | commit `00f7f1bc` | exact | 64-06 |
| 15 | `.planning/ROADMAP.md` (EDIT) | registry | docs | commit `00f7f1bc` | exact | 64-06 |
| 16 | `.planning/STATE.md` (EDIT) | registry | docs | commit `00f7f1bc` | exact | 64-06 |
| 17 | `.planning/PROJECT.md` (EDIT: "What This Is", Core Value; optional title line and Model constraint) | registry | docs | none (the section was never rewritten since `f4243afd`); commit `b10fb698` for commit-body style only | none | 64-06, on the owner's approval only |
| 18 | `64-GAPS.md` (GAP-64-01 status) + `.planning/milestones/v2.4-GAPS.md` (row `:41`, disposition `:61`) | gap registers | docs | `.planning/milestones/v2.4-GAPS.md:28-40` (RESOLVED-WITH-INSTRUCTION rows) | exact | 64-06, after the owner answers |
| 19 | `64-01-SUMMARY.md` to `64-06-SUMMARY.md` | plan summaries | docs | `58-SUMMARY.md`, `60-22-PLAN.md` output block | role-match | executor |

Evidence-path rule for rows 1 to 5: every committed path stays under `.planning/phases/64-feasibility-verdict/` or `tests/phase64/`. `.svg` and `.json` are not gitignored; `*.log`, `*.pt` and `*.npz` are (so retained command logs are never committed).

---

## Pattern Assignments

### 1. `E64/verify_phase64_verdict.py` (verifier CLI, batch)

**Analog:** `P60/verify_phase60_evidence.py` (850 lines) for shape, helpers, the label recompute, the pinned-module check, the real-data load path and `main`; `P59/verify_phase59_evidence.py` (1079 lines) for the frozen-diff check, the document-contract check, the home-path scan and the timed `final`. Both sit in the same position (`<phase>/evidence/`), use `REPO_ROOT = Path(__file__).resolve().parents[4]`, are loaded by tests by path, and print one success token per mode.

**Mode-to-source map** (copy the named block, then adapt):

| Mode (token) | Copy from | Lines |
|---|---|---|
| `inputs` (`INPUTS-OK`) | P60 `cmd_g2`: G2 recompute, forbidden later-arm prefixes, handoff verdict equals `decision_verdict(...)` | 523-536, 587-591, 593-614 |
| `numbers` (`NUMBERS-OK`) | P59 `_check_findings`: required tokens present in the document, digit-boundary regex | 972-995 (the regex is line 992) |
| `derive` (`DERIVE-OK`) | P60 `cmd_rescore`, CPU half only | 715-777 |
| `figure` (`FIGURE-OK`) | `cmd_rescore` load path + `baselines._full_mode` check-versus-write | 715-777; `baselines.py` 666-705 |
| `rules` (`RULES-OK`) | P59 `_check_findings` heading check; P59 `cmd_guardrails` home-path scan; RESEARCH Code Example 6 (wording guard) | 977-982; 899-921 |
| `frozen` (`FROZEN-OK`) | P60 `cmd_protocol` pinned-module loop; P59 `assert_scorecard_frozen` diff | 299-313; 266-269 |
| `charter` (`CHARTER-OK`) | P59 `_check_findings` structure; fence parser copied from `learnability_ruling.py` | 972-995; 119-146 |
| `ruling` (`RULING-OK`) | `learnability_ruling._fenced_blocks`, `tracked_and_clean`; P60 `is_tracked`, `is_clean` | 119-146, 213-224; 209-215 |
| `traceability` (`TRACEABILITY-OK`) | no code analog; RESEARCH Code Example 3; document precedent `58-SUMMARY.md:43-64` | n/a |
| `final` (`PHASE64-VERDICT-OK`) | P59 `_timed` + `cmd_final`; P60 `cmd_final` | 1012-1030; 809-816 |

**Header and bootstrap** (`verify_phase60_evidence.py:1-25`, `83-85`). Copy the shape. The docstring's first line starts "Phase 64:" (the repo's marker idiom, see `tests/phase60/test_static_guards.py:93-103`). Do NOT copy the module-level `import torch` and `from pinn...` lines at `:27-81`; import them inside `derive` and `figure` only (RESEARCH Pattern 5), so every other mode runs in about 0.1 s with no data root:
```python
#!/usr/bin/env python3
"""Phase 60: fail-closed evidence verifier for the single-system learnability phase.
...
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

if __package__ in (None, ""):
    _ROOT = Path(__file__).resolve().parents[4]
    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))

REPO_ROOT = Path(__file__).resolve().parents[4]
HEX64 = re.compile(r"^[0-9a-f]{64}$")
```
The `parents[4]` depth is identical for `.planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py`.

**Fail-closed core and helpers** (`verify_phase60_evidence.py:153-215`). Copy verbatim, changing only the message prefix to `verify_phase64_verdict FAIL-CLOSED:`. `repo_path` reads `REPO_ROOT` at call time, which is what lets tests patch it:
```python
class VerifyError(RuntimeError):
    """Fail-closed evidence verification error."""


def fail(message: str) -> None:
    raise VerifyError(f"verify_phase60_evidence FAIL-CLOSED: {message}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repo_path(raw: str | Path, *, what: str, root: Optional[Path] = None) -> Path:
    base = REPO_ROOT if root is None else root
    supplied = Path(str(raw))
    resolved = (base / supplied).resolve() if not supplied.is_absolute() else supplied.resolve()
    try:
        resolved.relative_to(base.resolve())
    except ValueError:
        fail(f"{what} escapes the repository: {raw!r}")
    candidate = base / supplied
    if not supplied.is_absolute() and candidate.is_symlink():
        fail(f"{what} is a symlink: {raw!r}")
    return resolved


def load_json(path: Path, *, what: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{what} is unreadable JSON: {path}: {exc}")


def _git(*args: str, root: Optional[Path] = None) -> subprocess.CompletedProcess[str]:
    base = REPO_ROOT if root is None else root
    return subprocess.run(
        ["git", *args],
        cwd=str(base),
        capture_output=True,
        text=True,
        check=False,
    )


def is_ancestor(ancestor: str, descendant: str, root: Optional[Path] = None) -> bool:
    return _git("merge-base", "--is-ancestor", ancestor, descendant, root=root).returncode == 0


def is_tracked(relative: str, root: Optional[Path] = None) -> bool:
    return _git("ls-files", "--error-unmatch", "--", relative, root=root).returncode == 0


def is_clean(relative: str, root: Optional[Path] = None) -> bool:
    proc = _git("status", "--porcelain", "--", relative, root=root)
    return proc.returncode == 0 and not proc.stdout.strip()
```

**`inputs`: recompute the pre-registered label, never type it** (`verify_phase60_evidence.py:593-614`, and the frozen rule it calls at `pinn/verification/feasibility_scorecard.py:734-752`). Phase 64 reuses exactly this call and compares to the handoff; it never edits `owner_answer` or `verdict_note` (both `null` by design, sealed):
```python
    handoff_file = g2_dir / "stop-handoff.json"
    ...
        handoff_data = load_json(handoff_file, what="stop-handoff.json")
        if not isinstance(handoff_data, Mapping) or handoff_data.get("schema") != HANDOFF_SCHEMA:
            fail("stop-handoff.json does not carry phase60-stop-handoff/v1 schema")
        ...
            card = load_scorecard()
            expected_verdict = decision_verdict(
                g2_fired=True,
                sweep_rescued=False,
                rung2b_counts=None,
                rung3_counts=None,
                control_branch=None,
                rung1_beats_formula=None,
                scorecard=card,
            )
        if handoff_data.get("verdict") != expected_verdict:
            fail(f"stop-handoff.json verdict {handoff_data.get('verdict')!r} != {expected_verdict!r}")
```
Also copy the absence check (`:587-591`): iterate `arms_dir.iterdir()` and fail on any directory whose name starts with one of `("r2a-", "r2b-", "c-r1u-", "c-r2a-", "c-r2b-", "p1-", "p2b-", "c-p1-", "c-p2b-")`. Phase 64 additionally asserts exactly seven arm directories and no `rescue.json`.

The handoff is a self-pinning root. Read-only check this session: `P60/g2/stop-handoff.json` has SHA-256 `7ed8223c066e62bd55e527dc703565367a0f9764a253e086a3bc0b4e719d02d5`; its two `basis` entries and its seven `arms[*].record` entries each carry `{"path", "sha256"}` and all nine matched the files on disk; `sum(arms[*].wall_hours)` equals `total_wall_hours` exactly (22.37828873402778). So `inputs` can check every cited record against the handoff without trusting any summary.

**`frozen`: pinned modules plus the sealed files.** Copy the per-module loop (`verify_phase60_evidence.py:299-313`), reading the 33 keys from `P60/run-protocol.json` `module_sha256` (verified this session: 33 keys, the first is `P60/launch_phase60_arm.py`):
```python
    module_shas = protocol.get("module_sha256")
    if not isinstance(module_shas, Mapping):
        fail("protocol module_sha256 is not a mapping")
    for mod_rel in PINNED_MODULES:
        if mod_rel not in module_shas:
            fail(f"pinned module {mod_rel} missing from protocol module_sha256")
        mod_path = repo_path(mod_rel, what=f"pinned module {mod_rel}")
        if not mod_path.is_file():
            fail(f"pinned module {mod_rel} does not exist")
        if not is_tracked(mod_rel) or not is_clean(mod_rel):
            fail(f"pinned module {mod_rel} is not tracked and clean")
        mod_disk_sha = sha256_file(mod_path)
        if mod_disk_sha != module_shas[mod_rel]:
            fail(f"pinned module {mod_rel} SHA-256 {mod_disk_sha} != pinned {module_shas[mod_rel]}")
```
For the eight sealed files (`P60/run-protocol.json`, `60-RUN-PROTOCOL.md`, `P60/g2/{g2-outcome,sweep-curve,skip-records,stop-handoff}.json`, `P59/scorecard-freeze.json`, `59-SCORECARD.md`) copy the diff form of `P59/verify_phase59_evidence.py:266-269`, with the phase base `1ebb1d9b` in place of the freeze commit:
```python
    freeze_commit = first_commit_of(FREEZE_REL.as_posix())
    diff = _git("diff", "--quiet", freeze_commit, "HEAD", "--", *rels)
    if diff.returncode != 0:
        fail(f"frozen files differ from the freeze commit {freeze_commit}")
```
Derive the 33 from `run-protocol.json` at runtime and assert the count is 33, instead of hard-coding a second list that can drift; hard-code only the eight sealed paths.

**`derive` and `figure`: the real-data load path** (`verify_phase60_evidence.py:715-731`, `749-777`; the middle `:732-748` loads the weights with `torch.load(..., weights_only=True)` and checks the file SHA-256 and tensor digest against the record). Copy the CPU float64 half only. One `open_real_context` per process, a plain frozen `DataContext` (not a context manager), NumPy `ArmData`:
```python
    card = load_scorecard()
    # learnability_data.open_real_context returns a plain DataContext (not a context manager);
    # the process-wide attestation counts every open, so one context serves all arms.
    ctx = open_real_context(repo_root=REPO_ROOT)
    for arm_dir in target_dirs:
        ...
        spec = arm_spec(record["arm_id"])
        first_omega_0 = float(record["first_omega_0"])

        arm_data = load_arm_data(spec, ctx, scorecard=card, dtype=torch.float32, device="cpu")
        attestation = ctx.attestation
        if attestation is None or attestation.test_split_opened != 0:
            fail(f"rescore opened the test split, or has no open attestation, for {arm_dir.name}")
        ...
            widened = OrderedDict(
                (name, tensor.detach().to("cpu").to(torch.float64))
                for name, tensor in weights.items()
            )
            if abs(first_omega_0 - 30.0) < 1e-9:
                cpu_model = build_network(ArchitectureSpec(seed=SEED), dtype=torch.float64, device="cpu")
            else:
                cpu_model = build_network_with_first_omega(first_omega_0, seed=SEED, dtype=torch.float64, device="cpu")
            cpu_model.load_state_dict(widened)
```
Phase 64 then calls the lower-level pieces instead of `score_network` (RESEARCH Code Example 1): `network_trajectory(model, _float32_rounded(ad.ic13), _float32_rounded(ad.masses), ad.score.times, dtype=torch.float64, device=torch.device("cpu"))` returns `(positions, velocities)` as NumPy arrays of shape (N, 3, 3) (`pinn/verification/feasibility_scorer.py:382-435`); `position_errors(pred, ref, inner_pair)` returns `(e_sys, e_in, R_sys)` (`:183`); `tier_defining_error(e_sys, e_in)` is `max_t max(e_sys, e_in)` (`:211`). `ad.score` is a `RecordView(grid, times, positions, inner_pair, masses)` (`pinn/verification/learnability_data.py:98-106`). Assertions beyond Phase 60's: the attestation summary (`pinn/verification/split_allowlist.py:325-337`) must show `test_split_opened` 0, `blocked_attempts` 0, `refused_before_open` 0, `opened["validation"]` 0 and `opened["other_under_root"]` 0, and the CPU `E` must equal the record's `states.<state>.cross_check.E` to 1e-12 (Phase 60 uses the same tolerance at `:774`). Never compare the CPU `E` to the official MPS `E` (RESEARCH Pitfall 2).

**`numbers` and `rules`/`charter`: the document contract** (`P59/verify_phase59_evidence.py:972-995`). The digit-boundary regex at line 992 is the one to reuse for "this rendered number appears in the verdict", so `1.1574` does not match inside `11.1574`:
```python
    text = path.read_text(encoding="utf-8")
    headings = re.findall(r"^## .+$", text, re.M)
    if not headings or headings[0] != "## In plain language":
        fail("59-FINDINGS.md does not open with ## In plain language")
    for heading in _FINDING_HEADINGS:
        if heading not in headings:
            fail(f"59-FINDINGS.md lacks heading {heading}")
    if SCORECARD_SHA256 not in text:
        fail("59-FINDINGS.md lacks the scorecard SHA-256")
    ...
    for row in panels["singles"]:
        ident = str(row["id"])
        if re.search(rf"(?<!\d){re.escape(ident)}(?!\d)", text) is None:
            fail(f"59-FINDINGS.md lacks single panel id {ident}")
```
Phase 64 applies the same first-`##`-heading rule to `64-VERDICT.md` and `64-CHARTER.md`.

**`rules`: the home-path scan** (`P59/verify_phase59_evidence.py:899-921`). The needle is `str(Path.home())` built at run time, never a literal in the source, so the verifier does not flag itself (see H2). Phase 59 lists tracked files with `git ls-files -- <dir>`; Phase 64 must list only the scan set named in H2:
```python
    home = str(Path.home())
    ...
    listed_proc = _git("ls-files", "--", EVIDENCE_REL.as_posix())
    if listed_proc.returncode != 0:
        fail(f"cannot list tracked evidence: {listed_proc.stderr.strip()}")
    for relative in [line for line in listed_proc.stdout.splitlines() if line.strip()]:
        path = REPO_ROOT / relative
        if not path.is_file():
            continue
        raw = path.read_bytes()
        if b"\0" in raw:
            continue
        text = raw.decode("utf-8", errors="replace")
        if home and home in text:
            fail(f"tracked evidence contains the home directory: {relative}")
```

**`ruling`: the fence parser** (`pinn/verification/learnability_ruling.py:72-76`, `119-146`). Copy these ~35 lines into the verifier rather than importing the private `_fenced_blocks` from a pinned module (H1). Count the `owner-quote` blocks; do not use `parse_machine_block`, which requires a `phase60-ruling` block that Phase 64 does not have:
```python
# Markdown line endings only: str.splitlines would also split on U+2028 and others.
_LINE_BREAK = re.compile(r"\r\n|\n|\r")
_FENCE_OPEN = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>.*?)[ \t]*$")
_FENCE_CLOSE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})[ \t]*$")

def _fenced_blocks(text):
    """``[(info string, content lines)]`` for every fenced block of ``text``, Markdown-style."""
    lines = _LINE_BREAK.split(text)
    blocks = []
    index = 0
    while index < len(lines):
        opening = _FENCE_OPEN.match(lines[index])
        if opening is None or (opening["fence"][0] == "`" and "`" in opening["info"]):
            index += 1
            continue
        fence, info = opening["fence"], opening["info"]
        content = []
        index += 1
        while True:
            if index >= len(lines):
                raise RulingError("a fenced block is never closed")
            closing = _FENCE_CLOSE.match(lines[index])
            if (
                closing is not None
                and closing["fence"][0] == fence[0]
                and len(closing["fence"]) >= len(fence)
            ):
                break
            content.append(lines[index])
            index += 1
        blocks.append((info, content))
        index += 1
    return blocks
```
Contrast to keep straight: the ruling file has exactly one `owner-quote` block (the rule at `learnability_ruling.py:172-173`); the charter holds several (the two D-06 statements and the D-07 statement, to be compared byte for byte with `64-CONTEXT.md:68`, `:69` and `:72`). The charter check is "these three quotes are present and byte-equal", not "exactly one".

**`final` and `main`** (`P59/verify_phase59_evidence.py:1012-1030`, `1043-1079`; `P60:809-850`). Each mode prints its token on its own line and `final` prints the aggregate token last (Phase 60 lost a plan clause to an `END=` line printed after `EXIT=0`). Note the precedent split: Phase 60's `final` excludes the data-dependent `rescore`; Phase 59's `final` includes its re-derivations. RESEARCH lists every mode under `final`, so keep `derive` and `figure` in it and let the unit test for the data-dependent modes skip with a stated reason when the data root is absent:
```python
def _timed(name: str, action) -> None:
    started = time.perf_counter()
    action()
    print(f"elapsed {name} {time.perf_counter() - started:.3f}")


def cmd_final(_args: argparse.Namespace) -> None:
    """Run every evidence check and the findings-page contract."""
    _timed("scorecard-frozen", assert_scorecard_frozen)
    ...
    _timed("findings", _check_findings)
    print("PHASE59-EVIDENCE-OK")
```
```python
COMMANDS = {
    "protocol": cmd_protocol,
    ...
    "final": cmd_final,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=tuple(COMMANDS))
    ...
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        COMMANDS[args.command](args)
    except Exception as exc:  # noqa: BLE001 - fail-closed CLI
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Do not copy:** the module-level `torch`/`pinn` imports; Phase 60's `REQUIRED_REAL_FIELDS` and `G2_TOKENS` tables (they belong to the producer's schema); the MPS half of `cmd_rescore` (`:779-804`; Phase 64 is CPU only); any `P59` `evidence_io.runtime_gate` or `require_frozen_scorecard` call (Phase 59-specific, see row 2).

**Test pattern:** row 10.

---

### 2. `E64/build_phase64_evidence.py` (producer, transform + file-I/O)

**Analog:** `pinn/verification/baselines.py::_full_mode` for the produce-then-check discipline, `pinn/verification/evidence_io.py` for the writer, and `cmd_rescore` (row 1) for the load path. It lives in the evidence directory like `P60/launch_phase60_arm.py`, which supplies the same bootstrap (`:52-57`).

**Check-versus-write discipline** (`pinn/verification/baselines.py:666-705`, trimmed). This is how "run the builder twice in separate processes and require one SHA-256" is realised: the second process runs `--check`, which compares freshly rendered bytes with the committed bytes and prints a token:
```python
def _full_mode(args, *, check, started_wall, started):
    collected = collect(args)
    payloads = build_payloads(collected)
    rendered = _rendered_bytes(payloads)
    directory = _evidence_dir(args)
    if check:
        same = True
        for name, raw in rendered.items():
            if not evidence_io.bytes_identical(directory / name, raw):
                print(f"BASELINES-CHECK-DIFF: {name}", file=sys.stderr)
                same = False
        same = _opened_zeros(collected["attestation"], directory) and same
        if not same:
            return 1
        print("BASELINES-CHECK-OK")
        return 0
    data_root = collected["data_root"]
    for name, payload in payloads.items():
        if name.endswith(".json"):
            evidence_io.write_json(directory / name, payload, data_root=data_root)
        else:
            evidence_io.write_text(directory / name, payload, data_root=data_root)
    evidence_io.write_json(
        directory / "files_opened.json",
        evidence_io.files_opened_record("baselines", collected["attestation"].summary()),
        data_root=data_root,
    )
    evidence_io.write_json(
        directory / "provenance.json",
        evidence_io.provenance_record(
            "baselines",
            sys.argv,
            data_root=data_root,
            data_root_source=collected["data_root_source"],
            utc_started=started_wall,
            monotonic_started=started,
        ),
        data_root=data_root,
    )
    return 0
```
with `_rendered_bytes` (`:630-637`) dispatching `.json` to `evidence_io.canonical_json_bytes` and everything else to `.encode("utf-8")`. The SVG goes through `write_text`.

**Writer, redaction and byte comparison** (`pinn/verification/evidence_io.py`). Reuse these four; do not re-implement them:
```python
# evidence_io.py:131-140
def canonical_json_bytes(payload: Any) -> bytes:
    """Sorted, indented JSON with non-finite floats as string sentinels."""
    text = json.dumps(
        json_safe(payload),
        sort_keys=True,
        indent=2,
        ensure_ascii=True,
        allow_nan=False,
    )
    return (text + "\n").encode("ascii")


# evidence_io.py:143-155
def guard_redaction(data: Any, *, data_root: Optional[Path] = None) -> None:
    """Refuse text that still contains the home directory or the resolved data root."""
    ...
    home = str(Path.home())
    if home and home in text:
        raise EvidenceRedactionError("evidence contains the host home prefix")
    ...


# evidence_io.py:187-193
def write_json(path: Path, payload: Any, *, data_root: Optional[Path] = None) -> str:
    """Atomically write canonical JSON and return the SHA-256 of the bytes."""
    ...


# evidence_io.py:301-308
def bytes_identical(path: Path, new_bytes: bytes) -> bool:
    """True when ``path`` already holds ``new_bytes``."""
    ...
```
`write_json` and `write_text` already call `guard_redaction`, so a host path cannot reach `numbers.json`, the SVG or the provenance file (RESEARCH Pitfall 9) even if the producer is careless; the verifier's `rules` scan is the second line.

**Provenance fields to imitate** (`evidence_io.py:270-298`): tool, redacted command, `git_head`, `worktree_dirty`, `python`, `numpy`, `torch`, UTC start and end, elapsed seconds, `data_root_source` (the label `"git_common_dir_default"`, never the root). `provenance_record` hard-codes `"schema": "phase59-provenance/v1"`; either override that key or write a Phase 64 record, so no Phase 59 schema string sits in Phase 64 evidence. A sibling attestation record is available as `evidence_io.files_opened_record(tool, attestation.summary())` (`:230-235`); the planner may instead embed the attestation summary in the provenance JSON.

**Determinism** (RESEARCH Pitfall 12): `torch.set_num_threads(1)`, pixel coordinates rounded to 0.1, fixed element order. The check of record is `--check` in a second process.

**Do not copy:** `baselines.py`'s `evidence_io.require_frozen_scorecard`, `evidence_io.runtime_gate`, `EVIDENCE_ROOT_REL` and `PRODUCER_MODULES` (all Phase 59-specific; `EVIDENCE_ROOT_REL` points at Phase 59's tree and `runtime_gate` is a 600 s budget gate); `PINNED_PYTHON` from `launch_phase60_arm.py:60` (a committed host path, which the `rules` scan would flag); any `runs/` output path.

**Import-only rule:** `evidence_io.py` is one of the 33 pinned files (H1). Import it; never edit it.

---

### 3. `E64/numbers.json` (number manifest, file-I/O)

**Analog:** `P59/baselines/baselines.json` (canonical JSON written by `evidence_io.write_json`).

Shape to imitate, from the real file's top-level keys: a `schema` string (`"phase59-baselines/v1"`, so use `"phase64-numbers/v1"`), a `plain_language` sentence, a `producer_sha256` map of producer module path to SHA-256, the `scorecard_sha256`, and named result blocks. The handoff's `basis` and `arms` entries (`P60/g2/stop-handoff.json`) show how to cite an input, as `{"path": "<repo-relative>", "sha256": "<64 hex>"}`; this is its `arms[0]` entry, reflowed:
```json
{"arm_id": "r1-1632",
 "record": {"path": ".planning/phases/60-single-system-learnability/evidence/arms/r1-1632/record.json",
            "sha256": "a87273674785128714f5eae4981dcee31fe4c2332dbd84213b7aeaa0098da0b7"},
 "seconds_per_step": 0.013596008833963424, "wall_hours": 2.5732112903124977}
```
Per RESEARCH Pattern 1, every entry also carries an id, a source file and key, the derivation, and a label that says whether it is "official (MPS float32)" or "re-derived (CPU float64)". Keys are written sorted by `canonical_json_bytes`, so do not rely on insertion order.

**Do not copy:** Phase 59's `producer_sha256` list of modules (it names Phase 59's producers); list Phase 64's own producer and the modules it imports.

---

### 4. `E64/figure-1632.svg` (figure)

**No repository analog.** There is no tracked `.svg`, no tracked Python that emits `<svg`/`polyline`, and the only plotting code in the repo is vendored `reference-code/.../GravNN` (matplotlib, which `pinn-train` does not have). Use RESEARCH Code Example 5 (a 60-line stdlib SVG polyline writer, prototyped, rendered and checked for byte determinism) and Pitfalls 11 and 12. Write it with `evidence_io.write_text` so the redaction guard applies. Read the series from the same `network_trajectory` call as `derive` (row 1), so the figure and the verdict's numbers share one source.

---

### 5. `E64/figure-1632.provenance.json` (provenance record, file-I/O)

**Analog:** `P59/baselines/provenance.json` (real keys: `command`, `data_root_source`, `elapsed_seconds`, `git_head`, `numpy`, `python`, `ru_maxrss_bytes`, `schema`, `tool`, `torch`, `utc_finished`, `utc_started`, `worktree_dirty`) plus the `{path, sha256}` citation form from `P60/g2/stop-handoff.json`. Required by D-04: the source paths and SHA-256 of the committed weights it read, the SHA-256 of the SVG, and the library versions. Repo-relative paths only; record `data_root_source`, never the root. The `figure` mode recomputes the SVG's SHA-256 and compares regenerated rounded series with the committed series (RESEARCH A5 notes only two runs on this Mac were compared, so compare series or record versions rather than assuming cross-machine byte equality).

Note the existing precedent: `P59/baselines/provenance.json` has `"command": "~/Desktop/..."`, a home-redacted path. That is accepted by the redaction guard but still names a host layout; prefer a command string with no path.

---

### 6. `.planning/phases/64-feasibility-verdict/64-VERDICT.md` (owner-facing verdict, docs)

**Analog:** `.planning/phases/58-verdict-traceability-close/58-VERDICT.md` (67 lines, the v2.3 verdict, same owner and same decision form) for structure and front matter; `.planning/phases/60-single-system-learnability/60-FINDINGS.md` for the plain-language register, the per-arm table, the machine-hours table and the evidence index; `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md` for the evidence-matrix and sign-off blocks.

**Front matter** (`58-VERDICT.md:1-13`). Copy the key set; set `schema_version: phase64-verdict/v1`:
```yaml
---
schema_version: phase58-verdict/v1
status: owner-signed
gate: not-run
evaluation: preserved-unspent
verdict: rethink
owner_decision: rethink
owner_decision_date: 2026-10-03
agent_recommendation: none ranked in the packet; ...
packet_citation: docs/work/designs/milestone_v2.3/58-verdict-traceability-close/2026-10-03-phase-58-diag-06-verdict-packet.md
terminal_citation: .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/terminal-state.json
verification_citation: .planning/phases/57-corrected-re-run-the-preserved-evaluation/57-VERIFICATION.md
---
```
Both precedents were written after the owner had decided, so neither shows a pre-sign-off `status` value. Phase 64 drafts the verdict before checkpoint 1 and finalises it after. The pre-sign-off value is a presentation-only choice for the planner to make and note in the plan; it must agree with whatever the `rules`/`ruling` modes check. Do not add a machine-read block (RESEARCH Pattern 3: a `phase64-ruling` block would be a new schema with no reader).

**Section skeleton** (`58-VERDICT.md:24-67`): "Decision boundary" (bullets), "Evidence matrix" (a three-column table `Evidence | Observed result | Grounding`, `:35-44`), "Requirement dispositions" (`:46-53`), "Routing of the next milestone" (`:55-67`), and the sign-off block of `43-VERDICT.md:116-125`:
```markdown
## Owner sign-off

- **Decision:** `adjust`
- **Date:** 2026-07-22
- **Meaning:** retain the demonstrated mechanical Stage-0 slice, block
  full-platform expansion, ...
- **Qualification:** this decision does not claim that the remedy is known. It
  does not authorize another held-out evaluation, Stage 1, or any PLAT-01..07
  implementation.
```

**Plain-language register** (`60-FINDINGS.md:1-12`): an `Audience` line, the frozen hashes the page depends on, a sentence that every number is copied from a named committed file, then `## In plain language` as the first `##` heading (the `rules` check, row 1), then a numbered list that leads with what happened and defines each term once:
```markdown
# Phase 60 Findings: Single-System Learnability

**Audience: the project owner, a non-specialist.**
**Run protocol:** SHA-256 `93486d24...` (sealed before any arm ran; every record cites it).
...
## In plain language

Think of the project's experiments as a ladder of exams, each harder than the last, ...

1. **At the locked setting, the network did not reproduce any of the three orbits.** ...
```
Phase 64's D-01 box (the label side by side with what the evidence shows) and the D-02 qualifier sentence have no precedent; their source text is `60-VERIFICATION.md:392-446` ("Independent observation for Phase 64") and RESEARCH findings 2 and 7. Use "levelled off", not "flat" (H5).

**Tables to extend, not reinvent.** The per-arm table (`60-FINDINGS.md`, "Result per arm") and the machine-hours table (`## Machine hours`, columns `Arm | Wall hours | Adam s + polish s | Timed seconds per step | Adam step budget | Budget outcome | Invocations / governed stops`, with a bold Total row) are the base for FEAS-06's tier-per-rung and cost sections. The evidence index (`## Evidence index`: tables of `What | Path | SHA-256 | Checked by`, then a "Verifier and test results at close" table) is the base for the verdict's own index. RESEARCH "Per-arm table" and "Ladder evidence (levels 0 to 9)" already hold the values and the sources for each cell; the `numbers` mode re-derives them.

**Test pattern:** `numbers`, `rules` and the structure checks of row 1; the first-heading test of row 10.

---

### 7. `.planning/phases/64-feasibility-verdict/64-CHARTER.md` (owner decision page, docs)

**Analog (partial):** no committed charter exists. Three tracked documents supply the layout:

- Framing: `docs/work/designs/milestone_v2.3/58-verdict-traceability-close/2026-10-03-phase-58-diag-06-verdict-packet.md:12-20` (an `Audience`, "This document is" and "This document is not" block) and `:24-38` ("What you are being asked to decide", numbered, with the consequence of each choice).
- Option layout: `59-GAPS.md:281-333` (GAP-59-08: options A, B, C with a recommendation) and `64-GAPS.md` GAP-64-01 (options A, B, C, A recommended). The charter reproduces both as pre-filled lines.
- Owner words: the `owner-quote` fence (row 8).

Content comes from `64-CONTEXT.md` D-06 to D-13 and `64-RESEARCH.md` "Charter inputs". The layout RESEARCH specifies and the verifier will check: a pre-filled table with item ids (C-1 and so on), a recommended answer in each row, short options, and an empty "Owner" column; the decision page between `<!-- page:begin -->` and `<!-- page:end -->` markers (about 60 lines); options, evidence and the draft `PROJECT.md` text in appendices; the first `##` heading `## In plain language`.

**Fence example for the quotes** (the fence must be longer than any backtick or tilde run inside the message; the info string is exactly `owner-quote`; copy the text byte for byte from `64-CONTEXT.md:68`, `:69` and `:72`):
~~~~markdown
```owner-quote
For now, the only device on which we will do the computation will be on this MacBook, so ignore ...
```
~~~~
(In the real file the fence is the longer of the two: for a message with no backticks, three backticks suffice; for one that contains a triple-backtick run, use four or more backticks or tildes. `learnability_ruling.py:17-20` states the rule.)

The wording guard (row 1, `rules`) strips fenced `owner-quote` blocks before scanning, so the owner's two Mac-only statements may appear there and nowhere else.

**Test pattern:** `charter` mode (row 1); negative controls in row 10 (truncate an owner quote and `charter` must fail).

---

### 8. `.planning/phases/64-feasibility-verdict/64-CHECKPOINT-1-RULING.md` (owner ruling record)

**Analog:** `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-RULING.md` for front matter and the "Authority and boundary" section; `60-17-PLAN.md` Task 3 for how the file is written from the owner's own words; `pinn/verification/learnability_ruling.py:1-27` for the file contract.

**Front matter and boundary section** (`57-RULING.md:1-30`):
```markdown
---
phase: 57
milestone: v2.3
created: 2026-09-08
pre_registered_at: "2026-09-08T02:05:10Z"
status: ratified
authority: direct owner instruction on 2026-09-08
---

# Phase 57 — GATE-04 and Checkpoints ③/④ Ruling

## Authority and boundary

The owner directly authorized the following decisions on 2026-09-08:

> GATE-04: require at least a 2:1 spread ...

This record resolves GAP-56-01, GAP-54-06, and owner checkpoints ③ and ④. It
does not resolve GAP-56-02 or checkpoint ⑤, authorize recipe retuning, ...
```
Adapt the key set to `60-17-PLAN.md:140-146`: phase `64-feasibility-verdict`, milestone `v2.4`, `created` today, `status: ratified`, `authority: owner, checkpoint 1 (FEAS-06, FEAS-10)`, then "Authority and boundary", then the owner's message verbatim in exactly one `owner-quote` fence, and nothing outside the fence that paraphrases the owner beyond restating the chosen option. Per RESEARCH Pattern 3, add no `phase64-ruling` machine block unless a reader exists.

**Ask-again rule** (`60-17-PLAN.md:129`): "If the message does not unambiguously choose one option ... ask again; never infer an answer or a value." Items the owner does not address are recorded as open, not approved (RESEARCH Pitfall 14). Commit with a body that quotes the owner (T-60-04 and T-60-20 in `60-17-PLAN.md:175-176`).

**What the file proves downstream:** the `ruling` mode (row 1) requires the file to be tracked and clean, to contain exactly one non-empty `owner-quote` block, and the `PROJECT.md` rewrite to be applied only if the record approves it.

**Test pattern:** `tests/phase60/test_ruling.py`, shown in row 10.

---

### 9. `tests/phase64/__init__.py` (test scaffold)

**Analog:** `tests/phase60/__init__.py`, one docstring line: `"""Phase 60 tests: the single-system learnability harness."""`. Write the equivalent: `"""Phase 64 tests: the feasibility verdict, charter and traceability verifier."""`.

---

### 10. `tests/phase64/test_verifier_phase64.py` (tests, batch)

**Analog:** `tests/phase60/test_verifier_phase60.py` (749 lines) for the loader, the synthetic-repo fixture and the real-shape fixtures; `tests/phase59/test_evidence_verifier.py` (1255 lines) for the frozen-repo fixture and the real-worktree smoke tests; `tests/phase60/test_ruling.py` (594 lines) for the owner-quote tests.

**Load the verifier by path and run it in-process** (`test_verifier_phase60.py:34-74`). Use module name `verify_phase64_verdict` and the Phase 64 path:
```python
VERIFIER_PATH = (
    Path(__file__).resolve().parents[2]
    / ".planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py"
)

def load_verifier():
    spec = importlib.util.spec_from_file_location("verify_phase60_evidence", VERIFIER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]: ...
def init_repo(root: Path) -> None: ...
def commit_all(root: Path, message: str) -> str: ...

def run_main(module, argv: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = module.main(argv)
    return code, stdout.getvalue(), stderr.getvalue()
```
`tests/phase60/test_ruling.py:30` already shows cross-importing the helpers (`from tests.phase59.test_evidence_verifier import commit_all, init_repo`); copying them is equally fine.

**Synthetic git repo with `REPO_ROOT` patched** (`test_verifier_phase60.py:98-104`, `176-195`). Every failing-mode test follows one shape: build a tree in a temp repo, commit, patch, run, assert exit code, token and the `FAIL-CLOSED` prefix:
```python
        commit_all(self.root, "setup protocol test")

        patcher = mock.patch.object(self.module, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_committed_protocol_with_current_digests_passes(self):
        code, out, err = run_main(self.module, ["protocol"])
        self.assertEqual(code, 0, f"stderr: {err}")
        self.assertIn("PROTOCOL-OK", out)

    def test_changed_pinned_file_fails(self):
        pinned = self.root / self.module.PINNED_MODULES[0]
        pinned.write_bytes(b"# modified\n")
        commit_all(self.root, "modify pinned")
        code, out, err = run_main(self.module, ["protocol"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL-CLOSED", err)
```
For `frozen`, build the temp repo the way `P59` tests do (`FrozenRepo`, `tests/phase59/test_evidence_verifier.py:76-156`: copy real bytes, commit "sources", write the record, commit "freeze").

**Real shapes, never tensors or context managers** (`test_verifier_phase60.py:678-713`, the repaired fixtures; the original tests had mocked the wrong shapes and the verifier crashed on first real use, twice):
```python
    @staticmethod
    def _real_context(attestation):
        """The real ``DataContext`` shape: a frozen dataclass, not a context manager."""
        return DataContext(
            allowlist=None,
            reader=None,
            attestation=attestation,
            stats=None,
            stats_sha256="0" * 64,
            normalizer_source="test",
            run_kind="fixture",
            data_root_source="test",
        )

    @staticmethod
    def _real_arm_data():
        """The real ``ArmData`` shape: numpy float64 arrays, not torch tensors."""
        return SimpleNamespace(
            ic13=np.zeros(13, dtype=np.float64),
            masses=np.ones(3, dtype=np.float64),
            score=SimpleNamespace(
                positions=np.zeros((10, 3, 3), dtype=np.float64),
                inner_pair=(0, 1),
                times=np.linspace(0.0, 1.0, 10),
                grid="gold",
            ),
        )

    def _run_rescore(self, argv, *, attestation):
        with mock.patch.object(self.module, "open_real_context") as mock_ctx, \
             mock.patch.object(self.module, "load_arm_data") as mock_load_data, \
             mock.patch.object(self.module, "score_network") as mock_score:
            mock_ctx.return_value = self._real_context(attestation)
            ...
```
Because Phase 64 imports `torch`/`pinn` lazily inside `derive`/`figure`, patch those names where the mode looks them up (inside the function), or call the mode's pure helper directly. Also add a no-mock integration test that skips with a stated reason when the data root is absent (RESEARCH "Unit tests"; the pure functions must never skip).

**Real-worktree smoke inside the suite** (`tests/phase59/test_evidence_verifier.py:350-355`). One per committed-JSON mode, so a mode is proven on the real tree before its synthetic tests are trusted (RESEARCH Pattern 4):
```python
    def test_real_worktree_prints_scorecard_frozen_ok(self) -> None:
        self.assertIsNotNone(self.module)
        code, out, err = run_main(self.module, ["scorecard-frozen"])
        self.assertEqual(code, 0, err)
        self.assertIn("SCORECARD-FROZEN-OK", out)
        self.assertNotIn("FAIL-CLOSED", err)
```

**Document-contract test** (`tests/phase59/test_evidence_verifier.py:1229-1251`): assert the first `##` heading is `## In plain language` and that every success token and command name appears in the document that lists them (apply to `64-VERDICT.md`, `64-CHARTER.md` and, if one is written, an `evidence/README.md`).

**Owner-quote tests** (`tests/phase60/test_ruling.py:32-66`, `262-303`). Copy the fixture builder and the hostile-quote table; adapt the `ruling` assertions to "exactly one `owner-quote` block, closed, non-empty":
```python
def ruling_file(machine_lines, *, quote=QUOTE, machine_fence="```", quote_fence="```",
                prose=PROSE, quote_first=False):
    """A synthetic ruling file: front matter, prose, one machine block and one quote block."""
    ...

    HOSTILE = (
        ("a fake machine block inside a tilde-fenced quote", "~~~~~~",
         "```phase60-ruling\nruling: checkpoint-4\nanswer: go-to-verdict\n```"),
        ("shorter fences inside a longer backtick fence", "`````", ...),
        ("a shell command", "```", "$(touch SENTINEL) `touch SENTINEL`; rm -rf / # nothing runs"),
        ("a very long line", "```", "x" * 100000),
    )

    def test_exactly_one_quote_block_is_required(self):
        ...
    def test_a_quote_that_closes_its_own_fence_early_is_refused_not_trusted(self):
        ...
    def test_nothing_in_the_file_reaches_a_command_or_a_path(self):
        ...
```
The last of those three spies on `subprocess.run` and asserts that every argv is a list starting with `git` and that `shell` is never true (`test_ruling.py:319-349`). `test_ruling.py:185-260` additionally pins the fence edge cases (indentation of up to three spaces, tilde versus backtick, a longer fence closes a shorter one, unclosed block refused, CRLF accepted, U+2028 does not split lines); reuse them for the copied parser.

**Negative controls and mutants.** Each mode needs a passing case and at least one failing case (flip one number in a temporary copy of the verdict and `numbers` must fail; insert Mac-only-rule wording outside a fence and `rules` must fail, inside an `owner-quote` fence it must pass; touch a frozen file in a temporary repo and `frozen` must fail; delete a table row or duplicate a roadmap id and `traceability` must fail; truncate an owner quote and `charter` must fail). The repo's mutant-style precedent is the injected-violation self-tests of `tests/phase60/test_static_guards.py:416-` (`DetectorSelfTests`) and the explicit negative control at `test_verifier_phase60.py:538-544` ("no setting reached Tier 1, so a curve that confirms 240.0 is wrong").

**Run commands:** the quick command is in `64-VALIDATION.md` (`unittest tests.phase64.test_verifier_phase64 -v`, target at most 30 s). The helper module imports `tests.phase59...` and `pinn.verification...`, so run from the repository root.

---

### 11. Frozen-path list for the `frozen` mode

**Analog:** `P60/run-protocol.json` `module_sha256` (33 keys, verified) and `P59/scorecard-freeze.json` (the pin-and-diff precedent; keys include `scorecard_path`, `scorecard_sha256`, `decision_sources`). Recommendation: derive the 33 at run time (row 1) rather than commit a second list. If a committed list is kept (RESEARCH Wave 0 gap), it must come with the arg-count self-test and a negative control (RESEARCH Code Example 4), because a plan `<automated>` gate that expands an unquoted multi-path variable passes vacuously under zsh (H4).

The 33 pinned paths, as printed from `module_sha256` this session (for the planner's reference; they are read from the file, not typed): `P60/launch_phase60_arm.py`; `pinn/architecture_spec.py`, `constants.py`, `loss_catalog.py`, `network.py`, `physics_residual.py`; `pinn/data/batches.py`, `preprocessing.py`, `types.py`; `pinn/training/atomic_io.py`, `config.py`, `controllers.py`, `determinism.py`, `grad_clip.py`, `scheduled_weights.py`, `signals.py`; `pinn/verification/artifacts/feasibility_scorecard_v1.json`, `artifacts/r_ref_stage0.json`, `diagnostic_architecture.py`, `evidence_io.py`, `feasibility_scorecard.py`, `feasibility_scorer.py`, `gate04_omega_remeasure.py`, `gate04_train_free.py`, `learnability_arms.py`, `learnability_data.py`, `learnability_g2.py`, `learnability_losses.py`, `learnability_protocol.py`, `learnability_ruling.py`, `learnability_run.py`, `production_reference.py`, `split_allowlist.py`.

---

### 12. `64-01-PLAN.md` to `64-06-PLAN.md` (execution plans)

**Analogs:** `60-17-PLAN.md` (the blocking owner checkpoint, for 64-05), `60-22-PLAN.md` (closeout: gate, document, hand-edited registries in one commit, for 64-06 and the document plans), `60-13-PLAN.md` (a verifier built with a tracer task and a blocking owner decision inside, for 64-01 and 64-02).

**Front matter and body skeleton** (`60-17-PLAN.md:1-36`, `54-199`). `autonomous: false` for the checkpoint plan only; `depends_on` follows the wave plan; `requirements` uses the Phase 64 ids:
```yaml
---
phase: 60-single-system-learnability
plan: 17
type: execute
wave: 17
depends_on: ["60-16"]
files_modified:
  - .planning/phases/60-single-system-learnability/60-CHECKPOINT-4-RULING.md
autonomous: false
requirements: [FEAS-03]

estimate:
  tokens: 40000
  raw_tokens: 40000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "..."
  artifacts:
    - path: "..."
      provides: "..."
      contains: "..."
  key_links:
    - from: "..."
      to: "..."
      via: "..."
      pattern: "..."
---
```
Body order: `<objective>` (with an "In plain language" paragraph and a Purpose and Output line), `<execution_context>` (the two `@~/.claude-max/gsd-core/...` includes, which Phase 59 and 60 plans all use), `<context>` with `<interfaces>`, `<tasks>`, `<threat_model>`, `<verification>`, `<success_criteria>`, an "Artifacts this phase produces" section, and `<output>` with the commit protocol.

**Checkpoint task skeleton** (`60-17-PLAN.md:98-135`, condensed):
```xml
<task type="checkpoint:decision" gate="blocking-human">
  <name>Task 2: Owner checkpoint ...</name>
  <files>None; the owner answers in chat.</files>
  <read_first>- The Task 1 decision material</read_first>
  <decision>...</decision>
  <context>...</context>
  <options>
    <option id="continue"><name>...</name><pros>...</pros><cons>...</cons></option>
    ...
  </options>
  <resume-signal>Answer in your own words, for example "...".</resume-signal>
  <action>... Record the owner's message verbatim. If the message does not unambiguously choose one option ... ask again; never infer an answer or a value.</action>
  <acceptance_criteria>...</acceptance_criteria>
  <done>The owner has answered in their own words.</done>
</task>
```
Tracer tasks are `<task type="tracer">` (and `tdd="true"` for verifier work, `60-13-PLAN.md:111`) and carry `<verify><automated>` plus `<fails_when>`; the verify command in these plans names the pinned interpreter by absolute path, which is acceptable in plan files (they are outside the `rules` scan set, H2).

**Closeout shape** (`60-22-PLAN.md:75-144`): Task 1 a tracer that runs the phase gate and refuses to close if anything is running or pending; Task 2 the owner-facing document, `<verify>` by `head -n 5 ... | grep -q "Audience"`, `grep -q "^## In plain language"` and `git ls-files --error-unmatch`; Task 3 the hand-edited registries (rows 14 to 16).

**Commit protocol block** (`60-22-PLAN.md:184`, adapted: the trailer is generic here), the line every plan ends with. Keep it, but supply the model attribution the executing session gives; the Phase 60 plans name their own session's model, which must not be copied:
```text
Commit protocol: `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set to this plan's files_modified plus its SUMMARY; explicit `git add -- <paths>`; bodies on every commit; several `-m` paragraphs with a `Co-Authored-By:` trailer last; never `-F`, never `--no-verify`. Never stage logs, `.planning/config.json` or the v2.2 design brief. No gsd-tools state.* or other mutating verb.
```
Two more repo rules: the subject carries no apostrophe or other quote character (the commit-msg hook rejects them, `60-17-PLAN.md:193`); and `scripts/agent-commit` appends its own `-m` after yours, so never pass a `--` pathspec to it (stage explicit owned paths first). Also never stage the two files dirty in this worktree: `.planning/config.json` and `docs/work/designs/milestone_v2.2/50-valid-stage-0-re-run/2026-08-16-stage0-causal-front-halt-brief.md`.

---

### 13. `64-VALIDATION.md` (EDIT)

**Analog:** `59-VALIDATION.md` (finished state: `nyquist_compliant: true`, `wave_0_complete: true`). The seeded `64-VALIDATION.md` front matter is `status: draft`, `nyquist_compliant: false`, `wave_0_complete: false`; the planner binds each row to a task id. Phase 60 left its own file at `status: draft` (an acknowledged follow-up, `64-CONTEXT.md` "Deferred"), so the flags are the planner's to set, not an executor's.

---

### 14, 15, 16. `.planning/REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md` (hand edits at close)

**Analog:** commit `00f7f1bc` ("docs(planning): close phase 60"), the exact precedent. Its body states the boundary to copy: "REQUIREMENTS.md: only the four checkboxes and the four Traceability status cells change ... No requirement text moved (tests.phase60.test_amendment passes) ... STATE.md: the Current Position block reads ... status, stopped_at, last_updated, last_activity_desc, state_head and completed_phases are left to the orchestrator. Hand edits only, reviewed as one aggregate diff; no gsd-tools state, roadmap or requirements verb was run."

**REQUIREMENTS.md hunk shape** (checkbox and status cell only). Phase 64 targets, read at this HEAD: `:143` `- [ ] **FEAS-06**`, `:196` `- [ ] **FEAS-10**`, `:313` `- [ ] **VER-22**`; rows `:417-419` (`| FEAS-06 | Phase 64 | Pending |`, and the same for FEAS-10 and VER-22); counts at `:5` (Total 24), `:422-424` (Coverage), footer `:428`:
```diff
-- [ ] **FEAS-03**: **Rung 1, the supervised ceiling.** ...
+- [x] **FEAS-03**: **Rung 1, the supervised ceiling.** ...
...
-| INST-05 | Phase 60 | Pending |
-| FEAS-04 | Phase 60 | Pending |
+| INST-05 | Phase 60 | Complete |
+| FEAS-04 | Phase 60 | Complete (recorded as skipped: no rescue) |
```
The status vocabulary now in the table is `Complete`, `Pending`, and `Complete (recorded as skipped: no rescue)`. The 12 requirements of Phases 61 to 63 still read `Pending` (rows `:405-416`); how they are labelled is GAP-64-01, which the owner decides at checkpoint 1. Apply the label only as the owner approves, and keep the edit to the status cell.

**Guard to re-run after the edit:** `tests.phase60.test_amendment` (its locators accept `[ ]` or `[x]`, e.g. `r"- \[[ xX]\] \*\*FEAS-09\*\*: "`, `tests/phase60/test_amendment.py:331`). The verify command of `60-22-PLAN.md:135` is the template:
```bash
grep -Eq '^- \[x\] \*\*FEAS-06\*\*' .planning/REQUIREMENTS.md && grep -Eq '^- \[x\] \*\*FEAS-10\*\*' .planning/REQUIREMENTS.md && grep -Eq '^- \[x\] \*\*VER-22\*\*' .planning/REQUIREMENTS.md && $PY -B -m unittest tests.phase60.test_amendment && git diff --quiet HEAD -- .planning/REQUIREMENTS.md .planning/ROADMAP.md .planning/STATE.md
```
(the last clause confirms the three files are committed).

**ROADMAP.md hunk shape.** Phase 64 targets: the list item at `:152`, the Phase 64 section's `**Plans**: TBD` at `:396`, and the Progress row at `:407` (`| 64. Feasibility Verdict | 0/TBD | Not started | - |`). The Phase 60 close wrote:
```diff
-- [ ] **Phase 60: Single-System Learnability** — The project's first real answer to "can it learn?":
+- [x] **Phase 60: Single-System Learnability** (completed 2026-10-23, stopped at G2: no rescue) — The project's first real answer to "can it learn?":
...
-| 60. Single-System Learnability | 22/23 | In Progress | - |
+| 60. Single-System Learnability | 23/23 | Complete (stopped at G2: no rescue) | 2026-10-23 |
```
and ticked the executed plans in the phase's plan list. The count `24` also appears in `ROADMAP.md:29`, `:66`, `:67` and `:413-414` (and `PROJECT.md:340`); two of those lines carry creation-time history ("20/20 mapped at roadmap creation"), which the `traceability` check must not flag (RESEARCH "VER-22 mechanics").

**STATE.md hunk shape.** Only the Current Position block (`Phase:`, `Plan:`, `Status:`, `Last activity:`), a "Decisions from 64-NN" entry, and the progress counters change; the front-matter fields the orchestrator owns stay untouched (listed above):
```diff
-  completed_plans: 32
-  percent: 97
+  completed_plans: 33
+  percent: 100
...
-Phase: 60 (Single-System Learnability) — EXECUTING (...)
+Phase: 60 (Single-System Learnability) — COMPLETE (...)
```
Do not run `gsd-tools` state, roadmap or requirements mutating verbs (they regress these files; repeated in two commit bodies). Review one aggregate `git diff` of the three files, then commit them alone as `docs(planning): ...`. Do not auto-advance STATE or run `/gsd-complete-milestone` or merge (out of scope, `64-CONTEXT.md` "Deferred").

---

### 17. `.planning/PROJECT.md` (EDIT, on approval only)

**No analog for the rewrite.** `git log -S"## What This Is" -- .planning/PROJECT.md` returns only the initial commit `f4243afd`; the two sections have never been rewritten. Targets at this HEAD: `:1` the title line (`# Three-Body Physics-Informed LLM`), `:3-5` "What This Is", `:7-9` "Core Value", `:369` the Model constraint ("Qwen 3.5 2B 4-bit"); `FEAS-10` names only the middle two, so the title and Model lines are the optional extra pre-filled line (D-13). `:340` ("24 requirements") and `:368` (Hardware, already carrying the Mac-only rule) stay as they are.

**Closest precedent (commit style only):** `b10fb698` evolved `PROJECT.md` at the v2.3 close in a `docs(planning)` commit whose body lists what changed in each file and records the owner's decisions and the checks run. Write the rewrite as a separate commit whose body quotes the owner's approval, and apply it only if the ruling file (row 8) records the approval; the `ruling` mode checks that.

---

### 18. Gap registers (EDIT after the owner answers)

**Analog:** `.planning/milestones/v2.4-GAPS.md`: rows `:28-40` show the closed form (`RESOLVED-WITH-INSTRUCTION (2026-10-18)` plus a one-line outcome); GAP-64-01 is row `:41` (`**OPEN (owner-routed, checkpoint ①)**`) with its disposition paragraph at `:61`. Update both that row and `64-GAPS.md`'s `Status` and `Resolution note` (currently `—`) from the owner's recorded words. Subagents do not write gap registers; the parent agent does (repo `CLAUDE.md`, STOP protocol).

---

### 19. `64-NN-SUMMARY.md`

**Analog:** `58-SUMMARY.md` (front matter keys `phase`, `plan`, `subsystem`, `tags`, `requires`, `provides`, `affects`, `key-decisions`, `completed`, `status`; then per-requirement sections, a dispositions table and "Files Created"). For the checkpoint plan, `60-17-PLAN.md:196` requires the summary to quote the owner's message verbatim. The VER-21 closeout paragraph (`58-SUMMARY.md:43-64`) is the precedent wording for the VER-22 record: "compared every `- [ ] **ID**` definition ... 15 defined, 15 mapped, no duplicates, no orphans", with the caution that a passing count shows no orphans, not no gaps.

---

## Shared Patterns

### S1. Fail-closed CLI with one token per mode
**Source:** `verify_phase60_evidence.py:153-158`, `819-850`; `verify_phase59_evidence.py:1043-1079`. **Apply to:** row 1. Each mode raises `VerifyError` via `fail(...)`; `main` catches everything, prints the message to stderr and returns 1; success prints `<MODE>-OK` on its own line; `final` prints the aggregate token last. Tests assert `code == 0` plus the token in stdout, or `code == 1` plus `FAIL-CLOSED` in stderr.

### S2. Cite inputs by repo-relative path and SHA-256
**Source:** `P60/g2/stop-handoff.json` (`basis`, `arms[*].record`); `60-FINDINGS.md` "Evidence index" tables. **Apply to:** rows 3, 5, 6. No number is typed by hand; each traces to a file and key and is re-derived (RESEARCH Pattern 1).

### S3. Real shapes before any test
**Source:** `test_verifier_phase60.py:678-713`; user memory (Phase 60's verifier crashed on first real use twice). **Apply to:** rows 1, 10. Run each new mode read-only on the real committed files before writing its tests; the frozen `DataContext` dataclass, NumPy `ArmData`, real JSON records; never a tensor where the producer returns an array, never a context manager where it returns a plain object. `open_real_context` is called once per process, from the repository root (H6).

### S4. Plain language first
**Source:** `60-FINDINGS.md:1-12`; `P59/verify_phase59_evidence.py:977-979`; `test_evidence_verifier.py:1229-1234`. **Apply to:** rows 6, 7 (and any README). The first `##` heading is exactly `## In plain language`, an `Audience` line precedes it, and each term is defined once. The repo's document checks are mechanical, so the heading text is load-bearing.

### S5. Verbatim owner words in an opaque fence
**Source:** `learnability_ruling.py:1-27`; `60-17-PLAN.md:25, 129, 146`; `test_ruling.py:262-350`. **Apply to:** rows 7, 8. Info string exactly `owner-quote`; the fence is longer than any backtick or tilde run inside the message; the message is never parsed, evaluated, formatted into a path or command, or paraphrased; an ambiguous reply is asked again for that item only; items not addressed are recorded open.

### S6. Hand-edited registries, one aggregate diff
**Source:** commit `00f7f1bc`; `60-22-PLAN.md:132`. **Apply to:** rows 14 to 18. Scoped edits (checkbox, status cell, position block, counters), no `gsd-tools` mutating verb, one `git diff` over the files reviewed, committed alone as `docs(planning): ...` with a body.

### S7. Commit protocol
**Source:** `scripts/agent-commit:1-30`; `60-22-PLAN.md:184`; repo `CLAUDE.md`. **Apply to:** every commit. `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set (the script exits 1 if either is empty); explicit `git add -- <paths>`, never `-A`, `.` or `-u`; subject `<type>(<scope>): <lowercase imperative>` at most 80 characters with no quote character, tick or semicolon; a body for `spec`, `evidence`, `verify` and `plan` commits and for multi-file or `.planning/` commits; a `Co-Authored-By:` or `Agent-Assisted-By:` trailer; no push from `milestone/*`.

### S8. Expensive commands keep their full output outside the repo
**Source:** global `CLAUDE.md` evidence-reuse rules; `60-22-PLAN.md:84` (detached run with `$HOME/.cache/3bp-phase60-logs/`). **Apply to:** only if a command over 60 s becomes necessary. RESEARCH expects none: Phase 64 changes no `pinn/` file, so `tests/phase60` discovery (about 13 minutes, 992 tests) and Phase 59 `final` (about 604 s) are substituted by the cheap set in `64-VALIDATION.md`. If either reason stops holding, run once, detached, log retained, elapsed time recorded.

### S9. zsh-safe gates that cannot pass vacuously
**Source:** RESEARCH Code Example 4; user memory (unquoted multi-path variables do not word-split under zsh). **Apply to:** every plan `<automated>` clause over a path list: write the list to a temp file, expand `$(cat "$T")`, assert the argument count against `wc -l`, and run a negative control over a path known to change.

---

## No Analog Found

| File or sub-part | Role | Data Flow | Reason | Use instead |
|------------------|------|-----------|--------|-------------|
| `E64/figure-1632.svg` (row 4) | figure | transform | no tracked SVG and no tracked SVG-emitting code; `pinn-train` has no matplotlib | RESEARCH Code Example 5, Pitfalls 11 and 12 |
| Time-constant-predictor derivation (inside rows 1 and 2) | derivation | transform | the observation exists only in an uncommitted scratch script (`git grep` for "time-constant", "constant predictor" over `*.py` and `*.json` finds nothing); `60-VERIFICATION.md:392-446` records the result, not code | RESEARCH Code Example 1, built on the `cmd_rescore` load path above |
| Mac-only wording guard (inside row 1, `rules`) | content scan | transform | new rule from D-06; nothing in the repo scans documents for it | RESEARCH Code Example 6 and Pitfall 7 (scan set per H2) |
| `traceability` mode (row 1) | registry counter | batch | VER-21 was verified by hand and recorded only in `58-SUMMARY.md:43-64`; no script exists | RESEARCH Code Example 3 |
| D-01 side-by-side box, D-02 qualifier sentence, charter bars, budget, stop-rule margin (rows 6, 7) | prose content | docs | new content; no document states a pass bar or a charter | `64-CONTEXT.md` D-01 to D-13; `64-RESEARCH.md` "Charter inputs"; owner decides |
| `PROJECT.md` rewrite (row 17) | registry prose | docs | the two sections have not changed since the initial commit | the owner's approved charter lines |

---

## Hazards and corrections for the planner

**H1. Two pinned modules are import-only.** `pinn/verification/evidence_io.py` and `pinn/verification/learnability_ruling.py` are among the 33 `module_sha256` keys in `P60/run-protocol.json`, as are `learnability_data.py`, `learnability_arms.py`, `feasibility_scorer.py`, `feasibility_scorecard.py` and `P60/launch_phase60_arm.py`. Phase 64 may import them read-only; one byte changed makes `verify_phase60_evidence.py protocol` fail. This is why row 1 copies the fence parser instead of extending `learnability_ruling.py`.

**H2. The `rules` scans must not read files that legitimately contain the forbidden text.** `64-VALIDATION.md` and `64-RESEARCH.md` contain the host interpreter path; `64-CONTEXT.md` contains the owner's two Mac-only statements; plan files contain `<automated>` commands with the host path; the verifier and its tests contain the guard's own word list. Scan only the deliverables: `64-VERDICT.md`, `64-CHARTER.md` and `64-CHECKPOINT-1-RULING.md` (owner-quote fences stripped first), plus `E64/numbers.json`, `E64/figure-1632.svg` and `E64/figure-1632.provenance.json`. Build the home-path needle with `str(Path.home())` at run time (as `P59/verify_phase59_evidence.py:899` does), never as a literal in the verifier source. Note also that `P60/launch_phase60_arm.py:60` already commits a host path, so a repository-wide `/Users/` scan would fail on existing files.

**H3. Phase 64 adds files only under `.planning/phases/64-feasibility-verdict/`, `tests/phase64/` and the registries.** No `pinn/` file is added or edited. The marker-discovered static guards (`tests/phase60/test_static_guards.py:106-132` scan `pinn/verification/*.py` whose docstring starts "Phase 60" and the Phase 60 evidence tree) and the repository-wide prohibition scans (`tests/phase39/test_prohibitions.py:185` globs `pinn/**/*.py`) therefore do not see Phase 64 files. Keep it that way: reach the corpus only through `open_real_context`/`load_arm_data`, and give every `torch.load` the literal keyword `weights_only=True`.

**H4. Plan gates and zsh.** A plan clause that expands an unquoted path list passes without testing anything (S9). The generic post-merge wave gate also finds no Makefile or pyproject and passes on `true`, so each wave runs the commands in `64-VALIDATION.md` "Sampling Rate" instead.

**H5. `64-RESEARCH.md`'s embedded copy of the decisions is stale in four places; `64-CONTEXT.md` governs.** Verified this session by diffing the two. CONTEXT was corrected after the research (commit `377faebc`). (a) D-01: RESEARCH says "Its accuracy curves stayed flat"; CONTEXT says they "levelled off early ... Do not call them 'flat'" (E fell 25 to 50 fold in the first about 5% of training, then settled at 1.14 to 1.24). (b) D-05: RESEARCH says "not projected from the flat curves"; CONTEXT says "because the curves levelled off far above Tier 1". (c) D-12: CONTEXT adds that "beats" needs a stated margin and the draft proposes one as the default, the owner deciding (RESEARCH Open Question 2). (d) D-13: CONTEXT adds the optional title-line and Model-constraint rewrite (Open Question 3) and the GAP-64-01 line (option A as the default; the close task applies it only as the owner approves). RESEARCH's own Pitfall 4 and decision-coverage map already use the corrected wording, so only the `<user_constraints>` copy is stale. Quote CONTEXT.

**H6. Data-dependent modes run from the repository root.** `default_data_root()` shells out to `git rev-parse --git-common-dir` in the current directory (`pinn/data/adapter.py:603-606`) and fails with exit 128 from elsewhere (RESEARCH Finding 6). `os.chdir(REPO_ROOT)` at the start of `derive` and `figure`, and run them from the root. Without the dataset only the committed-JSON modes run.

**H7. The official numbers are MPS float32; re-derived numbers are CPU float64.** Every quoted `E`, `eps_H` and tier in `record.json` `result`/`score_gold` is the MPS figure; the CPU cross-check is stored in `states.<state>.cross_check` and differs in the third or fourth digit (for `r1-1632` polish: record `result.E` 1.157387, `cross_check.E` 1.159997). Label every number, and compare a CPU re-derivation only with `cross_check`, to 1e-12 (S1, row 1).

**H8. Do not rewrite or fill sealed records.** `stop-handoff.json` has `owner_answer: null` and `verdict_note: null` by design and is a hashed input; Phase 64 reads it and never edits it. The label is recomputed, never typed, and never amended (D-01; SCOPE-42, SCOPE-43).

**H9. The owner-quote rule differs by file.** Ruling file: exactly one `owner-quote` block. Charter: several, three of them byte-equal to `64-CONTEXT.md:68`, `:69`, `:72`. A copied "exactly one" check would reject the charter.

**H10. Commit and attribution details.** The Phase 60 plans quote their own session's model name in the trailer; the Phase 64 executor supplies its own. The commit-msg hook rejects quote characters in the subject.

### Mechanical choices left to the planner (presentation-only; note each in the plan)

- The verdict's pre-sign-off `status` value (row 6).
- Whether an `evidence/README.md` exists (Phase 59 shipped one and tests its heading; the RESEARCH structure does not list one).
- Whether `final` includes `derive` and `figure` (row 1: the precedents split; RESEARCH includes them).
- Whether the frozen-path list is derived or committed (row 11; derivation recommended).
- Whether the provenance record reuses `evidence_io.provenance_record` with its schema key overridden, or is written fresh (row 2).

No new gap is raised by this mapping. GAP-64-01 is already recorded (`64-GAPS.md`, `v2.4-GAPS.md:41`) and stays owner-routed at checkpoint 1.

---

## Metadata

**Analog search scope:** `.planning/phases/{57,58,59,60,64}/`, `.planning/milestones/v2.0-phases/43-*/`, `.planning/milestones/v2.4-GAPS.md`, `.planning/{REQUIREMENTS,ROADMAP,STATE,PROJECT}.md`, `pinn/verification/`, `pinn/data/adapter.py`, `tests/phase{59,60}/`, `docs/work/designs/{milestone_v2.3,cross_cutting/v2.4-milestone-proposal}/`, `docs/runbooks/external-research/`, `scripts/`; commits `00f7f1bc`, `b10fb698`, `377faebc`.
**Files read for excerpts:** about 50; about 55 candidate paths checked with `git ls-files`.
**Pattern extraction date:** 2026-10-25
**Tooling note:** the Sequential Thinking MCP that repo `CLAUDE.md` asks for was not available in this toolset, as in the research session; the context-mode tools could not be loaded (no tool-search facility), so all reads used Read and Bash. No source file was modified; this file is the only write.
