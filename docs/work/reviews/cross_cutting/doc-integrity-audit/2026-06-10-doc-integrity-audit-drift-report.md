---
status: active
purpose: review-findings
created: 2026-06-10
milestone: v1.5
retirement_trigger: finding-by-finding closeout complete and reference audit passes
---

# Documentation Integrity Audit — Drift Report (2026-06-10)

Audit of the 13-doc inventory defined in
`docs/brainstorms/2026-06-10-doc-integrity-audit-requirements.md` (R1–R13), executed per
`docs/work/plans/cross_cutting/doc-integrity-audit/2026-06-10-doc-integrity-audit-plan.md` (U3/U4)
on branch `milestone/v1.5`. Procedure as captured in
`docs/runbooks/maintenance/doc-integrity-audit-runbook.md`.

## Method

- **Track 1 (R3):** referenced paths/scripts and internal cross-references checked on all 13 docs.
- **Track 2 (R4):** drift detection ran on all **11** Class 1–2 docs. (Plan §U3 says "9 Class 1–2
  docs"; the authoritative inventory contains 6 Class 1 + 5 Class 2 = 11. The plan figure is a
  miscount; the inventory governed.)
- **Track 3 (R5):** sampled content verification on the 2 Class 3 docs against on-disk
  `simulation_data/` — every check recorded as claim / method / result.
- **R6:** `AGENTS.md` ↔ `ANTIGRAVITY.md` consistency; symlink integrity.
- **Execution:** five read-only research subagents performed the sweeps; the parent agent
  adjudicated every finding. All Class 3 contradictions and all accepted findings below were
  **re-derived directly by the parent agent**; three subagent-suggested findings were refuted or
  materially corrected during adjudication and are recorded under "Rejected candidate findings".
- **R2 guard:** no file was edited during the audit pass. Excluded surfaces were read only for
  cross-checking.

## Verdict Summary

| # | Doc | Class | Verdict | Findings |
|---|---|---|---|---|
| 1 | `README.md` | 1 — root entry | drift-found | F-01 |
| 2 | `AGENTS.md` (+ `CLAUDE.md`/`GEMINI.md` symlinks) | 1 — root entry | verified-current | — |
| 3 | `ANTIGRAVITY.md` | 1 — root entry | verified-current | — |
| 4 | `.claude/rules/repo-map.md` | 1 — agent rules | drift-found | F-02 |
| 5 | `.claude/rules/dataset-reference.md` | 1 — agent rules | drift-found | F-03 |
| 6 | `.claude/rules/pinn-reference.md` | 1 — agent rules | drift-found | F-04, F-05 |
| 7 | `docs/README.md` | 2 — process | verified-current | — |
| 8 | `docs/git-guidelines.md` | 2 — process | verified-current | — |
| 9 | `pinn_instruction/issues/README.md` | 2 — sub-area | drift-found | F-06 |
| 10 | `pinn_instruction/markdown_conversion/README.md` | 2 — sub-area | drift-found | F-07 |
| 11 | `tools/spec-render-check/README.md` | 2 — sub-area | verified-current | — |
| 12 | `simulation_data/Documentation/README.md` | 3 — grounding | drift-found | F-08, F-09, F-10 |
| 13 | `simulation_data/Data/testing_data/README_TESTING.md` | 3 — grounding | drift-found | F-11, F-12 |

**Totals:** 5 verified-current, 8 drift-found, 0 not-verifiable. 12 findings: 7 Class 1–2
(direct-fix queue, U5) and 5 Class 3 (gated, report-only, U6).

---

## Per-Doc Records — Class 1

### 1. `README.md` — drift-found

Checks: 58 referenced paths extracted and tested (`test -e`); all real references resolve (6
template/placeholder examples excluded as non-assertions). 17 headings, no broken anchors.
Track 2 baseline: last commit 2026-06-08; repo changes since reviewed via
`git log --name-only` over described areas.

- **F-01 (stale-claim, minor).** The "Architecture & Repository Map" section (lines 29–42, Core +
  Ancillary Systems) does not list `tools/`. `tools/spec-render-check/` was created 2026-06-09
  (commits `d63de599`, `48a333d5`, `faa73d08` — Phase 22 render-verification suite), after the
  doc's last commit. Fix: add a `tools/` bullet to Ancillary Systems.

### 2. `AGENTS.md` — verified-current

