#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, gui, data
import psychopy.tools.filetools
import sys             #sys.exit()

def getSubjInfo():
    dlg = gui.Dlg(title='GoNoGo task', pos=(200, 400))
    dlg.addText('Subject Info', color='Blue')
    dlg.addField('ID:')
    dlg.addField('NAME :')
#    dlg.addField('Gender :', choices=['female','male'])
    thisInfo = dlg.show()  # you have to call show() for a Dlg (automatic with a DlgFromDict)    
    if dlg.OK:
        print ('Subject Info : ', thisInfo)
    else:
        print('User cancelled')
        core.quit()

    return thisInfo
    
    
def saveResult(expTitle, subjInfo, respResult):
    responseList = []
    responseList.append(subjInfo)
    responseList.append(respResult)
    psychopy.tools.filetools.toFile(expTitle+subjInfo[0]+subjInfo[1]+".pkl2", responseList)

if __name__ == '__main__':
    subjInfo = getSubjInfo()
    print (subjInfo)