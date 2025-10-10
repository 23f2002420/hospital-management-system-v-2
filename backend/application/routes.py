from flask import request, jsonify
from app import app
from .models import db, User, Patient, Department, Doctor, Appointment, Treatment
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from functools import wraps
from datetime import datetime


# --- DECORATORS  ---
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != "admin":
                return jsonify(message="Access denied: Admin privileges required"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def doctor_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != 'doctor':
                return jsonify(message="Access denied: Doctor privileges required"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def patient_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != "patient":
                return jsonify(message="Access denied: Patient privileges required"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


# # --- AUTHENTICATION ---
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify(message="Username and password are required"), 400
    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password): 
        return jsonify(message="Wrong username or password"), 401
    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    return jsonify(access_token=access_token, role = user.role)

@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    name = request.json.get("name", None)
    if not username or not password or not name:
        return jsonify(message="Username, password, and name are required"), 400
    if User.query.filter_by(username=username).first():
        return jsonify(message="User already exists"), 409
    new_user = User(username=username, role="patient")
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    new_patient = Patient(user_id=new_user.id, name=name)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify(message="Patient registered successfully"), 201

@app.route('/api/doctors', methods=['GET'])
@jwt_required()
def get_doctors():
    doctors = Doctor.query.all()
    doctor_list = [{'id': doc.id, 'name': doc.name, 'specialization': doc.specialization, 'department': doc.department.name, 'availability': doc.availability} for doc in doctors]
    return jsonify(doctor_list), 200

@app.route('/api/departments',methods = ['GET'])
@jwt_required()
def get_all_departments():
    departments = Department.query.all()
    dept_list = [{"id": d.id, "name": d.name, "description": d.description} for d in departments]
    return jsonify(dept_list), 200


@app.route('/api/doctors/<int:doctor_id>/schedule', methods = ['GET'])
@jwt_required()
def get_doctor_schedule(doctor_id):
    appointments = Appointment.query.filter_by(doctor_id = doctor_id).all()
    
    booked_slots = [
        {'date': appt.date.strftime('%Y-%m-%d'), 'time': appt.time.strftime('%H:%M:%S')}
        for appt in appointments
    ]
    return jsonify(booked_slots),200


# --admin routes ---
@app.route('/api/admin/dashboard', methods=['GET'])
@admin_required()
def admin_dashboard_stats():
    stats = {
        'total_doctors': Doctor.query.count(),
        'total_patients': Patient.query.count(),
        'total_appointments': Appointment.query.count()
    }
    return jsonify(stats), 200

@app.route('/api/admin/departments', methods=['POST'])
@admin_required()
def create_department():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify(message="Department name is required"), 400
    if Department.query.filter_by(name=data['name']).first(): 
        return jsonify(message="Department already exists"), 409
    new_dept = Department(name=data['name'], description=data.get('description', ''))
    db.session.add(new_dept)
    db.session.commit()
    return jsonify(message=f"Department '{new_dept.name}' created successfully"), 201

@app.route('/api/admin/doctors', methods=['POST'])
@admin_required()
def create_doctor():
    data = request.get_json()
    required_fields = ["username", "password", "name", "specialization", "department_id"]
    if not all (field in data for field in required_fields):
        return jsonify(message="Missing required fields for doctor creation"), 400
    if User.query.filter_by(username=data['username']).first(): 
        return jsonify(message="Username already exists"), 409
    if not Department.query.get(data['department_id']):
        return jsonify(message="Department not found"), 404
    new_user = User(username=data['username'], role='doctor')
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    new_doctor = Doctor(user_id=new_user.id, name=data['name'], specialization=data['specialization'], department_id=data['department_id'])
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify(message=f"Doctor '{new_doctor.name}' created successfully"), 201

@app.route('/api/admin/doctors', methods=['GET'])
@admin_required()
def get_all_doctors():
    doctors = Doctor.query.all()
    doctor_list = [{'id': doc.id, 'user_id': doc.user_id, 'name': doc.name, 'specialization': doc.specialization, 'department': doc.department.name} for doc in doctors]
    return jsonify(doctor_list), 200

@app.route('/api/admin/patients', methods=['GET'])
@admin_required()
def get_all_patients():
    patients = Patient.query.all()
    patient_list = [{'id': pat.id, 'user_id': pat.user_id, 'name': pat.name, 'profile': pat.profile} for pat in patients]
    return jsonify(patient_list), 200

@app.route('/api/admin/appointments', methods=['GET'])
@admin_required()
def get_all_appointments():
    query = Appointment.query
    status_filter = request.args.get('status', None)
    doctor_id_filter = request.args.get('doctor_id', None)
    if status_filter:
        query = query.filter(Appointment.status == status_filter)
    if doctor_id_filter:
        query = query.filter(Appointment.doctor_id == doctor_id_filter)
    appointments = query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    appointment_list = [{'id': appt.id, 'patient_name': appt.patient.name, 'doctor_name': appt.doctor.name, 'department': appt.doctor.department.name, 'date': appt.date.strftime('%Y-%m-%d'), 'time': appt.time.strftime('%H:%M'), 'status': appt.status} for appt in appointments]
    return jsonify(appointment_list), 200

@app.route('/api/admin/search', methods=['GET'])
@admin_required()
def search_users():
    query_str = request.args.get('query', '')
    role_filter = request.args.get('role', 'patient')
    if not query_str: 
        return jsonify(message="A search query is required"), 400
    results = []
    if role_filter == 'patient':
        patients = Patient.query.filter(Patient.name.ilike(f'%{query_str}%')).all()
        results = [{"id": p.id, "name": p.name, "user_id": p.user_id, "role": "patient"} for p in patients]
    elif role_filter == 'doctor':
        doctors = Doctor.query.filter(Doctor.name.ilike(f'%{query_str}%')).all()
        results = [{"id": d.id, "name": d.name, "specialization": d.specialization, "role": "doctor"} for d in doctors]
    else:
        return jsonify(message="Invalid role specified. Use 'patient' or 'doctor'."), 400
    return jsonify(results), 200

@app.route('/api/admin/doctors/<int:doctor_id>', methods=['PUT'])
@admin_required()
def update_doctor_profile(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify(message="Doctor not found"), 404
    data = request.get_json()
    if 'name' in data: 
        doctor.name = data['name']
    if 'specialization' in data: 
        doctor.specialization = data['specialization']
    if 'department_id' in data:
        if not Department.query.get(data['department_id']): 
            return jsonify(message="Department not found"), 404
        doctor.department_id = data['department_id']
    db.session.commit()
    return jsonify(message=f"Doctor {doctor.name}'s profile has been updated."), 200

@app.route('/api/admin/patients/<int:patient_id>', methods=['PUT'])
@admin_required()
def update_patient_profile(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify(message="Patient not found"), 404
    data = request.get_json()
    if 'name' in data: 
        patient.name = data['name']
    if 'profile' in data:
        patient.profile = data['profile']
    db.session.commit()
    return jsonify(message=f"Patient {patient.name}'s profile has been updated."), 200

@app.route('/api/admin/doctors/<int:doctor_id>', methods=['DELETE'])
@admin_required()
def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify(message="Doctor not found"), 404
    user = User.query.get(doctor.user_id)
    db.session.delete(doctor)
    if user:
        db.session.delete(user)
    db.session.commit()
    return jsonify(message="Doctor profile and user account have been deleted."), 200

@app.route('/api/admin/patients/<int:patient_id>', methods=['DELETE'])
@admin_required()
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify(message="Patient not found"), 404
    user = User.query.get(patient.user_id)
    db.session.delete(patient)
    if user: 
        db.session.delete(user)
    db.session.commit()
    return jsonify(message="Patient profile and user account have been deleted."), 200

# # --- doctor routes---
@app.route('/api/doctor/appointments', methods=['GET'])
@doctor_required()
def get_doctor_appointments():
    current_user_id = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(user_id=current_user_id).first()
    if not doctor:
        return jsonify(message="Doctor profile not found"), 404
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.date, Appointment.time).all()
    appointment_list = [{'id': appt.id, 'patient_name': appt.patient.name, 'date': appt.date.strftime('%Y-%m-%d'), 'time': appt.time.strftime('%H:%M'), 'status': appt.status} for appt in appointments]
    return jsonify(appointment_list), 200

@app.route('/api/doctor/profile', methods = ['GET'])
@doctor_required()
def get_doctor_profile():
    current_user_id = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(user_id = current_user_id).first()
    if not doctor:
        return jsonify(message = "Doctor profile not found"),404
    return jsonify({
        "id": doctor.id,
        "name":doctor.name,
        "specialization": doctor.specialization,
        "availability": doctor.availability
    }),200
    
    
@app.route('/api/doctor/appointment/<int:appointment_id>', methods = ['GET'])
@doctor_required()
def get_doctor_appointment_details(appointment_id):
    appt = Appointment.query.get(appointment_id)
    if not appt:
        return jsonify(message = "Appointment not found"),404
    
    current_user_id =int(get_jwt_identity())
    doctor = Doctor.query.filter_by(user_id= current_user_id).first()
    if appt.doctor_id!= doctor.id:
        return jsonify(message = "Unauthorized"),403
    
    appt_data = {
        "id": appt.id,
        "patient_name": appt.patient.name,
        "date": appt.date.strftime('%Y-%m-%d'),
        "time": appt.time.strftime('%H:%M'),
        "status": appt.status,
        "treatment": None,
    }    
    if appt.treatment:
        appt_data['treatment'] = {
            "diagnosis": appt.treatment.diagnosis,
            "prescription": appt.treatment.prescription,
            "notes": appt.treatment.notes
        }
    return jsonify(appt_data),200


@app.route('/api/appointments/<int:appointment_id>/complete', methods=['PUT'])
@doctor_required()
def complete_appointment(appointment_id):
    data = request.get_json()
    diagnosis = data.get('diagnosis')
    prescription = data.get('prescription')
    if not diagnosis or not prescription:
        return jsonify(message="Diagnosis and prescription are required"), 400
    appointment = Appointment.query.get(appointment_id)
    if not appointment: 
        return jsonify(message="Appointment not found"), 404
    current_user_id = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(user_id=current_user_id).first()
    if appointment.doctor_id != doctor.id:
        return jsonify(message="You are not authorized to modify this appointment"), 403
    appointment.status = 'Completed'
    new_treatment = Treatment(appointment_id=appointment.id, diagnosis=diagnosis, prescription=prescription, notes=data.get('notes', ''))
    db.session.add(new_treatment)
    db.session.commit()
    return jsonify(message="Appointment marked as completed and treatment recorded."), 200

@app.route('/api/patients/<int:patient_id>/history', methods=['GET'])
@doctor_required()
def get_patient_history(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify(message="Patient not found"), 404
    appointments = Appointment.query.filter_by(patient_id=patient.id, status='Completed').order_by(Appointment.date.desc()).all()
    history_list = []
    for appt in appointments:
        if appt.treatment: 
            history_list.append({'appointment_id': appt.id,
                                'doctor_name': appt.doctor.name,
                                'date': appt.date.strftime('%Y-%m-%d'), 
                                'diagnosis': appt.treatment.diagnosis,
                                'prescription': appt.treatment.prescription})
    return jsonify(history_list), 200

@app.route('/api/doctor/availability', methods=['PUT'])
@doctor_required()
def set_doctor_availability():
    current_user_id = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(user_id=current_user_id).first()
    if not doctor:
        return jsonify(message="Doctor profile not found"), 404
    data = request.get_json()
    if 'availability' not in data:
        return jsonify(message="Availability data is required"), 400
    doctor.availability = data['availability']
    db.session.commit()

    return jsonify(message="Your availability has been updated successfully."), 200

# # --- Patient Routes ----
@app.route('/api/appointments', methods=['POST'])
@patient_required()
def book_appointment():
    data = request.get_json()
    doctor_id = data.get('doctor_id')
    date_str = data.get('date')
    time_str = data.get('time')
    if not all([doctor_id, date_str, time_str]):
        return jsonify(message="Doctor ID, date, and time are required"), 400
    try:
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        appointment_time = datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        return jsonify(message="Invalid date or time format. Use YYYY-MM-DD and HH:MM"), 400

    existing_appointment = Appointment.query.filter_by(
        doctor_id=doctor_id,
        date=appointment_date,
        time=appointment_time
    ).first()
    
    if existing_appointment:
        return jsonify(message="This time slot is unavailable. Please choose another time."), 409

    current_user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=current_user_id).first()
    if not patient:
        return jsonify(message="Patient profile not found for this user."), 404

    new_appointment = Appointment(
        doctor_id=doctor_id, 
        patient_id=patient.id,
        date=appointment_date,
        time=appointment_time,
        status='Booked'
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify(message="Appointment booked successfully"), 201


@app.route('/api/patient/appointments', methods=['GET'])
@patient_required()
def get_patient_appointments():
    current_user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=current_user_id).first()
    if not patient:
        return jsonify(message="Patient profile not found"), 404
    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.date.desc()).all()
    appointment_list = []
    for appt in appointments:
        appt_data = {'id': appt.id, 'doctor_name': appt.doctor.name, 'department': appt.doctor.department.name, 'date': appt.date.strftime('%Y-%m-%d'), 'time': appt.time.strftime('%H:%M:%S'), 'status': appt.status, 'treatment': None}
        if appt.treatment: 
            appt_data['treatment'] = {'diagnosis': appt.treatment.diagnosis, 'prescription': appt.treatment.prescription, 'notes': appt.treatment.notes}
        appointment_list.append(appt_data)
    return jsonify(appointment_list), 200



@app.route('/api/appointments/<int:appointment_id>', methods=['GET'])
@patient_required()
def get_appointment_details(appointment_id):
    appt = Appointment.query.get(appointment_id)
    if not appt:
        return jsonify(message="Appointment not found"), 404
    
    current_user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=current_user_id).first()
    if appt.patient_id != patient.id:
        return jsonify(message="Unauthorized"), 403
        
    return jsonify({
        "id": appt.id,
        "doctor_id": appt.doctor.id,
        "doctor_name": appt.doctor.name,
        "date": appt.date.strftime('%Y-%m-%d'),
        "time": appt.time.strftime('%H:%M'),
        "status": appt.status
    }), 200




@app.route('/api/appointments/<int:appointment_id>/cancel', methods=['PUT'])
@patient_required()
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify(message="Appointment not found"), 404
    current_user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=current_user_id).first()
    if appointment.patient_id != patient.id:
        return jsonify(message="You are not authorized to cancel this appointment"), 403
    if appointment.status != "Booked": 
        return jsonify(message=f"Cannot cancel an appointment with status '{appointment.status}'"), 400
    appointment.status = 'Cancelled'
    db.session.commit()
    return jsonify(message="Appointment has been successfully cancelled."), 200

