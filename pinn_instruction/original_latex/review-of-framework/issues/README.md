# Issues Directory — Consolidated PINN Audit Documentation

Consolidated 2026-04-27 from 7 scattered audit/issue files (~246 KB) into 3 thematic documents grouped by system layer, with full per-section provenance tracking.

## Thematic Documents

- **[01-architecture-and-physics-foundations.md](01-architecture-and-physics-foundations.md)** — Network architecture (SIREN init, omega0 scheduling, LayerNorm), input vector design (14-D specification, normalization formulas), characteristic length D=6.694, softening dual-context strategy, COM frame convention, AD chain-rule factor correction.
- **[02-data-pipeline-and-validation.md](02-data-pipeline-and-validation.md)** — IC parsing and non-contiguous ID handling, blacklist enforcement, snapshot-completeness gates (TrajectoryValidator), validation metrics (SCS / SASD / IPR / PSC) as live training parameters, Brutus footer/mass drift protocol, file format decision (h5 vs txt/json), global scale computation.
- **[03-curriculum-and-training-loop.md](03-curriculum-and-training-loop.md)** — Data-driven stage assignment (PCA + K-means + quantiles), replay-and-lookahead batch construction, collocation vs data-fidelity point separation, ALM scheduling (mu, lambda, energy weight), gradient clipping, causal training mismatch resolution (Option A vs B vs Time-Windowed Hybrid), tau_L and L_max computation, stage transition criteria.

## Provenance

See **[MIGRATION.md](MIGRATION.md)** for a per-file, per-section provenance map tracing every major heading from the 7 original files to their destination(s) in the 3 thematic docs. Original files are preserved with git history in **[archive/](archive/)**.

## Canonical References

- [CTL Instruction (Curriculum Training Framework)](../../../markdown_conversion/pandoc_conversion/CTL-instruction-final.md)
- [PINN Architecture Plan (SQR-SkipResNet-SIREN)](../../../markdown_conversion/pandoc_conversion/PINN_architecture_plan.md)
- [Dataset Documentation (Simulation Data Pipeline)](../../../../simulation_data/Documentation/README.md)

## Cross-Doc Interaction Matrix

| Topic | Canonical Home | Also Referenced By |
|-------|---------------|--------------------|
| 14-D input vector specification | `01` §Input Vector Normalization Formulas | `02` (pipeline produces it), `03` (training consumes it) |
| COM frame transformation | `01` §Frame Convention | `02` (validation applies same transform) |
| Dual-epsilon strategy (eps=1e-10 / eps_soft=1e-5) | `01` §Dual-Context Epsilon Strategy | `02` (validation uses static eps), `03` (training uses dynamic eps) |
| D = 6.694 (characteristic length) | `01` §Quantitative Impact | `02` (recompute stage assignments), `03` (stage thresholds) |
| Replay/lookahead batch construction | `03` §Verbatim Reference Specification | `02` (DataLoader must support stage queries) |
| Stage assignment criteria | `03` §Data-Driven Adaptive Stage Assignment | `02` (pipeline outputs stage labels) |
| TrajectoryValidator gate | `02` §Confirmed Findings (B-06) | `03` (training loop assumes validated data) |
| SCS / SASD / IPR / PSC validation metrics | `02` §Validation Metrics as Live Training Parameters | `03` (feed into training loop as live parameters) |
