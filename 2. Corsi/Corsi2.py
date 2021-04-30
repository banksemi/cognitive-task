# -*- coding: utf-8 -*-
# Imports
from psychopy import visual, core, event, gui
# Import analyze_log
import random

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


# 화면에 넣기

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
win = visual.Window([255*4.5, 205*4.5], allowGUI=True, fullscr=False, waitBlanking=True, monitor='testMonitor', units='deg') # Create window
#응답 설정: 마우스로 클릭

mouse=event.Mouse(visible=True,win=win)

#상자 크기 (단위는 pixel)
box_size=3

#상자 위치 (총 9개 제시)
# box_positions = [[-26, -102], [98, -104], [-118, -63], [74, -28], [-45, -23], [-135, 31], [134, 44], [54, 92], [-11, 38]]
box_positions = [[40,150], [-150, 110], [140,100], [-80, 35], [40,0], [155, -50], [-170, -100], [-70, -130], [30, -115]]



#상자 자극 설정
#class psychopy.visual.Rect(win, width=0.5, height=0.5, **kwargs)
boxes = [visual.Rect(win, pos=[box_pos[0]/15, box_pos[1]/15], width=box_size, height=box_size) for box_pos in box_positions]

#'선택 완료' 버튼 박스
exit_box = visual.Rect(win, pos=[0,-10], width=3, height=1)
# '선택 완료'라는 텍스트의 위치 (버튼 박스 내)
exit_text = visual.TextStim(win, pos = [0,-10], text = _('exit'))

# Open log file to write
# 기록 파일 이름
file_name = exp_info['participant']+'_corsi.csv'
log_file = open(file_name, 'a')
#기록 파일 내 포함될 변인과 헤드 이름
log_file.write('participant, series, responses, errors\n') # Heading

# Instruction
text_instruction = visual.TextStim(win, wrapWidth= 30, pos=[0,0], text=_('instr')) # Text object
text_instruction.draw()
win.flip()
event.waitKeys()

#Experiment
def draw_boxes(colors):
    for box, color in zip(boxes, colors):
        box.setFillColor(color)
        box.draw()

test_i = -1
#test_series 배열 중 첫 번째 배열부터 시작
error_n = 0
#오류 수도 디폴트 값이 0
max_n = 0
#최대 값(점수)도 디폴트 값이 0

err_sum=0

while True:
    count = 0
    if err_sum==2:
        break
    err_sum=0
    test_i += 1 #박스 개수 증가 + alpha

    if test_i==8:
        break

    while(count<2):

        # #깜빡임 갯수와 순서 지정
        #
        # #중복 허용 x
        box_list = []
        box_random = random.randint(0,8)
        for i in range(test_i+2):
            while box_random in box_list:
                box_random = random.randint(0,8)
            box_list.append(box_random)

        # Present the series
        #시퀀스 제시
        mouse.setVisible(False)
        draw_boxes(['green']*len(boxes))
        win.flip()
        core.wait(1)

        for item in box_list:
            colors = ['green']*len(boxes)
            colors[item] = 'white'
            draw_boxes(colors)
            win.flip()
            core.wait(1)

            colors = ['green']*len(boxes)
            draw_boxes(colors)
            win.flip()
            core.wait(0.2)

        # Participant chooses boxes
        # 이제 참여자가 응답을 할 차례
        mouse.setVisible(True)
        colors = ['green']*len(boxes)
        draw_boxes(colors)
        exit_box.draw() #완료버튼 제시
        exit_text.draw() #'완료'텍스트 제시
        win.flip()
        responses = [] #빈 응답에서 append를 통해 축척
        while True:
            if sum(mouse.getPressed()):
                box_pressed = [box.contains(mouse.getPos()) for box in boxes]
                if sum(box_pressed):
                    colors[box_pressed.index(True)] = 'white'

                    draw_boxes(colors)
                    exit_box.draw()
                    exit_text.draw()
                    win.flip()
                    core.wait(0.2)

                    colors = ['green']*len(boxes)
                    draw_boxes(colors)  
                    exit_box.draw()
                    exit_text.draw()
                    win.flip()

                    if not (box_pressed.index(True) in responses):
                        responses.append(box_pressed.index(True))
                draw_boxes(colors)
                exit_box.draw()
                exit_text.draw()
                win.flip()

                if exit_box.contains(mouse.getPos()):
                    break
        win.flip()
        core.wait(1)
        errors = [int(i!=j) for i, j in zip(box_list, responses)]
        log_file.write('"%s", task, %s, %s, %s\n' %(exp_info['participant'], box_list, responses, errors))
        if errors == []: errors = [1] #전혀 값이 없을 때
        if sum(errors):
            err_sum += 1

        count = count+1

win.flip()
