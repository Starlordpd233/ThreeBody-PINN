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
