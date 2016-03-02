import numpy as np
import value_iter
import random
import matplotlib.pyplot as plt

def main():
    value_result = value_iter.main()

    random.seed(0)

    np.set_printoptions(suppress=True, precision=4, linewidth=300)

    SIZE = 6
    START = (4, 2)
    BLANK_REWARD = -0.04
    R_PLUS = 3.0
    WALL_FLAG = -9

    walls = np.ones((SIZE+2, SIZE+2), dtype=np.uint8)
    masks = np.ones((SIZE, SIZE), dtype=bool)
    costs = np.ones((SIZE, SIZE), dtype=np.float32)

    with open('./inputs/wall.txt') as wall_file:
        for row, line in enumerate(wall_file, 1):
            for col, num in enumerate(line.split(), 1):
                walls[row, col] = int(num)

    with open('./inputs/mask.txt') as mask_file:
        for row, line in enumerate(mask_file):
            for col, num in enumerate(line.split()):
                masks[row, col] = not int(num)

    with open('./inputs/maze.txt') as cost_file:
        for row, line in enumerate(cost_file):
            for col, num in enumerate(line.split()):
                cost = int(num)

                if cost != 0:
                    costs[row, col] = int(num)
                else:
                    costs[row, col] = BLANK_REWARD

    costs[costs == WALL_FLAG] = 0


    class Mover:
        def __init__(self, my_walls, my_total, my_costs):
            self.start_row = 3
            self.start_col = 1
            self.row = self.start_row
            self.col = self.start_col
            self.time = 0
            self.alpha = 1
            self.total = float(my_total)
            self.walls = my_walls
            self.costs = my_costs

        def reset(self):
            self.row = start_row
            self.col = start_col

        def next_move(self, next_dir):
            my_x = random.randint(0, 9)

            self.alpha = self.total / (self.total + self.time)
            self.time += 1

            row_del = 0
            col_del = 0

            if next_dir == 0:
                if my_x == 0:
                    col_del = -1
                elif my_x == 9:
                    col_del = 1
                else:
                    row_del = -1
            elif next_dir == 1:
                if my_x == 0:
                    row_del = -1
                elif my_x == 9:
                    row_del = 1
                else:
                    col_del = 1
            elif next_dir == 2:
                if my_x == 0:
                    col_del = 1
                elif my_x == 9:
                    col_del = -1
                else:
                    row_del = 1
            else:
                if my_x == 0:
                    row_del = 1
                elif my_x == 9:
                    row_del = -1
                else:
                    col_del = -1

            curr_cost = self.costs[self.row, self.col]

            if not self.walls[self.row + row_del + 1, self.col + col_del + 1]:
                self.row += row_del
                self.col += col_del

            return self.row, self.col, curr_cost

    # UP 0, RIGHT 1, DOWN 2, LEFT 3
    qvals = np.zeros((SIZE, SIZE, 4))
    nvals = np.zeros((SIZE, SIZE, 4))

    for x in xrange(4):
        qvals[:, :, x] = costs

    start_row, start_col = 3, 1
    curr_row, curr_col = start_row, start_col

    ITERATIONS = 100000
    EXP_THRESH = 200
    TRIAL_MAX = 7500
    GAMMA = 0.99
    ALPHA_SIZE = 5000

    rms = np.empty(TRIAL_MAX)

    mover = Mover(walls, ALPHA_SIZE, costs)
    trial_count = 0

    while trial_count < TRIAL_MAX:
        qcurr = qvals[curr_row, curr_col]
        ncurr = nvals[curr_row, curr_col]

        if any(ncurr < EXP_THRESH):
            my_dir = np.argmin(ncurr)
        else:
            my_dir = np.argmax(qcurr)

        next_row, next_col, curr_cost = mover.next_move(my_dir)
        qvals[curr_row, curr_col, my_dir] += mover.alpha * (curr_cost - qvals[curr_row, curr_col, my_dir] + GAMMA * np.max(qvals[next_row, next_col]))
        nvals[curr_row, curr_col, my_dir] += 1

        if masks[next_row, next_col]:
            curr_row, curr_col = next_row, next_col
        else:
            curr_row, curr_col = start_row, start_col
            mover.reset()

            td_results = np.amax(qvals, axis=2)
            rms[trial_count] = (sum(np.square(value_result - td_results).ravel()) / 24) ** 0.5

            trial_count += 1

    # for x in xrange(4):
    #     print nvals[:, :, x]
    #
    # for x in xrange(4):
    #     print qvals[:, :, x]

    policy = np.uint8(np.argmax(qvals, axis=2))

    policy[policy == 0] = ord('^')
    policy[policy == 1] = ord('>')
    policy[policy == 2] = ord('v')
    policy[policy == 3] = ord('<')
    policy[np.invert(masks)] = ord('.')

    print np.amax(qvals, axis=2)

    for i in xrange(4):
        print qvals[:, :, i]

    for i in xrange(SIZE):
        print policy[i, :].tostring()

    plt.plot(rms)
    plt.show()

    return np.amax(qvals, axis=2)

if __name__ == '__main__':
    main()