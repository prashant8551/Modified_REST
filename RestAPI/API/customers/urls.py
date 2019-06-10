from flask_restful import Api
from flask import Flask,Blueprint
from customers.views import CustomerResource

customer_api = Blueprint('customer_api', __name__)
api = Api(customer_api)

api.add_resource(CustomerResource, '/customers/','/customers/<int:customer_id>')
