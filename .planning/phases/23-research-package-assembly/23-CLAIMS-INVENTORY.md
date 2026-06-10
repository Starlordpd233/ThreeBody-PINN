# Phase 23: CLM Claims Register (PKG-03)

**Purpose:** This register is the canonical PKG-03 claims list. It enumerates every dataset figure stated in the Phase 23 research package with a stable CLM ID, classified as `claimed-unverified` or `verified`. It is also the Phase 24 verification checklist (D-12): Phase 24 re-verifies every row regardless of status, and the DATA-07 correction addendum keys off these CLM IDs.

**Status classification rule (D-13):** Only `simulation_data/Documentation/` files and committed prior-phase probe evidence count as grounding for `verified`. `.planning/codebase/*.md` maps do NOT. When in doubt, mark `claimed-unverified` — over-marking is harmless (Phase 24 verifies everything anyway).

**Scope:** Dataset figures only. The `D = 6.694` global-scale figure (CLM-13) is a convention conflict, not a dataset count; it is included because the issue doc presents it as a dataset-derived figure and it must be posed to the external research.

**Created:** 2026-06-10
**Append-only policy:** Existing CLM IDs are never renumbered. Additional package-stated figures receive the next CLM ID, or are quoted as non-claim context.

---

## Claims Table

| CLM ID | Figure | Value (claimed) | Source citation | Status | Phase-24 check |
|--------|--------|------------------|-----------------|--------|----------------|
| CLM-01 | Standard ID gaps | 1,250 gaps out of 4,000 nominal (31.2%) | Issue doc lines 58, 312 | `claimed-unverified` | DATA-01: count standard Brutus output files; compute `nominal - actual` |
| CLM-02 | Hierarchical ID gaps | 143 gaps out of 5,000 nominal (2.9%) | Issue doc lines 58, 311 | `claimed-unverified` | DATA-01: count hierarchical Brutus output files; compute `nominal - actual` |
| CLM-03 | Blacklist size | 65 IDs (2 hierarchical + 63 standard) | Issue doc lines 59, 297; `simulation_data/Documentation/problematic_ics_blacklist.json` (provenance) | `claimed-unverified` | DATA-02: verify blacklist count/composition against json; verify loading/consumption status (M11 finding) |
| CLM-04 | Standard IDs without gold counterpart | 184 | `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` | `verified` | DATA-03: re-verify 184-ID list against gold Brutus outputs |
| CLM-05 | Standard folder counts | 2,749 base vs 2,565 gold | `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`; `simulation_data/Documentation/README.md` | `verified` | DATA-04: count base and gold folders independently |
| CLM-06 | Hierarchical Brutus output | ~4,857 files | `simulation_data/Documentation/README.md` Brutus Parameters by Variant (line ~607) | `verified` | DATA-04: count hierarchical Brutus output files |
| CLM-07 | Minimal standard-gold footers | 219 files with minimal footers | `simulation_data/Documentation/README.md` Brutus Parameters by Variant (line ~627) | `verified` | DATA-05: parse footer schema across standard-gold files; count minimal-footers subset |
| CLM-08 | tol=1e-14 standard-gold files | 592 files | `simulation_data/Documentation/README.md` Brutus Parameters by Variant | `verified` | DATA-05: parse tolerance field across standard-gold files; count tol=1e-14 subset |
| CLM-09 | Folder-default tol / dt_out values | std: tol=1e-13, dt_out=0.17; hier base: tol=1e-15, dt_out=0.08; gold: tol=1e-13, dt_out=0.01 | `simulation_data/Documentation/README.md` Brutus Parameters by Variant (lines ~584-628) | `verified` | DATA-05: parse footer parameters; verify default values per variant |
| CLM-10 | Snapshot counts per trajectory | ~59 (standard) / ~125 (hierarchical) / ~1000 (gold) | Issue doc lines 13, 60, 311-312 | `claimed-unverified` | DATA-06: count output rows per trajectory file; README warns against hard-coding snapshot counts (lines ~629-637) |
| CLM-11 | `final_timestep >= 9.5` prevalence | Rule stated; prevalence figure not given | Issue doc lines 57, 202, 326; README Completeness Checks | `claimed-unverified` (prevalence) | DATA-06: compute `final_timestep` distribution; verify gate rule and quantify prevalence |
| CLM-12 | Nominal IC counts | ~4,000 standard / ~5,000 hierarchical | Issue doc lines 311-312 | `claimed-unverified` | DATA-01: verify actual vs nominal IC count |
| CLM-13 | `D = 6.694` global scale | `cbrt(G * M_tot * t_max^2) = 6.694` | Issue doc lines 231, 258, 289; conflicts with locked PHYS-01 `D = (GT^2)^(1/3) ~ 4.6416` (`ctl_instruction.md` section 2.5, line 598 explicitly rejects the 6.694 form) | `claimed-unverified` | PIPE-09 / EVID-10: pose as convention conflict to adjudicate; locked counter-position is PHYS-01 raw-mass D ~ 4.6416 |

