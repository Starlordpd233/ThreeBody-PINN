# Content Completeness Verification Report

**Generated:** 2026-03-21 12:42:12

**Structures verified:** 5


## Summary

| Structure | Status | Original Lines | Modular Lines |
|-----------|--------|----------------|---------------|
| Data-quality-assessment | FAIL | 398 | 390 |
| ctl-instruction | FAIL | 1616 | 1615 |
| pinn-architecture | FAIL | 856 | 627 |
| review_of_framework | FAIL | 533 | 536 |
| stage_strat_revision | FAIL | 497 | 493 |


## Detailed Results


### Data-quality-assessment

```
--- Data-quality-assessment/original
+++ Data-quality-assessment/modular
@@ -28,7 +28,6 @@
 \date{\today}
 
 
-
 \section{Introduction: The Intersection of Arbitrary-Precision Numerics and Causal Deep Learning}
 
 The integration of high-fidelity numerical analysis with deep learning represents a paradigm shift in the study of chaotic dynamical systems. The specific research stack under analysis—comprising the Brutus arbitrary-precision integrator written in C++, a Python-based data processing pipeline, and a Causal Training Labeled Physics-Informed Neural Network (CTL-PINN)—targets one of the most enduring challenges in classical mechanics: the Three-Body Problem. This system is characterized by non-linear interactions, extreme sensitivity to initial conditions, and phase space structures defined by the coexistence of stable invariant tori and chaotic seas. The successful modeling of such a system using neural networks requires a rigorous reassessment of what constitutes ``high-quality'' training data. Unlike traditional supervised learning tasks where data quality is often synonymous with label accuracy or noise reduction, the chaotic N-body problem imposes strict geometric and dynamical constraints—specifically symplectic conservation and phase space continuity—that must be preserved to ensure the learned model is physically viable.
@@ -54,7 +53,6 @@
 where the weights $w_i$ are dynamically adjusted based on the cumulative loss at previous time steps. Typically, $w_i \propto \exp(-\lambda \sum_{j < i} \mathcal{L}_j)$~\cite{ref10}. This forces the network to learn the trajectory sequentially, respecting the arrow of time.
 
 This architectural choice imposes strict requirements on the training data. The data must be \textit{causally continuous}. A gap in the data, a region of unphysical noise, or a ``stiffness spike'' (an under-resolved close encounter) at $t_{early}$ will result in a high residual $\mathcal{L}_{early}$. The causal weighting mechanism will then suppress the weights for all $t > t_{early}$ to zero, effectively halting the training process~\cite{ref10}. Thus, for CTL-PINNs, data quality is not just about global accuracy; it is about the \textit{continuity of learnability} along the temporal axis. A single ``bad'' segment renders the entire subsequent trajectory useless for training.
-
 \section{Assessment Strategy: Trade-offs Between Pre-Training Validation and Trial Training}
 
 The central strategic question is how to validate this complex data. The research identifies two primary methodologies: Static Pre-Training Validation (analyzing the dataset $\mathcal{D}$ itself) and Dynamic Trial Training (analyzing the interaction between $\mathcal{D}$ and the model $M$). Relying solely on one introduces significant risks.
@@ -129,7 +127,6 @@
 \textbf{Blind Spot} & Neural Network Inductive Bias & Physical Validity of Minima & None \\ \bottomrule
 \end{tabular}
 \end{table}
-
 \section{Mathematically Grounded Metrics for Data Quality}
 
 To operationalize the Staged Gate Protocol, we must define specific metrics. These metrics extend beyond simple error checking; they quantify the \textit{fitness} of the data for the specific task of causal physics-informed learning.
@@ -216,7 +213,6 @@
     \item \textbf{High Entropy:} The data explores diverse configurations.
     \item \textbf{Stiffness Coverage Ratio:} Specifically check the bin corresponding to $r_{min} \to 0$. If this bin is empty, the dataset lacks the ``hard'' physics examples necessary to train the network to handle singularities. The report recommends ``Importance Sampling'' to enrich the dataset with these high-stiffness events~\cite{ref9}.
 \end{itemize}
-
 \section{Risks to Model Parameters and Causal Training Dynamics}
 
 The user query specifically asks to address ``risks to model parameters.'' In the context of CTL-PINNs and chaotic data, these risks are non-trivial and often structural.
@@ -247,7 +243,6 @@
     \item[Parameter Consequence:] The weights responsible for high-frequency features will not converge within standard training times.
     \item[Mitigation:] Use the IPR metric to detect high-frequency content. If detected, the architecture should be augmented with Fourier Feature mappings (positional encoding) to shift the spectral bias of the network~\cite{ref8}.
 \end{description}
-
 \section{Detailed Implementation Protocol: The ``Staged Gate'' Workflow}
 
 This section synthesizes the research into a coherent, actionable workflow for the research team.
@@ -309,7 +304,6 @@
     \item \textbf{Balancing:} If the dataset is dominated by stable orbits (low entropy), use \textbf{Importance Resampling}. Run Brutus specifically initialized in ``chaotic'' regions (e.g., using the figure-8 or Pythagorean 3-body initial conditions) to generate more high-entropy examples~\cite{ref31}.
     \item \textbf{Symmetry Augmentation:} Apply $SO(3)$ rotations and translations to valid trajectories to increase dataset size without computational cost, ensuring the PINN learns rotational invariance~\cite{ref6}.
 \end{enumerate}
-
 \section{Synthesis and Conclusion}
 
 The development of a robust CTL-PINN for the Three-Body Problem requires moving beyond the notion of data ``accuracy'' to the more complex notion of data ``fitness for causal learning.'' The analysis reveals that the primary risks—spectral bias, causal firewalls, and dead gradients—stem from the mismatch between the continuous nature of the PINN and the discrete, variable-density nature of the Brutus data.
@@ -325,7 +319,6 @@
     \item \textbf{Adaptive Activation Functions:} Investigate using adaptive activation functions (like Rowdy or locally adaptive sine) to handle the varying frequency content of the N-body problem better than fixed Tanh/ReLU~\cite{ref8}.
     \item \textbf{Symplectic Neural Networks:} Consider modifying the architecture to be inherently symplectic (HNN), moving conservation from a soft loss term to a hard architectural constraint, which reduces the data quality burden regarding energy drift~\cite{ref33}.
 \end{itemize}
-
 \begin{thebibliography}{99}
 
 \bibitem{ref1} On the statistical convergence of N-body simulations of the Solar System. \textit{The Open Journal of Astrophysics}. \url{https://astro.theoj.org/article/154745}
@@ -395,4 +388,3 @@
 \bibitem{ref33} STIFFNESS-AWARE NEURAL NETWORK FOR LEARNING HAMILTONIAN SYSTEMS. OpenReview. \url{https://openreview.net/pdf/862118c84d67ec76a2491e8bff7f7d288934bc92.pdf}
 
 \end{thebibliography}
-
```


### ctl-instruction

