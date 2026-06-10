# Phase 23: Research Package Assembly - Pattern Map

**Mapped:** 2026-06-10
**Files analyzed:** 9 deliverables (1 package dir + 6 in-package artifacts + 1 phase-local + conditional gap files)
**Analogs found:** 9 / 9 (all markdown-artifact analogs in-repo; no code analogs apply)

> This is a documentation-assembly phase. "Role" = artifact role (manifest, research-brief, register, characterization, snapshot, gap-register), "Data Flow" = transform / aggregate / copy / index. There are no controllers/services. Every analog is an existing markdown artifact; the planner copies its heading skeleton, frontmatter, and table schema — not code.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `research_package/README.md` (manifest/index) | manifest | index | `.planning/research/edl/INDEX.md` + `ctl_pinn_resolution.md` frontmatter | role-match |
| `research_package/<framed-questions>.md` (PKG-02) | research-brief | transform | `.planning/research/edl/EDL-19-01-epsilon-H.md` | exact |
| `research_package/<claims-table>.md` (PKG-03, CLM IDs) | register/table | aggregate | `16-ISSUE-LEDGER.md` Status Table + EDL `INDEX.md` Registry | exact |
| `research_package/<consolidated-context>.md` (D-05) | aggregation | aggregate | `simulation_data/Documentation/README.md` (sectioned, source-labeled) | role-match |
| `research_package/specs/*.md` snapshots (issue doc, ctl, pinn_arch, sampling, DQA) | snapshot | copy (byte-for-byte) | source files themselves + `git hash-object` provenance | mechanical |
| `23-DQA-CHARACTERIZATION.md` (PKG-04, phase-local) | characterization | transform | `23-RESEARCH.md` §"DQA Characterization Inputs" + phase-artifact `NN-*.md` convention | role-match |
| delivery note (D-16; in plan SUMMARY or package README) | handoff note | transform | issue-02 `## References` + `ctl_pinn_resolution.md` §0 supersession block | partial |
| `23-GAPS.md` (created only on first gap) | gap-register | index | `19-GAPS.md` | exact |
| `.planning/milestones/v1.5-GAPS.md` (created only on first gap) | gap-index | index | `.planning/milestones/v1.4-GAPS.md` | exact |

## Pattern Assignments

### `research_package/README.md` — manifest/index (PKG-01, D-02)

**Analog:** `.planning/research/edl/INDEX.md` (registry table) + `ctl_pinn_resolution.md` frontmatter (provenance pinning).

**Frontmatter pattern** (from `ctl_pinn_resolution.md` lines 1-16): YAML block with `title`, `date`, `status`, `source_files`, `supersedes`, `project`. For the manifest, adapt to record snapshot provenance: `title`, `package_for: issue-02`, `source_commit`, `created`, `self_contained: true`.

