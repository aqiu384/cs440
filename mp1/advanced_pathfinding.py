def basic_pathfinding(input_file, frontier_type, output_file, turn_cost=0, move_cost=1, turn_heuristic=False):
    TURN_COST = turn_cost
    MOVE_COST = move_cost

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

    maze_file = open(input_file)

    MAZE_HEIGHT = len(maze_file.readline()) - 1
    MAZE_WIDTH = sum(1 for _ in maze_file) + 1
    maze_file.seek(0)

    wall_array = np.empty((MAZE_WIDTH, MAZE_HEIGHT), dtype=np.uint8)
    cost_array = np.zeros((MAZE_WIDTH, MAZE_HEIGHT), dtype=np.uint8)
    visit_array = np.zeros((MAZE_WIDTH, MAZE_HEIGHT), dtype=np.uint8)

    START_CHAR = 'P'
    END_CHAR = '.'
    WALL_CHAR = '%'
    GHOST_CHAR = 'G'
    PATH_CHAR = 'g'
    WALL_INT = ord(WALL_CHAR)
    PATH_INT = ord(PATH_CHAR)

    START_X = None
    START_Y = None
    START_DIR = DOWN_DIR

    END_X = None
    END_Y = None

    GHOST_X = None
    START_GHOST_Y = 0
    START_GHOST_DY = 1

    for row, line in enumerate(maze_file):
        if START_CHAR in line:
            START_X, START_Y = row, line.find(START_CHAR)
        if END_CHAR in line:
            END_X, END_Y = row, line.find(END_CHAR)
        if GHOST_CHAR in line:
            GHOST_X, START_GHOST_Y = row, line.find(GHOST_CHAR)
        wall_array[row] = np.fromstring(line[:-1], dtype=np.uint8)

    Y_GRID, X_GRID = np.meshgrid(np.arange(MAZE_HEIGHT), np.arange(MAZE_WIDTH))
    dist_array = np.tile(np.absolute(X_GRID - END_X) + np.absolute(Y_GRID - END_Y), (4, 1, 1)) * MOVE_COST

    if turn_heuristic:
        TURNS = np.ones((MAZE_WIDTH, MAZE_HEIGHT), dtype=np.uint8) * TURN_COST

        UP = np.copy(TURNS)
        UP[:, END_Y] = 0
        UP[:END_X] = 2 * TURN_COST

        DOWN = np.copy(TURNS)
        DOWN[:, END_Y] = 0
        DOWN[END_X + 1:] = 2 * TURN_COST

        LEFT = np.copy(TURNS)
        LEFT[END_X] = 0
        LEFT[:, :END_Y] = 2 * TURN_COST

        RIGHT = np.copy(TURNS)
        RIGHT[END_X] = 0
        RIGHT[:, END_Y + 1:] = 2 * TURN_COST

        dist_array[0] += LEFT
        dist_array[1] += RIGHT
        dist_array[2] += UP
        dist_array[3] += DOWN

    frontier = frontier_type()
    frontier.put_nowait((dist_array[START_DIR - 1, START_X, START_Y], (DOWN_DIR, START_X, START_Y, 0, START_GHOST_Y, START_GHOST_DY, '')))

    FRONTIER_COUNT = 0
    PATH_COST = None
    MY_PATH = None

    TURNS = {
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

    try:
        for INDEX in range(1000):
            priority, curr_posn = frontier.get_nowait()
            curr_dir, curr_x, curr_y, curr_cost, ghost_y, ghost_dy, curr_steps = curr_posn

            # if not visit_array[curr_x, curr_y]:
            if GHOST_X:
                if wall_array[GHOST_X, ghost_y + ghost_dy] == WALL_INT:
                    ghost_dy *= -1
                if GHOST_X == curr_x and ghost_y + ghost_dy == curr_y:
                    wall_array[GHOST_X, ghost_y] = WALL_INT
                wall_array[GHOST_X, ghost_y + ghost_dy] = WALL_INT

            visit_array[curr_x, curr_y] = curr_dir
            cost_array[curr_x, curr_y] = curr_cost
            FRONTIER_COUNT += 1

            if curr_x == END_X and curr_y == END_Y:
                PATH_COST = curr_cost
                MY_PATH = curr_steps
                wall_array[GHOST_X, ghost_y] = PATH_INT
                wall_array[GHOST_X, ghost_y + ghost_dy] = ord(GHOST_CHAR)
                raise IndexError('Found a path')

            for temp_dir, temp_dx, temp_dy, temp_cost in TURNS[curr_dir]:
                temp_x = curr_x + temp_dx
                temp_y = curr_y + temp_dy

                if wall_array[temp_x, temp_y] != WALL_INT and cost_array[temp_x, temp_y] < curr_cost + temp_cost: # visit_array[temp_x, temp_y]:
                    frontier.put_nowait((
                        dist_array[temp_dir - 1, temp_x, temp_y],
                        (temp_dir, temp_x, temp_y, curr_cost + temp_cost, ghost_y + ghost_dy, ghost_dy, curr_steps + (DIRECTIONS[temp_dir]))
                    ))
    except IndexError:
        pass

    LUT = {
        UP_DIR: lambda x, y: (x + 1, y),
        DOWN_DIR: lambda x, y: (x - 1, y),
        LEFT_DIR: lambda x, y: (x, y + 1),
        RIGHT_DIR: lambda x, y: (x, y - 1)
    }

    PATH_LENGTH = 0
    curr_x, curr_y = END_X, END_Y

    # while curr_x != START_X or curr_y != START_Y:
    #     next_x, next_y = LUT[visit_array[curr_x, curr_y]](curr_x, curr_y)
    #     wall_array[curr_x, curr_y] = ord(END_CHAR)
    #     curr_x, curr_y = next_x, next_y
    #     PATH_LENGTH += 1

    with open(output_file, 'wb') as outfile:
        for row in wall_array:
            outfile.write(row.tostring() + b'\n')

    return FRONTIER_COUNT, MY_PATH
