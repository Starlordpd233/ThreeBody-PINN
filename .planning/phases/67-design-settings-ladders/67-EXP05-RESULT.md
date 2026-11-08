# Phase 67 Experiment Result — EXP-05

The review's complete reading: every endpoint's frozen values, the
matched contrasts, the prediction and roadmap comparison, and the
SCOPE-49 disposition. GAP-59-08 stays explicit: E is the frozen
scorecard's position-error score; no energy bar is adjudicated here.

```json phase67-review
{
  "budget_steps": 148700,
  "confirmation": {
    "confirmed": [],
    "contrasts": {
      "lap1": {
        "arm": "lap1",
        "cases": {
          "main": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.005407673830025773,
                "tier": 1
              },
              "control": {
                "E": 0.027243759954814768,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.8015078007222686,
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
                "E": 0.015676362749794264,
                "tier": 1
              },
              "control": {
                "E": 0.11465182676222399,
                "tier": 0
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.8632698388460446,
            "tier_direction": "improved"
          },
          "repeat-system": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "settled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.012315061236409686,
                "tier": 1
              },
              "control": {
                "E": 0.03528830371107014,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.651015777430345,
            "tier_direction": "unchanged"
          }
        },
        "confirmation": "unsettled",
        "control": "lap10",
        "descriptive": {
          "adjacent_time_similarity": {
            "main": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9938457012176514,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9964244365692139,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9979904890060425,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9985747337341309,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9986845254898071,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9985023736953735,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9980407953262329,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9966896176338196,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9942570924758911,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9884307980537415,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9774336218833923,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9495965242385864,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.8968390226364136,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9941507577896118,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9978240728378296,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9982323050498962,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9985566735267639,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9986580014228821,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.998711347579956,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9984447360038757,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978814125061035,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9966490268707275,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9934003353118896,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9885785579681396,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9752222299575806,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9550203084945679,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9951128363609314,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9978105425834656,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.998327374458313,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9985527396202087,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9986785650253296,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9987319707870483,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9985957145690918,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982414841651917,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9975666999816895,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9960021376609802,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9934777617454529,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9859269261360168,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9758686423301697,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.995894730091095,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9978885650634766,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9983782172203064,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9986359477043152,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9987887740135193,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9987199306488037,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9985138177871704,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978376626968384,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9963917136192322,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929416179656982,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9857869744300842,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9670734405517578,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9365713000297546,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9955934286117554,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9978163838386536,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9984643459320068,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.998612642288208,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.998651385307312,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9986093044281006,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9982799291610718,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997417151927948,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9955117702484131,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9906006455421448,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9843290448188782,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9631816148757935,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9307559132575989,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999873042106628,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999829530715942,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999684691429138,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999327659606934,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998732805252075,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997059106826782,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999376654624939,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985236525535583,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968986511230469,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9926234483718872,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9842280149459839,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.96236252784729,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9214602708816528,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999871850013733,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999821782112122,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999961793422699,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999173283576965,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998281002044678,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996033310890198,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992149472236633,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982089996337891,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9966210126876831,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9922357797622681,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9855553507804871,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9679967761039734,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9486552476882935,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999873042106628,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999816417694092,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999540448188782,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998989105224609,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999788761138916,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995148181915283,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990537762641907,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977971315383911,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960052371025085,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9909918308258057,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9850074052810669,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9683241248130798,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9572503566741943,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999868869781494,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999809861183167,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999610781669617,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999128580093384,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998356699943542,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996131062507629,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992409944534302,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982267022132874,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996870219707489,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9930270910263062,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9882631301879883,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9749119281768799,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9650939702987671,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987006187439,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999980092048645,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999533891677856,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998939037322998,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997878074645996,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.99949049949646,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990198612213135,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977650046348572,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960800409317017,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9911503791809082,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985751211643219,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9696986675262451,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9610034227371216,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ]
            },
            "repeat-seed": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9938263893127441,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9963534474372864,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9979745745658875,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9982947111129761,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.998656153678894,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.99858158826828,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9981763362884521,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9973181486129761,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9956678152084351,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9910469651222229,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9828280806541443,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9622671008110046,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9259752631187439,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.995459794998169,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9976152777671814,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9984028339385986,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9983202219009399,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9985756874084473,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.998735785484314,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.998624324798584,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982497096061707,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.997159481048584,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9946970343589783,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9911864995956421,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9798681735992432,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9640430808067322,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9958539605140686,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.998053789138794,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9983298778533936,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9986382722854614,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9987799525260925,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9987823367118835,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9986356496810913,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.998235285282135,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9974769949913025,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.995435357093811,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.992275059223175,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9812233448028564,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9669778943061829,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9963444471359253,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9977819323539734,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9983490109443665,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9986317753791809,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9987672567367554,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9987106919288635,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9984859824180603,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977421760559082,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9962281584739685,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9922602772712708,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9863338470458984,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9686866998672485,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9445493817329407,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9964916110038757,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.99791020154953,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9980717897415161,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9986920952796936,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9987788796424866,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9986541867256165,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9982323050498962,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9970716834068298,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9941815733909607,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9871310591697693,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9777007102966309,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9481189846992493,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9085423350334167,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999874234199524,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999818801879883,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999678730964661,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999345541000366,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998724460601807,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997184872627258,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993950128555298,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986075758934021,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970444440841675,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929084181785583,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9849348068237305,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9640600085258484,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.926579475402832,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999871850013733,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999825358390808,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999580979347229,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999078512191772,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998064041137695,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995436668395996,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.99908846616745,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978458285331726,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959667921066284,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.990613579750061,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9832639098167419,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9629725217819214,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9418724179267883,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999865293502808,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999804496765137,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999541640281677,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998980760574341,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997842311859131,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995024800300598,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989869594573975,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976776242256165,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958101511001587,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9903093576431274,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9834225177764893,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9647646546363831,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9509849548339844,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987006187439,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999791979789734,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999513626098633,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998918175697327,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997658133506775,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994567632675171,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989712238311768,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997593104839325,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957067370414734,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9903287291526794,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9838626980781555,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9657849073410034,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9564179182052612,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999861121177673,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999791979789734,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999459385871887,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998733997344971,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997392892837524,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9993844032287598,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9987626075744629,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9971981644630432,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9951921105384827,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9891223907470703,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9829607009887695,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9644073843955994,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9555770754814148,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ]
            },
            "repeat-system": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9765540361404419,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9832199215888977,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.990013062953949,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9924786686897278,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9954972267150879,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.996017336845398,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9961075186729431,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9953919649124146,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9933848977088928,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9882489442825317,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9802534580230713,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9591556191444397,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9206137657165527,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9798721075057983,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.989078938961029,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9921504259109497,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9935716986656189,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9939422607421875,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.994914174079895,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.995358943939209,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9957630038261414,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959380626678467,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9958773851394653,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9953582286834717,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9932984113693237,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9897904396057129,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9815347194671631,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9901346564292908,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9919463396072388,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9932215213775635,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9945776462554932,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9954935908317566,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9960461258888245,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9960839152336121,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9951769709587097,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9931687116622925,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9899098873138428,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9802233576774597,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9650889039039612,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9849295616149902,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9915348887443542,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9931098818778992,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9941876530647278,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9946734309196472,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9955689907073975,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9957655668258667,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9961029887199402,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9956105351448059,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9943951964378357,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9925156235694885,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9870995283126831,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9800121784210205,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9840295314788818,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9909984469413757,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9923029541969299,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9936966896057129,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9950492978096008,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9959349632263184,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.996029794216156,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9955248236656189,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9942203164100647,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9898468852043152,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9822054505348206,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9618450999259949,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9315370917320251,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999955415725708,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999606609344482,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999479651451111,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999155402183533,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998494982719421,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996647238731384,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993292093276978,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9984490275382996,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9966986179351807,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9922631978988647,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9839369654655457,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.96240234375,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9206265807151794,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999579191207886,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999600052833557,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999388456344604,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998790621757507,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997878074645996,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995396733283997,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990968704223633,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978508353233337,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957573413848877,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9903771281242371,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9829946160316467,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9624257683753967,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9388824701309204,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999600052833557,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999597668647766,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999329447746277,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998740553855896,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997615218162537,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994500875473022,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.998892605304718,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9975738525390625,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9951943755149841,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.988853394985199,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9804162383079529,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9556616544723511,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9328624606132507,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999579191207886,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999958872795105,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999295473098755,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998630285263062,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997533559799194,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994406700134277,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.998871386051178,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9973885416984558,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9950183033943176,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9884749054908752,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.980159342288971,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9563855528831482,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9350361824035645,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999602437019348,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999583959579468,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999322295188904,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998706579208374,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997504949569702,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994411468505859,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.998908519744873,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9973835349082947,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9952226877212524,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.989122211933136,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9813206195831299,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9585052132606506,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9387605786323547,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp05",
        "reasons": [
          "the main/arm endpoint is unsettled",
          "the main/control endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      },
      "lap2": {
        "arm": "lap2",
        "cases": {
          "main": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.015753288018634588,
                "tier": 1
              },
              "control": {
                "E": 0.027243759954814768,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.4217652759838489,
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
                "E": 0.09900171619123573,
                "tier": 1
              },
              "control": {
                "E": 0.11465182676222399,
                "tier": 0
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.13650118810095344,
            "tier_direction": "improved"
          },
          "repeat-system": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.0041033828287498,
                "tier": 1
              },
              "control": {
                "E": 0.03528830371107014,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.8837183316504231,
            "tier_direction": "unchanged"
          }
        },
        "confirmation": "unsettled",
        "control": "lap10",
        "descriptive": {
          "adjacent_time_similarity": {
            "main": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9991719722747803,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9994975924491882,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9996747970581055,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999667763710022,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9995802640914917,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9993537068367004,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9988868236541748,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977896809577942,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957582354545593,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9902614951133728,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9802796840667725,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9548972249031067,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9065284729003906,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9992821216583252,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9995830655097961,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9996691346168518,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9996691346168518,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9995714426040649,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9993807077407837,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989610910415649,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9980658292770386,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964843392372131,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9918122291564941,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9853606224060059,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9664384126663208,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9387646913528442,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9993089437484741,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9995527267456055,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9996832013130188,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9996577501296997,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9995419383049011,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9992556571960449,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9987489581108093,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9973639249801636,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9949964284896851,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9889902472496033,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9798128604888916,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.954068124294281,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9192755222320557,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9993932843208313,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9996213316917419,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9996817708015442,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9996457099914551,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9995383024215698,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9991779923439026,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9985479116439819,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9970045685768127,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9943064451217651,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.987529456615448,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9773064851760864,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9458729028701782,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9061102271080017,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9993279576301575,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9996461272239685,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9996885061264038,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9996469616889954,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9995276927947998,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9992029666900635,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9985825419425964,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9970065355300903,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9947906732559204,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.988234281539917,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9786360263824463,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9484249949455261,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9152524471282959,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999873042106628,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999829530715942,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999684691429138,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999327659606934,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998732805252075,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997059106826782,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999376654624939,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985236525535583,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968986511230469,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9926234483718872,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9842280149459839,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.96236252784729,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9214602708816528,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999871850013733,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999821782112122,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999961793422699,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999173283576965,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998281002044678,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996033310890198,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992149472236633,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982089996337891,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9966210126876831,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9922357797622681,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9855553507804871,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9679967761039734,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9486552476882935,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999873042106628,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999816417694092,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999540448188782,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998989105224609,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999788761138916,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995148181915283,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990537762641907,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977971315383911,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960052371025085,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9909918308258057,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9850074052810669,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9683241248130798,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9572503566741943,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999868869781494,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999809861183167,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999610781669617,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999128580093384,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998356699943542,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996131062507629,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992409944534302,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982267022132874,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996870219707489,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9930270910263062,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9882631301879883,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9749119281768799,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9650939702987671,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987006187439,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999980092048645,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999533891677856,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998939037322998,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997878074645996,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.99949049949646,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990198612213135,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977650046348572,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960800409317017,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9911503791809082,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985751211643219,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9696986675262451,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9610034227371216,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ]
            },
            "repeat-seed": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9991569519042969,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9994996190071106,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9996533393859863,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9996752738952637,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9996132850646973,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994387626647949,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990665316581726,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982568025588989,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964617490768433,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9921863079071045,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9840353727340698,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9639124274253845,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9285779595375061,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9993404150009155,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9995624423027039,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9996408820152283,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9996793270111084,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9996018409729004,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994047284126282,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989385008811951,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979051351547241,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960792064666748,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9911547303199768,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9838520884513855,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9627888202667236,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9319043159484863,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9992825984954834,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9996140003204346,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9996790289878845,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9996694922447205,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9995803236961365,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9993255734443665,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9988340139389038,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9975650310516357,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9953274726867676,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9898717999458313,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9798969626426697,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9519127607345581,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9120202660560608,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9993909597396851,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999636709690094,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9996839165687561,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9996542930603027,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9995697736740112,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9993327260017395,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.998801589012146,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9974966645240784,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9952645301818848,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9893298149108887,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.97959965467453,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9529110789299011,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9125036597251892,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9993290901184082,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9996216893196106,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9996609687805176,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9996365308761597,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9994516372680664,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999006986618042,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9983392953872681,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9963235855102539,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9925035238265991,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9828728437423706,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9671689867973328,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.923717200756073,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.8701943159103394,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999874234199524,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999818801879883,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999678730964661,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999345541000366,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998724460601807,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997184872627258,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993950128555298,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986075758934021,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970444440841675,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929084181785583,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9849348068237305,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9640600085258484,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.926579475402832,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999871850013733,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999825358390808,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999580979347229,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999078512191772,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998064041137695,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995436668395996,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.99908846616745,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978458285331726,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959667921066284,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.990613579750061,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9832639098167419,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9629725217819214,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9418724179267883,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999865293502808,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999804496765137,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999541640281677,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998980760574341,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997842311859131,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995024800300598,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989869594573975,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976776242256165,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958101511001587,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9903093576431274,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9834225177764893,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9647646546363831,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9509849548339844,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987006187439,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999791979789734,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999513626098633,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998918175697327,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997658133506775,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994567632675171,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989712238311768,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997593104839325,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957067370414734,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9903287291526794,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9838626980781555,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9657849073410034,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9564179182052612,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999861121177673,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999791979789734,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999459385871887,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998733997344971,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997392892837524,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9993844032287598,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9987626075744629,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9971981644630432,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9951921105384827,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9891223907470703,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9829607009887695,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9644073843955994,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9555770754814148,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ]
            },
            "repeat-system": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9958465099334717,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9974307417869568,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9986147880554199,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9988457560539246,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9990021586418152,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.998900294303894,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.998551607131958,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9975950717926025,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9955998659133911,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9905875325202942,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9823861718177795,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9617387056350708,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9222621321678162,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9965462684631348,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9981693625450134,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9987673759460449,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9987974762916565,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9989848732948303,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9989613890647888,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9988176822662354,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9980992674827576,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.99672532081604,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9938521981239319,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.989181399345398,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9756486415863037,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9571331143379211,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9969741106033325,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9982642531394958,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9986542463302612,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9989283084869385,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9989914894104004,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9989500641822815,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9987200498580933,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9980498552322388,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9967523217201233,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9930037260055542,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9877586364746094,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9717199802398682,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9486828446388245,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9967404007911682,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9985077381134033,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9989002346992493,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9989335536956787,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9988841414451599,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9988909363746643,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9986374974250793,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978707432746887,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9962406754493713,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9922072887420654,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9861577153205872,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9692749977111816,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9435834288597107,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.997117280960083,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9985933899879456,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9988023042678833,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9989850521087646,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9989699721336365,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9987022876739502,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9981182813644409,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9960942268371582,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9935452342033386,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.986186683177948,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9754413366317749,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9408044219017029,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9031451344490051,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999955415725708,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999606609344482,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999479651451111,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999155402183533,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998494982719421,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996647238731384,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993292093276978,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9984490275382996,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9966986179351807,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9922631978988647,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9839369654655457,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.96240234375,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9206265807151794,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999579191207886,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999600052833557,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999388456344604,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998790621757507,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997878074645996,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995396733283997,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990968704223633,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978508353233337,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957573413848877,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9903771281242371,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9829946160316467,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9624257683753967,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9388824701309204,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999600052833557,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999597668647766,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999329447746277,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998740553855896,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997615218162537,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994500875473022,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.998892605304718,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9975738525390625,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9951943755149841,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.988853394985199,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9804162383079529,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9556616544723511,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9328624606132507,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999579191207886,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999958872795105,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999295473098755,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998630285263062,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997533559799194,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994406700134277,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.998871386051178,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9973885416984558,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9950183033943176,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9884749054908752,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.980159342288971,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9563855528831482,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9350361824035645,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999602437019348,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999583959579468,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999322295188904,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998706579208374,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997504949569702,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994411468505859,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.998908519744873,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9973835349082947,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9952226877212524,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.989122211933136,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9813206195831299,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9585052132606506,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9387605786323547,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp05",
        "reasons": [
          "the main/arm endpoint is unsettled",
          "the main/control endpoint is unsettled",
          "the repeat-system/arm endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      },
      "lap5": {
        "arm": "lap5",
        "cases": {
          "main": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.013948577928655764,
                "tier": 1
              },
              "control": {
                "E": 0.027243759954814768,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.4880083383574725,
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
                "E": 0.036324687262097394,
                "tier": 1
              },
              "control": {
                "E": 0.11465182676222399,
                "tier": 0
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.68317393374437,
            "tier_direction": "improved"
          },
          "repeat-system": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.01650364030491745,
                "tier": 1
              },
              "control": {
                "E": 0.03528830371107014,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.5323198179191548,
            "tier_direction": "unchanged"
          }
        },
        "confirmation": "unsettled",
        "control": "lap10",
        "descriptive": {
          "adjacent_time_similarity": {
            "main": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999392032623291,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999495148658752,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999383091926575,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999893307685852,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998189210891724,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996331930160522,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992458820343018,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.998313844203949,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9965479373931885,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9919084906578064,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9830166101455688,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9599262475967407,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9162378311157227,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999358654022217,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999502301216125,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999287128448486,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998726844787598,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997519850730896,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994785189628601,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990395307540894,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976620078086853,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9954438209533691,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.98956298828125,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9815946817398071,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9580857157707214,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9324420094490051,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999945878982544,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999502301216125,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999280571937561,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998719692230225,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997705817222595,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995094537734985,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990266561508179,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977697730064392,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958814978599548,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9902663826942444,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9832229018211365,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9619787931442261,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9401376843452454,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999946117401123,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999489784240723,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999294877052307,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998756647109985,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999763548374176,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995157122612,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990566968917847,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979296922683716,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960364103317261,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9909098744392395,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9842959046363831,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9650753736495972,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9465456008911133,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999442100524902,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999476671218872,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999916672706604,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998413920402527,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997032880783081,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9993078112602234,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9986446499824524,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9969096183776855,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9943974614143372,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9869930148124695,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9783313274383545,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9513484835624695,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9290145039558411,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999873042106628,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999829530715942,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999684691429138,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999327659606934,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998732805252075,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997059106826782,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999376654624939,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985236525535583,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968986511230469,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9926234483718872,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9842280149459839,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.96236252784729,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9214602708816528,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999871850013733,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999821782112122,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999961793422699,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999173283576965,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998281002044678,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996033310890198,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992149472236633,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982089996337891,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9966210126876831,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9922357797622681,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9855553507804871,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9679967761039734,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9486552476882935,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999873042106628,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999816417694092,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999540448188782,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998989105224609,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999788761138916,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995148181915283,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990537762641907,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977971315383911,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960052371025085,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9909918308258057,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9850074052810669,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9683241248130798,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9572503566741943,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999868869781494,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999809861183167,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999610781669617,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999128580093384,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998356699943542,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996131062507629,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992409944534302,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9982267022132874,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996870219707489,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9930270910263062,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9882631301879883,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9749119281768799,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9650939702987671,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987006187439,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999980092048645,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999533891677856,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998939037322998,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997878074645996,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.99949049949646,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990198612213135,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9977650046348572,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9960800409317017,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9911503791809082,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985751211643219,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9696986675262451,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9610034227371216,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ]
            },
            "repeat-seed": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999376535415649,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999502301216125,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999390840530396,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999048709869385,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998411536216736,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996863603591919,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993696808815002,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986479878425598,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970971345901489,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9930521845817566,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985528826713562,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9654781818389893,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9297792911529541,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999390840530396,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999497532844543,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999340176582336,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998780488967896,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997864961624146,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995545744895935,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991223812103271,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979690313339233,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9962936639785767,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9914025664329529,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9841527938842773,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9646382331848145,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9431871771812439,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999406337738037,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999486804008484,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999271631240845,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998672604560852,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997568726539612,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994595050811768,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989979267120361,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976691007614136,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9956722855567932,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9900476932525635,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9828184843063354,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.96163409948349,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9402247667312622,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999439716339111,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999488592147827,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999253749847412,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998689293861389,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997562170028687,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994751214981079,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989714026451111,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997664749622345,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958385229110718,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9903201460838318,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9834015965461731,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9635102152824402,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9453679919242859,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999943196773529,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999473094940186,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999139904975891,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998420476913452,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9996933341026306,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9992796182632446,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9986579418182373,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.996939480304718,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9943649172782898,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9867590665817261,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.977100670337677,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9502837061882019,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9262836575508118,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999874234199524,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999818801879883,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999678730964661,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999345541000366,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998724460601807,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997184872627258,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993950128555298,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986075758934021,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970444440841675,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929084181785583,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9849348068237305,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9640600085258484,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.926579475402832,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999871850013733,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999825358390808,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999580979347229,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999078512191772,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998064041137695,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995436668395996,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.99908846616745,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978458285331726,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9959667921066284,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.990613579750061,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9832639098167419,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9629725217819214,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9418724179267883,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999865293502808,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999804496765137,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999541640281677,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998980760574341,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997842311859131,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995024800300598,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989869594573975,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976776242256165,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958101511001587,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9903093576431274,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9834225177764893,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9647646546363831,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9509849548339844,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987006187439,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999791979789734,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999513626098633,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998918175697327,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997658133506775,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994567632675171,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989712238311768,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.997593104839325,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957067370414734,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9903287291526794,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9838626980781555,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9657849073410034,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9564179182052612,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999861121177673,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999791979789734,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999459385871887,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998733997344971,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997392892837524,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9993844032287598,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9987626075744629,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9971981644630432,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9951921105384827,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9891223907470703,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9829607009887695,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9644073843955994,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9555770754814148,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ]
            },
            "repeat-system": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9997128248214722,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999797523021698,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9998312592506409,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998215436935425,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997625946998596,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995811581611633,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992204308509827,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9983556866645813,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9967003464698792,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9924346208572388,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9846704006195068,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9647254347801208,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9265750646591187,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9996958374977112,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9998092651367188,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9998365044593811,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9997907280921936,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997049570083618,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994620680809021,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990313053131104,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978781342506409,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961994290351868,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991091251373291,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.983650803565979,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9624057412147522,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9342164993286133,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9997289776802063,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9998335242271423,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9998384118080139,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9997922778129578,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9996874332427979,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994354248046875,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9988248348236084,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9973855018615723,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.994877278804779,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9883467555046082,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9778051972389221,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9488630294799805,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9128472805023193,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9997544884681702,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9998278021812439,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9998294115066528,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9997754693031311,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9996526837348938,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999332845211029,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9986583590507507,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9970963001251221,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9941522479057312,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9865451455116272,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9721718430519104,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9359248280525208,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.8813819289207458,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9997221827507019,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9998369216918945,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9998321533203125,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999762237071991,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9996456503868103,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9993119835853577,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9987146258354187,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9971403479576111,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9945423603057861,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9871588349342346,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9770093560218811,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9466546773910522,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9075921773910522,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999955415725708,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999606609344482,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999479651451111,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999155402183533,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998494982719421,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996647238731384,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993292093276978,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9984490275382996,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9966986179351807,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9922631978988647,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9839369654655457,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.96240234375,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9206265807151794,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999579191207886,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999600052833557,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999388456344604,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998790621757507,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997878074645996,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995396733283997,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990968704223633,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978508353233337,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9957573413848877,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9903771281242371,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9829946160316467,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9624257683753967,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9388824701309204,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 37175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999600052833557,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999597668647766,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999329447746277,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998740553855896,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997615218162537,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994500875473022,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.998892605304718,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9975738525390625,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9951943755149841,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.988853394985199,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9804162383079529,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9556616544723511,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9328624606132507,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 74350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999579191207886,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.999958872795105,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999295473098755,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998630285263062,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997533559799194,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994406700134277,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.998871386051178,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9973885416984558,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9950183033943176,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9884749054908752,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.980159342288971,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9563855528831482,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9350361824035645,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 111525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999602437019348,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999583959579468,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999322295188904,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998706579208374,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997504949569702,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994411468505859,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.998908519744873,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9973835349082947,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9952226877212524,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.989122211933136,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9813206195831299,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9585052132606506,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9387605786323547,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 148700
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp05",
        "reasons": [
          "the main/arm endpoint is unsettled",
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
    "experiment": "exp05",
    "unconfirmed": [
      {
        "arm": "lap1",
        "confirmation": "unsettled",
        "reasons": [
          "the main/arm endpoint is unsettled",
          "the main/control endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled"
        ]
      },
      {
        "arm": "lap2",
        "confirmation": "unsettled",
        "reasons": [
          "the main/arm endpoint is unsettled",
          "the main/control endpoint is unsettled",
          "the repeat-system/arm endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled"
        ]
      },
      {
        "arm": "lap5",
        "confirmation": "unsettled",
        "reasons": [
          "the main/arm endpoint is unsettled",
          "the main/control endpoint is unsettled",
          "the repeat-system/arm endpoint is unsettled",
          "the repeat-system/control endpoint is unsettled"
        ]
      }
    ]
  },
  "contrasts": {
    "lap1": {
      "arm": "lap1",
      "cases": {
        "main": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.005407673830025773,
              "tier": 1
            },
            "control": {
              "E": 0.027243759954814768,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.8015078007222686,
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
              "E": 0.015676362749794264,
              "tier": 1
            },
            "control": {
              "E": 0.11465182676222399,
              "tier": 0
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.8632698388460446,
          "tier_direction": "improved"
        },
        "repeat-system": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "settled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.012315061236409686,
              "tier": 1
            },
            "control": {
              "E": 0.03528830371107014,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.651015777430345,
          "tier_direction": "unchanged"
        }
      },
      "confirmation": "unsettled",
      "control": "lap10",
      "descriptive": {
        "adjacent_time_similarity": {
          "main": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9938457012176514,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9964244365692139,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9979904890060425,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9985747337341309,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9986845254898071,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9985023736953735,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9980407953262329,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9966896176338196,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9942570924758911,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9884307980537415,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9774336218833923,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9495965242385864,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.8968390226364136,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9941507577896118,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9978240728378296,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9982323050498962,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9985566735267639,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9986580014228821,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.998711347579956,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9984447360038757,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978814125061035,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9966490268707275,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9934003353118896,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9885785579681396,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9752222299575806,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9550203084945679,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9951128363609314,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9978105425834656,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.998327374458313,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9985527396202087,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9986785650253296,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9987319707870483,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9985957145690918,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982414841651917,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9975666999816895,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9960021376609802,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9934777617454529,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9859269261360168,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9758686423301697,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.995894730091095,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9978885650634766,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9983782172203064,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9986359477043152,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9987887740135193,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9987199306488037,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9985138177871704,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978376626968384,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9963917136192322,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929416179656982,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9857869744300842,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9670734405517578,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9365713000297546,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9955934286117554,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9978163838386536,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9984643459320068,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.998612642288208,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.998651385307312,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9986093044281006,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9982799291610718,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997417151927948,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9955117702484131,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9906006455421448,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9843290448188782,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9631816148757935,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9307559132575989,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999873042106628,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999829530715942,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999684691429138,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999327659606934,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998732805252075,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997059106826782,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999376654624939,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985236525535583,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968986511230469,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9926234483718872,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9842280149459839,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.96236252784729,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9214602708816528,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999871850013733,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999821782112122,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999961793422699,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999173283576965,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998281002044678,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996033310890198,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992149472236633,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982089996337891,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9966210126876831,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9922357797622681,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9855553507804871,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9679967761039734,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9486552476882935,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999873042106628,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999816417694092,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999540448188782,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998989105224609,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999788761138916,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995148181915283,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990537762641907,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977971315383911,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960052371025085,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9909918308258057,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9850074052810669,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9683241248130798,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9572503566741943,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999868869781494,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999809861183167,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999610781669617,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999128580093384,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998356699943542,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996131062507629,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992409944534302,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982267022132874,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996870219707489,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9930270910263062,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9882631301879883,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9749119281768799,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9650939702987671,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987006187439,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999980092048645,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999533891677856,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998939037322998,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997878074645996,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.99949049949646,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990198612213135,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977650046348572,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960800409317017,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9911503791809082,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985751211643219,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9696986675262451,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9610034227371216,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ]
          },
          "repeat-seed": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9938263893127441,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9963534474372864,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9979745745658875,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9982947111129761,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.998656153678894,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.99858158826828,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9981763362884521,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9973181486129761,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9956678152084351,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9910469651222229,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9828280806541443,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9622671008110046,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9259752631187439,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.995459794998169,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9976152777671814,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9984028339385986,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9983202219009399,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9985756874084473,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.998735785484314,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.998624324798584,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982497096061707,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.997159481048584,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9946970343589783,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9911864995956421,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9798681735992432,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9640430808067322,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9958539605140686,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.998053789138794,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9983298778533936,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9986382722854614,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9987799525260925,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9987823367118835,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9986356496810913,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.998235285282135,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9974769949913025,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.995435357093811,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.992275059223175,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9812233448028564,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9669778943061829,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9963444471359253,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9977819323539734,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9983490109443665,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9986317753791809,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9987672567367554,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9987106919288635,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9984859824180603,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977421760559082,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9962281584739685,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9922602772712708,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9863338470458984,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9686866998672485,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9445493817329407,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9964916110038757,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.99791020154953,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9980717897415161,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9986920952796936,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9987788796424866,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9986541867256165,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9982323050498962,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9970716834068298,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9941815733909607,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9871310591697693,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9777007102966309,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9481189846992493,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9085423350334167,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999874234199524,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999818801879883,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999678730964661,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999345541000366,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998724460601807,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997184872627258,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993950128555298,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986075758934021,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970444440841675,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929084181785583,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9849348068237305,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9640600085258484,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.926579475402832,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999871850013733,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999825358390808,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999580979347229,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999078512191772,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998064041137695,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995436668395996,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.99908846616745,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978458285331726,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959667921066284,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.990613579750061,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9832639098167419,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9629725217819214,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9418724179267883,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999865293502808,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999804496765137,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999541640281677,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998980760574341,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997842311859131,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995024800300598,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989869594573975,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976776242256165,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958101511001587,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9903093576431274,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9834225177764893,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9647646546363831,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9509849548339844,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987006187439,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999791979789734,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999513626098633,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998918175697327,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997658133506775,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994567632675171,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989712238311768,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997593104839325,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957067370414734,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9903287291526794,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9838626980781555,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9657849073410034,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9564179182052612,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999861121177673,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999791979789734,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999459385871887,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998733997344971,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997392892837524,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9993844032287598,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9987626075744629,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9971981644630432,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9951921105384827,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9891223907470703,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9829607009887695,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9644073843955994,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9555770754814148,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ]
          },
          "repeat-system": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9765540361404419,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9832199215888977,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.990013062953949,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9924786686897278,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9954972267150879,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.996017336845398,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9961075186729431,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9953919649124146,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9933848977088928,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9882489442825317,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9802534580230713,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9591556191444397,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9206137657165527,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9798721075057983,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.989078938961029,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9921504259109497,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9935716986656189,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9939422607421875,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.994914174079895,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.995358943939209,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9957630038261414,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959380626678467,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9958773851394653,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9953582286834717,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9932984113693237,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9897904396057129,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9815347194671631,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9901346564292908,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9919463396072388,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9932215213775635,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9945776462554932,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9954935908317566,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9960461258888245,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9960839152336121,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9951769709587097,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9931687116622925,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9899098873138428,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9802233576774597,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9650889039039612,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9849295616149902,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9915348887443542,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9931098818778992,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9941876530647278,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9946734309196472,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9955689907073975,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9957655668258667,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9961029887199402,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9956105351448059,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9943951964378357,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9925156235694885,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9870995283126831,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9800121784210205,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9840295314788818,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9909984469413757,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9923029541969299,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9936966896057129,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9950492978096008,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9959349632263184,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.996029794216156,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9955248236656189,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9942203164100647,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9898468852043152,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9822054505348206,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9618450999259949,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9315370917320251,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999955415725708,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999606609344482,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999479651451111,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999155402183533,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998494982719421,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996647238731384,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993292093276978,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9984490275382996,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9966986179351807,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9922631978988647,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9839369654655457,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.96240234375,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9206265807151794,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999579191207886,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999600052833557,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999388456344604,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998790621757507,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997878074645996,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995396733283997,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990968704223633,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978508353233337,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957573413848877,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9903771281242371,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9829946160316467,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9624257683753967,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9388824701309204,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999600052833557,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999597668647766,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999329447746277,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998740553855896,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997615218162537,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994500875473022,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.998892605304718,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9975738525390625,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9951943755149841,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.988853394985199,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9804162383079529,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9556616544723511,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9328624606132507,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999579191207886,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999958872795105,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999295473098755,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998630285263062,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997533559799194,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994406700134277,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.998871386051178,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9973885416984558,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9950183033943176,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9884749054908752,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.980159342288971,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9563855528831482,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9350361824035645,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999602437019348,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999583959579468,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999322295188904,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998706579208374,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997504949569702,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994411468505859,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.998908519744873,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9973835349082947,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9952226877212524,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.989122211933136,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9813206195831299,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9585052132606506,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9387605786323547,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp05",
      "reasons": [
        "the main/arm endpoint is unsettled",
        "the main/control endpoint is unsettled",
        "the repeat-system/control endpoint is unsettled"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    },
    "lap2": {
      "arm": "lap2",
      "cases": {
        "main": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.015753288018634588,
              "tier": 1
            },
            "control": {
              "E": 0.027243759954814768,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.4217652759838489,
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
              "E": 0.09900171619123573,
              "tier": 1
            },
            "control": {
              "E": 0.11465182676222399,
              "tier": 0
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.13650118810095344,
          "tier_direction": "improved"
        },
        "repeat-system": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.0041033828287498,
              "tier": 1
            },
            "control": {
              "E": 0.03528830371107014,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.8837183316504231,
          "tier_direction": "unchanged"
        }
      },
      "confirmation": "unsettled",
      "control": "lap10",
      "descriptive": {
        "adjacent_time_similarity": {
          "main": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9991719722747803,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9994975924491882,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9996747970581055,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999667763710022,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9995802640914917,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9993537068367004,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9988868236541748,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977896809577942,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957582354545593,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9902614951133728,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9802796840667725,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9548972249031067,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9065284729003906,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9992821216583252,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9995830655097961,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9996691346168518,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9996691346168518,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9995714426040649,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9993807077407837,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989610910415649,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9980658292770386,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964843392372131,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9918122291564941,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9853606224060059,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9664384126663208,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9387646913528442,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9993089437484741,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9995527267456055,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9996832013130188,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9996577501296997,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9995419383049011,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9992556571960449,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9987489581108093,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9973639249801636,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9949964284896851,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9889902472496033,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9798128604888916,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.954068124294281,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9192755222320557,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9993932843208313,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9996213316917419,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9996817708015442,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9996457099914551,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9995383024215698,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9991779923439026,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9985479116439819,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9970045685768127,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9943064451217651,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.987529456615448,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9773064851760864,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9458729028701782,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9061102271080017,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9993279576301575,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9996461272239685,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9996885061264038,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9996469616889954,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9995276927947998,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9992029666900635,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9985825419425964,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9970065355300903,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9947906732559204,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.988234281539917,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9786360263824463,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9484249949455261,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9152524471282959,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999873042106628,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999829530715942,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999684691429138,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999327659606934,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998732805252075,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997059106826782,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999376654624939,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985236525535583,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968986511230469,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9926234483718872,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9842280149459839,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.96236252784729,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9214602708816528,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999871850013733,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999821782112122,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999961793422699,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999173283576965,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998281002044678,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996033310890198,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992149472236633,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982089996337891,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9966210126876831,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9922357797622681,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9855553507804871,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9679967761039734,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9486552476882935,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999873042106628,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999816417694092,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999540448188782,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998989105224609,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999788761138916,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995148181915283,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990537762641907,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977971315383911,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960052371025085,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9909918308258057,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9850074052810669,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9683241248130798,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9572503566741943,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999868869781494,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999809861183167,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999610781669617,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999128580093384,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998356699943542,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996131062507629,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992409944534302,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982267022132874,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996870219707489,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9930270910263062,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9882631301879883,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9749119281768799,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9650939702987671,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987006187439,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999980092048645,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999533891677856,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998939037322998,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997878074645996,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.99949049949646,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990198612213135,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977650046348572,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960800409317017,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9911503791809082,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985751211643219,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9696986675262451,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9610034227371216,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ]
          },
          "repeat-seed": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9991569519042969,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9994996190071106,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9996533393859863,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9996752738952637,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9996132850646973,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994387626647949,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990665316581726,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982568025588989,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964617490768433,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9921863079071045,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9840353727340698,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9639124274253845,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9285779595375061,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9993404150009155,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9995624423027039,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9996408820152283,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9996793270111084,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9996018409729004,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994047284126282,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989385008811951,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979051351547241,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960792064666748,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9911547303199768,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9838520884513855,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9627888202667236,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9319043159484863,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9992825984954834,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9996140003204346,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9996790289878845,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9996694922447205,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9995803236961365,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9993255734443665,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9988340139389038,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9975650310516357,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9953274726867676,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9898717999458313,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9798969626426697,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9519127607345581,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9120202660560608,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9993909597396851,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999636709690094,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9996839165687561,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9996542930603027,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9995697736740112,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9993327260017395,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.998801589012146,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9974966645240784,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9952645301818848,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9893298149108887,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.97959965467453,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9529110789299011,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9125036597251892,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9993290901184082,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9996216893196106,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9996609687805176,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9996365308761597,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9994516372680664,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999006986618042,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9983392953872681,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9963235855102539,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9925035238265991,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9828728437423706,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9671689867973328,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.923717200756073,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.8701943159103394,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999874234199524,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999818801879883,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999678730964661,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999345541000366,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998724460601807,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997184872627258,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993950128555298,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986075758934021,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970444440841675,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929084181785583,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9849348068237305,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9640600085258484,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.926579475402832,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999871850013733,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999825358390808,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999580979347229,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999078512191772,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998064041137695,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995436668395996,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.99908846616745,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978458285331726,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959667921066284,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.990613579750061,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9832639098167419,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9629725217819214,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9418724179267883,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999865293502808,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999804496765137,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999541640281677,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998980760574341,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997842311859131,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995024800300598,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989869594573975,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976776242256165,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958101511001587,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9903093576431274,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9834225177764893,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9647646546363831,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9509849548339844,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987006187439,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999791979789734,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999513626098633,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998918175697327,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997658133506775,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994567632675171,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989712238311768,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997593104839325,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957067370414734,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9903287291526794,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9838626980781555,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9657849073410034,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9564179182052612,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999861121177673,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999791979789734,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999459385871887,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998733997344971,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997392892837524,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9993844032287598,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9987626075744629,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9971981644630432,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9951921105384827,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9891223907470703,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9829607009887695,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9644073843955994,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9555770754814148,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ]
          },
          "repeat-system": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9958465099334717,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9974307417869568,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9986147880554199,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9988457560539246,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9990021586418152,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.998900294303894,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.998551607131958,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9975950717926025,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9955998659133911,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9905875325202942,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9823861718177795,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9617387056350708,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9222621321678162,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9965462684631348,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9981693625450134,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9987673759460449,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9987974762916565,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9989848732948303,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9989613890647888,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9988176822662354,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9980992674827576,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.99672532081604,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9938521981239319,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.989181399345398,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9756486415863037,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9571331143379211,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9969741106033325,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9982642531394958,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9986542463302612,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9989283084869385,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9989914894104004,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9989500641822815,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9987200498580933,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9980498552322388,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9967523217201233,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9930037260055542,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9877586364746094,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9717199802398682,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9486828446388245,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9967404007911682,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9985077381134033,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9989002346992493,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9989335536956787,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9988841414451599,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9988909363746643,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9986374974250793,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978707432746887,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9962406754493713,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9922072887420654,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9861577153205872,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9692749977111816,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9435834288597107,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.997117280960083,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9985933899879456,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9988023042678833,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9989850521087646,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9989699721336365,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9987022876739502,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9981182813644409,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9960942268371582,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9935452342033386,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.986186683177948,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9754413366317749,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9408044219017029,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9031451344490051,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999955415725708,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999606609344482,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999479651451111,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999155402183533,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998494982719421,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996647238731384,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993292093276978,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9984490275382996,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9966986179351807,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9922631978988647,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9839369654655457,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.96240234375,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9206265807151794,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999579191207886,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999600052833557,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999388456344604,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998790621757507,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997878074645996,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995396733283997,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990968704223633,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978508353233337,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957573413848877,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9903771281242371,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9829946160316467,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9624257683753967,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9388824701309204,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999600052833557,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999597668647766,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999329447746277,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998740553855896,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997615218162537,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994500875473022,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.998892605304718,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9975738525390625,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9951943755149841,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.988853394985199,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9804162383079529,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9556616544723511,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9328624606132507,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999579191207886,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999958872795105,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999295473098755,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998630285263062,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997533559799194,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994406700134277,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.998871386051178,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9973885416984558,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9950183033943176,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9884749054908752,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.980159342288971,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9563855528831482,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9350361824035645,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999602437019348,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999583959579468,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999322295188904,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998706579208374,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997504949569702,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994411468505859,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.998908519744873,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9973835349082947,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9952226877212524,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.989122211933136,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9813206195831299,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9585052132606506,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9387605786323547,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp05",
      "reasons": [
        "the main/arm endpoint is unsettled",
        "the main/control endpoint is unsettled",
        "the repeat-system/arm endpoint is unsettled",
        "the repeat-system/control endpoint is unsettled"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    },
    "lap5": {
      "arm": "lap5",
      "cases": {
        "main": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.013948577928655764,
              "tier": 1
            },
            "control": {
              "E": 0.027243759954814768,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.4880083383574725,
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
              "E": 0.036324687262097394,
              "tier": 1
            },
            "control": {
              "E": 0.11465182676222399,
              "tier": 0
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.68317393374437,
          "tier_direction": "improved"
        },
        "repeat-system": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.01650364030491745,
              "tier": 1
            },
            "control": {
              "E": 0.03528830371107014,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.5323198179191548,
          "tier_direction": "unchanged"
        }
      },
      "confirmation": "unsettled",
      "control": "lap10",
      "descriptive": {
        "adjacent_time_similarity": {
          "main": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999392032623291,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999495148658752,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999383091926575,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999893307685852,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998189210891724,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996331930160522,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992458820343018,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.998313844203949,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9965479373931885,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9919084906578064,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9830166101455688,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9599262475967407,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9162378311157227,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999358654022217,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999502301216125,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999287128448486,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998726844787598,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997519850730896,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994785189628601,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990395307540894,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976620078086853,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9954438209533691,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.98956298828125,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9815946817398071,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9580857157707214,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9324420094490051,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999945878982544,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999502301216125,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999280571937561,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998719692230225,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997705817222595,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995094537734985,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990266561508179,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977697730064392,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958814978599548,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9902663826942444,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9832229018211365,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9619787931442261,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9401376843452454,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999946117401123,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999489784240723,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999294877052307,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998756647109985,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999763548374176,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995157122612,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990566968917847,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979296922683716,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960364103317261,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9909098744392395,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9842959046363831,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9650753736495972,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9465456008911133,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999442100524902,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999476671218872,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999916672706604,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998413920402527,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997032880783081,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9993078112602234,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9986446499824524,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9969096183776855,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9943974614143372,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9869930148124695,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9783313274383545,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9513484835624695,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9290145039558411,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999873042106628,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999829530715942,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999684691429138,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999327659606934,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998732805252075,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997059106826782,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999376654624939,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985236525535583,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968986511230469,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9926234483718872,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9842280149459839,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.96236252784729,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9214602708816528,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999871850013733,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999821782112122,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999961793422699,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999173283576965,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998281002044678,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996033310890198,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992149472236633,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982089996337891,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9966210126876831,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9922357797622681,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9855553507804871,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9679967761039734,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9486552476882935,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999873042106628,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999816417694092,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999540448188782,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998989105224609,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999788761138916,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995148181915283,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990537762641907,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977971315383911,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960052371025085,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9909918308258057,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9850074052810669,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9683241248130798,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9572503566741943,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999868869781494,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999809861183167,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999610781669617,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999128580093384,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998356699943542,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996131062507629,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992409944534302,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9982267022132874,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996870219707489,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9930270910263062,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9882631301879883,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9749119281768799,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9650939702987671,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987006187439,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999980092048645,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999533891677856,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998939037322998,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997878074645996,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.99949049949646,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990198612213135,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9977650046348572,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9960800409317017,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9911503791809082,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985751211643219,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9696986675262451,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9610034227371216,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ]
          },
          "repeat-seed": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999376535415649,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999502301216125,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999390840530396,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999048709869385,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998411536216736,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996863603591919,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993696808815002,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986479878425598,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970971345901489,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9930521845817566,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985528826713562,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9654781818389893,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9297792911529541,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999390840530396,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999497532844543,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999340176582336,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998780488967896,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997864961624146,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995545744895935,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991223812103271,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979690313339233,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9962936639785767,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9914025664329529,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9841527938842773,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9646382331848145,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9431871771812439,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999406337738037,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999486804008484,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999271631240845,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998672604560852,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997568726539612,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994595050811768,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989979267120361,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976691007614136,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9956722855567932,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9900476932525635,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9828184843063354,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.96163409948349,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9402247667312622,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999439716339111,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999488592147827,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999253749847412,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998689293861389,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997562170028687,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994751214981079,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989714026451111,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997664749622345,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958385229110718,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9903201460838318,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9834015965461731,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9635102152824402,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9453679919242859,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999943196773529,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999473094940186,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999139904975891,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998420476913452,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9996933341026306,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9992796182632446,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9986579418182373,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.996939480304718,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9943649172782898,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9867590665817261,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.977100670337677,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9502837061882019,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9262836575508118,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999874234199524,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999818801879883,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999678730964661,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999345541000366,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998724460601807,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997184872627258,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993950128555298,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986075758934021,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970444440841675,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929084181785583,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9849348068237305,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9640600085258484,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.926579475402832,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999871850013733,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999825358390808,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999580979347229,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999078512191772,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998064041137695,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995436668395996,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.99908846616745,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978458285331726,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9959667921066284,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.990613579750061,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9832639098167419,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9629725217819214,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9418724179267883,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999865293502808,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999804496765137,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999541640281677,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998980760574341,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997842311859131,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995024800300598,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989869594573975,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976776242256165,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958101511001587,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9903093576431274,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9834225177764893,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9647646546363831,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9509849548339844,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987006187439,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999791979789734,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999513626098633,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998918175697327,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997658133506775,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994567632675171,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989712238311768,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.997593104839325,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957067370414734,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9903287291526794,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9838626980781555,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9657849073410034,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9564179182052612,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999861121177673,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999791979789734,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999459385871887,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998733997344971,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997392892837524,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9993844032287598,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9987626075744629,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9971981644630432,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9951921105384827,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9891223907470703,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9829607009887695,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9644073843955994,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9555770754814148,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ]
          },
          "repeat-system": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9997128248214722,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999797523021698,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9998312592506409,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998215436935425,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997625946998596,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995811581611633,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992204308509827,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9983556866645813,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9967003464698792,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9924346208572388,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9846704006195068,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9647254347801208,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9265750646591187,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9996958374977112,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9998092651367188,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9998365044593811,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9997907280921936,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997049570083618,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994620680809021,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990313053131104,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978781342506409,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961994290351868,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991091251373291,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.983650803565979,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9624057412147522,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9342164993286133,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9997289776802063,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9998335242271423,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9998384118080139,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9997922778129578,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9996874332427979,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994354248046875,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9988248348236084,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9973855018615723,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.994877278804779,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9883467555046082,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9778051972389221,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9488630294799805,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9128472805023193,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9997544884681702,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9998278021812439,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9998294115066528,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9997754693031311,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9996526837348938,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999332845211029,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9986583590507507,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9970963001251221,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9941522479057312,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9865451455116272,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9721718430519104,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9359248280525208,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.8813819289207458,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9997221827507019,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9998369216918945,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9998321533203125,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999762237071991,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9996456503868103,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9993119835853577,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9987146258354187,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9971403479576111,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9945423603057861,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9871588349342346,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9770093560218811,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9466546773910522,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9075921773910522,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999955415725708,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999606609344482,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999479651451111,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999155402183533,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998494982719421,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996647238731384,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993292093276978,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9984490275382996,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9966986179351807,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9922631978988647,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9839369654655457,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.96240234375,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9206265807151794,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999579191207886,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999600052833557,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999388456344604,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998790621757507,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997878074645996,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995396733283997,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990968704223633,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978508353233337,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9957573413848877,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9903771281242371,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9829946160316467,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9624257683753967,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9388824701309204,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 37175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999600052833557,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999597668647766,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999329447746277,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998740553855896,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997615218162537,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994500875473022,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.998892605304718,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9975738525390625,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9951943755149841,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.988853394985199,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9804162383079529,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9556616544723511,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9328624606132507,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 74350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999579191207886,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.999958872795105,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999295473098755,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998630285263062,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997533559799194,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994406700134277,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.998871386051178,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9973885416984558,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9950183033943176,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9884749054908752,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.980159342288971,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9563855528831482,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9350361824035645,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 111525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999602437019348,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999583959579468,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999322295188904,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998706579208374,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997504949569702,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994411468505859,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.998908519744873,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9973835349082947,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9952226877212524,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.989122211933136,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9813206195831299,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9585052132606506,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9387605786323547,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 148700
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp05",
      "reasons": [
        "the main/arm endpoint is unsettled",
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
  "experiment": "exp05",
  "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
  "predictions_comparison": {
    "lap1": {
      "case_directions": {
        "main": "improvement",
        "repeat-seed": "improvement",
        "repeat-system": "improvement"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, shorter window improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    },
    "lap2": {
      "case_directions": {
        "main": "improvement",
        "repeat-seed": "improvement",
        "repeat-system": "improvement"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, shorter window improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    },
    "lap5": {
      "case_directions": {
        "main": "improvement",
        "repeat-seed": "improvement",
        "repeat-system": "improvement"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, shorter window improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    }
  },
  "proposed_change": null,
  "roadmap_comparison": "each contrast's confirmation label is read against the committed prediction table; the roadmap's next experiment proceeds only when this review allows the dependent launch",
  "schema": "phase67-review/v1",
  "scope49_disposition": "none"
}
```
