#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from psychopy import visual, core, event, gui
import random
import winsound
from psychopy.tools import filetools
import filename
import numpy as np
import pandas as pd 

from PIL import Image
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common_seung import *

image_path = "./동물"
image_list = []
for i in os.listdir(image_path):
    image_list.append(os.path.join(image_path, i))
    if i.startswith('nogo'): # nogo 이미지는 두번
        image_list.append(os.path.join(image_path, i))
    
class drawling_image(drawling_object):
    def __init__(self, x, y, image, height = 1):
        image1 = Image.open(image)
        mag1_size = image1.size
        y_x = image1.size[0] / image1.size[1]
        self.image = visual.ImageStim(win, pos=[x, y], image=image, size=[y_x * height, height])
        super().__init__(self.image)
        
        
        
participant_id = inputParticipant()

#윈도우
win = visual.Window([1600, 900], allowGUI=True, fullscr=False, units='height')
window = window_manager(win)

introduction = ["g1.png","g2.png","g3.png","g4.png"]
for file_name in introduction:
    image = drawling_image(0, 0, file_name)
    window.append(image)
    window.update_wait_key()
    window.remove(image)


orders = image_list * 5
random.shuffle(orders)
    
result = pyresult(participant_id, 'Go, No-Go')

score = 0
inhibition = 0

go_reaction_time = []
nogo_reaction_time = []
for i, image_name in enumerate(orders):
    window.update_wait_time(0.5)
    image = drawling_image(0, 0, image_name, height=1) 
    window.append(image)
    go = not(os.path.basename(image_name).startswith('nogo'))
    
    start = datetime.now()
    while True:
        window.update()
        time = (datetime.now()-start).total_seconds()
        
        response_go = 'None'
        if window.getPressKey('space') or window.mouse.getClicked():
            response_go = True

        if time >= 1:
            response_go = False
            
        if response_go != 'None':
            result.write('trial_stimulus', 'Go' if go else 'NoGo', index=i)
            result.write('trial_response', 'Go' if response_go else 'NoGo', index=i)
            if go:
                result.write('trial_correct', 'Y' if go == response_go else 'N', index=i)
            else:
                result.write('trial_correct', '1' if go == response_go else '0', index=i)
                
            if go == True and response_go == True:
                score += 1
                
            if go == False and response_go == False:
                inhibition += 1
                
            if response_go:
                result.write('trial_reaction_time', time, index=i)
                if go:
                    go_reaction_time.append(time)
                else:
                    nogo_reaction_time.append(time)
                    
                
                
            break
            
    
    result.write('inhibition', inhibition)
    result.write('score', score)
    if len(go_reaction_time) > 0:
        result.write('go_reaction_time', np.array(go_reaction_time).mean())
        
    if len(nogo_reaction_time) > 0:
        result.write('nogo_reaction_time', np.array(nogo_reaction_time).mean())
    result.save()
    window.remove(image)
                
exit()


subinfo = filename.getSubjInfo()

win = visual.Window(fullscr=False, color=[1,1,1], units='pix')
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
