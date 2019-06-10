from flask_restful import Api
from flask import Blueprint
from Items.views import ItemResource

item_api = Blueprint('item_api', __name__)
api = Api(item_api)

api.add_resource(ItemResource, '/items/','/items/<int:item_id>')
