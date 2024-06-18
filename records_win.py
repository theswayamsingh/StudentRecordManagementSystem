import pandas as pd
from tkinter import *                         # pip install future (in pycharm).
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import ImageTk, Image
from sqlalchemy import create_engine as ce
import os,sys

# Getting required files.

if getattr(sys, 'frozen', False):
    main_win_icon_path = os.path.join(sys._MEIPASS,"resources","icon.ico")              # sys._MEIPASS is only usable in exe.
    other_win_icon_path = os.path.join(sys._MEIPASS,"resources","title_logo.ico")
    back_icon_path = os.path.join(sys._MEIPASS, 'resources', 'back-arrow.png')
else:
    main_win_icon_path = os.path.join("resources","icon.ico")
    other_win_icon_path = os.path.join("resources","title_logo.ico")
    back_icon_path = os.path.join('resources', 'back-arrow.png')

def main():
    global connection, info, tb
    # Main Window.

    connection = ''
    info = ''
    tb = ''

    root = Tk()
    root.title('Ledger Management')
    root.iconbitmap(main_win_icon_path)
    root.geometry('1174x700+180+60')
    root.resizable(False,False)
    root.config(bg='Dodgerblue4')

    # FUNCTIONS.

    def Connect():
        # Checking Connection.
        if tb:
            if connection and (info and info==[('Student_ID', 'varchar(10)', 'NO', 'PRI', None, ''), ('Student_Name', 'varchar(50)', 'YES', '', None, ''), ('Class', 'varchar(10)', 'YES', '', None, ''), ('Gender', 'varchar(20)', 'YES', '', None, ''), ('Phone', 'varchar(10)', 'YES', '', None, ''), ('Email', 'varchar(50)', 'YES', '', None, ''), ('Address', 'varchar(100)', 'YES', '', None, '')]):
                messagebox.showinfo('Already Connected!', 'You are already connected to database.')
                return

        def sql_connect():
            global connection
            host = hostval.get()                 # Available below.
            user = userval.get()
            password = passwordval.get()

            try:
                engine = ce("mysql+pymysql://{}:{}@{}".format(user, password, host))
                connection = engine.connect()
                sql.destroy()
                messagebox.showinfo('Connection succeed!', 'Successfully connected to MySQL Server.')
            except:
                messagebox.showerror("Connection error!", 'Incorrect information. Please try again.', parent=sql)
                return             # The code will not run forward.

            try:
                connection.execute('create database srms_records')
                connection.execute('use srms_records')
            except:
                connection.execute('use srms_records')

            connection.close()
            engine = ce("mysql+pymysql://{}:{}@{}/srms_records".format(user, password, host))
            connection = engine.connect()

            def tb_connect():
                global tb, info
                tb = tbval.get()
                if tb == '':
                    messagebox.showerror('Error!', 'Please enter a table name.')
                    return

                try:
                    connection.execute("CREATE TABLE {} (Student_ID varchar(10) Primary Key, Student_Name varchar(50) ,Class varchar(10), Gender varchar(20), Phone varchar(10), Email varchar(50), Address varchar(100))".format(tb))
                    tablewin.destroy()
                    btn_state()
                    messagebox.showinfo('Table Created.', 'Table has been created successfully.')
                except:
                    info=connection.execute('desc {}'.format(tb)).fetchall()
                    if info!=[('Student_ID', 'varchar(10)', 'NO', 'PRI', None, ''), ('Student_Name', 'varchar(50)', 'YES', '', None, ''), ('Class', 'varchar(10)', 'YES', '', None, ''), ('Gender', 'varchar(20)', 'YES', '', None, ''), ('Phone', 'varchar(10)', 'YES', '', None, ''), ('Email', 'varchar(50)', 'YES', '', None, ''), ('Address', 'varchar(100)', 'YES', '', None, '')]:
                        messagebox.showerror('Invalid Table!', 'The description of the table does not match with the Treeview.')
                        return
                    else:
                        tablewin.destroy()
                        btn_state()
                        refresh()
                        messagebox.showinfo('Table Connected.', 'Table has been connected successfully.')

            tablewin = Toplevel()
            tablewin.title('Table Connection.')
            tablewin.config(bg='cornflowerblue')
            tablewin.grab_set()  # Buttons that are out of window will not work.
            tablewin.iconbitmap(other_win_icon_path)
            tablewin.resizable(False, False)
            tablewin.geometry('470x250+530+280')

            l1 = Label(tablewin, text='Table', font=('Agency FB', 31, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l1.place(x=125, y=30)

            tables = connection.execute('show tables').fetchall()
            tables_list = []
            for i in tables:
                table = i[0]
                tables_list.append(table)
            tbval = StringVar()
            Combo = ttk.Combobox(tablewin, values=tables_list, font=('Agency FB', 26), width=12,textvariable=tbval, justify=CENTER)
            Combo.place(x=123, y=100)

            b1 = Button(tablewin, text='Ok', font=('Arial Rounded MT Bold', 20), bg='royalblue', bd=3, width=7, command=tb_connect)
            b1.place(x=158, y=170)

            tablewin.bind('<Return>', lambda event: tb_connect())


        sql = Toplevel()
        sql.title('MySQL Server Connection')
        sql.config(bg='cornflowerblue')
        sql.grab_set()                 # Buttons that are out of window will not work.
        sql.iconbitmap(other_win_icon_path)
        sql.resizable(False, False)
        sql.geometry('470x250+530+280')

        # Labels.
        dbl1 = Label(sql, text='Host', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=10)
        dbl1.place(x=50, y=15)

        dbl2 = Label(sql, text='User', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=10)
        dbl2.place(x=50, y=70)

        dbl3 = Label(sql, text='Password', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=10)
        dbl3.place(x=50, y=125)

        # Entry Boxes.
        hostval = StringVar()
        userval = StringVar()
        passwordval = StringVar()

        hostval.set('localhost')
        userval.set('root')

        e1 = Entry(sql, font=('Agency FB', 25), bd=2, width=15, bg='lavender', textvariable=hostval)
        e1.place(x=210,y=15)

        e2 = Entry(sql, font=('Agency FB', 25), bd=2, width=15, bg='lavender', textvariable=userval)
        e2.place(x=210, y=70)

        e3 = Entry(sql, font=('Agency FB', 25), bd=2, width=15, bg='lavender', textvariable=passwordval, show='*')
        e3.place(x=210, y=125)

        # Button.

        dbb = Button(sql, text='Connect', font=('Arial Rounded MT Bold', 20), bg='royalblue', bd=3, command=sql_connect)
        dbb.place(x=150, y=180)

        sql.bind('<Return>', lambda event:sql_connect())                        # To bind the button with enter key.
        sql.mainloop()

    def add():
        def submit():
            id = idval.get()
            name = nameval.get()
            Class = Classval.get()
            gender = Genderval.get()
            phone = phoneval.get()
            email = emailval.get()
            address = addressval.get()

            if len(id)>10:
                messagebox.showerror('Invalid ID!', 'The length of Student_ID exceeds limit.')
                return
            if id=='' or name=='':
                messagebox.showerror('Error!', 'Student ID and Student Name are must. ')
                return

            x = str(phone)  # To check the length of phone.
            if (len(x)!=0 and len(x)<10) or (len(x)!=0 and len(x)>10):
                messagebox.showerror('Invalid Phone', 'Please enter a valid phone number.')
                return
            if len(x)!=0:
                try:  # To check the type of phone.
                    phone = int(x)
                except:
                    messagebox.showerror('Invalid Phone', 'Please enter a valid phone number.')
                    return

            try:
                connection.execute('insert into {} values (%s, %s, %s, %s, %s, %s, %s)'.format(tb), (id, name, Class, gender, phone, email, address))
                res = messagebox.askyesno('Record added successfully!', 'Record with ID {} and Name {} added successfully. Do you want to clear the fill-up form?'.format(id, name), parent=addtop)
                if res == True:
                    idval.set('')
                    nameval.set('')
                    Classval.set('')
                    Genderval.set('')
                    phoneval.set('')
                    emailval.set('')
                    addressval.set('')

            except:
                messagebox.showerror('Duplicate Primary Key!', 'Multiple records with same Student ID found. Make sure that the Student ID is unique.', parent=addtop)

            refresh()

        addtop = Toplevel()
        addtop.title('Add Record')
        addtop.config(bg='cornflowerblue')
        addtop.grab_set()  # Button out of window not work.
        addtop.iconbitmap(other_win_icon_path)
        addtop.resizable(False, False)
        addtop.geometry('500x530+500+180')

        # Labels.
        l1 = Label(addtop, text='Student ID', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
        l1.place(x=25, y=15)

        l2 = Label(addtop, text='Student Name', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
        l2.place(x=25, y=70)

        l3 = Label(addtop, text='Class', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
        l3.place(x=25, y=125)

        l4 = Label(addtop, text='Gender', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
        l4.place(x=25, y=180)

        l5 = Label(addtop, text='Phone', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
        l5.place(x=25, y=235)

        l6 = Label(addtop, text='Email', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
        l6.place(x=25, y=290)

        l7 = Label(addtop, text='Address', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
        l7.place(x=25, y=345)

        l8 = Label(addtop, text='*Student ID and Name are must.', font=('Calibri', 18, 'bold'), bg='cornflowerblue', relief=GROOVE)
        l8.place(x=25, y=400)

        # Entry boxes.
        idval = StringVar()
        nameval = StringVar()
        Classval = StringVar()
        Genderval = StringVar()
        phoneval = StringVar()
        emailval = StringVar()
        addressval = StringVar()

        e1 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=idval)
        e1.place(x=200, y=15)

        e2 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=nameval)
        e2.place(x=200, y=70)

        e3 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=Classval)
        e3.place(x=200, y=125)

        e4 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=Genderval)
        e4.place(x=200, y=180)

        e5 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=phoneval)
        e5.place(x=200, y=235)

        e6 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=emailval)
        e6.place(x=200, y=290)

        e7 = Entry(addtop, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=addressval)
        e7.place(x=200, y=345)

        # Button.
        b = Button(addtop, text='Submit', font=('Arial Rounded MT Bold', 20), bg='royalblue', bd=3, width=12, command=submit)
        b.place(x=130, y=450)

        addtop.bind('<Return>', lambda event: submit())
        addtop.mainloop()

    def edit():
        def update():
            new_id = idval.get()
            new_name = nameval.get()
            new_class = Classval.get()
            new_gender = Genderval.get()
            new_phone = phoneval.get()
            new_email = emailval.get()
            new_address = addressval.get()

            if len(new_id)>10:
                messagebox.showerror('Invalid ID!', 'The length of Student_ID exceeds limit.')
                return
            if new_id=='' or new_name=='':
                messagebox.showerror('Error!', 'Student ID and Student Name are must. ')
                return

            x = str(new_phone)  # To check the length of phone.
            if (len(x) != 0 and len(x) < 10) or (len(x) != 0 and len(x) > 10):
                messagebox.showerror('Invalid Phone', 'Please enter a valid phone number.')
                return
            if len(x) != 0:
                try:  # To check the type of phone.
                    new_phone = int(x)
                except:
                    messagebox.showerror('Invalid Phone', 'Please enter a valid phone number.')
                    return

            if cur_id == new_id and cur_name == new_name and cur_class == new_class and cur_gender == new_gender and cur_phone == new_phone and cur_email == new_email and cur_address == new_address:
                messagebox.showinfo('Nothing to update', 'Please make some changes in order to update the record.', parent=top)
                return
            else:
                try:
                    connection.execute("update {} set Student_ID=%s, Student_Name=%s, Class=%s, Gender=%s, Phone=%s,Email=%s,Address=%s where Student_ID=%s".format(tb), (new_id, new_name, new_class, new_gender, new_phone, new_email, new_address, cur_id))
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
            top.geometry('500x530+500+180')

            # Labels.
            current_item = tree.focus()
            values = tree.item(current_item)
            selection = values["values"]

            cur_id = selection[0]
            cur_name = selection[1]
            cur_class = selection[2]
            cur_gender = selection[3]
            cur_phone = selection[4]
            cur_email = selection[5]
            cur_address = selection[6]

            l1 = Label(top, text='Student ID', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l1.place(x=25, y=15)

            l2 = Label(top, text='Student Name', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l2.place(x=25, y=70)

            l3 = Label(top, text='Class', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l3.place(x=25, y=125)

            l4 = Label(top, text='Gender', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l4.place(x=25, y=180)

            l5 = Label(top, text='Phone', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l5.place(x=25, y=235)

            l6 = Label(top, text='Email', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l6.place(x=25, y=290)

            l7 = Label(top, text='Address', font=('Agency FB', 25, 'bold'), bg='cornflowerblue', relief=SOLID, borderwidth=2, width=12)
            l7.place(x=25, y=345)

            # Entry boxes.
            idval = StringVar()
            nameval = StringVar()
            Classval = StringVar()
            Genderval = StringVar()
            phoneval = StringVar()
            emailval = StringVar()
            addressval = StringVar()

            e1 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=idval)
            e1.place(x=200, y=15)

            e2 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=nameval)
            e2.place(x=200, y=70)

            e3 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=Classval)
            e3.place(x=200, y=125)

            e4 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=Genderval)
            e4.place(x=200, y=180)

            e5 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=phoneval)
            e5.place(x=200, y=235)

            e6 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=emailval)
            e6.place(x=200, y=290)

            e7 = Entry(top, font=('Agency FB', 25), bd=2, width=20, bg='lavender', textvariable=addressval)
            e7.place(x=200, y=345)

            # Button.
            b = Button(top, text='Update', font=('Arial Rounded MT Bold', 20), bg='royalblue', bd=3, width=12, command=update)
            b.place(x=130, y=420)

            top.bind('<Return>', lambda event: update())

            idval.set(selection[0])
            nameval.set(selection[1])
            Classval.set(selection[2])
            Genderval.set(selection[3])
            phoneval.set(selection[4])
            emailval.set(selection[5])
            addressval.set(selection[6])

            top.mainloop()

    def search():
        def search_record():
            val_ = entry.get()
            choice = combo.get()
            tree.delete(*tree.get_children())
            datas = connection.execute("select * from {} where {}='{}'".format(tb, choice, val_)).fetchall()
            if not datas:
                messagebox.showinfo('Info', "No record found with {} as '{}'.".format(choice, val_), parent=s_top)
                return
            for i in datas:
                record = [i[0], i[1], i[2], i[3], i[4], i[5], i[6]]
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
        combo = ttk.Combobox(s_top, width=12, font=('Agency FB', 25, 'bold'), values=('Student_ID', 'Student_Name', 'Class', 'Gender', 'Phone', 'Email', 'Address'), state='readonly', justify=CENTER)
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

    def delete():
        if not tree.selection():
            messagebox.showerror('Error!', 'Please select an item from the database.')
        else:
            selections = tree.selection()

            if len(selections)==1:
                res = messagebox.askyesnocancel('Confirm Delete.',
                                                'Are you sure you want to delete the selected record from table {} in database srms_records?'.format(tb))
            else:
                res = messagebox.askyesnocancel('Confirm Delete.',
                                                'Are you sure you want to delete the selected records from table {} in database srms_records?'.format(tb))

            if res == True:
                for child in selections:
                    selection = tree.item(child)['values']
                    id_ = selection[0]

                    tree.delete(child)
                    connection.execute("delete from {} where Student_ID='{}'".format(tb, id_))

                if len(selections)==1:
                    messagebox.showinfo('Done!', 'The selected record was successfully deleted.')
                else:
                    messagebox.showinfo('Done!', 'The selected records were successfully deleted.')

    def refresh():
        tree.delete(*tree.get_children())
        datas=connection.execute('select * from {}'.format(tb)).fetchall()
        for i in datas:
            record = [i[0], i[1], i[2], i[3], i[4], i[5], i[6]]
            tree.insert('', END, values=record)

    def import_csv():
        try:
            csv_file_path = filedialog.askopenfilename()
            if csv_file_path != '':
                df = pd.read_csv('{}'.format(csv_file_path), header=0)
                try:
                    df.to_sql('{}'.format(tb), connection, index=False, if_exists='append')            # fail, replace, append.
                    for index, row in df.iterrows():
                        tree.insert('', END, values=list(row))
                except:
                    messagebox.showerror('Duplicate Primary Key!', 'Multiple records with same Student ID found. Make sure that the Student ID is unique. ')
                    return
        except:
            messagebox.showerror('Invalid file type.', 'Please select a valid CSV file.')

    def export_csv():
        file_path = filedialog.asksaveasfilename()
        if file_path != '':
            columns = ['Student_ID', 'Student_Name', 'Class', 'Gender', 'Phone', 'Email', 'Address']
            df = pd.read_sql('select * from {}'.format(tb), connection, columns=columns)
            path = '{}.csv'.format(file_path)
            df.to_csv(path, index=False)
            messagebox.showinfo('Successfully saved.', '{} has been successfully saved.'.format(path))

    def clear():
        res=messagebox.askyesnocancel('Confirm Delete.', 'Are you sure you want to delete all the records from table {} in database srms_records?'.format(tb))
        if res==True:
            connection.execute('Delete from {}'.format(tb))
            tree.delete(*tree.get_children())
            messagebox.showinfo('Done', 'The records are successfully deleted.')

    # FRAME.

    f1 = Frame(root, bg='silver', relief=SOLID, borderwidth=5)
    f1.place(x=10, y=80, width=1155, height=605)

    # Buttons.

    def btn1(text, command, x, y, state):
        def on_enter(self):
            button.config(font=('Agency FB', 20, 'bold'))

        def on_leave(self):
            button.config(font=('Agency FB', 18, 'bold'))

        button = Button(root, text=text, font=('Agency FB', 18, 'bold'), bg='steelblue', bd=5, width=10, command=command, state=state, disabledforeground='grey30')
        button.place(x=x, y=y)

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

        return button

    Add_btn = btn1('Add', add, 40, 10, DISABLED)
    Edit_btn = btn1('Edit', edit, 165, 10, DISABLED)
    Search_btn = btn1('Search', search, 290, 10, DISABLED)
    Delete_btn = btn1('Delete', delete, 415, 10, DISABLED)
    Refresh_btn = btn1('Refresh', refresh, 540, 10, DISABLED)

    def btn2(text, command, x, y):
        def on_enter(self):
            button.config(font=('Arial black', 18, 'bold'))

        def on_leave(self):
            button.config(font=('Arial black', 17, 'bold'))

        button = Button(root, text=text, font=('Arial black', 17, 'bold'), bg='royalblue', bd=5, width=20, command=command)
        button.place(x=x, y=y)

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

        return button

    Connect_btn = btn2('Connect', Connect, 800, 10)

    # Scrollbar.

    s1 = Scrollbar(f1, orient=HORIZONTAL)
    s1.pack(side=BOTTOM, fill=X)

    s2 = Scrollbar(f1, orient=VERTICAL)
    s2.pack(side=RIGHT, fill=Y)

    # Data Treeview.

    tree = ttk.Treeview(f1, columns=('a','b','c','d','e','f','g'), xscrollcommand=s1.set, yscrollcommand=s2.set)
    tree.pack(fill=BOTH, expand=1)

    s1.config(command=tree.xview)
    s2.config(command=tree.yview)

    tree.heading('a', text='Student ID', anchor=W)
    tree.heading('b', text='Student Name', anchor=W)
    tree.heading('c', text='Class', anchor=W)
    tree.heading('d', text='Gender', anchor=W)
    tree.heading('e', text='Phone', anchor=W)
    tree.heading('f', text='Email', anchor=W)
    tree.heading('g', text='Address', anchor=W)

    tree['show'] = 'headings'               # With this, additional column will be removed.

    style = ttk.Style()
    style.configure('Treeview.Heading', font=('Arial Rounded MT Bold', 18), foreground='navy')
    style.configure('Treeview', font=('Arial Rounded MT Bold', 14), background='lavender')

    def btn3(text, command, x, y, state):
        def on_enter(self):
            button.config(font=('Arial black', 19))

        def on_leave(self):
            button.config(font=('Arial black', 18))

        button = Button(f1, text=text, font=('Arial black', 18), bg='steelblue', bd=5, command=command, state=state, disabledforeground='grey30')
        button.place(x=x, y=y)

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

        return button

    Import_btn = btn3('Import', import_csv, 10, 500, DISABLED)
    Export_btn = btn3('Export', export_csv, 150, 500, DISABLED)

    def btn4(text, command, x, y, state):
        def on_enter(self):
            button.config(font=('Agency FB', 20, 'bold'))

        def on_leave(self):
            button.config(font=('Agency FB', 18, 'bold'))

        button = Button(f1, text=text, font=('Agency FB', 18, 'bold'), bg='royalblue', bd=5, width=10, command=command, state=state, disabledforeground='grey30')
        button.place(x=x, y=y)

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

        return button

    Clear_btn = btn4('Clear', clear, 1000, 500, DISABLED)

    Buttons = [Add_btn, Edit_btn, Search_btn, Delete_btn, Refresh_btn, Connect_btn, Import_btn, Export_btn, Clear_btn]
    def btn_state():
        for button in Buttons:
            button['state'] = 'normal'

    # Backbutton.
    def back():
        root.destroy()
        import main_win
        main_win.main()
    back_icon = ImageTk.PhotoImage(Image.open(back_icon_path))
    back_btn = Button(root, image=back_icon, bg='Dodgerblue4', border=0, activebackground='DodgerBlue4', command=back)
    back_btn.place(x=5, y=5)
    def on_enter(self):
        back_btn['background']='DodgerBlue3'
    def on_leave(self):
        back_btn['background']='DodgerBlue4'
    back_btn.bind('<Enter>', on_enter)
    back_btn.bind('<Leave>', on_leave)

    def on_closing():
        if messagebox.askokcancel("Confirm Exit", "Are you sure you want to exit?"):
            root.destroy()
    root.protocol('WM_DELETE_WINDOW', on_closing)

    root.mainloop()