"""
pygbm - Geometric Brownian Motion Simulator Package

A Python package for simulating Geometric Brownian Motion (GBM) stochastic processes,
commonly used in financial modeling and other applications.
"""

from .gbm_simulator import GBMSimulator
from .base import StochasticProcess

__version__ = "0.1.0"
__all__ = ["GBMSimulator", "StochasticProcess"]
