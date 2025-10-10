from .database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(), unique = True, nullable = False)
    password_hash = db.Column(db.String(), nullable = False)
    role = db.Column(db.String(), nullable = False, default = "user")
    doctor = db.relationship('Doctor', backref = "user", uselist = False, cascade = 'all')
    patient = db.relationship('Patient', backref = "user", uselist = False, cascade = 'all')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable =False, unique = True)
    name = db.Column(db.String, nullable = False)
    specialization = db.Column(db.String(), nullable = False)
    availability = db.Column(db.Text, nullable= True)
    
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable = False)
    appointments = db.relationship('Appointment', backref = 'doctor', lazy = True)
    
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False, unique = True)
    name = db.Column(db.String, nullable = False)
    profile = db.Column(db.Text)
    appointments = db.relationship('Appointment', backref = 'patient', lazy = True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date, nullable = False)
    time = db.Column(db.Time, nullable = False)
    status = db.Column(db.String(), nullable = False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable = False)
    treatment = db.relationship('Treatment',backref = 'appointment', uselist = False, cascade = "all")
    
class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"),nullable = False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    

class Department(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    doctors = db.relationship('Doctor', backref='department', lazy=True)
    