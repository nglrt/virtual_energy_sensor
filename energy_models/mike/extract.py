import numpy as np
import math
from scipy.fftpack import dct
from filter import ThresholdFilter
from window import Windowing

class FeatureExtractor:
    """
    This class transforms sound files to feature vectors
    Those feature vectors could either be one dimensional or 
    multi dimensional.
    """
    
    
    def __init__(self, windowSize=4096, stepSize=2048, threshold=100, mfcc_coeffs=13):
        self.mfcc_coeffs = mfcc_coeffs        
        self.windowSize = windowSize
        self.stepSize = stepSize
        self.windowFunc =  np.hamming(self.windowSize)
        self.threshold = ThresholdFilter(threshold = threshold)
        self.windowing = Windowing(self.windowSize,self.stepSize)
        self.melfilterbank = melFilter(self.windowSize, numcoeff=mfcc_coeffs)
        
    def calculateMultiFeatures(self, windowedData, featureTuple):
        """
        This function takes the windowed data and extracts the features
        specified in :featureTuple from the windowed data. 
        
        It returns a the concatenated matrix of all extracted features
        The concatenation happens along axis 1
        """
        return np.concatenate([self.calculateFeatures(windowedData, f) for f in featureTuple], axis=1)
    
    def calculateFeatures(self, windowedData, feature_type):
        """
        This function takes the windowedData and extracts 
        the features from the windowedData. The input array
        should have the following format:
            - The samples of a window in x direction
            - The windows of the sound file in y direction
        
        @param windowedData: The windowed input data in the form (x,y)
        @returns: A two dimensional array (x,y)
            - The x direction contains the windows
            - The y direction contains raw samples of one window     
        """
        x_len,y_len = windowedData.shape
        
        # MFCCs
        num_coefficients = self.mfcc_coeffs
        if feature_type == 1 :
            return self.calcMFCCs(windowedData,num_coefficients)
        
        # Delta MFCCs
        if feature_type == 2 :
            mfcc = self.calcMFCCs(windowedData,num_coefficients)
            dmfcc = np.resize(mfcc, (x_len, num_coefficients*2))
            
            n = 2
            denom = 2*sum(i**2 for i in xrange(n+1))

            for x in xrange(n,x_len-n):
                for y in xrange(n):
                    dmfcc[x, num_coefficients:] += n*(mfcc[x+n] - mfcc[x-n])
                dmfcc[x, num_coefficients:] /= denom

            return dmfcc

        # Powerspectrum             
        elif feature_type == 3 :
            R = 100
            out = np.ndarray((x_len, int(y_len/R)))
            for x in xrange(x_len):
                X = abs(np.fft.fft(windowedData[x])) ** 2
                out[x] = X.reshape(-1, R).mean(axis=1)
            return out

        # Zero-crossing-rate 
        elif feature_type == 4 :
            out = np.zeros((x_len,2))
            for x in xrange(x_len):
                out[x]=np.argmax(np.fft.fft(windowedData[x]))
            return out

        # Band-energy 
        elif feature_type == 5 :
            # number of bands the powerspectrum is divided in
            num_bands = 10 

            pspec = np.ndarray((x_len, y_len))
            out = np.ndarray((x_len,num_bands-1))

            # determine logarithmic spaced boundarys
            bounds = calcBounds(num_bands, y_len)

            # calc pspec and sum up energy in bands
            for x in xrange(x_len):
                pspec[x] = abs(np.fft.fft(windowedData[x])) ** 2
                abs_power = np.sum(pspec[x])

                for y in xrange(num_bands-1):
                   out[x, y] = np.sum(np.abs(pspec[x, int(bounds[y]) : int(bounds[y+1])])) #/ abs_power
                
            return out
                
        # Return none, if no feature was selected
        return None
            
    
    def __call__(self, rawAudioData, feature_type):
        """
        Extracts features from a sound files raw audio data. This
        raw audio data is a 1d array with the raw audio samples.
        
        There is a windowing function applied to the raw audio data, 
        silence windows are filtered out and then features are extracted.
        
        The result is a 2d array: The x dimension contains the extracted 
        features for each window and the y dimension contains the windows.
        
        @param rawAudioData: The raw samples from the sound file
        @returns the extracted features from the sound file
        """
        self.rawAudioData = rawAudioData
        windowedData = self.windowing.apply(self.rawAudioData)
        filteredData = self.threshold.apply(windowedData)
        return self.calculateFeatures(filteredData, feature_type)

    def calcMFCCs(self, windowedData, num_coefficients):

        x_len,y_len = windowedData.shape

        pspec = np.ndarray((x_len, y_len))
        out = np.ndarray((x_len,num_coefficients))
        logSpectrum = np.zeros(num_coefficients)

        for x in xrange(x_len):
            pspec[x] = abs(np.fft.fft(windowedData[x])) ** 2
            melSpectrum = np.dot(pspec[x], self.melfilterbank)
                
            for z in xrange(num_coefficients):
                if (melSpectrum[z] != 0):
                    logSpectrum[z] = np.log(melSpectrum[z])
            out[x] = dct(logSpectrum, type=2)
        
        return out

def melFilter(blockSize, numcoeff=13, minHz = 0, maxHz = 22050):
    
    numBands = int(numcoeff)
    
    maxMel = int(freqToMel(maxHz))
    minMel = int(freqToMel(minHz))

    # Create a matrix for triangular filters, one row per filter
    filterMatrix = np.zeros((numBands, blockSize))

    melRange = np.array(xrange(numBands + 2))

    melCenterFilters = melRange * (maxMel - minMel) / (numBands + 1) + minMel
    
    aux = np.log(1 + 1000.0 / 700.0) / 1000.0
    aux = (np.exp(melCenterFilters * aux) - 1) / 22050
    aux = 0.5 + 700 * blockSize * aux
    aux = np.floor(aux)

    # each array index represent the center of each triangular filter
    centerIndex = np.array(aux, int)
    

    for i in xrange(numBands):
        start, centre, end = centerIndex[i:i + 3]
        k1 = np.float32(centre - start)
        k2 = np.float32(end - centre)
        up = (np.array(xrange(start, centre)) - start) / k1
        down = (end - np.array(xrange(centre, end))) / k2

        filterMatrix[i][start:centre] = up
        filterMatrix[i][centre:end] = down

    return filterMatrix.transpose()


def calcBounds(num_bands, windowSize):
    """
    Calculates logarithmic distributed boundarys for the Bandenergy feature
    """
    # linear band steps
    linear_factor = 10 / num_bands
    
    bounds = np.zeros(num_bands)
    
    for x in xrange(1, num_bands ):
        bounds[x-1] = math.floor(np.log10(x*linear_factor) * windowSize)
    
    # revert    
    bounds = bounds[::-1]
    bounds[1:num_bands] = windowSize - bounds[1:num_bands]

    return bounds

def freqToMel(freq):
    """
    Converts a specified frequency into Mel.
    """
    return 1127.01048 * math.log(1+freq/700.0)

def freqToBark(freq):
    """
    Converts from frequency into Bark scale.
    """
    return 13 * math.atan(0.00076 * freq) + 3.5 * math.atan( (freq/7500) ** 2)
        
def melToFreq(mel):
    """
    Converts from Mel to Hertz
    """
    return 700 * (math.exp(freq / 1127.01048-1))
