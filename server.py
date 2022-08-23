from flask_app import app
from flask_app.controllers import main
from flask_app.controllers import users
from flask_app.controllers import trees
from flask_app.controllers import visitors

if __name__=="__main__":
    app.run()