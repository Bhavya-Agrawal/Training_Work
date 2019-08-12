import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from models.user import UserModel

# defining 2 classes item and itemlist that inherits class Resource
class Item(Resource):
    # define a local parser for all methods and as its without self, so its for Item whole thus use as Item.psrse.parse_args()
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required = True,
            help = "This field can't be left blank"
        )
    parser.add_argument('store_id',
            type=int,
            required = True,
            help = "This field can't be left blank, every item needs a store_id"
        )

    # to authenticate before sending request use decorator
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item doesnt exists'}, 404

    def post(self, name):
        # if item with name already exists
        if ItemModel.find_by_name(name):
            return {'message': "item with given name '{}' already exists".format(name)}, 404
        #data = request.get_json()
        data = Item.parser.parse_args()
        # the new item posted will access name as given by us and price of old data
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "error occured while inserting item"}, 500  #inernal server error

        return item.json(), 201


    def delete(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "delete from items where name=?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        # return {'message': 'item deleted'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        #data = request.get_json()
        #item here is an item bject
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()

# defining class for itemlist
class Itemlist(Resource):
    def get(self):
        #return {'items': [item.json() for item in ItemModel.query.all()]}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} # same as above return statement
