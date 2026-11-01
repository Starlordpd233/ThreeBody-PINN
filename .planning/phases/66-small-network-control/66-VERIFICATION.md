---
phase: 66-small-network-control
verified: 2026-11-01T21:27:15Z
status: passed
score: 37/37 must-haves verified (34 plan truths + 3 roadmap success criteria)
behavior_unverified: 0
overrides_applied: 0
prohibitions_judgment_tier: 4 # all 4 resolved with evidence; see prohibitions checklist below
re_verification:
  previous_status: none
  previous_score: n/a
  gaps_closed: []
  gaps_remaining: []
  regressions: []
gaps: []
deferred: []
behavior_unverified_items: []
coincidental_reliance_items: []
requirements:
  EXP-01:
    status: satisfied
    evidence: >
      A network with fewer parameters (157,065 < 795,657) and fewer layers
      (1 hidden < 12) fits orbit 1632 from time alone (data-only): main run
      E 0.011431234453278821, Tier 1 (E <= 0.1), confirmed on a second panel
      system (851/s42, E 0.01720558902801923) and a second seed (1632/s41,
      E 0.07898485527313073); the architecture is fixed on the committed
      prediction page 66-PREDICTION.md (exp01-d1-w384-o1000, design block
      byte-equal to exp01_design()). The pre-registered Tier-1 branch reading
      (REQUIREMENTS.md "How the first results can reshape the plan": "too
      small" is refuted for one orbit; EXP-02..05 run as planned) matches the
      recorded route phase67-as-planned.
    note: >
      The REQUIREMENTS.md traceability row (line 244) still reads "Pending"
      and the ROADMAP.md Phase 66 box is still unchecked. This is deliberate:
      the ruling page records "The EXP-01 requirement mark follows the phase
      verification, as in Phase 65", and 66-05-SUMMARY.md records the plan's
      own acceptance criterion that ROADMAP.md and REQUIREMENTS.md stay
      unchanged (verified: `git diff --stat 2b5d0df7..HEAD -- .planning/ROADMAP.md
      .planning/REQUIREMENTS.md pinn tests` is empty). Marking is the
      orchestrator's phase.complete step. Not counted as a gap.
must_haves:
  - id: SC-1
    truth: "A prediction page committed before the first run: architecture and parameter count (fewer layers/parameters than locked), what each suspect predicts, budget from the measured rate, reading rule"
    status: verified
    evidence: >
      66-TIMING-PREDICTION.md (frozen design, commit 4eab280b) and
      66-PREDICTION.md (budget, commit 3f4d0a85) both committed before every
      run commit (git merge-base --is-ancestor chain ORDER-OK). Page design
      blocks byte-equal to live exp01_design(); parameters 157,065 < 795,657,
      depth 1 < 12; suspect table, reading rule, band edges, N=465000 budget
      present; budget reproduces live: EXP01-BUDGET steps=465000
      loss_trace_stride=47 cap=3300.0.
  - id: SC-2
    truth: "The result on orbit 1632 is scored: tier, E against the constant predictor and the two-Kepler formula, neighbour-similarity trace; a confirming result repeated on a second panel system and a second seed"
    status: verified
    evidence: >
      Three committed records (main-1632-s42, repeat-851-s42, repeat-1632-s41)
      each status complete, 465000 steps, 14-entry similarity cadence with
      input+h1 rows, E_const and two_kepler comparison rows. verify-result
      prints VERIFY-RESULT-OK and check-run prints EXP01-CHECK-OK (empty
      mechanical/setting problems) on all three, re-run by this verification.
      diagnostic_phase66 review reproduces: EXP01-REVIEW confirmation=confirmed
      route=phase67-as-planned, all three runs tier1.
  - id: SC-3
    truth: "The review is recorded: the branch taken, the plain-language reading, and any plan change proposed under SCOPE-49 with the owner's answer"
    status: verified
    evidence: >
      66-RESULT.md (commit 89045a7f) records branch tier1 on all three, the
      pre-registered tier1 plain-language reading, and the SCOPE-49 proposal
      (none; route phase67-as-planned). 66-CHECKPOINT-1-RULING.md (commit
      e40ebca2, status ratified) records the owner's checkpoint 1 answer
      verbatim in one owner-quote block ("Accept the recorded proposal") and
      the CP1-EXP01 = accept row. RESULT-PAGE-OK and RULING-OK (the plan's
      automated checks) both reproduce under the pinned interpreter.
  - id: P1-T1
    truth: "66-01: a committed phase66 registration passes the unchanged admission door, fits the synthetic fixture end to end, and publishes a verify-accepted record with variant.registry phase66 / registered true"
    status: verified
    evidence: "tests/phase66 discovery 99 tests OK (includes test_tracer end-to-end AC and battery cases); live check-registration CHECK-REGISTRATION-OK on all four committed registrations; the three real records carry variant name exp01-d1-w384-o1000, registered true, registry phase66."
  - id: P1-T2
    truth: "66-01: the sealed REGISTRY still holds exactly locked-12; unknown/absent registry names refuse before any data access"
    status: verified
    evidence: "tests/phase66/test_catalog.py pins the catalog (within the 99 OK); REGISTRIES = MappingProxyType({phase66: ...}) at diagnostic_phase66.py:100; _named_registry refuses unknown names (diagnostic_fit.py:317-330) before data access."
  - id: P1-T3
    truth: "66-01: every Phase 65 settings refusal still refuses with the EXP-01 variant; the full Phase 65 suite still passes with 204 tests"
    status: verified
    evidence: "Live run: tests/phase65 discovery = 204 tests, OK (36.9 s) under the pinned interpreter."
  - id: P1-T4
    truth: "66-01: registration-declared loss_trace_stride (Site F) thins only the recorded trace, counts unchanged, and verify refuses disagreeing stride/length/last-entry"
    status: verified
    evidence: "tests/phase66/test_admission.py stride matrix passes (within 99 OK); real records show stride 47 with 9,894 loss entries and unchanged completed_steps 465000; timing record stride 1 with 5,200 entries."
  - id: P1-T5
    truth: "66-01: pinned Phase 65 modules byte-identical; smoke registration historical from the harness commit, identity anchored at 84128fe2"
    status: verified
    evidence: "Current digests of diagnostic_guard/data/variants/similarity.py match the smoke registration's recorded digests exactly; test_historical passes (within 99 OK); git log c919194d..HEAD on the phase 65 directory is empty."
  - id: P1-T6
    truth: "66-01: the launch path reads power first, refuses on anything but AC Power creating nothing, writes the exclusive power-gate.json receipt, then runs caffeinate -is <python> -B -m pinn.verification.diagnostic_fit run"
    status: verified
    evidence: "tests/phase66/test_tracer.py battery case and test_power.py refusal matrix pass (within 99 OK); all four real receipts record power_source 'AC Power' with checked_utc preceding the attempt started_utc."
  - id: P2-T1
    truth: "66-02: diagnostic_power refuses fail-closed on battery/UPS/garbage/misplaced-AC/nonzero-pmset/missing-pmset/timeout/outside-weekend-window/existing-output/inadmissible-registration; receipt records the window"
    status: verified
    evidence: "tests/phase66/test_power.py 22 tests OK (within 99 OK); require_weekend_window enforces America/Chicago Saturday / Sunday-before-22:00 in code (diagnostic_power.py:130); all real receipts carry the window block with isoweekday 7 (Sunday)."
  - id: P2-T2
    truth: "66-02: E-EXP01-concurrency — repeated/parallel launches into the same output directory refuse at the O_EXCL receipt or attempt claim; nothing retries, extends or resumes automatically"
    status: verified
    evidence: "Tracer/power tests exercise the exclusive paths (within 99 OK); write_record_exclusive is O_CREAT|O_EXCL (per 66-REVIEW.md trace); no retry directories exist under evidence/exp01/ or evidence/timing/."
  - id: P2-T3
    truth: "66-02: classify_exp01 edges — E == 0.1 inclusive is tier1; both band edges are near; non-finite is other; still_improving forces unsettled above Tier 1; confirm only for three shared tier1/near; route table"
    status: verified
    evidence: "tests/phase66/test_reading_rule.py 20 tests OK (within 99 OK); live review output matches: three tier1 runs -> confirmation=confirmed, route=phase67-as-planned."
  - id: P2-T4
    truth: "66-02: improvement_check reads only the DIAG-09 logger's output movement (0.75 reference fraction, strict 0.01 growth); unsettled never confirms and routes to owner"
    status: verified
    evidence: "tests/phase66/test_reading_rule.py ImprovementTests pass; all three real runs read still_improving false (growth 0.00024 / 0.00014 / -0.00055 < 0.01), and all three landed tier1 anyway."
  - id: P2-T5
    truth: "66-02: the step-0 first-layer-frequency bandwidth check [0.95 B, 1.00001 B] is the page's in-run setting check; failure is a setting problem, not mechanical"
    status: verified
    evidence: "Reading-rule/record-reader tests pass (within 99 OK); read-run on all three runs reported no setting problems (RESULT page); step-0 max 22.732187271118164 sits inside [21.5996, 22.7366] for B = 22.736420441699334."
  - id: P2-T6
    truth: "66-02: read_exp01_record/read_run_directory never read a branch from a run with a mechanical problem; the problem list is the D-10 list; out-of-branch routes to owner"
    status: verified
    evidence: "tests/phase66/test_reading_rule.py RecordReaderTests pass; all three real runs read with empty mechanical_problems and empty setting_problems."
  - id: P2-T7
    truth: "66-02: check-run runs the same checks as read-run and prints only the directory and value-free problem lists — never E, tier, eps_h, E_const, branch, improvement, similarity or loss"
    status: verified
    evidence: "Live check-run output observed on all four directories: JSON with dir/mechanical_problems/setting_problems only, final line EXP01-CHECK-OK; no score value appeared."
  - id: P2-T8
    truth: "66-02: exp01_budget sets N by time alone (largest 1,000-multiple whose projected wall at a 25 percent margin stays within 0.75 of the 3,300 s cap), stride ceil(N/10,000), N-independent record-size ceiling; refuses only on a broken input"
    status: verified
    evidence: "tests/phase66/test_budget.py 9 tests OK; live budget command reproduces EXP01-BUDGET steps=465000 loss_trace_stride=47 cap=3300.0; real records 1.25 MB each, far under the 10,485,760-byte limit."
  - id: P2-T9
    truth: "66-02: freeze — after this plan diagnostic_fit.py, diagnostic_phase66.py and diagnostic_power.py do not change for the rest of Phase 66; the seven dependency digests are recorded"
    status: verified
    evidence: "git log 734cb7da..HEAD on the three modules is empty; working tree clean on pinn/verification and tests/phase66; all seven current SHA-256 digests equal the frozen set recorded in 66-02-SUMMARY.md and 66-RESULT.md."
  - id: P3-T1
    truth: "66-03: 66-TIMING-PREDICTION.md committed before any Phase 66 run of any kind, holding the frozen design (exp01-design block, architecture/parameter breakdown, bandwidth case, suspect predictions, reading rule, repeats/confirmation, budget rule, no extension rule)"
    status: verified
    evidence: "Commit 4eab280b is an ancestor of the timing record commit a564ea35 and of every later commit (ORDER-OK chain); TimingPageTests pass (within 99 OK); design block byte-equal to exp01_design() re-checked live."
  - id: P3-T2
    truth: "66-03 (checker blocker 1): near applies only to a settled run with passing setting checks; a still-improving non-Tier-1 run reads unsettled; the near reading follows the owner-registered wording and never locates the fault"
    status: verified
    evidence: "Present on the committed pages and enforced by the classify/confirm/route code (reading-rule tests); RESULT page carries the owner-registered tier1 reading and the explicit 'What this result does not say' limits."
  - id: P3-T3
    truth: "66-03: the timing calibration ran once through the AC and weekend-window gate, detached after a passing survival test; verify-result VERIFY-RESULT-OK and check-run EXP01-CHECK-OK; the timing score was never read"
    status: verified
    evidence: "Timing record committed at a564ea35; this verification re-ran verify-result (OK, exit 0) and check-run (EXP01-CHECK-OK, empty problems, value-free) on evidence/timing/1632-s42; no read-run was issued by this verification against the timing directory."
  - id: P3-T4
    truth: "66-03: 66-PREDICTION.md committed after the timing record and before every experiment registration; its design block byte-identical to the timing page's; it states the budget exp01_budget computes from the committed timing evidence"
    status: verified
    evidence: "Ancestry a564ea35 -> 3f4d0a85 (ORDER-OK); both design blocks equal live exp01_design(); the page's budget section matches the live EXP01-BUDGET reproduction (N=465000, stride 47, cap 3300.0, projected wall 2470.2 s of the 2475 s target)."
  - id: P3-T5
    truth: "66-03: three fresh registrations pin 66-PREDICTION.md and the seven frozen code digests, differ only in title/orbit_key/orbit_note/seed, and pass check-registration; none reuses the Phase 65 smoke registration"
    status: verified
    evidence: "Live check-registration CHECK-REGISTRATION-OK on all three (commit 3f4d0a85 each); the 22-entry RESULT-page evidence-index digests (including the three registrations and both pages) all match committed bytes; the smoke registration file is untouched."
  - id: P3-T6
    truth: "66-03: evidence order — timing page, timing registration, timing record, prediction page, each experiment registration each have the previous as an ancestor"
    status: verified
    evidence: "git merge-base --is-ancestor chain verified live: 4eab280b -> a564ea35 -> 3f4d0a85 -> {a546016b, 3dc3646a, 277c25ce}; plus freeze 734cb7da -> 4eab280b and records -> 89045a7f -> e40ebca2. ORDER-OK."
  - id: P4-T1
    truth: "66-04: the three registered runs each ran once, one at a time, in order, through the AC and weekend-window gate; repeats ran whichever branch the main landed in; each directory holds record/weights/attempt(published)/power-gate(AC Power, window, checked before attempt)"
    status: verified
    evidence: "Records show orbit/seed/variant as registered; attempts published with started 18:12:51 / 18:51:17 / 19:30:40 UTC (sequential, non-overlapping) and ended walls 1957/1734/2034 s; receipts AC Power isoweekday 7, checked_utc 18:12:49 / 18:51:15 / 19:30:38 (before each attempt start); record_sha256 of each attempt equals the record bytes."
  - id: P4-T2
    truth: "66-04: each record verifies against its registration (VERIFY-RESULT-OK) and passes check-run (EXP01-CHECK-OK); frozen FEAS-01 score with tier/E, constant and two-Kepler rows, input+h1 similarity at cadence, Stage-0 TRAIN-only access"
    status: verified
    evidence: "Re-run live by this verification: VERIFY-RESULT-OK and EXP01-CHECK-OK (empty problem lists) on all three; access blocks show reads train=1 validation=0, test_split_opened=0 on each record."
  - id: P4-T3
    truth: "66-04: each run completed under its registered 3,300-second cap and each record is below 10,485,760 bytes"
    status: verified
    evidence: "Walls 1957/1734/2034 s < 3300 s; record sizes 1,250,910 / 1,251,193 / 1,251,013 bytes."
  - id: P4-T4
    truth: "66-04: evidence order — each registration's introducing commit is an ancestor of the commit that adds its record"
    status: verified
    evidence: "3f4d0a85 is an ancestor of a546016b, 3dc3646a and 277c25ce (git merge-base --is-ancestor)."
  - id: P4-T5
    truth: "66-04: resumability/run-state — no incomplete attempts, no retries needed, no overlap; a published attempt is verified and committed, never relaunched"
    status: verified
    evidence: "All three attempts published on first launch; no <role>-retry1 directories or registrations exist; commits are sequential and non-overlapping."
  - id: P5-T1
    truth: "66-05: 66-RESULT.md reports per run the tier, E beside the record's own E_const and band edges, two-Kepler E, eps_h with the GAP-59-08 sentence, input and h1 similarity traces at cadence, and the improvement check beside the label; every value from diagnostic_phase66 output; loss context only"
    status: verified
    evidence: "RESULT-PAGE-OK reproduced; every headline number re-derived by this verification from the committed records (E, E_const, two-Kepler, tier, 14-entry cadence, input+h1 rows, final step 465000, settled improvement check) — all match exactly; the GAP-59-08 sentence is present verbatim; loss appears only as context."
  - id: P5-T2
    truth: "66-05: 66-RESULT.md states each run's label, the confirmation, the route, the pre-registered plain-language reading, and the SCOPE-49 proposal (none for confirmed tier1)"
    status: verified
    evidence: "Review output EXP01-REVIEW confirmation=confirmed route=phase67-as-planned equals the page's confirmation/route lines; the tier1 reading and the 'no plan change is proposed' SCOPE-49 section are on the page."
  - id: P5-T3
    truth: "66-05: owner checkpoint 1 was one blocking-human decision, never auto-selected, presented only after 66-RESULT.md was committed"
    status: verified
    evidence: "Commit order: result 89045a7f (14:24:14-06:00) precedes ruling e40ebca2 (14:38:56-06:00); the ruling page records the protocol (presented after the result was committed; one message; answered same day). The chat presentation itself is a human-domain fact attested by the ratified ruling record."
  - id: P5-T4
    truth: "66-05: 66-CHECKPOINT-1-RULING.md holds every owner message verbatim in one owner-quote block, the recorded answer restating only the chosen option, the SHA-256 of 66-RESULT.md, and who applies any accepted change; no roadmap/requirement/spec/registration edited"
    status: verified
    evidence: "RULING-OK reproduced (status ratified, four sections, non-empty owner-quote block, cited digest present, well-formed CP1-EXP01 accept row); the cited RESULT digest bf143995410ae48a57845b5cf7f5500dc059c4fd0af96486a1b43801b88d26a9 equals both the 89045a7f blob and the current committed file; acceptance diff vs 2b5d0df7 is empty for ROADMAP/REQUIREMENTS/pinn/tests."
  - id: P5-T5
    truth: "66-05 (VERD-01 readiness): every number in 66-RESULT.md cites a committed record by path and SHA-256, and the page lists the machine hours used"
    status: verified
    evidence: "All 22 evidence-index SHA-256 digests re-checked against the committed files — all match; the page states 5,750 s = 1.5972222 h (about 1.60 machine-hours) from the four attempts' timestamps."
prohibitions:
  - statement: "66-03: MUST NOT run the timing calibration other than through the AC-power launch gate in the owner's weekend AC window, and MUST NOT work around a battery refusal (D-08)"
    status: resolved
    verification: judgment
    evidence: "The timing receipt records AC Power, isoweekday 7 (Sunday), checked_utc before the attempt; check-run re-verifies the receipt mechanically; the gate refusals are enforced in code and pinned by the test_power matrix. Non-authoritative LLM-judge verdict; the receipt evidence is mechanical."
  - statement: "66-04: MUST NOT launch any EXP-01 run other than through the AC-power launch gate in the owner's weekend window, and MUST NOT work around a battery refusal or an incomplete attempt by any route the page does not pre-register (D-07, D-08)"
    status: resolved
    verification: judgment
    evidence: "All three run receipts record AC Power on Sunday inside the window and precede their attempts; no retry directories or re-sized registrations exist; attempts sequential and non-overlapping. Non-authoritative LLM-judge verdict with mechanical receipt evidence."
  - statement: "66-05: MUST NOT report EXP-01 beyond its pre-registered label; tier1 reported only as refuting 'too small' for one orbit and showing the data-to-scorer path can produce a passing fit; the probe's lead stays an association (D-02, D-07, D-09; checker blocker 1)"
    status: resolved
    verification: judgment
    evidence: "66-RESULT.md reports exactly the owner-registered tier1 wording and carries the 'What this result does not say' limits section; the identifiability limit is stated; the review tool (not narration) produced the labels. This is the exact page the owner reviewed and accepted at checkpoint 1 — the human resolution exists."
  - statement: "66-05: MUST NOT write, infer or auto-approve the owner's checkpoint 1 answer; the ruling holds only the owner's own words; no plan change applied inside this plan (D-01, D-12)"
    status: resolved
    verification: judgment
    evidence: "The ruling holds one owner-quote block with a single verbatim message and restates only the chosen option; the plan edited no roadmap/requirement/spec/registration (acceptance diff empty). Authenticity of the verbatim quote is a human-domain fact attested by the ratified ruling record."
---

# Phase 66: Small-Network Control — Verification Report

**Phase Goal:** The project knows whether a network smaller than the locked one can fit one Stage-0 orbit, which settles whether "too small" can explain v2.4's failure.
**Verified:** 2026-11-01T21:27:15Z
**Status:** passed
**Re-verification:** No — initial verification

## Goal Achievement

The phase goal is achieved and mechanically evidenced. A network one-fifth the
size of the locked one (157,065 parameters, 1 hidden layer vs 795,657, 12
layers) fits orbit 1632 from time alone: the three pre-registered runs all
landed Tier 1 (E 0.0114 / 0.0172 / 0.0790 against the 0.1 line, each far below
the constant predictor's 1.1538 / 1.2337 and the two-Kepler 0.9168 / 0.4313),
the branch is confirmed, and the pre-registered route `phase67-as-planned`
answers the roadmap question: "too small" is refuted for one orbit. The owner
accepted the recorded proposal at checkpoint ① and the ruling is committed.

### Observable Truths

Full per-item evidence is in the frontmatter `must_haves` checklist above.
Summary:

| # | Truth group | Status | Evidence |
|---|---|---|---|
| 1 | Roadmap SC-1 (prediction page before first run) | ✓ VERIFIED | ORDER-OK ancestry chain; pages byte-tied to `exp01_design()`; live budget reproduction |
| 2 | Roadmap SC-2 (result scored; repeats confirm) | ✓ VERIFIED | verify-result + check-run re-run live on all three committed records; review reproduces confirmed/phase67-as-planned |
| 3 | Roadmap SC-3 (review recorded; owner answer) | ✓ VERIFIED | 66-RESULT.md + 66-CHECKPOINT-1-RULING.md; RESULT-PAGE-OK and RULING-OK reproduce |
| 4 | 66-01 truths T1–T6 (harness, admission door, sealed catalog, Phase 65 intact, stride, AC gate) | ✓ VERIFIED (6/6) | 99 phase66 tests OK; 204 phase65 tests OK; digests match; live check-registration OK |
| 5 | 66-02 truths T1–T9 (gate matrix, concurrency, reading rule, improvement check, bandwidth check, readers, check-run blindness, budget, freeze) | ✓ VERIFIED (9/9) | Tests + live CLI reproductions + freeze verified by git log and digests |
| 6 | 66-03 truths T1–T6 (timing page, blocker-1 wording, timing run, prediction page, registrations, evidence order) | ✓ VERIFIED (6/6) | Ancestry ORDER-OK; check-registration/check-run/verify-result reproduce |
| 7 | 66-04 truths T1–T5 (three runs, verification, caps/sizes, order, run-state) | ✓ VERIFIED (5/5) | Record/receipt/attempt fields re-extracted; sizes and walls under limits |
| 8 | 66-05 truths T1–T5 (result page, labels/route, checkpoint protocol, ruling page, VERD-01 readiness) | ✓ VERIFIED (5/5) | RESULT-PAGE-OK, RULING-OK, 22/22 digest cross-check, all headline numbers re-derived from records |

**Score:** 37/37 truths verified (0 present, behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `pinn/verification/diagnostic_phase66.py` | EXP01_VARIANT, PHASE66_REGISTRY, REGISTRIES, NEAR_BAND, classify_exp01, tier1_e_max, improvement_check, exp01_budget, exp01_design, readers, read-run/check-run/review/budget/design CLI | ✓ VERIFIED | All symbols present; substantive (43.5 KB); wired (imported by diagnostic_fit and the tests); frozen at cb0577fe… |
| `pinn/verification/diagnostic_power.py` | fail-closed AC gate, weekend window, exclusive receipt, caffeinate launch, check subcommand | ✓ VERIFIED | All symbols present; wired into every real launch (4 receipts on disk); frozen at 7e2f00e2… |
| `pinn/verification/diagnostic_fit.py` | registry-door extension (_named_registry, variant_registry, record fields, verify check, Site F stride) | ✓ VERIFIED | Six-site extension present; exercised by all four registrations; frozen at 4884a1a5… |
| `.planning/phases/66-small-network-control/66-TIMING-PREDICTION.md` | frozen design, committed before any run | ✓ VERIFIED | Commit 4eab280b; design block equals exp01_design(); digest matches evidence index |
| `.planning/phases/66-small-network-control/66-PREDICTION.md` | full prediction page with measured budget | ✓ VERIFIED | Commit 3f4d0a85; budget matches live EXP01-BUDGET; digest matches evidence index |
| `evidence/timing/timing-registration.json`, `evidence/timing/1632-s42/{record,diagnostic.weights,attempt,power-gate}` | timing calibration evidence | ✓ VERIFIED | check-registration/check-run/verify-result reproduce; score never read |
| `evidence/exp01/{main-1632-s42,repeat-851-s42,repeat-1632-s41}-registration.json` | three admitting registrations | ✓ VERIFIED | CHECK-REGISTRATION-OK on each; digests match |
| `evidence/exp01/<role>/{record.json,diagnostic.weights,attempt.json,power-gate.json}` ×3 | three complete run records | ✓ VERIFIED | status complete, 465000 steps, published attempts, AC receipts, all checks reproduce |
| `.planning/phases/66-small-network-control/66-RESULT.md` | result page | ✓ VERIFIED | RESULT-PAGE-OK; 22/22 digests; numbers re-derived |
| `.planning/phases/66-small-network-control/66-CHECKPOINT-1-RULING.md` | ratified owner ruling | ✓ VERIFIED | RULING-OK; verbatim owner-quote; cited digest equals the reviewed page |
| `tests/phase66/` (11 files) | contract suites | ✓ VERIFIED | 99 tests OK live |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| diagnostic_fit.py | diagnostic_phase66.py | REGISTRIES import; registry-aware admission lookup | ✓ WIRED | `from pinn.verification.diagnostic_phase66 import REGISTRIES` at line 81; `_named_registry` resolves before data access |
| diagnostic_phase66.py | diagnostic_variants.py | PHASE66_REGISTRY = register_variant(EXP01_VARIANT, into=REGISTRY) | ✓ WIRED | Line 95; sealed catalog unaltered (catalog test) |
| diagnostic_power.py | diagnostic_fit.py | launch composes `caffeinate -is <python> -B -m pinn.verification.diagnostic_fit run` | ✓ WIRED | Four real launches produced receipts + records through this path |
| diagnostic_phase66.py | artifacts/feasibility_scorecard_v1.json | tier1_e_max(load_scorecard()) — never a retyped 0.1 | ✓ WIRED | Reading-rule tests pin it; E 0.0114/0.0172/0.0790 all read Tier 1 |
| each record | its registration | record.registration.sha256; verify-result re-admits committed registration | ✓ WIRED | b0d79585… / 40754fb9… / 48a15ad6… all re-verified live |
| each receipt | its attempt | checked_utc precedes started_utc; check-run enforces | ✓ WIRED | 18:12:49<18:12:51, 18:51:15<18:51:17, 19:30:38<19:30:40 |
| each registration | 66-PREDICTION.md | page.sha256 pinned; admission re-checks page bytes | ✓ WIRED | check-registration OK; page digest 7ec16fe9… matches |
| 66-RESULT.md | three records | every number cited by path + SHA-256 | ✓ WIRED | 22/22 digests match committed bytes |
| 66-CHECKPOINT-1-RULING.md | 66-RESULT.md | cited SHA-256 of the reviewed page | ✓ WIRED | bf143995… equals both the 89045a7f blob and the current file |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|---|---|---|---|---|
| run records | scores.network.E / tier | frozen FEAS-01 scorer over the trained network, at run time | Yes (trained MPS runs, 465k steps each) | ✓ FLOWING |
| run records | comparisons window_mean_constant / two_kepler | frozen scorer over each record's own window | Yes | ✓ FLOWING |
| run records | similarity.entries (input, h1) | DIAG-09 logger at the registered 14-step cadence | Yes | ✓ FLOWING |
| 66-RESULT.md | every reported number | diagnostic_phase66 review/read-run output over committed records | Yes | ✓ FLOWING |
| 66-PREDICTION.md | budget N=465000 | exp01_budget over the committed timing record | Yes | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Record verifies against registration (×3) | `diagnostic_fit verify-result …` | VERIFY-RESULT-OK, exit 0, ×3 | ✓ PASS |
| Directory audit score-blind (×3 + timing) | `diagnostic_phase66 check-run --dir …` | EXP01-CHECK-OK, empty problems, no score printed | ✓ PASS |
| Three-run branch derivation | `diagnostic_phase66 review --main … --repeat-system … --repeat-seed …` | EXP01-REVIEW confirmation=confirmed route=phase67-as-planned, all tier1 | ✓ PASS |
| Budget from measured rate | `diagnostic_phase66 budget --timing-dir …` | EXP01-BUDGET steps=465000 loss_trace_stride=47 cap=3300.0 | ✓ PASS |
| Registration admission (×4) | `diagnostic_fit check-registration …` | CHECK-REGISTRATION-OK each | ✓ PASS |
| Phase 66 suite | `unittest discover -s tests/phase66 -t .` | 99 tests, OK (16.8 s) | ✓ PASS |
| Phase 65 suite | `unittest discover -s tests/phase65 -t .` | 204 tests, OK (36.9 s) | ✓ PASS |
| Plan-05 page check | RESULT-PAGE-OK command from 66-05-PLAN.md | RESULT-PAGE-OK confirmed phase67-as-planned | ✓ PASS |
| Plan-05 ruling check | RULING-OK command from 66-05-PLAN.md | RULING-OK | ✓ PASS |
| Design-block round trip | exp01_design() vs both pages' fenced blocks | byte-equal on both pages | ✓ PASS |
| Evidence-index digests | sha256 of all 22 cited files | all match the page's digests | ✓ PASS |
| Numbers vs records | re-derive E/E_const/two-Kepler/tier/cadence/settled from record.json | all match exactly on all three runs | ✓ PASS |

### Probe Execution

Not applicable — this phase's probes are the harness's own verify/check/review
CLIs, all run above (Behavioral Spot-Checks). No `scripts/*/tests/probe-*.sh`
exist for this phase.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|---|---|---|---|---|
| EXP-01 | 66-01..66-05 (all declare `[EXP-01]`) | The small-network control (tests "too small"): fewer parameters and fewer layers than the locked network fits orbit 1632 from time alone; architecture fixed on the prediction page | ✓ SATISFIED | Fit achieved and confirmed (Tier 1 ×3; E 0.0114/0.0172/0.0790); architecture pinned on the committed prediction page (157,065 params, 1 hidden layer); the pre-registered Tier-1 branch reading matches the recorded route. REQUIREMENTS.md row still "Pending" — deliberately left to the orchestrator's phase.complete step (see frontmatter note). Not a gap. |

No orphaned requirements: line 244 of REQUIREMENTS.md is the only Phase 66
mapping, and every plan declares exactly EXP-01.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| (none in phase 66 files) | — | No TBD/FIXME/XXX/TODO/HACK/PLACEHOLDER markers; no stub returns; no placeholder data; no retry/gap residue | — | — |

Known-accepted debt (documented, not phase-66 gaps): `66-REVIEW.md` records
2 critical (CR-01 foreign-orbit cross-check skip, CR-02 malformed-evidence
crash paths), 4 warning and 4 info findings in the frozen reading-rule
readers. The harness is frozen at 734cb7da by directive; the review is
advisory and records the findings for owner triage. Verified documented as
required; not verified fixed (per the task constraint, and per the review's
own boundary statement).

Pre-existing unrelated failures (not phase-66 gaps, per the task constraints):
tests/phase55 and tests/phase56 fail on a missing pytest module in the
environment; tests/phase64 has 4 failures from its own fail-closed guard
tripping on pinn/evaluate.py changed by phase 65 (commit 14529e8a). Not
encountered in this verification's runs (only phase65/phase66 discoveries
were run); documented here for the record.

### Human Verification Required

None outstanding for this phase. The phase's designed human decision — owner
checkpoint ① — was presented after the result page was committed and answered
("Accept the recorded proposal"), and is recorded verbatim in the ratified
66-CHECKPOINT-1-RULING.md, which cites the exact reviewed page by SHA-256.

### Gaps Summary

No gaps. All 37 must-haves (34 plan truths + 3 roadmap success criteria)
verified against the codebase and committed evidence with live re-runs under
the pinned interpreter; the EXP-01 requirement is satisfied per the
pre-registered Tier-1 branch reading; the harness freeze held (no change to
the three modules after 734cb7da; all seven digests match); the Phase 65
directory is untouched since c919194d; pre-registration order is proven by
git ancestry; and both test discoveries are green (99 + 204).

---

_Verified: 2026-11-01T21:27:15Z_
_Verifier: Claude (gsd-verifier)_
