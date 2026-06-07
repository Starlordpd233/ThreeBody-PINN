# Phase 20.5 - Plan Part 1 of 3: Planning & Governance Scaffolding (Tasks 1-4)

### Precondition

Do not execute until Task 0 in `20-5-PLAN.md` has passed in this session. The Non-Execution
Guard and Git context in `20-5-PLAN.md` apply to every task here.

### Guardrails

- Commit via `scripts/agent-commit` with `GIT_AGENT_ID` set. Never raw `git commit`, never
  `--no-verify`.
- Stage only explicitly named files. Never `git add -A` or `git add .`.
- Exclude any pre-existing unrelated working-tree edits from staging.
- No destructive operations (no resets, rebases, force-pushes, branch deletions).
- STOP and surface any decision that is not grounded per the `20-5-PLAN.md` Non-Execution
  Guard.

### Navigation

- Back to index: [`20-5-PLAN.md`](./20-5-PLAN.md)
- Previous: (this is the first part)
- Next: [`20-5-PLAN-part2.md`](./20-5-PLAN-part2.md) (Tasks 5–8)

---

## Task 1: Verify and complete the ROADMAP.md Phase 20.5 entries

**Files:**
- Modify: `.planning/ROADMAP.md` (details block only — the list item and progress row already
  exist; the coverage bump 30/30→32/32 is made in Task 2 with the SAMP-01/02 additions)

The phase directory `.planning/phases/20-5-sampling-coordinate-allocation/` already exists.

- [ ] **Step 1: Ensure the probes subdirectory exists (idempotent)**

The `probes/` subdirectory is created lazily for Task 6. Creating it now is harmless and
idempotent (it stays untracked until Task 6 adds a file):
```bash
mkdir -p ".planning/phases/20-5-sampling-coordinate-allocation/probes"
```

- [ ] **Step 2: Verify the Phase 20.5 list item already exists (do NOT re-insert)**

The Phase 20.5 top-level list item is already present in `.planning/ROADMAP.md` (added by
prior status work). Verify it — do not duplicate it:
```bash
grep -cF "**Phase 20.5: Sampling Coordinate Allocation (INSERTED)**" .planning/ROADMAP.md
```
Expected: exactly `1`. If `0`, the list item is missing and the live state has drifted — STOP
and re-derive before editing. If `>1`, a duplicate exists — STOP and surface.

- [ ] **Step 3: (Coverage bump deferred to Task 2 — no ROADMAP coverage edit here)**

The v1.4 coverage figure (`30/30` → `32/32`) is **not** changed in this task. It is bumped in
Task 2, together with the `SAMP-01`/`SAMP-02` additions to `.planning/REQUIREMENTS.md` that
justify it, so every commit stays internally consistent (`30/30` remains truthful until
SAMP-01/02 exist). Acknowledge and continue to Step 4.

- [ ] **Step 4: Add the Phase 20.5 details block**

In `.planning/ROADMAP.md`, find the line that begins the Phase 21 details section:
```
### Phase 21: Acceptance Checks, Validation Execution, and Handoff
```
Insert immediately BEFORE it (note the blank line after the block):
```
### Phase 20.5: Sampling Coordinate Allocation

**Goal**: `sampling_method.md` exposes one explicit, fixed, non-overlapping mapping from Sobol coordinates to physical sampling quantities; the §1.1 dimension claim, the "Sampling-Time Size Variability" section, and the "Velocity Sampling" section are mutually consistent and match `simulation_data/Scripts/ic_generation/ic_generation_utils.py`.
**Depends on**: Phase 16 (evidence framework). No content dependency on Phases 17–20; sequenced before Phase 21 so acceptance checks can cover it.
**Requirements**: SAMP-01, SAMP-02 (+ VER-05 applied throughout)
**Success Criteria** (what must be TRUE):

  1. Reader finds a "Sobol Coordinate Allocation Convention" subsection in `sampling_method.md` mapping `(u_1, …, u_7)` to physical quantities with no double-booking.
  2. Reader can verify the §1.1 dimension claim, "Sampling-Time Size Variability", and the Sobol coordinate allocation within "Velocity Sampling" are mutually consistent and agree with the locked `d = 3 + δ_s + 3δ_v` allocation. (The momentum-conservation procedure in "Velocity Sampling" was already reconciled to the code by Phase 18 (FRAME-03) — it states the symmetric `v1 = v3 = -v2/2` split that matches `ic_generation_utils.py` — so it is not an open discrepancy; Task 8 verifies this.)
  3. The phase-local gap register records GAP-20-5-01/02/03 at `RESOLVED-WITH-INSTRUCTION`.
  4. `20-5-DATA-ALIGNMENT.md` records the alignment with `ic_generation_utils.py` and the FUT-01 hand-off, and defines `AC-SAMP-01` for Phase 21 execution.

**Plans**: `.planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md` (authoritative GSD copy).

```

