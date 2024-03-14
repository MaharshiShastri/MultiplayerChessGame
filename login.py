import os
from tkinter import *
import mysql.connector
from tkinter import messagebox
import importlib


conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "<Enter root password>",
    database = "logindb"
    )
cursor = conn.cursor()

root = Tk()
root.title("Login")
root.geometry("800x800+300+200")
root.configure(bg = "#fff")
root.resizable(False,False)

img = PhotoImage(file = os.path.join("assets/images/banner.png"))
Label(root, image = img, bg = "#fff").place(x=100,y=250)

frame = Frame(root, width = 500, height = 500, bg = "#fff")
frame.place(x = 400, y = 250)

heading = Label(frame, text = "Sign in", fg = "#57a1f8", bg = "#fff", font = ("Times", 23,"bold"))
heading.place(x = 100, y = 5)

def signin():
    email_id = user.get()
    password = code.get()
    check = (email_id,)
    cursor.execute(" " "SELECT pass FROM login WHERE email_id = %s " " ", check)
    result = cursor.fetchall()
    if len(result) == 0:
        messagebox.showerror("Invalid", "Invalid email address, please re-enter")
        return 0
    for check in result:
        if check[0] == password:
            root.destroy()
            module = importlib.import_module("Menu")
            exit()
        else:
            messagebox.showerror("Invalid", "Invalid password, please re-enter")

def signup():
    window = Toplevel(root)
    window.title("Sign up")
    window.geometry("800x800+300+200")
    window.configure(bg = "#fff")
    window.resizable(False,False)
    frame = Frame(window, width = 350, height = 390, bg = "#fff").place(x = 480, y = 50)
    heading = Label(frame, text = "Sign up", fg = "#57a1f8", bg = "#fff", font = ("Times", 23,"bold")).place(x = 100, y = 5)

    label = Label(window, text = "Enter new email: ", fg = "black", bg = "#fff", font = ("Times", 9))
    label.place(x = 200, y = 210)
    user = Entry(window, width = 41, fg = "black", border = 3, bg = "#fff", font = ("Times", 11))
    user.place(x = 200, y = 230)
    Frame(window, width = 295, height = 2, bg = "black").place(x = 200, y = 257)

    label1 = Label(window, text = "Enter password:", fg = "black", bg = "#fff", font = ("Times", 9))
    label1.place(x = 200, y = 270)
    code = Entry(window, width = 41, fg = "black", border = 3, bg = "#fff", font = ("Times", 11))
    code.place(x = 200, y = 300)
    Frame(window, width = 295, height = 2, bg = "black").place(x=200, y = 327)

    def create():
        email_id = user.get()
        password = code.get()
        val = (email_id, password)
        cursor.execute(" " " INSERT INTO login(email_id, pass) VALUES (%s, %s)" " ", val)
        conn.commit()
        import main
    Button(window, width = 39, pady = 6, text = "Create", bg = "#57a1f8", fg = "white", border = 2, command  = create).place(x = 200, y =350)
    window.mainloop()
    window.destroy()

label = Label(frame, text = "Enter your email: ", fg = "black", bg = "#fff", font = ("Times", 9))
label.place(x = 0, y = 60)
user = Entry(frame, width = 41, fg = "black", border = 3, bg = "#fff", font = ("Times", 11))
user.place(x = 0, y = 80)
Frame(frame, width = 295, height = 2, bg = "black").place(x=0, y = 107)

label1 = Label(frame, text = "Enter your password:", fg = "black", bg = "#fff", font = ("Times", 9))
label1.place(x = 0, y = 130)
code = Entry(frame, width = 41, fg = "black", border = 3, bg = "#fff", font = ("Times", 11), show = '*')
code.place(x = 0, y = 150)
Frame(frame, width = 295, height = 2, bg = "black").place(x=0, y = 177)
Button(frame, width = 39, pady = 7, text = "Sign in", bg = "#57a1f8", fg = "white", border = 2, command = signin).place(x = 0, y = 204)

label = Label(frame, text = "Don't have an account?", fg = "black", bg = "#fff", font = ("Times", 9))
label.place(x = 0, y = 270)

sign_up = Button(frame, width = 6, text = "sign up", border = 0, bg = "#fff", cursor = "plus", fg = "#57a1f8", command = signup)
sign_up.place(x = 215, y = 270)

root.mainloop()
conn.close()