```
--- ctl-instruction/original
+++ ctl-instruction/modular
@@ -39,12 +39,35 @@
 \author{Starlordpd233}
 \date{June 2025}
 
-
 \section{Important Note}
 This instruction details the curriculum learning framework for training a specific type of PINN
 designed for this research that focuses on the three-body problem.
 For any information regarding the architecture and structure of the neural network,
 please refer to the \texttt{PINN\_architecture\_plan.tex} file.
+
+\begin{comment}
+\section{A Multi-Fidelity Curriculum Learning Framework}
+
+\subsection{Rationale for Curriculum + Transfer Learning in Chaotic Systems}
+
+A curriculum learning approach is highly beneficial for training on chaotic three-body dynamics.  Rather than presenting the neural network with the hardest cases upfront (which could confuse the optimizer or lead to bad local minima), we mimic the pedagogy of physics education: start with the basics, then incrementally increase complexity 16 3. Early in training, the network sees only the stable, regular orbits;  the loss landscape on this subset is much smoother and easier to navigate, allowing the model to tune into fundamental gravitational laws (like the $1/r^2$ force law, energy and momentum conservation) 3 17. Once this foundation is laid, we gradually introduce more chaotic data.  At each step, the network is already in a "good" region of parameter space and is less likely to be derailed by the sharp, complex patterns that chaotic trajectories bring 18 19. This guided progression greatly improves the optimizer's ability to converge to a physically meaningful solution, as evidenced by curriculum learning successes in other non-convex training problems 20.
+
+Moreover, curriculum learning enhances generalization and robustness 21 5. By first training on high-fidelity, noise-free data, the PINN builds a clean signal of the underlying physics.  Later, when lower-fidelity (slightly noisy) data is added, the network's internal representation already captures the true physics, so it can filter out the numerical noise and avoid overfitting to simulation artifacts 5. In essence, the curriculum acts as a form of regularization: the model must perform well on simple cases before seeing hard cases, which prevents it from simply memorizing chaotic trajectories.  Instead, it must learn general principles that apply across stages.  Given the multi-fidelity nature of our data, transfer learning naturally complements the curriculum.  We do not train a fresh model from scratch on each stage;  instead, we carry over the trained weights from one stage to the next (this combined approach we term Curriculum-Transfer Learning PINN (CTL-PINN)).  Transfer learning leverages the fact that Stage $i+1$ is just Stage $i$ with a bit more difficulty: the solution for the simpler problem is a very good initialization for the harder problem.  This offers multiple advantages:
+
+\begin{itemize}
+    \item \textbf{Faster Convergence:} Each time we move to a new stage, the model already "knows" how to handle all easier scenarios, so it can focus on learning the new data's complexities.  This significantly reduces training time on later stages. Empirically, we observe an accelerated convergence at each curriculum step, since the optimizer starts near a good solution rather than from random initialization.
+    \item \textbf{Avoiding Catastrophic Forgetting:} A critical detail in our implementation is replay of earlier data - i.e., when training on Stage i data, we include all samples from stages $0,1,\dots,i-1$ in the training set.  By training on the union of old and new data, the network retains its performance on earlier tasks.  This prevents the common pitfall where a model, upon learning new (harder) cases, forgets what it learned before.  The result is a monotonic expansion of capability: each stage adds to the model's knowledge without degrading prior accuracy.
+    \item \textbf{Implicit Regularization:} Initializing Stage $i$ with weights from Stage $i-1$ biases the training towards solutions that are close to the previous solution in weight space.  This is desirable because the previous solution was physically sensible;  therefore the new solution is constrained not to stray too far into unphysical regions even as it fits more complex data.  In practice, this means the model will seek a solution for the harder stage that still reproduces the simpler-stage behavior for those cases.  Such a bias acts as a regularizer that helps maintain physical consistency and stability across the curriculum.
+\end{itemize}
+
+In summary, the CTL-PINN framework - a staged curriculum with transfer learning and replay - is designed to overcome the training challenges of chaotic dynamics.  It guides the network to first learn conservation laws and stable motion, then gradually introduces chaos in a controlled fashion.  By the final stage, the network has effectively grown up from solving easy Kepler orbits to handling violent three-body interactions, all while maintaining conservation of energy and momentum.  This framework is robust, efficient, and we will demonstrate in the implementation that it is feasible even on modest hardware.
+
+\subsection{Defining the Curriculum Path}
+
+The curriculum path from stability to chaos is concretely defined by the stage criteria described in Section 2.2 (see Table 1).  To recap briefly, we start exclusively with the high-fidelity hierarchical data in Stage 0, then incrementally loosen the invariant thresholds to include more difficult systems, and eventually incorporate the low-fidelity random data in stages 2 and beyond.  Notably, we chose to introduce the low-fidelity data only after the network has mastered the high-fidelity cases.  An alternative strategy might have been to pre-train on the broader low-fidelity dataset and then fine-tune on the high-fidelity subset.  However, for chaotic dynamics, we deem that approach less effective establishing a correct physics baseline from precise data at the outset is paramount.  If the model were first trained on noisy chaotic data, it might pick up spurious correlations or be misled by numerical errors.  By contrast, our chosen path (HF first, then LF) ensures the PINN has a solid grasp of the true physics (thanks to Stage 0-1 on clean data) and can use that as an internal regularizer when confronted with the lower-precision chaotic cases 22.
+
+Each stage transition is a point where we expand the training set (adding new simulations) and then continue training (with transferred weights).  We also adjust certain training hyperparameters across stages to reflect the increasing difficulty - for example, the weight on the energy regularization term is ramped up with each stage (details in Section 4.2).  The curriculum is thus not only about data; it also involves a schedule for how strongly we enforce physical constraints as training progresses, ensuring that by the time we reach the most chaotic data, the network is highly constrained to obey invariants.  It's important to highlight that the stage definitions based on invariants are rooted in physical reasoning (bound vs unbound, circular vs eccentric, etc.) but the exact threshold values (e.g. $E<-0.5$ or $\tau_L>5$) are somewhat tunable.  In practice, one could adjust these thresholds or even define more finely graded stages if needed.  The provided five-stage scheme (with a couple of sub-stages) proved sufficient in our experience, striking a good balance between too slow a curriculum (many tiny steps) and too fast (jumps that are too large).  The invariants provide an interpretable way to calibrate these stages.  For example, if the training struggles when Stage 2 data (top 25\% stable random cases) is introduced, one might decide to break that into two smaller introductions (say top 10\% first, then next 15\%).  Conversely, if training is smooth, one could potentially combine some sub-stages.  Thus, while the current stage definitions are mathematically and empirically sound, they are also flexible guidelines.
+\end{comment}
 
 \section{Characterizing and Organizing the Multi-Fidelity Simulation Data}
 
@@ -248,30 +271,6 @@
 \end{itemize}
 
 Thanks to this pipeline, the datasets are well-suited for curriculum learning.  The easier stages (0-1) are drawn from the meticulously stable hierarchical runs (which passed all checks and have small step sizes), providing trustworthy ground truth for the PINN to latch onto.  The chaotic data introduced later has also passed basic energy-conservation and resolution checks, meaning the PINN won't be asked to learn from inconsistent or nonsensical training targets.  The five invariants used to define the curriculum stages are indeed the same metrics used during data generation (e.g., virial ratio and minimum separation were used as filters) - this consistency reinforces that the curriculum progression is grounded in physical measures of complexity.  Overall, the data generation strategy is effective and we recommend continuing with this hybrid approach for future data expansion.  It achieves a wide coverage without requiring higher precision or significantly more simulations.  Any gaps in the difficulty spectrum can be filled by targeted new simulations in an active learning loop (see Section 4.3) rather than by overhauling the sampling strategy.  In short, the current datasets and stage definitions are sufficiently comprehensive and well-structured for the learning task, striking a balance between fidelity, diversity, and manageability.
-\end{comment}
-
-\begin{comment}
-\section{A Multi-Fidelity Curriculum Learning Framework}
-
-\subsection{Rationale for Curriculum + Transfer Learning in Chaotic Systems}
-
-A curriculum learning approach is highly beneficial for training on chaotic three-body dynamics.  Rather than presenting the neural network with the hardest cases upfront (which could confuse the optimizer or lead to bad local minima), we mimic the pedagogy of physics education: start with the basics, then incrementally increase complexity 16 3. Early in training, the network sees only the stable, regular orbits;  the loss landscape on this subset is much smoother and easier to navigate, allowing the model to tune into fundamental gravitational laws (like the $1/r^2$ force law, energy and momentum conservation) 3 17. Once this foundation is laid, we gradually introduce more chaotic data.  At each step, the network is already in a "good" region of parameter space and is less likely to be derailed by the sharp, complex patterns that chaotic trajectories bring 18 19. This guided progression greatly improves the optimizer's ability to converge to a physically meaningful solution, as evidenced by curriculum learning successes in other non-convex training problems 20.
-
-Moreover, curriculum learning enhances generalization and robustness 21 5. By first training on high-fidelity, noise-free data, the PINN builds a clean signal of the underlying physics.  Later, when lower-fidelity (slightly noisy) data is added, the network's internal representation already captures the true physics, so it can filter out the numerical noise and avoid overfitting to simulation artifacts 5. In essence, the curriculum acts as a form of regularization: the model must perform well on simple cases before seeing hard cases, which prevents it from simply memorizing chaotic trajectories.  Instead, it must learn general principles that apply across stages.  Given the multi-fidelity nature of our data, transfer learning naturally complements the curriculum.  We do not train a fresh model from scratch on each stage;  instead, we carry over the trained weights from one stage to the next (this combined approach we term Curriculum-Transfer Learning PINN (CTL-PINN)).  Transfer learning leverages the fact that Stage $i+1$ is just Stage $i$ with a bit more difficulty: the solution for the simpler problem is a very good initialization for the harder problem.  This offers multiple advantages:
-
-\begin{itemize}
-    \item \textbf{Faster Convergence:} Each time we move to a new stage, the model already "knows" how to handle all easier scenarios, so it can focus on learning the new data's complexities.  This significantly reduces training time on later stages. Empirically, we observe an accelerated convergence at each curriculum step, since the optimizer starts near a good solution rather than from random initialization.
-    \item \textbf{Avoiding Catastrophic Forgetting:} A critical detail in our implementation is replay of earlier data - i.e., when training on Stage i data, we include all samples from stages $0,1,\dots,i-1$ in the training set.  By training on the union of old and new data, the network retains its performance on earlier tasks.  This prevents the common pitfall where a model, upon learning new (harder) cases, forgets what it learned before.  The result is a monotonic expansion of capability: each stage adds to the model's knowledge without degrading prior accuracy.
-    \item \textbf{Implicit Regularization:} Initializing Stage $i$ with weights from Stage $i-1$ biases the training towards solutions that are close to the previous solution in weight space.  This is desirable because the previous solution was physically sensible;  therefore the new solution is constrained not to stray too far into unphysical regions even as it fits more complex data.  In practice, this means the model will seek a solution for the harder stage that still reproduces the simpler-stage behavior for those cases.  Such a bias acts as a regularizer that helps maintain physical consistency and stability across the curriculum.
-\end{itemize}
-
-In summary, the CTL-PINN framework - a staged curriculum with transfer learning and replay - is designed to overcome the training challenges of chaotic dynamics.  It guides the network to first learn conservation laws and stable motion, then gradually introduces chaos in a controlled fashion.  By the final stage, the network has effectively grown up from solving easy Kepler orbits to handling violent three-body interactions, all while maintaining conservation of energy and momentum.  This framework is robust, efficient, and we will demonstrate in the implementation that it is feasible even on modest hardware.
-
-\subsection{Defining the Curriculum Path}
-
-The curriculum path from stability to chaos is concretely defined by the stage criteria described in Section 2.2 (see Table 1).  To recap briefly, we start exclusively with the high-fidelity hierarchical data in Stage 0, then incrementally loosen the invariant thresholds to include more difficult systems, and eventually incorporate the low-fidelity random data in stages 2 and beyond.  Notably, we chose to introduce the low-fidelity data only after the network has mastered the high-fidelity cases.  An alternative strategy might have been to pre-train on the broader low-fidelity dataset and then fine-tune on the high-fidelity subset.  However, for chaotic dynamics, we deem that approach less effective establishing a correct physics baseline from precise data at the outset is paramount.  If the model were first trained on noisy chaotic data, it might pick up spurious correlations or be misled by numerical errors.  By contrast, our chosen path (HF first, then LF) ensures the PINN has a solid grasp of the true physics (thanks to Stage 0-1 on clean data) and can use that as an internal regularizer when confronted with the lower-precision chaotic cases 22.
-
-Each stage transition is a point where we expand the training set (adding new simulations) and then continue training (with transferred weights).  We also adjust certain training hyperparameters across stages to reflect the increasing difficulty - for example, the weight on the energy regularization term is ramped up with each stage (details in Section 4.2).  The curriculum is thus not only about data; it also involves a schedule for how strongly we enforce physical constraints as training progresses, ensuring that by the time we reach the most chaotic data, the network is highly constrained to obey invariants.  It's important to highlight that the stage definitions based on invariants are rooted in physical reasoning (bound vs unbound, circular vs eccentric, etc.) but the exact threshold values (e.g. $E<-0.5$ or $\tau_L>5$) are somewhat tunable.  In practice, one could adjust these thresholds or even define more finely graded stages if needed.  The provided five-stage scheme (with a couple of sub-stages) proved sufficient in our experience, striking a good balance between too slow a curriculum (many tiny steps) and too fast (jumps that are too large).  The invariants provide an interpretable way to calibrate these stages.  For example, if the training struggles when Stage 2 data (top 25\% stable random cases) is introduced, one might decide to break that into two smaller introductions (say top 10\% first, then next 15\%).  Conversely, if training is smooth, one could potentially combine some sub-stages.  Thus, while the current stage definitions are mathematically and empirically sound, they are also flexible guidelines.
 \end{comment}
 
 \section{A Glimpse at the Data}
```


