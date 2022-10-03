from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    customers = db.relationship('Customer', lazy='select',
        backref=db.backref('account', lazy='joined'))
    operator = db.relationship('Operator', lazy='select',
        backref=db.backref('account', lazy='joined'))

    def set_password(self, value):
        # Store the password as a hash for security
        self.password_hash = generate_password_hash(value)

    # allow password = '...' to set a password
    password = property(fset=set_password)

    def check_password(self, value):
        return check_password_hash(self.password_hash, value)

def __repr__(self):
   return f'Account({self.id}, {self.username})'
