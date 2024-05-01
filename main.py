from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from models import User, Registration_data, db
from flask import flash
from auth import login_manager
from datetime import datetime


main_bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    #lógica para carregar o usuário com base no ID do usuário
    return User.query.get(int(user_id))


@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/profile')
@login_required
def profile():
    registration_data = Registration_data.query.filter_by(user_id=current_user.id).first()
    first_name = registration_data.name.split()[0] if registration_data else 'Usuário'
    return render_template('profile.html', first_name=first_name)

@main_bp.route('/update_user', methods=['GET', 'POST'])
@login_required
def update_user():
    if request.method == 'POST':
        name = request.form['name']
        medical_record_number = request.form['medical_record_number']
        date_of_birth_str = request.form['date_of_birth']
        diagnosis = request.form['diagnosis']
        blood_type = request.form['blood_type']
        father_name = request.form['father_name']
        mother_name = request.form['mother_name']
        address = request.form['address']
        zip_code = request.form['zip_code']
        contact_number = request.form['contact_number']
        
        # Converter a string de data de nascimento para um objeto de data Python
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()

        new_registration_data = Registration_data(
            name=name, medical_record_number=medical_record_number,
            date_of_birth=date_of_birth, diagnosis=diagnosis, blood_type=blood_type,
            father_name=father_name, mother_name=mother_name, address=address,
            zip_code=zip_code, contact_number=contact_number, user_id=current_user.id
        )

        try:
            db.session.add(new_registration_data)
            db.session.commit()
            flash('Cadastro atualizado com sucesso.', 'success')
            return redirect(url_for('main.profile'))  # Redireciona para a página de perfil
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar cadastro. Por favor, tente novamente.', 'error')
            current_app.logger.error(f'Erro ao atualizar cadastro: {str(e)}')
            return redirect(url_for('main.update_user'))  # Redireciona de volta para a página de atualização de usuário

    return render_template('update_user.html')

@main_bp.route('/calendar')
def calendar():
    return render_template('calendar.html')
