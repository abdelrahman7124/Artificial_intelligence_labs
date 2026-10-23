import DFS as dfs
import BFS as bfs
import GameBoard as gb



intial_state = (1, 2, 7, 3, 4, 0, 6, 8, 5) 
result_dfs = dfs.dfs(intial_state)
result_bfs = bfs.bfs(intial_state)



if result_bfs is not None:
    path = result_bfs
    print("Path to goal:", path)
else: print("No path found to the goal state.")

if result_dfs is not None:
    path = result_dfs
    print("Path to goal:", path)
else: print("No path found to the goal state.")