### pinn-architecture

**Inactive sections excluded:** input_vector_inactive, advanced_training_inactive, consolidated_blueprint_inactive

```
--- pinn-architecture/original
+++ pinn-architecture/modular
@@ -37,12 +37,11 @@
 \author{Starlordpd233}
 
 
-
 \section{Section 1: Foundational Architectural Principles: A Co-Designed Approach for Chaotic Systems}
 
 The accurate and long-term simulation of $\mathrm{N}$-body gravitational systems, particularly the notoriously chaotic three-body problem, presents a formidable challenge for traditional numerical and machine learning methods alike. The dynamics are characterized by an extreme sensitivity to initial conditions, where infinitesimal perturbations can lead to exponentially divergent trajectories over time. Furthermore, the solutions often contain a complex mixture of smooth, quasi-periodic motion and sharp, high-frequency events that occur during close encounters between bodies. A successful predictive model must therefore not only capture these multi-scale temporal features with high fidelity but also adhere to fundamental global conservation laws, such as the conservation of total energy and angular momentum, to ensure its long-term physical plausibility.$^1$
 
-A generic neural network architecture, such as a standard Multi-Layer Perceptron (MLP), lacks the specific structural priors necessary to handle this confluence of challenges. Such models often suffer from a "spectral bias," a tendency to learn low-frequency functions more easily, which makes them struggle to represent the high-frequency components inherent in chaotic dynamics.$^2$ More critically, enforcing the governing physical laws—in this case, Newton's laws of motion—within a Physics-Informed Neural Network (PINN) framework requires the computation of high-order derivatives of the network's output. For the $\mathrm{N}$-body problem, this involves calculating the second derivative of the predicted position with respect to time, $\frac{\mathrm{d}^2 \mathrm{r}}{\mathrm{d} t^2}$, to form the physics residual term in the loss function. Common activation functions like the Rectified Linear Unit (ReLU) are fundamentally unsuitable for this task. While computationally efficient, ReLU produces a piecewise linear output, meaning its first derivative is piecewise constant and its second derivative is a series of Dirac delta functions (i.e., zero almost everywhere). This mathematical property makes it impossible to accurately represent the smooth, continuously varying gravitational forces that govern celestial motion.$^1$
+A generic neural network architecture, such as a standard Multi-Layer Perceptron (MLP), lacks the specific structural priors necessary to handle this confluence of challenges. Such models often suffer from a "spectral bias," a tendency to learn low-frequency functions more easily, which makes them struggle to represent the high-frequency components inherent in chaotic dynamics.$^2$ More critically, enforcing the governing physical laws—in this case, Newton's laws of motion—within a Physics-Informed Neural Network (PINN) framework requires the computation of high-order derivatives of the network's output. For the $\mathrm{N}$-body problem, this involves calculating the second derivative of the predicted position with respect to time, $\frac{\mathrm{d}^2 \mathrm{r}}{\mathrm{d} t^2}$, to form the physics residual term in the loss function. Common activation functions like the Rectified Linear Unit (ReLU) are fundamentally unsuitable for this task. While computationally efficient, ReLU produces a piecewise linear output, meaning its first derivative is piecewise constant and its second derivative is a series of Dirac delta functions (i.e., zero almost everywhere). This mathematical property makes it impossible to represent the smooth, continuously varying gravitational forces that govern celestial motion.$^1$
 
 To overcome these fundamental limitations, a more principled approach is required—one where the architecture itself imparts a strong inductive bias that aligns with the underlying physics. The framework detailed in this report proposes a hybrid PINN that is not an arbitrary collection of techniques but a meticulously co-designed system. Each architectural component is deliberately chosen to counteract a specific, well-understood failure mode of standard models when applied to chaotic physical systems. This synergistic design methodically addresses the core requirements of the problem:
 
@@ -53,7 +52,6 @@
 \end{enumerate}
 
 This philosophy of pragmatic hybridization, which strategically borrows the most critical benefits from multiple advanced paradigms while avoiding their most restrictive drawbacks, is a central theme of the proposed design. The resulting model is a synergistic whole, where the SQR-SkipResNet enables the necessary depth for expressivity, the SIREN activations provide the derivative fidelity required for physics enforcement, and the HNN-style loss term ensures the long-term stability essential for physical realism.
-
 \section{The SQR-SkipResNet-SIREN Backbone: A Deep Dive into the Core Architecture}
 
 This section provides the definitive, mathematically-grounded specifications for each component of the neural network's core structure. Every choice is justified by its contribution to the model's ability to represent complex physical phenomena accurately and to be trained stably.
@@ -182,9 +180,7 @@
 \hline
 Weight Init. (First) & $\mathrm{U}\left[-\frac{1}{n_{\text{in}}}, \frac{1}{n_{\text{in}}}\right]$ & The mathematically-derived initialization for the first SIREN layer to create a random Fourier feature mapping.$^1$ \\
 \hline
-Weight Init. (Hidden) & $\mathrm{U}\left[-\frac{\text{hidden\_omega\_0}}{6 n_{\text{in}}}, \frac{\text{hidden\_omega\_0}}{6 n_{\text{in}}}\right]$
-\authcomment{I believe this formula for initialization is incorrect}
-& The principled initialization for all subsequent SIREN layers, designed to preserve activation variance and enable stable training of deep sinusoidal networks.$^1$ \\
+Weight Init. (Hidden) & $\mathrm{U}\left[-\frac{\text{hidden\_omega\_0}}{6 n_{\text{in}}}, \frac{\text{hidden\_omega\_0}}{6 n_{\text{in}}}\right]$ \authcomment{I believe this formula for initialization is incorrect} & The principled initialization for all subsequent SIREN layers, designed to preserve activation variance and enable stable training of deep sinusoidal networks.$^1$ \\
 \hline
 Skip Cadence & Alternating (per SQR SkipResNet) & The alternating pattern of plain and power-enhanced residual layers effectively balances feature transformation and stable gradient flow.$^1$ \\
 \hline
@@ -194,72 +190,6 @@
 \hline
 \end{longtable}
 \FloatBarrier
-
-
-
-
-\begin{comment}
-
-\section{Input Vector Formulation and Output Processing}
-
-The model's ability to learn and generalize across a vast space of possible $\mathrm{N}$-body trajectories depends critically on how information is presented to it. This section details the definitive formulation for the network's input vector and the processing of its output, resolving a critical discrepancy in the planning documents.
-
-\subsection{An Injective, Physically-Grounded Conditional Input}
-
-A non-autoregressive PINN must be conditioned on the specific trajectory it is meant to predict. A naive approach might be to feed the raw initial state vector (positions and velocities) as input. However, this is high-dimensional and fails to leverage the underlying physics of the problem. A more robust and principled approach is to condition the network on a compact, physically meaningful representation of the system.
-
-A critical flaw was identified in the initial plan: the proposed 7-dimensional vector of physical invariants$^1$ is non-injective. This means that multiple, physically distinct initial conditions—for example, systems that are simply rotations of each other or are at different phases of the same orbit—could map to the identical input vector. This ambiguity creates an impossible learning target for a conditional network, as it would be asked to produce different outputs for the exact same input, leading to training failure.
-
-To resolve this, this report formally adopts the 14-dimensional injective input vector specified in the more refined CTL instruction plan.$^1$ This vector ensures that every unique initial state maps to a unique input representation. The network input is a concatenation of the time coordinate $t$ and a 13-component initial condition vector, $\mathrm{IC}$:
-
-\[
-\text{Input} = [t, \mathrm{IC}]
-\]
-
-The $\mathrm{IC}$ vector is constructed from three distinct groups of physically meaningful quantities detailed as follows:
-
-\begin{equation}
-    \text{IC} = \begin{pmatrix}
-    m_1^{\text{norm}}, m_2^{\text{norm}}, m_3^{\text{norm}} & \text{(normalized masses)} \\
-    E^{\text{norm}} & \text{(normalized total energy)} \\
-    L_{\text{norm}} & \text{(normalized angular momentum)} \\
-    Q^{\text{norm}} & \text{(normalized virial ratio)} \\
-    s_{\min}^{\text{norm}} & \text{(normalized min separation)} \\
-    I_1^{\text{norm}}, I_2^{\text{norm}}, I_3 & \text{(shape invariants)} \\
-    \theta_1^{\text{norm}}, \theta_2^{\text{norm}} & \text{(normalized velocity angles)} \\
-    I^{\text{norm}} & \text{(normalized moment of inertia)}
-    \end{pmatrix}
-\end{equation}
-
-For more information on the input vector formulation, refer to the CTL instruction plan. When computing each component in the above vector,
-we need to use the scaled parameters that are dimensionless and then using the code snippet in the CTL instruction plan to
-compute the invariants and ensure that all components are normalized them to [-1,1].
-
-\subsubsection{Scaling the Training Data: Defining the G=1 System of Units}
-
-To simplify the physical equations and improve numerical stability, we adopt a non-dimensional system of units where the gravitational constant is 1. This is achieved by carefully choosing our characteristic time, \(T\), and characteristic length, \(D\).
-
-\begin{enumerate}
-    \item \textbf{Characteristic Time (T):} We define the characteristic time from the data. Let \(T = t_{max} = 10\), where \(t_{max}\) is the maximum time value across the entire simulation dataset. The input time \(t\) is then normalized to a dimensionless time \(t'\) in \([0, 1]\) using the formula:
-    \[
-        t' = \frac{t}{T}
-    \]
-
-    \authcomment{I believe this formula is incorrect for the normalization of time. Shouldn't we normalize the time to [-1,1]?}
-
-    \item \textbf{Characteristic Length (D):} By setting the new gravitational constant \(G^{\text{prime}}\) to 1, our characteristic length \(D\) is determined by our choice of \(T\). It is calculated using the physical value of \(G\) as follows (but since BRUTUS uses G=1, $D = \sqrt[3]{T^2} \approx 4.6416$):
-    \[
-        D = \sqrt[3]{G T^2}
-    \]
-\end{enumerate}
-
-All position-based quantities (e.g., \(\mathbf{r}\)) in the model must be scaled by this D to \(\mathbf{r}' = \mathbf{r} / D\), velocities to \(\mathbf{v}' = \mathbf{v} \cdot (T / D)\), and accelerations (from AD) are automatically scaled. This scaling is applied during data preprocessing (see CTL document Phase 1) to BRUTUS trajectories and initial conditions before computing the IC vector or feeding to the network.
-
-The scaled data ensures consistency in loss functions (e.g., no explicit G). For length-derived IC components (e.g., \(s_{\min}\)), compute from scaled data before [-1,1] normalization (cross-reference CTL Section 4.2).
-
-\end{comment}
-
-
 
 \section{The Multi-Component, Physics-Constrained Loss Function}
 
@@ -439,8 +369,8 @@
     \end{itemize}
 
     \item \textbf{Gradient Handling:} \\
-    – $\lambda_p$ must be treated as a non-trainable scalar updated via code (not autograd) \\
-    – $\mu_p$ is a dynamic parameter updated algorithmically (excluded from backpropagation)
+    -- $\lambda_p$ must be treated as a non-trainable scalar updated via code (not autograd) \\
+    -- $\mu_p$ is a dynamic parameter updated algorithmically (excluded from backpropagation)
 \end{enumerate}
 
 \begin{lstlisting}[language=Python, caption={ALM Parameter Updates}]
@@ -562,7 +492,6 @@
     \item \textbf{Softening Parameter:} The same value $\epsilon_{\text{soft}} = 10^{-5}$ is used consistently in both the physics residual and energy calculations to prevent numerical instabilities during close encounters.
     \item \textbf{Collocation Points:} The same set of $N_{\text{col}}$ points is used for both physics and energy loss evaluation to ensure computational efficiency.
 \end{itemize}
-
 \section{Advanced Training and Optimization Strategy}
 
 Successfully training the network requires a sophisticated approach to navigate the complex, non-convex loss landscape and handle numerical instabilities.
@@ -596,7 +525,6 @@
 
 # Then, call optimizer.step()
 \end{lstlisting}
-
 \section{Inference and Trajectory Generation}
 
 Once the model is trained, it can be used as a high-fidelity function approximator to generate entire trajectories on demand.
@@ -615,7 +543,7 @@
 
 The final layer of the SQR-SkipResNet-SIREN network is a standard linear layer without any activation function. This is crucial as it allows the network's outputs—the predicted positions—to take on any real value required by the physical system. The output is a 9-dimensional vector representing the concatenated positions of the three bodies at a given time $\mathrm{t}$:
 \[
-\mathrm cl r_\theta(\mathrm{t}) = [\mathrm{r}_1(\mathrm{t}), \mathrm{r}_2(\mathrm{t}), \mathrm{r}_3(\mathrm{t})]
+\mathrm{r}_\theta(\mathrm{t}) = [\mathrm{r}_1(\mathrm{t}), \mathrm{r}_2(\mathrm{t}), \mathrm{r}_3(\mathrm{t})]
 \]
 
 Crucially, the network does not predict velocities or accelerations directly. Instead, these kinematic quantities are derived from the position outputs using AD with respect to the time input, $t$. The velocity vector is computed as the first-order derivative of the position vector, and the acceleration vector is computed as the second-order derivative$^1$:
@@ -642,163 +570,6 @@
 ...
 \end{verbatim}
 
-\begin{comment}
-
-\section{Advanced Training Dynamics and Optimization}
-
-The successful training of the proposed hybrid PINN is a non-trivial task. The composite loss function creates a highly complex, non-convex optimization landscape, and naive training approaches are almost certain to fail. They may converge to poor local minima, suffer from numerical instability, or fail to properly balance the competing objectives of data fidelity and physics enforcement. This section details a suite of advanced, essential techniques for engineering the training dynamics to navigate this landscape effectively and achieve a robust, physically accurate solution.
-
-\subsection{Adaptive Loss Balancing via the Augmented Lagrangian Method (ALM)}
-
-The single most sensitive and critical aspect of training a PINN is balancing the influence of the data fidelity term ($\mathcal{L}_{\text{data}}$) and the physics residual term ($\mathcal{L}_{\text{physics}}$). These two terms often have vastly different magnitudes and generate conflicting gradients, pulling the network parameters in opposing directions. A fixed weighting factor, $\alpha$, is insufficient, as the optimal balance changes throughout the training process.
-
-A naive scheduling strategy, such as a "warmup" where $\alpha$ is sharply increased from zero to a large value, has been shown to fail catastrophically. This occurs because the optimizer first settles into a local minimum of the $\mathcal{L}_{\text{data}}$ landscape. The sudden introduction of a large $\mathcal{L}_{\text{physics}}$ term violently reshapes the total loss landscape, potentially placing the optimizer on a steep "cliff" from which it cannot recover, leading to training divergence.$^1$
-
-A more robust and principled solution is to move beyond pre-defined schedules and adopt an adaptive method that automates the balancing act. This report recommends the Adaptive Augmented Lagrangian Method (ALM), which reframes the multi-objective optimization problem into a more physically intuitive constrained optimization problem: minimize $\mathcal{L}_{\text{data}}$ subject to the constraint that $\mathcal{L}_{\text{physics}} \approx 0$.$^1$ The implementation, based on the framework proposed in the literature, proceeds as follows:
-
-\begin{enumerate}
-    \item \textbf{Lagrangian Formulation:} The loss is reformulated as an augmented Lagrangian, which includes both a Lagrange multiplier $\lambda_p$ and a quadratic penalty term with coefficient $\mu_p$:
-    \[
-    \mathcal{L}(\theta, \lambda_p) = \mathcal{L}_{\text{data}} + \lambda_p \mathcal{L}_{\text{physics}} + \frac{\mu_p}{2} \mathcal{L}_{\text{physics}}^2
-    \]
-    \item \textbf{Primal-Dual Updates:} The training involves alternating between a "primal" step, where the network weights $\theta$ are updated via gradient descent on $\mathcal{L}(\theta, \lambda_p)$, and a "dual" step, where the Lagrange multiplier $\lambda_p$ is updated via gradient ascent. The dual update rule is:
-    \[
-    \lambda_p \leftarrow \lambda_p + \mu_p \mathcal{L}_{\text{physics}}
-    \]
-    This update naturally increases the penalty on the physics term when its residual is large and decreases it when the constraint is satisfied.
-    \item \textbf{Adaptive Penalty Parameter $\mu_p$:} The key innovation of the adaptive ALM is that the penalty parameter $\mu_p$, which acts as the learning rate for the dual update, is not fixed. It is dynamically adjusted based on the history of the constraint violation, using a rule inspired by the RMSprop optimizer$^1$:
-    \begin{itemize}
-        \item First, a moving average of the squared physics loss is maintained: $\mathrm{v}_p \leftarrow \beta \mathrm{v}_p + (1 - \beta) \mathcal{L}_{\text{physics}}^2$
-        \item Then, the penalty parameter is updated as: $\mu_p \leftarrow \frac{\gamma}{\mathrm{v}_p + \epsilon}$ where $\beta$ is a momentum term (e.g., 0.99), $\gamma$ is a base learning rate (e.g., $10^{-2}$), and $\epsilon$ is a small constant for numerical stability.
-    \end{itemize}
-\end{enumerate}
-
-This dual-level adaptive mechanism is exceptionally robust. The Lagrange multiplier $\lambda_p$ automatically balances the data and physics terms, while the adaptive penalty $\mu_p$ stabilizes the update of $\lambda_p$, preventing the oscillations or runaway growth that can plague simpler ALM implementations. This automates what is arguably the most difficult hyperparameter tuning task in PINN training, leading to significantly more stable and reliable convergence.$^1$
-
-\subsection{Curriculum-Aware Energy Regularization Scheduling}
-
-Just as the balance between data and physics must be dynamic, the strength of the energy conservation regularizer should also adapt to the context of the training data. The Curriculum-Transfer Learning (CTL) framework provides a natural structure for this adaptation, as the training data is stratified into stages of increasing complexity, from highly stable, predictable systems to wildly chaotic ones. The energy conservation constraint is most critical for the latter.
-
-Therefore, the weight of the energy loss term, $\lambda_{\mathrm{E}}$, is scheduled to increase in lockstep with the curriculum stages. This strategy avoids over-constraining the model when it is learning simple dynamics, where energy is naturally well-conserved, but applies a strong physical regularization precisely when it is needed most—when the model is faced with chaotic trajectories that are prone to energy drift. The recommended definitive schedule, based on the five-stage curriculum, is (needs revision here based on the new 7-stage CTL plan):
-\[
-\lambda_{\mathrm{E}}(\mathrm{k}) = 10^{\mathrm{k}-3} \text{ for curriculum stage } \mathrm{k} \in \{0,1,\ldots,5\}
-\]
-
-This results in a progression from a very weak penalty ($\lambda_{\mathrm{E}} = 0.01$ for Stage 0) to a very strong penalty ($\lambda_{\mathrm{E}} = 1000$ for Stage 5), aligning the strength of the physical constraint with the inherent stability of the training examples for a more efficient and stable learning process.
-
-\subsection{Two-Phase Optimization Strategy}
-
-To achieve both efficient exploration of the complex loss landscape and high-precision convergence, a two-phase optimization strategy is employed. This approach combines a first-order stochastic optimizer with a quasi-second-order deterministic optimizer, leveraging the distinct strengths of both.$^1$
-
-\begin{enumerate}
-    \item \textbf{Phase 1 (Exploration and Initial Convergence):} The initial training phase utilizes the Adam optimizer. With its adaptive learning rates and momentum-based updates, Adam is a robust choice for stochastic optimization. It is well-suited for navigating the highly non-convex loss landscape of the PINN in the early stages of training, efficiently finding a good basin of attraction.
-    \item \textbf{Phase 2 (Fine-tuning and Polishing):}
-    Once the Adam optimizer has converged, the optimization process is switched to a quasi-Newton method to "polish"
-    the solution and minimize the residuals to a high precision. However, standard L-BFGS requires the full training
-    batch, which is computationally infeasible on consumer hardware for the large datasets in later curriculum stages.
-    Therefore, we will adopt a more memory-efficient approach:
-
-    Stochastic L-BFGS (L-BFGS-M): This is a variant of L-BFGS designed to work with mini-batches, just like Adam.
-    It uses historical gradient information to approximate the Hessian curvature while processing only a small
-    batch of data at a time. This provides the high-precision convergence benefits of a second-order method without
-    the prohibitive memory cost of full-batch optimization, making it ideal for our use case. (Consider searching for an
-    open-source algorithm for reference here.)
-\end{enumerate}
-
-\subsection{Stabilizing Training with Adaptive Gradient Clipping}
-
-A significant practical challenge in training PINNs for the $\mathrm{N}$-body problem arises from the terms in the loss function that involve inverse-square distances, such as the gravitational force $(\propto 1 / || \mathrm{r}_i - \mathrm{r}_j ||^3)$ and potential energy $(\propto 1 / || \mathrm{r}_i - \mathrm{r}_j ||)$. During simulated close encounters, the distance between bodies can become very small, causing these terms—and their gradients—to explode. A single such event can send an enormous gradient to the network weights, completely destabilizing the optimizer and destroying training progress.$^1$
-
-Gradient clipping is an essential technique to prevent this. However, using a fixed, constant clipping threshold is suboptimal. A more robust and adaptive strategy is to clip the global norm of the gradients relative to their recent typical magnitude. The recommended implementation is to clip the gradient norm to a multiple of the median gradient norm, calculated over a moving window of recent training steps.$^1$ The procedure is as follows:
-
-\begin{enumerate}
-    \item After computing the gradients for a training batch, calculate their global L2 norm: $\text{grad\_norm} = || \nabla \mathcal{L}_{\text{total}} ||$.
-    \item Maintain a queue of the $\text{grad\_norm}$ values from the last, e.g., 100, training steps.
-    \item Compute the median of this history, $\text{median\_norm}$. The median is used because it is a robust statistic, insensitive to the very outlier spikes we aim to control.
-    \item Set the dynamic clipping threshold: $\text{clip\_value} = C \times \text{median\_norm}$, where $C$ is a hyperparameter (a value of 5 is a robust starting point).
-    \item Apply the clipping operation to the network's parameters before the optimizer step.
-\end{enumerate}
-
-This adaptive approach normalizes the gradient updates. It automatically allows for larger gradients when the model is learning rapidly on stable data but aggressively caps the rare, extreme spikes that occur during chaotic close encounters, providing stability without unnecessarily throttling the optimizer.
-
-\begin{table}[htbp]
-    \centering
-    \caption{Training hyperparameters and optimizer settings}\label{tab:training_hyperparameters}
-    \begin{tabularx}{\textwidth}{|l|l|X|}
-        \hline
-        \textbf{Hyperparameter} & \textbf{Recommended Value} & \textbf{Rationale \& Justification} \\
-        \hline
-        Optimizer (Initial) & Adam, $\beta = (0.9, 0.999)$ & Standard, robust choice for stochastic optimization of the non-convex PINN loss landscape.$^1$ \\
-        \hline
-        Learning Rate (Adam) & Cosine decay: $10^{-3} \rightarrow 10^{-4}$ & Starts with a reasonably high LR for fast exploration and decays to a smaller value for fine-tuning near a minimum, preventing overshoot. \\
-        \hline
-        Optimizer (Fine-tune) & Stochastic L-BFGS & A quasi-Newton method that uses mini-batches, enabling high-precision polishing of the solution without the prohibitive memory cost of full-batch L-BFGS \\
-        \hline
-        Gradient Clipping & Global norm clipping at $5 \times$ median norm & Adaptive threshold prevents explosions from close encounters without suppressing learning during stable phases. The median provides a robust reference. \\
-        \hline
-        Physics Loss Weight & Adaptive ALM $(\gamma = 10^{-2}, \beta = 0.99)$ & Automates the difficult task of loss balancing for superior stability and convergence, treating the physics as a constraint to be satisfied. \\
-        \hline
-        Energy Loss Weight & Curriculum-scheduled: $\lambda_E(k) = 10^{k-3}$ & Aligns the strength of the energy constraint with the difficulty of the curriculum stage $k$, applying regularization only as strongly as needed.\\
-        \hline
-        Weight Decay & $10^{-6}$ (Range: $0 - 10^{-5}$) & Light L2 regularization to prevent network parameters from growing excessively large, which can lead to numerical instability.\\
-        \hline
-        Batch Size & 1024-4096 collocation points & A balance between providing a good gradient estimate and fitting within memory constraints. Should be scaled based on available GPU memory. \\
-        \hline
-    \end{tabularx}
-\end{table}
-\FloatBarrier
-
-\end{comment}
-
-\begin{comment}
-\section{Consolidated Implementation Blueprint and Final Recommendations}
-
-This final section consolidates the preceding architectural and training principles into a cohesive, actionable plan for implementation. The successful construction of the proposed model hinges on the tight integration of the network architecture, the multi-component loss function, and the advanced training dynamics, all orchestrated within the Curriculum-Transfer Learning (CTL) framework.
-
-\subsection{A Unified View of the Architecture and Loss Function (Needs update)}
-
-The complete model can be visualized as a data-flow pipeline. At its core is the SQR-SkipResNet backbone with SIREN activations. This network takes as input the 14-dimensional concatenated vector containing the time coordinate $t$ and the 13-dimensional conditional vector of physical invariants, masses, and orientation angles. The network processes this input through its 12 hidden layers, each 256 neurons wide, applying the principled SIREN initialization and the power-enhanced residual connections. The final linear layer outputs a 9-dimensional vector representing the predicted positions of the three bodies, $\mathrm{r}_\theta(\mathrm{t})$.
-
-This output then feeds into the three parallel heads of the loss function:
-
-\begin{enumerate}
-    \item \textbf{Data Loss ($\mathcal{L}_{\text{data}}$):} The predicted positions $\mathrm{r}_\theta(\mathrm{t})$ are compared against the ground-truth positions $\mathrm{r}_{\text{true}}(\mathrm{t})$ from the training data using an MAE loss.
-    \item \textbf{Physics Loss ($\mathcal{L}_{\text{physics}}$):} The position output $\mathrm{r}_\theta(\mathrm{t})$ is twice differentiated with respect to the time input $t$ using automatic differentiation to yield the predicted acceleration $\mathrm{a}_\theta(\mathrm{t})$. This is then used to compute the Newtonian physics residual, which is minimized via an MSE loss.
-    \item \textbf{Energy Loss ($\mathcal{L}_{\text{energy}}$):} The position output $\mathrm{r}_\theta(\mathrm{t})$ is differentiated once to get the predicted velocity $\mathrm{v}_\theta(\mathrm{t})$. The positions and velocities are used to compute the total system energy $H_{\text{total}}(\mathrm{t})$. This is compared against the initial energy $H_0$ using an MSE loss.
-\end{enumerate}
-
-The three loss components are then combined using the dynamically adjusted weights from the ALM and the curriculum schedule to form the final $\mathcal{L}_{\text{total}}$ that is used to update the network's weights.
-
-\subsection{Integration with the Curriculum-Transfer Learning (CTL) Framework (Needs update)}
-
-The designed model and its sophisticated training dynamics are intended to be deployed within the CTL framework outlined in the project proposal. This framework provides a structured, multi-stage approach to training that is essential for tackling a problem with such a wide range of difficulty. The implementation pathway is as follows:
-
-\begin{enumerate}
-    \item \textbf{Stage 0 Foundation:} Begin training using only the Stage 0 dataset, which consists of the most stable, predictable, high-fidelity simulations. Train the SQR-SkipResNet-SIREN model using the full suite of advanced techniques: the Adam optimizer followed by an L-BFGS polish, the adaptive ALM for loss balancing, and adaptive gradient clipping. Set the energy regularization weight $\lambda_E$ to its initial low value of 0.01. Train until the data and physics losses converge to a low, stable value.
-    \item \textbf{Stage Progression ($k=1$ to 5):} For each subsequent stage, execute the following transfer learning loop:
-    \begin{enumerate}[label=\alph*.]
-        \item \textbf{Expand Data:} Augment the training dataset to include all data from stages 0 through $\mathrm{k}$.
-        \item \textbf{Transfer Weights:} Initialize the network with the final, converged weights from the previous stage $(k-1)$.
-        \item \textbf{Reset Optimizer:} Reset the state of the Adam optimizer (its momentum and variance estimates) to start fresh on the new data distribution.
-        \item \textbf{Update Regularization:} Adjust the energy loss weight $\lambda_E$ according to the curriculum schedule, i.e., $\lambda_E(k) = 10^{k-2}$.
-        \item \textbf{Continue Training:} Resume training on the expanded dataset until the losses re-converge, again using the two-phase Adam/L-BFGS optimization strategy.
-    \end{enumerate}
-\end{enumerate}
-
-This process systematically exposes the network to progressively more complex and chaotic dynamics. By leveraging transfer learning, the model builds upon its existing knowledge at each stage, dramatically accelerating convergence and improving its ability to find a robust, generalizable physical solution.$^1$
-
-\subsection{Final Recommendations for a Robust and Performant Implementation}
-
-This report has detailed a comprehensive blueprint for a state-of-the-art PINN for the $\mathrm{N}$-body problem. The key to its success lies in moving beyond naive implementations and embracing a co-designed approach where architecture and training dynamics are tailored to the specific challenges of the physics. The most critical, non-negotiable design choices that differentiate this proposed model are:
-
-\begin{enumerate}
-    \item \textbf{Architecture is Foundational:} The choice of a deep, power-enhanced ResNet with SIREN activations (SQR-SkipResNet-SIREN) is not an arbitrary hyperparameter but a foundational requirement. It provides the necessary combination of expressive power to model complex trajectories, the high-fidelity derivatives needed for the physics loss, and the training stability required for deep networks. A simpler architecture will likely fail to converge or produce physically meaningful results.
-    \item \textbf{Training Dynamics are Paramount:} The chaotic nature of the problem and the composite structure of the loss function make the optimization landscape treacherous. A naive training loop will fail. The combination of an Adaptive Augmented Lagrangian Method for the physics loss, a curriculum-aware schedule for the energy loss, and adaptive gradient clipping is an essential suite of tools for ensuring stable, efficient, and robust convergence.
-    \item \textbf{Physics must be Multi-faceted:} Relying solely on a local physics residual is insufficient for ensuring the long-term plausibility of solutions to a chaotic system. The proposed framework combines the enforcement of the local, instantaneous ODEs ($\mathcal{L}_{\text{physics}}$) with the regularization of a global, conserved quantity ($\mathcal{L}_{\text{energy}}$). This multi-faceted approach to physics-informing the model provides a much stronger constraint, leading to solutions that are not only accurate in the short term but also maintain physical realism over long time horizons.
-\end{enumerate}
-
-By adhering to this detailed blueprint—from the principled choice of a hybrid architecture to the sophisticated engineering of the training dynamics—it is possible to successfully build and train a PINN for the $\mathrm{N}$-body problem that is accurate, physically plausible, and capable of stable, long-term predictions, representing a significant step forward in the application of machine learning to complex dynamical systems. The following table provides a final, consolidated summary for implementation.
-\end{comment}
 
 \begin{small}
 \begin{longtable}{|>{\raggedright\arraybackslash}p{0.18\textwidth}|>{\raggedright\arraybackslash}p{0.4\textwidth}|>{\raggedright\arraybackslash}p{0.4\textwidth}|}
@@ -833,7 +604,6 @@
 \hline
 \end{longtable}
 \end{small}
-
 \begin{thebibliography}{17}
     \bibitem{ref1} Power-enhanced ResNet for Function Approximation.pdf
     \bibitem{ref2} PIG: PHYSICS-INFORMED GAUSSIANS AS ADAPTIVE PARAMETRIC MESH REPRESENTATIONS - OpenReview, accessed June 25, 2025, \url{https://openreview.net/pdf/ba580795154cc26f5abe3ab4feab161a5246c2f3.pdf}
@@ -850,7 +620,8 @@
     \bibitem{ref13} Physics-Informed with Power-Enhanced Residual Network for Interpolation and Inverse Problems - ResearchGate, accessed June 25, 2025, \url{https://www.researchgate.net/publication/374946733_Physics-Informed_with_Power-Enhanced_Residual_Network_for_Interpolation_and_Inverse_Problems}
     \bibitem{ref14} Software | PNNL, accessed June 25, 2025, \url{https://www.pnnl.gov/projects/philms/software}
     \bibitem{ref15} lululxvi/deepxde: A library for scientific machine learning and physics-informed learning - GitHub, accessed June 25, 2025, \url{https://github.com/lululxvi/deepxde}
-    \bibitem{ref16} DeepXDE: A Deep Learning Library for Solving Differential Equations | SIAM Review - myqcloud.com, accessed June 25, 2025, \url{https://pdf-1307664364.cos.ap-chengdu.myqcloud.com/%E8%AE%BA%E6%96%87%E5%8F%82%E8%80%83/PINN/DeepXDE-%20A%20Deep%20Learning%20Library%20for%20Solving%20Differential%20Equations.pdf}
+    \bibitem{ref16} DeepXDE: A Deep Learning Library for Solving Differential Equations | SIAM Review - myqcloud.com, accessed June 25, 2025, \url{https://pdf-1307664364.cos.ap-chengdu.myqcloud.com/\%E8\%AE\%BA\%E6\%96\%87\%E5\%8F\%82\%E8\%80\%83/PINN/DeepXDE-\%20A\%20Deep\%20Learning\%20Library\%20for\%20Solving\%20Differential\%20Equations.pdf}
     \bibitem{ref17} omniscientoctopus/Physics-Informed-Neural-Networks: Investigating PINNs - GitHub, accessed June 25, 2025, \url{https://github.com/omniscientoctopus/Physics-Informed-Neural-Networks}
 \end{thebibliography}
 
+
```


