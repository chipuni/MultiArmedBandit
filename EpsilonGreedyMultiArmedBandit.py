from Generator import Generator
from MultiArmedBandit import MultiArmedBandit
from SimplestMultiArmedBandit import SimplestMultiArmedBandit


class EpsilonGreedyMultiArmedBandit(MultiArmedBandit):
    def __init__(self, generator1: Generator, generator2: Generator, epsilon: float):
        super().__init__(generator1, generator2)
        self._randomizer = Generator(0.5, 34567)
        self._epsilon = Generator(epsilon, 45678)
        self._simplest_mab = SimplestMultiArmedBandit(generator1, generator2)

    def choose_side(self):
        if self._epsilon.choose():
            if self._randomizer.choose():
                choice = 1
            else:
                choice = 2
        else:
            choice = self._simplest_mab.choose_side()
        return choice
