from app import db,ma
from helper.validators import ValidationHelper
from marshmallow import fields,post_dump,pre_load
from pytz import timezone
from models.db import SalesItems


class CustomerSchema(ma.Schema):
    c_id = fields.Str()
    customer_name = fields.Str()
    c_address = fields.Str()
    c_mobileno = fields.Integer()
    c_email = fields.Str()

class ItemSchema(ma.Schema):
    i_id = fields.Integer()
    item_quantity = fields.Str()
    item_name = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    item_price = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )

class OrderSchema(ma.Schema):

    id = fields.Integer()
    c_id = fields.Integer(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    i_id = fields.Integer(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    sale_quantity = fields.Str( required=True,
        validate = ValidationHelper.must_not_be_blank)

    sale_date = fields.DateTime('%d-%m-%Y')

    customer = fields.Nested(CustomerSchema)
    item = fields.Nested(ItemSchema)
    #bill = fields.Nested(BillSchema)


class BillSchema(OrderSchema):
    id = fields.Integer()
    bill_amount = fields.Str(
        required=False,
        validate=ValidationHelper.must_not_be_blank
    )
    o_id = fields.Integer()

    bill_date = fields.DateTime('%d-%m-%y')

