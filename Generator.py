from Assayer import Assayer
import numpy as np


class Generator(Assayer):
    def __init__(self, frac, seed):
        self._frac = frac
        self._seed = seed
        self._rng = None   # Only so that ._rng is in the constructor.
        self.reset()

    def choose(self) -> bool:
        result = self._rng.random() <= self._frac
        self.train(result)
        return result

    def reset(self):
        self._rng = np.random.default_rng(self._seed)
        self.hits = 0
        self.attempts = 0
