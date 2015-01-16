# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 10:09:58 2014

@author: Patrick
"""

'''Ablauf: Einlesen Train und Test, Filtern der Laenge 2, Zeitverschiebung
mit Kreuzkorrelation, beste Sensorkombination und Regressionsverfahren 
ermitteln mit MSE als Optimierungskriterium, Regressor speichern'''

import os
import sys
import fnmatch
import numpy as np
import random

#Fix the import path, so that we can import our parent folder with all required modules
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0,parentdir) 


from data_analysis import plotData
from data_analysis.bestRegressor import BestRegressor
from sklearn.externals import joblib
from data_analysis.loadtrain import LoadData
from data_analysis.regressor import Regressor
from mpltools import style

from scipy.stats.stats import pearsonr
from sklearn.metrics import mean_squared_error
import pylab as pl
from matplotlib.pyplot import close

try:
    close("all") 
except:
    pass


def forwinormac():
    if os.name=="nt":
        workdir= os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(workdir)
    if os.name=="posix":
        workdir= os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(workdir)


            
"""Klassen und Arbeitspfad laden"""
forwinormac()
loader=LoadData(sep=",", groundtruth_elements=1,skiprows=1, skipcols=0)
bestRegressor = BestRegressor()
regressor=Regressor()



"""Trainigsdaten laden"""
trainPowerData, trainFeatureData=loader.load_dir('train')

"""Testdaten laden"""
testPowerData, testFeatureData = loader.load_dir('test')

print testPowerData

#print trainPowerData[0:5]


#selection_idx = np.where(testPowerData > 24)
#testPowerData = testPowerData[selection_idx]
#testFeatureData = testFeatureData[selection_idx]

#testPowerData+=26
#trainPowerData+=26


'''
Berechnung des Optimalen Regressionsverfahren und der optimalen Sensorkombination nach MSE
Aufpassen, allSensorCombination bestimmt den besten Regressor mit der errror_func fuer den gesamten
Verlauf, OHNE den fehler für alle XX sekunden zu berechnen und zu mitteln
'''
error_func = mean_squared_error

#resultArray, resultTuple = bestRegressor.allSensorCombinations\
#(trainFeatureData, trainPowerData,testFeatureData,testPowerData, error_func)

resultTuple = bestRegressor.findGoodRegressor\
(trainFeatureData, trainPowerData,testFeatureData,testPowerData, error_func)


predictedPower =  bestRegressor.predictResultArrayEntry\
(resultTuple, trainFeatureData,trainPowerData,testFeatureData)

print("============= Predicted ===============")
print predictedPower

print("============= Real      ===============")
print testPowerData

regressor.printResult(resultTuple)
bestRegressor.printError(predictedPower, testPowerData)
bestRegressor.calculateMABSForChunks(predictedPower, testPowerData)
#meanError, std, errorInPercent = bestRegressor.calculateMABSForChunks(predictedPower, testPowerData)





