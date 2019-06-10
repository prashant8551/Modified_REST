from app import db,ma
from helper.validators import ValidationHelper
from marshmallow import fields, pre_load, post_dump
from models.db import SalesItems,Items,Customer


class OrderSchema(ma.Schema):

    id=fields.Integer()
    c_id=fields.Integer(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    i_id=fields.Integer(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    sale_quantity=fields.Str( required=True,
        validate=ValidationHelper.must_not_be_blank)

    customer_name = fields.Str()
    c_address = fields.Str()
    c_mobileno=fields.Integer()
    bill_amount = fields.Str()


class BillSchema(ma.Schema):
    id = fields.Integer()
    c_id = fields.Integer()

    i_id = fields.Integer(
        required=False,
        validate=ValidationHelper.must_not_be_blank
    )
    bill_amount=fields.Str(
        required=False,
        validate=ValidationHelper.must_not_be_blank
    )
    o_id=fields.Integer()