---

## Row Notes

**CLM-03 (blacklist 65):** The count `65 = 2 hierarchical + 63 standard` is directly observable in `problematic_ics_blacklist.json`, but DATA-02 (Phase 24) owns the verification verdict on both count/composition and loading/consumption status. The count is marked `claimed-unverified` to reflect that Phase 23 does not perform empirical probes — Phase 24 does. The M11 finding (blacklist not loaded at training time) is about consumption status, not count; that nuance is preserved for Phase 24.

**CLM-10 (snapshot counts):** The README explicitly warns against hard-coding snapshot counts (lines ~629-637); the `~` prefix signals approximation. These figures are `claimed-unverified` and will be empirically verified in Phase 24.

**CLM-11 (`final_timestep >= 9.5` prevalence):** The gate rule itself (`final_timestep >= 9.5`) is grounded in README Completeness Checks, but the *prevalence* (what fraction of trajectories satisfy it) is not stated in any `Documentation/` file. The rule is grounded; the prevalence figure is `claimed-unverified`.

**CLM-13 (`D = 6.694`):** This is NOT a dataset count. It is a contested convention claim: the issue doc derives `D = cbrt(G * M_tot * t_max^2) = 6.694` using total-mass scaling, while the locked v1.4 PHYS-01 convention uses raw-mass `D = (G * T^2)^(1/3) ~ 4.6416` and `ctl_instruction.md` section 2.5 line 598 explicitly rejects the 6.694 form. This is posed as a conflict to adjudicate in Phase 27 (PIPE-09) / Phase 25 (EVID-10), not as a figure to verify empirically.

---

*This register is the source of truth for the PKG-03 claims list. Plan 03 copies it into the research package as `claims-table.md`. Phase 24 consumes it as its verification checklist (D-12).*

---

## Post-delivery correction note (2026-06-10, doc-integrity audit findings F-08/F-09)

The repo-wide documentation-integrity audit (separate workstream) checked
`simulation_data/Documentation/README.md` against the on-disk dataset AFTER this register and
the package `claims-table.md` were delivered, and found two README claims false. The register
rows transcribed the README faithfully — the source itself was wrong. Original rows are left
as recorded (re-derivable against the snapshot pin); this note supersedes their claim text.

- **F-08 — gold filename token.** README claimed gold-standard simulation files carry a gold
  token in their filenames. On disk (re-verified 2026-06-10 by direct listing), gold output
  folders contain `brutus_hierarchical_XXXX.txt` / `brutus_standard_XXXX.txt` — gold status is
  indicated ONLY by parent folder. Affects the naming narrative copied into the package
  `consolidated-context.md` (folder/file-naming section, lines ~31-56). No CLM row carries
  this claim directly.
- **F-09 — absent `Result:` footers.** README claimed all Brutus output files end with a
  `Result:` footer and that ~2,470 files have a "partial" footer with still-parseable
  parameters. On disk, those 2,470 files (1,550 `brutus_hierarchical` + 701
  `brutus_standard_quasi_random` + 219 standard-gold) have NO footer at all; parameters for
  them come only from folder defaults. Footers that are present carry the full schema (see
  `.claude/rules/dataset-reference.md` dataset-anomalies note, corrected 2026-06-10).
  Affects: **CLM-07** (claim text "219 files with minimal footers" — the 219 are footer-less;
  count itself stands) and the partial/minimal-footer parameter attributions copied into the
  package `consolidated-context.md` (lines ~67-105, 138). **CLM-09 numeric values are NOT
  affected** (folder-default tol/dt_out re-verified correct); only its "parse footer
  parameters" verification plan narrows to full-schema files plus folder defaults elsewhere.

Correction routing: the delivered package stays byte-stable; the audit workstream issues a
dated erratum note beside the package, and the Phase 24 DATA-07 CLM-keyed correction addendum
is the authoritative follow-up that supersedes both this note and the erratum. The README
fixes (F-08/F-09) are user-approved and land in the audit workstream.
