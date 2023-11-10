from Generator import Generator
from MultiArmedBandit import MultiArmedBandit


class FixedExplorationMultiArmedBandit(MultiArmedBandit):
    def __init__(self, generator1: Generator, generator2: Generator, count_exploration: int):
        super().__init__(generator1, generator2)
        self._count_exploration = count_exploration

    def choose_side(self):
        if self.generator1.get_attempts() + self.generator2.get_attempts() < self._count_exploration:
            # Exploration
            side1 = self.generator1.get_attempts()
            side2 = self.generator2.get_attempts()
            return self.convert_min_to_choice(side1, side2)
        else:
            # Exploitation
            side1 = self.generator1.mean()
            side2 = self.generator2.mean()
            return self.convert_max_to_choice(side1, side2)