from flask import request,Response,jsonify
from flask_restful import Resource
from customers.serilizer import CustomerSchema
from models.db import Customer,Bill,SalesItems
from app import db
import json
import logging
import traceback
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import DatabaseError, IntegrityError
from app import spec

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

        """
        :param customer_id: It is use for view customer details
        :return: Customer details
        """
        """ paths:
            get:
              description: Get a customers details
              responses:
                '200':
                  content:
                    application/json:
                      schema:
                        $ref: '#/components/schemas/Customer'

                components:
                  schemas:
                    Customer:
                      properties:
                        c_address:
                          type: string
                        c_email:
                          format: email
                          type: string
                        c_id:
                          format: int32
                          type: integer
                        c_mobileno:
                          format: int32
                          type: integer
                        customer_name:
                          type: string
                      type: object

            """
        if customer_id:
            customer = Customer.query.filter_by(c_id=customer_id).first()
            if not customer:
                return {"err_msg": "customer id does not exit"}
            else:
                result_obj = customer_schema.dump(customer).data
                return {'status': 'success', 'customer': result_obj}, 200
        else:
            customers = Customer.query.all()
            customers = customers_schema.dump(customers).data
            #spec.components.schema("Users", schema=CustomerSchema)
            #print(spec.to_yaml())
            with open("customers/Customers.json", "w") as f:
                print("Success")
                f.write(json.dumps("........Register Customers Details..........") \
                + ",\n" + json.dumps(customers, indent=4,sort_keys=False) + ",\n")
            return {'status': 'success', 'customers': customers}, 200


    def post(self):
        """ method view for create new customer
            schemas:
                Customer:
                  properties:
                    c_address:
                      type: string
                    c_email:
                      format: email
                      type: string
                    c_id:
                      format: int32
                      type: integer
                    c_mobileno:
                      format: int32
                      type: integer
                    customer_name:
                      type: string
                  required:
                  - c_address
                  - c_email
                  - c_mobileno
                  - customer_name
                  type: object
        """

        response_obj = Response(mimetype='application/json')

        data = get_request_data(request)

        customer_data = data.get('customer', None)

        if not customer_data:
            return {'message': 'No input data provided'}, 400
            # Validate and deserialize input
        data, errors = customer_schema.load(customer_data)
        if errors:
            return {"status": "error", "data": errors}, 422

        customer_name = data['customer_name']
        c_address = data['c_address']
        c_mobileno = data['c_mobileno']
        c_email = data['c_email']
        customer = Customer(customer_name,c_address,c_mobileno,c_email)
        db.session.add(customer)
        db.session.commit()

        result_obj = customer_schema.dump(customer).data
        response_obj.data = json.dumps(result_obj)
        # spec.components.schema("Customer", schema=CustomerSchema)
        # print(spec.to_yaml())
        return response_obj

    def put(self,customer_id):
        """
        :param customer_id: It is use for update customer details
        :return: Customer details
        """
        """ method view for update customer details
            schemas:
                Customer:
                  properties:
                    c_address:
                      type: string
                    c_email:
                      format: email
                      type: string
                    c_id:
                      format: int32
                      type: integer
                    c_mobileno:
                      format: int32
                      type: integer
                    customer_name:
                      type: string
                  required:
                  - c_address
                  - c_email
                  - c_mobileno
                  - customer_name
                  type: object
        """

        response_obj = Response(mimetype='application/json')

        data = get_request_data(request)
        user_data = data.get('customer',
                             None)
        if not user_data:
            response_obj.data = json.dumps({
                "err_msg": "Customer details are not provided!"
            })
            response_obj.status_code = 400

        else:
            try:
                data, errors = customer_schema.load(user_data)
                customer = Customer.query.get(int(customer_id))

                if not customer:
                    logger.error("Edit customer: Customer doesn't exists! ")
                    response_obj.data = json.dumps({
                        "err_msg": "Customer id doesn't exists!"
                    })
                else:
                    customer.customer_name = data['customer_name']
                    customer.c_address = data['c_address']
                    customer.c_mobileno = data['c_mobileno']
                    customer.c_email = data['c_email']
                    db.session.add(customer)
                    db.session.commit()
                    result_obj = customer_schema.dump(customer).data
                    logger.info("Edit Customer: Customer updated successfully.")
                    print("Customer edited:")
                    response_obj.data = json.dumps({"Customer":result_obj})
                    # spec.components.schema("Customer", schema=CustomerSchema)
                    # print(spec.to_yaml())
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

            except Exception:
                response_obj.data = json.dumps({
                    "err_msg": "Error while updating user record!"
                })
                response_obj.status_code = 400

        return response_obj


    def delete(self, customer_id):
        """
        :param customer_id: It is use for remove customer
        :return: Delete Customer
        """
        """ method delete() view for delete customer """

        response_obj = Response(mimetype='application/json')
        try:
            customer = Customer.query.get_or_404(int(customer_id))
            db.session.delete(customer)
            db.session.commit()
            logger.info("Delete Customer: customer deleted successfully.")
            response_obj.data = json.dumps({"msg":"customer deleted successfully"})
            print("customer deleted")
            response_obj.status_code = 200

        except NotFound as ne:
            logger.error("Delete User: Error while deleting user record. " + str(ne))
            response_obj.data = json.dumps({
                "err_msg": "Customer id doesn't exists!"
            })
            response_obj.status_code = 404

        except DatabaseError as de:
            logger.error("Delete Customer: Error while deleting user record. " + str(de))
            response_obj.data = json.dumps({
                "err_msg": "Error while deleting user record!"
            })
            response_obj.status_code = 400

        except Exception as e:
            logger.error("Delete Customer: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            response_obj.data = json.dumps({
                "err_msg": "Error while deleting user record!"
            })
            response_obj.status_code = 400

        return response_obj

