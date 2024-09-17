from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Registration_data
from extensions import db, login_manager
from datetime import datetime

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
 
        # Autentica o usuário e inicia uma sessão
        login_user(new_user)
        
        # Define um indicador na sessão que o cadastro precisa ser concluído
        session['complete_registration'] = True
        
        flash('Usuário criado com sucesso. Continue com seu cadastro.', 'success')
        return redirect(url_for('auth.complete_registration'))

    return render_template('signup.html')
        

#  Rota para completar o cadastro
@auth_bp.route('/complete_registration', methods=['GET', 'POST'])
@login_required
def complete_registration(): 
    
   # Verifica se o usuário precisa completar o cadastro
    if not session.get('complete_registration'):
        return redirect(url_for('main.home'))  # Ou a rota que você deseja após o cadastro completo

    # Se houver sessão, permite que o usuário complete o cadastro
    
    if request.method == 'POST':
        # Cria um novo objeto Registration_data para armazenar os dados do formulário
        registration_data = Registration_data(
            name=request.form['name'],
            medical_record_number=request.form['medical_record_number'],
            date_of_birth=datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date(),
            diagnosis=request.form['diagnosis'],
            blood_type=request.form['blood_type'],
            father_name=request.form['father_name'],
            mother_name=request.form['mother_name'],
            address=request.form['address'],
            zip_code=request.form['zip_code'],
            contact_number=request.form['contact_number'],
            user_id=current_user.id  # Associa os dados ao usuário atual
        )

        db.session.add(registration_data)
        db.session.commit()

        # Remove o indicador da sessão após o cadastro ser concluído
        session.pop('complete_registration', None)

        flash('Cadastro finalizado com sucesso.', 'success')
        return redirect(url_for('main.profile'))  # Ou a rota que você deseja após o cadastro completo

    return render_template('complete_registration.html')

# Certificar-se de proteger as outras rotas para que o usuário não possa acessá-las
# sem ter concluído o cadastro
@auth_bp.before_request
def before_request():
    if current_user.is_authenticated and session.get('complete_registration'):
        if request.endpoint not in ['auth.complete_registration', 'auth.logout']:
            return redirect(url_for('auth.complete_registration'))



@auth_bp.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    if request.method == 'POST':
        email = request.form['email']

        # Lógica para redefinição de senha
        # ...

        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')