### review_of_framework

```
--- review_of_framework/original
+++ review_of_framework/modular
@@ -42,6 +42,7 @@
     tabsize=2
 }
 \lstset{style=mystyle}
+
 \title{\textbf{A Technical Review and Resolution Blueprint for the CTL-PINN Framework for the Three-Body Problem}}
 \author{}
 \date{}
@@ -60,6 +61,7 @@
 The solutions presented are rigorously grounded in established principles from celestial mechanics, numerical analysis, and deep learning. The resulting blueprint ensures that the final CTL-PINN framework is not only physically sound and mathematically consistent but also computationally robust and practically implementable.
 
 \clearpage
+
 \section{Foundational Physical Metrics for Curriculum Design}
 The efficacy of the Curriculum-Transfer Learning (CTL) framework is predicated on the ability to quantitatively stratify simulation data by its intrinsic physical difficulty. Without robust and computable metrics to distinguish stable, quasi-periodic systems from highly chaotic ones, the concept of a "curriculum" remains ill-defined. This section resolves critical omissions in the source documents by providing definitive, physically-grounded formulas and scalable implementation plans for the key metrics required for stage assignment: Lyapunov time ($\tau_L$), maximum angular momentum ($L_{\max}$), and global normalization scales.
 
@@ -293,7 +295,7 @@
 - \textbf{Stages 4-6 (Fully Chaotic \& Extreme Cases):} \texttt{first\_omega\_0 = 10.0}
 
 \paragraph{Implementation Action:}
-At the beginning of each new curriculum stage, a targeted re-initialization will occur. While the weights of all hidden layers and the output layer are transferred from the converged model of the previous stage, the weights of the first SIREN layer will be re-initialized using the uniform distribution $U[-1/\sqrt{n_{\text{in}}}, 1/\sqrt{n_{\text{in}}}]$ and the new \texttt{first\_omega\_0} value specified by the schedule above. This procedure allows the model to adapt its "input lens" to the new data regime—adjusting its frequency sensitivity—without inducing catastrophic forgetting in the deeper layers of the network. This approach resolves the implementation ambiguity while preserving the original intent of adapting the network's frequency bias to the complexity of the learning task.
+At the beginning of each new curriculum stage, a targeted re-initialization will occur. While the weights of all hidden layers and the output layer are transferred from the converged model of the previous stage, the weights of the first SIREN layer will be re-initialized using the uniform distribution $U[-1/\sqrt{n_{\text{in}}}, 1/\sqrt{n_{\text{in}}}]$ and the new \texttt{first\_omega\_0} value specified by the schedule above. This procedure allows the model to adapt its "input lens" to the new data regime\textemdash adjusting its frequency sensitivity\textemdash without inducing catastrophic forgetting in the deeper layers of the network. This approach resolves the implementation ambiguity while preserving the original intent of adapting the network's frequency bias to the complexity of the learning task.
 
 \section{A Rigorous Framework for the Multi-Component Loss Function}
 The composite loss function is the heart of the PINN, guiding the network to solutions that are both accurate to data and consistent with physical law. This section provides definitive specifications for its implementation, resolving ambiguities in the use of scaled units, the state management of ALM parameters, the practical application of automatic differentiation, and the selection of a key hyperparameter in the energy regularization term.
@@ -301,7 +303,7 @@
 \subsection{Clarifying the Use of Scaled Quantities in All Loss Components}
 \textbf{Issue Resolved: 18}
 \paragraph{Context and Validation}
-Issue 18 correctly identifies the need for an explicit, unified confirmation that all three loss terms—$\mathcal{L}_{\text{data}}$, $\mathcal{L}_{\text{physics}}$, and $\mathcal{L}_{\text{energy}}$—are computed using the same dimensionless, scaled quantities. While the \texttt{PINN\_architecture\_plan.tex} document implies this consistency, the absence of a consolidated, emphatic statement creates a risk of subtle but critical implementation errors. Dimensional inconsistency between loss terms would lead to an improperly balanced optimization problem, where gradients from different terms are not on comparable scales, likely causing training to fail or converge to a physically incorrect solution.
+Issue 18 correctly identifies the need for an explicit, unified confirmation that all three loss terms\textemdash$\mathcal{L}_{\text{data}}$, $\mathcal{L}_{\text{physics}}$, and $\mathcal{L}_{\text{energy}}$\textemdash are computed using the same dimensionless, scaled quantities. While the \texttt{PINN\_architecture\_plan.tex} document implies this consistency, the absence of a consolidated, emphatic statement creates a risk of subtle but critical implementation errors. Dimensional inconsistency between loss terms would lead to an improperly balanced optimization problem, where gradients from different terms are not on comparable scales, likely causing training to fail or converge to a physically incorrect solution.
 
 \paragraph{Proposed Solution and Imple\-mentation}
 It is established as a definitive and non-negotiable requirement that all loss components be computed entirely within the non-dimensional, $G=1$ system of units defined in Section 2. The following checklist must be used to validate the implementation:
@@ -531,3 +533,4 @@
 \renewcommand{\arraystretch}{1.0}
 \end{table}
 
+
```


