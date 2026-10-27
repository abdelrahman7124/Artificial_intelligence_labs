import GameBoard as gb

def dls(initial_state,max_depth):
    STACK = []
    cutoff_occurred = False
    nodes_expanded = 0
    
    STACK.append((initial_state,None,None,0))
    
    while STACK:
        node = STACK.pop()
        state,parent,last_move,level = node

        
        if gb.is_goal(state):
            return gb.get_path_from_node(node),cutoff_occurred,nodes_expanded
        
        if level < max_depth:
            nodes_expanded += 1
            for move,neighbour in gb.get_neighbours(state).items():
                STACK.append((neighbour,node,move, level + 1))
        else:
            cutoff_occurred = True
        
    return None,cutoff_occurred,nodes_expanded

def ids(initial_state):
    depth = 0
    total_nodes_expanded = 0
    while True:
        result,cutoff_occurred,nodes_expanded = dls(initial_state,depth)
        total_nodes_expanded += nodes_expanded
        if result is not None:
            path,cost = result
            return path,cost,total_nodes_expanded,depth
        if not cutoff_occurred:
            return None
        depth += 1