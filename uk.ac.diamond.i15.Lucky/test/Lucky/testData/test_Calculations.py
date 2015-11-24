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
        data = np.loadtxt('./T_62_1.txt', unpack=True) ##Raw file
        calib = np.loadtxt('./Calib.txt', unpack=True) ##Calib file
        integConf = [315, 800, 200] #Values lifted out of PreLucky_Variant.py
        bulbTemp = 2436
        
        self.luckCalc = LuckyCalculations(data, calib, integConf, bulbTemp)
        
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
                i1=np.log(Int[i]/2/pi/h/c**2/f1**5)*Kb/h/c
                i2=np.log(Int[i+delta]/2/pi/h/c**2/f2**5)*Kb/h/c
                TTwo.append(abs((f2-f1)/(i2-i1)))
            for i in range (k,count):
                a = float('nan')
                TTwo.append(a)
            return TTwo
        #Defined linear fit for Wien function
        def FWien(x,e,T):
            a=1/T
            b=Kb/h/c*np.log(e)
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
        Norm=y/yC*P #Normalization file
        invX=1/x*10**9 #Inverse of wavelength for Wien function
        self.W=Wien(Norm,x)
        self.Two=TwoCol(Norm,x)
        Two2=np.array(self.Two,dtype='float')
        TwoInt=Two2[start:end]
        bins=range(1000,3000,1)
        hist=np.histogram(TwoInt,bins,density=False)
        self.freq=np.array(hist[0])
        control=len(hist[1])-1
        self.value=np.array(np.delete(hist[1],control,0))
        p0=[1,2000]
        #Fit Planck in the range [start:end]
        bestP,covarP = curve_fit(Planck, x[start:end], Norm[start:end], p0)
        TP=round(bestP[1],2)
        eP=bestP[0]#Save planck Emissivity
        xp=x[start:end]
        FP=Planck(xp,eP,TP)#Create the new Planck with the fit parameters
        PRes=abs(Norm[start:end]-FP)#Planck Residual
        
        #Wien fit 
        invX1=invX[start:end]
        W1=self.W[start:end]
        #Fit Wien and control that there are no inf or nan arguments in the fit
        bestW,covarW = curve_fit(FWien,invX1[(np.isfinite(W1))],W1[(np.isfinite(W1))],p0=[1,TP])
        Residual=W1-FWien(invX1[(np.isfinite(W1))],*bestW)
        #Save Wien temperature
        TW=round(bestW[1])
        
        #Gaussian fit to the histogram two-colours
        popt,pcov = curve_fit(gaus,self.value,self.freq,p0=[1000,TP,100])
        Thist=round(popt[1],2)#Save Histogram temperature
        errTot=round(popt[2])

class DataUpdateTest(CalculationsTest):
    def runTest(self):
        assert_array_equal(self.P, self.luckCalc.planckIdeal, "Planck ideals differ")
        
        
        assert_array_equal(self.W, self.luckCalc.wienData, "Wien datasets differ")
        assert_array_equal(self.Two, self.luckCalc.twoColData, "Two-colour datasets differ")
        assert_array_equal(self.freq, self.luckCalc.twoColHistFreq, "Two-colour histogram (freq.) datasets differ")
        assert_array_equal(self.value, self.luckCalc.twoColHistValues, "Two-colour histogram (value) datasets differ")

# class PlanckCalcsTest(CalculationsTest):
#     def runTest(self):
#         self.assertEqual(self.P, self.luckCalc, msg)
