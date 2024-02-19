import sqlite3
conn = sqlite3.connect("Logindb.db")
cursor = conn.cursor()
command = " " " CREATE TABLE login(email_id varchar(50) PRIMARY KEY, password varchar(50));"""
cursor.execute(command)
conn.close()
