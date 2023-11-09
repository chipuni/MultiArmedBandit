from Generator import Generator
from MultiArmedBandit import MultiArmedBandit

import scipy.stats
import time


class ThompsonMultiArmedBandit(MultiArmedBandit):
    def choose_side(self):
        # The probability that a side should be chosen should match the probability that the
        # side has the higher average.
        mean1 = self.generator1.mean()
        std1 = self.generator1.stddev()
        nobs1 = self.generator1.get_attempts()

        mean2 = self.generator2.mean()
        std2 = self.generator2.stddev()
        nobs2 = self.generator2.get_attempts()

        # What is the chance that generator1's mean is greater than generator2's mean?
        probability = scipy.stats.ttest_ind_from_stats(mean1=mean1, std1=std1, nobs1=nobs1, mean2=mean2, std2=std2, nobs2=nobs2, equal_var=False, alternative='less').pvalue
        chooser = Generator(probability, time.time_ns())
        if chooser.choose():
            return 1
        else:
            return 2