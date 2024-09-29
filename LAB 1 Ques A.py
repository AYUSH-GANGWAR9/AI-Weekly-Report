from collections import deque
import time

startTime = time.time()

def isSafe(state):
    missionaries, cannibals, boatPosition = state
    if missionaries < 0 or cannibals < 0 or missionaries > 3 or cannibals > 3:
        return False
    if missionaries > 0 and cannibals > missionaries:
        return False
    if (3 - missionaries) > 0 and (3 - missionaries) < (3 - cannibals):
        return False
    return True

def generateNextStates(currentState):
    nextStates = []
    missionaries, cannibals, boatPosition = currentState
    possibleMoves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
    
    if boatPosition == 1:
        for m, c in possibleMoves:
            newState = (missionaries - m, cannibals - c, 0)
            if isSafe(newState):
                nextStates.append(newState)
    else:
        for m, c in possibleMoves:
            newState = (missionaries + m, cannibals + c, 1)
            if isSafe(newState):
                nextStates.append(newState)
                
    return nextStates

def searchSolution(initialState, targetState):
    explorationQueue = deque([(initialState, [])])
    visitedStates = set()
    
    while explorationQueue:
        currentState, pathSoFar = explorationQueue.popleft()
        
        if currentState in visitedStates:
            continue
            
        visitedStates.add(currentState)
        newPath = pathSoFar + [currentState]
        
        if currentState == targetState:
            return newPath
        
        for nextState in generateNextStates(currentState):
            explorationQueue.append((nextState, newPath))
    
    return None

initialState = (3, 3, 1)
targetState = (0, 0, 0)

solutionPath = searchSolution(initialState, targetState)

if solutionPath:
    for step in solutionPath:
        print(step)
else:
    print("No solution found.")

endTime = time.time()
print(f"Total runtime of the program is {endTime - startTime} seconds.")
