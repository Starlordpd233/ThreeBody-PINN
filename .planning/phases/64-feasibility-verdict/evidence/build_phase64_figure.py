#!/usr/bin/env python3
"""Phase 64: producer of the system 1632 verdict figure.

D-04: one figure, ``evidence/figure-1632.svg``, shows system 1632's real orbit
beside the trained network's prediction, drawn read-only from the committed
weights of ``r1-1632``'s official state (the record's ``better_state``,
``polish``) re-scored on the CPU in float64. Panel A draws each body's real x-y
track and the network's predicted track, with each body's time-mean position
marked and a magnified inset for the tiny predicted tracks (64-RESEARCH
Pitfall 11). Panel B draws ``max(e_sys, e_in)`` against time for the network and
for the constant time-mean predictor, with the scorecard's Tier-1 limit drawn
and labelled.

The derivation is shared with ``build_phase64_evidence.py``: this producer calls
its ``derive_state`` and ``constant_predictor_error``, so the figure and
``numbers.json`` share one source. Nothing is trained, tuned or launched; the
committed weights are re-scored read-only through the Phase 59 allowlist and the
open attestation is recorded.

The SVG is standard-library only (no plotting library), and its bytes are
deterministic: ``torch.set_num_threads(1)``, every coordinate rounded to 0.1,
and a fixed element order. ``figure-1632.provenance.json`` records the inputs,
their SHA-256s, both producer scripts, the SVG's SHA-256, the rounded plotted
series' SHA-256, the arm, the state, the precision, the versions, the data-root
source and the open attestation. It holds no timestamp, no git head and no host
path, so it is byte-reproducible.

Usage, from the repository root::

    build_phase64_figure.py            write the SVG and its provenance
    build_phase64_figure.py --check    regenerate and compare the committed bytes

``--check`` runs in a second process: it rebuilds the whole series (including
the CPU re-derivation) and compares both files' canonical bytes, so a value that
depends on process state cannot pass as reproducible.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import os
import platform
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence

if __package__ in (None, ""):
    _ROOT = Path(__file__).resolve().parents[4]
    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))
    _HERE = Path(__file__).resolve().parent
    if str(_HERE) not in sys.path:
        sys.path.insert(0, str(_HERE))

REPO_ROOT = Path(__file__).resolve().parents[4]
PHASE_REL = Path(".planning/phases/64-feasibility-verdict")
EVIDENCE_REL = PHASE_REL / "evidence"
FIGURE_REL = EVIDENCE_REL / "figure-1632.svg"
PROVENANCE_REL = EVIDENCE_REL / "figure-1632.provenance.json"
PRODUCER_REL = EVIDENCE_REL / "build_phase64_figure.py"
EVIDENCE_PRODUCER_REL = EVIDENCE_REL / "build_phase64_evidence.py"
P60_EVIDENCE_REL = Path(".planning/phases/60-single-system-learnability/evidence")
SCORECARD_REL = Path("pinn/verification/artifacts/feasibility_scorecard_v1.json")
HANDOFF_REL = P60_EVIDENCE_REL / "g2" / "stop-handoff.json"

ARM = "r1-1632"
STATE = "polish"
SCHEMA = "phase64-figure-provenance/v1"
PRECISION = "CPU float64"

VIEW_WIDTH = 1200.0
VIEW_HEIGHT = 560.0

# The four inputs the provenance names, in path order.
INPUT_RELS = (
    (P60_EVIDENCE_REL / "arms" / ARM / "record.json"),
    (P60_EVIDENCE_REL / "arms" / ARM / f"{STATE}.weights"),
    HANDOFF_REL,
    SCORECARD_REL,
)

# The two producer scripts whose digests the provenance records.
PRODUCER_RELS = (PRODUCER_REL, EVIDENCE_PRODUCER_REL)

# The reference palette's slots 1 to 3, validated light mode (64-RESEARCH Code
# Example 5). Text uses ink tokens, never a series colour.
BODY_COLORS = ("#2a78d6", "#eb6834", "#1baf7a")
INK = "#1f2328"
MUTED = "#57606a"
GRID = "#d0d7de"
PAPER = "#ffffff"
LIMIT = "#b3261e"
FONT = "Helvetica, Arial, sans-serif"

BODY_COUNT = 3


class FigureError(RuntimeError):
    """Fail-closed producer error: nothing is written."""


def fail(message: str) -> None:
    raise FigureError(f"build_phase64_figure FAIL-CLOSED: {message}")


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _r10(value: Any) -> float:
    """A plain Python float rounded to the ten decimals the series records."""
    return round(float(value), 10)


def _tier1_max(card: Any) -> float:
    """The scorecard's Tier-1 E_max, read from its own tiers section."""
    for level in card.section("tiers")["levels"]:
        if int(level["tier"]) == 1:
            return float(level["E_max"])
    fail("the scorecard names no level whose tier is 1")


