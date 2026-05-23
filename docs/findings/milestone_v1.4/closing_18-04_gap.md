# Response and Final Recommendation on Closing 18-04 Gap

**Status:** ACCEPTED 2026-05-21 — user-approved closure of GAP-18-04. The binding in this document is now the canonical Phase 18 rotation-gauge degeneracy contract; recorded in `.planning/phases/18-frame-and-gauge-contracts/18-CONTEXT.md` D-14 and `.planning/phases/18-frame-and-gauge-contracts/18-GAPS.md` GAP-18-04 Resolution note. The "Important validation note" section is informational guidance for Phase 21 VER-01/VER-04 — it is NOT a Phase 18 spec edit or `AC-FRAME-*` criterion.

According to the Phase 18 context gathered on 2026-05-20, **GAP-18-04 should be closed now, not deferred**, because Phase 18 explicitly locks the frame/gauge contract and currently cannot proceed past the open rotation-gauge threshold guard. 

## Final call

Adopt **option (c)**, but make it exact:

[
\boxed{\eta_{\mathrm{gauge}} = 10^{-8}}
]

Use this as a **dimensionless relative threshold**, evaluated against the global Phase-18 scale constants:

[
\boxed{\epsilon_\rho = \eta_{\mathrm{gauge}}D}
]

[
\boxed{\epsilon_\lambda = \eta_{\mathrm{gauge}}D}
]

and for fallback velocity candidates,

[
\boxed{\epsilon_v = \eta_{\mathrm{gauge}}V,\qquad V=D/T.}
]

So the algorithm should compare

[
\frac{|\rho|}{D} > 10^{-8},
\qquad
\frac{|\lambda_\perp|}{D} > 10^{-8},
\qquad
\frac{|c_\perp|}{V} > 10^{-8}
]

rather than comparing raw norms to hard-coded raw-coordinate constants.

This preserves the existing Phase 18 order — COM/boost, ordering, rotation, then scaling — while making the threshold behavior equivalent to applying a (10^{-8}) guard in scaled coordinates. The resolution’s rotation-gauge algorithm is already written in the pre-scaling COM-corrected frame, but its (\varepsilon_\rho) and (\varepsilon_\lambda) symbols are unbound; this contract binds them without changing the algorithm’s geometry. 

## Why this is the right engineering choice

Leaving the epsilons symbolic is not acceptable for Phase 18. The framework says every IC and BRUTUS snapshot must pass through one deterministic pipeline — parse, mass check, COM recenter, zero-momentum boost, canonical ordering, canonical rotation, then global scaling — and the rotation gauge is part of that locked contract. 

Absolute raw-coordinate thresholds are also the wrong choice. They would depend on whatever raw units the data happened to use, while the rest of the framework is explicitly organized around global (D,T,V) scaling metadata. A dimensionless threshold makes the gauge invariant under consistent unit rescalings and keeps the pre-scaling rotation step compatible with the later scaled IC13 construction. 

The value (10^{-8}) is small enough that valid near-collinear geometries are almost always handled by the generic gauge, but large enough to avoid normalizing vectors whose direction is dominated by floating-point roundoff. It is also deliberately much smaller than the dynamic training softening (\epsilon_{\text{train}}=10^{-5}), so the gauge is not using the force-softening scale to erase physical geometry. 

## Exact contract to insert into Step 2.4

Use this wording.

