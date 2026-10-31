# Phase 66: Small-Network Control - Pattern Map

**Mapped:** 2026-10-31 (Saturday), America/Chicago. HEAD `a5931bc7` on `milestone/v2.5`; every line number below is at that HEAD.
**Files classified:** 20 table rows, covering 21 authored paths (3 source, 8 test, 4 page/doc, 4 registration, 2 hand-edited state files) and 16 harness- or launcher-generated evidence files.
**Analogs found:** 20 / 20 rows have a tracked analog: 11 exact, 8 role-match, 1 partial (the reading-rule classifier).
**Scope:** `66-CONTEXT.md` (D-01..D-12) and `66-RESEARCH.md` (Patterns 1-7, Validation Architecture). New implementation names are RESEARCH's proposed layout, not locked decisions. Read-only mapping: no test, training, timing, MPS or Stage-0 read was run.

## Planner flags (read first)

Items found while mapping that RESEARCH did not state, or states differently. Each is verified against the tree.

1. **`evidence/runs/` is gitignored.** `.gitignore:339` is the bare pattern `runs/` (Phase 42 training-run output), so it matches a directory named `runs` at any depth. `git check-ignore -v` reports `.planning/phases/66-small-network-control/evidence/runs/main-1632-s42/record.json <= .gitignore:339:runs/`. RESEARCH's layout and diagram use `evidence/runs/{main-1632-s42,repeat-851-s42,repeat-1632-s41}/...` and `evidence/runs/*-registration.json`. A plain `git add` of those paths is refused, and admission needs tracked-clean files (`diagnostic_guard.py:373-377, 397-401`). Force-adding is possible (169 files under the top-level `runs/` are tracked and no hook refuses them), but it is a footgun for every file. Verified not ignored: `evidence/timing/`, `evidence/fit/`, `evidence/exp01/`, `evidence/experiments/`, `evidence/fits/`, `evidence/main/`. Phase 65 used `evidence/fit/<run>/`. Pick a non-`runs` name.
2. **`66-REVIEW.md` is the code-review artifact name.** `65-REVIEW.md` is the `gsd-code-reviewer` output (frontmatter `files_reviewed`, `findings`, `status: issues_found`), and `65-CLOSEOUT.md:62-63` calls it "the retained review record". RESEARCH uses `66-REVIEW.md` for the owner-checkpoint-1 reading. If the code-review step also writes `66-REVIEW.md` they collide. Phase 64's precedent keeps the checkpoint record separate: `64-CHECKPOINT-1-RULING.md` beside `64-VERDICT.md`. The planner should choose distinct names (see row 19).
3. **`--output` is the `record.json` path, not a directory.** `fit_diagnostic` hard-codes `RECORD_NAME = "record.json"` (`diagnostic_fit.py:126, 825`), and `_cmd_run` sets `record_path = Path(output_path)` with the attempt at `record_path.parent / "attempt.json"` (`:1459-1466`). So `diagnostic_power launch --output O` must end in `record.json`, and the receipt directory is `Path(O).parent`. RESEARCH Pattern 3 says "output directory"; read it that way.
4. **The receipt must not carry `sys.executable` or the exec argv.** `evidence_io.guard_redaction` (`evidence_io.py:143-151`) refuses any text containing `Path.home()`, and the pinned interpreter lives under `<home>/...`. Write `power-gate.json` with `learnability_arms.write_record_exclusive` (`:435-465`) so the redaction guard, canonical JSON and `O_EXCL` apply, and record repo-relative paths only.
5. **The registration schema literal stays `phase65-fit-registration/v1`.** `load_fit_registration` (`diagnostic_fit.py:290-291`) and `require_committed_registration` (`diagnostic_guard.py:361-366`) accept only that fit schema and the probe schema. A new `phase66-...` schema string would force an edit to the pinned `diagnostic_guard.py`.
6. **Admission still demands Phase 65's settings keys.** `validate_smoke_settings` (`diagnostic_fit.py:317-440`) requires `reading_rule` with truthy `mechanical_pass`, `incomplete` and `out_of_branch` (`:434-439`), truthy `timing_definitions` (`:432`), `optimizer.kind == "adam_constant_rate"` with null `scheduler`, `clipping`, `physics_term`, `polish` (`:417-428`), `loss.kind == "data_only"` (`:429-431`), a cap in (0, 3600) (`:408-416`), a cadence that starts at 0 and ends at `optimizer_steps` (`:393-407`), and `measured_steps == optimizer_steps - warmup_steps` (`:388-392`). The EXP-01 branch rule (TIER1, NEAR, BETWEEN, OTHER) lives on the page and may sit in extra `reading_rule` keys, which admission ignores. This is also why a new `settings.variant_registry` key can ride along without a schema change.
7. **`resolve_variant(str)` consults only the sealed `REGISTRY`** (`diagnostic_variants.py:165-170`), and `fit_diagnostic` calls it at `diagnostic_fit.py:791`. Phase 65 tests pass string names (`fit_diagnostic("locked-12", ...)` at `test_fit_short.py:124, 1246`). Phase 66 tests and any new call site must pass the `DiagnosticVariant` object, as `run_registered_smoke` already does (`:1146-1147`, the object returned by `validate_smoke_settings`).
8. **Import cycle.** `diagnostic_fit.py` will import `REGISTRIES` from `diagnostic_phase66.py`. Keep `diagnostic_phase66.py` free of any `diagnostic_fit` import: it needs only `diagnostic_variants`, and `classify_exp01` and `confirm` are pure functions.
9. **Test sequencing.** `66-VALIDATION.md` lists `test_pages.py` under Wave 0, but its real-page assertions need `66-TIMING-PREDICTION.md` and `66-PREDICTION.md`, which exist only after the harness freeze. Phase 65's `RegistrationContentTests` (`test_probe.py:1292`) reads real committed artifacts and so could only exist once they did. Split `test_pages.py` into a synthetic part (Wave 0) and a real-file part that lands with each page.
10. **Pinned analogs are read-only.** `launch_phase60_arm.py`, `evidence_io.py`, `learnability_arms.py`, `split_allowlist.py`, `network.py`, `architecture_spec.py`, `constants.py` and `diagnostic_architecture.py` are among the 33 `PINNED_MODULES` (`learnability_protocol.py:145-179`). None of `diagnostic_fit/guard/data/variants/similarity` is in that list, so the planned `diagnostic_fit.py` edit does not trip `load_protocol()`. It only retires registrations that pin `diagnostic_fit.py` by digest (the Phase 65 smoke), as `65-CLOSEOUT.md:86-89` anticipates.
11. **The historical-bytes anchor is not the registration's introducing commit.** RESEARCH's `test_diagnostic_fit_matches_at_the_introducing_commit` and `65-CLOSEOUT.md:108` point at `ac4358cb`. The smoke registration was amended at `b1dcacc4` (`fix(65-06)`) before the run: at `ac4358cb` it pinned `diagnostic_fit.py` at `b724d36c...`, and that file's blob does not hash to the recorded `b00e45b4...` until `b1dcacc4`. Anchor the test on the commit that added the smoke `record.json` (`84128fe2`). Verified: at `84128fe2` the registration bytes, the record's `registration.sha256` (`ba54e812...`) and all five code-dependency digests agree (section 12).

