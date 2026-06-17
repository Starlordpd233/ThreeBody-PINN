# Phase 24: Empirical Dataset Verification and Correction Addendum - Pattern Map

**Mapped:** 2026-06-10
**Files analyzed:** 10 (6 probe scripts + outputs dir, verified-facts register, correction addendum, issue ledger, optional gap register)
**Analogs found:** 10 / 10 (all artifacts have a strong in-repo precedent)

> **Phase nature:** This is a documentation + disposable-probe phase, NOT an application-code phase. There is no controller/service/component code. "Role" below is adapted to this phase's artifact taxonomy: `probe-script`, `evidence-register`, `correction-doc`, `ledger`, `gap-register`. All analogs are real files in this repo. Every probe is read-only over `simulation_data/`; the only writes are inside the phase directory and one sibling file in `research_package/` (D-18). Planner: copy the schemas below verbatim — do NOT redesign them (D-24 / "Don't Hand-Roll").

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `probes/data01_id_gaps.py` | probe-script | file-I/O + set arithmetic | `simulation_data/Validation/audit_reports/check_missing_results.py` | role-match (read-only folder/ID parse) |
| `probes/data02_blacklist.py` (+ grep) | probe-script | file-I/O (JSON read) + grep sweep | `check_missing_results.py` + RESEARCH §Code Examples inline one-liner | role-match |
| `probes/data03_gold_gap.py` | probe-script | file-I/O + set diff | `check_missing_results.py` | role-match |
| `probes/data04_footers.py` | probe-script | file-I/O (last-line footer parse) | `check_missing_results.py:5-21` (`check_last_line`) | exact (same footer-detection pattern) |
| `probes/data05_mass_drift.py` | probe-script | transform / numerical compare (numpy) | RESEARCH §Pattern 2 + dataset-reference IC/Brutus format | role-match (numpy-gated) |
| `probes/data06_snapshots.py` | probe-script | file-I/O (block-split distribution) | RESEARCH §Pattern 3 | role-match |
| `probes/outputs/*` | evidence-capture | captured stdout | v1.4 disposable-probe evidence (`21-*/evidence/*.stdout.txt`) | role-match |
| `24-VERIFIED-FACTS.md` | evidence-register | bookkeeping (CLM/DATA-keyed rows) | `RESEARCH-CONTEXT-MASTER.md` §"CLM Claims Register" (table schema) + the inline verdict/evidence prose pattern below | role-match |
| `research_package/DATA-07-CORRECTION-ADDENDUM.md` | correction-doc | sibling correction file | Inline sibling-correction structure below, preserving the retired erratum precedent without requiring a now-retired file read | exact (sibling-file precedent, D-18) |
| `24-ISSUE-LEDGER.md` | ledger | state-machine seed | `16-ISSUE-LEDGER.md` | exact (D-22/D-24 mandate this schema) |
| `24-GAPS.md` (only if a STOP gap fires) | gap-register | governance log | `22-GAPS.md` table in `16-ISSUE-LEDGER.md:479-485` + CLAUDE.md STOP-protocol field list | role-match |

## Pattern Assignments

### `probes/data0N_*.py` (probe-script, file-I/O) — all six

**Analog:** `simulation_data/Validation/audit_reports/check_missing_results.py` (read-only method reference per D-03 — Phase 24 runs its OWN probe, never cites the audit as a substitute).

**Folder-iteration + filename pattern** (`check_missing_results.py:34-47`):
```python
folders = ['brutus_hierarchical', 'brutus_hierarchical_gold_standard',
           'brutus_standard_quasi_random', 'brutus_standard_quasi_random_gold_standard']
for folder in folders:
    pattern = os.path.join(folder, '*.txt')
    txt_files = glob.glob(pattern)
    txt_files.sort()
```
Use the absolute base `simulation_data/Data/brutus_output/` and the four-variant list verbatim. Filenames are zero-padded 4-digit `brutus_{standard,hierarchical}_NNNN.txt` (NO `_gold_` infix — gold is folder-encoded only; dataset-reference.md "Mapping rule" + ERRATUM Correction 1).

**Footer-detection pattern** (`check_missing_results.py:5-21`) — copy directly for DATA-04:
```python
def check_last_line(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if line:
            return line.startswith('Result: filename=')
    return False
```
DATA-04 extends this: a `Result:` line present ⇒ parse the full schema (`eta`/`tol`/`Lw`/energy); absent ⇒ the file is one of the 1,550 hier / 701 std / 219 std-gold no-footer population (ERRATUM Correction 2; D-07). Do NOT use "minimal/partial footer" language — that is superseded.

