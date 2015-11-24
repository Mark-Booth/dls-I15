'''
Created on 24 Nov 2015

@author: wnm24546
'''

from scipy.constants import c, h, k, pi
from scipy.optimize import curve_fit
import numpy as np

#k is kb

class LuckyCalculations(object):
    
    def __init__(self, data, calib, integConf, bulbTemp):
        self.dataSet = data
        self.calibSet = calib
        self.intConf = integConf
        self.bulbTemp = bulbTemp
        
        self.planckPlotRange = [500, 1000]
        self.wienPlotRange = [1e9 / self.planckPlotRange[1], 1e9/self.planckPlotRange[0]]
        
        #Prepare the data
        self.updateData()
        self.fitAll()
                
        #Create a plot object
        self.plots = LuckyPlots(self)
    
    def update(self, data=None, calib=None, integConf=None, bulbTemp=None):
        self.dataSet = data if (data != None) else self.dataSet
        self.calibSet = calib if (calib != None) else self.calibSet
        self.intConf = integConf if (integConf != None) else self.intConf
        self.bulbTemp = bulbTemp if (bulbTemp != None) else self.bulbTemp
        
        self.updateData()
        self.fitAll()
        self.plots.reDraw(self)
    
    
    def updateData(self):
        #Normalises collected data
        self.planckIdeal = self.planck(self.dataSet[0], 1, self.bulbTemp)
        self.planckIdeal = np.reshape(self.planckIdeal, (1, len(self.planckIdeal)))
        #This step adds the normalised dataset back to the original data array
        self.dataSet = np.concatenate((self.dataSet, self.dataSet[1] / self.calibSet[1] * self.planckIdeal), axis=0)
        
        #Data sets for fitting or plotting, limited by integration range
        self.invWL = 1e9 / self.dataSet[0]# For Wien function
        self.invWLIntegLim = self.invWL[self.intConf[0]:self.intConf[1]]
        self.wlIntegLim = self.dataSet[0][self.intConf[0]:self.intConf[1]]
        self.normIntegLim = self.dataSet[2][self.intConf[0]:self.intConf[1]]
        
        #Calculate functions over the range of data
        self.wienData = self.wien(self.dataSet[0], self.dataSet[2])
        self.wienDataIntegLim = self.wienData[self.intConf[0]:self.intConf[1]]
        self.twoColData = self.twoColour(self.dataSet[0], self.dataSet[2], self.intConf[2])
        self.twoColDataLim = self.twoColData[self.intConf[0]:self.intConf[1]]
        self.twoColHistFreq, self.twoColHistValues = np.histogram(self.twoColDataLim, bins=range(1000,3000), density=False)
        self.twoColHistValues = np.delete(self.twoColHistValues, len(self.twoColHistFreq), 0)
        
        
    def fitAll(self):
        self.fitPlanck()
        self.fitWien()
        self.fitHistogram()
    
    def fitPlanck(self):
        #Do some fitting for Planck...
        ###
        self.planckFit, planckCov = curve_fit(self.planck, self.wlIntegLim, self.normIntegLim, [1,2000])
        self.planckTemp = self.planckFit[1]
        self.planckEmiss = self.planckFit[0]
        #Planck with fit params(??)
        self.planckFitData = self.planck(self.wlIntegLim, self.planckEmiss, self.planckTemp)
    
    def fitWien(self):
        #Do some fitting for Wien...
        ###
        self.wienFit, wienCov = curve_fit(self.fWien, self.invWLIntegLim[(np.isfinite(self.wienDataIntegLim))], self.wienDataIntegLim[(np.isfinite(self.wienDataIntegLim))], p0=[1, self.planckTemp])
        self.wienResidual = self.wienDataIntegLim - self.fWien(self.invWLIntegLim[(np.isfinite(self.wienDataIntegLim))], *self.wienFit)
        self.wienTemp = self.wienFit[1]

        pass
    
    def fitHistogram(self):
        #Gaussian fit of two colour histogram
        ###
        self.histFit, histCov = curve_fit(self.gaus, self.twoColHistValues, self.twoColHistFreq, p0=[1000,self.planckTemp,100])
        self.histTemp = self.histFit[1]
        self.histErr = self.histFit[2]
    
    #Planck function
    def planck(self, wavelength, emiss, temp):
        wavelength = wavelength * 1e-9
        return emiss / np.power(wavelength, 5) * (2 * pi * h * np.power(c, 2)) / np.expm1((h * c)/(k * wavelength * temp))
    
    #Wien function
    def wien(self, wavelength, intens):
        wavelength = wavelength * 1e-9
        return self.wienBase(np.power(wavelength, 5) * intens / (2 * pi * h * np.power(c, 2)))
        
    #Linear Wien function
    def fWien(self, wavelength, emiss, temp):