Checks: 83 referenced paths tested — all exist (incl. `.planning/REQUIREMENTS.md`,
`scripts/agent-commit`, `docs/git-guidelines.md`, framework-spec paths). 22 headings, no broken
anchors. Last commit 2026-06-10 (same day as audit); no repo changes post-date it.
Note (not a finding): `.planning/milestones/v1.5-GAPS.md` is referenced as the designated v1.5
gap index and does not exist yet — it is created on first gap entry by the STOP protocol, same
lifecycle as `v1.4-GAPS.md`.

### 3. `ANTIGRAVITY.md` — verified-current

Checks: 77 referenced paths tested — 59 exist, 18 are placeholders/env-var examples, 0 broken.
All 6 dataset variant folders and 4 key scripts verified on disk. 47 headings, no broken
references. Track 2: zero changes to framework specs since last commit (`b6a82cf4`).

**R6 result: PASS.** `CLAUDE.md → AGENTS.md` and `GEMINI.md → AGENTS.md` symlinks intact and
resolving (`ls -la`, `readlink`). Side-by-side review found complementary, not contradictory,
guidance; `ANTIGRAVITY.md` line 5 explicitly defers to `AGENTS.md` on conflict; both state the
same commit protocol and hook-bypass prohibition.

### 4. `.claude/rules/repo-map.md` — drift-found

Checks: all 8 Key Directories and all 8 Key Scripts rows verified on disk (`test -f`/`ls -d`).
Track 2 baseline `328b55bb` (2026-05-24): no moves/renames in the referenced script paths since.

- **F-02 (stale-claim, minor).** "Key Directories" omits two directories created after the doc's
  last commit: `tools/` (verification tooling, 2026-06-09, Phase 22) and the governed `docs/`
  tree (purpose-based docs structure with `docs/README.md` rules, `docs/runbooks/`,
  `docs/work/`, created 2026-06-08, commit `847bad6f`). Fix: add both entries to Key
  Directories.

### 5. `.claude/rules/dataset-reference.md` — drift-found

Checks: 2 IC folders + 4 Brutus output folders exist; file-count claims spot-verified
(`ic_standard_quasi_random` = 2,749 ✓; `brutus_standard_quasi_random_gold_standard` = 2,565 ✓);
184-ID gold exclusion consistent with `standard_quasi_random_ids_not_in_gold.md` ✓; 7 pipeline
script paths + provenance files exist, including
`simulation_data/Scripts/debug/audit_and_backfill_brutus_result_footers.py` ✓; parameter-set
table matches observed `Result:` footers ✓; mapping rule ("File names do **not** encode 'gold'")
matches observed reality ✓.

- **F-03 (contradiction).** "Known Issues and Gotchas" first bullet claims: "**All files contain
  a `Result:` footer**, but schema varies — some omit `eta`, a small subset … omit both `eta` and
  `tol`." Contradicted by direct observation: 1,550/4,857 files in `brutus_hierarchical`,
  701/2,749 in `brutus_standard_quasi_random`, and 219/2,565 in
  `brutus_standard_quasi_random_gold_standard` contain **no `Result:` footer at all** (tail scan
  of every file; full-file scans of samples find no `eta`/`tol`/`Lw`/`Result` marker anywhere).
  The doc's own "Mandatory Parsing Rules" item 2 states the opposite — "Result footer is
  optional: **Many files omit it**" — which matches reality. Corroborated by the doc's cited
  audit `simulation_data/Validation/audit_reports/footer_audit_20251224_170141.md`, whose
  summary table records exactly 1,550 / 701 / 219 files as "**Missing Footer**". Fix: correct
  the Known Issues bullet to match Parsing Rule 2 and the observed/audited state.

### 6. `.claude/rules/pinn-reference.md` — drift-found

Checks: framework-spec paths, `pinn/` reference files, and
`.planning/milestones/v1.4-phases/17-input-and-output-contracts/17-CONTEXT.md` all exist.
Track 2 baseline `192c7c3c` (2026-06-09).

- **F-04 (stale-claim).** "Mass slot encoding (raw vs fraction) is **GAP-17-01 — OPEN, awaiting
  user instruction**." Contradicted by `.planning/milestones/v1.4-GAPS.md` (line 22): GAP-17-01
  is `RESOLVED-WITH-INSTRUCTION: raw ordered masses m_i`, resolution batch authorized by the
  user on 2026-05-19. Fix: transcribe the resolved status.
