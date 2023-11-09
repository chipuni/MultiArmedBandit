from Generator import Generator
from MultiArmedBandit import MultiArmedBandit
from scipy.stats import beta


class BetaBinomialMultiArmedBandit(MultiArmedBandit):
    def __init__(self, generator1: Generator, generator2: Generator, frac: float):
        super().__init__(generator1, generator2)
        self._frac = frac

    def choose_side(self):
        beta1 = beta.ppf(self._frac, self.generator1.get_hits(), self.generator1.get_attempts() - self.generator1.get_hits())
        beta2 = beta.ppf(self._frac, self.generator2.get_hits(), self.generator2.get_attempts() - self.generator2.get_hits())
        return self.convert_max_to_choice(beta1, beta2)
