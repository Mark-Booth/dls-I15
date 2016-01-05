'''
Created on 24 Nov 2015

@author: wnm24546
'''

from scipy.constants import c, h, k, pi
from scipy.optimize import curve_fit
import numpy as np
from Lucky.LuckyExceptions import BadModelStateException

#k is kb

class CalculationService(object):
    
    def __init__(self, pp):
        self.parentPresenter = pp
        
        self.planckResults = (0, 0, 0, 0)
        self.wienResults = (0, 0, 0, 0)
        
        #TODO Spawn calculations and plots in a separate thread
    def createCalcs(self, dM, debug=False):
        self.updateModel(dM)
        self.dsCalcs = LuckyCalculations(self.dsData, self.dsCalib,
                                         self.integConf, self.bulbTemp, "Downstream Measurement")
        self.usCalcs = LuckyCalculations(self.usData, self.usCalib,
                                         self.integConf, self.bulbTemp, "Upstream Measurement")
        self.dsCalcs.runCalculations()
        self.usCalcs.runCalculations()
        self.updateResults()
        
        #Create plot objects once we've got some data to plot
        self.dsPlots = LuckyPlots(self.dsCalcs)
        self.usPlots = LuckyPlots(self.usCalcs)
    
    def updateCalcs(self):
        #Perhaps add updateModel call?
        self.dsCalcs.runCalculations()
        self.usCalcs.runCalculations()
        self.updateResults()
        
        #Update the plots with new values from the calculations //TODO Enable these to update plots every re-calculation.
#        self.dsPlots.updatePlots()
#        self.usPlots.updatePlots()
    
    def updateResults(self):
        def calculateResults(dsVal, usVal):
            avs = (dsVal + usVal)/2
            diff = dsVal - usVal
            return [dsVal, usVal, avs, diff]
        
        self.planckResults = calculateResults(self.dsCalcs.planckTemp, self.usCalcs.planckTemp)
        self.wienResults = calculateResults(self.dsCalcs.wienTemp, self.usCalcs.wienTemp)
        
    def updateModel(self, dM):
        self.dsData, self.usData = self.openData(dM)
        self.dsCalib, self.usCalib = self.openCalib(dM.calibType, dM.calibConfigData)
        
        self.integConf = dM.integrationConf
        self.bulbTemp = dM.calibConfigData.bulbTemp
    
    def updateData(self, usData=None, dsData=None):
        if (usData == None) and (dsData == None):
            raise BadModelStateException("No data given for data update")
        
        if dsData != None:
            newData = np.loadtxt(usData)
            self.dsCalcs.update(data=newData)

        if usData != None:
            newData = np.loadtxt(usData)
            self.usCalcs.update(data=usData)
    
    def updateIntegration(self, integConf):
        self.dsCalcs.update(integConf=integConf)
        self.usCalcs.update(integConf=integConf)
    
    def updateCalibration(self, calibType, calibConf):
        self.dsCalib, self.usCalib = self.openCalib(calibType, calibConf)
        self.bulbTemp = calibConf.bulbTemp
        
        self.dsCalcs.update(calib=self.dsCalib, bulbTemp=self.bulbTemp)
        self.usCalcs.update(calib=self.usCalib, bulbTemp=self.bulbTemp)
    
    def openCalib(self, calibType, calibConfig):
        calibFileLabels = calibConfig.calibFiles.keys()
        dsCalib, usCalib = None, None 
        for i in range(len(calibType)):
            if calibType[i] == 1:
                dsCalib = str(calibConfig.calibFiles[calibFileLabels[2*i]])
                usCalib = str(calibConfig.calibFiles[calibFileLabels[2*i+1]])
            
            if None not in [dsCalib, usCalib]:
                break
        return np.loadtxt(dsCalib, unpack=True), np.loadtxt(usCalib, unpack=True)
    
    def openData(self, dM):
        return np.loadtxt(dM.usdsPair[0], unpack=True), np.loadtxt(dM.usdsPair[1], unpack=True)
    
class LuckyCalculations(object): #TODO Make calcs use calcserv to get bulbTemp, integConf & calibset
    
    def __init__(self, data, calib, integConf, bulbTemp, label, debug=False):
        self.dataSet = data
        self.calibSet = calib
        self.intConf = integConf
        self.bulbTemp = bulbTemp
        self.label = label
        
        self.planckPlotRange = [500, 1000]
        self.wienPlotRange = [1e9 / self.planckPlotRange[1], 1e9/self.planckPlotRange[0]]
        
        #Prepare the data
        self.normaliseData()
    
    def update(self, data=None, integConf=None, calib=None, bulbTemp=None):
        self.dataSet = data if (data != None) else self.dataSet
        self.intConf = integConf if (integConf != None) else self.intConf
        self.calibSet = calib if (calib != None) else self.calibSet
        self.bulbTemp = bulbTemp if (bulbTemp != None) else self.bulbTemp
        
        if (data != None) or (calib != None) or (bulbTemp != None):
            self.normaliseData()
        if integConf != None:
            self.calculateRanges()
    
    def normaliseData(self):
        self.planckIdeal = self.planck(self.dataSet[0], 1, self.bulbTemp)
        self.planckIdeal = np.reshape(self.planckIdeal, (1, len(self.planckIdeal)))
        #This step adds the normalises dataset & concatenates with the original data array
        self.dataSet = np.concatenate((self.dataSet, self.dataSet[1] / self.calibSet[1] * self.planckIdeal), axis=0)
        
        #We've changed the data so we need to recalculate the ranges:
        self.calculateRanges()
    
    def calculateRanges(self):
        #Data sets for fitting or plotting, limited by integration range
        self.invWL = 1e9 / self.dataSet[0]# For Wien function
        self.invWLIntegLim = self.invWL[self.intConf[0]:self.intConf[1]]
        self.wlIntegLim = self.dataSet[0][self.intConf[0]:self.intConf[1]]
        self.normIntegLim = self.dataSet[2][self.intConf[0]:self.intConf[1]]
        
    def runCalculations(self):
        #Calculate functions over the range of data
        self.wienData = self.wien(self.dataSet[0], self.dataSet[2])
        self.wienDataIntegLim = self.wienData[self.intConf[0]:self.intConf[1]]
        self.twoColData = self.twoColour(self.dataSet[0], self.dataSet[2], self.intConf[2])
        self.twoColDataLim = self.twoColData[self.intConf[0]:self.intConf[1]]
        self.twoColHistFreq, self.twoColHistValues = np.histogram(self.twoColDataLim, bins=range(1000,3000), density=False)
        self.twoColHistValues = np.delete(self.twoColHistValues, len(self.twoColHistFreq), 0)
        
        #Do fits
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
            return np.log(intens * np.power(wavelength, 5) / (2 * pi * h * np.power(c, 2))) * (k / (h *c))
        
        for i in range(nWindows):
            f1 = (h * c) / (wavelength[i] * k)
            f2 = (h * c) / (wavelength[i + delta] * k)
            i1 = twoColCalc(wavelength[i], intens[i])
            i2 = twoColCalc(wavelength[i + delta], intens[i+delta])
            twoCol.append((f1 - f2) / (i2 - i1))
        
        for i in range(nWindows, nPoints):
            twoCol.append(float('nan'))
        
        return twoCol
    
    #Gaussian for fit
    def gaus(self, x, a, x0, sigma):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))

