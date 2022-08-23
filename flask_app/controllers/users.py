from flask import render_template, session, request, redirect, flash
from flask_app import app, isAuthenticated
from flask_app.models.user import User
from flask_app.models.tree import Tree
from flask_app.models.visitor import Visitor

# AUTH: Logout
@app.route('/logout')
def doLogout():
    # Pop auth cookie #
    session.pop('userID', None)

    return redirect('/')

# DISPLAYS: Dashboard
@app.route('/dashboard')
def gotoDashboard():
    # Authentication stuff #
    if not isAuthenticated():
        return redirect('/')

    # Template variables #
    user = User.getByID(session['userID'])
    trees = Tree.getAll()
    visitorCounts = Visitor.getVisitorCounts()

    return render_template('index.html', user=user, trees=trees, visitorCounts=visitorCounts)

# DISPLAYS: Account Page
@app.route('/account')
def gotoAccountPage():
    # Authentication stuff #
    if not isAuthenticated():
        return redirect('/')
    
    # Template variables #
    user = User.getByID(session['userID'])
    trees = Tree.getAllPlantedByUser(user)

    return render_template('userpage.html', user=user, trees=trees)



# POST: Login
@app.route('/trylogin', methods=['POST'])
def tryLogin():
    # Validate form #
    loginID = User.validateLogin(request.form)
    if loginID == None:
        flash("Email/password combo invalid")
        return redirect('/')
    
    # Save auth cookie #
    session['userID'] = loginID

    return redirect('/dashboard')

# POST: Register
@app.route('/doregister', methods=['POST'])
def doRegister():
    # Validate form #
    if not User.validateRegister(request.form):
        return redirect('/')
    loginID = User.save(request.form)
    if loginID == False:
        flash("Email has already been taken")
        return redirect('/')
    
    # Save auth cookie #
    session['userID'] = loginID

    return redirect('/dashboard')