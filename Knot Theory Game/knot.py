from copy import deepcopy
from kauffmanBracket import KauffmanBracket
import numpy as np
from enum import Enum


EMPTY = 0
UNCHANGED = 1
CHANGED = 2

KNOTTER = 3
UNKNOTTER = 4

class GameResult(Enum):
    NOT_FINISHED = 0
    KNOTTER_WIN = -1
    UNKNOTTER_WIN = 1


class Knot:

    def __init__(self, p1, p2, pd_code):
        self.knot = [pd_code, np.zeros(len(pd_code))]
        self.p1 = p1
        self.p2 = p2
        self.knot_hash = None
        self.is_game_over = False


    def get_knot_hash(self):
        self.knot_hash = str(self.knot[1])
        return self.knot_hash

    def available_moves(self):
        crossings = []
        for idx, crossing in enumerate(self.knot[1]):
            if crossing == EMPTY:
                crossings.append(idx)
        return crossings
        
    # move is a tuple of crossing index and boolean
    # indicating whether to chanhe the crossing or no 
    def play_move(self, move):
        crossing_idx, change = move
        if self.knot[1][crossing_idx] != EMPTY:
            print("check", crossing_idx)
            print("Illegal Move: Crossing Already Played")
        else:
            if change: 
                self.knot[1][crossing_idx] = CHANGED
                self.update_pd(crossing_idx)
            else:
                self.knot[1][crossing_idx] = UNCHANGED


    def check_game_over(self):
        num = 0
        for state in self.knot[1]:
            if state == EMPTY:
                num += 1
        if num == 0:
            return True
        return False

    def reset(self, pd_code):
        self.knot = [pd_code, np.zeros(len(pd_code))]
        self.is_game_over = False
        self.knot_hash = None

    def is_unknot(self, pd):
        kb=KauffmanBracket(pd)
        if len(kb[1])==1:
            return True
        return False

    def update_pd(self, crossing_idx):
        updated_pd = self.crossing_change(self.knot[0], crossing_idx)
        self.knot[0] = updated_pd


    def check_winner(self):
        if self.is_unknot(self.knot[0]):
            self.is_game_over = True
            return GameResult.UNKNOTTER_WIN
        elif self.check_game_over() == True:
            self.is_game_over = True
            return GameResult.KNOTTER_WIN
        return None


    def give_reward(self):
        result = self.check_winner()
        if result == GameResult.UNKNOTTER_WIN:
            self.p1.feed_reward(1)
            self.p2.feed_reward(0)
        elif result == GameResult.KNOTTER_WIN:
            self.p2.feed_reward(1)
            self.p1.feed_reward(0)


    def crossing_change(self, pd,cr):
        newpd=deepcopy(pd)
        if pd[cr][3]-pd[cr][1]==1 or pd[cr][3]-pd[cr][1]< -1:
            newpd[cr][0]=pd[cr][1]
            newpd[cr][1]=pd[cr][2]
            newpd[cr][2]=pd[cr][3]
            newpd[cr][3]=pd[cr][0]
        if pd[cr][1]-pd[cr][3]==1 or pd[cr][1]-pd[cr][3]< -1:
            newpd[cr][0]=pd[cr][3]
            newpd[cr][1]=pd[cr][0]
            newpd[cr][2]=pd[cr][1]
            newpd[cr][3]=pd[cr][2]
        return newpd



    def simulation(self, pd_code, iterations=100):
        for i in range(iterations):
            if i%1000 == 0:
                print("Rounds {}".format(i))
            while not self.is_game_over:
                positions = self.available_moves()
                p1_action = self.p1.choose_action(positions, self.knot)
                self.play_move(p1_action)
                knot_hash = self.get_knot_hash()
                self.p1.add_move(knot_hash)

                winner = self.check_winner()
                if winner is not None:
                    self.give_reward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset(pd_code)
                    break
                elif self.is_game_over:
                    break
                else:
                    positions = self.available_moves()
                    p2_action = self.p2.choose_action(positions, self.knot)
                    self.play_move(p2_action)
                    knot_hash = self.get_knot_hash()
                    self.p2.add_move(knot_hash)

                    winner = self.check_winner()
                    if winner is not None:
                        self.give_reward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset(pd_code)
                        break

    def play(self):
        while not self.is_game_over:
            # print("knot: ", self.knot)
            # Player 1
            positions = self.available_moves()
            p1_action = self.p1.choose_action(positions, self.knot)
            # take action and upate board state
            self.play_move(p1_action)
            # print(self.p1.name + ": ", p1_action)
            # check board status if it is end
            win = self.check_winner()
            if win is not None:
                # print("knot: ", self.knot)
                if win == GameResult.UNKNOTTER_WIN:
                    # print(self.p1.name, "wins!")
                    return self.p1.name
                elif win == GameResult.KNOTTER_WIN:
                    # print(self.p2.name, "wins!")
                    return self.p2.name
                break
            else:
                # print("knot: ", self.knot)
                # Player 2
                positions1 = self.available_moves()
                p2_action = self.p2.choose_action(positions1, self.knot)
                self.play_move(p2_action)
                # print(self.p2.name + ": ", p2_action)
                win = self.check_winner() 
                if win is not None:
                    # print("knot: ", self.knot)
                    if win == GameResult.KNOTTER_WIN:
                        # print(self.p2.name, "wins!")
                        return self.p2.name
                    elif win == GameResult.UNKNOTTER_WIN:
                        # print(self.p1.name, "wins!")
                        return self.p1.name
                    break