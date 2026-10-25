import DFS as dfs
import BFS as bfs
import IDS as ids
import GameBoard as gb



intial_state = (1, 2, 7, 3, 4, 0, 6, 8, 5) 
result_dfs,cost_dfs = dfs.dfs(intial_state)
result_bfs,cost_bfs = bfs.bfs(intial_state)
result_ids,cost_ids = ids.ids(intial_state)

if result_ids is not None:
    path = result_ids
    cost = cost_ids
    print("Path to goal:", path)
    print("Cost of path:", cost)
else: print("No path found to the goal state.")

if result_bfs is not None:
    path = result_bfs
    cost = cost_bfs
    print("Path to goal:", path)
    print("Cost of path:", cost)
else: print("No path found to the goal state.")

if result_dfs is not None:
    path = result_dfs
    cost = cost_dfs
    print("Path to goal:", path)
    print("Cost of path:", cost)
else: print("No path found to the goal state.")