# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:32:05 2015

@author: roc54795
"""
import matplotlib.pyplot as plt
import sys
fig, ax = plt.subplots()

def on_button_press(event):
    print dir(event)
    print "Button:", event.button
    print "Figure coordinates:", event.x, event.y
    print "Data coordinates:", event.xdata, event.ydata
    sys.stdout.flush()
    
fig.canvas.mpl_connect('button_press_event', on_button_press)