- [ ] **Step 5: Verify the progress-table row already exists (do NOT re-insert)**

The Phase 20.5 progress-table row is already present in `.planning/ROADMAP.md`. Verify it —
do not duplicate it:
```bash
grep -cF "| 20.5 Sampling Coordinate Allocation (INSERTED) |" .planning/ROADMAP.md
```
Expected: exactly `1`. If `0`, the row is missing and live state has drifted — STOP. If `>1`,
a duplicate exists — STOP and surface.

- [ ] **Step 6: Verify the ROADMAP structural edits (exact-row checks)**

Run:
```bash
grep -cF "**Phase 20.5: Sampling Coordinate Allocation (INSERTED)**" .planning/ROADMAP.md   # list item
grep -cF "### Phase 20.5: Sampling Coordinate Allocation" .planning/ROADMAP.md              # details heading
grep -cF "| 20.5 Sampling Coordinate Allocation (INSERTED) |" .planning/ROADMAP.md          # progress row
```
Expected: each returns exactly `1` — one list item, one details heading, one progress row. A
`0` means a required edit did not apply; a value `>1` means a duplicate was introduced. In
either case STOP, do not commit, and re-check. (The coverage line stays `30/30` here; Task 2
bumps it to `32/32` with the SAMP-01/02 additions and verifies it.)

- [ ] **Step 7: Commit**

Stage only the ROADMAP and commit with `scripts/agent-commit` (body required — `.planning/`
is a risk-elevated path):
```bash
git add .planning/ROADMAP.md
GIT_AGENT_ID="codex-gpt-5" scripts/agent-commit \
  -m "docs(planning): insert Phase 20.5 roadmap details block" \
  -m "Insert the absent Phase 20.5 details block between the Phase 20 and Phase 21 details sections. The Phase 20.5 list item and progress row already existed and were only verified. The coverage bump 30/30 to 32/32 is made in Task 2 with the SAMP-01/02 additions that justify it."
```
Note: the empty `probes/` directory is not tracked by git until it has a file (added in
Task 6); this is expected.

---

## Task 2: Add SAMP requirements and the SCOPE-05 data-alignment rule to REQUIREMENTS.md

**Files:**
- Modify: `.planning/REQUIREMENTS.md`

- [ ] **Step 1: Add the Sampling Coordinate Allocation requirement section**

In `.planning/REQUIREMENTS.md`, find the start of the Verification section:
```
### Verification and Handoff
```
Insert immediately BEFORE it:
```
### Sampling Coordinate Allocation

- [ ] **SAMP-01**: `sampling_method.md` documents an explicit Sobol coordinate allocation convention with no coordinate reused for two independent physical quantities. Allocation order: position → optional scale → optional velocity. Dimension formula `d = 3 + δ_s + 3δ_v`, where `δ_s = 1` iff sampling-time scaling is enabled and `δ_v = 1` iff velocity sampling is enabled.
- [ ] **SAMP-02**: The §1.1 dimension claim, the "Sampling-Time Size Variability" prose, and the "Velocity Sampling" prose/formula in `sampling_method.md` are mutually consistent and agree with the locked allocation, matching `simulation_data/Scripts/ic_generation/ic_generation_utils.py` (the implementation that generated the existing standard quasi-random dataset).

```

- [ ] **Step 2: Amend SCOPE-02**

In `.planning/REQUIREMENTS.md`, find the SCOPE-02 table row:
```
| **SCOPE-02** `sampling_method.md` revisions | **In scope, limited to FRAME-03** — hierarchical post-perturbation COM offset wording and any cross-reference needed for the unified preprocessing contract. No sampling-method content unrelated to Issue 01 is rewritten. |
```
Replace it with:
```
| **SCOPE-02** `sampling_method.md` revisions | **In scope, limited to (a) FRAME-03** — hierarchical post-perturbation COM offset wording and any cross-reference needed for the unified preprocessing contract — **AND (b) SAMP-01/SAMP-02** — the Sobol coordinate allocation convention (Phase 20.5). No sampling-method content unrelated to (a) or (b) is rewritten. Any other sampling-method discrepancy noticed during Phase 20.5 (for example, the §2.1 enhancement framing) is out of Phase 20.5 scope and handled separately if needed, not silently fixed. |
```

