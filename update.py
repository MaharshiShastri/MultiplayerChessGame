import mysql.connector
from tkinter import *
from tkinter import messagebox
import sys

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Maharshi#20",
    database = "logindb"
)
cursor = conn.cursor()

root = Tk()
root.title("Update")
root.geometry("800x800+300+200")
root.configure(bg = "#ff0")
root.resizable(False,False)

frame = Frame(root, width = 500, height = 500, bg = "#fff")
frame.place(x = 300, y = 250)

heading = Label(frame, text = "Update password", fg = "#57a1f8", bg = "#fff", font = ("Times", 23, "bold"))
heading.place(x = 50, y = 5)

def search():
        email_id = user_id.get()
        password1 = password_Entry.get()
        password2 = newpassword.get()
        cursor.execute("""SELECT email_id FROM login WHERE email_id = %s""",(email_id,))
        result = cursor.fetchall()
        if len(result) == 0:
            messagebox.showerror("Invalid", "Invalid email address, please re-enter")
            return 0
        for check in result:
            if check[0] == email_id:
                confirm(email_id, password1, password2)

def confirm(email_id, password1, password2):
    if password1 == password2:
        cursor.execute("""SELECT email_id FROM login WHERE email_id = %s""",(email_id,))
        print(email_id,password1,password2)
        result = cursor.fetchall()
        for check in result:
            if check[0] == email_id:
                    print(email_id,password1,password2)
                    sql_comm = '''
                            UPDATE login
                            SET pass = %s
                            WHERE email_id = %s
                            '''
                    data = (password1,email_id)
                    cursor.execute(sql_comm,data)
                    main_menu = messagebox.askyesno("Update", "Password successfully updated! Want to play?")
                    if main_menu:
                            conn.commit()
                            conn.close()
                            root.destroy()
                            sys.exit()
                    else:
                            conn.commit()
                            conn.close()
                            root.destroy()
                            sys.exit()
    else:
        chance = messagebox.askyesno("Invalid", "Passwords do not match! Want to re-entry?")
        if chance:
            search(user_id.get())

password = Label(frame, text = "Enter new password")
password.place(x = 0, y= 200)

password_Entry = Entry(frame, width = 50, bd = 3)
password_Entry.place(x = 0, y = 220)

confirm_password = Label(frame, text = "Confirm new password")
confirm_password.place(x = 0, y= 250)

newpassword = Entry(frame, width = 50, bd = 3)
newpassword.place(x = 0, y = 270)

label1 = Label(frame, text = "Enter your email: ", fg = "black", bg = "#fff", font = ("Times", 9)).place(x = 0, y= 150)
user_id = Entry(frame, width = 41, fg = "black", border = 3, bg = "#fff", font = ("Times", 11))
user_id.place(x = 0, y = 170)

Button(frame, text = "Update password", width = 25, command = search).place(x = 0, y = 300)

root.mainloop()
conn.close()
