import GameBoard as gb

def dls(initial_state,max_depth):
    STACK = []
    states = set()
    cutoff_occurred = False
    
    STACK.append((initial_state,None,None,0))
    states.add(initial_state)
    
    while STACK:
        node = STACK.pop()
        state,parent,last_move,level = node

        
        if gb.is_goal(state):
            return gb.get_path_from_node(node),cutoff_occurred
        
        if level < max_depth:
            for move,neighbour in gb.get_neighbours(state).items():
                if neighbour not in states :
                    STACK.append((neighbour,node,move, level + 1))
        else:
            cutoff_occurred = True
        
    return None,cutoff_occurred

def ids(initial_state):
    depth = 0
    while True:
        result,cutoff_occurred = dls(initial_state,depth)
        if result is not None:
            return result
        if not cutoff_occurred:
            return None
        depth += 1