from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify
from marshmallow import Schema, fields
from app import ma,db
from models.db import Customer,SalesItems,Bill,Items,User
from orders.serilizer import OrderSchema,BillSchema
from Items.serilizer import ItemSchema
from users.serilizer import UserSchema


# Create an APISpec
spec = APISpec(
    title="Swagger MobileStore",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Optional marshmallow support
#
# @app.route("/get")
# def get():
#     """ Get Orders details
#     ---
#     get:
#       description: Get a orders details
#       responses:
#         200:
#           content:
#             application/json:
#               schema: OrderSchema
#     """
#
#     orders = SalesItems.query.all()
#     return jsonify(OrderSchema(many=True).dump(orders).data)



# @app.route("/get")
# def get():
#     """ Get Items details
#     ---
#     get:
#       description: Get a Items details
#       responses:
#         200:
#           content:
#             application/json:
#               schema: ItemSchema
#     """
#
#     users = User.query.all()
#     return jsonify(UserSchema(many=True).dump(users).data)

@app.route("/get")
def get():
    """ Get Users details
    ---
    get:
      description: Get a Users details
      responses:
        200:
          content:
            application/json:
              schema: UserSchema
    """

    users = User.query.all()
    spec.components.schema("Users", schema=UserSchema)

    print(spec.to_yaml())
    return jsonify(UserSchema(many=True).dump(users).data)

# spec.components.schema("Category", schema=CategorySchema)



with app.test_request_context():
    spec.path(view=get)
# #
# import json
# print(json.dumps(spec.to_dict(), indent=2))
#
print(spec.to_yaml())
# print(spec.to_yaml())


if __name__ == "__main__":
    app.run(debug=True)
