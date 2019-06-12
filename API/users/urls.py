from flask_restful import Api
from flask import Flask,Blueprint
from users.views import UsersResource
from flask_cors import CORS

api_bp = Blueprint('api', __name__)
CORS(api_bp)
api = Api(api_bp)


api.add_resource(UsersResource, '/users/','/users/<int:user_id>')
