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

print sys.path

from sklearn.externals import joblib
from data_analysis.loadtrain import LoadData
from data_analysis.regressor import Regressor
from data_analysis import plotData
from data_analysis.bestRegressor import BestRegressor

from scipy.stats.stats import pearsonr
from sklearn.metrics import mean_squared_error
import pylab as pl
#close("all") 



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


"""Testdaten laden"""
trainPowerData, trainFeatureData = loader.load_dir("train/")
testPowerData, testFeatureData = loader.load_dir("test/")

testPowerData = testPowerData[1000:]
testFeatureData = testFeatureData[1000:,:]


def autocorr(x):
    x_ = np.zeros(x.shape)
    
    fold = 1000    
    
    x_[0:fold] = x[0:fold]    
    
    result = numpy.correlate(x,x_, mode='full')
    max_ = np.sum(x*x_)
    return result/max_
    
pl.plot(autocorr(testPowerData))
#pl.plot(testPowerData)

print trainPowerData.shape

"""Trainingsdaten/Testpowerdata mithilfe der Kreuzkorrelation verschieben um zeitliche Verzoegerung des Plugwise zu kompensieren"""

shift = True
#shift = False
if(shift):

    #shiften der Trainings und Testdaten    
    #training
    trainCpu = trainFeatureData[:,0]
    num_samples_to_shift = bestRegressor.calculateTimelag(trainCpu, trainPowerData)
    trainPowerData = bestRegressor.shiftArray(trainPowerData,num_samples_to_shift)
    print "Time lag during training: {0} samples".format(num_samples_to_shift)
       
    #testdaten
    testCpu = testFeatureData[:,0]    
    #num_samples_to_shift = bestRegressor.calculateTimelag(testCpu, testPowerData)
    testPowerData = bestRegressor.shiftArray(testPowerData,num_samples_to_shift)
    print "Time lag during testing: {0} samples".format(num_samples_to_shift)

    
"""Regressor with all (7) Parameters"""
#dtR_pred     = regressor.getDTR(trainFeatureData,trainPowerData,testFeatureData)
#etR_pred     = regressor.getETR(trainFeatureData,trainPowerData,testFeatureData)
#rfR_pred     = regressor.getRFR(trainFeatureData,trainPowerData,testFeatureData)
#erfR_pred    = regressor.getERFR(trainFeatureData,trainPowerData,testFeatureData)
#knR_pred     = regressor.getKNR(trainFeatureData,trainPowerData,testFeatureData)
#lassoR_pred  = regressor.getLassoR(trainFeatureData,trainPowerData,testFeatureData)
#larsR_pred   = regressor.getLarsR(trainFeatureData,trainPowerData,testFeatureData)
#linearR_pred = regressor.getLinearR(trainFeatureData,trainPowerData,testFeatureData)



"""Dictionary for Function Input"""
#regressor_dictionary = dict(dtR_pred=dtR_pred,etR_pred=etR_pred,rfR_pred=rfR_pred,
#                            erfR_pred=erfR_pred,knR_pred=knR_pred,
#                            lassoR_pred=lassoR_pred,larsR_pred=larsR_pred,
#                            linearR_pred=linearR_pred)




"""Calculate Best Regressor"""

#bestRegressor.totalError(testPowerData, regressor_dictionary)
#bestRegressor.leastSquare(testPowerData, regressor_dictionary)
#bestRegressor.crossCorrelationWithShift(testPowerData, regressor_dictionary)
#bestRegressor.absError(testPowerData, regressor_dictionary)
#resultArray = bestRegressor.allSensorPairs(trainFeatureData, trainPowerData, testFeatureData, testPowerData)
#resultTuple = bestRegressor.bestCombination(resultArray)

"""ERROR FUNC POSSIBILITIES:"""
error_func = pearsonr
#error_func = mean_squared_error
#error_func = bestRegressor.meanTotalError
#error_func = bestRegressor.meanAbsError

#resultArray, resultTuple = bestRegressor.allSensorCombinations(trainFeatureData, trainPowerData,testFeatureData[0:50], testPowerData[0:50], error_func)

resultTuple = (7,int('11111111111111111', 2))
#resultTuple = (7,76)

#print '{0:07b}'.format(resultTuple[1]) 


#predictedPower =  bestRegressor.predictResultArrayEntry(resultTuple, trainFeatureData,trainPowerData,testFeatureData)
#regressor.printResult(resultTuple)
#bestRegressor.saveRegressor(resultTuple, trainFeatureData, trainPowerData)
#bestRegressor.printError(predictedPower, testPowerData)

predictedPower =  bestRegressor.predictResultArrayEntry(resultTuple, trainFeatureData,trainPowerData,testFeatureData)
#bestRegressor.saveRegressor(resultTuple, bestRegressor.normSensorValues(trainFeatureData), trainPowerData)

#Our regressor
bestRegressor.printMeanMedianError(trainPowerData, testPowerData)


print("=======================")
print("Our regressor (%s)"%6)
print("=======================")
bestRegressor.printError(predictedPower, testPowerData)


#errors_ = bestRegressor.calculateErrorForChunks(predictedPower, testPowerData)

#pl.plot(errors_[:,3])
#pl.show()

#"""PLOT"""

#plotData.printAllRegressors(testPowerData,regressor_dictionary)
#plotData.printDiffSensors(predictedPower,testPowerData,testFeatureData)
#plotData.printDiffSensors(trainPowerData,trainPowerData,trainFeatureData)
#plotData.printPearson(predictedPower,testPowerData)











