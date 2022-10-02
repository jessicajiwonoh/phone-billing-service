import os

import click
from flask import Flask, jsonify, render_template
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
import socket

__version__ = (1, 0, 0, "dev")

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)

    # some deploy systems set the database url in the environ
    db_url = os.environ.get("DATABASE_URL")

    if db_url is None:
        # default to a sqlite database in the instance folder
        db_url = "sqlite:///test.db"

    app.config.from_mapping(
        # default secret that should be overridden in environ or config
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=db_url
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)
    
    def fetchDetails():
        hostname = socket.gethostname()
        host_ip = socket.gethostbyname(hostname)
        return str(hostname), str(host_ip)
    
    @app.route("/health")
    def health():
        return jsonify(
            status="UP"
        )

    @app.route("/")
    def details():
        hostname, host_ip = fetchDetails()
        return render_template('detail.html', HOSTNAME=hostname, IP=host_ip)

    # initialize Flask-SQLAlchemy and the init-db command
    db.init_app(app)
    app.cli.add_command(init_db_command)

    # apply the blueprints to the app
    from app import controllers
    app.register_blueprint(controllers.auth_bp)
    app.register_blueprint(controllers.call_bp)
    return app

def init_db():
    db.drop_all()
    db.create_all()

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")
