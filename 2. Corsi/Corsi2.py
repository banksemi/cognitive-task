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

# #안내문 내용
texts = {
    'instr':
        {'kor':"지금부터 화면에 9개의 블록이 나옵니다. 블록이 깜박이는 순서를 잘 기억했다가 나타난 순서대로 블록을 눌러주세요. 다 누른 후에는 완료버튼을 누릅니다. 준비됐다면 space bar를 눌러 시작합니다."},
    'exit':
        {'kor': '완료'}
}

#참여자 ID 윈도우
exp_info = {'participant':'participant_ID',
}  # default parameters of the experiment

####################################################################################
# 액셀 입출력을 위한 클래스
class pyresult:
    value_table = {
        'Corsi': {
            'total_score': ['B', 2],
            'block_span': ['C', 2],
            
            'trial_stimulus': ['B', 5],
            'trial_response': ['C', 5],
            'trial_reaction_time': ['D', 5],
            'trial_correct': ['E', 5],
        }
    }
    
    def __init__(self, participant_id, test_name):
        self.test_name = test_name
        self.output_path = '../output/' + participant_id + '.xlsx'
        if os.path.isfile(self.output_path):
            self.workbook = openpyxl.load_workbook(self.output_path)
        else:
            self.workbook = openpyxl.load_workbook('../CBT_result.xlsx')
        self.worksheet = self.workbook[self.test_name]
        
    def write(self, name, value, index=0):
        position = self.value_table[self.test_name][name]
        if isinstance(value, list):
            value = str(value)
        self.worksheet[position[0] + str(position[1] + index)] = value
    
    def read(self, name, index=0):
        position = self.value_table[self.test_name][name]
        return self.worksheet[position[0] + str(position[1] + index)].value
        
    def save(self):
        self.workbook.save(self.output_path)
        
    def close(self):
        self.workbook.close()
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.save()
        self.close()

# 객체 및 입력 이벤트 관리를 위한 Common Module 정의
class drawling_object:
    z = 0
    visible = True
    def __init__(self, dobject):
        self.dobject = dobject
        
    def setVisible(self, value):
        self.visible = value
        
    def draw(self):
        self.dobject.draw()
        
    def contains(self, pos):
        return self.dobject.contains(pos)
        
    def update(self):
        return
        
class window_manager:
    dobjects = []
    input_keys = []
    def __init__(self, win):
        self.win = win
        self.mouse=psycopy_mouse(visible=True,win=win)
    
    def append(self, dobject):
        self.dobjects.append(dobject)
        
    def remove(self, dobject):
        self.dobjects.remove(dobject)
    
    def getPressKey(self, key):
        for i in self.input_keys:
            if i == key:
                return True
        return False
        
    def update(self):
        self.mouse.update()
        self.win.update()
        self.input_keys = event.getKeys()
        if self.getPressKey('escape'):
            self.win.close()
            core.quit()
        for i in self.dobjects:
            i.update()
            if i.visible:
                i.draw()
            
    def update_wait_key(self):
        while True:
            self.update()
            if len(self.input_keys) > 0:
                return
                
    def update_wait_time(self, seconds=1):
        start_time = datetime.now()
        while (datetime.now() - start_time).total_seconds() < seconds:
            self.update()
            
    def isClickedObject(self, dobject):
        return self.mouse.getClicked() and dobject.contains(self.mouse.getPos())
            
# 터치스크린 문제를 해결하기 위해 mouse 객체 재정의
# 기존 window를 이용하는 mouse 객체와, ioHub로 얻은 mouse 객체를 함께 사용
class psycopy_mouse:
    def __init__(self, win, io=None, visible=None):
        self.win_mouse=event.Mouse(visible=True,win=win)
        if io is None:
            io = iohub.launchHubServer()
        self.io_mouse = io.devices.mouse
        self.clear()
        
        if visible is not None:
            self.setVisible(visible)
            
    def clear(self):
        self.io_mouse.clearEvents() # 이미 쌓여있는 이벤트는 초기화
        self.pressed = False
        self.clicked = False
        
    def setVisible(self, value):
        self.win_mouse.setVisible(value)
        
    def getClicked(self):
        return self.clicked
        
    def getPos(self):
        return self.win_mouse.getPos()
        
    def update(self):
        self.clicked = False # 클릭 초기화
        events = self.io_mouse.getEvents(event_type=(iohub.constants.EventConstants.MOUSE_BUTTON_PRESS))
        
        for e in events:
            if self.pressed == False:
                self.clicked = True
            self.pressed = True
        
        # release 신호 처리
        events = self.io_mouse.getEvents(event_type=(iohub.constants.EventConstants.MOUSE_BUTTON_RELEASE))
        for e in events:
            self.pressed = False
