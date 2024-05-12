# models.py
from flask_login import UserMixin, current_user
from extensions import db

# Definição do modelo de usuário
class User(UserMixin, db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Integer, default=1)  # 1 para verdadeiro, 0 para falso
    registration_data = db.relationship('Registration_data', uselist=False, backref='user', lazy=True)
    applications = db.relationship('Applications', uselist=False, backref='user', lazy=True)
    occurrences = db.relationship('Occurrence', uselist=False, backref='user', lazy=True)
    
    def __init__(self, email, password):
        self.email = email
        self.password = password  # Salva a senha em texto plano ao criar um usuário

    def check_password(self, password):
        return self.password == password  # Verifica se a senha fornecida corresponde à senha armazenada

    def is_active(self):
        return self.active == 1  # Retorna True se 'active' for 1, caso contrário False
    

class Registration_data(UserMixin, db.Model):
    __tablename__= 'Registration_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    medical_record_number = db.Column(db.String(20), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    diagnosis = db.Column(db.String(50), nullable=False)
    blood_type = db.Column(db.String(30), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    zip_code = db.Column(db.String(12), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, name, medical_record_number, date_of_birth, diagnosis, blood_type, father_name, mother_name, address, zip_code, contact_number, user_id):
        self.name = name
        self.medical_record_number = medical_record_number
        self.date_of_birth = date_of_birth
        self.diagnosis = diagnosis
        self.blood_type = blood_type
        self.father_name = father_name
        self.mother_name = mother_name
        self.address = address
        self.zip_code = zip_code
        self.contact_number = contact_number
        self.user_id = user_id
        
        
class Applications(UserMixin, db.Model):
    __tablename__= 'Applications'
    id = db.Column(db.Integer, primary_key=True)
    type_of_factor = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(150), nullable=False)
    absence = db.Column(db.String(10), nullable=False)
    application_date = db.Column(db.String(10), nullable=False)
    application_time = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, type_of_factor, dosage, purpose, absence, application_date, application_time, user_id):
        self.type_of_factor = type_of_factor
        self.dosage = dosage
        self.purpose = purpose
        self.absence = absence
        self.application_date = application_date
        self.application_time = application_time
        self.user_id = user_id
          
    
class Occurrence(UserMixin, db.Model):
    __tablename__= 'Occurrence'
    id = db.Column(db.Integer, primary_key=True)
    bleeding_type = db.Column(db.String(100), nullable=False)
    site_of_injury = db.Column(db.String(100), nullable=False)
    side = db.Column(db.String(100), nullable=False)
    occurrence_date = db.Column(db.String(10), nullable=False)
    occurrence_time = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, bleeding_type, site_of_injury, side, occurrence_date, occurrence_time, user_id):
        self.bleeding_type = bleeding_type
        self.site_of_injury = site_of_injury
        self.side = side
        self.occurrence_date = occurrence_date
        self.occurrence_time = occurrence_time
        self.user_id = user_id
