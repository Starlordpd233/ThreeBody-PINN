# EXP-02 depth ladder — Budget

The cost-only common-update budget derived from every committed
timing row of this experiment (67-04's phase67_budget). No score,
loss, tier or cosine value is read or appears here.

```json phase67-budget
{
  "common_optimizer_steps": 152900,
  "experiment": "exp02",
  "experiment_projected_seconds": {
    "exp02": 25466.885162053262
  },
  "inputs": {
    "cap_seconds": 3540.0,
    "min_steps": 300,
    "rate_margin": 0.25,
    "rows": {
      "exp02|d12|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 3645991,
        "published_bytes": 3631175,
        "residual_seconds": 4.63916616741335,
        "seconds_per_step": 0.013844172284007073,
        "warmup_seconds": 2.8137106725480407
      },
      "exp02|d12|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 3645995,
        "published_bytes": 3631179,
        "residual_seconds": 4.22864027362084,
        "seconds_per_step": 0.013344091942184605,
        "warmup_seconds": 2.9160845322185196
      },
      "exp02|d12|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 3645973,
        "published_bytes": 3631157,
        "residual_seconds": 4.882119414978661,
        "seconds_per_step": 0.013682186304184142,
        "warmup_seconds": 2.7623183648101985
      },
      "exp02|d2|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 1002496,
        "published_bytes": 987680,
        "residual_seconds": 3.6370029417448677,
        "seconds_per_step": 0.005391843730176333,
        "warmup_seconds": 1.1276836600154638
      },
      "exp02|d2|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 1002506,
        "published_bytes": 987690,
        "residual_seconds": 5.233246525167488,
        "seconds_per_step": 0.005570797606895212,
        "warmup_seconds": 2.229468658915721
      },
      "exp02|d2|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 1001948,
        "published_bytes": 987132,
        "residual_seconds": 4.004039815219585,
        "seconds_per_step": 0.0044467226112028585,
        "warmup_seconds": 0.9931296575232409
      },
      "exp02|d4|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 1530996,
        "published_bytes": 1516180,
        "residual_seconds": 4.628265113802627,
        "seconds_per_step": 0.006785594720975496,
        "warmup_seconds": 1.4353572081890889
      },
      "exp02|d4|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 1531010,
        "published_bytes": 1516194,
        "residual_seconds": 4.860785375407431,
        "seconds_per_step": 0.007065251749416347,
        "warmup_seconds": 1.5926984573015943
      },
      "exp02|d4|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 1530722,
        "published_bytes": 1515906,
        "residual_seconds": 3.915464315970894,
        "seconds_per_step": 0.0066160626892815344,
        "warmup_seconds": 1.3615619927295484
      },
      "exp02|d6|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 2059854,
        "published_bytes": 2045038,
        "residual_seconds": 4.3987046658294275,
        "seconds_per_step": 0.008296350374643225,
        "warmup_seconds": 1.816163833369501
      },
      "exp02|d6|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 2059845,
        "published_bytes": 2045029,
        "residual_seconds": 4.761323400889523,
        "seconds_per_step": 0.008752314894634764,
        "warmup_seconds": 1.8199016204453073
      },
      "exp02|d6|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 2059916,
        "published_bytes": 2045100,
        "residual_seconds": 4.466616451914888,
        "seconds_per_step": 0.008283501315279863,
        "warmup_seconds": 1.7714087317581289
      },
      "exp02|d8|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 2588652,
        "published_bytes": 2573836,
        "residual_seconds": 3.9734016915317625,
        "seconds_per_step": 0.010108226689975708,
        "warmup_seconds": 2.156844576529693
      },
      "exp02|d8|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 2588664,
        "published_bytes": 2573848,
        "residual_seconds": 4.808403858740348,
        "seconds_per_step": 0.010184268395998515,
        "warmup_seconds": 2.1646789532969706
      },
      "exp02|d8|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 2588651,
        "published_bytes": 2573835,
        "residual_seconds": 4.8134387757163495,
        "seconds_per_step": 0.010319278690614737,
        "warmup_seconds": 2.0930675746058114
      }
    },
    "size_ceiling_bytes": 9437184,
    "step_quantum": 100,
    "target_seconds": 2655.0,
    "time_fraction": 0.75
  },
  "loss_trace_stride": 153,
  "measured_steps": 152700,
  "per_row_projection_seconds": {
    "exp02|d12|hierarchical/gold/1632|41|10.0": 2654.3144412172737,
    "exp02|d12|hierarchical/gold/1632|42|10.0": 2558.4503877894717,
    "exp02|d12|hierarchical/gold/851|42|10.0": 2623.6857867205003,
    "exp02|d2|hierarchical/gold/1632|41|10.0": 1035.678891425939,
    "exp02|d2|hierarchical/gold/1632|42|10.0": 1072.9949017365698,
    "exp02|d2|hierarchical/gold/851|42|10.0": 854.8086714525394,
    "exp02|d4|hierarchical/gold/1632|41|10.0": 1303.38175729643,
    "exp02|d4|hierarchical/gold/1632|42|10.0": 1358.098668376172,
    "exp02|d4|hierarchical/gold/851|42|10.0": 1270.1460597667958,
    "exp02|d6|hierarchical/gold/1632|41|10.0": 1592.432307402399,
    "exp02|d6|hierarchical/gold/1632|42|10.0": 1680.4199096655377,
    "exp02|d6|hierarchical/gold/851|42|10.0": 1590.0652774976604,
    "exp02|d8|hierarchical/gold/1632|41|10.0": 1938.5459876262112,
    "exp02|d8|hierarchical/gold/1632|42|10.0": 1954.1922898965274,
    "exp02|d8|hierarchical/gold/851|42|10.0": 1979.6698241832346
  },
  "phase_cost_ledger": {
    "cap_seconds": 3540.0,
    "experiments": [
      {
        "basis": "measured_projection",
        "declared_runs": 15,
        "experiment": "exp02",
        "note": "measured timing rows; update this ledger with the measured projections before each science launch",
        "planned_seconds": 25466.885162053262
      }
    ]
  },
  "schema": "phase67-budget/v1",
  "score_cadence": [
    76450,
    114675,
    152900
  ],
  "similarity_cadence": [
    0,
    38225,
    76450,
    114675,
    152900
  ],
  "timing_evidence": {
    "rows": [
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/main-1632-s42/d2/record.json",
        "sha256": "ff6171b75e405f83b47ad45a3664bd5b1f64b726ea7f0c78ce02d96d95a801a6"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/main-1632-s42/d4/record.json",
        "sha256": "336cff1e52e3ede073525ece3bee498488efbea434bb765756bc193b910e664b"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/main-1632-s42/d6/record.json",
        "sha256": "475a105e28b0e9752182703eb679b89ba8b12d248f4a8caf77d3ff15361c0984"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/main-1632-s42/d8/record.json",
        "sha256": "136a4a258a4daaf095edcf1c425fb74d94377819a6f1f88ea185b8ca1fc85805"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/main-1632-s42/d12/record.json",
        "sha256": "042403551373c5396701993908dd0f67135525eac1ee2f2fcde96457d63e8dde"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/repeat-851-s42/d2/record.json",
        "sha256": "c70dba2e125ac36e167a417018fc740088ee4facdd98d3ece49bbd594d45af40"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/repeat-851-s42/d4/record.json",
        "sha256": "5123268ec311a796907b7131163e47bcbb1a85267c3cca4aa75f1e155dde0705"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/repeat-851-s42/d6/record.json",
        "sha256": "b7e82be2cdae2c63852458e90cbbbb7e0e483e8b61f456925801914ed28ef3b4"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/repeat-851-s42/d8/record.json",
        "sha256": "45a8ad33218e4d037b73ec241140f6458c76680d66f7bc5fe5c9ebb5a9de2390"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/repeat-851-s42/d12/record.json",
        "sha256": "9caa6947ba6d6192254a351e8a850f6b4e8b4beef1ecf0ef8afb657daab40851"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/repeat-1632-s41/d2/record.json",
        "sha256": "804b91f281ad50bd110919205e1a7720ae2c08af795d24f5395dc5d0cf767051"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/repeat-1632-s41/d4/record.json",
        "sha256": "826aa7ce1293300ada571f2c0e164f97bd28f56bf0dbcc1ba84a3c67ae0c4aad"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/repeat-1632-s41/d6/record.json",
        "sha256": "d1df0b6ec039da13a8166d1f9d315de1c5d38b8a89d938ca6f154f5fa5c42ec3"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/repeat-1632-s41/d8/record.json",
        "sha256": "dda113043d81a3fdd5efdc4bbbec275433f4323a903b3fe860c14491f0928e61"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp02/timing/repeat-1632-s41/d12/record.json",
        "sha256": "d8f8cafe4e30154ecc2ff373ac7c641eaf6f360b3c55674161ae98e6d862b3a6"
      }
    ]
  },
  "timing_evidence_digests": {
    "exp02|d12|hierarchical/gold/1632|41|10.0": null,
    "exp02|d12|hierarchical/gold/1632|42|10.0": null,
    "exp02|d12|hierarchical/gold/851|42|10.0": null,
    "exp02|d2|hierarchical/gold/1632|41|10.0": null,
    "exp02|d2|hierarchical/gold/1632|42|10.0": null,
    "exp02|d2|hierarchical/gold/851|42|10.0": null,
    "exp02|d4|hierarchical/gold/1632|41|10.0": null,
    "exp02|d4|hierarchical/gold/1632|42|10.0": null,
    "exp02|d4|hierarchical/gold/851|42|10.0": null,
    "exp02|d6|hierarchical/gold/1632|41|10.0": null,
    "exp02|d6|hierarchical/gold/1632|42|10.0": null,
    "exp02|d6|hierarchical/gold/851|42|10.0": null,
    "exp02|d8|hierarchical/gold/1632|41|10.0": null,
    "exp02|d8|hierarchical/gold/1632|42|10.0": null,
    "exp02|d8|hierarchical/gold/851|42|10.0": null
  },
  "warmup_steps": 200,
  "whole_run_cap_seconds": 3540.0
}
```

- common optimizer steps: 152900
- warmup steps: 200
- whole-run cap: 3540 seconds

The science registrations are frozen from this budget before any
science run; the timing prediction page is unchanged by this page.