- [ ] **Step 3: Add the SCOPE-05 data-alignment rule**

In `.planning/REQUIREMENTS.md`, find the SCOPE-04 table row:
```
| **SCOPE-04** Disposable validation probes | **In scope, limited** — probes may be created, recorded, or run only to test risky framework contracts and produce evidence for VER-04. They are not production framework code and are not packaged as reusable `pinn/` validation infrastructure during v1.4. |
```
Insert immediately AFTER it:
```
| **SCOPE-05** Data-spec alignment for sampling-method edits | When v1.4 framework-spec edits describe the data-generation pipeline, they MUST match the actual behavior of `simulation_data/Scripts/ic_generation/`. The no-live-code directive (2026-05-19) targets `pinn/` only; `simulation_data/Scripts/ic_generation/` is a permitted grounding source for data-generation specs because the existing dataset is fixed and the framework must remain compatible with it. Spec divergences from data must be (i) reconciled to match data, (ii) flagged in `docs/findings/` for separate handling, or (iii) explicitly authorized by the user as a data-regeneration directive for FUT-01. |
```

- [ ] **Step 4: Add SAMP traceability rows**

In `.planning/REQUIREMENTS.md`, find the ARCH-05 traceability row (Phase 20 is complete as of
2026-06-05, so the status reads `Complete`, not `Pending`):
```
| ARCH-05 | Phase 20 | Complete |
```
Insert immediately AFTER it:
```
| SAMP-01 | Phase 20.5 | Pending |
| SAMP-02 | Phase 20.5 | Pending |
```

- [ ] **Step 5: Update both coverage blocks (REQUIREMENTS and ROADMAP)**

The REQUIREMENTS coverage and the ROADMAP coverage must both move 30→32 here, together with
the SAMP-01/02 additions that justify them, so they land in one commit (Step 7) and each stays
truthful.

In `.planning/REQUIREMENTS.md`, find:
```
**Coverage:**
- v1.4 requirements: 30 total (5 EVID + 4 IO + 4 FRAME + 6 PHYS + 5 ARCH + 6 VER)
- Mapped to phases: 30
- Unmapped: 0
- SCOPE-01/02/03/04 are scope-boundary annotations (see "Scope Boundaries" table above), not numbered requirements.
```
Replace with:
```
**Coverage:**
- v1.4 requirements: 32 total (5 EVID + 4 IO + 4 FRAME + 6 PHYS + 5 ARCH + 2 SAMP + 6 VER)
- Mapped to phases: 32
- Unmapped: 0
- SCOPE-01 through SCOPE-05 are scope-boundary annotations (see "Scope Boundaries" table above), not numbered requirements.
```

Then in `.planning/ROADMAP.md`, find:
```
**Coverage:** 30/30 v1.4 requirements mapped
```
Replace with:
```
**Coverage:** 32/32 v1.4 requirements mapped
```

- [ ] **Step 6: Verify the REQUIREMENTS edits (exact-artifact checks)**

Run:
```bash
grep -cF "**SAMP-01**:" .planning/REQUIREMENTS.md                                   # expect 1 (definition)
grep -cF "**SAMP-02**:" .planning/REQUIREMENTS.md                                   # expect 1 (definition)
grep -F  "**SCOPE-02**" .planning/REQUIREMENTS.md | grep -c "FRAME-03"              # expect 1
grep -F  "**SCOPE-02**" .planning/REQUIREMENTS.md | grep -c "SAMP-01/SAMP-02"       # expect 1
grep -cF "**SCOPE-05** Data-spec alignment" .planning/REQUIREMENTS.md              # expect 1 (row)
grep -cF "simulation_data/Scripts/ic_generation/" .planning/REQUIREMENTS.md        # expect >= 1 (SCOPE-05 path)
grep -cF "| SAMP-01 | Phase 20.5 | Pending |" .planning/REQUIREMENTS.md            # expect 1 (traceability)
grep -cF "| SAMP-02 | Phase 20.5 | Pending |" .planning/REQUIREMENTS.md            # expect 1 (traceability)
grep -cF "32 total" .planning/REQUIREMENTS.md                                       # expect 1 (coverage)
grep -cF "Mapped to phases: 32" .planning/REQUIREMENTS.md                           # expect 1 (coverage)
grep -cF "32/32 v1.4 requirements" .planning/ROADMAP.md                             # expect 1 (ROADMAP coverage)
```
Each line must return its stated count. A `0` means an edit did not apply; a value above the
expected count means a duplicate was introduced. In either case STOP, do not commit, and
re-check the specific edit.

