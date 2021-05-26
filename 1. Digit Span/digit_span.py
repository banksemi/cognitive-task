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

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common_seung import *


participant_id = inputParticipant()
win, window = initWindow()

audio_image = drawling_image(0, 0, "./제시화면/audio.png", height=0.5) 
window.append(audio_image)

speak_image = drawling_image(0, 0, "./제시화면/speak.jpg", height=0.5) 
window.append(speak_image)

# 사전 정의된 stimulus
stimulus_set = []
result = pyresult(participant_id, 'Digit Span')

block_span = 0

input_text = drawling_text(0, -0.49, "INPUT_TEXT", [0,0,0], height = 0.01) # Text object
window.append(input_text)

def trial(stimulus):
    trial_result = {}
    audio_image.setVisible(True);
    speak_image.setVisible(False);
    window.update_wait_time(1)

    for index in stimulus:
        winsound.PlaySound("./음성/%d.wav" % index, winsound.SND_FILENAME)

        window.update_wait_time(0.3)


    # 비프음으로 인한 지연시간 제거
    t = threading.Thread(target=lambda: winsound.Beep(880,500)).start()
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
            
        input_text.setText(''.join(['*'] * len(responses)))
        
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


for trial_i in range(0, 8):
    corrects = []
    for trial_j in [0, 1]:
        trial_index = trial_i * 2 + trial_j
        stimulus = json.loads(result.read('trial_stimulus', trial_index))
        trial_result = trial(stimulus)
        for i in trial_result:
            result.write(i, trial_result[i], index=trial_index)

        corrects.append(trial_result['trial_correct'])
        
    if sum(corrects) == 0:
        for i in range(trial_i+1, 8):
            for j in [0, 1]:
                result.write('trial_response', ['stop'], index=i * 2 + j)
                result.write('trial_correct', 0, index=i * 2 + j)
                result.write('trial_score', 0, index=i * 2 + j)
        break
        
    if sum(corrects) == 2: # 2번 모두 성공
        block_span = trial_i + 2
        
result.write('block_span', block_span)

result.save()
result.close()