---
schema_version: 1
open_count: 2
waived_count: 0
fixed_count: 0
total_count: 2
last_updated: 2026-09-08T10:05:39.098Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 57 | unrun-verify | .planning/phases/57-corrected-re-run-the-preserved-evaluation/deferred-items.md |  | Phase-50 adjacent regression is unavailable because its archived .planning/phases/50-valid-stage-0-re-run/evidence path is absent in this checkout; preserved artifacts remain under .planning/milestones/v2.2-phases/. | open |  | 2026-09-08T10:02:55.085Z |  |
| 2 | 57 | stub | .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/run-ledger.md | 23 | The empty Phase-57 run ledger is an intentional pre-run scaffold; Plan 57-05 owns the operator-authorized smoke/band append. | open |  | 2026-09-08T10:05:39.098Z |  |

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
  }
]
````
