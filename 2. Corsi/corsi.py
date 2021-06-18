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

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common_seung import *

# 모니터 크기에 따라 블럭 사이즈 변경
alpha = 0.98 # 세로 해상도에 맞춰짐
background_color = [255,255,255]
block_color = [0,180,0]

# custom 객체 사전 정의
class drawling_box(drawling_object):
    i_effect = 0
    i_opacity_wait = datetime.now()
    def __init__(self, x, y, box_size, color):
        self.box = visual.Rect(win, pos=[x, y], width=box_size, height=box_size)
        self.color = color
        super().__init__(self.box)
        line = 2 * 2 / win.size[1]
        self.box_outline = visual.Rect(win, pos=[x, y], width=box_size+line, height=box_size+line)
        self.box_outline.setFillColor('black')
        
    def setWhiteColor(self, time, effect=False):
        if effect:
            self.i_effect = 15
        self.i_opacity_wait = datetime.now() + timedelta(seconds=time) 
        
    def draw(self):
        self.box_outline.draw()
        self.box.draw()
    
    def update(self):
        color1 = self.color
        color2 = [254,202,3]
        if (datetime.now() - self.i_opacity_wait).total_seconds() > 0:
            if self.i_effect > 0:
                self.i_effect -= 1
                
            mix_i = 1 - self.i_effect / 15.0
            mixed = [color1[i] * mix_i + color2[i] * (1 - mix_i) for i in range(0,3)]
            self.box.setFillColor(mixed, colorSpace='rgb255')
        else:
            self.box.setFillColor(color2, colorSpace='rgb255')

class drawling_image_easily_clickable(drawling_image):
    def __init__(self, *numbers, **params):
        super().__init__(*numbers, **params)
        self.clickableobject = visual.Rect(win, pos=[self.x, self.y], width=self.width * 1.65, height=self.height * 1.8)
    def contains(self, pos):
        return self.clickableobject.contains(pos)      
####################################################################################

participant_info = inputParticipant('Corsi')
win, window = initWindow()

if len(sys.argv) > 2 and sys.argv[2] == 'touch':
    window.mouse.touch_is_working = False

back = drawling_box(0, 0, 200, color=background_color)
back.z = -999
window.append(back)


#상자 크기 (단위는 pixel)
box_size=30

#상자 위치 (총 9개 제시)
box_positions = [[130,155], [30, 145], [180,120], [70, 110], [140, 90], [195, 60], [15, 50], [75,20], [135, 30]]

# box 매핑 
box_positions = [[i[0]+15, i[1]+15] for i in box_positions]

box_positions = [[i[0] - (255/2), i[1] - (205/2)] for i in box_positions]

# 0~205 비율을 0~1 비율로 수정
box_positions = [[i[0] / 205, i[1] / 205] for i in box_positions]
box_size /= 205

box_positions = [[i[0] * alpha, i[1] * alpha] for i in box_positions]
box_size *= alpha


boxes = []
for box_pos in box_positions:
    box = drawling_box(box_pos[0], box_pos[1], box_size, color=block_color) # 0,180,0
    boxes.append(box)
    window.append(box)

exit_box = drawling_image_easily_clickable(+0.70, -0.35, "ok.png", height=0.20) 
exit_box.setVisible(False)
window.append(exit_box)

def trial(stimulus, only_show=False):
    trial_result = {}
    # 시퀀스 제시
    window.mouse.setVisible(False)
        
    window.update_wait_time(1)

    for index in stimulus:
        boxes[index-1].setWhiteColor(1)
        window.update_wait_time(1)
        window.update_wait_time(0.2)

    window.mouse.setVisible(True)
    if only_show:
        return
    
    exit_box.setVisible(True)
    # 비프음으로 인한 지연시간 제거
    t = threading.Thread(target=lambda: winsound.Beep(580,500)).start()

    responses = []
    start = datetime.now()
    last_block_clicked = start
    while True:
        window.update()
        for i, box in enumerate(boxes):
            if window.isClickedObject(box):
                box.setWhiteColor(0.2, effect=True)


                responses.append(i+1)
                last_block_clicked = datetime.now()
                        
        if window.isClickedObject(exit_box) or window.getPressKey('space'):
            break
        if (datetime.now() - last_block_clicked).total_seconds() > 10:
            trial_result['nosave_timeout'] = True;
            break
        
    if len(responses) < len(stimulus):
        responses.append(0)
    
    correct = 1 if (stimulus == responses) else 0
    score = 0
    for i in zip(stimulus, responses):
        if i[0] == i[1]:
            score += 1

    exit_box.setVisible(False)
    trial_result['trial_response'] = responses;
    trial_result['trial_reaction_time1'] = (last_block_clicked-start).total_seconds();
    trial_result['trial_reaction_time2'] = (datetime.now()-start).total_seconds();
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
explaning = ['./튜토리얼/Corsi Block(%s)_T%d.PNG' % (task_type, i) for i in range(0,30)]
result = pyresult(participant_info, 'Corsi', task_type)
if task_type == 'A':
    window.save_state()
    try:
        showExplanation(explaning[1:1+7])
        
        for practice_count in range(0,3):
            for b in range(0,3):
                trial_result = trial([4,5])
                if 'nosave_timeout' in trial_result and b != 2: # 무응답
                    showExplanation(explaning[9:9+1])
                    continue
                elif trial_result['trial_correct'] == 0 or b == 2: # 오답
                    showExplanation(explaning[10])
                    trial([4,5], only_show = True)
                    showExplanation(explaning[11:11+3])
                else: # 정답
                    showExplanation(explaning[8])
                break
            trial_result = trial([8, 6])
            if trial_result['trial_correct'] == 1: # 정답
                break
            else:
                showExplanation(explaning[14])
                trial([8, 6], only_show = True)
                showExplanation(explaning[15:15+2])
                if practice_count != 2:
                    showExplanation(explaning[17])

                continue
    except PassException as e: 
        window.load_state()
    finally:
        window.reset_state()

    showExplanation(explaning[18])
if task_type == 'B':
    window.save_state()
    try:
        showExplanation(explaning[1:1+3])
    except PassException as e: 
        window.load_state()
    finally:
        window.reset_state()

# 본시행
window.event_listener_exit.append(lambda: exit_event('esc'))
block_span = 0

for trial_i in range(0, 8):
    for trial_j in [0, 1]:
        trial_index = trial_i * 2 + trial_j
        stimulus = list(range(1,10))
        random.shuffle(stimulus)
        stimulus = stimulus[0:trial_i+2]
        result.write('trial_stimulus', stimulus, index=trial_index)
result.save()

trial_index = 0
for trial_i in range(0, 8):
    corrects = []
    for trial_j in [0, 1]:
        trial_index = trial_i * 2 + trial_j
        stimulus = json.loads(result.read('trial_stimulus', trial_index))

        trial_result = trial(stimulus)
        window.force_refresh() # 화면을 먼저 갱신
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

window.exit()