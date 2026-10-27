import GameBoard as gb
import heapq as hq


def get_heuristic_manhattan_distance(state):
    sum_heuristic = 0
    for i in range (9):
        if state[i] == 0:
            continue
        current_position = (i // 3, i % 3)
        goal_position = gb.GOAL_STATE_POSITIONS[state[i]]
        manhattan_distance = abs(current_position[0] - goal_position[0]) + abs(current_position[1] - goal_position[1])
        sum_heuristic += manhattan_distance
    return sum_heuristic

def get_heuristic_euclidean_distance(state):
    sum_heuristic = 0
    for i in range (9):
        if state[i] == 0:
            continue
        current_position = (i // 3, i % 3)
        goal_position = gb.GOAL_STATE_POSITIONS[state[i]]
        euclidean_distance = ((current_position[0] - goal_position[0]) ** 2 + (current_position[1] - goal_position[1]) ** 2) ** 0.5
        sum_heuristic += euclidean_distance
    return sum_heuristic



heuristics = {
    "manhattan": get_heuristic_manhattan_distance,
    "euclidean": get_heuristic_euclidean_distance
}



def a_star(initial_state,heuristic_type):
    heuristic_function = heuristics[heuristic_type]
    queue = []
    states = {}
    visited = set()
    nodes_expanded = 0
    max_depth_reached = 0
    
    hq.heappush(queue, (0, (initial_state, None, None, 0)))
    visited.add(initial_state)
    states[initial_state] = 0

    while queue:
        _, node = hq.heappop(queue)
        state, parent, last_move, level = node
        visited.add(state)

        if gb.is_goal(state):
            path,cost = gb.get_path_from_node(node)
            return path,cost,nodes_expanded,max_depth_reached

        nodes_expanded += 1
        for move, neighbour in gb.get_neighbours(state).items():
            new_level = level + 1
            cost = new_level + heuristic_function(neighbour)

            if neighbour not in visited and neighbour not in states:
                hq.heappush(queue, (cost, (neighbour, node, move, new_level)))
                states[neighbour] = cost
                if new_level > max_depth_reached:
                    max_depth_reached = new_level

            elif neighbour in states and cost < states[neighbour]:
                for i in range(len(queue)):
                    if queue[i][1][0] == neighbour:
                        queue[i] = (cost, (neighbour, node, move, new_level))
                        hq.heapify(queue)
                        break
                states[neighbour] = cost
    return None