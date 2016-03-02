import numpy as np
# import matplotlib.pyplot as plt
# import cv2

START_CHAR = 'P'
END_CHAR = '.'
WALL_CHAR = '%'
GHOST_CHAR = 'G'
PATH_CHAR = 'g'
WALL_INT = ord(WALL_CHAR)
PATH_INT = ord(PATH_CHAR)
END_INT = ord(END_CHAR)


def write_path(input_file, solution_path, output_file, square_size=1, generate_gif=False):
    maze_file = open(input_file)
    print(solution_path)

    if not generate_gif:
        square_size = 1

    maze_height = len(maze_file.readline()) - 1
    maze_width = sum(1 for _ in maze_file) + 1
    maze_file.seek(0)

    wall_array = np.empty((maze_width, maze_height), dtype=np.uint8)

    start_x = None
    start_y = None

    for row, line in enumerate(maze_file):
        if START_CHAR in line:
            start_x, start_y = row, line.find(START_CHAR)
        wall_array[row] = np.fromstring(line[:-1], dtype=np.uint8)

    lut_x = {
        'U': -1 * square_size,
        'D': square_size,
        'L': 0,
        'R': 0
    }

    lut_y = {
        'U': 0,
        'D': 0,
        'L': -1 * square_size,
        'R': square_size
    }

    pac_x = start_x
    pac_y = start_y

    for curr_step, curr_dir in enumerate(solution_path[2]):
        pac_x += lut_x[curr_dir]
        pac_y += lut_y[curr_dir]

        wall_array[pac_x, pac_y] = END_INT

    with open(output_file, 'wb') as outfile:
        for row in wall_array:
            outfile.write(row.tostring() + b'\n')
        outfile.write(b'\nPath cost: ' + str.encode(str(solution_path[1])) + b'\n')
        outfile.write(b'Nodes expanded: ' + str.encode(str(solution_path[0])) + b'\n')


# START_CHAR = 'P'
# END_CHAR = '.'
# WALL_CHAR = '%'
# GHOST_CHAR = 'G'
# PATH_CHAR = 'g'
# SPACE_CHAR = ' '
# WALL_INT = ord(WALL_CHAR)
#
# wall_array = np.empty((MAZE_WIDTH, MAZE_HEIGHT), dtype=np.uint8)
# maze_array = np.zeros((MAZE_WIDTH * SQUARE_SIZE, MAZE_HEIGHT * SQUARE_SIZE), dtype=np.uint8)
#
# PAC_X = None
# PAC_Y = None
# GHOST_X = None
# GHOST_Y = None
# ghost_dy = SQUARE_SIZE
#
# for row, line in enumerate(maze_file):
#     if START_CHAR in line:
#         PAC_X, PAC_Y = row * SQUARE_SIZE, line.find(START_CHAR) * SQUARE_SIZE
#     if END_CHAR in line:
#         END_X, END_Y = row, line.find(END_CHAR)
#     if GHOST_CHAR in line:
#         GHOST_X, GHOST_Y = row * SQUARE_SIZE, line.find(GHOST_CHAR) * SQUARE_SIZE
#     wall_array[row] = np.fromstring(line[:-1], dtype=np.uint8)
#
# for row in range(MAZE_WIDTH):
#     for col in range(MAZE_HEIGHT):
#         if wall_array[row, col] == WALL_INT:
#             curr_row = row * SQUARE_SIZE
#             curr_col = col * SQUARE_SIZE
#             maze_array[curr_row:curr_row + SQUARE_SIZE, curr_col:curr_col + SQUARE_SIZE] = 100
#
# PACMAN = cv2.getStructuringElement(cv2.MORPH_CROSS, (SQUARE_SIZE, SQUARE_SIZE)) * 255
# GHOST = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (SQUARE_SIZE, SQUARE_SIZE)) * 255
#
# maze_array[PAC_X:PAC_X + SQUARE_SIZE, PAC_Y:PAC_Y + SQUARE_SIZE] = PACMAN
#
# if GHOST_X:
#     maze_array[GHOST_X:GHOST_X + SQUARE_SIZE, GHOST_Y:GHOST_Y + SQUARE_SIZE] = GHOST
#
# cv2.imwrite('sol_images/big_ghost_00.jpg', maze_array)
#
# for curr_step, curr_dir in enumerate('UUUULLLLULLLLULUULLLLLULLUULLULLUDUULLUULLLLLLUUUUUULLUULUULUULLUUUUUU'):
#     maze_array[PAC_X:PAC_X + SQUARE_SIZE, PAC_Y:PAC_Y + SQUARE_SIZE] = 0
#     PAC_X += LUT_X[curr_dir]
#     PAC_Y += LUT_Y[curr_dir]
#     maze_array[PAC_X:PAC_X + SQUARE_SIZE, PAC_Y:PAC_Y + SQUARE_SIZE] = PACMAN
#
#     if GHOST_X:
#         if wall_array[GHOST_X / SQUARE_SIZE, (GHOST_Y + ghost_dy) / SQUARE_SIZE] == WALL_INT:
#             ghost_dy *= -1
#         maze_array[GHOST_X:GHOST_X + SQUARE_SIZE, GHOST_Y:GHOST_Y + SQUARE_SIZE] = 0
#         GHOST_Y += ghost_dy
#         maze_array[GHOST_X:GHOST_X + SQUARE_SIZE, GHOST_Y:GHOST_Y + SQUARE_SIZE] = GHOST
#
#     cv2.imwrite('sol_images/big_ghost_{0:02d}.jpg'.format(curr_step + 1), maze_array)
#
# plt.imshow(maze_array, 'gray')
# plt.show()