### stage_strat_revision

```
--- stage_strat_revision/original
+++ stage_strat_revision/modular
@@ -1,4 +1,3 @@
-
 \usepackage[utf8]{inputenc}
 \usepackage{amsmath, amssymb, amsfonts}
 \usepackage{graphicx}
@@ -57,12 +56,9 @@
 \title{A Data-Driven Stage Assignment Framework for Curriculum Transfer Learning in N-Body Dynamics}
 \author{An Award-Winning Writer}
 \date{\today}
-
-
 \begin{abstract}
 This report presents a comprehensive, revised workflow for a data-driven curriculum stratification framework tailored to a Physics-Informed Neural Network (PINN) project for the three-body problem. The proposed methodology moves beyond static, heuristic-based criteria towards an adaptive system that derives its structure from the empirical properties of the simulation dataset itself. This approach, grounded in machine learning best practices, combines dimensionality reduction (PCA), unsupervised clustering (K-Means/GMM), and quantile-based binning to create a robust, interpretable, and effective curriculum. The report details a multi-phase algorithmic workflow, provides reference implementations, and outlines a protocol for empirical validation, aiming to improve training stability and final model accuracy for complex, chaotic dynamical systems.
 \end{abstract}
-
 
 \part{Foundational Principles of Data-Driven Curriculum Stratification for Physical Systems}
 
@@ -135,7 +131,7 @@
 
 Principal Component Analysis (PCA) offers a principled method to address this. PCA is an orthogonal linear transformation that projects the data onto a new coordinate system, where the axes (principal components, PCs) are ordered by the amount of variance they explain in the original data.[9, 10] The first principal component (PC1) represents the direction of maximum variance in the feature space. In the context of our physical invariants, this component can often be interpreted as a composite "stability" or "difficulty" score.[5]
 
-For instance, if PC1 is found to be a linear combination with positive weights on $L_{\text{norm}}$ and $\tau_L$ and a negative weight on $|E|$, then a high score on PC1 would correspond to a system that is simultaneously regular, predictable, and not excessively bound—a clear signature of stability. By ranking simulations based on their PC1 score, one can create a continuous, one-dimensional difficulty axis that optimally combines the information from multiple correlated invariants. This data-driven approach is superior to manually constructing a composite score (e.g., $-E + L_{\text{norm}}$ [5]), as the weights are derived directly from the dataset's covariance structure, ensuring they are optimally tailored to the specific data distribution.[11, 12]
+For instance, if PC1 is found to be a linear combination with positive weights on $L_{\text{norm}}$ and $\tau_L$ and a negative weight on $|E|$, then a high score on PC1 would correspond to a system that is simultaneously regular, predictable, and not excessively bound---a clear signature of stability. By ranking simulations based on their PC1 score, one can create a continuous, one-dimensional difficulty axis that optimally combines the information from multiple correlated invariants. This data-driven approach is superior to manually constructing a composite score (e.g., $-E + L_{\text{norm}}$ [5]), as the weights are derived directly from the dataset's covariance structure, ensuring they are optimally tailored to the specific data distribution.[11, 12]
 
 \subsection{Unsupervised Clustering for Discovering Dynamical Regimes}
 
```
