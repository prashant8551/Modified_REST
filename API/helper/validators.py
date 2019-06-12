from marshmallow import ValidationError


class ValidationHelper(object):

    def __init__(self):
        pass

    @staticmethod
    def must_not_be_blank(data):
        if not data:
            raise ValidationError('Field cannot be blank!')
