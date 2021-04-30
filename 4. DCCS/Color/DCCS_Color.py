#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, gui, data
from PIL import Image
import random
import winsound
import sys             #sys.exit()
import DCCS_Color_Info

subinfo = DCCS_Color_Info.getSubjInfo()
# Open log file to write
# 기록 파일 이름
file_name = subinfo[1]+'_dccs.csv' #ID-0, Name-1
log_file = open(file_name, 'a')
#기록 파일 내 포함될 변인과 헤드 이름
log_file.write('#image, z/slash, error, time\n') # Heading



mywin = visual.Window([1920,1080], screen=0, fullscr=False, color=(1, 1, 1), units='pix')

grim = visual.ImageStim(mywin, units ='pix', size=1000)                           #Tutorial
stim = visual.ImageStim(mywin, units ='pix', pos=(0,-240), size=480)              #Stimulus
RT = core.Clock()

rabbit = visual.ImageStim(mywin, units='pix', pos = (-320, 240), size=420)                  #fix 1
boat = visual.ImageStim(mywin, units='pix', pos= (310,260), size=380)                       #fix 2
preFix = visual.TextStim(mywin, text='+', color=[-1,-1,-1], height=80, pos=(0,-200), units='pix')


################################## BLOCK 1 - SHAPE #
Tutorial = ["T1.png", "T2.png", "T3.png", "T4.png", "T5.png", "T6.png", "T7.png", "T8.png"]

for t in range(8):
    grim.image = Tutorial[t]
    grim.draw()
    mywin.flip()
    while 'space' not in event.getKeys():pass

pictures = ["Blue_rabbit.png", "Red_boat.png", "Red_rabbit.png", "Blue_boat.png", "red_rabbit_square.png", "blue_boat_square.png"]
rabbit.image = pictures[0]
boat.image = pictures[1]

order = [2,3,3,2]
orders = []
for j in range(4):
    random.shuffle(order)
    orders.extend(order)
#print orders

results = [] 

sum_rw_1 = 0
sum_times_1 = 0.0
sum_times_correct_1 = 0.0 #error=1일때 times 합

for i in orders:                    #??? i or j
    rabbit.draw()
    boat.draw()
    preFix.draw()
    mywin.flip()
    winsound.Beep(880,500)
    core.wait(0.5)

    rabbit.draw()
    boat.draw()
    stim.image = pictures[i]
    stim.draw()
    mywin.flip()
    RT.reset()
    
    keys = []
    event.clearEvents('keyboard')
    while len(keys) == 0:
        keys = event.getKeys(['z', 'slash'], timeStamped=RT)
    
    if i == 2: 
        if keys[0][0] == 'slash':
            rw = 1
            #winsound.PlaySound('CASHREG.WAV', winsound.SND_FILENAME)
        else: 
            rw = 0
            #winsound.PlaySound('EXPLODE.WAV', winsound.SND_FILENAME)
    if i == 3:
        if keys[0][0] == 'z':
            rw = 1
            #winsound.PlaySound('CASHREG.WAV', winsound.SND_FILENAME)
        else: 
            rw = 0
            #winsound.PlaySound('EXPLODE.WAV', winsound.SND_FILENAME)
    core.wait(0.5)
    print(i,  keys[0][0], rw, keys[0][1])
    sum_rw_1 = sum_rw_1 + rw #error의 합 
    sum_times_1 = sum_times_1 + keys[0][1]
    if(rw == 1):
        sum_times_correct_1 = sum_times_correct_1 + keys[0][1]
        
    log_file.write('"%d", %s, %d, %s\n' %(i, keys[0][0], rw, keys[0][1]))

    results.append([i, rw, keys[0][1]])
    
string_name_1 = "block#1"


################################## BLOCK 2 - COLOR #
Tutorial2 = ["TT1.png", "TT2.png", "TT3.png", "TT4.png", "TT5.png", "TT6.png", "TT7.png", "TT8.png"]

for t in range(8):
    grim.image = Tutorial2[t]
    grim.draw()
    mywin.flip()
    while 'space' not in event.getKeys():pass

pictures = ["Blue_rabbit.png", "Red_boat.png", "Red_rabbit.png", "Blue_boat.png", "red_rabbit_square.png", "blue_boat_square.png"]
rabbit.image = pictures[0]
boat.image = pictures[1]

order = [2,3,3,2]
orders = []
for j in range(4):
    random.shuffle(order)
    orders.extend(order)
print(orders)


sum_rw_2 = 0
sum_times_2 = 0.0
sum_times_correct_2 = 0.0 #error=1일때 times 합

for i in orders:                    #??? i or j
    rabbit.draw()
    boat.draw()
    preFix.draw()
    mywin.flip()
    winsound.Beep(880,500)
    core.wait(0.5)

    rabbit.draw()
    boat.draw()
    stim.image = pictures[i]
    stim.draw()
    mywin.flip()
    RT.reset()

    keys = []
    event.clearEvents('keyboard')
    while len(keys) == 0:
        keys = event.getKeys(['z', 'slash'], timeStamped=RT)
    
    if i == 2: 
        if keys[0][0] == 'z':
            rw = 1
        else: 
            rw = 0
    if i == 3:
        if keys[0][0] == 'slash':
            rw = 1
        else: 
            rw = 0
    core.wait(0.5)
    print(i,  keys[0][0], rw, keys[0][1])
    sum_rw_2 = sum_rw_2 + rw #error의 합 
    sum_times_2 = sum_times_2 + keys[0][1]
    if(rw == 1):
        sum_times_correct_2 = sum_times_correct_2 + keys[0][1]
    log_file.write('"%d", %s, %d, %s\n' %(i, keys[0][0], rw, keys[0][1]))
    

    results.append([i, rw, keys[0][1]])

