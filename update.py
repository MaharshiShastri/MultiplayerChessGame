import sqlite3
from tkinter import *
from tkinter import messagebox

conn = sqlite3.connect("Logindb.db")
cursor = conn.cursor()

root = Tk()
root.title("Update")
root.geometry("800x800+300+200")
root.configure(bg = "#fff")
root.resizable(False,False)

frame = Frame(root, width = 500, height = 500, bg = "#fff")
frame.place(x = 400, y = 250)

heading = Label(frame, text = "Update password", fg = "#57a1f8", bg = "#fff", font = ("Times", 23, "bold"))
heading.place(x = 100, y = 5)

def search():
        email_id = user_id.get()
        for widgets in frame.winfo_children():
            widgets.destroy()
        cursor.execute("""SELECT email_id FROM login WHERE email_id = ?""",(email_id,))
        result = cursor.fetchall()
        if len(result) == 0:
            messagebox.showerror("Invalid", "Invalid email address, please re-enter")
            return 0
        for check in result:
            if check[0] == email_id:
                print("Inside  if check[0] == email_id: condition")
                password = Label(frame, text = "Enter new password")
                password.place(x = 300, y= 200)
                password_Entry = Entry(frame, width = 50, bd = 3)
                password_Entry.place(x = 350, y = 200)
                confirm_password = Label(frame, text = "Confirm new password")
                confirm_password.place(x = 300, y= 250)
                newpassword = Entry(frame, width = 50, bd = 3)
                newpassword.place(x = 350, y = 250)
                Button(root, text = "update password", width = 25, command = confirm(email_id,password_Entry.get(), newpassword.get())).place(x = 450, y = 450)

def confirm(email_id, password1, password2):
    print("++",password1, password2)
    if password1 == password2:
        cursor.execute("""SELECT email_id FROM login WHERE email_id = ?""",(email_id,))
        result = cursor.fetchall()
        for check in result:
            if check[0] == email_id:
                cursor.execute("UPDATE login SET password = ? WHERE email_id =?;""",(password1,email_id))
                play = messagebox.askyesno("Update", "Password successfully updated! Want to play?")
                if play:
                    import main
                    exit()
    else:
        chance = messagebox.askyesno("Invalid", "Passwords do not match! Want to re-entry?")
        if chance:
            search(user_id.get())

label1 = Label(frame, text = "Enter your email: ", fg = "black", bg = "#fff", font = ("Times", 9)).place(x = 0, y= 150)
user_id = Entry(frame, width = 41, fg = "black", border = 3, bg = "#fff", font = ("Times", 11))
user_id.place(x = 0, y = 170)

Button(root, text = "Search account", width = 25, command = search).place(x = 450, y = 450)

root.mainloop()
conn.close()
