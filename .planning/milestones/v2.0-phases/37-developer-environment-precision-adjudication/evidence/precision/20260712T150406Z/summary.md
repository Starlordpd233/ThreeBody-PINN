# Phase 37 Dual-Arm Precision Probe — D1-p Evidence

- **schema_version:** `phase37-precision/v1`
- **timestamp:** 2026-07-12T15:03:59Z
- **repository_commit:** `df25a3f15f97d39c64c8af18d048b72829baf638`
- **fingerprint.path:** `<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/37-developer-environment-precision-adjudication/evidence/environment/20260712T150344Z/fingerprint.json`
- **fingerprint.sha256:** `0628f5d11983614db6e84caef948e1165755403232fd9bec5341722bcc57e901`
- **orchestration.timeout_seconds:** 900
- **orchestration.fallback_policy:** stripped-for-mps
- **orchestration.u:** 0.3

## Arms

### fp32-mps
- **status:** ok
- **requested_device:** mps
- **resolved_device:** mps
- **actual_device:** mps
- **pre_import_fallback:** None
- **torch.version:** 2.12.1
- **torch.mps_is_built:** True
- **full_jacobian:** aggregate_relative_error=0.0 criterion=1e-06 passed=True median_ns=606992.085
- **scalar_u_jvp:** aggregate_relative_error=0.0 criterion=1e-06 passed=True median_ns=805568.9550000001

### fp64-cpu
- **status:** ok
- **requested_device:** cpu
- **resolved_device:** cpu
- **actual_device:** cpu
- **pre_import_fallback:** None
- **torch.version:** 2.12.1
- **torch.mps_is_built:** True
- **full_jacobian:** aggregate_relative_error=0.0 criterion=1e-06 passed=True median_ns=103400.83499999999
- **scalar_u_jvp:** aggregate_relative_error=0.0 criterion=1e-06 passed=True median_ns=112854.58499999999

## Verification
- **status:** pass
  - `both_patterns`: pass
  - `fingerprint_hash_present`: pass
  - `two_arms`: pass

## Owner Decision

Owner decision required; no D1-p verdict is recorded by this report.

