import os
import sys
import fnmatch
import numpy as np
import random
import numpy
import itertools

#Fix the import path, so that we can import our parent folder with all required modules
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0,parentdir) 

print sys.path
import scipy
from sklearn.externals import joblib
from data_analysis.loadtrain import LoadData, Hdf5Loader
from data_analysis.regressor import Regressor
from data_analysis import plotData
from data_analysis.bestRegressor import BestRegressor
from sklearn.cluster import MeanShift, estimate_bandwidth, DBSCAN, KMeans
from sklearn.cross_validation import train_test_split
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier,RandomForestClassifier
from sklearn.cross_validation import cross_val_score

from sklearn.manifold import Isomap

from scipy.stats.stats import pearsonr
from sklearn.metrics import mean_squared_error
import pylab as pl

import pandas as pd
import extract
import wav_dataset
import glob
import os


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
loader=LoadData(groundtruth_elements=1, skipcols=0)


def extractFeatures(rawData):
    extractor = extract.FeatureExtractor(windowSize=rawData.shape[1], stepSize=rawData.shape[1]/2, threshold=0, mfcc_coeffs=13)
    
    return extractor.calculateMultiFeatures(rawData, [1, 4, 5 ])

def cluster_nonparametric(inputData):
    """
    Clusters the power signal using DBSCAN clustering. This method does not
    need the number of clusters or cluster centers
    
    @param powerData: The power data which should be clustered
    @returns: List of labels for each input sample
    """
    if len(inputData.shape) == 2:
        powerMatrix = inputData
    else:
        powerMatrix = np.zeros((len(inputData),1))
        powerMatrix[:,0]=inputData   
        
    #clusterer = DBSCAN(eps=0.3, min_samples=60)
    clusterer = KMeans(n_clusters=10)
    clusterer.fit(powerMatrix)
    
    labels = clusterer.labels_
    
    for  i in range(0, len(labels)):
        if labels[i] < 0:        
            labels[i] = 0
    return labels


def cluster_pca_and_plot(featureData,labels):
    X = featureData
    y = labels
    
    
    clf = RandomForestClassifier(n_estimators=25,random_state=0)
    scores = cross_val_score(clf, X, y)    

    print( scores.mean())
    return
    pca=PCA(n_components=4)
    X_new = pca.fit_transform(X)    
    
    #iso = Isomap(n_neighbors=30, n_components=2)
    #iso.fit(X)
    #X_new = iso.embedding_        
        
    
    clusterer = KMeans(n_clusters=len(set(y)))        
    #clusterer = MeanShift(bandwidth=bandwidth, bin_seeding=True)    
    
    #clusterer = DBSCAN(eps=3, min_samples=10)     
    clusterer.fit(X_new)
    print len(set(clusterer.labels_))
    
    colors_dict = {}
    colors = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
    
    for i in range(X_new.shape[0]):
        
        if not y[i] in colors_dict:
            curr_color = colors.next()
            colors_dict[y[i]] = curr_color
        else:
            curr_color = colors_dict[y[i]]
        
        t = pl.plot(X_new[i,0], X_new[i,1], 'x', color=curr_color)
    
    
    df = pd.DataFrame()    
    df["clustered_class"]= pd.Series(clusterer.labels_)
    df["true_class"]=pd.Series(y)  
    
    print df.groupby(["true_class", "clustered_class"]).count()
    

def run_wav_test():
    pl.cla()
    ds = wav_dataset.DataSet(extract.FeatureExtractor(windowSize = 2000, stepSize=2000, threshold=0, mfcc_coeffs=26))
    
    for class_, files in wav_dataset.getDataSamples("wav").items():
        for file_ in files:
            ds.addFile(class_, 1, file_)
        
    X, y = ds.featureVector, ds.classes
    
    cluster_pca_and_plot(X,y)

def plot_power_clustering(powerData, clusters):
    colors_dict = {}
    colors = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
    
    for i in range(len(powerData)):
        
        if not clusters[i] in colors_dict:
            curr_color = colors.next()
            colors_dict[clusters[i]] = curr_color
        else:
            curr_color = colors_dict[clusters[i]]
        
        t = pl.plot(i, powerData[i], 'x', color=curr_color)
    pl.show()
        
def majority_vote(arr, bins, window_size=40):
    arr = arr.astype(np.int32) 
    result = np.zeros(arr.shape)
    for i in range(0, arr.shape[0], window_size):

        start=i
        stop=min(start+window_size, arr.shape[0]-1)
        
        hist = np.bincount(arr[start:stop], minlength=bins)

        y = np.argmax(hist)
        
        for j in range(start, stop):
            result[j] = y
    
    return result
        

def calculate_cluster_features(trainPowerData, trainFeatureData, testPowerData, testFeatureData):
    power_labels = cluster_nonparametric(trainPowerData)
    
    train_power_states = len(set(power_labels)) - (1 if -1 in power_labels else 0)
    
    print("Found {0} power states".format(train_power_states))
    
    clf = ExtraTreesClassifier()
    clf.fit(trainFeatureData[0:len_,:], power_labels[0:len_])
    
    testFeatureData_clusters = majority_vote(clf.predict(testFeatureData),train_power_states)
    
    
    
    x = np.zeros((trainFeatureData.shape[0], 1))
    #x[:,0] = feature_clusterer.labels_
    x[:,0] = power_labels[0:len_]

    y = np.zeros((testFeatureData.shape[0], 1))
    #y[:,0] = cluster_feature
    y[:,0] = testFeatureData_clusters
    
    print x.shape
    print trainFeatureData.shape
    
    print y.shape
    print testFeatureData.shape
    
    X = numpy.concatenate((x, trainFeatureData), axis=1)
    Y = numpy.concatenate((y, testFeatureData), axis=1)
    
    return X, Y
    
    