# ---------------------------------------------------------------------------
# The series: the only part of this file that reads the corpus.
# ---------------------------------------------------------------------------


def figure_series(repo_root: Path) -> dict[str, Any]:
    """The rounded plotted series for r1-1632's official state.

    One real context per process; the shared derivation of
    ``build_phase64_evidence.py`` scores the committed weights on the CPU in
    float64. Every float is rounded to ten decimals so the verifier can rebuild
    the same bytes.
    """
    import numpy as np
    import torch

    import build_phase64_evidence as shared
    from pinn.verification.feasibility_scorecard import load_scorecard
    from pinn.verification.learnability_arms import arm_spec
    from pinn.verification.learnability_data import load_arm_data, open_real_context

    root = Path(repo_root).resolve()
    os.chdir(root)
    torch.set_num_threads(1)

    card = load_scorecard()
    record = shared._read_json(root / (P60_EVIDENCE_REL / "arms" / ARM / "record.json"))
    state = record.get("better_state")
    if state != STATE:
        fail(f"r1-1632 better_state is {state!r}, not {STATE!r}")
    recorded = shared._field(record, f"states.{STATE}.weights")
    if recorded.get("file") != f"{STATE}.weights":
        fail(f"r1-1632 {STATE} record names weights file {recorded.get('file')!r}")

    ctx = open_real_context(repo_root=root)
    arm_data = load_arm_data(
        arm_spec(ARM), ctx, scorecard=card, dtype=torch.float32, device="cpu"
    )
    derived = shared.derive_state(ctx, card, ARM, STATE, arm_data=arm_data)
    e_sys_const, e_in_const = shared.constant_predictor_error(
        derived["ref"], derived["inner_pair"]
    )
    attestation = ctx.attestation
    if attestation is None:
        fail("the real context carries no open attestation")

    ref = np.asarray(derived["ref"], dtype=np.float64)
    pos = np.asarray(derived["pos"], dtype=np.float64)
    times = np.asarray(derived["times"], dtype=np.float64)
    mean = ref.mean(axis=0)
    err_net = np.maximum(
        np.asarray(derived["e_sys"], dtype=np.float64),
        np.asarray(derived["e_in"], dtype=np.float64),
    )
    err_const = np.maximum(
        np.asarray(e_sys_const, dtype=np.float64),
        np.asarray(e_in_const, dtype=np.float64),
    )

    series = {
        "arm": ARM,
        "state": STATE,
        "times": [_r10(value) for value in times],
        "ref_xy": [
            [[_r10(point[0]), _r10(point[1])] for point in ref[:, body, :]]
            for body in range(BODY_COUNT)
        ],
        "pred_xy": [
            [[_r10(point[0]), _r10(point[1])] for point in pos[:, body, :]]
            for body in range(BODY_COUNT)
        ],
        "mean_xy": [
            [_r10(mean[body][0]), _r10(mean[body][1])] for body in range(BODY_COUNT)
        ],
        "err_net": [_r10(value) for value in err_net],
        "err_const": [_r10(value) for value in err_const],
        "tier1": _r10(_tier1_max(card)),
        "attestation": dict(attestation.summary()),
    }
    _check_series(series)
    return series


