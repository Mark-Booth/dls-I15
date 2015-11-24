'''
Created on 24 Nov 2015

@author: wnm24546
'''

from scipy.constants import c, h, k, pi
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
#import sys

#k is kb

class LuckyCalculations(object):
    
    def __init__(self, integConf, data, calib):
        self.intConf = integConf
        self.dataSet = data
        self.calibSet = calib
        
        self.planckPlotRange = [500, 1000]
        self.wienPlotRange = [1e9 / self.planckPlotRange[1], 1e9/self.planckPlotRange[0]]
        
        #Calculated values
#         self.wienData = None
#         self.twoColourData = None
#         self.planckTemp = None
#         self.planckEmmis = None
#         
        self.updateData()
        self.doFits()
    
    
    def updateData(self):
        #Normalises collected data
        planckIdeal = self.planck(self.dataSet[0], 1, self.bulbTemp)
        self.dataSet = np.c_[self.dataSet, self.dataSet[1] / self.calibSet[1] * planckIdeal]
        self.invWL = 1e9 / self.dataSet[0]# For Wien function
        
        #Data sets for fitting, limited by integration range
        self.wlIntegLim = self.dataSet[0][self.intConf[0]:self.intConf[1]]
        self.invWLIntegLim = self.invWL[self.intConf[0]:self.intConf[1]]
        self.normIntegLim = self.dataSet[2][self.intConf[0]:self.intConf[1]]
        
        #Calculate functions over the range of data
        self.wienData = self.wien(self.dataSet[0], self.dataSet[2])
        self.twoColData = self.twoColour(self.dataSet[0], self.dataSet[2], self.intConf[2])
        self.twoColHistFreq, self.twoColHistValues = np.histogram(self.twoColData[self.intConf[0]:self.intConf[1]], bins=range(1000,3000), density=False)
        self.twoColHistValues = np.delete(self.twoColHistValues, len(self.twoColHistFreq), 0)
        self.twoColDataLim = self.twoColDataLim[self.intConf[0]:self.intConf[1]]
        
    def doFits(self):
        #Do some fitting for Planck...
        ###
        planckFit, planckCov = curve_fit(self.planck, self.wlIntegLim, self.normIntegLim, [1,2000])
        self.planckTemp = planckFit[1]
        self.planckEmmiss = planckFit[0]
        
        #Planck with fit params(??)
        self.planckFitData = self.planck(self.wlIntegLim, self.planckEmmiss, self.planckTemp)
        
        #Do some fitting for Wien...
        ###
        wienIntegLim = self.wienData[self.intConf[0]:self.intConf[1]]
        self.wienFit, wienCov = curve_fit(self.fWien, self.invWLIntegLim[(np.isfinite(wienIntegLim))], wienIntegLim[(np.isfinite(wienIntegLim))], p0 = [1, self.planckTemp])
        self.wienResidual = wienIntegLim - self.fWien(self.invWLIntegLim[(np.isfinite(wienIntegLim))], *self.wienFit)
        self.wienTemp = self.wienFit[1]
        
        #Gaussian fit of two colour histogram
        ###
        self.histFit, histCov = curve_fit(self.gaus, self.twoColHistFreq, p0=[1000,self.planckTemp,100])
        self.histTemp = self.histFit[1]
        self.histErr = self.histFit[2]
    
    
    #Planck function
    def planck(self, wavelength, emiss, temp):
        wavelength = wavelength * 1e-9
        return (emiss / np.power(wavelength, 5)) * (2 * pi * h * np.power(c, 2)) / np.expm1((h * c)/(k * wavelength * temp))
    
    #Wien function
    def wien(self, wavelength, intens):
        wavelength = wavelength * 1e-9
        return self.wienBase(np.power(wavelength, 5) * intens * 2 / (pi * h * np.power(c, 2)))
        
    #Linear Wien function
    def fWien(self, wavelength, emiss, temp):
        wavelength = wavelength * 1e-9
        wienVal = self.wienBase(emiss)
        return wienVal - (1/temp) * wavelength
    
    #Wien support function (this is just recycling code)
    def wienBase(self, exponent):
        return k / (h * c) * np.log(exponent)
    
    #Two colour function
    def twoColour(self, wavelength, intens, delta):
        twoCol = []
        wavelength = wavelength * 1e-9
        nPoints = len(wavelength)
        nWindows = nPoints - delta
        
        def twoColCalc(wavelength, intens):
            return np.log(intens / (2 * pi * h * np.power(c, 2) * np.power(wavelength, 5))) * k * h *c
        
        for i in range(nWindows):
            f1 = 1 / wavelength[i]
            f2 = 1 / wavelength[i + delta]
            i1 = twoColCalc(f1, intens[i])
            i2 = twoColCalc(f2, intens[i+delta])
            twoCol.append((f2 - f1) / (i2 - i1))
        
        for i in range(nWindows, nPoints):
            twoCol.append(float('nan'))
        
        return twoCol
    
    #Gaussian for fit
    def gaus(self, x, a, x0, sigma):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))
    
    def drawPlots(self):
        fig = plt.figure(figsize=(8,11))#Defines dimension of the figure 

        #Create set of subplots
        ax1 = fig.add_subplot(3, 2, 1)#Data & Calib datasets
        ax2 = fig.add_subplot(3, 2, 2)#Planck data
        ax3 = fig.add_subplot(3, 2, 3)#Wien data
        ax4 = fig.add_subplot(3, 2, 4)
        ax5 = fig.add_subplot(3, 2, 5)
        plt.subplots_adjust(wspace=0.3,hspace=0.3)
 
        #Raw and calibration data subgraph 
        ax1.plot(self.dataSet[0], self.dataSet[1], self.dataSet[0], self.calibSet[1],'red')
        ax1.set_title('Raw & Calibration Data')
        ax1.set_xlabel('Wavelength / nm')
        ax1.set_ylim(0,50000) #TODO Get max fn.
        ax1.grid(True, linestyle='-')

