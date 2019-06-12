from datetime import datetime
from flask_user import UserMixin
from werkzeug.security import generate_password_hash
from app import db,ma
from sqlalchemy import CheckConstraint
import enum


class RolesAvailable(enum.Enum):

    admin = "admin"
    member = "sale-person"

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True, index=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    role = db.Column(db.Enum(RolesAvailable))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, username, password,role):
        self.username = username
        self.password = generate_password_hash(password)

        user_role=role
        if user_role:
            self.role = user_role
        else:
            self.role = RolesAvailable.member


class Customer(db.Model):
    __tablename__='customers'
    c_id = db.Column(db.Integer,primary_key=True)
    customer_name = db.Column(db.String(255),nullable=False)
    c_address =db.Column(db.String(255),nullable=False)
    c_mobileno=db.Column(db.Integer,nullable=False)
    c_email=db.Column(db.String(255),nullable=False)
    register_date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    sales=db.relationship("SalesItems",backref=db.backref("customers"))

    def __init__(self,customer_name,c_address,c_mobileno,c_email):
        self.customer_name = customer_name
        self.c_address =c_address
        self.c_mobileno=c_mobileno
        self.c_email=c_email

class Items(db.Model):
    __tablename__='items'

    i_id=db.Column(db.Integer,primary_key=True)
    item_name=db.Column(db.String(255),nullable=False)
    item_quantity=db.Column(db.String(255),nullable=False)
    item_price=db.Column(db.String(255),nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    sales = db.relationship("SalesItems", backref=db.backref("items"))

    __table_args__ = (CheckConstraint(item_quantity > 0),{})
    def __init__(self,item_name,item_quantity,item_price):
        self.item_name=item_name
        self.item_name=item_name
        self.item_quantity=item_quantity
        self.item_price=item_price


class SalesItems(db.Model):
    __tablename__ = 'sales_items'
    id = db.Column(db.Integer(), primary_key=True)
    c_id = db.Column(db.Integer(), db.ForeignKey('customers.c_id', ondelete='CASCADE'))
    i_id = db.Column(db.Integer(), db.ForeignKey('items.i_id', ondelete='CASCADE'))
    sale_quantity=db.Column(db.String(255),nullable=False)
    sale_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer = db.relationship('Customer', backref=db.backref("sales_items", cascade="all, delete-orphan"))
    item = db.relationship('Items', backref=db.backref("sales_items", cascade="all, delete-orphan"))

    def __init__(self,c_id,i_id,sale_quantity):
        self.c_id=c_id
        self.i_id=i_id
        self.sale_quantity=sale_quantity

class Bill(db.Model):

    __tablename__='bills'
    id = db.Column(db.Integer,primary_key=True)
    i_id = db.Column(db.Integer(), db.ForeignKey('customers.c_id', ondelete='CASCADE'))
    c_id = db.Column(db.Integer(), db.ForeignKey('items.i_id', ondelete='CASCADE'))
    o_id= db.Column(db.Integer(), db.ForeignKey('sales_items.id', ondelete='CASCADE'))
    bill_amount = db.Column(db.String(255),nullable=False)
    bill_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self,c_id,i_id,o_id,bill_amount):
        self.i_id = i_id
        self.c_id = c_id
        self.o_id=o_id
        self.bill_amount = bill_amount








