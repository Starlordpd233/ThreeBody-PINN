# Phase 69: Findings & redesign decision - pattern map

Mapped 2026-11-08 in `trainex`, branch `milestone/v2.5`. Nine proposed output paths classified; eight have a close analog. Output names below are implementation suggestions under D-08/D-10 and may be consolidated. `69-SPEC.md` and `69-CONTEXT.md` govern scope; `69-RESEARCH.md` supplies the existing evidence inventory.

## File Classification

All `69-*.md` and `evidence/` outputs are relative to `.planning/phases/69-findings-redesign-decision/`.

| New file | Role | Data flow | Analog | Match | Primary responsibility |
|---|---|---|---|---|---|
| `evidence/verify_phase69.py` | utility | file-I/O, transform | A | exact | Check committed sources, accounting and active traceability without training or scoring. |
| `tests/phase69/test_verifier_phase69.py` | test | file-I/O, transform | B | exact | Exercise factual checks with small fixtures and deliberate corruptions. |
| `tests/phase69/__init__.py` | config | file-I/O | C | exact | Match the existing unittest package convention. |
| `69-FINDINGS.md` | model, document | transform | D | exact | One-page synthesis, suspect statuses, prediction links, qualified recommendation. |
| `69-EVIDENCE.md` | model, document | transform | D | role-match | Source revision/hash inventory and verified-difference/equivalence/open recipe comparison. |
| `69-ACCOUNTING.md` | model, document | batch, transform | none | none | Unique activity ledger, timing bases, unknown costs and reproducible subtotals. |
| `69-CHECKPOINT.md` | model, document | request-response | E | exact | Present completed findings, alternatives and the reserved v2.6/trainex-r5 choices. |
| `69-RULING.md` | model, document | event-driven | F | exact | Preserve actual owner words, presented packet identity and unanswered choices. |
| `69-HANDOFF.md` | model, document | transform | F | role-match | Carry obligations and open choices into v2.6 with their existing authority. |

## Pattern Assignments

### A. Verifier and source integrity

Copy the small command-dispatch structure from `.planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py:4733-4764`. Its `build_parser()` uses:

```python
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("command", choices=tuple(COMMANDS))
```

Use standard-library imports as in that file's lines 15-27. `VerifyError`, `fail`, `repo_path`, `load_json` and argument-array `_git` at lines 353-398 provide the error/path pattern. Proposed modes are `sources|cost|traceability|all`; these names are advisory. Keep handlers read-only and separate mechanical validity from scientific judgment.

For source bytes, `pinn/verification/evidence_io.py:350-359` supplies `_show_bytes`:

```python
proc = subprocess.run(
    ["git", "show", spec],
    cwd=str(repo), capture_output=True, check=False,
)
```

Adapt locally or reuse suitable public helpers; no shared-module edits are expected. Historical registrations must resolve at the run record's publication revision and match its recorded registration digest. `tests/phase67/test_historical.py:86-120` demonstrates the anchor and byte checks, including:

```python
registration_at_anchor = self._git(
    "show", f"{anchor}:{record['registration']['path']}"
)
```

Do not copy that test's additional live-registration equality assumption for re-pinned Phase 67 rows. Distinguish publication bytes, later registrations and current admission. `evidence_io.canonical_json_bytes` at lines 131-140 is the existing sorted, newline-terminated JSON convention if a machine-readable support file is useful.

### Active traceability and exact case identity

Adapt A's `traceability_report` at lines 823-918. It rejects empty definitions, duplicate definitions/table rows and disagreement between both mapping surfaces:

```python
defined_set = set(defined)
if defined_set != set(table_phase):
    missing = sorted(defined_set - set(table_phase))
    extra = sorted(set(table_phase) - defined_set)
```

Replace A's archived v2.4 paths, section selectors and `TRACEABLE_PHASES` at lines 769-783. Read live `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md`, derive the active set/count, require nonempty inventories, one phase per ID, agreeing mappings and existing phase directories. Neither `13` nor Phases 59-64 is a valid fixed closing criterion. Mapping does not establish satisfaction.

