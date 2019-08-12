import sqlite3
from db import db
#from models.store import StoreModel

class ItemModel(db.Model):
    # fetching tablename and its columns in sqlalchemy
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # make a store_id as foreign key to be used here as a reference with id of store
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    # in place of join
    store = db.relationship('StoreModel')
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # method for returning json represebtation of item
    def json(self):
        return {'name':self.name, 'price':self.price}

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
