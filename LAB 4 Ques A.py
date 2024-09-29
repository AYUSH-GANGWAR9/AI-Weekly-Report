import math
import random
import time

def calculateEuclideanDistance(cityA, cityB):
    return math.sqrt((cityA[0] - cityB[0])**2 + (cityA[1] - cityB[1])**2)

def getTotalDistance(tourPath):
    return sum(calculateEuclideanDistance(tourPath[i], tourPath[(i + 1) % len(tourPath)]) for i in range(len(tourPath)))

def performSimulatedAnnealing(cityList, initialTemperature=10000, coolingFactor=0.995, minimumTemperature=1e-8, maxIterations=1000000):
    currentTourPath = cityList[:]
    bestTourPath = currentTourPath[:]
    numCities = len(cityList)
    
    iterationCount = 1
    while initialTemperature > minimumTemperature and iterationCount < maxIterations:
        [index1, index2] = sorted(random.sample(range(numCities), 2))
        newTourPath = currentTourPath[:]
        newTourPath[index1:index2 + 1] = reversed(newTourPath[index1:index2 + 1])
        
        currentDistance = getTotalDistance(currentTourPath)
        newDistance = getTotalDistance(newTourPath)
        
        if newDistance < currentDistance:
            currentTourPath = newTourPath
            if newDistance < getTotalDistance(bestTourPath):
                bestTourPath = newTourPath
        elif random.random() < math.exp((currentDistance - newDistance) / initialTemperature):
            currentTourPath = newTourPath
        
        initialTemperature *= coolingFactor
        iterationCount += 1
    
    return bestTourPath, getTotalDistance(bestTourPath)

citiesList = [
    ("Jaipur", (26.9124, 75.7873)),
    ("Udaipur", (24.5854, 73.6684)),
    ("Jodhpur", (26.2389, 73.0243)),
    ("Ajmer", (26.4499, 74.6399)),
    ("Bikaner", (28.0229, 73.3120)),
    ("Pushkar", (26.4851, 74.6100)),
    ("Chittorgarh", (24.8796, 74.6293)),
    ("Jaisalmer", (26.9157, 70.9160)),
    ("Mount Abu", (24.5921, 72.7014)),
    ("Sikar", (27.6106, 75.1393)),
    ("Neemrana", (27.9852, 76.4577)),
    ("Kota", (25.1638, 75.8644)),
    ("Tonk", (26.0899, 75.7889)),
    ("Barmer", (25.7410, 71.4280)),
    ("Bundi", (25.4472, 75.6306)),
    ("Rani Sati Dadi Temple", (26.1865, 75.0499)),
    ("Sawai Madhopur", (26.0252, 76.3398)),
    ("Fatehpur Sikri", (27.0977, 77.6616)),
    ("Rajasthan", (26.5290, 74.6100)),
    ("Mandawa", (27.1500, 75.2520)),
    ("Jhalawar", (23.5867, 76.1632))
]

cityCoordinatesList = [city[1] for city in citiesList]

startExecutionTime = time.time()
bestTourPath, bestTourDistance = performSimulatedAnnealing(cityCoordinatesList)
endExecutionTime = time.time()

print(f"Number of cities: {len(cityCoordinatesList)}")
print(f"Best distance found: {bestTourDistance:.2f}")
print(f"Time taken: {endExecutionTime - startExecutionTime:.2f} seconds")
