from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import os, sys, ast
from sqlalchemy import create_engine as ce
import sqlite3


# Getting required files.

if getattr(sys, 'frozen', False):
    main_win_icon_path = os.path.join(sys._MEIPASS,"resources","icon.ico")              # sys._MEIPASS is only usable in exe.
    other_win_icon_path = os.path.join(sys._MEIPASS, "resources", "title_logo.ico")
    close_icon_path = os.path.join(sys._MEIPASS, 'resources', 'close.png')
    open_icon_path = os.path.join(sys._MEIPASS, 'resources', 'open.png')
    back_icon_path = os.path.join(sys._MEIPASS, 'resources', 'back-arrow.png')
    main_win_bg_path = os.path.join(sys._MEIPASS, 'resources', 'main_win.png')
    main_close_icon_path = os.path.join(sys._MEIPASS, 'resources', 'main_close.png')
    about_close_icon_path = os.path.join(sys._MEIPASS, 'resources', 'about_close.png')

    admins_text_file = os.path.join(sys._MEIPASS, 'resources', 'admins.txt')
    users_text_file = os.path.join(sys._MEIPASS, 'resources', 'users.txt')
    tb_values_text_file = os.path.join(sys._MEIPASS, 'resources', 'tb_values.txt')
    user_val_text_file = os.path.join(sys._MEIPASS, 'resources', 'user_val.txt')
    sql_text_file = os.path.join(sys._MEIPASS, 'resources', 'sql_connection.txt')
else:
    main_win_icon_path = os.path.join("resources","icon.ico")
    other_win_icon_path = os.path.join("resources", "title_logo.ico")
    close_icon_path = os.path.join('resources', 'close.png')
    open_icon_path = os.path.join('resources', 'open.png')
    back_icon_path = os.path.join('resources', 'back-arrow.png')
    main_win_bg_path = os.path.join('resources', 'main_win.png')
    main_close_icon_path = os.path.join('resources', 'main_close.png')
    about_close_icon_path = os.path.join('resources', 'about_close.png')

    admins_text_file = os.path.join('resources', 'admins.txt')
    users_text_file = os.path.join('resources', 'users.txt')
    tb_values_text_file = os.path.join('resources', 'tb_values.txt')
    user_val_text_file = os.path.join('resources', 'user_val.txt')
    sql_text_file = os.path.join('resources', 'sql_connection.txt')

