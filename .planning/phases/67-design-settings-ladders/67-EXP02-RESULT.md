# EXP-02 depth ladder — Result

The complete reviewed outcome of the 15 pre-registered EXP-02 science rows,
written only after every row was launched once, mechanically checked (each
PHASE67-ROW-OK, scores hidden during the run loop) and committed serially.
The committed machine review `evidence/exp02/review.json` (schema
`phase67-review/v1`) is the generated record and remains unchanged beside
this page; every numerical claim below is machine-copied from the committed
row evidence and cites its source.

## Setting and budget

- Common N = 152900 optimizer steps (warmup 200, measured 152700) at the
  frozen cadences — similarity events 0/38225/76450/114675/152900, score
  events 76450/114675/152900, loss-trace stride 153 — whole-launch cap
  3540 s, per the committed budget `evidence/exp02/budget.json` (652d1a9d).
- Arms: depths 2/4/6/8/12 with the locked layer types, width 256, first
  omega 30, hidden omega 1, raw 14-dim `[tau, IC13]` input, rate 1e-4,
  physical window [0,10]. Phase 66 EXP-01's width 384 and first omega 1000
  belong only to the positive control and were not imported (D-02/D-03).
- Parameter counts (the D-03 confound — the size change that accompanies
  depth is recorded, not controlled away): d2 137,737 / d4 269,321 /
  d6 400,905 / d8 532,489 / d12 795,657.
- Cases: main-1632-s42 (hierarchical/gold/1632, seed 42), repeat-851-s42
  (hierarchical/gold/851, seed 42), repeat-1632-s41 (hierarchical/gold/1632,
  seed 41). All three carry the committed same-window metadata and baselines.
- Execution: 15 serial launches in the declared case-major order between
  2026-11-03 20:45:54 and 2026-11-04 02:38:44 CST, each exactly once through
  diagnostic_power and the outer supervisor, every admission POWER-OK
  source=AC Power isoweekday=2 (receipt committed per row), zero retries,
  zero refusals, zero reused directories, TRAIN-only access attestations in
  every record, every attempt status=published. One commit per complete row
  before the next launch; hashes cited per row below.

## Endpoint outcomes (E, frozen tier, endpoint status)

E is the frozen scorecard's position-error score (GAP-59-08: no energy bar
or scorer definition is adjudicated here). Endpoint status applies the
registered final-quarter rule: a relative E improvement over the last
quarter strictly greater than 5% leaves the endpoint unsettled; no branch
extends, retries or re-sizes any run (no-continuation policy).

### Case main-1632-s42

| arm | params | E | tier | endpoint | rel. E vs d12 | wall s | ms/step | proj s | row commit |
|---|---|---|---|---|---|---|---|---|---|
| d2 | 137,737 | 0.121581 | 0 | settled | 2.491 | 777.8 | 5.072 | 1073.0 | 09a60d00 |
| d4 | 269,321 | 0.034400 | 1 | settled | 0.012 | 1043.9 | 6.807 | 1358.1 | 9c3aecab |
| d6 | 400,905 | 0.058867 | 1 | settled | 0.690 | 1277.3 | 8.334 | 1680.4 | a04e50fc |
| d8 | 532,489 | 0.033446 | 1 | settled | 0.040 | 1518.1 | 9.906 | 1954.2 | 9b2d7ba2 |
| d12 | 795,657 | 0.034826 | 1 | unsettled | - | 2135.6 | 13.930 | 2558.4 | 9d2957b3 |

Same-window comparison scores (`science/main-1632-s42/d12/record.json`):
window_mean_constant E = 1.153841, two_kepler E = 0.916849.

### Case repeat-851-s42

| arm | params | E | tier | endpoint | rel. E vs d12 | wall s | ms/step | proj s | row commit |
|---|---|---|---|---|---|---|---|---|---|
| d2 | 137,737 | 0.170434 | 0 | unsettled | 1.525 | 743.4 | 4.846 | 854.8 | 6a19af45 |
| d4 | 269,321 | 0.233286 | 0 | settled | 2.457 | 1005.5 | 6.556 | 1270.2 | 6a4c7f2c |
| d6 | 400,905 | 0.017319 | 1 | unsettled | 0.743 | 1229.2 | 8.016 | 1590.1 | 2756362d |
| d8 | 532,489 | 0.022800 | 1 | unsettled | 0.662 | 1481.8 | 9.668 | 1979.7 | eb3b113c |
| d12 | 795,657 | 0.067491 | 1 | unsettled | - | 2018.8 | 13.170 | 2623.7 | 97d52264 |

Same-window comparison scores (`science/repeat-851-s42/d12/record.json`):
window_mean_constant E = 1.233697, two_kepler E = 0.431260.

### Case repeat-1632-s41

| arm | params | E | tier | endpoint | rel. E vs d12 | wall s | ms/step | proj s | row commit |
|---|---|---|---|---|---|---|---|---|---|
| d2 | 137,737 | 0.100486 | 0 | unsettled | 0.243 | 693.6 | 4.526 | 1035.7 | c322c48e |
| d4 | 269,321 | 0.073865 | 1 | settled | 0.086 | 984.4 | 6.422 | 1303.4 | 5d190697 |
| d6 | 400,905 | 0.011827 | 1 | unsettled | 0.854 | 1287.7 | 8.404 | 1592.4 | ffd98e41 |
| d8 | 532,489 | 0.017155 | 1 | settled | 0.788 | 1517.2 | 9.902 | 1938.5 | 4aed8511 |
| d12 | 795,657 | 0.080813 | 1 | settled | - | 2035.7 | 13.284 | 2654.3 | c9b68e6e |

Same-window comparison scores (`science/repeat-1632-s41/d12/record.json`):
window_mean_constant E = 1.153841, two_kepler E = 0.916849.

Measured machine cost: 15 walls totalling 19750.2 s (the budget's measured
projection was 25466.9 s; every row ran inside both its 3540 s cap and its
per-row projection). No failed attempts exist.

## Adjacent-time hidden-state similarity at every cadence point

