import json
import pymysql

conn = pymysql.connect(host = "chess.czagoc02se2n.ap-south-1.rds.amazonaws.com",
user = "<user-level>",
password = "<pasword>",
port = 3306,
database = "<dbname>"
)
cursor = conn.cursor()
GET_RAW_PATH = "/getUser"
CREATE_RAW_PATH = "/createUser"
def lambda_handler(event, context):
    if event['rawPath'] == GET_RAW_PATH:
        email_id  = event['queryStringParameters']['email_id']
        password = event['queryStringParameters']['pass']
        sql = """SELECT pass FROM login WHERE email_id = %s"""
        check = (email_id,)
        cursor.execute(sql, check)
        result = cursor.fetchall()
        if len(result) == 0:
            data = {"error" : "User not found"} 
            return {'body' : json.dumps(data)}
        for check in result:
            if check[0] == password:
                conn.close()
                return {
                'statusCode': 200,
                'body': json.dumps(True)
                }
    if event['rawPath'] == CREATE_RAW_PATH:
        email_id = event['queryStringParameters']['email_id']
        password = event['queryStringParameters']['pass']
        val = (email_id, password)
        cursor.execute(" " " INSERT INTO login(email_id, pass) VALUES (%s, %s)" " ", val)
        conn.commit()
        conn.close()
        return {
            "statusCode" : 200,
            "body" : "User added"
        }
        
"""import requests
   import json
   response = requests.get("URL/getUser?email_id=EMAIL_ID&pass=PASSWORD")
   data = response.json()
   print(data)
"""
