"""Make sure to install PyMySQL (pip install pymysql) & to put the resourses folder in the same directory with this python file."""

from tkinter import *                         # pip install future (in pycharm).
from tkinter.ttk import Progressbar
from tkinter import ttk
from PIL import ImageTk, Image                # pip install pillow.
import os, sys

# Getting required files.

if getattr(sys, 'frozen', False):                               # When file is bundeled, frozen attribute is available for sys module.
    splash_image = Image.open(os.path.join(sys._MEIPASS, "resources", "splash.png"))
else:
    splash_image = Image.open(os.path.join("resources","splash.png"))

# Splash Screen.
splash_screen = Tk()
splash_screen.geometry('800x500+330+180')
splash_screen.resizable(False, False)
splash_screen.overrideredirect(True)               # Hide the title bar.

resized_splash = splash_image.resize((800, 500))
splash_bg = ImageTk.PhotoImage(resized_splash)

canvas = Canvas(splash_screen, height=510, width=810, bg='red')
canvas.place(x=-5, y=-5)

canvas.create_image(405,255, image=splash_bg, anchor=CENTER)                               # (x,y)centre of image and achor is the postion from where image will be stretched.

canvas.create_text(400, 80, text='Student Record', font=('Noto Sans CJK TC', 35, 'bold'), fill='yellow', anchor=CENTER)
canvas.create_text(405, 130, text='Management System', font=('Noto Sans CJK TC', 35, 'bold'), fill='yellow', anchor=CENTER)

canvas.create_line(150, 40, 670, 40, width=8, fill='royalblue')
canvas.create_line(150, 170, 670, 170, width=8, fill='royalblue')
canvas.create_line(154, 40, 154, 170, width=8, fill='cyan')
canvas.create_line(666, 40, 666, 170, width=8, fill='cyan')

canvas.create_text(400, 250, text='Designed & Developed by', font=('Agency FB', 30), fill='aquamarine', anchor=CENTER)
canvas.create_text(400, 310, text='Swayam Singh', font=('Agency FB', 40, 'bold'), fill='orange', anchor=CENTER)

canvas.create_text(400, 460, text='Loading...', font=('Calibri', 22), fill='aquamarine', anchor=CENTER)

s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')
progress=Progressbar(splash_screen,style="red.Horizontal.TProgressbar",orient=HORIZONTAL,length=800,mode='determinate')
progress.pack(anchor=CENTER, side=BOTTOM)

def bar():
    import time
    r=0
    for i in range(101):
        progress['value']=r
        splash_screen.update_idletasks()
        time.sleep(0.03)
        r=r+1
    splash_screen.destroy()
    import login_win
    login_win.main()
splash_screen.after(1500, bar)

splash_screen.mainloop()