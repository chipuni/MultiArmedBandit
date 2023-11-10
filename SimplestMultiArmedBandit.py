from MultiArmedBandit import MultiArmedBandit


class SimplestMultiArmedBandit(MultiArmedBandit):
    def choose_side(self):
        side1 = self.generator1.mean()
        side2 = self.generator2.mean()
        return self.convert_max_to_choice(side1, side2)
