# What v2.5 established

The architecture used in v2.4 fitted the tested orbit positions under a
different training recipe. The historical cause remains open. Each successful
fit used the answer for one orbit. Learning from physics, performance across
Stage 0 and accuracy on unseen initial conditions remain open.
[Matched records and limits](69-EVIDENCE.md#historical-failures-and-successful-locked-controls)

| Suspect or lead | Status within the tested scope | Observation and supporting detail |
|---|---|---|
| Too few parameters | Refuted for supervised fitting of the tested single orbits | A smaller network reached Tier 1 on 1632/42, 851/42 and 1632/41. Depth, width and first frequency changed together. [EXP-01](69-EVIDENCE.md#exp-01-small-network-control). |
| An overly harsh yardstick | Measurement defect confirmed; achievable neural-network bars open | Finite differences can reject the known answer. A constant predictor conserves its own energy while failing position accuracy. Neither finding explains a data-only fit learning mean positions. [YARD-01 through YARD-03](69-EVIDENCE.md#yardstick-and-current-owner-ruling). |
| Pipeline, training settings | Rate sensitivity confirmed. Historical cause open. | EXP-03's constant 1e-3 arm had worse position error than 1e-4 in all three cases. The other rate contrasts were unsettled or ambiguous. [EXP-03](69-EVIDENCE.md#exp-03-learning-rate-ladder) |
| Pipeline, physics terms | Open | These supervised, data-only experiments do not test learning from physics. The four named production defects remain v2.6 obligations. [Scope and obligations](69-CHECKPOINT.md#obligations-carried-to-v26). |
| Original adjacent-time hidden-state lead | Association reproduced; causal meaning open | DIAG-09 retained 144/144 required comparisons on the seven historical networks. This does not establish information loss or a failure mechanism. [DIAG-09](69-EVIDENCE.md#diag-09-original-probe-lead). |

The successful locked controls reached settled Tier 1 position scores of
`E = 0.041` on system 1632 with seed 42, `0.095` on 851 with seed 42 and
`0.035` on 1632 with seed 41. The historical matches for the two seed-42
runs were Tier 0 at `1.157` and `1.238`. Lower `E` means less position error.
The old recipe used cosine Adam starting at 1e-3, clipping and diagnostic
polish. The successful controls used constant Adam 1e-4 without clipping or
polish, with different update budgets and scored-state selection. Construction,
targets and loss agree; archived initial-tensor and exact runtime identity
remain unproved. This is a retrospective comparison of recipes, with several
settings changed together. [Exact scores and recipe comparison](69-EVIDENCE.md#recipe-comparability)

All depth, time-input and window contrasts were unsettled. The shorter windows
gave lower error in all nine comparisons, with endpoints still improving in
some cases. [Predictions, scores and replication limits](69-EVIDENCE.md#exp-05-window-length-ladder)

The measured subtotal was **29.90 hours** across 129 published attempts and
one yardstick capture. Probe, refusal and broader development and operator time
remain unknown. [Accounting and SCOPE-49 dispositions](69-ACCOUNTING.md)

The recommended v2.6 direction keeps the current model as the supervised fit
control and prioritizes the training recipe and physics pipeline. Another
diagnostic before closure would have to change that choice to justify its cost.
C-7 A routes the autograd measurement changes to v2.6. C-2, C-4, C-5 and C-6
remain open. The owner’s direction and trainex-r5 decision are pending.
[Decision packet](69-CHECKPOINT.md)

Exact source paths, revisions and SHA-256 values are in the inventory committed
at `0f53ab64061a1998e2df2a082149f087ee6c4b03`. [Checked inventory](evidence/69-evidence.json)
