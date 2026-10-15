## In plain language

This census counts inner laps for the 1,812 Stage-0 training systems and checks that the reader agrees with the gold sibling.
The median system completes 18.6086833245 inner laps by t = 10. The 10th percentile completes 10.4734179666 and the 90th completes 39.3491865301.
The phase-accuracy figure is how precisely a network must time those laps. For a 10% end-point miss the median figure is 0.000855272485007, about 1 part in 1169. For a 1% miss it is 8.55272485007e-05, about 1 part in 11692.
On the base grid, 28 training systems have fewer than 2 samples per inner period, 148 have fewer than 3, and 545 have fewer than 5.
The three single systems are the eligible systems nearest the 10th, 50th and 90th percentiles of N_in: id 1632 (N_in 10.4719940611, 11.9365995885 base samples per inner period), id 851 (N_in 18.6120483887, 6.71607968072 base samples per inner period), id 4658 (N_in 39.3492273866, 3.17668244847 base samples per inner period). A system is eligible only when the base grid has at least 3 samples per inner period. An equal distance picks the lower id.
The 16-system family takes one system from each bin of the census sorted by inner laps, so the family spans the census. The validation panel is all 227 Stage-0 validation systems, and those systems were not given difficulty numbers. No test-split file was opened.

## Numbers

- Training systems: 1812
- Validation systems: 227
- Pair-tracking failures: 0
- Gold-base max deviation: 9.68478155394e-07
- Largest inner unwrap step: 3.07334010207
- Base cross-check flags: 18