@app.route('/api/appointments/<int:appointment_id>/reschedule', methods=['PUT'])
@patient_required()
def reschedule_appointment(appointment_id):
    data = request.get_json()
    new_date_str = data.get('new_date')
    new_time_str = data.get('new_time')
    if not new_date_str or not new_time_str:
        return jsonify(message="New date and time are required"), 400
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify(message="Appointment not found"), 404
    current_user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=current_user_id).first()
    if appointment.patient_id != patient.id: 
        return jsonify(message="You are not authorized to reschedule this appointment"), 403
    if appointment.status != 'Booked':
        return jsonify(message=f"Cannot reschedule an appointment with status '{appointment.status}'"), 400
    try:
        new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
        new_time = datetime.strptime(new_time_str, '%H:%M').time()
    except ValueError:
        return jsonify(message="Invalid date or time format"), 400
    if Appointment.query.filter_by(doctor_id=appointment.doctor_id, date=new_date, time=new_time).first():
        return jsonify(message="This time slot is unavailable. Please choose another time."), 409
    appointment.date = new_date
    appointment.time = new_time
    db.session.commit()
    return jsonify(message="Appointment has been successfully rescheduled."), 200


@app.route('/api/patient/profile',methods =['GET'])
@patient_required()
def get_own_profile():
    current_user_id= int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id = current_user_id).first()
    if not patient:
        return jsonify(message = "Patient profile not found"),404
    
    profile_data = {
        "id": patient.id,
        "name": patient.name,
        "profile": patient.profile
    }
    return jsonify(profile_data),200


@app.route('/api/patient/profile', methods = ['PUT'])
@patient_required()
def update_own_profile():
    current_user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id = current_user_id).first()
    if not patient:
        return jsonify(message = "Patient profile not found"),404
    data = request.get_json()
    if 'name' in data:
        patient.name = data['name']
    if 'profile' in data:
        patient.profile = data['profile']    
    db.session.commit()
    return jsonify(message = "Your profile has been updated successfully."),200

