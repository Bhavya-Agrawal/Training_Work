from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Itemlist
from resources.store import Store, StoreList
#from models.item import ItemModel


app = Flask(__name__)

# sqlalchemy resides at the root folder ie Sqlalchemy here itself to look for data.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# if an object is created but not stored in database so sqlalchemy starts tracking so to make it off we are using this as false here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#define a secret key for app
app.secret_key = 'abc123'
api = Api(app)


jwt = JWT(app, authenticate, identity)  # call auth thus run as http://127.0.0.1:5000/auth on postman with Post request to get access-token

# for url to run on browser or postman add resource in api
api.add_resource(Item, '/item/<string:name>')  # to run the file as http://127.0.0.1/item/some_name
api.add_resource(Itemlist, '/items')
api.add_resource(UserRegister, '/user_register')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')

if __name__ == "__main__":
    # imorting here to avoid circular import due to importing table at top because of models, as this will cause running db again and again
    from db import db
    db.init_app(app)
    app.run(debug=True, port=5000)
