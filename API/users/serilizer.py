from app import db,ma
from helper.validators import ValidationHelper
from marshmallow import Schema, fields, pre_load, validate
from marshmallow_enum import EnumField
from models.db import  RolesAvailable

class UserSchema(ma.Schema):

    id=fields.Integer()
    username = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    # print(".........Username", username)
    password = fields.Str(
        required=True,
        # load_only=True,
        validate=ValidationHelper.must_not_be_blank)

    role = EnumField(RolesAvailable, by_value=True)