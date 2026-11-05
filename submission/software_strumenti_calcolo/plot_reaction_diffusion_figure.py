#!/usr/bin/env python3
"""Generate the main reaction-diffusion scenario figure."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq
from scipy.special import k0


R0 = 10.0
THETA = 10.0 / 28.62
R_OX = 200.0


def concentration(radius: np.ndarray, length: float) -> np.ndarray:
    return k0(radius / length) / k0(R0 / length)


def critical_radius(length: float) -> float:
    crossing = brentq(lambda radius: concentration(np.array([radius]), length)[0] - THETA, R0, 10000.0)
    return float(crossing)


def main() -> None:
    output = Path(__file__).parents[1] / "figures" / "Figure1_reaction_diffusion_scenarios.png"
    radii = np.linspace(R0, 600.0, 1200)
    scenarios = [
        (400.0, "lambda = 400 um (IC50 = 10 nM)", "#376f9f"),
        (627.6, "lambda = 627.6 um (baseline; IC50 = 10 nM)", "#1f2937"),
        (800.0, "lambda = 800 um (IC50 = 10 nM)", "#d97706"),
        (3845.0, "lambda = 3845 um (48 h; IC50 = 10 nM)", "#8b3a62"),
    ]
    baseline_critical = critical_radius(627.6)

    figure, axis = plt.subplots(figsize=(9.0, 5.6), dpi=220)
    axis.axvspan(baseline_critical, R_OX, color="#e9b4cf", alpha=0.45, label="Conditional sub-threshold region (baseline)")
    axis.axvline(R_OX, color="#555555", linestyle="--", linewidth=1.8, label=r"Scenario viability boundary $r_{ox}=200$ um")
    axis.axhline(THETA, color="#c2410c", linestyle=":", linewidth=2.0, label=r"Inhibition threshold $theta=0.349$")

    for length, label, color in scenarios:
        axis.plot(radii, concentration(radii, length), color=color, linewidth=2.2, label=label)
        radius = critical_radius(length)
        if length == 3845.0:
            axis.axvline(radius, color=color, linestyle="-.", linewidth=1.4)
            axis.text(radius + 7, 0.58, r"$r_{crit}$ = 526 um", color=color, rotation=90, va="center", fontsize=9)

    axis.axvline(baseline_critical, color="#1f2937", linestyle="-.", linewidth=1.5)
    axis.text(baseline_critical + 5, 0.38, r"Baseline $r_{crit}$ = 166 um", color="#1f2937", rotation=90, va="center", fontsize=9)
    axis.text((baseline_critical + R_OX) / 2, 0.12, "conditional\nsub-threshold", ha="center", va="center", fontsize=9, color="#7c2d5a")
    axis.set_xlim(R0, 600)
    axis.set_ylim(0, 1.03)
    axis.set_xlabel(r"Radial distance from capillary wall, $r$ (um)")
    axis.set_ylabel(r"Normalized free concentration, $C(r)/C_0$")
    axis.set_title("Cylindrical reaction-diffusion penetration scenarios")
    axis.grid(True, color="#d1d5db", linewidth=0.7, alpha=0.7)
    axis.legend(loc="upper right", fontsize=8, frameon=True)
    figure.tight_layout()
    figure.savefig(output, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()