---
phase: 64-feasibility-verdict
plan: 03
subsystem: verification
tags: [verdict-figure, svg-stdlib, panel-a, panel-b, provenance, byte-reproducible, independent-rederivation, rendered-look, feas-06]

requires:
  - phase: 64-feasibility-verdict
    provides: "the number manifest and the CPU re-derivation (64-02): derive_state, constant_predictor_error, rederive_state, rederive_constant_error, the open attestation and the shared evidence_io writers"
  - phase: 60-single-system-learnability
    provides: "the r1-1632 record with better_state polish and states.polish.weights, the committed polish.weights and the sealed stop-handoff.json"
  - phase: 59-read-only-baseline-scorecard
    provides: "the frozen feasibility scorecard with Tier-1 E_max 0.1"

provides:
  - "evidence/build_phase64_figure.py: the deterministic standard-library SVG producer for the one verdict figure, plus the figure_series derivation, the provenance and the legibility guard"
  - "evidence/figure-1632.svg: panel A (real orbit, network prediction, time-mean markers, three magnified insets), panel B (network error and constant-predictor error against time with the Tier-1 limit) and the legend"
  - "evidence/figure-1632.provenance.json: schema phase64-figure-provenance/v1 with four input SHA-256s, two producer SHA-256s, the SVG SHA-256, the series SHA-256, arm r1-1632, state polish, CPU float64, the three versions, data_root_source and the open attestation; no timestamp, git head or host path"
  - "verify_phase64_verdict.py figure: re-derives the series independently, matches series_sha256, regenerates the SVG from the series and requires byte equality, checks every provenance digest, enforces the viewBox on every text element and polyline point, rejects script/href/home-directory strings, and prints FIGURE-OK"
  - "tests/phase64/test_verifier_phase64.py: 29 new tests (135 in all) covering pure rendering, the fail-closed negative controls and the real files"

actuals:
  tokens: 64924
  tasks: 2
  commits: 2
  plan_head_before: 5575f04b6c9ec8515bb4d875900796edd16e83ec

tech-stack:
  added: []
  patterns:
    - "Standard-library SVG only: strings assembled from fixed-order helpers (_poly, _line, _rect, _text, _cross) with every coordinate rounded to 0.1; no plotting library, no install"
    - "One derived series feeds both panels and the provenance: figure_series rounds the shared derive_state and constant_predictor_error output to 10 decimals, and series_sha256 is the SHA-256 of evidence_io.canonical_json_bytes without the attestation"
    - "The verifier regenerates rather than trusts: rederive_state and rederive_constant_error rebuild the series, and render_svg is re-run on that series so the committed SVG must equal the bytes the verifier would write"
    - "Provenance without ambient state: no timestamp, git head or host path, so two runs in two processes produce the same bytes; the figure's own SHA-256 is recorded in the provenance and checked against the file"
    - "Legibility as a producer precondition: legibility_report measures the legend box and each predicted track's extent from the SVG before write or check, so an illegible figure cannot be committed silently"
    - "Fail-closed SVG inspection with xml.etree: every text x/y and every polyline point must lie inside the viewBox; script elements and href/xlink:href attributes are rejected"

key-files:
  created:
    - .planning/phases/64-feasibility-verdict/evidence/build_phase64_figure.py
    - .planning/phases/64-feasibility-verdict/evidence/figure-1632.svg
    - .planning/phases/64-feasibility-verdict/evidence/figure-1632.provenance.json
  modified:
    - .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py
    - tests/phase64/test_verifier_phase64.py

key-decisions:
  - "Panel A carries three 70x70 magnified insets, one per body, because the predicted tracks span only 0.0022 to 0.0041 units against an orbit about 0.54 x 0.53 wide: at full scale the prediction is a dot, and Pitfall 11 asks for it to be visible beside the real orbit"
  - "Inset polylines are 1.2 px while the panel A real tracks stay 1.5 px and the predicted tracks 3 px, so the tests can count exactly three real and three predicted tracks by stroke width without the inset copies inflating the count"
  - "Panel B draws the constant predictor as a 3.5 px dashed grey reference under the network's 1.5 px solid ink curve: the two curves differ by only about 0.006, so a same-width dashed line disappeared beneath the solid one; the wider reference stays visible as a fringe"
  - "The verifier checks provenance inputs by existence and SHA-256, not by git tracked/clean, so the temporary-copy negative controls in FigureModeTests exercise the digest path without a git repository"
  - "FIGURE_GROUPS is panel-a, panel-b and legend; the legend is a first-class group so a missing or out-of-canvas legend fails the same document check as a missing panel"
  - "The producer gained legibility_report and _check_legibility, run before every write and check: the plan's manual look is kept, and the measurable part (legend inside the canvas, each predicted track with non-zero extent) is now enforced in code"

