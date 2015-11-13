# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:30:10 2015

@author: roc54795
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

fig, ax = plt.subplots()

ax.scatter(np.random.normal(size=1000), np.random.normal(size=1000))

# useblit = True can lead to better performance on some backends
cursor = Cursor(ax, useblit=True, color='gray', linewidth=1)
