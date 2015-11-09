# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:24:12 2015

@author: roc54795
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.3)

t = np.linspace(0, 10, 1000)
lines = ax.plot(t, np.sin(t))

rax = plt.axes([0.05, 0.4, 0.15, 0.15])
radio = RadioButtons(rax, ('-', '--', '-.', 'steps', ':'))

def stylefunc(label):
    lines[0].set_linestyle(label)
    plt.draw()
    
radio.on_clicked(stylefunc)
