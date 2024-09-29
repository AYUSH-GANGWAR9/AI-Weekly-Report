from collections import deque

class PuzzleNode:
    def __init__(self, boardState, parentNode=None):
        self.state = boardState
        self.parent = parentNode

def generateSuccessors(currentNode):
    blankTileIndex = currentNode.state.index(0)
    successorsList = []
    possibleMoves = [-1, 1, 3, -3]
    
    for move in possibleMoves:
        newIndex = blankTileIndex + move
        if 0 <= newIndex < 9:
            newState = list(currentNode.state)
            newState[blankTileIndex], newState[newIndex] = newState[newIndex], newState[blankTileIndex]
            nextNode = PuzzleNode(newState, currentNode)
            successorsList.append(nextNode)
    
    return successorsList

def traceSolutionPath(currentNode):
    solutionPath = []
    while currentNode:
        solutionPath.append(currentNode.state)
        currentNode = currentNode.parent
    return solutionPath[::-1]

def breadthFirstSearch(startBoard, goalBoard):
    startNode = PuzzleNode(startBoard)
    goalNode = PuzzleNode(goalBoard)
    explorationQueue = deque([startNode])
    exploredStates = set()
    totalExploredNodes = 0
    
    while explorationQueue:
        currentNode = explorationQueue.popleft()
        
        if tuple(currentNode.state) in exploredStates:
            continue
        
        exploredStates.add(tuple(currentNode.state))
        print(currentNode.state)
        
        totalExploredNodes += 1
        
        if currentNode.state == list(goalNode.state):
            print('Total nodes explored:', totalExploredNodes)
            return traceSolutionPath(currentNode)
        
        for successor in generateSuccessors(currentNode):
            explorationQueue.append(successor)

    print('Total nodes explored:', totalExploredNodes)
    return None

initialBoard = [1, 2, 3, 4, 5, 6, 7, 8, 0]
goalBoard = [1, 2, 3, 4, 5, 6, 0, 7, 8]

solutionPath = breadthFirstSearch(initialBoard, goalBoard)
if solutionPath:
    print("Solution found:")
    for step in solutionPath:
        print(step)
else:
    print("No solution found.")
