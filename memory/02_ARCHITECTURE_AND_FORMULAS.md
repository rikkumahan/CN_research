# 02. Architecture & Formulas

## 1. System Variants (Whiteboard A / B / C)

- **A (Base Paper)**: Pradhan et al. (IET 2022) — Single-objective PSO optimizing FFNN accuracy.
- **B (Senior Code)**: Budithi (2024/2025) — MOPSO-FFNN-AD on synthetic dataset (3,000 samples).
- **C (Upgraded System)**: Real traffic benchmarks (ISCX VPN 2016, USTC-TFC 2016) + 1D-CNN, LSTM, Transformer baselines + 10-fold CV + 3-policy ablation + feature importance.

---

## 2. FFNN Architecture

- **Layer Structure**: $8 \text{ (Input)} \to 16 \text{ (Hidden 1)} \to 8 \text{ (Hidden 2)} \to 5 \text{ (Output)}$
- **Parameter Count ($D$)**:
  $$D = (8 \times 16 + 16) + (16 \times 8 + 8) + (8 \times 5 + 5) = 144 + 136 + 45 = 325$$
- **Activations**: Hidden layers = ReLU, Output layer = Softmax.

---

## 3. Five-Component Composite Fitness Function ($F$)

$$F(\omega) = \alpha f_1 + \beta \cdot \text{FRUR} + \gamma \cdot F_{\text{CPU}} + \delta \cdot F_{\text{FSD}} + \epsilon \cdot F_{\text{BW}}$$

### Default Operator Weights:
- $\alpha = 0.45$ ($f_1$: classification error $1 - \text{Accuracy}$)
- $\beta = 0.20$ (FRUR: Flow-Rule Update Rate under noise $\sigma_n = 0.10$)
- $\gamma = 0.15$ ($F_{\text{CPU}}$: Active weight density, fraction $|w| > 0.3$)
- $\delta = 0.10$ ($F_{\text{FSD}}$: Flow Setup Delay, $\min(\frac{1}{3D}\sum |w|, 1.0)$)
- $\epsilon = 0.10$ ($F_{\text{BW}}$: Bandwidth reduction, fraction $|w| > 0.05$)

### Ablation Policy Weights:
1. **Accuracy-Critical**: $\alpha = 0.80, \beta=0.08, \gamma=0.06, \delta=0.03, \epsilon=0.03$
2. **Bandwidth-Constrained**: $\epsilon = 0.50, \alpha=0.25, \beta=0.10, \gamma=0.10, \delta=0.05$
3. **Latency-Sensitive**: $\delta = 0.50, \alpha=0.25, \beta=0.10, \gamma=0.10, \epsilon=0.05$

---

## 4. Page-Hinkley Drift Detector

Tracks error rate $x_n = 1 - \text{acc}_n$:
$$\mu_n = \frac{(n-1)\mu_{n-1} + x_n}{n}$$
$$U_n = U_{n-1} + x_n - \mu_n + \delta$$
$$PH_n = U_n - \min_{0 \le j \le n} U_j$$
Alarm triggers when $PH_n > \lambda$ (parameters: $\delta = 0.05$, $\lambda = 2.0$).

---

## 5. Mathematical Stability Proofs

### Lemma 1 (First-Order Convergence)
For particle position $q_s$ under velocity recurrence:
$$\mathbb{E}[q_s] = \frac{1}{2^s}(q_0 - p) + p \longrightarrow p \quad \text{as } s \to \infty$$
where $p$ is the weighted attractor.

### Lemma 2 (Second-Order Variance Convergence)
$$\text{Var}[q_s] = \frac{1}{4^s}\text{Var}[q_0] + \mathbb{E}[(q_0 - p)^2]\left(\frac{1}{3^s} - \frac{1}{4^s}\right) \longrightarrow 0 \quad \text{as } s \to \infty$$
Both first and second moments converge, proving MOPSO-FFNN-AD is stable and well-posed.