## File Classification

All source paths are under `pinn/verification/`; test paths are under `tests/phase66/`; page and evidence paths are under `.planning/phases/66-small-network-control/`. The evidence directory name is a planner choice (flag 1).

| # | New/modified file | Role | Data flow | Closest tracked analog | Quality |
|---|---|---|---|---|---|
| 1 | `diagnostic_phase66.py` (catalog: `EXP01_VARIANT`, `PHASE66_REGISTRY`, `REGISTRIES`) | config/model | transform | `diagnostic_variants.py` | exact |
| 2 | `diagnostic_phase66.py` (`classify_exp01`, `confirm`) | utility | transform | `tests/phase64/test_verifier_phase64.py:1292-1310` and `.planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py:1187-1192` | partial |
| 3 | `diagnostic_power.py` (AC gate, `launch`, `check`, receipt) | middleware | request-response (CLI) + file-I/O | `scripts/phase60_run_control.py:96-112` (counter-example), `launch_phase60_arm.py:60-61, 118-122`, `diagnostic_fit.py:1505-1566`, `learnability_arms.py:435-465` | role-match |
| 4 | `diagnostic_fit.py` (modify, about 25 lines) | service | batch + file-I/O | itself (five edit sites) | exact |
| 5 | `__init__.py` | test | n/a | `tests/phase65/__init__.py` | exact |
| 6 | `test_catalog.py` | test | transform | `tests/phase65/test_contracts.py:57-162` | exact |
| 7 | `test_admission.py` | test | file-I/O (throwaway git repos) | `tests/phase65/test_fit_short.py:513-856` | exact |
| 8 | `test_records.py` | test | batch | `tests/phase65/test_fit_short.py:101-135, 1051-1091, 1208-1305` | exact |
| 9 | `test_reading_rule.py` | test | transform | `tests/phase64/test_verifier_phase64.py:1292-1310` | role-match |
| 10 | `test_power.py` | test | request-response (fakes) | `tests/phase60/test_launcher.py:124-141, 222-232` | role-match |
| 11 | `test_pages.py` | test | file-I/O (static) | `tests/phase65/test_probe.py:1292-1306, 1484-1494` | role-match |
| 12 | `test_historical.py` | test | file-I/O (git) | `tests/phase65/test_probe.py:1428-1462` | exact |
| 13 | `66-TIMING-PREDICTION.md` | doc (mechanics-only page) | n/a | `.planning/phases/65-probe-on-the-record-fit-harness/65-SMOKE-PREDICTION.md` | exact |
| 14 | `66-PREDICTION.md` | doc (full prediction page) | n/a | `65-SMOKE-PREDICTION.md` plus `65-PROBE-PREDICTION.md:66-103` | role-match |
| 15 | timing registration plus three experiment registrations | config | file-I/O | `.planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/smoke-registration.json` | exact |
| 16 | per-run `record.json`, `diagnostic.weights`, `attempt.json` (generated, 12 files) | evidence | file-I/O | `.planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/1632-smoke/` | exact |
| 17 | per-run `power-gate.json` (generated, 4 files) | evidence | file-I/O | `attempt.json` payload from `_claim_attempt` (`diagnostic_fit.py:1045-1069`) | role-match |
| 18 | `66-CLOSEOUT.md` | doc | n/a | `65-CLOSEOUT.md` | exact |
| 19 | checkpoint-1 record and plain-language reading (RESEARCH: `66-REVIEW.md`; see flag 2) | doc | n/a | `64-CHECKPOINT-1-RULING.md`, `64-VERDICT.md:26-35, 215-248`, `65-FINDINGS.md` | role-match |
| 20 | `.planning/REQUIREMENTS.md`, `.planning/STATE.md` (hand edits at close) | state | n/a | `65-CLOSEOUT.md:141-146`, `STATE.md:50-52` | role-match |

## Pattern Assignments

### 1. `diagnostic_phase66.py`: the variant catalog (config/model, transform)

**Analog:** `pinn/verification/diagnostic_variants.py`. Its header states the contract this file fulfils (`:14-17`): the registry is "deliberately small", later phases "register their own approved designs through `register_variant`, which never alters the sealed catalog and refuses duplicate names." Copy the docstring style (`"""Phase 66 (EXP-01): ..."""`), `from __future__ import annotations`, absolute `pinn.` imports and an explicit `__all__` (`:35-47`).

**Sealed entry and registry** (`diagnostic_variants.py:138-149`):
```python
LOCKED_12 = DiagnosticVariant(
    name="locked-12",
    time_features="raw_tau_ic13",
    depth=12,
    width=256,
    learning_rate=1e-4,
    window_length=10.0,
)
REGISTRY = MappingProxyType({"locked-12": LOCKED_12})
```

**Registration semantics** (`:176-195`, messages elided): returns a new immutable registry and refuses duplicates.
```python
registry = REGISTRY if into is None else into
if not isinstance(variant, DiagnosticVariant):
    raise VariantRefused(...)
if variant.name in registry:
    raise VariantRefused(...)
return MappingProxyType({**registry, variant.name: variant})
```

