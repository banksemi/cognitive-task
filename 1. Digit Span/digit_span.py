# -*- coding: utf-8 -*-
# Imports
from psychopy import visual, core, event, gui
from datetime import datetime, timedelta
from psychopy import iohub

# Import analyze_log
import random
import openpyxl
import os  
import json
import winsound
import threading
import winsound
import random

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common_seung import *


participant_info = inputParticipant('Digit Span')
win, window = initWindow()

audio_image = drawling_image(0, 0, "./제시화면/audio.png", height=0.8) 
window.append(audio_image)

speak_image = drawling_image(0, 0, "./제시화면/speak.png", height=0.8) 
window.append(speak_image)

input_text = drawling_text(0.8-0.1, -0.45, "", [0,0,0], height = 0.035) # Text object
window.append(input_text)

def trial(stimulus, input_show = False):
    trial_result = {}
    audio_image.setVisible(True);
    speak_image.setVisible(False);
    input_text.setText("")
    window.update_wait_time(1)

    for i, index in enumerate(stimulus):
        app  = ''
        if i == len(stimulus) - 1:
            app = "_저음"
        winsound.PlaySound("./음성/%d%s.wav" % (index, app), winsound.SND_FILENAME)

        window.update_wait_time(0.7)


    # 비프음으로 인한 지연시간 제거
    t = threading.Thread(target=lambda: winsound.Beep(600,500)).start()
    audio_image.setVisible(False);
    speak_image.setVisible(True);

    responses = []
    start = datetime.now()
    last_block_clicked = start

    while True:
        window.update()
        for j in range(1, 10):
            if window.getPressKey("num_" + str(j)):
                responses.append(j)
                last_block_clicked = datetime.now()

        if window.getPressKey('backspace'):
            responses = responses[0: len(responses) - 1]

        if window.getPressKey('num_enter') or window.getPressKey('return') or (datetime.now() - last_block_clicked).total_seconds() > 15:
            break
            
        input_text.setText(''.join([str(i) for i in responses]))
        if len(responses) == 0 and input_show == True:
            input_text.setText("INPUT")
        
    if len(responses) < len(stimulus):
        responses.append(0)
            
        
    correct = 1 if (stimulus == responses) else 0
    score = 0
    for i in zip(stimulus, responses):
        if i[0] == i[1]:
            score += 1

       
    trial_result['trial_response'] = responses
    trial_result['trial_correct'] = correct
    trial_result['trial_score'] = score
    return trial_result

def exit_event(message='stop'):
    for i in range(trial_index, 8*2):
        result.write('trial_response', [message], index=i)
        result.write('trial_correct', 0, index=i)
        result.write('trial_score', 0, index=i)
    result.save()
    result.close()

task_type = getTaskType()

explaning = ['./튜토리얼/Digit Span(%s)_T%d.PNG' % (task_type, i) for i in range(0,30)]
result = pyresult(participant_info, 'Digit Span', task_type)
block_span = 0

if task_type == 'A':
    window.save_state()
    practice_count = 0
    try:
        showExplanation(explaning[1:1+4])
        for i in range(0,3):
            practice_count += 1
            trial_result = trial([3,5])
            if trial_result['trial_correct'] == 1:
                showExplanation(explaning[5])
            else:
                showExplanation(explaning[6])

            trial_result = trial([9,4])
            if trial_result['trial_correct'] == 1:
                practice_count = 0 # 실패 카운트 초기화 후 본시행 시작
                break
            else:
                if practice_count != 3:
                    showExplanation(explaning[7])
    except PassException as e: 
        window.load_state()

    if practice_count == 3:
        showExplanation(explaning[9])
    else:
        showExplanation(explaning[8])
elif task_type == 'B':
    showExplanation(explaning[1:1+3])
    random.seed(445) # B 과제 본시행을 위한 시드값 고정
window.event_listener_exit.append(lambda: exit_event('esc'))

for trial_i in range(0, 8):
    for trial_j in [0, 1]:
        trial_index = trial_i * 2 + trial_j
        stimulus = list(range(1,10))
        while True:
            random.shuffle(stimulus)
            if not stimulus[trial_i + 2 - 1] == 6:
                break
        stimulus = stimulus[0:trial_i+2]
        result.write('trial_stimulus', stimulus, index=trial_index)


for trial_i in range(0, 8):
    corrects = []
    for trial_j in [0, 1]:
        trial_index = trial_i * 2 + trial_j
        stimulus = json.loads(result.read('trial_stimulus', trial_index))
        trial_result = trial(stimulus)
        for i in trial_result:
            result.write(i, trial_result[i], index=trial_index)

        corrects.append(trial_result['trial_correct'])
        result.save()
        
    if sum(corrects) == 0:
        trial_index += 1
        exit_event('stop')
        break
        
    if sum(corrects) == 2: # 2번 모두 성공
        block_span = trial_i + 2
        result.write('block_span', block_span)
    result.save()

result.save()
result.close()