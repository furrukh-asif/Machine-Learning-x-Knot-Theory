from random import randint
import numpy as np

class RandomPlayer:
    def __init__(self, name):
        self.name = name 

    def choose_action(self, available_moves, current_knot):
        random_idx = randint(0, len(available_moves)-1)
        crossing_idx = available_moves[random_idx]
        change = False
        if np.random.uniform(0, 1) < 0.5:
                change = True
        return (crossing_idx, change)