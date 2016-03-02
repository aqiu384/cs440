import numpy as np
from queue import PriorityQueue

Y_GRID, X_GRID = np.meshgrid(np.arange(10), np.arange(10))
dist_array = np.absolute(X_GRID - 5) + np.absolute(Y_GRID - 5)

print(np.tile(dist_array, (2, 1, 1)))

# x, y = np.meshgrid(np.arange(5), np.arange(10))
# distances = np.absolute(x - 5) + np.absolute(y - 5)
#
# print(distances)

# import queue
#
# MAZE_WIDTH = 37
# MAZE_HEIGHT = 37
#
# maze_file = open('mazes/maze.txt')
# wall_array = np.empty((MAZE_HEIGHT, MAZE_WIDTH), dtype=np.uint8)
# visit_array = np.zeros([MAZE_WIDTH, MAZE_HEIGHT], dtype=np.uint8)
#
# START_CHAR = 'P'
# END_CHAR = '.'
# WALL_CHAR = '%'
#
# START_X = None
# START_Y = None
# END_X = None
# END_Y = None
#
# for row, line in enumerate(maze_file):
#     if START_CHAR in line:
#         START_X, START_Y = row, line.find(START_CHAR)
#     if END_CHAR in line:
#         END_X, END_Y = row, line.find(END_CHAR)
#     wall_array[row] = np.fromstring(line[:-1], dtype=np.uint8)
#
# wall_array = np.subtract(wall_array, ord(WALL_CHAR))
#
# frontier = queue.LifoQueue()
# # frontier.appendleft((START_X, START_Y))
# frontier.put((START_X, START_Y))
#
# FRONTIER_COUNT = 0
#
# try:
#     for _ in range(1000):
#         curr_x, curr_y = frontier.get()
#         FRONTIER_COUNT += 1
#         temps = [(curr_x + 1, curr_y, ord('l')), (curr_x - 1, curr_y, ord('r')), (curr_x, curr_y + 1, ord('u')), (curr_x, curr_y - 1, ord('d'))]
#
#         for temp_x, temp_y, direction in temps:
#             if wall_array[temp_x, temp_y] and not visit_array[temp_x, temp_y]:
#                 visit_array[temp_x, temp_y] = direction
#                 # frontier.appendleft((temp_x, temp_y))
#                 frontier.put((temp_x, temp_y))
#
#                 if temp_x == END_X and temp_y == END_Y:
#                     raise IndexError('Found a path')
# except IndexError:
#     pass
#
# wall_array = np.add(wall_array, ord(WALL_CHAR))
#
# LUT = {
#     ord('l'): lambda x, y: (x - 1, y),
#     ord('r'): lambda x, y: (x + 1, y),
#     ord('u'): lambda x, y: (x, y - 1),
#     ord('d'): lambda x, y: (x, y + 1)
# }
#
# curr_x, curr_y = END_X, END_Y
#
# while curr_x != START_X or curr_y != START_Y:
#     next_x, next_y = LUT[visit_array[curr_x, curr_y]](curr_x, curr_y)
#     wall_array[curr_x, curr_y] = ord(END_CHAR)
#     curr_x, curr_y = next_x, next_y
#
# with open('solutions/maze.txt', 'wb') as outfile:
#     for row in wall_array:
#         outfile.write(row.tostring() + b'\n')
#
# print(FRONTIER_COUNT)
