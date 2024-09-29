import heapq
import re

class TextNode:
    def __init__(self, state, parent=None, gCost=0, hCost=0):
        self.state = state
        self.parent = parent
        self.g = gCost
        self.h = hCost
        self.f = gCost + hCost

    def __lt__(self, otherNode):
        return self.f < otherNode.f

def cleanText(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def calculateEditDistance(str1, str2):
    len1, len2 = len(str1), len(str2)
    dpMatrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    for i in range(len1 + 1):
        for j in range(len2 + 1):
            if i == 0:
                dpMatrix[i][j] = j
            elif j == 0:
                dpMatrix[i][j] = i
            elif str1[i-1] == str2[j-1]:
                dpMatrix[i][j] = dpMatrix[i-1][j-1]
            else:
                dpMatrix[i][j] = 1 + min(dpMatrix[i-1][j], dpMatrix[i][j-1], dpMatrix[i-1][j-1])
    
    return dpMatrix[len1][len2]

def getNeighbors(currentNode, text1, text2):
    neighborList = []
    idx1, idx2 = currentNode.state

    if idx1 < len(text1) and idx2 < len(text2):
        newState = (idx1 + 1, idx2 + 1)
        neighbor = TextNode(newState, currentNode)
        neighborList.append(neighbor)

    if idx1 < len(text1):
        newState = (idx1 + 1, idx2)
        neighbor = TextNode(newState, currentNode)
        neighborList.append(neighbor)

    if idx2 < len(text2):
        newState = (idx1, idx2 + 1)
        neighbor = TextNode(newState, currentNode)
        neighborList.append(neighbor)

    return neighborList

def heuristicCost(state, text1, text2):
    idx1, idx2 = state
    return ((len(text1) - idx1) + (len(text2) - idx2)) / 2

def performAStarSearch(text1, text2):
    startNode = TextNode((0, 0))
    goalState = (len(text1), len(text2))
    openNodes = []
    heapq.heappush(openNodes, (startNode.f, startNode))
    exploredStates = set()

    while openNodes:
        _, currentNode = heapq.heappop(openNodes)
        
        if currentNode.state in exploredStates:
            continue
        
        exploredStates.add(currentNode.state)

        if currentNode.state == goalState:
            alignmentPath = []
            while currentNode:
                alignmentPath.append(currentNode.state)
                currentNode = currentNode.parent
            return alignmentPath[::-1]

        for neighbor in getNeighbors(currentNode, text1, text2):
            idx1, idx2 = neighbor.state
            if idx1 < len(text1) and idx2 < len(text2):
                neighbor.g = currentNode.g + calculateEditDistance(text1[idx1], text2[idx2])
            else:
                neighbor.g = currentNode.g + 1
            neighbor.h = heuristicCost(neighbor.state, text1, text2)
            neighbor.f = neighbor.g + neighbor.h
            heapq.heappush(openNodes, (neighbor.f, neighbor))

    return None

def alignSentences(text1, text2):
    return performAStarSearch(text1, text2)

def plagiarismDetection(text1, text2, similarityThreshold=0.5):
    text1 = [cleanText(sentence) for sentence in text1]
    text2 = [cleanText(sentence) for sentence in text2]

    alignment = alignSentences(text1, text2)
    plagiarizedSections = []
    
    for idx1, idx2 in alignment:
        if idx1 < len(text1) and idx2 < len(text2):
            sentence1, sentence2 = text1[idx1], text2[idx2]
            maxLength = max(len(sentence1), len(sentence2))
            if maxLength > 0:
                similarityScore = 1 - (calculateEditDistance(sentence1, sentence2) / maxLength)
                if similarityScore >= similarityThreshold:
                    plagiarizedSections.append((text1[idx1], text2[idx2], similarityScore))
    
    return plagiarizedSections

inputText1 = [
    "Artificial intelligence is transforming various industries.",
    "Machine learning models are increasingly being adopted.",
    "Data science combines statistics, data analysis, and machine learning.",
    "Deep learning is a subset of machine learning.",
]

inputText2 = [
    "Artificial intelligence is changing multiple sectors.",
    "Models based on machine learning are being utilized more.",
    "The field of data science includes statistics and data analysis.",
    "Neural networks are a part of deep learning."   
]

plagiarismResults = plagiarismDetection(inputText1, inputText2)
if plagiarismResults:
    print("Potential plagiarism detected:")
    for result in plagiarismResults:
        print(f"Text1: {result[0]} \nText2: {result[1]} \nSimilarity: {result[2]}")
else:
    print("No plagiarism detected.")
