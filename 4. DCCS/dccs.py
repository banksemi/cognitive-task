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

task_type = getTaskType()

participant_info = inputParticipant('DCCS')
win, window = initWindow()

if task_type == 'A':
    basic_left_image = drawling_image(-0.37, +0.23, "이미지/blue_rabbit.png", height=0.45) 
    basic_right_image = drawling_image(+0.37, +0.23, "이미지/red_boat.png", height=0.45)
elif task_type == 'B':
    basic_left_image = drawling_image(-0.37, +0.23, "이미지/yellow_truck.png", height=0.45) 
    basic_right_image = drawling_image(+0.37, +0.23, "이미지/green_flower.png", height=0.45)
window.append(basic_left_image)
window.append(basic_right_image)

basic_plus_image = drawling_text(0, -0.2, "+", color=[0,0,0], height=0.1) 
window.append(basic_plus_image)
def trial(right_answer, image_name, timeout=5):
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
    prefix = 'trial%d_' % index
    reaction_time= []
    reaction_time_correct= []
    
    prefix = 'trial%d_' % index
    for trial_index in range(0, count):
        image_name = result.read(prefix + 'each_stimulus', trial_index)
        right_answer = answer[image_name]
        trial_result = trial(right_answer, image_name, timeout=10) # 본 시행시 무반응 시간

        if trial_result['trial_correct']:
            reaction_time_correct.append(trial_result['trial_time'])
        if trial_result['trial_response'] != 'none':
            reaction_time.append(trial_result['trial_time'])

        for i in trial_result:
            result.write(i.replace('trial_', prefix + 'each_'), trial_result[i], index=trial_index)
        result.save()
        
    if len(reaction_time) != 0:
        result.write(prefix + 'reaction_time', np.array(reaction_time).mean())
    if len(reaction_time_correct) != 0:
        result.write(prefix + 'reaction_time_correct', np.array(reaction_time_correct).mean())
    result.save()
    

# 기본값 Blue_rabbit, Red_boat
result = pyresult(participant_info, 'DCCS', task_type)

# 사용할 이미지를 사전 등록
images = {}
for i in os.listdir("./이미지"):
    image_path = os.path.join("./이미지", i)
    image = drawling_image(0, -0.23, image_path, height=0.45)
    image.z = 9
    image.setVisible(False)
    window.append(image)
    images[i] = image

explaning = ['./튜토리얼/DCCS(%s)_T%d.PNG' % (task_type, i) for i in range(0,60)]
practice = lambda x: trial(answer[x], x)['trial_correct'] == 1
if task_type == 'A':
    orders12 = ['blue_boat.png', 'red_rabbit.png']
    orders3 = ['blue_boat.png', 'red_rabbit.png', 'red_rabbit_square.png', 'blue_boat_square.png']
if task_type == 'B':
    orders12 = ['yellow_flower.png', 'green_truck.png']
    orders3 = ['yellow_flower.png', 'green_truck.png', 'yellow_flower_square.png', 'green_truck_square.png']
    random.seed(445) # B 과제 본시행을 위한 시드값 고정

orders12 *= int(12 / len(orders12))
random.shuffle(orders12)
for i in range(0,12):
    result.write('trial1_each_stimulus',orders12[i],i)
    
random.shuffle(orders12)
for i in range(0,12):
    result.write('trial2_each_stimulus',orders12[i],i)

orders3 *= int(12 / len(orders3))
random.shuffle(orders3)
for i in range(0,12):
    result.write('trial3_each_stimulus',orders3[i],i)
result.save()

