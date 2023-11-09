from Assayer import Assayer
import math
import numpy as np


class Generator(Assayer):
    def __init__(self, frac, seed):
        self._frac = frac
        self._seed = seed
        self._rng = None   # This line puts ._rng in the constructor.
        self.reset()

    def choose(self) -> bool:
        result = self._rng.random() <= self._frac
        self.train(result)
        return result

    def reset(self):
        self._rng = np.random.default_rng(self._seed)
        self.hits = 0
        self.attempts = 0

    def mean(self):
        return (self.get_hits() + 1) / (self.get_attempts() + 1)

    # This standard deviation comes from the fact that all values are either 0 or 1,
    # and 0*0 = 0 and 1*1 = 1.

    # The computational form of standard deviation can be found at
    # http://psychology.emory.edu/clinical/mcdowell/PSYCH560/Basics/var.html
    def stddev(self):
        if self.get_attempts() < 2:
            return 1.0
        else:
            return math.sqrt(( self.get_hits() - (self.get_hits() * self.get_hits() / self.get_attempts()) ) / (self.get_attempts() - 1) )
