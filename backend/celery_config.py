from celery.schedules import crontab

broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"
Timezone = "Asia/kolkata"
broker_connection_retry_on_startup = True


beat_schedule = {
    'send-monthly-reports': {
        'task': 'monthly_doctor_report', # Name of the task from tasks.py
        'schedule': crontab(day_of_month=1, hour=6, minute=0), # Runs 1st day of month at 6:00 AM
    },
    'send-daily-reminders-at-8am': {
        'task': 'send_daily_reminders', # Name of the task from tasks.py
        'schedule': crontab(hour=8, minute=0),  # Runs daily at 8:00 AM
    },  
}