- **F-05 (stale-claim).** Future-tense Phase 20 framing: "still subject to Phase 20 review
  (ARCH-01/02)", "Phase 20 ARCH-01 will lock final values", "Phase 20 ARCH-02 will lock the
  affine default", and "v1.4 contract under construction". Phase 20 completed and v1.4 was
  archived 2026-06-09 (`192c7c3c`). Locked outcomes per
  `.planning/milestones/v1.4-phases/20-architecture-and-normalization-cleanup/20-CONTEXT.md`:
  D-02 (`ARCH-01`) locks `first_omega_0 = 30`, `hidden_omega_0 = 1`, no omega0 scheduler;
  D-03 (`ARCH-02`) locks LayerNorm `elementwise_affine=False`. Fix: transcribe the locked
  outcomes and update tense. (Transcription-only fix; both decisions are recorded LOCKED
  user-side decisions, valid grounding under the v1.5 protocol.)

---

## Per-Doc Records — Class 2

### 7. `docs/README.md` — verified-current

Checks: directory-layout tree matches on-disk `docs/runbooks/` (EDL/, maintenance/, migration/)
after plan unit U1 (`0aadbff`, an intentional plan-directed fix, not audit drift);
`git-guidelines.md` link resolves; lifecycle/deletion-policy content matches current practice.
Track 2 baseline: last substantive commit before U1 (2026-06-08 reorganization).

### 8. `docs/git-guidelines.md` — verified-current

Checks: `scripts/agent-commit` exists and is executable; hooks present; commit-format rules match
the enforced hook behavior observed during this audit's own commits. Track 2: last commit
`b6a82cf4` — the same propagation commit that updated `AGENTS.md` and `ANTIGRAVITY.md`, so the
governance surfaces moved together; no divergence since.

### 9. `pinn_instruction/issues/README.md` — drift-found

Checks: all three thematic issue docs, `MIGRATION.md`, and `archive/` exist; framework-spec and
dataset-doc links resolve. Track 2 baseline `04fd8063` (2026-05-12).

- **F-06 (stale-claim, by omission).** The index describes the three issue docs with no status
  context. Since 2026-05-12: issue 01 was adjudicated during v1.4 (resolution doc
  `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md`
  plus applied spec revisions, Phases 17–22); milestone v1.5 (Phases 23–29) is actively
  adjudicating issue 02 (commit `458311da`); per repo governance the issue docs are
  non-authoritative audit inputs. A reader cannot tell any of this from the README. Fix: add a
  short dated Status note (facts above only — no rewriting of the index content).

### 10. `pinn_instruction/markdown_conversion/README.md` — drift-found

Checks: both indexed directories and all six table-linked artifacts exist on disk (incl. the
nested `review-of-framework/` and `stage-strat-revision/` files). Track 2 baseline 2026-05-20.

- **F-07 (stale-claim).** The index states it "tracks authoritative markdown conversions for the
  **v1.3 verification milestone**" and marks `ctl_instruction.md` / `pinn_architecture.md`
  "Verified in v1.3". Since 2026-05-20, 28 commits have revised `framework-specs/` (v1.4
  Phases 17–22 adjudication and cleanup); `sampling_method.md` is frozen-by-default (user
  directive 2026-06-10); `data_quality_assessment.md` is read-only under v1.5 SCOPE-09; and
  `framework-revisions/` now also contains `research_reports/` adjudication artifacts that the
  index does not mention. The v1.3-only framing materially understates the current authority
  state. Fix: add a dated status note recording the v1.4 revisions and current
  frozen/read-only designations; leave the conversion-provenance table itself intact.

### 11. `tools/spec-render-check/README.md` — verified-current

Checks: command examples well-formed against the committed tool layout; provenance claims
(Phase 22, T-22-01) consistent with git history; no changes to the tool's documented behavior
since last commit 2026-06-09.

---

## Per-Doc Records — Class 3 (report-only; no edits applied)

### 12. `simulation_data/Documentation/README.md` — drift-found

24 sampled claims across 9 categories (file counts, ID gaps, naming, IC schemas, parameter
tuples, footer schemas, script/provenance paths, gold-subset properties, directory structure).
**Verified (21):** all six per-folder file counts (4,857 / 2,749 / 4,857 / 4,857 / 2,749 /
2,565) ✓; ID-gap counts (143, 1,250, 1,434) ✓; IC schema (3 lines × 7 fields; standard masses
exactly 1.0; hierarchical masses varying) ✓; the complete footer-tuple distributions for both
gold folders, re-derived exactly — hierarchical gold `(1e-13,130,0.01)→4,146`,
`(1e-13,124,0.01)→649`, `(1e-14,118,0.01)→34`, `(1e-14,112,0.01)→27`, `(1e-14,124,0.01)→1`;
standard gold `(1e-13,130,0.01)→1,754`, `(1e-14,130,0.01)→592` ✓; full-schema tuples for the
base folders `(1e-15,130,0.08,10,0.263027)→3,307` and `(1e-13,118,0.17)→1,126` +
`(1e-13,130,0.17)→922` ✓; all referenced script/provenance paths ✓; gold IC folder removal and
the 184-ID exclusion (2,749 − 2,565 = 184, matching the exclusion list) ✓.
**Not sampled:** pipeline algorithm internals, conservation-metric implementations, physical
convention derivations (would require re-execution, not observation).

