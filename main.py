from datetime import date, datetime, timedelta

import bokeh
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from auth import login_manager
from charts import create_figure
from models import Applications, Occurrence, Registration_data, User, db

main_bp = Blueprint("main", __name__)


@login_manager.user_loader
def load_user(user_id):
    # lógica para carregar o usuário com base no ID do usuário
    return User.query.get(int(user_id))


@main_bp.route("/")
def index():

    return render_template("index.html")


#  Rota para perfil do ususario
@main_bp.route("/profile")
@login_required
def profile():
    registration_data = Registration_data.query.filter_by(
        user_id=current_user.id
    ).first()
    applications = Applications.query.filter_by(user_id=current_user.id).first()
    first_name = registration_data.name.split()[0] if registration_data else "Usuário"
    full_name = registration_data.name if registration_data else "Usuário"
    type_diagnosis = registration_data.diagnosis if registration_data else "Diagnóstico"
    blood_type = registration_data.blood_type if registration_data else "Tipo sanguíneo"
    type_of_factor = applications.type_of_factor if applications else "Fator"
    dosage = applications.dosage if applications else "Dosagem"
    application_date = applications.application_date if applications else "Data"
    age, months = (
        calculate_age(registration_data.date_of_birth)
        if registration_data
        else (None, None)
    )
    dash_rows = Applications.get_last_applications(current_user.id)
    plot = create_figure(dash_rows)
    script, div = bokeh.embed.components(plot)
    return render_template(
        "profile.html",
        first_name=first_name,
        full_name=full_name,
        age=age,
        months=months,
        type_diagnosis=type_diagnosis,
        blood_type=blood_type,
        type_of_factor=type_of_factor,
        dosage=dosage,
        application_date=application_date,
        script=script,
        div=div,
    )


def calculate_age(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year

    # Verifica se o mês e o dia de hoje são menores ou iguais ao mês e dia de nascimento
    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        age -= 1
        months = 12 - (date_of_birth.month - today.month)
    else:
        months = today.month - date_of_birth.month

    return age, months


#  Rota para editar o cadastro
@main_bp.route("/edit_user_data", methods=["GET", "POST"])
@login_required
def edit_user_data():
    # Obter o registro de dados do usuário atual, se existir
    registration_data = Registration_data.query.filter_by(
        user_id=current_user.id
    ).first()

    if request.method == "POST":
        name = request.form["name"]
        medical_record_number = request.form["medical_record_number"]
        date_of_birth_str = request.form["date_of_birth"]
        diagnosis = request.form["diagnosis"]
        blood_type = request.form["blood_type"]
        father_name = request.form["father_name"]
        mother_name = request.form["mother_name"]
        address = request.form["address"]
        zip_code = request.form["zip_code"]
        contact_number = request.form["contact_number"]

        # Converter a string de data de nascimento para um objeto de data Python
        date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()

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
                name=name,
                medical_record_number=medical_record_number,
                date_of_birth=date_of_birth,
                diagnosis=diagnosis,
                blood_type=blood_type,
                father_name=father_name,
                mother_name=mother_name,
                address=address,
                zip_code=zip_code,
                contact_number=contact_number,
                user_id=current_user.id,
            )

        try:
            db.session.add(registration_data)
            db.session.commit()
            flash("Cadastro atualizado com sucesso.", "success")
            return redirect(
                url_for("main.profile")
            )  # Redireciona para a página de perfil
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar cadastro. Por favor, tente novamente.", "error")
            current_app.logger.error(f"Erro ao atualizar cadastro: {str(e)}")
            return redirect(
                url_for("main.update_user")
            )  # Redireciona de volta para a página de atualização de usuário

    # Preencher o formulário com os dados existentes do usuário, se existir
    form_data = {}
    if registration_data:
        form_data = {
            "name": registration_data.name,
            "medical_record_number": registration_data.medical_record_number,
            "date_of_birth": registration_data.date_of_birth.strftime("%Y-%m-%d"),
            "diagnosis": registration_data.diagnosis,
            "blood_type": registration_data.blood_type,
            "father_name": registration_data.father_name,
            "mother_name": registration_data.mother_name,
            "address": registration_data.address,
            "zip_code": registration_data.zip_code,
            "contact_number": registration_data.contact_number,
        }

    return render_template("edit_user_data.html", form_data=form_data)


#  Rota para a pagina do fullcalendar
@main_bp.route("/calendar")
@login_required
def calendar():
    return render_template("calendar.html")


