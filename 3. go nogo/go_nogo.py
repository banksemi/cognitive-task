#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from psychopy import visual, core, event, gui
import random
import winsound
from psychopy.tools import filetools
import numpy as np
import pandas as pd 

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common_seung import *

task_type = getTaskType()
explaning = ['./튜토리얼/Go, No-Go(%s)_T%d.PNG' % (task_type, i) for i in range(0,30)]

image_path = "./이미지/" + task_type + '과제'

go_image_list = []
nogo_image_list = []
for i in os.listdir(image_path):
    if i.startswith('nogo'):
        nogo_image_list.append(os.path.join(image_path, i))
    else:
        go_image_list.append(os.path.join(image_path, i))

last = None
orders = []
for i in range(0,5):
    image_list = go_image_list + nogo_image_list * 2

    while True:
        random.shuffle(image_list)
        # 연속해서 같은 이미지가 있는 경우 다시 섞기
        reshuffle = False
        for j in range(0, len(image_list)-1):
            if image_list[j] == image_list[j+1]:
                reshuffle = True
        if reshuffle:
            continue
        if image_list[0] != last:
            last = image_list[-1]
            orders.extend(image_list)
            break

participant_info = inputParticipant('Go, No-Go')
win, window = initWindow()
result = pyresult(participant_info, 'Go, No-Go', task_type)

# 이미지 캐싱
images = {}
for i in set(orders):
    images[i] = drawling_image(0, 0, i, height=1)
    images[i].setVisible(False)
    window.append(images[i])


def trial(image_name, timeout=1):
    trial_result = {}
    images[image_name].setVisible(True)
    go = not(os.path.basename(image_name).startswith('nogo')) # 정답 설정
    
    start = datetime.now()
    while True:
        window.update()
        time = (datetime.now()-start).total_seconds()
        
        response_go = 'None'
        if window.getPressKey('space') or window.mouse.getClicked():
            response_go = True

        if time >= timeout:
            response_go = False
            
        if response_go != 'None':
            trial_result['trial_stimulus'] = 'Go' if go else 'NoGo'
            trial_result['trial_response'] = 'Go' if response_go else 'NoGo'

            if go:
                trial_result['trial_correct'] = 'Y' if go == response_go else 'N'
            else:
                trial_result['trial_correct'] = '1' if go == response_go else '0'
                
            if response_go:
                trial_result['trial_reaction_time'] = time
            break
    images[image_name].setVisible(False)
    return trial_result

# 연습 시행 루틴
window.save_state()
try:
    # 1번 이미지부터 순서대로 5장 튜토리얼 출력
    showExplanation(explaning[1:1+5])
    # 첫번째 연습 시행 (5 Go, 1 No-Go)
    success = True

    # 5장의 Go Task
    for i in go_image_list[0:5]:
        trial_result = trial(i, timeout=3)
        if trial_result['trial_response'] == 'NoGo': # Nogo 반응인 경우
            showExplanation(explaning[7]) # 7번 슬라이드 실행
            success = False

    # 1장의 NoGo Task
    trial_result = trial(nogo_image_list[0], timeout=2)
    if trial_result['trial_response'] == 'Go': # Go 반응인 경우
        showExplanation(explaning[8])
        success = False

    # 연습시행 1에 대한 결과 표시
    if success:
        showExplanation(explaning[6])
    else:
        showExplanation(explaning[9])

    # 두번째 연습 시행 (3 Go, 1 No-Go, 2 Go)
    # 만약 한번이라도 틀리면 연습시행 3으로...
    go_count = 5
    nogo_count = 2
    # 3장의 Go Task (5번째부터 연속된 3장)
    for i in go_image_list[5:5+3]:
        trial_result = trial(i, timeout=3)
        if trial_result['trial_response'] == 'NoGo':
            go_count -= 1
            showExplanation(explaning[7])

    # 1장의 NoGo Task
    trial_result = trial(nogo_image_list[0], timeout=2)
    if trial_result['trial_response'] == 'Go':
        nogo_count -= 1
        showExplanation(explaning[8])

    # 2장의 Go Task
    for i in go_image_list[3:3+2]:
        trial_result = trial(i, timeout=3)
        if trial_result['trial_response'] == 'NoGo':
            go_count -= 1
            showExplanation(explaning[7])

    # 1장의 NoGo Task
    trial_result = trial(nogo_image_list[0], timeout=2)
    if trial_result['trial_response'] == 'Go':
        nogo_count -= 1
        showExplanation(explaning[8])

    if go_count < 3 or nogo_count == 0: # 연습시행 2를 한번이라도 틀렸으면
        # 세번째 연습시행 (1 Go, 1 No-Go, 2 Go, 1 No-Go, 1 Go)
        showExplanation(explaning[9])

        # 1장의 Go Task
        for i in go_image_list[0:1]:
            trial_result = trial(i, timeout=3)
            if trial_result['trial_response'] == 'NoGo':
                showExplanation(explaning[7])

        # 1장의 NoGo Task
        for i in nogo_image_list * 1:
            trial_result = trial(i, timeout=2)
            if trial_result['trial_response'] == 'Go':
                showExplanation(explaning[8])

        # 2장의 Go Task (0번째부터 연속된 2장)
        for i in go_image_list[1:1+2]:
            trial_result = trial(i, timeout=3)
            if trial_result['trial_response'] == 'NoGo':
                showExplanation(explaning[7])

        # 1장의 NoGo Task
        for i in nogo_image_list * 1:
            trial_result = trial(i, timeout=2)
            if trial_result['trial_response'] == 'Go':
                showExplanation(explaning[8])

        # 1장의 Go Task
        for i in go_image_list[0:1]:
            trial_result = trial(i, timeout=3)
            if trial_result['trial_response'] == 'NoGo':
                showExplanation(explaning[7])

except PassException as e: 
    window.load_state()

# 본 시행 시작 피드백
showExplanation(explaning[10])

# 본 시행
score = 0
inhibition = 0
go_reaction_time = []
nogo_reaction_time = []

for trial_index, image_name in enumerate(orders):
    trial_result = trial(image_name)
    for i in trial_result:
        result.write(i, trial_result[i], index=trial_index)

    if trial_result['trial_stimulus'] == 'Go' and trial_result['trial_response'] == 'Go':
        score += 1
    if trial_result['trial_stimulus'] == 'NoGo' and trial_result['trial_response'] == 'NoGo':
        inhibition += 1
    if trial_result['trial_response'] == 'Go':
        if trial_result['trial_stimulus'] == 'Go':
            go_reaction_time.append(trial_result['trial_reaction_time'])
        else:
            nogo_reaction_time.append(trial_result['trial_reaction_time'])
    
    result.save()
    
result.write('inhibition', inhibition)
result.write('score', score)
if len(go_reaction_time) > 0:
    result.write('go_reaction_time', np.array(go_reaction_time).mean())
        
if len(nogo_reaction_time) > 0:
    result.write('nogo_reaction_time', np.array(nogo_reaction_time).mean())
result.save()
result.close()
                