Use `pinn/verification/diagnostic_phase67_execution.py:2279-2284`, `_case_role`, when joining reviewed numbers:

```python
"main-1632-s42": "main",
"repeat-851-s42": "repeat-system",
"repeat-1632-s41": "repeat-seed",
```

Join by case/system/seed/arm identity, never column order. Preserve raw review labels, endpoint selection and prediction links. D's narrative has a known EXP-03 repeat-column discrepancy; copy its provenance format, not its table values.

### B/C. Focused tests

B is `tests/phase64/test_verifier_phase64.py`. Copy `load_verifier()` at lines 69-74 (`importlib.util.spec_from_file_location`) and `run_main()` at lines 121-126. Copy `TraceabilityPureTests` at lines 648-677 and its one-mutation fixture pattern at lines 717-817:

```python
with self.assertRaises(self.module.VerifyError) as raised:
    self.report(requirements, roadmap, project)
return str(raised.exception)
```

Cover reordered cases, missing/extra/duplicate IDs, empty inventories, nonexistent phases, changed source digests, repeated control references and unknown duration. Use tiny temporary Git fixtures only where history matters. C is `tests/phase64/__init__.py`, a package docstring. Do not copy the large Phase 64 suite, its archived counts, production Git mutations or prose-presence assertions.

### D/E/F. Findings, checkpoint, ruling and handoff

D is `.planning/phases/67-design-settings-ladders/67-FINDINGS.md:3-42`: quantitative claims point to a committed review/result/prediction and a source-hash table. Use its explicit limitations at lines 306-325. Keep the Phase 69 main page short and put recipe/accounting details in linked support.

E is `.planning/phases/68-yardstick/68-CHECKPOINT-2.md:3-22`: evidence path/commit/digest followed by a compact item/recommendation/options/status table. Adapt the format to Phase 69's reserved decisions; the existing packet's recommendations and ratified status are not defaults.

F is `.planning/phases/68-yardstick/68-CHECKPOINT-2-RULING.md:7-10,27-58`: packet/audit identity, verbatim reply, individually open answers and a target/action/source-authority routing table. Its actual quote is:

```owner-quote
C-7: A. Leave C-2, C-4, C-5 and C-6 open for separate discussion.
```

Also follow `.planning/phases/66-small-network-control/66-CHECKPOINT-1-RULING.md:29-61` for recording when a committed result was presented. `.planning/phases/67-design-settings-ladders/67-EXP03-RULING.md:14-41` binds the reply and permission to reviewed digests while explicitly excluding scope/registration amendments. `diagnostic_phase67_execution._verify_ruling` at lines 2394-2471 checks chronology, hashes and nonempty words. Those checks cannot establish that a real owner interaction occurred. Require the actual owner-only checkpoint after findings; preserve missing replies as pending and explicit open choices as open.

## Shared Patterns

Use committed-byte SHA-256 provenance, repository-contained paths, explicit identity joins and errors that prevent false success. No auth middleware is involved. Preserve historical artifacts. Carry Phase 68's C-7 ruling and still-open companions, C-11 routing and the named physics-pipeline obligations without implementing them. Reporting must not launch training, read preserved evaluation data or grant work authority.

## No Analog Found

No complete unique-attempt cost ledger was identified. Implement only the phase-specific aggregation described in research/D-09: enumerate tracked attempts once by path plus registration/run identity; retain published, failed/partial, missing-duration and refusal categories; sum exact Decimal values or UTC differences on a stated basis. `started_utc`/`ended_utc` and `total_wall_seconds` are different views, not additive expenses. Unknown duration stays unknown; v2.4 remains outside v2.5 totals. D's lines 294-304 demonstrate coverage disclosure but contain a mixed timing basis, so they are not a uniform cost implementation to copy.

## Metadata

The map uses five bounded analog groups: Phase 64 verifier, Phase 64 tests, evidence I/O, Phase 67 identity/history checks, and Phase 66-68 reporting/rulings. Every named analog path was verified with `git ls-files -- <path>` in this worktree; no runtime mirror is referenced. No external research or scientific re-adjudication was performed. Only this pattern map was written.
