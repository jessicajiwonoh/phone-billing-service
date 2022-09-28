import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app import db
from app.models import *

bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.account is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    account_id = session.get("account_id")

    if account_id is not None:
        g.account = db.session.get(Account, account_id)
    else:
        g.account = None

# # Anything that takes user input is a controller
# @bp.route("/populate", methods=("GET", "POST"))
# def populate():
#     op = Operator(account_id=1)
#     #db.session.add(op)
#     db.session.add(Operator(account_id=3))
    
#     cust = Customer(account_id=5)
#     #db.session.add(cust)
#     db.session.add_all([cust, op])
#     db.session.commit()
#     op.customers.append(cust)
#     db.session.commit()


# Anything that takes user input is a controller
@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif db.session.execute(
            db.select(db.select(Account).filter_by(username=username).exists())
        ).scalar():
            error = f"Account {username} is already registered."

        if error is None:
            # the name is available, create the user and go to the login page
            db.session.add(Account(username=username, password=password))
            db.session.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")

@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        select = db.select(Account).filter_by(username=username)
        account = db.session.execute(select).scalar()

        if account is None:
            error = "Incorrect username."
        elif not account.check_password(password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["account_id"] = account.id
            return redirect(url_for("details"))

        flash(error)

    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("details"))