####################################################################################
# custom 객체 사전 정의
class drawling_box(drawling_object):
    i_effect = 0
    i_opacity_wait = datetime.now()
    def __init__(self, x, y, box_size, color):
        self.box = visual.Rect(win, pos=[x, y], width=box_size, height=box_size)
        self.color = color
        super().__init__(self.box)
        line = 0.14
        self.box_outline = visual.Rect(win, pos=[x, y], width=box_size+line, height=box_size+line)
        self.box_outline.setFillColor('black')
        
    def setWhiteColor(self, time, effect=False):
        if effect:
            self.i_effect = 15
        self.i_opacity_wait = datetime.now() + timedelta(seconds=time) 
        
    def draw(self):
        # self.box_outline.draw()
        self.box.draw()
    
    def update(self):
        color1 = self.color
        color2 = [255,255,255]
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

# Setting some parameters on GUI
dlg = gui.DlgFromDict(exp_info, title='Corsi Test',
   order = ['participant'],
    tip = {'participant':'Identifier of the participant.',})
if not dlg.OK:
    print ('User Cancelled')
    core.quit()

#윈도우
win = visual.Window([255*4.5, 205*4.5], allowGUI=True, fullscr=False, waitBlanking=True, monitor='testMonitor', units='deg')
window = window_manager(win)
#상자 크기 (단위는 pixel)
box_size=3

#상자 위치 (총 9개 제시)
# box_positions = [[-26, -102], [98, -104], [-118, -63], [74, -28], [-45, -23], [-135, 31], [134, 44], [54, 92], [-11, 38]]
box_positions = [[40,150], [-150, 110], [140,100], [-80, 35], [40,0], [155, -50], [-170, -100], [-70, -130], [30, -115]]

# Open log file to write
# 기록 파일 이름
file_name = exp_info['participant']+'_corsi.csv'
log_file = open(file_name, 'a')
#기록 파일 내 포함될 변인과 헤드 이름
log_file.write('participant, series, responses, errors\n') # Heading

# Instruction
text_instruction = drawling_object(visual.TextStim(win, wrapWidth=30, pos=[0,0], text=_('instr'))) # Text object
window.append(text_instruction)
window.update_wait_key()
window.remove(text_instruction)
        
boxes = []
for box_pos in box_positions:
    box = drawling_box(box_pos[0]/15, box_pos[1]/15, box_size, color=[0,180,0])
    boxes.append(box)
    window.append(box)

#'선택 완료' 버튼 박스
exit_box = drawling_object(visual.Rect(win, pos=[0,-10], width=3, height=1))
window.append(exit_box)

# '선택 완료'라는 텍스트의 위치 (버튼 박스 내)
exit_text = drawling_object(visual.TextStim(win, pos = [0,-10], text = _('exit')))
window.append(exit_text)

# 사전 정의된 stimulus
stimulus_set = []
result = pyresult(exp_info['participant'], 'Corsi')

block_span = 0
for trial_i in range(0, 7):
    corrects = []
    for trial_j in [0, 1]:
        trial_index = trial_i * 2 + trial_j
        stimulus = json.loads(result.read('trial_stimulus', trial_index))
        
        #시퀀스 제시
        window.mouse.setVisible(False)
        exit_box.setVisible(False)
        exit_text.setVisible(False)
        
        window.update_wait_time(1)

        for index in stimulus:
            boxes[index-1].setWhiteColor(1)
            window.update_wait_time(1)
            
            window.update_wait_time(0.2)

        # Participant chooses boxes
        # 이제 참여자가 응답을 할 차례
        window.mouse.setVisible(True)
        exit_box.setVisible(True)
        exit_text.setVisible(True)
        
        responses = []
        start = datetime.now()
        while True:
            window.update()
            for i, box in enumerate(boxes):
                if window.isClickedObject(box):
                    box.setWhiteColor(0.2, effect=True)

                    if not (i+1 in responses):
                        responses.append(i+1)
                        
            if window.isClickedObject(exit_box):
                break
        
        result.write('trial_response', responses, index=trial_index)
        result.write('trial_reaction_time', (datetime.now()-start).total_seconds(), index=trial_index)
        
        
        correct = 1 if (stimulus == responses) else 0
        corrects.append(correct)
        result.write('trial_correct', correct, index=trial_index)
    
    if sum(corrects) == 0:
        break
    if sum(corrects) == 2: # 2번 모두 성공
        block_span = trial_i + 2
        
result.write('block_span', block_span)

result.save()
result.close()