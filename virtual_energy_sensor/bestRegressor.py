# -*- coding: utf-8 -*-
"""
Created on Fri May 16 15:20:37 2014

@author: Patrick
"""
import numpy as np
from regressor import Regressor
from scipy.stats.stats import pearsonr
from sklearn.metrics import mean_squared_error


class BestRegressor():

    def __init__(self):
        self.reg = Regressor()
        self.regressorNames = ["DTR","ETR","RFR","ERFR","KNR","LassoR","LarsR","LinearR"]        
        self.regressorList =(self.reg.getDTR,self.reg.getETR,self.reg.getRFR,self.reg.getERFR,self.reg.getKNR,self.reg.getLassoR,self.reg.getLarsR,self.reg.getLinearR)           
        
    def shiftArray(self,array, x):  
        """
        Function to shift all elements in an numpy array by x elements 
        either to the right or to the left. 
        
        @returns the new array. The resulting array is padded with the first or last element
        
        """
        ar = np.array(array)       
        if(x>=0):
            ar[x:len(ar)] = array[0:len(array)-x]
            ar[0:x] = array[0]
        else:
            ar[0:len(ar)+x] = array[abs(x):len(array)]
            ar[len(ar)+x:len(ar)] = array[len(array)-1]
            
        return ar
    
    def calculateTimelag(self, trainDataCpu, trainDataPower):
        """
        Calculates the time lag between the recorded CPU trace and the recorded power trace
        
        @returns the time lag between both signals, in number of samples
        """
        
        time_lag = np.argmax(np.array(np.correlate(trainDataCpu,trainDataPower,"full")))-len(trainDataPower)+1
        return time_lag
    
    
    def meanTotalError(self,predicted,testPowerData):
        """
        Calculate Total Error between Real- and Predicted-PowerData 
        """
        
        diff = abs(sum(predicted)-sum(testPowerData))
        result = diff/len(testPowerData)
        return result
        
        
    def meanAbsError(self,predicted,testPowerData):
        """
        Absoluter Fehler - Betragsmetrik
        """
        
        sumLeastSquare = 0        
        for i in range(0,len(testPowerData)):
            sumLeastSquare+= abs(predicted[i] - testPowerData[i])
        result = sumLeastSquare/len(testPowerData)
        return result
            
        
    def allSensorCombinations(self,trainFeatureData, trainPowerData, testFeatureData, testPowerData, error_func=pearsonr):
       
        regressorCount = 8
        SensorCount = len(trainFeatureData[0])    
        resultArray = np.zeros((regressorCount,(2**SensorCount)-1),dtype=float)
        regressorList =(self.reg.getDTR,self.reg.getETR,self.reg.getRFR,self.reg.getERFR,self.reg.getKNR,self.reg.getLassoR,self.reg.getLarsR,self.reg.getLinearR)           
          
        for i in range(0,(2**SensorCount)-1):
            modifiedTrain = self.modifyTrain(trainFeatureData,i)
            for j in range(0,regressorCount):  
                predicted = regressorList[j](modifiedTrain,trainPowerData, testFeatureData)
                if(error_func == pearsonr):   
                    #Negiert, damit minimum bei jeder Errorfunc das optimum ist.
                    resultArray[j,i] = -error_func(predicted,testPowerData)[0]
                else:
                    resultArray[j,i] = error_func(predicted,testPowerData)
                            
        
        bestResult = self.bestCombination(resultArray)  
        print "----------------------------------------"        
        print ("Best Value for optimizing %s:") % error_func 
        print bestResult    
        return resultArray, bestResult               

    def allFeaturesResultTuple(self, trainFeatureData, regressor=3):
        SensorCount = len(trainFeatureData[0]) 
        return regressor, int(self.binaryRepresentationToDecimal(np.ones((SensorCount-1,),dtype=float)))

    def findGoodRegressor(self,trainFeatureData, trainPowerData, testFeatureData, testPowerData, error_func=pearsonr):
        """
        Einzeln jeden Sensor testen. Besten nehmen und wiederholen.
        """        
        regressorCount= len(self.regressorList)
        #goodSensorCombinations werden die beste Sensorkombination eines Regressor in decimal gespeichert
        goodSensorCombinations = np.zeros(regressorCount)
        #goodSensorError speichert den kleinst moeglichen fehler fuer jeden Regressor 1-7
        goodSensorError = np.zeros(regressorCount)
        for z in range(0,regressorCount):  
            result = []
            binaryRepresentation = np.zeros(len(trainFeatureData[0]))
            modifyNumber = 0
            bestResult = 9999
            for j in range(0, len(trainFeatureData[0])):         
                for i in range(0, len(trainFeatureData[0])):
                    if(binaryRepresentation[i] == 0):
                        print(modifyNumber + (1 << i)) 
                        modifiedTrain = self.modifyTrain(trainFeatureData, modifyNumber + (1 << i))
                        predicted = self.regressorList[z](modifiedTrain,trainPowerData, testFeatureData)
                        if(error_func == pearsonr):   
                            #Negiert, damit minimum bei jeder Errorfunc das optimum ist.
                            result.append(-error_func(predicted,testPowerData)[0])
                        else:
                            result.append(error_func(predicted,testPowerData))
                    else:
                        #hier elegantere loesung finden, nAn oder so
                        result.append(9999)
                
                if(min(result)< bestResult):
                    binaryRepresentation[np.argmin(result)] = 1
                    modifyNumber = modifyNumber + 2**np.argmin(result)
                    print self.invertArray(binaryRepresentation)
                    bestResult = min(result)
                    goodSensorError[z] = bestResult
                    result = []
                    
                else:
                    break 
            
            print ("Beste Sensorkombination fuer Regressor %s ist")%(self.regressorNames[z])
            print self.invertArray(binaryRepresentation)
            print self.binaryRepresentationToDecimal(binaryRepresentation)    
            goodSensorCombinations[z] = self.binaryRepresentationToDecimal(binaryRepresentation)
        
        resultTuple = (np.argmin(goodSensorError),int(goodSensorCombinations[np.argmin(goodSensorError)]))
        return resultTuple
        
    def printResultTuple(self, resultTuple, feature_len):
        
        print("=======================")
        print("     Result Tuple      ")
        print("=======================")  
        
        regressor_idx, features =  resultTuple
        print ("Raw result tuple: (%s, %s)"%(regressor_idx, features))
        print ("Regressor ist %s")%(self.regressorNames[regressor_idx])
        
        bin_fmt = "{0:%sb}"%feature_len
        binary = bin_fmt.format(features)     
        
        print("Features: %s" % binary)
     
    def invertArray(self,binaryRepresentation):
        return binaryRepresentation[::-1]            
            
    def binaryRepresentationToDecimal(self, binaryRepresentation):
        result = 0        
        for i in range(0,len(binaryRepresentation)):
            if(binaryRepresentation[i] == 1):            
                result = result + 2**i
        return result
    
    def bestCombination(self,resultArray):
        #best Combination for pearsonr        
        #return np.unravel_index(np.nanargmax(abs(resultArray)),resultArray.shape)
        return np.unravel_index(np.nanargmin(resultArray),resultArray.shape)
        
        
    """Erstellt neue Trainingsdaten nur mit Sensor i, Reihenfolge 0-6 = "Cpu","HD1 read","HD1 write","HD2 read","HD2 write","Network sent","Network received"""     
    
        
    def modifyTrain(self,trainFeatureData, i):    
        modifiedTrain = np.zeros((len(trainFeatureData),len(trainFeatureData[0])),dtype=float)
        #7 mit len(trainFeatureData[0]) ersetzen     
        bin_fmt = "{0:%sb}"%len(trainFeatureData[0])
        
        binary = bin_fmt.format(i)     
        for j in range(0,len(trainFeatureData[0])):
            if(binary[j] == "1"):
                modifiedTrain[:,j] = trainFeatureData[:,j]
        
        return modifiedTrain    
    
    def predictResultArrayEntry(self, resultTuple, trainFeatureData,trainPowerData,testFeatureData):
                 
        regressorList =(self.reg.getDTR,self.reg.getETR,self.reg.getRFR,self.reg.getERFR,self.reg.getKNR,self.reg.getLassoR,self.reg.getLarsR,self.reg.getLinearR)
        modifiedTrain = self.modifyTrain(trainFeatureData, resultTuple[1])
        predicted = regressorList[resultTuple[0]](modifiedTrain,trainPowerData,testFeatureData)
        return predicted   
        
    def saveRegressor(self, resultTuple, trainFeatureData, trainPowerData):
        
        regressorSaver =(self.reg.saveDTR,self.reg.saveETR,self.reg.saveRFR,self.reg.saveERFR,
                        self.reg.saveKNR,self.reg.saveLassoR,self.reg.saveLarsR,self.reg.saveLinearR)
        modifiedTrain = self.modifyTrain(trainFeatureData, resultTuple[1])
        regressorSaver[resultTuple[0]](modifiedTrain,trainPowerData)    
    
    def calculateErrorForChunks(self, predictedPower, realPower, chunk_len=60):
        """
        Calculates the error for small chunks of the input data. The chunk len
        hereby is configurable
        """
        result = np.zeros((len(predictedPower)/chunk_len+1, 4))
        for i in range(0, len(predictedPower), chunk_len):
            pearson_err = pearsonr(predictedPower[i:i+chunk_len],realPower[i:i+chunk_len])[0]
            ms_err = mean_squared_error(predictedPower[i:i+chunk_len],realPower[i:i+chunk_len])
            mt_err = self.meanTotalError(predictedPower[i:i+chunk_len],realPower[i:i+chunk_len])
            mabs_err = self.meanAbsError(predictedPower[i:i+chunk_len],realPower[i:i+chunk_len])
            
            result[i/chunk_len][0] = pearson_err
            result[i/chunk_len][1] = ms_err
            result[i/chunk_len][2] = mt_err
            result[i/chunk_len][3] = mabs_err
            
        return result
        
    def calculateMABSForChunks(self, predictedPower, realPower, chunk_len=60):
        """
        Calculates the mean absolute error for small chunks of the input data. The chunk len
        hereby is configurable.Return mean error, std, and mean error in %. 
        """
        result = np.zeros(len(predictedPower)/chunk_len+1)
        for i in range(0, len(predictedPower), chunk_len):
            mabs_err = self.meanAbsError(predictedPower[i:i+chunk_len],realPower[i:i+chunk_len])
            
            result[i/chunk_len] = mabs_err
        
        meanError = np.mean(result)
        std = np.std(result)
        errorInPercent = (meanError/np.mean(realPower))*100
        print '------------------'    
        print ('MABS Error for %d second chunks:')%(chunk_len)    
        print ('Mean Error: %f')%(meanError)  
        print ('Standard Deviation: %f')%(std)
        print ('Mean Power: %f')%(np.mean(realPower))
        print ('Mean Error in Percent: %f')%(errorInPercent)  
        
        return meanError, std, errorInPercent        
    
    def printError(self, predictedPower, testPowerData):
        
        print "Pearson Correlation:"
        print pearsonr(predictedPower,testPowerData)[0]
        
        print "MSE:"
        print mean_squared_error(predictedPower,testPowerData)
        
        print "Mean total Error in Watt pro Sample:"
        print self.meanTotalError(predictedPower,testPowerData)
        
        print "Mean Abs Error in Watt pro Sample:"
        print self.meanAbsError(predictedPower,testPowerData)
        
        print "Mean Rel Error [%]"
        print 100 - 100*(np.mean(testPowerData) / np.mean(predictedPower))   
        
        
    def printMeanMedianError(self,trainPowerData,testPowerData):
        print "------------------------"
        print "MEDIAN %f Watt" % (np.median(trainPowerData))
        medianArray = np.copy(testPowerData)
        medianArray[:] = np.median(trainPowerData)
        self.printError(medianArray, testPowerData)
        print "------------------------"
        print "MEAN = %f Watt"  % (np.mean(trainPowerData))
        meanArray = np.copy(testPowerData)
        meanArray[:] = np.mean(trainPowerData)
        self.printError(meanArray, testPowerData)



    
    
    """Plugwisedaten, also TrainPowerData und TestPowerData Verlaeufe filtern"""
    """plugwiseData = zu filternde Daten, filterSize = Groesse des Arrays fuer die Faltung, ConvolveMode= full, valid, same, optional"""        
    def filterData(self,plugwiseData,filterSize,ConvolveMode):
        convolveArray = []
        for i in range(0,filterSize):
            convolveArray.append(1.0/filterSize)        
        result =  np.convolve(plugwiseData, convolveArray,ConvolveMode)
        return result

        
    def FilterTrainAndTest(self,filterSize, trainPowerData,testPowerData,trainFeatureData,testFeatureData):
        #Trainings un d Testdaten filtern
        filteredTrainPowerData = self.filterData(trainPowerData, filterSize, 'valid')
        filteredTestPowerData = self.filterData(testPowerData, filterSize, 'valid')
        
        #Aufpassen, da Array kleiner wird nach der Faltung
        filteredTrainFeatureData = np.zeros([len(filteredTrainPowerData),len(trainFeatureData[0,:])])
        filteredTestFeatureData = np.zeros([len(filteredTestPowerData),len(testFeatureData[0,:])])
        for j in range(0, len(trainFeatureData[0,:])):
            filteredTrainFeatureData[:,j] = self.filterData(trainFeatureData[:,j], filterSize, 'valid')
            filteredTestFeatureData[:,j] = self.filterData(testFeatureData[:,j], filterSize, 'valid')   
        return  filteredTrainPowerData, filteredTrainFeatureData, filteredTestPowerData, filteredTestFeatureData                             
                
    def calcDeviation(self,errorArray):
        '''Berechnung der positiven und negativen Abweichung zum Mittelwert'''
        result = np.zeros(2)
        mean = np.mean(errorArray)
        minimum = min(errorArray)
        maximum = max(errorArray)
        abweichungPlus = maximum-mean
        abweichungMinus = mean-minimum
        result[0] = abweichungMinus
        result[1] = abweichungPlus   
        return result      
                
    def compareAndShift(self, featureData, powerData):
        '''verschiebt PowerData, dass maximale Ähnlichkeit mit CPU Verlauf besteht'''
        cpu = featureData[:,0]
        shiftAmountTrain = np.argmax(np.array(np.correlate(cpu,powerData,"full")))-len(powerData)+1
        powerData = self.shiftArray(powerData,shiftAmountTrain)
        print "Data shiftAmount"
        print shiftAmountTrain
        return powerData
        
    def findHighestCorrelationAndShift(self, trainFeatureData, trainPowerData, testPowerData):
            maxCorrelationValue = np.zeros(len(trainFeatureData[0]))
            shiftAmount = np.zeros(len(trainFeatureData[0]))
            normedTrainFeatureData = self.normValues(trainFeatureData)
            normedTrainPowerData= self.normValues(trainPowerData)        
            
            for i in range(0,len(normedTrainFeatureData[0])):
                shiftAmount[i] = np.argmax(np.array(np.correlate(normedTrainFeatureData[:,i],normedTrainPowerData,"full")))-len(normedTrainPowerData)+1
                maxCorrelationValue[i] = max(np.array(np.correlate(normedTrainFeatureData[:,i],normedTrainPowerData,"full")))
            
            print ("Hoechste Korrelation mit Sensor %d")%(np.argmax(maxCorrelationValue)+1)
            trainPowerData = self.shiftArray(trainPowerData,shiftAmount[np.argmax(maxCorrelationValue)])
            testPowerData = self.shiftArray(testPowerData,shiftAmount[np.argmax(maxCorrelationValue)])
            print ("Data shiftAmount is %d")%(shiftAmount[np.argmax(maxCorrelationValue)])
            return trainPowerData, testPowerData     
            
    def normValues(self,data):
        '''Normiert die Werte mittels des Maximums auf den Wert 1 und verschiebt diese um den mean auf der y Achse'''        
        normedData= np.ndarray.copy(data)        
        #wenn data nur aus einer Zeile besteht. Elegegantere loesung finden        
        if(len(np.shape(data)) == 1):
            maximum = max(data)
            if(maximum != 0):
                normedData = data/max(data)-np.mean(data)/max(data)
            return normedData
        
        else:
            for i in range(0,len(data[0])):
                maximum = max(data[:,i])
                #print maximum
                if(maximum != 0):
                    for j in range(0,len(data)):
                        normedData[j,i] = (data[j,i]/maximum)-np.mean(data[:,i])/max(data[:,i])
            return normedData