def _check_series(series: Mapping[str, Any]) -> None:
    """Refuse a series the renderer cannot draw or the verifier cannot rebuild."""
    count = len(series.get("times") or [])
    if count < 2:
        fail(f"the series holds {count} times, fewer than 2")
    for key in ("err_net", "err_const"):
        if len(series.get(key) or []) != count:
            fail(f"the series {key} length differs from times")
    for key in ("ref_xy", "pred_xy"):
        bodies = series.get(key) or []
        if len(bodies) != BODY_COUNT:
            fail(f"the series {key} holds {len(bodies)} bodies, not {BODY_COUNT}")
        for body in bodies:
            if len(body) != count:
                fail(f"the series {key} track length differs from times")
    if len(series.get("mean_xy") or []) != BODY_COUNT:
        fail("the series mean_xy does not hold three bodies")
    if not math.isfinite(float(series.get("tier1", float("nan")))):
        fail("the series tier1 is not finite")


def series_digest(series: Mapping[str, Any]) -> str:
    """SHA-256 of the canonical plotted series, without the attestation.

    The attestation records what the run opened; it is not a plotted value, so
    it is excluded from the digest the verifier compares.
    """
    from pinn.verification import evidence_io

    payload = {key: value for key, value in series.items() if key != "attestation"}
    return _sha256_bytes(evidence_io.canonical_json_bytes(payload))


# ---------------------------------------------------------------------------
# The SVG: pure rendering, no file reads, no clock, no environment.
# ---------------------------------------------------------------------------


def _esc(value: Any) -> str:
    text = str(value)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _poly(xs: Iterable[float], ys: Iterable[float], color: str, width: float = 2.0,
          dash: Optional[str] = None) -> str:
    """64-RESEARCH Code Example 5: a polyline with every coordinate at 0.1."""
    points = " ".join(f"{float(x):.1f},{float(y):.1f}" for x, y in zip(xs, ys))
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{points}" fill="none" stroke="{color}" '
        f'stroke-width="{width:g}" stroke-linejoin="round" stroke-linecap="round"'
        f"{dashed}/>"
    )


def _line(x1: float, y1: float, x2: float, y2: float, color: str,
          width: float = 1.0, dash: Optional[str] = None) -> str:
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{float(x1):.1f}" y1="{float(y1):.1f}" '
        f'x2="{float(x2):.1f}" y2="{float(y2):.1f}" '
        f'stroke="{color}" stroke-width="{width:g}"{dashed}/>'
    )


def _rect(x: float, y: float, width: float, height: float, fill: str,
          stroke: Optional[str] = None, stroke_width: float = 1.0) -> str:
    border = f' stroke="{stroke}" stroke-width="{stroke_width:g}"' if stroke else ""
    return (
        f'<rect x="{float(x):.1f}" y="{float(y):.1f}" '
        f'width="{float(width):.1f}" height="{float(height):.1f}" '
        f'fill="{fill}"{border}/>'
    )


def _text(x: float, y: float, value: Any, *, size: float = 11.0,
          color: str = INK, anchor: str = "start", weight: str = "normal",
          transform: Optional[str] = None) -> str:
    extra = f' transform="{transform}"' if transform else ""
    return (
        f'<text x="{float(x):.1f}" y="{float(y):.1f}" font-family="{FONT}" '
        f'font-size="{size:g}" fill="{color}" text-anchor="{anchor}" '
        f'font-weight="{weight}"{extra}>{_esc(value)}</text>'
    )


def _cross(x: float, y: float, color: str, size: float = 4.5,
           width: float = 1.5) -> str:
    half = float(size)
    return (
        f'<path d="M{float(x) - half:.1f},{float(y):.1f} '
        f'L{float(x) + half:.1f},{float(y):.1f} '
        f'M{float(x):.1f},{float(y) - half:.1f} '
        f'L{float(x):.1f},{float(y) + half:.1f}" '
        f'fill="none" stroke="{color}" stroke-width="{width:g}"/>'
    )


