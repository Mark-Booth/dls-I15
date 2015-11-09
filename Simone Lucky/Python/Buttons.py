# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:25:30 2015

@author: roc54795
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)

t = np.linspace(0, 10, 1000)
line, = plt.plot(t, np.sin(t), lw=2)

class Index:
    dt = 0
    def next(self, event):
        self.dt -= 1
        line.set_ydata(np.sin(t + self.dt))
        fig.canvas.draw()

    def prev(self, event):
        self.dt += 1
        line.set_ydata(np.sin(t + self.dt))
        fig.canvas.draw()

callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])

bnext = Button(axnext, '>')
bnext.on_clicked(callback.next)

bprev = Button(axprev, '<')
bprev.on_clicked(callback.prev)
