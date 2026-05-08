# A Data-Driven Stage Assignment Framework for Curriculum Transfer Learning in N-Body Dynamics

*An Award-Winning Writer*

## Contents

- [Part I: Foundational Principles of Data-Driven Curriculum Stratification for Physical Systems](#foundational-principles-of-data-driven-curriculum-stratification-for-physical-systems)
  - [The Rationale for Adaptive Curricula in Physics Simulations](#the-rationale-for-adaptive-curricula-in-physics-simulations)
  - [A Lexicon of Difficulty Metrics for the Three-Body Problem](#a-lexicon-of-difficulty-metrics-for-the-three-body-problem)
  - [Core Techniques for Data-Driven Stratification](#core-techniques-for-data-driven-stratification)
- [Part II: A Revised Algorithmic Workflow for Stage Stratification](#a-revised-algorithmic-workflow-for-stage-stratification)
  - [Phase I: Invariant Computation and Feature Engineering](#phase-i-invariant-computation-and-feature-engineering)
  - [Phase II: Exploratory Data Analysis (EDA) and Landscape Mapping](#phase-ii-exploratory-data-analysis-eda-and-landscape-mapping)
  - [Phase III: Deriving Adaptive Stage Criteria - A Hybrid Strategy](#phase-iii-deriving-adaptive-stage-criteria---a-hybrid-strategy)
  - [Phase IV: Final Stage Assignment and Population Balancing](#phase-iv-final-stage-assignment-and-population-balancing)
- [Part III: Implementation and Validation Protocol](#implementation-and-validation-protocol)
  - [Reference Implementation in Python](#reference-implementation-in-python)
  - [Advanced Architectural Considerations and Refinements](#advanced-architectural-considerations-and-refinements)
  - [A Protocol for Curriculum Validation](#a-protocol-for-curriculum-validation)
- [Part IV: Conclusions and Recommendations](#conclusions-and-recommendations)
- [References](#references)

## Abstract

This report presents a comprehensive, revised workflow for a data-driven curriculum stratification framework tailored to a Physics-Informed Neural Network (PINN) project for the three-body problem. The proposed methodology moves beyond static, heuristic-based criteria towards an adaptive system that derives its structure from the empirical properties of the simulation dataset itself. This approach, grounded in machine learning best practices, combines dimensionality reduction (PCA), unsupervised clustering (K-Means/GMM), and quantile-based binning to create a robust, interpretable, and effective curriculum. The report details a multi-phase algorithmic workflow, provides reference implementations, and outlines a protocol for empirical validation, aiming to improve training stability and final model accuracy for complex, chaotic dynamical systems.

# Foundational Principles of Data-Driven Curriculum Stratification for Physical Systems

The training of Physics-Informed Neural Networks (PINNs) on complex, chaotic dynamical systems represents a significant challenge at the intersection of scientific computing and machine learning. A key strategy for improving training stability and final model accuracy is Curriculum Learning (CL), where the model is exposed to training examples in a structured sequence, typically from "easy" to "hard".[1, 2] This report presents a comprehensive, revised workflow for a data-driven curriculum stratification framework tailored to a PINN project for the three-body problem. The proposed methodology moves beyond static, heuristic-based criteria, which have proven brittle, towards an adaptive system that derives its structure from the empirical properties of the simulation dataset itself. This approach is grounded in best practices from machine learning and is designed to be robust, interpretable, and directly implementable.

## The Rationale for Adaptive Curricula in Physics Simulations

The core premise of curriculum learning is to create a smooth "difficulty gradient" that guides the optimization process of a neural network towards a robust and generalizable solution.[3, 4] In the context of physics simulations, difficulty is often tied to the complexity of the underlying dynamics, such as the transition from regular, periodic motion to chaotic evolution. The initial approach for the CTL-PINN project, as detailed in the project documentation, relied on defining curriculum stages using fixed, theoretical thresholds on key physical invariants.[5] For instance, Stage 0 was defined by strict bounds on total energy ($E$), angular momentum ($L/L_{\text{max}}$), virial ratio ($Q$), and minimum particle separation ($s_{\text{min}}$) to isolate highly stable, hierarchical systems.[5]

While physically motivated, this static, heuristic-based approach possesses an inherent fragility: it presupposes that the training data will conform to idealized statistical distributions of these invariants. This assumption is frequently violated in practice, particularly when dealing with complex data generation processes. The project's use of Sobol-based quasi-random sampling for initial conditions (ICs) introduces a scaling factor, $s$, which systematically distorts the virial ratio, since $Q \propto 2T/|V|$ scales approximately as $s^3$.[5] Consequently, a large fraction of the quasi-random simulations, though potentially stable, fall outside the predefined $Q$ range (e.g., $[0.9, 1.1]$ for Stage 3), leading to underpopulated or even empty stages.[5] This mismatch between the curriculum's assumptions and the data's reality undermines the entire CL strategy, creating abrupt jumps in difficulty rather than a smooth progression.

This experience aligns with a broader consensus in machine learning research: "empirical adaptation to dataset statistics outperforms hand-crafted heuristics, especially in noisy or imbalanced data".[5] For PINNs applied to chaotic systems, this principle is especially pertinent. The "noise" is not merely measurement error but the intrinsic, high-frequency dynamics of chaos, and the "imbalance" is the often non-uniform distribution of stability across the phase space. Research on PINN training pathologies confirms that managing complexity is paramount for achieving convergence, with curriculum-based strategies being a primary tool for this purpose.[6, 7, 8] Papers on CL for PINNs advocate for approaches that progressively increase the difficulty, whether by sequencing the data samples or by gradually introducing more complex physical constraints.[4, 7]

This necessitates a paradigm shift. Instead of viewing the curriculum as a static, a priori set of rules, it should be conceptualized as a simplified, data-driven *model of the dataset's difficulty landscape*. A good curriculum, like any good model, must accurately represent the underlying data distribution, capturing its unique modes, skews, and correlations. A curriculum built on faulty assumptions is a mismatched model, leading to poor "predictions" about which data samples are genuinely easy or hard for the PINN to learn. Therefore, the design of the curriculum must be treated with the same analytical rigor as the design of the neural network itself. It requires a dedicated phase of exploratory data analysis (EDA), feature engineering (selection and transformation of physical invariants), model selection (e.g., choosing between clustering and quantile-based methods), and, ultimately, empirical validation. By adopting this data-driven philosophy, the curriculum becomes a robust and adaptive framework that is resilient to the specific artifacts of the data generation process, ensuring a smooth and effective learning path for the PINN.

## A Lexicon of Difficulty Metrics for the Three-Body Problem

To construct a data-driven curriculum, a set of quantitative features that correlate with learning difficulty is required. For the three-body problem, the conserved quantities and geometric properties of the system serve as excellent, physically interpretable difficulty metrics.[5] Each invariant provides a proxy for a specific aspect of dynamical complexity, forming a multi-dimensional feature space from which the curriculum can be constructed. The following metrics, computed from the initial state of each simulation, are foundational to the proposed framework.

**Total Mechanical Energy ($E$):** Defined as the sum of the system's kinetic ($T$) and potential ($V$) energies. $$E = T + V = \frac{1}{2}\sum_{i=1}^{3}m_{i}\lVert v_{i}'\rVert^{2} - \sum_{1\le i<j\le3}\frac{m_{i}m_{j}}{\lVert r_{i}'-r_{j}'\rVert+\epsilon}$$ In a system with gravitational constant $G=1$, a negative total energy ($E < 0$) indicates a gravitationally bound system. The more negative the value of $E$, the more tightly bound the system is, which often corresponds to more stable, regular orbits. Systems with energy close to zero ($E \approx 0$) are marginally bound or unbound and are susceptible to chaotic scattering, ejections, and fly-by encounters, which are significantly harder for a PINN to model accurately.[5]

**Virial Ratio ($Q$):** The ratio of twice the kinetic energy to the magnitude of the potential energy. $$Q = \frac{2T}{|V|}$$ For a stable, self-gravitating system in statistical equilibrium, the virial theorem states that $Q \approx 1$. A significant deviation from this value implies a state of disequilibrium. A system with $Q > 1$ has excess kinetic energy and will tend to expand, while a system with $Q < 1$ is dominated by potential energy and will tend to contract. Both scenarios often precede chaotic evolution, making $Q$ a key indicator of initial stability.[5]

**Normalized Angular Momentum ($L_{\text{norm}}$):** The magnitude of the total angular momentum vector, $L$, normalized by a characteristic maximum angular momentum, $L_{\text{max}}$. $$L_{\text{norm}} = \frac{\lVert L\rVert}{L_{\text{max}}} = \frac{\left\lVert\sum_{i=1}^{3}m_{i}(r_{i}'\times v_{i}')\right\rVert}{M_{\text{tot}}r_{\text{char}}v_{\text{char}}}$$ where $r_{\text{char}}$ is a characteristic length scale and $v_{\text{char}}$ is a characteristic velocity. A value of $L_{\text{norm}}$ close to 1 corresponds to near-circular orbits, which are highly regular and stable. Lower values indicate more eccentric (elongated) orbits, which lead to periodic close encounters between bodies, a primary driver of chaotic instabilities.[5]

**Minimum Initial Separation ($s_{\text{min}}$):** The smallest Euclidean distance between any pair of bodies in the initial configuration. $$s_{\text{min}} = \min_{1\le i<j\le3}\lVert r_{i}'-r_{j}'\rVert$$ This is a direct geometric indicator of the immediate risk of a close encounter. Very small values of $s_{\text{min}}$ signal impending strong gravitational interactions, which can lead to violent, unpredictable scattering events. These scenarios are among the most numerically challenging for both traditional integrators and PINNs.[5]

**Lyapunov Time ($\tau_L$):** The inverse of the largest Lyapunov exponent ($\lambda_{\text{max}}$), estimated from the simulated trajectory. $$\tau_{L} = \frac{1}{\lambda_{\text{max}}}$$ $\tau_{L}$ quantifies the timescale over which predictability is lost. It is the most direct measure of chaos in a dynamical system, representing the e-folding time for the exponential divergence of initially nearby trajectories. A short $\tau_{L}$ indicates strong chaos and high sensitivity to initial conditions, making long-term prediction fundamentally difficult. A long or infinite $\tau_{L}$ signifies regular, predictable motion.[5]

**Shape Invariants ($I_1, I_2, I_3$):** Dimensionless ratios of the three mutual distances between the bodies ($d_{\text{short}} \le d_{\text{mid}} \le d_{\text{long}}$). $$I_{1}=\frac{d_{\text{short}}}{d_{\text{long}}}, \quad I_{2}=\frac{d_{\text{mid}}}{d_{\text{long}}}, \quad I_{3}=\frac{d_{\text{short}}+d_{\text{mid}}-d_{\text{long}}}{d_{\text{short}}+d_{\text{mid}}+d_{\text{long}}}$$ These invariants describe the geometry of the initial configuration (e.g., collinear, isosceles, equilateral) independent of scale or orientation. Certain initial geometries are known to be more prone to chaotic evolution than others, making these invariants potentially useful secondary features for characterizing difficulty.[5]

These invariants form the feature vector for each simulation. By analyzing the statistical distributions and correlations of these features across the entire dataset, it is possible to construct a curriculum that is quantitatively grounded in the physics of the problem and empirically adapted to the data at hand.


| Invariant | Full Name | Role as a Difficulty Metric (Easy vs. Hard) |
|---|---|---|
| $E$ | Total Mechanical Energy | **Easy:** Large negative values (deeply bound). **Hard:** Values near zero. |
| $Q_{\text{norm}}$ | Normalized Virial Ratio | **Easy:** Values near 1 (virial equilibrium). **Hard:** Values far from 1. |
| $L_{\text{norm}}$ | Normalized Angular Momentum | **Easy:** Values near 1 (near-circular orbits). **Hard:** Low values. |
| $s_{\text{min}}$ | Minimum Initial Separation | **Easy:** Large values (well-separated). **Hard:** Small values. |
| $\tau_{L}$ | Lyapunov Time | **Easy:** Large or infinite values (regular). **Hard:** Small values (strong chaos). |

*Table: Physical Invariants and Their Interpretation as Difficulty Metrics*


## Core Techniques for Data-Driven Stratification

With a well-defined feature space of physical invariants, the next step is to select appropriate machine learning techniques to partition this space into curriculum stages. A hybrid approach combining dimensionality reduction, unsupervised clustering, and quantile-based binning provides a powerful and flexible toolkit for this task.

### Dimensionality Reduction with PCA for a Composite Stability Score

In the three-body problem, difficulty is a multi-faceted concept. A system can be challenging due to low angular momentum, near-zero energy, or a short Lyapunov time. These metrics are often strongly correlated; for example, a very tightly bound system (highly negative $E$) may evolve into chaos more quickly (short $\tau_L$).[5] Simply setting independent thresholds on each metric can lead to conflicting or redundant criteria.

Principal Component Analysis (PCA) offers a principled method to address this. PCA is an orthogonal linear transformation that projects the data onto a new coordinate system, where the axes (principal components, PCs) are ordered by the amount of variance they explain in the original data.[9, 10] The first principal component (PC1) represents the direction of maximum variance in the feature space. In the context of our physical invariants, this component can often be interpreted as a composite "stability" or "difficulty" score.[5]

For instance, if PC1 is found to be a linear combination with positive weights on $L_{\text{norm}}$ and $\tau_L$ and a negative weight on $|E|$, then a high score on PC1 would correspond to a system that is simultaneously regular, predictable, and not excessively bound---a clear signature of stability. By ranking simulations based on their PC1 score, one can create a continuous, one-dimensional difficulty axis that optimally combines the information from multiple correlated invariants. This data-driven approach is superior to manually constructing a composite score (e.g., $-E + L_{\text{norm}}$ [5]), as the weights are derived directly from the dataset's covariance structure, ensuring they are optimally tailored to the specific data distribution.[11, 12]

### Unsupervised Clustering for Discovering Dynamical Regimes

While PCA and quantile binning are excellent for ordering data along a continuous difficulty axis, they may not capture the full picture. Difficulty is not always just a matter of degree; it can also be a matter of kind. Unsupervised clustering algorithms, such as K-Means or Gaussian Mixture Models (GMM), partition the dataset into distinct groups based on similarity in the multi-dimensional feature space. This allows for the automatic discovery of different *dynamical regimes* or *phenomenological classes* of simulations.[5]

Consider two simulations that have the same short Lyapunov time, $\tau_L$. From a purely quantile-based perspective, they are equally difficult. However, their underlying dynamics could be completely different. One might be a "prompt ejection" event, where one body is quickly flung out of the system. The other might be a long-lived, complex "resonant encounter," where the bodies undergo multiple close approaches before settling into a new configuration. For a PINN, these two scenarios present qualitatively different challenges. The prompt ejection involves large velocities and an unbound trajectory, while the resonant encounter involves intricate, repeated interactions in a compact region of space.

A simple easy-to-hard curriculum might mix these two types of chaos, potentially confusing the learning process. Clustering in the full feature space (e.g., using $E, L_{\text{norm}}, s_{\text{min}}, \tau_L$) can distinguish between them. It might naturally group all prompt ejections into one cluster (characterized, perhaps, by $E \approx 0$ and high final velocities) and all resonant encounters into another (characterized by small $s_{\text{min}}$ and oscillating inter-particle distances). This reveals that the difficulty landscape is not a simple line but a structured space with distinct regions.

This allows for the design of a more sophisticated curriculum that introduces not just progressively harder simulations, but also qualitatively different types of physical phenomena stage by stage. For example, after learning stable orbits, the PINN could be trained specifically on the "prompt ejection" cluster, then on the "resonant encounter" cluster. This aligns with research suggesting that clustering can reveal "latent difficulty gradients" that hand-picked thresholds might overlook.[5, 13] K-Means is an efficient baseline for this task, while GMMs offer more flexibility by modeling non-spherical clusters and providing probabilistic assignments, which can be invaluable for identifying outliers or creating "soft" curriculum boundaries.[5, 14]

### Quantile-Based Binning for Robust and Balanced Pacing

Quantile-based binning is a non-parametric method that divides a ranked dataset into a predetermined number of continuous intervals ("bins"), each holding the same number of data points.[15] For example, quartiles divide the data into four bins, each containing 25% of the samples.

This technique is exceptionally robust and serves as a cornerstone of the adaptive curriculum. Its primary advantage is that it makes no assumptions about the underlying distribution of the difficulty metric. This is critical for the CTL-PINN project, where metrics like the raw virial ratio $Q$ have a distorted distribution and the Lyapunov time $\tau_L$ likely has a heavy tail corresponding to highly chaotic events.[5]

Using fixed thresholds (e.g., "$\tau_L < 2$") is risky; if the data distribution is skewed, such a rule might select 50% of the data or only 1%. In contrast, a quantile-based rule like "select the bottom 25% of simulations by $\tau_L$" guarantees that the resulting stage will contain exactly one-quarter of the samples it is applied to. This provides two key benefits:

1.  **Avoids Empty Stages:** It ensures that every defined stage will be populated with a predictable number of samples, preventing the issue of empty stages that plagued the original fixed-threshold design.[5]

2.  **Ensures Smooth Pacing:** It provides a balanced progression of difficulty. By dividing the chaotic systems into, for example, four equally sized quantile bins, the curriculum ensures the PINN is not suddenly overwhelmed by a disproportionately large number of difficult examples at a single transition. This smooth pacing is essential for stable training.[16]

This technique is a well-established best practice in curriculum learning for regression and simulation tasks, as it automatically adapts the stage boundaries to the empirical distribution of the data, ensuring a well-proportioned and steadily advancing curriculum.[5]

# A Revised Algorithmic Workflow for Stage Stratification

This section details a multi-phase, algorithmic workflow for implementing the data-driven curriculum. The process is designed to be systematic and reproducible, transforming the raw simulation outputs into a final, robust stage assignment for every trajectory in the dataset. The workflow is divided into four phases: (I) Invariant Computation and Feature Engineering, (II) Exploratory Data Analysis, (III) Derivation of Adaptive Stage Criteria, and (IV) Final Stage Assignment and Balancing.

## Phase I: Invariant Computation and Feature Engineering

The foundation of the data-driven curriculum is a comprehensive and accurate feature set. This phase focuses on processing the raw simulation data to compute the physical invariants discussed in Part 1 and correcting for any known sampling artifacts.

### Pre-computation and Data Loading

This initial step leverages the project's existing data processing pipeline. It involves executing the established Python scripts to perform the following actions for every simulation in the dataset:

1.  **Parse Raw Data:** Read the initial condition files (`ic_*.txt`) and the corresponding Brutus N-body integrator output files (`brutus_*.txt`).[5]

2.  **Center-of-Mass (COM) Transformation:** Verify and, if necessary, transform the initial conditions to the COM frame, ensuring zero total momentum. This is a critical prerequisite for consistent physical calculations, especially since the 'hierarchical' ICs may not initially be in the COM frame.[5]

3.  **Scaling to Dimensionless Units:** Apply the global characteristic scales for length, time, and velocity to convert all physical quantities into a consistent, dimensionless system where $G=1$. This is essential for numerical stability and for ensuring the PINN inputs are on a comparable scale.[5]

The output of this step is a clean, standardized set of initial conditions (masses, positions, velocities) for every simulation.

### Invariant Calculation

For each standardized initial condition, a dedicated function should compute the full suite of physical invariants defined in Section 1.2. This includes: Total Mechanical Energy ($E$), Raw Virial Ratio ($Q_{\text{raw}}$), Normalized Angular Momentum ($L_{\text{norm}}$), Minimum Initial Separation ($s_{\text{min}}$), Shape Invariants ($I_1, I_2, I_3$), and Lyapunov Time ($\tau_L$), estimated from the corresponding Brutus trajectory data using the Rosenstein-style estimator detailed in the project documentation.[5]

### Correcting for Sampling Artifacts: The Normalized Virial Ratio

A critical issue identified in the project is the distortion of the virial ratio for quasi-random ICs due to the Sobol sampling scale factor, $s$.[5] To address this, a normalized virial ratio, $Q_{\text{norm}}$, must be computed to place all simulations on a comparable footing.

The transformation is based on the physical scaling of the kinetic and potential energies. Since kinetic energy $T \propto v^2$ and potential energy $V \propto 1/r$, and the sampling scales positions as $r \to sr$ and velocities as $v \to sv$, the virial ratio scales as: $$Q \propto \frac{T}{|V|} \propto \frac{(sv)^2}{1/(sr)} = s^3 \frac{v^2}{1/r}$$ Therefore, to recover a scale-invariant measure of virial equilibrium, the raw virial ratio must be divided by $s^3$. The normalized virial ratio is defined as: $$Q_{\text{norm}} = \frac{Q_{\text{raw}}}{s^3}$$ This calculation should be applied to all simulations of type 'quasi-random'. For 'hierarchical' simulations, it can be assumed that $s=1$, so $Q_{\text{norm}} = Q_{\text{raw}}$.

**Contingency Plan:** If the scale factor $s$ is not explicitly stored with each IC, it must be recorded during the IC generation or estimated post-hoc. As suggested in the project analysis, one method is to estimate it by comparing the median momentum of the scaled sample to a baseline unscaled sample.[5] Without this correction, the virial ratio is not a reliable metric for the quasi-random set and should be excluded from the analysis for those simulations.

### Assembling the Invariant Feature DataFrame

The final step of this phase is to consolidate all computed information into a single, master `pandas.DataFrame`. This DataFrame will be the central data structure for all subsequent analysis and serves as a persistent, intermediate representation of the dataset's physical properties.

| sim_id | ic_type | s_factor | E | Q_raw | Q_norm | L_norm | s_min | tau_L | I1 | I2 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0001 | hierarchical | 1.0 | -2.5 | 1.01 | 1.01 | 0.95 | 3.1 | 1000.0 | 0.8 | 0.9 |
| 5001 | quasi-random | 1.2 | -0.8 | 1.75 | 1.01 | 0.45 | 1.5 | 12.3 | 0.3 | 0.7 |

*Table 2: Recommended structure for the Invariant Feature DataFrame.*

This DataFrame provides a complete, queryable summary of the entire dataset, enabling the powerful exploratory and algorithmic techniques described in the following phases.

## Phase II: Exploratory Data Analysis (EDA) and Landscape Mapping

Before defining the final curriculum stages, it is essential to perform a thorough exploratory data analysis (EDA). The goal of this phase is to build a strong intuition for the structure of the data, validate the physical assumptions, and identify the key relationships that will guide the stratification strategy. This process transforms the numerical data in the invariant DataFrame into actionable visual insights.

### Stratified Distribution Analysis

The first step is to understand the distribution of each key difficulty metric. This is achieved by generating histograms and, for a smoother representation, Kernel Density Estimate (KDE) plots for the primary invariants: $E$, $Q_{\text{norm}}$, $L_{\text{norm}}$, and $\tau_L$.

Crucially, these visualizations must be **stratified by `ic_type`**. Plotting the distributions for 'hierarchical' and 'quasi-random' systems separately (or overlaid with different colors) is expected to reveal fundamental differences between the two datasets.[5]

### Correlation Analysis

Next, the relationships *between* the different difficulty metrics must be investigated. A Pearson correlation matrix, visualized as a heatmap, is the standard tool for this analysis. Again, this should be performed separately for the 'hierarchical' and 'quasi-random' subsets.

### Low-Dimensional Visualization

To gain a more holistic view of the difficulty landscape, it is useful to visualize the data in a low-dimensional space.

- **Pair Plots:** A `seaborn.pairplot` can be used to show all pairwise scatter plots between the key invariants, with points colored by `ic_type`.

- **PCA Projection:** A powerful visualization technique is to perform a preliminary PCA on the standardized invariants and create a 2D scatter plot of the first two principal components (PC1 vs. PC2). The points on this plot can be colored by a key chaos indicator, such as $\tau_L$ or its inverse, $\lambda_{\text{max}}$.

This EDA phase is not merely a formality; it is a crucial step that ensures the subsequent algorithmic choices are grounded in the empirical reality of the data, not just in theoretical assumptions.

## Phase III: Deriving Adaptive Stage Criteria - A Hybrid Strategy

With a deep understanding of the data's structure from the EDA phase, the next step is to derive the specific rules for stage assignment. The guiding principle of the revised framework is to use a hybrid strategy tailored to the distinct physical nature of the two sub-datasets.


| Aspect | Original Fixed-Threshold Framework | Proposed Data-Driven Framework |
|--------|-----------------------------------|-------------------------------|
| **Thresholds** | Static, hard-coded values based on theory (e.g., $Q<1.3$, $\tau_L>5$).[5] | Adaptive, derived from data statistics (e.g., quantiles, cluster centroids).[5] |
| **Stage Population** | Prone to severe imbalance or empty stages if data distribution mismatches theory.[5] | Balanced by design through quantile binning and population checks, ensuring smooth pacing.[5] |
| **Robustness** | Brittle; fails when data generation artifacts (e.g., scaling) violate assumptions.[5] | Robust; automatically adapts to the dataset's empirical distribution, including skews and artifacts.[5] |
| **Difficulty Ordering** | Assumes a simple, monotonic difficulty gradient that may not hold in multi-dimensional feature space. | Discovers natural difficulty gradients and qualitatively distinct regimes via PCA and clustering.[5, 13] |
| **Interpretability** | High, as criteria are based on physical theory. | High, as data-driven clusters and quantiles are interpreted and labeled by their physical properties (e.g., mean $\tau_L$). |

*Table 3: Comparison of Original vs. Proposed Data-Driven Curriculum Framework*


### Stratifying the Stable Subset (Hierarchical ICs): Stages 0 and 1

The 'hierarchical' dataset consists entirely of dynamically stable systems. The goal here is not to separate stable from chaotic, but to rank the systems by their *degree* of stability and regularity. A simple, physically interpretable approach using quantile-based thresholds is most appropriate.

### Stratifying the Complex Subset (Quasi-Random ICs): Stages 2-6

The 'quasi-random' dataset is far more heterogeneous. A more powerful, multi-step strategy is required to properly parse this complexity. This involves a pipeline of feature preparation, dimensionality reduction with PCA, and regime discovery with unsupervised clustering. The algorithm involves:

1.  **Feature Preparation:** Select features $[E, Q_{\text{norm}}, L_{\text{norm}}, s_{\text{min}}, 1/\tau_L]$. Use the inverse Lyapunov time, $\lambda_{\text{max}} = 1/\tau_L$, to handle regular orbits where $\tau_L \to \infty$. Standardize all features.

2.  **Dimensionality Reduction with PCA:** Apply PCA to the standardized features to create a composite, low-dimensional representation.

3.  **Discovering Regimes with Clustering:** Apply K-Means (or GMM) to the principal component scores. The number of clusters, $k$, can be set to 5 (for Stages 2-6) or determined using heuristics like the elbow method.

4.  **Ordering Clusters by a Chaos Proxy:** Sort the discovered clusters by their median $\tau_L$ in descending order. The cluster with the highest median $\tau_L$ is the least chaotic and will form the earliest stage in this block.

## Phase IV: Final Stage Assignment and Population Balancing

The final phase translates the derived criteria into a definitive assignment of a stage label to every simulation.

### The Definitive Assignment Algorithm

The final stage assignment rules are summarized in Table 4.

### Population Control and Stage Merging

After the initial assignment, it is imperative to check the population of each stage. If any stage falls below a minimum population threshold (e.g., 5% of the total dataset), it should be merged with its most similar adjacent stage to ensure the curriculum has a sensible "pacing".


| Stage | Primary Data Source | Stratification Method | Specific Data-Driven Criteria | Expected Physical Characteristics |
|---|---|---|---|---|
| **0** | Hierarchical | Quantile Binning | $E$ in bottom quartile & $L_{\text{norm}}$ in top quartile. | Deeply bound, near-circular, highly regular orbits. |
| **1** | Hierarchical | Remainder | All other hierarchical systems. | Stable, bound, regular orbits, but less constrained. |
| **2** | Quasi-Random | PCA + Clustering | Members of the cluster with the highest median $\tau_L$. | Most stable of the chaotic set; long-term regular motion. |
| **3** | Quasi-Random | PCA + Clustering | Members of the cluster with the 2nd highest median $\tau_L$. | Onset of chaos; mildly chaotic systems. |
| **4** | Quasi-Random | PCA + Clustering | Members of the cluster with the 3rd highest median $\tau_L$. | Moderately chaotic systems, possibly resonant. |
| **5** | Quasi-Random | PCA + Clustering | Members of the cluster with the 4th highest median $\tau_L$. | Strongly chaotic systems with short predictability. |
| **6** | Quasi-Random | PCA + Clustering + Outlier | Most chaotic cluster (lowest median $\tau_L$) + outliers. | Violent, unpredictable dynamics; ejections, unbound systems. |

*Table 4: Final Proposed Stage Definitions and Data-Driven Criteria*



# Implementation and Validation Protocol

This part provides the practical tools and procedures required to execute the proposed workflow and validate its effectiveness.

## Reference Implementation in Python

The following Python code provides a reference implementation for the core functions of the stratification workflow.

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

def compute_invariants(raw_data_path: str, simulation_files: list) -> pd.DataFrame:
    """
    Parses raw data, computes all physical invariants, and returns a master DataFrame.
    This function is a placeholder for the user's existing pipeline for steps 2.1.1-2.1.4.
    """
    # For demonstration, we'll create a dummy DataFrame.
    num_samples = 15000
    data = {
        'sim_id': range(num_samples),
        'ic_type': np.random.choice(['hierarchical', 'quasi-random'], num_samples, p=[0.4, 0.6]),
        'E': np.random.randn(num_samples) * 2 - 1,
        'Q_norm': np.random.randn(num_samples) * 0.2 + 1,
        'L_norm': np.random.rand(num_samples),
        's_min': np.random.rand(num_samples) * 5,
        'tau_L': np.random.exponential(scale=10, size=num_samples)
    }
    df = pd.DataFrame(data)
    # Make hierarchical more stable for realism
    hier_mask = df['ic_type'] == 'hierarchical'
    df.loc[hier_mask, 'tau_L'] = np.random.exponential(scale=500, size=hier_mask.sum()) + 100
    df.loc[hier_mask, 'L_norm'] = np.random.uniform(0.7, 1.0, size=hier_mask.sum())
    df.loc[hier_mask, 'E'] = np.random.uniform(-5, -1, size=hier_mask.sum())
    return df

def perform_eda(invariant_df: pd.DataFrame):
    """
    Generates and saves key EDA plots for landscape mapping.
    """
    print("--- Performing Exploratory Data Analysis ---")
    #... (Plotting code as in original report)...
    print("EDA plots saved.")

def derive_adaptive_criteria(quasi_random_df: pd.DataFrame, k: int = 5) -> dict:
    """
    Implements the PCA -> Cluster -> Sort pipeline for the quasi-random dataset.
    """
    print(f"--- Deriving Adaptive Criteria for Quasi-Random Data (k={k}) ---")
    features = ['E', 'Q_norm', 'L_norm', 's_min', 'tau_L']
    df_for_clustering = quasi_random_df[features].copy()
    df_for_clustering['lambda_max'] = 1.0 / df_for_clustering['tau_L']
    df_for_clustering.replace([np.inf, -np.inf], 0, inplace=True)
    
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_for_clustering[['E', 'Q_norm', 'L_norm', 's_min', 'lambda_max']])
    
    pca = PCA(n_components=0.9)
    pcs = pca.fit_transform(scaled_features)
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(pcs)
    
    temp_df = quasi_random_df.copy()
    temp_df['cluster'] = cluster_labels
    cluster_median_tau_L = temp_df.groupby('cluster')['tau_L'].median()
    sorted_clusters = cluster_median_tau_L.sort_values(ascending=False).index.tolist()
    
    return {
        'kmeans_model': kmeans, 'pca_model': pca, 'scaler': scaler,
        'sorted_cluster_labels': sorted_clusters, 'cluster_assignments': cluster_labels
    }

def assign_stages(invariant_df: pd.DataFrame, k_clusters: int = 5, min_stage_pop_frac: float = 0.05) -> pd.DataFrame:
    """
    Assigns a final stage label to each simulation based on the hybrid strategy.
    """
    df = invariant_df.copy()
    df['stage'] = -1
    
    # Stratify Hierarchical Data (Stages 0, 1)
    hier_mask = df['ic_type'] == 'hierarchical'
    hier_df = df[hier_mask]
    e_q25 = hier_df['E'].quantile(0.25)
    l_q75 = hier_df['L_norm'].quantile(0.75)
    stage0_mask = hier_mask & (df['E'] <= e_q25) & (df['L_norm'] >= l_q75)
    df.loc[stage0_mask, 'stage'] = 0
    df.loc[hier_mask & (df['stage'] == -1), 'stage'] = 1

    # Stratify Quasi-Random Data (Stages 2-6)
    qr_mask = df['ic_type'] == 'quasi-random'
    qr_df = df[qr_mask]
    criteria = derive_adaptive_criteria(qr_df, k=k_clusters)
    sorted_labels = criteria['sorted_cluster_labels']
    cluster_map = {label: i for i, label in enumerate(sorted_labels)}
    
    for original_label, stage_offset in cluster_map.items():
        cluster_mask = qr_df.index[criteria['cluster_assignments'] == original_label]
        df.loc[cluster_mask, 'stage'] = stage_offset + 2

    # Add extreme outliers to Stage 6
    s_min_q1 = df['s_min'].quantile(0.01)
    extreme_outlier_mask = qr_mask & ((df['s_min'] <= s_min_q1) | (df['E'] > 0))
    df.loc[extreme_outlier_mask, 'stage'] = 6
    
    # Population Balancing
    #... (Merging logic as in original report)...
    
    # Re-label stages to be contiguous
    unique_stages = sorted(df['stage'].unique())
    stage_relabel_map = {old_label: new_label for new_label, old_label in enumerate(unique_stages)}
    df['stage'] = df['stage'].map(stage_relabel_map)
    
    print("\n--- Final Stage Populations ---")
    print(df['stage'].value_counts().sort_index())
    return df
```

## Advanced Architectural Considerations and Refinements

While the proposed workflow is robust, several refinements can enhance its performance and interpretability, such as using Gaussian Mixture Models (GMM) for more flexible clustering, performing feature selection to reduce noise, and using shape invariants for secondary analysis to improve physical interpretation.

## A Protocol for Curriculum Validation

The development of the curriculum does not end with the assignment of stage labels. Its effectiveness must be empirically validated.[5] The ultimate goal is to ensure a smooth difficulty gradient for the PINN, leading to stable and efficient training.

1.  **Implement the New Curriculum:** Generate and save stage labels for the dataset.

2.  **Create a Hold-out Validation Set:** Partition the data, ensuring the validation set is stratified across all curriculum stages.

3.  **Prototype Training Run:** Train a prototype of the CTL-PINN model following the full curriculum protocol.

4.  **Monitor Stage-wise Performance:** At the end of training for each stage $k$, evaluate the model's loss (e.g., $\mathcal{L}_{\text{data}}$) on the validation samples belonging to each stage.

5.  **Analyze the Transition Dynamics:** Plot the validation loss for each stage's data as a function of the training epochs.

6.  **Success Criterion:** The curriculum is successful if training proceeds without catastrophic spikes in validation loss upon stage transitions. A manageable increase in loss on newly introduced data, followed by a steady decrease, indicates a well-paced difficulty jump.

# Conclusions and Recommendations

The analysis presented in this report confirms that the initial fixed-threshold curriculum framework is ill-suited to the empirical realities of the generated dataset. The proposed solution is a complete overhaul of the stage assignment methodology, replacing the static framework with a robust, adaptive, and data-driven workflow.

**The core recommendations are as follows:**

1.  **Adopt a Hybrid, Data-Driven Stratification Strategy:** Use quantile-based binning for the stable subset and a PCA-plus-clustering approach for the complex subset.

2.  **Implement the Four-Phase Algorithmic Workflow:** Follow the systematic process from invariant computation to final stage assignment and balancing.

3.  **Prioritize Physical Interpretability:** Maintain the link to physics by using meaningful invariants and analyzing the physical characteristics of discovered clusters.

4.  **Embrace Iterative Validation:** Empirically validate the curriculum's effectiveness by monitoring the PINN's training dynamics and be prepared to refine the curriculum based on this feedback.

By implementing this comprehensive framework, the CTL-PINN project can overcome the critical bottleneck of stage assignment, ensuring a smoother learning progression and ultimately providing a much stronger foundation for training a PINN to accurately model the complex and chaotic dynamics of the three-body problem.

## References

1. Curriculum learning for data-driven modeling of dynamical systems, accessed August 1, 2025, <https://arxiv.org/pdf/2112.08458>
2. [2411.00973] Does the Definition of Difficulty Matter? Scoring Functions and their Role for Curriculum Learning - arXiv, accessed August 1, 2025, <https://arxiv.org/abs/2411.00973>
3. Data Parameters: A New Family of Parameters for Learning a Differentiable Curriculum - NIPS, accessed August 1, 2025, <http://papers.neurips.cc/paper/9289-data-parameters-a-new-family-of-parameters-for-learning-a-differentiable-curriculum.pdf>
4. physics-informed neural networks with curriculum training for poroelastic flow and deformation - NGM2024, accessed August 1, 2025, <https://www.ngm2024.se/Papers/bekele_ngm2024_paper_final.pdf>
5. stage-assignment-issue.txt
6. [2404.13909] Physics-informed neural networks with curriculum training for poroelastic flow and deformation processes - arXiv, accessed August 1, 2025, <https://arxiv.org/abs/2404.13909>
7. Dynamic Curriculum Regularization for Enhanced Training of..., accessed August 1, 2025, <https://ml4physicalsciences.github.io/2024/files/NeurIPS_ML4PS_2024_109.pdf>
8. Characterizing possible failure modes in physics-informed neural networks - OpenReview, accessed August 1, 2025, <https://openreview.net/forum?id=a2Gr9gNFD-J>
9. Principal component analysis - Wikipedia, accessed August 1, 2025, <https://en.wikipedia.org/wiki/Principal_component_analysis>
10. Principal component analysis: a review and recent developments | Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences, accessed August 1, 2025, <https://royalsocietypublishing.org/doi/10.1098/rsta.2015.0202>
11. Principal component analysis: a review and recent developments - PMC - PubMed Central, accessed August 1, 2025, <https://pmc.ncbi.nlm.nih.gov/articles/PMC4792409/>
12. Composite score analysis for unsupervised comparison and network visualization of metabolomics data - PMC, accessed August 1, 2025, <https://pmc.ncbi.nlm.nih.gov/articles/PMC6948848/>
13. Unsupervised Deep Embedding for Clustering Analysis - Proceedings of Machine Learning Research, accessed August 1, 2025, <https://proceedings.mlr.press/v48/xieb16.pdf>
14. Feature Selection for Unsupervised Learning, accessed August 1, 2025, <https://www.jmlr.org/papers/volume5/dy04a/dy04a.pdf>
15. Simulation-Based Inference with Quantile Regression - arXiv, accessed August 1, 2025, <https://arxiv.org/pdf/2401.02413>
16. Quantile Regression Estimands and Models: Revisiting the Motherhood Wage Penalty Debate - OSF, accessed August 1, 2025, <https://osf.io/9avrp/download>

