import json
from datetime import datetime, timedelta
from flask import(
    Blueprint, g, session, Response, request
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
@call_bp.route('/customer')
def get_call_history_by_customer():
    customer_id = request.form.get('customer')
    
    select_customer = db.select(Call).filter_by(customer_id=customer_id)
    calls_by_customer = db.session.execute(select_customer).scalars()

    return Response(json.dumps(Call.serialize_list(calls_by_customer)), mimetype='application/json')

# Post incoming call with customer id and minutes form data
# Record when the call is ended(datetime.now())
# Return get call history response after adding a new call to show the call history by customer
@call_bp.route('/add_call', methods=['POST'])
def add_call_by_customer():
    customer_id = request.form.get('customer')
    minutes = request.form.get('minutes')
    end_timestamp = datetime.now()
    start_timestamp = end_timestamp - timedelta(minutes=int(minutes))
    new_call = Call(customer_id=customer_id, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
    db.session.add(new_call)
    db.session.commit()
    return get_call_history_by_customer()