**Re-derivability header** (D-02; required on every probe — not present in the analog, this is the Phase 24 addition):
```python
# probes/data01_id_gaps.py
# Run from repo root: .venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data01_id_gaps.py
# Reads (read-only): simulation_data/Data/brutus_output/{4 variants}
# Records: value + command + dataset path + run date into 24-VERIFIED-FACTS.md
```
Every probe MUST be invoked as `.venv/bin/python` (numpy 2.2.0; system `python3` has none — RESEARCH Pitfall 1). DATA-01/03/06 need only stdlib but standardize on `.venv` to kill the split-interpreter footgun.

**DATA-01 ID-gap method** (D-13; RESEARCH §Pattern 1, pilot-VERIFIED std gaps[0..3998]=1250 / [0..3999]=1251 / hier=143): parse IDs, diff against nominal range — never bare file counts. Emit BOTH `gaps[0..max]` and `gaps[0..nominal_end]`; the nominal-range convention is a potential STOP gap (semantic) — surface, do not pick (RESEARCH Open Q1, Pitfall 2).

**DATA-05 mass-drift** (D-14; RESEARCH §Pattern 2): IC mass = col 0 of rows 1-3; Brutus t=0 mass = col 0 of body lines 1-3 of block 0 (dataset-reference.md formats); compare `np.allclose(rtol=1e-15)` on float64. Full population (D-15). If mismatches cluster in hierarchical, check `ic_generation/` perturbation provenance BEFORE a verdict (D-16) — ambiguity is a STOP gap.

**DATA-06 distribution** (D-09; RESEARCH §Pattern 3): `blocks = [b for b in open(p).read().split("\n\n") if b.strip()]`; `final_time = float(blocks[-1].splitlines()[0].split()[0])`; record per-variant min/median/mode/max + counts at modal value, not a single example.

---

### `research_package/DATA-07-CORRECTION-ADDENDUM.md` (correction-doc, sibling file)

**Analog:** the retired `research_package/ERRATUM-2026-06-10.md` sibling-correction precedent (retired 2026-06-11; its two corrections are now integrated in `RESEARCH-CONTEXT-MASTER.md` §"Correction Provenance And Verification Boundaries"). Do not require the executor to read the retired file from the package; use the inline structure below and the current master section. The addendum SUPERSEDES the master's correction-provenance section.

**Header / byte-stability statement** (retired erratum pattern, now described inline):
```markdown
# DATA-07 Correction Addendum — <actual execution date>
**Scope:** CLM-keyed corrections to package-stated dataset claims, established by Phase 24
read-only probes. Added sibling file only: no delivered package file modified; per-file
source hashes in the master's Per-File Manifest remain valid; this addendum is intentionally not in that manifest.
**Supersession:** supersedes the master's "Correction Provenance And Verification Boundaries" section, folding in its two corrections (D-07).
```

**Per-correction block** (retired erratum pattern, now described inline) — reuse: `## Correction N — <title>` / **Affects:** (CLM row + file:section) / **Package states:** (quoted claim) / **Corrected disk fact:** / **Evidence:** (repo-root probe command + path + actual run date — D-02). CLM-keyed rows carry claimed value, observed value, probe command/path, verdict (`confirmed`/`corrected`/`unverified`) (D-08/D-19).

**Two mandatory folded corrections** (D-07; restated from the current master correction-provenance section and re-probed by Phase 24): (1) gold filenames carry NO `_gold_` infix — folder-encoded only; (2) the 1,550/701/219 populations have NO `Result:` footer at all; CLM-07 count 219 stands, characterization corrected.

**Confirmed-claims summary + "Not affected" list** (retired erratum pattern, now described inline) — replicate so the external researcher stops over-discounting confirmed figures (D-19). **Nil-addendum case** (D-20): same file records all package claims confirmed + the probe index only when no package-stated claim is contradicted and no register row is held `unverified` behind an OPEN gap.

WR-01/02/03 (CONTEXT specifics) are correction candidates that route here; WR-02/03 are spec-citation typos (not dataset claims) — their channel inside the addendum is an open decision the planner surfaces, not resolves.

---

### `24-ISSUE-LEDGER.md` (ledger, state-machine seed)

**Analog:** `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` — INSTANTIATE this schema, do not redesign (D-24; "Don't Hand-Roll"). Phase 24 initializes states only; Phase 25 owns the operating protocol.

**Frontmatter** (`16-ISSUE-LEDGER.md:1-11`): `phase / slug / status: draft / created / total_findings / in_scope_findings / deferred_findings / traceability_verified`.

**Status table** (`16-ISSUE-LEDGER.md:17-39`) — reuse columns, seed every row `PENDING`:
```markdown
| ID | Title | Phase | Status | Verdict | Sources Disagree? | Evidence Packet | Acceptance Check | Spec Section | Dependents | Last Updated |
```
Seed scope (D-23): B-06, B-11, M11, M12, M13, D7, G1, G2, G3, G4, G5 as separate rows, D-03 training-data format, SCS, SASD, IPR, and PSC metric claims as separate rows, `compute_globals` `D=6.694` (PENDING, routed Phase 25 EVID-10 / Phase 27 PIPE-09 — D-05, not probed), footer/mass-drift protocol, precision handling — each with owning requirement + adjudication phase noted.

