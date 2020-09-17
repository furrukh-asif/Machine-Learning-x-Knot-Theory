import numpy as np 
import pickle


class Agent:

    def __init__(self, name, alpha=0.2, gamma=0.95, q_init=0.6):
        self.name = name
        self.move_history = []
        self.learning_rate = alpha
        self.discount_value = gamma
        self.q_init_val = q_init
        self.q = {}

    def get_board_hash(self, board):
        board_hash = str(board.reshape(9))
        return board_hash

    def choose_action(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.q_init_val:
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            max_value = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_board_hash = self.get_board_hash(next_board)
                value = 0 if self.q.get(next_board_hash) is None else self.q.get(next_board_hash)
                if value >= max_value:
                    max_value = value
                    action = p
        return action 


    def add_move(self, move):
        self.move_history.append(move)


    def feed_reward(self, reward):
        for state in reversed(self.move_history):
            if self.q.get(state) is None:
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
        
