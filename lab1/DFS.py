import GameBoard as gb

def dfs(initial_state): 
    STACK = []
    states = set()
    VISITED = set()
    nodes_expanded = 0
    max_depth_reached = 0
    
    STACK.append((initial_state, None, None, 0))
    states.add(initial_state)
    
    while STACK:
        node = STACK.pop()
        state = node[0]
        level = node[3]
        states.remove(state)
        VISITED.add(state)
        
        if gb.is_goal(state):
            path,cost = gb.get_path_from_node(node)
            return path,cost,nodes_expanded,max_depth_reached
        
        nodes_expanded += 1
        for move,neighbour in gb.get_neighbours(state).items():
            if  neighbour not in VISITED and neighbour not in states:
                STACK.append((neighbour, node, move, level + 1))
                states.add(neighbour)
                if level + 1 > max_depth_reached:
                    max_depth_reached = level + 1
    return None