**Per-file manifest table** — copy the column schema from EDL `INDEX.md` Registry table:
```
| EDL ID | Linked gap | Topic | Status | Brief | Blocking summary |
```
Adapt to D-02's required fields (role annotation, canonical source path, source commit hash):
```
| Snapshot file | Role annotation | Canonical source path | Source commit hash | Treatment |
```
**Commit-hash capture** (Don't-Hand-Roll, RESEARCH §230): `git log -1 --format=%H -- <path>` per file; `git rev-parse HEAD` for the package-wide pin. Record in committed state, not /tmp.

**Self-contained rule** (D-02, Pitfall 7): the manifest must reference ONLY its own snapshot copies — no repo-relative paths that dangle for repo-blind agents.

---

### `research_package/<framed-questions>.md` — research brief (PKG-02, D-08/D-09/D-10)

**Analog:** `.planning/research/edl/EDL-19-01-epsilon-H.md` — exact structural match for "neutral, never-presuppose-an-answer" external-research framing.

**Heading skeleton to copy** (EDL-19-01 headings, lines 12-164):
```
# <title>
## Short Answer Needed
## Current Project State
## Why This Is A Gap
## Agent Understanding
## Candidate Resolutions
### Option A: ...
### Option B: ...
## Dependency Map
## Core Files To Audit
## External Research Questions
## Return Format
```
The "Candidate Resolutions / Option A-E" shape (lines 64-96) is the model for D-09 neutral framing: present each finding's positions as options, never settle. The "Return Format" section (line 164) is the model for instructing the external research what to produce.

**D-08 cluster grouping** — depart from the single-question EDL brief by grouping per-finding questions into the three downstream-contract clusters (ingestion/selection, sampling/precision/global-scale, validation-metrics) that mirror Phases 26-28. Each finding's line ranges and in-scope/excluded status come pre-tabulated in `23-RESEARCH.md` §"Issue-02 Finding Inventory".

**D-10 hard-constraints preamble** — the six locked v1.4 conventions with exact citations are in `23-RESEARCH.md` §"Locked v1.4 Convention Citations". Copy verbatim; cite the SCS gate to `data_quality_assessment.md` lines 120/130/234 + SI-DQA-003 (Pitfall 1 — never imply it lives in an editable spec).

**Frontmatter** — follow EDL-19-01 (lines 1-10): `edl_id`-style id, `status`, `phase`, `topic`, `created`, `canonical: false`.

---

### `research_package/<claims-table>.md` — claims register (PKG-03, D-11/D-12/D-13)

**Analog:** `16-ISSUE-LEDGER.md` Status Table (stable-ID register with status + source columns) — exact role match.

**Table schema** — copy the stable-ID-per-row pattern from `16-ISSUE-LEDGER.md` line 17:
```
| ID | Title | Phase | Status | ... | Sources | ... | Last Updated |
```
Adapt to the CLM contract (D-11): every dataset figure gets a row.
```
| CLM ID | Figure | Value (claimed) | Source citation | Status | Phase-24 check |
```
`Status` ∈ {`claimed-unverified`, `verified`}. The pre-classified candidate rows (value, issue-doc line, grounding, recommended status) are already enumerated in `23-RESEARCH.md` §"CLM Candidate Claims Inventory" — copy them as the starting table.

**D-13 verified-status rule:** only `simulation_data/Documentation/` files or committed prior-phase probe evidence justify `verified`; `.planning/codebase/*.md` does NOT. Default `claimed-unverified` (Pitfall 3). The table IS Phase 24's checklist (D-12) — every inline figure in package prose must reference its CLM ID.

---

### `research_package/<consolidated-context>.md` — aggregation file (PKG-01, D-05)

**Analog:** `simulation_data/Documentation/README.md` — sectioned dataset-fact document; the model for one self-contained file holding scattered fragments.

**Pattern:** one file, each fragment under a heading labeled with its source path (D-05 "each fragment labeled with its source path"). Fragments and their source line ranges are pre-located in `23-RESEARCH.md` §"Document List & Roles" (last paragraph): README Dataset Sizes (81-90), File Naming/Mapping (193-231), Brutus Parameters by Variant (584-628), Completeness Checks (637-660); full `standard_quasi_random_ids_not_in_gold.md`; blacklist summary (65 = 2 hier + 63 std via `python3 -c "import json..."`); `calculate_metrics.py` provenance excerpt (SCOPE-07).

**Hard constraints:** specs are NEVER consolidated here (D-03 — they ship as intact snapshots); `pinn/` is EXCLUDED (D-06/SCOPE-10, Pitfall 5). The D-07 consolidation plan (what gets consolidated vs stays standalone) MUST be surfaced to the user before assembly — model this as a hard user gate in the plan.

---

### `research_package/specs/*.md` — byte-for-byte snapshots (D-03)

**Analog:** the source files themselves; provenance pattern from `ctl_pinn_resolution.md` `source_files:`/`supersedes:` frontmatter.

**Pattern:** mechanical copy — `ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md` (annotated FROZEN/SCOPE-08), `02-data-pipeline-and-validation.md` (annotated NON-authoritative), `data_quality_assessment.md` (annotated "research report, not authoritative spec"/SCOPE-09). No summarization, no excerpting (Pitfall 5). Verify byte-identity with `git hash-object` / `diff` against source (acceptance check PKG-01). Each snapshot's source path + commit hash recorded in the manifest.

---

### `23-DQA-CHARACTERIZATION.md` — characterization report (PKG-04, D-14, phase-local)

**Analog:** `23-RESEARCH.md` §"DQA Characterization Inputs" (the content is already drafted there) + the `NN-*.md` phase-artifact naming convention.

**Section skeleton** (from D-14 requirements + RESEARCH §"DQA Characterization Inputs"):
```
# Phase 23: data_quality_assessment.md Characterization
**Provenance** (git origin/history — git log --follow)
**Section map** (§1-§6 + Source Issues, line ranges)
**Relation to dataset↔framework compatibility verification** (what it covers / what remains unverified)
**Package-inclusion recommendation**
```
The provenance (commits `314d956`/`460cf4b`/`b5edcc2`/`6ab19ea`/`3732f1f`/`d3fcff9`), section map, and INCLUDE recommendation are pre-derived in RESEARCH. Zero edits to `data_quality_assessment.md` (verify `git diff --quiet`). This is an EARLY task (D-15) — completes before the document list is finalized.

**Frontmatter/header:** match prior phase artifacts (`17-CONTEXT.md` style): `# Phase 23: ... ` H1, `**Field:** value` metadata lines, `---` separator.

---

### Delivery note — handoff (D-16)

**Analog:** issue-02 `## References` section (annotated path list) + `ctl_pinn_resolution.md` §0 supersession/scope block.

**Must state** (D-16): how to use the package for external multi-AI research; that the resolution doc lands at `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/` (exact path); that `ctl_pinn_resolution.md` is a format precedent (suggestion only, no required schema — Don't-Hand-Roll); that Phase 24 runs in parallel and forwards a DATA-07 CLM-keyed correction addendum; that Phases 25-29 gate on resolution-doc landing + Phase 24 completion. STATE.md gate-open recorded via gsd-tools handlers ONLY (D-17, Pitfall 7) — never hand-edited.

---

### `23-GAPS.md` + `.planning/milestones/v1.5-GAPS.md` — gap registers (created ONLY on first gap)

**Analogs:** `19-GAPS.md` (phase-local) and `.planning/milestones/v1.4-GAPS.md` (milestone index).

**Required-fields header** (copy from `19-GAPS.md` line 18): Decision point - Where in artifact - Task context - Classification - Source silence (file:line) - Mathematical/engineering grounding - Agent was tempted to - What the user needs to decide - Confidence of impact - Status - Resolution note. Entry headings `## GAP-23-NN: <title>`. Neither file exists yet — create on first surfaced gap, per the v1.5 STOP protocol (CONTEXT line 14, governance). Subagents return findings to the parent; the parent decides and logs.

## Shared Patterns

### Provenance pinning
**Source:** `ctl_pinn_resolution.md` frontmatter (`source_files`, `supersedes`) + `git log -1 --format=%H -- <path>`
**Apply to:** manifest/README (every snapshot row), spec snapshots, delivery note
Pin source commit hashes so the snapshot is traceable and the research state is frozen (D-02). Record in committed state, not /tmp.

### Stable-ID register table
**Source:** `16-ISSUE-LEDGER.md` Status Table + EDL `INDEX.md` Registry
**Apply to:** claims table (CLM-NN), gap register (GAP-23-NN)
Markdown table, one stable-ID row per item, explicit `Status` column, source citation column.

### Neutral external-research framing
**Source:** `EDL-19-01-epsilon-H.md` (Candidate Resolutions / Options + Return Format)
**Apply to:** framed-questions doc, and the manifest's source-treatment preamble
Present positions as options; never presuppose an answer (D-09). Both the issue doc AND its "Recommended Resolutions" are non-authoritative — cite the SCS-threshold seed conflict as the worked example (Pitfall 2).

### Phase-artifact header convention
**Source:** `17-CONTEXT.md` / prior `NN-*.md`
**Apply to:** `23-DQA-CHARACTERIZATION.md`, `23-GAPS.md`
`# Phase 23: <name>` H1, `**Field:** value` metadata lines, `---` separators, `NN-` filename prefix in `.planning/phases/23-*/`.

### Self-contained / no-dangling-reference
**Source:** D-02 requirement (no direct analog — it is the inversion of the repo-relative path style in issue-02 `## References`)
**Apply to:** every in-package file
External AI agents have no repo access; in-package files reference only sibling snapshots. The issue-02 References block (with its `../../pinn/...` paths) is the anti-pattern to avoid carrying into the package.

## No Analog Found

| File | Role | Reason | Planner guidance |
|------|------|--------|------------------|
| (none) | — | Every Phase 23 deliverable maps to an existing repo markdown artifact | Use the analogs above; no RESEARCH-only fallback needed |

The only "novel" aspect is the package *directory* co-location of inputs+outputs, which itself mirrors `research_reports/01-architecture-and-physics-foundations/` (D-01) — the layout precedent is concrete, not absent.

## Metadata

**Analog search scope:** `.planning/research/edl/`, `.planning/milestones/v1.4-phases/{16,17,19}/`, `.planning/milestones/v1.4-GAPS.md`, `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-*/`, `simulation_data/Documentation/`, `pinn_instruction/issues/02-*.md`
**Files scanned:** 9 analogs (headings/frontmatter/table-schema extracted)
**Pattern extraction date:** 2026-06-10
