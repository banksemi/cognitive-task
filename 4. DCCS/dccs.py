#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, gui, data
from PIL import Image
import random
import winsound
import sys             #sys.exit()
import os
import numpy as np
import threading

import os, sys
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from common_seung import *

participant_info = inputParticipant('DCCS')
win, window = initWindow()


basic_left_image = drawling_image(-0.37, +0.23, "이미지/blue_rabbit.png", height=0.4) 
basic_right_image = drawling_image(+0.37, +0.23, "이미지/red_boat.png", height=0.4) 
window.append(basic_left_image)
window.append(basic_right_image)

basic_plus_image = drawling_text(0, -0.2, "+", color=[0,0,0], height=0.1) 
window.append(basic_plus_image)
def trial(right_answer, image_name, timeout=3):
    winsound.Beep(31111,1)
    image = images[image_name]
    trial_result = {}
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
            trial_result['trial_response'] = response
            trial_result['trial_correct'] = 1 if correct else 0
            trial_result['trial_time'] = time
            return trial_result

        if time >= timeout:
            image.setVisible(False)
            trial_result['trial_correct'] = 0
            trial_result['trial_response'] = response

            return trial_result

def game(index, answer, count=12):
    left=[]
    right=[]

    for i in answer:
        if answer[i] == 'left':
            left.append(i)
        if answer[i] == 'right':
            right.append(i)
    reaction_time= []
    reaction_time_correct= []
    
    orders = []
    for i in left:
        orders.append(('left', i))
        
    for i in right:
        orders.append(('right', i))

    orders *= int(count / len(orders))
    random.shuffle(orders)
    
    prefix = 'trial%d_' % index
    for trial_index, (right_answer, image_name) in enumerate(orders):
        trial_result = trial(right_answer, image_name, timeout=15) # 본 시행시 무반응 시간

        if trial_result['trial_correct']:
            reaction_time_correct.append(trial_result['trial_time'])
        reaction_time.append(trial_result['trial_time'])

        for i in trial_result:
            result.write(i.replace('trial_', prefix + 'each_'), trial_result[i], index=trial_index)
        result.save()
        
    result.write(prefix + 'reaction_time', np.array(reaction_time).mean())
    result.write(prefix + 'reaction_time_correct', np.array(reaction_time_correct).mean())
    result.save()
    

# 기본값 Blue_rabbit, Red_boat
result = pyresult(participant_info, 'DCCS')

# 사용할 이미지를 사전 등록
images = {}
for i in os.listdir("./이미지"):
    image_path = os.path.join("./이미지", i)
    image = drawling_image(0, -0.23, image_path, height=0.4)
    image.z = 9
    image.setVisible(False)
    window.append(image)
    images[i] = image

explaning = ['./튜토리얼/DCCS(A)_T%d.PNG' % i for i in range(0,60)]
# 색깔로 맞추기

practice = lambda x: trial(answer[x], x)['trial_correct'] == 1

answer = {
    "blue_boat.png": 'left',
    "red_rabbit.png": 'right'
}
window.save_state()
try:
    showExplanation(explaning[1:1+9])
    # 연습시행 1
    if not practice("red_rabbit.png"):
        showExplanation(explaning[11:11+3])
 
    if practice("blue_boat.png"):
        showExplanation(explaning[10])
    else:
        showExplanation(explaning[14:14+2])
        showExplanation(explaning[13])
    # 연습시행 2
    while True:
        if not practice("blue_boat.png"):
            showExplanation(explaning[14:14+2])
            showExplanation(explaning[13])

        if practice("red_rabbit.png"):
            break
        else:
            showExplanation(explaning[11:11+3])
except PassException as e: 
    window.load_state()
showExplanation(explaning[16])
game(1, answer)

answer = {
    "blue_boat.png": 'right',
    "red_rabbit.png": 'left'
}
window.save_state()
try:
    showExplanation(explaning[17:17+7])
    if not practice("red_rabbit.png"):
        showExplanation(explaning[25:25+3])
 
    if practice("blue_boat.png"):
        showExplanation(explaning[24])
    else:
        showExplanation(explaning[28:28+2])
        showExplanation(explaning[27])

    # 연습시행 2
    while True:
        if not practice("blue_boat.png"):
            showExplanation(explaning[28:28+2])
            showExplanation(explaning[27])

        if practice("red_rabbit.png"):
            break
        else:
            showExplanation(explaning[25:25+3])

except PassException as e: 
    window.load_state()

showExplanation(explaning[30])
game(2, answer)


# 테두리 -> 색깔,  일반 -> 모양
answer = {
    "blue_boat_square.png": 'left',
    "red_rabbit_square.png": 'right',
    "blue_boat.png": 'right',
    "red_rabbit.png": 'left',
}
window.save_state()
try:
    showExplanation(explaning[31:31+14])
    if not practice("blue_boat_square.png"):
        showExplanation(explaning[46:46+3])

    if not practice("red_rabbit_square.png"):
        showExplanation(explaning[49:49+2])
        showExplanation(explaning[48])

    if not practice("blue_boat.png"):
        showExplanation(explaning[51:51+2])
        showExplanation(explaning[48])

    if practice("red_rabbit.png"):
        showExplanation(explaning[45])
    else:
        showExplanation(explaning[53:53+2])
        showExplanation(explaning[48])


    while True:
        if not practice("red_rabbit_square.png"):
            showExplanation(explaning[49:49+2])
            showExplanation(explaning[48])

        if not practice("blue_boat.png"):
            showExplanation(explaning[51:51+2])
            showExplanation(explaning[48])

        if not practice("red_rabbit.png"):
            showExplanation(explaning[53:53+2])
            showExplanation(explaning[48])

        if practice("blue_boat_square.png"):
            break
        else:
            showExplanation(explaning[46:46+3])

except PassException as e: 
    window.load_state()
showExplanation(explaning[55])
game(3, answer)


result.save()