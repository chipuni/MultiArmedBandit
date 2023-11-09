from abc import ABC, abstractmethod


class Assayer:
    hits = 0
    attempts = 0

    def train(self, hit):
        self.attempts += 1
        if hit:
            self.hits += 1

    def get_hits(self):
        return self.hits

    def get_attempts(self):
        return self.attempts
