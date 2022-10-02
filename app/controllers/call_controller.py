import json
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Response
)

from app import db
from app.models import Call

call_bp = Blueprint("call", __name__, url_prefix="/call")

@call_bp.before_app_request
def load_calls():
    call_id = session.get("call_id")
    
    if call_id is not None:
        g.call = db.session.get(Call, call_id)
    else:
        g.call: None
        
def get_all_calls():
    select = db.select(Call).order_by(Call.start_timestamp.desc())
    calls = db.session.execute(select).scalars()
    return json.dumps(Call.serialize_list(calls))

@call_bp.route("/")
def index():
    return Response(json.dumps(get_all_calls()), mimetype='application/json')

# @call_bp.route("/all")
# def calls_api():
#     calls = get_all_calls()
#     print(calls)
#     return render_template("auth/register.html")
