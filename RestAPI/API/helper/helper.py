import logging
import sys
from flask import current_app, g
from flask import request, jsonify
from werkzeug.security import check_password_hash
from functools import wraps
from models.db import User
from users.serilizer import UserSchema
logger = logging.getLogger(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """

    try:
        user = User.query.filter(User.username == str(username)).first()
        if user and check_password_hash(user.password, password):
            g.current_user = user
            return True

    except Exception as e:
        logger.error("Auth: Error while fetching user data!" + str(e))

    return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return jsonify(err_msg='Could not verify your access level for this URL. '
                           'You have to login with proper credentials'), \
           401, {'WWW-Authenticate': 'Basic realm="Login Required"'}


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logger.debug("in auth decorator")
       # print("in auth decorator")
        if current_app.config['IS_AUTH_ENABLED']:
            logger.debug("AUTH is ENABLED")
            #print("auth is enabled")
            auth = request.authorization
            if not auth or not AuthUserHelper.check_for_auth(auth.username, auth.password):
                return authenticate()
            return f(*args, **kwargs)
        else:
            print("auth is disabled")
            logger.debug("AUTH is DISABLED")
    return decorated

class AuthHelper(object):

    def __init__(self, auth):
        self.user_pass = str(auth.username + ':' + auth.password)

    def get_user_json(self):
        user_schema = UserSchema()
        result = user_schema.dump(g.current_user)
        return result


class AuthUserHelper(object):

    def __init__(self):
        pass

    @staticmethod
    def check_for_auth(username, password):
        """This function is called to check if a username /
        password combination is valid.
        """
        user = User.query.filter_by(username=str(username)).first_or_404()

        if user and check_password_hash(user.password, password):
            g.current_user = user
            return user

        return False
