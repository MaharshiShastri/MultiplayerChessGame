import os
from tkinter import *
import sqlite3
from tkinter import messagebox

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
    email_id = user.get()
    password = code.get()
    cursor.execute(" " "SELECT password FROM login WHERE email_id = ? " " ", (email_id,))
    result = cursor.fetchall()
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
    window = Toplevel(root)
    window.title("Sign up")
    window.geometry("800x800+300+200")
    window.configure(bg = "#fff")
    window.resizable(False,False)
    frame = Frame(window, width = 350, height = 390, bg = "#fff").place(x = 480, y = 50)
    heading = Label(frame, text = "Sign up", fg = "#57a1f8", bg = "#fff", font = ("Times", 23,"bold")).place(x = 100, y = 5)

    label = Label(window, text = "Enter new email: ", fg = "black", bg = "#fff", font = ("Times", 9))
    label.place(x = 0, y = 80)
    user = Entry(window, width = 30, fg = "black", border = 0, bg = "#fff", font = ("Times", 11))
    user.place(x = 60, y = 80)
    Frame(window, width = 295, height = 2, bg = "black").place(x=25, y = 107)

    label1 = Label(window, text = "Enter password:", fg = "black", bg = "#fff", font = ("Times", 9))
    label1.place(x = 0, y = 150)
    code = Entry(window, width = 30, fg = "black", border = 0, bg = "#fff", font = ("Times", 11))
    code.place(x = 60, y = 150)
    Frame(window, width = 295, height = 2, bg = "black").place(x=25, y = 177)

    def create():
        email_id = user.get()
        password = code.get()
        print("++",email_id, password)
        val = (email_id, password)
        cursor.execute(" " " INSERT INTO login VALUES (?, ?)" " ", val)
        conn.commit()
        import main
        main = Main()
    Button(window, width = 39, pady = 7, text = "Create", bg = "#57a1f8", fg = "white", border = 2, command  = create).place(x = 30, y = 204)
    window.mainloop()
    
label = Label(frame, text = "Enter your email: ", fg = "black", bg = "#fff", font = ("Times", 9))
label.place(x = 0, y = 80)
user = Entry(frame, width = 30, fg = "black", border = 0, bg = "#fff", font = ("Times", 11))
user.place(x = 100, y = 80)
Frame(frame, width = 295, height = 2, bg = "black").place(x=25, y = 107)

label1 = Label(frame, text = "Enter your password:", fg = "black", bg = "#fff", font = ("Times", 9))
label1.place(x = 0, y = 100)
code = Entry(frame, width = 30, fg = "black", border = 0, bg = "#fff", font = ("Times", 11))
code.place(x = 100, y = 150)
Frame(frame, width = 295, height = 2, bg = "black").place(x=25, y = 177)

Button(frame, width = 39, pady = 7, text = "Sign in", bg = "#57a1f8", fg = "white", border = 2, command = signin).place(x = 30, y = 204)
label = Label(frame, text = "Don't have an account?", fg = "black", bg = "#fff", font = ("Times", 9))
label.place(x = 75, y = 270)

sign_up = Button(frame, width = 6, text = "sign up", border = 0, bg = "#fff", cursor = "plus", fg = "#57a1f8", command = signup)
sign_up.place(x = 215, y = 270)

root.mainloop()
conn.close()

