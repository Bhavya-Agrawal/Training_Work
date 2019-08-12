import sqlite3
from db import db

class StoreModel(db.Model):
    # fetching tablename and its columns in sqlalchemy
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # for join with ItemModel, if data or items becomes more in number it becomes an expensive task so for that use lazy=dynamic but now self.items wont work so for that do self.items.all()
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    # method for returning json represebtation of item
    def json(self):
        return {'name':self.name, 'items':[item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        # sqlalchemy itself creates connection and cursor etc., and to get first row only use .first()
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "Update items set price =? where name =?"
        # cursor.execute(query, (self.price, self.name))
        # connection.commit()
        # connection.close()