```markdown
#### Degeneracy thresholds for the canonical rotation gauge

The rotation-gauge degeneracy thresholds are dimensionless relative
thresholds, not raw-coordinate constants.

Let

\[
\eta_{\rm gauge}=10^{-8}.
\]

Because the rotation gauge is applied after COM recentering, zero-momentum
boosting, and canonical ordering, but before global scaling, define the
raw-space thresholds by the global Phase-18 scales:

\[
\epsilon_\rho = \eta_{\rm gauge}D,\qquad
\epsilon_\lambda = \eta_{\rm gauge}D,\qquad
\epsilon_v = \eta_{\rm gauge}V,\quad V=D/T.
\]

Equivalently, the implementation may compare the dimensionless ratios
\[
\|\rho\|/D,\quad \|\lambda_\perp\|/D,\quad \|c_\perp\|/V
\]
against \(\eta_{\rm gauge}\).

The primary Jacobi vector is admissible only if

\[
\|\rho\|/D > \eta_{\rm gauge}.
\]

If this condition fails, the trajectory is classified as
`gauge_degenerate_rho` and is rejected or quarantined for near-collision
review; the executor must not invent an arbitrary \(e_x\) axis.

After setting \(e_x=\rho/\|\rho\|\), compute

\[
\lambda_\perp = \lambda - (\lambda\cdot e_x)e_x.
\]

If

\[
\|\lambda_\perp\|/D > \eta_{\rm gauge},
\]

set

\[
e_y=\lambda_\perp/\|\lambda_\perp\|.
\]

Otherwise use the collinear fallback sequence. For each velocity-like
candidate

\[
c\in\{\dot\rho,\dot\lambda,\bar v_1(0),\bar v_2(0),\bar v_3(0)\},
\]

compute

\[
c_\perp=c-(c\cdot e_x)e_x.
\]

The first candidate satisfying

\[
\|c_\perp\|/V > \eta_{\rm gauge}
\]

is used to define

\[
e_y=c_\perp/\|c_\perp\|.
\]

If no candidate passes this test, choose the fixed coordinate basis vector
\(b\in\{e_1,e_2,e_3\}\) least aligned with \(e_x\), project it perpendicular
to \(e_x\), and normalize.

After selecting \(e_y\), orient its sign deterministically: if
\(\lambda_\perp\cdot e_y < 0\), replace \(e_y\leftarrow -e_y\). Then set

\[
e_z=e_x\times e_y.
\]

This keeps \(\lambda_y\ge 0\) whenever the sign is numerically meaningful.
For exact collinear geometries, \(\lambda_y=0\) and the fallback candidate
order supplies the deterministic sign.
```

## Important validation note

The existing resolution test says to check (R_0R_0^\top), (\det R_0), (\rho_y), (\rho_z), (\lambda_z), and (\lambda_y) at (10^{-12})-level tolerance. That remains correct for the **generic branch**, where (\lambda_\perp) defines (e_y). 

For the **fallback branch**, the test must be branch-aware:

[
|\lambda_z^g|/D \le \eta_{\rm gauge}
]

or, after scaling,

[
|\lambda_z'| \le 10^{-8}.
]

That is not a failure of the gauge. It is exactly what it means to intentionally classify a geometry as numerically collinear when (|\lambda_\perp|/D \le 10^{-8}).

## Resolution note to record

```markdown
RESOLVED — GAP-18-04 closes by binding the rotation-gauge degeneracy
guards as dimensionless relative thresholds.

Use eta_gauge = 1e-8. Since Phase 18 applies canonical rotation before
global scaling, define epsilon_rho = eta_gauge*D and
epsilon_lambda = eta_gauge*D in the COM-corrected, canonically ordered
raw coordinate frame. Velocity fallback candidates use
epsilon_v = eta_gauge*V, V = D/T. Implementations may equivalently compare
scaled ratios ||rho||/D, ||lambda_perp||/D, and ||candidate_perp||/V
against eta_gauge.

If ||rho||/D <= eta_gauge, classify the trajectory as
gauge_degenerate_rho and reject/quarantine it rather than inventing an
arbitrary primary x-axis. If ||lambda_perp||/D <= eta_gauge, use the
documented collinear fallback sequence, with projected velocity candidates
classified as nonzero only when ||candidate_perp||/V > eta_gauge. The
fixed-coordinate fallback remains the final deterministic fallback.

The threshold is not a physics softening parameter and is not tied to
epsilon_train or epsilon_inv. It is a numerical geometry guard for
stable construction of the canonical rotation matrix.
```

This is the cleanest closure: it gives implementers exact numbers, respects the pre-scaling rotation order, avoids unit-dependent raw thresholds, and prevents FUT-01 or Phase 21 from silently inventing gauge tolerances.