- [ ] **Step 7: Commit**

Stage the requirements file **and the ROADMAP** (both coverage blocks moved together) and
commit with `scripts/agent-commit` (body required — `.planning/` is a risk-elevated path and
this is a multi-file commit):
```bash
git add .planning/REQUIREMENTS.md .planning/ROADMAP.md
GIT_AGENT_ID="codex-gpt-5" scripts/agent-commit \
  -m "docs(planning): add SAMP requirements and SCOPE-05" \
  -m "Add the Phase 20.5 sampling requirements SAMP-01 and SAMP-02, the SCOPE-05 data-generation grounding carveout, the SCOPE-02 amendment for SAMP-01/SAMP-02, the SAMP traceability rows, and the 30 to 32 coverage totals in both REQUIREMENTS.md and ROADMAP.md."
```

---

## Task 3: Propagate the SCOPE-05 governance principle after REQUIREMENTS.md

**Files:**
- Modify: `AGENTS.md` and `ANTIGRAVITY.md` **only**. `CLAUDE.md` and `GEMINI.md` are
  **symlinks to `AGENTS.md`** — editing `AGENTS.md` already updates them. Do **not** edit or
  stage `CLAUDE.md`/`GEMINI.md` separately, and do not let any tool follow the symlinks and
  write the same change twice.

This task runs immediately after Task 2 because SCOPE-05 must exist in
`.planning/REQUIREMENTS.md` before root governance docs can cite it, and before Task 5
commits risk-elevated `sampling_method.md` edits that rely on the SCOPE-05 carveout. Commit
`a9ecd51` already records Phase 20.5 status in `.planning/PROJECT.md`, `.planning/STATE.md`,
and `.planning/MILESTONES.md`; this task should not restate those status updates.

- [ ] **Step 0: Verify symlink topology**

```bash
ls -l AGENTS.md CLAUDE.md GEMINI.md ANTIGRAVITY.md
```
Confirm `CLAUDE.md -> AGENTS.md` and `GEMINI.md -> AGENTS.md`, and that `ANTIGRAVITY.md` is a
separate regular file. If the topology differs, STOP and re-derive the edit targets before
proceeding.

- [ ] **Step 1: Apply the SCOPE-05 note with anchored edit targets**

Use the manual anchored edit path below as the primary path. If the current agent runtime has a
reliable `gsd-docs-update` skill, it may be used only as a drafting aid; review its output
against these same anchors before staging.

Insertion anchor:
- In `AGENTS.md`, insert in the **Source of Truth** section immediately after the existing
  paragraph that says live `pinn/` code may be referenced only in forward-pointing FUT-01
  hand-off documents.
- In `ANTIGRAVITY.md`, insert in the equivalent root-instruction/source-of-truth section after
  the same `pinn/` no-live-code directive. If the equivalent anchor is not present, STOP and
  re-derive the insertion point; do not place the note in an unrelated section.

Add this narrow note to each real target file:
```markdown
**SCOPE-05 data-generation carveout:** `simulation_data/Scripts/ic_generation/` is a permitted
grounding source for data-generation specs in
`pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`. This is a narrow
carveout from the `pinn/` no-live-code directive, not a general live-code exception. The
canonical rule lives in `.planning/REQUIREMENTS.md` SCOPE-05.
```

Do not restate the full SCOPE-05 row text; link to the canonical source. Do not edit
`CLAUDE.md`/`GEMINI.md` directly.

- [ ] **Step 2: Optional skill-output review (skip if Step 1 was manual)**

If `gsd-docs-update` was used as a drafting aid, review its output. Confirm it (a) adds the
SCOPE-05 cross-reference after
Task 2 has landed the canonical rule in `REQUIREMENTS.md`, (b) does not contradict the
existing `pinn/` no-live-code directive (SCOPE-01), (c) does not broaden the carveout beyond
`simulation_data/Scripts/ic_generation/`, (d) does not duplicate the `a9ecd51` status
updates, and (e) edited `AGENTS.md`/`ANTIGRAVITY.md` only — **not** `CLAUDE.md`/`GEMINI.md`
separately.

- [ ] **Step 3: If a tool edits unexpected files**

If a tool wrote to files outside `AGENTS.md` and `ANTIGRAVITY.md`, stop immediately. Remove
only the attempted SCOPE-05 edit with a targeted patch and return to the manual anchored path.
Do not use broad reset/restore commands.

