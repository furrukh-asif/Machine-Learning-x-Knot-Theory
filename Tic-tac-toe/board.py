import numpy as np 


class Board:

    def __init__(self):
        self.rows = 3
        self.columns = 3
        self.state = np.zeros((self.rows, self.columns), dtype=int8)

    def get_state(self):
        return self.state

    def get_position(self, x, y):
        return self.state[x,y]

    def set_position(self, x, y, val):
        self.state[x,y] = val

    def get_available_moves(self):
        return np.argwhere(self.state == 0)

    def check_row_win(self, symbol):
        count = 0
        win = False
        for i in range(3):
            count = 0
            for j in range(3):
                if self.state[i, j] == symbol:
                    count += 1
            if count == 3:
                win == True
                break
        return win

    def check_column_win(self, symbol):
        count = 0
        win = False
        for i in range(3):
            count = 0
            for j in range(3):
                if self.state[j, i] == symbol:
                    count += 1
            if count == 3:
                win == True
                break
        return win

    def check_forward_diagonal_win(self, symbol):
        count = 0
        win = False
        for i in range(3):
            if self.state[i, i] == symbol:
                count += 1
        if count == 3:
            win = True
        return win

    def check_backward_diagonal_win(self, symbol):
        count = 0
        win = False
        idx1 = 0
        idx2 = 2
        for i in range(3):
            if self.state[idx1, idx2] == symbol:
                count += 1
            idx1 += 1
            idx2 -= 1
        if count == 3:
            win = True
        return win

    def is_game_won(self):
        symbols = [1, -1]

        for symbol in symbols:
            if check_row_win(symbol) or check_column_win(symbol) or check_forward_diagonal_win(symbol) or check_backward_diagonal_win(symbol):
                return symbol

        return 0

    def is_game_ended(self):
        return len(self.get_available_moves()) == 0

    def reset_state(self):
        self.state = np.zeros((self.rows, self.columns), dtype=int8)

            


    