#  Rota para retornar os eventos em formato JSON
@main_bp.route("/api/eventos")
@login_required
def api_eventos():
    eventos = Applications.query.filter_by(user_id=current_user.id).all()

    eventos_formatados = []
    for evento in eventos:
        data_inicio = evento.application_date
        application_time = evento.application_time

        # Adicionados logs para depuração
        current_app.logger.info(
            f"Processando evento ID: {evento.id}, Data: {data_inicio}, Hora: {application_time}"
        )

        if not application_time:
            current_app.logger.warning(
                f"Evento {evento.id} sem horário de aplicação definido."
            )
            continue  # Ignorar este evento

        data_hora_evento = f"{data_inicio}T{application_time}"
        current_app.logger.info(f"Concatenando data e hora: {data_hora_evento}")

        try:
            data_hora_formatada = datetime.strptime(data_hora_evento, "%Y-%m-%dT%H:%M")
            eventos_formatados.append(
                {
                    "id": evento.id,
                    "title": evento.purpose,
                    "start": data_hora_formatada.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": (data_hora_formatada + timedelta(hours=1)).strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    ),
                }
            )
        except ValueError as e:
            current_app.logger.error(
                f"Erro ao formatar data/hora do evento {evento.id}: {e}"
            )

    return jsonify(eventos_formatados)


#  Rota para retornar detalhes do evento
@main_bp.route("/get_event_details/<int:event_id>")
@login_required
def get_event_details(event_id):
    evento = Applications.query.get(event_id)
    if evento:

        # Converte o valor booleano para 'Sim' ou 'Não'
        absence_display = "Sim" if evento.absence else "Não"

        event_details = {
            "purpose": evento.purpose,
            "dosage": evento.dosage,
            "type_of_factor": evento.type_of_factor,
            "absence": absence_display,  # Usa o valor convertido
            "application_date": evento.application_date,
            "application_time": evento.application_time,
        }
    else:
        event_details = {"error": "Evento não encontrado"}
    return jsonify(event_details)


#  Rota para deletar evento
@main_bp.route("/delete_event/<int:event_id>", methods=["DELETE"])
@login_required
def delete_event(event_id):
    evento = Applications.query.get_or_404(event_id)
    if evento.user_id != current_user.id:
        # Se o evento não pertencer ao usuário atual, não permitir a exclusão
        return jsonify({"message": "Permissão negada"}), 403
    db.session.delete(evento)
    db.session.commit()
    return jsonify({"message": "Evento excluído com sucesso"}), 200


#  Rota para editar evento
@main_bp.route("/edit_event/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    evento = Applications.query.get_or_404(event_id)
    if evento.user_id != current_user.id:
        # Se o evento não pertencer ao usuário atual, não permitir a edição
        return jsonify({"message": "Permissão negada"}), 403

    if request.method == "POST":
        # Atualizar os dados do evento com as informações recebidas do formulário
        evento.type_of_factor = request.form["type_of_factor"]
        evento.dosage = request.form["dosage"]
        evento.purpose = request.form["purpose"]
        evento.absence = request.form["absence"]

        evento.application_time = request.form["application_time"]
        db.session.commit()
        return jsonify({"message": "Evento atualizado com sucesso"}), 200
    else:
        event_data = {
            "type_of_factor": evento.type_of_factor,
            "dosage": evento.dosage,
            "purpose": evento.purpose,
            "absence": evento.absence,
            "application_time": evento.application_time,
        }
        return jsonify(event_data)


@main_bp.route("/add_application", methods=["POST"])
@login_required
def add_application():
    data = request.form
    new_application = Applications(
        type_of_factor=data.get("type_of_factor"),
        dosage=data.get("dosage"),
        purpose=data.get("eventPurpose"),
        absence=data.get("absence") == "true",
        application_date=data.get("application_date"),
        application_time=data.get("application_time"),
        user_id=current_user.id,
    )
    db.session.add(new_application)
    db.session.commit()
    flash("Aplicação adicionada com sucesso!", "success")
    return render_template("calendar.html")

    # Rota para adicionar detalhes de evento Sob demanda


@main_bp.route("/add_occurrence", methods=["POST"])
@login_required
def add_occurrence():
    data = request.form
    new_occurrence = Occurrence(
        bleeding_type=data.get("bleeding_type"),
        site_of_injury=data.get("site_of_injury"),
        side=data.get("side"),
        occurrence_date=data.get("occurrence_date"),
        occurrence_time=data.get("occurrence_time"),
        user_id=current_user.id,
    )
    db.session.add(new_occurrence)
    db.session.commit()
    flash("Detalhes do adicionados com sucesso!", "success")
    return render_template("calendar.html")