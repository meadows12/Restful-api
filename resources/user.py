
from flask_restful import Resource,reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,create_refresh_token

databse = "data.db"
class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type = str,
            required=True,
            help = "This Field cannot be empty"
    )

    parser.add_argument('password',
            type = str,
            required=True,
            help = "This Field cannot be empty"
    )

    def post(self): 
        data1 = UserRegister.parser.parse_args()

        if UserModel.find_username(data1['username']):
            return {"message":"User with this username already exists"},400

        user = UserModel(**data1)
        user.save_todb()

        return {"message":"User created successfully"},201

class UserLogin(Resource):

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

    @classmethod
    def post(cls):
        data = cls.parser.parse()

        user = UserModel.find_username(data['username'])

        if user and safe_str_cmp(user.password,data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return{
                'access_token':access_token,
                'refresh_token':refresh_token
            },200

        return {"message":"Invalis credentials"},201

