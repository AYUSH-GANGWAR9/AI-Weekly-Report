import random
from music21 import stream, note, midi

raagBhairavAsc = ['C', 'C#', 'E', 'F', 'G', 'G#', 'B']
raagBhairavDesc = ['C', 'B', 'G#', 'G', 'F', 'E', 'C#']

def createMelody(length):
    melody = []
    for _ in range(length):
        swara = random.choice(raagBhairavAsc if random.random() > 0.5 else raagBhairavDesc)
        melody.append(swara)
    return melody

def calculateFitness(melody):
    fitnessScore = 0

    for i in range(len(melody) - len(raagBhairavAsc) + 1):
        if melody[i:i + len(raagBhairavAsc)] == raagBhairavAsc:
            fitnessScore += 10 

        for j in range(2, len(raagBhairavAsc)):
            if melody[i:i + j] == raagBhairavAsc[:j]:
                fitnessScore += j  

    for i in range(len(melody) - len(raagBhairavDesc) + 1):
        if melody[i:i + len(raagBhairavDesc)] == raagBhairavDesc:
            fitnessScore += 10  

        for j in range(2, len(raagBhairavDesc)):
            if melody[i:i + j] == raagBhairavDesc[:j]:
                fitnessScore += j 

    return fitnessScore

def performCrossover(parent1, parent2):
    split = random.randint(1, len(parent1) - 1)
    child1 = parent1[:split] + parent2[split:]
    child2 = parent2[:split] + parent1[split:]
    return child1, child2

def applyMutation(melody, mutationRate=0.1):
    for i in range(len(melody)):
        if random.random() < mutationRate:
            melody[i] = random.choice(raagBhairavAsc if random.random() > 0.5 else raagBhairavDesc)
    return melody

def runGeneticAlgorithm(generations=1000, populationSize=100, mutationRate=0.6, melodyLength=64):
    population = [createMelody(melodyLength) for _ in range(populationSize)]
    
    for generation in range(generations):
        fitnessScores = [(melody, calculateFitness(melody)) for melody in population]
        fitnessScores.sort(key=lambda x: x[1], reverse=True)
        
        bestMelody = fitnessScores[0][0]
        print(f"Generation {generation}: Best Melody: {' '.join(bestMelody)} with Fitness: {fitnessScores[0][1]}")

        selected = [melody for melody, score in fitnessScores[:populationSize // 2]]

        nextPopulation = []
        while len(nextPopulation) < populationSize:
            parent1, parent2 = random.sample(selected, 2)
            child1, child2 = performCrossover(parent1, parent2)
            nextPopulation.append(applyMutation(child1, mutationRate))
            nextPopulation.append(applyMutation(child2, mutationRate))

        population = nextPopulation

    return bestMelody

def convertMelodyToStream(melody):
    melodyStream = stream.Stream()
    for swara in melody:
        n = note.Note(swara)
        melodyStream.append(n)
    return melodyStream

bestMelody = runGeneticAlgorithm()
melodyStream = convertMelodyToStream(bestMelody)

mf = midi.translate.music21ObjectToMidiFile(melodyStream)
mf.open("raag_bhairav_melody_corrected.mid", 'wb')
mf.write()
mf.close()
