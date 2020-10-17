import numpy as np 
from enum import Enum


class GameResult(Enum):
    NOT_FINISHED = 0
    NOUGHT_WIN = -1
    CROSS_WIN = 1
    DRAW = 3


BOARDDIM = 3
BOARDSIZE = BOARDDIM * BOARDDIM

EMPTY = 0
CROSS = 1
NOUGHT = -1

class Board:

    def __init__(self, p1, p2):
        self.state = np.zeros((BOARDDIM, BOARDDIM))
        self.board_hash = None
        self.is_game_over = False
        self.p1 = p1
        self.p2 = p2 
        self.cur_player_symbol = CROSS

    def get_board_hash(self):
        self.board_hash = str(self.state.reshape(BOARDSIZE))
        return self.board_hash

    def available_positions(self):
        positions = []
        for i in range(BOARDDIM):
            for j in range(BOARDDIM):
                if self.state[i, j] == EMPTY:
                    positions.append((i, j))
        return positions

    def check_winner(self):
        # check rows
        for i in range(BOARDDIM):
            if sum(self.state[i, :]) == CROSS*3:
                self.is_game_over = True
                return GameResult.CROSS_WIN
            elif sum(self.state[i, :]) == NOUGHT*3:
                self.is_game_over = True
                return GameResult.NOUGHT_WIN
        
        # check columns
        for i in range(BOARDDIM):
            if sum(self.state[:, i]) == CROSS*3:
                self.is_game_over = True
                return GameResult.CROSS_WIN
            elif sum(self.state[:, i]) == NOUGHT*3:
                self.is_game_over = True
                return GameResult.NOUGHT_WIN

        #diagonal
        forward_diagonal_sum = sum([self.state[i, i] for i in range(BOARDDIM)])
        backward_diagonal_sum = sum([self.state[i, BOARDDIM-(1+i)] for i in range(BOARDDIM)])
        if forward_diagonal_sum == CROSS*3 or backward_diagonal_sum == CROSS*3:
            self.is_game_over = True
            return GameResult.CROSS_WIN
        if forward_diagonal_sum == NOUGHT*3 or backward_diagonal_sum == NOUGHT*3:
            self.is_game_over = True
            return GameResult.NOUGHT_WIN

        if self.num_empty_positions() == 0:
            self.is_game_over = True
            return GameResult.DRAW

        return None
    

    def num_empty_positions(self):
        return np.count_nonzero(self.state == EMPTY)
    
    # def is_legal_move(self, pos):
    #     return (0 <= pos <= BOARDSIZE) and self.state[pos] == EMPTY

    def play_move(self, pos):
        if self.state[pos] != EMPTY:
            print("Illegal Move: Position Occupied")
        self.state[pos] = self.cur_player_symbol
        self.cur_player_symbol = CROSS if self.cur_player_symbol == NOUGHT else NOUGHT

    def give_reward(self):
        result = self.check_winner()
        if result == GameResult.CROSS_WIN:
            self.p1.feed_reward(1)
            self.p2.feed_reward(0)
        elif result == GameResult.NOUGHT_WIN:
            self.p2.feed_reward(1)
            self.p1.feed_reward(0)
        elif result == GameResult.DRAW:
            self.p1.feed_reward(0.1)
            self.p2.feed_reward(0.5)


    def reset_state(self):
        self.state = np.zeros((BOARDDIM, BOARDDIM))
        self.board_hash = None
        self.is_game_over = False
        self.cur_player_symbol = CROSS

    def print_board(self):
        # p1: x  p2: o
        for i in range(0, BOARDDIM):
            print('-------------')
            out = '| '
            for j in range(0, BOARDDIM):
                if self.state[i, j] == 1:
                    token = 'x'
                if self.state[i, j] == -1:
                    token = 'o'
                if self.state[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')

    def simulation(self, iterations=100):
        for i in range(iterations):
            if i%1000 == 0:
                print("Rounds {}".format(i))
            while not self.is_game_over:
                positions = self.available_positions()
                p1_action = self.p1.choose_action(positions, self.state, self.cur_player_symbol)
                self.play_move(p1_action)
                board_hash = self.get_board_hash()
                self.p1.add_move(board_hash)

                winner = self.check_winner()
                if winner is not None:
                    self.give_reward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset_state()
                    break
                else:
                    positions = self.available_positions()
                    p2_action = self.p2.choose_action(positions, self.state, self.cur_player_symbol)
                    self.play_move(p2_action)
                    board_hash = self.get_board_hash()
                    self.p2.add_move(board_hash)

                    winner = self.check_winner()
                    if winner is not None:
                        self.give_reward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset_state()
                        break
    
    def play2(self):
        while not self.is_game_over:
            # Player 1
            positions = self.available_positions()
            p1_action = self.p1.choose_action(positions, self.state, self.cur_player_symbol)
            # take action and upate board state
            self.play_move(p1_action)
            self.print_board()
            # check board status if it is end
            win = self.check_winner()
            if win is not None:
                if win == GameResult.CROSS_WIN:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset_state()
                break

            else:
                # Player 2
                positions = self.available_positions()
                p2_action = self.p2.chooseAction(positions)

                self.play_move(p2_action)
                self.print_board()
                win = self.check_winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset_state()
                    break

        

    


    
    
    





            


    