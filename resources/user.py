import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
    'username',
    type = str,
    required = True,
    help = "This field can't be left null"
    )

    parser.add_argument('password',
    type = str,
    required = True,
    help = "This field can;t be left null"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "The user with the given username already exists"}, 400

        #user = UserModel(data['username'], data['password'])
        user = UserModel(**data) #same as above line
        user.save_to_db()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "Insert into users values(Null,?,?)"
        # cursor.execute(query,(data['username'], data['password']))
        #
        # connection.commit()
        # connection.close()

        # json takes value in "" so use " " instead of ' '
        return {"message": "user created successfully"}, 201
