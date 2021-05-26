#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, gui, data
from PIL import Image
import random
import winsound
import sys             #sys.exit()

import numpy as np
import threading

import os, sys
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from common_seung import *

participant_info = inputParticipant()
win, window = initWindow()


basic_left_image = drawling_image(-0.35, +0.2, "Blue_rabbit.png", height=0.35) 
basic_right_image = drawling_image(+0.35, +0.2, "Red_boat.png", height=0.35) 
window.append(basic_left_image)
window.append(basic_right_image)

basic_plus_image = drawling_text(0, -0.2, "+", color=[0,0,0], height=0.1) 
window.append(basic_plus_image)

def game(left=[], right=[], count=12):
    result = {
        'score': 0,
        'accuracy': 0,
        'reaction_time': [],
        'reaction_time_correct': [],
        'trials': []
    }
    
    orders = []
    images = []
    for i in left:
        image = drawling_image(0, -0.2, i, height=0.35)
        images.append(image)
        orders.append(('left', image))
        
    for i in right:
        image = drawling_image(0, -0.2, i, height=0.35)
        images.append(image)
        orders.append(('right', image))
        
    for i in images:
        i.z = 9
        i.setVisible(False)
        window.append(i)
        
    orders *= int(count / len(orders))
    random.shuffle(orders)
    for right_answer, image in orders:
        window.update_wait_time(0.5)
        image.setVisible(True)
        threading.Thread(target=lambda: winsound.Beep(580,500)).start()

        start = datetime.now()
        while True:
            window.update()
            time = (datetime.now()-start).total_seconds()
            
            response = 'none'
            if window.getPressKey('z'):
                response = 'left'
            if window.getPressKey('slash'):
                response = 'right'
                
            if response != 'none':
                image.setVisible(False)
                correct = response == right_answer
                result['trials'].append([response, 1 if correct else 0, time])
                
                if correct:
                    result['score'] += 1
                    result['reaction_time_correct'].append(time)
                
                result['reaction_time'].append(time)
                break
    
    result['reaction_time_correct'] = np.array(result['reaction_time_correct']).mean()
    result['reaction_time'] = np.array(result['reaction_time']).mean()
    result['accuracy'] = result['score'] / count
    return result
    
def save(index, xlsx, game_result):
    prefix = 'trial%d_' % index
    result.write(prefix + 'score', game_result['score'])
    result.write(prefix + 'reaction_time', game_result['reaction_time'])
    result.write(prefix + 'reaction_time_correct', game_result['reaction_time_correct'])
    
    for i, row in enumerate(game_result['trials']):
        result.write(prefix + 'each_response', row[0], index=i)
        result.write(prefix + 'each_correct', row[1], index=i)
        result.write(prefix + 'each_time', row[2], index=i)
    
# 기본값 Blue_rabbit, Red_boat
result = pyresult(participant_info, 'DCCS')

# 색깔로 맞추기
showExplanation(["T1.png", "T2.png", "T3.png", "T4.png", "T5.png", "T6.png", "T7.png", "T8.png"])
save(1, result, game(["Blue_boat.png"], ["Red_rabbit.png"]))

# 모양으로 맞추기
showExplanation(["TT1.png", "TT2.png", "TT3.png", "TT4.png", "TT5.png", "TT6.png", "TT7.png", "TT8.png"])
save(2, result, game(["Red_rabbit.png"], ["Blue_boat.png"]))

# 테두리 -> 색깔,  일반 -> 모양
showExplanation(["TTT1.png", "TTT2.png", "TTT3.png", "TTT4.png", "TTT5.png", "TTT6.png", "TTT7.png",  "TTT15.png", "TTT16.png", "TTT8.png", "TTT9.png", "TTT10.png", "TTT11.png", "TTT12.png", "TTT13.png", "TTT14.png"])
save(3, result, game(["blue_boat_square.png", "Red_rabbit.png"], ["red_rabbit_square.png", "Blue_boat.png"]))


result.save()