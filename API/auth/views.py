import logging
import traceback
from flask import json,session
from werkzeug.exceptions import NotFound
from flask import request,Response
from flask_restful import Resource
from helper.helper import AuthHelper,AuthUserHelper
logger = logging.getLogger(__name__)

class AuthResource(Resource):
    def get(self):
        """
             Check for user credentials
             ---
                responses:
                    200:
                        description: Returns user object with assigned apps.
                    401:
                        description: For invalid credentials.
        """
        auth = request.authorization
        response_obj = Response(mimetype='application/json')

        if not auth:
            response_obj.data = json.dumps({
                "err_msg": "No authorization details are present in the header!"
            })
            response_obj.status_code = 400

        else:
            try:
                print("auth.username.....",auth.username)
                print("auth.password......",auth.password)
                if AuthUserHelper.check_for_auth(auth.username, auth.password):
                    session['logged_in'] = True
                    logger.info("Login: Login Successful!")
                    auth_helper = AuthHelper(auth)
                    #print(auth_helper)
                    print("login successfully...........................")
                    result_obj = auth_helper.get_user_json()
                    response_obj.data = json.dumps({'status': 'success', 'User': result_obj})

                else:
                    logger.error("Login: Invalid credentials.")
                    response_obj.data = json.dumps({
                        "err_msg": "Login Failed! Invalid Credentials"
                    })
                    response_obj.status_code = 401

            except NotFound as nf:
                logger.error("Login: Error while logging in user. User doesn't exists!. " + str(nf))
                response_obj.data = json.dumps({
                    "err_msg": "User doesn't exists!"
                })
                response_obj.status_code = 404

            except Exception as e:
                logger.error("Login: Error while fetching user data!\n"
                             + str(e) + "\n" + str(traceback.print_exc()))
                response_obj.data = json.dumps({
                    "err_msg": "Login Failed! Error in processing request."
                })
                response_obj.status_code = 400

        return response_obj

