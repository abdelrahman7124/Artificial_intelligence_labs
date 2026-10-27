import random
import time
import matplotlib.pyplot as plt
import A_STAR as a_star

NUMBER_OF_TRIES = 1000
HEURISTICS = ["manhattan","euclidean"]


def is_solvable(state):
    tiles = []
    for tile in state:
        if tile != 0:
            tiles.append(tile)
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1,len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions % 2 == 0


def get_random_state():
    state = [0,1,2,3,4,5,6,7,8]
    random.shuffle(state)
    while not is_solvable(state):
        random.shuffle(state)
    return tuple(state)


def print_row(name,key,scale):
    manhattan_average = totals["manhattan"][key] / NUMBER_OF_TRIES * scale
    euclidean_average = totals["euclidean"][key] / NUMBER_OF_TRIES * scale
    print(name.ljust(30) + str(round(manhattan_average,3)).rjust(12) + str(round(euclidean_average,3)).rjust(12))



random.seed(2026)

totals = {}
for heuristic in HEURISTICS:
    totals[heuristic] = {"cost": 0,"nodes": 0,"time": 0,"h / cost": 0}
same_path = 0
manhattan_fewer_nodes = 0
euclidean_fewer_nodes = 0
nodes_per_cost = {}


for i in range(NUMBER_OF_TRIES):
    initial_state = get_random_state()
    paths = {}
    nodes = {}

    for heuristic in HEURISTICS:
        start_time = time.perf_counter()
        path,cost,nodes_expanded,max_depth_reached = a_star.a_star(initial_state,heuristic)
        running_time = time.perf_counter() - start_time
        h = a_star.heuristics[heuristic](initial_state)

        totals[heuristic]["cost"] += cost
        totals[heuristic]["nodes"] += nodes_expanded
        totals[heuristic]["time"] += running_time
        totals[heuristic]["h / cost"] += h / cost
        paths[heuristic] = path
        nodes[heuristic] = nodes_expanded

    if paths["manhattan"] == paths["euclidean"]:
        same_path += 1
    if nodes["manhattan"] < nodes["euclidean"]:
        manhattan_fewer_nodes += 1
    elif nodes["euclidean"] < nodes["manhattan"]:
        euclidean_fewer_nodes += 1

    if cost not in nodes_per_cost:
        nodes_per_cost[cost] = {"manhattan": [],"euclidean": []}
    nodes_per_cost[cost]["manhattan"].append(nodes["manhattan"])
    nodes_per_cost[cost]["euclidean"].append(nodes["euclidean"])




print("Averages over " + str(NUMBER_OF_TRIES) + " random boards:")
print("".ljust(30) + "Manhattan".rjust(12) + "Euclidean".rjust(12))
print_row("Cost of path","cost",1)
print_row("Nodes expanded","nodes",1)
print_row("Running time (ms)","time",1000)
print_row("h(start) / cost of path (%)","h / cost",100)

print("\nSame path on " + str(same_path) + " boards")
print("Manhattan expanded fewer nodes on " + str(manhattan_fewer_nodes) + " boards")
print("Euclidean expanded fewer nodes on " + str(euclidean_fewer_nodes) + " boards")



costs = sorted(nodes_per_cost.keys())
average_manhattan = []
average_euclidean = []
for cost in costs:
    average_manhattan.append(sum(nodes_per_cost[cost]["manhattan"]) / len(nodes_per_cost[cost]["manhattan"]))
    average_euclidean.append(sum(nodes_per_cost[cost]["euclidean"]) / len(nodes_per_cost[cost]["euclidean"]))

plt.figure(figsize=(6.4,3.4))
plt.plot(costs,average_manhattan,color="#2a78d6",marker="o",markersize=4,label="Manhattan")
plt.plot(costs,average_euclidean,color="#eb6834",marker="s",markersize=4,label="Euclidean")
plt.yscale("log")
plt.xlabel("Cost of the optimal path (moves)")
plt.ylabel("Average nodes expanded (log scale)")
plt.grid(True,color="#dddddd")
plt.legend()
plt.tight_layout()
plt.savefig("nodes_vs_cost.png",dpi=200)
print("\nSaved the plot in nodes_vs_cost.png")
