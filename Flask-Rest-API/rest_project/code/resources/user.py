from models.user import UserModel
from flask import request
from flask_restful import Resource


class UserRegister(Resource):

    def post(self):

        data = request.get_json()

        if UserModel.find_by_username(data.get('username')):
            return {'message': 'A user with username %s does exist' % data.get('username')}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created successfully'}, 201


