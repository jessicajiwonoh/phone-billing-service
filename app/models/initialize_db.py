from sqlalchemy import event
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from app import db
from app import models

# Initialize test.db

now = datetime.now()
ten_min_ago = now - timedelta(minutes=10)
fiften_min_ago = now - timedelta(minutes=15)
thirty_min_ago = now - timedelta(minutes=30)
a_month_ago = now - relativedelta(months=1)
a_month_fiften_min_ago = now - relativedelta(months=1, minutes=15)
two_months_ago = now - relativedelta(months=2)
two_months_thirty_min_ago = now - relativedelta(months=2, minutes=30)

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

@event.listens_for(models.Call.__table__, 'after_create')
def create_calls(*args, **kwargs):
    db.session.add(models.Call(customer_id=1, start_timestamp=fiften_min_ago, end_timestamp=now))
    db.session.add(models.Call(customer_id=2, start_timestamp=ten_min_ago, end_timestamp=now))
    db.session.add(models.Call(customer_id=3, start_timestamp=thirty_min_ago, end_timestamp=now))
    db.session.add(models.Call(customer_id=1, start_timestamp=thirty_min_ago, end_timestamp=now))
    db.session.add(models.Call(customer_id=1, start_timestamp=a_month_fiften_min_ago, end_timestamp=a_month_ago))
    db.session.add(models.Call(customer_id=1, start_timestamp=two_months_thirty_min_ago, end_timestamp=two_months_ago))
    db.session.commit()
    
@event.listens_for(models.Invoice.__table__, 'after_create')
def create_invoices(*args, **kwargs):
    db.session.add(models.Invoice(customer_id=1, amount_billed=100, date_billed=now))
    db.session.commit()
