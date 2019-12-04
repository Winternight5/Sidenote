from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_heroku import Heroku
from flask_socketio import SocketIO

"""
Place where a lot of stuff gets initialized.
"""
socketio = SocketIO()
heroku = Heroku()
db = SQLAlchemy()
login = LoginManager()

def create_app(debug=False, test_config=None):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config.from_object(Config)

    if test_config is None:
    # load the instance config, if it exists, when not testing
        app.config.from_object('config.Config')
    else:
        app.config.from_mapping(test_config)
        
    db.init_app(app)
    socketio.init_app(app)
    login.init_app(app)
    login.login_view = 'login'
    
    with app.app_context():
        # Include our routes
        from . import routes, events, models
        db.create_all()
        return app

