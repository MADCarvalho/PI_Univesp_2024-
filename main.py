from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from models import User, Registration_data, db, Applications
from flask import flash
from auth import login_manager
from datetime import datetime,date


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
    full_name = registration_data.name if registration_data else 'Usuário'
    type_diagnosis = registration_data.diagnosis if registration_data else 'Diagnóstico'
    age, months = calculate_age(registration_data.date_of_birth) if registration_data else (None, None)
    return render_template('profile.html', first_name=first_name, full_name=full_name, age=age, months=months,
                           type_diagnosis=type_diagnosis)

def calculate_age(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    months = today.month - date_of_birth.month
    if months < 0 or (months == 0 and today.day < date_of_birth.day):
        age -= 1
        months += 12
    return age, months


@main_bp.route('/update_user', methods=['GET', 'POST'])
@login_required
def update_user():
    # Obter o registro de dados do usuário atual, se existir
    registration_data = Registration_data.query.filter_by(user_id=current_user.id).first()

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

        if registration_data:  # Se já existe registro de dados para o usuário, atualiza
            registration_data.name = name
            registration_data.medical_record_number = medical_record_number
            registration_data.date_of_birth = date_of_birth
            registration_data.diagnosis = diagnosis
            registration_data.blood_type = blood_type
            registration_data.father_name = father_name
            registration_data.mother_name = mother_name
            registration_data.address = address
            registration_data.zip_code = zip_code
            registration_data.contact_number = contact_number
        else:  # Se não existe registro de dados, cria um novo
            registration_data = Registration_data(
                name=name, medical_record_number=medical_record_number,
                date_of_birth=date_of_birth, diagnosis=diagnosis, blood_type=blood_type,
                father_name=father_name, mother_name=mother_name, address=address,
                zip_code=zip_code, contact_number=contact_number, user_id=current_user.id
            )

        try:
            db.session.add(registration_data)
            db.session.commit()
            flash('Cadastro atualizado com sucesso.', 'success')
            return redirect(url_for('main.profile'))  # Redireciona para a página de perfil
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar cadastro. Por favor, tente novamente.', 'error')
            current_app.logger.error(f'Erro ao atualizar cadastro: {str(e)}')
            return redirect(url_for('main.update_user'))  # Redireciona de volta para a página de atualização de usuário

    # Preencher o formulário com os dados existentes do usuário, se existir
    form_data = {}
    if registration_data:
        form_data = {
            'name': registration_data.name,
            'medical_record_number': registration_data.medical_record_number,
            'date_of_birth': registration_data.date_of_birth.strftime('%Y-%m-%d'),
            'diagnosis': registration_data.diagnosis,
            'blood_type': registration_data.blood_type,
            'father_name': registration_data.father_name,
            'mother_name': registration_data.mother_name,
            'address': registration_data.address,
            'zip_code': registration_data.zip_code,
            'contact_number': registration_data.contact_number
        }

    return render_template('update_user.html', form_data=form_data)

@main_bp.route('/calendar')
def calendar():
    return render_template('calendar.html')


@main_bp.route('/add_application', methods=['POST'])
@login_required
def add_application():
    data = request.form
    new_application = Applications(
        type_of_factor=data.get('type_of_factor'),
        dosage=data.get('dosage'),
        purpose=data.get('purpose'),
        absence=data.get('absence') == 'true',
        application_date=data.get('application_date'),
        application_time=data.get('application_time')
    )
    db.session.add(new_application)
    db.session.commit()
    flash('Aplicação adicionada com sucesso!', 'success')
    return render_template('calendar.html')    
    