import os
from flask import Flask, jsonify, render_template
import socket

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    if test_config is None:
        # load the instance config when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    def fetchDetails():
        hostname = socket.gethostname()
        host_ip = socket.gethostbyname(hostname)
        return str(hostname), str(host_ip)
    
    @app.route("/health")
    def health():
        return jsonify(
            status="UP"
        )
        
    @app.route("/details")
    def details():
        hostname, host_ip = fetchDetails()
        return render_template('index.html', HOSTNAME=hostname, IP=host_ip)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import db
    db.init_app(app)
    
    return app
