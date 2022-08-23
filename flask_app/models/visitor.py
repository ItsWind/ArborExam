from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.user import User
from flask_app.models.tree import Tree

class Visitor:
    def __init__(self, data):
        self.id = data['id']
        self.createdAt = data['createdAt']
        self.user = None
        self.tree = None

    @staticmethod
    def isUserInVisitors(user, visitors):
        for visitor in visitors:
            if user.id == visitor.user.id:
                return True
        return False

    @staticmethod
    def getVisitorCounts():
        counts = {}
        query = """
                SELECT tree_id, COUNT(id) as count FROM visitors
                GROUP BY tree_id;
                """
        results = connectToMySQL().query_db(query)
        for row in results:
            counts[row['tree_id']] = row['count']
        return counts

    @staticmethod
    def getAllByTreeID(treeID):
        data = {
            'treeID':treeID
        }
        query = """
                SELECT * FROM visitors 
                JOIN users ON visitors.user_id = users.id 
                JOIN trees on visitors.tree_id = trees.id
                WHERE visitors.tree_id=%(treeID)s
                """
        results = connectToMySQL().query_db(query, data)
        return Visitor.getVisitorsWithUserAndTree(results)

    @staticmethod
    def deleteWithUserAndTreeID(userID, treeID):
        data = {
            'userID':userID,
            'treeID':treeID
        }
        query = """
                DELETE FROM visitors 
                WHERE tree_id=%(treeID)s AND user_id=%(userID)s
                """
        connectToMySQL().query_db(query, data)

    @staticmethod
    def saveWithUserAndTreeID(userID, treeID):
        data = {
            'userID':userID,
            'treeID':treeID
        }
        query = """
                INSERT INTO visitors(
                    visitors.user_id,
                    visitors.tree_id
                )
                VALUES(
                    %(userID)s,
                    %(treeID)s
                )
                """
        id = connectToMySQL().query_db(query,data)
        return id

    @classmethod
    def getVisitorsWithUserAndTree(cls, queryResults):
        visitors = []
        for row in queryResults:
            visitor = cls(row)
            
            userData = row.copy()
            userData['id'] = row['users.id']
            userData['createdAt'] = row['users.createdAt']

            visitor.user = User(userData)

            treeData = row.copy()
            treeData['id'] = row['trees.id']
            treeData['createdAt'] = row['trees.createdAt']

            visitor.tree = Tree(userData)

            visitors.append(visitor)
        return visitors