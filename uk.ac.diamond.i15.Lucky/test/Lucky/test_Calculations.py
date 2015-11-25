'''
Created on 24 Nov 2015

@author: wnm24546
'''
import unittest
import numpy as np
from numpy.testing import assert_array_equal
from scipy.optimize import curve_fit

from Lucky.Calculations import LuckyCalculations


class CalculationsTest(unittest.TestCase):
    
    def setUp(self):
        data = np.loadtxt('./testData/T_62_1.txt', unpack=True) ##Raw file
        calib = np.loadtxt('./testData/Calib.txt', unpack=True) ##Calib file
        integConf = [315, 800, 200] #Values lifted out of PreLucky_Variant.py
        bulbTemp = 2436
        
        self.luckCalc = LuckyCalculations(data, calib, integConf, bulbTemp, debug=True)
        
        self.workingCalcs(data, calib, integConf)
    
    def workingCalcs(self, data, calib, integConf):
        from scipy.constants import h, c, k, pi
        ##Constants:
        Kb = k
        
        ##Session where I define all the function needed
        def Planck(x,e,T):
            x = x*10**(-9)
            a=np.expm1((h*c)/(k*x*T))#Order changed!! (h*c/k)/(x)/T
            P=e/(x)**5*(2*pi*h*c**2)*1/(a) ####NB Removed 
            return P
        #Defined Wien function
        def Wien(Int,x):
            #Order changed!!
            #W=Kb/h/c*np.log((x*10**(-9))**5*Int/2/pi/h/c**2)
            W=Kb/(h*c)*np.log((x*10**(-9))**5*Int/(2*pi*h*c**2))
            return W
        #Defined two-colour function
        def TwoCol(Int,x):
            count=len(x)
            delta=200
            k=count-delta
            TTwo=[]*count
            
            for i in range (0,k):#(0,count-1):
                f1=1/(x[i]*10**(-9))
                f2=1/(x[i+delta]*10**(-9))
                i1=np.log(Int[i]/(2*pi*h*c**2*f1**5))*(Kb/(h*c))#Order changed!!
                i2=np.log(Int[i+delta]/(2*pi*h*c**2*f2**5))*(Kb/(h*c))#i2=np.log(Int[i]/2/pi/h/c**2/f1**5)*Kb/h/c
                TTwo.append(abs((f2-f1)/(i2-i1)))
            for i in range (k,count):
                a = float('nan')
                TTwo.append(a)
            return TTwo
        #Defined linear fit for Wien function
        def FWien(x,e,T):
            a=1/T
            b=Kb/(h*c)*np.log(e)
            W=b-a*x
            return W
        #Defined Gauss fit
        def gaus(x, a, x0, sigma):
            return np.real(a*np.exp(-(x-x0)**2/(2*sigma**2)))
        
        x = data[0]
        y = data[1]
        xC = calib[0]
        yC = calib[1]
        start = integConf[0]
        end = integConf[1]
        delta = integConf[2]
        
        P=Planck(x,1,2436)##Ideal Planck
        self.P = np.reshape(P, (1, len(P)))
        self.Norm=y/yC*P #Normalization file
        self.invX=1e9/x #Inverse of wavelength for Wien function (CHANGED 1/x*10**9)
        self.W=Wien(self.Norm,x)
        self.Two=TwoCol(self.Norm,x)
        Two2=np.array(self.Two,dtype='float')
        self.TwoInt=Two2[start:end]
        bins=range(1000,3000,1)
        hist=np.histogram(self.TwoInt,bins,density=False)
        self.freq=np.array(hist[0])
        control=len(hist[1])-1
        self.value=np.array(np.delete(hist[1],control,0))
        p0=[1,2000]
        #Fit Planck in the range [start:end]
        self.xp=x[start:end]
        self.Normp=self.Norm[start:end]
        bestP,covarP = curve_fit(Planck, self.xp, self.Normp, p0)
        TP=round(bestP[1],2)
        self.TPNR = bestP[1]
        self.eP=bestP[0]#Save planck Emissivity
        FP=Planck(self.xp,self.eP,TP)#Create the new Planck with the fit parameters
        self.FPNR = Planck(self.xp,self.eP,self.TPNR)
        PRes=abs(self.Normp-FP)#Planck Residual
        
        #Wien fit 
        self.invX1=self.invX[start:end]
        self.W1=self.W[start:end]
        #Fit Wien and control that there are no inf or nan arguments in the fit
        self.bestW,covarW = curve_fit(FWien,self.invX1[(np.isfinite(self.W1))],self.W1[(np.isfinite(self.W1))],p0=[1,self.TPNR]) #Changed - was TP
        self.Residual=self.W1-FWien(self.invX1[(np.isfinite(self.W1))],*self.bestW)
        #Save Wien temperature
        TW=round(self.bestW[1])
        
        #Gaussian fit to the histogram two-colours
        popt,pcov = curve_fit(gaus,self.value,self.freq,p0=[1000,self.TPNR,100])#Changed - was TP
        Thist=round(popt[1],2)#Save Histogram temperature
        errTot=round(popt[2])
        self.Thist = popt[1]
        self.errTot = popt[2]

