#!/usr/bin/env python3
import sys

from Assayer import Assayer
from BetaBinomialMultiArmedBandit import BetaBinomialMultiArmedBandit
from EpsilonGreedyMultiArmedBandit import EpsilonGreedyMultiArmedBandit
from FixedExplorationMultiArmedBandit import FixedExplorationMultiArmedBandit
from Generator import Generator
from SimplestMultiArmedBandit import SimplestMultiArmedBandit
from ThompsonMultiArmedBandit import ThompsonMultiArmedBandit

NUM_ATTEMPTS = 10000


def count_hits(predictor: Assayer, attempts):
    for i in range(attempts):
        predictor.choose()

    return predictor.get_hits()


def display_results(smad1_hits, larger, larger_generator : Generator, smaller, smaller_generator : Generator, final_choice, correct_choice):
    print(f"Comparing generators with fraction hits at {smaller} and {larger}.")
    print(f"Multi-armed bandit hits {smad1_hits}")
    print(f"Larger generator side: {larger_generator.get_hits()} / {larger_generator.get_attempts()}")
    print(f"Smaller generator side: {smaller_generator.get_hits()} / {smaller_generator.get_attempts()}")
    print(f"Final choice: {final_choice} (should be {correct_choice})")

    print()


def multi_armed_bandit_factory(str_mab, firstGenerator, secondGenerator, param):
    if str_mab == "Simplest":
        return SimplestMultiArmedBandit(firstGenerator, secondGenerator)
    elif str_mab == "Epsilon":
        return EpsilonGreedyMultiArmedBandit(firstGenerator, secondGenerator, float(param))
    elif str_mab == "Thompson":
        return ThompsonMultiArmedBandit(firstGenerator, secondGenerator)
    elif str_mab == "Beta":
        return BetaBinomialMultiArmedBandit(firstGenerator, secondGenerator, float(param))
    elif str_mab == "Fixed":
        return FixedExplorationMultiArmedBandit(firstGenerator, secondGenerator, int(param))
    print(f"Unknown multi-armed bandit requested: {str_mab}")
    return None


def main(str_mab, param):
    hits = 0
    smaller_hits = 0
    larger_hits = 0

    correct_choices = Assayer()

    for rerun in range(30):
        for s in range(1, 20):
            smaller = s * 0.01

            smaller_generator = Generator(smaller, 12345 + rerun)

            for add in [0.005, 0.01, 0.02, 0.05]:
                smaller_generator.reset()

                larger = smaller + add
                larger_generator = Generator(larger, 67890 + rerun)

                mab1 = multi_armed_bandit_factory(str_mab, smaller_generator, larger_generator, param)
                mab1_hits = count_hits(mab1, NUM_ATTEMPTS)
                hits += mab1_hits

                # Did it choose the correct side?
                final_choice = mab1.choose_side()
                correct_choices.train(final_choice == 2)

                # display_results(mab1_hits, larger, larger_generator, smaller, smaller_generator, final_choice, 2)

                smaller_generator.reset()
                smaller_hits += count_hits(smaller_generator, NUM_ATTEMPTS)

                larger_generator.reset()
                larger_hits += count_hits(larger_generator, NUM_ATTEMPTS)

                smaller_generator.reset()
                larger_generator.reset()

                mab2 = multi_armed_bandit_factory(str_mab, larger_generator, smaller_generator, param)
                mab2_hits = count_hits(mab2, NUM_ATTEMPTS)
                hits += mab2_hits

                # Did it choose the correct side?
                final_choice = mab2.choose_side()
                correct_choices.train(final_choice == 1)

                # display_results(mab2_hits, larger, larger_generator, smaller, smaller_generator, final_choice, 1)

                smaller_generator.reset()
                smaller_hits += count_hits(smaller_generator, NUM_ATTEMPTS)

                larger_generator.reset()
                larger_hits += count_hits(larger_generator, NUM_ATTEMPTS)

                smaller_generator.reset()
                larger_generator.reset()


    print(f"Final correct choices: {correct_choices.get_hits()} / {correct_choices.get_attempts()}")
    print(f"Final hits: {hits}. The smaller would be {smaller_hits} and the larger would be {larger_hits}.")
    print(f"This gives an accuracy of {(hits - smaller_hits) / (larger_hits - smaller_hits)}")

if __name__ == '__main__':
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        main(sys.argv[1], None)
