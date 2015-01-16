# -*- coding: utf-8 -*-
"""
Created on Tue Aug 05 14:45:18 2014

@author: Patrick
"""
import os
import sys
import fnmatch
import numpy as np
from bestRegressor import BestRegressor
from loadtrain import LoadData
from regressor import Regressor
import pylab as pl
from sklearn.metrics import mean_squared_error
from mpltools import style
close("all") 


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

cachelist=os.listdir('train')
trainlist=fnmatch.filter(cachelist,'*.csv')
cachelist=os.listdir('test')
testlist=fnmatch.filter(cachelist,'*.csv')


"""Trainigsdaten laden"""
trainFeatureData=loader.getFeaturesData('train/'+trainlist[0])
trainPowerData=loader.getPowerData('train/'+trainlist[0])



"""extra Training"""
if len(trainlist) >1:
    for i in xrange(1,len(trainlist)):
        string='train/'+trainlist[i]
        print string
        extraTrainFeatureData=loader.getFeaturesData(string)
        extraTrainPowerData=loader.getPowerData(string)
        
        trainFeatureData=np.append(trainFeatureData,extraTrainFeatureData,0)
        trainPowerData=np.append(trainPowerData,extraTrainPowerData,0)

"""Testdaten laden"""
testFeatureData=loader.getFeaturesData('test/'+testlist[0])
testPowerData=loader.getPowerData('test/'+testlist[0])



pl.subplot(8,1,1)
pl.plot(np.sort(trainFeatureData[:,0]),label='CPU')

pl.subplot(8,1,2)
pl.hist(np.sort(trainFeatureData[:,0]))

  
pl.show()
