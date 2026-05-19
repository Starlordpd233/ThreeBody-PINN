I would add an explicit **Sobol coordinate allocation convention** to both the Markdown and the LaTeX/PDF source. The current text is ambiguous because it assigns (u_4) to global scaling, but then immediately says velocity sampling uses ((u_4,u_5,u_6)). That means (u_4) is double-booked whenever scaling is enabled. The Markdown and PDF both contain this same conflict. The document first says the Sobol engine uses 6 base dimensions, plus optional extras such as one dimension for global scaling; then the “Global Scaling” section maps (u_4) to the scale factor (s); then the “Velocity Sampling” section says the next three coordinates are ((u_4,u_5,u_6)).  

## Current state

The intended coordinate mapping appears to be:

[
u_1,u_2,u_3
]

for the sampled position of particle 2: polar angle, azimuthal angle, and radial distance. This part is clean and unambiguous in both files. 

Then the text says that optional global scaling uses an additional Sobol dimension:

[
s=s_{\min}+(s_{\max}-s_{\min})u_4.
]

The same section also states that the main block enables this scaling with range ([0.8,1.2]), so this is not merely a dormant option in the described run. 

But the next section says velocity sampling uses:

[
(u_4,u_5,u_6)
]

with

[
v_i=\Phi^{-1}(u_{3+i};\mu=0,\sigma=\text{velocity_scale}),\quad i=1,2,3.
]

So, under enabled scaling, (u_4) is being described as both the global scale coordinate and the first velocity coordinate. 

## The actual issue

This is not just a cosmetic indexing issue. If (u_4) is used for both (s) and the first velocity component, then the global spatial/velocity scale and one component of the sampled velocity vector become deterministically coupled. That would reduce the effective sampling dimension and inject an artificial correlation into the generated ICs.

The issue is especially important because the document already warns that quasi-random global scaling changes the virial ratio by (s^3). If the first velocity component is also tied to the same (u_4), then the sampling has an additional, undocumented correlation beyond the stated virial-ratio distortion. 

## My proposed fix

I would preserve the current statement that **global scaling uses (u_4)** when scaling is enabled, because that is already explicit in both files. Then I would shift the velocity coordinates forward by one coordinate whenever scaling is enabled.

That gives the following rule:

[
u_1,u_2,u_3 = \text{position coordinates}
]

If global scaling is disabled:

[
s=1,\qquad \mathbf{v}\text{ uses }(u_4,u_5,u_6).
]

If global scaling is enabled:

[
s=s_{\min}+(s_{\max}-s_{\min})u_4,
\qquad
\mathbf{v}\text{ uses }(u_5,u_6,u_7).
]

This is the cleanest correction because it keeps the current scale mapping (u_4\mapsto s) and only changes the velocity-index statement.

## Text I would add to both files

I would insert this immediately after the “Low-Discrepancy Engine: Sobol Sequence” subsection, or at the start of “Mapping Sobol Numbers to Physical Coordinates.”

### Markdown-ready insertion

```markdown
#### Sobol Coordinate Allocation Convention

Throughout this document, the Sobol coordinates \(u_i\) use 1-based mathematical indexing. In implementation, array indices should be shifted by one.

The first three Sobol coordinates are always reserved for position sampling:

\[
u_1,u_2,u_3 \quad \longrightarrow \quad \theta,\phi,r.
\]

Define

\[
\delta_s =
\begin{cases}
1, & \text{if global scaling is enabled, i.e. } s_{\min}\neq s_{\max},\\
0, & \text{otherwise.}
\end{cases}
\]

If global scaling is disabled, set \(s=1\) and do not consume an additional Sobol coordinate. The velocity coordinates are then

\[
(u_4,u_5,u_6).
\]

If global scaling is enabled, consume \(u_4\) for the scale factor,

\[
s=s_{\min}+(s_{\max}-s_{\min})u_4,
\]

and shift velocity sampling to the next three coordinates,

\[
(u_5,u_6,u_7).
\]

Equivalently, for both cases,

\[
v_i=\Phi^{-1}\!\left(u_{3+\delta_s+i};\,\mu=0,\sigma=\text{velocity\_scale}\right),
\quad i=1,2,3.
\]

Thus, the required Sobol dimension is

\[
d=6+\delta_s.
\]

This convention prevents any Sobol coordinate from being reused for two independent physical quantities.
```

