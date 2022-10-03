from datetime import date, datetime
from sqlalchemy.inspection import inspect

from app import db
from app.models import Serializer

class Invoice(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    amount_billed = db.Column(db.Integer, nullable=False)
    date_billed = db.Column(db.DateTime, nullable=False)
    date_paid = db.Column(db.DateTime)
    
    def serialize(self):
        serialized = {}
        for c in inspect(self).attrs.keys():
            value = getattr(self, c)
            if(isinstance(value, (datetime, date))):
                value = value.isoformat()
            serialized[c] = value
        
        return serialized

def __repr__(self):
   return f'Invoice({self.id}, {self.customer_id}, {self.amount_billed}, {self.date_billed}, {self.date_paid})'