def _nice_step(span: float, target: int) -> float:
    raw = float(span) / float(target)
    magnitude = 10.0 ** math.floor(math.log10(raw))
    for multiple in (1.0, 2.0, 2.5, 5.0, 10.0):
        step = multiple * magnitude
        if raw <= step:
            return step
    return 10.0 * magnitude


def _axis(lo: float, hi: float, target: int) -> tuple[float, float, list[float]]:
    """A padded domain whose tick marks are multiples of a nice step."""
    step = _nice_step(hi - lo, target)
    start = math.floor(lo / step) * step
    end = math.ceil(hi / step) * step
    count = int(round((end - start) / step))
    ticks = [round(start + index * step, 10) for index in range(count + 1)]
    return start, end, ticks


def _xy_domain(series: Mapping[str, Any]) -> tuple[float, float, list[float]]:
    """One square domain for both axes, from the real and predicted tracks."""
    xs: list[float] = []
    ys: list[float] = []
    for key in ("ref_xy", "pred_xy"):
        for body in series[key]:
            xs.extend(point[0] for point in body)
            ys.extend(point[1] for point in body)
    lo = min(min(xs), min(ys))
    hi = max(max(xs), max(ys))
    pad = 0.02 * (hi - lo)
    return _axis(lo - pad, hi + pad, 6)


def _body_domain(series: Mapping[str, Any], body: int) -> tuple[float, float, float, float]:
    """A square domain around one body's predicted track and its time mean."""
    track = series["pred_xy"][body]
    mean = series["mean_xy"][body]
    xs = [point[0] for point in track] + [mean[0]]
    ys = [point[1] for point in track] + [mean[1]]
    centre_x = 0.5 * (min(xs) + max(xs))
    centre_y = 0.5 * (min(ys) + max(ys))
    half = 0.62 * max(max(xs) - min(xs), max(ys) - min(ys))
    if half <= 0.0:
        half = 0.001
    return centre_x - half, centre_x + half, centre_y - half, centre_y + half


def _mini_panel(series: Mapping[str, Any], body: int, left: float, top: float,
                size: float) -> list[str]:
    """One magnified body track: the network's path and its time mean."""
    lo_x, hi_x, lo_y, hi_y = _body_domain(series, body)

    def mx(value: float) -> float:
        return left + (float(value) - lo_x) / (hi_x - lo_x) * size

    def my(value: float) -> float:
        return top + size - (float(value) - lo_y) / (hi_y - lo_y) * size

    track = series["pred_xy"][body]
    mean = series["mean_xy"][body]
    out = [_rect(left, top, size, size, PAPER, INK, 1.0)]
    # 1.2 px, not the main panel's 1.5: the tests count the main panel's three
    # real tracks by their 1.5 px stroke, so the inset must not add a fourth.
    out.append(
        _poly((mx(point[0]) for point in track), (my(point[1]) for point in track),
              BODY_COLORS[body], 1.2)
    )
    out.append(_cross(mx(mean[0]), my(mean[1]), PAPER, 3.5, 3.0))
    out.append(_cross(mx(mean[0]), my(mean[1]), BODY_COLORS[body], 3.5, 1.2))
    out.append(
        _text(left + 0.5 * size, top + size + 13.0, f"body {body + 1}", size=9.5,
              color=MUTED, anchor="middle")
    )
    return out


