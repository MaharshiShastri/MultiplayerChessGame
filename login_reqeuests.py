import pymysql
import os
import logging
import traceback
ENDPOINT = ""
PORT = "3306"
USER = "root"
REGION = "ap-south-1"
DBNAME = "chess"
DBPASS = "<password>"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def make_connection():
    return pymysql.connect(host=endpoint, user=dbuser, passwd=password,
        port=int(port), db=database, autocommit=True)
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
email_id = ('',)
password = ""
def handler(event, context):
    try:
        conn = make_connection()
        cursor = conn.cursor()
        try:
           cursor.execute("""SELECT * FROM chess.login WHERE email_id = %s""", email_id)
           result = cursor.fetchall()
        except:
            return log_err ("ERROR: Cannot execute cursor.\n{}".format(
                traceback.format_exc()) )
        try:
            for check in result:
                if check[0] == password:
                    root.destroy()
                    pass
                else:
                    return log_err("ERROR: No User by this email_id.\n{}".format(
                traceback.format_exc()))
        except:
            return logg_err("ERROR: Cannot retrieve query data.\n{}".format(
                traceback.format_exc()))
    except:
        return log_err("ERROR: Cannot connect to database from handler.\n{}".format(
            traceback.format_exc()))
    finally:
        try:
            conn.close()
        except:
            pass
            
