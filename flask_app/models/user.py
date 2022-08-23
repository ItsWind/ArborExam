from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.fullName = self.firstName + " " + self.lastName
        self.email = data['email']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    @staticmethod
    def validateRegister(form):
        isValid = True
        if len(form['firstName']) < 2:
            flash("First name must be at least 2 characters")
            isValid = False
        if len(form['lastName']) < 2:
            flash("Last name must be at least 2 characters")
            isValid = False
        if not EMAIL_REGEX.match(form['email']):
            flash("You must enter a valid email")
            isValid = False
        if len(form['password']) < 8:
            flash("Password must be at least 8 characters")
            isValid = False
        if form['password'] != form['cfpassword']:
            flash("Confirm password must match with entered password")
            isValid = False
        return isValid

    @staticmethod
    def validateLogin(form):
        query = """
                SELECT * FROM users 
                WHERE users.email=%(email)s
                """
        results = connectToMySQL().query_db(query, form)

        if len(results) > 0:
            enteredPassword = form['password']
            for user in results:
                passwordHash = user['password']
                if bcrypt.check_password_hash(passwordHash, enteredPassword):
                    return user['id']
        return None

    @classmethod
    def getAll(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL().query_db(query)
        return results

    @classmethod
    def getByID(cls, id):
        data = {
            'id':id
        }
        query = """
                SELECT * FROM users 
                WHERE id=%(id)s
                """
        results = connectToMySQL().query_db(query, data)
        for user in results:
            return cls(user)

    @classmethod
    def save(cls, form):
        rawPass = form['password'].encode('utf8')
        data = form.copy()
        data['hashedPassword'] = bcrypt.generate_password_hash(rawPass).decode('utf8')

        query = """
                INSERT INTO users(
                    users.firstName,
                    users.lastName,
                    users.email,
                    users.password
                )
                VALUES(
                    %(firstName)s,
                    %(lastName)s,
                    %(email)s,
                    %(hashedPassword)s
                )
                """
        id = connectToMySQL().query_db(query,data)
        return id