- [ ] **Step 4: Stage explicitly and commit**

Run `git status --short`, confirm only `AGENTS.md` and `ANTIGRAVITY.md` changed (the symlinks
`CLAUDE.md`/`GEMINI.md` should NOT appear as separate modifications). If `CLAUDE.md` or
`GEMINI.md` appear as separate modified paths, STOP; a tool likely followed or replaced a
symlink. Remove only the attempted Task 3 edit with a targeted patch and retry against
`AGENTS.md` and `ANTIGRAVITY.md` explicitly.

Then:
```bash
git add AGENTS.md ANTIGRAVITY.md
GIT_AGENT_ID="codex-gpt-5" scripts/agent-commit \
  -m "docs(governance): propagate SCOPE-05 data-spec alignment rule" \
  -m "Cross-reference the canonical SCOPE-05 data-generation grounding carveout from the root agent instructions so future agents treat simulation_data/Scripts/ic_generation/ as a permitted grounding source distinct from the pinn/ no-live-code directive. Edits AGENTS.md and ANTIGRAVITY.md only; CLAUDE.md and GEMINI.md inherit via symlink."
```

---

## Task 4: Verify the gap register and milestone gap index (verification-only)

**Files:** none modified. The phase-local gap register and the milestone gap index already
exist (created and resolved 2026-05-19). This task confirms they are present and internally
consistent. It produces **no commit**. Do NOT recreate, renumber, or re-count anything.

If any check below fails, the live state has drifted from what this plan assumes. Do not
invent a replacement structure or count: STOP and, for any process-artifact schema decision
(gap-index format, gap IDs, counts), follow the `CLAUDE.md` STOP protocol before changing
anything.

- [ ] **Step 1: Verify the phase-local gap register**

```bash
GAPS=.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md
test -f "$GAPS" && echo "EXISTS"
grep -cF "## GAP-20-5-01" "$GAPS"              # expect 1
grep -cF "## GAP-20-5-02" "$GAPS"              # expect 1
grep -cF "## GAP-20-5-03" "$GAPS"              # expect 1
# Verify each gap's OWN section is RESOLVED-WITH-INSTRUCTION (not just an aggregate count,
# which could false-pass if one gap had the status twice and another had none):
for g in GAP-20-5-01 GAP-20-5-02 GAP-20-5-03; do
  n=$(awk -v g="$g" '
    $0 ~ ("^## " g) {ingap=1; next}
    /^## / {ingap=0}
    ingap && /RESOLVED-WITH-INSTRUCTION/ {c++}
    END {print c+0}' "$GAPS")
  echo "$g -> RESOLVED-WITH-INSTRUCTION x$n (expect >= 1)"
done
```
All three gap IDs must be present, and each gap's own section must report
`RESOLVED-WITH-INSTRUCTION` (each loop line must print `x1` or more). Preserve the
`GAP-20-5-0X` IDs exactly — do not rename them to dot-decimal form.

- [ ] **Step 2: Verify the milestone gap index has exactly one Phase 20.5 section**

```bash
INDEX=.planning/milestones/v1.4-GAPS.md
grep -cF "## Phase 20.5: Sampling Coordinate Allocation" "$INDEX"   # expect 1
grep -cF "GAP-20-5-01" "$INDEX"                                     # expect 1
grep -cF "GAP-20-5-02" "$INDEX"                                     # expect 1
grep -cF "GAP-20-5-03" "$INDEX"                                     # expect 1
```

- [ ] **Step 3: Verify the milestone counts are already consistent — do NOT change them**

The index already records `total_gaps: 21` / `resolved_gaps: 21`, and those 21 gaps
**already include** the three Phase 20.5 gaps. A bump to 24 would be wrong: it would make the
frontmatter disagree with the 21 gaps actually recorded. Confirm the frontmatter equals the
actual number of distinct gap rows and leave it unchanged:

```bash
INDEX=.planning/milestones/v1.4-GAPS.md
grep -cE "^total_gaps: 21$"    "$INDEX"   # expect 1
grep -cE "^resolved_gaps: 21$" "$INDEX"   # expect 1
# distinct gap-row IDs in the index — must equal 21:
grep -oE "^\| GAP-[0-9]+(-[0-9]+)+" "$INDEX" | sort -u | wc -l   # expect 21
```
If `total_gaps`/`resolved_gaps` do not match the distinct gap-row count, STOP — the index is
internally inconsistent, and reconciling it is a process-artifact decision that must be
surfaced under the STOP protocol, not guessed.

This task makes no file changes and therefore has **no commit**.

---
