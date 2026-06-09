---
phase: 22
plan: 01
wave: 0
status: complete
executed_at: 2026-06-09
pre_ws_a_baseline_ref: v1.4-pre-phase-22 (tag on faa73d0)
footnote_policy: unsupported
---

# 22-01 Summary — Wave 0: Detector, Census, Footnote Probe

## Completed Deliverables

| Artifact | Status | Location |
|----------|--------|----------|
| Detector toolchain | ✅ pinned + lockfile committed | `tools/spec-render-check/` |
| detect.mjs (6 layers + census + sanity gate) | ✅ implemented + selftest green | `tools/spec-render-check/detect.mjs` |
| Regression fixtures + negative controls | ✅ G1 pass | `tools/spec-render-check/fixtures/regression.md` |
| Stage-0 footnote probe | ✅ confirmed `unsupported` | `.planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-STAGE0-FOOTNOTE-PROBE.md` |
| Pre-WS-A baseline ref | ✅ `v1.4-pre-phase-22` tag on faa73d0 | git tag |
| Pre-WS-A comment census | ✅ 26 comments (13+13+0) | `.planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-COMMENT-CENSUS-PRE.md` |
| README | ✅ run commands documented | `tools/spec-render-check/README.md` |

## Key Decisions

### Footnote Policy (22-STAGE0-FOOTNOTE-PROBE.md)

**Result:** `unsupported`

**Evidence:** User screenshot of Cursor Markdown Preview showed `[^probe1]` and `[^probe2]` rendering as literal text, not as superscript footnote links. Definitions also rendered as inline text, not as a footnotes list.

**Implications:**
- Detector D4 flags `[^n]` refs/defs as DEFINITE survivors
- The 37 footnote refs / 17 defs in `pinn_architecture.md` are repair targets
- `--footnote-policy unsupported` enables `--all` to reach zero with footnotes converted to a render-safe form
- 22-02 will handle footnote repair in `pinn_architecture.md`

## Verification Results

```
$ node tools/spec-render-check/detect.mjs --selftest
sanity gate: PASS (inline + block math rendered by KaTeX)
regression fixtures: 9 labeled regions → all match expectations
negative control sampling_method.md: 0 findings (1 suppressed)
SELFTEST PASS (G1): regression reproduced, negative controls clean.

$ node tools/spec-render-check/detect.mjs pinn_instruction/markdown_conversion/framework-specs/sampling_method.md
-- totals: 0 DEFINITE, 0 REVIEW, 1 SUPPRESSED (surfaced for review) --
```

## Pre-WS-A Census Summary

| File | Comment Count |
|------|---------------|
| ctl_instruction.md | 13 |
| pinn_architecture.md | 13 |
| sampling_method.md | 0 |
| **Union** | **26** |

Downstream plans (22-04, 22-05) consume `22-COMMENT-CENSUS-PRE.md` for before/after preservation diff and G3 audit.

## Next Steps

- **22-02:** Repair `pinn_architecture.md` (footnotes + other defects)
- **22-03:** Repair `ctl_instruction.md` (non-footnote defects)
- **22-04:** Wave 2 governance (author-comment preservation + FUT-05 handoff)
- **22-05:** Wave 3 closure (full detector suite + content-preservation audit)
