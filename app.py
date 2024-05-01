# app.py
from flask import Flask
from auth import auth_bp
from main import main_bp
from extensions import db, init_app

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'projetointegradorunivesp2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'

    init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
