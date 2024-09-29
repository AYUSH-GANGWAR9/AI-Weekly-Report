from collections import deque

def displayState(board):
    print(" ".join(board))

def swapPositions(board, sourceIndex, targetIndex):
    board[targetIndex], board[sourceIndex] = board[sourceIndex], board[targetIndex]

def breadthFirstSearchLeap(startConfig):
    endConfig = ['W', 'W', 'W', '_', 'E', 'E', 'E']
    stateQueue = deque([(startConfig, [])])
    seenStates = set()
    seenStates.add(tuple(startConfig))

    while stateQueue:
        currentConfig, movementHistory = stateQueue.popleft()
        displayState(currentConfig)
        if currentConfig == endConfig:
            return movementHistory

        blankIndex = currentConfig.index('_')
        potentialMoves = []

        if blankIndex - 1 >= 0 and currentConfig[blankIndex - 1] == 'E':
            potentialMoves.append((blankIndex - 1, blankIndex))
        if blankIndex - 2 >= 0 and currentConfig[blankIndex - 2] == 'E' and currentConfig[blankIndex - 1] == 'W':
            potentialMoves.append((blankIndex - 2, blankIndex))

        if blankIndex + 1 < len(currentConfig) and currentConfig[blankIndex + 1] == 'W':
            potentialMoves.append((blankIndex + 1, blankIndex))
        if blankIndex + 2 < len(currentConfig) and currentConfig[blankIndex + 2] == 'W' and currentConfig[blankIndex + 1] == 'E':
            potentialMoves.append((blankIndex + 2, blankIndex))

        for source, target in potentialMoves:
            newConfig = currentConfig[:]
            swapPositions(newConfig, source, target)
            if tuple(newConfig) not in seenStates:
                seenStates.add(tuple(newConfig))
                stateQueue.append((newConfig, movementHistory + [(source, target)]))

    return None

def depthFirstSearchLeap(startConfig):
    endConfig = ['W', 'W', 'W', '_', 'E', 'E', 'E']
    stateStack = [(startConfig, [])]
    seenStates = set()
    seenStates.add(tuple(startConfig))

    while stateStack:
        currentConfig, movementHistory = stateStack.pop()
        displayState(currentConfig)
        if currentConfig == endConfig:
            return movementHistory

        blankIndex = currentConfig.index('_')
        potentialMoves = []

        if blankIndex - 1 >= 0 and currentConfig[blankIndex - 1] == 'E':
            potentialMoves.append((blankIndex - 1, blankIndex))
        if blankIndex - 2 >= 0 and currentConfig[blankIndex - 2] == 'E' and currentConfig[blankIndex - 1] == 'W':
            potentialMoves.append((blankIndex - 2, blankIndex))

        if blankIndex + 1 < len(currentConfig) and currentConfig[blankIndex + 1] == 'W':
            potentialMoves.append((blankIndex + 1, blankIndex))
        if blankIndex + 2 < len(currentConfig) and currentConfig[blankIndex + 2] == 'W' and currentConfig[blankIndex + 1] == 'E':
            potentialMoves.append((blankIndex + 2, blankIndex))

        for source, target in potentialMoves:
            newConfig = currentConfig[:]
            swapPositions(newConfig, source, target)
            if tuple(newConfig) not in seenStates:
                seenStates.add(tuple(newConfig))
                stateStack.append((newConfig, movementHistory + [(source, target)]))

    return None

if __name__ == "__main__":
    initialConfig = ['E', 'E', 'E', '_', 'W', 'W', 'W']
    
    print("BFS Initial Configuration:")
    displayState(initialConfig)
    print("\nBFS Solving...\n")
    bfsSolution = breadthFirstSearchLeap(initialConfig)
    
    if bfsSolution:
        print("\nBFS Solution found!")
        print(f"Moves: {bfsSolution}")
    else:
        print("No solution found with BFS.")

    print("\nDFS Initial Configuration:")
    displayState(initialConfig)
    print("\nDFS Solving...\n")
    dfsSolution = depthFirstSearchLeap(initialConfig)
    
    if dfsSolution:
        print("\nDFS Solution found!")
        print(f"Moves: {dfsSolution}")
    else:
        print("No solution found with DFS.")
