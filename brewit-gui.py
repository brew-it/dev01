import sys
import datetime
import time

import tkinter as tk
import misc.datehelper
import misc.constants
import data.config
import robot.device_info
import gui.batchselect

from tkinter import messagebox
from robot.states.controller import *


import time
logger = logging.getLogger(__name__)


def ButtonStart():
    SetCurrentState(STATE_STARTING)

def ButtonQuit():
    sys.exit(0)

def ButtonSelectBatch():
	gui.batchselect.ButtonSelectBatch(top, tk)
	
def ButtonStop():
    SetCurrentState(STATE_STOPPING)

def ButtonPause():
    current_state = GetCurrentState()
    if(current_state == STATE_PAUSING):
        SetCurrentState(STATE_ENDPAUSE)
    else:
        # we keep the old state value to resume later and we pause...
        data.config.SetConfig('states','paused_state', current_state)
        SetCurrentState(STATE_PAUSING)

		

def PlaceLabels(top, tk):
	global device_state,  batch_id,  time_endofstate, fermenting_temp
	global lbl_device_state, lbl_fermenting_temp, lbl_batch_id, lbl_eos_time

	device_state = tk.StringVar()
	lbl_device_state = tk.Label(top, textvariable=device_state, fg=misc.constants.GUI_WINDOWS_FORECOLOR, bg=misc.constants.GUI_WINDOWS_BACKCOLOR)

	fermenting_temp = tk.StringVar()
	lbl_fermenting_temp = tk.Label(top, textvariable=fermenting_temp, fg=misc.constants.GUI_WINDOWS_FORECOLOR, bg=misc.constants.GUI_WINDOWS_BACKCOLOR)

	batch_id = tk.StringVar()
	batch_id.set('none');
	lbl_batch_id = tk.Label(top, textvariable=batch_id, fg=misc.constants.GUI_WINDOWS_FORECOLOR, bg=misc.constants.GUI_WINDOWS_BACKCOLOR)

	time_endofstate = tk.StringVar()
	lbl_eos_time = tk.Label(top, textvariable=time_endofstate, fg=misc.constants.GUI_WINDOWS_FORECOLOR, bg=misc.constants.GUI_WINDOWS_BACKCOLOR)

		
def PlaceButtons(top, tk):
	#lbl_logo.place(x=0, y=0)
	LBL_X_ALIGN = 75

	BUTTON_WIDTH = 106
	BUTTON_HEIGHT = 30

	BUTTON_X_ALIGN = 0
	BUTTON_ROW_1_Y = 160 
	BUTTON_ROW_2_Y = BUTTON_ROW_1_Y + BUTTON_HEIGHT + 2

	lbl_batch_id.place(x=LBL_X_ALIGN, y=5)
	lbl_device_state.place(x=LBL_X_ALIGN, y=30)
	lbl_fermenting_temp.place(x=LBL_X_ALIGN, y=50)
	lbl_eos_time.place(x=LBL_X_ALIGN,y=70)

	btnStart = tk.Button (top, text='Start',command = ButtonStart)
	btnStart.place(bordermode=tk.OUTSIDE, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, x= BUTTON_WIDTH*0+1, y=BUTTON_ROW_1_Y)

	btnBatch = tk.Button (top, text='Batch...',command = ButtonSelectBatch)
	btnBatch.place(bordermode=tk.OUTSIDE, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, x= BUTTON_WIDTH*1+1, y=BUTTON_ROW_1_Y)

	btnStop = tk.Button (top, text='Stop',command = ButtonStop)
	btnStop.place(bordermode=tk.OUTSIDE, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, x= BUTTON_WIDTH*2+1, y=BUTTON_ROW_1_Y)

	btnStop = tk.Button (top, text='Pause',command = ButtonPause)
	btnStop.place(bordermode=tk.OUTSIDE, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, x= BUTTON_WIDTH*0+1, y=BUTTON_ROW_2_Y)

	btnStop = tk.Button (top, text='Quit',command = ButtonQuit)
	btnStop.place(bordermode=tk.OUTSIDE, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, x= BUTTON_WIDTH*2+1, y=BUTTON_ROW_2_Y)		


def ProgramLoop():
        global cpt
        global device_state, fermenting_temp

        state_value = robot.states.controller.GetCurrentStateName(robot.states.controller.GetCurrentState())
        logging.info((str(state_value)))
        device_state.set("Current state: ")
        
        if((GetCurrentState() == STATE_DISPENSING)):
            time_endofstate.set("Enjoy your beer!")  
        elif((GetCurrentState() == STATE_IDLE)):
            time_endofstate.set("")  
        else:
            a = datetime.datetime.now()
            f ="%Y-%m-%d %H:%M:%S.%f"
            b = GetEOSTime()
            if(b == ""):
                time_endofstate.set("")
            else:
                test = datetime.datetime.strptime(b, f)

                time_difference = test -a
                time_differences_in_seconds = time_difference / datetime.timedelta(seconds=1)
                ending_time = "Time remaining: " +str(misc.datehelper.ddhhmmss(time_differences_in_seconds)) + ""
                time_endofstate.set(ending_time)


        cur_batchid= robot.device_info.GetBatchId()
        batch_id.set('Batch #: ' + str(cur_batchid))

		
        fermenting_temp.set("Current Temperature:" + str(robot.device_info.GetFermenterTemperature()))
        top.after(500, ProgramLoop)

cpt=0

window_title = misc.constants.PROGRAM_TITLE + " " + misc.constants.PROGRAM_VERSION 
top = tk.Tk()
top.title(window_title)
top.configure(background='black')
#top.attributes('-fullscreen',True)
top.geometry(misc.constants.GUI_SCREEN_SIZE)


img_logo = tk.PhotoImage(file="./resources/logo.gif")
img_logo = img_logo.subsample(2,2)
c = tk.Canvas(top, bg='black', bd=0, highlightthickness=0, relief='ridge')
c.place(x=0,y=0)
c.create_image(0,0,image = img_logo, anchor=tk.NW)

PlaceLabels(top,tk)
PlaceButtons(top,tk)


top.after(1000, ProgramLoop)
#visualkb = tk.Toplevel()
#visualkb.attributes('-fullscreen',True)

top.mainloop()