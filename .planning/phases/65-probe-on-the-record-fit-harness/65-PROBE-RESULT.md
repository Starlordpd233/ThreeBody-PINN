# Phase 65 Probe Result: the 2026-10-27 lead, reproduced on the record

**Status:** registered reading-rule verdict **`retained`** — every required
historical figure reproduced exactly, so the exploratory association stays on
record. No SCOPE-49 pivot is proposed; no roadmap, framework-spec, pass-bar or
later-experiment change is made or asked for. Result of record:
`evidence/probe/reproduction.json` (verified by `verify-result`,
`VERIFY-RESULT-OK`, exit 0).

## What ran

One registered run of the read-only DIAG-09 probe (plan 65-05, Task 65-05-01)
at run commit `22cee7d2` under the committed registration
(`f469e003`; expectations SHA-256 `4f8cd085…a2cb`). The runner re-checked the
committed-clean gate itself before any data or weight access, verified every
weight SHA-256 before `torch.load` (`weights_only=True`, CPU map location),
reconstructed each arm's architecture/frequency at CPU float64 seed 42, and
loaded each committed trained state only after its record and digest agreed.
Zero optimizer steps (interlock `attempted_steps: 0`); model parameter digests
matched before/after every one of the 15 measurements. All seven arms' Stage-0
training orbits were read through the guarded seam — `hierarchical/gold/1632`,
`/4658`, `/851`, split `train`, orbit stage 0, 1,001 samples, window [0, 10] —
and nothing else. No test-split or validation file was opened; the preserved
held-out evaluation stays unspent. The historical scripts were never executed.

## The original tokens, and what became of them

The preserved tokens are the 2026-10-27 all-arm table
(`toolu_01NHGWRv6pEQCJmqeAXxqonK`) and single-arm r1-1632 output
(`toolu_01PUFNWxrDDsVrU8DTCH4tX3`), byte-preserved in `evidence/original/` and
registered field-by-field with exact formatter rounding cells in
`evidence/probe/expectations.json`. Reproduction is exact formatter equality
under the original `.2f`/`.3f`/`.4f`/`.3g` formatters — never a widened
tolerance.

**144 of 144 required fields reproduced; 0 not_reproduced.** By group:

