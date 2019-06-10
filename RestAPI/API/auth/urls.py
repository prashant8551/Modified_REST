from flask_restful import Api
from flask import Flask,Blueprint,jsonify
from auth.views import AuthResource

auth_api = Blueprint('auth_api', __name__)
auth = Api(auth_api)

print("helllo world.............")

auth.add_resource(AuthResource, '/login/')