string_name_2 = "block#2"


################################## BLOCK 3 - MIX #
Tutorial3 = ["TTT1.png", "TTT2.png", "TTT3.png", "TTT4.png", "TTT5.png", "TTT6.png", "TTT7.png",  "TTT15.png", "TTT16.png", "TTT8.png", "TTT9.png", "TTT10.png", "TTT11.png", "TTT12.png", "TTT13.png", "TTT14.png"]

for t in range(16):
    grim.image = Tutorial3[t]
    grim.draw()
    mywin.flip()
    while 'space' not in event.getKeys():pass

pictures = ["Blue_rabbit.png", "Red_boat.png", "Red_rabbit.png", "Blue_boat.png", "red_rabbit_square.png", "blue_boat_square.png"]
rabbit.image = pictures[0]
boat.image = pictures[1]

order = [2,3,4,5]
orders = []
for j in range(2):
    random.shuffle(order)
    orders.extend(order)
print(orders)
 
sum_rw_3 = 0
sum_times_3 = 0.0
sum_times_correct_3 = 0.0 #error=1일때 times 합

for i in orders:
    rabbit.draw()
    boat.draw()
    preFix.draw()
    mywin.flip()
    winsound.Beep(880,500)
    core.wait(0.5)

    rabbit.draw()
    boat.draw()
    stim.image = pictures[i]
    stim.draw()
    mywin.flip()

    RT.reset()
    keys = []
    event.clearEvents('keyboard')
    while len(keys) == 0:
        keys = event.getKeys(['z', 'slash'], timeStamped=RT)

    if i == 2:
        if keys[0][0] == 'z':
            rw = 1
        else: 
            rw = 0
    if i == 3:
        if keys[0][0] == 'slash':
            rw = 1
        else: 
            rw = 0
    if i == 5:
        if keys[0][0] == 'z':
            rw = 1
        else: 
            rw = 0
    if i == 4:
        if keys[0][0] == 'slash':
            rw = 1
        else: 
            rw = 0
    core.wait(0.5)
    print(i,  keys[0][0], rw, keys[0][1])
    sum_rw_3 = sum_rw_3 + rw #error의 합 
    sum_times_3 = sum_times_3 + keys[0][1]
    if(rw == 1):
        sum_times_correct_3 = sum_times_correct_3 + keys[0][1]
    log_file.write('"%d", %s, %d, %s\n' %(i, keys[0][0], rw, keys[0][1]))

    results.append([i, rw, keys[0][1]])
    
string_name_3 = "block#3"


Tutorial4 = ["TTTT1.png", "TTTT2.png", "TTTT3.png"]

for t in range(3):
    grim.image = Tutorial4[t]
    grim.draw()
    mywin.flip()
    while 'space' not in event.getKeys():pass


pictures = ["Blue_rabbit.png", "Red_boat.png", "Red_rabbit.png", "Blue_boat.png", "red_rabbit_square.png", "blue_boat_square.png"]
rabbit.image = pictures[0]
boat.image = pictures[1]

order = [2,3,4,5]
orders = []
for j in range(3):
    random.shuffle(order)
    orders.extend(order)
print(orders)
 
sum_rw_4 = 0
sum_times_4 = 0.0
sum_times_correct_4 = 0.0 #error=1일때 times 합

for i in orders:
    rabbit.draw()
    boat.draw()
    preFix.draw()
    mywin.flip()
    winsound.Beep(880,500)
    core.wait(0.5)

    rabbit.draw()
    boat.draw()
    stim.image = pictures[i]
    stim.draw()
    mywin.flip()

    RT.reset()
    keys = []
    event.clearEvents('keyboard')
    while len(keys) == 0:
        keys = event.getKeys(['z', 'slash'], timeStamped=RT)

    if i == 2:
        if keys[0][0] == 'z':
            rw = 1
        else: 
            rw = 0
    if i == 3:
        if keys[0][0] == 'slash':
            rw = 1
        else: 
            rw = 0
    if i == 5:
        if keys[0][0] == 'z':
            rw = 1
        else: 
            rw = 0
    if i == 4:
        if keys[0][0] == 'slash':
            rw = 1
        else: 
            rw = 0
    core.wait(0.5)
    print(i,  keys[0][0], rw, keys[0][1])
    sum_rw_4 = sum_rw_4 + rw #error의 합 
    sum_times_4 = sum_times_4 + keys[0][1]
    if(rw == 1):
        sum_times_correct_4 = sum_times_correct_4 + keys[0][1]
    log_file.write('"%d", %s, %d, %s\n' %(i, keys[0][0], rw, keys[0][1]))

    results.append([i, rw, keys[0][1]])

string_name_4 = "block#4"


log_file.write('\n#block, correct_sum, avg_total, avg_correct\n') # Heading

log_file.write('"%s", %d, %f, %f\n' %(string_name_1, sum_rw_1, sum_times_1/20, sum_times_correct_1/20))
log_file.write('"%s", %d, %f, %f\n' %(string_name_2, sum_rw_2, sum_times_2/20, sum_times_correct_2/20))
log_file.write('"%s", %d, %f, %f\n' %(string_name_3, sum_rw_3, sum_times_3/8, sum_times_correct_3/8))
log_file.write('"%s", %d, %f, %f\n' %(string_name_4, sum_rw_4, sum_times_4/12, sum_times_correct_4/12))



mywin.close()

