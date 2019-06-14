from app import db,ma
from helper.validators import ValidationHelper
from marshmallow import Schema, fields, pre_load, validate

class CustomerSchema(ma.Schema):
    c_id=fields.Integer()

    customer_name = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    c_address= fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    c_mobileno=fields.Integer(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )

    c_email = fields.Email(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )

    register_date = fields.DateTime('%d-%m-%y')
    
    modified_date = fields.DateTime('%d-%m-%y')



