import heapq

def calculateManhattanDistance(state, goalState):
    totalDistance = 0
    for tile in range(1, 9):
        xi, yi = divmod(state.index(tile), 3)
        xg, yg = divmod(goalState.index(tile), 3)
        totalDistance += abs(xi - xg) + abs(yi - yg)
    return totalDistance

class PuzzleNode:
    def __init__(self, boardState, parentNode=None, gValue=0, hValue=0):
        self.state = boardState
        self.parent = parentNode
        self.g = gValue
        self.h = hValue
        self.f = gValue + hValue

    def __lt__(self, otherNode):
        return self.f < otherNode.f

def generateSuccessors(currentNode, goalState):
    blankTileIndex = currentNode.state.index(0)
    successorsList = []
    possibleMoves = [-1, 1, 3, -3]
    
    for move in possibleMoves:
        newIndex = blankTileIndex + move
        if 0 <= newIndex < 9:
            newState = list(currentNode.state)
            newState[blankTileIndex], newState[newIndex] = newState[newIndex], newState[blankTileIndex]
            gValue = currentNode.g + 1
            hValue = calculateManhattanDistance(newState, goalState)
            nextNode = PuzzleNode(newState, currentNode, gValue, hValue)
            successorsList.append(nextNode)
    
    return successorsList

def aStarSearch(startBoard, goalBoard):
    startNode = PuzzleNode(startBoard, None, 0, calculateManhattanDistance(startBoard, goalBoard))
    goalNode = PuzzleNode(goalBoard)
    openNodes = []
    heapq.heappush(openNodes, startNode)
    exploredStates = set()
    totalExploredNodes = 0
    
    while openNodes:
        currentNode = heapq.heappop(openNodes)
        
        if tuple(currentNode.state) in exploredStates:
            continue
        
        exploredStates.add(tuple(currentNode.state))
        totalExploredNodes += 1
        
        if currentNode.state == goalNode.state:
            solutionPath = []
            while currentNode:
                solutionPath.append(currentNode.state)
                currentNode = currentNode.parent
            print('Total nodes explored:', totalExploredNodes)
            return solutionPath[::-1]
        
        for successor in generateSuccessors(currentNode, goalBoard):
            if tuple(successor.state) not in exploredStates:
                heapq.heappush(openNodes, successor)

    print('Total nodes explored:', totalExploredNodes)
    return None

initialBoard = [1, 2, 3, 4, 5, 6, 7, 8, 0]
goalBoard = [1, 2, 3, 4, 5, 6, 0, 7, 8]

solutionPath = aStarSearch(initialBoard, goalBoard)
if solutionPath:
    print("Solution found:")
    for step in solutionPath:
        print(step)
else:
    print("No solution found.")
