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

# background_color = [0,0,0]
# block_color = [64, 71, 202]
# with pyresult('승화','Corsi') as result:
#    result.write('total_score', 6)

# #안내문 내용
texts = {
    'instr':
        {'kor':"지금부터 화면에 9개의 블록이 나옵니다. 블록이 깜박이는 순서를 잘 기억했다가 나타난 순서대로 블록을 눌러주세요. 다 누른 후에는 완료버튼을 누릅니다. 준비됐다면 space bar를 눌러 시작합니다."},
    'exit':
        {'kor': '완료'}
}


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
            
####################################################################################
# 안내문
# Language specific components
def _(string):
    # You should use texts dictionary to strore the strings, and set exp_info['language'] to specify the language
    return texts[string]['kor']

participant_info = inputParticipant()
win, window = initWindow()

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

# Instruction
'''
text_instruction = drawling_object(visual.TextStim(win, wrapWidth=30, pos=[0,0], text=_('instr'))) # Text object
window.append(text_instruction)
window.update_wait_key()
window.remove(text_instruction)

'''

boxes = []
for box_pos in box_positions:
    box = drawling_box(box_pos[0], box_pos[1], box_size, color=block_color) # 0,180,0
    boxes.append(box)
    window.append(box)

    
exit_box = drawling_image(+0.65, -0.35, "ok2.png", height=0.20) 
window.append(exit_box)

# 사전 정의된 stimulus
stimulus_set = []
result = pyresult(participant_info, 'Corsi')


def trial(stimulus):
    trial_result = {}
    # 시퀀스 제시
    window.mouse.setVisible(False)
    exit_box.setVisible(False)
        
    window.update_wait_time(1)

    for index in stimulus:
        boxes[index-1].setWhiteColor(1)
        window.update_wait_time(1)
        window.update_wait_time(0.2)

    window.mouse.setVisible(True)
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
                        
        if window.isClickedObject(exit_box) or window.getPressKey('space') or (datetime.now() - last_block_clicked).total_seconds() > 15:
            break
        
    if len(responses) < len(stimulus):
        responses.append(0)
    
    correct = 1 if (stimulus == responses) else 0
    score = 0
    for i in zip(stimulus, responses):
        if i[0] == i[1]:
            score += 1

    trial_result['trial_response'] = responses;
    trial_result['trial_reaction_time1'] = (last_block_clicked-start).total_seconds();
    trial_result['trial_reaction_time2'] = (datetime.now()-start).total_seconds();
    trial_result['trial_correct'] = correct
    trial_result['trial_score'] = score
    return trial_result

block_span = 0
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

result.save()
result.close()