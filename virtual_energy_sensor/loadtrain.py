import numpy as np
import fnmatch, os
import h5py

class Hdf5Loader():
    def loadDirectory(self, dirname):
        """
        Loads all hdf5 files in the directory dirname
        
        @param dirname: The directory which contains the files to load
        @returns: list of h5py File objects
        """
        cachelist=os.listdir(dirname)
        testlist=fnmatch.filter(cachelist,'*.hdf5')
        
        for file_ in testlist:
            print("Using {0}".format(file_))
        
        files = [h5py.File(os.path.join(dirname, fn),'r') for fn in testlist]
        return files
    
    def getDatasets(self, dirname, dataset_list):
        """
        Loads all hdf5 files in a given directory. It extracts all datasets
        which are specified in :dataset_list and merges the datasets from 
        all files. 
        
        Finally it returns a numpy array for each dataset in the :dataset_list
        
        
        @param dirname: The directory containing the hdf5 files
        @param dataset_list: List of datasets to load
        
        @returns: A list of numpy arrays loaded from the dataset files
        """
        
        files = self.loadDirectory(dirname)
        
        result = []
        for dataset_name in dataset_list:
            arr = np.concatenate([f[dataset_name] for f in files])
            result.append(arr)
        
        return result
        

class LoadData():
    """
    This class extracts data from features and corresponding powervalues and returns them as array
    """
    
    def __init__(self, sep=";", groundtruth_elements=2, skiprows=1, skipcols=1):
        self.sep = sep
        self.num_groundtruth_elements = groundtruth_elements
        self.skiprows=1
        self.skipcols = skipcols
    
    def getFeatureCount(self, file_):
        fd = open(file_, 'r')
        fd.readline()
        count = len(fd.readline().split(self.sep))
        
        return count - self.num_groundtruth_elements
        
    
    def getFeaturesData(self,csvname):
        cols = range(self.skipcols, self.getFeatureCount(csvname))        
        print cols
        log = np.loadtxt(csvname,delimiter=self.sep,skiprows=self.skiprows,usecols=cols)
        return log
        
    def getPowerData(self,csvname):
        cols = [self.getFeatureCount(csvname)]
        power = np.loadtxt(csvname,delimiter=self.sep,skiprows=self.skiprows,usecols=cols)
        
        return power

    def load_dir(self, dirname):
        """
        Loads all files of a directory to a single feature and power data set
        """
        cachelist=os.listdir(dirname)
        testlist=fnmatch.filter(cachelist,'*.csv')        
        
        testFeatureDataLst = []
        testPowerDataLst = []
        """Testdaten laden"""
        for file_ in testlist:
            testFeatureDataLst.append(self.getFeaturesData(os.path.join(dirname,file_)))
            testPowerDataLst.append(self.getPowerData(os.path.join(dirname,file_)))
            
        testFeatureData = np.concatenate(testFeatureDataLst)
        testPowerData = np.concatenate(testPowerDataLst)
        
        return testPowerData, testFeatureData