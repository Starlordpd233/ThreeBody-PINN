# Evidence Packet: PSC - Phase Space Coverage Entropy

## Header

| Field | Value |
|---|---|
| ID | `PSC` |
| Title | Phase Space Coverage Entropy population and weighting contract |
| Severity | `MAJOR` |
| Current Status | `DEFERRED` |
| Current Verdict | `defer-with-blocker` |
| Phase | Phase 28 |
| Acceptance Check ID | `AC-VAL-04` |
| Spec Sections Touched | None yet - PSC clause parked pending GAP-28-03 |
| Code Paths Touched | Not code-applicable |

## Source Positions

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | `§5.4 Q-C4:L675-L728` | Proposes PSC as a dataset-level, report-only diversity diagnostic over sorted scaled pair-distance grid coordinates, with full-`ln K` normalized entropy, SCR at `d_min < 0.5`, and a deduplicated equal-record-weighted pooled population. It explicitly flags the population/weighting construction as consolidator-original synthesis present in neither input, and asks the project to sanity-check the composed weighting on first run. |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `L167-L169` | Defines PSC as Shannon entropy of data points across a discretized phase-space grid and assigns curriculum replay usage to downstream training. It does not specify grid construction, population, weighting, deduplication, or report-only/no-gate semantics. |

Do not treat either primary source as authoritative before user resolution. The resolution doc gives a detailed candidate construction, but it also marks the composition as original synthesis requiring verification/sign-off.

## Spec Evidence

- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md:L176-L190` is the read-only written home of the PSC concept: Shannon entropy over binned phase-space occupancy, low/high entropy interpretation, and a close-encounter/stiffness bin check. It does not specify the population, weighting, deduplication, or fixed-grid constants.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:L237-L242` defines Stage 6 with the scaled `s_min < 0.5` criterion, which is the candidate SCR anchor.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:L891-L905` states that Stage 3 invariants consume scaled initial conditions and retain `s_min` as metadata for stage assignment.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:L452-L458` establishes the data-side admission-gate pattern before stage assignment, `compute_globals`, or training. This supports a post-Step-1A admitted-set PSC placement once the population/weighting convention is resolved.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` currently has no PSC clause in a `Data-side quality-metric contracts` subsection. No PSC framework-spec edit has been made in this packet.

### Dataset Evidence (§3b)

- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md:20` (`CLM-05b`) records the standard base/gold count structure: 2,749 base vs 2,565 gold outputs, so base-minus-gold is 184.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md:24` (`CLM-09`) records folder-default `dt_out` context: standard base `dt_out=0.17`, hierarchical base `dt_out=0.08`, and gold variants `dt_out=0.01`.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md:25` (`CLM-10`) records snapshot-resolution context: standard base median 61, hierarchical base median 127, and gold medians 1003.

These rows ground the two-layer pooled-population confound. Naive all-snapshot pooling double-counts physical systems with both base and gold records, and gold-backed records carry about `1003 / 61 ~= 16.4` times as many standard snapshots as base-only records. The rows do not, by themselves, authorize the composed population/weighting convention as canonical.

## FUT-01 Hand-off Note (formerly "Code Evidence")

Live `pinn/` code is not a v1.5 evidence source and was not consulted for this verdict. FUT-01 will need to implement whichever PSC population/weighting convention the user resolves, plus the report-only PSC/SCR metadata and any doc-03 replay-governance integration after framework-spec authorization.

## Verdict

`defer-with-blocker`

The packet cannot lock the PSC population/weighting construction without user instruction. The following elements are grounded enough to carry forward as constraints for a later PSC clause, but are not landed as canonical spec text here:

- PSC is data-side and report-only; it has no per-trajectory reject authority.
- Sorted pair distances make the grid permutation-invariant.
- Log-space distance bins are appropriate because close encounters span orders of magnitude and would collapse into edge bins under a naive linear grid.
- Scaled distances are required if SCR uses the Stage-6 `s_min < 0.5` anchor.
- `H_norm = H / ln K` avoids the self-referential occupied-bin-denominator failure mode in which a uniformly filled small subset of bins can appear fully covered.
- Miller-Madow correction should be reported, not silently added.
- The naive all-snapshot pooled value is confounded by both resolution mix and base/gold duplication.
- The candidate grid constants (`[1e-3, 1e2]`, 25 bins per axis, `K = 625`) are provisional.

The decisive population/weighting convention remains blocked. The dataset evidence proves the two confounds exist: base/gold duplication and snapshot-resolution skew. First-principles accounting also shows the proposed fixes are orthogonal: dedup-prefer-gold removes duplicate physical-system representation, while equal-record weighting gives each surviving record equal total snapshot mass. However, the composed rule exists in neither primary input, and the resolution doc explicitly flags it as consolidator-original content requiring a first-run sanity check. Because PSC/SCR outputs can drive dataset-curation and doc-03 replay decisions, Phase 28 cannot canonize the synthesis without user sign-off or the specified empirical verification. No PSC spec clause is landed until GAP-28-03 is resolved or explicitly deferred by the user.

## Before / After Spec Note

Before this packet: no canonical PSC contract existed in editable framework specs. DQA §3.4 and issue-02 carried the PSC concept; the resolution doc carried a detailed candidate construction and explicitly flagged the population/weighting synthesis as original.

After this packet: no framework-spec PSC edit has been made. The intended `ctl_instruction.md` PSC clause and optional `pinn_architecture.md` visibility note remain parked pending GAP-28-03.

## Named Acceptance Check

`AC-VAL-04`

Phase 28 Plan 04 owns AC-VAL-04, but its runnable structural check is parked with the spec edit. Once GAP-28-03 is resolved, AC-VAL-04 must verify the PSC clause, report-only/no-gate semantics, Shannon entropy formula, sorted scaled log-distance grid, `H_norm = H / ln K`, SCR at `d_min < 0.5`, resolved population/weighting convention, naive-pooled-not-a-deliverable statement, packet citation, and doc-03 replay-governance forward reference.

## Status Transition Log

```text
2026-06-16 <pending-28-04-sha> PENDING -> IN_PROGRESS (Phase 28 Plan 04; PSC EVID-06 packet opened and Q-C4 composition fork evaluated)
2026-06-16 <pending-28-04-sha> IN_PROGRESS -> DEFERRED (Phase 28 Plan 04; GAP-28-03 opened for PSC population/weighting composition sign-off, no spec edit landed)
```
