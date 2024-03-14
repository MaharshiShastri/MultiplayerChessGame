import mysql.connector
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "<Enter password for root>",
    database = "logindb"
    )
cursor = conn.cursor()
login_table = " " " CREATE TABLE login(email_id VARCHAR(50) PRIMARY KEY, pass VARCHAR(50)); " " "
cursor.execute(login_table)
moves_table = 
    
