from psychopy import visual, core, event, gui
from datetime import datetime, timedelta
from psychopy import iohub

# Import analyze_log
import random
import openpyxl
import os  
import json

from PIL import Image

####################################################################################
# 액셀 입출력을 위한 클래스
class pyresult:
    value_table = {
        'Digit Span': {
            'block_span': ['D', 2],
            
            'trial_stimulus': ['B', 5],
            'trial_response': ['C', 5],
            'trial_correct': ['D', 5],
            'trial_score': ['E', 5],
        },
        'Corsi': {
            'block_span': ['D', 2],
            
            'trial_stimulus': ['B', 5],
            'trial_response': ['C', 5],
            'trial_reaction_time1': ['D', 5],
            'trial_reaction_time2': ['E', 5],
            'trial_correct': ['F', 5],
            'trial_score': ['G', 5],
        },
        'Go, No-Go': {
            'inhibition': ['B', 2],
            'score': ['C', 2],
            'go_reaction_time': ['F', 2],
            'nogo_reaction_time': ['G', 2],
            
            'trial_stimulus': ['B', 5],
            'trial_response': ['C', 5],
            'trial_correct': ['D', 5],
            'trial_reaction_time': ['E', 5],
        },
        'DCCS': {
            'trial1_score': ['C', 2],
            'trial1_reaction_time': ['D', 2],
            'trial1_reaction_time_correct': ['E', 2],
            'trial1_each_response': ['C', 5],
            'trial1_each_correct': ['D', 5],
            'trial1_each_time': ['E', 5],
            
            
            'trial2_score': ['F', 2],
            'trial2_reaction_time': ['G', 2],
            'trial2_reaction_time_correct': ['H', 2],
            'trial2_each_response': ['C', 17],
            'trial2_each_correct': ['D', 17],
            'trial2_each_time': ['E', 17],
            
            
            'trial3_score': ['I', 2],
            'trial3_reaction_time': ['J', 2],
            'trial3_reaction_time_correct': ['K', 2],
            'trial3_each_response': ['C', 29],
            'trial3_each_correct': ['D', 29],
            'trial3_each_time': ['E', 29],
        }
    }
    
    def __init__(self, participant_id, test_name, output_path = None):
        self.test_name = test_name
        self.participant_id = participant_id
        if output_path is None:
            self.output_path = '../output/' + participant_id + '.xlsx'

        if os.path.isfile(self.output_path):
            self.workbook = openpyxl.load_workbook(self.output_path)
        else:
            self.workbook = openpyxl.load_workbook('../template/' + '메인' + '.xlsx')
        self.worksheet = self.workbook[self.test_name]
        
    def write(self, name, value, index=0, autosave=True):
        position = self.value_table[self.test_name][name]
        if isinstance(value, list):
            value = str(value)
        self.worksheet[position[0] + str(position[1] + index)] = value
        if autosave:
            self.save()
    
    def read(self, name, index=0):
        position = self.value_table[self.test_name][name]
        return self.worksheet[position[0] + str(position[1] + index)].value
        
    def save(self, reload=True):
        self.workbook.save(self.output_path)
        self.__init__(self.participant_id, self.test_name, self.output_path)
        
    def close(self):
        self.workbook.close()
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.save(reload=False)
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
        self.mouse=psycopy_mouse(visible=True, win=win)
    
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
        self.dobjects.sort(key= lambda x: x.z)
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
            

class drawling_image(drawling_object):
    def __init__(self, x, y, image, height = 1):
        global win
        image1 = Image.open(image)
        mag1_size = image1.size
        y_x = image1.size[0] / image1.size[1]
        self.image = visual.ImageStim(win, pos=[x, y], image=image, size=[y_x * height, height])
        super().__init__(self.image)
        
class drawling_text(drawling_object):
    def __init__(self, x, y, text, color, height = 1):
        global win
        
        self.text = visual.TextStim(win, text=text, color=color, pos=[x, y], height=height)
        super().__init__(self.text)
    def setText(self, text):
        self.text.setText(text)
        
def inputParticipant():
    with open('../id.txt', 'r') as f:
        json_data = json.load(f)

    # Setting some parameters on GUI
    exp_info = {
        'Participant ID': json_data['last_id'],
    }
    dlg = gui.DlgFromDict(exp_info, title='Corsi Test',)
    if not dlg.OK:
        print ('User Cancelled')
        core.quit()
    id = exp_info['Participant ID']
    json_data['last_id'] = id
    with open('../id.txt', 'w', encoding='utf-8') as make_file:
        json.dump(json_data, make_file, indent="\t")

    return id


def showExplanation(images):
    for file_name in images:
        image = drawling_image(0, 0, file_name)
        image.z = 999999
        window.append(image)
        window.update_wait_key()
        window.remove(image)
        
win = None
window = None
def initWindow():
    #윈도우
    global win, window
    win = visual.Window([1600, 900], allowGUI=True, fullscr=False, units='height', color=[255,255,255])
    window = window_manager(win)
    return win, window
####################################################################################