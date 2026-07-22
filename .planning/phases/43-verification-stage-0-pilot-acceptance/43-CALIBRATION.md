# Phase 43 ACC-05 Stage-0 pilot calibration

**Status:** `AWAITING-OWNER-RATIFICATION`  
**Pilot date:** 2026-07-22  
**Decision boundary:** This document reports observations and candidate options. It does not ratify or persist R-1 or R-2.

## Pilot contract

Three ordinary real-data runs used the Phase 41 smoke configuration with only the seed and unique run name changed. Each run used the admitted dataset, MPS/float32, 300 Adam steps, the owner-ratified D4-a wall-clock checkpoint ceiling of `120.0` seconds, and the values present before this calibration:

- `run.guards.loss_explosion_ceiling = 100000000000.0`
- `run.guards.disk_floor_fraction = 0.05`
- `run.guards.memory_watermark_fraction = 0.7`
- `run.recover_retries = 0`

The complete machine-readable evidence and SHA-256 identities are in [`evidence/pilot/README.md`](evidence/pilot/README.md). The run directories remain local execution artifacts under `runs/stage0-pilot-seed{41,42,43}/`.

## Raw observations

| Seed | Run path | Terminal disposition | Steps finite | Final total loss | Peak total loss | Final validation | Trend | Peak driver / current memory | Wall clock | Final seconds/step EMA |
| ---: | --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| 41 | `runs/stage0-pilot-seed41` | `finished` | 300 / 300 | 566643776.0 | 6081173504.0 | 463856672.0 | worsening | 356581376 / 156940544 bytes | 201.914951 s | 0.09881577425706371 |
| 42 | `runs/stage0-pilot-seed42` | `finished` | 300 / 300 | 650443456.0 | 3734660096.0 | 78489008.0 | improving | 356581376 / 156940544 bytes | 197.683446 s | 0.09758273411582492 |
| 43 | `runs/stage0-pilot-seed43` | `finished` | 300 / 300 | 150720096.0 | 3832843264.0 | 1851546240.0 | worsening | 356581376 / 156940544 bytes | 195.713358 s | 0.09618073375458501 |

All three runs emitted `stage-0-init.pt`, steps 100/200/300 checkpoints, `best.pt`, `latest.pt`, and the wall-clock checkpoint. No seed emitted a failure bundle or a non-finite step. No seed was excluded; a diverged seed would remain in this table and the band.

The wall-clock checkpoint is expected despite each process taking about 196–202 seconds overall: D4-a controls the checkpoint interval inside the admitted training portion, not total process initialization and shutdown time.

## Defined spread calculation

For every reported metric, the absolute span is `max(seed values) - min(seed values)`. The relative span is `(max - min) / median(seed values)`. No values are rounded before the calculation.

| Metric | Minimum | Median | Maximum | Absolute span | Relative span |
| --- | ---: | ---: | ---: | ---: | ---: |
| Final total loss | 150720096.0 | 566643776.0 | 650443456.0 | 499723360.0 | 0.8819003775663107 |
| Final validation loss | 78489008.0 | 463856672.0 | 1851546240.0 | 1773057232.0 | 3.8224247683129153 |
| Peak total loss | 3734660096.0 | 3832843264.0 | 6081173504.0 | 2346513408.0 | 0.612212200284744 |
| Wall clock seconds | 195.713358 | 197.683446 | 201.914951 | 6.201593000000003 | 0.03137133192224908 |
| Final seconds/step EMA | 0.09618073375458501 | 0.09758273411582492 | 0.09881577425706371 | 0.0026350405024787027 | 0.027003142782933975 |

## Confidence

**Overall confidence: HIGH.** Three distinct seeds completed the same admitted-data configuration with 300/300 finite steps and intact evidence bundles. This is sufficient for the requested seed-band calibration. It is not a convergence claim: final validation relative span is `3.8224247683129153`, and two final validation trends were worsening.

Field-level limits matter:

- Loss and retry evidence is direct: every step loss and recovery disposition is recorded.
- Memory evidence is direct for MPS driver/current bytes on this 25769803776-byte machine.
- Disk evidence is weak: the guards did not trip and the immediate post-run free-space snapshot was `680716528 / 971298980 = 0.7008310952823198`, but the runtime schema does not record the minimum free-space fraction over the run.

## Owner decision candidates

These options are candidates, not defaults. The owner must provide the exact four values before Task 3 changes supported configuration.

### R-1: `run.guards.loss_explosion_ceiling`

| Option | Exact value | Evidence link and tradeoff |
| --- | ---: | --- |
| A — retain prior ratification | `100000000000.0` | The largest observed total loss was `6081173504.0` (seed 41), so this is exactly `16.444194518413795 ×` the pilot peak. It preserves the existing owner-ratified threshold. |
| B — exact 10× pilot peak | `60811735040.0` | `10 × 6081173504.0`; tighter than A without opaque rounding, but calibrated only to these three MPS/float32 seeds. |

### R-1: `run.guards.disk_floor_fraction`

| Option | Exact value | Evidence link and tradeoff |
| --- | ---: | --- |
| A — retain provisional value | `0.05` | No disk guard tripped. Immediate post-run free fraction was `0.7008310952823198`, or `14.016621905646396 ×` this floor. The pilot did not approach disk pressure, so it provides no defensible evidence-derived tightening alternative. |

### R-1: `run.guards.memory_watermark_fraction`

| Option | Exact value | Evidence link and tradeoff |
| --- | ---: | --- |
| A — retain provisional value | `0.7` | Peak driver memory was `356581376 / 25769803776 = 0.013837178548177084`; the current watermark is `50.58834773019665 ×` that observed fraction. This preserves broad headroom. |
| B — exact 10× pilot peak fraction | `0.13837178548177084` | `10 × 356581376 / 25769803776`; tighter and fully derived, but hardware- and workload-specific and not exercised near the boundary. |

### R-2: `run.recover_retries`

| Option | Exact value | Evidence link and tradeoff |
| --- | ---: | --- |
| A — retain zero retries | `0` | All three runs finished without a recovery attempt. This is the only value directly supported by the pilot and preserves immediate halt semantics. |
| B — permit one retry | `1` | A bounded operational policy option if the owner wants one recovery opportunity, but the pilot observed no recovery path and therefore does not demonstrate benefit. |

## Ratification record

**Owner sign-off:** pending.  
**Exact R-1 values:** pending.  
**Exact R-2 value:** pending.  
**Persistence status:** no R-1/R-2 value has been changed by this calibration task.
