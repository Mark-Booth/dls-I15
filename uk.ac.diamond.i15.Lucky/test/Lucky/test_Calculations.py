'''
Created on 24 Nov 2015

@author: wnm24546
'''
import unittest
import numpy as np
import os, time
from numpy.testing import assert_array_equal
from scipy.optimize import curve_fit

from Lucky.Calculations import LuckyCalculations, CalculationService, LuckyPlots
from Lucky.DataModel import MainData, CalibrationConfigData
from Lucky.test.mock_Calculations import mock_Calculations

class LuckyCalculationsTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.wdir = os.path.join('.','testData')
        self.dsDataFile = os.path.join(self.wdir, 'T_635.txt')
        self.usDataFile = os.path.join(self.wdir, 'T_636.txt')
        self.dsCalibFile = os.path.join(self.wdir, 'Calib.txt')
        self.usCalibFile = os.path.join(self.wdir, 'CalibF2MTW.txt')
        
        
        self.dsData = np.loadtxt(self.dsDataFile, unpack=True) ##Raw file
        self.usData = np.loadtxt(self.usDataFile, unpack=True)
        self.calib = np.loadtxt('./testData/Calib.txt', unpack=True) ##Calib file
        self.integConf = [315, 800, 200] #Values lifted out of PreLucky_Variant.py
        self.bulbTemp = 2436


class PlottingTest(LuckyCalculationsTest):
    def setUp(self):
        LuckyCalculationsTest.setUp(self)
       
    def runTest(self):
        luckCalcPlot = LuckyCalculations(self.dsData, self.calib, self.integConf, self.bulbTemp, "TestData", debug=False)
        luckCalcPlot.runCalculations()
        LuckyPlots(luckCalcPlot)
        print "Test sleeping for 20s"
        time.sleep(20)
 
###
       
class ServiceTest(LuckyCalculationsTest):
    def setUp(self):
        LuckyCalculationsTest.setUp(self)
        
        cc = CalibrationConfigData(calibDir=self.wdir, calibDS=self.dsCalibFile, calibUS=self.usCalibFile)
        dm = MainData(dataDir=self.wdir, usdsPair=[self.dsDataFile, self.usDataFile])
        dm.calibConfigData = cc
        
        self.calcServ = CalculationService(None)
        self.calcServ.updateModel(dm)
        
    def runTest(self):
        assert_array_equal(self.calcServ.dsData, np.loadtxt(self.dsDataFile, unpack=True), 'dsData ndarrays differ')
        assert_array_equal(self.calcServ.usData, np.loadtxt(self.usDataFile, unpack=True), 'usData ndarrays differ')
        
        assert_array_equal(self.calcServ.dsCalib, np.loadtxt(self.dsCalibFile, unpack=True), 'dsCalibFile ndarrays differ')
        assert_array_equal(self.calcServ.usCalib, np.loadtxt(self.usCalibFile, unpack=True), 'usCalibFile ndarrays differ')
        try:
            assert_array_equal(self.calcServ.dsCalibFile, self.calcServ.usCalibFile)
            self.fail('DS & US calibration ndarrays should differ')
        except:
            pass
        
        self.usCalibFile = os.path.join(self.wdir, 'Calib.txt')
        cc = CalibrationConfigData(calibDir=self.wdir, calibDS=self.dsCalibFile, calibUS=self.usCalibFile)
        dm = MainData(dataDir=self.wdir, usdsPair=[self.dsDataFile, self.usDataFile])
        dm.calibConfigData = cc
        
        self.calcServ.updateModel(dm)
        assert_array_equal(self.calcServ.dsCalib, self.calcServ.usCalib)
        
        #Test the updateResults method
        self.calcServ.dsCalcs = mock_Calculations(2011.64, 2013.53)
        self.calcServ.usCalcs = mock_Calculations(2014.76, 2015.99)
        self.calcServ.updateResults()
        
        self.assertEquals(self.calcServ.planckResults, [2011.64, 2014.76, (2011.64+2014.76)/2, 2011.64-2014.76], "planckResults not consistent with input mock data")
        self.assertEquals(self.calcServ.wienResults, [2013.53, 2015.99, (2013.53+2015.99)/2, 2013.53-2015.99], "wienResults not consistent with input mock data")

###

