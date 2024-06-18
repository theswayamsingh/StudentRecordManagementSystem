from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import ast, sys, os
import sqlite3

if getattr(sys, 'frozen', False):
    img = Image.open(os.path.join(sys._MEIPASS, "resources", "login.png"))  # sys._MEIPASS is only usable in exe.
    close_icon_path = os.path.join(sys._MEIPASS, 'resources', 'close.png')
    main_win_icon_path = os.path.join(sys._MEIPASS, "resources", "icon.ico")
    eye_icon_path = os.path.join(sys._MEIPASS, 'resources', 'eye.png')

    admins_text_file = os.path.join(sys._MEIPASS, 'resources', 'admins.txt')
    users_text_file = os.path.join(sys._MEIPASS, 'resources', 'users.txt')
    user_val_text_file = os.path.join(sys._MEIPASS, 'resources', 'user_val.txt')
    sql_text_file = os.path.join(sys._MEIPASS, 'resources', 'sql_connection.txt')
else:
    img = Image.open(os.path.join("resources", "login.png"))
    close_icon_path = os.path.join('resources', 'close.png')
    main_win_icon_path = os.path.join("resources", "icon.ico")
    eye_icon_path = os.path.join('resources', 'eye.png')

    admins_text_file = os.path.join('resources', 'admins.txt')
    users_text_file = os.path.join('resources', 'users.txt')
    user_val_text_file = os.path.join('resources', 'user_val.txt')
    sql_text_file = os.path.join('resources', 'sql_connection.txt')


# Connecting to the database where users details will be stored.
connector = sqlite3.connect('c:/Program Files/Common Files/admins_users.db')
connector.execute(
    "CREATE TABLE IF NOT EXISTS admins_users (S_No INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Username TEXT, Password TEXT, Designation TEXT)"
)

datas = connector.execute('select * from admins_users').fetchall()
if not datas:
    connector.execute("insert into admins_users (S_No, Username, Password, Designation) values (1, 'Swayam','Singh','Admin')")
    connector.commit()

datas = connector.execute("select * from admins_users where Designation='Admin'").fetchall()
file = open(admins_text_file, 'w')
file.truncate()
dict = {}
for i in datas:
    username = i[1]
    password = i[2]
    dict[username] = password
file.write(str(dict))
file.close()

datas = connector.execute("select * from admins_users where Designation='Guest'").fetchall()
if datas:
    file = open(users_text_file, 'w')
    file.truncate()
    dict = {}
    for i in datas:
        username = i[1]
        password = i[2]
        dict[username] = password
    file.write(str(dict))
    file.close()
connector.close()

