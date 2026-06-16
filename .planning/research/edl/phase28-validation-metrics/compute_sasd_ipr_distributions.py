#!/usr/bin/env python3
"""
EDL decision-support for Phase 28 GAP-28-01 (SASD endpoint) and GAP-28-02 (IPR units).

NON-CANONICAL research support per CLAUDE.md EDL protocol. Does NOT resolve the gaps and
authorizes no spec edit. Produces the resolution-doc-specified verification numbers so the
user can rule on two source-silent forks with data in hand.

Construction is the SETTLED part of each contract (02-resolution-doc.md sec5.2/5.3 + the two
EVID-06 packets); only the endpoint (SASD) and the units (IPR) are the open forks.

  SASD_i = dt_i * max_body [ ||a_b|| / max(||v_b||, 1e-12) ]      (per-body max, full-norm)
     left : ratio at t_i only          both : dt_i*max_b max(ratio_b(t_i),ratio_b(t_{i+1}))
     flag : max_i SASD_i > 0.5         (SASD is scale-invariant: raw == scaled)
  IPR  = mean_k || q''_spline(tau_k) - F_grav^eps(q_spline(tau_k)) ||^2   (stacked 9-vector)
     spline CubicHermiteSpline(t,q,dydx=v); 10 mid-offset pts/interval; eps=1e-10; G=1
     flag : IPR > 1e-3 RAW (open fork: raw vs scaled, ~464x per resolution doc sec5.3)

VALIDATED: analytic circular binary (well-resolved) -> IPR ~1e-10; dt=0.17 coarsening ~9e-6.

Population: "clean" = no collision (min_sep >= COLL) and no escape (max_sep <= ESC), which
approximates the admitted set (the precise admitted list is the Stage-gate output; this proxy
is stated so the numbers are interpretable). Raw output is dominated by close encounters whose
residuals are physically enormous, so flag rates are reported on the clean subset and the IPR
distribution is stratified by minimum approach distance.

Usage: .venv/bin/python compute_sasd_ipr_distributions.py [N_PER_TIER=150] [SEED=42]
"""
import sys, json, random, glob, math
import numpy as np
from scipy.interpolate import CubicHermiteSpline

EPS          = 1e-10
N_INT        = 10
SASD_FLAG    = 0.5
IPR_FLAG_RAW = 1e-3
RAW_OVER_SCALED = 2.155e-3                              # raw IPR ~= scaled * 2.155e-3
SCALED_OVER_RAW = 1.0 / RAW_OVER_SCALED                # ~464.2
IPR_FLAG_SCALED_AS_RAW = IPR_FLAG_RAW * RAW_OVER_SCALED # raw-value equiv of scaled-1e-3 ~2.155e-6
OFFSETS = (np.arange(N_INT) + 0.5) / N_INT
COLL = 0.01     # possible_collision threshold (dataset detection convention)
ESC  = 100.0    # possible_escape threshold (dataset detection convention)

ROOT = "<home>/Desktop/3_body_problem/simulation_data/Data/brutus_output"
TIERS = {
    "std_base":  f"{ROOT}/brutus_standard_quasi_random",
    "std_gold":  f"{ROOT}/brutus_standard_quasi_random_gold_standard",
    "hier_base": f"{ROOT}/brutus_hierarchical",
    "hier_gold": f"{ROOT}/brutus_hierarchical_gold_standard",
}


def parse_brutus(path):
    times, P, V = [], [], []
    cur_t, bodies = None, []
    with open(path) as fh:
        for line in fh:
            toks = line.split()
            if not toks or toks[0].lower().startswith("result"):
                continue
            if len(toks) == 3:
                if cur_t is not None and len(bodies) == 3:
                    times.append(cur_t); P.append([b[0] for b in bodies]); V.append([b[1] for b in bodies])
                cur_t, bodies = float(toks[0]), []
            elif len(toks) == 7:
                vals = list(map(float, toks)); bodies.append((vals[1:4], vals[4:7]))
    if cur_t is not None and len(bodies) == 3:
        times.append(cur_t); P.append([b[0] for b in bodies]); V.append([b[1] for b in bodies])
    return np.array(times), np.array(P), np.array(V)


def grav_accel(Q, eps=EPS):
    qb = Q[:, :, None, :]; qc = Q[:, None, :, :]
    diff = qc - qb
    inv = 1.0 / np.power(np.sum(diff * diff, axis=-1) + eps * eps, 1.5)
    d = np.arange(3); inv[:, d, d] = 0.0
    return np.sum(diff * inv[..., None], axis=2)


def sep_stats(P):
    ds = [np.linalg.norm(P[:, a, :] - P[:, b, :], axis=1) for a, b in [(0,1),(0,2),(1,2)]]
    ds = np.stack(ds)
    return float(ds.min()), float(ds.max())


def sasd_conventions(t, P, V):
    A = grav_accel(P)
    ratio = np.linalg.norm(A, axis=-1) / np.maximum(np.linalg.norm(V, axis=-1), 1e-12)
    dt = np.diff(t)
    left = float((dt * ratio[:-1].max(axis=1)).max())
    both = float((dt * np.maximum(ratio[:-1], ratio[1:]).max(axis=1)).max())
    return left, both


def ipr_raw(t, P, V):
    n = len(t)
    chs = CubicHermiteSpline(t, P.reshape(n, 9), V.reshape(n, 9), axis=0)
    d2 = chs.derivative(2)
    dt = np.diff(t)
    tau = (t[:-1, None] + OFFSETS[None, :] * dt[:, None]).reshape(-1)
    r = d2(tau) - grav_accel(chs(tau).reshape(-1, 3, 3)).reshape(-1, 9)
    return float(np.mean(np.sum(r * r, axis=1)))


