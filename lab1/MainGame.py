import DFS as dfs
import BFS as bfs
import IDS as ids
import A_STAR as a_star
import GameBoard as gb



initial_state = (1, 2, 7, 3, 4, 0, 6, 8, 5) 
result_dfs,cost_dfs = dfs.dfs(initial_state)
result_bfs,cost_bfs = bfs.bfs(initial_state)
result_ids,cost_ids = ids.ids(initial_state)
result_a_star_manhattan,cost_a_star_manhattan = a_star.a_star(initial_state,"manhattan")
result_a_star_euclidean,cost_a_star_euclidean = a_star.a_star(initial_state,"euclidean")



print("IDS:")
if result_ids is not None:
    path = result_ids
    cost = cost_ids
    print("Path to goal:", path)
    print("Cost of path:", cost)
else: print("No path found to the goal state.")
print("**************************************************************\n\n\n")



print("BFS:")
if result_bfs is not None:
    path = result_bfs
    cost = cost_bfs
    print("Path to goal:", path)
    print("Cost of path:", cost)
else: print("No path found to the goal state.")
print("**************************************************************\n\n\n")



print("A* with Manhattan heuristic:")
if result_a_star_manhattan is not None:
    path = result_a_star_manhattan
    cost = cost_a_star_manhattan
    print("Path to goal:", path)
    print("Cost of path:", cost)
else: print("No path found to the goal state.")
print("**************************************************************\n\n\n")



print("A* with Euclidean heuristic:")
if result_a_star_euclidean is not None:
    path = result_a_star_euclidean
    cost = cost_a_star_euclidean
    print("Path to goal:", path)
    print("Cost of path:", cost)
else: print("No path found to the goal state.")
print("**************************************************************\n\n\n")



print("DFS:")
if result_dfs is not None:
    path = result_dfs
    cost = cost_dfs
    print("Path to goal:", path)
    print("Cost of path:", cost)
else: print("No path found to the goal state.")
print("**************************************************************\n\n\n")