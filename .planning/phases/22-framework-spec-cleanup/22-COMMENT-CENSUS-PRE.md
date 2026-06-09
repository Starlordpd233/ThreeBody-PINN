---
phase: 22
slug: framework-spec-cleanup
artifact: comment-census-pre
status: committed
created: 2026-06-09
source_ref: faa73d0 (last commit before WS-A edits)
---

# Pre-WS-A Author Comment Census

**Source files:**
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` (blob: see source_ref)
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (blob: see source_ref)
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` (blob: see source_ref)

**Union count: 26** (13 ctl + 13 pinn + 0 sampling)

---

## ctl_instruction.md (13 comments)

### 1. multi-stage-data-stratification (line 107)
- **Form:** Author note
- **Section:** multi-stage-data-stratification-by-difficulty-revised-to-handle-the-issue-that-virial-ratio-is-not-preserved-for-quasi-random-ic-sampling
- **Snippet:** > **Author note:** I have a suggestion: how about we give the entire IC files a …
- **Verbatim text:** > **Author note:** I have a suggestion: how about we give the entire IC files a scan > using some algorithms and analyze the gathered data from there, to first > get an insight on what the data looks like, and then we can decide on > the criteria for each stage? This will be a good starting point > considering that simply designing the criteria based on theoretical > values might not be the best way to go espesically since my IC sampling > method is complicated -- virial ratio is not preserved for quasi-random > IC sampling.
- **text_hash:** 8b920ecad3a513403d49a2514d90b0bbca531b2f442bc66ebdeea8bb579deb48

COMMENT_HASH ctl_instruction::multi-stage-data-stratification-by-difficulty-revised-to-handle-the-issue-that-virial-ratio-is-not-preserved-for-quasi-random-ic-sampling::1 8b920ecad3a513403d49a2514d90b0bbca531b2f442bc66ebdeea8bb579deb48

### 2. phase-1-data-preparation (line 338)
- **Form:** Author Comment
- **Section:** phase-1-data-preparation-and-stratification
- **Snippet:** Author Comment: I believe this is another case for broken syntax or stale code f…
- **Verbatim text:** Author Comment: I believe this is another case for broken syntax or stale code from conversion. Also, this not estatement itself is outdated since all the code in the code folder is already outdated and unusuable.
- **text_hash:** da01bd121776ab4be31d8b772206e1e1566cd90c480ae81e7196ae320fe12a60

COMMENT_HASH ctl_instruction::phase-1-data-preparation-and-stratification::1 da01bd121776ab4be31d8b772206e1e1566cd90c480ae81e7196ae320fe12a60

