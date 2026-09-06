---
phase: "55"
slug: "architecture-characterization-probe"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-09-06"
---

# Phase 55 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

**Register origin:** `register_authored_at_plan_time: true` — all four PLAN files
(55-01 … 55-04) carried a parseable `<threat_model>` block. This audit **verifies
the planned mitigations exist**; it did not scan for new threats.

**Depth:** ASVS L1 (grep-depth). `threats_open: 0` with a plan-time register at
ASVS L1 satisfies the secure-phase short-circuit — no `gsd-security-auditor`
L2/L3 pass was required. Each mitigation below was confirmed by direct file
inspection of `pinn/verification/architecture_characterization_probe.py` and
`tests/phase55/test_architecture_characterization.py`, cross-checked against the
passing `55-VERIFICATION.md` (12/12 must-haves, 46 phase-55 tests green).

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| caller / on-disk JSON → `SweepCase` | Case configuration (label, seed, masses, IC13 mode) from a Python caller or a `--cases-config` file | Untrusted field types and values |
| operator argv → `main` | `--precision`, `--device`, `--n-col`, `--cases-config`, `--evidence-root` from the command line | Untrusted strings → path and tensor construction |
| `measure_case` → `pinn/` primitives | Tensors cross into the trainer's physics / AD functions | Numeric tensors; non-finite intermediates must fail, not surface as a plausible measurement |
| probe module → `tests/phase38` prohibition glob | The new file enters an existing repo-wide mechanical scan whose guarantees protect every other module | Static-analysis surface |
| probe → filesystem | The evidence writer creates directories and files under an operator-supplied root | Path; committed `.planning/` artifact |
| probe → git subprocess | `git_head()` and the dirty-tree probe spawn subprocesses whose failure must not silently gap the provenance record | Subprocess exit / timeout |
| Phase 55 → Phase 56 governance | Building the capability vs. exercising it — crossing early produces an ungoverned precursor to a value `54-RULING.md` requires measured with provenance | Control-flow reachability |
| test suite → committed baseline | The suite reads a git-tracked fixture whose integrity is the entire value of the tier-2 regression net | Read-only file handle |
| committed evidence → downstream readers | Phase 56 and the milestone audit cite this run | Provenance claims |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-55-01 | Tampering | `SweepCase.__post_init__` | medium | mitigate | Fail-closed per-field validation (`_validated_label/_seed/_masses/_ic13_mode` + `__post_init__`) raising `ValueError` before any tensor is built | closed |
| T-55-02 | Tampering | `ArchitectureSpec` construction in `measure_case` | medium | mitigate | Always constructs a real `ArchitectureSpec(seed=…)`; its `__post_init__` fail-closed rejects any non-conformant topology | closed |
| T-55-03 | Tampering | AD / force path | high | mitigate | Direct calls to `componentwise_du` / `softened_acceleration` so their `_require_finite` guards raise on a non-finite intermediate; no shadowing local finite checks; SC3 mutation test proves the real functions are on the path | closed |
| T-55-04 | Spoofing | probe result provenance | medium | mitigate | Every result carries `precision`, `device`, `n_col`, `collocation_times`, `causal_clip_min_weight`, `median_convention`, `ic13_rng_scheme` | closed |
| T-55-05 | Tampering | `tests/phase38/test_prohibitions.py` coverage | medium | mitigate | `set_default_dtype` / `is_available` / v1.3-import guarantees re-homed into `tests/phase55/` **before** the Phase-38 glob exclusion lands | closed |
| T-55-06 | Tampering / Info Disclosure | `--evidence-root` | high | mitigate | `_reject_dataset_evidence_root` resolves the root and refuses any path beneath `simulation_data/` before `_new_run_dir` creates anything; `test_evidence_root_inside_simulation_data_is_rejected` | closed |
| T-55-07 | Tampering | `--cases-config` JSON | high | mitigate | Validate-before-construct per-field parsing raising `ValueError` before any tensor or path; `SweepCase` + `ArchitectureSpec` `__post_init__` as two further nets; `test_malformed_cases_config_raises_value_error` | closed |
| T-55-08 | Tampering | concurrent evidence writes | medium | mitigate | `_new_run_dir` `mkdir(exist_ok=False)` + suffix retry; both files via `atomic_write_text` (tmp-write, fsync, `os.replace`, parent fsync); `test_cli_allocates_non_overwriting_run_dirs` | closed |
| T-55-09 | Repudiation | evidence provenance | high | mitigate | `_provenance` records argv, resolved command, git sha + availability flag, worktree dirty flag, Torch/NumPy versions, UTC timestamp, runtime, conventions, clip facts; `test_cli_writes_provenance_evidence` | closed |
| T-55-10 | Denial of Service | git subprocess | low | mitigate | Both git probes bounded by `_GIT_TIMEOUT_S`; a missing binary, non-repo, non-zero exit or timeout all degrade to an explicit unknown rather than hanging | closed |
| T-55-11 | Elevation of Privilege | Phase-38 prohibition glob | medium | mitigate | Exclusion is a single argued per-file entry with a rationale comment; every other module's assertions are untouched; the two non-precision guarantees re-homed first | closed |
| T-55-12 | Tampering | Phase 55 / Phase 56 governance boundary | high | mitigate | AST call-graph closure proving both new-structure helpers are unreachable from `run_sweep`/`measure_case`/`main`, plus a call recorder proving every default-path `causal_physics_loss` call receives exactly `DEFAULT_N_COL` values; gated by the preceding `checkpoint:decision` | closed |
| T-55-13 | Tampering | `stratified_collocation_times` inputs | medium | mitigate | Validate-then-sample ordering: `TypeError` on a non-`Generator` rng, `ValueError` on non-positive `n_bins`/`per_bin`, closing cardinality assertion mirroring `CollocationSampler.uniform` | closed |
| T-55-14 | Tampering | `bin_mean_residuals` inputs | medium | mitigate | Fail-closed `ValueError` on a length mismatch, an out-of-range bin index, or an empty bin (`raise ValueError(f"empty bin {bin_id}")`) | closed |
| T-55-15 | Repudiation | test vacuity | medium | mitigate | The containment test asserts its own closure is non-empty and reaches a known-reachable helper before asserting absence of the two forbidden names; both containment tests carry a recorded negative-control observation | closed |
| T-55-16 | Tampering | `tests/phase55/fixtures/six_case_baseline.json` | high | mitigate | Suite opens the baseline read-only; session-scoped autouse fixture asserts its sha256 is unchanged at teardown; AST scan asserts no write-mode handle in the suite; comparison proven fail-first against a perturbed in-memory copy | closed |
| T-55-17 | Repudiation | committed evidence run | high | mitigate | `raw.json` carries argv, resolved command, git sha + availability, dirty flag, Torch/NumPy versions and the full six-row output — every downstream citation is re-derivable | closed |
| T-55-18 | Spoofing | audit cross-check | medium | mitigate | The comparison is recorded at decade resolution with the reason stated (the original ad-hoc collocation scheme is unrecoverable); a column outside the audit's decade halts and surfaces rather than widening the claim | closed |
| T-55-19 | Tampering | evidence directory ambiguity | medium | mitigate | Exactly one run directory is committed; an exploratory leftover is removed before the commit and the removal is recorded | closed |
| T-55-20 | Information Disclosure | provenance argv capture | low | accept | The recorded argv is the operator's own command line and could embed a local absolute path under a non-default `--evidence-root`. The committed run uses only defaults, so no local path is recorded; verbatim argv capture is required by SC2's re-derivability wording and the operator controls what they pass. | closed — accepted |
| T-55-SC | Tampering (supply chain) | package installs | low | accept | No npm / pip / cargo install occurs in this phase; every import is stdlib or an already-pinned, long-standing project dependency (`torch`, `numpy`). `55-RESEARCH.md` Package Legitimacy Audit records `[SLOP]: none`, `[SUS]: none` and marks the gate not applicable. | closed — accepted |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `workflow.security_block_on` (high) count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-55-01 | T-55-20 | Provenance must capture argv verbatim for SC2 re-derivability; the committed run uses defaults only (no local path recorded); the operator controls what non-default paths they pass. | plan-time disposition (55-04), confirmed gsd-secure-phase | 2026-09-06 |
| AR-55-02 | T-55-SC | No package-manager install in this phase; all imports are stdlib or pinned pre-existing deps; RESEARCH.md legitimacy audit clean. | plan-time disposition (55-01…04), confirmed gsd-secure-phase | 2026-09-06 |

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-06 | 21 | 21 (19 mitigated + 2 accepted) | 0 | Claude (gsd-secure-phase, ASVS L1) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-09-06
