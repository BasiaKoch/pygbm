"""
Unit tests for GBM simulator core logic.
"""

import pytest
import numpy as np
from pygbm import GBMSimulator, StochasticProcess


class TestGBMInitialization:
    """Test GBM simulator initialization."""

    def test_valid_initialization(self):
        """Test that valid parameters initialize correctly."""
        sim = GBMSimulator(y0=100.0, mu=0.05, sigma=0.2)
        assert sim.y0 == 100.0
        assert sim.mu == 0.05
        assert sim.sigma == 0.2

    def test_initialization_with_seed(self):
        """Test initialization with a random seed."""
        sim = GBMSimulator(y0=100.0, mu=0.05, sigma=0.2, seed=42)
        assert sim._seed == 42

    def test_invalid_y0_negative(self):
        """Test that negative y0 raises ValueError."""
        with pytest.raises(ValueError, match="Initial value y0 must be positive"):
            GBMSimulator(y0=-1.0, mu=0.05, sigma=0.2)

    def test_invalid_y0_zero(self):
        """Test that zero y0 raises ValueError."""
        with pytest.raises(ValueError, match="Initial value y0 must be positive"):
            GBMSimulator(y0=0.0, mu=0.05, sigma=0.2)

    def test_invalid_sigma_negative(self):
        """Test that negative sigma raises ValueError."""
        with pytest.raises(ValueError, match="Volatility sigma must be non-negative"):
            GBMSimulator(y0=100.0, mu=0.05, sigma=-0.1)

    def test_valid_sigma_zero(self):
        """Test that zero sigma is allowed (deterministic case)."""
        sim = GBMSimulator(y0=100.0, mu=0.05, sigma=0.0)
        assert sim.sigma == 0.0

    def test_is_stochastic_process(self):
        """Test that GBMSimulator is a StochasticProcess."""
        sim = GBMSimulator(y0=100.0, mu=0.05, sigma=0.2)
        assert isinstance(sim, StochasticProcess)


class TestGBMSimulation:
    """Test GBM path simulation."""

    def test_simulate_basic(self, basic_simulator, default_sim_params):
        """Test basic simulation returns correct array shapes."""
        t, y = basic_simulator.simulate_path(**default_sim_params)

        # Check shapes (N+1 points including t=0)
        assert len(t) == default_sim_params["N"] + 1
        assert len(y) == default_sim_params["N"] + 1

        # Check initial condition
        assert y[0] == basic_simulator.y0

        # Check time array
        assert t[0] == 0.0
        assert np.isclose(t[-1], default_sim_params["T"])

    def test_simulate_reproducibility(self, simulator_with_seed):
        """Test that simulation with same seed produces same results."""
        t1, y1 = simulator_with_seed.simulate_path(T=1.0, N=100, seed=42)
        t2, y2 = simulator_with_seed.simulate_path(T=1.0, N=100, seed=42)

        np.testing.assert_array_equal(t1, t2)
        np.testing.assert_array_equal(y1, y2)

    def test_simulate_positive_values(self, basic_simulator):
        """Test that GBM stays positive (as it should mathematically)."""
        t, y = basic_simulator.simulate_path(T=1.0, N=100)
        assert np.all(y > 0), "GBM values should always be positive"

    def test_simulate_zero_volatility(self):
        """Test simulation with zero volatility (deterministic case)."""
        sim = GBMSimulator(y0=100.0, mu=0.05, sigma=0.0, seed=42)
        t, y = sim.simulate_path(T=1.0, N=100)

        # With sigma=0, GBM is deterministic: Y(t) = y0 * exp(mu * t)
        expected = sim.y0 * np.exp(sim.mu * t)
        np.testing.assert_allclose(y, expected, rtol=1e-10)

    def test_simulate_invalid_T(self, basic_simulator):
        """Test that invalid T raises ValueError."""
        with pytest.raises(ValueError, match="T must be > 0"):
            basic_simulator.simulate_path(T=0.0, N=100)

        with pytest.raises(ValueError, match="T must be > 0"):
            basic_simulator.simulate_path(T=-1.0, N=100)

    def test_simulate_invalid_N(self, basic_simulator):
        """Test that invalid N raises ValueError."""
        with pytest.raises(ValueError, match="N must be >= 1"):
            basic_simulator.simulate_path(T=1.0, N=0)

        with pytest.raises(ValueError, match="N must be >= 1"):
            basic_simulator.simulate_path(T=1.0, N=-1)

    def test_simulate_single_step(self, basic_simulator):
        """Test simulation with N=1 (single step)."""
        t, y = basic_simulator.simulate_path(T=1.0, N=1)
        assert len(t) == 2
        assert len(y) == 2
        assert y[0] == basic_simulator.y0

    def test_simulate_different_time_horizons(self, basic_simulator):
        """Test simulations with different time horizons."""
        t1, y1 = basic_simulator.simulate_path(T=0.5, N=50)
        t2, y2 = basic_simulator.simulate_path(T=2.0, N=200)

        assert np.isclose(t1[-1], 0.5)
        assert np.isclose(t2[-1], 2.0)


class TestGBMStatisticalProperties:
    """Test statistical properties of GBM simulations."""

    def test_mean_approximation(self):
        """Test that sample mean approximates theoretical mean (Monte Carlo)."""
        sim = GBMSimulator(y0=100.0, mu=0.05, sigma=0.2, seed=42)

        # Run many simulations
        n_sims = 1000
        T = 1.0
        final_values = []

        for i in range(n_sims):
            _, y = sim.simulate_path(T=T, N=100, seed=i)
            final_values.append(y[-1])

        # Theoretical mean: E[Y(T)] = y0 * exp(mu * T)
        theoretical_mean = sim.y0 * np.exp(sim.mu * T)
        sample_mean = np.mean(final_values)

        # Allow 5% error for Monte Carlo approximation
        assert np.isclose(sample_mean, theoretical_mean, rtol=0.05)

    def test_monotonic_time(self, basic_simulator):
        """Test that time array is strictly increasing."""
        t, _ = basic_simulator.simulate_path(T=1.0, N=100)
        assert np.all(np.diff(t) > 0), "Time should be strictly increasing"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_small_y0(self):
        """Test with very small initial value."""
        sim = GBMSimulator(y0=1e-10, mu=0.05, sigma=0.2)
        t, y = sim.simulate_path(T=1.0, N=100)
        assert np.all(np.isfinite(y)), "All values should be finite"
        assert np.all(y > 0), "All values should be positive"

    def test_very_large_y0(self):
        """Test with very large initial value."""
        sim = GBMSimulator(y0=1e10, mu=0.05, sigma=0.2)
        t, y = sim.simulate_path(T=1.0, N=100)
        assert np.all(np.isfinite(y)), "All values should be finite"
        assert np.all(y > 0), "All values should be positive"

    def test_high_volatility(self):
        """Test with high volatility."""
        sim = GBMSimulator(y0=100.0, mu=0.05, sigma=2.0)
        t, y = sim.simulate_path(T=1.0, N=100)
        assert np.all(np.isfinite(y)), "All values should be finite"
        assert np.all(y > 0), "All values should be positive"

    def test_negative_drift(self):
        """Test with negative drift (mu < 0)."""
        sim = GBMSimulator(y0=100.0, mu=-0.1, sigma=0.2)
        t, y = sim.simulate_path(T=1.0, N=100)
        assert np.all(y > 0), "All values should be positive even with negative drift"
        assert y[0] == 100.0, "Initial value should be preserved"