class DataUpdateTest(CalculationsTest):
    def runTest(self):
        #Normalised data
        assert_array_equal(self.P, self.luckCalc.planckIdeal, "Planck ideal datasets differ")
        assert_array_equal(self.Norm, self.luckCalc.dataSet[2], "Normalised y datasets differ")
        
        #Sliced datasets
        assert_array_equal(self.invX, self.luckCalc.invWL, "Inverse wavelength datasets differ")
        assert_array_equal(self.invX1, self.luckCalc.invWLIntegLim, "Integration limited inverse wavelength datasets differ")
        assert_array_equal(self.xp, self.luckCalc.wlIntegLim, "Integration limited wavelength datasets differ")
        assert_array_equal(self.Normp, self.luckCalc.normIntegLim, "Integration limited normalised y datasets differ")
        
        #Functions calculated by defauls
        assert_array_equal(self.W, self.luckCalc.wienData, "Wien datasets differ")
        assert_array_equal(self.W1, self.luckCalc.wienDataIntegLim, "Integration limited Wien datasets differ")
        assert_array_equal(self.Two, self.luckCalc.twoColData, "Two-colour datasets differ")
        assert_array_equal(self.TwoInt, self.luckCalc.twoColDataLim, "Integration limited two-colour datasets differ")
        assert_array_equal(self.freq, self.luckCalc.twoColHistFreq, "Two-colour histogram (freq.) datasets differ")
        assert_array_equal(self.value, self.luckCalc.twoColHistValues, "Two-colour histogram (value) datasets differ")
        assert_array_equal(self.value, self.luckCalc.twoColHistValues, "Two-colour histogram (value) datasets differ")

class PlanckCalcsTest(CalculationsTest):
    def runTest(self):
        self.assertEqual(self.TPNR, self.luckCalc.planckTemp, "Wrong Planck temperature calculated")
        self.assertEqual(self.eP, self.luckCalc.planckEmiss, "Wrong Planck emissivity calculated")
        assert_array_equal(self.FPNR, self.luckCalc.planckFitData, "Planck datasets from fitted values differ")

class WienCalcsTest(CalculationsTest):
    def runTest(self):
        assert_array_equal(self.bestW, self.luckCalc.wienFit, "Wien fits differ")
        assert_array_equal(self.Residual, self.luckCalc.wienResidual, "Wien residual datasets differ")
        
class HistogramCalcsTest(CalculationsTest):
    def runTest(self):
        self.assertEqual(self.Thist, self.luckCalc.histTemp, "Wrong temperature calculated from histogram fit")
        self.assertEqual(self.errTot, self.luckCalc.histErr, "Wrong histogram fit error calculated")
        
