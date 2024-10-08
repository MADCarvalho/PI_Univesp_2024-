from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, session, url_for

from auth import auth_bp
from extensions import db, init_app
from main import main_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "projetointegradorunivesp2024"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://default:e5S6IVgfAFuY@ep-muddy-morning-a64mj7do-pooler.us-west-2.aws.neon.tech:5432/verceldb?sslmode=require"
)

init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
oauth = OAuth(app)

google = oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id="28099972731-9v8k8tmqo8plbfba77defrkoh6av5r74.apps.googleusercontent.com",
    client_secret="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",
    client_kwargs={"scope": "openid email profile"},
)


# Routes for google login
@app.route("/google-login")
def google_login():
    redirect_uri = url_for("authorize", _external=True)
    google = oauth.create_client("google")
    return google.authorize_redirect(redirect_uri)


@app.route("/authorize")
def authorize():
    from flask_login import login_user

    from models import User

    token = oauth.google.authorize_access_token()
    user = token["userinfo"]
    email = user["email"]
    password = user["sub"]

    # Verifica se o usuário já existe
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        login_user(existing_user)
        return redirect(url_for("main.profile"))

    # Não fazer hash da senha, armazenar em texto plano
    new_user = User(email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    # Autentica o usuário e inicia uma sessão
    login_user(new_user)

    # Define um indicador na sessão que o cadastro precisa ser concluído
    session["complete_registration"] = True

    return redirect(url_for("auth.complete_registration"))


if __name__ == "__main__":
    app.run(debug=True)
