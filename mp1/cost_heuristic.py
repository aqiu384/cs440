import numpy as np
from Queue import PriorityQueue

LEFT_DIR = 1
RIGHT_DIR = 2
UP_DIR = 3
DOWN_DIR = 4

DIRECTIONS = {
    LEFT_DIR: 'L',
    RIGHT_DIR: 'R',
    UP_DIR: 'U',
    DOWN_DIR: 'D'
}

START_CHAR = 'P'
END_CHAR = '.'
WALL_CHAR = '%'
GHOST_CHAR = 'G'
PATH_CHAR = 'g'
WALL_INT = ord(WALL_CHAR)
PATH_INT = ord(PATH_CHAR)


class AstarQueue(PriorityQueue):
    def put(self, item, block=True, timeout=None):
        priority, curr_posn = item
        return PriorityQueue.put(self, (priority + curr_posn[3], curr_posn), block, timeout)


def cost_heuristic(input_file, move_cost=1, turn_cost=0, turn_heuristic=False):
    maze_file = open(input_file)

    maze_height = len(maze_file.readline()) - 1
    maze_width = sum(1 for _ in maze_file) + 1
    maze_file.seek(0)

    wall_array = np.empty((maze_width, maze_height), dtype=np.uint8)
    cost_array = np.zeros((maze_width, maze_height), dtype=np.uint8)
    visit_array = np.zeros((maze_width, maze_height), dtype=np.uint8)

    start_x = None
    start_y = None
    start_dir = RIGHT_DIR

    end_x = None
    end_y = None

    for row, line in enumerate(maze_file):
        if START_CHAR in line:
            start_x, start_y = row, line.find(START_CHAR)
        if END_CHAR in line:
            end_x, end_y = row, line.find(END_CHAR)
        wall_array[row] = np.fromstring(line[:-1], dtype=np.uint8)

    y_grid, x_grid = np.meshgrid(np.arange(maze_height), np.arange(maze_width))
    dist_array = np.tile(np.absolute(x_grid - end_x) + np.absolute(y_grid - end_y), (4, 1, 1)) * move_cost
    
    # if turn_heuristic:
    #     turns = np.ones((maze_width, maze_height), dtype=np.uint8) * turn_cost
    #
    #     up = np.copy(turns)
    #     up[:, end_y] = 0
    #     up[:end_x] = 2 * turn_cost
    #
    #     down = np.copy(turns)
    #     down[:, end_y] = 0
    #     down[end_x + 1:] = 2 * turn_cost
    #
    #     left = np.copy(turns)
    #     left[end_x] = 0
    #     left[:, :end_y] = 2 * turn_cost
    #
    #     right = np.copy(turns)
    #     right[end_x] = 0
    #     right[:, end_y + 1:] = 2 * turn_cost
    #
    #     dist_array[0] += left
    #     dist_array[1] += right
    #     dist_array[2] += up
    #     dist_array[3] += down

    turns = {
        UP_DIR: [
            (UP_DIR, -1, 0, move_cost),
            (DOWN_DIR, 1, 0, move_cost + 2 * turn_cost),
            (LEFT_DIR, 0, -1, move_cost + turn_cost),
            (RIGHT_DIR, 0, 1, move_cost + turn_cost)
        ],
        DOWN_DIR: [
            (UP_DIR, -1, 0, move_cost + 2 * turn_cost),
            (DOWN_DIR, 1, 0, move_cost),
            (LEFT_DIR, 0, -1, move_cost + turn_cost),
            (RIGHT_DIR, 0, 1, move_cost + turn_cost)
        ],
        LEFT_DIR: [
            (UP_DIR, -1, 0, move_cost + turn_cost),
            (DOWN_DIR, 1, 0, move_cost + turn_cost),
            (LEFT_DIR, 0, -1, move_cost),
            (RIGHT_DIR, 0, 1, move_cost + 2 * turn_cost)
        ],
        RIGHT_DIR: [
            (UP_DIR, -1, 0, move_cost + turn_cost),
            (DOWN_DIR, 1, 0, move_cost + turn_cost),
            (LEFT_DIR, 0, -1, move_cost + 2 * turn_cost),
            (RIGHT_DIR, 0, 1, move_cost)
        ]
    }

    frontier_count = 0

    frontier = AstarQueue()
    visit_array[start_x, start_y] = start_dir
    frontier.put_nowait((
        dist_array[start_dir - 1, start_x, start_y],
        (start_dir, start_x, start_y, 0, '')
    ))

    for _ in range(1000):
        priority, curr_posn = frontier.get_nowait()
        curr_dir, curr_x, curr_y, curr_cost, curr_steps = curr_posn

        cost_array[curr_x, curr_y] = curr_cost
        frontier_count += 1

        if curr_x == end_x and curr_y == end_y:
            return frontier_count, curr_cost, curr_steps

        for temp_dir, temp_dx, temp_dy, temp_cost in turns[curr_dir]:
            temp_x = curr_x + temp_dx
            temp_y = curr_y + temp_dy

            if wall_array[temp_x, temp_y] != WALL_INT and not visit_array[temp_x, temp_y]:
                visit_array[temp_x, temp_y] = temp_dir
                frontier.put_nowait((
                    dist_array[temp_dir - 1, temp_x, temp_y],
                    (temp_dir, temp_x, temp_y, curr_cost + temp_cost, curr_steps + DIRECTIONS[temp_dir])
                ))
