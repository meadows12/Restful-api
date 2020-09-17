import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel

databse = "data.db"
class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type = str,
            required=True,
            help = "This field cannot be empty"
    )

    parser.add_argument('password',
            type = str,
            required=True,
            help = "This field cannot be empty"
    )

    def post(self): 
        data1 = UserRegister.parser.parse_args()

        if UserModel.find_username(data1['username']):
            return {"message":"User with this username already exists"},400

        user = UserModel(**data1)
        user.save_todb()

        return {"message":"User created successfully"},201