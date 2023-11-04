#!/usr/bin/env python3

from Assayer import Assayer
from Generator import Generator
from SimplestMultiArmedBandit import SimplestMultiArmedBandit


def count_hits(predictor: Assayer, attempts):
    for i in range(attempts):
        predictor.choose()

    return predictor.get_hits()


NUM_ATTEMPTS = 10000


def main():
    for s in range(1, 20):
        smaller = s * 0.01
        smaller_generator = Generator(smaller, 12345)

        for add in [0.001, 0.002, 0.005, 0.01, 0.02, 0.05]:
            larger = smaller + add
            larger_generator = Generator(larger, 67890)

            smad1 = SimplestMultiArmedBandit(smaller_generator, larger_generator)
            smad1_hits = count_hits(smad1, NUM_ATTEMPTS)
            print(f"Multi-armed bandit hits {smad1_hits}")

            smaller_generator.reset()
            smaller_hits = count_hits(smaller_generator, NUM_ATTEMPTS)
            print(f"Smaller generator hits {smaller_hits}")

            larger_generator.reset()
            larger_hits = count_hits(larger_generator, NUM_ATTEMPTS)
            print(f"Larger generator hits {larger_hits}")

            print()


if __name__ == '__main__':
    main()
