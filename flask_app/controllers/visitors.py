from flask import render_template, session, request, redirect, flash
from flask_app import app, isAuthenticated
from flask_app.models.user import User
from flask_app.models.tree import Tree
from flask_app.models.visitor import Visitor

# POSTS: Visitor
@app.route('/tree/<int:id>/visit')
def visitTree(id):
    # Authentication stuff #
    if not isAuthenticated():
        return redirect('/')

    Visitor.saveWithUserAndTreeID(session['userID'], id)
    
    return redirect(f'/tree/{id}')

@app.route('/tree/<int:id>/unvisit')
def unvisitTree(id):
    # Authentication stuff #
    if not isAuthenticated():
        return redirect('/')

    Visitor.deleteWithUserAndTreeID(session['userID'], id)
    
    return redirect(f'/tree/{id}')