from sqlalchemy import event

from app import db
from app import models

# Initialize test.db

@event.listens_for(models.Account.__table__, 'after_create')
def create_accounts(*args, **kwargs):
    db.session.add(models.Account(username='abc123', password='qwerty1234'))
    db.session.add(models.Account(username='abc456', password='qwerty1234'))
    db.session.add(models.Account(username='abc789', password='qwerty1234'))
    db.session.add(models.Account(username='abc012', password='qwerty1234'))
    db.session.add(models.Account(username='abc345', password='qwerty1234'))
    db.session.add(models.Account(username='abc689', password='qwerty1234'))
    db.session.commit()

@event.listens_for(models.Customer.__table__, 'after_create')
def create_customers(*args, **kwargs):
    db.session.add(models.Customer(account_id=2))
    db.session.commit()

@event.listens_for(models.Operator.__table__, 'after_create')
def create_operators(*args, **kwargs):
    db.session.add(models.Operator(account_id=1))
    db.session.add(models.Operator(account_id=3))

@event.listens_for(models.po_to_cust, 'after_create')
def create_po_to_cust(*args, **kwargs):
    cust_first = models.Customer(account_id=4)
    cust_second = models.Customer(account_id=6)
    op = models.Operator(account_id=5)
    db.session.add_all([cust_first, cust_second])
    op.customers.extend([cust_first, cust_second])
    db.session.commit()
