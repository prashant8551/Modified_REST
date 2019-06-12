from flask_restful import Api
from flask import Blueprint
from Items.views import ItemResource
from flask_cors import CORS

item_api = Blueprint('item_api', __name__)
CORS(item_api)
api = Api(item_api)

api.add_resource(ItemResource, '/items/', '/items/<int:item_id>')
