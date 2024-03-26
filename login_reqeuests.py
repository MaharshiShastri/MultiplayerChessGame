import requests
import json
import boto3
import pymysql
import os
ENDPOINT = ""
PORT = "3306"
USER = "root"
REGION = "ap-south-1"
DBNAME = "chess"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
email_id = ''
response = requests.get()#get status code from Lambda
if response.status_code == 200:
    pass