- **F-08 (contradiction — GATED).** Lines 203–228 specify a `_gold_` filename infix for
  gold-standard files (`ic_*_gold_XXXX.txt`, `brutus_hierarchical_gold_XXXX.txt`,
  `brutus_standard_gold_XXXX.txt`) and line 222 states "Gold-standard status is encoded in
  **both** the folder name and the filename." Observed: **0** of 4,857 files in
  `brutus_hierarchical_gold_standard/` and **0** of 2,565 in
  `brutus_standard_quasi_random_gold_standard/` carry `_gold_`; all use the base prefixes
  (`brutus_hierarchical_XXXX.txt`, `brutus_standard_XXXX.txt`). Method:
  `ls <folder> | grep -c '_gold_'` → 0 for both. Cross-corroboration:
  `.claude/rules/dataset-reference.md` already records the correct rule ("File names do **not**
  encode 'gold'; the folder defines the variant"). Observation settles the correct content;
  a specific edit is proposed in U6.
- **F-09 (contradiction — GATED).** Line 591 claims "**All Brutus output files contain a
  `Result:` footer**"; lines 595–601 describe 1,550 `brutus_hierarchical` files as "Partial
  footers (no `eta`; **tol/Lw/dt still parseable**)"; lines 611–618 describe 701
  `brutus_standard_quasi_random` files the same way; lines 620–627 describe 219
  `brutus_standard_quasi_random_gold_standard` files as "Minimal footers (no `eta` or `tol`;
  **only `dt`, `Lw`, `t_cpu`, and energy fields**)". Observed: those exact populations —
  1,550, 701, and 219 files — contain **no footer of any kind** (tail scan of all 15,028 files;
  full-file scans of samples find no `Result`/`tol`/`Lw`/`eta`/energy markers; files end with
  the final snapshot block). The doc's population *counts* are exactly right; the
  *characterization* is wrong. Corroboration: the doc's own cited audit
  (`footer_audit_20251224_170141.md`) records these same counts in its "**Missing Footer**"
  column, so the on-disk state was the same in 2025-12. Observation settles the correct
  content; a specific edit is proposed in U6.
- **F-10 (not-verifiable — GATED question).** Line 601's parenthetical "(same parameters,
  different Brutus build omitted `eta`)" asserts provenance that cannot be observed from the
  artifacts — and since the F-09 populations carry no footer, "same parameters" cannot be
  confirmed from file content at all. Recorded as not-verifiable; surfaced as a question in U6.
  No replacement content is proposed.

### 13. `simulation_data/Data/testing_data/README_TESTING.md` — drift-found

Checks verified: 8-directory structure ✓; IC format (3 lines × 7 fields) ✓; Brutus snapshot
structure ✓; parameter table (hier `1e-15/130/0.15`, std `1e-14/122/0.18`) matches actual
`Result:` footers in the testing outputs ✓; final timestamps ≥ 9.5 ✓; `test_pipeline.py`,
prescreening script, and `brutus` executable exist ✓.

- **F-11 (stale-claim — GATED).** 23 command examples hardcode `<home>/…` absolute
  paths (lines 12–253). The current checkout is `<home>/Desktop/3_body_problem`;
  the old spelling still resolves on this machine only because APFS is case-insensitive
  (verified: `ls -d <home>/Desktop/3_body_problem` succeeds), and would break on any
  case-sensitive filesystem. A proposed edit (repo-relative or `$REPO_ROOT`-based paths) is
  offered in U6.
- **F-12 (cosmetic — GATED, note only).** The output-format example (lines 198–209) includes
  `# Header:` / `# Body lines:` annotation comments that do not occur in real output files
  (verified by inspection). Same annotation idiom is used in `.claude/rules/dataset-reference.md`;
  recorded for completeness, no edit proposed.

---

## Rejected candidate findings (adjudication record)

1. Subagent claim that root `README.md`'s Ancillary Systems "lists `.claude/rules/` and
   `.planning/` only" — refuted by direct read (the section lists `pinn_instruction/`,
   `paper_templates/`, `reference-code/`); replaced by the narrower, evidence-backed F-01.
