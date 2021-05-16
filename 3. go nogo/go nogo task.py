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
win = visual.Window([1600, 900], allowGUI=True, fullscr=False, units='height', color=[255,255,255])
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
            
    window.remove(image)
    
result.write('inhibition', inhibition)
result.write('score', score)
if len(go_reaction_time) > 0:
    result.write('go_reaction_time', np.array(go_reaction_time).mean())
        
if len(nogo_reaction_time) > 0:
    result.write('nogo_reaction_time', np.array(nogo_reaction_time).mean())
result.save()
                