| Group | Measured | Reproduced | Not reproduced |
|---|---|---|---|
| All-arm rows, 7 arms × init + selected state (r1-1632's init row carries its 19 historical per-layer fields) | 110 | 110 | 0 |
| r1-1632 Adam/polish supplement, measured fields (frequency, adj-cos per layer, movement, rate) | 34 | 34 | 0 |
| **Required total** | **144** | **144** | **0** |

The all-arm token rows, all reproduced (cyc = first-layer frequency median;
h1/h2 = centred neighbour cosine after hidden layers 1/2; range = min/max over
h3..h12; move = output movement; rate = the labelled comparator):

| Arm | State | cyc | h1 | h2 | range | move | rate |
|---|---|---|---|---|---|---|---|
| g2s-1632-w060 | init | 0.78 | 1.000 | 1.000 | [0.751, 1.000] | 2.7741 | 195 |
| g2s-1632-w060 | adam | 7.75 | 0.938 | 0.017 | [-0.004, 0.003] | 0.0034 | 1.9e+08 |
| g2s-1632-w120 | init | 1.56 | 1.000 | 1.000 | [0.413, 0.999] | 2.8467 | 388 |
| g2s-1632-w120 | adam | 16.80 | 0.772 | -0.004 | [-0.003, 0.004] | 0.0032 | 4.65e+08 |
| g2s-1632-w240 | init | 3.13 | 0.999 | 0.999 | [0.104, 0.996] | 2.8247 | 810 |
| g2s-1632-w240 | adam | 33.53 | 0.479 | -0.000 | [-0.005, 0.004] | 0.0030 | 9.74e+08 |
| g2s-1632-w480 | init | 6.25 | 0.997 | 0.995 | [0.020, 0.987] | 2.8461 | 1.61e+03 |
| g2s-1632-w480 | adam | 66.38 | 0.256 | -0.002 | [-0.005, 0.003] | 0.0030 | 9.67e+08 |
| r1-1632 | init | 0.39 | 1.0000 | 1.0000 | [0.925, 1.000] | 2.8730 | 101 |
| r1-1632 | polish | 4.25 | 0.985 | 0.351 | [-0.004, 0.018] | 0.0034 | 4.97e+07 |
| r1-4658 | init | 0.39 | 1.000 | 1.000 | [0.921, 1.000] | 7.0396 | 51.9 |
| r1-4658 | adam | 5.29 | 0.929 | -0.000 | [-0.004, 0.001] | 0.0030 | 2.19e+09 |
| r1-851 | init | 0.39 | 1.000 | 1.000 | [0.932, 1.000] | 2.3525 | 77.4 |
| r1-851 | adam | 3.98 | 0.981 | 0.201 | [-0.004, 0.004] | 0.0031 | 1.59e+08 |

r1-1632's init row also reproduced its twelve historical per-layer values at
`.4f` (adj_input 1.0000; h1 1.0000; h3 0.9999; … h12 0.9248), and the
supplement reproduced Adam's and polish's per-layer values (h3: adam 0.0186,
polish 0.0177, as printed) — the Adam/polish rows stay distinct from the
all-arm table, and the adam h3 value was never merged into a range token.

## Provenance limitations

**None.** Every registered available historical numeric field had its original
source output, and every one was compared. The reading rule's
provenance-limitation branch stayed empty.

## Preserved-only figures (reported verbatim, never compared)

64 fields — the single-arm `moving`, `spike` and skip/siren columns (32 per
supplement state) — have no shared-measurement definition, and a second
reduction is forbidden (D-05). They are preserved verbatim with their own
formatters in the registration and listed in the result's `not_measured`
record. No result is fabricated for them, in either direction.

## New measurements (raw values the original never printed)

130 per-layer deep-layer entries (`h3..h12` for each all-arm row) are recorded
in `reproduction.json#new_measurements` with raw values and deltas to the
registered range. 120 of them are new measurements per the registered rule
(all arms except r1-1632). The remaining 10 — r1-1632/polish `h3..h12` — carry
raw values whose historical targets exist in the supplement and were separately
compared there (and reproduced); the runner's all-arm row is labelled
`new_measurements: true` and its field set does not see the supplement's
coverage, so these 10 are redundant labels on real measurements, not invented
targets. The verdict is unaffected either way: new measurements never enter
the reading rule. A per-layer example (r1-851/adam/h12): raw 0.00084699,
deltas +0.00485 to the registered deep minimum −0.004 and −0.00315 to the
maximum 0.004.

## What the reproduced numbers say — association only

At the CPU64 seed-42 reconstruction, adjacent-time (0.01 apart) hidden states
are near-perfectly correlated through the network at initialization for the
ω₀ = 30 arms (cosine ≈ 1.000 deep into the network), with the init correlation
floor dropping as `first_omega_0` rises (deep minimum 0.751 at ω₀ 60, 0.020 at
ω₀ 480). After training, the correlation collapses to formatter-zero from
layer 2–3 on on every arm (|cos| ≤ 0.018 tokens), the output's movement
collapses from 2.35–7.04× the orbit's own variation to 0.30–0.35% of it, and
the labelled output-rate comparator rises from 51.9–1.61e+03 to
4.97e+07–2.19e+09. These are the same figures the 2026-10-27 exploration
printed; this run reproduces them exactly.

This is a **measured association, on the record as a reproduction of
already-seen exploratory results** — it is not an independent prospective
discovery (the chronology of D-02 is preserved), and it does not establish
information loss, a capacity limit, or the cause of the v2.4 failure (D-07).
Those questions belong to Phases 66–67's experiments and the Phase 69
findings page, under their own prediction pages.

## Labels that travel with these numbers

- **Reconstruction, not history:** the rerun's initialization is CPU float64,
  seed 42 — a reconstruction of the original probe's initialization, not the
  historical MPS float32 training initialization (D-04). A matching seed does
  not establish identical initial weights across runtimes. Trained states are
  the committed Phase 60 weights, digest-verified before load.
- **The rate comparator:** the `rate` column is the RMS of the network's
  autograd d/dτ over the RMS of `torch.gradient` of the gold targets in the
  same normalized τ coordinate — a labelled comparator, not a physical
  velocity claim. Adjacent gold samples are physically 0.01 apart; that says
  nothing about normalized-τ spacing (D-05).

## Logger parity (INST-08(c))

The actual fit logger entry, `diagnostic_fit.log_similarity`, ran on the
registered r1-1632 polish state inside the same registered run — same
admission/hash/data gates, same weights, same sample coordinates, CPU64, no
updates (`step: -1`, point `probe-logger-parity`) — and its receipt is
materialized at `evidence/probe/logger-parity.json` and cross-checked by
`verify-result` against the run's recorded entry: exact agreement, all 13
measured layers. The shared logger and the probe use the one
`measure_time_signal` implementation (D-05), so the logger's DIAG-09 value is
the probe's value by construction and now by receipt. No fit ran in this plan;
a logger mismatch would have blocked acceptance of its training trace rather
than being relabelled agreement.

## Run defects found after the measurements (routed, not repaired here)

The runner's measurement, comparison, reading-rule and interlock paths worked
exactly as registered. Two post-measurement defects in the 65-04 runner
surfaced, and one plan/CLI mismatch; none touches the result's content, and
the immutable reading rule was never edited:

1. `_render_stdout` crashed (`KeyError: 'measured'`) rendering
   `preserved_only` verdicts, after `reproduction.json` was fully written and
   fsynced. `reproduction.stdout.txt` was therefore regenerated from the
   committed result bytes by this plan's executor with the preserved-only
   branch corrected; the file carries its own provenance header and is not
   runner output. The first result is the result — no re-run, no retry.
2. `reading_rule.new_measurements` in the result scans the field-verdict list,
   which never carries `new_measurement` statuses; the real entries live in
   `reproduction.json#new_measurements` (130, counted above). Reporting-only.
3. The plan's Task 2 names a standalone `logger-parity` CLI subcommand; the
   shipped runner performs the parity call inside `run` and exposes
   `--logger-parity` on `verify-result` (the shape its own tests pin). The
   receipt above is the run's actual logger call, materialized in the
   test-sanctioned file shape.

These belong to `pinn/verification/diagnostic_probe.py`, whose bytes are
digest-pinned by the committed registration — any edit changes what that
registration admits and is therefore not taken inside this plan. They are
handed to the orchestrator/owner to route (a small remediation with a
registration-digest decision), alongside the suite gap that no phase65 test
renders the stdout file with preserved-only fields present.

## Branch and routing

- **Registered branch: on-record (`retained`).** `scope49_proposal: false`.
- No owner decision is requested by this result. The Phase 66–67 experiments
  run under their own prediction pages; the yardstick and findings decisions
  remain Phases 68–69's.
- Prohibitions honored: no causal claim, no independent-discovery framing, no
  tolerance widened, no rule edited, no ROADMAP/spec/pass-bar change, no
  later-experiment choice made here.
