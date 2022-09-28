from app import db

customer_to_po = db.Table('customer_to_po',
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'), primary_key=True),
    db.Column('po_id', db.Integer, db.ForeignKey('phone_operator.id'), primary_key=True)
)

def __repr__(self):
   return f"Customer to Phone Operator({self.customer_id}, {self.po_id})"
