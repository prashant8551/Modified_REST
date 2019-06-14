
from flask import g

from users.serilizer import UserSchema


class AuthHelper(object):

    def __init__(self, auth):
        self.user_pass = str(auth.username + ':' + auth.password)

    # def create_user_auth_token(self):
    #     b64_string = base64.b64encode(self.user_pass.encode("utf-8"))
    #     print(b64_string,".....b64_string")
    #     user_token = UserAuthToken(user=g.current_user, token=b64_string)
    #     print("user_token=>",user_token.token)
    #     g.current_user.token.append(user_token)
    #     db.session.commit()

    def get_user_json(self):
        user_schema = UserSchema()
        result = user_schema.dump(g.current_user)


        # print(result,"..........result")
        # user_apps_helper = UserAppsHelper()
        # result['user']['apps'] = user_apps_helper.get_user_apps_data()
        #
        # #print(result['user'],"....result['user']")
        # print(result['user']['apps'],"....result['user']")
        #
        # try:
        #     result['user']['token'] = str((g.current_user.token[0]).token.decode("utf-8"))
        # except AttributeError:
        #     result['user']['token'] = str((g.current_user.token[0]).token)

        return result