###


import matplotlib.pyplot as plt

class LuckyPlots(object):
    def __init__(self, luckyCalcs, debug=False):
        if debug:
            return
        self.debug = debug
        
        self.fig = plt.figure()
        self.fig.suptitle(luckyCalcs.label, fontsize="16", weight="bold")
        self.ax1 = self.fig.add_subplot(3, 2, 1)#Raw+Calib
        self.ax2 = self.fig.add_subplot(3, 2, 3)#Planck
        self.ax3 = self.fig.add_subplot(3, 2, 4)#Wien
        self.ax4 = self.fig.add_subplot(3, 2, 5)#2Colour
        self.ax5 = self.fig.add_subplot(3, 2, 6)#Histogram
        #Layout settings for the plots
        plt.subplots_adjust(wspace=0.3, hspace=0.7)
        
        #One-time configuration of plots
        self.ax1.set_title('Raw & Calibration Data', fontsize='medium', style='italic')
        self.ax1.set_xlabel('Wavelength / nm')
        self.ax1.grid(True, linestyle='-')
        
        self.ax2.set_title('Planck Function Data', fontsize='medium', style='italic')
        self.ax2.set_xlabel('Wavelength / nm')
        self.ax2.set_yticks([])
        
        self.ax3.set_title('Wien Function Data', fontsize='medium', style='italic')
        self.ax3.set_xlabel(r'1/Wavelength / m$^{-1}$')
        self.ax3.set_ylabel("Wien Function")
        self.ax3.set_yticks([])
        
        self.ax4.set_title('Sliding Two-Colour Function', fontsize='medium', style='italic')
        self.ax4.set_xlabel('Wavelength  / nm')
        self.ax4.set_ylabel('Temperature / K')
        self.ax4.grid(True, linestyle='-')
        
        self.ax5.set_title('Histogram (from Two-Colour Function)', fontsize='medium', style='italic')
        self.ax5.set_xlabel('Temperature / K')
        self.ax5.set_ylabel('Counts / a.u.')
     
        self.updatePlots(luckyCalcs, redraw=False)
         
        if not self.debug:
            #Draw the plots if we're not debugging
            plt.ion()
            plt.show()
            #Needed to make plt appear!
            #   http://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
            plt.pause(0.001)
            
    def updatePlots(self, calcs, redraw=True):
        #Raw and calibration data subgraph 
        self.ax1.plot(calcs.dataSet[0], calcs.dataSet[1], 
                 calcs.dataSet[0], calcs.calibSet[1],'red')
        self.ax1.set_ylim(0, self.getYMax(calcs.dataSet[1], calcs.calibSet[1]))
#        self.ax1.set_ylim(0,50000) #TODO Get max fn.
        
        #Planck data subgraph
        self.ax2.plot(calcs.dataSet[0], calcs.dataSet[2], 
                 calcs.wlIntegLim, calcs.planckFitData, 'red')
        self.ax2.set_xlim(*calcs.planckPlotRange)
          
        #Wien data subgraph
        self.ax3.plot(calcs.invWL, calcs.wienData,
                 calcs.invWLIntegLim, calcs.fWien(calcs.invWLIntegLim,*calcs.wienFit), 'red', 
                 calcs.invWLIntegLim, calcs.wienResidual)
        self.ax3.set_xlim(*calcs.wienPlotRange)
        
        #Two Colour data subgraph
        self.ax4.plot(calcs.dataSet[0], calcs.twoColData, 
                 calcs.wlIntegLim, calcs.twoColDataLim, 'red')
        self.ax4.set_xlim(*calcs.planckPlotRange)
        
        #Histogram subgraph
        self.ax5.plot(calcs.twoColHistValues, calcs.twoColHistFreq,
                 calcs.twoColHistValues, calcs.gaus(calcs.twoColHistValues, *calcs.histFit), 'red')
        
        if redraw and not self.debug:
            plt.draw()
            #Needed to make plt appear!
            #   http://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
            plt.pause(0.001)
            
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
        
    def getYMax(self, *data):
        maxes = []
        for dat in data:
            maxes.append(np.amax(dat))
        
        return max(maxes)*1.1
    
    