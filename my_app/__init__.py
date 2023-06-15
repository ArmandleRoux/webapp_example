from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'

    db_name = 'app_db.db'
    # Get path to database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, db_name)

    app.config['SECRET_KEY'] = "thisisareallybadsecretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

    Session(app)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main_app.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(username):
        return User.query.get(username)
    
    from .main_app import main_app as main_blueprint
    app.register_blueprint(main_blueprint)

    return app