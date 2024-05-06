from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy.dialects.postgresql import psycopg2

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def init_app(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
