from flask import request,Response,jsonify
from flask_restful import Resource
from users.serilizer import UserSchema
from models.db import User
from app import db
import json
import logging
import traceback
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import DatabaseError, IntegrityError


users_schema = UserSchema(many=True)
user_schema = UserSchema()

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


class UsersResource(Resource):

    def get(self):
        users = User.query.all()
        users = users_schema.dump(users).data
        return {'status': 'success', 'data': users}, 200


    def post(self):

        response_obj = Response(mimetype='application/json')

        data = get_request_data(request)

        user_data = data.get('user', None)

        if not user_data:
            return {'message': 'No input data provided'}, 400
            # Validate and deserialize input
        data, errors = user_schema.load(user_data)

        print(errors,"....................")
        if errors:
            return {"status": "error", "data": errors}, 422
        user = User(username=data['username'],password=data['password'],role=data['role'])
        db.session.add(user)
        db.session.commit()

        result_obj = user_schema.dump(user).data
        response_obj.data = json.dumps(result_obj)

        return response_obj

    def put(self,user_id):

        response_obj = Response(mimetype='application/json')

        data = get_request_data(request)
        print("data.......",data)#data....... {'user': {'apps': [2], 'username': 'dipak', 'first_name': 'dipak', 'last_name': 'patil'}}

        user_data = data.get('user',
                             None)
        if not user_data:
            response_obj.data = json.dumps({
                "err_msg": "User details are not provided!"
            })
            response_obj.status_code = 400

        else:
            try:
                data, errors = user_schema.load(user_data)
                user = User.query.get(int(user_id))
                print("user.....", user)
                print(user.id, "......id.....")  # gets user id
                print(user.username, ".......")
                print(user.password, ".......")

                if not user:
                    logger.error("Edit User: User doesn't exists! ")
                    response_obj.data = json.dumps({
                        "err_msg": "User doesn't exists!"
                    })
                else:
                    user.username = data['username']
                    print(user.username,"....user.first_name....")
                    user.password = data['password']
                    print(user.password)
                    db.session.add(user)
                    db.session.commit()
                    result_obj = user_schema.dump(user)
                    logger.info("Edit User: User updated successfully.")
                    print("user edited:")
                    response_obj.data = json.dumps(result_obj)
                    response_obj.status_code = 200

            # TODO: Handling validation error. Need to write appropriate serializer.

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


    def delete(self, user_id):
        """
             DELETE Deletes a user with user_id.
             ---
                parameters:
                  - name: user_id
                    type: integer
                    in: path
                    required: true
                    description: ID of a user.
                responses:
                    200:
                        description: Deletes the user with user id.
                    400:
                        description: Any DB error occurred.
                    401:
                        description: Only Admin Role Users can access.
        """
        response_obj = Response(mimetype='application/json')

        try:
            user = User.query.get_or_404(int(user_id))
            db.session.delete(user)
            db.session.commit()
            logger.info("Delete User: User deleted successfully.")
            response_obj.data = json.dumps({"msg":"user deleted successfully"})
            print("user deleted")
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

