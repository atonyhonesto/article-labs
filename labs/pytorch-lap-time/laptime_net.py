"""A small PyTorch regression model for lap time, trained the careful way.

Standardised inputs, a held-out validation set, early stopping on validation
loss, and a saved checkpoint that carries its own normalisation statistics so
inference can't silently use the wrong scaling.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
from torch import nn

FEATURES = ["tire_age", "fuel_kg", "track_temp", "soft"]


def make_data(n: int = 4000, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    age = rng.integers(0, 35, n).astype(np.float32)
    fuel = rng.uniform(0, 100, n).astype(np.float32)
    temp = rng.uniform(20, 50, n).astype(np.float32)
    soft = rng.integers(0, 2, n).astype(np.float32)
    cliff = np.where((soft == 1) & (age > 18), 0.12 * np.clip(age - 18, 0, None) ** 1.3, 0.0)
    y = 90 - 0.7 * soft + 0.04 * age + 0.03 * fuel + 0.015 * (temp - 35) * age / 10 + cliff + rng.normal(0, 0.1, n)
    return np.stack([age, fuel, temp, soft], axis=1), y.astype(np.float32)


class LapTimeNet(nn.Module):
    def __init__(self, n_in: int = len(FEATURES), hidden: int = 32):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_in, hidden), nn.ReLU(), nn.Linear(hidden, hidden), nn.ReLU(),
                                 nn.Linear(hidden, 1))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)


@dataclass
class Trained:
    model: LapTimeNet
    x_mean: np.ndarray
    x_std: np.ndarray
    y_mean: float
    y_std: float
    epochs_run: int
    val_mae_s: float

    def predict(self, x: np.ndarray) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            z = torch.from_numpy(((x - self.x_mean) / self.x_std).astype(np.float32))
            return self.model(z).numpy() * self.y_std + self.y_mean

    def save(self, path: str) -> None:
        torch.save({"state": self.model.state_dict(), "x_mean": self.x_mean, "x_std": self.x_std,
                    "y_mean": self.y_mean, "y_std": self.y_std}, path)

    @staticmethod
    def load(path: str) -> "Trained":
        ck = torch.load(path, weights_only=False)
        m = LapTimeNet()
        m.load_state_dict(ck["state"])
        return Trained(m, ck["x_mean"], ck["x_std"], ck["y_mean"], ck["y_std"], 0, float("nan"))


def train(x: np.ndarray, y: np.ndarray, epochs: int = 300, patience: int = 20, seed: int = 0) -> Trained:
    torch.manual_seed(seed)
    idx = np.random.default_rng(seed).permutation(len(x))
    split = int(0.8 * len(x))
    tr, va = idx[:split], idx[split:]
    x_mean, x_std = x[tr].mean(0), x[tr].std(0) + 1e-6          # statistics from TRAINING data only
    y_mean, y_std = float(y[tr].mean()), float(y[tr].std())
    norm = lambda a: torch.from_numpy(((a - x_mean) / x_std).astype(np.float32))
    xt, xv = norm(x[tr]), norm(x[va])
    yt = torch.from_numpy((y[tr] - y_mean) / y_std)
    yv = torch.from_numpy((y[va] - y_mean) / y_std)

    model = LapTimeNet()
    opt = torch.optim.Adam(model.parameters(), lr=3e-3)
    loss_fn = nn.MSELoss()
    best, best_state, since_best, epoch = float("inf"), None, 0, 0
    for epoch in range(1, epochs + 1):
        model.train()
        perm = torch.randperm(len(xt))
        for i in range(0, len(xt), 256):
            b = perm[i:i + 256]
            opt.zero_grad()
            loss_fn(model(xt[b]), yt[b]).backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            val = loss_fn(model(xv), yv).item()
        if val < best - 1e-5:
            best, best_state, since_best = val, {k: v.clone() for k, v in model.state_dict().items()}, 0
        else:
            since_best += 1
            if since_best >= patience:
                break
    model.load_state_dict(best_state)
    trained = Trained(model, x_mean, x_std, y_mean, y_std, epoch, 0.0)
    trained.val_mae_s = float(np.abs(trained.predict(x[va]) - y[va]).mean())
    return trained