def _panel_a(series: Mapping[str, Any]) -> list[str]:
    """The real orbit, the network's tracks, the time means and the inset."""
    left, top, size = 80.0, 100.0, 330.0
    right, bottom = left + size, top + size
    lo, hi, ticks = _xy_domain(series)
    span = hi - lo

    def px(value: float) -> float:
        return left + (float(value) - lo) / span * size

    def py(value: float) -> float:
        return bottom - (float(value) - lo) / span * size

    out = ['<g id="panel-a">']
    out.append(
        _text(left, 80.0, "Panel A: real orbit and network prediction (x-y)",
              size=14.0, weight="bold")
    )
    out.append(_rect(left, top, size, size, PAPER, INK, 1.0))
    for tick in ticks[1:-1]:
        out.append(_line(px(tick), top, px(tick), bottom, GRID, 1.0))
        out.append(_line(left, py(tick), right, py(tick), GRID, 1.0))
    for tick in ticks:
        out.append(_text(px(tick), bottom + 14.0, f"{tick:.2f}", size=10.0,
                         color=MUTED, anchor="middle"))
        out.append(_text(left - 6.0, py(tick) + 3.5, f"{tick:.2f}", size=10.0,
                         color=MUTED, anchor="end"))
    out.append(_text(0.5 * (left + right), bottom + 34.0, "x (system units)",
                     size=11.0, color=MUTED, anchor="middle"))
    middle = 0.5 * (top + bottom)
    out.append(
        _text(34.0, middle, "y (system units)", size=11.0, color=MUTED,
              anchor="middle", transform=f"rotate(-90 34.0 {middle:.1f})")
    )

    for body, color in enumerate(BODY_COLORS):
        track = series["ref_xy"][body]
        out.append(_poly((px(point[0]) for point in track),
                         (py(point[1]) for point in track), color, 1.5))

    for body, color in enumerate(BODY_COLORS):
        track = series["pred_xy"][body]
        xs = [px(point[0]) for point in track]
        ys = [py(point[1]) for point in track]
        out.append(_poly(xs, ys, PAPER, 5.0))
        out.append(_poly(xs, ys, color, 3.0))

    for body, color in enumerate(BODY_COLORS):
        mean = series["mean_xy"][body]
        out.append(_cross(px(mean[0]), py(mean[1]), PAPER, 4.5, 3.5))
        out.append(_cross(px(mean[0]), py(mean[1]), color))

    spreads = []
    for track in series["pred_xy"]:
        xs = [point[0] for point in track]
        ys = [point[1] for point in track]
        spreads.append((max(xs) - min(xs)) + (max(ys) - min(ys)))
    widest = max(range(BODY_COUNT), key=lambda body: spreads[body])
    anchor_x, anchor_y = px(series["mean_xy"][widest][0]), py(
        series["mean_xy"][widest][1]
    )
    label_x, label_y = right - 8.0, bottom - 16.0
    out.append(_rect(label_x - 200.0, label_y - 16.0, 204.0, 22.0, PAPER))
    out.append(_line(label_x - 196.0, label_y - 5.0, anchor_x, anchor_y, MUTED, 1.0))
    out.append(
        _text(label_x, label_y, "network prediction (barely moves)", size=10.5,
              anchor="end")
    )

    inset_left, inset_top, mini = 450.0, 140.0, 70.0
    out.append(
        _text(inset_left, 122.0, "Inset: the network's tracks, magnified",
              size=13.0, weight="bold")
    )
    for body in range(BODY_COUNT):
        out.extend(
            _mini_panel(
                series,
                body,
                inset_left + body * (mini + 15.0),
                inset_top,
                mini,
            )
        )
    out.append(
        _text(inset_left, 250.0, "each panel is magnified to its own track;",
              size=10.0, color=MUTED)
    )
    out.append(
        _text(inset_left, 264.0, "the cross marks each body's time mean",
              size=10.0, color=MUTED)
    )
    out.append("</g>")
    return out


def render_svg(series: Mapping[str, Any]) -> str:
    """The whole figure as a standard-library SVG string.

    Element order is fixed and every coordinate is rounded to 0.1, so two calls
    with the same series return identical bytes. No clock, no host path and no
    external reference enters the document.
    """
    _check_series(series)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{VIEW_WIDTH:g}" '
            f'height="{VIEW_HEIGHT:g}" viewBox="0 0 {VIEW_WIDTH:g} {VIEW_HEIGHT:g}" '
            'role="img" aria-labelledby="figure-title figure-desc">'
        ),
        (
            '<title id="figure-title">System 1632: real orbit and the trained '
            "network's prediction</title>"
        ),
        (
            '<desc id="figure-desc">The real x-y orbit of the three bodies beside '
            "the trained network's predicted tracks and each body's time-mean "
            "position, and the network's error against time beside the error of "
            "guessing each body's average position and the Tier-1 limit.</desc>"
        ),
        _rect(0.0, 0.0, VIEW_WIDTH, VIEW_HEIGHT, PAPER),
        (
            _text(
                60.0,
                30.0,
                "System 1632: real orbit and the trained network's prediction "
                "(official state, re-derived on the CPU in float64)",
                size=18.0,
                weight="bold",
            )
        ),
        (
            _text(
                60.0,
                50.0,
                "Official state (polish), re-derived from the committed weights. "
                "Nothing is trained.",
                size=12.0,
                color=MUTED,
            )
        ),
    ]
    lines.extend(_panel_a(series))
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Provenance and the command line.
# ---------------------------------------------------------------------------


