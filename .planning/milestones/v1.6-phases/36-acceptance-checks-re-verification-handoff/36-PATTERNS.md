# Phase 36: Acceptance Checks, Re-verification & Handoff - Pattern Map

**Mapped:** 2026-06-30
**Files analyzed:** 5 new artifacts (manifest, probe-results, verification, handoff, evidence dir)
**Analogs found:** 5 / 5 (one composite from two sources)

Read-only pattern mapping for v1.6 closure. Every analog below is a `.planning/` GSD closure
artifact; no live `pinn/` code is cited as an analog (it is non-grounding for v1.6). The two
canonical precedents are Phase 21 (v1.4 closure) and Phase 29 (v1.5 closure); Phases 33/34/35 give
the recent in-milestone verification frontmatter shape.

---

## File Classification

| New artifact | Role | Data Flow | Closest Analog | Match Quality |
|--------------|------|-----------|----------------|---------------|
| `36-ACCEPTANCE-MANIFEST.md` | manifest/inventory | transform (contracts → check rows) | `29-ACCEPTANCE-EVIDENCE-2026-06-17.md` (AC table) | role-match (no standalone manifest precedent) |
| `36-PROBE-RESULTS.md` | evidence record | batch (probe runs → PASS/FAIL + hashes) | `21-PROBE-RESULTS.md` | exact |
| `36-VERIFICATION.md` | verification report | request-response (audit → verdict) | `29-VERIFICATION.md` + `35-VERIFICATION.md` (frontmatter) | exact |
| `36-HANDOFF.md` | handoff | transform (ledger rows → dispositions) | `29-HANDOFF.md` (then `21-HANDOFF.md`) | exact |
| `36/evidence/` (raw probe outputs) | evidence dir | file-I/O (hashed stdout/stderr) | `21-acceptance-checks-and-handoff/evidence/` + `probes/` | exact |

---

## Pattern Assignments

### `36-ACCEPTANCE-MANIFEST.md` (manifest, transform)

**Analog:** `.planning/milestones/v1.5-phases/29-acceptance-checks-re-verification-and-handoff/29-ACCEPTANCE-EVIDENCE-2026-06-17.md` (the AC table in §2).

**Note:** No prior phase produced a *standalone* manifest file — Phase 29 folded the AC inventory
and the run results into one `ACCEPTANCE-EVIDENCE` document. The SPEC (D-36-01) splits these into a
separate `36-ACCEPTANCE-MANIFEST.md` (the static inventory) and `36-PROBE-RESULTS.md` (the run
record). So replicate the Phase 29 *table columns* for the manifest but drop the run-result/result-date
columns (those belong in PROBE-RESULTS). This is a structural split, not a fabricated shape.

**Table shape to replicate** (29-ACCEPTANCE-EVIDENCE §2):
```
| AC-ID | Asserts (landed clause) | Command / Function | Input data | Pass criterion | Result (date) | Evidence (probe) |
```

**Phase 36 manifest columns** (SPEC R1 — the locked seven fields; drop "Result", that lives in
PROBE-RESULTS):
```
| Requirement ID | Contract source | Pass criterion | Data / expression | Command / function | Expected evidence path | Owning phase |
```

**What to replicate / what differs:** Keep the one-row-per-contract-check shape and the
landed-clause + numeric-pass-criterion discipline from Phase 29. Differs: Phase 36 manifest is the
*static* inventory keyed by v1.6 contract/requirement ID (sorted by ID per Edge `ordering R1`), with
`Owning phase` and `Expected evidence path` columns that point forward into the probe run; the
PASS/FAIL result is deliberately NOT in this file.

---

### `36-PROBE-RESULTS.md` (evidence record, batch)

**Analog:** `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/21-PROBE-RESULTS.md`

**Header block to replicate** (21-PROBE-RESULTS lines 1-12): fresh execution date, interpreter,
an environment-evidence file with its own SHA-256, and a statement that the doc *summarizes* the
captured raw output rather than replacing it.

**Per-probe block to replicate** (one `##` section per check, e.g. lines 14-22):
```
## <check name>

- **Status:** PASS
- **Command:** `<interpreter> <probe path>`
- **Raw stdout evidence:** `…/evidence/<probe>.stdout.txt`
- **SHA-256:** `<hash>`
- **Observed metric:** `<value>`
- **Pass criterion:** `<numeric criterion>`
```

