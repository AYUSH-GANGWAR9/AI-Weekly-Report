import pandas as pd
import numpy as np
from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

dataFilePath = '2020_bn_nb_data.txt'
studentGradesData = pd.read_csv(dataFilePath, delim_whitespace=True)
studentGradesData.columns = ['ec100', 'it101', 'ma101', 'ph100', 'qp']

bayesianGraphModel = BayesianModel([('ec100', 'ph100'), ('it101', 'ph100'), ('ma101', 'ph100')])
bayesianGraphModel.fit(studentGradesData, estimator=MaximumLikelihoodEstimator)

inputStudentGrades = pd.DataFrame(data={
    'ec100': ['DD'],
    'it101': ['CC'],
    'ma101': ['CD']
})

inferenceAlgorithm = VariableElimination(bayesianGraphModel)
predictedPh100Grade = inferenceAlgorithm.map_query(variables=['ph100'], evidence=dict(inputStudentGrades.iloc[0]))
print(f"Predicted grade in PH100 for EC100: DD, IT101: CC, MA101: CD is: {predictedPh100Grade['ph100']}")

featuresGrades = studentGradesData[['ec100', 'it101', 'ma101']]
targetQualification = studentGradesData['qp']

encodedFeatures = featuresGrades.apply(lambda column: column.astype('category').cat.codes)
encodedTarget = targetQualification.astype('category').cat.codes

trialCount = 20
accuracyScores = []

for _ in range(trialCount):
    trainFeatures, testFeatures, trainTarget, testTarget = train_test_split(encodedFeatures, encodedTarget, test_size=0.3, random_state=None)
    
    naiveBayesModel = GaussianNB()
    naiveBayesModel.fit(trainFeatures, trainTarget)
    
    predictions = naiveBayesModel.predict(testFeatures)
    accuracy = accuracy_score(testTarget, predictions)
    accuracyScores.append(accuracy)

averageAccuracy = np.mean(accuracyScores)
print(f"Mean accuracy of Naive Bayes classifier over {trialCount} trials: {averageAccuracy:.2f}")
