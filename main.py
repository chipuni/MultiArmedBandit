#!/usr/bin/env python3
import sys

from Assayer import Assayer
from BetaBinomialMultiArmedBandit import BetaBinomialMultiArmedBandit
from EpsilonGreedyMultiArmedBandit import EpsilonGreedyMultiArmedBandit
from FixedExplorationMultiArmedBandit import FixedExplorationMultiArmedBandit
from Generator import Generator
from SimplestMultiArmedBandit import SimplestMultiArmedBandit
from ThompsonMultiArmedBandit import ThompsonMultiArmedBandit


def count_hits(predictor: Assayer, attempts):
    for i in range(attempts):
        predictor.choose()

    return predictor.get_hits()


NUM_ATTEMPTS = 10000


def main(strMAB):
    correct_choices = Assayer()

    for rerun in range(30):
        for s in range(1, 20):
            smaller = s * 0.01

            smaller_generator = Generator(smaller, 12345 + rerun)

            for add in [0.001, 0.002, 0.005, 0.01, 0.02, 0.05]:
                larger = smaller + add
                larger_generator = Generator(larger, 67890 + rerun)

                smad1 = multi_armed_bandit_factory(strMAB, smaller_generator, larger_generator)
                smad1_hits = count_hits(smad1, NUM_ATTEMPTS)
                final_choice = smad1.choose_side()
                correct_choices.train(final_choice == 2)
                # display_results(smad1_hits, larger, larger_generator, smaller, smaller_generator, final_choice, 2)

                smad2 = multi_armed_bandit_factory(strMAB, larger_generator, smaller_generator)
                smad2_hits = count_hits(smad2, NUM_ATTEMPTS)
                final_choice = smad2.choose_side()
                correct_choices.train(final_choice == 1)
                # display_results(smad2_hits, larger, larger_generator, smaller, smaller_generator, final_choice, 1)

    print(f"Final correct choices: {correct_choices.get_hits()} / {correct_choices.get_attempts()}")


def display_results(smad1_hits, larger, larger_generator, smaller, smaller_generator, final_choice, correct_choice):
    print(f"Comparing generators with fraction hits at {smaller} and {larger}.")
    print(f"Multi-armed bandit hits {smad1_hits}")
    print(f"Final choice: {final_choice} (should be {correct_choice})")

    smaller_generator.reset()
    smaller_hits = count_hits(smaller_generator, NUM_ATTEMPTS)
    print(f"Smaller generator hits {smaller_hits}")
    larger_generator.reset()
    larger_hits = count_hits(larger_generator, NUM_ATTEMPTS)
    print(f"Larger generator hits {larger_hits}")
    print()


def multi_armed_bandit_factory(strMAB, firstGenerator, secondGenerator):
    if strMAB == "Simplest":
        return SimplestMultiArmedBandit(firstGenerator, secondGenerator)
    elif strMAB == "Epsilon":
        return EpsilonGreedyMultiArmedBandit(firstGenerator, secondGenerator, 0.04)
    elif strMAB == "Thompson":
        return ThompsonMultiArmedBandit(firstGenerator, secondGenerator)
    elif strMAB == "Beta":
        return BetaBinomialMultiArmedBandit(firstGenerator, secondGenerator, 0.95)
    elif strMAB == "Fixed":
        return FixedExplorationMultiArmedBandit(firstGenerator, secondGenerator, 200)
    print(f"Unknown multi-armed bandit requested: {strMAB}")
    return None


if __name__ == '__main__':
    main(sys.argv[1])