**Adaptation** (RESEARCH "Catalog module"; imports only `diagnostic_variants` and `types`, see flag 8):
```python
EXP01_VARIANT = DiagnosticVariant(
    name="exp01-d1-w384-o1000", time_features="raw_tau_ic13", depth=1, width=384,
    learning_rate=1e-4, window_length=10.0, first_omega_0=1000.0)
PHASE66_REGISTRY = register_variant(EXP01_VARIANT, into=REGISTRY)
REGISTRIES = MappingProxyType({"phase66": PHASE66_REGISTRY})
```
Facts the file relies on: the name regex is `[a-z0-9][a-z0-9-]*` (`:50`); `hidden_omega_0` defaults to the locked constant (`:84`), which is D-06's 1.0; `window_length` is capped at 10.0 (`:59, 114-118`); `to_json_dict()` (`:120-132`) is the byte-agreeing block that admission compares (`diagnostic_fit.py:338-343`) and that `test_pages.py` compares to the page. `build_variant` (`:203-223`) already builds depth 1 by replacing only `hidden_depth`, `hidden_width`, `first_omega_0`, `hidden_omega_0` on a copy of `ArchitectureSpec(seed)`, so no builder change is needed. Do not edit `diagnostic_variants.py`: the smoke registration pins its digest `ad8ed66c...`.

### 2. `diagnostic_phase66.py`: `classify_exp01` and `confirm` (utility, transform)

**Analog (partial, rule only):** no tracked branch classifier exists. The closest precedents are how Phase 64 reads Tier 1 and how its tests pin the inclusive edge.

Scorecard (`pinn/verification/artifacts/feasibility_scorecard_v1.json:614, 627-629`): `"comparison": "inclusive_le"`, Tier 1 `"E_max": 0.1`, `"tier": 1`. Phase 64 reads the limit from the scorecard instead of retyping it (`verify_phase64_verdict.py:1187-1192`):
```python
def _tier1_max(card: Any) -> float:
    """The scorecard's Tier-1 E_max, read from its own tiers section."""
    for level in card.section("tiers")["levels"]:
        if int(level["tier"]) == 1:
            return float(level["E_max"])
    fail("the scorecard names no level whose tier is 1")
```
Test precedent for the exact edge (`test_verifier_phase64.py:1292-1310`): one test ties the limit to the scorecard (`self.assertEqual(card.section("tiers")["comparison"], "inclusive_le")`), another feeds `[0.1, 0.1000001, 0.05, 0.0]` and asserts exactly the in-limit values count.

**Adaptation** (RESEARCH "Reading rule", with the limit passed in rather than hand-typed, so the unit test can bind it to the scorecard):
```python
def classify_exp01(e, e_const, *, tier1_max, band=0.05):
    if not math.isfinite(e):
        return "other"
    if e <= tier1_max:
        return "tier1"
    lo, hi = (1 - band) * e_const, (1 + band) * e_const
    if lo <= e <= hi:
        return "near"
    return "between" if e < lo else "other"
```
`e_const` is the record's own `comparisons[window_mean_constant].score.E`, never a retyped figure (RESEARCH Pitfall 5). Committed values for the page: 1632 `1.1538408194255343` (`64-feasibility-verdict/evidence/numbers.json` entries[170] `cpu.const.1632.E`, equal to the Phase 65 smoke record's comparison row) and 851 `1.233696866477104` (entries[172] `cpu.const.851.E`). `confirm(main, r1, r2)` takes the three branch labels. Keep both functions free of any harness import.

### 3. `diagnostic_power.py`: the AC-power launch gate (middleware, request-response + file-I/O)

Composed from four tracked precedents plus one counter-example. Entry shape: `main(argv=None) -> int` with `if __name__ == "__main__": sys.exit(main())` (`diagnostic_fit.py:1569-1570`), subcommands `launch` and `check`.

**Counter-example, do not copy** (`scripts/phase60_run_control.py:96-98, 108-112`). Fail-open: a missing or garbled `pmset` reads as "not on battery".
```python
def _run(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
    return subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False, **kwargs)

def on_battery() -> bool:
    try:
        return "Battery Power" in _run(["pmset", "-g", "batt"]).stdout
    except OSError:
        return False
```
Keep its `_run` shape (argv list, `stdin=DEVNULL`, `capture_output`, `text`, `check=False`) and add `timeout=`. The gate must instead parse the first line positively and refuse on anything else. Verified this session: `/usr/bin/pmset -g batt` first line is exactly `Now drawing from 'AC Power'` followed by `\n`.

**Command composition** (`launch_phase60_arm.py:60-61, 118-122`): argv-list construction, never a shell.
```python
PINNED_PYTHON = "<home>/miniforge3/envs/pinn-train/bin/python"
CAFFEINATE = "/usr/bin/caffeinate"
...
argv = [CAFFEINATE, "-is", PINNED_PYTHON, "-B", "-m", RUNNER_MODULE, _catalog_arm(arm_id)]
```
Target argv: `[CAFFEINATE, "-is", sys.executable, "-B", "-m", "pinn.verification.diagnostic_fit", "run", "--registration", R, "--output", O]`. There is no tracked Python `os.exec*` call in `pinn/`, `scripts/`, the Phase 60 evidence directory or `tools/` (a grep of `*.py` returned nothing); the tracked precedents are argv-list plus `subprocess` (above) and the shell `exec` of the pinned interpreter at `scripts/phase60-power-guard.sh:18`. RESEARCH proposes `os.execv`; either choice must write the receipt before the process image changes, and `launch_phase60_arm.py` is pinned, so read it, never edit it.

**CLI conventions** (`diagnostic_fit.py:1534-1545, 1564-1566`): a `required` map per command, `FIT-REFUSED: ...` to stderr, exit code 2.
```python
missing = [f"--{name}" for name in required if getattr(args, name) is None]
if missing:
    print(f"FIT-REFUSED: missing required flags: {', '.join(missing)}", file=sys.stderr)
    return 2
...
except (DiagnosticFitRefused, DiagnosticRegistrationRefused, FirstResultExists) as exc:
    print(f"FIT-REFUSED: {exc}", file=sys.stderr)
    return 2
```
Define a typed refusal in the style of `DiagnosticRegistrationRefused` (`diagnostic_guard.py:53-60`: `class X(RuntimeError)` with a docstring saying when it is raised and what has not happened yet). On refusal nothing is created, because the gate precedes `diagnostic_fit run`.

**Receipt** (`learnability_arms.py:435-465`): `write_record_exclusive(path, payload)` does `reject_evidence_root`, `canonical_json_bytes` (sorted keys, indent 2, ASCII, trailing newline, `evidence_io.py:131-140`), `guard_redaction`, `os.open(..., O_CREAT | O_EXCL | O_WRONLY)` and fsyncs, raising `FirstResultExists` on a second write. Payload timestamps follow `_claim_attempt` (`diagnostic_fit.py:1056-1067`): `datetime.now(timezone.utc).isoformat(timespec="seconds")`. Keep it to checked UTC time, the power source token, the raw first line, repo-relative registration and output, and load average (flag 4). The harness creates only `attempt.json`, `record.json` and `diagnostic.weights` in that directory (`_claim_attempt` uses `O_EXCL` on `attempt.json` alone, `:1054-1068`), so a pre-existing `power-gate.json` does not collide.

