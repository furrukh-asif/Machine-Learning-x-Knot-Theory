import numpy as np 
import pickle
import timeit
from random import randint

EMPTY = 0
UNCHANGED = 1
CHANGED = 2


class Agent:

    def __init__(self, name, alpha=0.2, gamma=0.95, q_init=0.6):
        self.name = name
        self.move_history = []
        self.learning_rate = alpha
        self.discount_value = gamma
        self.q_init_val = q_init
        self.q = {}

    def get_knot_hash(self, knot):
        knot_hash = str(knot[1])
        return knot_hash

    def choose_action(self, available_moves, current_knot):
        action = None
        if np.random.uniform(0, 1) <= self.q_init_val:
            random_idx = randint(0, len(available_moves)-1)
            crossing_idx = available_moves[random_idx]
            change = False
            if np.random.uniform(0, 1) < 0.5:
                change = True
            action = (crossing_idx, change)
        else:
            max_value = -999
            for crossing_idx in available_moves:
                change_knot = False
                for i in range(2):
                    new_state = current_knot[1].copy()
                    if change_knot:
                        new_state[crossing_idx] = CHANGED
                    else:
                        new_state[crossing_idx] = UNCHANGED
                    next_knot_hash = self.get_knot_hash(new_state)
                    value = 0 if self.q.get(next_knot_hash) is None else self.q.get(next_knot_hash)
                    if value > max_value:
                        max_value = value
                        action = (crossing_idx, change_knot)
                    change_knot = True
        return action 


    def add_move(self, move):
        self.move_history.append(move) 


    def feed_reward(self, reward):
        for state in reversed(self.move_history):
            if state not in self.q:
                self.q[state] = 0
            self.q[state] += self.learning_rate*(self.discount_value*reward - self.q[state])
            reward = self.q[state]

    def reset(self):
        self.move_history = []
        
    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.q, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file,'rb')
        self.q = pickle.load(fr)
        fr.close()
        