requirements-completed: [FEAS-06]

coverage:
  - id: D1
    description: "D-04: one figure shows system 1632's real orbit beside the trained network's prediction, from the committed r1-1632 polish weights re-scored on the CPU in float64 in seconds; nothing is trained"
    requirement: "FEAS-06"
    verification:
      - kind: unit
        ref: "tests/phase64/test_verifier_phase64.py#FigureRenderTests"
        status: pass
      - kind: integration
        ref: "python -B .planning/phases/64-feasibility-verdict/evidence/build_phase64_figure.py -> FIGURE-WRITTEN d9754afa..., FIGURE-LEGIBLE ..."
        status: pass
    human_judgment: false
  - id: D2
    description: "The provenance records the four input paths and SHA-256s, both producer digests, the SVG and series digests, arm, state, precision, versions, data_root_source and the open attestation, with no timestamp, git head or host path"
    verification:
      - kind: unit
        ref: "tests/phase64/test_verifier_phase64.py#FigureModeTests.test_the_provenance_holds_the_contracted_keys"
        status: pass
      - kind: integration
        ref: "shasum -a 256 figure-1632.svg -> d9754afa... equals provenance.figure.sha256"
        status: pass
    human_judgment: false
  - id: D3
    description: "The SVG is byte-reproducible: a second process regenerates both files and prints FIGURE-CHECK-OK, and the committed bytes are unchanged"
    verification:
      - kind: other
        ref: "python -B .planning/phases/64-feasibility-verdict/evidence/build_phase64_figure.py --check -> FIGURE-CHECK-OK"
        status: pass
    human_judgment: false
  - id: D4
    description: "figure re-derives the plotted series with the verifier's own code, matches series_sha256, regenerates the SVG from that series and requires byte equality, checks every provenance digest, enforces the viewBox and rejects script, href and home-directory strings"
    verification:
      - kind: unit
        ref: "tests/phase64/test_verifier_phase64.py#FigureModeTests,FigureRealTests"
        status: pass
      - kind: integration
        ref: "python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py figure -> figure times 1001, FIGURE-OK"
        status: pass
    human_judgment: false
  - id: D5
    description: "The figure was rendered and looked at before it was committed: legend inside the canvas, labels legible, predicted tracks visible beside the real orbit, both error curves above the Tier-1 line"
    verification:
      - kind: manual
        ref: "qlmanage -t -s 1400 on a 700x327 copy in /private/var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/opencode/phase64-03-render; PNG not committed"
        status: pass
    human_judgment: true

duration: 28min
completed: 2026-10-26
status: complete
---

# Phase 64 Plan 03: The System 1632 Verdict Figure Summary

**The verdict's one figure is committed: system 1632's real orbit beside the trained network's near-still prediction, the two error curves against time with the Tier-1 limit, and a provenance record that lets a second process regenerate and verify every byte.**

In plain language: the left panel shows the three bodies on their real orbits, the network's prediction for each body sitting almost still near that body's average position, and three magnified insets because the prediction is roughly a hundred times smaller than the orbit. The right panel shows how wrong the network is at every moment, beside the error of simply guessing each body's average position, and the 0.1 line it would have to get under to reach Tier 1; both curves stay far above it. The figure is drawn from the committed weights on the CPU in about three seconds, with no plotting library, and a separate checker re-derives the data, rebuilds the SVG and refuses any byte that differs.

## Performance

- **Duration:** about 28 min
- **Started:** 2026-10-26T05:01:08Z (precondition checked; ledger base `5575f04b`, the 64-02 summary commit)
- **Completed:** 2026-10-26T05:29Z
- **Tasks:** 2
- **Commits:** 2
- **Files modified:** 5 (the producer, SVG and provenance created; the verifier and the test module extended)

## Accomplishments

