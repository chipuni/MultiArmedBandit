from Assayer import Assayer
from Generator import Generator


def safe_division(x, y):
    if y == 0:
        return 1.0
    else:
        return x / y


class SimplestMultiArmedBandit(Assayer):
    def __init__(self, generator1: Generator, generator2: Generator):
        self._randomizer = Generator(0.5, 34567)
        self._generator1 = generator1
        self._generator2 = generator2

    def choose(self) -> bool:
        # Choose which side to use.

        side1 = safe_division(self._generator1.get_hits(), self._generator2.get_attempts())
        side2 = safe_division(self._generator2.get_hits(), self._generator2.get_attempts())
        if side1 > side2:
            choice = 1
        elif side1 < side2:
            choice = 2
        else:
            if self._randomizer.choose():
                choice = 1
            else:
                choice = 2

        if choice == 1:
            result = self._generator1.choose()
        else:
            result = self._generator2.choose()

        self.train(result)

        return result