### 4. `diagnostic_fit.py`: the registry-aware edit (service, batch + file-I/O)

Five edit sites; everything else is untouched. After the edit this file's digest changes (flag 10).

**Site A, imports** (`:61-99`). The diagnostic imports are alphabetical: `diagnostic_data`, `diagnostic_guard`, `diagnostic_similarity`, `diagnostic_variants`. Insert `from pinn.verification.diagnostic_phase66 import REGISTRIES` between `diagnostic_guard` (`:71-80`) and `diagnostic_similarity` (`:81`). `REGISTRY` stays imported from `diagnostic_variants` (`:83`).

**Site B, `validate_smoke_settings`** (`:331-343`). Replace only the `try/resolve_variant/except` (`:334-337`); keep the byte-agreement loop (`:338-343`) and the 4-tuple return (`:440`) unchanged.
```python
    variant_block = settings.get("variant")
    if not isinstance(variant_block, Mapping) or not isinstance(variant_block.get("name"), str):
        raise DiagnosticFitRefused("the settings name no diagnostic variant")
    try:
        variant = resolve_variant(variant_block["name"])        # :334-337  <- replace
    except VariantRefused as exc:
        raise DiagnosticFitRefused(str(exc)) from exc
    for field, value in variant.to_json_dict().items():          # :338  keep
        if variant_block.get(field) != value:
```
Replacement per RESEARCH "Registry-aware lookup": a `_named_registry(name)` helper (None gives the sealed `REGISTRY` object itself, so Phase 65 behaviour is identical; a non-string or unknown name raises `DiagnosticFitRefused`), then `registry[variant_block["name"]]` with the unknown-name refusal listing `list(registry)`. Place the helper beside `_parse_orbit_key` (`:295`).

**Site C, `fit_diagnostic`** (signature `:750-772`, record `:976-979`). Add `variant_registry=None` after `run_context=None`. `resolved = resolve_variant(variant)` (`:791`) stays, because callers pass the object (flag 7). Current record block:
```python
        "variant": {
            **resolved.to_json_dict(),
            "registered": resolved.name in REGISTRY,
        },
```
Change `registered` to test membership in the selected registry and add a `registry` field. Keep the Phase 65 default intact: locked-12 under the default must still record `registered: True`.

**Site D, `run_registered_smoke`** (`:1146-1184`). Add one keyword to the `fit_diagnostic(...)` call, next to `seed=int(settings["seed"])` (`:1159`): `variant_registry=settings.get("variant_registry"),`. Nothing else in this function changes.

**Site E, `verify_fit_result`** (`:1308-1317`). Add one more `check(...)` after the per-field loop:
```python
    variant_block = record.get("variant") or {}
    check(variant_block.get("name") == settings["variant"]["name"],
          "the result's variant is not the registered variant")
    for field, value in variant.to_json_dict().items():
        check(variant_block.get(field) == value,
              f"the result's variant field {field} disagrees with the registration")
```
New check: `variant_block.get("registry") == settings.get("variant_registry")`. A Phase 65-shaped record (no `registry` key) against a registration with no `variant_registry` gives `None == None` and still verifies, which `test_records.py` must assert.

### 5. `tests/phase66/__init__.py` (test)

**Analog:** `tests/phase65/__init__.py`, one line: `"""Phase 65 synthetic test package (INST-08 / DIAG-09 Wave 0)."""`. Use `"""Phase 66 synthetic test package (EXP-01 Wave 0)."""`. There is no `tests/__init__.py`; `python -B -m unittest discover -s tests/phase66 -t .` works the way Phase 65's does.

### 6. `test_catalog.py` (test, transform)

**Analog:** `tests/phase65/test_contracts.py::RegistryContractTests` (`:57-162`). Module docstring states plan and requirement (`:1-12`); imports `:14-44`. Core assertions to mirror:
```python
def test_the_registry_holds_exactly_the_sealed_entry_and_no_ladders(self):    # :60-62
    self.assertEqual(list(REGISTRY), ["locked-12"])
    self.assertIs(REGISTRY["locked-12"], LOCKED_12)

def test_register_variant_refuses_duplicate_names(self):                      # :90-105
    register = _symbol(self, "register_variant")
    with self.assertRaises(diagnostic_variants.VariantRefused) as caught:
        register(LOCKED_12)
    self.assertIn("locked-12", str(caught.exception))
    ...
    extended = register(approved)
    self.assertIn("probe-depth4", extended)
    self.assertNotIn("probe-depth4", REGISTRY)  # the sealed catalog is unchanged
```
Also mirror immutability (`:75-79`, `TypeError` on item assignment, `AttributeError` on `pop`) and order (`:107-120`, `names(extended)`). Phase 66 adds: `EXP01_VARIANT` fields equal the page; the built model is `SQRSkipResNetSIREN` with `model.input_layer.omega_0 == 1000.0` and `len(model.hidden_layers) == 1` (attribute names verified in `pinn/network.py:169, 191, 194`); parameter count 157,065 via `sum(p.numel() for p in build_variant(EXP01_VARIANT, seed=42, dtype=torch.float64, device=CPU).parameters())`; and `ArchitectureSpec(hidden_depth=1)` still raises `ValueError` (`pinn/architecture_spec.py:88-92`).

### 7. `test_admission.py` (test, file-I/O in throwaway git repos)

**Analog:** `tests/phase65/test_fit_short.py::FitRegistrationAdmissionTests` (`:716-856`). Import the helpers rather than copy them, as `test_contracts.py:44` does for `_loaded`: `_fit_registration_fixture` (`:551-669`), `_smoke_settings` (`:513-548`), `_fit_symbols` (`:672-682`), `_NoDataNoOptimizer` (`:685-713`).

