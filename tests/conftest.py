"""
Pytest configuration and shared fixtures for pygbm tests.
"""

import pytest
import numpy as np
from pygbm import GBMSimulator


@pytest.fixture
def basic_simulator():
    """Fixture providing a basic GBM simulator instance."""
    return GBMSimulator(y0=100.0, mu=0.05, sigma=0.2)


@pytest.fixture
def simulator_with_seed():
    """Fixture providing a GBM simulator with fixed seed for reproducible tests."""
    return GBMSimulator(y0=100.0, mu=0.05, sigma=0.2, seed=42)


@pytest.fixture
def default_sim_params():
    """Fixture providing default simulation parameters."""
    return {
        "T": 1.0,
        "N": 100
    }


@pytest.fixture
def sample_gbm_request():
    """Fixture providing a sample GBM API request."""
    return {
        "y0": 100.0,
        "mu": 0.05,
        "sigma": 0.2,
        "T": 1.0,
        "N": 100
    }
