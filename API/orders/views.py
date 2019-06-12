from flask import request,Response,jsonify
# from flask_restful import Api,Resource, fields
from flask_restful import Resource
from orders.serilizer import OrderSchema,BillSchema
from Items.serilizer import ItemSchema
from models.db import SalesItems,Customer,Items,Bill
from app import db
from app import mail,Message
import json
import logging
import traceback
from sqlalchemy.exc import DatabaseError
from app import spec


orders_schema = OrderSchema(many=True)
order_schema = OrderSchema()
item_schema = ItemSchema()
bills_schema = BillSchema(many=True)
bill_schema = BillSchema()

logger = logging.getLogger(__name__)


def get_request_data(request):

    """ get user request body json data """
    try:
        if request.mimetype == 'application/json':
            data = request.get_json()
        else:
            data = request.form.to_dict()

    except Exception as e:
        logger.error("Request Data: Fetching request data failed! " + str(e))
        return jsonify(err_msg="Error in fetching request data"), 400

    return data


class OrderResource(Resource):

    def get(self, order_id=None):

        """ get all selling item order details

              get:
                  description: Get a orders details
                  responses:
                    '200':
                      content:
                        application/json:
                          schema:
                            $ref: '#/components/schemas/Orders'

                     schemas:
                        Orders:
                          properties:
                            bill_amount:
                              type: string
                            c_address:
                              type: string
                            c_id:
                              format: int32
                              type: integer
                            c_mobileno:
                              format: int32
                              type: integer
                            customer_name:
                              type: string
                            i_id:
                              format: int32
                              type: integer
                            id:
                              format: int32
                              type: integer
                            sale_quantity:
                              type: string
                          required:
                          - c_id
                          - i_id
                          - sale_quantity
                          type: object
        """

        if order_id:
            sale_item = SalesItems.query.filter_by(id=order_id).first()
            if not sale_item:
                return json.dumps({"err_msg": "order id does not exit"})
            else:
                result_obj = order_schema.dump(sale_item).data
                return {'status': 'success', 'Sale-Item': result_obj}, 200
        else:
            sales_items = SalesItems.query.all()
            sales_items = orders_schema.dump(sales_items).data
            with open("orders/Orders.json", "w") as f:
                print("Success")
                f.write(json.dumps("........Sale Items Details..........") \
                + ",\n" + json.dumps(sales_items, indent=4,sort_keys=False) + ",\n")
            return {'status': 'success', 'Sale-Items': sales_items}, 200

    def post(self):

        """ create order for selling items

            components:
                  schemas:
                    Orders:
                      properties:
                        bill_amount:
                          type: string
                        c_address:
                          type: string
                        c_id:
                          format: int32
                          type: integer
                        c_mobileno:
                          format: int32
                          type: integer
                        customer_name:
                          type: string
                        i_id:
                          format: int32
                          type: integer
                        id:
                          format: int32
                          type: integer
                        sale_quantity:
                          type: string
                      required:
                      - c_id
                      - i_id
                      - sale_quantity
                      type: object
        """

        response_obj = Response(mimetype='application/json')
        data = get_request_data(request)
        order_data = data.get('order', None)
        if not order_data:
            return {'message': 'No input data provided'}, 400

        data, errors = order_schema.load(order_data)
        #print(errors,"errors.....................")
        if errors:
            return {"status": "error", "data": errors}, 422
        try:
            customer = Customer.query.filter_by(c_id=int(data['c_id'])).first()
            if not customer:
                response_obj.data = json.dumps({"msg": "please enter valid customer ID"})
            item = Items.query.filter_by(i_id=int(data['i_id'])).first()

            if not item:
                response_obj.data = json.dumps({"msg": "please enter valid Item ID"})

            total_quantity = item.item_quantity
            #print(total_quantity,"total qantity................")
            sale_quantity = data['sale_quantity']
            #print(sale_quantity, "....sale_quantity")

            print(sale_quantity,"sale_quantity")
            if int(sale_quantity) < 0:
              response_obj.data = json.dumps({"msg": "please enter positive sale quantity"}) 
            else:
              if int(total_quantity) > 0 and int(sale_quantity) <= int(total_quantity):
                  sale_item = SalesItems(customer.c_id, item.i_id, sale_quantity)
                  item.item_quantity = int(total_quantity) - int(sale_quantity)

                  ''' After selling item update Items table '''

                  db.session.add_all([sale_item,item])
                  db.session.commit()
                  bill_amount = int(sale_quantity) * int(item.item_price)

                  s_id = SalesItems.query.filter_by(i_id=item.i_id).first()
                  bill = Bill(customer.c_id, item.i_id, s_id.id, bill_amount)

                  """ send bill to the customer """

                  msg = Message('Invoice', sender='prashantmali.info@gmail.com', recipients=[customer.c_email])
                  msg.body = f"Invoice Details: \n Item name:{item.item_name} \n Quantity:{sale_quantity} \n Total amount:{bill_amount}"
                  mail.send(msg)

                  #print(f"Item name:{item.item_name} \n Item Quantity:{sale_quantity} \n Total Bill:{bill_amount}")
                  
                  db.session.add(bill)
                  db.session.commit()
                  item_cust_info = order_schema.dump(sale_item).data
                  bill_info = bill_schema.dump(bill).data
                  item_info = item_schema.dump(item).data

                  """ Generate Yaml file """
                  #spec.components.schema("Orders", schema=OrderSchema)
                  #print(spec.to_yaml())
                  response_obj.data = json.dumps(({"status": 'success', "Order": [{"Item_info":item_info},{"Sale-Item-Customer":item_cust_info},{"bill":bill_info},]}))
              else:
                  response_obj.data = json.dumps({"msg":"please select less sale quantity from available quantity"})

        except Exception as e:
             print(e)

        return response_obj

    def delete(self, order_id):

        """  view for cancel order/item """
        response_obj = Response(mimetype='application/json')

        try:

            order = SalesItems.query.get(int(order_id))
            if not order:
                response_obj.data = json.dumps({
                    "err_msg": "Order id doesn't exists!"
                })
            else:
                print(order.id,"..........")

                item = Items.query.filter_by(i_id=int(order.i_id)).first()

                customer = Customer.query.get(int(order.c_id))

                """ After cancel order update Item table """

                item.item_quantity = int(item.item_quantity) + int(order.sale_quantity)
                db.session.add(item)
                db.session.commit()

                """ send bill to the customer """

                msg = Message('Bill', sender='prashantmali.info@gmail.com', recipients=[customer.c_email])
                msg.body = f"Cancel..........\n Order id :  {order_id} \n Item name:{item.item_name} \n Item Price:{int(item.item_price)*int(order.sale_quantity)}"
                mail.send(msg)

                """ Remove order id """
                db.session.delete(order)
                db.session.commit()

                #print(f"Cancel Order ..........\n customer_name:{customer.customer_name} \n  Order id :  {order_id} \n Item name:{item.item_name} \n Item Price:{item.item_price}"
                logger.info("Delete order: order deleted successfully.")
                # spec.components.schema("Orders", schema=OrderSchema)
                # print(spec.to_yaml())
                response_obj.data = json.dumps({"msg":"order deleted successfully"})
                print("order deleted")
                response_obj.status_code = 200

        except DatabaseError as de:
            logger.error("Delete order: Error while deleting order " + str(de))
            response_obj.data = json.dumps({
                "err_msg": "Order doesn't exist"
            })
            response_obj.status_code = 400

        except Exception as e:
            logger.error("Delete order: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            response_obj.data = json.dumps({
                "err_msg": "Order doesn't exist"
            })
            response_obj.status_code = 400

        return response_obj