#Draws text label on plot
#         txt=plt.text(4500,33,TP)
#         txt1=plt.text(4200,33,'T=')
#         txt2=plt.text(2000,17,TW)
#         txt3=plt.text(1800,17,'T=')
#         txt.set_size(15)
#         txt1.set_size(15)
#         txt2.set_size(15)
#         txt3.set_size(15)
#         fig.canvas.draw()
   

        #Planck data subgraph
        ax2.plot(self.dataSet[0], self.dataSet[2], self.wlIntegLim, self.planckFitData,'red')
        ax2.set_title('Planck Function Data')
        ax2.set_xlabel('Wavelength / nm')
        ax2.set_xlim(*self.planckPlotRange)
        ax2.set_yticks([])
  
        #Wien data subgraph
        ax3.plot(self.invWL, self.wienData, self.invWLIntegLim, self.FWien(self.invWLIntegLim,*self.wienFit), 'red', self.invWLIntegLim, self.wienResidual)
        ax3.set_title('Wien Function Data')
        ax3.set_xlabel('1/Wavelength / 1/m)')
        ax3.set_ylabel("Wien Function")
        ax3.set_xlim(*self.wienPlotRange)
        ax3.set_yticks([])
        
        #Two Colour data subgraph
        ax4.plot(self.dataSet[0], self.twoColData, self.wlIntegLim, self.twoColDataLim, 'red')
        ax4.set_title('Sliding Two Colours')
        ax4.set_xlabel('Wavelength  / nm')
        ax4.set_ylabel('Temperature / K')
        ax4.set_xlim(*self.planckPlotRange)
        ax4.grid(True, linestyle='-')

        #Histogram subgraph
        ax5.plot(self.twoColHistValues, self.twoColHistFreq, self.twoColHistValues, self.gaus(self.twoColHistValues, *self.histFit),'red')
        ax5.set_title('Histogram')
        ax5.set_xlabel('T(K)')
        ax5.set_ylabel('# Counts')

        plt.show()