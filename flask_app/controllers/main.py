from flask import render_template, redirect
from flask_app import app, isAuthenticated

# MAIN: Login
@app.route('/')
def gotoHomePage():
    # Authentication stuff #
    if isAuthenticated():
        return redirect('/dashboard')
    
    return render_template('login.html')