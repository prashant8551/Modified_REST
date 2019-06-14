from flask import request,Response,jsonify
from flask_restful import Resource
from Items.serilizer import ItemSchema
from models.db import Items
from app import db
import json
import logging
import traceback
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy import desc

items_schema = ItemSchema(many=True)
item_schema = ItemSchema()

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


class ItemResource(Resource):

    def get(self, item_id=None):
        """ get all item list data

                 get:
                  description: Get a Items details
                  responses:
                    '200':
                      content:
                        application/json:
                          schema:
                            $ref: '#/components/schemas/Items'

                components:
                      schemas:
                        Items:
                          properties:
                            i_id:
                              format: int32
                              type: integer
                            item_name:
                              type: string
                            item_price:
                              type: string
                            item_quantity:
                              type: string
                          required:
                          - item_name
                          - item_price
                          - item_quantity
                          type: object
        """

        if item_id:
            item = Items.query.filter_by(i_id=item_id).first()
            if not item:
                return json.dumps({"err_msg": "item does not exit"})
            else:
                result_obj = item_schema.dump(item).data
                return {'status': 'success', 'Item': result_obj}, 200
        else:
            items = Items.query.order_by(desc(Items.purchase_date)).all()
            items = items_schema.dump(items).data
            with open("Items/Items.json", "w") as f:
                print("Success")
                f.write(json.dumps("........Add Items Details..........") \
                + ",\n" + json.dumps(items, indent=4,sort_keys=False) + ",\n")
            return {'status': 'success', 'Items': items}, 200

    def post(self):

        """ Add new item  """

        response_obj = Response(mimetype='application/json')

        data = get_request_data(request)

        item_data = data.get('item', None)

        if not item_data:
            return {'message': 'No input data provided'}, 400
            # Validate and deserialize input
        data, errors = item_schema.load(item_data)

        print(errors,"....................")
        if errors:
            return {"status": "error", "data": errors}, 422

        item_name = data['item_name']
        item_quantity = data['item_quantity']
        item_price = data['item_price']

        item = Items(item_name,item_quantity,item_price)
        db.session.add(item)
        db.session.commit()

        result_obj = item_schema.dump(item).data
        response_obj.data = json.dumps({"status":"success","Item":result_obj})

        return response_obj

    def put(self,item_id):

        """ update item details """

        response_obj = Response(mimetype='application/json')

        data = get_request_data(request)

        item_data = data.get('item',None)

        if not item_data:
            response_obj.data = json.dumps({
                "err_msg": "Items details are not provided!"
            })
            response_obj.status_code = 400

        else:
            try:
                data, errors = item_schema.load(item_data)
                item = Items.query.get(int(item_id))

                if not item:
                    logger.error("Edit item: item doesn't exists! ")
                    response_obj.data = json.dumps({
                        "err_msg": "item id doesn't exists!"
                    })
                else:
                    item.item_name = data['item_name']
                    item.item_price = data['item_price']
                    item.item_quantity = data['item_quantity']
                    db.session.add(item)
                    db.session.commit()
                    result_obj = item_schema.dump(item).data
                    logger.info("Edit Item: Item updated successfully.")
                    print("Item edited:")
                    response_obj.data = json.dumps({"status": "success", "Item": result_obj})

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
                response_obj.data = json.dumps({
                    "err_msg": "Error while updating user record!"
                })
                response_obj.status_code = 400

        return response_obj


    def delete(self, item_id):

        """ Remove item """

        response_obj = Response(mimetype='application/json')
        try:
            item = Items.query.get_or_404(int(item_id))
            db.session.delete(item)
            db.session.commit()

            logger.info("Delete item: Item deleted successfully.")
            response_obj.data = json.dumps({"msg": "Item deleted successfully"})
            print("item deleted")
            response_obj.status_code = 200

        except NotFound as ne:
            logger.error("Delete Item: Error while deleting user record. " + str(ne))
            response_obj.data = json.dumps({
                "err_msg": "Item doesn't exists!"
            })
            response_obj.status_code = 404

        except DatabaseError as de:
            logger.error("Delete Item: Error while deleting Item record. " + str(de))
            response_obj.data = json.dumps({
                "err_msg": "Error while deleting Item record!"
            })
            response_obj.status_code = 400

        except Exception as e:
            logger.error("Delete Item: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            response_obj.data = json.dumps({
                "err_msg": "Error while deleting Item record!"
            })
            response_obj.status_code = 400

        return response_obj

