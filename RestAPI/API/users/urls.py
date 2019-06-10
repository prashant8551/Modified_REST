from flask_restful import Api
from flask import Flask,Blueprint
from users.views import UsersResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

print("helllo world.............")

api.add_resource(UsersResource, '/users/','/users/<int:user_id>')
