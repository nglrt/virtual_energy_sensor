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
import plotData
from bestRegressor import BestRegressor
from sklearn.externals import joblib
from loadtrain import LoadData
from regressor import Regressor
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
loader=LoadData()
bestRegressor = BestRegressor()
regressor=Regressor()



"""Trainigsdaten laden"""
<<<<<<< HEAD:exp3_longterm/createRegressor.py
trainPowerData, trainFeatureData=loader.load_dir('train_pl_monitor')

"""Testdaten laden"""
testPowerData, testFeatureData = loader.load_dir('test_pl_monitor')
=======
trainPowerData, trainFeatureData=loader.load_dir('train_fe')

"""Testdaten laden"""
testPowerData, testFeatureData = loader.load_dir('test_fe')
>>>>>>> d0a00ffb888c82ef5656498123b981637318ddf9:data_analysis/createRegressor.py


selection_idx = np.where(testPowerData > 24)
testPowerData = testPowerData[selection_idx]
testFeatureData = testFeatureData[selection_idx]

#testPowerData+=26
#trainPowerData+=26

#selection = np.where(testPowerData>16)
#testPowerData = testPowerData[selection]
#testFeatureData = testFeatureData[selection]

"""Filterung der aller Daten mit Filtersize = 2"""

filterSize = 2



filteredTrainPowerData, filteredTrainFeatureData, filteredTestPowerData, filteredTestFeatureData = \
bestRegressor.FilterTrainAndTest(filterSize, trainPowerData,testPowerData,trainFeatureData,testFeatureData)



'''
Train- und TestPowerData zeitlich verschieben fuer hochste Korrelation
'''
filteredTrainPowerData = bestRegressor.compareAndShift(filteredTrainFeatureData, filteredTrainPowerData)
filteredTestPowerData = bestRegressor.compareAndShift(filteredTestFeatureData,filteredTestPowerData)   

'''
Berechnung des Optimalen Regressionsverfahren und der optimalen Sensorkombination nach MSE
Aufpassen, allSensorCombination bestimmt den besten Regressor mit der errror_func fuer den gesamten
Verlauf, OHNE den fehler für alle XX sekunden zu berechnen und zu mitteln
'''

<<<<<<< HEAD:exp3_longterm/createRegressor.py
error_func = mean_squared_error
resultArray, resultTuple = bestRegressor.allSensorCombinations\
(filteredTrainFeatureData, filteredTrainPowerData,filteredTestFeatureData,filteredTestPowerData, error_func)

#resultTuple = (2,96)
#resultTuple = (3,int('1111111', 2))


=======
resultTuple = (3,112)
#resultTuple = (7,int('1011111', 2))
>>>>>>> d0a00ffb888c82ef5656498123b981637318ddf9:data_analysis/createRegressor.py

regressor.printResult(resultTuple)
#bestRegressor.saveRegressor(resultTuple, filteredTrainFeatureData, filteredTrainPowerData)

predictedPower =  bestRegressor.predictResultArrayEntry\
(resultTuple, filteredTrainFeatureData,filteredTrainPowerData,filteredTestFeatureData)

bestRegressor.printError(predictedPower, filteredTestPowerData)

meanError, std, errorInPercent = bestRegressor.calculateMABSForChunks(predictedPower, filteredTestPowerData)


style.use('ggplot')
cpu,difReadTimeMainHD,difWriteTimeMainHD,difReadTimeSecondHD,difWriteTimeSecondHD,difPackets_sent,difPackets_recv,=np.split(filteredTestFeatureData,7,1)

pl.figure(0)
plotData.printDiffSensors(predictedPower, filteredTestPowerData, filteredTestFeatureData)

pl.figure(1)
#pl.ylim([12,24])
pl.subplot(2,1,1)
#pl.xlim([0,580])
pl.plot(filteredTestPowerData,label='Plugwise Power [W]')    
pl.plot(predictedPower,marker = '.', label = 'Regressor Power [W]')
pl.legend(loc = 9)
pl.subplot(2,1,2)
#pl.xlim([0,580])
pl.plot(cpu, label = 'CPU Load [%]')
#pl.xlabel('Time [s]')
#pl.ylabel('Power [W]')
pl.legend(loc= 9)




