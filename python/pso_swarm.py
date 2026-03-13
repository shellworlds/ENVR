# SN-112BA: Particle Swarm Optimization for swarm coordination. Main developer: shellworlds.
"""Decentralized PSO for spatial coordination POC."""

import numpy as np
from typing import Callable, Tuple


def pso_minimize(
    obj: Callable[[np.ndarray], float],
    dim: int,
    bounds: Tuple[float, float],
    n_particles: int = 30,
    max_iter: int = 100,
    w: float = 0.7,
    c1: float = 1.5,
    c2: float = 1.5,
) -> Tuple[np.ndarray, float]:
    lo, hi = bounds
    x = np.random.uniform(lo, hi, (n_particles, dim))
    v = np.zeros_like(x)
    pbest = x.copy()
    pbest_f = np.array([obj(p) for p in pbest])
    gidx = np.argmin(pbest_f)
    gbest = pbest[gidx].copy()
    gbest_f = pbest_f[gidx]

    for _ in range(max_iter - 1):
        r1, r2 = np.random.rand(2, n_particles, dim)
        v = w * v + c1 * r1 * (pbest - x) + c2 * r2 * (gbest - x)
        x = np.clip(x + v, lo, hi)
        f = np.array([obj(p) for p in x])
        better = f < pbest_f
        pbest[better] = x[better]
        pbest_f[better] = f[better]
        if pbest_f.min() < gbest_f:
            gidx = np.argmin(pbest_f)
            gbest = pbest[gidx].copy()
            gbest_f = pbest_f[gidx]
    return gbest, gbest_f


if __name__ == "__main__":
    def sphere(z): return np.sum(z**2)

    best, val = pso_minimize(sphere, dim=5, bounds=(-5, 5), max_iter=50)
    print("PSO sphere minimum:", round(val, 6), "at", np.round(best, 4))
