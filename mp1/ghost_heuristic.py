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

BACKTRACKS = {
    LEFT_DIR: 'RL',
    RIGHT_DIR: 'LR',
    UP_DIR: 'DU',
    DOWN_DIR: 'UD'
}

START_CHAR = 'P'
END_CHAR = '.'
WALL_CHAR = '%'
GHOST_CHAR = 'G'
PATH_CHAR = 'g'
WALL_INT = ord(WALL_CHAR)
PATH_INT = ord(PATH_CHAR)

MOVE_COST = 1
TURN_COST = 0


class AstarQueue(PriorityQueue):
    def put(self, item, block=True, timeout=None):
        priority, curr_posn = item
        return PriorityQueue.put(self, (priority + curr_posn[3], curr_posn), block, timeout)


def ghost_heuristic(input_file):
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

    ghost_x = None
    start_ghost_y = 0
    start_ghost_dy = 1

    for row, line in enumerate(maze_file):
        if START_CHAR in line:
            start_x, start_y = row, line.find(START_CHAR)
        if END_CHAR in line:
            end_x, end_y = row, line.find(END_CHAR)
        if GHOST_CHAR in line:
            ghost_x, start_ghost_y = row, line.find(GHOST_CHAR)
        wall_array[row] = np.fromstring(line[:-1], dtype=np.uint8)

    y_grid, x_grid = np.meshgrid(np.arange(maze_height), np.arange(maze_width))
    dist_array = np.tile(np.absolute(x_grid - end_x) + np.absolute(y_grid - end_y), (4, 1, 1))

    turns = {
        UP_DIR: [
            (UP_DIR, -1, 0, MOVE_COST),
            (DOWN_DIR, 1, 0, MOVE_COST + 2 * TURN_COST),
            (LEFT_DIR, 0, -1, MOVE_COST + TURN_COST),
            (RIGHT_DIR, 0, 1, MOVE_COST + TURN_COST)
        ],
        DOWN_DIR: [
            (UP_DIR, -1, 0, MOVE_COST + 2 * TURN_COST),
            (DOWN_DIR, 1, 0, MOVE_COST),
            (LEFT_DIR, 0, -1, MOVE_COST + TURN_COST),
            (RIGHT_DIR, 0, 1, MOVE_COST + TURN_COST)
        ],
        LEFT_DIR: [
            (UP_DIR, -1, 0, MOVE_COST + TURN_COST),
            (DOWN_DIR, 1, 0, MOVE_COST + TURN_COST),
            (LEFT_DIR, 0, -1, MOVE_COST),
            (RIGHT_DIR, 0, 1, MOVE_COST + 2 * TURN_COST)
        ],
        RIGHT_DIR: [
            (UP_DIR, -1, 0, MOVE_COST + TURN_COST),
            (DOWN_DIR, 1, 0, MOVE_COST + TURN_COST),
            (LEFT_DIR, 0, -1, MOVE_COST + 2 * TURN_COST),
            (RIGHT_DIR, 0, 1, MOVE_COST)
        ]
    }

    frontier_count = 0
    final_steps = None

    frontier = AstarQueue()
    frontier.put_nowait((
        dist_array[start_dir - 1, start_x, start_y],
        (start_dir, start_x, start_y, 0, start_ghost_y, start_ghost_dy, '')
    ))

    try:
        for _ in range(1000):
            priority, curr_posn = frontier.get_nowait()
            curr_dir, curr_x, curr_y, curr_cost, ghost_y, ghost_dy, curr_steps = curr_posn

            if ghost_x and wall_array[ghost_x, ghost_y + ghost_dy] == WALL_INT:
                ghost_dy *= -1

            visit_array[curr_x, curr_y] = curr_dir
            cost_array[curr_x, curr_y] = curr_cost
            frontier_count += 1

            if curr_x == end_x and curr_y == end_y:
                final_steps = curr_steps
                raise IndexError('Found a path')

            for temp_dir, temp_dx, temp_dy, temp_cost in turns[curr_dir]:
                temp_x = curr_x + temp_dx
                temp_y = curr_y + temp_dy

                if wall_array[temp_x, temp_y] != WALL_INT and not visit_array[temp_x, temp_y]:
                    if temp_x == ghost_x and curr_x == ghost_x and temp_y == ghost_y and curr_y == ghost_y + ghost_dy:
                        continue
                    elif temp_x == ghost_x and temp_y == ghost_y + ghost_dy:
                        if curr_x != ghost_x or curr_y != ghost_y + 2 * ghost_dy:
                            if wall_array[ghost_x, ghost_y + 2 * ghost_dy] == WALL_INT:
                                new_dy = ghost_dy
                            else:
                                new_dy = -1 * ghost_dy

                            frontier.put_nowait((
                                dist_array[temp_dir - 1, temp_x, temp_y] + 1,
                                (curr_dir, curr_x, curr_y, curr_cost, ghost_y + ghost_dy + new_dy, new_dy, curr_steps + BACKTRACKS[curr_dir])
                            ))
                    else:
                        frontier.put_nowait((
                            dist_array[temp_dir - 1, temp_x, temp_y],
                            (temp_dir, temp_x, temp_y, curr_cost + temp_cost, ghost_y + ghost_dy, ghost_dy, curr_steps + DIRECTIONS[temp_dir])
                        ))
    except IndexError:
        return frontier_count, final_steps
