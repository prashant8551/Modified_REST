from flask_script import Manager
from models.create_models import CreateUsersCommand,CreateCustomerCommand,CreateItemsCommand,CreateSalesCommand
from flask.cli import FlaskGroup
from app import create_app,db

cli = FlaskGroup(create_app=create_app)
manager = Manager(create_app)


manager.add_command('create_users', CreateUsersCommand)
manager.add_command('create_customers', CreateCustomerCommand)
manager.add_command('create_items', CreateItemsCommand)
manager.add_command('create_sales', CreateSalesCommand)

if __name__ == "__main__":
    manager.run()