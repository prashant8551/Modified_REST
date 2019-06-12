from flask_restful import Api

from flask import Flask,Blueprint
from orders.views import OrderResource,BillResource
from flask_cors import CORS


order_api = Blueprint('order_api', __name__)
CORS(order_api)
api = Api(order_api)

api.add_resource(OrderResource, '/orders/', '/orders/<int:order_id>')
api.add_resource(BillResource, '/bills/', '/bill/<int:bill_id>')


