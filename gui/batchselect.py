import misc.constants
import data.config
from functools import partial

KEYB_BUTTON_WIDTH = 6
KEYB_BUTTON_HEIGHT = 2


def ButtonSelectBatch(top, tk):
    visualkb = tk.Tk()
    visualkb.configure(background=misc.constants.GUI_WINDOWS_BACKCOLOR)
    visualkb.geometry(misc.constants.GUI_SCREEN_SIZE)

    txt_batchnum= tk.Entry(visualkb, width=24, font=('Helvetica', '18'))
    txt_batchnum.place(x=0, y=0)

    lf = tk.LabelFrame(visualkb, bd=0, background=misc.constants.GUI_WINDOWS_BACKCOLOR)
    lf.place(x=0, y=40)


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
        cmd = partial(ButtonClicked, tk, label, txt_batchnum, visualkb)
        btn[n] = tk.Button(lf, text=label, width=KEYB_BUTTON_WIDTH, height=KEYB_BUTTON_HEIGHT, command=cmd)
        btn[n].grid(row=r, column=c)
        n += 1
        c += 1
        if c > 3:
            c = 0
            r += 1

    visualkb.mainloop()
	
	
	
	
def ButtonClicked(tk, btn, textfield, window):
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