from flask import Flask
import os
import mysql.connector

app = Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="remotemysql.com",user=os.getenv("DB_USER"),password=os.getenv("DB_PASS"),database=os.getenv("DB_NAME"))
cursor=conn.cursor()

from app import routes
from app import authentication
from app import dashboard

