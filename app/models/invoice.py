from app import db

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

def __repr__(self):
   return f"Invoice({self.id}, {self.customer_id})"
