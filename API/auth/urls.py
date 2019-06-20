from flask_restful import Api
from flask import Flask,Blueprint,jsonify
from auth.views import AuthResource
from flask_cors import CORS


auth_api = Blueprint('auth_api', __name__)
CORS(auth_api)
auth = Api(auth_api)

auth.add_resource(AuthResource, '/login/')