- **Task 1 — the tracer:** `build_phase64_figure.py` and panel A. `figure_series` sets `torch.set_num_threads(1)`, chdirs to the repository root, opens one `open_real_context`, reads r1-1632's `better_state` (`polish`), calls the shared `derive_state` and `constant_predictor_error`, and rounds every float to 10 decimals. `render_svg` lays out a 1200 x 560 viewBox with panel A (80–410 x 100–430), the real x-y tracks at 1.5 px in the three body colours, the predicted tracks at 3 px over a white halo, a cross at each time-mean, axis labels and a leader-line label reading "network prediction (barely moves)", plus three 70 x 70 magnified insets. The provenance and `verify_phase64_verdict.py figure` landed in the same task, with 20 new tests. 126 tests at that point; `FIGURE-OK` and `FIGURE-CHECK-OK`.
- **Task 2 — panel B, the legend and the look:** panel B (760–1140 x 100–430) plots `max(e_sys, e_in)` from 0 to 1.25 against time 0 to 10, with the network's error as a solid ink curve, the constant time-mean predictor as a wider dashed grey reference beneath it, and the scorecard's Tier-1 limit at 0.1 as a red dashed line labelled "Tier 1 limit (0.1)". A legend group below both panels lists the three real orbits, the network prediction, the time-mean position, the network error, the constant-predictor error and the Tier-1 limit. `legibility_report` and `_check_legibility` were added, and 9 tests took the module to 135. The final SVG is `d9754afa…` and the provenance `409e5e87…`.

## Task Commits

Each task was committed atomically through `scripts/agent-commit`:

1. **Task 1: panel A, the provenance and the figure check** — `b25dd48b` (`evidence`)
2. **Task 2: panel B, the legend, the legibility guard and the rendered look** — `a547f59e` (`evidence`)

## Verification Results

| Command | Result |
|---|---|
| `python -B -m unittest tests.phase64.test_verifier_phase64 -v` | Ran 135 tests in 56.2 s, `OK`, exit 0 |
| `verify_phase64_verdict.py figure` | `figure times 1001`, `FIGURE-OK`, exit 0 (2.2 s) |
| `build_phase64_figure.py` | `FIGURE-LEGIBLE …`, `FIGURE-WRITTEN d9754afa…`, exit 0 (2.7 s) |
| `build_phase64_figure.py --check` | `FIGURE-CHECK-OK`, exit 0 (2.2 s); both files byte-unchanged |
| `verify_phase64_verdict.py numbers` | `NUMBERS-OK`, exit 0 (1.5 s) |
| `verify_phase64_verdict.py derive` | `DERIVE-OK`, exit 0 (5.6 s) |
| `verify_phase64_verdict.py frozen` | `FROZEN-OK`, exit 0 (0.5 s) |
| `verify_phase64_verdict.py inputs` | `INPUTS-OK`, exit 0 (0.6 s) |
| `verify_phase60_evidence.py final` | `PHASE60-EVIDENCE-OK`, exit 0 |
| `verify_phase59_evidence.py scorecard-frozen` | `SCORECARD-FROZEN-OK`, exit 0 |
| `verify_phase59_evidence.py guardrails` | `GUARDRAILS-OK`, exit 0 |

The committed digests are:

- `figure-1632.svg` — `d9754afaf0aefdf2c4b3f27dfc97b6cac06e4bac4adb63b5b5447efdd69a7695`
- `figure-1632.provenance.json` — `409e5e87adc3729b4ae26d40b5b3f1fd6a68116cd0b842588fee9154f1d8bde0`
- `series_sha256` — `6574144710f53fa6fa86b7d0990fa2801578bf443a5c898ac216d2a939c6f8ec`
- `build_phase64_figure.py` — `263d2277af74056b6e2537203edf029ac48b29724927b71cd609cb170b2d7d9a`

The provenance's open attestation read `schema phase59-files-opened/v1`, `data_root_source git_common_dir_default`, `opened.train 258`, `opened.validation 0`, `opened.other_under_root 0`, `test_split_opened 0`, `blocked_attempts 0`, `refused_before_open 0`. The versions are python `3.11.15`, numpy `2.4.6`, torch `2.12.1`.

### Rendered look (the manual row)

