import sqlite3
import tkinter

conn = sqlite3.connect("Logindb.db")
cursor = conn.cursor()

root = Tk()
root.title("Update")
root.geometry("800x800+300+200")
root.configure(bg = "#fff")
root.resizable(False,False)

frame = Frame(root, width = 300, height = 300, bg = "#fff")
frame.place(x = 400, y = 250)

heading = Label(frame, text = "
