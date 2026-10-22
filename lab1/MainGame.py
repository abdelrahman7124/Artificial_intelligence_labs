import DFS as dfs
import GameBoard as gb



intial_state = (1,0,2,3,4,5,6,7,8)  
result = dfs.dfs(intial_state)

if result is not None:
    path = result
    print("Path to goal:", path)
else: print("No path found to the goal state.")