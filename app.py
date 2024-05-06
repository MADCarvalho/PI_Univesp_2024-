from flask import Flask
from auth import auth_bp
from main import main_bp
from extensions import db, init_app

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'projetointegradorunivesp2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://default:e5S6IVgfAFuY@ep-muddy-morning-a64mj7do-pooler.us-west-2.aws.neon.tech:5432/verceldb?sslmode=require"

    init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
