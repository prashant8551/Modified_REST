import configparser

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask,Blueprint
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_mail import Mail, Message


# Flask extensions
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
mail=Mail()


def create_app(main=True):
    app = Flask(__name__)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'prashantmali.info@gmail.com'
    app.config['MAIL_PASSWORD'] = "Prashant@#123"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'
    app.config['SECRET_KEY'] = 'dev'
    app.config['DEBUG'] = True
    app.config['SWAGGER'] = \
        {
        "swagger_version": "2.0",
        "title": "Mobile API",
        "uiversion": 3,
        "headers": [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
            ('Access-Control-Allow-Credentials', "true"),
        ],
        "specs": [
            {
                "version": "0.0.1",
                "title": "API m1",
                "endpoint": 'm1_spec',
                "description": 'This is the version 1 of Mobile API',
                "route": '/api/m1/'
            }
        ]
    }

    CORS(app, supports_credentials=True)
    # Setup Flask-SQLAlchemy

    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    # Setup Flask-Migrate
    migrate.init_app(app, db)


    from users.urls import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from customers.urls import customer_api
    app.register_blueprint(customer_api, url_prefix='/api')

    from Items.urls import item_api
    app.register_blueprint(item_api, url_prefix='/api')

    from orders.urls import order_api
    app.register_blueprint(order_api, url_prefix='/api')

    from auth.urls import auth_api
    app.register_blueprint(auth_api, url_prefix='/api')

    return app
