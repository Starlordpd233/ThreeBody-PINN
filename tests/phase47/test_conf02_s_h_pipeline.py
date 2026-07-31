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
import json
from types import SimpleNamespace

import numpy as np
import pytest
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
from pinn.train import _assert_s_h_matches_artifact
from pinn.training.run_metadata import (
    TRAINING_METADATA_FILENAME,
    TRAINING_METADATA_SCHEMA_VERSION,
    compute_s_h,
    load_training_metadata,
    validate_s_h,
    write_training_metadata,
)
from pinn.training.validation_gate import RATIFIED_VALIDATION_FRAME
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


# ---------------------------------------------------------------------------
# D-13..D-18 — split-scoped median, fail-closed validation, metadata artifact
# ---------------------------------------------------------------------------

_DELETE = object()


class _PoolSource:
    """Duck-typed train-split StageIndex: ``k0``/``uabs0`` accessors + pools.

    ``stage0`` maps key -> (k0, uabs0) admitted at Stage 0; ``later`` maps
    key -> (k0, uabs0) admitted at Stage 1, which ``records_at_or_below(0)``
    must never surface. Insertion order is the caller's, so the median's
    order-invariance is exercised by permuting the constructor mapping.
    """

    def __init__(self, stage0, *, later=None):
        self._s0 = dict(stage0)
        self._later = dict(later or {})

    def records_at(self, stage):
        numeric = int(getattr(stage, "value", stage))
        if numeric == 0:
            return tuple(self._s0)
        if numeric == 1:
            return tuple(self._later)
        return ()

    def records_at_or_below(self, stage):
        numeric = int(getattr(stage, "value", stage))
        keys = list(self._s0)
        if numeric >= 1:
            keys += list(self._later)
        return tuple(keys)

    def _pair(self, key):
        if key in self._s0:
            return self._s0[key]
        return self._later[key]

    def k0(self, key):
        return self._pair(key)[0]

    def uabs0(self, key):
        return self._pair(key)[1]


def test_median_train_split_only():
    """D-12/D-13/D-14 + Q3: the median reduces over the Stage-0 train pool."""
    # Distinct per-record sums; the Stage-1 ("validation-side") records carry
    # sums that would dominate any median they leaked into — their exclusion
    # is proven by the returned value, not by construction prose.
    train_keys = [RecordKey("hierarchical", "base", i) for i in (3, 0, 4, 1, 2)]
    train_sums = [4.0, 1.0, 5.0, 2.0, 3.0]  # aligned with train_keys; median 3.0
    stage0 = {key: (total - 0.5, 0.5) for key, total in zip(train_keys, train_sums)}
    later = {
        RecordKey("hierarchical", "base", 100 + i): (5e8, 5e8) for i in range(3)
    }
    source = _PoolSource(stage0, later=later)

    s_h, n_train = compute_s_h(source)
    assert type(s_h) is float
    assert type(n_train) is int
    assert n_train == 5
    assert s_h == 3.0

    # Even population: numpy.median averages the two central values (D-14),
    # in float64 (the .2/.4 pair does not terminate in binary).
    even = _PoolSource(
        {key: (total, 0.0) for key, total in zip(
            [RecordKey("hierarchical", "base", i) for i in range(4)],
            [0.1, 0.2, 0.4, 0.8],
        )}
    )
    s_h_even, n_even = compute_s_h(even)
    assert n_even == 4
    assert s_h_even == (0.2 + 0.4) / 2  # 0.30000000000000004, bit-exact

    # Order invariance: permuting the record iteration order yields a
    # bit-identical float64 S_H (D-14).
    permuted = _PoolSource(dict(reversed(list(stage0.items()))), later=later)
    s_h_perm, n_perm = compute_s_h(permuted)
    assert (s_h_perm, n_perm) == (s_h, n_train)

    # Single-element population yields that element.
    single = _PoolSource({RecordKey("hierarchical", "base", 7): (2.5, 5.0)})
    s_h_single, n_single = compute_s_h(single)
    assert (s_h_single, n_single) == (7.5, 1)

    # Q3: records_at(0) and records_at_or_below(0) coincide at Stage 0 —
    # asserted on the stub (exact) and on a real StageIndex (sorted), so a
    # later stage extension goes red here instead of silently changing S_H.
    all_stage0 = _PoolSource(stage0)
    assert all_stage0.records_at(0) == all_stage0.records_at_or_below(0)
    with TinyCorpus() as corpus:
        adapter = _adapter(corpus)
        manifest = write_split_manifest(adapter, corpus.run_dir, seed=20260731)
        train = StageIndex.from_split(adapter, manifest, "train")
        assert sorted(train.records_at(0)) == sorted(train.records_at_or_below(0))


