from basic_pathfinding import basic_pathfinding
from cost_heuristic import cost_heuristic
from ghost_heuristic import ghost_heuristic
from ghost_pathfind import ghost_pathfind
from write_solution import write_path
from Queue import Queue, LifoQueue, PriorityQueue


class AstarQueue(PriorityQueue):
    def put(self, item, block=True, timeout=None):
        priority, curr_posn = item
        return PriorityQueue.put(self, (priority + curr_posn[3], curr_posn), block, timeout)

# print('DFS', basic_pathfinding('mazes/medium.txt', LifoQueue))
# print('BFS', basic_pathfinding('mazes/medium.txt', Queue))
# print('Greedy', basic_pathfinding('mazes/medium.txt', PriorityQueue))
# print('A*', basic_pathfinding('mazes/medium.txt', AstarQueue))
# print
# print('DFS', basic_pathfinding('mazes/big.txt', LifoQueue))
# print('BFS', basic_pathfinding('mazes/big.txt', Queue))
# print('Greedy', basic_pathfinding('mazes/big.txt', PriorityQueue))
# print('A*', basic_pathfinding('mazes/big.txt', AstarQueue))
# print
# print('DFS', basic_pathfinding('mazes/open.txt', LifoQueue))
# print('BFS', basic_pathfinding('mazes/open.txt', Queue))
# print('Greedy', basic_pathfinding('mazes/open.txt', PriorityQueue))
# print('A*', basic_pathfinding('mazes/open.txt', AstarQueue))

# write_path('mazes/medium.txt', basic_pathfinding('mazes/medium.txt', LifoQueue), 'solutions/part1/medium_dfs.txt')
# write_path('mazes/medium.txt', basic_pathfinding('mazes/medium.txt', Queue), 'solutions/part1/medium_bfs.txt')
# write_path('mazes/medium.txt', basic_pathfinding('mazes/medium.txt', PriorityQueue), 'solutions/part1/medium_greedy.txt')
# write_path('mazes/medium.txt', basic_pathfinding('mazes/medium.txt', AstarQueue), 'solutions/part1/medium_astar.txt')
#
# write_path('mazes/big.txt', basic_pathfinding('mazes/big.txt', LifoQueue), 'solutions/part1/big_dfs.txt')
# write_path('mazes/big.txt', basic_pathfinding('mazes/big.txt', Queue), 'solutions/part1/big_bfs.txt')
# write_path('mazes/big.txt', basic_pathfinding('mazes/big.txt', PriorityQueue), 'solutions/part1/big_greedy.txt')
# write_path('mazes/big.txt', basic_pathfinding('mazes/big.txt', AstarQueue), 'solutions/part1/big_astar.txt')
#
# write_path('mazes/open.txt', basic_pathfinding('mazes/open.txt', LifoQueue), 'solutions/part1/open_dfs.txt')
# write_path('mazes/open.txt', basic_pathfinding('mazes/open.txt', Queue), 'solutions/part1/open_bfs.txt')
# write_path('mazes/open.txt', basic_pathfinding('mazes/open.txt', PriorityQueue), 'solutions/part1/open_greedy.txt')
# write_path('mazes/open.txt', basic_pathfinding('mazes/open.txt', AstarQueue), 'solutions/part1/open_astar.txt')

# write_path(
#     'mazes/small.txt',
#     cost_heuristic('mazes/small.txt', move_cost=2, turn_cost=1),
#     'solutions/part2/small21_manhattan.txt'
# )
# write_path(
#     'mazes/small.txt',
#     cost_heuristic('mazes/small.txt', move_cost=2, turn_cost=1, turn_heuristic=True),
#     'solutions/part2/small21_improved.txt'
# )
# write_path(
#     'mazes/small.txt',
#     cost_heuristic('mazes/small.txt', move_cost=1, turn_cost=2),
#     'solutions/part2/small12_manhattan.txt'
# )
# write_path(
#     'mazes/small.txt',
#     cost_heuristic('mazes/small.txt', move_cost=1, turn_cost=2, turn_heuristic=True),
#     'solutions/part2/small12_improved.txt'
# )


# write_path(
#     'mazes/big.txt',
#     cost_heuristic('mazes/big.txt', move_cost=2, turn_cost=1),
#     'solutions/part2/big21_manhattan.txt'
# )
# write_path(
#     'mazes/big.txt',
#     cost_heuristic('mazes/big.txt', move_cost=2, turn_cost=1, turn_heuristic=True),
#     'solutions/part2/big21_improved.txt'
# )
# write_path(
#     'mazes/big.txt',
#     cost_heuristic('mazes/big.txt', move_cost=1, turn_cost=2),
#     'solutions/part2/big12_manhattan.txt'
# )
# write_path(
#     'mazes/big.txt',
#     cost_heuristic('mazes/big.txt', move_cost=1, turn_cost=2, turn_heuristic=True),
#     'solutions/part2/big12_improved.txt'
# )

# write_path(
#     'mazes/big.txt',
#     cost_heuristic('mazes/big.txt', move_cost=1, turn_cost=1),
#     'solutions/part2/big12_manhattan.txt'
# )
# write_path(
#     'mazes/big.txt',
#     cost_heuristic('mazes/big.txt', move_cost=2, turn_cost=2),
#     'solutions/part2/big12_improved.txt'
# )
#
# print(len('UULLLLDDLLLLUULLLLLLLLUULLULLLLUULLDLLLLLLLLUULLUUUUUUUUUU'))

# print('A*:', basic_pathfinding('mazes/small.txt', AstarQueue, 'solutions/small_astar.txt', move_cost=2, turn_cost=1))
# print('A*:', basic_pathfinding('mazes/small.txt', AstarQueue, 'solutions/small_astar.txt', move_cost=2, turn_cost=1, turn_heuristic=True))
# print('A*:', basic_pathfinding('mazes/big.txt', AstarQueue, 'solutions/big_astar.txt', move_cost=2, turn_cost=1))
# print('A*:', basic_pathfinding('mazes/big.txt', AstarQueue, 'solutions/big_astar.txt', move_cost=2, turn_cost=1, turn_heuristic=True))
# print()
# print('A*:', basic_pathfinding('mazes/small.txt', AstarQueue, 'solutions/small_astar.txt', move_cost=1, turn_cost=2))
# print('A*:', basic_pathfinding('mazes/small.txt', AstarQueue, 'solutions/small_astar.txt', move_cost=1, turn_cost=2, turn_heuristic=True))

# print('A*:', cost_heuristic('mazes/small.txt', move_cost=1, turn_cost=2))
# print('A*:', cost_heuristic('mazes/small.txt', move_cost=1, turn_cost=2, turn_heuristic=True))

# print('A*:', ghost_heuristic('mazes/big_ghost.txt'))
# print('A*:', cost_heuristic('mazes/big.txt', move_cost=2, turn_cost=1))
# print('A*:', cost_heuristic('mazes/big.txt', move_cost=2, turn_cost=1, turn_heuristic=True))

print('A*:', ghost_pathfind('mazes/big_ghost.txt'))
print('A*:', ghost_heuristic('mazes/big_ghost.txt'))