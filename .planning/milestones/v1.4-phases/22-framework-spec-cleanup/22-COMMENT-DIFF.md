---
phase: 22
slug: framework-spec-cleanup
artifact: comment-diff
status: committed
created: 2026-06-09
consumes:
  - .planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-COMMENT-CENSUS-PRE.md
  - .planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-COMMENT-CENSUS-POST.md
---

# Pre/Post WS-A Census Diff

**Method:** Parse `COMMENT_HASH <stable-comment-id> <text_hash>` lines from the committed PRE and POST censuses. Compare by stable-id (bijection) and by text_hash (byte identity).

**Result:**

| Metric | Value |
|--------|-------|
| PRE total | 26 |
| POST total | 26 |
| Lost (stable-id in PRE, not in POST) | 0 |
| Gained (stable-id in POST, not in PRE) | 0 |
| Common by stable-id | 26 |
| Hash-identical (PRE text_hash = POST text_hash) | 23 |
| Hash-changed (D-05 wrapper repairs) | 3 |

## D-05 Wrapper Repair Register (3 comments)

Each of the 3 hash-changed comments is a **mechanical wrapper repair** under D-05: the WS-A edits (22-02 math normalization) repaired Markdown-render-breaking syntax in the **prose surrounding** the author-comment clause. The author-comment clause itself is byte-identical between PRE and POST in all 3 cases. The verbatim-text hash changes only because the surrounding prose (which is part of the censused text blob) was syntax-normalized.

### 1. `pinn_architecture::3-4-soft-energy-conservation-regularizer-le-enforcing-a-global-conservation-law::1`
- **PRE hash:** `d52fb46ae588ded9c90a9313454fb82b3fd44e1bb0ab2903eb816767fac4a962`
- **POST hash:** `ef54ad6d04a6335fd3cc2fc24d273c0483b5e2d6d6b490d24058c934e1d2d923`
- **Wrapper change:** `` `10^-5` `` → `$10^{-5}$`; backtick `epsilon_H` → `$\epsilon_H$`; `<=` → `$\leq$`
- **Comment clause preserved:** `(Author Comment: I am not sure why there is a duplicate 10^-5 here)` byte-identical

### 2. `pinn_architecture::3-4-soft-energy-conservation-regularizer-le-enforcing-a-global-conservation-law::2`
- **PRE hash:** `465b94063376c82437d69f8684019dabe6a54d99555dc4664a949d088708ac2f`
- **POST hash:** `9647dd1059a7492329e485809d1da1b7d475f78b18e25ed5973384ae4b0a24f4`
- **Wrapper change:** `` `10^-5` `` → `$10^{-5}$`
- **Comment clause preserved:** `(author comment: again duplicate number)` byte-identical

### 3. `pinn_architecture::4-2-optional-alm-ablation-p2::1`
- **PRE hash:** `d4948db1a221eca479600880018243b74a8327199613f9ff15eb5e7e0f136fae`
- **POST hash:** `8a81ec714461e8a7e393e5f204960555c8d515c2cab8f4e8adbc54e728977030`
- **Wrapper change:** raw-subscript math `c_E = RMS_n(ΔH_n), c_{L,α} = RMS_n((L'_θ,α(u_n) - L_0,α') / L_scale)` → proper LaTeX `$c_E = \mathrm{RMS}_n(\Delta H_n)$, $c_{L,\alpha} = \mathrm{RMS}_n((L'_{\theta,\alpha}(u_n) - L'_{0,\alpha}) / L_{scale})$`
- **Comment clause preserved:** `(Author Comment: this syntax is not ideal since it invovles math equations/formula; it should properly use correct markdown render-friendly syntax)` byte-identical

## Negative Findings

- 0 author comments deleted.
- 0 author comments semantically altered.
- 0 comments extracted, resolved, rewritten, or reclassified.
- 26 PRE ↔ 26 POST bijection is exact by stable `COMMENT_HASH` id.

## Acceptance Verdict

✅ **PASS** — 0 comments lost, 0 semantically changed. All 3 hash deltas are documented mechanical D-05 wrapper repairs; the author-comment clause in each is byte-identical.
