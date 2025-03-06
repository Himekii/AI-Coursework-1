# +------------------------------------------------------------
# Utility functions
def print_state(state):
    by, bx, rows = state
    for row in rows:
        print(row, '\n', end = '')


def trans(state, state1):
    by, bx, rows = state
    by1, bx1, rows1 = state1
    if bx < bx1:
        print("moved blank right")
    elif bx > bx1:
        print("moved blank left")
    elif by < by1:
        print("moved blank down")
    elif by > by1:
        print("moved blank up")
    else:
        print("Error")

def print_path(path):
    print_state(path[0])
    for i in range(1, len(path)):
        trans(path[i - 1], path[i])
        print_state(path[i])

def get_path(state, predecessor):
    """
    Given a path specified by  @predecessor dictionary, and a @state
    returns the list of spaces along the path that goes from the state whose predecessor is None to @state
    :param state: state
    :param predecessor: path
    :return:
    """
    current = state
    path = []
    
    while current != None:
        path.append(current)
        current = predecessor[current]
    return path

def move(state):
    """
    move(state):
    generator that returns all states that are reached from
    state, in one move and are safe.

    There are five possible moves from left to right: move one or two jailers,
    one or two convicts, or one of each.  For each of these, there is one yield.

    We could make five more yield like the above for moves from right to left,
    but we can instead take advantage of the symmetry of the problem.
    :param state:
    :return: next_state
    """
    by, bx, rows = state
    
    
    if bx < 2: #Blank space not on right
        #Move Right
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx] = temp_rows[by][bx+1]
        temp_rows[by][bx+1] = 0
        next_state = by, bx+1, tuple(tuple(row) for row in temp_rows)
        yield next_state
    if bx > 0: #Blank space not on left
        #Move Left
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx] = temp_rows[by][bx-1]
        temp_rows[by][bx-1] = 0
        next_state = by, bx-1, tuple(tuple(row) for row in temp_rows)
        yield next_state
    if by < 2: #Blank space not at bottom
        #Move Down
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx] = temp_rows[by+1][bx]
        temp_rows[by+1][bx] = 0
        next_state = by+1, bx, tuple(tuple(row) for row in temp_rows)
        yield next_state
    if by > 0: #Blank space not at top
        #Move Up
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx] = temp_rows[by-1][bx]
        temp_rows[by-1][bx] = 0
        next_state = by-1, bx, tuple(tuple(row) for row in temp_rows)
        yield next_state

    return None


def dfs_stack(state, goal):
    """
    NON-RECURSIVE version of the depth first search of a cyclic search space.
    uses a stack of states, @state, and a dictionary @predecessor to store the predecessor of each state along the
    search path.

    calls @get_path
    calls @is_goal

    Note: the dictionary is initialized by the statement:  predecessor = {state : None}. "None" is a marker
    to identify the starting state when reconstruction a path by @get_path
    :param state: state from which the search starts
    :return: path to the goal state
    """
    stack = [state]
    
    predecessor = {}
    prev_node = None
    
    # while stack:
    while stack:
        current = stack[-1]
        
        if current not in predecessor:
            predecessor[current] = prev_node
        else:
            stack.pop()
            continue
            
        if current == goal:
            return get_path(current, predecessor)


        
        offspring = move(current)

        hasKids = False
        
        for next_state in offspring:
            hasKids = True
            stack.append(next_state)

        if not hasKids:
            print("No kids")
            
        prev_node = current

def iddfs_stack(state, goal):
    return 0;

def ida_stack(state, goal):
    return 0;

print("\nTEST OF DFS STACK:")
goal = (0, 2, ((3, 2, 0),(6, 1, 8), (4, 7, 5)))
path = dfs_stack((0, 0, ((0, 7, 1), (4, 3, 2), (8, 6, 5))), goal)
print(path)
print_path(path)