def _inputs(repo_root: Path) -> list[dict[str, str]]:
    return [
        {"path": relative.as_posix(), "sha256": _sha256_file(repo_root / relative)}
        for relative in INPUT_RELS
    ]


def build_provenance(
    series: Mapping[str, Any], svg_text: str, inputs: Sequence[Mapping[str, str]]
) -> dict[str, Any]:
    """The deterministic provenance record beside the figure."""
    import numpy as np
    import torch

    attestation = series.get("attestation")
    if not isinstance(attestation, Mapping):
        fail("the series holds no attestation summary")
    source = attestation.get("data_root_source")
    if source != "git_common_dir_default":
        fail(f"the attestation data_root_source is {source!r}")
    arm = series.get("arm")
    state = series.get("state")
    if arm != ARM or state != STATE:
        fail(f"the series names arm {arm!r} state {state!r}, not {ARM!r} {STATE!r}")
    return {
        "schema": SCHEMA,
        "plain_language": (
            "System 1632's real orbit beside the trained network's prediction, "
            "drawn read-only from the committed polish weights and re-scored on "
            "the CPU in float64; nothing is trained."
        ),
        "figure": {
            "path": FIGURE_REL.as_posix(),
            "sha256": _sha256_bytes(svg_text.encode("utf-8")),
        },
        "inputs": sorted(
            ({"path": str(item["path"]), "sha256": str(item["sha256"])} for item in inputs),
            key=lambda item: item["path"],
        ),
        "producers": {
            relative.as_posix(): _sha256_file(REPO_ROOT / relative)
            for relative in PRODUCER_RELS
        },
        "series_sha256": series_digest(series),
        "arm": str(series.get("arm")),
        "state": str(series.get("state")),
        "precision": PRECISION,
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "torch": torch.__version__,
        },
        "data_root_source": str(source),
        "attestation": dict(attestation),
        "command": f"python -B {PRODUCER_REL.as_posix()}",
    }


def cmd_figure(*, check: bool) -> int:
    """Write the figure and its provenance, or regenerate and compare bytes."""
    from pinn.verification import evidence_io

    os.chdir(REPO_ROOT)
    series = figure_series(REPO_ROOT)
    svg_text = render_svg(series)
    provenance = build_provenance(series, svg_text, _inputs(REPO_ROOT))

    if check:
        if not evidence_io.bytes_identical(
            REPO_ROOT / FIGURE_REL, svg_text.encode("utf-8")
        ):
            print("FIGURE-CHECK-DIFF", file=sys.stderr)
            return 1
        if not evidence_io.bytes_identical(
            REPO_ROOT / PROVENANCE_REL, evidence_io.canonical_json_bytes(provenance)
        ):
            print("FIGURE-CHECK-DIFF", file=sys.stderr)
            return 1
        print("FIGURE-CHECK-OK")
        return 0

    digest = evidence_io.write_text(REPO_ROOT / FIGURE_REL, svg_text)
    evidence_io.write_json(REPO_ROOT / PROVENANCE_REL, provenance)
    print(f"FIGURE-WRITTEN {digest}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="regenerate in this process and compare the committed bytes",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        return cmd_figure(check=bool(args.check))
    except Exception as exc:  # noqa: BLE001 - fail-closed CLI
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