2. Subagent claim that `docs/git-guidelines.md` drifted because a "governance doc" was updated
   one day later — refuted: commit `b6a82cf4` itself modified `docs/git-guidelines.md` together
   with `AGENTS.md`/`ANTIGRAVITY.md` (verified via `git show --stat`).
3. Subagent characterization of the F-09 populations as "0 partial footers (doc claims wrong
   counts)" — corrected by full re-derivation: the doc's counts are exact; the files have **no**
   footer rather than a partial one. The finding was retained in corrected form.
4. Subagent verdict "verified-current" for `.claude/rules/dataset-reference.md` — overturned:
   content-level check (F-03) found a contradicted footer claim the path-existence sweep missed.

## R10 Coordination Flag — Phase 23 (CRITICAL)

Phase 23's research package was finalized and the external gate opened on 2026-06-10
(commits `c91772b8`, `548e0e1c`) **before** this audit completed. The package file
`pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/consolidated-context.md`
**transcribes both contradicted Class 3 claim sets verbatim** from
`simulation_data/Documentation/README.md`:

- Gold `_gold_` filename-infix specification (package lines 31–56) — contradicted by F-08.
- "Partial footer" distributions, tagged CLM-05 / CLM-06 (package lines 71–92, including
  "tol/Lw/dt still parseable → 1,550") — contradicted by F-09.

Impact: external research consuming the package would receive an incorrect file-naming contract
and an incorrect footer-parseability claim. The parameter tuples themselves (CLM-09 et al.) are
unaffected — they were independently verified correct here and previously corrected in
`b59d1758`. **This flag is surfaced to the user in U6 for a decision on amending the delivered
package**; no package file is touched by this audit (R2: `.planning`-adjacent and
adjudication-lifecycle artifacts are out of audit edit scope; the package belongs to Phase 23).

## Remediation Queue

- **U5 (direct fix, Class 1–2):** F-01, F-02, F-03, F-04, F-05, F-06, F-07 — each fix commits
  atomically referencing its finding ID.
- **U6 (gated, Class 3):** F-08, F-09 (evidence-settled proposed edits), F-10 (question), F-11
  (proposed edit), F-12 (note only) — no edit without per-finding user sign-off. Plus the R10
  package flag above.

---

## Resolution Status (post-U6 closeout, 2026-06-10)

| Finding | Status | Resolution |
|---|---|---|
| F-01 | addressed | `2333f30` — tools/ added to root README repository map |
| F-02 | addressed | `8dccb23` — docs/ and tools/ added to repo-map Key Directories |
| F-03 | addressed | `b5a34a1` — footer claim corrected in dataset-reference rule |
| F-04 | addressed | `90dbf39` — GAP-17-01 transcribed as RESOLVED-WITH-INSTRUCTION |
| F-05 | addressed | `90dbf39` — Phase 20 ARCH-01/02 locked outcomes transcribed |
| F-06 | addressed | `181b1b2` — adjudication status note added to issues README |
| F-07 | addressed | `e26f502` — post-v1.3 status note added to markdown conversion index |
| F-08 | addressed | user-approved full fix 2026-06-10; `d18f676` + supplemental instance `31b2cff` |
| F-09 | addressed | user-approved 2026-06-10; `ae609f3` (incl. the Known Anomalies §1 instance) |
| F-10 | addressed | user instructed: unverifiable provenance claim dropped (within `ae609f3`) |
| F-11 | addressed | user-approved 2026-06-10; `f0fe027` — repo-relative paths |
| F-12 | addressed | cosmetic note recorded by design; user did not request an edit |
| R10 flag | addressed | user instruction 2026-06-10: erratum option — `2fa2202` adds `ERRATUM-2026-06-10.md` beside the Phase 23 package (zero byte changes to delivered files); authoritative correction defers to the Phase 24 DATA-07 CLM-keyed addendum |

Post-fix scans during U5/U6 found two additional instances of already-approved findings — the
F-08 `_gold_` mapping block in the pipeline-overview section and the F-09 Known Anomalies §1
entry — both fixed under the same sign-offs and noted in the respective commit bodies.

**New observation (OPEN, minor, no action taken):** surfaced after this report was committed
and is not part of any approved finding. The dataset README's Known Anomalies §2 illustrates
`Result: filename=` paths as `<home>/Desktop/3_body_problem/...`, while sampled
footers record `<home>/Desktop/cursor/3_Body_Problem/...` (an older machine-era
path). The section's operative guidance — treat `Result: filename=` as informational only,
never as an authoritative mapping — is unaffected. Left for a future pass or user direction.
