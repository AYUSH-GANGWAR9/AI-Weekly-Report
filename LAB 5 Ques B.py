import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler

def fetchStockData(stockTicker, startPeriod, endPeriod):
    stockData = yf.download(stockTicker, start=startPeriod, end=endPeriod)
    stockData['Returns'] = stockData['Adj Close'].pct_change().dropna()
    return stockData

def extractReturns(stockData):
    stockData = stockData.dropna(subset=['Returns'])
    returnValues = stockData['Returns'].values.reshape(-1, 1)
    return returnValues

def trainHMM(returns, numStates=2):
    hmmModel = GaussianHMM(n_components=numStates, covariance_type="full", n_iter=1000)
    hmmModel.fit(returns)
    hiddenStates = hmmModel.predict(returns)
    return hmmModel, hiddenStates

def displayStates(stockData, hiddenStates, model):
    stockData['Hidden State'] = hiddenStates
    fig, axs = plt.subplots(model.n_components, figsize=(10, 6))
    for i, ax in enumerate(axs):
        stateData = stockData[stockData['Hidden State'] == i]
        ax.plot(stateData.index, stateData['Adj Close'], label=f'State {i}')
        ax.set_title(f'State {i}')
        ax.legend()
    plt.show()

def evaluateStock(ticker, startDate, endDate, numStates=2):
    stockData = fetchStockData(ticker, startDate, endDate)
    returns = extractReturns(stockData)
    scaler = StandardScaler()
    scaledReturns = scaler.fit_transform(returns)
    hmmModel, hiddenStates = trainHMM(scaledReturns, numStates)
    displayStates(stockData, hiddenStates, hmmModel)
    return hmmModel, stockData

stockTicker = "AAPL"
startDate = "2015-01-01"
endDate = "2023-01-01"

hmmModel, stockDataWithStates = evaluateStock(stockTicker, startDate, endDate)

print("Transition Matrix")
print(hmmModel.transmat_)

print("\nMeans and Variances of Each Hidden State")
for i in range(hmmModel.n_components):
    print(f"\nState {i}")
    print("Mean = ", hmmModel.means_[i])
    print("Variance = ", np.diag(hmmModel.covars_[i]))
