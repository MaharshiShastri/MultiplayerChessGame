import mysql.connector
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Maharshi#20",
    database = "logindb"
    )
cursor = conn.cursor()
login_table = " " " CREATE TABLE login(email_id VARCHAR(50) NOT NULL PRIMARY KEY, pass VARCHAR(50)); " " "
cursor.execute(login_table)
moves_table ="""CREATE TABLE move(
                                idmove INT NOT NULL PRIMARY KEY,
                                initialmovecol INT NOT NULL,
                                initialmoverow INT NOT NULL,
                                finalmovecol INT NOT NULL,
                                finalmoverow INT NOT NULL,
                                captured BOOL NOT NULL,
                                piece VARCHAR(10) NOT NULL,
                                UNIQUE KEY idmove
                                );
                                """ 
    
