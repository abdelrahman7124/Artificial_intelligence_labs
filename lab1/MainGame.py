import time
import DFS as dfs
import BFS as bfs
import IDS as ids
import A_STAR as a_star



initial_state = (1, 2, 7, 3, 4, 0, 6, 8, 5)


def print_result(name,result,running_time):
    print(name + ":")
    if result is not None:
        path,cost,nodes_expanded,max_depth_reached = result
        print("Path to goal:", path)
        print("Cost of path:", cost)
        print("Nodes expanded:", nodes_expanded)
        print("Search depth:", max_depth_reached)
        print("Running time:", round(running_time,4), "s")
    else: print("No path found to the goal state.")
    print("**************************************************************\n\n\n")



start_time = time.time()
result_ids = ids.ids(initial_state)
print_result("IDS",result_ids,time.time() - start_time)

start_time = time.time()
result_bfs = bfs.bfs(initial_state)
print_result("BFS",result_bfs,time.time() - start_time)

start_time = time.time()
result_a_star_manhattan = a_star.a_star(initial_state,"manhattan")
print_result("A* with Manhattan heuristic",result_a_star_manhattan,time.time() - start_time)

start_time = time.time()
result_a_star_euclidean = a_star.a_star(initial_state,"euclidean")
print_result("A* with Euclidean heuristic",result_a_star_euclidean,time.time() - start_time)

start_time = time.time()
result_dfs = dfs.dfs(initial_state)
print_result("DFS",result_dfs,time.time() - start_time)