def main():
    # Clearing SQL info.
    file = open(sql_text_file, 'w')
    file.truncate()
    file.close()

    # Login window.
    login_win = Tk()
    login_win.geometry('925x500+300+180')
    login_win.resizable(False, False)
    login_win.overrideredirect(True)
    login_win.iconbitmap(main_win_icon_path)

    # Images.
    resized_image = img.resize((921, 496))
    image = ImageTk.PhotoImage(resized_image)
    close_img = ImageTk.PhotoImage(Image.open(close_icon_path))
    eye_img = ImageTk.PhotoImage(Image.open(eye_icon_path))

    # Functions.

    def signin_win():

        # Background.
        Label(login_win, image=image, border=0, bg='white').place(x=2, y=2)

        # Close Button.
        def close():
            if messagebox.askokcancel("Confirm Exit", "Are you sure you want to exit?"):
                login_win.destroy()
        Button(login_win, image=close_img, border=0, command=close, bg='slateblue4', activebackground='slateblue4').place(
            x=895, y=2)

        # SignIn Frame.
        f1 = Frame(login_win, width=350, height=400, bg='slateblue4', relief=GROOVE, borderwidth=5).place(x=280, y=50)

        # Heading.
        Label(login_win,text="Sign in",fg='#ff4f5a',bg='slateblue4', font=('Agency FB', 35, 'bold')).place(x=396,y=85)

        # Username Entry Box.

        def on_enter1(self):
                e1.delete(0,'end')
        def on_leave1(self):
            if e1.get()=='':
                e1.insert(0,'Username')

        e1 = Entry(f1,width=25,fg='black',border=0,bg='slateblue4',)
        e1.config(font=('Bahnschrift Light Condensed', 19,))
        e1.bind("<FocusIn>", on_enter1)
        e1.bind("<Leave>", on_leave1)
        e1.insert(0,'Username')
        e1.place(x=333,y=177)

        Frame(f1,width=250,height=2,bg='black').place(x=330,y=212)

        # Password Entry Box.

        def on_enter2(self):
            e2.delete(0,'end')
            e2.config(show='*')
        def on_leave2(self):
            if e2.get()=='':
                e2.config(show='')
                e2.insert(0,'Password')

        e2 =Entry(f1,width=20,fg='black',border=0,bg='slateblue4')
        e2.config(font=('Bahnschrift Light Condensed', 19,))
        e2.bind("<FocusIn>", on_enter2)
        e2.bind("<Leave>", on_leave2)
        e2.insert(0,'Password')
        e2.place(x=333,y=244)

        Frame(f1,width=250,height=2,bg='black').place(x=330,y=279)

        def on_click1(self):
            e2.config(show='')
        def on_leave11(self):
            e2.config(show='*')
        b1 = Button(f1, image=eye_img, border=0, bg='slateblue4', activebackground='slateblue4')
        b1.place(x=550, y=244)
        b1.bind('<ButtonPress-1>', on_click1)
        b1.bind('<ButtonRelease-1>', on_leave11)

        # Signin Function.
        def signincmd():
            key = e1.get()
            value = e2.get()

            file = open(users_text_file, 'r')
            data = file.read()
            file.close()
            if data:
                dict = ast.literal_eval(data)
                if key in dict.keys() and value == dict[key]:
                    file = open(user_val_text_file, 'w')
                    file.truncate(0)
                    file.write(str([key, value]))
                    file.close()

                    login_win.destroy()
                    import main_win
                    main_win.main()
                    return

            file = open(admins_text_file, 'r')
            data = file.read()
            file.close()
            dict = ast.literal_eval(data)
            if key in dict.keys() and value == dict[key]:
                file = open(user_val_text_file, 'w')
                file.truncate(0)
                file.write(str([key, value]))
                file.close()

                login_win.destroy()
                import main_win
                main_win.main()
            else:
                messagebox.showwarning('Login Failed', 'Invalid username and password.')

        # Signin Button.
        Button(f1,width=35,pady=7,text='Sign in', font=('Arial Narrow',13), bg='#ff4f5a',fg='white',relief=RAISED, borderwidth=3, command=signincmd).place(x=313,y=325)
        login_win.bind('<Return>', lambda event : signincmd())

        # Don't have account ?
        l1=Label(f1,text="Don't have an account?",fg="black",bg='slateblue4')
        l1.config(font=('Arial Narrow', 15))
        l1.place(x=330,y=400)

        # Signup option.
        b2=Button(f1,width=6,text='Sign up', font=('Arial Narrow', 15, 'bold'), border=0,bg='slateblue4',fg='#ff4f5a',
                  activebackground='slateblue4', activeforeground='white',command=signup_win)
        b2.place(x=510,y=395)

    def signup_win():

        # Background.
        Label(login_win, image=image, border=0, bg='white').place(x=2, y=2)

        # Close Button.
        def close():
            login_win.destroy()
        Button(login_win, image=close_img, border=0, command=close, bg='slateblue4', activebackground='slateblue4').place(
            x=895, y=2)

        # Signup Frame.
        f1 = Frame(login_win, width=350, height=400, bg='slateblue4', relief=GROOVE, borderwidth=5).place(x=280, y=50)

        # Heading.
        Label(f1, text="Sign up", fg='#ff4f5a', bg='slateblue4',
              font=('Agency FB', 35, 'bold')).place(x=390, y=85)

        # Username Entry Box.

        def on_enter1(self):
            e1.delete(0, 'end')

        def on_leave1(self):
            if e1.get() == '':
                e1.insert(0, 'Username')

        e1 = Entry(f1, width=25, fg='black', border=0, bg='slateblue4')
        e1.config(font=('Bahnschrift Light Condensed', 16))
        e1.bind("<FocusIn>", on_enter1)
        e1.bind("<Leave>", on_leave1)
        e1.insert(0, 'Username')
        e1.place(x=335, y=170)

        Frame(f1, width=250, height=2, bg='black').place(x=330, y=200)

        # Password Entry Box.

        def on_enter2(self):
            e2.delete(0, 'end')
            e2.config(show='*')

        def on_leave2(self):
            if e2.get() == '':
                e2.config(show='')
                e2.insert(0, 'Password')

        e2 = Entry(f1, width=20, fg='black', border=0, bg='slateblue4')
        e2.config(font=('Bahnschrift Light Condensed', 16))
        e2.bind("<FocusIn>", on_enter2)
        e2.bind("<Leave>", on_leave2)
        e2.insert(0, 'Password')
        e2.place(x=335, y=220)

        Frame(f1, width=250, height=2, bg='black').place(x=330, y=250)

        def on_enter3(self):
            e3.delete(0, 'end')
            e3.config(show='*')
        def on_leave3(self):
            if e3.get() == '':
                e3.config(show='')
                e3.insert(0, 'Confirm Password')

        e3 = Entry(f1, width=20, fg='black', border=0, bg='slateblue4')
        e3.config(font=('Bahnschrift Light Condensed', 16))
        e3.bind("<FocusIn>", on_enter3)
        e3.bind("<Leave>", on_leave3)
        e3.insert(0, 'Confirm Password')
        e3.place(x=335, y=270)

        Frame(f1, width=250, height=2, bg='black').place(x=330, y=300)

        def on_click1(self):
            e2.config(show='')
        def on_leave11(self):
            e2.config(show='*')
        def on_click2(self):
            e3.config(show='')
        def on_leave22(self):
            e3.config(show='*')
        b1 = Button(f1, image=eye_img, border=0, bg='slateblue4', activebackground='slateblue4')
        b1.place(x=550, y=210)
        b2 = Button(f1, image=eye_img, border=0, bg='slateblue4', activebackground='slateblue4')
        b2.place(x=550, y=260)
        b1.bind('<ButtonPress-1>', on_click1)
        b1.bind('<ButtonRelease-1>', on_leave11)
        b2.bind('<ButtonPress-1>', on_click2)
        b2.bind('<ButtonRelease-1>', on_leave22)

        # Signup Function.
        def signupcmd():
            key = e1.get()
            val = e2.get()
            val2 = e3.get()

            if val != val2:
                messagebox.showwarning('Error!', 'Both the passwords should match.')

            else:
                file = open(users_text_file, 'r')
                data = file.read()
                file.close()
                if data:
                    dict = ast.literal_eval(data)        # String to original form(dictionary).
                    if key in dict.keys():
                        messagebox.showwarning('Existing User!', 'Username already exist. Try signing in.')
                        return

                file = open(admins_text_file, 'r')
                data = file.read()
                file.close()
                if data:
                    dict2 = ast.literal_eval(data)  # String to original form(dictionary).
                    if key in dict2.keys():
                        messagebox.showwarning('Existing User!', 'Username already exist. Try signing in.')
                        return

                try:
                    dict[key] = val  # Adding key and val in dict.
                    file = open(users_text_file, 'w')
                    file.write(str(dict))  # Writing the updated dict in the form of string.
                    file.close()
                except:
                    file = open(users_text_file, 'w')
                    file.write(str({key:val}))  # Writing the updated dict in the form of string.
                    file.close()

                file = open(user_val_text_file, 'w')
                file.truncate(0)
                file.write(str([key, val]))
                file.close()

                connector = sqlite3.connect('c:/Program Files/Common Files/admins_users.db')
                connector.execute("insert into admins_users (Username, Password, Designation) values (?, ?, ?)", (key, val, 'Guest'))     # Adding user to the table.
                connector.commit()
                connector.close()

                login_win.destroy()
                import main_win
                main_win.main()

        # Signup Button.
        Button(f1, width=35, pady=7, text='Sign up', font=('Arial Narrow', 13), bg='#ff4f5a', fg='white'
               ,relief=RAISED, borderwidth=3, command=signupcmd).place(x=312, y=330)
        login_win.bind('<Return>', lambda event: signupcmd())

        # Already have account?
        l1 = Label(f1, text="Already have an account?", fg="black", bg='slateblue4')
        l1.config(font=('Arial Narrow', 15))
        l1.place(x=325, y=400)

        # Signin option.
        b2 = Button(f1, width=6, text='Sign in', font=('Arial Narrow', 15, 'bold'), border=0, bg='slateblue4',
                    fg='#ff4f5a',
                    activebackground='slateblue4', activeforeground='white', command=signin_win)
        b2.place(x=518, y=395)

    # Default Screen.
    signin_win()

    login_win.mainloop()