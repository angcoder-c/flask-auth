import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DefaultConfig

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
appdir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(DefaultConfig)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .public import bp_public
    app.register_blueprint(bp_public)
    from .auth import bp_auth
    app.register_blueprint(bp_auth)

    return app