`_smoke_settings(**overrides)` ends with `settings.update(overrides)` (`:547`), and `_fit_registration_fixture` builds `settings = _smoke_settings(**(settings_extra or {}))` (`:622`), so one `settings_extra` carries the Phase 66 pair. The fixture pins a synthetic `fit_dep.py` (`:589`), never the live harness, so Phase 66 tests are independent of real digests.
```python
class FitRegistrationAdmissionTests(unittest.TestCase):
    def setUp(self):                                                    # :720-728
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.tmp = Path(self.stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase65-fitreg-")))
        self.fit, self.symbols = _fit_symbols(self)
        self.guard = _module(self, "diagnostic_guard")
        self.nodata = self.stack.enter_context(_NoDataNoOptimizer()(self))

    def test_a_committed_matching_registration_admits(self):            # :730-737
        root, commit = _fit_registration_fixture(self.tmp / "ok")
        admitted_root, doc = self.symbols["admission"](
            root / "reg/smoke-registration.json", repo_root=root)
```
Adapt with `settings_extra={"variant": EXP01_VARIANT.to_json_dict(), "variant_registry": "phase66"}`. The refusal matrix to re-run for the EXP01 variant is the `cases` dict at `:811-834` inside a `subTest` loop; the cap tests are `:790-809` (`for cap in (3600, 7200)` refuse, `3599.5` passes); the MPS gate tests patch `torch.backends.mps.is_available` (`:836-856`). Registry-name cases to add: `"phase65"`, `""`, `7`, `["phase66"]` refuse; null behaves as the sealed default; locked-12 under `"phase66"` admits; EXP01 under the default or null refuses.

### 8. `test_records.py` (test, batch)

**Analog:** three pieces of `tests/phase65/test_fit_short.py`.

(a) Shared fit for record assertions, `ShortFitTests.setUpClass` (`:104-135`):
```python
stack = ExitStack()
cls.addClassCleanup(stack.close)
cls.fixture = stack.enter_context(gold_corpus_fixture())
cls.spec, cls.context, cls.scorecard, cls.data = _loaded(cls.fixture)
...
cls.record = cls.fit.fit_diagnostic(
    "locked-12", cls.data, context=cls.context, scorecard=cls.scorecard,
    runtime=FIXTURE_RUNTIME, evidence_root=cls.root, steps=2,
    times_physical=cls.data.score.times, seed=SEED)
```
Phase 66: pass `EXP01_VARIANT` (flag 7) with `variant_registry="phase66"`; assert `variant.registered is True`, `variant.registry == "phase66"`, similarity rows exactly `["input", "h1"]` (the logger hooks `input` and `h{order}`, `diagnostic_similarity.py:208-210`), the `scores.network` block, and both comparison rows.

(b) End-to-end registered run, `AttemptOwnershipTests._patched_data` (`:1051-1069`) with `test_a_registered_run_publishes_once_and_marks_the_attempt` (`:1071-1091`). RESEARCH's `test_records` list does not cover `run_registered_smoke` passing `settings["variant_registry"]` through (Site D), and this is the only existing way to test it: build the fixture registration with the Phase 66 pair, patch the data seam, run `run_registered_smoke`, then assert the published record's `variant.registry == "phase66"`.

(c) Verification, `VerifyResultTests` (`:1208-1305`): the attestation shim in `setUp` (`:1220-1233`), the `_record` builder (`:1242-1268`, calls `fit_diagnostic` with `registration_provenance` and `logger_parity_provenance`) and `test_a_complete_agreeing_record_verifies` (`:1270-1275`). Adapt `_record` to the Phase 66 variant, then add the registry-mismatch refusal and the Phase 65-shaped no-`registry` record that still verifies (Site E).

Record field paths for the scripted real-record checks (verified against the committed Phase 65 smoke record): `scores.network.{tier,E,eps_h}`; `comparisons` is a list of rows with `comparison` in `{"window_mean_constant","two_kepler"}` and `score.E` (the Kepler row also carries `applicable`); `similarity.entries[*].layers[*].{name,adjacent_cosine_mean}`; `similarity.entries[*].first_layer_frequency.{median,max}` (computed as `weight[:, 0].abs() * omega / math.pi`, `diagnostic_similarity.py:224-227`); `loss.{final,trace}`; `timing.{seconds_per_step,end_to_end_seconds_per_completed_step,warmup_seconds,phases}`; `access.{reads,attestation,stage0}`; `registration.{path,sha256}`; `weights.{file,sha256,tensor_digest}`.

### 9. `test_reading_rule.py` (test, transform)

**Analog:** `tests/phase64/test_verifier_phase64.py:1292-1310`.
```python
def test_the_tier1_limit_is_the_scorecards_inclusive_0_1(self):
    card = load_scorecard()
    self.assertEqual(self.verifier._tier1_max(card), 0.1)
    self.assertEqual(card.section("tiers")["comparison"], "inclusive_le")

def test_within_tier1_counts_an_error_of_exactly_the_limit(self):
    derived = {"e_sys": np.array([0.1, 0.1000001, 0.05, 0.0], dtype=np.float64), ...}
    ...
    # 0.1 is inside the tier; 0.1000001 is the one moment excluded.
    self.assertEqual(count, 3)
```
Apply to `classify_exp01`: `E == 0.1` is `tier1`; the next float above `0.1` (use `math.nextafter`) is not; each band edge `0.95*E_const` and `1.05*E_const` is `near`; just inside and just outside the edges; NaN and infinity are `other`; both systems' `E_const` constants (flag in section 2). Tie the Tier-1 limit to the scorecard in one test, as above. `confirm` gets the full 3-branch truth table.

### 10. `test_power.py` (test, request-response with fakes)

**Analog:** `tests/phase60/test_launcher.py`. Safety-net setUp (`:124-141`): patch the real binary away (`mock.patch.object(launcher, "CAFFEINATE", "/usr/bin/true")`) and make the host probe fail the test if reached. Exact-argv assertion (`:222-232`):
```python
class ArmArgvTests(unittest.TestCase):
    def test_a_fresh_arm_command_is_caffeinate_over_the_pinned_runner(self):
        self.assertEqual(
            launcher.arm_argv("r1-1632", resume=False),
            ["/usr/bin/caffeinate", "-is",
             "<home>/miniforge3/envs/pinn-train/bin/python",
             "-B", "-m", "pinn.verification.learnability_run", "r1-1632"],
        )
```
No existing test fakes `pmset` (grep for `pmset|on_battery|caffeinate` under `tests/` found only the launcher and `tests/phase42/test_wrapper_exit.py:20`, a real-caffeinate skip guard), so the fake-`run` injection `require_ac_power(run=...)` is new. Cases (RESEARCH Pattern 3): AC first line passes; `Battery Power`, `UPS Power`, empty, garbage, `'AC Power'` appearing only on a later line, nonzero exit, `FileNotFoundError` and timeout all refuse; on refusal the exec or subprocess spy and `diagnostic_fit` are never reached and no output directory is created; on AC the spy receives exactly the target argv from section 3. Keep the real-`pmset` check out of the unit suite; it is the separate acceptance command `python -B -m pinn.verification.diagnostic_power check`.

