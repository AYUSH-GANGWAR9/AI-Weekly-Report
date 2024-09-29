import random
import math

def calculateCost(puzzle):
    totalCost = 0
    for row in range(512):
        for col in range(512):
            if col + 1 != 512 and (col + 1) % 128 == 0:
                totalCost += abs(int(puzzle[(512 * row) + col]) - int(puzzle[(512 * row) + col + 1]))
            if row + 1 != 512 and (row + 1) % 128 == 0:
                totalCost += abs(int(puzzle[(512 * row) + col]) - int(puzzle[(512 * (row + 1)) + col]))
    return totalCost

def exchangePieces(puzzle):
    firstIndex, secondIndex = random.sample(range(16), 2)
    firstRow = int(firstIndex / 4)
    secondRow = int(secondIndex / 4)
    firstCol = int(firstIndex % 4)
    secondCol = int(secondIndex % 4)
    firstRowNum = int(128 * firstRow)
    secondRowNum = int(128 * secondRow)
    firstColNum = int(128 * firstCol)
    secondColNum = int(128 * secondCol)
    piece1 = []
    piece2 = []
    for i in range(128):
        for j in range(128):
            if (512 * (firstRowNum + i)) + (firstColNum + j) >= 262144:
                print(i, j, firstRowNum, firstColNum)
            piece1.append(puzzle[(512 * (firstRowNum + i)) + (firstColNum + j)])
    for i in range(128):
        for j in range(128):
            piece2.append(puzzle[(512 * (secondRowNum + i)) + (secondColNum + j)])
    for i in range(128):
        for j in range(128):
            puzzle[(512 * (firstRowNum + i)) + (firstColNum + j)] = piece2[(i * 128) + j]
    for i in range(128):
        for j in range(128):
            puzzle[(512 * (secondRowNum + i)) + (secondColNum + j)] = piece1[(i * 128) + j]

    return puzzle

def performSimulatedAnnealing(puzzle, initialTemperature, coolingRate, minimumTemperature):
    minimumCost = float('inf')
    optimalState = []
    iterationCount = 0
    temperature = initialTemperature
    currentState = puzzle
    currentCost = calculateCost(currentState)
    
    while temperature > minimumTemperature:
        iterationCount += 1
        newState = exchangePieces(currentState.copy())
        newCost = calculateCost(newState)
        
        if newCost < currentCost:
            currentState = newState
            currentCost = newCost
            if currentCost < minimumCost:
                minimumCost = currentCost
                optimalState = currentState.copy()
        else:
            if random.uniform(0, 1) < math.exp((currentCost - newCost) / temperature):
                currentState = newState
                currentCost = newCost
        
        temperature *= coolingRate 
    
    return optimalState, minimumCost

puzzleData = []
with open('scrambled_lena.mat', 'r') as file:
    for _ in range(5):
        next(file)
    
    for line in file:
        puzzleData.append(line)

finalAnswer = []
minCost = float('inf')
for attempt in range(5):
    initialTemperature = 1000
    coolingRate = 0.99
    minimumTemperature = 0.1
    solvedPuzzle, cost = performSimulatedAnnealing(puzzleData, initialTemperature, coolingRate, minimumTemperature)
    if cost < minCost:
        minCost = cost
        puzzleData = solvedPuzzle.copy()
        finalAnswer = puzzleData
    print(cost)

with open('answer.mat', 'w') as file:
    for item in finalAnswer:
        file.write(f"{item}")
