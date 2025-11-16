from abc import ABC, abstractmethod
from typing import Tuple, Optional
import numpy as np

class StochasticProcess(ABC):
    def __init__(self, seed: Optional[int] = None) -> None:
        self._seed = seed

    @abstractmethod
    def simulate_path(self, T: float, N: int, seed: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        ...