### 11. `test_pages.py` (test, static file-I/O)

**Analog:** `tests/phase65/test_probe.py::RegistrationContentTests` (`:1292-1306` helpers, `:1484-1494` page test).
```python
@classmethod
def _phase_dir(cls):
    return (Path(__file__).resolve().parents[2]
            / ".planning/phases/65-probe-on-the-record-fit-harness")

def test_the_page_is_named_and_the_reading_rule_is_immutable(self):
    doc = self._registration()
    page = self._phase_dir() / "65-PROBE-PREDICTION.md"
    self.assertTrue(page.is_file())
    self.assertEqual(hashlib.sha256(page.read_bytes()).hexdigest(), doc["page"]["sha256"])
    text = page.read_text()
    for branch in ("retained", "withdrawn", "SCOPE-49", "provenance"):
        self.assertIn(branch, text)
```
Adapt to: each Phase 66 registration's `page.sha256` equals its page; the page's machine-checkable variant block equals `EXP01_VARIANT.to_json_dict()`; the timing page and the main page carry the same design block; band numbers equal 0.95 and 1.05 times the two `E_const` constants. When asserting a number appears, use digit-boundary matching: Phase 64's `test_digit_boundary_does_not_match_inside_a_longer_number` (`test_verifier_phase64.py:2346-2352`) records that a plain substring match accepts `0.01` inside `0.010856`. Use the same mutate-and-reject style (`:2341-2344`: replace a number in the page text and assert the check fails). There is no existing fenced-JSON extractor (see No Analog Found). Flag 9 applies: real-file assertions can only be committed with the pages.

### 12. `test_historical.py` (test, file-I/O via git)

**Analog:** `tests/phase65/test_probe.py:1428-1462`, `test_recorded_dependencies_match_the_historical_run_commit`.
```python
def git(*args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=True).stdout

registration_commit = git(
    "log", "-n1", "--format=%H", "--diff-filter=A", "--", relative).decode().strip()
...
git("merge-base", "--is-ancestor", registration_commit, run_commit)
git("merge-base", "--is-ancestor", run_commit, "HEAD")
...
for entry in doc["code_dependencies"]:
    committed = git("show", f"{run_commit}:{entry['path']}")
    self.assertEqual(hashlib.sha256(committed).hexdigest(), entry["sha256"])
```
Adapt to the Phase 65 smoke registration (`.planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/smoke-registration.json`, whose introducing commit `ac4358cbe61159c0a4663c9e719f19a43182edfb` is quoted at `65-CLOSEOUT.md:108` but is not the right anchor, see flag 11; anchor on `84128fe2`, the commit that added `evidence/fit/1632-smoke/record.json`, found with `git log -n1 --diff-filter=A --format=%H -- <that path>`): (a) live SHA-256 of `diagnostic_guard.py`, `diagnostic_data.py`, `diagnostic_variants.py`, `diagnostic_similarity.py` equal the registration's digests; (b) `git show <anchor>:pinn/verification/diagnostic_fit.py` hashes to the recorded `b00e45b4...34c2cd`, and `git show <anchor>:<registration path>` hashes to the record's `registration.sha256` (`ba54e812...`); (c) the 11 Phase 65 evidence files hash to the table at `65-CLOSEOUT.md:127-139` (parse or hard-code the table; it is the committed source of those hashes). Do not call `check-registration` on the smoke registration from a test: it is expected to refuse live once `diagnostic_fit.py` changes (flag 10).

### 13. `66-TIMING-PREDICTION.md` (doc, mechanics-only page)

**Analog:** `65-SMOKE-PREDICTION.md` (86 lines). Reuse its skeleton and register:
```
# Phase 65 Smoke Prediction: the registered 20-step system-1632 fit
**Registered before the first real optimizer step** ... This page and `evidence/fit/smoke-registration.json` are committed together and the run admits only their committed-clean bytes. ...
## What this run is
## Mechanical acceptance rule (the only rule)
## Incomplete and error branches
## What this run is not
```
The load-bearing sentence for a calibration run (`:57-60`): "**No E value, tier, similarity figure or improvement is predicted or required.** A record with every mechanical box ticked is a pass regardless of the numbers; a record failing any mechanical box is incomplete and is not a result." The "What this run is not" section (`:76-86`) is the template for stating the measured rate is "a budget input, not steady-state throughput for other depths". Add RESEARCH Pattern 4's frozen design block (variant JSON, parameter count, numeric band, branch table, repeats and confirmation rule). This page is never amended after its registration pins it.

### 14. `66-PREDICTION.md` (doc, full prediction page)

**Analog:** the same skeleton, plus the immutable-rule phrasing of `65-PROBE-PREDICTION.md:66-103` (heading "The reproduction rule (immutable after observation)", then a numbered "Reading rule" whose last clause is "No tolerance is widened after results"). Content is RESEARCH Pattern 5 items 1-10: variant JSON block, bandwidth calculation, suspect table, numeric band, branch table, repeats and confirmation, budget from the timing record (cite its SHA-256), record readout fields, the GAP-59-08 sentence, the mechanical-failure rule, plain-language reading per branch. Census lap counts for the bandwidth section are in code as `PANEL_INNER_LAPS = {1632: 10.47, 851: 18.61, 4658: 39.35}` (`learnability_arms.py:90`) and at full precision in `59-.../evidence/census/panels.json` (`N_in` 10.471994061054543 and 18.612048388702).

### 15. Registrations (config, file-I/O)

**Analog:** `.planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/smoke-registration.json` (138 lines). Serialization: insertion-order keys, `json.dumps(doc, indent=2) + "\n"` (the fixture does exactly this, `test_fit_short.py:645`). No tracked script builds registrations or computes their digests (Phase 65 authored them inline); the digest function to mirror is `_sha256_file` (`diagnostic_fit.py:271-276`, 1 MiB blocks).

