from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
oauth = OAuth()

login_manager = LoginManager()
login_manager.login_view = "login"


def create_app(dev_settings):
    app = Flask(__name__)
    app.config.from_object(dev_settings)

    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)

    with app.app_context():
        from . import routes

        return app