def frac(mask):
    return (int(mask.sum()), len(mask), float(mask.mean()) if len(mask) else float("nan"))


def main():
    n_per = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    rng = random.Random(seed)
    out = {"params": {"n_per_tier": n_per, "seed": seed, "eps": EPS, "coll": COLL, "esc": ESC,
                      "sasd_flag": SASD_FLAG, "ipr_flag_raw": IPR_FLAG_RAW,
                      "scaled_over_raw": SCALED_OVER_RAW,
                      "ipr_flag_scaled_as_raw": IPR_FLAG_SCALED_AS_RAW}, "tiers": {}}

    print(f"# Phase 28 EDL  n_per_tier={n_per} seed={seed}  clean = min_sep>={COLL} & max_sep<={ESC}")
    print(f"# SASD flag>{SASD_FLAG} (scale-invariant) | IPR raw flag>{IPR_FLAG_RAW} | "
          f"scaled-1e-3 == raw>{IPR_FLAG_SCALED_AS_RAW:.3e}  (scaled = raw x{SCALED_OVER_RAW:.0f})")
    print()
    gold_pool = []   # (min_sep, ipr) for stratification across gold tiers

    for tier, folder in TIERS.items():
        files = sorted(glob.glob(f"{folder}/*.txt"))
        sample = files if len(files) <= n_per else rng.sample(files, n_per)
        rows = []
        for fp in sample:
            try:
                t, P, V = parse_brutus(fp)
                if len(t) < 4 or not np.all(np.diff(t) > 0):
                    continue
                mn, mx = sep_stats(P)
                ipr = ipr_raw(t, P, V)
                sl, sb = sasd_conventions(t, P, V)
                if all(map(math.isfinite, (ipr, sl, sb, mn, mx))):
                    rows.append((mn, mx, ipr, sl, sb))
            except Exception:
                pass
        if not rows:
            print(f"[{tier}] no usable trajectories"); continue
        mn = np.array([r[0] for r in rows]); mx = np.array([r[1] for r in rows])
        ipr = np.array([r[2] for r in rows]); sl = np.array([r[3] for r in rows]); sb = np.array([r[4] for r in rows])
        clean = (mn >= COLL) & (mx <= ESC)
        ci = ipr[clean]; csl = sl[clean]; csb = sb[clean]
        if "gold" in tier:
            gold_pool += list(zip(mn[clean].tolist(), ci.tolist()))

        def pr(a, p): return float(np.percentile(a, p)) if len(a) else float("nan")
        rec = {"n_total": len(rows), "n_clean": int(clean.sum()),
               "ipr_raw_clean": {"p10": pr(ci,10), "p50": pr(ci,50), "p90": pr(ci,90),
                                  "max": float(ci.max()) if len(ci) else None},
               "ipr_flag_raw":    frac(ci > IPR_FLAG_RAW),
               "ipr_flag_scaled": frac(ci > IPR_FLAG_SCALED_AS_RAW),
               "sasd_flag_left":  frac(csl > SASD_FLAG),
               "sasd_flag_both":  frac(csb > SASD_FLAG),
               "sasd_cross_only_both": int(np.sum((csl <= SASD_FLAG) & (csb > SASD_FLAG)))}
        out["tiers"][tier] = rec
        print(f"[{tier}] n={len(rows)}  clean={int(clean.sum())}  "
              f"(excluded {len(rows)-int(clean.sum())} collide/escape)")
        if len(ci):
            print(f"   IPR(raw,clean)  p10={pr(ci,10):.2e}  p50={pr(ci,50):.2e}  "
                  f"p90={pr(ci,90):.2e}  max={ci.max():.2e}")
            print(f"   IPR flag  raw>1e-3 : {int((ci>IPR_FLAG_RAW).sum())}/{len(ci)} "
                  f"= {100*(ci>IPR_FLAG_RAW).mean():.0f}%   scaled>1e-3 (raw>{IPR_FLAG_SCALED_AS_RAW:.1e}) : "
                  f"{int((ci>IPR_FLAG_SCALED_AS_RAW).sum())}/{len(ci)} = {100*(ci>IPR_FLAG_SCALED_AS_RAW).mean():.0f}%")
            print(f"   SASD flag  left>0.5 : {int((csl>SASD_FLAG).sum())}/{len(csl)} = {100*(csl>SASD_FLAG).mean():.0f}%"
                  f"   both>0.5 : {int((csb>SASD_FLAG).sum())}/{len(csb)} = {100*(csb>SASD_FLAG).mean():.0f}%"
                  f"   cross-only-both: {int(np.sum((csl<=SASD_FLAG)&(csb>SASD_FLAG)))}")
        print()

    # ---- gold IPR stratified by minimum approach distance ----
    if gold_pool:
        gp = np.array(gold_pool)  # (.,2): min_sep, ipr
        print("[gold clean] IPR(raw) median stratified by minimum approach distance:")
        edges = [0.01, 0.05, 0.1, 0.3, 1.0, np.inf]
        out["gold_strat"] = []
        for lo, hi in zip(edges[:-1], edges[1:]):
            m = (gp[:,0] >= lo) & (gp[:,0] < hi)
            if m.any():
                med = float(np.median(gp[m,1])); cnt = int(m.sum())
                print(f"   min_sep in [{lo:>4}, {hi:>4}) : n={cnt:4d}  median IPR(raw) = {med:.2e}")
                out["gold_strat"].append({"lo": lo, "hi": None if hi==np.inf else hi, "n": cnt, "median_ipr_raw": med})
        print()

    res = "<home>/Desktop/3_body_problem/.planning/research/edl/phase28-validation-metrics/results.json"
    with open(res, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"# results -> {res}")


if __name__ == "__main__":
    main()
