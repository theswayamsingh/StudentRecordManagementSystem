import numpy as np
import pandas as pd                           # pip install pandas
from tkinter import *                         # pip install future (in pycharm)
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import ImageTk, Image                # pip install pillow
from sqlalchemy import create_engine as ce
from sqlalchemy import text
import os, sys, ast
import matplotlib.pyplot as plt               # pip install matplotlib

# Getting Required Files.

if getattr(sys, 'frozen', False):
    main_win_icon_path = os.path.join(sys._MEIPASS,"resources","icon.ico")              # sys._MEIPASS is only usable in exe.
    other_win_icon_path = os.path.join(sys._MEIPASS,"resources","title_logo.ico")
    back_icon_path = os.path.join(sys._MEIPASS, 'resources', 'back-arrow.png')
    close_icon_path = os.path.join(sys._MEIPASS, 'resources', 'close.png')

    admins_text_file = os.path.join(sys._MEIPASS, 'resources', 'admins.txt')
    users_text_file = os.path.join(sys._MEIPASS, 'resources', 'users.txt')
    tb_values_text_file = os.path.join(sys._MEIPASS, 'resources', 'tb_values.txt')
    user_val_text_file = os.path.join(sys._MEIPASS, 'resources', 'user_val.txt')
    sql_text_file = os.path.join(sys._MEIPASS, 'resources', 'sql_connection.txt')
else:
    main_win_icon_path = os.path.join("resources","icon.ico")
    other_win_icon_path = os.path.join("resources","title_logo.ico")
    back_icon_path = os.path.join('resources', 'back-arrow.png')
    close_icon_path = os.path.join('resources', 'close.png')

    admins_text_file = os.path.join('resources', 'admins.txt')
    users_text_file = os.path.join('resources', 'users.txt')
    tb_values_text_file = os.path.join('resources', 'tb_values.txt')
    user_val_text_file = os.path.join('resources', 'user_val.txt')
    sql_text_file = os.path.join('resources', 'sql_connection.txt')