**Lifecycle Rules block** (`16-ISSUE-LEDGER.md:45-55`) — copy the exact state machine: `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`; `DEFERRED` absorbing + written blocker; "FIX_APPLIED is not closure; VERIFIED requires a passing acceptance check." Phase 24 does NOT over-specify Phase 25-owned columns.

**Per-finding notes + status-transition log** (`16-ISSUE-LEDGER.md:61-77`): each entry `date · commit-short-SHA · status transition · actor/plan`. Seed rows use `SEED_SHA PENDING -> PENDING (seeded by Phase 24 PNN)`.

**Two annexes** (D-23): (a) the verified-facts register linked at the stable path (standalone `24-VERIFIED-FACTS.md` recommended — RESEARCH Open Q4); (b) the anomalies section for discrepancies contradicting NO package claim (D-12).

---

### `24-VERIFIED-FACTS.md` (evidence-register)

**Analog:** `RESEARCH-CONTEXT-MASTER.md` §"CLM Claims Register" (table schema) + the inline retired-erratum verdict/evidence-citation style above. Per-row: CLM/DATA ID · claimed value · observed value · executable repo-root probe command · dataset path · actual run date · verdict (D-02/D-08). Prose-sweep figures with no CLM row get extension IDs `CLM-14+` here (D-06) — the delivered `RESEARCH-CONTEXT-MASTER.md` stays byte-stable against its 2026-06-11 post-consolidation baseline. Probe-checklist maps 1:1 onto the master's CLM-01..12 rows via each row's "Phase-24 check" column (D-04); CLM-13 is `PENDING`, not probed (D-05).

---

### `24-GAPS.md` (gap-register — created ONLY on first STOP gap)

**Analog:** `22-GAPS.md` table embedded at `16-ISSUE-LEDGER.md:479-485` + the CLAUDE.md STOP-protocol field list. Required fields: Decision point · Where in artifact · Task context · Classification (semantic / operational / process-schema / cross-phase) · Source silence (file:line) · Math/engineering grounding · Tempted to · What user must decide (A/B/C) · Confidence · Status (`OPEN`) · Resolution note. Mirror into `.planning/milestones/v1.5-GAPS.md`. Candidate gaps: DATA-01 nominal-range convention (Open Q1), DATA-05 hierarchical mass baseline (Open Q3). Subagents never write the register — the executor/orchestrator does.

## Shared Patterns

### Re-derivability (SCOPE-06 / D-02)
**Source:** RESEARCH §Pattern 1-3 headers; absent from `check_missing_results.py` (it prints counts only).
**Apply to:** every probe + every register row. Each recorded fact carries probe command + dataset path + observed value + run date so any later probe reproduces it without this session's context.

### Read-only / byte-stability (VER-09 / D-18)
**Source:** retired erratum sibling-file pattern (described inline above), with the current master carrying the manifest and correction-provenance sections.
**Apply to:** all probes (never write inside `simulation_data/`, never touch `pinn/`); the addendum (sibling in `research_package/`, not added to manifest).

### Interpreter standardization (RESEARCH Pitfall 1)
**Source:** RESEARCH Standard Stack — `.venv/bin/python` (numpy 2.2.0) is the ONLY numpy interpreter.
**Apply to:** all six probe invocation strings; record `.venv/bin/python ...` in the register, never bare `python3`.

### Dataset format constants
**Source:** `.claude/rules/dataset-reference.md` (IC/Brutus formats, four-variant folder list, mapping rule, footer optionality, final_timestep>=9.5 gate) + `RESEARCH-CONTEXT-MASTER.md` §"Correction Provenance And Verification Boundaries" (corrected footer/gold facts).
**Apply to:** DATA-01/03 (filename ID parse), DATA-04 (footer schema), DATA-05 (mass col 0), DATA-06 (block split + final-time gate).

### Mandatory commit path (D-25)
**Source:** CLAUDE.md Git Commit Protocol — `scripts/agent-commit`, one atomic commit per plan; raw `git commit` forbidden.
**Apply to:** every plan's commit step.

## No Analog Found

None. Every Phase 24 artifact has a strong in-repo precedent. The closest thing to a novel element is the per-probe re-derivability header (D-02), which extends the `check_missing_results.py` pattern rather than replacing it.

## Metadata

**Analog search scope:** `.planning/milestones/v1.4-phases/16-*/`, `.planning/phases/23-*/`, `pinn_instruction/.../research_package/`, `simulation_data/Validation/audit_reports/`, `.claude/rules/`.
**Files scanned:** 7 (16-ISSUE-LEDGER.md, retired erratum/claims-table history as context only, RESEARCH-CONTEXT-MASTER.md, check_missing_results.py, plus CONTEXT/RESEARCH and dataset-reference rule).
**Pattern extraction date:** 2026-06-10
