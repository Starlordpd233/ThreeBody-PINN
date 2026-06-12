# Open Research Questions

Registry of open research questions routed through the external-research handoff workflow
(package → external AI research → consolidation → resolution doc → user picks). See
`.planning/notes/training-execution-parallel-work-boundary.md` for the workflow decision.

Questions PH-1 through PH-10 originate from the training-execution reference design
(`docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md`,
Section 7 — a quick-brainstorm baseline per its 2026-06-11 standing note). PH-2/PH-3/PH-4
are excluded — they are owned by the framework specs (specwork), not open trainex research.

## Trainex research rounds

R1 is split into two parallel sub-packages with different output contracts (user decision
2026-06-11; a single ~10-item package would cost per-topic depth). Both live under
`pinn_instruction/markdown_conversion/framework-specs/trainex-r1/`; the shared
DELIVERY-NOTE.md at that root covers handoff, result routing, and consolidation join
points.

| Round | Contents | Status |
|---|---|---|
| **trainex-r1a** (decisions & structure) | D1 ML framework (PH-1, incl. precision conditional pending v1.5 Phase 27) · D2 experiment tracking/monitoring (PH-10) · D3 compute utilization + in-memory-vs-streaming ingestion (PH-8) · D4 checkpoint/resume policy + unattended-run auto-guards + on-failure diagnostic bundle (PH-9 policy layer) · D5 training-loop skeleton capabilities (structural slices of PH-7/PH-6 pulled forward + loss-weighting machinery) · D6 reproducibility & determinism policy · D7 curriculum stage-boundary mechanics · baseline critique mandate | PACKAGE-READY (2026-06-11) — `trainex-r1/research_package_a/`; awaiting user handoff. Output: options menus + door classifications + decision sheet (user picks) + first-run recipe |
| **trainex-r1b** (runbook & ops knowledge) | K4 training feasibility envelope + K5 trainer-correctness verification ladder (the two priorities; K5 incl. smoke-test pattern + known-solution fixtures) · K1 PINN health watchlist · K2 unattended-Mac training ops · K3 runbook design patterns | PACKAGE-READY (2026-06-11) — `trainex-r1/research_package_b/`; awaiting user handoff. Output: cited runbook-ready findings + parameterized estimates + decision-relevant observations |
| **trainex-r2** (pure tuning) | Numeric values for PH-7 optimizer/LR and PH-6 collocation, inside the skeleton fixed by r1a's D5 pick | NOT PACKAGED — gated on the user's r1a decision-sheet picks |
| **later / data-gated** | PH-5 train/val/test split fractions and stratification policy | DEFERRED — needs actual `simulation_data/` statistics AND the v1.5 data contracts (Phases 26–27); cannot be answered by an external agent without data |

**Excluded from trainex entirely (decision 2026-06-11):** float64-necessity evidence
gathering. It is a specwork adjudication input for v1.5 Phase 27; trainex resolutions are
explicitly non-grounding for spec adjudication, so the channels must not mix. If gathered
externally, route it as a separate EDL-style support brief through the specwork channel.

## Framework integrity rounds

| Round | Contents | Status |
|---|---|---|
| **integrity-r1** (framework integrity audit) | Disruption-first audit of the three framework specs as a whole (`ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`) — RD-1 fundamental viability red-team · RD-2 cross-spec coherence · RD-3 buildability gaps · RD-4 math/physics correctness · RD-5 ambiguity · RD-6 scientific soundness · RD-7 data–framework compatibility · RD-8 load-bearing assumptions/risk register. Hardened output contract: per-H1/H2 coverage matrix, S1–S4 severity rubric, evidence classes, novelty classification (`against-in-flight-edit` absorbs the v1.5 Phase 26–28 overlap; timing user-confirmed 2026-06-12), constants concordance, minimum-decision-list in gap-register A/B/C format | PACKAGE-READY (2026-06-12) — `pinn_instruction/markdown_conversion/framework-specs/integrity-r1/`; awaiting user handoff (multi-AI fan-out, single package). Output standing: **findings register — NOT a candidate verdict source, NOT a grounding source**; feeds user triage into future milestones. Results → `integrity-r1/research_results/<agent>-resolution.md`; Stage-2 consolidation prompt authored when results land |