### 3. 2-5-global-scaling (line 613)
- **Form:** Author Comment
- **Section:** 2-5-global-scaling
- **Snippet:** Author Comment: so far all the inline math notations that have this format `xxxx…
- **Verbatim text:** Author Comment: so far all the inline math notations that have this format `xxxx` are rendered as literal text strings in the preview and are not readable. Consider changing this syntax in a way that is machine-reading friendly and also renders correctly and nicely for human reader reading in preview.
- **text_hash:** 8a6de2944c0056149e52ef0c89421e878e8ba0f28479ee7302d2c059c1414cb8

COMMENT_HASH ctl_instruction::2-5-global-scaling::1 8a6de2944c0056149e52ef0c89421e878e8ba0f28479ee7302d2c059c1414cb8

### 4. outputs-of-this-step (line 701)
- **Form:** Author Comment
- **Section:** outputs-of-this-step
- **Snippet:** Author Comment: this section is a syntax disaster. ALl the raw latex syntax are …
- **Verbatim text:** Author Comment: this section is a syntax disaster. ALl the raw latex syntax are broken in rendered preview, and they show up as literal text strings. The other syntax are also incorrect for proper markdown file. Carefully look into this and think about how to fix it. Maintaining the exact, identifical math equation and expressions is of the utmost importance here. The following sections after this and below this should also be carefully examined.
- **text_hash:** 163eaafab275fbdbf1c97403428ab7d0b850764524234161238592b51b836c7f

COMMENT_HASH ctl_instruction::outputs-of-this-step::1 163eaafab275fbdbf1c97403428ab7d0b850764524234161238592b51b836c7f

### 5. outputs-of-this-step (line 894)
- **Form:** Author note
- **Section:** outputs-of-this-step
- **Snippet:** > **Author note:** We need the code snippets here for this.
- **Verbatim text:** > **Author note:** We need the code snippets here for this.
- **text_hash:** 73ee9823a5d3c65465fb5ba683a1c9a7763ffe71f268d858d08256e89c4f4aee

COMMENT_HASH ctl_instruction::outputs-of-this-step::2 73ee9823a5d3c65465fb5ba683a1c9a7763ffe71f268d858d08256e89c4f4aee

### 6. outputs-of-this-step (line 896)
- **Form:** Author note
- **Section:** outputs-of-this-step
- **Snippet:** > **Author note:** The two paragraphs below are suspicious. We need to carefully
- **Verbatim text:** > **Author note:** The two paragraphs below are suspicious. We need to carefully > examine them.
- **text_hash:** 2627d08f0081bb3d4d0ef8f8df19edaae1a4f7a56477f1e7ddf402072e6d9ea2

COMMENT_HASH ctl_instruction::outputs-of-this-step::3 2627d08f0081bb3d4d0ef8f8df19edaae1a4f7a56477f1e7ddf402072e6d9ea2

### 7. scope (line 940)
- **Form:** Author note + Historical author note
- **Section:** scope
- **Snippet:** > **Historical author note (pre-Phase 17; retained as a non-normative
- **Verbatim text:** > **Historical author note (pre-Phase 17; retained as a non-normative > question):** Confirm that all components in the IC vector are in the > range $[-1,1]$ and that it is the final form that will be fed to the > PINN.
- **text_hash:** 7c3d8f3737fb50c33cf492170c9f722837935461df8afacab0390e738fc09261

COMMENT_HASH ctl_instruction::scope::1 7c3d8f3737fb50c33cf492170c9f722837935461df8afacab0390e738fc09261

### 8. scope (line 985)
- **Form:** Author note + Historical author note
- **Section:** scope
- **Snippet:** > **Historical author note (pre-Phase 17; retained as a non-normative
- **Verbatim text:** > **Historical author note (pre-Phase 17; retained as a non-normative > question):** Confirm on this mathematcial guarantees' arguments and the > numerical implementation's purpose and validity. If confirmed, how > should we integrate and implement this into the existing workflow? > Also, we have to add the time t into this vector to achieve the > final 14-dimensional input vector ready to be fed to the PINN.
- **text_hash:** 0045d83b62889c268edef6b1fe51febf3f5ddb042cd676e9ef4a75779b78434a

COMMENT_HASH ctl_instruction::scope::2 0045d83b62889c268edef6b1fe51febf3f5ddb042cd676e9ef4a75779b78434a

### 9. network-input-contract (line 1051)
- **Form:** Author Comment
- **Section:** network-input-contract
- **Snippet:** Author Comment: again the syntax issues here above in the `` format are all brok…
- **Verbatim text:** Author Comment: again the syntax issues here above in the `` format are all broken and need fixing.
- **text_hash:** 8a01fd9387ba5a4a6905d76dde107f311880cbad419e5be309322ccc2cf85592

COMMENT_HASH ctl_instruction::network-input-contract::1 8a01fd9387ba5a4a6905d76dde107f311880cbad419e5be309322ccc2cf85592

### 10. phase-2-ctl-pinn-training-loop (line 1064)
- **Form:** Author note + Historical author note
- **Section:** phase-2-the-definitive-ctl-pinn-training-loop
- **Snippet:** > **Historical author note (pre-Phase 17; retained as a non-normative
- **Verbatim text:** > **Historical author note (pre-Phase 17; retained as a non-normative > question):** My biggest question now for this training loop is that: how are we > feeding the exact input vector and brutus simulation data into the > network? We need a very specific description that clearly tells me what > the input format is going to be. For example, right now I know that our > input vector is a 14th-dimentional input vector; but my question is that > since the brutus simulation data has a bunch of time series and time > snapshots, at each which there is a set of 3-body positions and > velocities, how are we handing the Brutus simulation data to this neural > network? Like how do we use the Brutus simulation data in this workflow? > and how do we input it together with the input vector? In which step? > After the network output a predicted trajectory do we just give it the > brutus ground-truth data and let it optimize based on that? This ties to > my bigger question that what is the network ultimately doing? Looking at > the PINN docment section 5.2 on "5.2 Output Layer and Kinematic > Consistency via Automatic Differentiation", is the ouptut file going to > be something similar to a brutus output file, sort of acting as a > replacement for the brutus algorithm?
- **text_hash:** b059fe94752976fb3ea293fe37e356079e9006677cd35b6afc2aa3610998c9c5

COMMENT_HASH ctl_instruction::phase-2-the-definitive-ctl-pinn-training-loop::1 b059fe94752976fb3ea293fe37e356079e9006677cd35b6afc2aa3610998c9c5

### 11. stage-transition-criteria (line 1248)
- **Form:** Author note
- **Section:** stage-transition-criteria
- **Snippet:** > **Author note:** Now, for this, we will need to look at how the first stage go…
- **Verbatim text:** > **Author note:** Now, for this, we will need to look at how the first stage goes > when the actual process starts. All of this transition creteria is > theoretical now, and it will heavily depend on what the actual situation > is like. Because I only have a limited amount of training data, maybe > not even enough, I would not expect the network to perform > extraodinarily well. All I have to see is that the network has the > potential to do something similar to a 3-body integrator and that it has > the potential to become better with more training data and optimization. > Based on this, how should we handle the stage transition criteria > depending on the actual situations that might happen? Should we first > test train stage 0 and see how it goes and then go from there?
- **text_hash:** 526c5fb81a29c56e04cf24f787d67e24e79cca59ebdbe51f1c034e13af6308f5

COMMENT_HASH ctl_instruction::stage-transition-criteria::1 526c5fb81a29c56e04cf24f787d67e24e79cca59ebdbe51f1c034e13af6308f5

### 12. evaluation-metrics-and-validation (line 1354)
- **Form:** Author note
- **Section:** evaluation-metrics-and-validation
- **Snippet:** > **Author note:** Should we also use the same definition here for the Lyapunov …
- **Verbatim text:** > **Author note:** Should we also use the same definition here for the Lyapunov time from section 2.3 'Necessary Calculations of Invariants'?
- **text_hash:** c40652716b0b963b54bad3873af181f3db1eb98576acd469539ca86d73bc4592

COMMENT_HASH ctl_instruction::evaluation-metrics-and-validation::1 c40652716b0b963b54bad3873af181f3db1eb98576acd469539ca86d73bc4592

### 13. reproducibility-note (line 1422)
- **Form:** Author Comment
- **Section:** reproducibility-note-ignore-now-and-come-back-later
- **Snippet:** - `stage.yaml` -- curriculum definition and data-set indices\ (Author Comment: w…
- **Verbatim text:** - `stage.yaml` -- curriculum definition and data-set indices\ (Author Comment: why is there a "\" sign here and in the next line?)
- **text_hash:** 4520ed07344a70b3237d2e97d7f3e5a75810f80158c83994663242461ccb54b3

COMMENT_HASH ctl_instruction::reproducibility-note-ignore-now-and-come-back-later::1 4520ed07344a70b3237d2e97d7f3e5a75810f80158c83994663242461ccb54b3

---

## pinn_architecture.md (13 comments)

### 1. 1-foundational-architectural-principles (line 103)
- **Form:** Author Comment
- **Section:** 1-foundational-architectural-principles-a-co-designed-approach-for-chaotic-systems
- **Snippet:** Author Comment: Again, all the superscript instances are rendered as raw literal…
- **Verbatim text:** Author Comment: Again, all the superscript instances are rendered as raw literal strings in the preview. Fix this carefully.
- **text_hash:** dfe0f412d957af30446590fabb18c887c0648994f497887645f83c9670af6ca1

COMMENT_HASH pinn_architecture::1-foundational-architectural-principles-a-co-designed-approach-for-chaotic-systems::1 dfe0f412d957af30446590fabb18c887c0648994f497887645f83c9670af6ca1

### 2. 2-2-principled-initialization (line 188)
- **Form:** Author Comment
- **Section:** 2-2-a-principled-initialization-scheme-for-siren-layers
- **Snippet:** Author Comment: All of these fields with `\text{xxx}` are not rnedered correctly…
- **Verbatim text:** Author Comment: All of these fields with `\text{xxx}` are not rnedered correctly and show up in the preview as raw literal text strings. The examples are the hidden omega 0, and first omega, etc.
- **text_hash:** 8d74449463fd26cca848bd9da336ee57262846643c8d9bd07473a4b57c4a21cb

COMMENT_HASH pinn_architecture::2-2-a-principled-initialization-scheme-for-siren-layers::1 8d74449463fd26cca848bd9da336ee57262846643c8d9bd07473a4b57c4a21cb

### 3. 2-4-finalized-architectural-hyperparameters (line 249)
- **Form:** Author Comment
- **Section:** 2-4-finalized-architectural-hyperparameters
- **Snippet:** Author Comment: I'm not sure why this section is formatted like this. It looks l…
- **Verbatim text:** Author Comment: I'm not sure why this section is formatted like this. It looks like broken syntax to me and it displays in the preview simply as a paragraph. Look into this.
- **text_hash:** bbbb389ff65b4f88e6fcef38f95ff99d6d7cd19e2394e35036d366e70c983520

COMMENT_HASH pinn_architecture::2-4-finalized-architectural-hyperparameters::1 bbbb389ff65b4f88e6fcef38f95ff99d6d7cd19e2394e35036d366e70c983520

### 4. 3-multi-component-loss (line 284)
- **Form:** Author Comment
- **Section:** 3-the-multi-component-physics-constrained-loss-function
- **Snippet:** Author Comment: the above formula is not written in the correct syntax. We need …
- **Verbatim text:** Author Comment: the above formula is not written in the correct syntax. We need to fix it so that it will be rendered correctly in markdown preview in Cursor.
- **text_hash:** 601905e2feecac9793c8dddd46849d85e858023a2384ff0b3a8fee6716be386c

COMMENT_HASH pinn_architecture::3-the-multi-component-physics-constrained-loss-function::1 601905e2feecac9793c8dddd46849d85e858023a2384ff0b3a8fee6716be386c

### 5. 3-multi-component-loss (line 288)
- **Form:** Author Comment
- **Section:** 3-the-multi-component-physics-constrained-loss-function
- **Snippet:** Author Comment: the above canonical text form is also rendered in raw text strin…
- **Verbatim text:** Author Comment: the above canonical text form is also rendered in raw text strings in preview.
- **text_hash:** 80062e903a56aa9f08cc63885a39d7fd59b8c8be52daae2c62f2dfc8992f4081

COMMENT_HASH pinn_architecture::3-the-multi-component-physics-constrained-loss-function::2 80062e903a56aa9f08cc63885a39d7fd59b8c8be52daae2c62f2dfc8992f4081

### 6. 3-1-data-fidelity-term (line 307)
- **Form:** Author Comment
- **Section:** 3-1-data-fidelity-term-mathcalltextdata-anchoring-to-ground-truth
- **Snippet:** Author Comment: again, the syntax is broken
- **Verbatim text:** Author Comment: again, the syntax is broken
- **text_hash:** 09323f6986e5b324a2031d961a426889f2101190df6e27a85e56185316ad2d28

COMMENT_HASH pinn_architecture::3-1-data-fidelity-term-mathcalltextdata-anchoring-to-ground-truth::1 09323f6986e5b324a2031d961a426889f2101190df6e27a85e56185316ad2d28

### 7. 3-1-data-fidelity-term (line 353)
- **Form:** Author Comment
- **Section:** 3-1-data-fidelity-term-mathcalltextdata-anchoring-to-ground-truth
- **Snippet:** **[Author Comment: This above batch construction is not consistent with the CTL …
- **Verbatim text:** **[Author Comment: This above batch construction is not consistent with the CTL instruction plan. Look into this.]**
- **text_hash:** 8b1fa20a28617841ed2b043f26e7df410ec1d21e2e32c57a28d48e7f8b98f533

COMMENT_HASH pinn_architecture::3-1-data-fidelity-term-mathcalltextdata-anchoring-to-ground-truth::2 8b1fa20a28617841ed2b043f26e7df410ec1d21e2e32c57a28d48e7f8b98f533

### 8. 3-4-soft-energy-conservation (line 536)
- **Form:** Author Comment
- **Section:** 3-4-soft-energy-conservation-regularizer-le-enforcing-a-global-conservation-law
- **Snippet:** $\epsilon_{train} = 10^{-5}$ (`10^-5`). (Author Comment: I am not sure why there…
- **Verbatim text:** $\epsilon_{train} = 10^{-5}$ (`10^-5`). (Author Comment: I am not sure why there is a duplicate 10^-5 here)Persist both $S_H$ and `epsilon_H` in training metadata. $S_H$ must be finite and strictly positive; $S_H <= 0$ or non-finite $S_H$ is a preprocessing/metadata validation failure. Do not apply a fallback numeric floor. Use `epsilon_H` only in $|H_0| + epsilon_H$. Phase 21 reports activation behavior only and must not reselect `epsilon_H` unless a new user instruction opens a replacement gap.
- **text_hash:** d52fb46ae588ded9c90a9313454fb82b3fd44e1bb0ab2903eb816767fac4a962

COMMENT_HASH pinn_architecture::3-4-soft-energy-conservation-regularizer-le-enforcing-a-global-conservation-law::1 d52fb46ae588ded9c90a9313454fb82b3fd44e1bb0ab2903eb816767fac4a962

### 9. 3-4-soft-energy-conservation (line 594)
- **Form:** Author Comment
- **Section:** 3-4-soft-energy-conservation-regularizer-le-enforcing-a-global-conservation-law
- **Snippet:** - **Softening Parameter:** The same value $\epsilon_{train} = 10^{-5}$ (`10^-5`)…
- **Verbatim text:** - **Softening Parameter:** The same value $\epsilon_{train} = 10^{-5}$ (`10^-5`) (author comment: again duplicate number) is used consistently in both the physics residual and energy calculations to prevent numerical instabilities during close encounters.
- **text_hash:** 465b94063376c82437d69f8684019dabe6a54d99555dc4664a949d088708ac2f

COMMENT_HASH pinn_architecture::3-4-soft-energy-conservation-regularizer-le-enforcing-a-global-conservation-law::2 465b94063376c82437d69f8684019dabe6a54d99555dc4664a949d088708ac2f

### 10. 4-2-optional-alm-ablation (line 676)
- **Form:** Author Comment
- **Section:** 4-2-optional-alm-ablation-p2
- **Snippet:** - **Constraints:** c_E = RMS_n(ΔH_n) (energy drift), c_{L,α} = RMS_n((L'_θ,α(u_n…
- **Verbatim text:** - **Constraints:** c_E = RMS_n(ΔH_n) (energy drift), c_{L,α} = RMS_n((L'_θ,α(u_n) - L_0,α') / L_scale) (angular momentum drift per component). (Author Comment: this syntax is not ideal since it invovles math equations/formula; it should properly use correct markdown render-friendly syntax)
- **text_hash:** d4948db1a221eca479600880018243b74a8327199613f9ff15eb5e7e0f136fae

COMMENT_HASH pinn_architecture::4-2-optional-alm-ablation-p2::1 d4948db1a221eca479600880018243b74a8327199613f9ff15eb5e7e0f136fae

### 11. si-pinn-002 (line 1017)
- **Form:** Author Comment
- **Section:** si-pinn-002-author-comments-preserved-in-converted-body
- **Snippet:** ### SI-PINN-002: Author comments preserved in converted body
- **Verbatim text:** ### SI-PINN-002: Author comments preserved in converted body
- **text_hash:** 8d2d2399e1edb974ac73b514b96fe239da416d0af688de985a94ae2baaca3aaf

COMMENT_HASH pinn_architecture::si-pinn-002-author-comments-preserved-in-converted-body::1 8d2d2399e1edb974ac73b514b96fe239da416d0af688de985a94ae2baaca3aaf

### 12. si-pinn-002 (line 1020)
- **Form:** Author Comment + \authcomment
- **Section:** si-pinn-002-author-comments-preserved-in-converted-body
- **Snippet:** - **Description:** 3 author comments from the LaTeX source (`\authcomment{}`) ar…
- **Verbatim text:** - **Description:** 3 author comments from the LaTeX source (`\authcomment{}`) are preserved in the converted body as bold bracketed text (`**[...]**`). These are editorial notes from the original authors, not content discrepancies: 1. "Need more detail on this dynamic scheduling for omega_0" (Section 2) 2. "Need confirmation on this hidden layer's detail" (Section 2) 3. "Comment: This above batch construction is not consistent with the CTL instruction plan" (Section 3)
- **text_hash:** 6a7655c3538e1e11ab1db4fafb6a97ec82ed389bea49db44614710b4394f5218

COMMENT_HASH pinn_architecture::si-pinn-002-author-comments-preserved-in-converted-body::2 6a7655c3538e1e11ab1db4fafb6a97ec82ed389bea49db44614710b4394f5218

### 13. si-pinn-003 (line 1029)
- **Form:** Author Comment
- **Section:** si-pinn-003-batch-construction-inconsistency-with-ctl-instruction-plan
- **Snippet:** - **Description:** The author comment "This above batch construction is not cons…
- **Verbatim text:** - **Description:** The author comment "This above batch construction is not consistent with the CTL instruction plan" flags a methodological inconsistency between the data sampling strategy described here and the CTL curriculum training plan. This should be investigated and resolved during training implementation.
- **text_hash:** 894e12714e35042a23d3c335a09d3852d7b2e7709bcaec94e6e7cc7ad83c900e

COMMENT_HASH pinn_architecture::si-pinn-003-batch-construction-inconsistency-with-ctl-instruction-plan::1 894e12714e35042a23d3c335a09d3852d7b2e7709bcaec94e6e7cc7ad83c900e

---

## sampling_method.md (0 comments)

Negative control confirmed: 0 author comments found.

---

## Summary

| File | Count |
|------|-------|
| ctl_instruction.md | 13 |
| pinn_architecture.md | 13 |
| sampling_method.md | 0 |
| **Union** | **26** |

**Source ref:** faa73d0 (pre-WS-A baseline)
**Generated:** 2026-06-09
**Method:** `node tools/spec-render-check/detect.mjs --census` over all 3 framework specs