| Key | Phase 66 treatment | Why |
|---|---|---|
| `schema` | copy verbatim, `phase65-fit-registration/v1` | flag 5 |
| `title`, `committed_before` | rewrite | cosmetic, but state the settings are immutable after the run |
| `page` `{path, sha256}` | the matching Phase 66 page | re-checked on every admission |
| `settings.variant` | `EXP01_VARIANT.to_json_dict()` | byte-agreement loop (`:338-343`) |
| `settings.variant_registry` | add `"phase66"` | the one new key |
| `settings.{seed, orbit_key, optimizer_steps, warmup_steps, measured_steps, similarity_cadence, whole_run_cap_seconds}` | per run (`orbit_key` form `hierarchical/gold/851`, `_parse_orbit_key` at `:295`) | flag 6 consistency rules |
| `settings.{runtime, physical_window, optimizer, loss}` | float32 on mps; `[0, 10]`; `adam_constant_rate` with `lr` 0.0001 and null `scheduler`/`clipping`/`physics_term`/`polish`; `data_only` | D-06 |
| `settings.{timing_definitions, reading_rule}` | rewrite, keeping `reading_rule.{mechanical_pass, incomplete, out_of_branch}` | flag 6 |
| `logger_parity`, `context`, `frozen[4]`, `pinned` | copy verbatim | the receipt (`run_commit` `22cee7d2...`), probe result, scorer/scorecard/`reader_acceptance.json`/`splits.json`, and the 33-module protocol are unchanged; `runs/stage0-v23g7-seed42/splits.json` is tracked and clean (verified) |
| `code_dependencies` | the five Phase 65 modules with the new `diagnostic_fit.py` digest, plus `diagnostic_phase66.py` and `diagnostic_power.py` | freeze rule: finish and commit all harness code first |
| `threats` | optional, cosmetic | not read by admission |

Order of operations (`65-06-PLAN.md:99` and RESEARCH Pattern 4): commit the page, compute digests, write the registration, commit both, run `check-registration`, only then launch. The evidence-order ancestry snippet in RESEARCH "Code Examples" is the closing check.

### 16. Run evidence directories (generated by the harness)

**Analog:** `.planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/1632-smoke/` holds exactly `record.json` (418,595 B), `diagnostic.weights` (3,192,653 B) and `attempt.json` (555 B). Never hand-author these. The attempt payload is `{schema: "phase65-fit-attempt/v1", status, pid, started_utc, registration{path, sha256}, output, whole_run_cap_seconds}` (`diagnostic_fit.py:1056-1067`), later updated in place by `_mark_attempt` (`:1072-1079`). A burned directory refuses a second attempt, so use one directory per role and seed (RESEARCH Pitfall 4: `run_id` omits the seed). The CLI triple and success tokens (`check-registration` and `verify-result` as run at `65-CLOSEOUT.md:107-108`; the `run` flags are at `diagnostic_fit.py:1523-1525`):
```
-m pinn.verification.diagnostic_fit check-registration --registration R     # CHECK-REGISTRATION-OK
-m pinn.verification.diagnostic_fit run --registration R --output D/record.json   # FIT-RUN-COMPLETE (via the Phase 66 launcher)
-m pinn.verification.diagnostic_fit verify-result --registration R --result D/record.json   # VERIFY-RESULT-OK
```
Weights for the 157,065-parameter network are about 0.63 MB (4 bytes per parameter); the record is dominated by 66 KB per similarity entry (RESEARCH Pattern 4), so keep the cadence near 14 entries.

### 17. `power-gate.json` (generated receipt)

**Analog:** the `attempt.json` payload above for shape and the UTC timestamp format; `write_record_exclusive` for the write (section 3). It is the only new evidence file type, so its schema name is the agent's call within D-discretion ("smallest AC-power launch check"). It sits beside `attempt.json` and `record.json` in the run directory and is committed with them.

### 18. `66-CLOSEOUT.md` (doc)

**Analog:** `65-CLOSEOUT.md` (146 lines). Frontmatter (`:1-7`): `phase`, `closed`, `status`, `decision_authority`, `requirements`. Sections in order: an authority paragraph, `## Decisions` (numbered), a `## Defect dispositions and reuse conditions` table (`| Item | Disposition | Required action before affected future use |`), `## Fresh closeout checks` (a `| Command arguments | Observed result |` table under the interpreter note at `:95-98`), `## Preserved evidence hashes` (SHA-256 table, `:127-139`), `## Transition` (`:141-146`). Phase 66 must record in it: the Phase 65 smoke registration is historical after the Phase 66 harness commit (RESEARCH Open Question 3 puts this in the Phase 66 closeout, not `65-CLOSEOUT.md`, which must stay unchanged); the WR-03 and WR-04 stance (RESEARCH Pitfall 9); the committed record sizes; and the test counts (Phase 65 at 204, Phase 66 as measured).

### 19. Checkpoint-1 record and reading (doc; name to be chosen, flag 2)

**Analogs:**
- `64-CHECKPOINT-1-RULING.md` (45 lines): frontmatter `phase, milestone, created, status: ratified, authority`; `## Authority and boundary`; `## The owner's words` holding the reply verbatim in a fenced `owner-quote` block ("never parsed"); `## Recorded answers` table (`| ID | Recorded answer | Applied by |`). The Phase 66 owner answer is manual-only (`66-VALIDATION.md`, Manual-Only Verifications); D-08's budget answer is already verbatim in `66-CONTEXT.md`.
- `64-VERDICT.md:26-35` (`## In plain language`, a numbered list that defines each term in one sentence), `:215-223` (a three-option decision table with consequences) and `:227-248` (`## Owner sign-off`: Decision, Date, Meaning, Items left open, Record with SHA-256).
- `65-FINDINGS.md` sections 1-8 for the evidence-index habit (`## 8. Evidence index`, `:184`).

Content required by SC-3: the branch taken, the plain-language reading (RESEARCH Pattern 5 item 10 has the per-branch wording), any SCOPE-49 proposal with the owner's answer, and the SHA-256 of the three run records and the timing record.

### 20. `REQUIREMENTS.md` and `STATE.md` (hand edits at close)

**Analog:** the `## Transition` paragraph of `65-CLOSEOUT.md:141-146`, and the standing note at `.planning/STATE.md:50-52`: "**This file is maintained by hand in this checkout.** The `gsd-tools` mutating verbs have corrupted it before ... The v2.5 start was written by hand and its diff reviewed." Edit by hand and review the diff; do not call `gsd-tools` mutating verbs on `STATE.md`. Update the EXP-01 checkbox and its traceability row in `REQUIREMENTS.md` (`:115`, `:244`) only after the checkpoint-1 answer is recorded.

## Shared Patterns

