"""CONF-02 S_H pipeline invariants (plan 47-02).

The spec contract (``pinn_architecture.md`` §3.4:539-542, transcribed in
47-CONTEXT.md D-09/D-10): ``S_H = median_train(K0 + Uabs0)`` is computed ONCE,
in float64, at run setup before step 1, over the train split only, from the
matched-Plummer components at the training softening
``pinn.constants.EPS_SOFT = 1e-5`` — never per-minibatch, never recomputed
mid-run. ``Uabs0`` is the ABSOLUTE VALUE of the softened potential
(``V_eps < 0``, so ``Uabs0 = -V_eps``); ``K0 + Uabs0`` is strictly positive and
distinct from the signed ``H_0 = K0 + V_eps`` (D-10). Both components are
captured at admission from ``pre.r_gauge[0]`` / ``pre.v_gauge[0]`` /
``pre.masses_ordered`` — the completed CONF-09 frame tuple
``{position: r_prime, time: u, velocity: dr_prime_du, masses: ordered_raw}`` —
BEFORE the fp32 residency cast (D-12), and the median is never reduced from
fp32 resident tensors.

The softened pairwise sum has exactly ONE home —
``pinn.loss_catalog._matched_plummer_components`` (D-11): the admission capture
calls that seam rather than reimplementing the loop, and
``_matched_plummer_hamiltonian`` delegates to it with signature and return
value unchanged. The dual-epsilon defence is structural: no CONF-02 production
file references the invariants-side verification module or its epsilon
constant (47-02 Task 1 criterion 3); this test file is not a production file
and names that constant only to build the deliberately mis-softened oracle
that proves the capture used the training softening.

Train-free and dataset-free (SCOPE-27/28): every number comes from synthetic
snapshots, the phase-39 tiny corpus, or duck-typed stub sources.
"""

from __future__ import annotations

import inspect
from types import SimpleNamespace

import numpy as np
import torch

from pinn.constants import EPS_SOFT
from pinn.data.adapter import (
    BRUTUS_FOLDER_TABLE,
    AdmittedSetAdapter,
    parse_brutus_file,
)
from pinn.data.preprocessing import preprocess_trajectory
from pinn.data.splits import StageIndex, write_split_manifest
from pinn.data.types import RecordKey, StageLabel
from pinn.loss_catalog import _matched_plummer_components, _matched_plummer_hamiltonian
from pinn.verification.gate_metrics import EPS_INV
from tests.phase39._fixtures import TinyCorpus

_PAIRS = ((0, 1), (0, 2), (1, 2))
_CPU_F64 = dict(dtype=torch.float64, device=torch.device("cpu"))


# ---------------------------------------------------------------------------
# Fixture plumbing
# ---------------------------------------------------------------------------


def _adapter(corpus):
    return AdmittedSetAdapter(
        root=corpus.data_root,
        blacklist_path=corpus.blacklist_path,
        precision="float32",
        device="cpu",
        run_dir=corpus.run_dir,
        version_metadata_path=corpus.version_metadata_path,
    )


def _folder_for(variant, fidelity):
    for folder, (v, f) in BRUTUS_FOLDER_TABLE.items():
        if v == variant and f == fidelity:
            return folder
    raise KeyError((variant, fidelity))


# ---------------------------------------------------------------------------
# D-09/D-10/D-11/D-12 — the admission-time S_H components
# ---------------------------------------------------------------------------


