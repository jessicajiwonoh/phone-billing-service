import json
from datetime import datetime, timedelta
from flask import(
    Blueprint, g, redirect, session, url_for, Response
)

from app import db
from app.models import Call

call_bp = Blueprint('call', __name__, url_prefix='/call')

@call_bp.before_app_request
def load_calls():
    call_id = session.get('call_id')
    
    if call_id is not None:
        g.call = db.session.get(Call, call_id)
    else:
        g.call: None
        
def get_all_calls():
    select = db.select(Call).order_by(Call.start_timestamp.desc())
    calls = db.session.execute(select).scalars()
    return Response(json.dumps(Call.serialize_list(calls)), mimetype='application/json')

# Index returns all calls
@call_bp.route('/')
def index():
    return get_all_calls()

# Get the call history by customer id
@call_bp.route('/customer=<int:customer_id>')
def get_call_history_by_customer(customer_id):
    select_customer = db.select(Call).filter_by(customer_id=customer_id)
    calls_by_customer = db.session.execute(select_customer).scalars()

    return Response(json.dumps(Call.serialize_list(calls_by_customer)), mimetype='application/json')

# Post incoming call by customer id
# Record when the call is ended(datetime.now())
# Redirect after adding a new call to show the call history by customer
@call_bp.route('/customer=<int:customer_id>/add_call_min=<int:min>', methods=['GET', 'POST'])
def add_call_by_customer(customer_id, min):
    end_timestamp = datetime.now()
    start_timestamp = end_timestamp - timedelta(minutes=min)
    new_call = Call(customer_id=customer_id, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
    db.session.add(new_call)
    db.session.commit()
    
    return redirect(url_for('call.get_call_history_by_customer', customer_id=customer_id))
