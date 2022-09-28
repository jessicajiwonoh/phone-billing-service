from app import db

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    amount_billed = db.Column(db.Integer, nullable=False)
    date_billed = db.Column(db.DateTime, nullable=False)
    date_paid = db.Column(db.DateTime)

def __repr__(self):
   return f"Invoice({self.id}, {self.customer_id}, {self.amount_billed}, {self.date_billed}, {self.date_paid})"
