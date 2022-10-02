from app import db

po_to_cust = db.Table('po_to_cust',
    db.Column('po_id', db.Integer, db.ForeignKey('operator.id'), primary_key=True),
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'), primary_key=True)
)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

class Operator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    customers = db.relationship('Customer', secondary=po_to_cust,
        backref=db.backref('operators'))

def __repr__(self):
   return f"Phone Operator({self.po_id}, Customner{self.customer_id})"
