from celery import shared_task
from jinja2 import Template 
import requests
import csv 
import io 
from datetime import date, timedelta
from .mail import send_email
from .models import db,User, Appointment , Doctor, Patient , Treatment



# task-1 -> Download patient Treatments as CSV  for user .
# User triggered async job 
@shared_task(ignore_results = False, name = "export_treatments_csv")
def export_treatments_csv(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        print(f"Patient with ID {patient_id} not found.")
        return "Patient not found"
    appointments = Appointment.query.filter_by(
        patient_id = patient_id,
        status = 'Completed'
    ).order_by(Appointment.date.desc()).all()
    
    if not appointments:
        return "No treatment history found."

    # Create CSV 
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write Header Row 
    header = ['Appointment ID', 'Date', 'Doctor','Specialization','Diagnosis','Prescription','Notes']
    writer.writerow(header)
    
    for appt in appointments:
        if appt.treatment:
            row = [
                appt.id,
                appt.date.strftime('%Y-%m-%d'),
                appt.doctor.name,
                appt.doctor.specialization,
                appt.treatment.diagnosis,
                appt.treatment.prescription,
                appt.treatment.notes
            ]
            writer.writerow(row)
            
    csv_data = output.getvalue()
    output.close()
    
    csv_filename = f"patient_{patient_id}_treatment_history_{date.today().strftime('%Y%m%d')}.csv"
    try:
        user_email = patient.user.username
        send_email(
            to_address = user_email,
            subject = "Your Treatment History export",
            message = f"Dear{patient.name}, \n\n Please find treatment history attached as a CSV file. \n\nRegrads,\n Hospital Management System ",
            content = "plain",
            attachment_file_content = csv_data,
            attachment_filename = csv_filename
        )
        return f"CSV export successfully for patient {patient_id}."
    except Exception as e:
        print(f"EMAIL SENDING FAILED for patient ID {patient_id}: {e}")
        return f"CSV export failed for patient {patient_id} due to email error."

# task-2 > Monthly Activity Report for Doctor  
# schedule job via crontab 
@shared_task(ignore_results = False, name= "monthly_doctor_report")
def monthly_doctor_report():
    today = date.today()
    last_day_of_prev_month = today.replace(day=1)-timedelta(days=1)
    first_day_of_prev_month = last_day_of_prev_month.replace(day=1)
    month_name = first_day_of_prev_month.strftime("%B %Y")
    
    print(f"Generating monthly reports for {month_name}")
    doctors = Doctor.query.all()
    for doctor in doctors:
        appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.status == 'Completed',
            Appointment.date.between(first_day_of_prev_month,last_day_of_prev_month)
        ).order_by(Appointment.date).all()
        
        if not appointments:
            continue 
        report_data = {
            "doctor_name": doctor.name,
            "month_name":month_name,
            'total_appointments':len(appointments),
            'appointments':[
                {
                    'date':appt.date.strftime('%Y-%m-%d'),
                    'patient_name': appt.patient.name,
                    'diagnosis': appt.treatment.diagnosis if appt.treatment else 'N/A',
                    'prescription': appt.treatment.prescription if appt.treatment else 'N/A'
                }for appt in appointments
            ]
        }
        
        # HTML Email Template 
        mail_template_str = """
        <html><body>
        <h3>Monthly Activity Report for Dr. {{ report_data.doctor_name }} - {{ report_data.month_name }}</h3>
        <p>This report summarizes your activity for the past month.</p>
        <p><strong>Total Completed Appointments:</strong> {{ report_data.total_appointments }}</p>
        <hr>
        <h4>Appointment Details:</h4>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th>Date</th>
                    <th>Patient Name</th>
                    <th>Diagnosis</th>
                    <th>Prescription</th>
                </tr>
            </thead>
            <tbody>
                {% for appt in report_data.appointments %}
                <tr>
                    <td>{{ appt.date }}</td>
                    <td>{{ appt.patient_name }}</td>
                    <td>{{ appt.diagnosis }}</td>
                    <td>{{ appt.prescription }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <br>
        <p>Regards,<br>Hospital Management System</p>
        </body></html>
        """
        message_html = Template(mail_template_str).render(report_data=report_data)
        try:
            user_email = doctor.user.username
            send_email(
                to_address=user_email,
                subject=f"Your Monthly Report - {month_name}",
                message=message_html,
                content="html"
            )
            print(f"Sent monthly report to Dr. {doctor.name}.")
        except Exception as e:
            print(f"Failed to send monthly report to Dr. {doctor.name}: {e}")

    return f"Monthly reports generation complete for {month_name}."   
        

# ---Task-3 > Daily Appintment Reminders ---
@shared_task(ignore_results=False, name = "send_daily_reminders")
def send_daily_reminders():
    today = date.today()
    print(f"Checking for appointment on {today}")
    
    appointments_today = Appointment.query.filter(
        Appointment.date == today,
        Appointment.status == 'Booked'
    ).all()
    
    if not appointments_today:
        print(f"No reminders to send today.")
        return "No reminders sent."
    
    print(f"Found {len(appointments_today)} appointments.Sending reminders...")
    for appt in appointments_today:
        patient_name = appt.patient.name
        doctor_name = appt.doctor.name
        appt_time_str = appt.time.strftime('%I:%M %p')
        
        try:
            reminder_subject = f"Appintment Reminder: {today.strftime('%B %d,%Y')} at {appt_time_str}"
            reminder_message = (
                f"Dear {patient_name},\n\n"
                f"This is a reminder for your upcoming appointment with Dr.{doctor_name}"
                f"today, {today.strftime('%B %d')}, at {appt_time_str}. \n\n"
                f"Please arrive a few minutes early.\n\n"
                f"Regards, \n Hospital Management System"
            )
            
            user_email = appt.patient.user.username 
            send_email(
                to_address = user_email,
                subject= reminder_subject,
                message = reminder_message,
                content = 'plain'
            )
            print(f"Sent email reminder for appointment ID{appt.id} to {user_email}.")
        except Exception as e:
            print(f"Failed to send email reminder for appointment ID {appt.id}:{e}")
            
    return f"Processed {len(appointments_today)} reminders."