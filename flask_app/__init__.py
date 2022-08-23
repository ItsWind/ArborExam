# __init__.py
import os
from flask import Flask, session
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = os.urandom(12).hex()
bcrypt = Bcrypt(app)

def isAuthenticated():
    return 'userID' in session