def test_uabs0_is_absolute_value():
    """The captured pair is (kinetic, |softened potential|) at EPS_SOFT.

    (i)   the component seam returns ``(kinetic, potential)`` with
          ``potential < 0`` whose sum is bit-identical to
          ``_matched_plummer_hamiltonian`` (seam preservation, D-11);
    (ii)  the admission-captured ``uabs0`` equals ``abs(potential)`` computed
          in float64 at the training softening — never the signed Hamiltonian,
          never a mis-softened recomputation (D-09/D-10);
    (iii) captured ``k0``/``uabs0`` are Python floats carrying float64
          precision, computed from ``pre.r_gauge[0]`` / ``pre.v_gauge[0]`` /
          ``pre.masses_ordered`` (D-12).
    """
    # (i) seam shape and seam preservation on a synthetic 3-body snapshot.
    masses = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    positions = np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            [[0.1, 0.0, 0.0], [1.0, 0.1, 0.0], [0.0, 1.0, 0.1]],
        ],
        dtype=np.float64,
    )
    velocities = np.array(
        [
            [[0.1, 0.2, 0.3], [-0.2, 0.1, 0.0], [0.0, -0.1, 0.2]],
            [[0.2, 0.1, 0.0], [0.0, 0.3, -0.1], [0.1, 0.0, 0.1]],
        ],
        dtype=np.float64,
    )
    kinetic, potential = _matched_plummer_components(
        positions, velocities, masses, **_CPU_F64
    )
    assert tuple(kinetic.shape) == (2,)
    assert tuple(potential.shape) == (2,)
    assert bool(torch.all(kinetic > 0.0))
    assert bool(torch.all(potential < 0.0))

    hamiltonian = _matched_plummer_hamiltonian(
        positions, velocities, masses, **_CPU_F64
    )
    assert torch.equal(kinetic + potential, hamiltonian)

    # Closed-form components at the training softening. The independent numpy
    # oracle and the torch seam may differ by a few unit round-offs from
    # reduction order, so the bound is DERIVED from the float64 dtype contract
    # (never a declared physics tolerance); the bit-exact claim lives in the
    # torch.equal seam-preservation assertion above.
    speed_sq = (velocities * velocities).sum(-1)
    k_expected = 0.5 * (masses * speed_sq).sum(-1)
    v_expected = np.zeros(2, dtype=np.float64)
    for i, j in _PAIRS:
        delta = positions[:, j] - positions[:, i]
        r_safe = np.sqrt((delta * delta).sum(-1) + EPS_SOFT ** 2)
        v_expected -= masses[i] * masses[j] / r_safe
    f64_round = 8.0 * np.finfo(np.float64).eps
    for actual, expected in ((kinetic.numpy(), k_expected), (potential.numpy(), v_expected)):
        bound = f64_round * np.maximum(1.0, np.abs(expected))
        assert np.all(np.abs(actual - expected) <= bound)

    # (ii)/(iii) admission capture over the tiny corpus, recomputed
    # independently from the parsed source through preprocess_trajectory.
    with TinyCorpus() as corpus:
        adapter = _adapter(corpus)
        keys = adapter.record_keys()
        assert keys, "tiny corpus must admit records"
        for key in keys:
            path = corpus._brutus_path(
                _folder_for(key.variant, key.fidelity), key.variant, key.id
            )
            parsed = parse_brutus_file(path, root=corpus.data_root)
            pre = preprocess_trajectory(
                parsed.times, parsed.positions, parsed.velocities, parsed.masses
            )
            k_expected_t, v_expected_t = _matched_plummer_components(
                pre.r_gauge[0], pre.v_gauge[0], pre.masses_ordered, **_CPU_F64
            )
            record = adapter.get(key)
            # (iii) Python floats carrying float64 precision, from the
            # completed-frame float64 inputs at snapshot 0.
            assert type(record.k0) is float
            assert type(record.uabs0) is float
            assert record.k0 == float(k_expected_t[0])
            # (ii) uabs0 is the ABSOLUTE VALUE of the softened potential.
            assert float(v_expected_t[0]) < 0.0
            assert record.uabs0 == float(abs(v_expected_t[0]))
            assert record.uabs0 == float(-v_expected_t[0])
            # Never the signed Hamiltonian H_0 = K0 + V_eps, and never its
            # magnitude: |K + V| = |V| - K here (bound system, K > 0), which
            # differs from |V| by the strictly positive kinetic term.
            h0_signed = float(k_expected_t[0] + v_expected_t[0])
            assert record.uabs0 != h0_signed
            assert record.uabs0 != abs(h0_signed)
            # Never a mis-softened recomputation: the invariants-side epsilon
            # is five orders of magnitude away and yields a measurably
            # different potential on these separations.
            _, v_mis_t = _matched_plummer_components(
                pre.r_gauge[0],
                pre.v_gauge[0],
                pre.masses_ordered,
                eps_soft=EPS_INV,
                **_CPU_F64,
            )
            assert record.uabs0 != float(abs(v_mis_t[0]))


def test_seam_preserves_hamiltonian_signature():
    """D-11: the extraction is invisible to existing callers."""
    signature = inspect.signature(_matched_plummer_hamiltonian)
    assert list(signature.parameters) == [
        "positions",
        "velocities",
        "masses",
        "dtype",
        "device",
        "eps_soft",
    ]
    assert signature.parameters["dtype"].kind is inspect.Parameter.KEYWORD_ONLY
    assert signature.parameters["device"].kind is inspect.Parameter.KEYWORD_ONLY
    assert signature.parameters["eps_soft"].kind is inspect.Parameter.KEYWORD_ONLY
    assert signature.parameters["eps_soft"].default == EPS_SOFT
    components_signature = inspect.signature(_matched_plummer_components)
    assert list(components_signature.parameters) == list(signature.parameters)
    assert components_signature.parameters["eps_soft"].default == EPS_SOFT


def test_stageindex_k0_uabs0_delegate():
    """D-12: the new accessors follow the ``_source_value`` delegation pattern.

    Source-backed path: a ``StageIndex.from_split`` over a TinyCorpus adapter
    returns the same floats stored on the underlying ``AdmittedRecord``.
    Direct-records path (``source=None``): the values are read off the record
    itself.
    """
    with TinyCorpus() as corpus:
        adapter = _adapter(corpus)
        manifest = write_split_manifest(adapter, corpus.run_dir, seed=20260731)
        train = StageIndex.from_split(adapter, manifest, "train")
        assert train.record_keys(), "train split must be non-empty"
        for key in train.record_keys():
            record = adapter.get(key)
            assert train.k0(key) == record.k0
            assert train.uabs0(key) == record.uabs0
            assert type(train.k0(key)) is float
            assert type(train.uabs0(key)) is float

    record = SimpleNamespace(
        record_key=RecordKey("hierarchical", "base", 0),
        physical_key=RecordKey("hierarchical", "base", 0).physical_key,
        stage_label=StageLabel.STAGE_0,
        k0=0.75,
        uabs0=1.25,
    )
    index = StageIndex([record])
    assert index.k0(record.record_key) == 0.75
    assert index.uabs0(record.record_key) == 1.25
