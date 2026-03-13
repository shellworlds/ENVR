# SN-112BA: FedStress federated learning client stub. Main developer: shellworlds.
"""Privacy-preserving stress detection client; local training, aggregate weights only."""

import numpy as np
from typing import List, Tuple


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))


def local_stress_model(weights: np.ndarray, X: np.ndarray) -> np.ndarray:
    logits = X @ weights
    return sigmoid(logits)


def train_local_round(
    X: np.ndarray, y: np.ndarray, w: np.ndarray, lr: float = 0.01, steps: int = 10
) -> np.ndarray:
    w = w.copy()
    n = len(y)
    for _ in range(steps):
        pred = local_stress_model(w, X)
        grad = X.T @ (pred - y) / n
        w -= lr * grad
    return w


def fedstress_round(
    client_weights: List[np.ndarray],
) -> np.ndarray:
    return np.mean(client_weights, axis=0)


if __name__ == "__main__":
    np.random.seed(42)
    dim = 8
    X = np.random.randn(50, dim)
    y = (X @ np.random.randn(dim) + np.random.randn(50) * 0.1 > 0).astype(float)
    w0 = np.zeros(dim)
    w1 = train_local_round(X[:25], y[:25], w0)
    w2 = train_local_round(X[25:], y[25:], w0)
    w_agg = fedstress_round([w1, w2])
    pred = (local_stress_model(w_agg, X) > 0.5).astype(float)
    acc = (pred == y).mean()
    print("FedStress local round accuracy:", round(acc, 4))
