import time

"""
State: 1
Path Length: 20
States accessed: 2757
Computation Time: 24.003028869628906ms 


State: 2
Path Length: 22
States accessed: 4020
Computation Time: 33.9961051940918ms 


State: 3
Path Length: 26
States accessed: 13844
Computation Time: 167.7267551422119ms 


State: 4
Path Length: 30
States accessed: 49335
Computation Time: 468.0652618408203ms 


State: 5
Path Length: 22
States accessed: 4299
Computation Time: 35.9952449798584ms 


State: 6
Path Length: 20
States accessed: 294
Computation Time: 2.0117759704589844ms 


State: 7
Path Length: 14
States accessed: 104
Computation Time: 0.9958744049072266ms 


State: 8
Path Length: 26
States accessed: 12900
Computation Time: 106.24861717224121ms 


State: 9
Path Length: 22
States accessed: 7795
Computation Time: 63.802480697631836ms 


State: 10
Path Length: 31
States accessed: 40638
Computation Time: 384.0053081512451ms 
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

    :param state:
    :return: next_state
    """
    by, bx, rows = state
    
    if bx < len(rows[0])-1: #Blank space not on right
        #Move Right
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx], temp_rows[by][bx+1] = temp_rows[by][bx+1], 0
        next_state = [by, bx+1, temp_rows]
        yield next_state
    if bx > 0: #Blank space not on left
        #Move Left
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx], temp_rows[by][bx-1] = temp_rows[by][bx-1], 0
        next_state = [by, bx-1, temp_rows]
        yield next_state
    if by < len(rows)-1: #Blank space not at bottom
        #Move Down
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx], temp_rows[by+1][bx] = temp_rows[by+1][bx], 0
        next_state = [by+1, bx, temp_rows]
        yield next_state
    if by > 0: #Blank space not at top
        #Move Up
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx], temp_rows[by-1][bx]  = temp_rows[by-1][bx], 0
        next_state = [by-1, bx, temp_rows]
        yield next_state

    return None

def manhattan(state, state1):
    """
    Calculates the manhattan distance for each value in @state to its equivalence in @state1, 
    summing them up to find the total manhattan distance from @state to @state1.
    
    param state: state to compare from
    param state1: state to compare to
    
    return: the manhattan distance between @state and @state1
    """
    by, bx, rows = state
    by1, bx1, rows1 = state1
    
    result = 0
    indices = {}
    
    
    # Finds the x and y index of each value
    for row in range(len(rows)): 
        for val in range(len(rows[row])):
            indices[rows[row][val]] = [row,val]

    # Calculates the distance between the x and y index of each values
    # from the corresponding value in the previous state and then adds
    # the value to @result.
    for row in range(len(rows1)):
        for val in range(len(rows1[row])):
            result += abs(indices[rows1[row][val]][0] - row) + abs(indices[rows1[row][val]][1] - val)
   
    return result


def IDAstar(state, goal):
    """
    IDA* search algorithm to search the tree of possible moves from @state. Uses a heuristic equivalent to the 
    sum of each nodes depth and its manhattan distance to the goal. Creates a threshold based on the manhattan
    distance from the @state to the @goal and is updated to the smallest heuristic of the unexplored nodes each 
    time a search is completed.
    
    calls: @IDAstar
    
    param case: state from which the search starts
    param goal: state for the search to find
    return: the path from @state to @goal and the number of states accessed
    """
    
    
    # Each number multiplied by maximum manhatten (across and up/down) for each number
    maxMoves = (len(state[2])*len(state[2][0]) * (len(state[2])-1 + len(state[2][0])-1))
    
    # Initial threshold of the hueristic of @state
    thresh = manhattan(state, goal)
    
    # Number for the amount of states accessed
    accesses = 0
    
    # Loops as long as thresh is below the maximum moves (g) + maxmimum depth (h)
    while thresh <= maxMoves + maxMoves:
        predecessor = {(state[0], state[1], tuple(tuple(row) for row in state[2])) : None} # Initialises predecessors with hashable state.
        stack = [[0,state]] # Initialises stack with initial state with depth 0.
        minmanhattan = maxMoves * maxMoves # Reset minmanattan to high number
        while stack:  # While new states still available to search
            
            depth, current = stack.pop() # Destack most recent unseen element with depth
            key = current[0], current[1], tuple(tuple(row) for row in current[2]) # Hashable copy of current
            
            if current == goal: #Checks if current is the target state
                return get_path(key, predecessor), accesses # Returns path from inital state to target state and the number of accesses.
    
            # Heuristic of the node using depth + manhattan distance to goal
            h = depth + manhattan(current, goal) 
    
            if h <= thresh: # If heuristic of node is below threshold
                for next_state in move(current): # For each child / possible move
                    accesses += 1 # Updates the state accesses number
                    nextKey = next_state[0], next_state[1], tuple(tuple(row) for row in next_state[2]) # Hashable copy of next_state
                    if nextKey not in predecessor: # If node is has not been explored
                        stack.append([depth + 1, next_state]) # Append the next_state with a depth 1 deeper than the parent
                        predecessor[nextKey] = key # Store next_state with its parent
            elif h < minmanhattan: # If heuristic of node is above the threshold and below the smallest unexplored child
                minmanhattan = h # Update minmanhattan to the heurstic of the node
        
        if minmanhattan != maxMoves * maxMoves: # If minmanhatten has been updated
            thresh = minmanhattan # Update threshold to minmanhatten
        else: # If minmanhatten has not been updated
            thresh += 1 # Increment threshold
    print("No solution found")
    return [], accesses # Return no path with the number of accesses


def solve_puzzle(case, goal):
    """
    The main function to call @IDAstar using the given state and goal 
    while collecting efficiency information and returning it.
    
    calls: @IDAstar
    
    param case: state from which the search starts
    param goal: state for the search to find
    return: number of moves, number of states accessed, computation time and path from case to goal 
    """
    start = time.time()
    path, accesses = IDAstar(case, goal)
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