class BillResource(Resource):

    """ get all selling item order bill details """

    def get(self, bill_id=None):
        if bill_id:
            bill = Bill.query.filter_by(id=bill_id).first()
            if not bill:
                return {"err_msg": "bill id does not exit"}
            else:
                result_obj = bill_schema.dump(bill).data
                return {'status': 'success', 'Bill-Item': result_obj}, 200
        else:
            bills = Bill.query.all()
            bills = bills_schema.dump(bills).data
            return {'status': 'success', 'Bills': bills}, 200


    def delete(self, bill_id):

        """ delete bill """

        response_obj = Response(mimetype='application/json')
        try:
            bill = Bill.query.get_or_404(int(bill_id))
            db.session.delete(bill)
            db.session.commit()
            logger.info("Delete Bill: Bill deleted successfully.")
            response_obj.data = json.dumps({"msg":"Bill deleted successfully"})
            print("Bill deleted")
            response_obj.status_code = 200

        except DatabaseError as de:
            logger.error("Delete order: Error while deleting order " + str(de))
            response_obj.data = json.dumps({
                "err_msg": "Bill ID doesn't exist"
            })
            response_obj.status_code = 400

        except Exception as e:
            logger.error("Delete Bill: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            response_obj.data = json.dumps({
                "err_msg": "Bill ID doesn't exist"
            })
            response_obj.status_code = 400

        return response_obj

