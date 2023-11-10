from Assayer import Assayer
from Generator import Generator
from abc import ABC, abstractmethod


class MultiArmedBandit(Assayer):
    def __init__(self, generator1: Generator, generator2: Generator):
        self.generator1 = generator1
        self.generator2 = generator2
        self.coin_flip = Generator(0.5, 34567)

    def choose(self) -> bool:
        # Choose which side to use.

        choice = self.choose_side()

        if choice == 1:
            result = self.generator1.choose()
        else:
            result = self.generator2.choose()

        self.train(result)

        return result

    @abstractmethod
    def choose_side(self):
        pass

    def convert_max_to_choice(self, side1, side2):
        if side1 > side2:
            choice = 1
        elif side1 < side2:
            choice = 2
        else:
            if self.coin_flip.choose():
                choice = 1
            else:
                choice = 2
        return choice

    def convert_min_to_choice(self, side1, side2):
        if side1 > side2:
            choice = 2
        elif side1 < side2:
            choice = 1
        else:
            if self.coin_flip.choose():
                choice = 1
            else:
                choice = 2
        return choice