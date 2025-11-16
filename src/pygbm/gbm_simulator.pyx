from __future__ import annotations
from typing import Tuple, Optional
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from .base import StochasticProcess


class GBMSimulator(StochasticProcess):
    """
    Simulate paths of a Geometric Brownian Motion (GBM) process.

    dY_t = μ * Y_t * dt + σ * Y_t * dW_t
    where:
      μ = drift (expected return)
      σ = volatility
      W_t = standard Brownian motion
    """

    def __init__(self, y0: float, mu: float, sigma: float, seed: Optional[int] = None) -> None:
        """Initialize a GBM simulator."""
        super().__init__(seed=seed)
        if y0 <= 0:
            raise ValueError("Initial value y0 must be positive.")
        if sigma < 0:
            raise ValueError("Volatility sigma must be non-negative.")
        self.y0, self.mu, self.sigma = float(y0), float(mu), float(sigma)

    def simulate_path(
        self, T: float, N: int, seed: Optional[int] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simulate a GBM path over time horizon [0, T] using N steps.

        Returns:
            t (np.ndarray): time points
            y (np.ndarray): simulated GBM values
        """
        if T <= 0:
            raise ValueError("T must be > 0.")
        if N < 1:
            raise ValueError("N must be >= 1.")

        rng = np.random.default_rng(seed if seed is not None else self._seed)
        dt = T / N
        t = np.linspace(0.0, T, N + 1)
        z = rng.standard_normal(N)
        dW = np.sqrt(dt) * z
        W = np.concatenate(([0.0], np.cumsum(dW)))
        drift = (self.mu - 0.5 * self.sigma**2) * t
        diffusion = self.sigma * W
        y = self.y0 * np.exp(drift + diffusion)
        return t, y

    def plot_path(
        self,
        t: np.ndarray,
        y: np.ndarray,
        *,
        show: bool = True,
        output: Optional[str] = None
    ) -> None:
        """
        Plot the simulated GBM path.
        Args:
            t: time array
            y: simulated path
            show: display the plot interactively
            output: filename to save the plot
        """
        if output and not show:
            matplotlib.use("Agg", force=True)

        plt.figure()
        plt.plot(t, y, label="GBM Path")
        plt.xlabel("Time")
        plt.ylabel("Y(t)")
        plt.title("Geometric Brownian Motion Simulation")
        plt.legend()
        plt.grid(True)

        if output:
            plt.savefig(output, dpi=150)
            print(f"Plot saved to {output}")

        if show:
            plt.show()

        plt.close()

