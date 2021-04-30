#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pickle
import glob
import csv
import sys
#import matplotlib.pyplot as plt
#from matplotlib import font_manager, rc

files = glob.glob('*.pkl2')         # total file -1
file = open(files[0])               # open file number
alpha = pickle.load(file)
file.close()

objnum = len(alpha[1])


#print pd.DataFrame(alpha[1])

#sys.exit(0)

eggbox = np.zeros((4, 20))
eggox = np.zeros((4, 20))


def makegg():
    for i in range(objnum) :
        eggbox[i/20][i%20] = alpha[1][i][2]
        if eggbox[i/20][i%20] > 15.0 or eggbox[i/20][i%20] < 0.3:
            eggbox[i/20][i%20] = 0
    
    for puck,_ in enumerate(range(8,20)):
        eggbox[3][puck] = eggbox[2][_]
    
    eggbox[2][8:20] = 0
    return eggbox

print (makegg())

def makox():
    for j in range(objnum) :
        eggox[j/20][j%20] = alpha[1][j][1]

    for puck,_ in enumerate(range(8,20)):
        eggox[3][puck] = eggox[2][_]
    
    for i in range(80) :
        if eggbox[i/20][i%20] == 0:
            eggox[i/20][i%20] = 0

    return eggox

print(makox())


filternum = np.sum(makox(), axis = 1)    #correct amount
filter1data = makegg() * makox()
filtersum = np.sum(filter1data, axis = 1)
filterave = filtersum / filternum
#print filterave
#print filternum
wholedata = zip(filterave,filternum)
#print wholedata

pasta = np.array(wholedata)
pasta = pasta.reshape(1,8)
print(pasta)


threelayerporkbelly = pd.DataFrame(pasta)
threelayerporkbelly.to_csv('DCCS#00.csv')