def run_regression(trainPowerData, trainFeatureData, testPowerData, testFeatureData, shift=False):
    bestRegressor = BestRegressor()
    
    pl.cla()

    if(shift):
        """Trainingsdaten/Testpowerdata mithilfe der Kreuzkorrelation verschieben um zeitliche Verzoegerung des Plugwise zu kompensieren"""
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
    
    rfr = RandomForestClassifier()
    cv = cross_val_score(rfr, trainFeatureData, cluster_nonparametric(trainPowerData))
    print("Cross fold is : {0}".format( cv.mean()))    
    
    #rfr = RandomForestClassifier()
    #rfr.fit(trainFeatureData, cluster_nonparametric(trainPowerData))
    #plot_power_clustering(testPowerData, rfr.predict(testFeatureData))    
    
    #return    
    
    """Also add features gained from cluster centers"""
    trainFeatureData, testFeatureData = calculate_cluster_features(trainPowerData, trainFeatureData, testPowerData, testFeatureData)
    #testFeatureData= testFeatureData[:,0]
    #trainFeatureData= trainFeatureData[:,0] 
    
    """ERROR FUNC POSSIBILITIES:"""
    error_func = pearsonr
    #error_func = mean_squared_error
    #error_func = bestRegressor.meanTotalError
    #error_func = bestRegressor.meanAbsError
    
    
    #resultArray, resultTuple = bestRegressor.allSensorCombinations(trainFeatureData, trainPowerData,testFeatureData[0:50], testPowerData[0:50], error_func)
    resultTuple = bestRegressor.findGoodRegressor(trainFeatureData, trainPowerData,testFeatureData[0:500], testPowerData[0:500], error_func)
    
    #resultTuple = bestRegressor.allFeaturesResultTuple(trainFeatureData, 3)    # for coffee machine
    #resultTuple = (2, 16794128) # for fan
    #resultTuple = (2, 11282677760)  # for printer
    
    #print trainFeatureData
    
    #plot_power_clustering(testPowerData, cluster_nonparametric(testPowerData))
    
    predictedPower =  bestRegressor.predictResultArrayEntry(resultTuple, trainFeatureData,trainPowerData,testFeatureData)
    bestRegressor.printMeanMedianError(trainPowerData, testPowerData)
    
    
    print("=======================")
    print("Our regressor:")
    bestRegressor.printResultTuple(resultTuple, len(trainFeatureData[0,:]))
    print("=======================")
    bestRegressor.printError(predictedPower, testPowerData)
    
    bestRegressor.calculateMABSForChunks(predictedPower, testPowerData, chunk_len=600)
    #errors_ = bestRegressor.calculateErrorForChunks(predictedPower, testPowerData)
    
    #pl.plot(errors_[:,3])
    #pl.show()
    
    #"""PLOT"""
    plotData.printRealAndPredicted(predictedPower, testPowerData)
    #plotData.printAllRegressors(testPowerData,regressor_dictionary)
    #plotData.printDiffSensors(predictedPower,testPowerData,testFeatureData)
    #plotData.printDiffSensors(trainPowerData,trainPowerData,trainFeatureData)
    #plotData.printPearson(predictedPower,testPowerData)

def save_rawdata_as_wav(rawData):
    x = testRawData.shape
    audio_data = np.reshape(rawData, (x[0]*x[1], 1))

    audio_data= audio_data.astype(numpy.int16)
    scipy.io.wavfile.write("test.wav", 44100, audio_data)

"""Testdaten laden"""
#trainPowerData, trainFeatureData = loader.load_dir("train/")
#testPowerData, testFeatureData = loader.load_dir("test/")
 
ldr = Hdf5Loader()

print("Loading Dataset")
testPowerData, testRawData = ldr.getDatasets("test/coffee", ("power", "audio"))
trainPowerData, trainRawData = ldr.getDatasets("train/coffee", ("power", "audio"))

"""Esure equal length"""
len_ = min(testPowerData.shape[0], testRawData.shape[0])
testPowerData = testPowerData[0:len_,0]
testRawData = testRawData[0:len_, :]

len_ = min(trainPowerData.shape[0], trainRawData.shape[0])
trainPowerData = trainPowerData[0:len_,0]
trainRawData = trainRawData[0:len_, :]


#pl.plot(audio_data[:,0])
#pl.show()

print("Extracting Features")
testFeatureData = extractFeatures(testRawData)
trainFeatureData = extractFeatures(trainRawData)


print("Starting analysis")
#plot_power_clustering(testPowerData, cluster_nonparametric(testPowerData))
#cluster_pca_and_plot(testFeatureData, cluster_nonparametric(testPowerData))

#run_wav_test()
#run_clustering(testPowerData, testFeatureData)
run_regression(trainPowerData, trainFeatureData, testPowerData, testFeatureData)