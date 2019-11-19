# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 09:39:37 2019

@author: LAP
"""


import matplotlib.pyplot as plt
import numpy as np

fileread = open("stopNames_lat_log.txt","r")

line = fileread.readline()

Xwhole = list()
Ywhole = list()

x=list()
y=list()
count = 0
while line:
    print(line)
    count += 1
    tmp = line.split('|')
    #gps = tmp[1].split(',')
    #lat = float(gps[0])
    #log = float(gps[1].split('\n')[0])
    lat = float(tmp[1])
    log = float(tmp[2].split('\n')[0])
    x.append(lat)
    y.append(log)
    if (tmp[0] == 'Outer Ring Rd, Banashankari 3rd Stage, Banashankari, Bengaluru, Karnataka 560085, India'):
        
        Xwhole.append(x)
        Ywhole.append(y)
        x = list()
        y = list()
        line = fileread.readline()
    line = fileread.readline()
    print(count)

color = ['black','green','red','pink','orange','yellow','blue','purple']

for i in range(len(Xwhole)):
    print(i)
    plt.plot(Xwhole[i],Ywhole[i],c=color[i])
    #plt.show()
    
#plt.scatter() plot for PES University
plt.scatter(12.9344948 ,77.5345164,s=40,c='blue')
plt.show()

'''
Clarence stop
42.9716062 | -78.6317353

do 3, 6, 4->one stop is off


mapping : 4-6, 1-2, 2-5, 3-5
'''