## Lines I would replace

I would also replace the existing velocity sentence. Current version:

```markdown
The next three Sobol coordinates \((u_4, u_5, u_6)\) are mapped to a 3D velocity vector \(\mathbf{v}\) ...
```

Replace it with:

```markdown
The three velocity coordinates are \((u_{4+\delta_s},u_{5+\delta_s},u_{6+\delta_s})\), where \(\delta_s=1\) if global scaling consumes \(u_4\), and \(\delta_s=0\) otherwise. These coordinates are mapped to a 3D velocity vector \(\mathbf{v}\) using inverse transform sampling from a normal distribution with mean 0 and standard deviation \(\sigma=\text{velocity\_scale}\).
```

And replace the formula:

```markdown
\[
v_i = \Phi^{-1}(u_{3+i};\,\mu=0,\,\sigma=\text{velocity\_scale}),\quad i=1,2,3.
\]
```

with:

```markdown
\[
v_i = \Phi^{-1}(u_{3+\delta_s+i};\,\mu=0,\,\sigma=\text{velocity\_scale}),\quad i=1,2,3.
\]
```

## LaTeX-ready version

For the LaTeX source behind the PDF, I would add:

```latex
\paragraph{Sobol Coordinate Allocation Convention.}
Throughout this document, the Sobol coordinates \(u_i\) use 1-based mathematical indexing. In implementation, array indices should be shifted by one.

The first three Sobol coordinates are always reserved for position sampling:
\[
u_1,u_2,u_3 \quad \longrightarrow \quad \theta,\phi,r.
\]

Define
\[
\delta_s =
\begin{cases}
1, & \text{if global scaling is enabled, i.e. } s_{\min}\neq s_{\max},\\
0, & \text{otherwise.}
\end{cases}
\]

If global scaling is disabled, set \(s=1\) and do not consume an additional Sobol coordinate. The velocity coordinates are then
\[
(u_4,u_5,u_6).
\]

If global scaling is enabled, consume \(u_4\) for the scale factor,
\[
s=s_{\min}+(s_{\max}-s_{\min})u_4,
\]
and shift velocity sampling to the next three coordinates,
\[
(u_5,u_6,u_7).
\]

Equivalently, for both cases,
\[
v_i=\Phi^{-1}\!\left(u_{3+\delta_s+i};\,\mu=0,\sigma=\texttt{velocity\_scale}\right),
\quad i=1,2,3.
\]

Thus, the required Sobol dimension is
\[
d=6+\delta_s.
\]

This convention prevents any Sobol coordinate from being reused for two independent physical quantities.
```

## Implementation note I would add

I would also add a short code-level clarification because this is exactly the kind of thing that gets misimplemented due to 1-based math notation versus 0-based Python arrays:

```python
scale_enabled = scale_range is not None and scale_range[0] != scale_range[1]

sobol_dim = 6 + int(scale_enabled)
u = sobol_engine.random(n)

# Python uses 0-based indexing:
# u[:, 0], u[:, 1], u[:, 2] -> position coordinates
idx = 3

if scale_enabled:
    s_min, s_max = scale_range
    s = s_min + (s_max - s_min) * u[:, idx]  # mathematical u_4
    idx += 1
else:
    s = 1.0

velocity_coords = u[:, idx:idx+3]  # u_4,u_5,u_6 if no scaling; u_5,u_6,u_7 if scaling
v = scipy.stats.norm.ppf(
    velocity_coords,
    loc=0.0,
    scale=velocity_scale
)
```

## One alternative, but I would not choose it here

The other possible fix is to keep velocities permanently assigned to ((u_4,u_5,u_6)) and move global scaling to (u_7). That would also be mathematically valid and would align with the phrase “base 6 dimensions plus optional extras.” But it conflicts with the current text’s explicit statement that scaling maps (u_4) to (s). Since both files already state that (u_4) is the scale coordinate, I would instead keep (u_4) for scaling and shift velocities to ((u_5,u_6,u_7)) when scaling is enabled.

My recommendation: add the (\delta_s) convention and update the velocity-sampling formula. This resolves the ambiguity with minimal disruption and makes the enabled-scaling case implementation-ready.
