import random
import numpy as np

np.set_printoptions(suppress=True, precision=4, linewidth=300)

mapper = np.empty((9, 15), dtype=np.uint8)

with open('./inputs/map.txt') as map_file:
    for row, line in enumerate(map_file):
        mapper[row] = np.fromstring(line[:-1], dtype=np.uint8)

neg_weights = np.zeros((9, 15))
neg_weights[mapper != ord('W')] = -0.1

plus_weights = np.copy(neg_weights)
plus_weights[mapper == ord('S')] = 5

class Mover:
    def __init__(self, my_map, my_total):
        self.STUDENT = ord('S')
        self.GROCERY = ord('G')
        self.PIZZA = ord('P')
        self.WALL = ord('W')

        self.FORWARD = 0
        self.RIGHT = 1
        self.LEFT = 2
        self.STAY = 3
        self.NORMAL = 5
        
        self.NORTH = 0
        self.EAST = 1
        self.SOUTH = 2
        self.WEST = 3

        self.row = 6
        self.col = 2
        self.time = 0
        self.alpha = 1
        self.total = float(my_total)
        self.map = my_map

        self.groceries = True
        self.pizzas = False

        self.lookup = np.array([
            [[-1, 0], [0, 1], [0, -1], [0, 0]],
            [[0, 1], [1, 0], [-1, 0], [0, 0]],
            [[1, 0], [0, -1], [0, 1], [0, 0]],
            [[0, -1], [-1, 0], [1, 0], [0, 0]]
        ])

    def next_move(self, next_dir):
        my_rand = random.randint(0, 19)
        my_loc = self.map[self.row, self.col]
        my_reward = -0.1

        self.alpha = self.total / (self.total + self.time)
        self.time += 1

        his_dir = self.NORMAL

        if my_loc == self.PIZZA:
            if self.pizzas:
                if my_rand == 0:
                    his_dir = self.RIGHT
                elif my_rand == 1:
                    his_dir = self.LEFT
                elif 2 <= my_rand <= 7:
                    his_dir = self.STAY
                else:
                    his_dir = self.FORWARD
            else:
                if self.groceries:
                    self.pizzas = True
                    self.groceries = False
        elif my_loc == self.GROCERY:
            self.groceries = True
        elif my_loc == self.STUDENT and self.pizzas:
            self.pizzas = False
            my_reward = 5

        if his_dir == self.NORMAL:
            if my_rand == 0:
                his_dir = self.RIGHT
            elif my_rand == 1:
                his_dir = self.LEFT
            elif self.pizzas and 2 <= my_rand <= 5:
                his_dir = self.STAY
            else:
                his_dir = self.FORWARD

        next_row, next_col = self.lookup[next_dir, his_dir]

        if self.map[self.row + next_row, self.col + next_col] != self.WALL:
            self.row += next_row
            self.col += next_col

        return self.row, self.col, 2 * self.pizzas + self.groceries, my_reward

EXP_THRESH = 200
STEP_MAX = 100000
GAMMA = 0.99
ALPHA_SIZE = 50000

mover = Mover(mapper, ALPHA_SIZE)
trial_count = 0

qvals = np.zeros((9, 15, 4, 4))
nvals = np.zeros((9, 15, 4, 4), dtype=np.uint32)

# for i in xrange(2):
#     for j in xrange(4):
#         qvals[:, :, i, j] = neg_weights
#
# for i in xrange(2, 4):
#     for j in xrange(4):
#         qvals[:, :, i, j] = plus_weights

curr_row, curr_col, curr_state = 6, 2, 1

for _ in xrange(STEP_MAX):
    qcurr = qvals[curr_row, curr_col, curr_state]
    ncurr = nvals[curr_row, curr_col, curr_state]

    if any(ncurr < EXP_THRESH):
        my_dir = np.argmin(ncurr)
    else:
        my_dir = np.argmax(qcurr)

    next_row, next_col, next_state, curr_cost = mover.next_move(my_dir)
    qvals[curr_row, curr_col, curr_state, my_dir] += mover.alpha * (curr_cost - qvals[curr_row, curr_col, curr_state, my_dir] + GAMMA * np.max(qvals[next_row, next_col, next_state]))
    nvals[curr_row, curr_col, curr_state, my_dir] += 1

    curr_row, curr_col, curr_state = next_row, next_col, next_state

# for i in xrange(4):
#     print qvals[:, :, 1, i]
#     print

for i, typer in enumerate(['Nothing', 'Groceries', 'Pizza', 'Both']):
    print typer

    my_qvals = qvals[:, :, i, :]
    policy = np.uint8(np.argmax(my_qvals, axis=2))

    policy[policy == 0] = ord('^')
    policy[policy == 1] = ord('>')
    policy[policy == 2] = ord('v')
    policy[policy == 3] = ord('<')
    policy[mapper == ord('W')] = ord('.')

    # print np.amax(qvals, axis=2)

    for j in xrange(9):
        print policy[j, :].tostring()

    print