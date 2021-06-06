from flask import Flask
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)

from app import routes
from app import authentication
from app import dashboard