### Typed refusal, admission before side effects
**Source:** `diagnostic_fit.py:538-556`, `1456-1470`; `diagnostic_guard.py:53-60`. **Apply to:** `diagnostic_power.py`, the Site B lookup, every new test.
Admission raises a typed `RuntimeError` subclass before any data read, optimizer construction or attempt claim; the CLI maps it to `FIT-REFUSED: <reason>` on stderr and exit 2. Tests prove "before any access" with spies that fail the test on contact (`_NoDataNoOptimizer`, `test_fit_short.py:685-713`; `mock.patch.object(torch.optim.Adam, "step", side_effect=AssertionError(...))`). Stage-0 TRAIN-only access and the pre-open refusals in `diagnostic_data.py` are unchanged and need no edit (D-11).

### Exclusive, canonical, redacted JSON
**Source:** `learnability_arms.py:435-465`, `evidence_io.py:131-155`. **Apply to:** `power-gate.json`, any new evidence writer.
`O_EXCL` first-writer-wins, sorted-key indent-2 ASCII JSON with a trailing newline, and a refusal of any text containing the home prefix. A second write raises `FirstResultExists`; nothing is overwritten.

### Pin, commit, then freeze
**Source:** `diagnostic_guard.py:324-459` (what admission checks), `65-06-PLAN.md:99` (how Phase 65 sequenced it). **Apply to:** pages, registrations, harness code.
Every registered artifact must be git-tracked, unmodified and hash-exact (`:397-410`); the registration's introducing commit must be an ancestor of HEAD (`:412-422`); an unrelated dirty file elsewhere is never a refusal reason. Therefore: finish and commit all harness code, then the page, then the registration, run `check-registration`, then launch. A later edit to any pinned file retires every earlier registration's live admission.

### Test conventions
**Source:** `tests/phase65/` throughout. **Apply to:** all of `tests/phase66/`.
Standard-library `unittest` only; `from __future__ import annotations`; a module docstring naming the plan and requirement; `ExitStack` plus `tempfile.TemporaryDirectory(prefix="phase66-...")` plus `unittest.mock`; synthetic corpus via `tests.phase60._fixtures.gold_corpus_fixture`; throwaway `git init` repos for admission; CPU float64 `FIXTURE_RUNTIME`; no real corpus, no training and no MPS except a deliberate parity test. Full-suite regression gate: `python -B -m unittest discover -s tests/phase65 -t .` stays at 204 passing.

### Interpreter and working directory
**Source:** `65-CLOSEOUT.md:95-96`. **Apply to:** every command.
`<home>/miniforge3/envs/pinn-train/bin/python -B` from the trainex root (`.worktrees/trainex`, branch `milestone/v2.5`).

### Commit protocol
**Source:** `CLAUDE.md` "Git Commit Protocol", `scripts/agent-commit`, `docs/git-guidelines.md`, `65-06-PLAN.md:99, 123`. **Apply to:** every commit task.
Use `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`; stage explicit owned paths; message `<type>(<scope>): <lowercase imperative subject>` with a body for `.planning/` and multi-file commits and an `Agent-Assisted-By:` or `Co-Authored-By:` trailer; run `git diff --check`. Pre-existing modified and untracked files (`.planning/config.json`, `.agents/`, `.gsd/`, `.planning/state.json` and others) are user-owned and are never staged. Commit the harness extension, each page-plus-registration pair, each run record and the review as separate logical units.

### Frozen and pinned sources
**Source:** `learnability_protocol.py:145-179`. **Apply to:** all planning.
The 33 `PINNED_MODULES` (flag 10) are import-only. The scorer, scorecard, `reader_acceptance.json` and `splits.json` are registration `frozen[]` entries. SCOPE-46 forbids locked-value moves, so `ArchitectureSpec` stays depth-12; a variant only selects what to build.

### Expensive-run evidence retention
**Source:** global `CLAUDE.md` "Expensive validation evidence reuse". **Apply to:** the four compute launches.
Any command expected to exceed 60 seconds keeps complete stdout, stderr, exit status, command, directory and elapsed time in a session temp file outside the repository, and is not rerun merely to reformat output. A refusal on battery is a deferral to the next AC window, never a failure to work around (D-08).

## No Analog Found

| File or behaviour | Role | Data flow | Reason |
|---|---|---|---|
| Registration builder (digest computation plus JSON write) | utility | file-I/O | No tracked script exists; Phase 65 wrote registrations inline. Plan an inline snippet using `hashlib` as in `_sha256_file`, or a small tested helper, and say which. |
| Branch classifier `classify_exp01` / `confirm` | utility | transform | Only the Tier-1 reading and its inclusive-edge tests exist (section 2). The band logic is new. |
| Positive AC-power parse of `pmset -g batt` | middleware | request-response | The only tracked precedent (`on_battery`) is fail-open and is a counter-example. |
| Python `os.exec*` launcher composition | middleware | request-response | No tracked Python `os.exec*` call; the precedents are argv-list plus `subprocess` and the shell `exec` at `scripts/phase60-power-guard.sh:18`. |
| Extracting a fenced JSON block from a Markdown page | utility | file-I/O | No existing extractor. A `re` pattern in `test_pages.py` is enough; keep the block label stable on both pages. |
| Budget computation from the timing record (RESEARCH Pattern 4 formula) | utility | transform | No script exists. Show the arithmetic on the page with the record's SHA-256, or add a tested helper, but do not leave it to prose. |
| Faked `pmset` in tests | test | request-response | No existing test fakes `pmset`; the injected-`run` design in `test_power.py` is new. |

## Metadata

**Analog search scope:** `pinn/verification/diagnostic_*.py`, `pinn/network.py`, `pinn/architecture_spec.py`, `pinn/verification/{evidence_io,learnability_arms,learnability_protocol}.py`, `scripts/phase60_run_control.py`, `scripts/phase60-power-guard.sh`, `.planning/phases/60-single-system-learnability/evidence/launch_phase60_arm.py`, `tests/phase60`, `tests/phase64`, `tests/phase65`, Phase 59/64/65 planning evidence, `.gitignore`, `.githooks`.
**Tracked-source gate:** 56 analog and reference paths checked with `git ls-files -- <path>`; 0 untracked. No gitignored runtime mirror is named. The only gitignore finding (flag 1) concerns proposed new output paths.
**Read-only commands used:** `git ls-files`, `git check-ignore`, `git log`, `git show`, `git status`, `git rev-parse`, `pmset -g batt`, and `python3 -I` JSON reads of committed census, `numbers.json` and the Phase 65 smoke record. No test, training run, timing run, MPS compute or Stage-0 data file was opened or executed.
**Pattern extraction date:** 2026-10-31
