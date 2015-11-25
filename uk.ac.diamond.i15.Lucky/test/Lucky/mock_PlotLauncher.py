'''
Created on 25 Nov 2015

@author: wnm24546
'''
import numpy as np
import time
from Lucky.Calculations import LuckyCalculations, LuckyPlots
import matplotlib.pyplot as plt

data = np.loadtxt('/scratch/ecl-ws/misc-ws_git/dls-i15.git/uk.ac.diamond.i15.Lucky/test/Lucky/testData/T_62_1.txt', unpack=True) ##Raw file
calib = np.loadtxt('/scratch/ecl-ws/misc-ws_git/dls-i15.git/uk.ac.diamond.i15.Lucky/test/Lucky//testData/Calib.txt', unpack=True) ##Calib file
integConf = [315, 800, 200] #Values lifted out of PreLucky_Variant.py
bulbTemp = 2436

luckCalc = LuckyCalculations(data, calib, integConf, bulbTemp)
# luckCalc.plots.

#time.sleep(10)