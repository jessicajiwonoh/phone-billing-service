from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    invoices = db.relationship('Invoice', lazy='select',
        backref=db.backref('customer', lazy='joined'))

def __repr__(self):
   return f"Customer({self.id}, {self.account_id})"