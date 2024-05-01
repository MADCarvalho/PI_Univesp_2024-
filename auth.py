from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from models import User
from extensions import db, login_manager

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Você precisa estar logado para acessar esta página.', 'error')
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password and user.is_active:
            login_user(user)
            return redirect(url_for('main.profile'))
        else:
            flash('E-mail ou senha inválidos.', 'error')
            return redirect(url_for('auth.login'))  # Redireciona de volta para a página de login com uma mensagem de erro
    # Adiciona um retorno para o método GET
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'success')
    return redirect(url_for('main.index'))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verifica se o usuário já existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Este e-mail já existe. Por favor, use um e-mail diferente.', 'error')
            return redirect(url_for('auth.signup'))

        # Não fazer hash da senha, armazenar em texto plano
        new_user = User(email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        # Obter o id do usuário recém-criado
        new_user_id = new_user.id

        flash('Usuario criado com sucesso. Continue com seu cadastro.', 'success')
        return redirect(url_for('main.update_user'))  # Redireciona para a página de login

    return render_template('signup.html')

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    if request.method == 'POST':
        email = request.form['email']

        # Lógica para redefinição de senha
        # ...

        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')
