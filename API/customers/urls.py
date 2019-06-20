from flask_restful import Api
from flask import Blueprint
from customers.views import CustomerResource
from flask_cors import CORS

customer_api = Blueprint('customer_api', __name__)
CORS(customer_api)

api = Api(customer_api)
api.add_resource(CustomerResource, '/customers/','/customers/<int:customer_id>')
