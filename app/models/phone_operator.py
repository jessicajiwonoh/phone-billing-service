from app import db

class PhoneOperator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

def __repr__(self):
   return f"Phone Operator({self.id}, {self.account_id})"
