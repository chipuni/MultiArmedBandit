# UCB comes from https://cse442-17f.github.io/LinUCB/
from MultiArmedBandit import MultiArmedBandit
import math


class UCBMultiArmedBandit(MultiArmedBandit):
    def choose_side(self):
        # We need at least one attempt on each side.
        if self.generator1.get_attempts() == 0:
            return 1
        if self.generator2.get_attempts() == 0:
            return 2

        time = self.get_attempts()
        ucb1 = self.generator1.mean() + math.sqrt(2 * math.log(time) / self.generator1.get_attempts())
        ucb2 = self.generator2.mean() + math.sqrt(2 * math.log(time) / self.generator2.get_attempts())

        return self.convert_max_to_choice(ucb1, ucb2)
