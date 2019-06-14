from flask_script import Command

from app import db

class CreateUsersCommand(Command):

    def run(self):
        create_users()
        print('Users created.')

def create_users():
    """ Create users """
    # Create all tables if not exists
    db.create_all()
    db.session.commit()


class CreateCustomerCommand(Command):

    def run(self):
        create_customers()
        print('customers created.')


def create_customers():
    """ Create users """
    # Create all tables if not exists
    db.create_all()
    db.session.commit()


class CreateItemsCommand(Command):

    def run(self):
        create_items()
        print('Items created.')


def create_items():
    """ Create users """
    # Create all tables if not exists
    db.create_all()
    db.session.commit()


class CreateSalesCommand(Command):

    def run(self):
        create_sales()
        print('Items created.')


def create_sales():
    """ Create users """
    # Create all tables if not exists
    db.create_all()
    db.session.commit()