def main():

    # If previously connected.
    file = open(sql_text_file, 'r')
    data = file.read()
    file.close()
    global connection
    try:
        lst = ast.literal_eval(data)
        u = lst[0]
        p = lst[1]
        h = lst[2]
        engine = ce("mysql+pymysql://{}:{}@{}/srms_marksheet".format(u, p, h))
        connection = engine.connect()
    except:
        pass

    # Main Window.
    win = Tk()
    win.geometry('1000x600+275+125')
    win.resizable(False, False)
    win.iconbitmap(main_win_icon_path)
    win.overrideredirect(True)

    # Setting up images.
    close_img = ImageTk.PhotoImage(Image.open(close_icon_path))
    open_img = ImageTk.PhotoImage(Image.open(open_icon_path))
    about_close_img = ImageTk.PhotoImage(Image.open(about_close_icon_path))
    back_icon = ImageTk.PhotoImage(Image.open(back_icon_path))
    main_close_icon = ImageTk.PhotoImage(Image.open(main_close_icon_path))
    main_win_bg = Image.open(main_win_bg_path)

    # Background.
    canvas = Canvas(win, height=600, width=1000, bg='white')
    canvas.place(x=0, y=0)
    resized_main_img = main_win_bg.resize((996, 596))
    main_bg = ImageTk.PhotoImage(resized_main_img)
    canvas.create_image(500, 300, image=main_bg, anchor=CENTER)

    def toggle_win():
        f1 = Frame(win, width=330, height=600, bg='cornflowerblue')                                #bg='#12c4c0'
        f1.place(x=0, y=0)

        Frame(f1, width=300, height=2, bg='black')

        def bttn(x, y, text, bg, active_bg, cmd):
            def on_enter(self):
                button['background'] = active_bg  # ffcc66

            def on_leave(self):
                button['background'] = bg

            button = Button(f1, text=text, width=41, height=3, fg='#262626', border=0, bg=bg,
                            font=( 'Bahnschrift', 11, ),activeforeground='#262626', activebackground=active_bg, command=cmd)
            button.place(x=x, y=y)

            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

        def users():

            file = open(user_val_text_file, 'r')
            data = file.read()
            file.close()
            lst = ast.literal_eval(data)
            username = lst[0]
            password = lst[1]

            file = open(admins_text_file, 'r')
            data = file.read()
            file.close()
            dict = ast.literal_eval(data)

            if username in dict.keys() and dict[username]==password:
                f1.destroy()

                win = Toplevel()
                win.grab_set()
                win.geometry('370x360+580+250')
                win.overrideredirect(True)
                win.config(bg='cornflowerblue')

                frame = Frame(win, borderwidth=3, relief=SOLID, bg='red')
                frame.place(x=5, y=35, height=320, width=360)

                # Close Button.
                def close():
                    win.destroy()
                Button(win, image=close_img, border=0, command=close, bg='cornflowerblue',
                       activebackground='cornflowerblue').place(x=340, y=3)

                s2 = Scrollbar(frame, orient=VERTICAL)
                s2.pack(side=RIGHT, fill=Y)

                tree = ttk.Treeview(frame, columns=('a', 'b'), yscrollcommand=s2.set, height=220, selectmode=BROWSE)
                tree['show'] = 'headings'
                tree.pack(fill=BOTH, expand=1)
                tree.column('#1', width=170, stretch=NO)
                tree.column('#2', width=160, stretch=NO)
                tree.heading('a', text='Users', anchor=W)
                tree.heading('b', text='Designation', anchor=W)
                style = ttk.Style()
                style.configure('Treeview.Heading', font=('Arial Rounded MT Bold', 18), foreground='navy')
                style.configure('Treeview', font=('Microsoft YaHei ', 12, 'bold'), background='lavender')

                def list_users():
                    tree.delete(*tree.get_children())
                    file = open(admins_text_file, 'r')
                    data = file.read()
                    file.close()
                    if data:
                        dict = ast.literal_eval(data)
                        for user in dict.keys():
                            val = [user, 'Admin']
                            tree.insert('', END, values=val)

                    file = open(users_text_file, 'r')
                    data = file.read()
                    file.close()
                    if data:
                        dict = ast.literal_eval(data)
                        for user in dict.keys():
                            val = [user, 'Guest']
                            tree.insert('', END, values=val)

                list_users()

                def right_click_func(self):
                    cur_item = tree.identify('item', self.x, self.y)  # ID of row (stands for child in get_childre().
                    tree.selection_set(cur_item)

                    if tree.selection:
                        selection = tree.item(cur_item)['values']
                        user = selection[0]
                        designation = selection[1]

                        menu = Menu(win, tearoff=0)

                        if designation == 'Admin':

                            def dismiss_admin():

                                # At least one admin is required.
                                file = open(admins_text_file, 'r')
                                data = file.read()
                                file.close()
                                dict = ast.literal_eval(data)
                                if len(dict.keys()) == 1:
                                    messagebox.showwarning('Cannot Operate!', 'There need to be at least one Admin.')
                                    return

                                # Removing user from admins.txt
                                file = open(admins_text_file, 'r+')
                                data = file.read()
                                file.truncate(0)
                                file.close()
                                dict = ast.literal_eval(data)
                                user_pass = dict[user]
                                dict.pop(user)
                                file = open(admins_text_file, 'w')
                                file.write(str(dict))
                                file.close()

                                connector = sqlite3.connect('c:/Program Files/Common Files/admins_users.db')
                                connector.execute("update admins_users set Designation='Guest' where Username='{}'".format(user))
                                connector.commit()
                                connector.close()

                                # Adding user to users.txt
                                file = open(users_text_file, 'r+')
                                data = file.read()
                                file.truncate(0)
                                file.close()
                                if data:
                                    dict = ast.literal_eval(data)
                                    dict[user] = user_pass
                                    file = open(users_text_file, 'w')
                                    file.write(str(dict))
                                    file.close()
                                else:
                                    file = open(users_text_file, 'w')
                                    file.write(str({user: user_pass}))
                                    file.close()

                                # Refreshing.
                                list_users()

                            def remove_user():

                                # At least one admin is required.
                                file = open(admins_text_file, 'r')
                                data = file.read()
                                file.close()
                                dict = ast.literal_eval(data)
                                if len(dict.keys()) == 1:
                                    messagebox.showwarning('Cannot Operate!', 'There need to be at least one Admin.')
                                    return

                                # Removing admin.
                                file = open(admins_text_file, 'r+')
                                data = file.read()
                                file.truncate(0)
                                file.close()
                                dict = ast.literal_eval(data)
                                dict.pop(user)
                                file = open(admins_text_file, 'w')
                                file.write(str(dict))
                                file.close()

                                connector = sqlite3.connect('c:/Program Files/Common Files/admins_users.db')
                                connector.execute(
                                    "delete from admins_users where Username='{}'".format(user))
                                connector.commit()
                                connector.close()

                                # Refreshing.
                                list_users()

                            menu.add_command(label='Dismiss Admin', command=dismiss_admin)
                            menu.add_command(label='Remove User', command=remove_user)

                        else:
                            def make_admin():
                                # Removing user from users.txt
                                file = open(users_text_file, 'r+')
                                data = file.read()
                                file.truncate(0)
                                file.close()
                                if data:
                                    dict = ast.literal_eval(data)
                                    user_pass = dict[user]
                                    dict.pop(user)
                                    if dict:
                                        file = open(users_text_file, 'w')
                                        file.write(str(dict))
                                        file.close()

                                # Adding user to admins.txt
                                file = open(admins_text_file, 'r+')
                                data = file.read()
                                file.truncate(0)
                                file.close()
                                dict = ast.literal_eval(data)
                                dict[user] = user_pass
                                file = open(admins_text_file, 'w')
                                file.write(str(dict))
                                file.close()

                                connector = sqlite3.connect('c:/Program Files/Common Files/admins_users.db')
                                connector.execute(
                                    "update admins_users set Designation='Admin' where Username='{}'".format(user))
                                connector.commit()
                                connector.close()

                                # Refreshing.
                                list_users()

                            def remove_user():

                                # Removing user.
                                file = open(users_text_file, 'r+')
                                data = file.read()
                                file.truncate(0)
                                file.close()
                                if data:
                                    dict = ast.literal_eval(data)
                                    dict.pop(user)
                                    if dict:
                                        file = open(users_text_file, 'w')
                                        file.write(str(dict))
                                        file.close()

                                    connector = sqlite3.connect('c:/Program Files/Common Files/admins_users.db')
                                    connector.execute(
                                        "delete from admins_users where Username='{}'".format(user))
                                    connector.commit()
                                    connector.close()

                                # Refreshing.
                                list_users()

                            menu.add_command(label='Make Admin', command=make_admin)
                            menu.add_command(label='Remove User', command=remove_user)

                        try:
                            menu.tk_popup(self.x_root, self.y_root)
                        finally:
                            menu.grab_release()

                tree.bind('<Button-3>', right_click_func)  # Button-3 = Right Button Click.

                win.mainloop()
            else:
                messagebox.showwarning('Access Denied!', 'Only Admins have access to users settings.')

        def ledger():
            file = open(user_val_text_file, 'r')
            data = file.read()
            file.close()
            lst = ast.literal_eval(data)
            username = lst[0]
            password = lst[1]

            file = open(admins_text_file, 'r')
            data = file.read()
            file.close()
            dict = ast.literal_eval(data)

            if username in dict.keys() and dict[username]==password:
                win.destroy()
                import records_win
                records_win.main()
            else:
                messagebox.showwarning('Access Denied!', 'Only Admins have access to ledger.')

        def marksheet():
            f1.destroy()

            # Checking for connection.
            file = open(sql_text_file, 'r')
            data = file.read()
            if not data:
                con_condition = ''
                file.close()
            else:
                con_condition = '.'
                file.close()

            def tb_window():

                # Select tb Frame.
                f2 = Frame(win, width=300, height=200, bg='cornflowerblue', relief=RIDGE, borderwidth=3)
                f2.place(x=350, y=200)

                def close_f2():
                    f2.destroy()

                def select_tb():
                    tb = combo.get()
                    if tb != '':
                        try:
                            int(tb[0:2])
                            Class = tb[0:2]
                            stream = tb[5:]
                            val_list = [tb, Class, stream]
                        except:
                            Class = tb[0]
                            stream = tb[5:]
                            val_list = [tb, Class, stream]

                        file = open(tb_values_text_file, 'w')
                        file.truncate()
                        file.write(str(val_list))
                        file.close()

                        connection.close()
                        win.destroy()
                        import marksheet_win
                        marksheet_win.main()

                def new_tb():
                    f2.destroy()
                    create_tb_frame = Frame(win, bg='cornflowerblue', width=370, height=235, relief=GROOVE,
                                            borderwidth=4)
                    create_tb_frame.place(x=320, y=180)

                    def create_tb():
                        Class = e1.get()
                        section = e2.get()
                        stream = e3.get()
                        tb = Class + '_' + str(section) + '_' + str(stream)

                        val_list = [tb, Class, stream]
                        file = open(tb_values_text_file, 'w')
                        file.truncate()
                        file.write(str(val_list))
                        file.close()

                        if e1.get() == '' or e2.get() == '':
                            messagebox.showerror('Incomplete Form!', 'Please fill-up the empty fields.')
                            return
                        if int(e1.get()) > 10:
                            if e3.get() == '':
                                messagebox.showerror('Incomplete Form!', 'Please fill-up the empty fields.')
                                return

                        if int(e1.get()) <= 10:
                            try:
                                connection.execute(
                                    "CREATE TABLE {} (Roll_No varchar(10) Primary Key, Student_Name varchar(50), Science varchar(3), Maths varchar(3), Social varchar(3), English varchar(3), Hindi varchar(3), Computer varchar(3))".format(
                                        tb))
                            except:
                                messagebox.showerror('Already exist!',
                                                     "Table with name '{}' already exist in the database.".format(
                                                         tb))
                                return

                            connection.close()
                            win.destroy()
                            import marksheet_win
                            marksheet_win.main()

                        elif int(e1.get()) > 10:
                            try:
                                if e3.get() == 'PCM':
                                    connection.execute(
                                        "CREATE TABLE {} (Roll_No varchar(10) Primary Key, Student_Name varchar(50), Physics varchar(3), Chemistry varchar(3), Maths varchar(3), English varchar(3), Op_Sub varchar(20), Op_Marks varchar(3), Add_Sub varchar(20), Add_Marks varchar(3))".format(
                                            tb))
                                elif e3.get() == 'PCB':
                                    connection.execute(
                                        "CREATE TABLE {} (Roll_No varchar(10) Primary Key, Student_Name varchar(50), Physics varchar(3), Chemistry varchar(3), Biology varchar(3), English varchar(3), Op_Sub varchar(20), Op_Marks varchar(3), Add_Sub varchar(20), Add_Marks varchar(3))".format(
                                            tb))
                                elif e3.get() == 'Commerce':
                                    connection.execute(
                                        "CREATE TABLE {} (Roll_No varchar(10) Primary Key, Student_Name varchar(50), Accountancy varchar(3), Business varchar(3), Economics varchar(3), English varchar(3), Op_Sub varchar(20), Op_Marks varchar(3), Add_Sub varchar(20), Add_Marks varchar(3))".format(
                                            tb))
                                elif e3.get() == 'Arts':
                                    connection.execute(
                                        "CREATE TABLE {} (Roll_No varchar(10) Primary Key, Student_Name varchar(50), Pol_Science varchar(3), Geography varchar(3), History varchar(3), English varchar(3), Op_Sub varchar(20), Op_Marks varchar(3), Add_Sub varchar(20), Add_Marks varchar(3))".format(
                                            tb))
                            except:
                                messagebox.showerror('Already exist!',
                                                     "Table with name '{}' already exist in the database.".format(
                                                         tb))
                                return

                            connection.close()
                            win.destroy()
                            import marksheet_win
                            marksheet_win.main()

                    # Backbutton.
                    def back():
                        create_tb_frame.destroy()
                        tb_window()
                    back_btn = Button(create_tb_frame, image=back_icon, bg='cornflowerblue', border=0,
                                      activebackground='cornflowerblue', command=back)
                    back_btn.place(x=5, y=2)

                    # Close Button.
                    def close_f3():
                        create_tb_frame.destroy()

                    close_btn = Button(create_tb_frame, image=close_img, border=0, command=close_f3,
                                       bg='cornflowerblue', activebackground='cornflowerblue')
                    close_btn.place(x=333, y=2)

                    Frame(create_tb_frame, width=310, height=2, bg='black').place(x=30, y=35)

                    # Class.
                    Label(create_tb_frame, text='Class', font=('Agency FB', 18), bg='cornflowerblue', relief=SOLID,
                          borderwidth=1, width=14).place(x=30, y=50)
                    e1 = ttk.Combobox(create_tb_frame, font=('Agency FB', 18), values=list(range(1, 13)), width=14,
                                      state='readonly', justify=CENTER)
                    e1.place(x=175, y=50)

                    # Section.
                    Label(create_tb_frame, text='Section', font=('Agency FB', 18), bg='cornflowerblue', relief=SOLID,
                          borderwidth=1, width=14).place(x=30, y=95)
                    e2 = ttk.Combobox(create_tb_frame, font=('Agency FB', 18),
                                      values=['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'], width=14,
                                      state='readonly', justify=CENTER)
                    e2.place(x=175, y=95)

                    # Stream.
                    def func(self):
                        if e1.get() != '':
                            if int(e1.get()) > 10:
                                e3['state'] = 'readonly'
                            else:
                                e3.set('')
                                e3['state'] = DISABLED

                    e1.bind('<FocusIn>', func)
                    Label(create_tb_frame, text='Stream', font=('Agency FB', 18), bg='cornflowerblue', relief=SOLID,
                          borderwidth=1,
                          width=14).place(x=30, y=140)
                    e3 = ttk.Combobox(create_tb_frame, font=('Agency FB', 18),
                                      values=['PCM', 'PCB', 'Arts', 'Commerce'],
                                      width=14, state=DISABLED, justify=CENTER)
                    e3.place(x=175, y=140)

                    # Create button.
                    create_tb_btn = Button(create_tb_frame, text='Create Table', width=43, bg='Skyblue4',
                                           activebackground='Skyblue2', command=create_tb)
                    create_tb_btn.place(x=30, y=185)

                # Select Table Frame.
                Button(f2, image=close_img, border=0, command=close_f2, bg='cornflowerblue',
                       activebackground='cornflowerblue').place(x=264, y=2)
                Label(f2, text='Select Table', font=('Microsoft YaHei UI Light', 20, 'bold'),
                      bg='cornflowerblue').place(x=30, y=40)

                global tables_list
                tables = connection.execute('show tables').fetchall()
                tables_list = []
                for i in tables:
                    table = i[0]
                    tables_list.append(table)
                combo = ttk.Combobox(f2, width=15, values=tables_list, font=('Microsoft YaHei UI Light', 15, 'bold'),
                                     state='readonly')
                combo.place(x=30, y=90)
                Button(f2, text='Open', font=('Microsoft YaHei UI Light', 10, 'bold'), bg='royalblue',
                       command=select_tb).place(x=235, y=155)
                New_btn = Button(f2, text=' New ', font=('Microsoft YaHei UI Light', 10, 'bold'), bg='royalblue',
                       command=new_tb, state=DISABLED, disabledforeground='grey30')
                New_btn.place(x=175, y=155)

                file = open(user_val_text_file, 'r')
                data = file.read()
                file.close()
                lst = ast.literal_eval(data)
                username = lst[0]
                file = open(admins_text_file, 'r')
                data = file.read()
                file.close()
                dict = ast.literal_eval(data)
                if username in dict.keys():
                    New_btn.config(state=NORMAL)

            def sql_window():

                def sql_connect():
                    global connection
                    host = hostval.get()  # Available below.
                    user = userval.get()
                    password = passwordval.get()

                    try:
                        engine = ce("mysql+pymysql://{}:{}@{}".format(user, password, host))
                        connection = engine.connect()
                        sql.destroy()
                        messagebox.showinfo('Connection succeed!', 'Successfully connected to MySQL Server.')
                    except:
                        messagebox.showerror("Connection error!", 'Incorrect information. Please try again.', parent=sql)
                        return  # The code will not run forward.

                    try:
                        connection.execute('create database srms_marksheet')
                        connection.execute('use srms_marksheet')
                    except:
                        connection.execute('use srms_marksheet')

                    connection.close()
                    engine = ce("mysql+pymysql://{}:{}@{}/srms_marksheet".format(user, password, host))
                    connection = engine.connect()

                    lst = [user, password, host]
                    file = open(sql_text_file, 'w')
                    file.truncate(0)
                    file.write(str(lst))
                    file.close()

                    tb_window()

                sql = Toplevel()
                sql.title('MySQL Server Connection')
                sql.config(bg='cornflowerblue', relief=GROOVE, borderwidth=5)
                sql.grab_set()  # Buttons that are out of window will not work.
                sql.overrideredirect(True)
                sql.resizable(False, False)
                sql.geometry('470x270+540+290')

                # Close Button.
                def close():
                    sql.destroy()
                Button(sql, image=close_img, border=0, command=close, bg='cornflowerblue',
                       activebackground='cornflowerblue').place(x=430, y=5)

                # Labels.
                dbl1 = Label(sql, text='Host', font=('Microsoft YaHei UI Light', 18, 'bold'), bg='cornflowerblue', relief=SOLID,
                             borderwidth=1, width=10)
                dbl1.place(x=45, y=35)

                dbl2 = Label(sql, text='User', font=('Microsoft YaHei UI Light', 18, 'bold'), bg='cornflowerblue', relief=SOLID,
                             borderwidth=1, width=10)
                dbl2.place(x=45, y=90)

                dbl3 = Label(sql, text='Password', font=('Microsoft YaHei UI Light', 18, 'bold'), bg='cornflowerblue', relief=SOLID,
                             borderwidth=1, width=10)
                dbl3.place(x=45, y=145)

                # Entry Boxes.
                hostval = StringVar()
                userval = StringVar()
                passwordval = StringVar()

                hostval.set('localhost')
                userval.set('root')

                e1 = Entry(sql, font=('Microsoft YaHei UI Light', 17, 'bold'), bd=2, width=15, bg='lavender', textvariable=hostval)
                e1.place(x=210, y=35)

                e1 = Entry(sql, font=('Microsoft YaHei UI Light', 17, 'bold'), bd=2, width=15, bg='lavender', textvariable=userval)
                e1.place(x=210, y=90)

                e2 = Entry(sql, font=('Microsoft YaHei UI Light', 17, 'bold'), bd=2, width=15, bg='lavender', textvariable=passwordval, show='*')
                e2.place(x=210, y=145)

                # Button.
                dbb = Button(sql, text='Connect', font=('Microsoft YaHei UI ', 18), bg='royalblue', bd=3,
                             command=sql_connect)
                dbb.place(x=160, y=200)

                sql.bind('<Return>', lambda event: sql_connect())  # To bind the button with enter key.
                sql.mainloop()

            if con_condition:
                tb_window()
            else:
                sql_window()

        def about():
            f1.destroy()

            win = Toplevel()
            win.geometry('800x500+378+180')
            win.grab_set()
            win.resizable(False, False)
            win.overrideredirect(True)

            canvas = Canvas(win, height=496, width=796, bg='black')
            canvas.place(x=0, y=0)

            def close():
                win.destroy()

            Button(win, image=about_close_img, border=0, command=close, bg='black', activebackground='black').place(x=764, y=4)

            canvas.create_text(20, 50, text='Hi', font=('Consolas', 16), fill='white', anchor=W)

            canvas.create_text(20, 100, text='This is Swayam Singh,', font=('Consolas', 16), fill='white', anchor=W)
            canvas.create_text(20, 128, text='this software is designed to manage the records', font=('Consolas', 16),
                               fill='white', anchor=W)
            canvas.create_text(20, 158, text='of students, including ledger and marksheet.', font=('Consolas', 16),
                               fill='white', anchor=W)

            canvas.create_text(20, 208, text='This is develoved by using Python framework (tkinter)',
                               font=('Consolas', 16), fill='white', anchor=W)
            canvas.create_text(20, 236, text='and Python libraries (ast, os, sys, PyMySQL, numpy, pandas,',
                               font=('Consolas', 16), fill='white', anchor=W)
            canvas.create_text(20, 264, text='matplotlib, pillow, tkinter, sqlite3 and sqlalchemy).', font=('Consolas', 16),
                               fill='white', anchor=W)

            canvas.create_text(20, 314, text='For any query or feedback, contact on:', font=('Consolas', 16),
                               fill='white', anchor=W)

            canvas.create_text(20, 354, text='1) Instagram : @theinfinityofficial OR @s4m_r4jput',
                               font=('Consolas', 16), fill='white', anchor=W)
            canvas.create_text(20, 382, text='2) Gmail : theinfinityoffici4l@gmail.com', font=('Consolas', 16),
                               fill='white', anchor=W)
            canvas.create_text(20, 410, text='3) Github : s4m-singh', font=('Consolas', 16), fill='white', anchor=W)

            canvas.create_text(20, 450, text='Thank You :)', font=('Consolas', 16), fill='white', anchor=W)

        def signout():
            win.destroy()
            import login_win
            login_win.main()

        bttn(0, 80, 'U S E R S', 'cornflowerblue', 'royalblue', users)
        bttn(0, 135, 'L E D G E R', 'cornflowerblue', 'royalblue', ledger)
        bttn(0, 190, 'M A R K S H E E T', 'cornflowerblue', 'royalblue', marksheet)
        bttn(0, 245, 'A B O U T', 'cornflowerblue', 'royalblue', about)
        bttn(0, 300, 'S I G N O U T', 'cornflowerblue', 'royalblue', signout)

        # Close Button.
        def close():
            f1.destroy()
        Button(f1, image=close_img, border=0, command=close, bg='cornflowerblue', activebackground='cornflowerblue').place(x=5,y=10)

    # Open Button.
    Button(win, image=open_img, command=toggle_win, border=0, bg='black', activebackground='black').place(x=10,y=8)

    # Main Close Button.
    def on_closing():
        if messagebox.askokcancel("Confirm Exit", "Are you sure you want to exit?"):
            win.destroy()
    Button(win, image=main_close_icon, command=on_closing, border=0, bg='black', activebackground='black').place(x=957, y=4)

    win.mainloop()
