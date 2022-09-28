from app import db

class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    start_timestamp = db.Column(db.DateTime, nullable=False)
    end_timestamp = db.Column(db.DateTime, nullable=False)

def __repr__(self):
   return f"Call({self.id}, {self.customer_id}, {self.start_timestamp}, {self.end_timestamp})"