def main():
    global connection, tb

    file = open(sql_text_file, 'r')
    data = file.read()
    sqlvals = ast.literal_eval(data)
    file.close()

    user = sqlvals[0]
    password = sqlvals[1]
    host = sqlvals[2]
    engine = ce("mysql+pymysql://{}:{}@{}/srms_marksheet".format(user, password, host))
    connection = engine.connect()

    # Main Window.

    root = Tk()
    root.title('Marksheet Management')
    root.geometry('1410x650+10+100')
    root.resizable(False, False)
    root.iconbitmap(main_win_icon_path)
    root.config(bg='DodgerBlue4')

    # Functions.

    def add():
        def submit():
            roll_no = rollval.get()
            name = nameval.get()
            sub1_marks = sub1val.get()
            sub2_marks = sub2val.get()
            sub3_marks = sub3val.get()
            sub4_marks = sub4val.get()
            sub5_marks = sub5val.get()
            sub6_marks = sub6val.get()
            if Class>10:
                op_sub = e7.get()
                add_sub = e9.get()

            if roll_no=='' or name=='':
                messagebox.showerror('Error!', 'Roll_No and Name are must. ')
                return

            # Checking type of Roll No.
            try:
                int(roll_no)
            except:
                messagebox.showerror('Invalid Roll_No!', 'Roll_No needs to be integer.')
                return
            #Checking length of Roll No.
            rollstr = str(roll_no)
            if len(rollstr)>5:
                messagebox.showerror('Invalid Roll_No!', 'The length of Roll_No exceeds limit.')
                return

            # Checking the data type of marks.
            subjects = [sub1_marks, sub2_marks, sub3_marks, sub4_marks, sub5_marks, sub6_marks]
            x = []
            for sub in subjects:
                if sub != '':
                    try:
                        sub=int(sub)
                        x.append(sub)
                    except:
                        messagebox.showerror('Invalid marks!', 'Marks needs to be integer.')
                        return
            # Checking the length of marks.
            for sub in x:
                if sub>100:
                    messagebox.showerror('Invalid Marks!', 'Marks in one subject cannot be greater than 100.')
                    return

            try:
                if Class<=10:
                    connection.execute(text("insert into {} values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(tb, roll_no, name, sub1_marks, sub2_marks, sub3_marks, sub4_marks, sub5_marks, sub6_marks)))
                    connection.commit()
                elif Class>10:
                    connection.execute(text("insert into {} values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(tb, roll_no, name, sub1_marks, sub2_marks, sub3_marks, sub4_marks, op_sub, sub5_marks, add_sub, sub6_marks)))
                    connection.commit()
                res = messagebox.askyesno('Record added successfully!', "Record with Roll No. '{}' and Name '{}' added successfully. Do you want to clear the fill-up form?".format(roll_no, name), parent=addtop)
                if res == True:
                    rollval.set('')
                    nameval.set('')
                    sub1val.set('')
                    sub2val.set('')
                    sub3val.set('')
                    sub4val.set('')
                    sub5val.set('')
                    sub6val.set('')
                    if Class>10:
                        e7.set('')
                        e9.set('')

            except:
                messagebox.showerror('Duplicate Primary Key!', 'Multiple records with same Roll_No found. Make sure that the Roll_No is unique.', parent=addtop)

            refresh()

        addtop = Toplevel()
        addtop.title('Add Record')
        addtop.config(bg='cornflowerblue')
        addtop.grab_set()  # Button out of window not work.
        addtop.iconbitmap(other_win_icon_path)
        addtop.resizable(False, False)

        if Class<=10:
            addtop.geometry('500x560+500+150')

            # Labels.
            l1 = Label(addtop, text='Roll No.', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                       borderwidth=2, width=12)
            l1.place(x=25, y=15)

            l2 = Label(addtop, text='Name', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                       borderwidth=2, width=12)
            l2.place(x=25, y=70)

            l3 = Label(addtop, text='Science', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                       borderwidth=2, width=12)
            l3.place(x=25, y=125)

            l4 = Label(addtop, text='Maths', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                       borderwidth=2, width=12)
            l4.place(x=25, y=180)

            l5 = Label(addtop, text='Social', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                       borderwidth=2, width=12)
            l5.place(x=25, y=235)

            l6 = Label(addtop, text='English', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                       borderwidth=2, width=12)
            l6.place(x=25, y=290)

            l7 = Label(addtop, text='Hindi', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                       borderwidth=2, width=12)
            l7.place(x=25, y=345)

            l8 = Label(addtop, text='Computer', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                       borderwidth=2, width=12)
            l8.place(x=25, y=400)

            l9 = Label(addtop, text='*Roll No. and Name are must.', font=('Calibri', 14, 'bold'), bg='cornflowerblue',
                        relief=GROOVE)
            l9.place(x=25, y=455)

            # Entry boxes.
            rollval = StringVar()
            nameval = StringVar()
            sub1val = StringVar()
            sub2val = StringVar()
            sub3val = StringVar()
            sub4val = StringVar()
            sub5val = StringVar()
            sub6val = StringVar()

            e1 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=rollval)
            e1.place(x=200, y=15)

            e2 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=nameval)
            e2.place(x=200, y=70)

            e3 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=sub1val)
            e3.place(x=200, y=125)

            e4 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=sub2val)
            e4.place(x=200, y=180)

            e5 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=sub3val)
            e5.place(x=200, y=235)

            e6 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=sub4val)
            e6.place(x=200, y=290)

            e7 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=sub5val)
            e7.place(x=200, y=345)

            e8 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=sub6val)
            e8.place(x=200, y=400)

            # Button.
            b = Button(addtop, text='Submit', font=('Arial Rounded MT Bold', 20), bg='royalblue', bd=3, width=12,
                       command=submit)
            b.place(x=130, y=490)

        elif Class>10:
            addtop.geometry('500x665+500+100')

            # Labels.
            l1 = Label(addtop, text='Roll No.', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l1.place(x=25, y=15)

            l2 = Label(addtop, text='Name', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l2.place(x=25, y=70)

            l3 = Label(addtop, text=sub1, font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l3.place(x=25, y=125)

            l4 = Label(addtop, text=sub2, font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l4.place(x=25, y=180)

            l5 = Label(addtop, text=sub3, font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l5.place(x=25, y=235)

            l6 = Label(addtop, text='English', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l6.place(x=25, y=290)

            l7 = Label(addtop, text='Op_Sub', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l7.place(x=25, y=345)

            l8 = Label(addtop, text='Op_marks', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l8.place(x=25, y=400)

            l9 = Label(addtop, text='Add_Sub', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l9.place(x=25, y=455)

            l10 = Label(addtop, text='Add_Marks', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,borderwidth=2, width=12)
            l10.place(x=25, y=510)

            l11 = Label(addtop, text='*Roll No. and Name are must.', font=('Calibri', 14, 'bold'), bg='cornflowerblue', relief=GROOVE)
            l11.place(x=25, y=565)

            # Entry boxes.
            rollval = StringVar()
            nameval = StringVar()
            sub1val = StringVar()
            sub2val = StringVar()
            sub3val = StringVar()
            sub4val = StringVar()
            sub5val = StringVar()
            sub6val = StringVar()

            e1 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=rollval)
            e1.place(x=200, y=15)

            e2 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=nameval)
            e2.place(x=200, y=70)

            e3 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=sub1val)
            e3.place(x=200, y=125)

            e4 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=sub2val)
            e4.place(x=200, y=180)

            e5 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=sub3val)
            e5.place(x=200, y=235)

            e6 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=sub4val)
            e6.place(x=200, y=290)

            e7 = ttk.Combobox(addtop, font=('Agency FB', 25), values=['None', 'IP', 'PE', 'Hindi', 'Music', 'Maths', 'Painting', 'Psychology'], width=19, state='readonly')
            e7.place(x=200, y=345)
            e7.current(0)

            e8 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=sub5val)
            e8.place(x=200, y=400)

            e9 = ttk.Combobox(addtop, font=('Agency FB', 25), values=['None', 'PE', 'Music', 'Painting', 'Psychology'], width=19, state='readonly')
            e9.place(x=200, y=455)
            e9.current(0)

            e10 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, textvariable=sub6val)
            e10.place(x=200, y=510)

            # Button.
            b = Button(addtop, text='Submit', font=('Arial Rounded MT Bold', 20), bg='royalblue', bd=3, width=12, command=submit)
            b.place(x=130, y=600)

        addtop.bind('<Return>', lambda event: submit())
        addtop.mainloop()

    def edit():
        def update():
            new_roll = rollval.get()
            new_name = nameval.get()
            new_sub1 = sub1val.get()
            new_sub2 = sub2val.get()
            new_sub3 = sub3val.get()
            new_sub4 = sub4val.get()
            new_sub5marks = sub5marksval.get()
            new_sub6marks = sub6marksval.get()

            if Class>10:
                new_sub5name = e7.get()
                new_sub6name = e9.get()

            if new_roll=='' or new_name=='':
                messagebox.showerror('Error!', 'Roll_No and Name are must. ')
                return

            # Checking type of Roll No.
            try:
                int(new_roll)
            except:
                messagebox.showerror('Invalid Roll_No!', 'Roll_No needs to be integer.')
                return
            #Checking length of Roll No.
            rollstr = str(new_roll)
            if len(rollstr)>5:
                messagebox.showerror('Invalid Roll_No!', 'The length of Roll_No exceeds limit.')
                return

            # Checking the type and marks.
            subjects = [new_sub1, new_sub2, new_sub3, new_sub4, new_sub5marks, new_sub6marks]
            x = []
            for sub in subjects:
                if sub != '':
                    try:
                        sub=int(sub)
                        x.append(sub)
                    except:
                        messagebox.showerror('Invalid marks!', 'Marks needs to be integer.')
                        return
            # Checking the length of marks.
            for sub in x:
                if sub>100:
                    messagebox.showerror('Invalid Marks!', 'Marks in one subject cannot be greater than 100.')
                    return

            if Class <= 10:
                if cur_roll == new_roll and cur_name == new_name and cur_sub1 == new_sub1 and cur_sub2 == new_sub2 and cur_sub3 == new_sub3 and cur_sub4 == new_sub4 and cur_sub5marks == new_sub5marks and cur_sub6marks == new_sub6marks:
                    messagebox.showinfo('Nothing to update', 'Please make some changes in order to update the record.', parent=top)
                    return
            elif Class > 10:
                if cur_roll == new_roll and cur_name == new_name and cur_sub1 == new_sub1 and cur_sub2 == new_sub2 and cur_sub3 == new_sub3 and cur_sub4 == new_sub4 and cur_sub5name == new_sub5name and cur_sub5marks == new_sub5marks and cur_sub6name == new_sub6name and cur_sub6marks == new_sub6marks:
                    messagebox.showinfo('Nothing to update', 'Please make some changes in order to update the record.', parent=top)
                    return

            try:
                if Class<=10:
                    connection.execute(text("update {} set Roll_No='{}', Student_Name='{}', Science='{}', Maths='{}', Social='{}', English='{}', Hindi='{}', Computer='{}' where Roll_No='{}'".format(tb, new_roll, new_name, new_sub1, new_sub2, new_sub3, new_sub4, new_sub5marks, new_sub6marks, cur_roll)))
                    connection.commit()
                    top.destroy()
                    messagebox.showinfo('Successfully modified!', 'The data has been successfully updated.')
                elif Class>10:
                    connection.execute(text("update {} set Roll_No='{}', Student_Name='{}', {}='{}', {}='{}', {}='{}', English='{}', Op_Sub='{}', Op_Marks='{}', Add_Sub='{}', Add_Marks='{}' where Roll_No='{}'".format(tb, new_roll, new_name, sub1, new_sub1, sub2, new_sub2, sub3, new_sub3, new_sub4, new_sub5name, new_sub5marks, new_sub6name, new_sub6marks, cur_roll)))
                    connection.commit()
                    top.destroy()
                    messagebox.showinfo('Successfully modified!', 'The data has been successfully updated.')

            except:
                messagebox.showerror('Duplicate Primary Key!', 'Multiple records with same Student ID found. Make sure that the Student ID is unique.')

            refresh()

        if not tree.selection():
            messagebox.showerror('Error!', 'Please select an item from the database.')

        else:
            if len(tree.selection())>1:
                messagebox.showerror('Error!', 'Only one record can be edited at a time. Please select only one record.')
                return

            top = Toplevel()
            top.title('Add Record')
            top.config(bg='cornflowerblue')
            top.grab_set()  # Button out of window not work.
            top.iconbitmap(other_win_icon_path)
            top.resizable(False, False)

            if Class<=10:
                top.geometry('500x560+500+150')

                # Labels.
                current_item = tree.focus()
                values = tree.item(current_item)
                selection = values["values"]

                cur_roll = selection[0]
                cur_name = selection[1]
                cur_sub1 = selection[2]
                cur_sub2 = selection[3]
                cur_sub3 = selection[4]
                cur_sub4 = selection[5]
                cur_sub5marks = selection[6]
                cur_sub6marks = selection[7]

                cur_roll = str(cur_roll)
                cur_sub1 = str(cur_sub1)
                cur_sub2 = str(cur_sub2)
                cur_sub3 = str(cur_sub3)
                cur_sub4 = str(cur_sub4)
                cur_sub5marks = str(cur_sub5marks)
                cur_sub6marks = str(cur_sub6marks)

                l1 = Label(top, text='Roll No.', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
                l1.place(x=25, y=15)

                l2 = Label(top, text='Name', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
                l2.place(x=25, y=70)

                l3 = Label(top, text='Science', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
                l3.place(x=25, y=125)

                l4 = Label(top, text='Maths', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
                l4.place(x=25, y=180)

                l5 = Label(top, text='Social', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
                l5.place(x=25, y=235)

                l6 = Label(top, text='English', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
                l6.place(x=25, y=290)

                l7 = Label(top, text='Hindi', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
                l7.place(x=25, y=345)

                l8 = Label(top, text='Computer', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
                l8.place(x=25, y=400)

                # Entry boxes.
                rollval = StringVar()
                nameval = StringVar()
                sub1val = StringVar()
                sub2val = StringVar()
                sub3val = StringVar()
                sub4val = StringVar()
                sub5marksval = StringVar()
                sub6marksval = StringVar()

                e1 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=rollval)
                e1.place(x=200, y=15)

                e2 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=nameval)
                e2.place(x=200, y=70)

                e3 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=sub1val)
                e3.place(x=200, y=125)

                e4 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=sub2val)
                e4.place(x=200, y=180)

                e5 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=sub3val)
                e5.place(x=200, y=235)

                e6 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=sub4val)
                e6.place(x=200, y=290)

                e7 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=sub5marksval)
                e7.place(x=200, y=345)

                e8 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=sub6marksval)
                e8.place(x=200, y=400)

                # Button.
                b = Button(top, text='Update', font=('Arial Rounded MT Bold', 20), bg='royalblue', bd=3, width=12, command=update)
                b.place(x=130, y=460)

                top.bind('<Return>', lambda event: update())

                rollval.set(selection[0])
                nameval.set(selection[1])
                sub1val.set(selection[2])
                sub2val.set(selection[3])
                sub3val.set(selection[4])
                sub4val.set(selection[5])
                sub5marksval.set(selection[6])
                sub6marksval.set(selection[7])

            elif Class > 10:
                top.geometry('500x665+500+100')

                # Labels.
                current_item = tree.focus()
                values = tree.item(current_item)
                selection = values["values"]

                cur_roll = selection[0]
                cur_name = selection[1]
                cur_sub1 = selection[2]
                cur_sub2 = selection[3]
                cur_sub3 = selection[4]
                cur_sub4 = selection[5]
                cur_sub5name = selection[6]
                cur_sub5marks = selection[7]
                cur_sub6name = selection[8]
                cur_sub6marks = selection[9]

                cur_roll = str(cur_roll)
                cur_sub1 = str(cur_sub1)
                cur_sub2 = str(cur_sub2)
                cur_sub3 = str(cur_sub3)
                cur_sub4 = str(cur_sub4)
                cur_sub5marks = str(cur_sub5marks)
                cur_sub6marks = str(cur_sub6marks)

                l1 = Label(top, text='Roll No.', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                           borderwidth=2, width=12)
                l1.place(x=25, y=15)

                l2 = Label(top, text='Name', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                           borderwidth=2, width=12)
                l2.place(x=25, y=70)

                l3 = Label(top, text=sub1, font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                           borderwidth=2, width=12)
                l3.place(x=25, y=125)

                l4 = Label(top, text=sub2, font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                           borderwidth=2, width=12)
                l4.place(x=25, y=180)

                l5 = Label(top, text=sub3, font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                           borderwidth=2, width=12)
                l5.place(x=25, y=235)

                l6 = Label(top, text='English', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                           borderwidth=2, width=12)
                l6.place(x=25, y=290)

                l7 = Label(top, text='Op_Sub', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                           borderwidth=2, width=12)
                l7.place(x=25, y=345)

                l8 = Label(top, text='Op_Marks', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                           borderwidth=2, width=12)
                l8.place(x=25, y=400)

                l9 = Label(top, text='Add_Sub', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                           borderwidth=2, width=12)
                l9.place(x=25, y=455)

                l10 = Label(top, text='Add_Marks', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID,
                           borderwidth=2, width=12)
                l10.place(x=25, y=510)

                # Entry boxes.
                rollval = StringVar()
                nameval = StringVar()
                sub1val = StringVar()
                sub2val = StringVar()
                sub3val = StringVar()
                sub4val = StringVar()
                sub5marksval = StringVar()
                sub6marksval = StringVar()

                e1 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=rollval)
                e1.place(x=200, y=15)

                e2 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=nameval)
                e2.place(x=200, y=70)

                e3 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=sub1val)
                e3.place(x=200, y=125)

                e4 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=sub2val)
                e4.place(x=200, y=180)

                e5 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=sub3val)
                e5.place(x=200, y=235)

                e6 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=sub4val)
                e6.place(x=200, y=290)

                opsubs = ['None', 'IP', 'PE', 'Hindi', 'Music', 'Maths', 'Painting', 'Psychology']
                e7 = ttk.Combobox(top, font=('Agency FB', 25), values=opsubs,
                                  width=19, state='readonly')
                e7.place(x=200, y=345)
                if cur_sub5name == 'nan':
                    e7.current(0)
                else:
                    e7.current(opsubs.index(cur_sub5name))

                e8 = Entry(top, font=('Agency FB', 25), bd=2, width=20, textvariable=sub5marksval)
                e8.place(x=200, y=400)

                addsubs = ['None', 'PE', 'Music', 'Painting', 'Psychology']
                e9 = ttk.Combobox(top, font=('Agency FB', 25), values=addsubs, width=19,
                                  state='readonly')
                e9.place(x=200, y=455)
                if cur_sub6name == 'nan':
                    e9.current(0)
                else:
                    e9.current(addsubs.index(cur_sub6name))

                e10 = Entry(top, font=('Agency FB', 25), bd=2, width=20, textvariable=sub6marksval)
                e10.place(x=200, y=510)

                # Button.
                b = Button(top, text='Update', font=('Arial Rounded MT Bold', 20), bg='royalblue', bd=3, width=12,
                           command=update)
                b.place(x=130, y=570)

                top.bind('<Return>', lambda event: update())

                rollval.set(selection[0])
                nameval.set(selection[1])
                sub1val.set(selection[2])
                sub2val.set(selection[3])
                sub3val.set(selection[4])
                sub4val.set(selection[5])
                sub5marksval.set(selection[7])
                sub6marksval.set(selection[9])

            top.mainloop()

    def search():
        def search_record():
            val_ = entry.get()
            choice = combo.get()
            tree.delete(*tree.get_children())
            datas = connection.execute(text("select * from {} where {}='{}'".format(tb, choice, val_))).fetchall()
            if not datas:
                messagebox.showinfo('Info', "No record found with {} as '{}'.".format(choice, val_), parent=s_top)
                return
            for i in datas:
                if Class<=10:
                    record = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]]
                    tree.insert('', END, values=record)
                elif Class>10:
                    record = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]]
                    tree.insert('', END, values=record)
            s_top.destroy()

        s_top = Toplevel()
        s_top.title('Search Record')
        s_top.config(bg='cornflowerblue')
        s_top.grab_set()               # Button out of window not work.
        s_top.iconbitmap(other_win_icon_path)
        s_top.resizable(False, False)
        s_top.geometry('450x250+540+290')

        # Combobox.
        if Class<=10:
            vals = ('Roll_No', 'Student_Name', 'Science', 'Maths', 'Social', 'English', 'Hindi', 'Computer')
        elif Class>10:
            vals = ('Roll_No', 'Student_Name', sub1, sub2, sub3, 'English', 'Op_Sub', 'Op_marks', 'Add_Sub', 'Add_Marks')
        combo = ttk.Combobox(s_top, width=12, font=('Agency FB', 25, 'bold'), values=vals, state='readonly', justify=CENTER)
        combo.place(x=130, y=30)
        combo.current(0)

        # Entry box.
        val = StringVar()
        entry = Entry(s_top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', justify=CENTER, textvariable=val)
        entry.place(x=80, y=85)

        # Button.
        button = Button(s_top, text='Search', font=('Arial Rounded MT Bold', 20), bg='royalblue', bd=3, width=10, command=search_record)
        button.place(x=130, y=145)

        s_top.bind('<Return>', lambda event: search_record())
        s_top.mainloop()

    def refresh():
        tree.delete(*tree.get_children())
        datas=connection.execute(text('select * from {}'.format(tb))).fetchall()
        for i in datas:
            if Class<=10:
                record = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]]
                tree.insert('', END, values=record)

            elif Class>10:
                record = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]]
                tree.insert('', END, values=record)

    def delete():
        if not tree.selection():
            messagebox.showerror('Error!', 'Please select an item from the database.')
        else:
            selections = tree.selection()

            if len(selections) == 1:
                res = messagebox.askyesnocancel('Confirm Delete.',
                                                'Are you sure you want to delete the selected record from table {} in database srms_marksheet?'.format(
                                                    tb))
            else:
                res = messagebox.askyesnocancel('Confirm Delete.',
                                                'Are you sure you want to delete the selected records from table {} in database srms_marksheet?'.format(
                                                    tb))

            if res == True:
                for child in selections:
                    record = tree.item(child)['values']
                    roll = record[0]

                    tree.delete(child)
                    connection.execute(text("delete from {} where Student_ID='{}'".format(tb, roll)))
                    connection.commit()

                if len(selections) == 1:
                    messagebox.showinfo('Done!', 'The selected record was successfully deleted.')
                else:
                    messagebox.showinfo('Done!', 'The selected records were successfully deleted.')

    def clear():
        res=messagebox.askyesnocancel('Confirm Delete.', 'Are you sure you want to delete all the records from table {} in database srms_marksheet?'.format(tb))
        if res==True:
            connection.execute(text('Delete from {}'.format(tb)))
            connection.commit()
            tree.delete(*tree.get_children())
            messagebox.showinfo('Done', 'The records are successfully deleted.')

    def import_csv():
        try:
            csv_file_path = filedialog.askopenfilename()
            if csv_file_path != '':
                df = pd.read_csv('{}'.format(csv_file_path))
                if Class<=10:
                    if list(df.columns) != ['Roll_No', 'Student_Name', 'Science', 'Maths', 'Social', 'English', 'Hindi', 'Computer']:
                        messagebox.showerror('Invalid Data!', 'The data in CSV file does not match with the Treeview.')
                        return
                elif Class>10:
                    if list(df.columns) != ['Roll_No', 'Student_Name', sub1, sub2, sub3, 'English', 'Op_Sub', 'Op_Marks', 'Add_Sub', 'Add_Marks']:
                        messagebox.showerror('Invalid Data!', 'The data in CSV file does not match with the Treeview.')
                        return

                try:
                    df.to_sql('{}'.format(tb), connection, index=False, if_exists='append')            # fail, replace, append.
                    for index, row in df.iterrows():
                        tree.insert('', END, values=list(row))
                except:
                    messagebox.showerror('Duplicate Primary Key!', 'Multiple records with same Roll_No found. Make sure that the Roll_No is unique. ')
                    return
        except:
            messagebox.showerror('Invalid file type.', 'Please select a valid CSV file.')

    def export_csv():
        file_path = filedialog.asksaveasfilename()
        if file_path != '':
            if Class<=10:
                column = ['Roll_No', 'Student_Name', 'Science', 'Maths', 'Social', 'English', 'Hindi', 'Computer']
            elif Class>10:
                column = ['Roll_No', 'Student_Name', sub1, sub2, sub3, 'English', 'Op_Sub', 'Op_Marks', 'Add_Sub', 'Add_Marks']
            df = pd.read_sql('select * from {}'.format(tb), connection, columns=column)
            path = '{}.csv'.format(file_path)
            df.to_csv(path, index=False)
            messagebox.showinfo('Successfully saved.', '{} has been successfully saved.'.format(path))

    def plot():
        def plot_graph():

            plt.figure(figsize=(8, 5))
            plt.grid(True)
            plt.title('Graph')
            plt.xlabel('Subjects')
            plt.ylabel('Marks')
            plt.xlim(0, 7)
            plt.ylim(0, 100)

            # Plotting.
            marks_list = []      # For Bar chart.
            roll_list = []
            for child in selections:
                record = tree.item(child)['values']
                if Class <= 10:
                    subs = ['Science', 'Maths', 'Social', 'English', 'Hindi', 'Computer']
                    marks = [record[2], record[3], record[4], record[5], record[6], record[7]]
                    marks_list.append(marks)
                elif Class > 10:
                    if len(selections)>1:
                        subs = [sub1, sub2, sub3, 'English', 'Optional', 'Additional']
                    else:
                        opsub = record[6]
                        addsub = record[8]
                        subs = [sub1, sub2, sub3, 'English', opsub, addsub]
                    marks = [record[2], record[3], record[4], record[5], record[7], record[9]]
                    marks_list.append(marks)

                roll = 'Roll_No-' + str(record[0])
                roll_list.append(roll)

                if combo.get() == 'Line':
                    plt.plot(np.arange(1, 7, 1), marks, label=roll)
                elif combo.get() == 'Scatter':
                    plt.scatter(np.arange(1, 7, 1), marks, label=roll)

            if combo.get() == 'Pie':            # Pie Chart cannot be used for multiple records.
                plt.xlabel('')
                plt.ylabel('')
                plt.pie(marks_list[0], labels=subs, colors=['red', 'cyan', 'pink', 'lightgreen', 'yellow', 'silver'], autopct='%3.1f%%', explode=[0.15, 0.05, 0.1, 0.15, 0.1, 0.2])

            elif combo.get() == 'Bar':
                X = np.arange(1, 7)         # Position of Bars on X-axis.
                Y = 0                       # To shift Position of Bars on X-axis.
                i = 0                       # Index of roll in roll_list.
                for marks in marks_list:
                    if len(selections) == 1:
                        plt.bar(X, marks_list[0], color='orange', label=roll_list[0])
                    else:
                        plt.bar(X+Y, marks, width=0.15, label=roll_list[i])
                        Y+=0.15
                        i+=1

            if combo.get() != 'Pie':
                plt.xticks(np.arange(1, 7, 1), subs)
                plt.legend(loc=1)

            plt.show()

        if not tree.selection():
            messagebox.showerror('Error!', 'Please select an item from the database.')
        else:
            selections = tree.selection()

            # Checking for empty marks.
            for child in selections:
                record = tree.item(child)['values']
                if Class <= 10:
                    marks = [record[2], record[3], record[4], record[5], record[6], record[7]]
                elif Class > 10:
                    marks = [record[2], record[3], record[4], record[5], record[7], record[9]]
                for i in marks:
                    try:
                        int(i)
                    except:
                        messagebox.showerror('Cannot Plot!', 'Empty marks found in subject(s).')
                        return


            # Creating plot selection window.
            win = Toplevel()
            win.overrideredirect(True)
            win.geometry('300x200+600+350')
            win.configure(bg='cornflowerblue', relief=RIDGE, borderwidth=5)
            win.grab_set()

            close_img = ImageTk.PhotoImage(Image.open(close_icon_path))
            def close():
                win.destroy()
            Button(win, image=close_img, border=0, command=close, bg='cornflowerblue', activebackground='cornflowerblue').place(x=260,y=5)

            Label(win, text='Graph Type', font=('Microsoft YaHei UI Light', 20, 'bold'),
                  bg='cornflowerblue').place(x=30, y=40)
            combo = ttk.Combobox(win, width=15, values=['Line', 'Scatter', 'Pie', 'Bar'], font=('Microsoft YaHei UI Light', 15, 'bold'),
                                 state='readonly')
            combo.current(0)
            combo.place(x=30, y=90)
            if len(selections)>1:
                combo.config(values=['Line', 'Scatter', 'Bar'])

            Button(win, text='Plot', font=('Microsoft YaHei UI Light', 12, 'bold'), bg='royalblue', command=plot_graph).place(x=235, y=145)

            win.mainloop()

    def plot_all():
        datas = connection.execute(text('select * from {}'.format(tb))).fetchall()

        # Checking for any empty value.
        for tup in datas:
            if Class <= 10:
                marks = [tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]]
                for mark in marks:
                    try:
                        int(mark)
                    except:
                        messagebox.showerror('Cannot Plot!', 'Empty marks found in subject(s).')
                        return
            elif Class > 10:
                marks = [tup[2], tup[3], tup[4], tup[5], tup[7], tup[9]]
                for mark in marks:
                    try:
                        int(mark)
                    except:
                        messagebox.showerror('Cannot Plot!', 'Empty marks found in subject(s).')
                        return

        def plotall_graph():
            if Class <= 10:
                subs = ['Science', 'Maths', 'Social', 'English', 'Hindi', 'Computer']
            elif Class > 10:
                subs = [sub1, sub2, sub3, 'English', 'Optional', 'Additional']
            plt.figure(figsize=(8, 5))
            plt.grid(True)
            plt.title('Graph')
            plt.xlabel('Subjects')
            plt.ylabel('Marks')
            plt.xlim(0, 7)
            plt.ylim(0, 100)
            plt.xticks(np.arange(1, 7, 1), subs)
            for tup in datas:
                if Class <= 10:
                    roll = 'Roll_No-' + tup[0]
                    marks = [int(tup[2]), int(tup[3]), int(tup[4]), int(tup[5]), int(tup[6]), int(tup[7])]
                elif Class > 10:
                    roll = 'Roll_No-'+tup[0]
                    marks = [int(tup[2]), int(tup[3]), int(tup[4]), int(tup[5]), int(tup[7]), int(tup[9])]

                if combo.get()=='Line':
                    plt.plot(np.arange(1, 7, 1), marks, label=roll)
                elif combo.get()=='Scatter':
                    plt.scatter(np.arange(1, 7, 1), marks, label=roll)

            plt.legend(loc=1)
            plt.show()

        # Creating plot selection window.
        win = Toplevel()
        win.overrideredirect(True)
        win.geometry('300x200+600+350')
        win.configure(bg='cornflowerblue', relief=RIDGE, borderwidth=5)
        win.grab_set()

        close_img = ImageTk.PhotoImage(Image.open(close_icon_path))

        def close():
            win.destroy()
        Button(win, image=close_img, border=0, command=close, bg='cornflowerblue',
               activebackground='cornflowerblue').place(x=260, y=5)

        Label(win, text='Graph Type', font=('Microsoft YaHei UI Light', 20, 'bold'),
              bg='cornflowerblue').place(x=30, y=40)
        combo = ttk.Combobox(win, width=15, values=['Line', 'Scatter'],
                             font=('Microsoft YaHei UI Light', 15, 'bold'),
                             state='readonly')
        combo.current(0)
        combo.place(x=30, y=90)

        Button(win, text='Plot', font=('Microsoft YaHei UI Light', 12, 'bold'), bg='royalblue',
               command=plotall_graph).place(x=235, y=145)

        win.mainloop()

    # FRAME.

    f1 = Frame(root, bg='silver', relief=SOLID, borderwidth=5)
    f1.place(x=155, y=10, width=1100, height=630)

    # Buttons.

    def btn(text, command, x, y, state):
        def on_enter(self):
            button.config(font=('Agency FB', 22, 'bold'))

        def on_leave(self):
            button.config(font=('Agency FB', 20, 'bold'))

        button = Button(root, text=text, font=('Agency FB', 20, 'bold'), bg='steelblue',  activebackground='black',
                        activeforeground='white', disabledforeground='grey30', bd=5, width=10, command=command, state=state)
        button.place(x=x, y=y)

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

        return button

    Add_btn = btn('Add', add, 20, 100, DISABLED)
    Edit_btn = btn('Edit', edit, 20, 200, DISABLED)
    Del_btn = btn('Delete', delete, 20, 300, DISABLED)
    Search_btn = btn('Search', search, 20, 400, NORMAL)
    Refresh_btn = btn('Refresh', refresh, 20, 500, NORMAL)

    Clear_btn = btn('Clear', clear, 1275, 100, DISABLED)
    Import_btn = btn('Import', import_csv, 1275, 200, DISABLED)
    Export_btn = btn('Export', export_csv, 1275, 300, DISABLED)
    Plot_btn = btn('Plot', plot, 1275, 400, NORMAL)
    Plot_all_btn = btn('Plot All', plot_all, 1275, 500, NORMAL)

    # Changing Button state when user is admin.
    Buttons = [Add_btn, Edit_btn, Del_btn, Clear_btn, Import_btn, Export_btn]
    def btn_state():
        for button in Buttons:
            button['state'] = 'normal'
    file = open(admins_text_file, 'r')
    data = file.read()
    file.close()
    dict = ast.literal_eval(data)
    file = open(user_val_text_file, 'r')
    data = file.read()
    file.close()
    cur_user_info = ast.literal_eval(data)
    cur_user = cur_user_info[0]
    if cur_user in dict.keys():
        btn_state()

    # Getting Values.
    file = open(tb_values_text_file, 'r')
    data = file.read()
    val_list = ast.literal_eval(data)
    tb = val_list[0]
    Class = int(val_list[1])
    stream = val_list[2]
    file.close()

    # Treeview:
    if Class<=10:
        tree = ttk.Treeview(f1, height=100, columns=('a', "b", 'c', "d", "e", "f", "g", 'h'))
        X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
        X_scroller.pack(side=BOTTOM, fill=X)
        Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
        Y_scroller.pack(side=RIGHT, fill=Y)
        tree.config(xscrollcommand=X_scroller.set)
        tree.config(yscrollcommand=Y_scroller.set)
        tree.heading('a', text='Roll No.', anchor=W)
        tree.heading('b', text='Student_Name', anchor=W)
        tree.heading('c', text='Science', anchor=W)
        tree.heading('d', text='Maths', anchor=W)
        tree.heading('e', text='Social', anchor=W)
        tree.heading('f', text='English', anchor=W)
        tree.heading('g', text='Hindi', anchor=W)
        tree.heading('h', text='Computer', anchor=W)
        tree['show'] = 'headings'
        tree.column('#1', width=130, stretch=NO)
        tree.column('#2', width=300, stretch=NO)
        tree.column('#3', width=105, stretch=NO)
        tree.column('#4', width=105, stretch=NO)
        tree.column('#5', width=105, stretch=NO)
        tree.column('#6', width=105, stretch=NO)
        tree.column('#7', width=105, stretch=NO)
        tree.column('#8', width=105, stretch=NO)
        tree.place(y=0, relwidth=1, relheight=1, relx=0)

        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Arial Rounded MT Bold', 16), foreground='black')
        style.configure('Treeview', font=('Microsoft YaHei ', 14, 'bold'), background='lavender')

    if Class>10:
        global sub1, sub2, sub3
        if stream == 'pcm' or stream == 'PCM':
            sub1 = 'Physics'
            sub2 = 'Chemistry'
            sub3 = 'Maths'
        elif stream == 'pcb' or stream == 'PCB':
            sub1 = 'Physics'
            sub2 = 'Chemistry'
            sub3 = 'Biology'
        elif stream == 'arts' or stream == 'Arts':
            sub1 = 'Pol_Sci.'
            sub2 = 'Geography'
            sub3 = 'History'
        elif stream == 'commerce' or stream == 'Commerce':
            sub1 = 'Accountancy'
            sub2 = 'Business'
            sub3 = 'Economics'

        tree = ttk.Treeview(f1, height=100, columns=('a', "b", 'c', "d", "e", "f", "g", 'h', 'i', 'j'))
        X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
        X_scroller.pack(side=BOTTOM, fill=X)
        Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
        Y_scroller.pack(side=RIGHT, fill=Y)
        tree.config(xscrollcommand=X_scroller.set)
        tree.config(yscrollcommand=Y_scroller.set)
        tree.heading('a', text='Roll No.', anchor=W)
        tree.heading('b', text='Student_Name', anchor=W)
        tree.heading('c', text=sub1, anchor=W)
        tree.heading('d', text=sub2, anchor=W)
        tree.heading('e', text=sub3, anchor=W)
        tree.heading('f', text='English', anchor=W)
        tree.heading('g', text='Op_Sub', anchor=W)
        tree.heading('h', text='Op_Marks', anchor=W)
        tree.heading('i', text='Add_Sub', anchor=W)
        tree.heading('j', text='Add_Marks', anchor=W)
        tree['show'] = 'headings'
        tree.column('#1', width=90, stretch=NO)
        tree.column('#2', width=175, stretch=NO)
        tree.column('#3', width=90, stretch=NO)
        tree.column('#4', width=120, stretch=NO)
        tree.column('#5', width=90, stretch=NO)
        tree.column('#6', width=90, stretch=NO)
        tree.column('#7', width=90, stretch=NO)
        tree.column('#8', width=110, stretch=NO)
        tree.column('#9', width=100, stretch=NO)
        tree.column('#10', width=120, stretch=NO)
        tree.place(y=0, relwidth=1, relheight=1, relx=0)

        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Arial Rounded MT Bold', 16), foreground='black')
        style.configure('Treeview', font=('Microsoft YaHei ', 14, 'bold'), background='lavender')

    refresh()

    # Backbutton.
    def back():
        connection.close()
        root.destroy()
        import home_screen
        home_screen.main()
    back_icon = ImageTk.PhotoImage(Image.open(back_icon_path))
    back_btn = Button(root, image=back_icon, bg='DodgerBlue4', border=0, activebackground='steelblue', command=back)
    back_btn.place(x=5, y=5)
    def on_enter(self):
        back_btn['background']='steelblue'
    def on_leave(self):
        back_btn['background']='DodgerBlue4'
    back_btn.bind('<Enter>', on_enter)
    back_btn.bind('<Leave>', on_leave)

    def on_closing():
        if messagebox.askokcancel("Confirm Exit", "Are you sure you want to exit?"):
            root.destroy()
    root.protocol('WM_DELETE_WINDOW', on_closing)

    root.mainloop()