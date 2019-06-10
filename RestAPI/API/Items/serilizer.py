from app import db,ma
from helper.validators import ValidationHelper
from marshmallow import Schema, fields, pre_load, validate

class ItemSchema(ma.Schema):

    i_id=fields.Integer()
    item_name = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )

    item_quantity = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )

    item_price = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
