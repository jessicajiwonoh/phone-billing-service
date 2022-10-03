import json
from datetime import datetime
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from flask import(
    Blueprint, g, redirect, session, url_for, Response, request
)

from app import db
from app.models import Invoice, Call

invoice_bp = Blueprint('invoice', __name__, url_prefix='/invoice')
FLAT_RATE = 0.02

@invoice_bp.before_app_request
def load_invoices():
    invoice_id = session.get('invoice_id')
    
    if invoice_id is not None:
        g.invoice = db.session.get(Invoice, invoice_id)
    else:
        g.invoice = None

def get_all_invoices():
    select = db.select(Invoice).order_by(Invoice.date_billed.desc())
    invoices = db.session.execute(select).scalars()
    return Response(json.dumps(Invoice.serialize_list(invoices)), mimetype='application/json')

# Calculate rate per call filtered by cusomter id
def calculate_call_rate(customer_id):
    call_history = defaultdict(list)

    timestamps = db.session.query(Call.start_timestamp, Call.end_timestamp).filter_by(customer_id=customer_id).all()
    for timestamp in timestamps:
        daily_call = []
        time_duration_rate = {}
        
        start_time = timestamp.start_timestamp
        end_time = timestamp.end_timestamp
        call_time = (end_time - start_time).total_seconds() / 60.0
        
        rate_per_call = call_time * FLAT_RATE
        
        dt = datetime.strptime(start_time.isoformat(), '%Y-%m-%dT%H:%M:%S.%f')
        formatted_time = dt.strftime('%m/%d/%Y, %H:%M')
        
        time_duration_rate['datetime'] = formatted_time
        time_duration_rate['duration'] = call_time
        time_duration_rate['rate'] = rate_per_call
        
        daily_call.append(time_duration_rate)
        call_history[dt.month].append(daily_call)

    return call_history

# Calculate invoice based on fixed call rate and usage
def calculate_invoice_per_period(customer_id, month):
    call_rates =  calculate_call_rate(customer_id)
    monthly_call = defaultdict(int)
    
    if month is not None:
        month = int(month)
        monthly = call_rates[month]
 
        for idx in monthly:
            print(monthly)
            rate = idx[0]['rate']
            monthly_call[month] += rate
    else:
        for period in call_rates:
            monthly = call_rates[period]
            for idx in monthly:
                rate = idx[0]['rate']
                monthly_call[period] += rate
        
    return monthly_call

# Index returns all invoices
@invoice_bp.route('/')
def index():
    return get_all_invoices()

# Get the invoice history by customer id
@invoice_bp.route('/customer')
def get_invoice_per_customer():
    customer_id = request.form.get('customer')
    return Response(json.dumps(calculate_call_rate(customer_id)), mimetype='application/json')

# Get consolidated invoice by month for specific customer id
@invoice_bp.route('/consolidated')
def get_consolidated_invoice():
    customer_id = request.form.get('customer')
    return Response(json.dumps(calculate_invoice_per_period(customer_id, None)), mimetype='application/json')

# Get specific month invoice by customer id
@invoice_bp.route('/month')
def get_specific_month_invoice():
    customer_id = request.form.get('customer')
    month_int = request.form.get('month')
    return Response(json.dumps(calculate_invoice_per_period(customer_id, month_int)), mimetype='application/json')

# Customers receive invoice every first day of the month
@invoice_bp.route('/generate_invoice', methods=['POST'])
def generate_invoice_by_customer():
    customer_id = request.form.get('customer')
    
    today = datetime.now()
    a_month_ago = today - relativedelta(months=1)

    if today.day == 1:
        previous_month_invoice = calculate_invoice_per_period(customer_id, a_month_ago.month)
        print('Generate invoice for the first day of the month')
        new_invoice = Invoice(customer_id=customer_id, amount_billed=previous_month_invoice[a_month_ago.month], date_billed=today, date_paid=None)
        db.session.add(new_invoice)
        db.session.commit()
        return Response(json.dumps(previous_month_invoice), mimetype='application/json')
    else:
        print("Today is not the first day of the month. Redirecting to current month's usage")
        return redirect(url_for('invoice.get_specific_month_invoice', customer_id=customer_id, month=today.month))
