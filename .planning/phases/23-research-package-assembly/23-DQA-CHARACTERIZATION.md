# Phase 23: data_quality_assessment.md Characterization

**File:** `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md`
**Lines:** 328 (plus trailing newline)
**Location:** `framework-revisions/` (research report, NOT an authoritative spec; SCOPE-09)
**Characterized:** 2026-06-10
**Characterized by:** Phase 23 Plan 01 Task 1 (T-23-01-01)
**Governance:** Read-only — zero edits to the source file (SCOPE-09, CLAUDE.md Source of Truth)

---

## Provenance

Git history (`git log --follow --oneline`), recorded re-derivably:

| Commit | Phase / Event | Description |
|--------|---------------|-------------|
| `bf127b0` | pre-v1.3 | Original consolidation into `markdown_conversion/` |
| `314d956` | Phase 11 Plan 02 | Copy pandoc candidate, strip citations, audit sections 1–3 |
| `460cf4b` | Phase 11 Plan 02 | Rebuild table as GFM, convert desclist syntax, audit sections 4–6 |
| `f381e94` | Phase 11 | Fix missing title page, section numbers, equation numbers, table caption |
| `b5edcc2` | Phase 11 Plan 03 | Append Source Issues metadata (SI-DQA-001/002/003) |
| `740513d` | Phase 15.1 Task 7 | Bold title in data_quality_assessment.md |
| `16b8e4f` | Phase 15.1 Task 8 | Bold all 4 header cells in assessment table |
| `431567c` | Phase 15.1 Task 9 | Replace prose em-dashes with Unicode em-dash |
| `6ab19ea` | post-Phase 15.1 | Move revision markdowns into `framework-revisions/` |
| `f8595f7` | post-v1.3 | Archive v1.3 milestone files |
| `3732f1f` | post-v1.3 SCS correction | Correct SCS/raw-drift gate inconsistency (SI-DQA-003) |
| `d3fcff9` | post-v1.3 | Retire stale v1.3 closure audit reports |

**Design edits:** None during v1.4 or v1.5. The file carries v1.3-era content plus the post-v1.3 SCS-gate correction (`3732f1f`). Formatting-only changes in Phase 15.1 (`740513d`, `16b8e4f`, `431567c`) did not alter substantive content.

---

## Section Map

| Section | Lines | Content |
|---------|-------|---------|
| Title + front matter | 1–8 | Title, "Research Report" label, date |
| §1 Introduction | 9–30 | Brutus/Bulirsch-Stoer landscape; CTL-PINN architecture and causal-training rationale |
| §2 Assessment Strategy / Staged Gate | 31–105 | Static vs Dynamic validation trade-offs; the "Staged Gate" Protocol (Phase 1 Physics Gate, Phase 2 Stiffness Gate, Phase 3 Learnability Gate); comparative analysis table |
| §3 Mathematically Grounded Metrics | 106–191 | **The canonical metric definitions:** |
| — §3.1 SCS (Symplectic Conservation Score) | 110–137 | Raw drift `epsilon_H` (eq 3); `SCS = log10(epsilon_H)` (eq 4); **locked gate `epsilon_H > 1e-5` / `SCS > -5`** at lines 120 and 130; boundary behavior at line 134; marginal band at line 128 |
| — §3.2 SASD (Stiffness-Aware Sampling Density) | 138–159 | Curvature-based stiffness proxy (eq 5); interpretation thresholds; causal-link breakage risk |
| — §3.3 IPR (Interpolation Physics Residual) | 160–175 | PCHIP spline + synthetic collocation-point residual (eq 6); data-density sufficiency test |
| — §3.4 PSC (Phase Space Coverage Entropy) | 176–191 | Shannon entropy on discretized phase space (eq 7); stiffness-coverage ratio |
| §4 Risks to Model Parameters | 192–219 | Causal "firewall" effect; dead neuron problem; spectral bias |
| §5 Implementation Protocol | 220–291 | Phase 1 static audit (224); **SCS reject gate at line 234**; Phase 2 overfit challenge; Phase 3 dataset composition |
| §6 Synthesis | 292–307 | Conclusions; future-work recommendations |
| Source Issues | 308–328 | SI-DQA-001 (orphaned bibliography); **SI-DQA-002** (superseded — initial audit missed SCS gate inconsistency); **SI-DQA-003** (SCS gate correction: raw-drift vs log distinction, threshold tightened -4 to -5) |

---

## Relation to the Not-yet-Performed Dataset-Framework Compatibility Verification

### What ground DQA covers

1. **Four validation-metric definitions** (SCS, SASD, IPR, PSC) with mathematical derivations and interpretation thresholds.
2. **Staged-gate protocol** (static Physics Gate, Stiffness Gate, dynamic Learnability Gate) with explicit reject/flag criteria.
3. **The locked post-v1.3 SCS gate** (`epsilon_H > 1e-5` / `SCS > -5`) at lines 120/130/234 — the only written home of this gate in the repository.

### What remains UNVERIFIED

1. **Metric definitions vs the actual snapshot distributions.** No phase has yet computed SCS/SASD/IPR/PSC against the on-disk `simulation_data/` dataset to confirm the definitions align with real Brutus output characteristics.
2. **Threshold vs the dataset's real drift profile.** The `SCS > -5` gate threshold was set analytically and ratified post-v1.3, but whether the actual dataset's drift distribution is consistent with this threshold is Phase 24 (DATA-01) and Phase 28 (VAL-01) territory.
3. **Dataset-framework compatibility in general.** Per CLAUDE.md: "no dedicated phase or milestone has yet verified dataset <-> framework compatibility; `data_quality_assessment.md` (in `framework-revisions/`, a research report — not an authoritative spec) may cover parts of that ground and is to be characterized, not edited, during v1.5."

### Non-authoritative status

The file is a research report under `framework-revisions/`, not an authoritative framework spec (SCOPE-09). It is the sole written home of the post-v1.3 SCS gate, yet v1.5 spec edits land in the editable specs (`ctl_instruction.md`, `pinn_architecture.md`), never here. This creates a tension: the locked gate lives in a file that v1.5 cannot edit, and its migration into an editable spec (if needed) is a Phase 28 concern (VAL-01).

---

## Package-Inclusion Recommendation

**Recommendation: INCLUDE** the DQA snapshot in the research package.

**Annotation:** "research report, not authoritative spec (SCOPE-09); sole written home of the post-v1.3 SCS gate; metric definitions unverified against dataset"

**Rationale:**

1. Section 3 is the most complete existing statement of the four contested validation metrics (SCS/SASD/IPR/PSC) that the external research must adjudicate.
2. The SCS gate that the known seed conflict turns on (ratio-based `> 1e-6` / `< 1e-8` vs locked `epsilon_H > 1e-5` / `SCS > -5`) is documented only here and in the issue doc — excluding DQA would require the external research to adjudicate SCS without seeing the metric's canonical definition.
3. The file is 328 lines and self-contained; inclusion does not bloat the package.

**Final call:** The final inclusion decision rides the D-07 user checkpoint. This recommendation is advisory only (A3).

---

*This characterization was produced with zero edits to `data_quality_assessment.md` (verified: `git diff --quiet`).*