def test_s_h_fails_closed(tmp_path):
    """D-17: invalid S_H is a refusal BEFORE any artifact exists."""
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    metadata_path = run_dir / TRAINING_METADATA_FILENAME

    # NaN, +inf, -inf, negative, and the exact-zero boundary all refuse, and
    # the refusal names the predicate.
    for bad in (float("nan"), float("inf"), float("-inf"), -1.0, 0.0):
        with pytest.raises(ValueError, match="finite and strictly positive"):
            validate_s_h(bad)
        with pytest.raises(ValueError, match="finite and strictly positive"):
            write_training_metadata(
                run_dir, s_h=bad, n_train=240, energy_floor_factor=1e-4
            )
        # Refusal precedes artifact: a partially-completed run must not leave
        # records that read like evidence.
        assert not metadata_path.exists()

    # An empty train-split population refuses before any median is taken.
    with pytest.raises(ValueError, match="empty"):
        compute_s_h(_PoolSource({}))
    assert not metadata_path.exists()


def test_metadata_roundtrip_revalidates(tmp_path):
    """D-15/D-16/D-18: write -> load is bit-identical; every tamper raises."""
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    metadata_path = run_dir / TRAINING_METADATA_FILENAME
    s_h = (0.2 + 0.4) / 2  # 0.30000000000000004 — float64 fidelity probe
    factor = 1e-4
    write_training_metadata(
        run_dir, s_h=s_h, n_train=240, energy_floor_factor=factor
    )

    payload = load_training_metadata(run_dir, expected_energy_floor_factor=factor)
    assert set(payload) == {
        "schema_version",
        "s_h",
        "eps_h",
        "n_train",
        "eps_train",
        "energy_floor_factor",
        "frame",
    }
    assert payload["schema_version"] == TRAINING_METADATA_SCHEMA_VERSION
    assert payload["s_h"] == s_h  # bit-identical float64 round-trip
    assert payload["eps_h"] == factor * s_h  # exact float64 product (D-15)
    assert payload["n_train"] == 240
    assert payload["eps_train"] == EPS_SOFT
    assert payload["energy_floor_factor"] == factor
    assert payload["frame"] == {
        "position_frame": RATIFIED_VALIDATION_FRAME.position_frame,
        "time_coord": RATIFIED_VALIDATION_FRAME.time_coord,
        "mass_convention": RATIFIED_VALIDATION_FRAME.mass_convention,
    }

    pristine_text = metadata_path.read_text(encoding="utf-8")
    pristine = json.loads(pristine_text)

    def write_payload(data):
        metadata_path.write_text(
            json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )

    def mutated(**changes):
        data = dict(pristine)
        for name, value in changes.items():
            if value is _DELETE:
                data.pop(name)
            else:
                data[name] = value
        return data

    # A persisted number is trusted only after re-checking (D-18).
    write_payload(mutated(s_h=-1.0))
    with pytest.raises(ValueError, match="strictly positive"):
        load_training_metadata(run_dir, expected_energy_floor_factor=factor)

    write_payload(mutated(s_h=float("inf")))
    with pytest.raises(ValueError, match="strictly positive"):
        load_training_metadata(run_dir, expected_energy_floor_factor=factor)

    write_payload(mutated(eps_h=1.0))
    with pytest.raises(ValueError, match="eps_h"):
        load_training_metadata(run_dir, expected_energy_floor_factor=factor)

    write_payload(mutated(n_train=_DELETE))
    with pytest.raises(ValueError, match="keys must be exactly"):
        load_training_metadata(run_dir, expected_energy_floor_factor=factor)

    unknown = mutated()
    unknown["surprise"] = 1
    write_payload(unknown)
    with pytest.raises(ValueError, match="keys must be exactly"):
        load_training_metadata(run_dir, expected_energy_floor_factor=factor)

    write_payload(mutated(n_train=True))
    with pytest.raises(ValueError, match="n_train"):
        load_training_metadata(run_dir, expected_energy_floor_factor=factor)

    metadata_path.write_text(pristine_text[: len(pristine_text) // 2], encoding="utf-8")
    with pytest.raises(ValueError, match="not valid JSON"):
        load_training_metadata(run_dir, expected_energy_floor_factor=factor)

    # Cycle-2 review MEDIUM: a persisted artifact produced under different
    # softening/factor settings than the live run refuses at the boundary.
    write_payload(mutated(eps_train=1e-10))
    with pytest.raises(ValueError, match="eps_train"):
        load_training_metadata(run_dir, expected_energy_floor_factor=factor)

    # Factor tampered WITH the product kept consistent: the eps_h product
    # check passes, so only the live-factor cross-check can catch this.
    write_payload(mutated(energy_floor_factor=2e-4, eps_h=2e-4 * s_h))
    with pytest.raises(ValueError, match="energy_floor_factor"):
        load_training_metadata(run_dir, expected_energy_floor_factor=factor)

    # Cycle-3 review MEDIUM (codex): the expected bindings arrive as EXPLICIT
    # keyword arguments — a well-formed payload loaded against a DIFFERENT
    # live expectation also raises (the only implementable form of the check,
    # since energy_floor_factor is configurable).
    write_payload(pristine)
    with pytest.raises(ValueError, match="energy_floor_factor"):
        load_training_metadata(run_dir, expected_energy_floor_factor=3e-4)
    with pytest.raises(ValueError, match="eps_train"):
        load_training_metadata(
            run_dir,
            expected_energy_floor_factor=factor,
            expected_eps_train=2e-5,
        )
    # The matched call still succeeds after the tamper sequence.
    assert (
        load_training_metadata(run_dir, expected_energy_floor_factor=factor)["s_h"]
        == s_h
    )


def test_resume_recompute_refuses_mismatch(tmp_path):
    """D-18 resume path: recompute from the live source; never overwrite."""
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    metadata_path = run_dir / TRAINING_METADATA_FILENAME
    keys = [RecordKey("hierarchical", "base", i) for i in range(4)]
    source = _PoolSource({key: (1.0 + i, 2.0) for i, key in enumerate(keys)})
    s_h, n_train = compute_s_h(source)
    write_training_metadata(
        run_dir, s_h=s_h, n_train=n_train, energy_floor_factor=1e-4
    )
    original_bytes = metadata_path.read_bytes()

    # A matched live source does not raise and RETURNS the validated s_h
    # (the resume branch binds the same local the fresh branch binds).
    assert (
        _assert_s_h_matches_artifact(run_dir, source, energy_floor_factor=1e-4)
        == s_h
    )
    assert metadata_path.read_bytes() == original_bytes

    # Mutated live source (different median): fail-closed refusal naming the
    # mismatch, and the artifact stays byte-identical — never an overwrite.
    mutated_source = _PoolSource(
        {key: (10.0 + i, 2.0) for i, key in enumerate(keys)}
    )
    with pytest.raises(ValueError, match="recompute"):
        _assert_s_h_matches_artifact(
            run_dir, mutated_source, energy_floor_factor=1e-4
        )
    assert metadata_path.read_bytes() == original_bytes

    # Population drift with an unchanged median: the n_train cross-check
    # fires even when s_h alone would pass.
    five_keys = [RecordKey("hierarchical", "base", 10 + i) for i in range(5)]
    drifted = _PoolSource(
        {key: (total, 0.0) for key, total in zip(
            five_keys, [3.0, 4.0, 4.5, 5.0, 6.0]
        )}
    )
    with pytest.raises(ValueError, match="n_train"):
        _assert_s_h_matches_artifact(run_dir, drifted, energy_floor_factor=1e-4)
    assert metadata_path.read_bytes() == original_bytes
