import sqlite3
from db import db

class UserModel(db.Model):
    # fetching tablename and its columns in sqlalchemy
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {'id': self.id, 'username': self.username}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "select * from users where username=?"
        # # if a single parameter is there use , always like(3*5)+2 we use bracket for rendering correctly and to maintain priority
        # result = cursor.execute(query, (username,))
        # # returns 1st row
        # row = result.fetchone()
        # if row:
        #     # to fetch all values id, username, password in order use *row
        #     user = cls(*row)
        #
        # else:
        #     user = None;
        #
        # connection.close()
        # return user

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