**What to replicate / what differs:** Replicate the PASS-labeled per-probe block, the
one-evidence-file-plus-hash-per-probe rule, and the "exit code 0" assertion. Differs: Phase 36 must
emit exactly one PASS/**FAIL/SKIP** row per manifest row (SPEC R2 — Phase 21 only had PASS cases),
must route any FAIL/missing-evidence back to the originating phase (fail-closed), and must keep
results tied to one manifest snapshot (Edge `concurrency R2`). SKIP rows need a written reason.

---

### `36-VERIFICATION.md` (verification report, request-response)

**Primary analog (body):** `.planning/milestones/v1.5-phases/29-acceptance-checks-re-verification-and-handoff/29-VERIFICATION.md`
**Frontmatter analog (recent in-milestone shape):** `.planning/phases/35-loss-energy-weight-contracts/35-VERIFICATION.md`

**Body section skeleton to replicate** (29-VERIFICATION headings):
```
## Goal Achievement  (### Observable Truths / ### Deferred Items / ### Required Artifacts)
## Key Link Verification
## Requirements Coverage          (table: | Requirement | Evidence | Status |)
## Anti-Patterns Found
## Governance Verification (CLAUDE.md STOP Protocol Checks)
## Human Verification Required
## Reconciliation Recommendation: REQUIREMENTS.md and ROADMAP …
## Gaps Summary
```

**Frontmatter block to replicate** (35-VERIFICATION lines 1-39): `phase`, `verified` (ISO-8601),
`status`, `score`, `gaps_remaining: []`, `must_haves:` list, `artifacts:` list (path + provides),
and `prohibitions:` list (statement / status / verification).

**Requirements-coverage table shape** (21-VERIFICATION lines 27-35; also in 29):
```
| Requirement | Evidence | Status |
| `VER-13` | <evidence ref> | PASS |
```

**Ledger-state + reconciliation:** the §"Reconciliation Recommendation" block in 29-VERIFICATION
(lines 143-163) is the precedent for the R6 REQUIREMENTS.md/ROADMAP.md flips — it lists each flip as
`line N: [ ] → [x]` with an evidence citation and a "why not auto-applied / owned-path" note.

**What to replicate / what differs:** Replicate the 29 body skeleton, the 35 frontmatter schema,
the Requirements-coverage table, and the explicit per-flip reconciliation list. Differs for Phase 36:
add a **ledger-state table whose counts come from a fresh parse of `32-ISSUE-LEDGER.md`** (SPEC R3 —
record `BLOCKED` not `passed` if any in-scope row is `PENDING`/`IN_PROGRESS`/`FIX_APPLIED`; D-05/D-06
are the known live blockers); add the **32/32 traceability audit** naming evidence for `VER-13..VER-18`;
add a **protected-path / probe-target guard** proving `pinn/` is untouched (Prohibition row 1). In
Phase 29 the REQUIREMENTS/ROADMAP flips were *recommended* for the orchestrator; in Phase 36 R6 puts
those edits **in scope** (D-36-17) as Phase-36-owned manual edits, so this file both audits and
records them.

---

### `36-HANDOFF.md` (handoff, transform)

**Primary analog:** `.planning/milestones/v1.5-phases/29-acceptance-checks-re-verification-and-handoff/29-HANDOFF.md`
**Secondary (SI table + fixed list):** `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/21-HANDOFF.md`

**Section skeleton to replicate** (29-HANDOFF headings):
```
## Evidence Used
## 1. Fixed
## 2. Intentionally Unchanged
## 3. Deferred
## 4. SI Metadata Reconciliation
## 5. FUT-01 / Consumption Notes
## 6. Milestone-Closure Gate (G1-G8)
```

**SI reconciliation table shape to replicate** (21-HANDOFF lines 48-58):
```
| Entry | Status | Evidence |
| `SI-CTL-001` | Retired with B-03 back-reference | `ctl_instruction.md:1446-1448` |
| `SI-PINN-002` | Preserved untouched | `pinn_architecture.md:1017-1024` |
```

**What to replicate / what differs:** Replicate the Fixed / Intentionally-Unchanged / Deferred
trio, the SI `| Entry | Status | Evidence |` table, and the closure-gate section. Differs for Phase
36: the SI table must cover the corrected **four-ID universe** (`SI-CTL-001`, `SI-PINN-002`,
`SI-PINN-003`, `SI-DQA-003` — D-36-09; note 21-HANDOFF predates this and listed `SI-DQA-003` only as
"preserved untouched", which Phase 36 must re-adjudicate for Issue-03 relevance), every `SI-*` hit
needs a retire-with-back-reference *or* preserve-with-reason+owner (no row assumed irrelevant, D-36-10),
and `SI-DQA-003`'s disposition is STOP-governed (D-36-18 — surface a gap rather than invent). Section 5
becomes **FUT-01 *and* FUT-04** dispositions for training-loop-implementation-shaped findings, folding
`trainex-r1-research-handoff.md` as a routing input only (D-36-13). Every ledger row must appear
exactly once across the Fixed/Unchanged/Deferred tables (SPEC R5).

---

### `36/evidence/` (raw probe outputs + probe scripts) (evidence dir, file-I/O)

**Analog:** `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/evidence/` and
`…/21-…/probes/`

**Layout to replicate:**
- `probes/` (or inline): one disposable script per check — Phase 21 used `probe_<name>.py`; Phase 29
  used `ac-<family>-NN.sh` + a `run-ac-suite.sh` driver. Either naming is acceptable (planner's
  discretion, D-36 the agent's-discretion note).
- `evidence/`: one captured `<probe>.stdout.txt` per probe, plus a `python_environment.stdout.txt`,
  each with a SHA-256 recorded in `36-PROBE-RESULTS.md`.

**What to replicate / what differs:** Replicate the one-stdout-file-plus-hash-per-probe layout and
an environment-evidence capture. Differs: Phase 36 probes are fresh disposable spec-consistency /
formula-sanity checks (D-36-04/05), must be fail-closed (nonzero exit on required-check failure), and
must include a protected-path guard so no probe executes against or mutates live `pinn/` code (D-36-06).
Phase 29's `run-ac-suite.sh` driver-with-one-result-line-per-check is the better model than Phase 21's
five standalone scripts, given the larger v1.6 contract set.

---

## Shared Patterns

### SHA-256 evidence capture
**Source:** `21-PROBE-RESULTS.md` (header + per-probe blocks).
**Apply to:** `36-PROBE-RESULTS.md` and every file under `36/evidence/`.
Every captured raw output file gets a committed SHA-256 in the summarizing markdown — re-derivable,
never `/tmp` (governance: verification-integrity rule).

### Requirements-coverage table
**Source:** `21-VERIFICATION.md:27-35`, `29-VERIFICATION.md` §Requirements Coverage.
**Apply to:** `36-VERIFICATION.md` for `VER-13`..`VER-18`. Columns `| Requirement | Evidence | Status |`.

### REQUIREMENTS/ROADMAP reconciliation list
**Source:** `29-VERIFICATION.md:143-163`.
**Apply to:** `36-VERIFICATION.md` R6 section — per-flip `line N: [ ] → [x]` + evidence citation; but
unlike Phase 29 (recommend-only), Phase 36 owns and applies the edits manually (D-36-17), each flip
required to match a terminal `32-ISSUE-LEDGER.md` row.

### Verification frontmatter schema
**Source:** `35-VERIFICATION.md:1-39`.
**Apply to:** `36-VERIFICATION.md` (and as a model for plan frontmatter, `35-01-PLAN.md:1-20`:
`phase` / `plan` / `type` / `wave` / `depends_on` / `files_modified` / `requirements` / `must_haves`).

### STOP-protocol governance block
**Source:** `29-VERIFICATION.md` §"Governance Verification (CLAUDE.md STOP Protocol Checks)" and
§"Human Verification Required".
**Apply to:** `36-VERIFICATION.md` — record the `pinn/`-untouched guard and any SI/ledger STOP
checkpoints (e.g. `SI-DQA-003`, D-05/D-06) here rather than silently resolving them.

---

## No Analog Found

| Artifact aspect | Reason | Planner guidance |
|------|--------|------------------|
| Standalone `36-ACCEPTANCE-MANIFEST.md` as a file separate from the run record | Phases 21 and 29 combined inventory + results into one document; no prior phase emitted a separate static manifest | Reuse the 29-ACCEPTANCE-EVIDENCE §2 column set (minus result/date columns); this is a structural split of an existing shape, not an invented one — do not fabricate new field semantics |
| Four-ID SI universe incl. `SI-DQA-003` re-adjudicated for Issue-03 relevance | 21-HANDOFF treated `SI-DQA-003` as a blanket "preserved untouched" data-quality row; Issue-03 relevance was never adjudicated | `SI-DQA-003` disposition is STOP-governed (D-36-18) — surface a gap if source-silent, do not copy the Phase 21 blanket-preserve verdict by default |

---

## Metadata

**Analog search scope:**
`.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/`,
`.planning/milestones/v1.5-phases/29-acceptance-checks-re-verification-and-handoff/`,
`.planning/phases/35-loss-energy-weight-contracts/`.
**Files inspected:** 21-PROBE-RESULTS / 21-HANDOFF / 21-VERIFICATION (+ evidence/, probes/);
29-VERIFICATION / 29-HANDOFF / 29-ACCEPTANCE-EVIDENCE-2026-06-17; 35-VERIFICATION / 35-01-PLAN.
**Pattern extraction date:** 2026-06-30
