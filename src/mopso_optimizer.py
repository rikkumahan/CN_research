"""
src/mopso_optimizer.py
Particle Swarm Optimization & Multi-Objective PSO with Adaptive Drift Detection
Supports:
- Single-Objective PSO (Base Paper: Pradhan et al. 2022)
- Bi-Objective MOPSO with Multi-Scale Seeding (Senior: Budithi Supraja & Ours)
- Page-Hinkley Drift Detector (Tracks error rate 1 - acc)
- Configurable Deployment Policy Weights for Ablation
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import numpy as np
from sklearn.metrics import accuracy_score
from src.models import FFNN, DEFAULT_WEIGHTS

# ----------------------------------------------------------------------
# 1. Page-Hinkley Drift Detector (Patent Claim 3)
# ----------------------------------------------------------------------
class PageHinkley:
    """
    Sequential anomaly detection tracking error rate (1 - acc).
    Raises alarm when PH = U - U_min > lambda.
    """
    def __init__(self, delta=0.05, lam=2.0):
        self.delta = delta
        self.lam = lam
        self._reset()

    def _reset(self):
        self.mu = None
        self.U = 0.0
        self.Umin = 0.0
        self.n = 0

    def update(self, acc):
        err = 1.0 - acc
        self.mu = err if self.mu is None else (self.mu * self.n + err) / (self.n + 1)
        self.n += 1
        self.U += err - self.mu + self.delta
        self.Umin = min(self.Umin, self.U)
        PH = self.U - self.Umin
        if PH > self.lam:
            self._reset()
            return True, float(PH)
        return False, float(PH)


# ----------------------------------------------------------------------
# 2. Single-Objective PSO (Base Paper A: Pradhan et al. 2022)
# ----------------------------------------------------------------------
def pso_run(ffnn, Xfit, yfit, n_p=50, T=350,
            w0=0.9, wf=0.4, c1=1.5, c2=1.5,
            warm=None, verbose=False, tag="PSO"):
    """
    Standard single-objective PSO optimizing Cross-Entropy loss.
    """
    D = ffnn.D
    pos = np.random.randn(n_p, D) * np.sqrt(2.0 / ffnn.ni)
    if warm is not None:
        pos[0] = warm.copy()
        for k in range(1, min(6, n_p)):
            pos[k] = warm + np.random.randn(D) * 0.01

    vel = np.zeros((n_p, D))
    pb = pos.copy()
    pbf = np.array([ffnn.ce(Xfit, yfit, p) for p in pos])
    gi = np.argmin(pbf)
    gb = pb[gi].copy()
    gbf = pbf[gi]
    hist = []

    for t in range(T):
        w = w0 - (w0 - wf) * t / T
        r1 = np.random.rand(n_p, D)
        r2 = np.random.rand(n_p, D)
        vel = np.clip(w * vel + c1 * r1 * (pb - pos) + c2 * r2 * (gb - pos), -0.5, 0.5)
        pos = np.clip(pos + vel, -5.0, 5.0)

        for i in range(n_p):
            f = ffnn.ce(Xfit, yfit, pos[i])
            if f < pbf[i]:
                pbf[i] = f
                pb[i] = pos[i].copy()
            if f < gbf:
                gbf = f
                gb = pos[i].copy()

        hist.append(ffnn.acc(Xfit, yfit, gb))
        if verbose and (t + 1) % 100 == 0:
            print(f"  [{tag}] t={t+1:3d}/{T}  CE={gbf:.4f}  acc={hist[-1]:.4f}")

    return gb, hist


# ----------------------------------------------------------------------
# 3. MOPSO Archive & Dominance Utilities
# ----------------------------------------------------------------------
def _dom(a1, a2, b1, b2):
    return (a1 <= b1 and a2 <= b2) and (a1 < b1 or a2 < b2)

def _crowd(arc):
    n = len(arc)
    if n <= 2:
        return np.full(n, 1e9)
    f1v = np.array([s[1] for s in arc])
    Fv = np.array([s[2] for s in arc])
    cd = np.zeros(n)
    for fv in [f1v, Fv]:
        o = np.argsort(fv)
        sp = fv[o[-1]] - fv[o[0]] + 1e-12
        cd[o[0]] += 1e9
        cd[o[-1]] += 1e9
        for k in range(1, n - 1):
            cd[o[k]] += (fv[o[k + 1]] - fv[o[k - 1]]) / sp
    return cd

def _add(arc, sol, amax):
    # sol = [w, f1, F, f2, f3, f4, f5]
    for s in arc:
        if _dom(s[1], s[2], sol[1], sol[2]):
            return arc
    arc = [s for s in arc if not _dom(sol[1], sol[2], s[1], s[2])]
    arc.append(sol)
    if len(arc) > amax:
        arc.pop(int(np.argmin(_crowd(arc))))
    return arc

def _leader(arc):
    if len(arc) == 1:
        return arc[0][0]
    cd = _crowd(arc)
    pr = cd / cd.sum()
    return arc[int(np.random.choice(len(arc), p=pr))][0]


# ----------------------------------------------------------------------
# 4. Multi-Objective PSO with Multi-Scale Seeding (Senior B & Upgraded C)
# ----------------------------------------------------------------------
def mopso_run(ffnn, Xfit, yfit, Xvl, warm_w,
              weights=DEFAULT_WEIGHTS,
              n_p=55, T=300, amax=50,
              w0=0.9, wf=0.4, c1=2.0, c2=2.0,
              mu_p=0.12, mu_s=0.04, frur_every=5,
              verbose=False, tag="MOPSO"):
    """
    Bi-Objective MOPSO optimizing:
      Objective 1: f1 = Classification Error (1 - Accuracy)
      Objective 2: F  = Composite SDWN Overhead
    """
    D = ffnn.D
    scales = [1.0, 0.85, 0.70, 0.55, 0.40, 0.25, 0.12, 0.05]
    n_per_s = 6
    pos = np.zeros((n_p, D))

    idx = 0
    for sc in scales:
        for _ in range(n_per_s):
            if idx < n_p:
                noise = np.random.randn(D) * 0.03 * max(sc, 0.1)
                pos[idx] = warm_w * sc + noise
                idx += 1

    while idx < n_p:
        pos[idx] = np.random.randn(D) * np.sqrt(2.0 / ffnn.ni)
        idx += 1

    vel = np.zeros((n_p, D))
    pb = pos.copy()
    arc = []
    pbf1 = np.ones(n_p)
    pbF = np.full(n_p, np.inf)

    frur_cache = np.zeros(n_p)
    for i in range(n_p):
        f1 = ffnn.f1_err(Xfit, yfit, pos[i])
        f2 = ffnn.f2_frur(Xvl, pos[i])
        frur_cache[i] = f2
        f3 = ffnn.f3_cpu(pos[i])
        f4 = ffnn.f4_fsd(pos[i])
        f5 = ffnn.f5_bw(pos[i])
        F = (weights['alpha'] * f1 +
             weights['beta'] * f2 +
             weights['gamma'] * f3 +
             weights['delta'] * f4 +
             weights['epsilon'] * f5)
        pbf1[i] = f1
        pbF[i] = F
        arc = _add(arc, [pos[i].copy(), f1, F, f2, f3, f4, f5], amax)

    hist_acc, hist_F = [], []

    for t in range(T):
        w = w0 - (w0 - wf) * t / T
        lg = _leader(arc)
        r1 = np.random.rand(n_p, D)
        r2 = np.random.rand(n_p, D)
        vel = np.clip(w * vel + c1 * r1 * (pb - pos) + c2 * r2 * (lg - pos), -0.5, 0.5)
        pos = np.clip(pos + vel, -5.0, 5.0)

        if t % frur_every == 0:
            frur_cache = np.array([ffnn.f2_frur(Xvl, pos[i]) for i in range(n_p)])

        for i in range(n_p):
            f1 = ffnn.f1_err(Xfit, yfit, pos[i])
            f2 = frur_cache[i]
            f3 = ffnn.f3_cpu(pos[i])
            f4 = ffnn.f4_fsd(pos[i])
            f5 = ffnn.f5_bw(pos[i])
            F = (weights['alpha'] * f1 +
                 weights['beta'] * f2 +
                 weights['gamma'] * f3 +
                 weights['delta'] * f4 +
                 weights['epsilon'] * f5)

            if _dom(f1, F, pbf1[i], pbF[i]):
                pb[i] = pos[i].copy()
                pbf1[i] = f1
                pbF[i] = F
            elif not _dom(pbf1[i], pbF[i], f1, F) and np.random.rand() < 0.3:
                pb[i] = pos[i].copy()
                pbf1[i] = f1
                pbF[i] = F

            arc = _add(arc, [pos[i].copy(), f1, F, f2, f3, f4, f5], amax)

        # Archive mutation
        for s in arc:
            if np.random.rand() < mu_p:
                s[0] = np.clip(s[0] + np.random.randn(D) * mu_s, -5.0, 5.0)

        best = min(arc, key=lambda s: s[1])
        hist_acc.append(1.0 - best[1])
        hist_F.append(best[2])

        if verbose and (t + 1) % 80 == 0:
            print(f"  [{tag}] t={t+1:3d}/{T}  arch={len(arc):3d}  acc={hist_acc[-1]:.4f}  F={hist_F[-1]:.4f}")

    # Guaranteed injection of PSO warm-start
    f1w = ffnn.f1_err(Xfit, yfit, warm_w)
    f2w = ffnn.f2_frur(Xvl, warm_w)
    f3w = ffnn.f3_cpu(warm_w)
    f4w = ffnn.f4_fsd(warm_w)
    f5w = ffnn.f5_bw(warm_w)
    Fw = (weights['alpha'] * f1w +
          weights['beta'] * f2w +
          weights['gamma'] * f3w +
          weights['delta'] * f4w +
          weights['epsilon'] * f5w)
    arc = _add(arc, [warm_w.copy(), f1w, Fw, f2w, f3w, f4w, f5w], amax)

    return arc, hist_acc, hist_F


def deploy_knee(arc, ffnn, Xfit, yfit):
    """
    Returns the knee solution (highest accuracy member of non-dominated archive).
    """
    ev = [(i, ffnn.acc(Xfit, yfit, s[0]), s[2]) for i, s in enumerate(arc)]
    return arc[max(ev, key=lambda e: e[1])[0]]

