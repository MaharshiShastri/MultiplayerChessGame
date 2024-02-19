import os
from tkinter import *
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("Logindb.db")
cursor = conn.cursor()

root = Tk()
root.title("Login")
root.geometry("800x800+300+200")
root.configure(bg = "#fff")
root.resizable(False,False)

img = PhotoImage(file = os.path.join("assets/images/") + "banner.png")
Label(root, image = img, bg = "#fff").place(x=100,y=250)

frame = Frame(root, width = 300, height = 300, bg = "#fff")
frame.place(x = 450, y = 250)

heading = Label(frame, text = "Sign in", fg = "#57a1f8", bg = "#fff", font = ("Times", 23,"bold"))
heading.place(x = 100, y = 5)

def signin():
    cursor.execute(" " "SELECT password FROM login WHERE email_id = ? " " ", (email_id,))
    result = cursor.fetchall()
    email_id = user.get()
    password = code.get()
    result = back.authenticate(email_id, password)
    if len(result) == 0:
        messagebox.showerror("Invalid", "Invalid email address, please re-enter")
        return 0
    for check in result:
        if check[0] == password:
            import main
            main = Main()
            exit()
        else:
            messagebox.showerror("Invalid", "Invalid password, please re-enter")
def signup():
    user = Entry(frame, width = 30, fg = "black", border = 0, bg = "#fff", font = ("Times", 11))
    user.place(x = 30, y = 80)
    label = Label(frame, text = "Enter new email address: ", fg = "black", bg = "#fff", font = ("Times", 11))
    label.place(x=0, y = 80)
    
    code = Entry(frame, width = 30, fg = "black", border = 0, bg = "#fff", font = ("Times", 11))
    code.place(x = 30, y = 150)
    label = Label(frame, text = "Enter password : ", fg = "black", bg = "#fff", font = ("Times", 11))
    label.place(x=0, y = 150)

    Button(frame, width = 39, pady = 7, text = "Create", bg = "#57a1f8", fg = "white", border = 2).place(x = 30, y = 204)
    
    email_id = user.get()
    password = code.get()

    val = (email_id, password)
    cursor.execute(" " " INSERT INTO login VALUES (?, ?)" " ", val)
    conn.commit()
    pass

user = Entry(frame, width = 30, fg = "black", border = 0, bg = "#fff", font = ("Times", 11))
user.place(x = 30, y = 80)
user.insert(0, "Enter your Email-ID")
Frame(frame, width = 295, height = 2, bg = "black").place(x=25, y = 107)

code = Entry(frame, width = 30, fg = "black", border = 0, bg = "#fff", font = ("Times", 11))
code.place(x = 30, y = 150)
code.insert(0, "Enter your password")
Frame(frame, width = 295, height = 2, bg = "black").place(x=25, y = 177)

Button(frame, width = 39, pady = 7, text = "Sign in", bg = "#57a1f8", fg = "white", border = 2, command = signin).place(x = 30, y = 204)
label = Label(frame, text = "Don't have an account?", fg = "black", bg = "#fff", font = ("Times", 9))
label.place(x = 75, y = 270)

sign_up = Button(frame, width = 6, text = "sign up", border = 0, bg = "#fff", cursor = "plus", fg = "#57a1f8", command = signup)
sign_up.place(x = 215, y = 270)

root.mainloop()
conn.close()

