---
schema_version: 1
open_count: 2
waived_count: 0
fixed_count: 2
total_count: 4
last_updated: 2026-11-04T02:36:12.699Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 57 | unrun-verify | .planning/phases/57-corrected-re-run-the-preserved-evaluation/deferred-items.md |  | Phase-50 adjacent regression is unavailable because its archived .planning/phases/50-valid-stage-0-re-run/evidence path is absent in this checkout; preserved artifacts remain under .planning/milestones/v2.2-phases/. | open |  | 2026-09-08T10:02:55.085Z |  |
| 2 | 57 | stub | .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/run-ledger.md | 23 | The empty Phase-57 run ledger is an intentional pre-run scaffold; Plan 57-05 owns the operator-authorized smoke/band append. | open |  | 2026-09-08T10:05:39.098Z |  |
| 3 | 67 | deviation | pinn/verification/diagnostic_phase67_execution.py | 1091 | 67-08 deviation: timing/science rows declared the observed gold-grid float64 endpoint 9.999999999999831 as t_end; the settings door requires the variant's nominal window length (10.0). Fixed in e2a3a380 with regression test; registrations re-pinned in c6dfb15c. | fixed |  | 2026-11-03T22:23:01.675Z | 2026-11-04T02:36:12.627Z |
| 4 | 67 | unrun-verify | .planning/phases/67-design-settings-ladders/67-08-PLAN.md |  | 67-08 task 3 verify gates never ran: launch-row refused at the AC-power admission gate (pmset Battery Power) before row 1 of 15; all timing rows, budget and science registrations are deferred until the Mac is on AC (window closes 2026-11-04 07:30 America/Chicago). check-budget/check-matrix-science unrun. | fixed |  | 2026-11-03T22:23:13.193Z | 2026-11-04T02:36:12.699Z |

````json
[
  {
    "id": 1,
    "kind": "unrun-verify",
    "phase": "57",
    "file": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/deferred-items.md",
    "line": null,
    "description": "Phase-50 adjacent regression is unavailable because its archived .planning/phases/50-valid-stage-0-re-run/evidence path is absent in this checkout; preserved artifacts remain under .planning/milestones/v2.2-phases/.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-08T10:02:55.085Z",
    "resolved_at": null
  },
  {
    "id": 2,
    "kind": "stub",
    "phase": "57",
    "file": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/run-ledger.md",
    "line": 23,
    "description": "The empty Phase-57 run ledger is an intentional pre-run scaffold; Plan 57-05 owns the operator-authorized smoke/band append.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-08T10:05:39.098Z",
    "resolved_at": null
  },
  {
    "id": 3,
    "kind": "deviation",
    "phase": "67",
    "file": "pinn/verification/diagnostic_phase67_execution.py",
    "line": 1091,
    "description": "67-08 deviation: timing/science rows declared the observed gold-grid float64 endpoint 9.999999999999831 as t_end; the settings door requires the variant's nominal window length (10.0). Fixed in e2a3a380 with regression test; registrations re-pinned in c6dfb15c.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-11-03T22:23:01.675Z",
    "resolved_at": "2026-11-04T02:36:12.627Z"
  },
  {
    "id": 4,
    "kind": "unrun-verify",
    "phase": "67",
    "file": ".planning/phases/67-design-settings-ladders/67-08-PLAN.md",
    "line": null,
    "description": "67-08 task 3 verify gates never ran: launch-row refused at the AC-power admission gate (pmset Battery Power) before row 1 of 15; all timing rows, budget and science registrations are deferred until the Mac is on AC (window closes 2026-11-04 07:30 America/Chicago). check-budget/check-matrix-science unrun.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-11-03T22:23:13.193Z",
    "resolved_at": "2026-11-04T02:36:12.699Z"
  }
]
````
