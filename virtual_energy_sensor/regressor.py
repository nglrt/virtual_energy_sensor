from sklearn import tree
from sklearn import neighbors
from sklearn import linear_model
from sklearn import ensemble

from sklearn.externals import joblib
import numpy as np
import sklearn
from sklearn.gaussian_process import GaussianProcess


#import random


class Regressor():
    """
    This class trains different regressors und let them predict powervalues for test data
    """
    '''Test bezueglich Gaussian Process Regression'''
    def getGaussianProcess(self,f_train,p_train,f_test):
        GP = GaussianProcess()
        GP.fit(f_train,p_train)
        p_pred = GP.predict(f_test)
        print "GaussianProcess done"
        return p_pred
           
    #DTR Decision_Tree
    def getDTR(self,f_train,p_train,f_test):
        DTR=tree.DecisionTreeRegressor(random_state=1234)
        DTR.fit(f_train,p_train)
        p_pred=DTR.predict(f_test)
        print "DT done"
        return p_pred
        
    def saveDTR(self,f_train,p_train):
        DTR=tree.DecisionTreeRegressor(random_state=1234)
        DTR.fit(f_train,p_train)
        joblib.dump(DTR, 'regressor/DTR.pkl') 
        print "DTR Regressor saved"    
        sklearn.tree.export_graphviz(DTR, out_file='DTR.dot', feature_names=None, max_depth=None, close=True)
    
    #ETR Extra_Tree
    def getETR(self,f_train,p_train,f_test):
        ETR=tree.ExtraTreeRegressor(random_state=1234)
        ETR.fit(f_train,p_train)
        p_pred=ETR.predict(f_test)
        print "ET done"
        return p_pred
        
    def saveETR(self,f_train,p_train):
        ETR=tree.ExtraTreeRegressor(random_state=1234)
        ETR.fit(f_train,p_train)
        joblib.dump(ETR, 'regressor/ETR.pkl') 
        print "ETR Regressor saved"  
        sklearn.tree.export_graphviz(ETR, out_file='ETR.dot')
        
        
        
    #RFR Random_Forest
    def getRFR(self,f_train,p_train,f_test):
        RFR=ensemble.RandomForestRegressor(random_state=1234)
        RFR.fit(f_train,p_train)
        p_pred=RFR.predict(f_test)
        print "RF done"
        return p_pred
    
    def saveRFR(self,f_train,p_train):
        RFR=ensemble.RandomForestRegressor(random_state=1234)
        RFR.fit(f_train,p_train)
        joblib.dump(RFR, 'regressor/RFR.pkl') 
        print "RFR Regressor saved"  
        
        
    #ERFR Extra_Random_Forest
    def getERFR(self,f_train,p_train,f_test):
        ERFR=ensemble.ExtraTreesRegressor(random_state=1234)
        ERFR.fit(f_train,p_train)
        p_pred=ERFR.predict(f_test)
        print "ERF done"
        return p_pred
     
    def saveERFR(self,f_train,p_train):
        ERFR=ensemble.ExtraTreesRegressor(random_state=1234)
        ERFR.fit(f_train,p_train)
        joblib.dump(ERFR, 'regressor/ERFR.pkl') 
        print "ERFR Regressor saved"  
    
    #KNR K_Next_Neighbours
    def getKNR(self,f_train,p_train,f_test):
        KNR=neighbors.KNeighborsRegressor()
        KNR.fit(f_train,p_train)
        p_pred=KNR.predict(f_test)
        print "KNR done"
        return p_pred
        
    def saveKNR(self,f_train,p_train):
        KNR=neighbors.KNeighborsRegressor()
        KNR.fit(f_train,p_train)
        joblib.dump(KNR, 'regressor/KNR.pkl') 
        print "KNR Regressor saved"    
        
    
    #Lasso
    def getLassoR(self,f_train,p_train,f_test):
        LassoR=linear_model.Lasso()
        LassoR.fit(f_train,p_train)
        p_pred=LassoR.predict(f_test)
        print "LassoR done"
        return p_pred
        
    def saveLassoR(self,f_train,p_train):
        LassoR=linear_model.Lasso()
        LassoR.fit(f_train,p_train)
        joblib.dump(LassoR, 'regressor/LassoR.pkl') 
        print "LassoR Regressor saved"  
    
    #Lars
    def getLarsR(self,f_train,p_train,f_test):
        LarsR=linear_model.Lars()
        LarsR.fit(f_train,p_train)
        p_pred=LarsR.predict(f_test)
        print "Lars done"
        return p_pred
        
    def saveLarsR(self,f_train,p_train):
        LarsR=linear_model.Lars()
        LarsR.fit(f_train,p_train)
        joblib.dump(LarsR, 'regressor/LarsR.pkl') 
        print "LarsR Regressor saved"   

    #Linear
    def getLinearR(self,f_train,p_train,f_test):
        LinearR=linear_model.LinearRegression()
        LinearR.fit(f_train,p_train)
        p_pred=LinearR.predict(f_test)
        print "Linear done"
        return p_pred
        
    def saveLinearR(self,f_train,p_train):
        LinearR=linear_model.LinearRegression()
        LinearR.fit(f_train,p_train)
        joblib.dump(LinearR, 'regressor/LinearR.pkl') 
        print "LinearR Regressor saved"  
        print "Koeffizient :"
        print LinearR.coef_
        print "Intercept :"
        print LinearR.intercept_
        
        
    def printResult(self,resultTuple):
        regressorList = ("DTR","ETR","RFR","ERFR","KNR","LassoR","LarsR","LinearR")
        print "xxxxxxxxxxxxxxxxxxxx"
        print("Bester Regressor ist %s mit Sensorkombination: ")%(regressorList[resultTuple[0]])
        print bin(resultTuple[1])
        print "xxxxxxxxxxxxxxxxxxxx"   
        