A 700 x 327 copy of the SVG was rendered with `qlmanage -t -s 1400` into `/private/var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/opencode/phase64-03-render` and opened. The PNG is outside the repository and is not committed. Checked and found: the legend sits fully inside the canvas below both panels; every title, axis label, tick label and legend entry is legible; each body's predicted track is visible in its inset beside the real orbit; the network and constant-predictor curves both run above the Tier-1 line for the whole window; the "Tier 1 limit (0.1)" label does not collide with the curves. The producer's measured report is `FIGURE-LEGIBLE legend 80.0,476.0,1120.0,544.0 predicted 0.0022x0.0018 0.0040x0.0032 0.0041x0.0034` — the legend box and the three predicted-track extents.

### Mutant checks

- Task 1: the text-element viewBox check removed by hand — `figure` failed on the moved text and `FigureModeTests.test_a_text_element_outside_the_viewbox_fails` failed; restored, `FIGURE-OK` again.
- Task 2: the legend's maximum-y bound removed by hand — the legend check accepted a box past the canvas and the legibility test failed; restored, `FIGURE-CHECK-OK` again.

## Files Created/Modified

- `.planning/phases/64-feasibility-verdict/evidence/build_phase64_figure.py` — the producer: `figure_series`, `series_digest`, the SVG helpers (`_poly`, `_line`, `_rect`, `_text`, `_cross`, `_axis`), `_panel_a`, `_mini_panel`, `_panel_b`, `_legend`, `legibility_report`, `_check_legibility`, `render_svg`, `build_provenance`, `cmd_figure`, `main`.
- `.planning/phases/64-feasibility-verdict/evidence/figure-1632.svg` — 124 lines: title, `panel-a` with three real tracks, three predicted tracks and three insets, `panel-b` with two error curves and the Tier-1 line, and `legend`.
- `.planning/phases/64-feasibility-verdict/evidence/figure-1632.provenance.json` — 53 lines, canonical JSON: schema, figure, inputs (four), producers (two), series_sha256, arm, state, precision, versions, data_root_source, attestation, command and plain_language.
- `.planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py` — `FIGURE_*` constants, `_check_svg_document`, `cmd_figure`, the shared `_check_attestation_summary`, and the `figure` entry in `COMMANDS`.
- `tests/phase64/test_verifier_phase64.py` — `FigureRenderTests`, `FigureModeTests` and `FigureRealTests` (29 tests), taking the module to 135.

## Decisions Made

- **Insets are part of panel A, not a second figure.** The predicted tracks are 0.0022 to 0.0041 units across against an orbit about 0.54 x 0.53; without magnification the network's motion is a single dot. Three 70 x 70 insets keep the full orbit and the prediction visible in one panel, as 64-RESEARCH Pitfall 11 asks.
- **Stroke widths encode the element class.** Panel A real tracks are 1.5 px, predicted tracks 3 px, and inset copies 1.2 px, so tests can assert exactly three of each in panel A without mistaking an inset copy for a main track.
- **The constant-predictor reference is deliberately wider.** The two error curves differ by about 0.006, so a same-width dashed line under the solid ink curve is invisible; a 3.5 px dashed grey line under a 1.5 px solid ink line leaves a visible fringe on both sides while keeping the network curve primary.
- **The verifier regenerates the SVG.** `figure` does not parse-and-accept the committed document: it rebuilds the series with `rederive_state` and `rederive_constant_error`, then calls the producer's `render_svg` on that series and requires byte equality. A changed input, a changed series or a hand-edited SVG all fail.
- **Inputs are checked by digest, not by git state.** Existence plus SHA-256 is the contract, so the temporary-copy negative controls in `FigureModeTests` can prove a stale input digest fails without needing a git checkout.
- **Legibility is measurable, not only visual.** The legend box and each predicted track's extent are computed from the generated SVG and asserted before writing; the manual render remains the check for the things a number cannot express (type legibility, overlap, visual balance).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical functionality] The legibility requirement was manual-only (Task 2)**
- **Found during:** Task 2, after the first panel B render
- **Issue:** the plan required the figure to be looked at, but nothing prevented a later regeneration from committing a legend outside the canvas or a predicted track collapsed to a point.
- **Fix:** `legibility_report` measures the legend's bounding box and each body's predicted-track extent from the SVG, `_check_legibility` refuses a legend outside the viewBox or a zero-extent predicted track, and both the write path and `--check` call it. The manual render was still performed.
- **Files modified:** `.planning/phases/64-feasibility-verdict/evidence/build_phase64_figure.py`
- **Commit:** `a547f59e`

### Presentation choices the plan's wording did not cover