if task_type == 'A':
    # 색깔로 맞추기
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
        for i in range(0,4):
            if not practice("blue_boat.png"):
                showExplanation(explaning[14:14+2])
                showExplanation(explaning[13])

            if practice("red_rabbit.png"):
                break
            else:
                showExplanation(explaning[11:11+2])
                if i != 3:
                    showExplanation(explaning[13])

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
        for i in range(0,4):
            if not practice("blue_boat.png"):
                showExplanation(explaning[28:28+2])
                showExplanation(explaning[27])

            if practice("red_rabbit.png"):
                break
            else:
                showExplanation(explaning[25:25+2])                
                if i != 3:
                    showExplanation(explaning[27])

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


        for i in range(0,3):
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
                showExplanation(explaning[46:46+2])
                if i != 2:
                    showExplanation(explaning[48])

    except PassException as e: 
        window.load_state()
    showExplanation(explaning[55])
    game(3, answer)


if task_type == 'B':  # yellow_truck green_flower

    # 색깔로 맞추기
    answer = {
        "yellow_flower.png": 'left',
        "green_truck.png": 'right'
    }
    window.save_state()
    try:
        showExplanation(explaning[1:1+7])
        # 연습시행 1
        if not practice("green_truck.png"):
            showExplanation(explaning[9:9+3])
 
        if practice("yellow_flower.png"):
            showExplanation(explaning[8])
        else:
            showExplanation(explaning[12:12+2])
            showExplanation(explaning[11])
        # 연습시행 2
        for i in range(0,4):
            if not practice("yellow_flower.png"):
                showExplanation(explaning[12:12+2])
                showExplanation(explaning[11])

            if practice("green_truck.png"):
                break
            else:
                showExplanation(explaning[9:9+2])
                if i != 3:
                    showExplanation(explaning[11])
    except PassException as e: 
        window.load_state()
    showExplanation(explaning[14])
    game(1, answer) 

    answer = {
        "yellow_flower.png": 'right',
        "green_truck.png": 'left'
    }
    window.save_state()
    try:
        showExplanation(explaning[15:15+7])
        if not practice("green_truck.png"):
            showExplanation(explaning[26:26+2])
            showExplanation(explaning[25])
 
        if practice("yellow_flower.png"):
            showExplanation(explaning[22])
        else:
            showExplanation(explaning[23:23+3])

        # 연습시행 2
        for i in range(0,4):
            if not practice("yellow_flower.png"):
                showExplanation(explaning[23:23+3])

            if practice("red_rabbit.png"):
                break
            else:
                showExplanation(explaning[26:26+2])
                if i != 3:
                    showExplanation(explaning[25])

    except PassException as e: 
        window.load_state()

    showExplanation(explaning[28])
    game(2, answer)

    # yellow_truck green_flower
    # 테두리 -> 색깔,  일반 -> 모양
    answer = {
        "yellow_flower_square.png": 'left',
        "green_truck_square.png": 'right',
        "yellow_flower.png": 'right',
        "green_truck.png": 'left'
    }
    window.save_state()
    try:
        showExplanation(explaning[29:29+14])
        if not practice("yellow_flower_square.png"):
            showExplanation(explaning[44:44+3])

        if not practice("green_truck_square.png"):
            showExplanation(explaning[47:47+2])
            showExplanation(explaning[46])

        if not practice("yellow_flower.png"):
            showExplanation(explaning[51:51+2])
            showExplanation(explaning[46])

        if practice("green_truck.png"):
            showExplanation(explaning[43])
        else:
            showExplanation(explaning[49:49+2])
            showExplanation(explaning[46])


        for i in range(0,3):
            if not practice("green_truck_square.png"):
                showExplanation(explaning[47:47+2])
                showExplanation(explaning[46])

            if not practice("yellow_flower.png"):
                showExplanation(explaning[51:51+2])
                showExplanation(explaning[46])

            if not practice("green_truck.png"):
                showExplanation(explaning[49:49+2])
                showExplanation(explaning[46])

            if practice("yellow_flower_square.png"):
                break
            else:
                showExplanation(explaning[44:44+2])
                if i != 2:
                    showExplanation(explaning[46])

    except PassException as e: 
        window.load_state()
    showExplanation(explaning[53])
    game(3, answer)