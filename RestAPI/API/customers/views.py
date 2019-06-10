from flask import request,Response,jsonify
from flask_restful import Resource
from customers.serilizer import CustomerSchema
from models.db import Customer,Bill
from app import db
import json
import logging
import traceback
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import DatabaseError, IntegrityError


customers_schema = CustomerSchema(many=True)
customer_schema = CustomerSchema()

logger = logging.getLogger(__name__)


def get_request_data(request):
    try:
        if request.mimetype == 'application/json':
            data = request.get_json()
        else:
            data = request.form.to_dict()

    except Exception as e:
        logger.error("Request Data: Fetching request data failed! " + str(e))
        return jsonify(err_msg="Error in fetching request data"), 400

    return data


class CustomerResource(Resource):

    def get(self,customer_id=None):

        """  view method for customer details  """

        if customer_id:
            # db.session.query(Bill).delete()
            # db.session.commit()
            user = Customer.query.filter_by(c_id=customer_id).first()
            if not user:
                return json.dumps({"err_msg": "customer does not exit"})
            else:
                result_obj = customer_schema.dump(user).data
                return {'status': 'success', 'customer': result_obj}, 200
        else:
            customers = Customer.query.all()
            customers = customers_schema.dump(customers).data
            return {'status': 'success', 'customers': customers}, 200


    def post(self):

        """ method view for create new customer """

        response_obj = Response(mimetype='application/json')

        data = get_request_data(request)

        customer_data = data.get('customer', None)

        if not customer_data:
            return {'message': 'No input data provided'}, 400
            # Validate and deserialize input
        data, errors = customer_schema.load(customer_data)

        print(errors,"....................")
        if errors:
            return {"status": "error", "data": errors}, 422

        customer_name=data['customer_name']
        c_address = data['c_address']
        c_mobileno =data['c_mobileno']
        c_email =data['c_email']
        customer = Customer(customer_name,c_address,c_mobileno,c_email)
        db.session.add(customer)
        db.session.commit()

        result_obj = customer_schema.dump(customer).data
        response_obj.data = json.dumps(result_obj)

        return response_obj

    def put(self,customer_id):

        """ method view for update customer details """
        response_obj = Response(mimetype='application/json')

        data = get_request_data(request)
        print("data.......",data)#data....... {'user': {'apps': [2], 'username': 'dipak', 'first_name': 'dipak', 'last_name': 'patil'}}

        user_data = data.get('customer',
                             None)
        if not user_data:
            response_obj.data = json.dumps({
                "err_msg": "User details are not provided!"
            })
            response_obj.status_code = 400

        else:
            try:
                data, errors = customer_schema.load(user_data)
                customer = Customer.query.get(int(customer_id))

                if not customer:
                    logger.error("Edit customer: Customer doesn't exists! ")
                    response_obj.data = json.dumps({
                        "err_msg": "Customer doesn't exists!"
                    })
                else:
                    customer.customer_name = data['customer_name']
                    customer.c_address = data['c_address']
                    customer.c_mobileno = data['c_mobileno']
                    customer.c_email = data['c_email']
                    db.session.add(customer)
                    db.session.commit()
                    result_obj = customer_schema.dump(customer)
                    logger.info("Edit Customer: Customer updated successfully.")
                    print("Customer edited:")
                    response_obj.data = json.dumps(({'status': 'success', 'data': result_obj}, 200))
                    response_obj.status_code = 200

            except NotFound as ne:
                logger.error("Edit User: Error while editing user record. " + str(ne))
                response_obj.data = json.dumps({
                    "err_msg": "App doesn't exists!"
                })
                response_obj.status_code = 404

            except ValueError as ve:
                logger.error("Edit User: Error while editing user record. " + str(ve))
                response_obj.data = json.dumps({
                    "err_msg": "Error processing request! Please check for request parameters."
                })
                response_obj.status_code = 400

            except DatabaseError as de:
                logger.error("Edit User: Error while updating user record. " + str(de))
                response_obj.data = json.dumps({
                    "err_msg": "Error while updating user record!"
                })
                response_obj.status_code = 400

            except Exception as e:
                # logger.error("Edit User: Error while processing request.\n"
                #              + str(e) + "\n" + str(traceback.print_exc()))
                response_obj.data = json.dumps({
                    "err_msg": "Error while updating user record!"
                })
                response_obj.status_code = 400

        return response_obj


    def delete(self, customer_id):

        """ method delete() view for delete customer """

        response_obj = Response(mimetype='application/json')
        try:
            customer = Customer.query.get_or_404(int(customer_id))
            db.session.delete(customer)
            db.session.commit()
            logger.info("Delete customer: customer deleted successfully.")
            response_obj.data = json.dumps({"msg":"customer deleted successfully"})
            print("customer deleted")
            response_obj.status_code = 200

        except NotFound as ne:
            logger.error("Delete User: Error while deleting user record. " + str(ne))
            response_obj.data = json.dumps({
                "err_msg": "User doesn't exists!"
            })
            response_obj.status_code = 404

        except DatabaseError as de:
            logger.error("Delete User: Error while deleting user record. " + str(de))
            response_obj.data = json.dumps({
                "err_msg": "Error while deleting user record!"
            })
            response_obj.status_code = 400

        except Exception as e:
            logger.error("Delete User: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            response_obj.data = json.dumps({
                "err_msg": "Error while deleting user record!"
            })
            response_obj.status_code = 400

        return response_obj

