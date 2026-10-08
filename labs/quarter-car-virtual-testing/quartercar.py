"""Quarter-car model: the smallest vehicle model that shows the ride-vs-grip trade-off.

Two masses on two springs:
    sprung mass  ms (a quarter of the body) on the suspension spring ks and damper cs
    unsprung mass mu (wheel, hub, brake) on the tyre spring kt
    road profile zr(t) pushes the tyre from below

    ms * zs'' = -ks (zs - zu) - cs (zs' - zu')
    mu * zu'' =  ks (zs - zu) + cs (zs' - zu') - kt (zu - zr)

Three numbers judge a setup, the way a virtual test rig (MSC Adams, Simulink) would:
    comfort      RMS body acceleration            (lower is better)
    road holding RMS dynamic tyre load / static   (lower is better: steadier grip)
    travel       peak suspension deflection       (must stay inside the bump stops)
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

G = 9.81


@dataclass
class Car:
    ms: float = 300.0        # kg, quarter of the body
    mu: float = 40.0         # kg
    ks: float = 25_000.0     # N/m
    kt: float = 250_000.0    # N/m
    cs: float = 1_800.0      # N·s/m

    @property
    def critical_damping(self) -> float:
        return 2 * (self.ks * self.ms) ** 0.5

    @property
    def body_hz(self) -> float:
        k = self.ks * self.kt / (self.ks + self.kt)
        return (k / self.ms) ** 0.5 / (2 * np.pi)


def bump(height=0.05, length=2.0, speed=10.0, start=0.5):
    """A smooth (1 - cos) speed bump, as a function of time at the given speed (m, m, m/s)."""
    dur = length / speed
    def zr(t):
        tt = np.clip((np.asarray(t) - start) / dur, 0, 1)
        return np.where((tt > 0) & (tt < 1), height / 2 * (1 - np.cos(2 * np.pi * tt)), 0.0)
    return zr


def rough_road(speed=25.0, seed=0, roughness=16e-6, n=200):
    """ISO 8608-style random road (class B-ish) built from a sum of sinusoids."""
    rng = np.random.default_rng(seed)
    freqs = np.linspace(0.011, 2.83, n)                     # spatial frequency, cycles/m
    dn = freqs[1] - freqs[0]
    psd = roughness * (freqs / 0.1) ** -2
    amp, phase = np.sqrt(2 * psd * dn), rng.uniform(0, 2 * np.pi, n)
    def zr(t):
        x = speed * np.atleast_1d(t)[:, None]
        return (amp * np.sin(2 * np.pi * freqs * x + phase)).sum(axis=1)
    return zr


def simulate(car: Car, road, t_end=3.0, fs=1000):
    t = np.arange(0, t_end, 1 / fs)
    def rhs(tt, y):
        zs, vs, zu, vu = y
        zr = float(np.squeeze(road(tt)))
        fsusp = car.ks * (zs - zu) + car.cs * (vs - vu)
        return [vs, -fsusp / car.ms, vu, (fsusp - car.kt * (zu - zr)) / car.mu]
    sol = solve_ivp(rhs, (0, t_end), [0, 0, 0, 0], t_eval=t, max_step=1 / fs, rtol=1e-6, atol=1e-9)
    zs, vs, zu, vu = sol.y
    zr = np.squeeze(road(t))
    acc = -(car.ks * (zs - zu) + car.cs * (vs - vu)) / car.ms
    tyre_load = car.kt * (zu - zr)                          # dynamic part of the tyre force
    static = (car.ms + car.mu) * G
    return {
        "comfort_rms_ms2": float(np.sqrt(np.mean(acc ** 2))),
        "grip_rms_pct": float(np.sqrt(np.mean(tyre_load ** 2)) / static * 100),
        "travel_mm": float(np.max(np.abs(zs - zu)) * 1000),
        "lost_contact": bool(np.any(tyre_load < -static)),   # dynamic unload larger than static load
    }


def sweep(car: Car, road, ratios=(0.1, 0.2, 0.3, 0.45, 0.7, 1.0), **kw):
    out = []
    for z in ratios:
        c = Car(car.ms, car.mu, car.ks, car.kt, z * car.critical_damping)
        out.append((z, c.cs, simulate(c, road, **kw)))
    return out
