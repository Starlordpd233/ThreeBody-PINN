## In plain language

This survey reads all 12023 training-split records and asks how hard each stage is: how fast the inner pair spins, how close bodies come, how violent the accelerations are, and how quickly a small error grows (the Lyapunov time, tau_L). Every stage label and every tau_L value here is diagnostic. The official stage mapping beyond Stages 0 and 1 is owner-pending, and nothing in this survey gates a result.

Stage 0 has 1812 records with a median of 18.61 inner laps by t = 10 (10th to 90th percentile 10.47 to 39.35); a median closest approach of 0.03929 (smallest 0.005466); a median peak acceleration of 582.4; a median tau_L of 21.41 over 1495 finite readings (317 infinite, 0 not computable), so a small starting error grows by about 1.22 by t = 10.

Stage 1 has 2074 records with a median of 25.02 inner laps by t = 10 (10th to 90th percentile 13.71 to 56.15); a median closest approach of 0.03801 (smallest 0.008621); a median peak acceleration of 787.4; a median tau_L of 24.64 over 1660 finite readings (414 infinite, 0 not computable), so a small starting error grows by about 1.102 by t = 10.

Stage 2 has 3886 records with a median of 21.53 inner laps by t = 10 (10th to 90th percentile 11.86 to 48.51); a median closest approach of 0.03859 (smallest 0.003302); a median peak acceleration of 685.9; a median tau_L of 21.25 over 3125 finite readings (761 infinite, 0 not computable), so a small starting error grows by about 1.151 by t = 10.

Stage 4a has 1404 records with no inner-lap count (no hierarchical split); a median closest approach of 0.01594 (smallest 0.001748); a median peak acceleration of 3966; a median tau_L of 10.74 over 655 finite readings (749 infinite, 0 not computable), so a small starting error grows by about 1 by t = 10.

Stage 4b has 654 records with no inner-lap count (no hierarchical split); a median closest approach of 0.01701 (smallest 0.002139); a median peak acceleration of 3504; a median tau_L of 2.984 over 654 finite readings (0 infinite, 0 not computable), so a small starting error grows by about 28.53 by t = 10.

Stage 5 has 1923 records with no inner-lap count (no hierarchical split); a median closest approach of 0.005793 (smallest 0.0002672); a median peak acceleration of 2.98e+04; a median tau_L of 5.02 over 1225 finite readings (698 infinite, 0 not computable), so a small starting error grows by about 2.144 by t = 10.

Stage 6 has 269 records with no inner-lap count (no hierarchical split); a median closest approach of 0.007083 (smallest 0.0007175); a median peak acceleration of 1.993e+04; a median tau_L of 1.706 over 269 finite readings (0 infinite, 0 not computable), so a small starting error grows by about 351.6 by t = 10.

1 records are unlabelled because tau_L could not be computed for them.

Stage 3 is empty. It needs a virial ratio between 0.9 and 1.1, and the standard base records span only 0.0006319 to 0.1192.

By N_in (larger is harder) the stages rank 1, 2, 0 from hardest to easiest; the Spearman rank correlation with the curriculum order is 0.5 over 3 stages.

By acc_max (larger is harder) the stages rank 5, 6, 4a, 4b, 1, 2, 0 from hardest to easiest; the Spearman rank correlation with the curriculum order is 0.8929 over 7 stages.

By closest_approach (smaller is harder) the stages rank 5, 6, 4a, 4b, 1, 2, 0 from hardest to easiest; the Spearman rank correlation with the curriculum order is 0.8929 over 7 stages.

By tau_L_primary (smaller is harder) the stages rank 6, 4b, 5, 4a, 2, 0, 1 from hardest to easiest; the Spearman rank correlation with the curriculum order is 0.9286 over 7 stages.

By error_growth (larger is harder) the stages rank 6, 4b, 5, 0, 2, 1, 4a from hardest to easiest; the Spearman rank correlation with the curriculum order is 0.6429 over 7 stages.

By phase_accuracy_0.1 (smaller is harder) the stages rank 1, 2, 0 from hardest to easiest; the Spearman rank correlation with the curriculum order is 0.5 over 3 stages.

The Stage 4b probe system is standard/base/2279 with value 2.984 against a stage median of 2.984 over 654 candidates; under the sensitivity fit windows it is 1 time unit(s): standard/base/1916 (differs); 2 time unit(s): standard/base/281 (differs); 3 time unit(s): standard/base/73 (differs).
The Stage 6 probe system is standard/base/3418 with value 0.2657 against a stage median of 0.2657 over 269 candidates; under the sensitivity fit windows it is 1 time unit(s): standard/base/512 (differs); 2 time unit(s): standard/base/1074 (differs); 3 time unit(s): standard/base/509 (differs).

Reminder: the labels and tau_L are diagnostic, the official mapping is owner-pending, and these picks are the pre-declared rule's output, not a judgment about which system is most informative.

## Numbers

- Records surveyed: 12023
- Stage 3 records: 0
- Unlabelled records: 1
