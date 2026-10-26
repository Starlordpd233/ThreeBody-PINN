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
import xml.etree.ElementTree as ElementTree
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

# The layout, in viewBox units. The inset sits between panel A and panel B, and
# the legend sits below both panels, so the legibility check can measure that
# nothing overlaps and nothing leaves the canvas.
PANEL_A = (80.0, 100.0, 330.0, 330.0)
INSET_LEFT = 450.0
INSET_TOP = 140.0
INSET_MINI = 70.0
INSET_GAP = 15.0
INSET_RIGHT = INSET_LEFT + 3.0 * INSET_MINI + 2.0 * INSET_GAP
PANEL_B = (760.0, 100.0, 380.0, 330.0)
LEGEND = (80.0, 476.0, 1040.0, 68.0)

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
    left, top, size, _height = PANEL_A
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

    inset_left, inset_top, mini = INSET_LEFT, INSET_TOP, INSET_MINI
    out.append(
        _text(inset_left, 122.0, "Inset: the network's tracks, magnified",
              size=13.0, weight="bold")
    )
    for body in range(BODY_COUNT):
        out.extend(
            _mini_panel(
                series,
                body,
                inset_left + body * (mini + INSET_GAP),
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


def _panel_b(series: Mapping[str, Any]) -> list[str]:
    """The network's error against time, the constant predictor's, the limit."""
    left, top, width, height = PANEL_B
    right, bottom = left + width, top + height
    times = series["times"]
    t_lo, t_hi = min(times), max(times)
    y_top = max(max(series["err_net"]), max(series["err_const"]))
    y_lo, y_hi, y_ticks = _axis(0.0, y_top, 5)
    _, _, t_ticks = _axis(t_lo, t_hi, 5)

    def bx(value: float) -> float:
        return left + (float(value) - t_lo) / (t_hi - t_lo) * width

    def by(value: float) -> float:
        return bottom - (float(value) - y_lo) / (y_hi - y_lo) * height

    out = ['<g id="panel-b">']
    out.append(
        _text(left, 80.0, "Panel B: error against time", size=14.0, weight="bold")
    )
    out.append(_rect(left, top, width, height, PAPER, INK, 1.0))
    for tick in y_ticks[1:-1]:
        out.append(_line(left, by(tick), right, by(tick), GRID, 1.0))
    for tick in t_ticks[1:-1]:
        out.append(_line(bx(tick), top, bx(tick), bottom, GRID, 1.0))
    for tick in t_ticks:
        out.append(
            _text(bx(tick), bottom + 14.0, f"{tick:g}", size=10.0, color=MUTED,
                  anchor="middle")
        )
    for tick in y_ticks:
        out.append(
            _text(left - 6.0, by(tick) + 3.5, f"{tick:g}", size=10.0, color=MUTED,
                  anchor="end")
        )
    out.append(
        _text(0.5 * (left + right), bottom + 34.0, "time (system units)", size=11.0,
              color=MUTED, anchor="middle")
    )
    middle = 0.5 * (top + bottom)
    out.append(
        _text(
            714.0,
            middle,
            "error (largest of the body and inner-pair errors)",
            size=11.0,
            color=MUTED,
            anchor="middle",
            transform=f"rotate(-90 714.0 {middle:.1f})",
        )
    )

    tier1 = float(series["tier1"])
    out.append(_line(left, by(tier1), right, by(tier1), LIMIT, 1.5, "6 4"))
    out.append(
        _text(
            right - 4.0,
            by(tier1) - 6.0,
            f"Tier 1 limit ({tier1:g})",
            size=10.0,
            color=LIMIT,
            anchor="end",
        )
    )
    # The dashed reference is wider and drawn underneath: the two curves differ
    # by about 0.006, so a same-width dashed line would disappear behind the
    # solid network curve and the comparison would be invisible.
    out.append(
        _poly(
            (bx(value) for value in times),
            (by(value) for value in series["err_const"]),
            MUTED,
            3.5,
            "6 4",
        )
    )
    out.append(
        _poly(
            (bx(value) for value in times),
            (by(value) for value in series["err_net"]),
            INK,
            1.5,
        )
    )
    out.append("</g>")
    return out


def _legend() -> list[str]:
    """The legend inside the canvas: a swatch, then its label, one row at a time."""
    left, top, width, height = LEGEND
    out = ['<g id="legend">']
    out.append(_rect(left, top, width, height, PAPER, GRID, 1.0))

    def entry(
        x: float,
        y: float,
        label: str,
        *,
        color: str,
        stroke: float = 2.0,
        dash: Optional[str] = None,
        cross: bool = False,
    ) -> tuple[list[str], float]:
        elements: list[str] = []
        if cross:
            centre = x + 11.0
            elements.append(
                _line(centre - 5.0, y - 4.0, centre + 5.0, y - 4.0, color, stroke)
            )
            elements.append(_line(centre, y - 9.0, centre, y + 1.0, color, stroke))
        else:
            elements.append(_line(x, y - 4.0, x + 22.0, y - 4.0, color, stroke, dash))
        text_x = x + 28.0
        elements.append(_text(text_x, y, label, size=11.0))
        # 0.55 em per character is a safe upper bound for Helvetica at this size,
        # so the layout cannot collide even if the renderer picks Arial instead.
        advance = 28.0 + 0.55 * 11.0 * len(label) + 24.0
        return elements, x + advance

    x, y = 96.0, 494.0
    for body, color in enumerate(BODY_COLORS):
        elements, x = entry(x, y, f"real orbit, body {body + 1}", color=color)
        out.extend(elements)
    elements, x = entry(x, y, "network prediction", color=BODY_COLORS[0], stroke=3.0)
    out.extend(elements)

    x, y = 96.0, 522.0
    elements, x = entry(x, y, "time-mean position", color=INK, cross=True)
    out.extend(elements)
    elements, x = entry(x, y, "network error", color=INK, stroke=2.0)
    out.extend(elements)
    elements, x = entry(
        x,
        y,
        "error of guessing each body's average position",
        color=MUTED,
        stroke=1.5,
        dash="6 4",
    )
    out.extend(elements)
    elements, x = entry(x, y, "Tier 1 limit", color=LIMIT, stroke=1.5, dash="6 4")
    out.extend(elements)
    out.append("</g>")
    return out


def legibility_report(series: Mapping[str, Any], svg_text: str) -> dict[str, Any]:
    """Measure the legend, the two panels and each predicted track in the document."""
    try:
        root = ElementTree.fromstring(svg_text)
    except ElementTree.ParseError as exc:
        fail(f"the rendered SVG is not well-formed XML: {exc}")

    groups = {
        element.get("id"): element
        for element in root.iter()
        if element.get("id") in {"panel-a", "panel-b", "legend"}
    }
    for name in ("panel-a", "panel-b", "legend"):
        if name not in groups:
            fail(f"the rendered SVG has no group with id {name!r}")

    xs: list[float] = []
    ys: list[float] = []
    for element in groups["legend"].iter():
        tag = element.tag.rsplit("}", 1)[-1]
        if tag == "text":
            x, y = float(element.get("x")), float(element.get("y"))
            size = float(element.get("font-size", "11"))
            estimate = 0.55 * size * len(element.text or "")
            anchor = element.get("text-anchor", "start")
            if anchor == "middle":
                xs.extend([x - 0.5 * estimate, x + 0.5 * estimate])
            elif anchor == "end":
                xs.extend([x - estimate, x])
            else:
                xs.extend([x, x + estimate])
            ys.extend([y - size, y])
        elif tag == "line":
            xs.extend([float(element.get("x1")), float(element.get("x2"))])
            ys.extend([float(element.get("y1")), float(element.get("y2"))])
        elif tag == "rect":
            x, y = float(element.get("x")), float(element.get("y"))
            xs.extend([x, x + float(element.get("width"))])
            ys.extend([y, y + float(element.get("height"))])
    legend = [min(xs), min(ys), max(xs), max(ys)]

    frames: dict[str, list[float]] = {}
    for name in ("panel-a", "panel-b"):
        rect = next(
            element
            for element in groups[name].iter()
            if element.tag.rsplit("}", 1)[-1] == "rect"
        )
        x, y = float(rect.get("x")), float(rect.get("y"))
        frames[name] = [
            x,
            y,
            x + float(rect.get("width")),
            y + float(rect.get("height")),
        ]

    spans = []
    for track in series["pred_xy"]:
        track_x = [point[0] for point in track]
        track_y = [point[1] for point in track]
        spans.append([max(track_x) - min(track_x), max(track_y) - min(track_y)])

    return {
        "legend": legend,
        "frames": frames,
        "predicted_spans": spans,
        "min_err_net": min(series["err_net"]),
        "min_err_const": min(series["err_const"]),
        "tier1": float(series["tier1"]),
    }


def _check_legibility(series: Mapping[str, Any], svg_text: str) -> dict[str, Any]:
    """Refuse a figure whose legend escapes the canvas or whose tracks are dots."""
    report = legibility_report(series, svg_text)
    legend = report["legend"]
    if legend[0] < 0.0 or legend[1] < 0.0:
        fail(f"the legend starts outside the canvas at {legend[0]:.1f},{legend[1]:.1f}")
    if legend[2] > VIEW_WIDTH or legend[3] > VIEW_HEIGHT:
        fail(f"the legend ends outside the canvas at {legend[2]:.1f},{legend[3]:.1f}")
    panel_bottom = max(frame[3] for frame in report["frames"].values())
    if legend[1] <= panel_bottom + 8.0:
        fail(
            f"the legend at y {legend[1]:.1f} overlaps the panels ending at "
            f"{panel_bottom:.1f}"
        )
    if report["frames"]["panel-b"][0] <= INSET_RIGHT + 20.0:
        fail("panel B starts inside the inset")
    for body, (span_x, span_y) in enumerate(report["predicted_spans"]):
        if span_x <= 0.0 or span_y <= 0.0:
            fail(f"body {body + 1}'s predicted track has no extent: {span_x}x{span_y}")
    for label in (
        "x (system units)",
        "y (system units)",
        "time (system units)",
        "error (largest of the body and inner-pair errors)",
        f"Tier 1 limit ({float(series['tier1']):g})",
    ):
        if label not in svg_text:
            fail(f"the figure is missing the label {label!r}")
    return report


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
    lines.extend(_panel_b(series))
    lines.extend(_legend())
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
    report = _check_legibility(series, svg_text)
    provenance = build_provenance(series, svg_text, _inputs(REPO_ROOT))
    legend = report["legend"]
    spans = " ".join(
        f"{span_x:.4f}x{span_y:.4f}" for span_x, span_y in report["predicted_spans"]
    )
    print(
        f"FIGURE-LEGIBLE legend {legend[0]:.1f},{legend[1]:.1f},"
        f"{legend[2]:.1f},{legend[3]:.1f} predicted {spans}"
    )

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
