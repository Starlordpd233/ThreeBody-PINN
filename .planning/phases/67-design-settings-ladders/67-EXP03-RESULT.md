# Phase 67 Experiment Result — EXP-03

The review's complete reading: every endpoint's frozen values, the
matched contrasts, the prediction and roadmap comparison, and the
SCOPE-49 disposition. GAP-59-08 stays explicit: E is the frozen
scorecard's position-error score; no energy bar is adjudicated here.

```json phase67-review
{
  "budget_steps": 155100,
  "confirmation": {
    "confirmed": [
      {
        "arm": "lr1e-3",
        "confirmation": "confirmed-worsening"
      }
    ],
    "contrasts": {
      "lr1e-3": {
        "arm": "lr1e-3",
        "cases": {
          "main": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 1.4551508979130539,
                "tier": 0
              },
              "control": {
                "E": 0.040691019043637484,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 34.76098441654986,
            "tier_direction": "worsened"
          },
          "repeat-seed": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 1.4024505668393392,
                "tier": 0
              },
              "control": {
                "E": 0.03491785615016659,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 39.16428044173176,
            "tier_direction": "worsened"
          },
          "repeat-system": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 1.5639231628850137,
                "tier": 0
              },
              "control": {
                "E": 0.09549573839491703,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 15.376889578229147,
            "tier_direction": "worsened"
          }
        },
        "confirmation": "confirmed-worsening",
        "control": "lr1e-4",
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
                      "adjacent_cosine_mean": 0.9998746514320374,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9993506669998169,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9911553859710693,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9551479816436768,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.6514114737510681,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.21333256363868713,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.0010502415243536234,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": -0.0016552109736949205,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.0009392162319272757,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": -0.0014964346773922443,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.00045337845222093165,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.0022931608837097883,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": -0.005452209617942572,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9997854232788086,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9982057809829712,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9558442831039429,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.7303365468978882,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.03642311692237854,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.0006389201735146344,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": -0.0012985869543626904,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": -0.0021475644316524267,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.0007950661238282919,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.0003432423691265285,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": -0.0036402433179318905,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.0002082827122649178,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": -0.0053091393783688545,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999680757522583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9966989159584045,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.8956877589225769,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.4491543471813202,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": -0.0012277752393856645,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": -0.002444631652906537,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": -0.0014381337678059936,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": -0.0021932946983724833,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": -0.0019786888733506203,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.00017463386757299304,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.000519188295584172,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.001347001176327467,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": -0.002154938643798232,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9996010065078735,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9946120381355286,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.7940441370010376,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.24798113107681274,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": -0.004531601909548044,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.00028374436078593135,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": -2.3113667339202948e-05,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": -0.0008456743089482188,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": -0.00393932219594717,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": -0.0018416013335809112,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 1.4812409972364549e-05,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.0013676033122465014,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": -0.0018080566078424454,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999093413352966,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997975826263428,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995217323303223,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990523457527161,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977886080741882,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957399964332581,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9901987910270691,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9825018048286438,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9615046381950378,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9389911890029907,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
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
                      "adjacent_cosine_mean": 0.9999570250511169,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999048113822937,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997943043708801,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999528169631958,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989920854568481,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976863861083984,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957477450370789,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9904364943504333,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9838588237762451,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9654865860939026,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9542497396469116,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999981164932251,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999582767486572,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999063611030579,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999798595905304,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995154738426208,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990686774253845,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978678226470947,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959396123886108,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9909234046936035,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9848374724388123,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9675301313400269,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9567607641220093,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987781047821,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815225601196,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999613165855408,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999911367893219,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998155832290649,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995834827423096,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992039203643799,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981580972671509,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968430995941162,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929201602935791,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9886854290962219,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9761550426483154,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9698630571365356,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9998865127563477,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9993888139724731,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9925609230995178,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9621824026107788,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.6812936067581177,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.22548463940620422,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.003008781000971794,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": -0.003709736978635192,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": -0.0020381989888846874,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": -0.0018530855886638165,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": -0.0055136545561254025,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.004028624389320612,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": -0.002525984775274992,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9998068809509277,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9983575344085693,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9478579163551331,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.7083415389060974,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.03214969485998154,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": -0.0017908815061673522,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": -0.001739039085805416,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.001917719142511487,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": -0.0022463116329163313,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": -0.0030226316303014755,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": -0.0013616791693493724,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.0009448858327232301,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.0016628482844680548,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9997245073318481,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9969354867935181,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.8859174251556396,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.438077449798584,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": -0.00019763672025874257,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.0028387673664838076,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": -0.0005180435837246478,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.00104482879396528,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": -0.0012270776787772775,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": -0.0014750347472727299,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": -0.0014021858805790544,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.0036816962528973818,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": -0.0024859027471393347,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9996522068977356,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9954362511634827,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.8172602653503418,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.2727125287055969,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": -0.0028302522841840982,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": -0.003926251083612442,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": -0.003322550328448415,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.0009302963153459132,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.0027217187453061342,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.0042549483478069305,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": -0.002858209190890193,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.002757567912340164,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.0025910737458616495,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999223351478577,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999829113483429,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995903372764587,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992087483406067,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981492757797241,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964054226875305,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917572140693665,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9849987030029297,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9668107628822327,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9471333026885986,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
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
                      "adjacent_cosine_mean": 0.9999577403068542,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999076724052429,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997920989990234,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995192885398865,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990827441215515,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978979229927063,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961216449737549,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991334080696106,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9851789474487305,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.967799961566925,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9550234079360962,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
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
                      "adjacent_cosine_mean": 0.9999063611030579,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998209476470947,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999584972858429,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992243647575378,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982348084449768,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968690872192383,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9930570125579834,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9889869093894958,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9768524169921875,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9696897268295288,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999876618385315,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999806880950928,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999955952167511,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999062418937683,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997995495796204,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995240569114685,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990931153297424,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978749752044678,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961003661155701,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9912582635879517,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9861302971839905,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9709347486495972,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9624550342559814,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9998959302902222,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9994467496871948,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9900456666946411,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9499315023422241,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.6414554119110107,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.20199018716812134,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.0007150886231102049,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": -0.0018872771179303527,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": -0.0003220918879378587,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 5.88443290325813e-05,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": -0.0012761311372742057,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.0033324873074889183,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": -0.0015223019290715456,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9998219013214111,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9984787702560425,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9586173295974731,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.7504780292510986,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.04559456184506416,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": -3.0929713830119e-05,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": -0.00309168198145926,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": -0.0014778099721297622,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.00019037455786019564,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": -0.0013096180045977235,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": -0.0021393278148025274,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.0025605210103094578,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.00022530216665472835,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9997442364692688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9972327947616577,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9117815494537354,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.49665749073028564,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": -0.004347582813352346,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": -0.002915716264396906,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.0009228203562088311,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": -0.00175646529532969,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.0022462911438196898,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": -0.000808694981969893,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": -0.0009383969590999186,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.0039045452140271664,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": -0.002674757968634367,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9996750354766846,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9957952499389648,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.8265535831451416,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.28348952531814575,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": -0.003065342316403985,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.00017847084382083267,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": -0.00012626945681404322,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": -0.0009415843524038792,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": -0.0008999562123790383,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.0032382486388087273,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": -0.0029010979924350977,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.0003410322533454746,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": -0.0019255464430898428,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9998270273208618,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995975494384766,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991806745529175,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981272220611572,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964404106140137,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917224049568176,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9855460524559021,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.968417227268219,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9510875940322876,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
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
                      "adjacent_cosine_mean": 0.9999069571495056,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997982382774353,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995154738426208,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990515112876892,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977757334709167,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959514737129211,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9907388687133789,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9843775629997253,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9668378233909607,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9533820748329163,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
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
                      "adjacent_cosine_mean": 0.9999014735221863,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997973442077637,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995213747024536,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990800023078918,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997909665107727,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960767030715942,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991156816482544,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985405683517456,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9690045118331909,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9582934975624084,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880194664001,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999808073043823,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999561905860901,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999022483825684,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997812509536743,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994936585426331,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990067481994629,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977021217346191,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.995904803276062,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9907554984092712,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9851889610290527,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.968751847743988,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9597102403640747,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp03",
        "reasons": [],
        "scope_disposition": {
          "dependent_launch_allowed": false,
          "reason": "a refuted lead: the registered hypothesis is contradicted on all three cases, so a concrete owner proposal under SCOPE-49 is recorded before dependent work continues",
          "scope49_disposition": "proposal-pending"
        }
      },
      "lr1e-5": {
        "arm": "lr1e-5",
        "cases": {
          "main": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.2097428875427889,
                "tier": 0
              },
              "control": {
                "E": 0.040691019043637484,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 4.1545253098198005,
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
                "E": 0.18744816464300104,
                "tier": 0
              },
              "control": {
                "E": 0.03491785615016659,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 4.368260979049446,
            "tier_direction": "worsened"
          },
          "repeat-system": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.21207523896683939,
                "tier": 0
              },
              "control": {
                "E": 0.09549573839491703,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 1.2207822310333334,
            "tier_direction": "worsened"
          }
        },
        "confirmation": "unsettled",
        "control": "lr1e-4",
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
                      "adjacent_cosine_mean": 0.9999837279319763,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999698400497437,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999356865882874,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998800158500671,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997189044952393,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994206428527832,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986338019371033,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9972665905952454,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9936047792434692,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9875799417495728,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9706918001174927,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9464858770370483,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
                },
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
                      "adjacent_cosine_mean": 0.9999698400497437,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999359250068665,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999880850315094,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997216463088989,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994302988052368,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986612796783447,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.997359037399292,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9938575625419617,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.988423764705658,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9727455973625183,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9524453282356262,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
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
                      "adjacent_cosine_mean": 0.9999698996543884,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999936044216156,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998814463615417,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997234344482422,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999436616897583,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986796379089355,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9974161982536316,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9940141439437866,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.988919198513031,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9739335179328918,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9558897614479065,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
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
                      "adjacent_cosine_mean": 0.9999699592590332,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999362230300903,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998819828033447,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997252225875854,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994419813156128,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986953735351562,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9974596500396729,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9941338896751404,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9892734289169312,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9747949838638306,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9583056569099426,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999093413352966,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997975826263428,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995217323303223,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990523457527161,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977886080741882,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957399964332581,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9901987910270691,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9825018048286438,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9615046381950378,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9389911890029907,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
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
                      "adjacent_cosine_mean": 0.9999570250511169,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999048113822937,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997943043708801,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999528169631958,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989920854568481,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976863861083984,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957477450370789,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9904364943504333,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9838588237762451,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9654865860939026,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9542497396469116,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999981164932251,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999582767486572,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999063611030579,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999798595905304,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995154738426208,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990686774253845,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978678226470947,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959396123886108,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9909234046936035,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9848374724388123,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9675301313400269,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9567607641220093,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987781047821,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815225601196,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999613165855408,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999911367893219,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998155832290649,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995834827423096,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992039203643799,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981580972671509,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968430995941162,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929201602935791,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9886854290962219,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9761550426483154,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9698630571365356,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999827146530151,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999691247940063,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999936044216156,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998762011528015,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997261166572571,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994266629219055,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986933469772339,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9973498582839966,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9937376379966736,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9878357648849487,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9714356660842896,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9489167928695679,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999827146530151,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999691247940063,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999362826347351,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998772144317627,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997286796569824,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994363784790039,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9987202882766724,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9974389672279358,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9939811825752258,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9886475205421448,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9735094308853149,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.954601526260376,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999826550483704,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999691247940063,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999365210533142,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998779296875,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997305870056152,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994428753852844,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9987386465072632,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9974983930587769,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9941413402557373,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9891550540924072,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9748091101646423,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9581443071365356,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999826550483704,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999691247940063,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999366402626038,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998785257339478,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997321963310242,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994481205940247,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.998753547668457,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9975417852401733,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9942600131034851,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9895209670066833,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9757128953933716,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9606232643127441,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999223351478577,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999829113483429,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995903372764587,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992087483406067,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981492757797241,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964054226875305,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917572140693665,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9849987030029297,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9668107628822327,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9471333026885986,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
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
                      "adjacent_cosine_mean": 0.9999577403068542,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999076724052429,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997920989990234,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995192885398865,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990827441215515,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978979229927063,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961216449737549,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991334080696106,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9851789474487305,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.967799961566925,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9550234079360962,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
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
                      "adjacent_cosine_mean": 0.9999063611030579,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998209476470947,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999584972858429,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992243647575378,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982348084449768,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968690872192383,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9930570125579834,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9889869093894958,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9768524169921875,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9696897268295288,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999876618385315,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999806880950928,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999955952167511,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999062418937683,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997995495796204,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995240569114685,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990931153297424,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978749752044678,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961003661155701,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9912582635879517,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9861302971839905,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9709347486495972,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9624550342559814,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999706745147705,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999401569366455,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998800158500671,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997210502624512,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994403123855591,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986776113510132,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9972873330116272,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9936521053314209,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9882293343544006,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9723194241523743,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9492626190185547,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
                },
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
                      "adjacent_cosine_mean": 0.9999708533287048,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999404549598694,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998810887336731,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999724268913269,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994499683380127,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9987029433250427,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9973691701889038,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9938797354698181,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9889911413192749,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9742316603660583,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9548203349113464,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
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
                      "adjacent_cosine_mean": 0.9999708533287048,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999406933784485,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998818635940552,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997265338897705,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994574189186096,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9987229704856873,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9974265694618225,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9940385222434998,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9894617795944214,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9753822088241577,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9580660462379456,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
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
                      "adjacent_cosine_mean": 0.9999708533287048,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999940812587738,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998824596405029,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997285008430481,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994630217552185,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9987390041351318,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9974715709686279,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9941607713699341,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.989805281162262,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9762389063835144,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.960281252861023,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9998270273208618,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995975494384766,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991806745529175,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981272220611572,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964404106140137,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917224049568176,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9855460524559021,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.968417227268219,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9510875940322876,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
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
                      "adjacent_cosine_mean": 0.9999069571495056,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997982382774353,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995154738426208,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990515112876892,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977757334709167,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959514737129211,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9907388687133789,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9843775629997253,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9668378233909607,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9533820748329163,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
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
                      "adjacent_cosine_mean": 0.9999014735221863,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997973442077637,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995213747024536,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990800023078918,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997909665107727,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960767030715942,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991156816482544,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985405683517456,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9690045118331909,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9582934975624084,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880194664001,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999808073043823,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999561905860901,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999022483825684,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997812509536743,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994936585426331,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990067481994629,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977021217346191,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.995904803276062,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9907554984092712,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9851889610290527,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.968751847743988,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9597102403640747,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp03",
        "reasons": [
          "the repeat-seed/arm endpoint is unsettled"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      },
      "lr3e-4": {
        "arm": "lr3e-4",
        "cases": {
          "main": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 1.3814863535666753,
                "tier": 0
              },
              "control": {
                "E": 0.040691019043637484,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 32.950645278388194,
            "tier_direction": "worsened"
          },
          "repeat-seed": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.017057375824979466,
                "tier": 1
              },
              "control": {
                "E": 0.03491785615016659,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.5114999113455571,
            "tier_direction": "unchanged"
          },
          "repeat-system": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 1.9228096305533615,
                "tier": 0
              },
              "control": {
                "E": 0.09549573839491703,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 19.13503076547453,
            "tier_direction": "worsened"
          }
        },
        "confirmation": "unsettled",
        "control": "lr1e-4",
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
                      "adjacent_cosine_mean": 0.9999845027923584,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999720454216003,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999147653579712,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9997923374176025,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9994936585426331,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9987136721611023,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9972629547119141,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9930123090744019,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9857931137084961,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9655543565750122,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9421334266662598,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.8712400197982788,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.8035227656364441,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999806880950928,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999565482139587,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999876856803894,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9996949434280396,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9991337060928345,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9977458715438843,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.994398295879364,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9856904149055481,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9728690385818481,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9359161257743835,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9091687202453613,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.815343976020813,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.660544753074646,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999734163284302,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999415278434753,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9997374415397644,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9992541670799255,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9975742101669312,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9933544993400574,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9823021292686462,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9538373947143555,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9081090092658997,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.8097403049468994,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.7703856825828552,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.6362945437431335,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.40083372592926025,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999726414680481,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999274611473083,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9995900392532349,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9987033009529114,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9943681359291077,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9832749962806702,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.943345844745636,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.8580484390258789,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.6789649128913879,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.47924041748046875,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.36624929308891296,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.2315276563167572,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.051371730864048004,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999093413352966,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997975826263428,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995217323303223,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990523457527161,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977886080741882,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957399964332581,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9901987910270691,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9825018048286438,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9615046381950378,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9389911890029907,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
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
                      "adjacent_cosine_mean": 0.9999570250511169,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999048113822937,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997943043708801,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999528169631958,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989920854568481,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976863861083984,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957477450370789,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9904364943504333,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9838588237762451,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9654865860939026,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9542497396469116,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999981164932251,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999582767486572,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999063611030579,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999798595905304,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995154738426208,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990686774253845,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978678226470947,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959396123886108,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9909234046936035,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9848374724388123,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9675301313400269,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9567607641220093,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987781047821,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815225601196,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999613165855408,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999911367893219,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998155832290649,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995834827423096,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992039203643799,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981580972671509,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968430995941162,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929201602935791,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9886854290962219,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9761550426483154,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9698630571365356,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999838471412659,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999968409538269,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999252557754517,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998241662979126,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9995728135108948,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9989343881607056,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9974363446235657,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9933798909187317,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9862207770347595,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9658624529838562,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.936864972114563,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.8545464873313904,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.7390842437744141,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999796152114868,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999555945396423,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9998581409454346,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9996405839920044,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.998845100402832,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.996878445148468,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.991321325302124,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9773474335670471,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9534393548965454,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.8930949568748474,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.8397305011749268,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.6987637281417847,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.4891899824142456,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999762177467346,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999430179595947,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9996972680091858,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9991495609283447,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9968569278717041,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9911171197891235,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9726919531822205,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.929699718952179,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.8388150930404663,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.6951751708984375,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.5617995858192444,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.41210535168647766,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.13381275534629822,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999971330165863,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999290704727173,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9997280240058899,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9992228150367737,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9971075654029846,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9916315078735352,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9723247289657593,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.927555501461029,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.8343968391418457,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.68959641456604,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.6367811560630798,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.5308375954627991,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.23006439208984375,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999223351478577,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999829113483429,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995903372764587,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992087483406067,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981492757797241,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964054226875305,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917572140693665,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9849987030029297,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9668107628822327,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9471333026885986,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
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
                      "adjacent_cosine_mean": 0.9999577403068542,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999076724052429,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997920989990234,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995192885398865,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990827441215515,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978979229927063,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961216449737549,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991334080696106,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9851789474487305,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.967799961566925,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9550234079360962,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
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
                      "adjacent_cosine_mean": 0.9999063611030579,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998209476470947,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999584972858429,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992243647575378,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982348084449768,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968690872192383,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9930570125579834,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9889869093894958,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9768524169921875,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9696897268295288,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999876618385315,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999806880950928,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999955952167511,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999062418937683,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997995495796204,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995240569114685,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990931153297424,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978749752044678,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961003661155701,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9912582635879517,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9861302971839905,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9709347486495972,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9624550342559814,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999852776527405,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999730587005615,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999239444732666,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998185634613037,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9995579719543457,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9988653063774109,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9974443316459656,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9935091733932495,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.987309455871582,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9687085151672363,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9474671483039856,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.8812741637229919,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.8156684637069702,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999980092048645,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999592304229736,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9998560547828674,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9996192455291748,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9988877177238464,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9970987439155579,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9921833276748657,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9795806407928467,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.95966637134552,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9068878293037415,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.8585330247879028,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.736363410949707,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.5517135858535767,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999748468399048,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999434947967529,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9998196959495544,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9994894862174988,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.998094379901886,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.994618833065033,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9836592674255371,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9597755074501038,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.919785737991333,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.8322849273681641,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.751070499420166,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.5947805047035217,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.29055532813072205,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999719262123108,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999931812286377,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9996684193611145,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9989897608757019,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9956936240196228,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9873120188713074,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9611513614654541,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9001468420028687,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.778596818447113,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.6179459095001221,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.5373857617378235,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.4336725175380707,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.16719873249530792,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9998270273208618,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995975494384766,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991806745529175,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981272220611572,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964404106140137,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917224049568176,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9855460524559021,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.968417227268219,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9510875940322876,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
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
                      "adjacent_cosine_mean": 0.9999069571495056,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997982382774353,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995154738426208,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990515112876892,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977757334709167,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959514737129211,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9907388687133789,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9843775629997253,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9668378233909607,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9533820748329163,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
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
                      "adjacent_cosine_mean": 0.9999014735221863,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997973442077637,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995213747024536,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990800023078918,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997909665107727,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960767030715942,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991156816482544,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985405683517456,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9690045118331909,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9582934975624084,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880194664001,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999808073043823,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999561905860901,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999022483825684,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997812509536743,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994936585426331,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990067481994629,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977021217346191,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.995904803276062,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9907554984092712,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9851889610290527,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.968751847743988,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9597102403640747,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp03",
        "reasons": [
          "the repeat-seed/arm endpoint is unsettled"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      },
      "lr3e-5": {
        "arm": "lr3e-5",
        "cases": {
          "main": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.07747289529864392,
                "tier": 1
              },
              "control": {
                "E": 0.040691019043637484,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.9039310668420752,
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
                "E": 0.018883270414925272,
                "tier": 1
              },
              "control": {
                "E": 0.03491785615016659,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.45920876889702233,
            "tier_direction": "unchanged"
          },
          "repeat-system": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.22019943911402998,
                "tier": 0
              },
              "control": {
                "E": 0.09549573839491703,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 1.3058561859944797,
            "tier_direction": "worsened"
          }
        },
        "confirmation": "ambiguous",
        "control": "lr1e-4",
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
                      "adjacent_cosine_mean": 0.9999837875366211,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999966561794281,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999319911003113,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998648762702942,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996928572654724,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994035959243774,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986318349838257,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9973423480987549,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9937536716461182,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9883225560188293,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.973264753818512,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.954010009765625,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999843835830688,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999681115150452,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999346137046814,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998693466186523,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996952414512634,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994103908538818,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986366033554077,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9975231289863586,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.994235634803772,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9901553988456726,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9787139892578125,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9673320651054382,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999845623970032,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999662041664124,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999931275844574,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998687505722046,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996941089630127,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994006156921387,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985951781272888,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9973862767219543,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9940211772918701,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9898398518562317,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9777593016624451,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9670145511627197,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999845027923584,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999666810035706,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999305605888367,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998689889907837,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996961355209351,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994193315505981,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986250996589661,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9974803328514099,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9942770004272461,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9907599091529846,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9808781147003174,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9755021929740906,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999093413352966,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997975826263428,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995217323303223,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990523457527161,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977886080741882,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957399964332581,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9901987910270691,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9825018048286438,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9615046381950378,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9389911890029907,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
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
                      "adjacent_cosine_mean": 0.9999570250511169,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999048113822937,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997943043708801,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999528169631958,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989920854568481,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976863861083984,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957477450370789,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9904364943504333,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9838588237762451,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9654865860939026,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9542497396469116,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999981164932251,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999582767486572,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999063611030579,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999798595905304,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995154738426208,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990686774253845,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978678226470947,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959396123886108,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9909234046936035,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9848374724388123,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9675301313400269,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9567607641220093,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987781047821,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815225601196,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999613165855408,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999911367893219,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998155832290649,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995834827423096,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992039203643799,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981580972671509,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968430995941162,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929201602935791,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9886854290962219,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9761550426483154,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9698630571365356,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999828934669495,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999681115150452,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999364018440247,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998695254325867,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996961951255798,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993757605552673,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985257983207703,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9971329569816589,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9932491183280945,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9876306056976318,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9713481664657593,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9548459649085999,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999983549118042,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999679923057556,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999933123588562,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998679161071777,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996901154518127,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993728995323181,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985023140907288,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9972275495529175,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9934086799621582,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9881814122200012,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9740744829177856,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9573840498924255,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884366989136,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836683273315,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999968409538269,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999333620071411,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998725652694702,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997027516365051,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994240403175354,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986358880996704,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9974416494369507,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9940036535263062,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9897809028625488,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9779372215270996,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9689526557922363,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999832510948181,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999665021896362,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999318718910217,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998573064804077,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996671080589294,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993177652359009,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9984073042869568,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970848560333252,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9932873249053955,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9886032938957214,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9753113985061646,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9655031561851501,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999223351478577,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999829113483429,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995903372764587,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992087483406067,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981492757797241,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964054226875305,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917572140693665,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9849987030029297,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9668107628822327,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9471333026885986,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
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
                      "adjacent_cosine_mean": 0.9999577403068542,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999076724052429,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997920989990234,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995192885398865,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990827441215515,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978979229927063,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961216449737549,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991334080696106,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9851789474487305,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.967799961566925,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9550234079360962,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
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
                      "adjacent_cosine_mean": 0.9999063611030579,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998209476470947,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999584972858429,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992243647575378,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982348084449768,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968690872192383,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9930570125579834,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9889869093894958,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9768524169921875,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9696897268295288,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999876618385315,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999806880950928,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999955952167511,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999062418937683,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997995495796204,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995240569114685,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990931153297424,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978749752044678,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961003661155701,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9912582635879517,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9861302971839905,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9709347486495972,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9624550342559814,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9999701976776123,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999401569366455,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998803734779358,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997192621231079,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994460344314575,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986644387245178,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9975467920303345,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9942454099655151,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.989407479763031,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9753216505050659,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9581091403961182,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999837875366211,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999690055847168,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999378323554993,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998803734779358,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997130632400513,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999439537525177,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9987099766731262,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.997511625289917,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9943333864212036,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9898386001586914,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9778183698654175,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9650532603263855,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
                },
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
                      "adjacent_cosine_mean": 0.9999678730964661,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999343156814575,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998725652694702,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997145533561707,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994427561759949,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986782670021057,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9974682331085205,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9941845536231995,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9898409843444824,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9777600169181824,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9666435122489929,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999886751174927,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999839663505554,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999682903289795,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999338984489441,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998685121536255,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997128844261169,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994113445281982,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985894560813904,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9974014759063721,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9940905570983887,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9896047711372375,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.977627694606781,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9670004844665527,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
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
                      "adjacent_cosine_mean": 0.9998270273208618,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995975494384766,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991806745529175,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981272220611572,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964404106140137,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917224049568176,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9855460524559021,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.968417227268219,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9510875940322876,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 38775
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
                      "adjacent_cosine_mean": 0.9999069571495056,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997982382774353,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995154738426208,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990515112876892,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977757334709167,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959514737129211,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9907388687133789,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9843775629997253,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9668378233909607,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9533820748329163,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 77550
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
                      "adjacent_cosine_mean": 0.9999014735221863,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997973442077637,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995213747024536,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990800023078918,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997909665107727,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960767030715942,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991156816482544,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985405683517456,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9690045118331909,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9582934975624084,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 116325
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880194664001,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999808073043823,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999561905860901,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999022483825684,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997812509536743,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994936585426331,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990067481994629,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977021217346191,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.995904803276062,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9907554984092712,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9851889610290527,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.968751847743988,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9597102403640747,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 155100
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp03",
        "reasons": [
          "the registered cases disagree on the E direction"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the ambiguous branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      }
    },
    "descriptive": {
      "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
      "loss": "context only",
      "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
    },
    "experiment": "exp03",
    "unconfirmed": [
      {
        "arm": "lr1e-5",
        "confirmation": "unsettled",
        "reasons": [
          "the repeat-seed/arm endpoint is unsettled"
        ]
      },
      {
        "arm": "lr3e-4",
        "confirmation": "unsettled",
        "reasons": [
          "the repeat-seed/arm endpoint is unsettled"
        ]
      },
      {
        "arm": "lr3e-5",
        "confirmation": "ambiguous",
        "reasons": [
          "the registered cases disagree on the E direction"
        ]
      }
    ]
  },
  "contrasts": {
    "lr1e-3": {
      "arm": "lr1e-3",
      "cases": {
        "main": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 1.4551508979130539,
              "tier": 0
            },
            "control": {
              "E": 0.040691019043637484,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 34.76098441654986,
          "tier_direction": "worsened"
        },
        "repeat-seed": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 1.4024505668393392,
              "tier": 0
            },
            "control": {
              "E": 0.03491785615016659,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 39.16428044173176,
          "tier_direction": "worsened"
        },
        "repeat-system": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 1.5639231628850137,
              "tier": 0
            },
            "control": {
              "E": 0.09549573839491703,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 15.376889578229147,
          "tier_direction": "worsened"
        }
      },
      "confirmation": "confirmed-worsening",
      "control": "lr1e-4",
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
                    "adjacent_cosine_mean": 0.9998746514320374,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9993506669998169,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9911553859710693,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9551479816436768,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.6514114737510681,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.21333256363868713,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.0010502415243536234,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": -0.0016552109736949205,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.0009392162319272757,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": -0.0014964346773922443,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.00045337845222093165,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.0022931608837097883,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": -0.005452209617942572,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9997854232788086,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9982057809829712,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9558442831039429,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.7303365468978882,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.03642311692237854,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.0006389201735146344,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": -0.0012985869543626904,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": -0.0021475644316524267,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.0007950661238282919,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.0003432423691265285,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": -0.0036402433179318905,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.0002082827122649178,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": -0.0053091393783688545,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999680757522583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9966989159584045,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.8956877589225769,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.4491543471813202,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": -0.0012277752393856645,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": -0.002444631652906537,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": -0.0014381337678059936,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": -0.0021932946983724833,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": -0.0019786888733506203,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.00017463386757299304,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.000519188295584172,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.001347001176327467,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": -0.002154938643798232,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9996010065078735,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9946120381355286,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.7940441370010376,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.24798113107681274,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": -0.004531601909548044,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.00028374436078593135,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": -2.3113667339202948e-05,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": -0.0008456743089482188,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": -0.00393932219594717,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": -0.0018416013335809112,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 1.4812409972364549e-05,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.0013676033122465014,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": -0.0018080566078424454,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999093413352966,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997975826263428,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995217323303223,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990523457527161,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977886080741882,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957399964332581,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9901987910270691,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9825018048286438,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9615046381950378,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9389911890029907,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
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
                    "adjacent_cosine_mean": 0.9999570250511169,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999048113822937,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997943043708801,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999528169631958,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989920854568481,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976863861083984,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957477450370789,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9904364943504333,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9838588237762451,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9654865860939026,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9542497396469116,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999981164932251,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999582767486572,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999063611030579,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999798595905304,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995154738426208,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990686774253845,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978678226470947,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959396123886108,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9909234046936035,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9848374724388123,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9675301313400269,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9567607641220093,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987781047821,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815225601196,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999613165855408,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999911367893219,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998155832290649,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995834827423096,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992039203643799,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981580972671509,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968430995941162,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929201602935791,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9886854290962219,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9761550426483154,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9698630571365356,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9998865127563477,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9993888139724731,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9925609230995178,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9621824026107788,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.6812936067581177,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.22548463940620422,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.003008781000971794,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": -0.003709736978635192,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": -0.0020381989888846874,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": -0.0018530855886638165,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": -0.0055136545561254025,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.004028624389320612,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": -0.002525984775274992,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9998068809509277,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9983575344085693,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9478579163551331,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.7083415389060974,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.03214969485998154,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": -0.0017908815061673522,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": -0.001739039085805416,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.001917719142511487,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": -0.0022463116329163313,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": -0.0030226316303014755,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": -0.0013616791693493724,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.0009448858327232301,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.0016628482844680548,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9997245073318481,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9969354867935181,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.8859174251556396,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.438077449798584,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": -0.00019763672025874257,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.0028387673664838076,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": -0.0005180435837246478,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.00104482879396528,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": -0.0012270776787772775,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": -0.0014750347472727299,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": -0.0014021858805790544,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.0036816962528973818,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": -0.0024859027471393347,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9996522068977356,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9954362511634827,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.8172602653503418,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.2727125287055969,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": -0.0028302522841840982,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": -0.003926251083612442,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": -0.003322550328448415,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.0009302963153459132,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.0027217187453061342,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.0042549483478069305,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": -0.002858209190890193,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.002757567912340164,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.0025910737458616495,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999223351478577,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999829113483429,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995903372764587,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992087483406067,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981492757797241,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964054226875305,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917572140693665,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9849987030029297,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9668107628822327,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9471333026885986,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
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
                    "adjacent_cosine_mean": 0.9999577403068542,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999076724052429,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997920989990234,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995192885398865,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990827441215515,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978979229927063,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961216449737549,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991334080696106,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9851789474487305,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.967799961566925,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9550234079360962,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
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
                    "adjacent_cosine_mean": 0.9999063611030579,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998209476470947,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999584972858429,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992243647575378,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982348084449768,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968690872192383,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9930570125579834,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9889869093894958,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9768524169921875,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9696897268295288,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999876618385315,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999806880950928,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999955952167511,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999062418937683,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997995495796204,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995240569114685,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990931153297424,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978749752044678,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961003661155701,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9912582635879517,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9861302971839905,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9709347486495972,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9624550342559814,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9998959302902222,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9994467496871948,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9900456666946411,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9499315023422241,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.6414554119110107,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.20199018716812134,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.0007150886231102049,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": -0.0018872771179303527,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": -0.0003220918879378587,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 5.88443290325813e-05,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": -0.0012761311372742057,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.0033324873074889183,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": -0.0015223019290715456,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9998219013214111,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9984787702560425,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9586173295974731,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.7504780292510986,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.04559456184506416,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": -3.0929713830119e-05,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": -0.00309168198145926,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": -0.0014778099721297622,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.00019037455786019564,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": -0.0013096180045977235,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": -0.0021393278148025274,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.0025605210103094578,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.00022530216665472835,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9997442364692688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9972327947616577,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9117815494537354,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.49665749073028564,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": -0.004347582813352346,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": -0.002915716264396906,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.0009228203562088311,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": -0.00175646529532969,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.0022462911438196898,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": -0.000808694981969893,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": -0.0009383969590999186,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.0039045452140271664,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": -0.002674757968634367,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9996750354766846,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9957952499389648,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.8265535831451416,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.28348952531814575,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": -0.003065342316403985,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.00017847084382083267,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": -0.00012626945681404322,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": -0.0009415843524038792,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": -0.0008999562123790383,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.0032382486388087273,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": -0.0029010979924350977,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.0003410322533454746,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": -0.0019255464430898428,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9998270273208618,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995975494384766,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991806745529175,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981272220611572,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964404106140137,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917224049568176,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9855460524559021,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.968417227268219,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9510875940322876,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
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
                    "adjacent_cosine_mean": 0.9999069571495056,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997982382774353,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995154738426208,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990515112876892,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977757334709167,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959514737129211,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9907388687133789,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9843775629997253,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9668378233909607,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9533820748329163,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
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
                    "adjacent_cosine_mean": 0.9999014735221863,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997973442077637,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995213747024536,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990800023078918,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997909665107727,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960767030715942,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991156816482544,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985405683517456,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9690045118331909,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9582934975624084,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880194664001,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999808073043823,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999561905860901,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999022483825684,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997812509536743,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994936585426331,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990067481994629,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977021217346191,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.995904803276062,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9907554984092712,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9851889610290527,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.968751847743988,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9597102403640747,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp03",
      "reasons": [],
      "scope_disposition": {
        "dependent_launch_allowed": false,
        "reason": "a refuted lead: the registered hypothesis is contradicted on all three cases, so a concrete owner proposal under SCOPE-49 is recorded before dependent work continues",
        "scope49_disposition": "proposal-pending"
      }
    },
    "lr1e-5": {
      "arm": "lr1e-5",
      "cases": {
        "main": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.2097428875427889,
              "tier": 0
            },
            "control": {
              "E": 0.040691019043637484,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 4.1545253098198005,
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
              "E": 0.18744816464300104,
              "tier": 0
            },
            "control": {
              "E": 0.03491785615016659,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 4.368260979049446,
          "tier_direction": "worsened"
        },
        "repeat-system": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.21207523896683939,
              "tier": 0
            },
            "control": {
              "E": 0.09549573839491703,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 1.2207822310333334,
          "tier_direction": "worsened"
        }
      },
      "confirmation": "unsettled",
      "control": "lr1e-4",
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
                    "adjacent_cosine_mean": 0.9999837279319763,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999698400497437,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999356865882874,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998800158500671,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997189044952393,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994206428527832,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986338019371033,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9972665905952454,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9936047792434692,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9875799417495728,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9706918001174927,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9464858770370483,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
              },
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
                    "adjacent_cosine_mean": 0.9999698400497437,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999359250068665,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999880850315094,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997216463088989,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994302988052368,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986612796783447,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.997359037399292,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9938575625419617,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.988423764705658,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9727455973625183,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9524453282356262,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
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
                    "adjacent_cosine_mean": 0.9999698996543884,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999936044216156,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998814463615417,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997234344482422,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999436616897583,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986796379089355,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9974161982536316,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9940141439437866,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.988919198513031,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9739335179328918,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9558897614479065,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
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
                    "adjacent_cosine_mean": 0.9999699592590332,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999362230300903,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998819828033447,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997252225875854,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994419813156128,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986953735351562,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9974596500396729,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9941338896751404,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9892734289169312,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9747949838638306,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9583056569099426,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999093413352966,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997975826263428,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995217323303223,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990523457527161,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977886080741882,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957399964332581,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9901987910270691,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9825018048286438,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9615046381950378,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9389911890029907,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
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
                    "adjacent_cosine_mean": 0.9999570250511169,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999048113822937,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997943043708801,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999528169631958,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989920854568481,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976863861083984,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957477450370789,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9904364943504333,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9838588237762451,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9654865860939026,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9542497396469116,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999981164932251,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999582767486572,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999063611030579,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999798595905304,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995154738426208,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990686774253845,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978678226470947,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959396123886108,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9909234046936035,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9848374724388123,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9675301313400269,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9567607641220093,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987781047821,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815225601196,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999613165855408,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999911367893219,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998155832290649,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995834827423096,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992039203643799,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981580972671509,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968430995941162,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929201602935791,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9886854290962219,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9761550426483154,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9698630571365356,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999827146530151,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999691247940063,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999936044216156,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998762011528015,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997261166572571,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994266629219055,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986933469772339,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9973498582839966,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9937376379966736,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9878357648849487,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9714356660842896,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9489167928695679,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999827146530151,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999691247940063,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999362826347351,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998772144317627,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997286796569824,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994363784790039,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9987202882766724,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9974389672279358,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9939811825752258,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9886475205421448,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9735094308853149,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.954601526260376,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999826550483704,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999691247940063,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999365210533142,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998779296875,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997305870056152,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994428753852844,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9987386465072632,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9974983930587769,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9941413402557373,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9891550540924072,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9748091101646423,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9581443071365356,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999826550483704,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999691247940063,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999366402626038,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998785257339478,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997321963310242,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994481205940247,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.998753547668457,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9975417852401733,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9942600131034851,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9895209670066833,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9757128953933716,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9606232643127441,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999223351478577,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999829113483429,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995903372764587,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992087483406067,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981492757797241,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964054226875305,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917572140693665,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9849987030029297,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9668107628822327,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9471333026885986,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
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
                    "adjacent_cosine_mean": 0.9999577403068542,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999076724052429,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997920989990234,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995192885398865,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990827441215515,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978979229927063,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961216449737549,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991334080696106,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9851789474487305,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.967799961566925,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9550234079360962,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
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
                    "adjacent_cosine_mean": 0.9999063611030579,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998209476470947,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999584972858429,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992243647575378,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982348084449768,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968690872192383,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9930570125579834,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9889869093894958,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9768524169921875,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9696897268295288,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999876618385315,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999806880950928,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999955952167511,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999062418937683,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997995495796204,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995240569114685,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990931153297424,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978749752044678,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961003661155701,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9912582635879517,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9861302971839905,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9709347486495972,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9624550342559814,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999706745147705,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999401569366455,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998800158500671,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997210502624512,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994403123855591,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986776113510132,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9972873330116272,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9936521053314209,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9882293343544006,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9723194241523743,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9492626190185547,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
              },
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
                    "adjacent_cosine_mean": 0.9999708533287048,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999404549598694,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998810887336731,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999724268913269,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994499683380127,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9987029433250427,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9973691701889038,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9938797354698181,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9889911413192749,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9742316603660583,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9548203349113464,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
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
                    "adjacent_cosine_mean": 0.9999708533287048,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999406933784485,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998818635940552,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997265338897705,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994574189186096,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9987229704856873,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9974265694618225,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9940385222434998,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9894617795944214,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9753822088241577,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9580660462379456,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
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
                    "adjacent_cosine_mean": 0.9999708533287048,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999940812587738,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998824596405029,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997285008430481,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994630217552185,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9987390041351318,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9974715709686279,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9941607713699341,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.989805281162262,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9762389063835144,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.960281252861023,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9998270273208618,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995975494384766,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991806745529175,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981272220611572,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964404106140137,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917224049568176,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9855460524559021,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.968417227268219,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9510875940322876,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
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
                    "adjacent_cosine_mean": 0.9999069571495056,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997982382774353,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995154738426208,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990515112876892,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977757334709167,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959514737129211,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9907388687133789,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9843775629997253,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9668378233909607,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9533820748329163,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
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
                    "adjacent_cosine_mean": 0.9999014735221863,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997973442077637,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995213747024536,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990800023078918,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997909665107727,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960767030715942,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991156816482544,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985405683517456,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9690045118331909,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9582934975624084,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880194664001,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999808073043823,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999561905860901,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999022483825684,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997812509536743,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994936585426331,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990067481994629,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977021217346191,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.995904803276062,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9907554984092712,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9851889610290527,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.968751847743988,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9597102403640747,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp03",
      "reasons": [
        "the repeat-seed/arm endpoint is unsettled"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    },
    "lr3e-4": {
      "arm": "lr3e-4",
      "cases": {
        "main": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 1.3814863535666753,
              "tier": 0
            },
            "control": {
              "E": 0.040691019043637484,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 32.950645278388194,
          "tier_direction": "worsened"
        },
        "repeat-seed": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.017057375824979466,
              "tier": 1
            },
            "control": {
              "E": 0.03491785615016659,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.5114999113455571,
          "tier_direction": "unchanged"
        },
        "repeat-system": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 1.9228096305533615,
              "tier": 0
            },
            "control": {
              "E": 0.09549573839491703,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 19.13503076547453,
          "tier_direction": "worsened"
        }
      },
      "confirmation": "unsettled",
      "control": "lr1e-4",
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
                    "adjacent_cosine_mean": 0.9999845027923584,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999720454216003,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999147653579712,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9997923374176025,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9994936585426331,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9987136721611023,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9972629547119141,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9930123090744019,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9857931137084961,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9655543565750122,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9421334266662598,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.8712400197982788,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.8035227656364441,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999806880950928,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999565482139587,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999876856803894,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9996949434280396,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9991337060928345,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9977458715438843,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.994398295879364,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9856904149055481,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9728690385818481,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9359161257743835,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9091687202453613,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.815343976020813,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.660544753074646,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999734163284302,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999415278434753,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9997374415397644,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9992541670799255,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9975742101669312,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9933544993400574,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9823021292686462,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9538373947143555,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9081090092658997,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.8097403049468994,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.7703856825828552,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.6362945437431335,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.40083372592926025,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999726414680481,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999274611473083,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9995900392532349,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9987033009529114,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9943681359291077,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9832749962806702,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.943345844745636,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.8580484390258789,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.6789649128913879,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.47924041748046875,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.36624929308891296,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.2315276563167572,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.051371730864048004,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999093413352966,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997975826263428,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995217323303223,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990523457527161,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977886080741882,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957399964332581,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9901987910270691,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9825018048286438,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9615046381950378,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9389911890029907,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
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
                    "adjacent_cosine_mean": 0.9999570250511169,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999048113822937,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997943043708801,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999528169631958,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989920854568481,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976863861083984,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957477450370789,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9904364943504333,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9838588237762451,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9654865860939026,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9542497396469116,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999981164932251,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999582767486572,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999063611030579,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999798595905304,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995154738426208,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990686774253845,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978678226470947,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959396123886108,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9909234046936035,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9848374724388123,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9675301313400269,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9567607641220093,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987781047821,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815225601196,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999613165855408,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999911367893219,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998155832290649,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995834827423096,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992039203643799,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981580972671509,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968430995941162,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929201602935791,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9886854290962219,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9761550426483154,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9698630571365356,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999838471412659,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999968409538269,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999252557754517,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998241662979126,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9995728135108948,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9989343881607056,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9974363446235657,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9933798909187317,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9862207770347595,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9658624529838562,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.936864972114563,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.8545464873313904,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.7390842437744141,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999796152114868,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999555945396423,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9998581409454346,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9996405839920044,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.998845100402832,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.996878445148468,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.991321325302124,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9773474335670471,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9534393548965454,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.8930949568748474,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.8397305011749268,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.6987637281417847,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.4891899824142456,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999762177467346,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999430179595947,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9996972680091858,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9991495609283447,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9968569278717041,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9911171197891235,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9726919531822205,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.929699718952179,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.8388150930404663,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.6951751708984375,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.5617995858192444,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.41210535168647766,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.13381275534629822,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999971330165863,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999290704727173,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9997280240058899,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9992228150367737,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9971075654029846,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9916315078735352,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9723247289657593,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.927555501461029,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.8343968391418457,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.68959641456604,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.6367811560630798,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.5308375954627991,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.23006439208984375,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999223351478577,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999829113483429,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995903372764587,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992087483406067,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981492757797241,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964054226875305,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917572140693665,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9849987030029297,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9668107628822327,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9471333026885986,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
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
                    "adjacent_cosine_mean": 0.9999577403068542,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999076724052429,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997920989990234,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995192885398865,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990827441215515,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978979229927063,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961216449737549,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991334080696106,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9851789474487305,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.967799961566925,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9550234079360962,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
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
                    "adjacent_cosine_mean": 0.9999063611030579,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998209476470947,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999584972858429,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992243647575378,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982348084449768,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968690872192383,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9930570125579834,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9889869093894958,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9768524169921875,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9696897268295288,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999876618385315,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999806880950928,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999955952167511,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999062418937683,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997995495796204,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995240569114685,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990931153297424,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978749752044678,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961003661155701,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9912582635879517,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9861302971839905,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9709347486495972,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9624550342559814,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999852776527405,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999730587005615,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999239444732666,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998185634613037,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9995579719543457,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9988653063774109,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9974443316459656,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9935091733932495,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.987309455871582,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9687085151672363,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9474671483039856,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.8812741637229919,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.8156684637069702,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999980092048645,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999592304229736,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9998560547828674,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9996192455291748,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9988877177238464,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9970987439155579,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9921833276748657,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9795806407928467,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.95966637134552,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9068878293037415,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.8585330247879028,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.736363410949707,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.5517135858535767,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999748468399048,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999434947967529,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9998196959495544,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9994894862174988,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.998094379901886,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.994618833065033,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9836592674255371,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9597755074501038,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.919785737991333,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.8322849273681641,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.751070499420166,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.5947805047035217,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.29055532813072205,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999719262123108,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999931812286377,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9996684193611145,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9989897608757019,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9956936240196228,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9873120188713074,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9611513614654541,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9001468420028687,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.778596818447113,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.6179459095001221,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.5373857617378235,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.4336725175380707,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.16719873249530792,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9998270273208618,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995975494384766,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991806745529175,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981272220611572,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964404106140137,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917224049568176,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9855460524559021,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.968417227268219,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9510875940322876,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
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
                    "adjacent_cosine_mean": 0.9999069571495056,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997982382774353,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995154738426208,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990515112876892,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977757334709167,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959514737129211,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9907388687133789,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9843775629997253,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9668378233909607,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9533820748329163,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
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
                    "adjacent_cosine_mean": 0.9999014735221863,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997973442077637,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995213747024536,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990800023078918,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997909665107727,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960767030715942,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991156816482544,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985405683517456,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9690045118331909,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9582934975624084,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880194664001,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999808073043823,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999561905860901,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999022483825684,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997812509536743,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994936585426331,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990067481994629,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977021217346191,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.995904803276062,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9907554984092712,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9851889610290527,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.968751847743988,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9597102403640747,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp03",
      "reasons": [
        "the repeat-seed/arm endpoint is unsettled"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    },
    "lr3e-5": {
      "arm": "lr3e-5",
      "cases": {
        "main": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.07747289529864392,
              "tier": 1
            },
            "control": {
              "E": 0.040691019043637484,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.9039310668420752,
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
              "E": 0.018883270414925272,
              "tier": 1
            },
            "control": {
              "E": 0.03491785615016659,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.45920876889702233,
          "tier_direction": "unchanged"
        },
        "repeat-system": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.22019943911402998,
              "tier": 0
            },
            "control": {
              "E": 0.09549573839491703,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 1.3058561859944797,
          "tier_direction": "worsened"
        }
      },
      "confirmation": "ambiguous",
      "control": "lr1e-4",
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
                    "adjacent_cosine_mean": 0.9999837875366211,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999966561794281,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999319911003113,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998648762702942,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996928572654724,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994035959243774,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986318349838257,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9973423480987549,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9937536716461182,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9883225560188293,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.973264753818512,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.954010009765625,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999843835830688,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999681115150452,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999346137046814,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998693466186523,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996952414512634,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994103908538818,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986366033554077,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9975231289863586,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.994235634803772,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9901553988456726,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9787139892578125,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9673320651054382,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999845623970032,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999662041664124,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999931275844574,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998687505722046,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996941089630127,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994006156921387,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985951781272888,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9973862767219543,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9940211772918701,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9898398518562317,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9777593016624451,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9670145511627197,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999845027923584,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999666810035706,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999305605888367,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998689889907837,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996961355209351,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994193315505981,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986250996589661,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9974803328514099,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9942770004272461,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9907599091529846,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9808781147003174,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9755021929740906,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999093413352966,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997975826263428,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995217323303223,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990523457527161,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977886080741882,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957399964332581,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9901987910270691,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9825018048286438,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9615046381950378,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9389911890029907,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
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
                    "adjacent_cosine_mean": 0.9999570250511169,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999048113822937,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997943043708801,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999528169631958,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989920854568481,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976863861083984,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957477450370789,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9904364943504333,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9838588237762451,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9654865860939026,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9542497396469116,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999981164932251,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999582767486572,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999063611030579,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999798595905304,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995154738426208,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990686774253845,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978678226470947,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959396123886108,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9909234046936035,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9848374724388123,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9675301313400269,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9567607641220093,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987781047821,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815225601196,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999613165855408,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999911367893219,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998155832290649,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995834827423096,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992039203643799,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981580972671509,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968430995941162,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929201602935791,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9886854290962219,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9761550426483154,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9698630571365356,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999828934669495,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999681115150452,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999364018440247,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998695254325867,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996961951255798,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993757605552673,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985257983207703,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9971329569816589,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9932491183280945,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9876306056976318,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9713481664657593,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9548459649085999,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999983549118042,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999679923057556,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999933123588562,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998679161071777,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996901154518127,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993728995323181,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985023140907288,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9972275495529175,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9934086799621582,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9881814122200012,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9740744829177856,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9573840498924255,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884366989136,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836683273315,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999968409538269,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999333620071411,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998725652694702,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997027516365051,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994240403175354,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986358880996704,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9974416494369507,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9940036535263062,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9897809028625488,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9779372215270996,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9689526557922363,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999832510948181,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999665021896362,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999318718910217,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998573064804077,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996671080589294,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993177652359009,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9984073042869568,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970848560333252,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9932873249053955,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9886032938957214,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9753113985061646,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9655031561851501,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999223351478577,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999829113483429,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995903372764587,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992087483406067,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981492757797241,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964054226875305,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917572140693665,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9849987030029297,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9668107628822327,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9471333026885986,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
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
                    "adjacent_cosine_mean": 0.9999577403068542,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999076724052429,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997920989990234,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995192885398865,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990827441215515,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978979229927063,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961216449737549,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991334080696106,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9851789474487305,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.967799961566925,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9550234079360962,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
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
                    "adjacent_cosine_mean": 0.9999063611030579,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998209476470947,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999584972858429,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992243647575378,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982348084449768,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968690872192383,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9930570125579834,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9889869093894958,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9768524169921875,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9696897268295288,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999876618385315,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999806880950928,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999955952167511,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999062418937683,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997995495796204,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995240569114685,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990931153297424,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978749752044678,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961003661155701,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9912582635879517,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9861302971839905,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9709347486495972,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9624550342559814,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9999701976776123,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999401569366455,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998803734779358,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997192621231079,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994460344314575,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986644387245178,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9975467920303345,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9942454099655151,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.989407479763031,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9753216505050659,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9581091403961182,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999837875366211,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999690055847168,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999378323554993,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998803734779358,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997130632400513,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999439537525177,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9987099766731262,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.997511625289917,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9943333864212036,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9898386001586914,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9778183698654175,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9650532603263855,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
              },
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
                    "adjacent_cosine_mean": 0.9999678730964661,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999343156814575,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998725652694702,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997145533561707,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994427561759949,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986782670021057,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9974682331085205,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9941845536231995,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9898409843444824,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9777600169181824,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9666435122489929,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999886751174927,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999839663505554,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999682903289795,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999338984489441,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998685121536255,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997128844261169,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994113445281982,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985894560813904,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9974014759063721,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9940905570983887,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9896047711372375,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.977627694606781,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9670004844665527,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
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
                    "adjacent_cosine_mean": 0.9998270273208618,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995975494384766,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991806745529175,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981272220611572,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964404106140137,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917224049568176,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9855460524559021,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.968417227268219,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9510875940322876,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 38775
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
                    "adjacent_cosine_mean": 0.9999069571495056,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997982382774353,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995154738426208,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990515112876892,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977757334709167,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959514737129211,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9907388687133789,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9843775629997253,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9668378233909607,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9533820748329163,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 77550
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
                    "adjacent_cosine_mean": 0.9999014735221863,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997973442077637,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995213747024536,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990800023078918,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997909665107727,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960767030715942,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991156816482544,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985405683517456,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9690045118331909,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9582934975624084,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 116325
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880194664001,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999808073043823,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999561905860901,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999022483825684,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997812509536743,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994936585426331,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990067481994629,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977021217346191,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.995904803276062,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9907554984092712,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9851889610290527,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.968751847743988,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9597102403640747,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 155100
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp03",
      "reasons": [
        "the registered cases disagree on the E direction"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the ambiguous branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    }
  },
  "dependent_launch_allowed": false,
  "experiment": "exp03",
  "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
  "predictions_comparison": {
    "lr1e-3": {
      "case_directions": {
        "main": "worsening",
        "repeat-seed": "worsening",
        "repeat-system": "worsening"
      },
      "observed_confirmation": "confirmed-worsening",
      "observed_disposition": "proposal-pending",
      "registered_hypothesis": "under the hypothesis, learning-rate sensitivity improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    },
    "lr1e-5": {
      "case_directions": {
        "main": "worsening",
        "repeat-seed": "worsening",
        "repeat-system": "worsening"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, learning-rate sensitivity improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    },
    "lr3e-4": {
      "case_directions": {
        "main": "worsening",
        "repeat-seed": "improvement",
        "repeat-system": "worsening"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, learning-rate sensitivity improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    },
    "lr3e-5": {
      "case_directions": {
        "main": "worsening",
        "repeat-seed": "improvement",
        "repeat-system": "worsening"
      },
      "observed_confirmation": "ambiguous",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, learning-rate sensitivity improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    }
  },
  "proposed_change": "a refuted lead or an out-of-rule result was observed; the owner decides under SCOPE-49 whether the remaining experiments run, change or stop",
  "roadmap_comparison": "each contrast's confirmation label is read against the committed prediction table; the roadmap's next experiment proceeds only when this review allows the dependent launch",
  "schema": "phase67-review/v1",
  "scope49_disposition": "proposal-pending"
}
```