**2. Three magnified insets in panel A (Task 1)**
- **Found during:** Task 1, after the first real render showed the predicted tracks as a dot
- **Choice:** three 70 x 70 inset panels, one per body, each repeating the real track, the predicted track and the time-mean marker at a scale set by that body's own extent.
- **Why:** 64-RESEARCH Pitfall 11 requires the prediction to be visible beside the real orbit; at full scale it is not. The insets are presentation-only and read from the same series.
- **Commit:** `b25dd48b`

**3. Inset polylines use 1.2 px (Task 1)**
- **Found during:** Task 1, writing the stroke-width test
- **Choice:** inset copies are 1.2 px while panel A's real tracks stay 1.5 px and its predicted tracks 3 px.
- **Why:** the tests count panel A's three real and three predicted tracks by width; 1.5 px inset copies would make the count ambiguous.
- **Commit:** `b25dd48b`

**4. The constant-predictor curve is a wider dashed reference beneath the network curve (Task 2)**
- **Found during:** Task 2, on the rendered look: a same-width dashed line vanished under the solid curve
- **Choice:** 3.5 px dashed grey under 1.5 px solid ink, rather than the plan's same-weight dashed neutral grey.
- **Why:** the curves differ by about 0.006, less than a stroke width; the wider reference is the only way both remain distinguishable without moving one curve off its true values.
- **Commit:** `a547f59e`

**5. `FIGURE_GROUPS` includes the legend, and the attestation check is shared (Task 1)**
- **Found during:** Task 1, wiring the document check
- **Choice:** the required group list is `panel-a`, `panel-b` and `legend`; `_check_attestation_summary` now backs both the live and recorded attestation checks with unchanged messages.
- **Why:** a missing or out-of-canvas legend should fail the same way a missing panel does, and duplicating the five-counter check would let the two copies drift.
- **Commit:** `b25dd48b`

## Known Stubs

None. Every plotted value is derived from the committed weights and the scorecard; the provenance's four inputs and two producers exist and match their recorded SHA-256s; the SVG is complete (no placeholder text, no unwired panel). The three insets repeat committed series values and introduce no new data.

## Threat Flags

None beyond the plan's threat model. The new surface is read-only: committed weights, records and scorecard read through `repo_path` containment, with `torch.load(weights_only=True)` after a digest check, and no network, write path or new trust boundary. The SVG is inert by construction — `_check_svg_document` rejects every `script` element and every `href`/`xlink:href` attribute — and neither the SVG nor the provenance contains a home-directory string (`test_a_home_directory_string_fails`).

## Notes

- `.planning/STATE.md`, `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` were not modified and no state, roadmap or requirements verb was run: the orchestrator owns those files.
- `git status --porcelain -- pinn .planning/phases/60-single-system-learnability .planning/phases/59-read-only-baseline-scorecard runs` prints nothing after the plan, so no training output, sealed evidence or pinned module was touched.
- Pre-existing user-owned changes in the working tree (`.planning/config.json`, `.planning/state.json`, `.planning/milestone.lock`, `.planning/tmp/`, `.agents/`, `.gsd/`, `.planning/agent-history.json`, the v2.2 stage-0 halt brief, the `docs/work` review folders, `phase-40-plan-04-grok.md`) were left alone and never staged.
- The figure and both checks must run from the repository root, because `default_data_root()` reads the git common directory from the working directory; on this Mac the external data root resolved and `FigureRealTests` ran rather than skipped.
- The rendered PNG lives only under the temporary directory named above; no binary artifact entered the repository.
- Ledger: 2 commits measured from `5575f04b` (`git rev-list --count`).

## Next Phase Readiness

- 64-04 and 64-05 can cite `evidence/figure-1632.svg` with its SHA-256 `d9754afa…` and the provenance; the figure quotes only values already present in `numbers.json` and is re-derived from the same helpers.
- `figure` is in the verifier's `COMMANDS` table; the wave gate is green: 135 tests, `FIGURE-OK`, `FIGURE-CHECK-OK`, `NUMBERS-OK`, `DERIVE-OK`, `FROZEN-OK`, `INPUTS-OK`, `PHASE60-EVIDENCE-OK`, `SCORECARD-FROZEN-OK`, `GUARDRAILS-OK`.
- No gaps were raised: the plan and 64-RESEARCH answered every presentation question, and `64-GAPS.md` was not written.

## Self-Check: PASSED
