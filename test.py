#!/usr/bin/env python3
# −*− coding:utf-8 −*−

import numpy as np
import matplotlib.pyplot as plt
from signal_smooth import *

''' load all data '''
data = np.genfromtxt("test.txt")
x = data[:,0]
y = data[:,1]

''' extract data if y-coordinate from 0.17857 to 0.18724 '''
data_cut = data[(data[:,1]>=0.17857) & (data[:,1]<=0.18724)]
x_cut = data_cut[:,0]
y_cut = data_cut[:,1]

''' collect the unique x value from the extracted data '''
x_cut_unique = np.unique(x_cut)
# calculate the mean value (four kind of mean) of y at each unique x
#y_cut_HM = np.array([1/np.mean(1/y_cut[np.where(x_cut == x_value)]) for x_value in x_cut_unique]) # harmonic mean
#y_cut_GM = np.array([np.exp(np.mean(np.log(y_cut[np.where(x_cut == x_value)]))) for x_value in x_cut_unique]) # geometric mean
#y_cut_AM = np.array([np.mean(y_cut[np.where(x_cut == x_value)]) for x_value in x_cut_unique]) # arithmetic mean
y_cut_QM = np.array([np.sqrt(np.mean(y_cut[np.where(x_cut == x_value)]**2)) for x_value in x_cut_unique]) # quadratic mean

''' applying SIGSMOOTH method '''
sig_smooth = SIGSMOOTH(y_cut_QM)
y_smooth = sig_smooth.PLS_interpolation(x_cut_unique, l=1e11, n=2)

''' save the result '''
#np.savetxt("Test_line.txt", np.vstack((x_cut_unique, y_smooth)).T, fmt='%3.17f %1.20f')

''' plot the result '''
fig, ax = plt.subplots()
ax.scatter(x, y, alpha=0.1, s=20)
ax.plot(x_cut_unique, y_smooth, color='orange')
plt.show()
