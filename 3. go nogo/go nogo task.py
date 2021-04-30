#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from psychopy import visual, core, event, gui
import random
import winsound
from psychopy.tools import filetools
import filename
import numpy as np
import pandas as pd 

subinfo = filename.getSubjInfo()

win = visual.Window(fullscr=True, color=[1,1,1], units='pix')
intro = visual.ImageStim(win, units='pix')
first = visual.ImageStim(win, units='pix')
#animal = visual.ImageStim(win, units='pix')
preFix = visual.TextStim(win, text='+', color=[-1,-1,-1], height=50, units='pix')
stim = visual.ImageStim(win, units ='pix')             #Stimulus
RT = core.Clock()


introduction = ["g1.png","g2.png","g3.png","g4.png"]
for int in introduction:
    intro.image = int
    intro.draw()
    win.flip()
    while 'space' not in event.getKeys():pass

animals = ["cow.png", "cat.png", "bear.png", "zebra.png", "elephant.png", "giraffe.png", "rabbit.png", "dog.png", "wolf.png", "lion.png", "tiger.png", "tiger2.png"]     #tiger-10
order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
orders = []

for j in range(5):
    random.shuffle(order)
    orders.extend(order)
#print orders
results = []

for i in orders:
    preFix.draw()
    win.flip()
    winsound.Beep(880,500) 
    core.wait(0.5)
    stim.image = animals[i]
    stim.draw()
    win.flip()
    RT.reset()
     
    keys = []
    event.clearEvents('keyboard')
    while (len(keys) == 0) and (RT.getTime() < 1.0):
        keys = event.getKeys(['space'], timeStamped=RT)

    if len(keys) == 0:
        keys.append(('No space', 1))
#core.wait(0.5)
    print(i, keys[0][0], keys[0][1])
    results.append([i, keys[0][1]])

filename.saveResult('GNG',subinfo, basket)
alpha=np.array(basket)
alpha2=pd.DataFrame(alpha)
fname = 'GNG' + subinfo[0] + subinfo[1] + '.csv'
alpha2.to_csv(fname)

first.image = "g5.png"
first.draw()
win.flip()
while 'space' not in event.getKeys():pass

win.close()
