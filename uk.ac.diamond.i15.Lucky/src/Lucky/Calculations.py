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
        self.invWL = 1 / self.dataSet[0] * 1e9 # For Wien function
        
        #Data sets for fitting, limited by integration range
        self.wlIntegLim = self.dataSet[0][self.intConf[0]:self.intConf[1]]
        self.invWLIntegLim = self.invWL[self.intConf[0]:self.intConf[1]]
        self.normIntegLim = self.dataSet[2][self.intConf[0]:self.intConf[1]]
        
        #Calculate functions over the range of data
        self.wienData = self.wien(self.dataSet[0], self.dataSet[2])
        self.twoColData = self.twoColour(self.dataSet[0], self.dataSet[2], self.intConf[2])
        self.twoColHistFreq, self.twoColHistValues = np.histogram(self.twoColData[self.intConf[0]:self.intConf[1]], bins=range(1000,3000), density=False)
        self.twoColHistValues = np.delete(self.twoColHistValues, len(self.twoColHistFreq), 0)
        
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
        wienFit, wienCov = curve_fit(self.fWien, self.invWLIntegLim[(np.isfinite(wienIntegLim))], wienIntegLim[(np.isfinite(wienIntegLim))], p0 = [1, self.planckTemp])
        self.wienResidual = wienIntegLim - self.fWien(self.invWLIntegLim[(np.isfinite(wienIntegLim))], *wienFit)
        self.wienTemp = self.wienFit[1]
        
        #Gaussian fit of two colour histogram
        ###
        histFit, histCov = curve_fit(self.gaus, self.twoColHistFreq, p0=[1000,self.planckTemp,100])
        self.histTemp = histFit[1]
        self.histErr = histFit[2]
    
    
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
    
    def drawPlots(self, x,y,yC,Norm,xp,FP,PFrom,PTo,invX,W,invX1,bestW,Two2,value,freq,popt,TwoInt,Residual,TP):
        fig = plt.figure(figsize=(8,11))#Defines dimension of the figure 

        #Adding subplots to show
        ax1 = fig.add_subplot(3, 2, 1)
        ax2 = fig.add_subplot(3, 2, 2)
        ax3 = fig.add_subplot(3, 2, 3)
        ax4 = fig.add_subplot(3, 2, 4)
        ax5 = fig.add_subplot(3, 2, 5)
        plt.subplots_adjust(wspace=0.3,hspace=0.3)
 
        #Raw and calibration data subgraph 
        ax1.plot(x, y, x, yC,'red')
        ax1.set_title('Raw vs Calib data')
        ax1.set_xlabel('wavelength (nm)')
        ax1.set_ylim(0,50000)
        ax1.grid(True)
        ticklines = ax1.get_xticklines()
        ticklines.extend( ax1.get_yticklines() )
        gridlines = ax1.get_xgridlines()
        gridlines.extend( ax1.get_ygridlines() )
        ticklabels = ax1.get_xticklabels()
        ticklabels.extend( ax1.get_yticklabels() )

        for line in ticklines:
            line.set_linewidth(3)

        for line in gridlines:
            line.set_linestyle('-')

        for label in ticklabels:
            label.set_color('black')
            label.set_fontsize('medium')


        txt=plt.text(4500,33,TP)
        txt1=plt.text(4200,33,'T=')
        txt2=plt.text(2000,17,TW)
        txt3=plt.text(1800,17,'T=')
        txt.set_size(15)
        txt1.set_size(15)
        txt2.set_size(15)
        txt3.set_size(15)
        fig.canvas.draw()
   

        #Planck subgraph
        ax2.plot(x, Norm, xp, FP,'red')
        ax2.set_title('Planck')
        ax2.set_xlabel('wavelength (nm)')
        ax2.set_xlim(PFrom,PTo)
        ax2.set_yticks([])
        #ax2.grid(True)
        def on_button_press(event):
            #print dir(event)
            #print "BADGER"
            #print "Button:", event.button
            #print "Figure coordinates:", event.x, event.y
            print "Data coordinates:", event.xdata, event.ydata
            #start=event.xdata
            sys.stdout.flush()
   
        #Wien subgraph
        ax3.plot(invX,W,invX1,self.FWien(invX1,*bestW),'red',invX1,Residual)
        ax3.set_title('Wien')
        ax3.set_xlabel('1/wavelength (1/m)')
        ax3.set_ylabel("Wien function")
        ax3.set_xlim(10**9/PTo,10**9/PFrom)
        ax3.set_yticks([])
        #ax3.grid(True)
   
    
        #Two Colours subgraph
        ax4.plot(x,Two2,x[start:end],TwoInt,'red')
        ax4.set_title('Sliding Two-Colours')
        ax4.set_xlabel('wavelength (nm)')
        ax4.set_ylabel('T (K)')
        ax4.set_xlim(PFrom,PTo)
        ax4.grid(True)
        ticklines4 = ax4.get_xticklines()
        ticklines4.extend( ax4.get_yticklines() )
        gridlines4 = ax4.get_xgridlines()
        gridlines4.extend( ax4.get_ygridlines() )
        ticklabels4 = ax4.get_xticklabels()
        ticklabels4.extend( ax4.get_yticklabels() )

        for line in ticklines4:
            line.set_linewidth(3)

        for line in gridlines4:
            line.set_linestyle('-')

        for label in ticklabels4:
            label.set_color('black')
            label.set_fontsize('medium')
   
    

        #Histogram subgraph
        ax5.plot(value,freq,value,self.gaus(value,*popt),'red')
        ax5.set_title('Histogram')
        ax5.set_xlabel('T(K)')
        ax5.set_ylabel('# Counts')
    


        #pylab.show() #it plots everything
        fig.canvas.mpl_connect('button_press_event', on_button_press)
        plt.show()