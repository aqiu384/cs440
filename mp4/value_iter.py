import numpy as np
import matplotlib.pyplot as plt


def main():
    np.set_printoptions(suppress=True, precision=4, linewidth=300)

    SIZE = 6
    START = (4, 2)
    BLANK_REWARD = -0.04
    GAMMA = 0.99
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

    BASE_GRID = list(reversed(np.meshgrid(np.arange(1, SIZE+1), np.arange(1, SIZE+1))))
    UP_GRID = list(reversed(np.meshgrid(np.arange(1, SIZE+1), np.arange(0, SIZE))))
    RIGHT_GRID = list(reversed(np.meshgrid(np.arange(2, SIZE+2), np.arange(1, SIZE+1))))
    DOWN_GRID = list(reversed(np.meshgrid(np.arange(1, SIZE+1), np.arange(2, SIZE+2))))
    LEFT_GRID = list(reversed(np.meshgrid(np.arange(0, SIZE), np.arange(1, SIZE+1))))

    ALL_GRIDS = [np.empty((SIZE, SIZE, 4), dtype=np.uint8), np.empty((SIZE, SIZE, 4), dtype=np.uint8)]

    for index, grid in enumerate([UP_GRID, RIGHT_GRID, DOWN_GRID, LEFT_GRID]):
        diff = walls[BASE_GRID] - walls[grid]
        diff = (diff == 255)

        grid[0][diff] = BASE_GRID[0][diff]
        grid[1][diff] = BASE_GRID[1][diff]

        grid[0] -= 1
        grid[1] -= 1

        grid[0][grid[0] < 0] = 0
        grid[0][grid[0] > SIZE - 1] = SIZE - 1

        grid[1][grid[1] < 0] = 0
        grid[1][grid[1] > SIZE - 1] = SIZE - 1

        ALL_GRIDS[0][:, :, index] = grid[0]
        ALL_GRIDS[1][:, :, index] = grid[1]

    UP_WEIGHT = np.array([0.8, 0.1, 0, 0.1])
    RIGHT_WEIGHT = np.array([0.1, 0.8, 0.1, 0])
    DOWN_WEIGHT = np.array([0, 0.1, 0.8, 0.1])
    LEFT_WEIGHT = np.array([0.1, 0, 0.1, 0.8])

    ALL_WEIGHTS = list(enumerate([UP_WEIGHT, RIGHT_WEIGHT, DOWN_WEIGHT, LEFT_WEIGHT]))
    AVG_GRID = np.empty((SIZE, SIZE, 4))

    FLAG = False
    currs = [np.copy(costs), np.copy(costs)]

    ITERATIONS = 50
    utilities = np.empty((np.count_nonzero(masks), ITERATIONS + 1))
    utilities[:, 0] = currs[FLAG][masks]

    # 50, 1000
    for x in xrange(ITERATIONS):
        # print x
        DIR_GRID = currs[FLAG][ALL_GRIDS]

        for index, weight in ALL_WEIGHTS:
            AVG_GRID[:, :, index] = np.dot(DIR_GRID, weight)

        currs[not FLAG][masks] = (costs + GAMMA * np.amax(AVG_GRID, axis=2))[masks]
        FLAG = not FLAG

        utilities[:, x + 1] = currs[FLAG][masks]

    policy = np.uint8(np.argmax(currs[FLAG][ALL_GRIDS], axis=2))

    policy[policy == 0] = ord('^')
    policy[policy == 1] = ord('>')
    policy[policy == 2] = ord('v')
    policy[policy == 3] = ord('<')
    policy[np.invert(masks)] = ord('.')

    print currs[FLAG]
    print

    for i in xrange(SIZE):
        print policy[i, :].tostring()

    for i in xrange(np.count_nonzero(masks)):
        plt.plot(utilities[i])

    plt.show()

    return currs[FLAG]

if __name__ == '__main__':
    main()
