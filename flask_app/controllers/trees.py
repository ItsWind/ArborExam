from flask import render_template, session, request, redirect
from flask_app import app, isAuthenticated
from flask_app.models.user import User
from flask_app.models.tree import Tree
from flask_app.models.visitor import Visitor

# DISPLAYS: Plant New Tree
@app.route('/tree/new')
def displayEditorNew():
    # Authentication stuff #
    if not isAuthenticated():
        return redirect('/')

    # Template variables #
    user = User.getByID(session['userID'])
    mode = {'title':"Plant New Tree", 'action':"/tree/new/post", 'button':"Plant"}

    return render_template('treeeditor.html', user=user, mode=mode, tree = None)

# DISPLAYS: Edit Tree
@app.route('/tree/<int:id>/edit')
def displayEditorEdit(id):
    # Authentication stuff #
    if not isAuthenticated():
        return redirect('/')

    # Template variables #
    user = User.getByID(session['userID'])
    tree = Tree.getByID(id)
    mode = {'title':"Edit Tree", 'action':f"/tree/{id}/edit/post", 'button':"Update"}

    return render_template('treeeditor.html', user=user, mode=mode, tree=tree)

# EDIT: Delete Tree
@app.route('/tree/<int:id>/delete')
def deleteTree(id):
    # Authentication stuff #
    if not isAuthenticated():
        return redirect('/')
    
    # Delete tree #
    Tree.deleteByID(id)

    return redirect('/dashboard')

# DISPLAYS: Tree Page
@app.route('/tree/<int:id>')
def displayTree(id):
    # Authentication stuff #
    if not isAuthenticated():
        return redirect('/')
    
    # Template variables #
    user = User.getByID(session['userID'])
    tree = Tree.getByID(id)
    visitors = Visitor.getAllByTreeID(id)
    hasVisited = Visitor.isUserInVisitors(user, visitors)

    return render_template('treepage.html', user=user, tree=tree, visitors=visitors, hasVisited=hasVisited)



# POSTS: Edit Tree
@app.route('/tree/<int:id>/edit/post', methods=['POST'])
def tryEdit(id):
    # Authentication stuff #
    if not isAuthenticated():
        return redirect('/')

    # Validate form #
    if not Tree.validateData(request.form):
        return redirect(f"/tree/{id}/edit")

    # Edit tree #
    Tree.editByID(request.form)

    return redirect('/dashboard')

#POSTS: New Tree
@app.route('/tree/new/post', methods=['POST'])
def tryAddNew():
    # Authentication stuff #
    if not isAuthenticated():
        return redirect('/')

    # Validate form #
    if not Tree.validateData(request.form):
        return redirect('/tree/new')

    # Save new tree #
    Tree.save(request.form)
    
    return redirect('/dashboard')