# Standard Quasi-Random ICs Not in Gold Standard

Generated: 2026-03-18

## Summary

- `ic_standard_quasi_random/` contains **2,749** ICs.
- `ic_standard_quasi_random_for_gold_standard/` contains **2,565** ICs.
- All 2,565 gold-standard ICs are a **byte-identical subset** of the standard ICs
  (differing only in filename prefix: `ic_standard_` vs `ic_standard_gold_`).
- **184 ICs** exist in the standard folder but have no gold-standard counterpart.

These 184 ICs were simulated at standard Brutus resolution but were never
selected for gold-standard (higher temporal resolution, `dt_out=0.01`) re-simulation.

## The 184 IDs

Listed below are the numeric IDs whose IC files (`ic_standard_XXXX.txt`) appear
in `ic_standard_quasi_random/` but have no matching file in
`ic_standard_quasi_random_for_gold_standard/`.

```
0038  0042  0049  0138  0142  0149  0238  0242  0249  0338
0342  0349  0438  0442  0449  0504  0540  0555  0557  0579
0585  0586  0638  0642  0649  0704  0740  0755  0757  0779
0785  0786  0838  0842  0849  0904  0940  0955  0957  0979
0985  0986  1023  1043  1055  1061  1127  1130  1144  1148
1150  1154  1155  1191  1238  1242  1338  1342  1426  1440
1455  1457  1479  1485  1486  1538  1542  1549  1604  1640
1655  1657  1679  1685  1686  1702  1723  1743  1755  1761
1827  1830  1840  1844  1848  1850  1854  1855  1891  1909
1941  1956  1958  1975  2004  2039  2056  2060  2107  2110
2127  2136  2164  2172  2206  2219  2274  2277  2281  2351
2359  2382  2386  2402  2439  2455  2460  2495  2538  2542
2604  2640  2655  2657  2679  2685  2686  2723  2743  2755
2761  2827  2830  2844  2848  2850  2854  2855  2909  2941
2956  2958  3004  3039  3056  3060  3107  3110  3136  3172
3219  3277  3359  3362  3368  3382  3386  3402  3439  3455
3460  3538  3542  3604  3640  3655  3657  3679  3685  3686
3723  3743  3755  3761  3827  3830  3844  3848  3850  3854
3855  3891  3941  3958
```

Total: **184 IDs**
