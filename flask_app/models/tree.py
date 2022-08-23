from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.user import User

class Tree:
    def __init__(self, data):
        self.id = data['id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.plantedAt = data['plantedAt']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.planter = None

    @staticmethod
    def validateData(form):
        isValid = True

        if len(form['species']) < 5:
            flash("Species is a required field and/or you made it too short")
            isValid = False
        elif len(form['species']) > 39:
            flash("The longest tree species name is 39 characters ;)")
            isValid = False

        if len(form['location']) < 2:
            flash("Location is a required field and/or you made it too short")
            isValid = False

        if len(form['reason']) < 1:
            flash("Reason is a required field")
            isValid = False
        elif len(form['reason']) > 50:
            flash("Reason cannot be more than 50 characters")
            isValid = False

        if len(form['plantedAt']) < 10:
            flash("Date planted is a required field")
            isValid = False

        return isValid

    @staticmethod
    def deleteByID(id):
        tree = Tree.getByID(id)
        if tree.planter.id != session['userID']:
            flash("tree.planter.id is not equal to session userID")
            return
            
        data = {
            'id':id
        }
        query = """
                DELETE FROM trees 
                WHERE trees.id=%(id)s
                """
        connectToMySQL().query_db(query, data)

    @staticmethod
    def getAll():
        query = """
                SELECT * FROM trees 
                JOIN users ON trees.user_id = users.id 
                ORDER BY trees.updatedAt DESC
                """
        results = connectToMySQL().query_db(query)
        return Tree.getTreesWithPlanter(results)

    @staticmethod
    def getAllPlantedByUser(user):
        data = {
            'userID':user.id
        }
        query = """
                SELECT * FROM trees 
                JOIN users ON trees.user_id = users.id 
                WHERE trees.user_id=%(userID)s 
                ORDER BY trees.updatedAt DESC
                """
        results = connectToMySQL().query_db(query, data)
        return Tree.getTreesWithPlanter(results)


    @staticmethod
    def getByID(id):
        data = {
            'id':id
        }
        query = """
                SELECT * FROM trees 
                JOIN users ON trees.user_id = users.id 
                WHERE trees.id=%(id)s
                """
        results = connectToMySQL().query_db(query, data)

        trees = Tree.getTreesWithPlanter(results)

        if len(trees) > 0:
            return trees[0]
        else:
            print("That ID does not exist")

    @staticmethod
    def editByID(form):
        tree = Tree.getByID(form['treeID'])
        if tree.planter.id != session['userID']:
            flash("tree.planter.id is not equal to session userID")
            return

        query = """
                UPDATE trees SET
                    trees.species=%(species)s,
                    trees.location=%(location)s,
                    trees.reason=%(reason)s,
                    trees.plantedAt=%(plantedAt)s,
                    trees.updatedAt=NOW()
                WHERE trees.id=%(treeID)s
                """
        id = connectToMySQL().query_db(query,form)
        return id

    @staticmethod
    def save(form):
        if int(form['authUserID']) != session['userID']:
            flash("authUserID is not equal to session userID")
            return

        query = """
                INSERT INTO trees(
                    trees.species,
                    trees.location,
                    trees.reason,
                    trees.plantedAt,
                    trees.user_id
                )
                VALUES(
                    %(species)s,
                    %(location)s,
                    %(reason)s,
                    %(plantedAt)s,
                    %(authUserID)s
                )
                """
        id = connectToMySQL().query_db(query,form)
        return id

    @classmethod
    def getTreesWithPlanter(cls, queryResults):
        trees = []
        for row in queryResults:
            tree = cls(row)

            userData = row.copy()
            userData['id'] = row['users.id']
            userData['createdAt'] = row['users.createdAt']
            userData['updatedAt'] = row['users.updatedAt']

            tree.planter = User(userData)
            trees.append(tree)
        return trees