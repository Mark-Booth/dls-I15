'''
Created on 12 Jan 2016

@author: wnm24546
'''
import os
import numpy as np
from Lucky.Calculations import LuckyCalculations

wdir = os.path.join('.','testData')
dsDataFile = os.path.join(wdir, 'T_635.txt')
usDataFile = os.path.join(wdir, 'T_636.txt')
dsCalibFile = os.path.join(wdir, 'Calib.txt')
usCalibFile = os.path.join(wdir, 'CalibF2MTW.txt')
        
        
dsData = np.loadtxt(dsDataFile, unpack=True) ##Raw file
usData = np.loadtxt(usDataFile, unpack=True)
calib = np.loadtxt('./testData/Calib.txt', unpack=True) ##Calib file
integConf = [315, 800, 200] #Values lifted out of PreLucky_Variant.py
bulbTemp = 2436

luckCalc = LuckyCalculations(dsData, calib, integConf, bulbTemp, debug=True)
luckCalc.runCalculations()
