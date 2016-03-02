# coding=UTF8
from Tkinter import Tk, Button
from tkFont import Font
from Queue import PriorityQueue, Empty
from time import sleep

import numpy as np

YERS = np.array([-1, 1, 0, 0, 0])
XERS = np.array([0, 0, -1, 1, 0])

BEST_POS = 2 ** 16 - 1
BEST_NEG = -1 * 2 ** 16
SIZE = 6
DEPTH = 3

class Board:
    def __init__(self, board_file):
        self.player = 1
        self.opponent = -1
        self.empty = 0
        self.size = SIZE
        self.colors = {}
        self.values = []
        self.colors = np.zeros((SIZE + 2, SIZE + 2), dtype=np.int8)
        self.score = 0
        self.nodes_left = SIZE ** 2

        board_list = open(board_file, 'r')

        for line in board_list:
            self.values.append([int(x) for x in line.strip().split('\t')])

        self.values = np.array(self.values, dtype=np.uint8)
        self.values = np.pad(self.values, 1, 'constant', constant_values=0)

        # UP = self.values[:-2, 1:-1]
        # DOWN = self.values[2:, 1:-1]
        # LEFT = self.values[1:-1, :-2]
        # RIGHT = self.values[1:-1, 2:]
        # CENTER = self.values[1:-1, 1:-1]

        for y in xrange(1, self.size + 1):
            for x in xrange(1, self.size + 1):
                self.colors[x, y] = self.empty

    def move(self, x, y):
        y_cross = YERS + y
        x_cross = XERS + x

        my_cols = self.colors[y_cross, x_cross]
        my_inds = np.array([0, 0, 0, 0, self.player], dtype=np.int8)

        if any(my_cols == self.player):
            my_inds += (my_cols == self.opponent) * 2 * self.player

        self.score += np.dot(my_inds, self.values[y_cross, x_cross])
        self.colors[y_cross, x_cross] += my_inds
        self.nodes_left -= 1

        self.player, self.opponent = self.opponent, self.player

    def possible_moves(self, color):
        anti_color = -1 * color
        moves = PriorityQueue()

        for y in xrange(1, self.size + 1):
            for x in xrange(1, self.size + 1):
                if not self.colors[y, x]:
                    y_cross = YERS + y
                    x_cross = XERS + x

                    my_cols = self.colors[y_cross, x_cross]
                    my_inds = np.array([0, 0, 0, 0, color], dtype=np.int8)

                    if any(my_cols == color):
                        my_inds += (my_cols == anti_color) * 2 * color

                    priority = anti_color * np.dot(my_inds, self.values[y_cross, x_cross])
                    moves.put_nowait((priority, y, x, my_inds))

        return moves

    def negamax(self, depth, color, curr_score, nodes_left):
        if depth == 0 or nodes_left == 0:
            # print '\t' * 4 + str(color * curr_score)
            return color * curr_score, None

        best_value = BEST_NEG
        best_move = None

        moves = self.possible_moves(color)

        while True:
            try:
                priority, y, x, my_inds = moves.get_nowait()

                d_score = -1 * color * priority
                y_cross = YERS + y
                x_cross = XERS + x

                # print '\t' * (3 - depth) + str(curr_score + d_score) + ' ' + str(y) + ' ' + str(x)

                # if depth > 1:
                # print curr_score + d_score, y, x, my_inds

                self.colors[y_cross, x_cross] += my_inds
                val, move = self.negamax(depth - 1, -1 * color, curr_score + d_score, nodes_left - 1)
                val *= -1
                self.colors[y_cross, x_cross] -= my_inds

                # print '\t' * (3 - depth) + str(val) + ' ' + str(move)

                if val > best_value:
                    best_value = val
                    best_move = (y, x)

            except Empty:
                # print '\t' * (3 - depth) + str(best_value) + ' ' + str(best_move)
                return best_value, best_move

    def root_negamax(self):
        val, move = self.negamax(3, self.player, self.score, self.nodes_left)
        return self.player * val, move

    def negalphabeta(self, depth, alpha, beta, color, curr_score, nodes_left):
        if depth == 0 or nodes_left == 0:
            return color * curr_score, None

        best_value = BEST_NEG
        best_move = None

        moves = self.possible_moves(color)

        while True:
            try:
                priority, y, x, my_inds = moves.get_nowait()

                d_score = -1 * color * priority
                y_cross = YERS + y
                x_cross = XERS + x

                self.colors[y_cross, x_cross] += my_inds
                val, move = self.negalphabeta(depth - 1, -1 * beta, -1 * alpha, -1 * color, curr_score + d_score, nodes_left - 1)
                val *= -1
                self.colors[y_cross, x_cross] -= my_inds

                if val > best_value:
                    best_value = val
                    best_move = (y, x)

                alpha = max(alpha, val)
                if alpha >= beta:
                    break

            except Empty:
                break

        return best_value, best_move

    def root_negalphabeta(self):
        val, move = self.negalphabeta(DEPTH, BEST_NEG, BEST_POS, self.player, self.score, self.nodes_left)
        return self.player * val, move


COLORS = {
    -1: 'green',
    0: 'gray',
    1: 'light blue',
}


class GUI:
    def __init__(self):
        self.app = Tk()
        self.app.title('War Game')
        self.app.resizable(width=False, height=False)
        self.font = Font(family="Helvetica", size=32)
        self.buttons = {}
        self.board = Board('./boards/Smolensk.txt')
        self.size = SIZE

        for y in xrange(1, self.size + 1):
            for x in xrange(1, self.size + 1):
                handler = lambda x=x, y=y: self.move(x, y)
                button = Button(self.app, command=handler, font=self.font, width=3, height=1, text=self.board.values[y, x], background='gray')
                button.grid(row=y, column=x)
                self.buttons[x, y] = button

        handler = lambda: self.auto_move()
        button = Button(self.app, text='Start AI', command=handler)
        button.grid(row=self.size + 1, column=1, columnspan=self.size, sticky="WE")

    def auto_move(self):
        while self.board.nodes_left > 0:
            if self.board.player == 1:
                cost, (y, x) = self.board.root_negalphabeta()
            else:
                cost, (y, x) = self.board.root_negalphabeta()

            print 'Player: {} Heuristic {}'.format(self.board.player, cost)
            self.move(x, y)
            print 'Score: {}'.format(self.board.score)

    def move(self, x, y):
        self.app.config(cursor="watch")
        self.app.update()
        self.board.move(x, y)
        self.update(x, y)
        self.app.config(cursor="")

    def update(self, x, y):
        self.buttons[x, y]['state'] = 'disabled'
        for y in xrange(1, self.size + 1):
            for x in xrange(1, self.size + 1):
                self.buttons[x, y]['background'] = COLORS[self.board.colors[y, x]]
                self.buttons[x, y].update()

    def mainloop(self):
        self.app.mainloop()
 
if __name__ == '__main__':
    GUI().mainloop()