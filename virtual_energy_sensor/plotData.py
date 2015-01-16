# -*- coding: utf-8 -*-
"""
Created on Mon May 19 10:20:19 2014

@author: Patrick
"""

import numpy as np
import pylab as pl
"""
Plotzone
"""

pl.rcParams['figure.figsize'] = (20.0, 16.0)

def printAllRegressors(testPowerData,regressor_dictionary):
    t = np.arange(0.0,testPowerData.size,1)
    
    pl.subplot(8,1,1)
    pl.plot(t,testPowerData,label='Plugwise')
    pl.plot(t,regressor_dictionary["dtR_pred"],label='DTR')
    pl.legend()
    
    pl.subplot(8,1,2)
    pl.plot(t,testPowerData,label='Plugwise')
    pl.plot(t,regressor_dictionary["etR_pred"],label='ETR')
    pl.legend()
    
    pl.subplot(8,1,3)
    pl.plot(t,testPowerData,label='Plugwise')
    pl.plot(t,regressor_dictionary["rfR_pred"],label='RFR')
    pl.legend()
    
    pl.subplot(8,1,4)
    pl.plot(t,testPowerData,label='Plugwise')
    pl.plot(t,regressor_dictionary["erfR_pred"],label='ERFR')
    pl.legend()
    
    pl.subplot(8,1,5)
    pl.plot(t,testPowerData,label='Plugwise')
    pl.plot(t,regressor_dictionary["knR_pred"],label='KNR')
    pl.legend()
    
    pl.subplot(8,1,6)
    pl.plot(t,testPowerData,label='Plugwise')
    pl.plot(t,regressor_dictionary["lassoR_pred"],label='LassoR')
    pl.legend()
    
    pl.subplot(8,1,7)
    pl.plot(t,testPowerData,label='Plugwise')
    pl.plot(t,regressor_dictionary["larsR_pred"],label='LarsR')
    pl.legend()
    
    pl.subplot(8,1,8)
    pl.plot(t,testPowerData,label='Plugwise')
    pl.plot(t,regressor_dictionary["linearR_pred"],label='LinearR')
    pl.legend()
    
    pl.show()


"""Plot + Parameter"""
def printDiffSensors(regressor,testPowerData,testFeatureData):   
    t = np.arange(0.0,testPowerData.size,1)
    #testFeatureData.shape
    len_ = testFeatureData.shape[1]
    
    pl.subplot(len_+1,1,1)
    pl.plot(t,regressor,label='Predicted Power')
    pl.plot(t,testPowerData,label='Plugwise')    
    #pl.plot(t,cpu,label='CPU-Idle')
    pl.legend()
    
    labels = ["cpu","difReadTimeMainHD","difWriteTimeMainHD",
                     "difReadTimeSecondHD","difWriteTimeSecondHD",
                     "self.difPackets_sent","self.difPackets_recv",  
                     "self.batteryEnergyChange", "self.batteryChargeInPercent", 
                     "self.readCountHdd", "self.writeCountHdd", "self.cpu_user",
                     "self.cpu_idle", "self.cpu_iowait", "self.cpu_irq", "self.cpu_softirq",
                     "self.cpu_clock"]
    
    #cpu,difReadTimeMainHD,difWriteTimeMainHD,difReadTimeSecondHD,difWriteTimeSecondHD,difPackets_sent,difPackets_recv,=np.split(testFeatureData[:,0:7],7,1)
    
    for i in range(len_):
    
        pl.subplot(len_+2,1,i+2)
        pl.plot(t,testFeatureData[:,i], label=labels[i]) # TODO: add label again
        pl.legend()
    
    
    pl.show()

"""Plot + Parameter"""
def printRealAndPredicted(predictedPowerData,testPowerData):   
    t = np.arange(0.0,testPowerData.size,1)
    #testFeatureData.shape
    
    pl.plot(t,predictedPowerData,label='Predicted Power')
    pl.plot(t,testPowerData,label='Plugwise')    
    #pl.plot(t,cpu,label='CPU-Idle')
    pl.legend()
    
    pl.show()

    
def printPearson(predictedPower,testPowerData):   
    pl.subplot(1,1,1)
    pl.axis([10, 35, 10, 35])
    t = np.arange(0.0,testPowerData.size,1)
    
    pl.plot(predictedPower, testPowerData,'bo',label='PearsonRegression')
    pl.plot(t, t,'rx',label='Maximal Correlation') 
    pl.xlabel('predicted Power')    
    pl.ylabel('Plugwise')
    pl.legend()
    pl.show()