Centred hidden-state cosine between adjacent cadence events for input and
every hidden layer of each arm (arm rows) and the d12 control of the same
case (control rows), machine-copied from `review.json` -> confirmation ->
contrasts -> descriptive -> adjacent_time_similarity (identical values live
in each row's committed `record.json` similarity block). Per-layer ordering
is preserved across unequal depths (input, h1, ..., hd). This trace is
associated evidence only: no cosine threshold and no causal claim.

### Case main-1632-s42

**d2**

| step | input | h1 | h2 |
|---|---|---|---|
| 0 | 0.999988 | 0.999984 | 0.999970 |
| 38225 | 0.999988 | 0.999978 | 0.999937 |
| 76450 | 0.999988 | 0.999977 | 0.999938 |
| 114675 | 0.999987 | 0.999976 | 0.999937 |
| 152900 | 0.999987 | 0.999976 | 0.999935 |

**d4**

| step | input | h1 | h2 | h3 | h4 |
|---|---|---|---|---|---|
| 0 | 0.999988 | 0.999984 | 0.999970 | 0.999935 | 0.999878 |
| 38225 | 0.999988 | 0.999984 | 0.999972 | 0.999942 | 0.999920 |
| 76450 | 0.999988 | 0.999983 | 0.999971 | 0.999939 | 0.999914 |
| 114675 | 0.999988 | 0.999982 | 0.999970 | 0.999939 | 0.999915 |
| 152900 | 0.999988 | 0.999981 | 0.999969 | 0.999937 | 0.999912 |

**d6**

| step | input | h1 | h2 | h3 | h4 | h5 | h6 |
|---|---|---|---|---|---|---|---|
| 0 | 0.999988 | 0.999984 | 0.999970 | 0.999935 | 0.999878 | 0.999712 | 0.999390 |
| 38225 | 0.999988 | 0.999984 | 0.999973 | 0.999943 | 0.999915 | 0.999812 | 0.999751 |
| 76450 | 0.999988 | 0.999984 | 0.999971 | 0.999937 | 0.999905 | 0.999784 | 0.999678 |
| 114675 | 0.999988 | 0.999983 | 0.999967 | 0.999928 | 0.999882 | 0.999746 | 0.999574 |
| 152900 | 0.999988 | 0.999981 | 0.999963 | 0.999917 | 0.999863 | 0.999700 | 0.999506 |

**d8**

| step | input | h1 | h2 | h3 | h4 | h5 | h6 | h7 | h8 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.999988 | 0.999984 | 0.999970 | 0.999935 | 0.999878 | 0.999712 | 0.999390 | 0.998555 | 0.996966 |
| 38225 | 0.999988 | 0.999983 | 0.999959 | 0.999910 | 0.999815 | 0.999567 | 0.999168 | 0.998147 | 0.996618 |
| 76450 | 0.999988 | 0.999984 | 0.999959 | 0.999909 | 0.999824 | 0.999597 | 0.999248 | 0.998294 | 0.996972 |
| 114675 | 0.999988 | 0.999983 | 0.999959 | 0.999911 | 0.999827 | 0.999609 | 0.999285 | 0.998418 | 0.997558 |
| 152900 | 0.999988 | 0.999983 | 0.999956 | 0.999900 | 0.999800 | 0.999541 | 0.999222 | 0.998302 | 0.997415 |

**d12** (the d12 control run of this case)

| step | input | h1 | h2 | h3 | h4 | h5 | h6 | h7 | h8 | h9 | h10 | h11 | h12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.999988 | 0.999984 | 0.999970 | 0.999935 | 0.999878 | 0.999712 | 0.999390 | 0.998555 | 0.996966 | 0.992760 | 0.984454 | 0.962920 | 0.922495 |
| 38225 | 0.999988 | 0.999983 | 0.999959 | 0.999909 | 0.999797 | 0.999521 | 0.999051 | 0.997784 | 0.995722 | 0.990158 | 0.982359 | 0.961142 | 0.938033 |
| 76450 | 0.999988 | 0.999983 | 0.999957 | 0.999905 | 0.999794 | 0.999527 | 0.998988 | 0.997675 | 0.995697 | 0.990292 | 0.983338 | 0.964181 | 0.950472 |
| 114675 | 0.999988 | 0.999982 | 0.999960 | 0.999911 | 0.999810 | 0.999555 | 0.999131 | 0.997980 | 0.996253 | 0.991743 | 0.986573 | 0.971435 | 0.963687 |
| 152900 | 0.999988 | 0.999982 | 0.999961 | 0.999911 | 0.999815 | 0.999583 | 0.999200 | 0.998145 | 0.996798 | 0.992795 | 0.988280 | 0.975159 | 0.967213 |

### Case repeat-851-s42

**d2**

| step | input | h1 | h2 |
|---|---|---|---|
| 0 | 0.999988 | 0.999984 | 0.999970 |
| 38225 | 0.999988 | 0.999982 | 0.999964 |
| 76450 | 0.999985 | 0.999961 | 0.999861 |
| 114675 | 0.999985 | 0.999961 | 0.999873 |
| 152900 | 0.999985 | 0.999960 | 0.999875 |

**d4**

| step | input | h1 | h2 | h3 | h4 |
|---|---|---|---|---|---|
| 0 | 0.999988 | 0.999984 | 0.999970 | 0.999940 | 0.999878 |
| 38225 | 0.999988 | 0.999982 | 0.999956 | 0.999901 | 0.999785 |
| 76450 | 0.999988 | 0.999982 | 0.999955 | 0.999902 | 0.999825 |
| 114675 | 0.999988 | 0.999981 | 0.999953 | 0.999895 | 0.999822 |
| 152900 | 0.999988 | 0.999980 | 0.999950 | 0.999883 | 0.999802 |

**d6**

| step | input | h1 | h2 | h3 | h4 | h5 | h6 |
|---|---|---|---|---|---|---|---|
| 0 | 0.999988 | 0.999984 | 0.999970 | 0.999940 | 0.999878 | 0.999716 | 0.999416 |
| 38225 | 0.999988 | 0.999984 | 0.999970 | 0.999933 | 0.999889 | 0.999744 | 0.999591 |
| 76450 | 0.999988 | 0.999983 | 0.999966 | 0.999923 | 0.999857 | 0.999663 | 0.999485 |
| 114675 | 0.999988 | 0.999981 | 0.999958 | 0.999906 | 0.999824 | 0.999605 | 0.999320 |
| 152900 | 0.999988 | 0.999979 | 0.999949 | 0.999883 | 0.999780 | 0.999523 | 0.999134 |

**d8**

| step | input | h1 | h2 | h3 | h4 | h5 | h6 | h7 | h8 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.999988 | 0.999984 | 0.999970 | 0.999940 | 0.999878 | 0.999716 | 0.999416 | 0.998611 | 0.997069 |
| 38225 | 0.999988 | 0.999983 | 0.999964 | 0.999919 | 0.999843 | 0.999626 | 0.999316 | 0.998417 | 0.997091 |
| 76450 | 0.999988 | 0.999983 | 0.999962 | 0.999910 | 0.999827 | 0.999606 | 0.999303 | 0.998517 | 0.997564 |
| 114675 | 0.999988 | 0.999981 | 0.999961 | 0.999909 | 0.999833 | 0.999598 | 0.999319 | 0.998546 | 0.997716 |
| 152900 | 0.999988 | 0.999981 | 0.999957 | 0.999899 | 0.999799 | 0.999546 | 0.999240 | 0.998339 | 0.997325 |

**d12** (the d12 control run of this case)

| step | input | h1 | h2 | h3 | h4 | h5 | h6 | h7 | h8 | h9 | h10 | h11 | h12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.999988 | 0.999984 | 0.999970 | 0.999940 | 0.999878 | 0.999716 | 0.999416 | 0.998611 | 0.997069 | 0.992935 | 0.985227 | 0.965045 | 0.926563 |
| 38225 | 0.999988 | 0.999983 | 0.999963 | 0.999915 | 0.999827 | 0.999597 | 0.999180 | 0.998124 | 0.996430 | 0.991690 | 0.985419 | 0.968081 | 0.949792 |
| 76450 | 0.999988 | 0.999982 | 0.999959 | 0.999907 | 0.999798 | 0.999515 | 0.999047 | 0.997763 | 0.995922 | 0.990638 | 0.984028 | 0.965990 | 0.950944 |
| 114675 | 0.999988 | 0.999981 | 0.999957 | 0.999901 | 0.999797 | 0.999521 | 0.999077 | 0.997904 | 0.996046 | 0.991059 | 0.985065 | 0.968301 | 0.956678 |
| 152900 | 0.999988 | 0.999981 | 0.999956 | 0.999902 | 0.999781 | 0.999493 | 0.999001 | 0.997684 | 0.995841 | 0.990603 | 0.984624 | 0.967401 | 0.956827 |

### Case repeat-1632-s41

**d2**

| step | input | h1 | h2 |
|---|---|---|---|
| 0 | 0.999988 | 0.999983 | 0.999969 |
| 38225 | 0.999988 | 0.999974 | 0.999933 |
| 76450 | 0.999988 | 0.999974 | 0.999935 |
| 114675 | 0.999988 | 0.999973 | 0.999934 |
| 152900 | 0.999987 | 0.999973 | 0.999933 |

**d4**

| step | input | h1 | h2 | h3 | h4 |
|---|---|---|---|---|---|
| 0 | 0.999988 | 0.999983 | 0.999969 | 0.999935 | 0.999873 |
| 38225 | 0.999988 | 0.999982 | 0.999970 | 0.999941 | 0.999924 |
| 76450 | 0.999988 | 0.999982 | 0.999967 | 0.999933 | 0.999917 |
| 114675 | 0.999988 | 0.999981 | 0.999966 | 0.999932 | 0.999915 |
| 152900 | 0.999988 | 0.999981 | 0.999966 | 0.999931 | 0.999914 |

**d6**

| step | input | h1 | h2 | h3 | h4 | h5 | h6 |
|---|---|---|---|---|---|---|---|
| 0 | 0.999988 | 0.999983 | 0.999969 | 0.999935 | 0.999873 | 0.999718 | 0.999392 |
| 38225 | 0.999988 | 0.999983 | 0.999967 | 0.999930 | 0.999875 | 0.999712 | 0.999517 |
| 76450 | 0.999988 | 0.999983 | 0.999967 | 0.999931 | 0.999888 | 0.999757 | 0.999619 |
| 114675 | 0.999988 | 0.999982 | 0.999960 | 0.999914 | 0.999852 | 0.999683 | 0.999452 |
| 152900 | 0.999988 | 0.999980 | 0.999953 | 0.999900 | 0.999832 | 0.999612 | 0.999356 |

**d8**

| step | input | h1 | h2 | h3 | h4 | h5 | h6 | h7 | h8 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.999988 | 0.999983 | 0.999969 | 0.999935 | 0.999873 | 0.999718 | 0.999392 | 0.998595 | 0.997002 |
| 38225 | 0.999988 | 0.999985 | 0.999959 | 0.999904 | 0.999815 | 0.999573 | 0.999226 | 0.998260 | 0.996987 |
| 76450 | 0.999988 | 0.999984 | 0.999967 | 0.999924 | 0.999849 | 0.999658 | 0.999375 | 0.998640 | 0.997706 |
| 114675 | 0.999988 | 0.999983 | 0.999959 | 0.999905 | 0.999820 | 0.999610 | 0.999260 | 0.998348 | 0.997308 |
| 152900 | 0.999988 | 0.999982 | 0.999958 | 0.999910 | 0.999821 | 0.999588 | 0.999274 | 0.998387 | 0.997560 |

**d12** (the d12 control run of this case)

| step | input | h1 | h2 | h3 | h4 | h5 | h6 | h7 | h8 | h9 | h10 | h11 | h12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.999988 | 0.999983 | 0.999969 | 0.999935 | 0.999873 | 0.999718 | 0.999392 | 0.998595 | 0.997002 | 0.992824 | 0.984743 | 0.963486 | 0.925689 |
| 38225 | 0.999988 | 0.999982 | 0.999961 | 0.999917 | 0.999827 | 0.999593 | 0.999181 | 0.998042 | 0.996473 | 0.992009 | 0.985925 | 0.968818 | 0.953537 |
| 76450 | 0.999988 | 0.999982 | 0.999958 | 0.999908 | 0.999792 | 0.999519 | 0.999080 | 0.997891 | 0.996089 | 0.991250 | 0.984893 | 0.967167 | 0.953521 |
| 114675 | 0.999988 | 0.999981 | 0.999958 | 0.999906 | 0.999821 | 0.999584 | 0.999219 | 0.998222 | 0.996814 | 0.992934 | 0.988601 | 0.975997 | 0.967674 |
| 152900 | 0.999988 | 0.999981 | 0.999956 | 0.999897 | 0.999770 | 0.999485 | 0.998977 | 0.997640 | 0.995823 | 0.990756 | 0.985626 | 0.970439 | 0.964184 |

## Matched contrasts against each case's d12 control

Each d2/d4/d6/d8 arm against the freshly registered d12 control of the same
case (freshly registered controls, never a historical run). Direction is the
exact E ordering; a case qualifies through a matching tier change OR a
relative E effect of at least 20%; confirmation requires all three cases
qualifying in one direction with all paired endpoints settled and clean.

### Arm d2 vs d12

| case | direction | arm E/tier | d12 E/tier | relative effect | tier direction | qualifies | endpoints (arm/control) |
|---|---|---|---|---|---|---|---|
| main | worsening | 0.121581/t0 | 0.034826/t1 | 2.491 | worsened | True | settled/unsettled |
| repeat-system | worsening | 0.170434/t0 | 0.067491/t1 | 1.525 | worsened | True | unsettled/unsettled |
| repeat-seed | worsening | 0.100486/t0 | 0.080813/t1 | 0.243 | worsened | True | unsettled/settled |

Arm confirmation label: **unsettled**.

### Arm d4 vs d12

| case | direction | arm E/tier | d12 E/tier | relative effect | tier direction | qualifies | endpoints (arm/control) |
|---|---|---|---|---|---|---|---|
| main | improvement | 0.034400/t1 | 0.034826/t1 | 0.012 | unchanged | False | settled/unsettled |
| repeat-system | worsening | 0.233286/t0 | 0.067491/t1 | 2.457 | worsened | True | settled/unsettled |
| repeat-seed | improvement | 0.073865/t1 | 0.080813/t1 | 0.086 | unchanged | False | settled/settled |

Arm confirmation label: **unsettled**.

### Arm d6 vs d12

| case | direction | arm E/tier | d12 E/tier | relative effect | tier direction | qualifies | endpoints (arm/control) |
|---|---|---|---|---|---|---|---|
| main | worsening | 0.058867/t1 | 0.034826/t1 | 0.690 | unchanged | True | settled/unsettled |
| repeat-system | improvement | 0.017319/t1 | 0.067491/t1 | 0.743 | unchanged | True | unsettled/unsettled |
| repeat-seed | improvement | 0.011827/t1 | 0.080813/t1 | 0.854 | unchanged | True | unsettled/settled |

Arm confirmation label: **unsettled**.

### Arm d8 vs d12

| case | direction | arm E/tier | d12 E/tier | relative effect | tier direction | qualifies | endpoints (arm/control) |
|---|---|---|---|---|---|---|---|
| main | improvement | 0.033446/t1 | 0.034826/t1 | 0.040 | unchanged | False | settled/unsettled |
| repeat-system | improvement | 0.022800/t1 | 0.067491/t1 | 0.662 | unchanged | True | unsettled/unsettled |
| repeat-seed | improvement | 0.017155/t1 | 0.080813/t1 | 0.788 | unchanged | True | settled/settled |

Arm confirmation label: **unsettled**.

## Reading against the committed prediction (prospective rule)

The registered hypothesis ("shallower depth improves the one-orbit fit: each
shallower arm's E is below the d12 control's on all three registered cases
under the registered effect rule") is **not supported on any arm at this
budget**, and **no arm is confirmable** in either direction: every arm's
confirmation label is `unsettled` because at least one paired endpoint is
unsettled — most consequentially the d12 control's own main-case endpoint,
which is unsettled (its final-quarter improvement exceeded 5%), blocking
confirmation for every arm of the main case, plus further arm-side
unsettled endpoints enumerated in `review.json` -> confirmation ->
unconfirmed. Observed per-arm directions at this budget:

- **d2: worsening on all three cases** (tier 0 vs the control's tier 1;
  relative effects 0.243-2.491). Consistent in direction, but not a
  registered confirmation (unsettled endpoints), so it is recorded as an
  observed fit only — the depth-2 arm fits worse everywhere.
- **d4: mixed** — improvement on main (0.012) and repeat-seed (0.086), large
  worsening on repeat-system (2.457, tier 0).
- **d6: mixed** — worsening on main (0.690), improvement on repeat-system
  (0.743) and repeat-seed (0.854).
- **d8: improvement on all three cases** (main 0.040, repeat-system 0.662,
  repeat-seed 0.788; tier 1 throughout). Direction-consistent, but main does
  not qualify (4.0% < 20% and no tier change), so the three-case
  confirmation rule does not fire; unsettled endpoints additionally block.
- **d12 (control): unsettled on main and repeat-system, settled on
  repeat-seed.** Its own endpoint remains inside the final-quarter
  improvement bound on two of three cases at N=152900.

The finite-budget depth-associated effect this experiment can state: at
N=152900 the d12 control and the d4/d6/d8 arms all reach tier 1 while d2
stays tier 0 on every case, several shallower arms beat the control's E on
individual cases, and the main-case contrasts remain inside the
unsettled/no-qualify band — so depth is not separable from its accompanying
parameter-count change (D-03) and the endpoint question stays open at this
budget. A successful endpoint remains an observed fit; confirmation requires
the full three-case rule above, which no arm meets.

## Prediction-table and roadmap comparison

Against the committed prediction table (`67-EXP02-PREDICTION.md`, byte-frozen
before any science run): each arm's observed branch is read against its
registered hypothesis/flat/opposite/unsettled/mechanical rows. The observed
dispositions (machine record: `review.json` -> predictions_comparison) are
d2: directions worsening/worsening/worsening, observed_confirmation
unsettled, disposition none; d4: improvement/worsening/improvement,
unsettled, none; d6: worsening/improvement/improvement, unsettled, none;
d8: improvement/improvement/improvement, unsettled, none. No arm landed on
the mechanical branch; no favourable-main selection was made — every
declared arm including mixed, small-effect and unsettled outcomes is
published here equally.

Roadmap comparison (`review.json` -> roadmap_comparison): each contrast's
confirmation label is read against the committed prediction table; the
roadmap's next experiment proceeds only when this review allows the
dependent launch. This review records dependent_launch_allowed = true,
scope49_disposition = none, proposed_change = null.

## SCOPE-49 disposition and dependent work

The observed experiment branch is the registered `unsettled` continue route:
no continuation runs (no-continuation policy — nothing extends, retries or
re-sizes any run after its score is read), no scope/resource/out-of-rule
change is proposed, and the EXP-03 rate ladder's dependent work may proceed
under D-01. No owner ruling is required on this route; no ruling file is
created.

## Descriptive limitations

- Loss is context only; it enters no rule.
- Adjacent-time similarity is associated evidence, not an information-loss
  proof or causation; no cosine threshold exists.
- GAP-59-08 stays explicit: E is the frozen scorecard's position-error
  score; the energy-check limitation is owner-routed and untouched here.
- No new-IC generalization claim: every run fits its own registered orbit
  window; the held-out evaluation remains unspent (TRAIN-only access, zero
  validation/test opens per the access attestations).
- The EXP-01 positive control (Phase 66) changes depth, width and first
  omega together; this ladder isolates the declared depth intervention
  while documenting its parameter-count change, and none of its numbers
  were reinterpreted here.

## Evidence citations

- Per row: `evidence/exp02/science/{case}/{arm}/registration.json` (committed
  at 652d1a9d), plus `record.json`, `attempt.json` (status=published),
  `power-gate.json` (AC Power receipts) and `diagnostic.weights`, committed
  together at the row hash cited in the endpoint table (Git chronology:
  09a60d00, 9c3aecab, a04e50fc, 9b2d7ba2, 9d2957b3, 6a19af45, 6a4c7f2c,
  2756362d, eb3b113c, 97d52264, c322c48e, 5d190697, ffd98e41, 4aed8511,
  c9b68e6e — one row per commit, in launch order).
- Machine review: `evidence/exp02/review.json` (generated by `review
  --experiment exp02`, PHASE67-REVIEW-WRITTEN allowed=True), committed
  beside this page.
- Design/budget/prediction: `evidence/exp02/design.json`,
  `evidence/exp02/budget.json`, `67-EXP02-PREDICTION.md`,
  `67-EXP02-BUDGET.md` (all committed at 652d1a9d; the prediction page was
  byte-frozen before any science launch).

## The generated review (embedded)

The byte-exact committed `review.json` as generated by `review
--experiment exp02`, embedded for the check-review digest match:

```json phase67-review
{
  "budget_steps": 152900,
  "confirmation": {
    "confirmed": [],
    "contrasts": {
      "d2": {
        "arm": "d2",
        "cases": {
          "main": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.12158120320360874,
                "tier": 0
              },
              "control": {
                "E": 0.03482590188705743,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 2.4911142745966544,
            "tier_direction": "worsened"
          },
          "repeat-seed": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.10048647826697461,
                "tier": 0
              },
              "control": {
                "E": 0.08081264163459871,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.2434499879527864,
            "tier_direction": "worsened"
          },
          "repeat-system": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.17043356151106176,
                "tier": 0
              },
              "control": {
                "E": 0.06749088823348984,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 1.5252825377172983,
            "tier_direction": "worsened"
          }
        },
        "confirmation": "unsettled",
        "control": "d12",
        "descriptive": {
          "adjacent_time_similarity": {
            "main": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999837279319763,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999697208404541,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999876618385315,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999775290489197,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999374747276306,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999876022338867,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999769330024719,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999380111694336,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999874234199524,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999763369560242,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999368786811829,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999873042106628,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999755620956421,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999353289604187,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 152900
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999837279319763,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999697208404541,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999352097511292,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998775124549866,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999712347984314,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999390184879303,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985547661781311,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9969659447669983,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9927595257759094,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9844540953636169,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9629203677177429,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9224951267242432,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999832510948181,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999594688415527,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999092817306519,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997974634170532,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995214939117432,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990511536598206,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997784435749054,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957220554351807,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9901578426361084,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9823592305183411,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.961142361164093,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9380327463150024,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999828338623047,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999569058418274,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999046921730042,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997938871383667,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995269775390625,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.99898761510849,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976747035980225,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9956965446472168,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9902918338775635,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9833380579948425,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9641813039779663,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.950472354888916,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999818801879883,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999598264694214,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999111294746399,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998100399971008,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995549321174622,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991307258605957,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979795813560486,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9962527751922607,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917433857917786,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9865732192993164,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9714349508285522,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9636873602867126,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987781047821,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815821647644,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999961256980896,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999112486839294,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998151659965515,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995825290679932,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991995096206665,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981447458267212,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996797502040863,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9927946329116821,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9882802963256836,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9751591682434082,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9672127962112427,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 152900
                }
              ]
            },
            "repeat-seed": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999827742576599,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999688863754272,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987781047821,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999741315841675,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999328851699829,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999876618385315,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999738931655884,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999352097511292,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999875426292419,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999732375144958,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999343156814575,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999874234199524,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999726414680481,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999326467514038,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 152900
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999827742576599,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999688863754272,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999354481697083,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999873161315918,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999718189239502,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993919730186462,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985952973365784,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.997002363204956,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9928239583969116,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9847432971000671,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9634863138198853,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.925688624382019,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999824166297913,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999611973762512,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999170899391174,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998269081115723,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995925426483154,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991812705993652,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9980418682098389,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964726567268372,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9920085072517395,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9859246611595154,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9688183665275574,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9535370469093323,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999820590019226,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999577403068542,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999076128005981,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997918605804443,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995185136795044,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990800619125366,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997891366481781,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960888624191284,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9912503957748413,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9848934412002563,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9671668410301208,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9535211324691772,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999806880950928,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999575018882751,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999062418937683,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998205304145813,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995840787887573,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992190599441528,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982219338417053,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996813952922821,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.992933988571167,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9886007308959961,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9759966135025024,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9676738381385803,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999808073043823,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999955952167511,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998968243598938,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997695684432983,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999484658241272,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989774823188782,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997639536857605,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958228468894958,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.990756094455719,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9856263995170593,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9704390168190002,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9641836881637573,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 152900
                }
              ]
            },
            "repeat-system": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836683273315,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999704957008362,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987781047821,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815821647644,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999639987945557,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999851584434509,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999613165855408,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9998610615730286,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999851584434509,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999605417251587,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9998728036880493,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999850988388062,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999599456787109,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9998748898506165,
                      "name": "h2",
                      "order": 2
                    }
                  ],
                  "step": 152900
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836683273315,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999704957008362,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999396800994873,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998784065246582,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997159242630005,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994155764579773,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986107349395752,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970688223838806,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929354786872864,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985227108001709,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9650446772575378,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.926563024520874,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999831914901733,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999628663063049,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999151825904846,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999826967716217,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995973110198975,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991797804832458,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981237053871155,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964298605918884,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9916902780532837,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9854190349578857,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9680813550949097,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9497920870780945,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999820590019226,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999585151672363,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999068975448608,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999798059463501,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995145201683044,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990473985671997,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977627396583557,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959222674369812,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9906383156776428,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9840281009674072,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9659903645515442,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9509439468383789,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999811053276062,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999571442604065,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999013543128967,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997971057891846,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995208978652954,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990772008895874,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.99790358543396,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960460066795349,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9910587072372437,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9850650429725647,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9683007597923279,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9566783308982849,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999808669090271,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999561905860901,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999021291732788,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997810125350952,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994930624961853,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990007877349854,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976843595504761,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958409070968628,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9906029105186462,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9846235513687134,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9674005508422852,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9568272233009338,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 152900
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp02",
        "reasons": [
          "the main/control endpoint is unsettled",
          "the repeat-system/arm endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled",
          "the repeat-seed/arm endpoint is unsettled"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      },
      "d4": {
        "arm": "d4",
        "cases": {
          "main": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "settled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.0343996498236197,
                "tier": 1
              },
              "control": {
                "E": 0.03482590188705743,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": false,
            "reasons": [
              "the effect is below the registered twenty-percent line with no matching tier change"
            ],
            "relative_E_effect": 0.012239512556490032,
            "tier_direction": "unchanged"
          },
          "repeat-seed": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.07386500305114937,
                "tier": 1
              },
              "control": {
                "E": 0.08081264163459871,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": false,
            "reasons": [
              "the effect is below the registered twenty-percent line with no matching tier change"
            ],
            "relative_E_effect": 0.08597217518100299,
            "tier_direction": "unchanged"
          },
          "repeat-system": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.23328599364334615,
                "tier": 0
              },
              "control": {
                "E": 0.06749088823348984,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 2.4565553921334624,
            "tier_direction": "worsened"
          }
        },
        "confirmation": "unsettled",
        "control": "d12",
        "descriptive": {
          "adjacent_time_similarity": {
            "main": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999837279319763,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999697208404541,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999352097511292,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998775124549866,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999839067459106,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999719262123108,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999424815177917,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9999196529388428,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999831318855286,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999706745147705,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999392032623291,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9999144673347473,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999821782112122,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999697208404541,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999390840530396,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9999154210090637,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880194664001,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999814629554749,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999691247940063,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999374747276306,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9999117255210876,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 152900
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999837279319763,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999697208404541,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999352097511292,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998775124549866,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999712347984314,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999390184879303,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985547661781311,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9969659447669983,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9927595257759094,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9844540953636169,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9629203677177429,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9224951267242432,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999832510948181,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999594688415527,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999092817306519,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997974634170532,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995214939117432,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990511536598206,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997784435749054,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957220554351807,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9901578426361084,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9823592305183411,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.961142361164093,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9380327463150024,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999828338623047,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999569058418274,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999046921730042,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997938871383667,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995269775390625,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.99898761510849,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976747035980225,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9956965446472168,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9902918338775635,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9833380579948425,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9641813039779663,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.950472354888916,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999818801879883,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999598264694214,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999111294746399,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998100399971008,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995549321174622,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991307258605957,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979795813560486,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9962527751922607,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917433857917786,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9865732192993164,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9714349508285522,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9636873602867126,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987781047821,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815821647644,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999961256980896,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999112486839294,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998151659965515,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995825290679932,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991995096206665,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981447458267212,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996797502040863,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9927946329116821,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9882802963256836,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9751591682434082,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9672127962112427,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 152900
                }
              ]
            },
            "repeat-seed": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999827742576599,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999688863754272,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999354481697083,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999873161315918,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999822974205017,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999704360961914,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999410510063171,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999923825263977,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999817609786987,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999672770500183,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999333620071411,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999916672706604,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999812245368958,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999662041664124,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999318718910217,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9999145269393921,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999812841415405,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999658465385437,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999309182167053,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9999140501022339,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 152900
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999827742576599,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999688863754272,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999354481697083,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999873161315918,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999718189239502,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993919730186462,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985952973365784,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.997002363204956,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9928239583969116,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9847432971000671,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9634863138198853,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.925688624382019,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999824166297913,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999611973762512,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999170899391174,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998269081115723,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995925426483154,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991812705993652,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9980418682098389,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964726567268372,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9920085072517395,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9859246611595154,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9688183665275574,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9535370469093323,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999820590019226,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999577403068542,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999076128005981,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997918605804443,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995185136795044,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990800619125366,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997891366481781,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960888624191284,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9912503957748413,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9848934412002563,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9671668410301208,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9535211324691772,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999806880950928,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999575018882751,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999062418937683,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998205304145813,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995840787887573,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992190599441528,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982219338417053,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996813952922821,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.992933988571167,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9886007308959961,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9759966135025024,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9676738381385803,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999808073043823,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999955952167511,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998968243598938,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997695684432983,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999484658241272,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989774823188782,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997639536857605,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958228468894958,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.990756094455719,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9856263995170593,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9704390168190002,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9641836881637573,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 152900
                }
              ]
            },
            "repeat-system": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836683273315,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999704957008362,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999396800994873,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998784065246582,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999822974205017,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999557137489319,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999013543128967,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997854828834534,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815821647644,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999549388885498,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999015927314758,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998254179954529,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999806880950928,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999532699584961,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998951554298401,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998224973678589,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999876618385315,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999797344207764,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999498128890991,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998834729194641,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998022317886353,
                      "name": "h4",
                      "order": 4
                    }
                  ],
                  "step": 152900
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836683273315,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999704957008362,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999396800994873,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998784065246582,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997159242630005,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994155764579773,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986107349395752,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970688223838806,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929354786872864,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985227108001709,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9650446772575378,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.926563024520874,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999831914901733,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999628663063049,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999151825904846,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999826967716217,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995973110198975,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991797804832458,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981237053871155,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964298605918884,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9916902780532837,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9854190349578857,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9680813550949097,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9497920870780945,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999820590019226,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999585151672363,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999068975448608,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999798059463501,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995145201683044,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990473985671997,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977627396583557,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959222674369812,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9906383156776428,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9840281009674072,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9659903645515442,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9509439468383789,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999811053276062,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999571442604065,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999013543128967,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997971057891846,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995208978652954,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990772008895874,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.99790358543396,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960460066795349,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9910587072372437,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9850650429725647,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9683007597923279,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9566783308982849,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999808669090271,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999561905860901,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999021291732788,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997810125350952,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994930624961853,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990007877349854,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976843595504761,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958409070968628,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9906029105186462,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9846235513687134,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9674005508422852,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9568272233009338,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 152900
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp02",
        "reasons": [
          "the main/control endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      },
      "d6": {
        "arm": "d6",
        "cases": {
          "main": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.0588671343305699,
                "tier": 1
              },
              "control": {
                "E": 0.03482590188705743,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.6903261980545311,
            "tier_direction": "unchanged"
          },
          "repeat-seed": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.011827234768698413,
                "tier": 1
              },
              "control": {
                "E": 0.08081264163459871,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.8536462299775291,
            "tier_direction": "unchanged"
          },
          "repeat-system": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.01731869678957498,
                "tier": 1
              },
              "control": {
                "E": 0.06749088823348984,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.7433920749470708,
            "tier_direction": "unchanged"
          }
        },
        "confirmation": "unsettled",
        "control": "d12",
        "descriptive": {
          "adjacent_time_similarity": {
            "main": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999837279319763,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999697208404541,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999352097511292,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998775124549866,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999712347984314,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999390184879303,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999841451644897,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999728798866272,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999430179595947,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9999150633811951,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9998119473457336,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9997508525848389,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999984085559845,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999706745147705,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999372363090515,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9999054074287415,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997837543487549,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9996777176856995,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999826550483704,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999668002128601,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999282360076904,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998819828033447,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997456073760986,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9995741248130798,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880790710449,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999812245368958,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999625086784363,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999173879623413,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998629093170166,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996998310089111,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9995063543319702,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 152900
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999837279319763,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999697208404541,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999352097511292,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998775124549866,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999712347984314,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999390184879303,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985547661781311,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9969659447669983,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9927595257759094,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9844540953636169,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9629203677177429,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9224951267242432,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999832510948181,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999594688415527,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999092817306519,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997974634170532,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995214939117432,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990511536598206,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997784435749054,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957220554351807,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9901578426361084,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9823592305183411,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.961142361164093,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9380327463150024,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999828338623047,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999569058418274,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999046921730042,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997938871383667,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995269775390625,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.99898761510849,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976747035980225,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9956965446472168,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9902918338775635,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9833380579948425,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9641813039779663,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.950472354888916,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999818801879883,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999598264694214,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999111294746399,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998100399971008,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995549321174622,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991307258605957,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979795813560486,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9962527751922607,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917433857917786,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9865732192993164,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9714349508285522,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9636873602867126,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987781047821,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815821647644,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999961256980896,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999112486839294,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998151659965515,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995825290679932,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991995096206665,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981447458267212,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996797502040863,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9927946329116821,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9882802963256836,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9751591682434082,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9672127962112427,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 152900
                }
              ]
            },
            "repeat-seed": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999827742576599,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999688863754272,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999354481697083,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999873161315918,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999718189239502,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993919730186462,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999828338623047,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999966561794281,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999929666519165,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998751878738403,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997119307518005,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9995174407958984,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999828934669495,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999669194221497,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999306797981262,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998878240585327,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997573494911194,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9996187686920166,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999981701374054,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999604225158691,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999135732650757,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998517036437988,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996830821037292,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999451756477356,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999875426292419,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999798536300659,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999533891677856,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998995065689087,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999832272529602,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996119141578674,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993558526039124,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 152900
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999827742576599,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999688863754272,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999354481697083,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999873161315918,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999718189239502,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993919730186462,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985952973365784,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.997002363204956,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9928239583969116,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9847432971000671,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9634863138198853,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.925688624382019,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999824166297913,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999611973762512,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999170899391174,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998269081115723,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995925426483154,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991812705993652,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9980418682098389,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964726567268372,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9920085072517395,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9859246611595154,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9688183665275574,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9535370469093323,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999820590019226,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999577403068542,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999076128005981,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997918605804443,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995185136795044,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990800619125366,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997891366481781,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960888624191284,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9912503957748413,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9848934412002563,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9671668410301208,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9535211324691772,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999806880950928,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999575018882751,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999062418937683,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998205304145813,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995840787887573,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992190599441528,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982219338417053,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996813952922821,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.992933988571167,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9886007308959961,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9759966135025024,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9676738381385803,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999808073043823,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999955952167511,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998968243598938,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997695684432983,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999484658241272,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989774823188782,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997639536857605,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958228468894958,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.990756094455719,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9856263995170593,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9704390168190002,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9641836881637573,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 152900
                }
              ]
            },
            "repeat-system": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836683273315,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999704957008362,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999396800994873,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998784065246582,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997159242630005,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994155764579773,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999840259552002,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999700784683228,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999334812164307,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998892545700073,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997441172599792,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9995907545089722,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881982803345,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999828338623047,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999657273292542,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999231100082397,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998571872711182,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996629357337952,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994845986366272,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880194664001,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999811053276062,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999583959579468,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999058842658997,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998243451118469,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996048808097839,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993204474449158,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999876618385315,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999793767929077,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999492168426514,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999882698059082,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997798800468445,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995233416557312,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991335868835449,
                      "name": "h6",
                      "order": 6
                    }
                  ],
                  "step": 152900
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836683273315,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999704957008362,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999396800994873,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998784065246582,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997159242630005,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994155764579773,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986107349395752,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970688223838806,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929354786872864,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985227108001709,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9650446772575378,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.926563024520874,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999831914901733,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999628663063049,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999151825904846,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999826967716217,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995973110198975,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991797804832458,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981237053871155,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964298605918884,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9916902780532837,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9854190349578857,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9680813550949097,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9497920870780945,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999820590019226,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999585151672363,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999068975448608,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999798059463501,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995145201683044,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990473985671997,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977627396583557,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959222674369812,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9906383156776428,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9840281009674072,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9659903645515442,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9509439468383789,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999811053276062,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999571442604065,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999013543128967,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997971057891846,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995208978652954,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990772008895874,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.99790358543396,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960460066795349,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9910587072372437,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9850650429725647,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9683007597923279,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9566783308982849,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999808669090271,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999561905860901,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999021291732788,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997810125350952,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994930624961853,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990007877349854,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976843595504761,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958409070968628,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9906029105186462,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9846235513687134,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9674005508422852,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9568272233009338,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 152900
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp02",
        "reasons": [
          "the main/control endpoint is unsettled",
          "the repeat-system/arm endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled",
          "the repeat-seed/arm endpoint is unsettled"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      },
      "d8": {
        "arm": "d8",
        "cases": {
          "main": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "settled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.03344629454651585,
                "tier": 1
              },
              "control": {
                "E": 0.03482590188705743,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": false,
            "reasons": [
              "the effect is below the registered twenty-percent line with no matching tier change"
            ],
            "relative_E_effect": 0.03961440381402703,
            "tier_direction": "unchanged"
          },
          "repeat-seed": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.01715509046203649,
                "tier": 1
              },
              "control": {
                "E": 0.08081264163459871,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.787717736791668,
            "tier_direction": "unchanged"
          },
          "repeat-system": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.022799860938189802,
                "tier": 1
              },
              "control": {
                "E": 0.06749088823348984,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.6621786801899546,
            "tier_direction": "unchanged"
          }
        },
        "confirmation": "unsettled",
        "control": "d12",
        "descriptive": {
          "adjacent_time_similarity": {
            "main": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999837279319763,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999697208404541,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999352097511292,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998775124549866,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999712347984314,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999390184879303,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985547661781311,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9969659447669983,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999833703041077,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999591112136841,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999096393585205,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998154044151306,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995670318603516,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991677403450012,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981472492218018,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9966184496879578,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836087226868,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999589920043945,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999092817306519,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998242259025574,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995966553688049,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999248206615448,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982942938804626,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9969724416732788,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999828934669495,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999594688415527,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999112486839294,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998270273208618,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996085166931152,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992854595184326,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9984181523323059,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9975581169128418,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999827742576599,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999563097953796,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999004006385803,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997996687889099,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995405077934265,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992218017578125,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.99830162525177,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.99741530418396,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 152900
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999837279319763,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999697208404541,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999352097511292,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998775124549866,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999712347984314,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999390184879303,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985547661781311,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9969659447669983,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9927595257759094,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9844540953636169,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9629203677177429,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9224951267242432,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999832510948181,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999594688415527,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999092817306519,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997974634170532,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995214939117432,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990511536598206,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997784435749054,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957220554351807,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9901578426361084,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9823592305183411,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.961142361164093,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9380327463150024,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999828338623047,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999569058418274,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999046921730042,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997938871383667,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995269775390625,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.99898761510849,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976747035980225,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9956965446472168,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9902918338775635,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9833380579948425,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9641813039779663,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.950472354888916,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999818801879883,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999598264694214,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999111294746399,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998100399971008,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995549321174622,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991307258605957,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979795813560486,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9962527751922607,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917433857917786,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9865732192993164,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9714349508285522,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9636873602867126,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987781047821,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815821647644,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999961256980896,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999112486839294,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998151659965515,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995825290679932,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991995096206665,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981447458267212,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996797502040863,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9927946329116821,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9882802963256836,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9751591682434082,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9672127962112427,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 152900
                }
              ]
            },
            "repeat-seed": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999827742576599,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999688863754272,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999354481697083,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999873161315918,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999718189239502,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993919730186462,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985952973365784,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.997002363204956,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999847412109375,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999586343765259,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999040365219116,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998147487640381,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995729923248291,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992263317108154,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982595443725586,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9969871640205383,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999839067459106,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999669194221497,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999241828918457,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998491406440735,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996576905250549,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993747472763062,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986397624015808,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9977055788040161,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999831318855286,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999593496322632,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999052882194519,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998201131820679,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996104836463928,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992596507072449,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9983482956886292,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9973083734512329,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999981701374054,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999583959579468,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999098181724548,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998214244842529,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995882511138916,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992741346359253,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9983866810798645,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9975599646568298,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 152900
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999827742576599,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999688863754272,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999354481697083,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999873161315918,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999718189239502,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993919730186462,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985952973365784,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.997002363204956,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9928239583969116,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9847432971000671,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9634863138198853,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.925688624382019,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999824166297913,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999611973762512,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999170899391174,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998269081115723,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995925426483154,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991812705993652,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9980418682098389,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964726567268372,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9920085072517395,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9859246611595154,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9688183665275574,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9535370469093323,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999820590019226,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999577403068542,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999076128005981,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997918605804443,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995185136795044,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990800619125366,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997891366481781,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960888624191284,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9912503957748413,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9848934412002563,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9671668410301208,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9535211324691772,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999806880950928,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999575018882751,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999062418937683,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998205304145813,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995840787887573,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992190599441528,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982219338417053,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996813952922821,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.992933988571167,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9886007308959961,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9759966135025024,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9676738381385803,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999808073043823,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999955952167511,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998968243598938,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997695684432983,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999484658241272,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989774823188782,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997639536857605,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958228468894958,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.990756094455719,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9856263995170593,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9704390168190002,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9641836881637573,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 152900
                }
              ]
            },
            "repeat-system": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836683273315,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999704957008362,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999396800994873,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998784065246582,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997159242630005,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994155764579773,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986107349395752,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970688223838806,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999829530715942,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999637603759766,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999194145202637,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998425245285034,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999626100063324,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993156790733337,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9984166026115417,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970910549163818,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999834299087524,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999623894691467,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999099373817444,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998265504837036,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996059536933899,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993029832839966,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985170364379883,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9975638389587402,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880194664001,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999814629554749,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999610781669617,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999090433120728,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998332262039185,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995976686477661,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993191361427307,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985458254814148,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9977155923843384,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880790710449,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999814629554749,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999565482139587,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998990297317505,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997987151145935,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995457530021667,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992395043373108,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9983389973640442,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9973251819610596,
                      "name": "h8",
                      "order": 8
                    }
                  ],
                  "step": 152900
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836683273315,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999704957008362,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999396800994873,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998784065246582,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997159242630005,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994155764579773,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986107349395752,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970688223838806,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929354786872864,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985227108001709,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9650446772575378,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.926563024520874,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999831914901733,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999628663063049,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999151825904846,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999826967716217,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995973110198975,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991797804832458,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981237053871155,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964298605918884,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9916902780532837,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9854190349578857,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9680813550949097,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9497920870780945,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38225
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999820590019226,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999585151672363,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999068975448608,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999798059463501,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995145201683044,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990473985671997,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977627396583557,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959222674369812,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9906383156776428,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9840281009674072,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9659903645515442,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9509439468383789,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 76450
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999811053276062,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999571442604065,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999013543128967,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997971057891846,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995208978652954,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990772008895874,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.99790358543396,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960460066795349,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9910587072372437,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9850650429725647,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9683007597923279,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9566783308982849,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 114675
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999879002571106,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999808669090271,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999561905860901,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999021291732788,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997810125350952,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994930624961853,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990007877349854,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976843595504761,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958409070968628,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9906029105186462,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9846235513687134,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9674005508422852,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9568272233009338,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 152900
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp02",
        "reasons": [
          "the main/control endpoint is unsettled",
          "the repeat-system/arm endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      }
    },
    "descriptive": {
      "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
      "loss": "context only",
      "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
    },
    "experiment": "exp02",
    "unconfirmed": [
      {
        "arm": "d2",
        "confirmation": "unsettled",
        "reasons": [
          "the main/control endpoint is unsettled",
          "the repeat-system/arm endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled",
          "the repeat-seed/arm endpoint is unsettled"
        ]
      },
      {
        "arm": "d4",
        "confirmation": "unsettled",
        "reasons": [
          "the main/control endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled"
        ]
      },
      {
        "arm": "d6",
        "confirmation": "unsettled",
        "reasons": [
          "the main/control endpoint is unsettled",
          "the repeat-system/arm endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled",
          "the repeat-seed/arm endpoint is unsettled"
        ]
      },
      {
        "arm": "d8",
        "confirmation": "unsettled",
        "reasons": [
          "the main/control endpoint is unsettled",
          "the repeat-system/arm endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled"
        ]
      }
    ]
  },
  "contrasts": {
    "d2": {
      "arm": "d2",
      "cases": {
        "main": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.12158120320360874,
              "tier": 0
            },
            "control": {
              "E": 0.03482590188705743,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 2.4911142745966544,
          "tier_direction": "worsened"
        },
        "repeat-seed": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.10048647826697461,
              "tier": 0
            },
            "control": {
              "E": 0.08081264163459871,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.2434499879527864,
          "tier_direction": "worsened"
        },
        "repeat-system": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.17043356151106176,
              "tier": 0
            },
            "control": {
              "E": 0.06749088823348984,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 1.5252825377172983,
          "tier_direction": "worsened"
        }
      },
      "confirmation": "unsettled",
      "control": "d12",
      "descriptive": {
        "adjacent_time_similarity": {
          "main": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999837279319763,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999697208404541,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999876618385315,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999775290489197,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999374747276306,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999876022338867,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999769330024719,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999380111694336,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999874234199524,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999763369560242,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999368786811829,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999873042106628,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999755620956421,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999353289604187,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 152900
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999837279319763,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999697208404541,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999352097511292,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998775124549866,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999712347984314,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999390184879303,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985547661781311,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9969659447669983,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9927595257759094,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9844540953636169,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9629203677177429,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9224951267242432,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999832510948181,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999594688415527,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999092817306519,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997974634170532,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995214939117432,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990511536598206,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997784435749054,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957220554351807,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9901578426361084,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9823592305183411,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.961142361164093,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9380327463150024,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999828338623047,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999569058418274,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999046921730042,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997938871383667,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995269775390625,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.99898761510849,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976747035980225,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9956965446472168,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9902918338775635,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9833380579948425,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9641813039779663,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.950472354888916,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999818801879883,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999598264694214,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999111294746399,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998100399971008,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995549321174622,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991307258605957,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979795813560486,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9962527751922607,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917433857917786,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9865732192993164,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9714349508285522,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9636873602867126,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987781047821,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815821647644,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999961256980896,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999112486839294,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998151659965515,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995825290679932,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991995096206665,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981447458267212,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996797502040863,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9927946329116821,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9882802963256836,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9751591682434082,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9672127962112427,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 152900
              }
            ]
          },
          "repeat-seed": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999827742576599,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999688863754272,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987781047821,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999741315841675,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999328851699829,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999876618385315,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999738931655884,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999352097511292,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999875426292419,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999732375144958,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999343156814575,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999874234199524,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999726414680481,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999326467514038,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 152900
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999827742576599,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999688863754272,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999354481697083,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999873161315918,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999718189239502,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993919730186462,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985952973365784,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.997002363204956,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9928239583969116,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9847432971000671,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9634863138198853,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.925688624382019,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999824166297913,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999611973762512,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999170899391174,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998269081115723,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995925426483154,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991812705993652,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9980418682098389,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964726567268372,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9920085072517395,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9859246611595154,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9688183665275574,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9535370469093323,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999820590019226,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999577403068542,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999076128005981,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997918605804443,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995185136795044,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990800619125366,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997891366481781,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960888624191284,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9912503957748413,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9848934412002563,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9671668410301208,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9535211324691772,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999806880950928,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999575018882751,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999062418937683,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998205304145813,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995840787887573,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992190599441528,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982219338417053,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996813952922821,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.992933988571167,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9886007308959961,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9759966135025024,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9676738381385803,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999808073043823,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999955952167511,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998968243598938,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997695684432983,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999484658241272,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989774823188782,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997639536857605,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958228468894958,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.990756094455719,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9856263995170593,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9704390168190002,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9641836881637573,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 152900
              }
            ]
          },
          "repeat-system": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836683273315,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999704957008362,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987781047821,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815821647644,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999639987945557,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999851584434509,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999613165855408,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9998610615730286,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999851584434509,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999605417251587,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9998728036880493,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999850988388062,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999599456787109,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9998748898506165,
                    "name": "h2",
                    "order": 2
                  }
                ],
                "step": 152900
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836683273315,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999704957008362,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999396800994873,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998784065246582,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997159242630005,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994155764579773,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986107349395752,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970688223838806,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929354786872864,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985227108001709,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9650446772575378,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.926563024520874,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999831914901733,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999628663063049,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999151825904846,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999826967716217,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995973110198975,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991797804832458,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981237053871155,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964298605918884,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9916902780532837,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9854190349578857,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9680813550949097,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9497920870780945,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999820590019226,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999585151672363,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999068975448608,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999798059463501,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995145201683044,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990473985671997,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977627396583557,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959222674369812,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9906383156776428,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9840281009674072,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9659903645515442,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9509439468383789,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999811053276062,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999571442604065,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999013543128967,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997971057891846,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995208978652954,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990772008895874,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.99790358543396,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960460066795349,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9910587072372437,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9850650429725647,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9683007597923279,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9566783308982849,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999808669090271,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999561905860901,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999021291732788,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997810125350952,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994930624961853,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990007877349854,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976843595504761,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958409070968628,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9906029105186462,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9846235513687134,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9674005508422852,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9568272233009338,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 152900
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp02",
      "reasons": [
        "the main/control endpoint is unsettled",
        "the repeat-system/arm endpoint is unsettled",
        "the repeat-system/control endpoint is unsettled",
        "the repeat-seed/arm endpoint is unsettled"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    },
    "d4": {
      "arm": "d4",
      "cases": {
        "main": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "settled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.0343996498236197,
              "tier": 1
            },
            "control": {
              "E": 0.03482590188705743,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": false,
          "reasons": [
            "the effect is below the registered twenty-percent line with no matching tier change"
          ],
          "relative_E_effect": 0.012239512556490032,
          "tier_direction": "unchanged"
        },
        "repeat-seed": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.07386500305114937,
              "tier": 1
            },
            "control": {
              "E": 0.08081264163459871,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": false,
          "reasons": [
            "the effect is below the registered twenty-percent line with no matching tier change"
          ],
          "relative_E_effect": 0.08597217518100299,
          "tier_direction": "unchanged"
        },
        "repeat-system": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.23328599364334615,
              "tier": 0
            },
            "control": {
              "E": 0.06749088823348984,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 2.4565553921334624,
          "tier_direction": "worsened"
        }
      },
      "confirmation": "unsettled",
      "control": "d12",
      "descriptive": {
        "adjacent_time_similarity": {
          "main": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999837279319763,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999697208404541,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999352097511292,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998775124549866,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999839067459106,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999719262123108,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999424815177917,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9999196529388428,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999831318855286,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999706745147705,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999392032623291,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9999144673347473,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999821782112122,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999697208404541,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999390840530396,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9999154210090637,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880194664001,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999814629554749,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999691247940063,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999374747276306,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9999117255210876,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 152900
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999837279319763,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999697208404541,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999352097511292,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998775124549866,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999712347984314,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999390184879303,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985547661781311,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9969659447669983,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9927595257759094,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9844540953636169,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9629203677177429,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9224951267242432,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999832510948181,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999594688415527,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999092817306519,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997974634170532,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995214939117432,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990511536598206,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997784435749054,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957220554351807,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9901578426361084,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9823592305183411,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.961142361164093,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9380327463150024,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999828338623047,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999569058418274,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999046921730042,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997938871383667,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995269775390625,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.99898761510849,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976747035980225,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9956965446472168,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9902918338775635,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9833380579948425,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9641813039779663,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.950472354888916,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999818801879883,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999598264694214,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999111294746399,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998100399971008,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995549321174622,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991307258605957,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979795813560486,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9962527751922607,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917433857917786,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9865732192993164,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9714349508285522,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9636873602867126,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987781047821,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815821647644,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999961256980896,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999112486839294,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998151659965515,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995825290679932,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991995096206665,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981447458267212,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996797502040863,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9927946329116821,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9882802963256836,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9751591682434082,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9672127962112427,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 152900
              }
            ]
          },
          "repeat-seed": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999827742576599,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999688863754272,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999354481697083,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999873161315918,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999822974205017,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999704360961914,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999410510063171,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999923825263977,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999817609786987,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999672770500183,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999333620071411,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999916672706604,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999812245368958,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999662041664124,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999318718910217,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9999145269393921,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999812841415405,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999658465385437,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999309182167053,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9999140501022339,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 152900
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999827742576599,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999688863754272,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999354481697083,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999873161315918,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999718189239502,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993919730186462,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985952973365784,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.997002363204956,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9928239583969116,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9847432971000671,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9634863138198853,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.925688624382019,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999824166297913,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999611973762512,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999170899391174,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998269081115723,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995925426483154,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991812705993652,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9980418682098389,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964726567268372,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9920085072517395,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9859246611595154,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9688183665275574,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9535370469093323,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999820590019226,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999577403068542,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999076128005981,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997918605804443,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995185136795044,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990800619125366,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997891366481781,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960888624191284,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9912503957748413,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9848934412002563,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9671668410301208,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9535211324691772,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999806880950928,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999575018882751,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999062418937683,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998205304145813,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995840787887573,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992190599441528,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982219338417053,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996813952922821,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.992933988571167,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9886007308959961,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9759966135025024,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9676738381385803,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999808073043823,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999955952167511,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998968243598938,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997695684432983,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999484658241272,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989774823188782,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997639536857605,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958228468894958,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.990756094455719,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9856263995170593,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9704390168190002,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9641836881637573,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 152900
              }
            ]
          },
          "repeat-system": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836683273315,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999704957008362,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999396800994873,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998784065246582,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999822974205017,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999557137489319,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999013543128967,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997854828834534,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815821647644,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999549388885498,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999015927314758,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998254179954529,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999806880950928,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999532699584961,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998951554298401,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998224973678589,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999876618385315,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999797344207764,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999498128890991,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998834729194641,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998022317886353,
                    "name": "h4",
                    "order": 4
                  }
                ],
                "step": 152900
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836683273315,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999704957008362,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999396800994873,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998784065246582,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997159242630005,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994155764579773,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986107349395752,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970688223838806,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929354786872864,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985227108001709,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9650446772575378,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.926563024520874,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999831914901733,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999628663063049,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999151825904846,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999826967716217,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995973110198975,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991797804832458,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981237053871155,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964298605918884,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9916902780532837,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9854190349578857,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9680813550949097,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9497920870780945,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999820590019226,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999585151672363,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999068975448608,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999798059463501,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995145201683044,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990473985671997,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977627396583557,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959222674369812,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9906383156776428,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9840281009674072,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9659903645515442,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9509439468383789,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999811053276062,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999571442604065,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999013543128967,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997971057891846,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995208978652954,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990772008895874,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.99790358543396,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960460066795349,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9910587072372437,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9850650429725647,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9683007597923279,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9566783308982849,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999808669090271,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999561905860901,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999021291732788,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997810125350952,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994930624961853,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990007877349854,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976843595504761,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958409070968628,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9906029105186462,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9846235513687134,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9674005508422852,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9568272233009338,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 152900
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp02",
      "reasons": [
        "the main/control endpoint is unsettled",
        "the repeat-system/control endpoint is unsettled"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    },
    "d6": {
      "arm": "d6",
      "cases": {
        "main": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.0588671343305699,
              "tier": 1
            },
            "control": {
              "E": 0.03482590188705743,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.6903261980545311,
          "tier_direction": "unchanged"
        },
        "repeat-seed": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.011827234768698413,
              "tier": 1
            },
            "control": {
              "E": 0.08081264163459871,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.8536462299775291,
          "tier_direction": "unchanged"
        },
        "repeat-system": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.01731869678957498,
              "tier": 1
            },
            "control": {
              "E": 0.06749088823348984,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.7433920749470708,
          "tier_direction": "unchanged"
        }
      },
      "confirmation": "unsettled",
      "control": "d12",
      "descriptive": {
        "adjacent_time_similarity": {
          "main": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999837279319763,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999697208404541,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999352097511292,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998775124549866,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999712347984314,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999390184879303,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999841451644897,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999728798866272,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999430179595947,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9999150633811951,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9998119473457336,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9997508525848389,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999984085559845,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999706745147705,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999372363090515,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9999054074287415,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997837543487549,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9996777176856995,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999826550483704,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999668002128601,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999282360076904,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998819828033447,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997456073760986,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9995741248130798,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880790710449,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999812245368958,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999625086784363,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999173879623413,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998629093170166,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996998310089111,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9995063543319702,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 152900
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999837279319763,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999697208404541,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999352097511292,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998775124549866,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999712347984314,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999390184879303,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985547661781311,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9969659447669983,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9927595257759094,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9844540953636169,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9629203677177429,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9224951267242432,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999832510948181,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999594688415527,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999092817306519,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997974634170532,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995214939117432,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990511536598206,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997784435749054,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957220554351807,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9901578426361084,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9823592305183411,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.961142361164093,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9380327463150024,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999828338623047,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999569058418274,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999046921730042,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997938871383667,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995269775390625,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.99898761510849,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976747035980225,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9956965446472168,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9902918338775635,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9833380579948425,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9641813039779663,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.950472354888916,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999818801879883,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999598264694214,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999111294746399,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998100399971008,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995549321174622,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991307258605957,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979795813560486,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9962527751922607,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917433857917786,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9865732192993164,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9714349508285522,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9636873602867126,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987781047821,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815821647644,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999961256980896,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999112486839294,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998151659965515,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995825290679932,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991995096206665,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981447458267212,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996797502040863,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9927946329116821,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9882802963256836,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9751591682434082,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9672127962112427,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 152900
              }
            ]
          },
          "repeat-seed": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999827742576599,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999688863754272,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999354481697083,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999873161315918,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999718189239502,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993919730186462,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999828338623047,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999966561794281,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999929666519165,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998751878738403,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997119307518005,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9995174407958984,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999828934669495,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999669194221497,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999306797981262,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998878240585327,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997573494911194,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9996187686920166,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999981701374054,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999604225158691,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999135732650757,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998517036437988,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996830821037292,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999451756477356,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999875426292419,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999798536300659,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999533891677856,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998995065689087,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999832272529602,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996119141578674,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993558526039124,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 152900
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999827742576599,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999688863754272,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999354481697083,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999873161315918,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999718189239502,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993919730186462,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985952973365784,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.997002363204956,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9928239583969116,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9847432971000671,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9634863138198853,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.925688624382019,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999824166297913,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999611973762512,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999170899391174,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998269081115723,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995925426483154,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991812705993652,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9980418682098389,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964726567268372,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9920085072517395,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9859246611595154,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9688183665275574,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9535370469093323,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999820590019226,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999577403068542,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999076128005981,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997918605804443,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995185136795044,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990800619125366,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997891366481781,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960888624191284,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9912503957748413,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9848934412002563,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9671668410301208,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9535211324691772,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999806880950928,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999575018882751,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999062418937683,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998205304145813,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995840787887573,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992190599441528,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982219338417053,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996813952922821,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.992933988571167,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9886007308959961,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9759966135025024,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9676738381385803,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999808073043823,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999955952167511,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998968243598938,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997695684432983,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999484658241272,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989774823188782,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997639536857605,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958228468894958,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.990756094455719,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9856263995170593,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9704390168190002,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9641836881637573,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 152900
              }
            ]
          },
          "repeat-system": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836683273315,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999704957008362,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999396800994873,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998784065246582,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997159242630005,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994155764579773,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999840259552002,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999700784683228,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999334812164307,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998892545700073,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997441172599792,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9995907545089722,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881982803345,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999828338623047,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999657273292542,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999231100082397,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998571872711182,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996629357337952,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994845986366272,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880194664001,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999811053276062,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999583959579468,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999058842658997,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998243451118469,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996048808097839,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993204474449158,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999876618385315,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999793767929077,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999492168426514,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999882698059082,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997798800468445,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995233416557312,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991335868835449,
                    "name": "h6",
                    "order": 6
                  }
                ],
                "step": 152900
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836683273315,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999704957008362,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999396800994873,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998784065246582,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997159242630005,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994155764579773,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986107349395752,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970688223838806,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929354786872864,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985227108001709,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9650446772575378,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.926563024520874,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999831914901733,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999628663063049,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999151825904846,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999826967716217,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995973110198975,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991797804832458,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981237053871155,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964298605918884,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9916902780532837,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9854190349578857,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9680813550949097,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9497920870780945,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999820590019226,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999585151672363,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999068975448608,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999798059463501,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995145201683044,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990473985671997,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977627396583557,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959222674369812,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9906383156776428,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9840281009674072,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9659903645515442,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9509439468383789,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999811053276062,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999571442604065,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999013543128967,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997971057891846,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995208978652954,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990772008895874,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.99790358543396,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960460066795349,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9910587072372437,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9850650429725647,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9683007597923279,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9566783308982849,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999808669090271,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999561905860901,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999021291732788,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997810125350952,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994930624961853,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990007877349854,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976843595504761,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958409070968628,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9906029105186462,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9846235513687134,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9674005508422852,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9568272233009338,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 152900
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp02",
      "reasons": [
        "the main/control endpoint is unsettled",
        "the repeat-system/arm endpoint is unsettled",
        "the repeat-system/control endpoint is unsettled",
        "the repeat-seed/arm endpoint is unsettled"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    },
    "d8": {
      "arm": "d8",
      "cases": {
        "main": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "settled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.03344629454651585,
              "tier": 1
            },
            "control": {
              "E": 0.03482590188705743,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": false,
          "reasons": [
            "the effect is below the registered twenty-percent line with no matching tier change"
          ],
          "relative_E_effect": 0.03961440381402703,
          "tier_direction": "unchanged"
        },
        "repeat-seed": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.01715509046203649,
              "tier": 1
            },
            "control": {
              "E": 0.08081264163459871,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.787717736791668,
          "tier_direction": "unchanged"
        },
        "repeat-system": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.022799860938189802,
              "tier": 1
            },
            "control": {
              "E": 0.06749088823348984,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.6621786801899546,
          "tier_direction": "unchanged"
        }
      },
      "confirmation": "unsettled",
      "control": "d12",
      "descriptive": {
        "adjacent_time_similarity": {
          "main": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999837279319763,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999697208404541,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999352097511292,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998775124549866,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999712347984314,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999390184879303,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985547661781311,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9969659447669983,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999833703041077,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999591112136841,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999096393585205,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998154044151306,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995670318603516,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991677403450012,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981472492218018,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9966184496879578,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836087226868,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999589920043945,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999092817306519,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998242259025574,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995966553688049,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999248206615448,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982942938804626,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9969724416732788,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999828934669495,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999594688415527,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999112486839294,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998270273208618,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996085166931152,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992854595184326,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9984181523323059,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9975581169128418,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999827742576599,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999563097953796,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999004006385803,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997996687889099,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995405077934265,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992218017578125,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.99830162525177,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.99741530418396,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 152900
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999837279319763,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999697208404541,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999352097511292,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998775124549866,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999712347984314,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999390184879303,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985547661781311,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9969659447669983,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9927595257759094,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9844540953636169,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9629203677177429,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9224951267242432,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999832510948181,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999594688415527,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999092817306519,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997974634170532,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995214939117432,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990511536598206,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997784435749054,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957220554351807,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9901578426361084,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9823592305183411,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.961142361164093,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9380327463150024,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999828338623047,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999569058418274,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999046921730042,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997938871383667,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995269775390625,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.99898761510849,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976747035980225,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9956965446472168,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9902918338775635,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9833380579948425,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9641813039779663,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.950472354888916,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999818801879883,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999598264694214,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999111294746399,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998100399971008,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995549321174622,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991307258605957,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979795813560486,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9962527751922607,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917433857917786,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9865732192993164,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9714349508285522,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9636873602867126,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987781047821,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815821647644,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999961256980896,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999112486839294,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998151659965515,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995825290679932,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991995096206665,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981447458267212,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996797502040863,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9927946329116821,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9882802963256836,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9751591682434082,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9672127962112427,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 152900
              }
            ]
          },
          "repeat-seed": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999827742576599,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999688863754272,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999354481697083,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999873161315918,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999718189239502,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993919730186462,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985952973365784,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.997002363204956,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999847412109375,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999586343765259,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999040365219116,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998147487640381,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995729923248291,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992263317108154,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982595443725586,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9969871640205383,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999839067459106,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999669194221497,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999241828918457,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998491406440735,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996576905250549,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993747472763062,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986397624015808,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9977055788040161,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999831318855286,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999593496322632,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999052882194519,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998201131820679,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996104836463928,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992596507072449,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9983482956886292,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9973083734512329,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999981701374054,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999583959579468,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999098181724548,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998214244842529,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995882511138916,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992741346359253,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9983866810798645,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9975599646568298,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 152900
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999827742576599,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999688863754272,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999354481697083,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999873161315918,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999718189239502,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993919730186462,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985952973365784,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.997002363204956,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9928239583969116,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9847432971000671,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9634863138198853,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.925688624382019,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999824166297913,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999611973762512,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999170899391174,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998269081115723,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995925426483154,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991812705993652,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9980418682098389,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964726567268372,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9920085072517395,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9859246611595154,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9688183665275574,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9535370469093323,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999820590019226,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999577403068542,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999076128005981,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997918605804443,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995185136795044,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990800619125366,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997891366481781,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960888624191284,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9912503957748413,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9848934412002563,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9671668410301208,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9535211324691772,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999806880950928,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999575018882751,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999062418937683,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998205304145813,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995840787887573,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992190599441528,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982219338417053,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996813952922821,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.992933988571167,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9886007308959961,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9759966135025024,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9676738381385803,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999808073043823,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999955952167511,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998968243598938,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997695684432983,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999484658241272,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989774823188782,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997639536857605,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958228468894958,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.990756094455719,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9856263995170593,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9704390168190002,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9641836881637573,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 152900
              }
            ]
          },
          "repeat-system": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836683273315,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999704957008362,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999396800994873,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998784065246582,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997159242630005,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994155764579773,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986107349395752,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970688223838806,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999829530715942,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999637603759766,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999194145202637,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998425245285034,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999626100063324,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993156790733337,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9984166026115417,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970910549163818,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999834299087524,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999623894691467,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999099373817444,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998265504837036,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996059536933899,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993029832839966,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985170364379883,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9975638389587402,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880194664001,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999814629554749,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999610781669617,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999090433120728,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998332262039185,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995976686477661,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993191361427307,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985458254814148,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9977155923843384,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880790710449,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999814629554749,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999565482139587,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998990297317505,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997987151145935,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995457530021667,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992395043373108,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9983389973640442,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9973251819610596,
                    "name": "h8",
                    "order": 8
                  }
                ],
                "step": 152900
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836683273315,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999704957008362,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999396800994873,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998784065246582,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997159242630005,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994155764579773,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986107349395752,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970688223838806,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929354786872864,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985227108001709,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9650446772575378,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.926563024520874,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999831914901733,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999628663063049,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999151825904846,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999826967716217,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995973110198975,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991797804832458,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981237053871155,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964298605918884,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9916902780532837,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9854190349578857,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9680813550949097,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9497920870780945,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38225
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999820590019226,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999585151672363,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999068975448608,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999798059463501,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995145201683044,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990473985671997,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977627396583557,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959222674369812,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9906383156776428,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9840281009674072,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9659903645515442,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9509439468383789,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 76450
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999811053276062,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999571442604065,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999013543128967,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997971057891846,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995208978652954,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990772008895874,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.99790358543396,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960460066795349,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9910587072372437,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9850650429725647,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9683007597923279,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9566783308982849,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 114675
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999879002571106,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999808669090271,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999561905860901,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999021291732788,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997810125350952,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994930624961853,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990007877349854,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976843595504761,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958409070968628,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9906029105186462,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9846235513687134,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9674005508422852,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9568272233009338,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 152900
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp02",
      "reasons": [
        "the main/control endpoint is unsettled",
        "the repeat-system/arm endpoint is unsettled",
        "the repeat-system/control endpoint is unsettled"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    }
  },
  "dependent_launch_allowed": true,
  "experiment": "exp02",
  "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
  "predictions_comparison": {
    "d2": {
      "case_directions": {
        "main": "worsening",
        "repeat-seed": "worsening",
        "repeat-system": "worsening"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, shallower depth improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    },
    "d4": {
      "case_directions": {
        "main": "improvement",
        "repeat-seed": "improvement",
        "repeat-system": "worsening"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, shallower depth improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    },
    "d6": {
      "case_directions": {
        "main": "worsening",
        "repeat-seed": "improvement",
        "repeat-system": "improvement"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, shallower depth improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    },
    "d8": {
      "case_directions": {
        "main": "improvement",
        "repeat-seed": "improvement",
        "repeat-system": "improvement"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, shallower depth improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    }
  },
  "proposed_change": null,
  "roadmap_comparison": "each contrast's confirmation label is read against the committed prediction table; the roadmap's next experiment proceeds only when this review allows the dependent launch",
  "schema": "phase67-review/v1",
  "scope49_disposition": "none"
}
```
