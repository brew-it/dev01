import sys
import datetime
import time

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

import data.config
import robot.device_info
from tkinter import messagebox
from misc.constants import *
from robot.states.controller import *
from functools import partial

BACK_COLOR = "black"
FORE_COLOR = "white"


def KeyboardButtonClicked(btn, textfield, window):
    s = "button %s clicked" % btn
    #textfield.set(s)
    content = textfield.get()
    if(btn == '<-'):
        #on delete uen value
        content = content[:-1] 
    else:
        content = content + btn

    if(btn == 'OK'):
        content = content[:-2] 
        data.config.SetConfig('batchinfo','batchid',content)
        window.destroy()
    else:
        textfield.delete(0,tk.END)
        textfield.insert(0,content)
    #messagebox.showinfo('button clicked',test)
    #textfield.insert(0,s)




def ButtonStart():
    SetCurrentState(STATE_STARTING)

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



def ButtonSelectBatch():
    ##SetCurrentState(STATE_PREFERMENTING)
    visualkb = tk.Tk()
    visualkb.configure(background='black')
    visualkb.geometry('600x220')



    lf = tk.LabelFrame(visualkb, text="test", bd=3)
    lf.place(x=0, y=20)

    txt_batchnum= tk.Entry(visualkb, width=21, font=('Helvetica', '18'))
    txt_batchnum.place(x=0, y=0)


    btn_list = [
        '7','8','9',
        '4','5','6',
        '1','2','3',
        '0','<-','OK']

    r=1
    c=0
    n=0

    btn = list(range(len(btn_list)))
    for label in btn_list:
        cmd = partial(KeyboardButtonClicked, label, txt_batchnum, visualkb)
        btn[n] = tk.Button(lf, text=label, width=5, command=cmd)
        btn[n].grid(row=r, column=c)
        n += 1
        c += 1
        if c > 3:
            c = 0
            r += 1


    visualkb.mainloop()
    

def GetDateTimeFormatted(datetime_value):
    date_format ="%Y-%m-%d %H:%M:%S"
    return datetime.datetime.strptime(datetime_value.split(".")[0], date_format)
    
def ddhhmmss(seconds):
    dhms = ''
    for scale in 86400, 3600, 60:
        result, seconds = divmod(seconds, scale)
        if dhms != '' or result > 0:
            if(scale == 86400):
                dhms += str(int(result)) + "d "
            elif(scale == 3600):
                dhms += '{0:01g}'.format(result) + "h"
            elif(scale == 60):
                dhms += str(int(result)) + "m "

    dhms += str(int(seconds)) + "s"
    return dhms
        



def ProgramLoop():
        global cpt
        state_value = GetCurrentStateName(GetCurrentState())
        print(str(GetCurrentState()))
        device_state.set("Current state: " + state_value)
        
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
                ending_time = "Time remaining: " +str(ddhhmmss(time_differences_in_seconds)) + ""
                time_endofstate.set(ending_time)


        cur_batchid= robot.device_info.GetBatchId()
        batch_id.set('Batch #: ' + str(cur_batchid))

        fermenting_temp.set("Current Temperature:" + str(robot.device_info.GetFermenterTemperature()))
        top.after(500, ProgramLoop)

cpt=0

window_title = PROGRAM_TITLE + " " + PROGRAM_VERSION 
top = tk.Tk()
top.title(window_title)
top.configure(background='black')
#top.attributes('-fullscreen',True)
top.geometry('600x220')


photo = tk.PhotoImage(file="./resources/logo.gif")
c = tk.Canvas(top, bg='black', bd=0, highlightthickness=0, relief='ridge')
c.place(x=0,y=0)
c.create_image(80,110,image = photo)

#lbl_logo = tkinter.Label(top, text=window_title,  fg=WINDOWS_FORECOLOR, bg=WINDOWS_BACKCOLOR, font=('Helvetica', 24))
#lbl_logo = tkinter.Label(top, image=photo)
#lbl_logo.photo = photo

device_state = tk.StringVar()
lbl_device_state = tk.Label(top, textvariable=device_state, fg=WINDOWS_FORECOLOR, bg=WINDOWS_BACKCOLOR)

fermenting_temp = tk.StringVar()
lbl_fermenting_temp = tk.Label(top, textvariable=fermenting_temp, fg=WINDOWS_FORECOLOR, bg=WINDOWS_BACKCOLOR)

batch_id = tk.StringVar()
batch_id.set('none');
lbl_batch_id = tk.Label(top, textvariable=batch_id, fg=WINDOWS_FORECOLOR, bg=WINDOWS_BACKCOLOR)

time_endofstate = tk.StringVar()
lbl_eos_time = tk.Label(top, textvariable=time_endofstate, fg=WINDOWS_FORECOLOR, bg=WINDOWS_BACKCOLOR)

#lbl_logo.place(x=0, y=0)
lbl_batch_id.place(x=160, y=10)
lbl_device_state.place(x=160, y=30)
lbl_fermenting_temp.place(x=160, y=50)
lbl_eos_time.place(x=160,y=70)

btnStart = tk.Button (top, text='Start',command = ButtonStart)
btnStart.place(bordermode=tk.OUTSIDE, height=30, width=100, x= 160, y=175)

btnBatch = tk.Button (top, text='Batch...',command = ButtonSelectBatch)
btnBatch.place(bordermode=tk.OUTSIDE, height=30, width=100, x= 260, y=175)

btnStop = tk.Button (top, text='Stop',command = ButtonStop)
btnStop.place(bordermode=tk.OUTSIDE, height=30, width=100, x= 360, y=175)


btnStop = tk.Button (top, text='Pause',command = ButtonPause)
btnStop.place(bordermode=tk.OUTSIDE, height=30, width=100, x= 460, y=175)




top.after(1000, ProgramLoop)
#visualkb = tk.Toplevel()
#visualkb.attributes('-fullscreen',True)

top.mainloop()


    



