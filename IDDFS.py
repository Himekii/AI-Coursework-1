import time

"""
State: 1
Path Length: 22
States accessed: 79228
Computation Time: 368.0005073547363ms 


State: 2
Path Length: 24
States accessed: 122164
Computation Time: 624.0708827972412ms 


State: 3
Path Length: 40
States accessed: 1684010
Computation Time: 8737.18810081482ms 


State: 4
Path Length: 34
States accessed: 1272873
Computation Time: 6551.671981811523ms 


State: 5
Path Length: 22
States accessed: 350602
Computation Time: 1773.611068725586ms 


State: 6
Path Length: 28
States accessed: 278142
Computation Time: 1366.4963245391846ms 


State: 7
Path Length: 14
States accessed: 22140
Computation Time: 132.60436058044434ms 


State: 8
Path Length: 38
States accessed: 1852312
Computation Time: 9567.428350448608ms 


State: 9
Path Length: 22
States accessed: 125813
Computation Time: 577.1675109863281ms 


State: 10
Path Length: 35
States accessed: 988424
Computation Time: 5134.518146514893ms 
"""

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
    state, in one move.

    :param state: a list containing the blank position (x,y) and the grid of values
    :return: next_state
    """
    by, bx, rows = state
    
    if bx < len(rows[0])-1: # Blank space not on right
         #Move Blank Right
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx], temp_rows[by][bx+1] = temp_rows[by][bx+1], 0
        next_state = [by, bx+1, temp_rows]
        yield next_state
    if bx > 0: # Blank space not on left
         #Move Blank Left
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx], temp_rows[by][bx-1] = temp_rows[by][bx-1], 0
        next_state = [by, bx-1, temp_rows]
        yield next_state
    if by < len(rows)-1: # Blank space not at bottom
        # Move Blank Down
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx], temp_rows[by+1][bx] = temp_rows[by+1][bx], 0
        next_state = [by+1, bx, temp_rows]
        yield next_state
    if by > 0: # Blank space not at top
        # Move Blank Up
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx], temp_rows[by-1][bx]  = temp_rows[by-1][bx], 0
        next_state = [by-1, bx, temp_rows]
        yield next_state
    
    return None


def iddfs(state, goal):
    """
    NON-RECURSIVE version of the depth first search of a cyclic search space.
    uses a stack of states, @state, and a dictionary @predecessor to store the predecessor of each state along the
    search path. Searches the entire tree using DFS until the search depth is reach, then increments the search depth 
    by 1 each time the search is complete.

    calls @get_path

    Note: the dictionary is initialized by the statement:  predecessor = {state : None}. "None" is a marker
    to identify the starting state when reconstruction a path by @get_path
    :param state: state from which the search starts
    :param goal: state for the search to find
    :return: path to the goal state and number of states accessed
    """
    
    # Each number multiplied by maximum manhatten (across and up/down) for each number
    maxMoves = (len(state[2])*len(state[2][0]) * (len(state[2])-1 + len(state[2][0])-1))+1
    
    # Number for the amount of states accessed
    accesses = 0
    
    for search_depth in range(maxMoves + maxMoves):
        predecessor = {(state[0], state[1], tuple(tuple(row) for row in state[2])) : None}
        stack = [[0,state]]
        while stack: # While new states still available to search
            
            depth, current = stack.pop() # Destack most recent unseen element with depth
            key = current[0], current[1], tuple(tuple(row) for row in current[2]) # Hashable copy of current
                
            if current == goal: # Checks if current is the target state
                return get_path(key, predecessor), accesses # Returns path from inital state to target state and the number of accesses.

            if depth <= search_depth: # If depth of current node is higher than the search depth
                for next_state in move(current): # For each child / possible move
                    accesses += 1 # Updates the state accesses number
                    nextKey = next_state[0], next_state[1], tuple(tuple(row) for row in next_state[2]) # Hashable copy of next_state
                    if nextKey not in predecessor: # If node is has not been explored
                        stack.append([depth + 1, next_state]) # Append the next_state with a depth 1 deeper than the parent
                        predecessor[nextKey] = key # Store next_state with its parent
                    
    print("No solution found")
    return [], accesses

def solve_puzzle(case, goal):
    """
    The main function to call @iddfs using the given state and goal 
    while collecting efficiency information and returning it.
    
    calls: @iddfs
    
    param case: state from which the search starts
    param goal: state for the search to find
    return: number of moves, number of states accessed, computation time and path from case to goal 
    """
    start = time.time()
    path, accesses = iddfs(case, goal)
    compTime = time.time() - start
    print(f"Path Length: {len(path)-1}")
    print(f"States accessed: {accesses}")
    print(f"Computation Time: {compTime * 1000}ms \n\n")
    return (len(path)-1, accesses, compTime, path)
        
cases1 = [[0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]],
[0, 2, [[5, 6, 0], [1, 3, 8], [4, 7, 2]]],
[2, 0, [[3, 5, 6], [1, 2, 7], [0, 8, 4]]],
[1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]],
[2, 0, [[6, 4, 8], [7, 1, 3], [0, 2, 5]]]]

goal1 = [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]] 

index = 1

for case1 in cases1:
    print(f"State: {index}")
    solve_puzzle(case1, goal1)
    index+=1

cases2 = [[0, 0, [[0, 1, 8], [3, 6, 7], [5, 4, 2]]],
[2, 0, [[6, 4, 1], [7, 3, 2], [0, 5, 8]]],
[0, 0, [[0, 7, 1], [5, 4, 8], [6, 2, 3]]],
[0, 2, [[5, 4, 0], [2, 3, 1], [8, 7, 6]]],
[2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]]]

goal2 = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]

for case2 in cases2:
    print(f"State: {index}")
    solve_puzzle(case2, goal2)
    index+=1