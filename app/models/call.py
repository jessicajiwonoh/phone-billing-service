from datetime import date, datetime
from sqlalchemy.inspection import inspect

from app import db
from app.models import Serializer

class Call(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    start_timestamp = db.Column(db.DateTime, nullable=False)
    end_timestamp = db.Column(db.DateTime, nullable=False)
    
    def serialize(self):
        serialized = {}
        for c in inspect(self).attrs.keys():
            value = getattr(self, c)
            if(isinstance(value, (datetime, date))):
                value = value.isoformat()
            serialized[c] = value
            
        return serialized

def __repr__(self):
   return f"Call({self.id}, {self.customer_id}, {self.start_timestamp}, {self.end_timestamp})"
