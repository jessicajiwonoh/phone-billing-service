from urllib import request, response
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app import db
from app.models.invoice import Invoice

customer_to_po = db.Table('customer_to_po',
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'), primary_key=True),
    db.Column('po_id', db.Integer, db.ForeignKey('phone_operator.id'), primary_key=True)
)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    customers = db.relationship('Customer', lazy='select',
        backref=db.backref('account', lazy='joined'))
    phone_op = db.relationship('PhoneOperator', lazy='select',
        backref=db.backref('account', lazy='joined'))

    def set_password(self, value):
        # Store the password as a hash for security
        self.password_hash = generate_password_hash(value)

    # allow password = "..." to set a password
    password = property(fset=set_password)

    def check_password(self, value):
        return check_password_hash(self.password_hash, value)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    invoices = db.relationship('Invoice', lazy='select',
        backref=db.backref('customer', lazy='joined'))

class PhoneOperator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

def __repr__(self):
   return f"Account({self.id}, {self.username})"