#         wavelength = wavelength * 1e-9
        return self.wienBase(emiss) - (1/temp) * wavelength
    
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
            return np.log(intens / (2 * pi * h * np.power(c, 2) * np.power(wavelength, 5))) * (k / (h *c))
        
        for i in range(nWindows):
            f1 = 1 / wavelength[i]
            f2 = 1 / wavelength[i + delta]
            i1 = twoColCalc(f1, intens[i])
            i2 = twoColCalc(f2, intens[i+delta])
            twoCol.append(abs((f2 - f1) / (i2 - i1)))
        
        for i in range(nWindows, nPoints):
            twoCol.append(float('nan'))
        
        return twoCol
    
    #Gaussian for fit
    def gaus(self, x, a, x0, sigma):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))

###


import matplotlib.pyplot as plt

class LuckyPlots(object):
    def __init__(self, luckyCalcs):
        self.calcs = luckyCalcs
        
        self.ax1 = plt.subplot(3, 2, 1)#Raw+Calib
        self.ax2 = plt.subplot(3, 2, 3)#Planck
        self.ax2 = plt.subplot(3, 2, 4)#Wien
        self.ax2 = plt.subplot(3, 2, 5)#2Colour
        self.ax2 = plt.subplot(3, 2, 6)#Histogram
        plt.subplots_adjust(wspace=0.3, hspace=0.3)
        
        #One-time configuration of plots
        self.ax1.set_title('Raw & Calibration Data')
        self.ax1.set_xlabel('Wavelength / nm')
        self.ax1.grid(True, linestyle='-')
        
        self.ax2.set_title('Planck Function Data')
        self.ax2.set_xlabel('Wavelength / nm')
        self.ax2.set_yticks([])
        
        self.ax3.set_title('Wien Function Data')
        self.ax3.set_xlabel(r'1/Wavelength / m$^{-1}$')
        self.ax3.set_ylabel("Wien Function")
        self.ax3.set_yticks([])
        
        self.ax4.set_title('Sliding Two-Colour Function')
        self.ax4.set_xlabel('Wavelength  / nm')
        self.ax4.set_ylabel('Temperature / K')
        self.ax4.grid(True, linestyle='-')
        
        self.ax5.set_title('Histogram (from Two-Colour Function)')
        self.ax5.set_xlabel('Temperature / K')
        self.ax5.set_ylabel('Counts / a.u.')
     
        self.updatePlots(False)
        
        #All the plots are set up, so set interactive and show
        plt.ion()
        plt.show()
            
    def updatePlots(self, redraw):
        #Raw and calibration data subgraph 
        self.ax1.plot(self.calcs.dataSet[0], self.calcs.dataSet[1], 
                 self.calcs.dataSet[0], self.calcs.calibSet[1],'red')
        self.ax1.set_ylim(0, self.getYMax(self.calcs.dataSet[1], self.calcs.calibSet[1]))
#        self.ax1.set_ylim(0,50000) #TODO Get max fn.
        
        #Planck data subgraph
        self.ax2.plot(self.calcs.dataSet[0], self.calcs.dataSet[2], 
                 self.calcs.wlIntegLim, self.calcs.planckFitData, 'red')
        self.ax2.set_xlim(*self.calcs.planckPlotRange)
          
        #Wien data subgraph
        self.ax3.plot(self.calcs.invWL, self.calcs.wienData,
                 self.calcs.invWLIntegLim, self.calcs.FWien(self.calcs.invWLIntegLim,*self.calcs.wienFit), 'red', 
                 self.calcs.invWLIntegLim, self.calcs.wienResidual)
        self.ax3.set_xlim(*self.calcs.wienPlotRange)
        
        #Two Colour data subgraph
        self.ax4.plot(self.calcs.dataSet[0], self.calcs.twoColData, 
                 self.calcs.wlIntegLim, self.calcs.twoColDataLim, 'red')
        self.ax4.set_xlim(*self.calcs.planckPlotRange)
        
        #Histogram subgraph
        self.ax5.plot(self.calcs.twoColHistValues, self.calcs.twoColHistFreq,
                 self.calcs.twoColHistValues, self.calcs.gaus(self.calcs.twoColHistValues, *self.calcs.histFit), 'red')
        
        if redraw:
            plt.draw()
            
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

    def reDraw(self, luckyCalcs):
        self.calcs = luckyCalcs
        self.updatePlots(True)
        
    def getYMax(self, *data):
        maxes = []
        for dat in data:
            maxes.append(np.amax(dat))
        
        return max(maxes)*1.1
    
    