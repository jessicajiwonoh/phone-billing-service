import json
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Response
)

from app import db
from app.models import Invoice

invoice_bp = Blueprint("invoice", __name__, url_prefix="/invoice")

@invoice_bp.before_app_request
def load_invoices():
    invoice_id = session.get("invoice_id")
    
    if invoice_id is not None:
        g.invoice = db.session.get(Invoice, invoice_id)
    else:
        g.invoice = None

def get_all_invoices():
    select = db.select(Invoice).order_by(Invoice.date_billed.desc())
    invoices = db.session.execute(select).scalars()
    return json.dumps(Invoice.serialize_list(invoices))

@invoice_bp.route("/")
def index():
    return Response(json.dumps(get_all_invoices()), mimetype='application/json')