class CalculationsTest(LuckyCalculationsTest):
    def setUp(self):
        LuckyCalculationsTest.setUp(self)
        
        self.luckCalc = LuckyCalculations(self.dsData, self.calib, self.integConf, self.bulbTemp, "TestData", debug=True)
        self.luckCalc.runCalculations()
        
        self.workingCalcs(self.dsData, self.calib, self.integConf)
    
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
                f1=(h*c)/(x[i]*10**(-9)*Kb)
                f2=(h*c)/(x[i+delta]*10**(-9)*Kb)
                i1=np.log(Int[i]*(x[i]*10**(-9))**5/(2*pi*h*c**2))*(Kb/(h*c))#Order changed!!
                i2=np.log(Int[i+delta]*(x[i+delta]*10**(-9))**5/(2*pi*h*c**2))*(Kb/(h*c))#i2=np.log(Int[i]/2/pi/h/c**2/f1**5)*Kb/h/c
                TTwo.append((f1-f2)/(i2-i1))
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
        
        self.x = data[0]
        y = data[1]
        xC = calib[0]
        yC = calib[1]
        start = integConf[0]
        end = integConf[1]
        delta = integConf[2]
        
        P=Planck(self.x,1,2436)##Ideal Planck
        self.P = np.reshape(P, (1, len(P)))
        self.Norm=y/yC*P #Normalization file
        self.invX=1e9/self.x #Inverse of wavelength for Wien function (CHANGED 1/x*10**9)
        self.W=Wien(self.Norm,self.x)
        self.Two=TwoCol(self.Norm,self.x)
        Two2=np.array(self.Two,dtype='float')
        self.TwoInt=Two2[start:end]
        bins=range(1000,3000,1)
        hist=np.histogram(self.TwoInt,bins,density=False)
        self.freq=np.array(hist[0])
        control=len(hist[1])-1
        self.value=np.array(np.delete(hist[1],control,0))
        p0=[1,2000]
        #Fit Planck in the range [start:end]
        self.xp=self.x[start:end]
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
        
class CalculationStateTest(CalculationsTest):
    def runTest(self):
        #Normalised dsData
        assert_array_equal(self.P, self.luckCalc.planckIdeal, "Planck ideal datasets differ")
        assert_array_equal(self.Norm, self.luckCalc.dataSet[2], "Normalised y datasets differ")
        
        #Sliced datasets
        assert_array_equal(self.invX, self.luckCalc.invWL, "Inverse wavelength datasets differ")
        assert_array_equal(self.invX1, self.luckCalc.invWLIntegLim, "Integration limited inverse wavelength datasets differ")
        assert_array_equal(self.xp, self.luckCalc.wlIntegLim, "Integration limited wavelength datasets differ")
        assert_array_equal(self.Normp, self.luckCalc.normIntegLim, "Integration limited normalised y datasets differ")
        
        #Functions calculated by defaults
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
        self.assertEqual(self.Thist, self.luckCalc.twoColTemp, "Wrong temperature calculated from two-colour fit")
        self.assertEqual(self.errTot, self.luckCalc.twoColErr, "Wrong two-colour fit error calculated")
        
class UpdateTest(CalculationsTest):
    def runTest(self):
        #Initial state
        data = self.luckCalc.dataSet
        integConf = self.luckCalc.intConf
        calibSet = self.luckCalc.calibSet
        bulbTemp = self.luckCalc.bulbTemp
        
        newIntConf = [300,700,100]
        
        def updateInteg(newIntConf):
            self.luckCalc.update(integConf=newIntConf)
            invWlIntLim = self.invX[newIntConf[0]:newIntConf[1]]
            wlIntLim = self.x[newIntConf[0]:newIntConf[1]]
            normIntLim = self.Norm[newIntConf[0]:newIntConf[1]]
        
            self.assertNotEqual(integConf, self.luckCalc.intConf, "Old integconf & curren have the same value")
            self.assertEqual(newIntConf, self.luckCalc.intConf, "New integconf & current have different values")
            assert_array_equal(invWlIntLim, self.luckCalc.invWLIntegLim, "Integration limited inverse wavelength datasets differ")
            assert_array_equal(wlIntLim, self.luckCalc.wlIntegLim, "Integration limited wavelength datasets differ")
            assert_array_equal(normIntLim, self.luckCalc.normIntegLim, "Integration limited normalised y datasets differ")
        
        ##TODO Add tests for updating the data & the calibration
        